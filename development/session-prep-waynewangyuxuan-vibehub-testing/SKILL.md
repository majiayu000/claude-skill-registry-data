---
name: session-prep
description: Prepares a session by organizing scattered information. Use when user says they have information to organize, want to prepare a session, or mentions "prep".
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Session Prep（准备阶段）

> **使用位置**：vibehub-testing
>
> **用途**：当用户有零散信息要整理时，帮助创建 session 文件夹并整理信息。

## 触发条件

用户说类似：
- "我有一堆关于 XXX 的信息要整理"
- "帮我准备一个 session"
- "我想开始搞 XXX，先帮我整理一下"

## 执行步骤

### Step 1: 询问项目名

如果用户没有提供项目名，先询问：
> 这个 session 是关于什么项目/主题的？请给我一个代号（如 sunset-pipeline）

### Step 2: 创建 Session 文件夹

创建以下结构：

```
sessions/{YYYY-MM-DD-HHMM}-{project_handle}/
  prep/
    raw_dump.md
    to_upload/
```

时间戳格式：`YYYY-MM-DD-HHMM`（如 `2025-12-06-1430`）

### Step 3: 初始化 prep/raw_dump.md

```markdown
---
prep_id: {timestamp}-{project_handle}
status: gathering
---

# Session 准备：{项目名}

## 1. 原始信息 Dump

（用户的零散信息会放在这里）

## 2. 相关文件清单

| 文件名 | 位置 | 类型 | 备注 |
|--------|------|------|------|

## 3. 待整理
```

### Step 4: 引导用户 Dump 信息

告诉用户：
> 文件夹已创建：`sessions/{timestamp}-{project}/`
>
> 请把你手头的信息 dump 给我，可以是：
> - 聊天记录、笔记
> - 想法、TODO
> - 相关链接、文件路径
> - 任何零散的东西

### Step 5: 整理信息

当用户 dump 完信息后：

1. **分类整理**，更新 `prep/raw_dump.md`：
   - 核心概念/目标
   - 关键参考资料
   - 待办/行动项
   - 不确定/需澄清

2. **建议 Drive 结构**：
   ```
   My Drive/
     Projects/
       {项目名}/
         README.md
         references/
         notes/
   ```

3. **生成待上传内容**到 `prep/to_upload/`

### Step 6: Drive 上传（重要！）

**这一步必须完成，不能跳过。**

1. **列出待上传文件清单**，告诉用户：
   ```
   请将以下文件上传到 Google Drive：

   | 本地文件 | 上传到 Drive 路径 |
   |----------|-------------------|
   | prep/to_upload/README.md | My Drive/Projects/{项目}/README.md |
   | prep/to_upload/xxx.pdf | My Drive/Projects/{项目}/references/xxx.pdf |
   | ... | ... |

   上传完成后，请告诉我「已上传」。
   ```

2. **等待用户确认**上传完成

3. **记录 Drive 路径**，更新 `prep/raw_dump.md` 添加：
   ```markdown
   ## Drive 文件位置

   | 文件 | Drive 路径 | 用途 |
   |------|-----------|------|
   | README.md | My Drive/Projects/{项目}/README.md | 项目概览 |
   | xxx.pdf | My Drive/Projects/{项目}/references/xxx.pdf | 参考资料 |
   ```

4. 更新状态为 `uploaded`

### Step 7: 完成并引导下一步

1. 更新 `prep/raw_dump.md` 状态为 `ready_for_session`
2. 提示用户：
   > prep 完成！文件已整理到 Drive。
   >
   > 接下来请说「开始生成启动 prompt」或使用 session-start skill。
   >
   > 在项目 repo 工作时，你可以让 Claude 搜索以下 Drive 关键词：
   > - {关键词1}
   > - {关键词2}

## 输出

1. `sessions/{timestamp}-{project}/` 文件夹结构
2. `prep/raw_dump.md`：整理好的信息 + Drive 路径记录
3. `prep/to_upload/`：已上传到 Drive 的内容
4. **Drive 搜索关键词**：供后续在项目 repo 使用
