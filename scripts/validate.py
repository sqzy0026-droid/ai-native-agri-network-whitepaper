from __future__ import annotations

import json
import re
import sys
from datetime import date, datetime
from pathlib import Path
from urllib.parse import unquote
from urllib.parse import urlparse

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:
    Draft202012Validator = None
    FormatChecker = None


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "protocol" / "schemas" / "agri-protocol.schema.json"
EXAMPLE_PATH = ROOT / "protocol" / "examples" / "complete-transaction.json"
WHITEPAPER_PATH = ROOT / "WHITEPAPER.md"


def _matches_type(value: object, expected: str) -> bool:
    checks = {
        "object": lambda x: isinstance(x, dict),
        "array": lambda x: isinstance(x, list),
        "string": lambda x: isinstance(x, str),
        "number": lambda x: isinstance(x, (int, float)) and not isinstance(x, bool),
        "integer": lambda x: isinstance(x, int) and not isinstance(x, bool),
        "boolean": lambda x: isinstance(x, bool),
        "null": lambda x: x is None,
    }
    return checks[expected](value)


def _validate_format(value: str, fmt: str) -> bool:
    try:
        if fmt == "date":
            date.fromisoformat(value)
        elif fmt == "date-time":
            datetime.fromisoformat(value.replace("Z", "+00:00"))
        elif fmt == "uri":
            parsed = urlparse(value)
            return bool(parsed.scheme and parsed.netloc)
    except ValueError:
        return False
    return True


def offline_validate(schema: dict, value: object, path: str = "$") -> list[str]:
    """Validate the JSON Schema subset used by this repository without dependencies."""
    errors: list[str] = []
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: expected const {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: value {value!r} is not in enum")

    expected = schema.get("type")
    if expected:
        types = expected if isinstance(expected, list) else [expected]
        if not any(_matches_type(value, item) for item in types):
            errors.append(f"{path}: expected type {types}, got {type(value).__name__}")
            return errors

    if isinstance(value, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                errors.append(f"{path}: missing required property {key}")
        properties = schema.get("properties", {})
        for key, item in value.items():
            if key in properties:
                errors.extend(offline_validate(properties[key], item, f"{path}.{key}"))
            elif schema.get("additionalProperties") is False:
                errors.append(f"{path}: unexpected property {key}")
            elif isinstance(schema.get("additionalProperties"), dict):
                errors.extend(offline_validate(schema["additionalProperties"], item, f"{path}.{key}"))

    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: too few items")
        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(value):
                errors.extend(offline_validate(item_schema, item, f"{path}[{index}]"))
        if schema.get("uniqueItems"):
            encoded = [json.dumps(item, ensure_ascii=False, sort_keys=True) for item in value]
            if len(encoded) != len(set(encoded)):
                errors.append(f"{path}: array items are not unique")

    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path}: string is too short")
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            errors.append(f"{path}: string is too long")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append(f"{path}: string does not match pattern")
        if "format" in schema and not _validate_format(value, schema["format"]):
            errors.append(f"{path}: invalid {schema['format']}")

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: value is below minimum")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{path}: value is above maximum")
        if "exclusiveMinimum" in schema and value <= schema["exclusiveMinimum"]:
            errors.append(f"{path}: value must be greater than exclusive minimum")
    return errors


def validate_schema_and_examples() -> list[str]:
    errors: list[str] = []
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    example = json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))
    defs = schema["$defs"]
    use_standard_validator = Draft202012Validator is not None
    if use_standard_validator:
        Draft202012Validator.check_schema(schema)
        checker = FormatChecker()

    for name in ("VillageNode", "Farmer", "ProductBatch", "Evidence", "Offer", "Intent", "RecommendationReceipt"):
        if use_standard_validator:
            validator = Draft202012Validator(defs[name], format_checker=checker)
            for issue in sorted(validator.iter_errors(example[name]), key=lambda e: list(e.path)):
                path = ".".join(str(part) for part in issue.path)
                errors.append(f"{name}.{path}: {issue.message}")
        else:
            errors.extend(offline_validate(defs[name], example[name], name))

    events = example["OrderEvents"]
    if use_standard_validator:
        event_validator = Draft202012Validator(defs["OrderEvent"], format_checker=checker)
        for index, event in enumerate(events):
            for issue in sorted(event_validator.iter_errors(event), key=lambda e: list(e.path)):
                path = ".".join(str(part) for part in issue.path)
                errors.append(f"OrderEvents[{index}].{path}: {issue.message}")
    else:
        for index, event in enumerate(events):
            errors.extend(offline_validate(defs["OrderEvent"], event, f"OrderEvents[{index}]"))

    sequences = [event["sequence"] for event in events]
    if sequences != list(range(1, len(events) + 1)):
        errors.append(f"订单事件序号不连续: {sequences}")

    if len({event["event_id"] for event in events}) != len(events):
        errors.append("订单事件ID存在重复")
    if len({event["idempotency_key"] for event in events}) != len(events):
        errors.append("订单事件幂等键存在重复")

    allowed = {
        "PROPOSED": {"ACCEPTED", "CANCELLED"},
        "ACCEPTED": {"PAYMENT_PENDING", "PAID", "CANCELLED"},
        "PAYMENT_PENDING": {"PAID", "CANCELLED"},
        "PAID": {"COLLECTED", "SHIPPED", "REFUND_PENDING"},
        "COLLECTED": {"SHIPPED", "REFUND_PENDING"},
        "SHIPPED": {"DELIVERED", "DISPUTED"},
        "DELIVERED": {"COMPLETED", "DISPUTED"},
        "DISPUTED": {"REFUND_PENDING", "RESOLVED"},
        "REFUND_PENDING": {"REFUNDED", "RESOLVED"},
        "REFUNDED": {"RESOLVED"},
        "COMPLETED": set(),
        "RESOLVED": set(),
        "CANCELLED": set(),
    }
    for previous, current in zip(events, events[1:]):
        if current["event_type"] not in allowed[previous["event_type"]]:
            errors.append(f"非法状态迁移: {previous['event_type']} -> {current['event_type']}")

    return errors


def validate_markdown_links() -> list[str]:
    errors: list[str] = []
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for markdown in ROOT.rglob("*.md"):
        content = markdown.read_text(encoding="utf-8")
        for target in pattern.findall(content):
            target = target.strip().split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (markdown.parent / unquote(target)).resolve()
            if not resolved.exists():
                errors.append(f"失效链接: {markdown.relative_to(ROOT)} -> {target}")
    return errors


def validate_whitepaper() -> list[str]:
    errors: list[str] = []
    content = WHITEPAPER_PATH.read_text(encoding="utf-8")
    required = [
        "# 执行摘要",
        "# 第四章 技术主线：农业Agent Harness",
        "# 第五章 开放交易协议",
        "# 第十二章 90天试点",
        "# 第十三章 科学验证与停止条件",
    ]
    for heading in required:
        if heading not in content:
            errors.append(f"白皮书缺少章节: {heading}")
    forbidden = ["codex-file-citation", "PLACEHOLDER", "TODO"]
    for token in forbidden:
        if token in content:
            errors.append(f"白皮书含有未清理标记: {token}")
    return errors


def main() -> int:
    errors = validate_schema_and_examples() + validate_markdown_links() + validate_whitepaper()
    if errors:
        print("验证失败：")
        for error in errors:
            print(f"- {error}")
        return 1
    validator_name = "jsonschema" if Draft202012Validator is not None else "离线标准库后备校验器"
    print(f"验证通过：Schema、协议样例、订单事件、Markdown链接和白皮书章节均正常（{validator_name}）。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
