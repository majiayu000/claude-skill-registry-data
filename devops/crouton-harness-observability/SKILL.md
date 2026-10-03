---
name: crouton-harness-observability
layer: stack
description: How to MEASURE this repo instead of eyeballing it — interpret the loop-station context-budget trend (history.jsonl, thresholds, the tokenizer-switch gotcha), read a session trace, use the eval ledger (cost-per-success), and pick the right evidence tool (app-shots, smoke-deployed, db-counts, --check modes). Use when asked "is the harness bloating", "how big is CLAUDE.md really", "did this agent run actually succeed", "prove this works", "what evidence do we have", or when tempted to declare a capability (browser, tool) unavailable. For RUNNING the loop-station scripts, defer to the loop-station skill — this skill is interpretation + the wider evidence toolkit.
---

# crouton-harness-observability

One line: the repo's proof toolkit — where the measurements live, how to read them without fooling yourself, and which gaps still force eyeballing.

"The harness" = this repo's agent-operating layer: root `CLAUDE.md` + `AGENTS.md` + `.claude/skills/**` + `.claude/agents/**` + the LLM CI workflows. It is treated as a system worth measuring (AGENTS.md "Observe the harness").

## When to use / when NOT to use

| You want to… | Use |
|---|---|
| Interpret a loop-station record, the budget trend, a session trace, the eval ledger; pick an evidence tool; know what is NOT instrumented | **this skill** |
| Run the loop-station scripts (gather/append/parse/advisor mechanics, CI wiring) | **loop-station** skill (it owns the runbooks; this skill never restates them) |
| Boot/observe an app locally or on staging, screenshots, DB inspection runbook | **crouton-run-and-operate** |
| Run tests + the honest coverage picture | **crouton-validation-reality** |
| Understand which workflow produced a CI artifact | **crouton-ci-and-deploy-map** |
| Know which config file a measurement reads | **crouton-config-registry** |

## 1. The loop-station inventory (WS1) — reading it

**Data:** `writeups/loop-station/history.jsonl` — committed on purpose (tiny, `git blame`-able; see its README). One JSON record per merge that touches the harness, appended by CI (`.github/workflows/loop-station-inventory.yml`). The WS2 runtime *trace* is the only loop-station dataset that is gitignored.

**Record shape and thresholds are owned by the loop-station skill** (`.claude/skills/loop-station/SKILL.md`; threshold bands in `.claude/skills/loop-station/lib/scorecard.mjs` `THRESHOLDS` — tune only there). Don't restate them here. The one field to check *before reading any number* is `tokenizer` — `anthropic` (API `count_tokens`) vs `heuristic` (offline fallback). That field is the ruler.

**Current numbers:** run `node .claude/skills/loop-station/gather.mjs --pretty` — never quote a remembered measurement (no API key in the env → `heuristic` tokenizer, so compare only against heuristic-era records).

### The tokenizer discontinuity — the #1 misread

Every record carries `tokenizer`. **Never compare numbers across two tokenizers.** The heuristic overcounts vs Anthropic `count_tokens` by roughly 20–25% here. Two real traps in the committed history:

