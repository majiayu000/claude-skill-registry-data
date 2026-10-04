---
name: pbi
description: '[Project Management] Use when a workflow step or the user asks for PBI work, --mode=refine (idea to PBI, acceptance criteria) | story (slicing) | mockup (HTML, --explore) | challenge (Dev BA PIC) | review (--type=) | dor (Definition of Ready, M1-M7).'
---

> Codex compatibility note:
> - Invoke repository skills with `$skill-name` in Codex; this mirrored copy rewrites legacy Claude `/skill-name` references.
> - Host-native execution: Codex runs a skill by loading its `SKILL.md` instructions and executing the required steps with available tools. No separate `Skill` tool is required; a loaded skill is already activated.
> - Source vs execution: prefer the registered `.agents/skills/<name>/SKILL.md` for Codex execution. `.claude/**` remains the canonical authoring source; reading it for a registry or source inspection does not switch this session to Claude Code.
> - Capability check: interpret Claude tool names through the active host before declaring a blocker. Continue when Codex can perform the required operation; stop and ask only when the actual capability is unavailable, naming the step and evidence. Host-native execution is not a protocol deviation and needs no extra approval.
> - Task tracker mandate: BEFORE executing any workflow or skill step, create/update task tracking for all steps and keep it synchronized as progress changes.
> - Use ask user tool to ask user.
> - Ignore Claude-specific mode-switch instructions when they appear.
> - Strict execution contract: when a user explicitly invokes a skill, execute that skill protocol as written.
> - Subagent authorization: when a skill is user-invoked or AI-detected and its protocol requires subagents, that skill activation authorizes use of the required `spawn_agent` subagent(s) for that task.
> - Do not skip, reorder, or merge protocol steps unless the user explicitly approves the deviation first.
> - For workflow skills, steps follow the guided contract in `$start-workflow` (gate steps fixed; other steps may flex with a logged reason); report step-by-step evidence.
> - If a required step/tool cannot run in this environment, stop and ask the user before adapting.
> **[BLOCKING] Mode routing — detect FIRST.** An explicit `--mode=refine`, `--mode=story`, `--mode=mockup`, `--mode=challenge`, `--mode=review` or `--mode=dor` selects that mode. With no mode, show the [Mode Dispatch](#mode-dispatch) table and stop: ask nothing, guess nothing, run nothing. Formerly `/refine`, `/story`, `/pbi-mockup`, `/pbi-challenge`, `/artifact-review`, `/dor-gate`: those slash commands no longer exist, and each mode works called directly with no workflow. Read the mode file in full before anything else.

## Quick Summary

**Goal:** One PBI skill with six modes that carry a product backlog item from idea to groomable: refine it, slice it into stories, mock it up, challenge it, review the artifacts and gate it on the Definition of Ready.

**Summary:**

- Each mode is the complete, unchanged contract of one former skill: inputs, flags, outputs, report paths, round caps, ask user tool gates and Next Steps live in that mode's reference file. This file only routes.
- Run exactly one mode per invocation. A mode never chains into another; its own Next Steps section offers the follow-up `$pbi --mode=<x>` and the user decides.
- `--reuse` links three modes: `--mode=review --type=pbi` produces the report, `--mode=challenge` and `--mode=dor` consume it (see [The `--reuse` contract](#the---reuse-contract)).
- Project specifics (artifact roots, spec roots, design system) come from `docs/project-config.json`; every mode resolves them at run time.

**Key Rules:**

- **[BLOCKING]** No mode, or an unknown mode value, prints the table below and stops. Never infer a mode from the artifact, the flags or the conversation.
- **[BLOCKING]** Read the selected mode's reference in full FIRST; its rules, gates and reminders are the only instructions for the invocation — why: each mode's gates (scope gate, validated-fix loop, DoR criteria) are not restated here.
- Every mode keeps the flags of the former skill unchanged (`--type`, `--reuse`, `--explore`, `--source`) and ignores flags that belong to another mode.

## Mode Dispatch

Detect the mode from the invocation arguments before any other work; do not load a mode file the invocation did not select.

| Mode | Purpose | Read in full FIRST |
| --- | --- | --- |
| _(none)_ | Show this table and stop — no question, no default mode | — |
| `--mode=refine [idea \| PBI \| requirement text]` | Idea refinement: ideas to PBIs, problem-hypothesis validation, the interview, acceptance criteria, estimates. Formerly `/refine` | `references/mode-refine.md` |
| `--mode=story [PBI path]` | User stories from PBIs: slicing features, breaking down requirements into INVEST stories. Formerly `/story` | `references/mode-story.md` |
| `--mode=mockup [--source=<path>] [--explore]` | Interactive HTML mockup from a PBI, story or spec artifact; `--explore` offers 1-3 design directions behind a scope gate. Formerly `/pbi-mockup` | `references/mode-mockup.md` |
| `--mode=challenge [PBI path] [--reuse=<report \| pbi-review>]` | Dev BA PIC review of a PBI draft: an AI-assisted challenge of each draft by a different reviewer. Formerly `/pbi-challenge` | `references/mode-challenge.md` |
| `--mode=review [--type={pbi\|story\|spec-tests\|design}] [artifact path]` | Artifact quality review before handoff: per-type checklist, M1-M7 gate, validated-fix loop with full re-review. Formerly `/artifact-review` | `references/mode-review.md` |
| `--mode=dor [PBI path] [--reuse=<report \| pbi-review>]` | Definition of Ready check of a PBI (8 DoR criteria, M1-M7 gates) before grooming. Formerly `/dor-gate` | `references/mode-dor.md` |

- **[BLOCKING]** When `--mode=refine`, read `references/mode-refine.md` in full FIRST; it owns the interview, the estimate re-derivation and the PBI template (`pbis/` artifact path) for the invocation.
- **[BLOCKING]** When `--mode=story`, read `references/mode-story.md` in full FIRST; it owns the slicing, the INVEST/SPIDR gates and the story template (`pbis/stories/` artifact path).
- **[BLOCKING]** When `--mode=mockup`, read `references/mode-mockup.md` in full FIRST; its Step 0 scope gate, journey report and design-authority read run before any generation, and it reads `references/mockup-explore-directions.md` (only with `--explore`) and `references/mockup-interactive-demo.md` where it names them. The mode runs in the main session when it must ask the user.
- **[BLOCKING]** When `--mode=challenge`, read `references/mode-challenge.md` in full FIRST; it is a cross-person review and never a self-review, and it owns its `--reuse` consumer rules.
- **[BLOCKING]** When `--mode=review`, read `references/mode-review.md` in full FIRST; it owns the `--type` dispatch (reading only the resolved type's `references/review-type-<type>.md`), the adversarial mindset, the M1-M7 gate, the round caps and the validated-fix loop.
- **[BLOCKING]** When `--mode=dor`, read `references/mode-dor.md` in full FIRST; it owns the 8 DoR criteria, the verdict template and its `--reuse` consumer rules.

## The `--reuse` contract

`--mode=review --type=pbi` is the producer; `--mode=challenge` and `--mode=dor` are the consumers. The contract lives once in `.claude/skills/shared/m1-m7-gates.md` → "Reusing an earlier verdict"; the consumer modes restate only their own consumer-owned checks.

- **Symbolic id.** A workflow passes `--reuse=pbi-review`; it resolves to the report written by that run's `pbi --mode=review --type=pbi` step (path recorded in the run report; unresolvable means no `--reuse`). A caller may instead pass the report path.
- **Identity.** The report header records the PBI path and the SHA-256 of the PBI file's bytes; size and mtime are never an identity. A mismatch, unreadable digest or unresolvable report turns reuse off for the whole run, per PBI.
- **Coverage map.** Only the criteria the map lists (M1-M5/M7 verdicts and the releasable-outcome / full-flow row) may be cited from the report. Consumer-owned checks are NEVER reusable: DoR — story template, GIVEN/WHEN/THEN with 3+ scenarios and an auth scenario, dependency Type and Status columns, UI design ready, story points, AI pre-review presence; challenge — the vagueness-token check and AC coverage.
- **Verdicts.** A reused FAIL stays FAIL. A standalone run (no `--reuse`) evaluates every criterion.

## Closing Reminders

**IMPORTANT MUST ATTENTION Goal:** Route to exactly one PBI mode and follow its reference alone; no mode means show the table and stop.

- **MUST ATTENTION** detect `--mode=` FIRST; no mode or an unknown mode prints the Mode Dispatch table, asks nothing and runs nothing — why: a guessed mode runs the wrong gates on a real artifact.
- **MUST ATTENTION** read `references/mode-<x>.md` in full before any work; every rule, flag, gate, report path and round cap of the former skill is there and unchanged.
- **MUST ATTENTION** honor the `--reuse` contract: SHA-256 identity, per-PBI binding, coverage map only, consumer-owned checks always evaluated, a reused FAIL stays FAIL.
- **MUST ATTENTION** one mode per invocation; follow-ups are offered by the mode's own Next Steps and chosen by the user.
