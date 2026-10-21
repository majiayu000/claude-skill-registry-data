---
name: portfolio-github-workflow
description: Safely inspect, edit, validate, and publish an existing video portfolio or static GitHub Pages site. Use only for repository-backed portfolio changes or deployment checks; not for generic websites, backend services, or unrelated Git operations. For visual and loading-performance review use video-portfolio-performance instead.
version: 1.0.0
---

# Portfolio GitHub Workflow

Use this entrypoint only when an existing portfolio/static-site repository and an authorized GitHub Pages change are in scope. Preserve the public URL and history. Read the mode-specific reference only when needed:

- Before editing or media replacement: [references/inspect-media.md](references/inspect-media.md)
- Before publishing: [references/publish.md](references/publish.md)
- After a layout/media change: [references/validate.md](references/validate.md)

## Core gates

1. Resolve the real worktree with `git rev-parse --show-toplevel`; preserve unrelated changes.
2. Verify authorship/labels and never invent clients, metrics, or project claims.
3. Keep source media, repository state, and deployed Pages state separately verifiable.
4. Use dry-run before any push; stop on authentication, policy, or diverged-remote failures.

## Before / After

Before, a portfolio update is one command away from an accident:

```
git add -A; git commit -m "update"; git push origin main
# 鉴权失败、403、远端已分叉 —— 全都等到推完才知道
```

After, the change is inspected before anything leaves the machine:

```
scripts/safe_publish.ps1 -DryRun   # 列出将要改动的文件与发布动作，不做任何写操作
scripts/safe_publish.ps1           # 确认后再执行，遇到鉴权 / 403 / 远端分叉立即停止
```

The public URL, the commit history, and the existing media are preserved in both runs.
