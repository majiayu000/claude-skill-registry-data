---
name: vsa-docs-and-writing
description: Load when writing or updating ANY documentation for the VSA website — deciding which doc is authoritative for a fact, updating docs/ after a code/schema/env change, writing a new runbook or incident entry, drafting PR titles/bodies/commit messages, committing graphify graph output, or creating/maintaining a .claude/skills/ skill. Provides the authority order (AGENTS.md → docs/ → playbooks → skills), the full docs/ inventory with update triggers, code-change→doc-update mapping, house style, templates, and the skill-library maintenance protocol. Triggers - "which doc do I update?", "where is this documented?", "write a runbook", "is this doc stale?", editing AGENTS.md/CLAUDE.md/GEMINI.md, adding a SKILL.md.
---

# VSA Docs and Writing

**What this skill is for.** This repo's knowledge lives in four layers: a manifest (`AGENTS.md`), documents of record (`docs/`), domain playbooks (`.claude/agents/`), and skills (`.claude/skills/`). This skill tells you which layer owns which fact, when a code change obligates a doc change, how to write in this repo's house style, and how to maintain the skill library itself. It is the meta-skill: it documents the documentation.

**When NOT to use this skill:**

| You actually need… | Go to |
|---|---|
| Whether a change is *allowed* at all, PR/branch mechanics, protected domains | `vsa-change-control` |
| What verification evidence a PR needs, acceptance-criteria discipline | `vsa-validation-and-qa` |
| The incident history itself (full narratives) | `vsa-failure-archaeology` |
| Architecture invariants and WHY they exist | `vsa-architecture-contract` |
| RLS/migration authoring rules | `vsa-supabase-security-reference` |
| Config/env-var catalog | `vsa-config-and-flags` |

---

## 1. Authority order

When two documents disagree, the higher one wins. Fix the lower one; never route around the higher one.

| Rank | Layer | Role |
|---|---|---|
| 1 | `AGENTS.md` (repo root) | The manifest. Self-described "Single source of truth for AI coding agents." Change control, conventions, never-do list, domain facts (Houses, presidents, application keys). |
| 2 | `docs/*.md` | Documents of record per subsystem: runbooks, architecture notes, checklists. |
| 3 | `.claude/agents/*.md` | 12 domain playbooks + README. Scoped personas; Codex and Gemini read them as playbooks via `AGENTS.md`/`GEMINI.md` routing. |
| 4 | `.claude/skills/*/SKILL.md` | Skill library (this layer). Distilled operational knowledge; must cite and never contradict layers 1–3. |

`CLAUDE.md` (root) and `GEMINI.md` (root) are **tool-specific entry points**, not independent authorities: they orient Claude Code and Gemini CLI respectively and must agree with `AGENTS.md`. `GEMINI.md` explicitly defers ("Read … `AGENTS.md` for shared repo workflows"); `CLAUDE.md` restates a subset and can drift (see §1.1).

### 1.1 Known drift — maintenance items

**Resolved 2026-07-10** (the agent-workflow-consistency PR, branch `chore/agent-workflow-consistency`): the volatile-fact and adapter-drift items are fixed at the source —
- **D1** — the stale "no CI test gate" claim in `AGENTS.md` §PR/branch was corrected to "CI runs but does not gate a merge while `main` is unprotected."
- **D2** — the stale provider hierarchy in `CLAUDE.md` was replaced with a pointer to `src/App.tsx` + a `grep` re-verify command.
- **D3** — the incomplete Supabase table list in `CLAUDE.md` was replaced with a pointer to `supabase/migrations/` + `docs/leaderboard-system.md`.
- **D5** — the `GEMINI.md` `graphify update .` tail that conflicted with `AGENTS.md` was removed; `GEMINI.md` is now a thin adapter.
- **D6** — the stale admin-route list in `CLAUDE.md` was replaced with a pointer + `grep -n "admin/" src/routes/index.tsx`.
- **D7** — `GEMINI.md`'s `gh pr create` rule was harmonized with `AGENTS.md` ("not unless the user or governing task explicitly asks").
- **D8** — the stale "3 test files" list in `AGENTS.md` §Testing was removed and replaced with `find src -name "*.test.ts*"` + a pointer to `vsa-validation-and-qa` §2.

