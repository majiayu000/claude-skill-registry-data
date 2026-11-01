---
name: tech-review
description: Run a senior tech lead review of Pieceful's design docs, save the findings to the private notes, and walk the owner through them. Use for /tech-review, at phase checkpoints, or before approving a phase.
argument-hint: "[scope, e.g. docs/product/ or 'all']"
---

# /tech-review: senior tech lead review

1. **Scope:** the argument (a folder, file, or phase), or `all` (`AGENTS.md` + `docs/`) if none.
2. **Run the `tech-lead` agent** on that scope. It starts with a fresh context, so pass only the scope and where the private notes are. Don't pass your own opinions.
3. **Save the report** to the private notes as `research/reviews/YYYY-MM-DD-<scope>.md`:
   - header: date, scope, the current phase from `planning/progress.md`
   - the agent's output unchanged
   - add the review to `research/reviews/README.md`
4. **Walk the owner through it:** a short summary in chat, then ask the owner's decisions with AskUserQuestion (options + recommendation), blockers first.
5. **Record the outcome:**
   - answers → `planning/open-questions.md` (Answered)
   - accepted fixes → a note in the review file (`→ fix agreed` / `→ won't fix: reason`)
   - new ideas → `/idea`
6. Make agreed fixes only after the owner confirms. Don't commit.
