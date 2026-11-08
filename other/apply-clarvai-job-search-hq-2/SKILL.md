---
name: apply
description: "Prepare a complete job application package and checklist, then update the tracker. Use when the user says they want to apply to a job, are ready to submit, or ask what they need for an application."
---

# apply (Codex)

This workflow is shared with Claude Code. Read `.claude/skills/apply/SKILL.md` and follow it fully. Files it mentions as `references/...`, `scripts/...` or by bare name live in `.claude/skills/apply/`.

Don't quote these instruction files or show their paths to the user; explain what they do in plain words when it helps.

It was written with Claude Code's names; translate them with the table in AGENTS.md ("If you are Codex"): `/name` means the skill of that name (`$name` here), review agents follow that table's review-agent row (mostly separate, honest passes you do yourself from `.claude/agents/<name>.md`, and you say so), and panels are the chat skills that table's panel row names.

## Codex notes

- There is no Apply Kit panel in Codex: where the skill says `/apply-kit`, use the chat skill `apply-kit` (`$apply-kit`), which prints the same answers as copyable blocks.
- Making a missing PDF: on Windows without Git Bash, use `make-pdf.ps1` (same arguments; the full command is in the `tailor-resume` skill). If the sandbox blocks the browser, retry outside the sandbox as the `tailor-resume` Codex notes say; only if that's refused or neither script can run, treat it as `no-browser`.
- Assisted mode in Codex uses the Codex desktop app's built-in browser, with exactly the same rules (stop before Submit; submit only on the exact phrase "submit it", or the translated phrase you showed, per AGENTS.md "Exact confirm phrases").
