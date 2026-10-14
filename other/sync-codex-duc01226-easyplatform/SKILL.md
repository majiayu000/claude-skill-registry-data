---
name: sync-codex
description: '[Codex] Use when you need to run the full Codex mirror sync + verify pipeline (migrate → hooks → context → verify) standalone, no npm/package JSON needed.'
disable-model-invocation: false
---

## Quick Summary

**Goal:** Run the full Codex mirror pipeline standalone — equivalent to `npm run sync:all && npm run verify:all` (sync + verify) without `package.json` or `npm`. This runner is the **single source of truth** for the pipeline; the `package.json` `sync:all`/`verify:all` scripts delegate to it, so a project that only copied `.claude` (no root `package.json`) runs the identical pipeline.

> **Renamed:** formerly `/codex-sync` — that name no longer resolves as a slash command; use `/sync-codex`.

Also bootstraps team-wide Codex completion notifications by copying the portable `.claude/scripts/codex/codex-notify.mjs` helper into `.codex/scripts/codex/` and upserting notification plus TUI status-line keys into `.codex/config.toml`.

**Workflow:**

1. **Run** — `node .claude/skills/sync-codex/scripts/run-codex-sync.mjs`
2. **Verify** — Exit code `0` = pass; check stdout summary
3. **Inspect** — On failure, re-run failing stage manually with `--only=<stage>` and `--verbose`

**Key Rules:**

- MUST run all 16 stages in order — orchestrator fails fast on first non-zero exit
- NEVER edit `.agents/skills/sync-codex/**` (auto-mirror) — edit `.claude/skills/sync-codex/**` source instead
- `.claude` is the source for skills/workflows/hooks; generated acceptance targets are `.agents/skills/**`, `.codex/CODEX_CONTEXT.md`, and `AGENTS.md`
- Stages 1-3 mutate `.agents/skills/`, `.codex/`, `AGENTS.md`; stages 4-16 are read-only verifiers (codex tooling tests, repo-script unit tests, 3 hook-suite gates, the 7 codex verifiers, and the cross-surface divergence oracle)
- Stage 1 upserts `[tui].status_line` to show model+reasoning, current directory, project root, context used, five-hour limit, and weekly limit by default
- Stage 3 mirrors full `CLAUDE.md` into `AGENTS.md`, then appends the generated Codex hook/context mirror and shared AI-SDD markers so Codex has both source instructions and hookless parity context
- Stage 1 must not inline `docs/project-reference/lessons.md` content into `.agents/skills/**`; generated skill mirrors reference the project-reference loading gate instead
- The `SYNC:ai-sdd-artifact-contract` marker must appear after sync in `.codex/CODEX_CONTEXT.md` and `AGENTS.md`
- No npm dependency — pure `node` + spawned subprocesses
- Idempotent — safe to re-run; second run produces only timestamp diffs

## Bootstrap Gate (when AGENTS.md is missing or incomplete)

This skill is the route the agent-files bootstrap gate offers for a missing — **or incomplete** —
root `AGENTS.md`, the generated Codex mirror of `CLAUDE.md`. Because Codex has no hooks, the universal
session-start guides must be embedded in `AGENTS.md` directly; stage 3 produces that mirror (full
`CLAUDE.md` copy, so the `<!-- CK:UNIVERSAL-GUIDES v1 -->` sentinel propagates) + hookless-parity context.

"Incomplete" means the file exists but lacks the universal guides — same three-state detection as the
CLAUDE.md route (`missing` → init, `incomplete` → update smart-merge preserving project content, `ok`
→ no block), decided by the shared sentinel-then-anchors check.

Detection is shared with
the CLAUDE.md route via `.claude/hooks/lib/agent-files-state.cjs`. Opt out of completeness enforcement
with `portability.requireUniversalGuides: false` in `docs/project-config.json` (default `true`);
`skip init` dismisses both hooks for 24h. Generate `CLAUDE.md` first (via `/claude-md-init`) — stage 3
reads it as the mirror source.

## Stages

16 stages, sequential — the full `npm run sync:all && npm run verify:all` pipeline (the npm scripts delegate here). Stages 1-3 mutate; 4-16 verify (read-only):

