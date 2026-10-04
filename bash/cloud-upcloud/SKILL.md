---
name: cloud-upcloud
description: 使用 upcloud CLI 操作 UpCloud。当用户提到 UpCloud、UpCloud VPS、UpCloud 云服务器等时触发此技能。
---

# UpCloud Operator Skill

## 安装 CLI
```bash
pip install upcloud-cli
# 或
brew install upcloud-cli
```

## 认证
```bash
export UPCLOUD_USERNAME="your_username"
export UPCLOUD_PASSWORD="your_password"
```

## 常用命令
```bash
# 服务器
upcloud server list
upcloud server create --hostname my-server --zone fi-hel1 --title "My Server"
upcloud server delete <uuid>

# 存储
upcloud storage list
upcloud storage create --name my-storage --size 100 --zone fi-hel1

# 网络
upcloud network list

# 防火墙
upcloud firewall list
```

## 安全机制
- 只读操作：直接执行
- 写操作：先确认后执行