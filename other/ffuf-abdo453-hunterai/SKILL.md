---
name: "ffuf"
description: ">"
---

# Ffuf

*Sourced from killvxk-malskills-zh*

# ffuf

基于 Go 的 Web 模糊测试工具 — FUZZ 关键字可放置在请求的任意位置（URL、请求头、请求体、主机名）。

## 快速开始

```bash
# 目录模糊测试
ffuf -u http://example.com/FUZZ -w /usr/share/wordlists/dirb/common.txt

# 带文件扩展名
ffuf -u http://example.com/FUZZ -w common.txt -e .php,.html,.txt

# 子域名/虚拟主机模糊测试
ffuf -u http://FUZZ.example.com -w subdomains.txt -H "Host: FUZZ.example.com"
```

## 核心参数

| 参数 | 说明 |
|------|-------------|
| `-u <url>` | 目标 URL（用 `FUZZ` 作为占位符） |
| `-w <wordlist>` | 字典路径（用 `:KEYWORD` 命名 payload） |
| `-e <ext>` | 为每个词追加扩展名 |
| `-t <n>` | 线程数（默认 40） |
| `-rate <n>` | 每秒最大请求数 |
| `-H <header>` | 自定义请求头 |
| `-X <method>` | HTTP 方法（默认 GET） |
| `-d <data>` | POST 请求体数据 |
| `-b <cookies>` | Cookie 字符串 |
| `-r` | 跟随重定向 |
| `-k` | 跳过 TLS 验证 |
| `-x <proxy>` | 代理 URL |
| `-o <file>` | 输出文件 |
| `-of <format>` | 输出格式：`json`、`html`、`csv`、`md`、`all` |
| `-v` | 详细模式（显示重定向） |
| `-s` | 静默模式 |
| `-p <delay>` | 请求间延迟（如 `0.1` 或 `0.1-0.5`） |

## 过滤与匹配

| 参数 | 说明 |
|------|-------------|
| `-mc <codes>` | 匹配 HTTP 状态码（默认 `200,204,301,302,307,401,403,405`） |
| `-ml <n>` | 按响应行数匹配 |
| `-mw <n>` | 按词数匹配 |
| `-ms <size>` | 按响应大小匹配 |
| `-mr <regex>` | 按响应体正则匹配 |
| `-fc <codes>` | 过滤（排除）状态码 |
| `-fl <n>` | 按行数过滤 |
| `-fw <n>` | 按词数过滤 |
| `-fs <n>` | 按大小过滤 |
| `-fr <regex>` | 按正则过滤 |

## 多 FUZZ 位置

```bash
# 两个字典：W1 + W2
ffuf -u http://target.com/W1/W2 -w list1.txt:W1 -w list2.txt:W2

# 集束炸弹模式（所有组合）
ffuf -u http://target.com/W1?param=W2 -w list1.txt:W1 -w list2.txt:W2 -mode clusterbomb

# 音叉模式（配对位置）
ffuf -u http://target.com/W1?user=W2 -w paths.txt:W1 -w users.txt:W2 -mode pitchfork
```

## 常用工作流

```bash
# 标准目录模糊测试，带噪声过滤
ffuf -u https://target.com/FUZZ -w raft-medium.txt -fc 404 -o dirs.json -of json

# POST 登录暴力破解
ffuf -u https://target.com/login -X POST -d "user=admin&pass=FUZZ" -w passwords.txt -fc 401

# 参数发现（GET）
ffuf -u "https://target.com/page?FUZZ=test" -w params.txt -fw 42

# 虚拟主机发现
ffuf -u http://target.com -H "Host: FUZZ.target.com" -w vhosts.txt -fw 42

# 带认证的 API 端点模糊测试
ffuf -u https://api.target.com/v1/FUZZ -w api-words.txt -H "Authorization: Bearer TOKEN" -mc 200,201,204
```

## 资源

| 文件 | 何时加载 |
|------|--------------|
| `references/filters.md` | 所有过滤/匹配参数、噪声过滤策略、多 FUZZ 模式 |

