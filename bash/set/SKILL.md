---
name: "set"
description: ">"
---

# Set

*Sourced from killvxk-malskills-zh*

# SET — Social-Engineer Toolkit

综合社会工程学框架 — 鱼叉式钓鱼、凭据收割与载荷投递。

## 快速开始

```bash
# 启动交互式菜单
sudo setoolkit

# 或通过 CLI 启动特定攻击
sudo python setoolkit
```

## 主菜单结构

```
1) Social-Engineering Attacks
2) Penetration Testing (Fast-Track)
3) Third Party Modules
4) Update the Social-Engineer Toolkit
```

## 关键攻击向量

### 1. 鱼叉式钓鱼攻击向量 (Spear-Phishing Attack Vector)
`1 > 1` — 发送含嵌入载荷的钓鱼邮件：
- 文件格式利用（PDF、Office 宏）
- 自定义载荷附件
- 批量邮件活动

### 2. 网站攻击向量 (Website Attack Vector)
`1 > 2` — 基于 Web 的攻击：

| 选项 | 说明 |
|------|------|
| Java Applet | 已签名的 Java applet 投放载荷 |
| Metasploit Browser | 浏览器利用载荷投递 |
| **Credential Harvester** | 克隆网站 + 捕获凭据 |
| Tabnabbing | 替换不活跃的浏览器标签 |
| Web Jacking | 通过 iframe 重定向 |
| Multi-Attack | 组合多种 Web 攻击 |

### 3. 凭据收割器 (Credential Harvester)

```
1 > 2 > 3   # 凭据收割攻击
> 2         # 网站克隆器
> 输入回传 IP
> 输入要克隆的 URL（如 https://mail.google.com）
```

SET 克隆目标网站并在本地提供服务。提交至表单的凭据将被拦截并记录。

### 4. 批量邮件攻击 (Mass Mailer Attack)
`1 > 5` — 发送批量鱼叉式钓鱼邮件：
- 单个定向邮件
- 从列表批量发送
- 需要 SMTP 凭据

## 常用工作流

```bash
# 凭据收割器配合网站克隆
sudo setoolkit
# 1 > 2 > 3 > 2
# 输入攻击者 IP：192.168.1.5
# 要克隆的 URL：https://outlook.office365.com

# 捕获的凭据存储在：/var/www/ 或 SET 报告目录
cat /root/.set/reports/2024*/

# 基于 Java 的载荷投递（旧式但对旧 JRE 仍有效）
# 1 > 2 > 1

# 带 Office 宏载荷的鱼叉钓鱼
# 1 > 1 > 1（发送至特定地址）
```

## 日志与报告

- 凭据：`/root/.set/reports/`
- 邮件日志：`/root/.set/`
- 配置文件：`/etc/setoolkit/set.config`

## 资源文件

| 文件 | 加载时机 |
|------|----------|
| `references/attack-vectors.md` | 完整菜单树、载荷选项、SMTP 配置及规避技巧 |