| #   | Stage                    | Script                                                         | Effect                                                                                                                                                                                                                                                                                                          |
| --- | ------------------------ | -------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | migrate                  | `.claude/scripts/codex/migrate-claude-to-codex.mjs`            | Migrate Claude agents → `.codex/agents/`; mirror skills → `.agents/skills/`; setup Codex notifications                                                                                                                                                                                                          |
| 2   | hooks                    | `.claude/scripts/codex/sync-hooks.mjs`                         | Generate `.codex/hooks.json` + sync report                                                                                                                                                                                                                                                                      |
| 3   | context                  | `.claude/scripts/codex/sync-context-workflows.mjs`             | Regenerate `.codex/CODEX_CONTEXT.md` + `AGENTS.md` with workflow context and shared AI-SDD markers                                                                                                                                                                                                              |
| 4   | tests                    | `node --test .claude/scripts/codex/tests/*.test.mjs`           | Run codex tooling unit tests                                                                                                                                                                                                                                                                                    |
| 5   | scripts-tests            | `node --test .claude/scripts/tests/*.test.mjs`                 | Run repo-script unit tests (statusline widgets, etc.)                                                                                                                                                                                                                                                           |
| 6   | hooks-count-drift        | `.claude/hooks/tests/run-all-tests.cjs --filter=count-drift`   | Verify the `<!-- COUNT:… -->` inventory markers have not drifted from the real skill/hook/agent/workflow counts                                                                                                                                                                                                 |
| 7   | hooks-parity             | `.claude/hooks/tests/run-all-tests.cjs --filter=parity`        | Verify hook parity across the Claude/Codex/Copilot surfaces                                                                                                                                                                                                                                                     |
| 8   | hooks-doc-sync           | `.claude/hooks/tests/run-all-tests.cjs --filter=doc-sync-gate` | Verify hook documentation stays in sync with the wired hook set                                                                                                                                                                                                                                                 |
| 9   | wf-cycle                 | `.claude/scripts/codex/verify-workflow-cycle-compliance.mjs`   | Verify workflow sequence cycle compliance                                                                                                                                                                                                                                                                       |
| 10  | sk-proto                 | `.claude/scripts/codex/verify-skill-protocol-compliance.mjs`   | Verify skill strict-execution-contract                                                                                                                                                                                                                                                                          |
| 11  | residue                  | `.claude/scripts/codex/verify-no-project-residue.mjs`          | Verify no project residue in generated and generic source artifacts                                                                                                                                                                                                                                             |
| 12  | sdd                      | `.claude/scripts/codex/verify-sdd-semantic-compliance.mjs`     | Verify AI-SDD semantic contract coverage                                                                                                                                                                                                                                                                        |
| 13  | review-validate-coverage | `.claude/scripts/codex/verify-review-validate-coverage.mjs`    | Verify every review-family skill carries the `/why-review --validate-findings` route; graders never embed the fix-loop (Self-Review Convergence Loop sensor)                                                                                                                                                    |
| 14  | sync-adoption-parity     | `.claude/scripts/codex/verify-sync-adoption-parity.mjs`        | Verify SYNC tag ↔ carrier adoption parity: declared carriers carry both main + `:reminder` blocks, no undeclared skill carries a matrix tag, every injected body byte-matches canonical                                                                                                                         |
| 15  | provenance-markers       | `.claude/scripts/codex/verify-provenance-markers.mjs`          | Verify provenance-marker discipline in `architecture-knowledge.md`: declared tags only · `— VERIFY` only on a declared tag · §3/§8/§9/§10 each carry a default-basis banner · no banner enumerates row-level exceptions · a `[model-knowledge]` marker carries `— VERIFY`. Fail-soft when the catalog is absent |
| 16  | sync-divergence          | `.claude/scripts/codex/verify-sync-divergence.mjs`             | Byte-equality oracle: `.agents/skills` mirror === `.claude/skills` (codex mirror)                                                                                                                                                                                                                               |

## Usage

