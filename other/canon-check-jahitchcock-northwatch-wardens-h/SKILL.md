---
name: canon-check
description: Check Northwatch Wardens content for canonical consistency. Use when reviewing adventure text, NPC descriptions, world-building, or player-facing material for geography errors, unknown NPCs, broken link rules, or tone issues. Also auto-activates when the user asks to review, proofread, or validate campaign content.
argument-hint: [file-path|"check all"|paste-text]
allowed-tools: Read Grep Glob
---

Target: **$ARGUMENTS**

Scope: file path → that file | pasted text → analyze directly | "check all"/no arg → all `.md` in `Season 1/` and `World Building/` (exclude `DMEyesOnly/` unless asked).

Load [canonical-data.md](references/canonical-data.md).

**Parallel — always:** `validate-canon` (geography + NPC names)
**Parallel — if files are in `build/players-guide-toc.json`:** scan for `[text](path.md)` links and repo path references
**Only if tone review requested:** flag patterns from [canonical-data.md](references/canonical-data.md) tone section

For "check all": spawn one subagent per file.

Report findings grouped by check type (file, line, flagged text, suggestion). Nothing flagged → `No canonical issues found.`

If player-facing link issues found: offer to convert links to chapter references. Do not edit without approval.

`skill-self-review canon-check` (add `--agentic` if running inside an agent)