- The apparent budget "drop" at the heuristic→anthropic switch is the ruler changing, **not a diet**. (The API tokenizer landed in PR #958; the switch *shows up* at the first record where CI actually ran with `ANTHROPIC_API_KEY` — a later PR — so the step and the code change don't share a commit.)
- A record can silently **revert to `heuristic`** when CI runs without the key (it happened; the point reads red). That is missing-secret noise, **not a regression** — check the surrounding anthropic-era points before ticketing.

The advisor (`advisor.mjs`, see loop-station skill) encodes this rule: deltas are compared only within the same tokenizer. A large corpus step can also be deliberate (e.g. a batch of new skills landing) — read the PR behind the record before calling it drift.

## 2. The session trace (WS2) — reading it at a glance

Producer mechanics live in the loop-station skill (`parse-transcripts.mjs`, `collect-traces.mjs`). What you get is `trace.jsonl` of events:

```
{ ts, kind, name, parent, depth, agentId?, durMs? }
```

- `kind` = skill / agent / tool; `parent` + `depth` reconstruct the real call tree (2+-level agent recursion supported).
- **Privacy rule:** names + correlation ids + durations only — never tool inputs or results. Runtime exhaust → gitignored; CI ships it as an artifact tagged by `run_id` (the two-step collect→upload snippet lives in `claude.yml`).
- How to read one fast: sort by `ts`, indent by `depth`. Look for (a) the same skill/agent firing repeatedly at the same depth = a retry loop; (b) a long `durMs` on an agent with few children = it stalled, not worked; (c) tools firing with no skill parent = the model bypassed the skill it should have loaded.
- pi-harness runs (`pi-telemetry.mjs`, #944) emit the same event shape but at **agent granularity only** — no tool-level nesting until pi-otel spans are wired (open).

## 3. The eval ledger — did the run actually succeed, and at what cost?

**Data:** `writeups/reports/eval-ledger.jsonl` (committed, append-only). **Scripts:** `scripts/eval-ledger/{schema,append,scoreboard}.mjs` — usage in `scripts/eval-ledger/README.md`:

```bash
node scripts/eval-ledger/scoreboard.mjs          # markdown rollup; --json / --html
node scripts/eval-ledger/append.mjs --flow a11y-reports --harness pi \
  --model anthropic/claude-haiku-4-5-20251001 --outcome report   # append one run; --check validates only
```

Semantics that matter when reading it:

- One record per agent run: `{ ts, flow, skill, harness, model, cost_usd, turns, wall_s, artifact_gate, ci, outcome, human, fix_rounds, ref, notes }`.
- **Success** = no gate failed AND `outcome ∈ {merged, report}`. **The routing metric is cost-per-success**, never raw cost or vibes. `model` is provider-qualified (`anthropic/…` vs `ollama/…`) because it's a cost board.
- **The gold negative:** the seed record is the 2026-06-22 pi/Haiku decompose spike that merged unreviewed to main with full creds and was **reverted in PR #862** (`outcome: "reverted"`, `human: "down"`). `outcome: reverted` is the strongest failure signal the ledger has; it birthed the reports-only-first rule (#867). Never delete or "clean up" that row.
- The ledger feeds `.claude/routing.json` (model routing, #864/#865) — routing changes should cite ledger evidence, the way the orchestrator/decomposer opus→sonnet demotion cited an N=4 A/B.
- Weekly scoreboard post: `.github/workflows/eval-scoreboard.yml`, cadence config-as-data in `.github/digests.yml` (see crouton-config-registry).

## 4. Evidence tools — pick by what you must prove

Full operating runbooks for the app-facing ones are in **crouton-run-and-operate**; this table is the "which proof do I reach for" index.

| To prove… | Tool (exact invocation) | Notes |
|---|---|---|
| "the UI renders like this" | `node scripts/app-shots.mjs <baseUrl> <path[:name]> […] [--out <dir>]` | Uses preinstalled chromium at `/opt/pw-browsers` (globs newest build — never hardcode a build number); output `screenshots/<name>.png` (HARD GATE location); exit 1 on any failure |
| "the DEPLOY actually works" (not just built) | `node scripts/smoke-deployed.mjs --url <url> --email <e> --password <pw> [--app <n>] [--manifest <app>/deploy.config.json]` | Login proof via `/api/auth/get-session` → optional CRUD round-trip from `deploy.config.json` `smoke.crud` → screenshot. Built because "typecheck + boot" twice masqueraded as done (#293, per its header). Report-only in CI unless `smoke.required: true` |
| "a generated app still boots/auths/CRUDs" | e2e fixture harness — see **crouton-validation-reality** and the **e2e-smoke** skill | Trace/video/screenshots land in `playwright-report/`; CI artifact `visual-qa-<fixture>` (14-day) |
| "types still hold" | `pnpm typecheck` (never `npx nuxt typecheck` from root) | Necessary, never sufficient — AGENTS.md "Done is signed off, not asserted"; the story behind it: `crouton-failure-archaeology` (#988) |
| "what data is on a remote DB" (read-only) | `node scripts/db-counts.mjs --app <app> --env staging\|prod [--dry-run]` | SELECTs only; discovers db name from `wrangler.jsonc`; real run needs CF creds, `--dry-run` needs none |
| "which gates apply to this path" | `node scripts/harness-stages.mjs <path>` | e.g. `packages/crouton-core/x.ts` → `stage: package, gates(required): test-first` |
| "layer tags are honest" | `node scripts/harness-layers.mjs --check` | ⚠️ Despite its own header it is wired into **no** CI workflow, and it can be red for pre-existing untagged skills — a failure here may not be yours (re-verify block; #1098) |
| "generated docs aren't stale" | `node scripts/gen-skills-doc.mjs --check` · `node scripts/gen-routing.mjs --check` · `node scripts/gen-package-catalog.mjs --check` | skills-doc: a skill missing from `META` only warns; stale HTML fails — new skills trip it until registered + regenerated |
| "is a budget regression worth a ticket" | `node .claude/skills/loop-station/advisor.mjs --pretty` | Deterministic gate over history.jsonl; cross-check any always-on red against the tokenizer rule (§1) before ticketing |

## 5. Verify capabilities, don't assume (#629)

Root CLAUDE.md ("You HAVE a headless browser") is the standing rule; the incident behind it is [#629](https://github.com/FriendlyInternet/nuxt-crouton/issues/629): an agent checked the default Playwright path (empty), saw `npx playwright install` fail (egress-blocked CDN), and declared "no browser" — while chromium sat preinstalled at `/opt/pw-browsers`. **Two partial negatives are not proof of absence.** Before declaring anything unavailable: env vars → non-default paths → filesystem search → system binaries. Same doctrine applies to TodoWrite (absent on some harnesses — fall back per root CLAUDE.md, don't retry-spam) and any "X isn't available here" claim inherited from a prior session: probe for 5 seconds first. `app-shots.mjs`'s `findChromium()` is the codified fix (env override: `PLAYWRIGHT_CHROMIUM_PATH`).

## 6. What has NO instrumentation (open gaps)

| Gap | Status |
|---|---|
| **Staging Worker logs**: only a couple of apps have a `logs` script, and those tail the **production** worker (`npx wrangler tail <app>`). No staging tail script exists; hand-type `npx wrangler tail <app>-staging --env staging`. No log persistence (no Logpush/Sentry) — an untailed Worker error is gone forever | open |
| **Runtime product analytics**: `packages/crouton-analytics` exists (PostHog default, epic #945/#946) but no app/poc/fixture depends on it (re-verify block). No uptime checks; deployed smoke runs only on deploys | open |
| **Visual regression**: screenshots exist, comparison is human — pixel-diff baselines explicitly deferred (`e2e/CLAUDE.md`) | open, deliberate |
| **`harness-layers --check` in CI**: documented as CI-enforced, actually unwired (§4; #1098) | open drift |
| **pi WS2 tool-level nesting**: agent-granularity only until pi-otel spans are collected | open |
| **CI-agent tokenizer flakiness**: loop-station CI records silently fall back to `heuristic` when the key is missing — a red in history may be a missing secret, not growth | known noise mode |

## Provenance and maintenance

verified: 2026-07-02

Facts checked against: `writeups/loop-station/history.jsonl` (all records read) + its README; live `gather.mjs --pretty` and `advisor.mjs --pretty` runs; `.claude/skills/loop-station/SKILL.md` + `lib/scorecard.mjs` + `parse-transcripts.mjs`; `scripts/eval-ledger/{README.md,append.mjs,scoreboard.mjs}` + `writeups/reports/eval-ledger.jsonl`; headers of `scripts/{app-shots,smoke-deployed,db-counts}.mjs`; live runs of the `--check` modes; GitHub issue #629; greps for `crouton-analytics` consumers and `"logs"` scripts. Unverified-but-cited: issue numbers inside quoted script/skill prose (#293, #867, #944 etc.) — taken from the cited files themselves. Volatile facts (token counts, record counts, exit codes, issue states) — re-verify here, not in the prose:

```bash
node .claude/skills/loop-station/gather.mjs --pretty        # current budget numbers (§1)
grep -o '"tokenizer":"[a-z]*"' writeups/loop-station/history.jsonl | tail -3   # ruler of recent records
sed -n '/THRESHOLDS/,/^}/p' .claude/skills/loop-station/lib/scorecard.mjs      # threshold bands
node scripts/eval-ledger/scoreboard.mjs                     # ledger state + record count
node scripts/harness-layers.mjs --check; grep -rl harness-layers .github/ || echo "still unwired"
grep -rl crouton-analytics --include=package.json apps pocs fixtures || echo "still unconsumed"
gh issue view 629 --json state -q .state                    # capability-assumption incident still open?
grep -l '"logs"' apps/*/package.json                        # which apps have a logs script (2 at verification, both prod-tail)
```
