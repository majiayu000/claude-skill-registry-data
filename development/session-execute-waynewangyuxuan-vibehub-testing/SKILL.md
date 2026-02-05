---
name: session-execute
description: Executes work in a project repo using a startup prompt. Use when user pastes a startup prompt or asks to begin executing a session. This skill is meant for use in project repos, not in vibehub.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Session Execute（执行 Session）

> **使用位置**：实际项目 repo（不是 vibehub-testing）
>
> **用途**：配合 `session-start` 生成的启动 prompt，在项目 repo 里真正干活。

## 触发条件

用户在项目 repo 的 Claude Code 会话中：
- 贴入了启动 prompt
- 说「开始执行」「按这个 prompt 工作」等

## Claude 行为约定

### 1. 先理解，再行动

**开始工作前：**
- 阅读启动 prompt 里提到的入口文件/文档
- 理解项目现状和目标
- 输出你的理解，让用户确认

**格式：**
```
## 我的理解

**项目现状：**
- ...

**本次目标：**
- ...

**我的计划：**
1. 第一步：...
2. 第二步：...

请确认这个理解是否正确？
```

### 2. 制定计划，逐步执行

**每个大任务前：**
- 制定实现计划
- 拆分成小步骤
- 让用户确认后再开始

**执行时：**
- 每完成一步，简短汇报
- 遇到问题及时沟通
- 不确定的地方先问

### 3. 代码修改原则

- **先读后改**：修改任何文件前，先阅读理解
- **最小改动**：只改必要的部分，不做额外重构
- **保持风格**：遵循项目现有的代码风格
- **及时提交**：完成一个功能点后建议 commit

### 4. 沟通方式

**进度汇报：**
```
完成：XXX
进行中：YYY
待做：ZZZ
```

**遇到问题：**
```
问题：...
可能的解决方案：
1. ...
2. ...
你觉得哪个更好？
```

**需要确认：**
```
我打算这样做：...
这样 OK 吗？
```

### 5. 与 Drive 的交互

如果启动 prompt 里提到了 Drive 文档：
- 让用户提供相关内容（搜索结果、文档内容）
- 根据内容调整工作计划
- 如果需要更多信息，明确告诉用户去哪里找

## 工作流程

```
1. 接收启动 prompt
   |
2. 阅读相关文件，输出理解
   |
3. 制定计划，用户确认
   |
4. 逐步执行
   +-- 完成一步 -> 汇报
   +-- 遇到问题 -> 沟通
   +-- 需要确认 -> 询问
   |
5. 完成任务，总结
```

## 注意事项

1. **这是通用 skill**：适用于任何项目，具体内容由启动 prompt 决定
2. **保持沟通**：宁可多问，不要自作主张
3. **及时反馈**：让用户随时知道进度
4. **灵活应变**：根据实际情况调整计划
