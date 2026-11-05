---
name: session-observer
description: PROPOSE-ONLY session review — turn what actually happened this session into dated, evidence-backed skill improvement proposals in docs/skill-proposals.md. Never edits a skill, CLAUDE.md, or AGENTS.md itself. Use at the end of a wave, after a correction, or when the operator says "observe this session".
triggers: session review, skill proposals, end of a wave, after a correction, witnessed trigger, evidence-backed proposal, propose only, what happened this session, skill-proposals.md
---

# Session Observer (propose-only)

Compounding upgrade for the skill library: after real work happens, the
session that just lived through it writes down what would have made it
go better — as a **proposal an operator approves**, never as a silent
edit.

## The contract — read before doing anything

> **This skill writes to exactly ONE file: `docs/skill-proposals.md`.**
>
> It MUST NOT edit any `SKILL.md`, `CLAUDE.md`, `AGENTS.md`, memory file,
> or installed skill. It MUST NOT install, delete, or reorder skills.

**Why propose-only, not auto-apply.** Skill files steer every future
session. A background process that rewrites them silently is a
self-modifying instruction surface: one bad inference propagates into
every later run with no diff anyone read, and it is a prompt-injection
target (a compromised source becomes permanent instructions). The value
here is the *observation*; the operator keeps the write.

## Run

1. **Gather what actually happened** — no speculation:
   - `git log --oneline origin/main..HEAD` and the session's merged PRs
   - files changed, and which verify gates ran (green AND red)
   - **operator corrections**: places the operator said "no", redirected,
     or rejected an approach. These are the highest-signal input.
   - defects found, and whether an existing skill should have caught them
   - after a manager job: its metrics row (`node scripts/agent-os/ledger-render.mjs --metrics`). A finding class that recurs across three jobs, or a
     near-zero rate of manager catches before the PR opened, is a proposal; UNKNOWN cells are a gap to name, not to fill
2. **Keep only evidence-backed candidates.** Every proposal needs a
   witnessed trigger from THIS session. If you cannot cite the moment
   that motivated it, drop it — see Traps.
3. **Append one dated block** to `docs/skill-proposals.md` using the
   template below. Append; never rewrite existing blocks.
4. **Report** the count and the single highest-value proposal. Stop
   there — approval is the operator's move.

## Proposal template

```markdown
## 2026-07-30 · <session topic>

### P1 · <target skill or "NEW: <name>">
- **Trigger (witnessed):** what happened, with PR/file/line refs
- **Cost:** what it cost — rework, a wrong claim shipped, minutes lost
- **Proposed edit:** the specific line/rule to add or change
- **Confidence:** high (recurred ≥2×) | medium (once, clear) | low (hunch)
- **Status:** proposed
```

## Traps

- **Inventing improvements.** The failure mode is a tidy list of
  plausible-sounding upgrades nobody's experience motivated. A proposal
  without a citable trigger is slop — this skill exists to capture
  evidence, not to generate advice.
- **Proposing what already exists.** ~1,000 skills are installed and
  repo-level skills sit in `.claude/skills/`. Grep before proposing
  "NEW:" — a duplicate proposal is worse than none. (Pasted plans in this
  repo have come back ~85% already-shipped, four separate times.)
- **Rewriting the queue.** Append-only. The dated history of what was
  proposed and rejected is itself the signal; a rejected idea reappearing
  every wave is the thing you want to be able to see.
- **Silent scope creep into an edit.** If a proposal feels obviously
  right, it is still a proposal. Write it down and stop.
- **A correction applied to one artifact is not applied.** A 2026-09-08
  finding (`canonical-business-truth.test.ts`'s cause) was corrected in
  this queue but the correction never reached the skill that carried the
  same wrong claim — same session, same author, two artifacts. When a
  prior proposal turns out to be wrong or incomplete, grep for every place
  the ORIGINAL claim appears (this queue, the target skill, any memory
  entry it cites), not just the file you happened to be editing.

## Approval path (operator)

Review `docs/skill-proposals.md` → for accepted items either edit the
skill directly or hand the proposal to the global `skill-improver`
skill (it iterates against a reviewer agent) → mark the block
`Status: applied <PR>` or `Status: rejected <reason>`.

## When NOT to use

Mid-task — it reads a finished session, so running it early produces
half-evidence. Not for capturing durable operator facts either: those
belong in the memory system (`~/.claude/projects/.../memory/`) and
`.remember/remember.md`, not in a skill-improvement queue.
