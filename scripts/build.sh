#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE="$ROOT_DIR/WHITEPAPER.md"
OUTPUT_DIR="$ROOT_DIR/dist"

command -v pandoc >/dev/null 2>&1 || {
  echo "未找到pandoc，无法构建。"
  exit 2
}

mkdir -p "$OUTPUT_DIR"
pandoc "$SOURCE" --standalone --toc --metadata title="AI原生开放助农网络白皮书" -o "$OUTPUT_DIR/AI原生开放助农网络白皮书.html"

if command -v xelatex >/dev/null 2>&1; then
  pandoc "$SOURCE" --toc --pdf-engine=xelatex -V documentclass=ctexbook -V classoption=oneside -o "$OUTPUT_DIR/AI原生开放助农网络白皮书.pdf"
else
  echo "未找到xelatex，已跳过PDF，仅生成HTML。"
fi

echo "构建完成：$OUTPUT_DIR"
