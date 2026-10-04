---
name: cloud-ucloud
description: 使用 ucloud CLI 操作 UCloud 优刻得。当用户提到 UCloud、优刻得、UCloud 云、UCloud VPS 等时触发此技能。
---

# UCloud Operator Skill

## 安装 CLI
```bash
# macOS/Linux
curl -fsSL https://github.com/ucloud/ucloud-cli/releases/latest/download/ucloud-cli-linux-amd64.tar.gz | tar -xz
mv ucloud /usr/local/bin/
```

## 认证
```bash
ucloud config init
# 输入公钥、私钥（从 https://console.ucloud.cn 获取）
```

## 常用命令
```bash
# 云主机
ucloud uhost list
ucloud uhost create --name my-host --cpu 2 --memory 4 --image-id uimage-xxx
ucloud uhost delete <uhost-id>

# 镜像
ucloud image list

# 存储
ucloud ulb list                    # 负载均衡
ucloud ufile bucket list           # 对象存储

# 网络
ucloud vpc list
ucloud subnet list

# 数据库
ucloud udb list
```

## 安全机制
- 只读操作：直接执行
- 写操作：先确认后执行