Remaining (fix in a `docs:` PR when convenient; until then trust the "truth" column):

| # | Claim | Where | Truth (evidence) |
|---|---|---|---|
| ~~D4~~ | ~~`REACT_APP_OPENAI_API_KEY` described as the AI-assistant key~~ | ~~`CLAUDE.md` env setup and `AGENTS.md` dev setup~~ | **RESOLVED 2026-07-29; updated 2026-08-01 by #353.** Removed from public setup docs because `REACT_APP_*` vars compile into the public bundle. The legacy `secure-ai` Edge Function source was later deleted, so `OPENAI_API_KEY` has no current repo consumer; production still needs the deployed function deleted and the Supabase secret unset manually. |

---

## 2. docs/ inventory (26 files, verified 2026-07-06)

Legend for Status: **living** = keep current; **snapshot** = dated point-in-time record, do not "update", supersede instead; **stale-candidate** = flagged for review/archive.

| File | Record of what | Update trigger | Status |
|---|---|---|---|
| `admin-analytics-setup.md` | GA4 `analytics-proxy` Edge Function secrets + setup | Analytics secrets/scopes change | living |
| `admin-content-management.md` | `academic_terms` model, year/quarter content management | Term model or admin content flow changes | living |
| `ask-vsa-assistant.md` | Ask VSA architecture, Gemini model, safety filters, privacy | Assistant prompt/model/knowledge-base changes | living |
| `claude-subagent-task-template.md` | Parent-agent internal task contract for Claude specialists | Subagent context/ownership fields change | living |
| `claude-subagent-workflow.md` | How Claude Code loads `.claude/agents/` subagents | Roster or workflow changes | living |
| `codex-subagent-task-template.md` | Parent-agent internal task contract for Codex specialists/passes | Playbook context/ownership fields change | living |
| `codex-subagent-workflow.md` | How Codex routes to playbooks via AGENTS.md | Roster or routing changes | living |
| `data-rights-anonymization-runbook.md` | Manual anonymization procedure (order, RPCs, safeguards) | Data-rights RPCs or policy change | living |
| `DEPLOYMENT_GUIDE.md` | Beginner tutorial for manual `vercel` CLI deploy | — | **stale-candidate.** Tutorial voice ("puts it on the internet so anyone can access it!"); real deploy path is CI (`deploy.yml` → `npx vercel --prod` on push to `main`). See `vsa-run-and-operate` for the real path. |
| `DESIGN.md` | Original design doc for the Cabinet management feature | — | snapshot (feature shipped; historical) |
| `dynamic-content-routing-audit.md` | Public/admin route ↔ content-source ↔ admin-editor map (dated 2026-06-02) | New route reading Supabase data, or content-source change | living (re-date on update) |
| `event-image-migration.md` | Event/House-event image → repo-static migration pipeline | Pipeline scripts/workflows change | living |
| `final-compliance-reaudit.md` | Compliance re-audit report, June 19 2026 | — | snapshot |
| `gemini-cli-workflow.md` | Gemini CLI lifecycle (Research → Strategy → Execution) | Gemini workflow changes | living |
| `graphify-workflow.md` | Graphify install, usage, hook, commit rules | Graphify tooling/conventions change | living |
| `house-image-migration.md` | House profile/parent image migration to `/public/images/houses/` | House image pipeline changes | living |
| `leaderboard-system.md` | Single active member-based points/attendance model; links to the account/check-in retirement decision | Leaderboard/points schema or view changes | living |
| `leaderboard-test-checklist.md` | Manual QA checklist for leaderboard surfaces | Leaderboard UI changes | living |
| `member-photo-requests.md` | Member photo request/approval system + egress design | Photo request flow changes | living |
| `privacy-data-rights-architecture.md` | Data-rights architecture + admin runbook (reviewed 2026-06-19) | Data-rights schema/flows change | living (re-date on update) |
| `public-calendar.md` | `/calendar` page data sources and behavior | Calendar page changes | living |
| `rls-verification-checklist.md` | RLS verification runbook (`verify-rls-security.mjs`) | Any RLS/grant change | living |
| `security-headers-and-csp.md` | Vercel security headers policy; CSP rollout plan | `vercel.json` header changes | living |
| `stitch-prompts.md` | One-off UI-generation prompts for stitch.withgoogle.com | — | **stale-candidate.** Design-exploration artifact, not a document of record; candidate for archive once the UI campaign no longer uses it. |
| `storage-egress-audit.md` | Which public content is still Supabase Storage-backed (`npm run audit:storage-content`), expected vs abnormal, offline `public/images` measurement, and the external Supabase/Vercel quota-alert checklist | Image columns, buckets, audit script, or dashboard/plan settings change | living (re-date on update) |
| `supabase-usage-audit.sql` | Egress/usage audit queries (run in Supabase SQL editor) | Storage/egress model changes | living (interpretation guide: `vsa-diagnostics-and-measurement`) |
| `vsa-wrapped.md` | `/wrapped` year-in-review page: data rules, privacy | Wrapped page or its data changes | living (yearly refresh — see `vsa-seasonal-operations`) |

