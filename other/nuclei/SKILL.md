---
name: "nuclei"
description: ">"
---

# Nuclei

*Sourced from killvxk-malskills-zh*

# Nuclei

基于模板的漏洞扫描器 — 超过 10,000 个社区模板，覆盖 CVE、配置错误和信息暴露。

## 快速开始

```bash
# 使用自动更新的模板扫描 URL
nuclei -u https://example.com

# 从 URL 列表扫描
nuclei -l urls.txt

# 运行特定模板类别
nuclei -u https://example.com -t technologies/
```

## 核心参数

| 参数 | 说明 |
|------|-------------|
| `-u <url>` | 单个目标 URL |
| `-l <file>` | 包含 URL 列表的文件 |
| `-t <path>` | 模板文件/目录/URL |
| `-tags <tags>` | 按标签运行模板（如 `cve,rce,lfi`） |
| `-severity <s>` | 按严重程度过滤：`info,low,medium,high,critical` |
| `-et <path>` | 排除模板路径 |
| `-etags <tags>` | 排除标签 |
| `-es <severity>` | 排除严重程度 |
| `-H <header>` | 自定义 HTTP 头 |
| `-V <var=val>` | 模板变量覆盖 |
| `-o <file>` | 输出文件（默认标准输出） |
| `-json` | JSON 格式输出 |
| `-jsonl` | JSON Lines 格式输出 |
| `-c <n>` | 并发模板数（默认 25） |
| `-rate-limit <n>` | 最大请求速率（每秒） |
| `-timeout <n>` | HTTP 超时（默认 5 秒） |
| `-retries <n>` | 超时重试次数 |
| `-rl <n>` | 每个主机的速率限制 |
| `-proxy <url>` | HTTP/SOCKS5 代理 |
| `-update-templates` | 更新社区模板 |
| `-nt` | 仅使用新模板（上次更新后新增的） |
| `-silent` | 仅打印发现结果 |
| `-v` | 详细输出 |
| `-stats` | 显示扫描统计信息 |

## 模板类别

```bash
nuclei -u https://target.com -t cves/              # CVE templates
nuclei -u https://target.com -t exposures/         # Exposed files/panels
nuclei -u https://target.com -t technologies/      # Tech fingerprinting
nuclei -u https://target.com -t misconfigurations/ # Misconfigs
nuclei -u https://target.com -t default-logins/    # Default credentials
nuclei -u https://target.com -t network/           # TCP/UDP templates
```

## 常见工作流

```bash
# 先更新模板
nuclei -update-templates

# 全面 Web 扫描（跳过 info 级别）
nuclei -l urls.txt -es info -o findings.txt

# 以 CVE 为重点的扫描
nuclei -u https://target.com -tags cve -severity medium,high,critical

# 暴露的面板和管理界面
nuclei -u https://target.com -tags panel,login,exposure

# 使用自定义模板
nuclei -u https://target.com -t /path/to/custom.yaml

# 通过代理扫描（Burp）
nuclei -u https://target.com -proxy http://127.0.0.1:8080

# 快速侦察并进行技术指纹识别
nuclei -l urls.txt -t technologies/ -silent
```

## 参考资源

| 文件 | 加载时机 |
|------|--------------|
| `references/templates.md` | 模板语法、自定义模板编写、标签参考 |

