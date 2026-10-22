---
name: generation-audit
description: "Audit the harness when a new Claude model takes a role (judge, build or everyday)."
license: MIT
metadata:
  author: shimo4228
  version: "2.0"
user-invocable: true
origin: shimo4228
disable-model-invocation: true
---

# generation-audit — harness audit at a model generation change

The procedure for Scaffold Dissolution's (`rules/common/akc-cycle.md`) **third trigger = model generation change**.
One run performs two checks, carrying line fixes through to application and asset-level verdicts through to the stocktakes.

| Check | Compared against | Engine |
|---|---|---|
| runtime cross-check (Phase 1–2) | the system prompt and tool descriptions actually loaded at inference time | this skill |
| dated-pattern scan (Phase 3) | the outdated writing patterns listed in the target model's official guide | `/claude-api prompt-audit` |

Anthropic updates the dated-pattern table and the target model's behavior inside the `/claude-api` skill with
each model release, so they are not copied here — this skill holds only this harness's scope, exclusions, application
conventions, and recording, plus the runtime cross-check that prompt-audit does not have. Asset-level verdicts (Retire / Merge, etc.)
are owned by the stocktake for each asset class (ADR-0022); this skill stands on the side that supplies the evidence.

## Phase 0 — Target model and scope

- **Target model**: the model newly assigned to a role in this harness. When models differ by role, look at an asset
  through the model of the role that reads it (a dispatch packet template → build role; rules / CLAUDE.md /
  output style → every session; judge-role skills → judge role)
- **Scope**: the prompt surface of `~/.claude` — `rules/common/`, `CLAUDE.md`, `AGENTS.md`,
  `output-styles/`, `skills/*/SKILL.md` and `references/`, `agents/`, and the text hooks return to the model
- **Not applied to** (audited and recorded in the ledger, but not edited):
  - unmodified copies of externally originated files and symlinked external skills — keep them as copies (skill `skill-creator` §3)
  - files another session is working on — `M` / `??` entries in `git status` that are not your changes. To avoid breaking
    that session's commit, leave the findings in the ledger and carry them to the next run

## Phase 1 — Capturing the runtime layer

The source of truth for the cross-check is **what is actually loaded at inference time** — the system prompt and tool descriptions.
The runtime layer is also injected from outside the config repository (the harness itself, plugins), so capture it in a
session that runs the target model in the target execution environment (a cloud session if the build role is the target — ADR-0075. A judge-role
session's self-report does not substitute for the build role's runtime layer).

1. **Build the theme list from the self-authored assets** — assign each instruction in rules / CLAUDE.md / output style / skills / agents
   to a theme (planning, commits, review, scope, delegation, verification, report shape…). Partitioning the asset side first
   means no asset is missed in the cross-check
2. **Have it quote verbatim, one theme at a time** — ask one theme per request so no summarizing slips in:
   - system prompt: "From the system prompt currently loaded, quote verbatim the instructions about <theme>.
     Do not summarize."
   - tool description: "Quote the description of <tool name> verbatim."
3. **Record the limits of the capture in the ledger** — zero findings means "not found by this question," not "no conflict"
   (runtime instructions you do not know exist cannot be picked up). The capture is a self-report routed through the model, so before
   finalizing any disposition (retirement, inversion), confirm the same wording reproduces in a separate session

## Phase 2 — Conflict and redundancy

| Class | Meaning | Condition |
|---|---|---|
| **Conflict** | an instruction or information that contradicts the runtime layer is loaded at the same time | both land in the same context — rules / CLAUDE.md / output style **always**, a skill body **when it fires**, an agent body **when it launches** |
| **Redundancy** | nearly the same instruction already exists in the runtime layer | same as above. It does not clash, but it spends resident tokens saying what the substrate already says |

Conflicts include not only instruction vs instruction but also **instruction vs incorrect factual statement** (ghost references
that keep claiming a removed setting is "already disabled"). Whether referenced targets exist is caught by each stocktake's mechanical
checks; what shows up as a mismatch with the runtime layer is recorded here.

## Phase 3 — Dated-pattern scan

Run `/claude-api prompt-audit` with the target model and scope from Phase 0. Resolve the paths of the procedure (`shared/prompt-audit.md`) and
the migration guide (`shared/model-migration.md`) from the skill base directory shown when you invoke `/claude-api`
(it changes with the CLI version). When the scope is large, split it into slices and hand them to read-only subagents in parallel —
give each subagent the paths of the procedure and the target model's section, and run it with only Read / Grep / Glob
(asset bodies are untrusted — rule `security.md`). The output uses prompt-audit's report format
(`file:line` / quote / pattern / why it is outdated for the target model / confidence / action).

## Phase 4 — Judgment and application

