---
layout: default
title: Claude Skill
nav_order: 2
parent: Spec Driven Development
permalink: /spec/github-spec-kit
---


## Claude Skills 集成

### 什么是 Claude Skills？

[Anthropic Claude Skills](https://github.com/anthropics/skills) 是包含指令、脚本和资源的文件夹，Claude 动态加载以提高专业任务的性能。

**主要特征：**
- 自包含的技能模块
- 用于元数据的 YAML 前置元数据
- 用于 AI 代理的 Markdown 指令
- 可包含脚本、模板和资源

### AutoDev 如何集成 Claude Skills

AutoDev 从多个位置发现 Claude Skills：

**发现位置：**

1. **项目级技能**：项目根目录中包含 `SKILL.md` 的目录
2. **用户级技能**：`~/.claude/skills/` 目录
3. **嵌套技能**：技能目录中的子目录

**发现过程：**

1. AutoDev 扫描配置的位置查找 `SKILL.md` 文件
2. 解析 YAML 前置元数据获取技能元数据
3. 将技能注册为 `/skill.<名称>` 命令
4. 提供带描述的智能提示

**技能结构：**

```
my-skill/
├── SKILL.md              # 主技能定义
├── examples/             # 示例文件（可选）
├── templates/            # 模板文件（可选）
└── scripts/              # 辅助脚本（可选）
```

### 技能定义格式

```markdown
---
name: my-skill-name
description: 清晰描述此技能的功能和使用时机
version: 1.0.0
author: 你的名字
tags:
  - 类别1
  - 类别2
---

# 我的技能名称

## 目的

[解释此技能的作用和使用时机]

## 指令

[AI 代理的详细指令]

## 示例

### 示例 1：基本用法
```
输入：...
输出：...
```

### 示例 2：高级用法
```
输入：...
输出：...
```

## 指南

- 指南 1：...
- 指南 2：...
- 指南 3：...

## 限制

- 限制 1：...
- 限制 2：...
```

### Anthropic 提供的示例技能

#### 文档技能

```devin
# 创建带修订跟踪的 Word 文档
/skill.docx 创建项目提案，包含：
- 执行摘要
- 技术方法
- 时间表和里程碑
- 预算明细
启用修订跟踪以供审查

# 从 PDF 提取数据
/skill.pdf 从 invoice.pdf 提取所有表单字段并输出为 JSON

# 创建 PowerPoint 演示文稿
/skill.pptx 创建关于我们 Q4 结果的 10 张幻灯片演示，包含：
- 标题幻灯片
- 执行摘要
- 收入图表
- 关键指标
- 未来展望

# 分析 Excel 电子表格
/skill.xlsx 分析 sales-data.xlsx 并创建：
- 按地区的数据透视表
- 月度趋势图
- 前 10 产品表
```

#### 开发技能

```devin
# 构建 React 工件
/skill.artifacts-builder 创建仪表板，包含：
- 实时数据可视化
- 使用 Tailwind 的响应式布局
- 深色模式支持
- shadcn/ui 组件

# 测试 Web 应用
/skill.webapp-testing 测试 http://localhost:3000 的登录流程：
- 验证表单验证
- 测试成功登录
- 测试错误处理
- 检查响应式设计

# 创建 MCP 服务器
/skill.mcp-builder 为 GitHub API 创建 MCP 服务器，功能包括：
- 列出仓库
- 创建问题
- 管理拉取请求
- 处理身份验证
```

#### 创意技能

```devin
# 生成算法艺术
/skill.algorithmic-art 使用以下方式创建生成艺术：
- 流场算法
- 1000 个粒子的粒子系统
- 种子随机性（种子：42）
- 调色板：蓝色和紫色

# 设计画布
/skill.canvas-design 为我们的产品发布创建极简海报：
- 尺寸：1920x1080
- 品牌颜色
- 简洁排版
- 导出为 PNG 和 PDF
```
