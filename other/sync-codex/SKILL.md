---
name: sync-codex
description: '[Codex] Use when running the full Codex mirror sync and verify pipeline, or when `.claude/**` edits leave `.agents/`, `.codex/` or `AGENTS.md` stale.'
---

## Quick Summary

**Goal:** Run the full Codex mirror pipeline (sync + verify) from inside the bundle. This runner is the **single and only** entrypoint for the pipeline.

> **PORTABILITY CONTRACT — `.claude/` and `.codex/` are portable, self-running and self-testing.**
> Copy them into ANY repository — a Python repo, a .NET repo, a repo with no `package.json` at all —
> and every sync / verify / check / fix / test entrypoint still works, because each one is a path
> INSIDE the bundle invoked with plain `node`. **Never** drive this framework through a host
> `package.json` script, and never document one: `npm run …` names a command that does not exist in
> most projects the bundle is copied into. The only external requirement is `node` >= 18 — no
> `node_modules`, no npm, no lockfile (`PORT-001` enforces the pipeline imports only `node:`
> built-ins). Catalog regeneration additionally needs Python 3 (`py -3` on Windows, `python3` on macOS/Linux).
>
> Discover the roster instead of memorizing it:
> `node .claude/skills/sync-codex/scripts/run-codex-sync.mjs --list-stages`

**Summary:**

- Run the 19-stage orchestrator in order; stage 1 reconciles `CLAUDE.md`, stages 2-4 generate the Codex mirrors, and stages 5-19 run tests and read-only release gates.
- Keep `.claude` canonical and source-owned; never hand-edit `.agents`, `.codex`, or `AGENTS.md`, and expect Claude slash invocations to become Codex dollar invocations only in generated mirrors.
- Keep `AGENTS.md` discoverable under Codex's read budget: it is the project-information projection of `CLAUDE.md` (Doc Lookup and project rules first; universal rules arrive by hook, never through this file); fix a discovery defect in `CLAUDE.md`, its template, or the projection script, then re-sync.
- If a stage fails, rerun that stage with `--only=<stage> --verbose`, then rerun the full pipeline and inspect the generated diff before handoff.

> **Renamed:** formerly `/codex-sync` — that name no longer resolves as a slash command; use `/sync-codex`.

Also upserts the TUI notification and status-line keys into `.codex/config.toml`. Alerts come from the mirrored `Stop`/`SessionEnd` hooks, which Codex runs for the main thread only. The sync removes the retired legacy `notify = ["node", ".codex/scripts/codex/codex-notify.mjs"]` line and its generated helper: Codex ran that command after every turn of every thread, subagent threads included, which duplicated the hook alerts. A project's own `notify` command is kept. The bundle pins no auto-compaction budget, so Codex applies its own default: the sync never writes `model_auto_compact_token_limit`, and it retires a top-level one only when its value is exactly the formerly bundled `500000` (plus the unchanged bundled comment block above it). Any other value is the user's — kept, with one `kept user-set model_auto_compact_token_limit=<v>` line.

**Workflow:**

1. **Preflight** — The runner checks `CLAUDE.md`; it initializes a missing file, updates a marker-managed stale file, and leaves a markerless file untouched as project-owned (run `/ai-context-refresh --mode update` to add generated sections around it).
2. **Run** — `node .claude/skills/sync-codex/scripts/run-codex-sync.mjs`
3. **Verify** — Exit code `0` = pass; check stdout summary
4. **Inspect** — On failure, re-run the failing stage manually with `--only=<stage>` and `--verbose`

**Key Rules:**

- MUST evaluate all 19 stages in order — configured stages fail fast on the first non-zero exit;
  optional stages emit an explicit `SKIP (not configured)` when the adopter has not declared their contract
- NEVER edit `.agents/skills/sync-codex/**` (auto-mirror) — edit `.claude/skills/sync-codex/**` source instead
- `.claude` is the source for skills/workflows/hooks; generated acceptance targets are `.agents/skills/**`, `.codex/agents/*.toml`, `.codex/hooks.json`, and `AGENTS.md`
- Stage 1 may mutate `CLAUDE.md`; stages 2-4 mutate `.agents/skills/`, `.codex/`, `AGENTS.md`; stages 5-19 are read-only (tooling tests,
  optional tech-spec freshness and feature-registry validation, 3 hook-suite gates, the other Codex
  verifiers, and the cross-surface divergence oracle)
