# 设置指南

## 🎉 仓库已创建成功！

仓库地址：https://github.com/phaip88/webhost_keepalive_simple

## 📋 下一步操作

### 1. 配置 GitHub Secrets

进入仓库设置页面配置敏感信息：

1. 访问：https://github.com/phaip88/webhost_keepalive_simple/settings/secrets/actions

2. 点击 `New repository secret` 添加以下配置：

#### 必需配置

**SITE_ACCOUNTS**
- Name: `SITE_ACCOUNTS`
- Secret: 你的账号信息

格式示例：
```
单账号：
user@example.com,password

多账号（用分号分隔）：
user1@example.com,pass1;user2@example.com,pass2;user3@example.com,pass3
```

#### 可选配置（Telegram 通知）

**TELEGRAM_BOT_TOKEN**
- Name: `TELEGRAM_BOT_TOKEN`
- Secret: 你的 Telegram Bot Token

如何获取：
1. 在 Telegram 搜索 @BotFather
2. 发送 `/newbot` 创建机器人
3. 按提示设置机器人名称
4. 获取 Token（格式：`123456789:ABCdefGHIjklMNOpqrsTUVwxyz`）

**TELEGRAM_CHAT_ID**
- Name: `TELEGRAM_CHAT_ID`
- Secret: 你的 Telegram Chat ID

如何获取：
1. 在 Telegram 搜索 @userinfobot
2. 发送任意消息
3. 获取你的 ID（纯数字，如：`123456789`）

### 2. 启用 GitHub Actions

1. 访问：https://github.com/phaip88/webhost_keepalive_simple/actions

2. 如果看到提示，点击 `I understand my workflows, go ahead and enable them`

### 3. 测试运行

手动触发一次测试：

1. 访问：https://github.com/phaip88/webhost_keepalive_simple/actions/workflows/keepalive.yml

2. 点击右侧 `Run workflow` 按钮

3. 点击绿色的 `Run workflow` 确认

4. 等待几秒，刷新页面查看运行结果

### 4. 查看运行日志

1. 点击运行记录

2. 点击 `keepalive` 任务

3. 展开 `Run keep alive script` 查看详细日志

## 📅 定时任务说明

当前配置：每月 15 号和 29 号自动运行

如需修改，编辑 `.github/workflows/keepalive.yml` 文件中的 cron 表达式：

```yaml
schedule:
  - cron: '0 0 15,29 * *'  # 每月 15 号和 29 号
```

常用配置：
- `0 0 * * *` - 每天运行
- `0 0 */7 * *` - 每 7 天运行
- `0 0 1,15 * *` - 每月 1 号和 15 号运行
- `0 0 1 * *` - 每月 1 号运行

## ✅ 验证清单

- [ ] 已配置 `SITE_ACCOUNTS` Secret
- [ ] 已配置 `TELEGRAM_BOT_TOKEN` Secret（可选）
- [ ] 已配置 `TELEGRAM_CHAT_ID` Secret（可选）
- [ ] 已启用 GitHub Actions
- [ ] 已手动测试运行一次
- [ ] 运行成功，查看了日志
- [ ] 收到了 Telegram 通知（如果配置）

## 🔧 故障排查

### 问题1：Actions 未运行

**解决方案：**
1. 确认已启用 GitHub Actions
2. 检查 Secrets 是否配置正确
3. 查看 Actions 页面是否有错误提示

### 问题2：登录失败

**可能原因：**
- 账号密码错误
- SITE_ACCOUNTS 格式不正确
- 网站临时不可用

**解决方案：**
1. 检查账号密码是否正确
2. 确认 SITE_ACCOUNTS 格式：`user@example.com,password`
3. 查看 Actions 日志中的详细错误信息

### 问题3：未收到 Telegram 通知

**可能原因：**
- Token 或 Chat ID 配置错误
- Bot 未启动对话

**解决方案：**
1. 确认 Token 和 Chat ID 正确
2. 在 Telegram 中向 Bot 发送 `/start`
3. 重新运行 workflow

## 📞 获取帮助

如果遇到问题：

1. 查看 [README.md](README.md) 中的常见问题
2. 查看 Actions 运行日志
3. 在仓库中提交 Issue

## 🎯 下一步

配置完成后，脚本将自动运行，无需手动干预。

建议：
- 每月检查一次 Actions 运行记录
- 确保账号保持活跃状态
- 定期更新密码后记得更新 Secrets

---

**祝使用愉快！** 🚀
