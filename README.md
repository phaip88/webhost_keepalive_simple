# WebHostMost 账号保活脚本 (轻量版)

[![Keep Alive](https://github.com/phaip88/webhost_keepalive_simple/actions/workflows/keepalive.yml/badge.svg)](https://github.com/phaip88/webhost_keepalive_simple/actions/workflows/keepalive.yml)

## 项目简介

本项目用于自动登录 [WebHostMost](https://client.webhostmost.com/login) 网站，实现账号保活。

**特点：**
- ✅ 轻量级：仅需 `requests` 库，无需 Playwright 和 Chromium
- ✅ 快速：每个账号登录仅需 3-5 秒
- ✅ 多账号支持：可同时管理多个账号
- ✅ TG 通知：优化的 Telegram 通知格式
- ✅ 严格验证：检测到倒计时元素才算成功
- ✅ GitHub Actions：自动定时运行

## 功能说明

### 1. 多账号支持
通过环境变量配置多个账号，支持批量保活。

### 2. 成功判定标准
- ✅ 登录成功
- ✅ 检测到倒计时元素（多语言支持）
- 只有同时满足以上条件才算保活成功

### 3. Telegram 通知
优化的通知格式，包含：
- 成功/失败统计
- 每个账号的详细状态
- 倒计时确认信息
- 失败原因说明

**通知示例：**
```
📌 WebHostMost 保活报告
🕒 2026-02-11 21:30:58 UTC+8

📊 执行结果
✅ 成功: 2 | 失败: 0

👤 账号详情
✅ user1@example.com
   ⏱️ 倒计时元素已确认 (德语)
✅ user2@example.com
   ⏱️ 倒计时元素已确认 (英语)

💡 提示: 请确保每 45 天至少登录一次
```

### 4. 自动重试
登录失败时自动重试，最多 3 次尝试。

## 使用方式

### 方法一：Fork 部署（推荐）

1. **Fork 本仓库**
   - 点击右上角 `Fork` 按钮

2. **配置 Secrets**
   
   进入 `Settings` → `Secrets and variables` → `Actions` → `New repository secret`

   **必需配置：**
   
   - `SITE_ACCOUNTS`：账号信息
     ```
     单账号格式：
     user@example.com,password
     
     多账号格式（用分号分隔）：
     user1@example.com,pass1;user2@example.com,pass2
     ```

   **可选配置（Telegram 通知）：**
   
   - `TELEGRAM_BOT_TOKEN`：你的 Telegram Bot Token
   - `TELEGRAM_CHAT_ID`：你的 Telegram Chat ID

3. **启用 GitHub Actions**
   
   进入 `Actions` 页面，点击 `I understand my workflows, go ahead and enable them`

4. **手动测试**
   
   进入 `Actions` → `Keep Alive` → `Run workflow`

### 方法二：本地运行

1. **安装依赖**
   ```bash
   pip install requests
   ```

2. **配置环境变量**
   
   **Windows (PowerShell):**
   ```powershell
   $env:SITE_ACCOUNTS="user@example.com,password"
   ```
   
   **Linux/Mac:**
   ```bash
   export SITE_ACCOUNTS="user@example.com,password"
   ```

3. **运行脚本**
   ```bash
   python login.py
   ```

## 定时任务配置

GitHub Actions 默认配置：
- 每月 15 号和 29 号自动运行
- 支持手动触发

修改定时任务：编辑 `.github/workflows/keepalive.yml` 中的 `cron` 表达式

```yaml
schedule:
  - cron: '0 0 15,29 * *'  # 每月 15 号和 29 号
```

常用 cron 表达式：
- `0 0 * * *` - 每天运行
- `0 0 */7 * *` - 每 7 天运行
- `0 0 1,15 * *` - 每月 1 号和 15 号运行

## 日志示例

```
🚀 开始登录账号: user@example.com (尝试 1/3)
✅ 账号 user@example.com 登录成功
⏱️ 检测到倒计时元素 (语言: Zeit bis zur Sperrung)
```

## 技术说明

### 工作原理
1. 获取登录页面并提取 CSRF token
2. 提交登录表单
3. 检查登录是否成功
4. 验证倒计时元素是否存在
5. 发送 Telegram 通知（如果配置）

### 倒计时检测
支持多语言倒计时检测：
- 英语：Time until suspension
- 荷兰语：Tijd tot schorsing
- 德语：Zeit bis zur Sperrung
- 日语：停止までの時間
- 西班牙语：Tiempo hasta la suspensión

### 依赖说明
- `requests`：HTTP 请求库
- Python 3.7+

## 常见问题

**Q: 为什么要检测倒计时元素？**

A: 倒计时元素是账号处于活跃状态的标志。只有检测到倒计时才能确保保活成功。

**Q: 支持多少个账号？**

A: 理论上无限制，但建议不超过 10 个账号，以避免触发网站的防刷机制。

**Q: GitHub Actions 会消耗多少时间？**

A: 每个账号约 3-5 秒，10 个账号约 30-50 秒。

**Q: 如何获取 Telegram Bot Token？**

A: 在 Telegram 中搜索 @BotFather，发送 `/newbot` 创建机器人。

**Q: 如何获取 Telegram Chat ID？**

A: 在 Telegram 中搜索 @userinfobot，发送任意消息获取你的 Chat ID。

**Q: 登录失败怎么办？**

A: 检查账号密码是否正确，查看 Actions 日志中的错误信息。

## 注意事项

1. 确保账号密码正确
2. 建议每 30-40 天运行一次（网站要求 45 天内登录）
3. GitHub Actions 免费账户有执行时长限制
4. 本项目仅用于保活，不涉及其他操作

## 项目结构

```
webhost_keepalive_simple/
├── login.py                    # 主脚本
├── .github/
│   └── workflows/
│       └── keepalive.yml      # GitHub Actions 工作流
├── README.md                   # 项目说明
└── LICENSE                     # 许可证
```

## 更新日志

### 2026-02-11 - v1.0
- ✅ 初始版本发布
- ✅ 轻量级实现（仅需 requests）
- ✅ 多账号支持
- ✅ 优化的 TG 通知
- ✅ 严格的成功验证
- ✅ GitHub Actions 支持

## 许可证

MIT License

## 致谢

感谢 WebHostMost 提供的免费托管服务。

---

**⭐ 如果这个项目对你有帮助，请给个 Star！**
