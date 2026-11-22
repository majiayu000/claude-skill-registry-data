---
name: "dnsx"
description: ">"
---

# Dnsx

*Sourced from killvxk-malskills-zh*

# dnsx

快速 DNS 工具集 — 大规模解析、暴力破解和提取 DNS 记录。

## 快速开始

```bash
# 解析子域名列表
cat subs.txt | dnsx

# 对域名执行 DNS 暴力破解
dnsx -d example.com -w wordlist.txt

# 提取 A 记录并显示响应
cat subs.txt | dnsx -a -resp
```

## 核心参数

| 参数 | 说明 |
|------|-------------|
| `-l <file>` | 输入主机/子域名列表文件 |
| `-d <domain>` | 目标域名（用于暴力破解） |
| `-w <wordlist>` | 暴力破解字典 |
| `-a` | 查询 A 记录 |
| `-aaaa` | 查询 AAAA 记录 |
| `-cname` | 查询 CNAME 记录 |
| `-mx` | 查询 MX 记录 |
| `-ns` | 查询 NS 记录 |
| `-txt` | 查询 TXT 记录 |
| `-ptr` | 查询 PTR 记录 |
| `-resp` | 显示 DNS 响应内容 |
| `-resp-only` | 仅显示 DNS 响应 |
| `-rcode <code>` | 按 rcode 过滤（如 `noerror,nxdomain`） |
| `-r <resolvers>` | 自定义解析器文件 |
| `-rl <n>` | 速率限制（请求/秒） |
| `-t <n>` | 线程数（默认 100） |
| `-timeout <n>` | 超时时间（默认 5s） |
| `-silent` | 仅输出结果 |
| `-o <file>` | 输出文件 |
| `-json` | JSON 格式输出 |
| `-wildcard` | 过滤通配符子域名 |

## 常用工作流

```bash
# 管道：subfinder -> dnsx 解析
subfinder -d target.com -silent | dnsx -silent

# 使用字典进行 DNS 暴力破解
dnsx -d target.com -w /usr/share/dnsrecon/subdomains-top1mil-5000.txt -t 50

# 以 JSON 格式获取所有记录类型
cat subs.txt | dnsx -a -cname -mx -txt -resp -o dns_records.json -json

# 批量解析 IP 地址
cat domains.txt | dnsx -a -resp-only | sort -u

# 过滤通配符结果
cat subs.txt | dnsx -wildcard -d target.com -silent

# 对 IP 列表执行反向 DNS（PTR）查询
cat ips.txt | dnsx -ptr -resp-only
```

## 资源

| 文件 | 何时加载 |
|------|--------------|
| `references/dns-records.md` | DNS 记录类型、暴力破解字典、通配符检测 |

