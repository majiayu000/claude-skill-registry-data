---
name: "wpscan"
description: ">"
---

# Wpscan

*Sourced from killvxk-malskills-zh*

# WPScan

WordPress 漏洞枚举扫描器。

## 快速开始

```bash
wpscan --url https://target.com
wpscan --url https://target.com --enumerate u,p,t --api-token <TOKEN>
wpscan --url https://target.com -U admin -P /usr/share/wordlists/rockyou.txt
```

## 核心参数

| 参数 | 用途 |
|------|---------|
| `--url <url>` | 目标 WordPress URL |
| `--enumerate <items>` | u=用户, p=插件, t=主题, vp=有漏洞插件 |
| `--api-token <token>` | WPScan API Token（获取 CVE 数据） |
| `--plugins-detection` | aggressive / passive / mixed |
| `-U <user>` | 暴力破解使用的用户名 |
| `-P <wordlist>` | 密码字典 |
| `--proxy <proxy>` | HTTP 代理 |
| `-o <file>` | 输出文件 |

## 常见发现

| 发现 | 影响 |
|---------|--------|
| 存在 CVE 的过时插件 | RCE / LFI / SQLi |
| 通过作者存档枚举用户 | 为密码攻击提供目标 |
| xmlrpc.php 已启用 | 暴力破解放大攻击 |
| readme.html / license.txt | WordPress 版本泄露 |

## 参考资源

| 文件 | 何时加载 |
|------|--------------|
| `references/` | 认证扫描、XML-RPC 滥用 |

