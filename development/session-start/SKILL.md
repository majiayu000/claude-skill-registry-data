---
name: session-start
description: Starts a session and generates a startup prompt for use in the target project repo. Use when user wants to start a session, generate a startup prompt, or begin working on a project.
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Session Start（开 Session）

> **使用位置**：vibehub-testing
>
> **用途**：通过对话确定 session 内容，最终输出一个可以带到实际项目 repo 使用的「启动 prompt」。

## 触发条件

用户说类似：
- "我要开一个 session"
- "帮我生成一个启动 prompt"
- "我想在 XXX 项目上开始干活"
- "生成启动 prompt"

## 执行步骤

### Step 1: 检查是否有 prep

查看 `sessions/` 目录，是否有对应项目的 prep：
- 如果有，阅读 `prep/raw_dump.md` 提取信息
- 如果没有，进入 Step 2 对话收集

### Step 2: 对话收集信息

询问用户关键问题：

1. **项目名/代号**：这个项目叫什么？
2. **目标**：你这次想做什么？
3. **背景信息**：
   - 有什么相关的 Drive 文档？
   - 有什么相关的代码/文件？
   - 需要我了解什么背景？
4. **目标项目 repo**：代码仓库在哪里？（路径）

### Step 3: 对话澄清

通过对话确认：
- 项目的核心目标
- 需要参考的资料
- 工作范围和边界
- 任何特殊要求

### Step 4: 生成 session.md

在 `sessions/{timestamp}-{project}/` 下生成或更新 `session.md`：

```markdown
---
session_id: {timestamp}-{project}
project_handle: {project}
target_repo: {目标项目路径}
status: ready
created_at: {ISO timestamp}
---

# Session: {项目名}

## 目标
{这次要做什么}

## 背景信息
{相关的 Drive 文档、代码位置、关键概念}

## 工作范围
{明确要做什么、不做什么}

## 启动 Prompt
见下方独立输出
```

### Step 5: 生成「启动 Prompt」

**这是核心输出**——一段可以直接复制到项目 repo 的 Claude Code 会话中使用的 prompt。

**重要：启动 Prompt 必须包含 Drive 搜索指引！**

输出格式：

```
---

## 启动 Prompt（复制到项目 repo 使用）

### 项目背景

{项目是什么、要做什么}

### Drive 文档（重要！）

在开始工作前，请让我提供以下 Drive 文档的内容：

| 文档 | Drive 路径 | 用途 |
|------|-----------|------|
| {文档1} | My Drive/Projects/{项目}/xxx | {用途} |
| {文档2} | My Drive/Projects/{项目}/references/xxx | {用途} |

**搜索关键词**：{keyword1}, {keyword2}, {keyword3}

> 注意：当你需要这些文档时，请告诉我「请提供 XXX 文档的内容」，我会从 Drive 复制给你。

### 代码位置

- 入口文件：{入口文件路径}
- 关键目录：{目录}
- 配置文件：{配置}

### 本次目标

{具体要完成的任务}

### 工作方式

1. **先读 Drive 文档**：告诉我你需要哪些文档，我会提供内容
2. 阅读相关代码，理解现状
3. 制定实现计划，让我确认
4. 逐步实现，每完成一步汇报
5. 遇到问题及时沟通

### 开始

请先告诉我你需要阅读哪些 Drive 文档，然后我会提供内容。

---
```

### Step 6: 引导用户

告诉用户：
> session.md 已生成：`sessions/{path}/session.md`
>
> **启动 Prompt 已包含 Drive 搜索指引。**
>
> 请复制上面的「启动 Prompt」，到项目 repo `{target_repo}` 打开 Claude Code，贴入开始工作。
>
> 当 Claude 需要 Drive 文档时，你可以：
> 1. 在 Drive 搜索相关关键词
> 2. 打开文档，复制内容给 Claude

## 输出清单

1. `sessions/{timestamp}-{project}/session.md`
2. **启动 Prompt**（包含 Drive 搜索指引）
3. **Drive 关键词清单**
4. 下一步指引
