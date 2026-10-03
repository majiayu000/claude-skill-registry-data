---
name: resolving-merge-conflicts
description: "Use when you need to resolve an in-progress git merge/rebase conflict."
license: MIT
---

<!--
  Source: https://github.com/mattpocock/skills
  Pinned commit: c55ee46073ed923f86ce59a5eb3b6d895095d1b7 (2026-09-18)
  Upstream path: skills/engineering/resolving-merge-conflicts/
  License: MIT (c) 2026 Matt Pocock -- full text in LICENSE next to this file
  Forge vendor note: frontmatter license: MIT key and this provenance block added; agents/openai.yaml (Codex UI metadata, no function in Claude Code) not shipped; everything else verbatim. Safety read: runs no destructive git -- it forbids aborting and finishes with a normal local commit or rebase continue; no push, reset, clean or branch deletion.
  Reviewed for prompt-injection patterns, hidden/zero-width/bidi/control unicode, network use and deletes by build-boss, 2026-09-24 -- clean; every upstream file sha256-verified against the pinned-commit manifest before copying.
-->

1. **See the current state** of the merge/rebase. Check git history, and the conflicting files.

2. **Find the primary sources** for each conflict. Understand deeply why each change was made, and what the original intent was. Read the commit messages, check the PRs, check original issues/tickets.

3. **Resolve each hunk.** Preserve both intents where possible. Where incompatible, pick the one matching the merge's stated goal and note the trade-off. Do **not** invent new behaviour. Always resolve; never `--abort`.

4. Discover the project's **automated checks** and run them, typically typecheck, then tests, then format. Fix anything the merge broke.

5. **Finish the merge/rebase.** Stage everything and commit. If rebasing, continue the rebase process until all commits are rebased.
