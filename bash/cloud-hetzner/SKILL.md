---
name: cloud-hetzner
description: 使用 hcloud CLI 操作 Hetzner Cloud。当用户提到 Hetzner、hcloud、Hetzner Cloud、Hetzner VPS 等时触发此技能。
---

# Hetzner Cloud Operator Skill

## 安装 CLI
```bash
# macOS
brew install hcloud

# Linux
curl -fsSL https://github.com/hetznercloud/cli/releases/latest/download/hcloud-linux-amd64.tar.gz | tar -xz
```

## 认证
```bash
hcloud context create my-project
# 输入 API Token（从 https://console.hetzner.cloud 获取）
```

## 常用命令
```bash
# 服务器
hcloud server list
hcloud server create --name my-server --type cx22 --image ubuntu-22.04
hcloud server delete my-server

# 镜像
hcloud image list --type system

# 类型
hcloud server-type list

# 网络
hcloud network list
hcloud network create --name my-network --ip-range 10.0.0.0/16

# 负载均衡
hcloud load-balancer list
```

## 安全机制
- 只读操作：直接执行
- 写操作：先确认后执行