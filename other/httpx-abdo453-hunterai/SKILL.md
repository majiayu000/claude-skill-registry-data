---
name: "httpx"
description: ">"
---

# Httpx

*Sourced from killvxk-malskills-zh*

# httpx

ProjectDiscovery 出品的快速 HTTP 工具包 — 大规模探测和指纹识别 Web 服务器。

## 快速开始

```bash
# 探测一批 host
cat hosts.txt | httpx

# 探测并显示状态码和标题
httpx -l hosts.txt -status-code -title

# 静默模式（仅输出存活 URL）
cat subs.txt | httpx -silent
```

## 核心参数

| 参数 | 说明 |
|------|------|
| `-l <file>` | 包含 host 的输入文件 |
| `-u <url>` | 单个目标 |
| `-silent` | 仅打印存活 URL |
| `-status-code` | 显示 HTTP 状态码 |
| `-title` | 提取页面标题 |
| `-tech-detect` | 检测技术栈（Wappalyzer） |
| `-web-server` | 显示 Web 服务器请求头 |
| `-content-type` | 显示 Content-Type 请求头 |
| `-ip` | 解析并显示 IP |
| `-cname` | 显示 CNAME |
| `-location` | 显示重定向地址 |
| `-content-length` | 显示响应大小 |
| `-hash <algo>` | 对响应体计算哈希（md5、sha1、sha256） |
| `-favicon` | 提取 favicon 哈希（Shodan mmh3） |
| `-follow-redirects` | 跟随 HTTP 重定向 |
| `-threads <n>` | 并发线程数（默认 50） |
| `-rate-limit <n>` | 每秒请求数 |
| `-timeout <n>` | 超时时间（秒，默认 5） |
| `-retries <n>` | 重试次数 |
| `-H <header>` | 自定义请求头 |
| `-proxy <url>` | HTTP/SOCKS5 代理 |
| `-o <file>` | 输出文件 |
| `-json` | JSON 输出 |
| `-csv` | CSV 输出 |
| `-ports <p>` | 探测指定端口（如 `80,443,8080`） |
| `-tls-probe` | 探测 TLS |
| `-http2` | 启用 HTTP/2 |
| `-screenshot` | 截图（需要 chromium） |

## 常用工作流

```bash
# 完整侦察流水线：subfinder -> httpx
subfinder -d target.com -silent | httpx -status-code -title -tech-detect -o live.txt

# 探测列表并获取所有元数据
httpx -l hosts.txt -status-code -title -tech-detect -web-server -ip -o full.json -json

# 查找后台/登录面板
httpx -l hosts.txt -title -silent | grep -iE "admin|login|portal|dashboard"

# 指定端口探测
httpx -l hosts.txt -ports 80,443,8080,8443,3000,8888 -status-code -silent

# Favicon 哈希（用于 Shodan 关联分析）
httpx -u https://target.com -favicon

# 对所有存活 host 截图
httpx -l hosts.txt -screenshot -output screenshots/
```

## 参考资源

| 文件 | 加载时机 |
|------|----------|
| `references/output-fields.md` | 所有输出字段参数、JSON 格式和过滤选项 |

