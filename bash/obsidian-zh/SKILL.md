---
name: obsidian
description: 使用 obsidian-cli 管理 Obsidian 笔记库，支持日常笔记管理、任务追踪和内容组织。适用于自动化笔记工作流、任务记录和知识管理。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["obsidian"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "obsidian-cli-manager",
              "bins": ["obsidian"],
              "label": "安装 Obsidian CLI (npm)",
            },
          ],
      },
  }
---

# Obsidian 笔记管理技能

使用 `obsidian` CLI 工具与 Obsidian 笔记库交互，实现自动化笔记管理和任务追踪。

## 初始化配置

首次使用需要配置 Obsidian 笔记库路径：

```bash
# 交互式配置
obsidian init

# 或直接指定笔记库路径
obsidian init --vault /path/to/your/vault
```

## 日常笔记管理

打开或创建今天的日常笔记（交互模式）：

```bash
obsidian daily
```

查看笔记库中的所有 Markdown 文件：

```bash
obsidian files
```

浏览模式 - 在笔记库中浏览文件：

```bash
obsidian view
```

## 任务管理

查看和管理集中式任务日志中的任务：

```bash
obsidian tasks
```

## 配置管理

显示当前配置或创建/编辑配置文件：

```bash
obsidian config
```

## 内容组织功能

**分区组织** - 内容通过前缀自动路由到相应分区：

- `[] 任务` → 任务分区（复选框格式）
- `- 想法` → 想法分区（列表格式）
- `? 问题` → 问题分区（列表格式）
- `! 洞察` → 洞察分区（列表格式）

**任务日志** - 任务自动记录到集中式文件，并包含反向链接

**艾森豪威尔标签** - 带颜色优先级高亮：

- `#do`（红色）- 紧急且重要
- `#delegate`（橙色）- 紧急但不重要
- `#schedule`（蓝色）- 重要但不紧急
- `#eliminate`（灰色）- 不紧急也不重要

## 使用场景

- **日常笔记自动化** - 快速创建和管理每日笔记
- **任务追踪** - 集中管理任务和待办事项
- **知识管理** - 组织和分类笔记内容
- **工作流优化** - 通过分区和标签系统提高效率
- **团队协作** - 标准化笔记格式和任务管理流程

## 安装要求

确保已安装 Node.js (>=14.0.0)：

```bash
# 通过 npm 全局安装
npm install -g obsidian-cli-manager

# 或从源码安装
git clone https://github.com/caneppelevitor/obsidian-cli.git
cd obsidian-cli
npm install
npm link
```

## 提示

- 使用 `obsidian init` 命令首次配置笔记库路径
- 日常笔记支持分区自动组织功能
- 任务会自动记录到集中式任务日志
- 使用艾森豪威尔标签进行优先级管理
- 可以在 tmux 中配置快捷键快速打开（可选）

## 高级功能

### 与 OpenClaw 集成

通过 OpenClaw 自动化 Obsidian 工作流：

```bash
# 创建今天的日常笔记
obsidian daily

# 列出所有笔记文件
obsidian files --format json

# 查看任务列表
obsidian tasks
```

### 自定义配置

配置文件位于 `~/.obsidian-cli/config.yaml`，可以自定义：

- 笔记库路径
- 日常笔记模板
- 分区设置
- 任务日志位置
