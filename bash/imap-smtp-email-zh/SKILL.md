---
name: imap-smtp-email-zh
description: 通过 IMAP/SMTP 收发邮件。检查新邮件/未读邮件、获取内容、搜索邮箱、标记已读/未读、发送带附件的邮件。支持多账号。兼容 Gmail、Outlook、163.com、vip.163.com、126.com、vip.126.com、188.com、vip.188.com 及任何标准 IMAP/SMTP 服务器。
metadata:
  openclaw:
    emoji: "📧"
    requires:
      bins:
        - node
        - npm
---

# IMAP/SMTP 邮件工具

通过 IMAP 协议读取、搜索和管理邮件。通过 SMTP 协议发送邮件。支持 Gmail、Outlook、163.com、vip.163.com、126.com、vip.126.com、188.com、vip.188.com 及任何标准 IMAP/SMTP 服务器。

## 配置

运行配置脚本设置邮箱账号：

```bash
bash setup.sh
```

配置文件存储在 `~/.config/imap-smtp-email/.env`（技能更新后不会被覆盖）。如果该路径未找到配置，将回退到技能目录下的 `.env` 文件（向后兼容）。

### 配置文件格式

```bash
# 默认账号（无前缀）
IMAP_HOST=imap.gmail.com
IMAP_PORT=993
IMAP_USER=your@email.com
IMAP_PASS=your_password
IMAP_TLS=true
IMAP_REJECT_UNAUTHORIZED=true
IMAP_MAILBOX=INBOX

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_SECURE=false
SMTP_USER=your@email.com
SMTP_PASS=your_password
SMTP_FROM=your@email.com
SMTP_REJECT_UNAUTHORIZED=true

# 文件访问白名单（安全限制）
ALLOWED_READ_DIRS=~/Downloads,~/Documents
ALLOWED_WRITE_DIRS=~/Downloads
```

## 多账号

可以在同一配置文件中添加多个邮箱账号。每个账号使用名称前缀（大写）来区分所有变量。

### 添加账号

运行配置脚本并选择"添加新账号"：

```bash
bash setup.sh
```

或手动在 `~/.config/imap-smtp-email/.env` 中添加带前缀的变量：

```bash
# 工作账号（WORK_ 前缀）
WORK_IMAP_HOST=imap.company.com
WORK_IMAP_PORT=993
WORK_IMAP_USER=me@company.com
WORK_IMAP_PASS=password
WORK_IMAP_TLS=true
WORK_IMAP_REJECT_UNAUTHORIZED=true
WORK_IMAP_MAILBOX=INBOX
WORK_SMTP_HOST=smtp.company.com
WORK_SMTP_PORT=587
WORK_SMTP_SECURE=false
WORK_SMTP_USER=me@company.com
WORK_SMTP_PASS=password
WORK_SMTP_FROM=me@company.com
WORK_SMTP_REJECT_UNAUTHORIZED=true
```

### 使用指定账号

在命令前添加 `--account <名称>`：

```bash
node scripts/imap.js --account work check
node scripts/smtp.js --account work send --to foo@bar.com --subject 你好 --body 你好世界
```

不指定 `--account` 时，使用默认（无前缀）账号。

### 账号命名规则

- 仅允许字母和数字（如 `work`、`163`、`personal2`）
- 大小写不敏感：`work` 和 `WORK` 指向同一账号
- `.env` 中的前缀始终为大写（如 `WORK_IMAP_HOST`）
- `ALLOWED_READ_DIRS` 和 `ALLOWED_WRITE_DIRS` 为所有账号共享（始终无前缀）

## 常用邮箱服务器

| 服务商 | IMAP 地址 | IMAP 端口 | SMTP 地址 | SMTP 端口 |
|--------|-----------|-----------|-----------|-----------|
| 163.com | imap.163.com | 993 | smtp.163.com | 465 |
| vip.163.com | imap.vip.163.com | 993 | smtp.vip.163.com | 465 |
| 126.com | imap.126.com | 993 | smtp.126.com | 465 |
| vip.126.com | imap.vip.126.com | 993 | smtp.vip.126.com | 465 |
| 188.com | imap.188.com | 993 | smtp.188.com | 465 |
| vip.188.com | imap.vip.188.com | 993 | smtp.vip.188.com | 465 |
| yeah.net | imap.yeah.net | 993 | smtp.yeah.net | 465 |
| Gmail | imap.gmail.com | 993 | smtp.gmail.com | 587 |
| Outlook | outlook.office365.com | 993 | smtp.office365.com | 587 |
| QQ 邮箱 | imap.qq.com | 993 | smtp.qq.com | 587 |

**Gmail 注意事项：**
- Gmail **不接受**普通账号密码
- 必须生成**应用专用密码**：https://myaccount.google.com/apppasswords
- 将生成的 16 位应用专用密码作为 `IMAP_PASS` / `SMTP_PASS`
- 需要开启 Google 账号两步验证

