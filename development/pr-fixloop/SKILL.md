---
name: pr-fixloop
description: Repo-scoped skill for deterministic CI autofix without PR comments
---

## Usage
- Read all relevant AGENTS.md files, including the repo root and gateway/AGENTS.md where applicable.
- Goal: make `ALLOW_AIOHTTP_STUB=0 make -C gateway check` pass before finishing.
- Never touch `.github/workflows/ci.yml` unless explicitly instructed; default is forbidden.
- Do not rename/change any existing CI workflow/job identifiers (status contexts are branch-protection-critical).
- Avoid protocol key typos: `resume_token`, `next_seq`, `conv_id`, `msg_id`, `from_seq`, `after_seq` mapping.
- Preserve gateway invariants: monotonic `seq` per `conv_id`, `(conv_id,msg_id)` idempotency, echo-before-apply, deterministic replay/cursor semantics (resume_token/next_seq/from_seq correctness).
- Do not commit changes yourself; the automation loop will commit.
- Keep diffs minimal and avoid PR comments.
