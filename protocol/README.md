# 开放交易协议草案

当前协议版本为 `agri-market/0.1`，用于概念验证和一致性测试，不用于生产交易。

## 对象

| 对象 | 作用 |
|---|---|
| `VillageNode` | 描述村级节点、区域、运营主体和接口 |
| `Farmer` | 描述农户公开身份及核验状态 |
| `ProductBatch` | 描述一批实际农产品 |
| `Evidence` | 描述一项可验证但可被质疑的声明 |
| `Offer` | 描述批次当前交易条件 |
| `Intent` | 描述消费者可撤销需求 |
| `RecommendationReceipt` | 描述候选、过滤、排序和商业关系 |
| `OrderEvent` | 描述订单状态变化 |

## 兼容原则

- 业务主键不得使用某个软件供应商私有账号；
- 未知字段应被保留或安全忽略，不得导致历史数据丢失；
- 状态变化只追加事件，不覆盖旧事件；
- 公开对象不得包含身份证、银行卡和完整收货地址；
- 签名证明提交主体，不替代现场事实核验；
- 协议扩展使用命名空间，不能重新定义核心字段含义。

## 文件

- [JSON Schema](schemas/agri-protocol.schema.json)
- [完整交易样例](examples/complete-transaction.json)

## 验证

在仓库根目录运行：

```bash
python scripts/validate.py
```
