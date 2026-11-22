---
name: "john"
description: ">"
---

# John

*Sourced from killvxk-malskills-zh*

# John the Ripper

CPU 密码破解器 — 支持数百种哈希格式，字典 + 规则 + 递增暴力破解。

## 快速开始

```bash
# 自动检测格式并破解
john hashes.txt --wordlist=/usr/share/wordlists/rockyou.txt

# 显示已破解密码
john hashes.txt --show

# 单一破解模式（快速，基于用户名提示）
john hashes.txt --single

# 递增暴力破解
john hashes.txt --incremental
```

## 核心参数

| 参数 | 用途 |
|------|------|
| `--wordlist=FILE` | 字典攻击 |
| `--rules[=RULE]` | 应用变形规则 |
| `--format=TYPE` | 强制指定哈希格式 |
| `--single` | 单一破解（用户名提示） |
| `--incremental` | 暴力破解 |
| `--show` | 显示已破解密码 |
| `--pot=FILE` | 自定义 pot 文件 |
| `--fork=N` | 并行进程数 |
| `--list=formats` | 列出所有支持的格式 |

## 常用工作流

**NTLM 配合规则：**
```bash
john ntlm.txt --format=NT --wordlist=rockyou.txt --rules=best64
```

**SSH 私钥：**
```bash
ssh2john id_rsa > id_rsa.hash
john id_rsa.hash --wordlist=rockyou.txt
```

**Zip 压缩包：**
```bash
zip2john archive.zip > zip.hash
john zip.hash --wordlist=rockyou.txt
```

## 参考资源

| 文件 | 加载时机 |
|------|----------|
| `references/` | 规则语法和格式列表 |

