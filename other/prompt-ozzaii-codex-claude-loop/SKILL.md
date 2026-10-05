---
name: prompt
description: Send an additional request to the exact Codex session for an implemented codex-claude-loop lane, sequenced behind its writer lock
argument-hint: <slug> <additional request>
allowed-tools: Bash, Read
---

Load the `codex-claude-loop` skill and source its bundled
`lib/codex-claude-loop.sh`. Split `$ARGUMENTS` into the first word as the slug and the
entire remaining text as one request, then call:

```bash
cl_prompt <slug> "<additional request>"
```

Do not call `codex exec resume` directly. `cl_prompt` resumes the stored session id,
holds the same writer lock as `cl_impl` and `cl_revise`, and waits behind a running lane
instead of starting a competing Codex process in the worktree.

The lane must already have a valid approved plan and a successful implementation marker.
The follow-up is a writer phase: it clears any standing review approval, restores the
implementation marker only after Codex exits cleanly, and prints Codex's final response.
After it succeeds, re-review before release.
