---
name: cloud-scaleway
description: 使用 scw CLI 操作 Scaleway。当用户提到 Scaleway、scw、Scaleway 云、Scaleway VPS 等时触发此技能。
---

# Scaleway Operator Skill

## 安装 CLI
```bash
# macOS
brew install scaleway-cli

# Linux
curl -o /usr/local/bin/scw -L "https://github.com/scaleway/scaleway-cli/releases/latest/download/scw-linux-x86_64"
chmod +x /usr/local/bin/scw
```

## 认证
```bash
scw init
```

## 常用命令
```bash
# 实例
scw instance server list
scw instance server create type=DEV1-S image=ubuntu_jammy name=my-server
scw instance server delete <server-id>

# 镜像
scw instance image list

# 存储
scw object bucket list
scw object bucket create my-bucket

# Kubernetes
scw k8s cluster list
scw k8s cluster create name=my-cluster version=1.27

# 数据库
scw rdb instance list
```

## 安全机制
- 只读操作：直接执行
- 写操作：先确认后执行