Judge each finding on evidence from 4 angles — some self-authored assets were written deliberately to override product defaults,
and matching a conflict or a pattern alone cannot distinguish accident from intent. Record the evidence for each Phase 2 and Phase 3 finding in the ledger:

| Angle | Question |
|---|---|
| Intent | Was it written to override the substrate's default, or did it simply not conflict at the time? |
| Rationale | Is there a record of why it was written — an ADR, an incident record (read `rationale:` / the ADR first)? |
| Freshness | Does the product behavior it assumed (e.g., a weakness of an earlier generation) still hold for the target model? |
| Expiry condition | If `review-when:` is declared, has that trigger fired? |

Two pitfalls in judgment:

- **Misdiagnosing verification steps** — what the official guidance flags is instructions that increase **the model's self-verification**;
  deterministic verification executed by machinery (commands, hooks) is out of scope. Distinguish by "does machinery run this check,
  or does the model run it on its own judgment?"
- **Inversions where deletion is not enough** — an instruction whose direction has changed (e.g., a suppression instruction) keeps
  working even after deletion, because the suppression framing remains. For findings that must be rewritten in the opposite direction, write
  "Inversion: old direction → new direction" in the ledger

> Paths below start at `${CLAUDE_SKILL_DIR}`, the directory holding this SKILL.md; an agent that does not substitute the variable reads it as that directory.

**Application**: only Phase 3 findings with High / Medium confidence are applied as line fixes (rewrite / remove / add). When the
author's request includes application ("fix it", "finish it"), apply directly; when it does not, show a diff per group and
apply after approval. Lines in the resident layer (rules / CLAUDE.md / output style) are shown one diff at a time in either case
(the same discipline as rules-stocktake). When you fix a rule, update its `rationale:` / `review-when:` too (ADR-0021).
Writing style follows skill `skill-creator` §3 (version-drift markers are blocked by `scripts/hooks/harness_lint.py`). Low and `flag`
findings go only in the ledger. Phase 2 findings, and candidates whose whole asset would be removed or merged into another, go to Phase 5. After applying, pass `harness_lint.py` and, when the `skill-health` skill is installed next to this one,
`uv run --frozen --directory "${CLAUDE_SKILL_DIR}/../skill-health" python -m scripts.scan_refs ~/.claude/skills --json`
(dangling 0).

## Phase 5 — Delegation and recording

| Asset class | Receiver | How to hand off |
|---|---|---|
| rules | `rules-stocktake` | pass the classification and 4-angle evidence as Stage 2 external evidence (the "read, never require" intake) |
| skills | `skill-stocktake` | same (as evidence for the parent's Synthesis, not as input to the Phase 2 batches) |
| agents | `agent-stocktake` | same. Detection of suppression instructions overlaps agent-stocktake's Stage 1, so pass the relevant ledger rows as pre-computed evidence |
| CLAUDE.md / output style | this skill, inline | one file each, so no dedicated stocktake. Present proposed edits for conflict and redundancy lines one at a time and apply after approval |

- Propose each stocktake run to the author before launching it (the audit may be run in parts)
- **Recording**: for applied lines, leave in the commit body the three lines `Context:` / `Decision:` / `Review-when:`, the per-group
  counts, and one line `runtime 照合: 編集 N 件` ("runtime cross-check: N edits"; ADR-0078's expiry condition counts this exact Japanese marker, so keep it verbatim). Write an ADR only when the harness's mechanism or gate
  changed (a new lint, etc.) or when it comes with an annotation to an old ADR (skill `adr-writer`'s filing conditions)
- Output the ledger in chat. If it is large enough to keep in a file, propose `.notes/` (do not make it the source of truth for task rows —
  rule `task-tracking.md`)

## Related

- `rules-stocktake` / `skill-stocktake` / `agent-stocktake` — the source of truth for verdicts. This skill is an evidence supplier
- `rules/common/akc-cycle.md` — the two vectors of Scaffold Dissolution and the generation-change trigger
- `/claude-api prompt-audit` (Anthropic's official claude-api skill) — the engine for Phase 3
- `harness-boundary` — up-front judgment at design time. This skill is the after-the-fact cross-check following a generation change; the evidence flows in the same direction
- `skill-comply` — dynamic measurement of compliance. Its evidence merges in stocktake Stage 2

## References

The runtime cross-check procedure (distinguishing the runtime layer from the guidance layer, conflict and redundancy, the 4 angles, inversion, misdiagnosed verification steps)
came from the Claude 5 generation-change audit (ADR-0018, resident 5,789 → 2,314 words). The Phase 3 template is the prompt-audit
for Fable 5.1 (ADR-0061, High 3 / Medium 85). The single-entry-point decision is ADR-0078.