---

## 3. Code-change → doc-update map

When you make the change on the left, the docs on the right are part of the SAME PR (or an immediately following `docs:` PR). "Skill" targets mean: update that skill's relevant table and re-date its provenance line.

| You changed… | You must update… |
|---|---|
| DB schema (new table/column/view, migration) | `src/types/database.ts` (AGENTS.md requires it) + the owning runbook in `docs/` (e.g. `leaderboard-system.md`, `member-photo-requests.md`) |
| RLS policy / grant / SECURITY DEFINER function | `docs/rls-verification-checklist.md` if checks change; re-run `node scripts/verify-rls-security.mjs`; theory home is `vsa-supabase-security-reference` |
| New env var or Edge Function secret | `.env.example` + `AGENTS.md`/`CLAUDE.md` dev-setup blocks if user-facing + catalog in `vsa-config-and-flags` skill |
| New route or content source | `docs/dynamic-content-routing-audit.md` route map (re-date "Last updated") |
| Incident resolved / dead-end confirmed | Incident entry in `vsa-failure-archaeology` skill (template §5.2); one-paragraph trap pointer in `vsa-debugging-playbook` if it cost debugging time |
| New npm script / operational script | `AGENTS.md` "Other useful commands" if general-purpose; runbook home is `vsa-run-and-operate` |
| New/renamed/removed `.claude/agents/` playbook | `.claude/agents/README.md` — the **canonical roster**; update the row there. `AGENTS.md`, `GEMINI.md`, and `vsa-change-control` point at the README instead of repeating it; `src/__meta__/playbookRoster.test.ts` fails if the registry and actual `.claude/agents/*.md` files diverge. The per-tool workflow docs (`docs/*-subagent-workflow.md`) retain task-type routing references, so refresh those for additions, renames, or removals. |
| New/renamed `.claude/skills/` skill | "Pick a skill" routing table + fact-ownership table in `.claude/skills/README.md`, plus the roster in §6.4 of this skill |
| Graphify graph refresh (`graphify-out/*`) | Separate `chore: update graphify graph` commit — never mixed into a feature PR (§4.4) |
| House/president/application-key domain facts | `AGENTS.md` "Domain-critical facts" — the ONLY home; skills cite it |
| Test added/removed | Update `vsa-validation-and-qa` §2 when the test's purpose changes the golden inventory. `AGENTS.md` intentionally does not enumerate tests; derive the current file set with `find src -name "*.test.ts*" | sort`. |
| Assistant behavior/knowledge change | `docs/ask-vsa-assistant.md`; deploy-order rules live in the assistant docs and `vsa-architecture-contract` |
| Security headers / `vercel.json` | `docs/security-headers-and-csp.md` |

