# GitHub公开发布检查表

仓库地址：<https://github.com/sqzy0026-droid/ai-native-agri-network-whitepaper>

## 发布前

- [x] 使用仓库级GitHub身份提交，不修改机器全局身份；
- [x] 本地验证脚本通过；
- [x] 未发现账号密钥、真实联系方式、证件、地址或支付数据；
- [x] 样例数据使用保留示例域名和虚构标识；
- [x] 已明确双授权及第三方内容排除项；
- [x] GitHub Actions校验工作流通过；
- [ ] 将仓库可见性从Private改为Public；
- [ ] 以未登录访问验证README、LICENSE和Actions页面。

## 发布后的持续要求

每次提交前运行：

```bash
python scripts/validate.py
```

不得提交真实农户、消费者、村级节点或合作机构的身份证明、完整联系方式、收货地址、银行卡、支付凭据、未脱敏订单和内部政务材料。

新增第三方代码、图片或长篇文字前，应记录来源和许可证；仅有公开链接而没有许可证，不代表可以复制、修改或重新授权。
