---
name: "xsstrike"
description: ">"
---

# Xsstrike

*Sourced from killvxk-malskills-zh*

# XSStrike

上下文感知的 XSS 检测与 Payload 生成工具。

## 快速开始

```bash
python xsstrike.py -u "http://target.com/search?q=test"
python xsstrike.py -u "http://target.com" --crawl
python xsstrike.py -u "http://target.com/feedback" --blind
python xsstrike.py -u "http://target.com/?q=test" --fuzzer
```

## 核心参数

| 参数 | 用途 |
|------|---------|
| `-u <url>` | 带参数的目标 URL |
| `--crawl` | 爬取并测试所有发现的链接 |
| `--blind` | 盲 XSS 模式（不检查响应中的反射） |
| `--fuzzer` | 使用 payload 列表进行模糊测试 |
| `-l <level>` | 爬取深度 |
| `--data <post>` | POST 数据 |
| `-p <param>` | 仅测试指定参数 |
| `--headers <h>` | 自定义请求头 |
| `--proxy <proxy>` | 通过代理路由流量 |

## 参考资源

| 文件 | 何时加载 |
|------|--------------|
| `references/` | DOM XSS 测试、WAF 绕过技术 |

