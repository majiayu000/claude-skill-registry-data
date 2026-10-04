---
name: chain
description: >
  Discover and run token-efficient chains of skills and prompts using the cache.
  Auto-matches user intent to chains/registry.yaml (skills + chains catalog),
  executes steps with minimal handoffs. Always offers opt-out when ambiguous or if the
  user prefers a single skill. Registers logical custom chains to chains/registry.yaml.
  Use at .github/skills/chain/SKILL.md or when a task spans multiple skills.
argument-hint: "Chain id or intent, e.g. 'session-start', 'deliver PR', 'migration-safe', 'deploy check'"
user-invocable: true
disable-model-invocation: false
---

# Chain — cache-first skill & prompt composition

**Purpose:** Run predefined or auto-matched **chains** of skills/prompts with **one shared cache load** and **minimal handoffs** between steps. Complements ``.github/prompts/orchestrator-v2.prompt.md`` (ad-hoc plans) and loops (scheduled autonomy).

**Chains are optional.** If the user is unsure, says no, or intent is unclear — stop and offer a non-chain path. Never force a chain.

## Phase 0 — Manifest & registry (required)

1. Read `.github/project-manifest.yaml` or `.claude/project-manifest.yaml` — `paths`, `token_policy`, `chain_policy`
2. Read `CHAIN.md` — human overview
3. Read `chains/registry.yaml` — machine catalog (`skills:` inventory + `chains:` composition)

Do **not** read application source in Phase 0.

## Phase 1 — Resolve chain (with opt-out)

**Input:** User argument (`$ARGUMENTS`) or infer from the current request.

### 1a — Explicit opt-out (check first)

If the user says any of: **no chain**, **skip chain**, **don't chain**, **without chain**, **not chained**, **single skill**, **just run**, **directly**, or names one skill/prompt only (e.g. "just `.github/skills/loop-triage/SKILL.md`") → **do not chain**.

Respond briefly:

```markdown
Skipping chain. Running: <skill-or-prompt-or-direct-task>.
```

Then run **only** that skill/prompt, or handle the request directly with a minimal cache load if needed. Jump to **Phase 4 (opt-out summary)** — skip Phases 2–3.

### 1b — Match chain

1. If argument matches a chain `id` in `chains/registry.yaml` → candidate chain.
2. If user names **2+ skills/prompts** in order (e.g. `/github-expert .github/skills/git-workflow-guardrails/SKILL.md .github/skills/project-drift-guardian/SKILL.md`) → **custom chain**. Run as ad-hoc sequence; proceed to Phase 2–3 using that order. After Phase 4, evaluate **Phase 5** for registry.
3. Else score chains by `intents` keyword overlap (case-insensitive).
4. **Clear winner** (one chain scores highest by ≥2 intent hits, or exact id) → candidate chain.
5. **Ambiguous** (tie, no match, or vague opener like "help" / "start") → **do not auto-run**. Present:

```markdown
I can run a skill chain, or you can skip it.

**Chains (pick 1):**
1. `<id-a>` — <one-line description> (<n> steps)
2. `<id-b>` — <one-line description> (<n> steps)

**Or skip chain:**
3. **No chain** — run one skill, go direct, or tell me what you want

Reply with `1`, `2`, `3`, a chain id, or a single skill name.
```

Wait for user reply. If they pick **3** or decline → opt-out path (1a). **Never** silently default to `session-start` when ambiguous.

### 1c — Confirm before run (low confidence)

If `chain_policy.require_confirm_before_run` is true, or the match was inferred (not an explicit chain id), show a one-line plan and ask:

`Run chain <id> (<n> steps)? Reply yes / no / or name a different skill.`

- **yes** → continue to Phase 2
- **no** or alternate skill → opt-out path (1a)

Respect `chain_policy.max_steps_default` — do not exceed a chain's `max_steps`.

Emit when proceeding: `Chain: <id> (<n> steps, tier <token_tier>)`

