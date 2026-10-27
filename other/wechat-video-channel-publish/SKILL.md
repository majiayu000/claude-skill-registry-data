---
name: wechat-video-channel-publish
description: Use when the user wants to log into 微信视频号, validate cookie state, upload videos, set scheduled publish time, fill long description, set a cover image, or save drafts through a local Playwright CLI.
---

# WeChat Video Channel Publish

This skill packages a focused 微信视频号 publishing workflow for local agent execution.

Use it when the task is specifically about:

- 视频号扫码登录
- 上传短视频
- 设置标题、标签、正文长描述
- 设置封面图
- 定时发布
- 保存草稿（best effort；平台 UI 可能在部分状态下拒绝）
- 发布后补评论

## Quick Start

1. Read `references/runtime-requirements.md`.
2. Build the CLI if `dist/cli.js` does not exist.
3. Run `tencent login` or `tencent check`.
4. Run `tencent upload` with absolute video and cover paths.
5. If the task uses a publishing queue, first normalize it into direct CLI arguments.
6. Before any public repo push, read `references/privacy-checklist.md`.

## Workflow

### Step 1: Prepare Runtime

- Run all commands in the repo root.
- If needed, execute:
  - `npm install`
  - `npx playwright install chromium`
  - `npm run build`

### Step 2: Login or Reuse Cookie

- For first-time login:
  - `node dist/cli.js tencent login --account <name>`
- For validation:
  - `node dist/cli.js tencent check --account <name>`

The cookie file is stored outside the repo by default and must never be committed.

### Step 3: Publish a Video

- Read `references/publish-workflow.md`.
- Use absolute paths for `--file` and `--cover`.
- Supported fields:
  - `--title`
  - `--tags`
  - `--caption`
  - `--cover`
  - `--pinned-comment`
  - `--schedule`
  - `--category`
  - `--draft`

### Step 4: Validate Carefully

- Prefer `--draft` when verifying a new selector path or runtime change, but do not combine it with `--schedule`.
- Treat `cover` and `pinned-comment` as runtime-sensitive features.
- If UI changes break these steps, keep login and upload logic intact and narrow the failure to the affected selector flow.

### Step 5: Repo Hygiene

- Keep cookies, screenshots, local logs, and temporary exports out of git.
- When sharing publicly, include only reusable code, templates, and references.

## Resource Loading Rules

- Read `references/runtime-requirements.md` before execution.
- Read `references/publish-workflow.md` when mapping a publishing plan into CLI arguments.
- Read `references/privacy-checklist.md` before creating or updating a public repository.

## Output Expectations

- The agent should execute the real CLI when feasible.
- The agent should report what fields were actually attempted at runtime.
- If a selector-dependent step is flaky, the agent should say exactly which sub-step failed:
  - login
  - upload
  - caption
  - cover
  - comment

## Guardrails

- Do not print or commit cookie JSON.
- Do not embed user-specific absolute paths in committed docs except as obvious placeholders.
- Do not claim comment pinning is fully reliable unless it was verified in the current session.
- Do not claim `--draft + --schedule` is supported; use `--schedule` without `--draft` for real scheduled publishing.
