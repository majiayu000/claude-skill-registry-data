---
name: "nmap"
description: ">"
---

# Nmap

*Sourced from killvxk-malskills-zh*

# Nmap

快速、可脚本化的网络扫描器 — 端口扫描和服务枚举的行业标准。

## 快速开始

```bash
# 基础 TCP SYN 扫描，扫描前 1000 个端口
nmap -sS -T4 <target>

# 全端口扫描，含版本检测 + 脚本 + 操作系统识别
nmap -sS -sV -sC -O -p- -T4 <target> -oA output/nmap_full

# 快速扫描前 100 个端口
nmap -F -T4 <target>
```

## 核心扫描类型

| 参数 | 扫描类型 | 说明 |
|------|-----------|-------|
| `-sS` | TCP SYN（隐蔽扫描） | 需要 root；最常用 |
| `-sT` | TCP Connect | 无需 root；噪声更大 |
| `-sU` | UDP 扫描 | 较慢；可与 `-sS` 结合 |
| `-sN/sF/sX` | Null/FIN/Xmas | 防火墙规避 |
| `-sA` | ACK 扫描 | 映射防火墙规则 |
| `-sV` | 版本检测 | 服务 banner |
| `-sC` | 默认脚本 | 运行常用 NSE 脚本 |
| `-O` | 操作系统检测 | 需要 root |
| `-A` | 激进模式 | `-sV -sC -O --traceroute` |

## 端口选择

```bash
-p 22,80,443          # specific ports
-p 1-1024             # range
-p-                   # all 65535 ports
--top-ports 1000      # top N most common
-F                    # top 100 (fast)
```

## 输出格式

```bash
-oN file.txt          # normal (human-readable)
-oX file.xml          # XML (parseable)
-oG file.gnmap        # grepable
-oA basename          # all three formats
```

## 时序与性能

| 模板 | 使用场景 |
|----------|----------|
| `-T0` | 偏执模式 — IDS 规避 |
| `-T1` | 慢速 |
| `-T3` | 默认 |
| `-T4` | 激进 — 快速网络 |
| `-T5` | 极速 — 可能遗漏结果 |

精细调节：`--min-rate 1000 --max-retries 2`

## 目标指定

```bash
nmap 192.168.1.1
nmap 192.168.1.0/24
nmap 192.168.1.1-254
nmap -iL targets.txt        # from file
nmap --exclude 192.168.1.5
```

## NSE 脚本

```bash
# 运行特定脚本
nmap --script smb-vuln-ms17-010 -p 445 <target>

# 运行某个类别
nmap --script vuln <target>
nmap --script "safe and discovery" <target>

# 认证暴力破解
nmap --script http-brute -p 80 <target>
```

脚本类别：`auth`、`broadcast`、`brute`、`default`、`discovery`、`dos`、`exploit`、`external`、`fuzzer`、`intrusive`、`malware`、`safe`、`version`、`vuln`

## 常见工作流

```bash
# 仅主机发现（ping 扫描）
nmap -sn 192.168.1.0/24

# 全面侦察一行命令
nmap -sS -sV -sC -O -p- -T4 --open -oA full_scan <target>

# 内网 Windows 环境
nmap -sS -p 135,139,445,3389,5985 -T4 192.168.1.0/24

# Web 面
nmap -sV -p 80,443,8080,8443 --script http-headers,http-title <target>

# UDP 常用服务
nmap -sU --top-ports 20 -T4 <target>
```

## 参考资源

| 文件 | 加载时机 |
|------|--------------|
| `references/nse-scripts.md` | 需要按类别查询 NSE 脚本列表、语法或漏洞脚本时 |

