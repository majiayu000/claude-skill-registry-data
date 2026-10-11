---
name: pr-description
description: Generates a reviewer-friendly pull request description from the branch diff. Use when opening a PR, when asked to summarize a branch, or before requesting review.
---

# PR Description

Produce a PR description a busy reviewer can act on in under a minute.

## When to use this skill

- The user asks to open a PR or "write the PR description".
- A branch is ready and needs a summary before review.

## How to use it

1. Collect the real change surface — never write from memory:
   ```bash
   git log main..HEAD --oneline
   git diff main...HEAD --stat
   ```
2. Structure the description:
   - **What** — 1-2 sentences: the user-visible outcome, not the mechanics.
   - **Why** — the problem or ticket this solves; link issues.
   - **How** — only the non-obvious decisions (tricky trade-offs, rejected alternatives). Skip a file-by-file tour; the diff already shows it.
   - **Testing** — what was actually run (commands + result), not what "should" pass.
   - **Risk / rollback** — what could break and how to revert.
3. Call out anything a reviewer must look at extra carefully (migrations, auth changes, deletions).

## Decision tree

- Diff > ~800 lines → open with a "review order" hint (which files to read first).
- Pure dependency bump → compress to What + changelog link + test evidence.
- Breaking API change → put a **BREAKING** banner at the top with the migration step.

## Done means

The description answers what/why/testing without the reviewer opening the diff, and every claim in "Testing" corresponds to a command that was actually executed.

---

Part of [awesome-antigravity-skills](https://github.com/LichAmnesia/awesome-antigravity-skills). Browse more Agent Skills at [orangebot.ai/skills](https://orangebot.ai/skills).
