---
name: cloud-aws
description: 仅使用 AWS CLI 操作 AWS。Agent 直接执行 aws 命令（无需脚本）。仅在用户提到 AWS、S3、EC2、Lambda 等时激活。
---

# AWS Cloud Operator Skill（极简纯 AWS CLI）

## 激活条件
用户提到 “AWS”、“S3”、“EC2”、“Lambda”、“CloudFormation”、“项目/账号”等时立即激活。

## 执行规则（核心）
- Agent 直接执行 `aws ...` 命令（系统内置 shell）。
- 自动加上 `--output table`（人类阅读）或 `--output json`。
- 执行前先检查认证：`aws sts get-caller-identity`。

## 安全与确认机制（强制）
- **只读操作**（list、describe、get）：直接执行。
- **写操作**（create、delete、update、deploy）：
  1. 先完整展示即将执行的**完整命令**
  2. 询问：“确认要执行这条命令吗？(yes/no)”
  3. 只有用户回复 **yes** 后才执行
- 删除类操作额外提醒风险。

## 示例交互
**用户**：列出我的所有 S3 桶  
**Agent**：直接执行 `aws s3 ls --output table`

**用户**：创建一个 EC2 实例  
**Agent**：即将执行：`aws ec2 run-instances --image-id ami-xxx --instance-type t2.micro`  
确认要执行这条命令吗？(yes/no)

## 常用模板
- 账号信息：`aws sts get-caller-identity`
- S3：`aws s3 ls` / `aws s3 mb s3://my-bucket`
- EC2：`aws ec2 describe-instances`
- 设置 region：`aws configure set region us-east-1`

## 提示
- 未认证时提示用户运行 `aws configure`。