**Rule of thumb:** if a future zero-context session would make a wrong decision because a doc still describes the old world, the doc update is part of your change, not optional follow-up.

---

## 4. House style

### 4.1 Voice (for docs/ runbooks and skills)

Modeled on the best existing docs (`docs/data-rights-anonymization-runbook.md`, `docs/event-image-migration.md`, `docs/rls-verification-checklist.md`):

- **Imperative runbook voice.** "Run X. If you see Y, do Z." Not "one could consider running…".
- **Numbered steps for procedures; tables for reference data; checklists for QA.** Prose only for WHY.
- **Define jargon at first use** (RLS = Row Level Security; egress = bytes served out of Supabase, which is billed; CRA = Create React App; degraded mode = the app running without Supabase).
- **Copy-pasteable fenced commands** — every command verified against the repo before writing it down. A wrong runbook is worse than none.
- **State what a doc does NOT do** (see the anonymization runbook's "It does not delete…" opener) and what is unverified ("needs schema verification" convention from `privacy-data-rights-architecture.md`).
- **Date volatile claims** ("Last updated: YYYY-MM-DD" header or inline "as of YYYY-MM-DD").
- No emojis in new docs (`DEPLOYMENT_GUIDE.md`'s 🚀 is the anti-pattern), no marketing prose.

### 4.2 PR titles and bodies

PR titles are CI-enforced by `.github/workflows/pr-title.yml`:

```
^(feat|fix|chore|docs|refactor|test|style|perf|ci|build|revert|security)(\([a-z0-9-]+\))?!?: .+
```

Examples that pass: `docs: update admin runbook`, `feat(ai): improve Ask VSA chat`, `fix!: remove deprecated backend`. Full change-gating and branch rules: `vsa-change-control` (do not duplicate here).

PR bodies, per `AGENTS.md` "PR and final response expectations": summary, files changed, **safety confirmations**, verification results, manual QA performed, pushed branch, and manual PR title/body when PR creation wasn't requested. If `.gitignore` had pre-existing local changes, explicitly confirm it was preserved and left uncommitted.

### 4.3 Commit messages

Observed in `git log` (verified 2026-07-06): conventional-commit style dominates — `feat:`, `fix:`, `chore:`, `docs:`, optional scope (`feat(cabinet):`, `feat(ai):`), imperative mood, lowercase after the colon. Merged-PR commits carry `(#N)`. Some intermediate commits on agent branches don't conform (e.g. `Rewrite Wrapped recap copy`) — the regex is enforced on **PR titles**, not individual commits, but write conventional commits anyway so squash-merges pass without editing.

### 4.4 Graphify commit convention

- Graph output changes (`graphify-out/*.md`, `graph.json`, `graph.html`) go in their **own commit**: `chore: update graphify graph` (precedent: commits `a0d45b77`, `bf7b4ace`). Never mixed into a feature PR.
- **Never commit:** `graphify-out/cache/`, `graphify-out/cost.json`, `graphify-out/.graphify_labels.json`, `graphify-out/.graphify_root` — all gitignored (`.gitignore` L48–51).

---

## 5. Templates

### 5.1 Runbook template (for new docs/ files)

```markdown
# <System> <Runbook|Architecture|Checklist>

Last updated: YYYY-MM-DD

One-paragraph purpose. State explicitly what this doc does NOT cover or authorize.

## Prerequisites
- <access, env vars, roles needed>

## Procedure
1. Run:
   ```bash
   <exact command>
   ```
   Expected output: <what success looks like>. If you see <failure sign>, <recovery step>.
2. …

## Verification
- [ ] <observable check proving it worked>

## Known failure modes
| Symptom | Cause | Fix |
|---|---|---|
```

### 5.2 Incident-entry template

Incidents live in ONE place: the `vsa-failure-archaeology` skill. New entries use its format:

```markdown
### <short incident name> (YYYY-MM)
- **Symptom:** what was observed, verbatim errors if any
- **Root cause:** the actual mechanism
- **Evidence:** commit hash / PR # / migration filename (e.g. `20260620020000_fix_user_profiles_rls_recursion.sql`, #160)
- **Status:** fixed | mitigated | open
```

### 5.3 Acceptance criteria

Owned by `vsa-validation-and-qa` — write acceptance criteria per that skill's discipline; do not define a competing format here. The subagent task templates (below) each contain an "Acceptance criteria" field that should follow it.

### 5.4 Agent task templates (existing, copy-paste)

- `docs/claude-subagent-task-template.md` — fill-every-field prompt for Claude subagent tasks (subagent, goal, problem, scope, constraints, acceptance criteria).
- `docs/codex-subagent-task-template.md` — same shape for Codex playbook tasks.

---

## 6. Skill-library maintenance protocol

### 6.1 Format contract

Every skill is `.claude/skills/<name>/SKILL.md` with YAML frontmatter:

```yaml
---
name: <skill-name>
description: <trigger-rich 1–3 sentences: exactly WHEN to load it — symptoms, tasks, file areas, keywords — and what it provides>
---
```

Body conventions (all existing vsa-* skills follow these):
1. One-paragraph "What this skill is for".
2. A "When NOT to use this skill" table pointing to sibling skills by exact name.
3. Tables/checklists/numbered runbooks; fenced verified commands; jargon defined at first use.
4. Closing `## Provenance and maintenance` section: sources (file paths, commit hashes) + one-line re-verification commands for every claim that can drift.
5. Optional `scripts/` subdirectory for helpers (node/bash, no new npm deps).

### 6.2 Rules for new skills

- **One home per fact.** Each command runbook, incident narrative, or config catalog lives in exactly one skill; others cross-reference by skill name. Small orientation summaries are the only permitted duplication.
- **Trigger-rich description.** A Sonnet-class model reading only the description must know whether to load it. Name symptoms and keywords, not just topics.
- **Never contradict or route around `AGENTS.md`** (authority order §1). Nothing may weaken the "Things to never do" list, protected domains, or RLS rules.
- **No oversell.** Unshipped/unproven things stay labeled "open" or "candidate".
- Date-stamp volatile facts ("as of YYYY-MM-DD").

### 6.3 The maintenance loop

On any significant repo change, or quarterly (align with `vsa-seasonal-operations` turnover):

1. Open the affected skill's `## Provenance and maintenance` section.
2. **Run its re-verification commands.**
3. Where output disagrees with the skill text, fix the text (or mark `OPEN`/`UNVERIFIED` if the world is now ambiguous).
4. Re-date the provenance line.
5. Commit as `docs: refresh <skill-name> skill` (skills are docs; use `docs:` type).

### 6.4 Skill roster (16 planned; verify which exist with `ls .claude/skills/`)

| Skill | One-liner |
|---|---|
| `vsa-change-control` | Change classification, protected domains, never-do list with incidents, branch/PR conventions, approval flow |
| `vsa-debugging-playbook` | Symptom→triage table, discriminating experiments, time-costing traps |
| `vsa-failure-archaeology` | Full incident chronicle: symptom → root cause → evidence → status |
| `vsa-architecture-contract` | Load-bearing design decisions, invariants + WHY, known-weak points |
| `vsa-supabase-security-reference` | RLS theory as applied here, definer-view gotcha, check-in secrets, migration checklist |
| `vsa-design-system-reference` | Semantic tokens, type scale, dark mode, motion conventions, mobile patterns, a11y |
| `vsa-config-and-flags` | Catalog of every config axis: env vars, secrets, vercel.json, application windows |
| `vsa-build-and-env` | Dev environment from scratch; setup traps |
| `vsa-run-and-operate` | Dev server, real deploy path, migration application, Edge Function deploys, image pipeline |
| `vsa-diagnostics-and-measurement` | Diagnostic tools with interpretation guides (RLS verifier, usage audit, analyze, vitals) |
| `vsa-validation-and-qa` | Evidence bar, verification commands, acceptable warnings, test inventory, acceptance criteria |
| `vsa-docs-and-writing` | (this skill) docs authority, inventory, house style, templates, skill maintenance |
| `vsa-seasonal-operations` | Academic-year clock, freeze windows, turnover checklist |
| `vsa-ui-excellence-campaign` | Executable campaign for mobile + site-wide UI excellence |
| `vsa-research-frontier` | Open problems to beat org-website state of the art |
| `vsa-research-methodology` | How a hunch becomes an accepted change; multi-agent branch lifecycle |

---

## 7. Multi-agent workflow docs

Development here is multi-tool (branches prefixed `claude/`, `codex/`, `gemini/`, `antigravity/`). Three docs define per-tool routing:

| Doc | Serves |
|---|---|
| `docs/claude-subagent-workflow.md` | Claude Code — loads `.claude/agents/*.md` as native subagents with tool grants |
| `docs/codex-subagent-workflow.md` | Codex — reads the same playbooks, delegates with its own native mechanics when available, or performs sequential specialist passes |
| `docs/gemini-cli-workflow.md` | Gemini CLI — Research → Strategy → Execution lifecycle, playbook routing via `GEMINI.md` |

The 12-playbook roster with edit/audit modes lives canonically in `.claude/agents/README.md`. `AGENTS.md`, `GEMINI.md`, and `vsa-change-control` point at it instead of duplicating it, and `src/__meta__/playbookRoster.test.ts` fails if the README registry drifts from the actual `.claude/agents/*.md` files. The per-tool workflow docs (`docs/*-subagent-workflow.md`) keep task-type→playbook quick references for routing; refresh those when a playbook is added, renamed, or removed.

---

## Provenance and maintenance

Written 2026-07-06 from repo state at commit `368fbf63` (branch `codex/reactbits-ui`). Sources: `AGENTS.md`, `CLAUDE.md` (root), `GEMINI.md`, all 26 files in `docs/`, `.claude/agents/README.md`, `.github/workflows/{deploy,pr-title}.yml`, `.gitignore`, `src/App.tsx` (provider check), `git log`. Owner interview facts dated 2026-07-05.

Re-verify before trusting:

```bash
ls docs/ | wc -l                                   # §2 inventory count (expect 26)
grep -n "no automated CI test gate" AGENTS.md      # D1 still present? If gone, delete D1
grep -n "Provider" src/App.tsx                      # D2 provider hierarchy
grep -n "OPENAI" CLAUDE.md AGENTS.md .env.example   # D4 legacy key still documented?
grep -n "graphify update" GEMINI.md                 # D5 still present?
grep -n "regex = " .github/workflows/pr-title.yml   # §4.2 PR title regex
git log --oneline -5 --grep="graphify graph"        # §4.4 commit convention precedent
grep -n "graphify-out" .gitignore                   # §4.4 never-commit list
ls .claude/skills/                                  # §6.4 which skills actually exist
ls .claude/agents/ | wc -l                          # §7 playbook count (expect 13 incl. README)
```

UNVERIFIED items: none load-bearing. All 16 `vsa-*` skills now exist on disk (verified 2026-07-07); the roster in §6.4 is complete. Re-verify with `ls .claude/skills/` before quoting the set — it is the self-checking source of truth.