## Phase 2 — Shared cache load (once per chain)

Load **only** the selected chain's `cache_files_required`, capped by `min(chain.max_cache_files, chain_policy.max_cache_files_per_chain, token_policy.max_cache_files_default + 2)`.

Rules:

- Read `docs/codebase/*` by **section** (grep headings / offset-limit) when files are large.
- Read `TODO/*.md` — latest date file; ≤5 open bullets.
- Read `.copilot/memories/INDEX.md` — ≤2 memories if relevant.
- Record **Cache cited** list for the whole chain (not per step).

Confirm in one line: `Chain cache: <files>. Shared context ready.`

## Phase 3 — Execute steps

For each step in order (`steps[]` in registry):

| Field | Rule |
|-------|------|
| `required: true` | Always run |
| `required: false` + `when` | Skip unless condition true (e.g. `code_changed`, `tests_requested`, `fixes_applied`) |
| `skill_args` | Optional mode/scope passed to the skill (e.g. `fix`, `deep fix`, `auth module fix`). Merge with user `$ARGUMENTS` when present |
| `default_mode` / `fix_policy` | Chain-level hints; honour `suggest_only` for critical/high; **`fix_policy.rollback.required`** — init `bug-hunt-backup.py` before any patch; critical security fixes are rollback-exempt |
| `type: skill` | Follow `.github/skills/<invoke>/SKILL.md` (or synced `.github/skills/`, `.claude/commands/`) |
| `type: prompt` | Follow `.github/prompts/<invoke>.md` or mapped prompt (e.g. `orchestrator-v2` → `.github/prompts`.github/prompts/orchestrator-v2.prompt.md`-v2.prompt.md`) |

**Token rules per step:**

1. Do **not** re-load cache files already in shared context — reference by name.
2. Handoff to next step: ≤80 tokens (bullets or compact JSON keyed by `handoff` id).
3. Stay in `.github/skills/cache-efficient/SKILL.md` tone unless the step requires depth.
4. If a step fails a guardrail (e.g. test DB safety), **stop the chain** and report; do not continue to dependent steps.

**Invoke mapping (Grok):**

| Registry `invoke` | Grok command |
|-------------------|--------------|
| `load-project-cache-first` | `.github/prompts/load-project-cache-first.prompt.md` |
| `daily-standup-with-cache` | `.github/prompts/daily-standup-with-cache.prompt.md` |
| `cache-efficient` | `.github/skills/cache-efficient/SKILL.md` |
| `loop-triage` | `.github/skills/loop-triage/SKILL.md` |
| `loop-verifier` | `.github/skills/loop-verifier/SKILL.md` |
| `orchestrator-v2` | ``.github/prompts/orchestrator-v2.prompt.md`` |
| `model-schema-check` | `.github/prompts/model-schema-check.prompt.md` |
| Other skill ids | `/<invoke>` per `.github/skills/` or `.github/agents/` |

## Phase 4 — Summary (required)

**Chain completed:**

```markdown
## Chain complete: <chain-id>

- Steps run: <list>
- Steps skipped: <list or "none">
- Cache cited: <paths>
- Handoff: <final bullet or JSON>
- Next: <1–3 actions>
```

**Opt-out (no chain):**

```markdown
## Chain skipped (user choice)

- Mode: single skill / direct
- Ran: <skill-or-prompt-or-task>
- Cache cited: <paths or "minimal">
- Next: <1–3 actions>
```

Optional: append to `reports.github/skills/chain/SKILL.mds/YYYY-MM-DD-<chain-id>.md` when the chain produces auditable output. Do not write a report for opt-out unless the user asks.

## Phase 5 — Register logical custom chains

When `chain_policy.register_custom_chains` is true (default), after a **successful** custom or ad-hoc multi-skill run, or when the user asks to **save/add to registry**:

### Qualifies for registry when ALL true

