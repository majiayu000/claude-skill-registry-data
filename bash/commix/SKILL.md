---
name: "commix"
description: ">"
---

# Commix

*Sourced from killvxk-malskills-zh*

# Commix

自动化 OS 命令注入检测与利用工具。

## 快速开始

```bash
commix --url="http://target.com/page?ip=127.0.0.1"
commix --url="http://target.com/ping" --data="ip=127.0.0.1"
commix -r request.txt
commix --url="http://target.com/?ip=1" --os-shell
```

## 核心参数

| 参数 | 用途 |
|------|---------|
| `--url <url>` | 目标 URL |
| `--data <data>` | POST 请求体 |
| `-r <file>` | Burp 格式的请求文件 |
| `--cookie <c>` | 会话 Cookie |
| `--os-cmd <cmd>` | 执行单条 OS 命令 |
| `--os-shell` | 交互式伪 Shell |
| `--technique <t>` | classic / timebased / tempfile-based / file-based |
| `--level <1-3>` | 模糊测试深度 |
| `--proxy <proxy>` | HTTP 代理 |
| `--batch` | 非交互式默认选项 |

## 参考资源

| 文件 | 加载时机 |
|------|--------------|
| `references/` | 盲注、通过命令注入上传文件 |

