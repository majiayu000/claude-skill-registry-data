---
name: conventional-commits
description: Create Git commits using Conventional Commits with a scoped Chinese subject and a concise bullet-list body. Use when Codex is asked to commit changes, prepare a commit message, amend a commit message, or review whether a proposed commit follows the required format.
---

# Conventional Commits

## Workflow

1. Inspect `git status`, staged and unstaged diffs, and recent commit style.
2. Do not stage unrelated files. Never include secrets, generated output, dependencies, local data, or user changes unrelated to the requested work.
3. Run the verification appropriate to the changed files before committing.
4. Choose one commit type and an optional concise scope.
5. Write the subject and body in Chinese unless the repository explicitly uses another language.
6. Run `git diff --cached --check` and review `git diff --cached --stat` before committing.
7. Create the commit non-interactively and report its hash and verification result.

## Message Format

Use exactly this structure when the change needs a body:

```text
type(scope): 简短中文摘要

- 具体变更一
- 具体变更二
- 具体变更三
- ...
- 具体变更n
```

Keep the subject imperative, specific, and free of a trailing period. Separate the body from the subject with one blank line. Use `- ` bullets that describe delivered behavior or artifacts, not the development process.

For a genuinely small change, a subject-only commit is acceptable:

```text
fix(auth): 修复过期令牌未被拒绝的问题
```

## Types

- `feat`: Add user-visible behavior.
- `fix`: Correct faulty behavior.
- `docs`: Change documentation only.
- `refactor`: Restructure code without changing behavior.
- `test`: Add or revise tests only.
- `build`: Change build tools or dependencies.
- `ci`: Change automation workflows.
- `perf`: Improve performance.
- `style`: Change formatting without changing behavior.
- `chore`: Perform repository maintenance not covered above.
- `revert`: Revert an earlier commit.

Use a lowercase scope naming the affected subsystem, such as `api`, `auth`, `mcp`, `frontend`, or `docs`. Omit the scope when no single subsystem accurately describes the change.

## Breaking Changes

Add `!` before the colon and a `BREAKING CHANGE:` footer when compatibility is intentionally broken:

```text
feat(api)!: 调整文档查询参数

- 要求调用方同时传入工作区和知识库 ID

BREAKING CHANGE: 旧版仅传 knowledge_base_id 的调用方式不再受支持。
```

## Example

```text
docs(api): 添加核心TCP协议和管理API文档

- 定义MCNP Core TCP协议v1规范，包括连接、安全、帧格式
- 详细描述会话建立、消息模型、各种方法接口和数据结构
- 添加HTTP错误模型和错误码映射规范
- 包含环境管理、一键搭建、配置识别等功能API文档
- 初始化Rust项目基础结构和.gitignore配置
```

Before using `docs`, confirm the staged changes are documentation-only. If source code or project scaffolding is included, split the work into coherent commits or choose the type that represents the primary delivered change.