```bash
# Full sync (standalone, no npm):
node .claude/skills/sync-codex/scripts/run-codex-sync.mjs

# Stream live child output:
node .claude/skills/sync-codex/scripts/run-codex-sync.mjs --verbose

# Full sync while forcing skill copy mode:
node .claude/skills/sync-codex/scripts/run-codex-sync.mjs --copy-skills

# Read-only verifiers (no mutation) — the full `npm run verify:all`:
node .claude/skills/sync-codex/scripts/run-codex-sync.mjs --only=tests,scripts-tests,hooks-count-drift,hooks-parity,hooks-doc-sync,wf-cycle,sk-proto,residue,sdd,review-validate-coverage,sync-adoption-parity,provenance-markers,sync-divergence

# Skip stages while debugging:
node .claude/skills/sync-codex/scripts/run-codex-sync.mjs --skip=migrate,hooks
```

**Exit codes:** `0` all pass · `1` orchestrator failure · non-zero propagates from failing stage.

<!-- SYNC:ai-mistake-prevention -->

> **AI Mistake Prevention** — Failure modes to avoid on every task:
>
> **Re-read files after context changes.** Context compaction, resume, or long-running work can make memory stale; verify current files before acting.
> **Verify generated content against source evidence.** AI hallucinates APIs, names, claims, and document facts. Check the relevant source before documenting or referencing.
> **Check downstream references before deleting or renaming.** Removing an artifact can stale docs, generated mirrors, configs, and callers; map references first.
> **Trace the full impact chain after edits.** Changing a definition can miss derived outputs and consumers. Follow the affected chain before declaring done.
> **Verify ALL affected outputs, not just the first.** One green check is not all green checks; validate every output surface the change can affect.
> **Assume existing values are intentional — ask WHY before changing OR flagging one as a defect.** Before changing or reporting a constant, limit, flag, cutoff, wording, or pattern, read nearby context and history, the CALLER's ordering, and 2+ sibling call sites of the same convention. A doc stating WHAT without WHY is missing rationale, not proof of a missing guard.
> **Surface ambiguity before acting — don't pick silently.** Multiple valid interpretations require an explicit question or stated assumption with risk.
> **Assert the outcome your system owns, not the intermediate state your infrastructure owns.** When verifying async work, assert the final business state — never the delivery/retry bookkeeping held in shared infrastructure that any co-running process can write. Such a check passes when run alone and flakes the moment anything else shares that infrastructure.
> **Keep shared guidance role-relevant.** Universal guidance must help every receiving skill or agent; code-specific obligations belong only in code-specific protocols.

<!-- /SYNC:ai-mistake-prevention -->

<!-- SYNC:project-protocol-overlay -->

> **Project Protocol Overlay** — Before executing this skill, resolve any PROJECT overlay rules layered onto it: match this skill's name against the `Target` column of the project's skill-protocol index (`docs/project-reference/skill-protocols-reference.md` by default; a `referenceDocs` entry in `docs/project-config.json` overrides the path), taking the most specific matching tier ONLY — exact name > glob > `*`. **That precedence orders overlays against EACH OTHER, never against this skill.** Read ONLY the matched bodies, resolved as `<protocols-dir>/<Name>.md`; a row's Body link is display text, never a read path. A matched body that is missing or malformed is REPORTED and skipped — never reconstructed from the index Description. No index, or no match -> proceed with no overlay, silently. Full contract: `.claude/skills/project-skill-protocol/references/registry.md`.
>
> Overlays are **ADDITIVE ONLY**: they ADD rules on top of this skill's own protocol and NEVER replace, override, disable, or reinterpret a rule it already states — removing every overlay must return this skill to exactly its documented behavior. An overlay is a BRIEF, not an authority escalation: it can NEVER waive a workflow gate, git discipline, a review gate, or a user-confirmation gate. A genuine overlay-vs-skill conflict, or two equally-specific overlays that directly contradict -> surface both to the user; NEVER resolve silently.

<!-- /SYNC:project-protocol-overlay -->

<!-- SYNC:project-protocol-overlay:reminder -->