**163.com 注意事项：**
- 使用**授权码**，而非账号密码
- 需先在网页设置中启用 IMAP/SMTP 服务

## IMAP 命令（收邮件）

### check
检查新邮件/未读邮件。

```bash
node scripts/imap.js [--account <名称>] check [--limit 10] [--mailbox INBOX] [--recent 2h]
```

参数说明：
- `--limit <数量>`：最大结果数（默认：10）
- `--mailbox <名称>`：要检查的邮箱（默认：INBOX）
- `--recent <时间>`：仅显示最近 X 时间内的邮件（如 30m、2h、7d）

### fetch
通过 UID 获取完整邮件内容。

```bash
node scripts/imap.js [--account <名称>] fetch <uid> [--mailbox INBOX]
```

### download
下载邮件中的所有附件，或指定附件。

```bash
node scripts/imap.js [--account <名称>] download <uid> [--mailbox INBOX] [--dir <路径>] [--file <文件名>]
```

参数说明：
- `--mailbox <名称>`：邮箱（默认：INBOX）
- `--dir <路径>`：输出目录（默认：当前目录）
- `--file <文件名>`：仅下载指定附件（默认：下载全部）

### search
使用筛选条件搜索邮件。

```bash
node scripts/imap.js [--account <名称>] search [选项]

选项：
  --unseen           仅未读邮件
  --seen             仅已读邮件
  --from <邮箱>      发件人包含
  --subject <文本>   主题包含
  --recent <时间>    最近 X 时间内（如 30m、2h、7d）
  --since <日期>     指定日期之后（YYYY-MM-DD）
  --before <日期>    指定日期之前（YYYY-MM-DD）
  --limit <数量>     最大结果数（默认：20）
  --mailbox <名称>   搜索邮箱（默认：INBOX）
```

### mark-read / mark-unread
将邮件标记为已读或未读。

```bash
node scripts/imap.js [--account <名称>] mark-read <uid> [uid2 uid3...]
node scripts/imap.js [--account <名称>] mark-unread <uid> [uid2 uid3...]
```

### list-mailboxes
列出所有可用的邮箱/文件夹。

```bash
node scripts/imap.js [--account <名称>] list-mailboxes
```

### list-accounts
列出所有已配置的邮箱账号。

```bash
node scripts/imap.js list-accounts
node scripts/smtp.js list-accounts
```

显示账号名称、邮箱地址、服务器地址及配置状态。

## SMTP 命令（发邮件）

### send
通过 SMTP 发送邮件。

```bash
node scripts/smtp.js [--account <名称>] send --to <邮箱> --subject <文本> [选项]
```

**必填参数：**
- `--to <邮箱>`：收件人（多个收件人用逗号分隔）
- `--subject <文本>`：邮件主题，或使用 `--subject-file <文件>`

**可选参数：**
- `--body <文本>`：纯文本正文
- `--html`：将正文作为 HTML 发送
- `--body-file <文件>`：从文件读取正文
- `--html-file <文件>`：从文件读取 HTML 正文
- `--cc <邮箱>`：抄送
- `--bcc <邮箱>`：密送
- `--attach <文件>`：附件（多个文件用逗号分隔）
- `--from <邮箱>`：覆盖默认发件人

**使用示例：**
```bash
# 简单文本邮件
node scripts/smtp.js send --to recipient@example.com --subject "你好" --body "世界"

# HTML 邮件
node scripts/smtp.js send --to recipient@example.com --subject "新闻通讯" --html --body "<h1>欢迎</h1>"

# 带附件的邮件
node scripts/smtp.js send --to recipient@example.com --subject "报告" --body "请查收附件" --attach report.pdf

# 多个收件人
node scripts/smtp.js send --to "a@example.com,b@example.com" --cc "c@example.com" --subject "更新" --body "团队更新"
```

### test
通过向自己发送测试邮件来测试 SMTP 连接。

```bash
node scripts/smtp.js [--account <名称>] test
```

## 依赖安装

```bash
npm install
```

## 安全说明

- 配置文件存储在 `~/.config/imap-smtp-email/.env`，权限为 `600`（仅所有者可读写）
- **Gmail**：普通密码会被拒绝——请前往 https://myaccount.google.com/apppasswords 生成应用专用密码
- **163.com**：请使用授权码，而非账号密码

## 故障排除

**连接超时：**
- 确认服务器正在运行且可访问
- 检查主机/端口配置

**认证失败：**
- 确认用户名（通常为完整邮箱地址）
- 检查密码是否正确
- 163.com：请使用授权码，而非账号密码
- Gmail：普通密码不可用——请前往 https://myaccount.google.com/apppasswords 生成应用专用密码

**TLS/SSL 错误：**
- 确保 `IMAP_TLS`/`SMTP_SECURE` 设置与服务器要求匹配
- 自签名证书：设置 `IMAP_REJECT_UNAUTHORIZED=false` 或 `SMTP_REJECT_UNAUTHORIZED=false`
