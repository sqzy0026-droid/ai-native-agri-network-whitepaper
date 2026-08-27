# GitHub发布步骤

本目录已经初始化为`main`分支的本地Git仓库，但当前机器尚未登录GitHub，也没有配置Git提交者姓名和邮箱，因此自动发布在提交前停止。

## 1. 确认许可证

先阅读[许可证建议](governance/LICENSE_PROPOSAL.md)，由权利人明确著作权主体和各类内容的许可证。确认后再增加正式`LICENSE`文件。

## 2. 配置提交身份

在本仓库中配置真实姓名和邮箱，不建议为了通过命令而填写虚假身份。

```bash
git config user.name "你的姓名或组织名称"
git config user.email "你的GitHub邮箱"
```

## 3. 本地验证与提交

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate.py
git add .
git commit -m "Initial public whitepaper draft"
```

## 4. 登录GitHub

```bash
gh auth login
```

## 5. 创建远程仓库并推送

建议仓库名：`ai-native-agri-network-whitepaper`。

正式开放许可尚未确认前，建议先创建私有仓库进行内部审阅：

```bash
gh repo create ai-native-agri-network-whitepaper --private --source . --remote origin --push
```

完成许可证和公开发布审核后，再将仓库改为公开。不要把真实农户、消费者、支付、身份证明和收货地址提交到公开仓库。
