---
name: sanitize-git-history
description: 'Audit Git history for confidential words by automatically running the contextual sensitive-history scanner against terms or a.sensitive.replacements.local.txt (phase 1), then rewrite a fresh clone with git filter-repo, re-audit, restore remotes, and stop before pushing (phase 2). Use when the user asks to inspect sensitive history, sanitize a repo, scrub confidential terms, or make a repository publishable.'
---

Read and follow [the canonical instruction](../../../../../../../../git/llm-shared/instructions/sanitize-git-history.md)
