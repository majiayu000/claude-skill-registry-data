---
name: cloud-vultr
description: 仅使用 Vultr CLI（vultr-cli）操作 Vultr 云。Agent 直接执行 vultr-cli 命令（无需脚本）。仅在用户提到 Vultr、VPS、实例、对象存储等时激活。
---

# Vultr Cloud Operator Skill（极简纯 Vultr CLI）

## 前置安装

- 安装cli工具，brew install vultr
- 配置Key，echo "api-key: xxx" > ~/.vultr-cli.yaml

## 激活条件
用户提到 “Vultr”、“VPS”、“实例”、“服务器”、“Cloud Compute”、“对象存储”等关键词时立即激活。

## 执行规则（核心）
- Agent **直接执行** `vultr-cli ...` 命令（系统内置 shell）。
- 自动加上 `--output json`（结构化）或 table（如果支持）。
- 执行前先检查认证：`vultr-cli account get`

## 安全与确认机制（强制）
- **只读操作**（list、get、describe）：直接执行并返回结果。
- **写操作**（create、delete、update、start、stop、deploy 等）：
  1. 先完整展示即将执行的**完整命令**
  2. 询问：“确认要执行这条命令吗？(yes/no)”
  3. 只有用户回复 **yes** 后才真正执行
- 删除/销毁类操作额外提醒风险。

## 示例交互
**用户**：列出我的所有 Vultr 实例  
**Agent**：直接执行 `vultr-cli instance list --output json` 并展示结果

**用户**：创建一个 VPS  
**Agent**：即将执行：`vultr-cli instance create --region nrt --plan vc2-1c-2gb --os 387`  
确认要执行这条命令吗？(yes/no)

## 常用模板
- 账号信息：`vultr-cli account get`
- 实例列表：`vultr-cli instance list`
- 创建实例：`vultr-cli instance create --region xxx --plan xxx --os xxx`
- 对象存储：`vultr-cli object-storage list`
- 配置 API Key：`export VULTR_API_KEY=你的密钥`

## 提示
- 未认证时提示用户设置 `export VULTR_API_KEY=xxx` 或运行 `vultr-cli account get` 测试。