1. **Logical order** — each step's output feeds the next (audit → guardrails → drift; not random specialists).
2. **Resolvable invokes** — every step maps to an existing `.github/skills/` or `.github/prompts/` target (passes `chain-audit.sh`).
3. **Reusable intent** — likely to be run again (repo health, delivery prep, etc.) — not a one-off task-specific sequence.
4. **Within budget** — `max_steps` ≤ `chain_policy.max_steps_default`; cache files ≤ `max_cache_files_per_chain`.
5. **No duplicate** — no existing chain in `chains/registry.yaml` with the same steps in the same order.

### Does NOT qualify

- One-off orchestrator plans (use ``.github/prompts/orchestrator-v2.prompt.md`` instead).
- Single skill with extra context.
- Steps that failed or were skipped due to guardrail stop.
- User said "don't save" or "no registry".

### Registration steps

1. Propose `id` (kebab-case), `name`, `intents` (≥3 phrases), `cache_files_required`, and `steps[]` mirroring the run.
2. If user did not pre-approve registration, ask: `Register as chain <id>? yes / no`
3. On yes (or explicit user rule like "add to registry"):
   - Append entry to `chains/registry.yaml`
   - Add row to `CHAIN.md` Active chains table
   - Run `bash scripts.github/skills/chain/SKILL.md-audit.sh`
   - Run `python3 scripts/sync_grok_to_github_claude.py` if skill text changed
   - Note in summary: `Registered: <id>`

### Custom chain from this session

If the user previously ran `github-expert` → `git-workflow-guardrails` → `project-drift-guardian` for repo/branch health, that maps to registry id **`repo-health`** (see `chains/registry.yaml`).

## Opt-out examples

| User says | Action |
|-----------|--------|
| "no chain, just security audit" | Run `/security-audit-agent` only |
| "skip chain" | Ask which single skill or proceed with their original request |
| "1" / `delivery` after menu | Run that chain |
| "3" / "no chain" after menu | Opt-out; no multi-step chain |
| `.github/skills/chain/SKILL.md` with no args | Show chain menu + opt-out option (do not auto-run) |

## Auto-match examples

| User says | Chain |
|-----------|-------|
| "start my day" / empty session | `session-start` (standup must offer switch to latest remote branch worked on) |
| "run daily triage" | `loop-daily` |
| "commit and push this branch" | `delivery` |
| "merge develop into master" / "promote to master" | `promote-master` |
| "add migration for profiles" | `migration-safe` |
| "audit auth on this form" | `security-review` |
| "cyber essentials" / "UK CE compliance" / "NCSC" | `cyber-essentials-review` |
| "CE bug hunt" / "compliance weaknesses" | `cyber-essentials-hunt` |
| "CE before deploy" / "certification ship check" | `cyber-essentials-pre-deploy` |
| "deploy to production" | `deploy-check` |
| "set up SES email" | `ses-email-setup` |
| "implement X with tests and docs" | `complex-task` |
| "repo health / all in order / pull branches" | `repo-health` |
| "full documentation" / "document the project" / "onboarding docs" | `documentation-full` |
| "refresh docs" / "update documentation" | `documentation-refresh` |
| "deploy template" / "deploy grok to project" | `template-deploy` |

## Anti-patterns

- Forcing a chain when the user said no or intent is unclear
- Auto-running `session-start` without offering the skip option
- Registering illogical or duplicate chains without audit pass
- Reloading full cache at every step
- Pasting cache paragraphs into handoffs
- Chaining unrelated skills without a registry entry (use ``.github/prompts/orchestrator-v2.prompt.md`` instead, or register via Phase 5)
- Exceeding `max_cache_files` or reading source before shared cache load

## Related

- Registry: `CHAIN.md`, `chains/registry.yaml`
- Audit: `bash scripts.github/skills/chain/SKILL.md-audit.sh`
- Loops: `.github/skills/loop-engineering/SKILL.md` (scheduled); chains (on-demand composition)
- Token mode: `.github/skills/cache-efficient/SKILL.md`