- Stage 2 upserts `[tui].status_line` to show model+reasoning, current directory, project root, context used, five-hour limit, and weekly limit by default
- Stage 2 never upserts `model_auto_compact_token_limit`; it retires the top-level key only when its value equals the formerly bundled `500000` and keeps any other value. No host pins a compaction budget — any compaction default change goes here AND in the other two surfaces, never in one alone
- Stage 2 also raises top-level `project_doc_max_bytes` to 98304 (never lowers a larger value): Codex silently stops reading `AGENTS.md` at 32 KiB by default, which cut the generated root mid-file. The projection still emits Doc Lookup and the project rules first, so they survive a host that ignores the project value; there, set the key in `~/.codex/config.toml` instead. The budget covers every `AGENTS.md` concatenated from the project root to the working directory, not the root alone.
- Stage 4 generates the bounded `AGENTS.md` projection of `CLAUDE.md` (project information only) and removes the retired `.codex/CODEX_CONTEXT.md`. The framework's shared protocols and the workflow route reach Codex through the mirrored hooks (`.codex/hooks.json`), never through a generated file; a Codex host that runs no hook is unsupported. Review the new handlers in Codex `/hooks` after the first sync and after any handler change: until they are reviewed, Codex receives no universal rules and no workflow route, and no static fallback exists (`.claude/docs/hooks/README.md#hook-only-delivery-host-requirements`).
- Stage 2 must not inline `lessons.md` content — it lives in the project-reference docs root (default `docs/project-reference/`; a `docsRoots.projectReference.path` entry in `docs/project-config.json` overrides the path) — into `.agents/skills/**`; generated skill mirrors carry no project content
- `AGENTS.md` and the skill mirrors carry no shared-protocol text: the universal hook delivers it (`verify-skill-protocol-compliance.mjs` fails on any copy)
- No npm dependency — pure `node` + spawned subprocesses
- Idempotent — safe to re-run; second run produces only timestamp diffs
- **opencode handoff:** when the project has a local `.opencode/` directory, the runner hands off to `/sync-opencode` after all 19 stages pass (its `--verify-only` form under `--verify-only`). The handoff is an integration step, NOT a 20th stage — the 19-stage roster stays fixed

## opencode handoff (when `.opencode/` exists)

opencode has no shell-command hooks, so its hook surface is a generated JS bridge at
`.opencode/plugins/easy-claude-hooks.js` produced by `/sync-opencode` from `.claude/settings.json`.
`/sync-opencode` also reconciles the framework's recommended opencode defaults
(`.opencode/opencode.recommended.json`) into the project-root `opencode.json`. Because a project
running opencode expects both surfaces to track the framework, a full `/sync-codex` run
automatically hands off to the opencode pipeline once the 19 Codex stages pass:

```bash
# Runs automatically at the end of a full codex sync when .opencode/ exists:
node .claude/skills/sync-opencode/scripts/run-opencode-sync.mjs
```

- The handoff is skipped silently when the project has no `.opencode/` directory, and skipped with an explicit message when `.opencode/` exists but the opencode runner is absent.
- Under `--verify-only` the handoff inherits the read-only contract (`run-opencode-sync.mjs --verify-only`), so no invocation of the codex runner ever mutates the opencode surface in verify mode.
- A handoff failure fails the codex run with the opencode stage's exit code — a green `/sync-codex` never hides a red opencode surface.
- opencode discovers skills directly from `.claude/skills` and `.agents/skills`, so the handoff syncs **hooks + recommended config + the sub-agent mirror** — no skill mirror is produced (sub-agents are not auto-discovered, so `.claude/agents/*.md` is mirrored into `.opencode/agent/*.md`).

## Bootstrap Gate (when AGENTS.md is missing)

