---
name: repo-asset-management
description: Durable repo asset management for visual evidence, backlog attachments, and repo-provider asset fallbacks.
---

# Repo Asset Management

Use when a workflow needs durable links for approved design assets, prototype screenshots, backlog evidence, or PR before/after visuals.

## Steps

1. Prefer backlog attachments.
   - backlog attachments preferred when the backlog provider supports durable files.
2. Fall back to repo-provider storage.
   - Use repo-provider assets when backlog attachments are unavailable, size-limited, visibility-mismatched, or unsuitable for PR/review reuse.
3. Select provider from `.devpunks/settings.json`; if absent, infer only from existing repo/provider hints and surface conflicts.
4. Load exactly one provider reference:
   - GitHub: [references/github.md](references/github.md)
   - GitLab: [references/gitlab.md](references/gitlab.md)
   - Azure: [references/azure.md](references/azure.md)
   - Bitbucket: [references/bitbucket.md](references/bitbucket.md)
5. Return stable URLs plus original local filenames to the caller.

## Rules

- Never hand off temp file paths, transient browser URLs, or local screenshots as durable evidence.
- Do not copy provider commands into caller skills; link this skill instead.
- If upload cannot run, record the blocker and preserve the local file path only as pending evidence.
