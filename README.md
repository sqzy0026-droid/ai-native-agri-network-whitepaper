# AI原生开放助农网络

这是一个面向小农户、村级助农节点和消费者AI代理的开放交易基础设施实验。

项目不以建设新的全国农产品商城为目标，而是验证一件更小、也更困难的事情：

> 一个小农户能否通过村级可信节点，在不购买中心平台流量、不交出数据主权的情况下，被消费者AI发现，并完成一次真实、可追溯、可售后的交易。

## 当前状态

项目处于协议与原型设计阶段，尚未进入生产运营。本仓库首先交付白皮书、架构、协议草案、样例数据和验证工具，不包含真实农户、消费者、支付或食品安全数据。

## 核心判断

```text
农业交易 Agent = 可替换模型 + Agri Harness + 开放交易协议
```

- 模型负责理解、推理和生成建议；
- Agri Harness负责工具、权限、审批、会话、恢复、审计和插件；
- 开放交易协议负责身份、批次、要约、订单、履约、证据和争议；
- 村级节点负责现实世界的连接、核验、集货与售后协助；
- 支付、物流、检测和仲裁由可替换的合规服务商承担。

## 文档导航

- [白皮书](WHITEPAPER.md)
- [Agri Harness技术架构](architecture/AGRI_HARNESS_ARCHITECTURE.md)
- [威胁模型](architecture/THREAT_MODEL.md)
- [协议草案](protocol/README.md)
- [JSON Schema](protocol/schemas/agri-protocol.schema.json)
- [样例交易](protocol/examples/complete-transaction.json)
- [90天试点计划](pilot/90_DAY_PILOT.md)
- [许可证建议](governance/LICENSE_PROPOSAL.md)
- [GitHub发布步骤](PUBLISHING.md)

## 快速验证

需要Python 3.10或以上版本。

```bash
python scripts/validate.py
```

验证内容包括：

- JSON Schema自身结构；
- 协议样例的字段和类型；
- 订单事件顺序；
- Markdown相对链接；
- 白皮书必需章节。

## 构建白皮书

如果本机已安装Pandoc，可生成HTML；如果同时安装XeLaTeX和中文字体，可生成PDF。

```bash
bash scripts/build.sh
```

Windows PowerShell：

```powershell
./scripts/build.ps1
```

## 设计底线

- 可以有中心，但不能只有一个不可替代的中心；
- 可以集中部署，但身份、数据、规则和退出权不能集中设计；
- 村级节点核验真实性，不掌握全国流量；
- AI可以建议和调用工具，不能绕过权限与人工确认；
- 数字签名证明谁提交了证据，不证明现实陈述天然真实；
- 农户收益、消费者复购和退出演练同时通过，才允许扩大试点。

## 许可证状态

本仓库当前为公开评审草案，尚未正式授予开源许可证。建议的分层许可方案见[许可证建议](governance/LICENSE_PROPOSAL.md)。在权利人明确确认前，不接收外部代码贡献，也不宣称本仓库已经开源。

## 免责声明

本项目不构成法律、食品安全、支付、投资或经营许可意见。进入真实交易试点前，应由具备相应资质的专业人员完成合规审查。
