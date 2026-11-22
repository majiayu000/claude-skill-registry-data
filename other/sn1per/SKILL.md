---
name: "sn1per"
description: ">"
---

# Sn1Per

*Sourced from killvxk-malskills-zh*

# Sn1per

自动化侦察框架 — 编排 nmap、nikto、metasploit、amass 等 20+ 种工具。

## 快速开始

```bash
git clone https://github.com/1N3/Sn1per
cd Sn1per && bash install.sh

# 对目标进行完整侦察
sniper -t target.com

# 网络 CIDR 扫描
sniper -t 10.10.10.0/24 -m discover

# 仅 Web 扫描
sniper -t target.com -m web
```

## 扫描模式

| 模式 | 用途 |
|------|------|
| （默认） | 完整侦察 + 漏洞扫描 |
| `discover` | 网络发现（ping 扫描、端口扫描） |
| `stealth` | 速度较慢、更安静的扫描 |
| `web` | Web 专项扫描（nikto、gobuster 等） |
| `bruteforce` | 服务暴力破解 |
| `airstrike` | 从 CIDR 发起批量扫描 |
| `nuke` | 完整攻击自动化 |

## 常用工作流

**完整目标评估：**
```bash
sniper -t target.com
# 结果保存在 /usr/share/sniper/loot/
```

**CIDR 发现：**
```bash
sniper -t 192.168.1.0/24 -m discover -w workspace1
```

**Web 应用评估：**
```bash
sniper -t https://app.target.com -m web
```

## 资源文件

| 文件 | 加载时机 |
|------|----------|
| `references/` | 模块配置与战利品存储路径 |