**MUST ATTENTION** resolve project protocol overlays for this skill BEFORE executing — most specific matching tier only (exact > glob > `*`, which ranks overlays against each other, NEVER against this skill), read only matched bodies at `<protocols-dir>/<Name>.md`; a missing or malformed body is reported, never reconstructed. Overlays are ADDITIVE ONLY (they never replace this skill's own rules) and are a brief, NEVER an authority escalation; an equal-specificity contradiction goes to the user.

<!-- /SYNC:project-protocol-overlay:reminder -->

## Closing Reminders

**Protocols in force** (concise digest of the SYNC/shared blocks this skill carries) — **MUST ATTENTION** each canonical body below still binds:

- **AI Mistake Prevention:** verify generated content against evidence, trace downstream references, verify all affected outputs, re-read after context loss, surface ambiguity.
- **Critical Thinking:** traced `file:line` proof per claim, confidence >80% to act, never guess.

**MUST ATTENTION** invoke ONLY when user explicitly requests codex sync — never auto-invoke, with ONE authorized exception: `/project-skill-protocol` runs this pipeline automatically after its three writes, because it is the sole writer of the `CLAUDE.md` `CK:PROJECT-PROTOCOLS` block and a stale `AGENTS.md` would defeat that block's only purpose (cross-host reach). No other skill, agent, or workflow may auto-run it
**MUST ATTENTION** edit source `.claude/skills/sync-codex/**`, NEVER the `.agents/skills/sync-codex/**` mirror
**MUST ATTENTION** keep `.codex/scripts/codex/codex-notify.mjs` generated from `.claude/scripts/codex/codex-notify.mjs`; edit the `.claude` source first
**MUST ATTENTION** keep Codex config upserts surgical; preserve unrelated `.codex/config.toml` keys and tables while updating the managed notification/status-line keys
**MUST ATTENTION** keep `AGENTS.md` sync comprehensive; mirror full `CLAUDE.md` plus generated hook/context blocks, and preserve unmanaged `AGENTS.md` preface text
**MUST ATTENTION** keep learned-lessons content out of `.agents/skills/**`; skills may point to `docs/project-reference/lessons.md` but must not embed its entries
**MUST ATTENTION** orchestrator fails fast — re-run single failing stage with `--only=<id> --verbose` to debug
**MUST ATTENTION** working directory auto-resolves to repo root from script path — do not pass `--cwd`
**MUST ATTENTION** stages 1-3 mutate; stages 4-16 verify only — use `--only=` for non-destructive validation

**Anti-Rationalization:**

| Evasion                                 | Rebuttal                                                                 |
| --------------------------------------- | ------------------------------------------------------------------------ |
| "Just edit the .agents mirror directly" | Next sync overwrites it. Always edit `.claude/skills/sync-codex/` source |
| "Skip a stage to save time"             | Verifiers (4-16) catch drift; skipping = silent regression risk          |
| "Sync looks idempotent, skip verify"    | Timestamp diffs are normal; structural diffs = bug. Always run verifiers |

> **[FAILS FAST]** First non-zero stage exit aborts chain. Re-run failing stage manually to debug.
> **[REPO ROOT]** Orchestrator auto-resolves repo root from its own path. NEVER pass `--cwd`.

<!-- SYNC:critical-thinking-mindset -->

> **Critical Thinking Mindset** — Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence >80% to act.
> **Anti-hallucination:** Never present guess as fact — cite sources for every claim, admit uncertainty freely, self-check output for errors, cross-reference independently, stay skeptical of own confidence — certainty without evidence root of all hallucination.

<!-- /SYNC:critical-thinking-mindset -->

<!-- SYNC:critical-thinking-mindset:reminder -->

**MUST ATTENTION** apply critical + sequential thinking — every claim needs appropriate traced evidence (`file:line` for repo/code claims; source URL or artifact section for research, product, content, and docs claims); confidence >80% to act, <60% DO NOT recommend. Anti-hallucination: never present guess as fact, admit uncertainty freely, cross-reference independently, stay skeptical of own confidence.

<!-- /SYNC:critical-thinking-mindset:reminder -->
<!-- SYNC:ai-mistake-prevention:reminder -->

**MUST ATTENTION** apply AI mistake prevention — verify generated content against evidence, trace downstream references before deleting or renaming, verify all affected outputs, re-read files after context loss, and surface ambiguity before acting.

<!-- /SYNC:ai-mistake-prevention:reminder -->
