---
name: cloud-ksyun
description: 使用 ksyun CLI 操作金山云。当用户提到金山云、KSYUN、KS3、金山云VPS 等时触发此技能。
---

# 金山云 Operator Skill

## 安装 CLI
```bash
pip install ks3client
# 或下载官方 CLI
```

## 认证
```bash
export KSYUN_ACCESS_KEY="your_access_key"
export KSYUN_SECRET_KEY="your_secret_key"
```

## 常用命令
```bash
# 云服务器 KE
ksyun kec describe-instances
ksyun kec run-instances --image-id xxx --instance-type S1.SMALL1
ksyun kec terminate-instances --instance-id xxx

# 对象存储 KS3
ksyun ks3 ls
ksyun ks3 mb s3://my-bucket
ksyun ks3 cp local-file s3://bucket/key

# 负载均衡
ksyun slb describe-loadbalancers

# 云数据库
ksyun kdb describe-db-instances

# VPC
ksyun vpc describe-vpcs
```

## 安全机制
- 只读操作：直接执行
- 写操作：先确认后执行