This skill is the route the agent-files bootstrap gate offers for a missing root `AGENTS.md`, the
generated Codex projection of `CLAUDE.md`. The projection holds project information only (Doc Lookup,
project rules, naming, development commands, skill activation); the framework rules every agent follows
are delivered by the universal hook, and the workflow route only by the `workflow-route-inject` hook (in
each person's route mode). Stage 4 writes the projection; no protocol text and no route pointer is stamped.

Detection is existence-only and shared with the CLAUDE.md route via `.claude/hooks/lib/agent-files-state.cjs`;
`skip init` dismisses both hooks for 24h. The stage-1 preflight generates or updates `CLAUDE.md` before
the mirror stages. A markerless root is project-owned and is left as it is; `/ai-context-refresh --mode update`
adds generated sections around it through an AI smart-merge. When `/ai-context-refresh` has just completed source editing, it
calls this same runner with `--skip=claude-md` so the root is not processed twice.

## Coordination with ai-context-refresh

`sync-codex` owns generated Codex surfaces; `ai-context-refresh` owns the root AI-context lifecycle. Keep
the user-facing skills separate, but use this runner as their one portable executable coordinator:

- A full `/sync-codex` run performs the `CLAUDE.md` preflight first. Missing roots are initialized;
  marker-managed roots are updated; markerless roots are project-owned and preserved.
- After an explicit `/ai-context-refresh` init/update/refactor, that skill calls
  `node .claude/skills/sync-codex/scripts/run-codex-sync.mjs --skip=claude-md` after its final AI edits.
- Do not recursively invoke the other skill or hand-edit mirrors. If `.claude` (and optionally stale
  `.codex`) is copied into another project, run the full runner from the copied bundle; `.claude` is
  authoritative and `.codex`, `.agents`, and `AGENTS.md` are disposable generated outputs.

## Skill profile on Codex

Stage 2 maps the project config's `skillProfile` onto each skill mirror's `agents/openai.yaml`. The host-independent rules (presets, lists, the called set, refusals) belong to `resolveProfile()` in `.claude/scripts/sync-skill-profile.cjs`; read `.claude/config/README.md` → Skill profile for them. The called set is every workflow step, every agent `skills:` entry, and the curated `calledByOthers` and `entrySkills` lists in `.claude/config/skill-profiles.json`.

| Profile list | Skill nothing starts | Called skill |
| --- | --- | --- |
| `nameOnly` | `policy.allow_implicit_invocation: false` (Codex has no name-only listing) | Keeps implicit invocation, with one `kept implicit invocation for <name> ...` note line — a workflow step does not reach a Codex skill whose implicit invocation is off (`CODEX_STEP_REACHES_HIDDEN_SKILL = false`), so preset `standard` hides nothing on Codex |
| `commandOnly` / `off` | `allow_implicit_invocation: false`; `$name` still runs it | Refused, unless `allowHidingCalledSkills: true`; with the opt-in, `allow_implicit_invocation: false` plus a warning line |

- **No profile, no change.** The resolver loads only when `skillProfile` is declared, so a project without one gets a byte-identical mirror.
- **Refused profile stops everything.** A refusal prints the resolver's message and `skill-profile: nothing was written`, then exits `1` before any mirror, agent or config write — `--no-skills` included. The stage-19 divergence oracle fails the same way.
- **Fail-closed inputs.** A project config that exists but is not valid JSON fails the sync, because it cannot tell whether the config hides skills; a `.claude/workflows.json` without a `workflows` map fails the resolver.
- **A skill that ships its own `agents/openai.yaml`** without the policy is kept as it is: the profile is skipped for it with one `conflict:` line.

## Stages

19 stages, sequential — the complete sync + verify pipeline, owned entirely by this runner.
Stage 1 reconciles `CLAUDE.md`; stages 2-4 mutate mirrors; 5-19 verify (read-only) and are exactly what `--verify-only` selects, derived from each stage's own `mutate` marker rather than any transcribed list. Tech-spec freshness and feature-registry are optional
capabilities: if their configuration contract is absent, the runner records an explicit skip and
continues; if declared but malformed, their direct verifier fails closed:

| #   | Stage           | Script                                                       | Effect                                                                                              |
| --- | --------------- | ----------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| 1   | claude-md       | `.claude/skills/ai-context-refresh/scripts/generate-claude-md.cjs --check` | Preflight `CLAUDE.md`; init missing or update marker-managed stale; a markerless root is left as written |
| 2   | migrate         | `.claude/scripts/codex/migrate-claude-to-codex.mjs`          | Migrate Claude agents → `.codex/agents/`; mirror skills → `.agents/skills/`; setup Codex notifications |
| 3   | hooks           | `.claude/scripts/codex/sync-hooks.mjs`                       | Generate `.codex/hooks.json` + sync report                                                           |
| 4   | context         | `.claude/scripts/codex/sync-context-workflows.mjs`           | Regenerate the `AGENTS.md` project projection of `CLAUDE.md`; remove the retired `.codex/CODEX_CONTEXT.md`   |
| 5   | tests           | Runner discovers `.claude/scripts/codex/tests/*.test.{mjs,cjs}` | Run Codex tooling tests; missing or empty discovery fails |
| 6   | scripts-tests   | Runner discovers `.claude/scripts/tests/*.test.{mjs,cjs}` | Run repo-script tests, including review and experience policies; missing or empty discovery fails |
| 7   | tech-spec-freshness | `.claude/skills/tech-spec/scripts/generate-tech-specs.mjs --check` | Verify configured derived technical views; explicit skip when `techSpecScan` is absent |
| 8   | feature-registry | `.claude/scripts/codex/verify-feature-registry.mjs --configured-roots` | Verify configured canonical TC/BR identity, continuation parts, split limits, links, ranges, summaries, and coverage; explicit skip when `specSystem.featureRegistryRoots` is absent |
| 9   | hooks-count-drift | `.claude/hooks/tests/run-all-tests.cjs --filter=count-drift` | Verify the `<!-- COUNT:… -->` inventory markers have not drifted from the real skill/hook/agent/workflow counts |
| 10  | hooks-parity    | `.claude/hooks/tests/run-all-tests.cjs --filter=parity`       | Verify hook parity across the Claude/Codex/Copilot surfaces                                          |
| 11  | hooks-doc-sync  | `.claude/hooks/tests/run-all-tests.cjs --filter=doc-sync-gate` | Verify hook documentation stays in sync with the wired hook set                                     |
| 12  | wf-cycle        | `.claude/scripts/codex/verify-workflow-cycle-compliance.mjs` | Verify workflow sequence cycle compliance                                                            |
| 13  | sk-proto        | `.claude/scripts/codex/verify-skill-protocol-compliance.mjs` | Verify skill strict-execution-contract                                                               |
| 14  | residue         | `.claude/scripts/codex/verify-no-project-residue.mjs`        | Verify no project residue in generated and generic source artifacts                                  |
| 15  | sdd             | `.claude/scripts/codex/verify-sdd-semantic-compliance.mjs`   | Verify AI-SDD semantic contract coverage                                                             |
| 16  | review-validate-coverage | `.claude/scripts/codex/verify-review-validate-coverage.mjs` | Verify every review-family skill carries the `/why-review --validate-findings` route; graders never embed the fix-loop (Self-Review Convergence Loop sensor) |
| 17  | sync-adoption-parity | `.claude/scripts/codex/verify-sync-adoption-parity.mjs` | Verify SYNC tag ↔ carrier adoption parity: declared carriers carry both main + `:reminder` blocks, no undeclared skill carries a matrix tag, every injected body byte-matches canonical |
| 18  | provenance-markers | `.claude/scripts/codex/verify-provenance-markers.mjs`     | Verify provenance-marker discipline in `architecture-knowledge.md`: declared tags only · `— VERIFY` only on a declared tag · §3/§8/§9/§10 each carry a default-basis banner · no banner enumerates row-level exceptions · a `[model-knowledge]` marker carries `— VERIFY`. Fail-soft when the catalog is absent |
| 19  | sync-divergence | `.claude/scripts/codex/verify-sync-divergence.mjs`           | Byte-equality oracle over FOUR mirrors: `.agents/skills`, `.codex/agents/*.toml`, the context mirror (`AGENTS.md`; a leftover `.codex/CODEX_CONTEXT.md` is an orphan), and `.codex/hooks.json` — each re-materialized by the REAL writer into a temp dir, then diffed |

## Usage

```bash
# Discover the stage roster (MUTATE vs verify) — no need to read this file or any package.json:
node .claude/skills/sync-codex/scripts/run-codex-sync.mjs --list-stages

# Full sync (standalone, no npm):
node .claude/skills/sync-codex/scripts/run-codex-sync.mjs

# Stream live child output:
node .claude/skills/sync-codex/scripts/run-codex-sync.mjs --verbose

# Full sync while forcing skill copy mode:
node .claude/skills/sync-codex/scripts/run-codex-sync.mjs --copy-skills

# Every read-only gate (no mutation) — derived from the mutate markers, never a transcribed id list:
node .claude/skills/sync-codex/scripts/run-codex-sync.mjs --verify-only

# Self-test the framework (both suites ship inside the bundle):
node .claude/hooks/tests/test-all-hooks.cjs
node .claude/hooks/tests/run-all-tests.cjs

# Configured feature-registry adoption roots (continuation parts discovered automatically):
node .claude/scripts/codex/verify-feature-registry.mjs --configured-roots

# Explicit paths or the whole tree remain available for audits (omit paths for whole-tree mode).
# {spec-root} = specRoots.business.path from docs/project-config.json, default docs/specs:
node .claude/scripts/codex/verify-feature-registry.mjs {spec-root}/Area/README.Feature.md

# Skip stages while debugging:
node .claude/skills/sync-codex/scripts/run-codex-sync.mjs --skip=migrate,hooks
```

**Exit codes:** `0` all pass · `1` orchestrator failure · non-zero propagates from failing stage.

<!-- PROTOCOL-GUIDES:START -->

> **Protocol guides** — A hook delivers each protocol's full text when this skill loads. If a protocol's text is not in your context, read its file below before you act on it.

- `ai-discovery-doc-quality` — Agent-guide content value, authority, retention and verified discovery; writing a doc that an agent reads → .claude/skills/shared/protocols/ai-discovery-doc-quality.md

<!-- PROTOCOL-GUIDES:END -->

## Closing Reminders

**MUST ATTENTION** `/sync-codex` is model-invocable: run it once, after the `.claude/**` source edits are final and verified, when they leave mirrors stale — why: the pipeline rewrites every generated surface, so a run over half-finished source has to be repeated. An `/ai-context-refresh` completion calls the runner with `--skip=claude-md`; `/project-skill-protocol` may run its documented completion handoff. Never call it from inside its own stages, and never hand-edit a mirror instead.
**MUST ATTENTION** edit source `.claude/skills/sync-codex/**`, NEVER the `.agents/skills/sync-codex/**` mirror
**MUST ATTENTION** never reinstall a Codex legacy `notify` command — it runs for every thread, subagents included; alerts belong to the main-thread `Stop`/`SessionEnd` hooks
**MUST ATTENTION** keep Codex config upserts surgical; preserve unrelated `.codex/config.toml` keys and tables while updating the managed notification/status-line keys; retire the old compaction budget only on an exact bundled-value match
**MUST ATTENTION** keep `AGENTS.md` sync comprehensive for project information: mirror the project projection of `CLAUDE.md` (never framework or universal rules — hooks deliver those) and preserve unmanaged `AGENTS.md` preface text
**MUST ATTENTION** keep `AGENTS.md` discoverable under Codex's read budget — Doc Lookup and the project rules project first; a discovery defect in `AGENTS.md` is fixed in `CLAUDE.md`, its template or the projection script (never by adding a framework or universal rule to the root), then re-synced
**MUST ATTENTION** keep learned-lessons content out of `.agents/skills/**`; skills may point to `lessons.md` in the project-reference docs root (default `docs/project-reference/`; path from `docsRoots.projectReference.path` in `docs/project-config.json`) but must not embed its entries
**MUST ATTENTION** orchestrator fails fast — re-run single failing stage with `--only=<id> --verbose` to debug
**MUST ATTENTION** working directory auto-resolves to repo root from script path — do not pass `--cwd`
**MUST ATTENTION** stage 1 may reconcile `CLAUDE.md`, stages 2-4 mutate mirrors; stages 5-19 verify only — use `--only=` for non-destructive validation

**Anti-Rationalization:**

| Evasion                                 | Rebuttal                                                                 |
| --------------------------------------- | ------------------------------------------------------------------------ |
| "Just edit the .agents mirror directly" | Next sync overwrites it. Always edit `.claude/skills/sync-codex/` source |
| "Skip a stage to save time"             | Read-only gates (5-19) catch drift; skipping = silent regression risk    |
| "Sync looks idempotent, skip verify"    | Timestamp diffs are normal; structural diffs = bug. Always run verifiers |

> **[FAILS FAST]** First non-zero stage exit aborts chain. Re-run failing stage manually to debug.
> **[REPO ROOT]** Orchestrator auto-resolves repo root from its own path. NEVER pass `--cwd`.

<!-- SYNC:ai-discovery-doc-quality:reminder -->

**MUST ATTENTION** AI-read guides: purpose/read-when and priorities first; retain action-changing rules, exceptions and rationale; verify triggered discovery and parser contracts. Use the content-value and semantic-disposition gate after enhancement; keep evidence in temporary reports and fix generated output at its source.

<!-- /SYNC:ai-discovery-doc-quality:reminder -->
