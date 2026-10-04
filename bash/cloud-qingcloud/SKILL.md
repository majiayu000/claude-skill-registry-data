---
name: cloud-qingcloud
description: 使用 qingcloud CLI 操作青云 QingCloud。当用户提到青云、QingCloud、青云云、青云QingCloud 等时触发此技能。
---

# QingCloud Operator Skill

## 安装 CLI
```bash
pip install qingcloud-cli
```

## 认证
```bash
qingcloud configure
# 输入 qy_access_key_id 和 qy_secret_access_key
```

## 常用命令
```bash
# 云服务器
qingcloud iaas describe-instances
qingcloud iaas run-instances --image-id img-xxx --instance-type c1m1.small
qingcloud iaas terminate-instances --instances i-xxx

# 硬盘
qingcloud iaas describe-volumes
qingcloud iaas create-volumes --size 100 --volume-type 0

# 网络
qingcloud iaas describe-vxnet
qingcloud iaas create-vxnet --vxnet-name my-vxnet

# 负载均衡
qingcloud iaas describe-loadbalancers

# 对象存储
qingcloud object list-buckets
```

## 安全机制
- 只读操作：直接执行
- 写操作：先确认后执行