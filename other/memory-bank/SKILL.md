---
name: memory-bank
description: Repo-committed project memory — decisions, context, solved mysteries as distilled one-fact files; recall before related work. Trigger when starting work in a previously-touched area, after solving something non-obvious, on lasting decisions, or "remember this" / "why did we do X".
---

# Memory Bank — Durable Project Knowledge

The missing memory layer: knowledge that must outlive sessions AND machines AND assistants. Lives in the repo (`memory-bank/` at project root), committed to git, readable by humans. Distilled facts, never transcripts — recall should cost tens of tokens, not thousands.

**Division of labor (don't duplicate the other layers):**
- `handover.md` = *current state* (what's in flight, next steps) — volatile, overwritten.
- Skill `learnings.md` = *technique knowledge* (how to do X well) — per-skill, project-agnostic.
- Auto-memory (assistant-level) = user preferences and cross-project facts.
- **memory-bank = this project's durable truths**: decisions + why, domain context, constraints, solved-mystery writeups. If it belongs in git history or code comments, it doesn't belong here.

## Self-improvement (do this first and last)
1. **At start:** read `learnings.md` in this skill's folder if it exists. Apply relevant lessons.
2. **At end of every use:** append one dated bullet — a recall that saved rework, a capture format that proved useful/useless. Merge instead of duplicating; delete disproven bullets.

## Structure
```
memory-bank/
  INDEX.md          ← one line per entry: - [Title](file.md) — recall hook
  decisions/        ← choices with lasting consequences: what, why, alternatives rejected
  context/          ← domain/product truths not derivable from code (why this feature exists, external constraints)
  solutions/        ← solved-mystery writeups: symptom → root cause → fix → how to spot it again
```
One fact per file, kebab-case names, each file ≤ ~20 lines with a one-line summary at top. `INDEX.md` is the only file read routinely — keep every line's *recall hook* specific enough to judge relevance without opening the file.

## Recall protocol (the half most setups skip)
1. **Before starting work in any area**, scan `INDEX.md` (create the folder + index on first use). Open only the entries whose hooks match the task — never bulk-read the bank.
2. Treat entries as point-in-time claims: verify against current code before acting on anything load-bearing, and update the entry if it drifted.
3. When the user asks "why is X like this" — check `decisions/` before deriving an answer from code.

## Capture protocol
Capture at these moments (not on a timer):
- **A decision with lasting consequences is made** → `decisions/`: what was chosen, why, what was rejected and why. Convert relative dates to absolute.
- **A non-obvious problem is solved** (took >30 min or >2 failed hypotheses) → `solutions/`: symptom → cause → fix, written so the *next* occurrence is recognized in one read.
- **External/domain context surfaces** that code can't express (client requirement, API quirk, design intent) → `context/`.
- **User says "remember this"** → capture; if it's actually a preference or cross-project fact, route it to the appropriate layer instead and say so.
- **A handover note is over its ceiling** → it is demoting to you. Decisions and solved mysteries become entries here; session narrative is **not** accepted (git already holds it) and must be dropped, not parked. See the `handover` skill's routing table. In parallel mode the demoting session holds `memory-bank/INDEX.md` in `locks.md` while writing — the bank is shared and owned by no role.

Rules: distill — never paste transcripts, diffs, or code blocks longer than 5 lines (link `file:line` instead). Check the index for an existing entry to update before creating; delete entries proven wrong; add the index line in the same step as the file (an unindexed memory is invisible). Link related entries by filename.

## Maintenance
- Entries whose subject was removed from the codebase → delete file + index line.
- The `memory-gardener` skill's pruning rules apply to `memory-bank/` too — invoke it when INDEX.md exceeds ~40 lines.
- Commit memory-bank changes with the work that produced them — the memory and the code change share a commit and stay in sync.
