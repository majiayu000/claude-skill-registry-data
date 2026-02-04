---
name: ux-design-gemini
description: "Create UX designs using memex-cli with Gemini backend. Use when (1) Generating user flows and wireframes, (2) Creating UI component specifications, (3) Designing interaction patterns, (4) Building design system documentation, (5) Producing responsive layout guides."
---

# UX Design with Gemini

Use memex-cli to leverage Gemini for UX design tasks with memory and replay support.

## Quick Start

### Generate User Flow

```bash
memex-cli run --backend "gemini" --prompt "设计一个电商App的用户购物流程，包含浏览、加购、结算、支付的完整流程图" --stream-format "text"
```

### Create Wireframe Spec

```bash
memex-cli run --backend "gemini" --prompt "为登录注册页面创建线框图规格说明，包含布局、组件位置、交互状态" --stream-format "text"
```

### Design Component System

```bash
memex-cli run --backend "gemini" --prompt "设计一套移动端UI组件规范，包含按钮、输入框、卡片、导航栏的样式定义" --stream-format "jsonl"
```

## Common UX Tasks

### 用户研究

```bash
memex-cli run --backend "gemini" --prompt "为健身App设计用户画像和使用场景分析" --stream-format "text"
```

### 信息架构

```bash
memex-cli run --backend "gemini" --prompt "设计一个SaaS后台管理系统的信息架构和导航结构" --stream-format "text"
```

### 交互设计

```bash
memex-cli run --backend "gemini" --prompt "设计表单提交的交互反馈方案，包含加载、成功、错误状态" --stream-format "text"
```

### 响应式布局

```bash
memex-cli run --backend "gemini" --prompt "设计一个产品详情页的响应式布局方案，适配手机、平板、桌面端" --stream-format "text"
```

## Workflow Pattern

### 1. 初始设计

```bash
memex-cli run --backend "gemini" --prompt "<设计需求>" --stream-format "jsonl"
```

### 2. 查看事件日志

```bash
memex-cli replay --events ./run.events.jsonl --format text
```

### 3. 迭代优化

```bash
memex-cli resume --run-id <RUN_ID> --backend "gemini" --prompt "基于上一轮设计，优化<具体方面>" --stream-format "text"
```

## Output Formats

- `text`: 可读的设计文档，适合直接阅读
- `jsonl`: 结构化输出，适合后续处理或存档

## Tips

1. 复杂设计任务拆分为多个步骤，利用resume连续迭代
2. 使用jsonl格式保存完整设计过程，便于回溯
3. 在prompt中明确指定输出格式要求（如Markdown表格、列表等）