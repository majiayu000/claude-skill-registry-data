---
name: pr-review
description: "Use when reviewing, inspecting, or commenting on a GitHub pull request or GitLab merge request by number, URL, or branch, including a second review after an automated reviewer. Use review-agent-feedback for replies to existing bot threads; this skill does not review uncommitted local diffs."
---

# PR Review

## Activation and Scope

Review a GitHub PR or GitLab MR by number, URL, or branch, not uncommitted diffs.
Ask for a missing target; do not invent one. Existing bot-thread replies belong
to `review-agent-feedback` when available, not this review/posting workflow.
Detect the provider from `origin`: GitLab uses `glab`, GitHub uses `gh`.

This body owns the actor contract, including isolated/body-only use. Resolve
`<skill>` and optional references from the real, symlink-resolved skill directory,
not cwd. No sibling skill or evaluator bundle is required. Missing executable
assets, provider access, or host capabilities are explicit blockers/degradation,
not permission to fabricate a clean review or install unrelated tooling.

Every defect needs opened definitions, an upstream validation hop, a downstream
consumer hop, and a concrete failure on the cumulative diff. Only deterministic
gate measurements are exempt. `max` adds blind refutation and reproduction;
cheaper levels retain evidence requirements and disclose the missing adversarial stage.

## Effort levels

`--level` on preflight picks how much is spent. **Only `max` spawns agents.** Every level below
it runs the same lenses inline in your own context — no finder sub-agents, no skeptics — which
is why its cost does not scale with the number of units. The default is `high`.

| level | gate | find | verify | candidates per lens |
|---|---|---|---|---|
| `low` | 생략 | `logic`+`boundary`만, 팩 1패스 | prescreen | 렌즈당 4 |
| `medium` | ✅ | 적용 렌즈 전부, 인라인 순차 (정밀도 편향) | prescreen | 렌즈당 3 |
| `high` (기본) | ✅ | 적용 렌즈 전부, 인라인 순차 (재현율 편향) | prescreen | 렌즈당 4 |
| `xhigh` | ✅ | 전부 + sweep 패스 | prescreen | 렌즈당 6 |
| `max` | ✅ | workflow.js 팬아웃 | prescreen + blind tracer + reproducer | 규모 기반 (기존) |

`summary.md` prints the resolved plan as a `level=` line; `context.json → level` drives the
disclosure `post_review.py` puts in the posted body. Candidate confidence uses
the screening scale (≥80 strong, 60–79 summary, <60 dropped); posting uses the
severity-weighted bars in step 4. Do not impose a final finding-count cap:
`--max-inline` limits inline placement, not the findings disclosed.

**Pick `max` when the review is the gate** — a release branch, a change to money/auth/data, or
any MR whose findings you intend to state as verified. Pick `high` (or below) for a running
review of ordinary work. Say which level ran when you report in chat; never describe an inline
level's output as verified.

### 0. Preflight

```bash
python3 <skill>/scripts/mr_context.py --mr <ref> --repo-dir <repo> --worktree --history 5 --level high
```

Read `<out_dir>/summary.md`. Stop and say so when `eligible=false` (closed/merged/draft, or a
review by this skill already exists for this head) unless the user explicitly asked to review it
anyway. When `large=true` (> 40 files or > 2000 added lines), tell the user the scale and
ask whether to narrow (directories or lenses) before spending agents.

`--worktree` guarantees safe isolation: reuse a clean primary/linked checkout
at `head_sha` (`context.checkout`, `worktree=null`); only a dirty or different-head
checkout needs `<out_dir>/worktree`. Never create a redundant detached worktree.

`workflow_args.json` already contains the finder units, the checkout path, the candidate caps,
the hunk ranges and prior lessons for the prescreen — never hand-build it. A **unit** is one
lens bundle × one shard of the changed files (bundles: behavior = logic/boundary/data/async,
contract = security/contract/rules, intent = tests/scope/intent); each unit has one
self-contained pack (`pack/<unit>.md`: that slice's cumulative diff, the definitions and
one-hop neighbours of the symbols it defines, matching rules, threads and prior lessons). One
finder applies its bundle's lenses separately over one pack read. Shards keep
packs under ~150 KB of diff; `defs.md` and `hunks/<file>.patch` serve skeptics.

### 1. Gate

```bash
python3 <skill>/scripts/quality_gate.py --context <out_dir>/context.json
```

Run except at low: lint, scoped typecheck, targeted tests, LOC, longest touched
function, approximate complexity and test/source ratio against `base_sha`.
Only `gate.json → candidates` (`G1..`; failure 95, new breach 90, pre-existing 60,
unanchorable 50) are hop-exempt. All review numbers come from the gate, never estimates.

### 2. Find — inline (`low` / `medium` / `high` / `xhigh`)

**Do not dispatch sub-agents at these levels.** You are the finder. Work through the units in
`units.json` yourself, in this context, in sequence:

1. Read `pack/<unit>.md` whole, in one call — it already holds that slice's diff, the
   definitions and one-hop neighbours, matching rules, threads and prior lessons. Do not grep
   around it; that is what the pack exists to prevent.
2. Apply each of the unit's lenses to that pack **separately**, and tag every candidate with its
   `lens`. Do not let one lens's conclusion suppress another's.
3. Emit the finder schema below, at most `perLensCap` candidates and 3 `verified_ok`
   entries per lens. Attest every assigned file exactly once in `reviewed_files`.
4. `xhigh` only: after every unit, take one more pass over the diff as a fresh reviewer holding
   the current list, looking **only** for defects not already on it — moved/extracted code that
   dropped a guard, setup/teardown asymmetry in tests, config defaults flipped. Add nothing you
   already have; return nothing rather than padding.

State missing hops and cap confidence at 50. Low/medium favor actionable precision;
high/xhigh favor recall with a nameable failure scenario, then confidence screening.

### Finder contract (all levels)

Apply only the generated unit's effort-selected lenses independently; never share finder conclusions.
Low is limited to `logic` and `boundary`. The five-lens base below applies to other
levels when selected by the generator; topic matches do not add undisclosed lenses.
`logic` covers control/data flow; `boundary` covers changed exports, callers and
callee shapes; `tests` covers real regression assertions; `rules` requires explicit
rule text, matching glob, changed line, and cited rule; `scope` compares description
with cumulative diff. `intent`, when selected, applies with linked issues:
map each claim, criterion, checklist/table row to code/tests and quote unmet issue lines.
`security` applies to security/controller/gateway/DTO/ops or auth/token/secret/
permission/env changes; `data` to DB/migration/query/repository/transaction changes;
`async` to async/gateway/queue/stream/retry/timeout; `contract` to DTO/controller/
gateway/generated changes. Check authorization/injection, partial writes/indexes/
migration symmetry, durability/idempotency/cancellation, and public/generated
API shape/error documentation respectively.

```json
{"lens":"<id>","reviewed_files":["<each assigned path once>"],"inspected":["<opened files/symbols>"],
 "candidates":[{"path":"...","new_line":1,"end_line":null,"severity":"critical|high|medium|low",
 "category":"bug|security|performance|business-logic|data|api-contract|test|rule|scope",
 "title":"<Korean>","what":"<Korean>","why":"<Korean failure scenario>","how":"<Korean fix>",
 "evidence":["path:line — proof"],"upstream":"<observed>","downstream":"<observed>",
 "suggestion":null,"rule":null,"confidence":80,"newly_reachable":false}],
 "verified_ok":[{"concern":"...","why_ok":"<evidence file:line>","loc":"file:line","thread":null}]}
```

Severity: critical = loss/corruption, auth bypass, secrets, payment/quota error;
high = reachable wrong behavior, partial write or crash; medium = degradation,
missing timeout/cleanup or consumer-visible drift; low = rare but concrete risk.
Exclude style/naming, speculative refactors, unsupported "consider adding", and
linter/typechecker/CI findings (the gate owns those). A call site is not a definition.
Require `suggestion` for API-contract and one-line decorator/description/config fixes;
apply and check it before shipping, or strip the code while retaining the finding.

### 2b. Screen — inline levels

Write the candidates to `<out_dir>/candidates.json` and run the deterministic stage:

```bash
python3 <skill>/scripts/prescreen.py --args <out_dir>/workflow_args.json \
  --candidates <out_dir>/candidates.json --out <out_dir>/prescreened.json
```

Merge `prescreened.json → candidates`. Dedup, off-hunk checks and committed memory
match max; security/data retain their exemption. Dropped reasons go in chat, not the MR.

### 2 (max). Find + Verify — fan-out

Claude Code: `Workflow({scriptPath: "<skill>/references/workflow.js", args: <contents of
workflow_args.json>})`. Omo native: **do not execute `workflow.js` through the current Omo
session**. Run the pinned adapter instead:

```bash
python3 <skill>/scripts/omo_driver.py --args <out_dir>/workflow_args.json \
  --profile omo-flash --provider zai --model glm-5.3-flash
```

The Omo adapter pins `zai/glm-5.3-flash`, checks `--no-model-fallback`, and
sets `SENPI_NO_FALLBACK=1`; never silently switch providers. It owns rate-limit
backoff: 429 is not a format error/provider switch. `omo-flash` uses 24 finder
turns, 18 skeptic turns, cap floor 40, concurrency 10, high thinking;
`standard` uses Workflow budgets. Finder/tracer permissions are read-only;
only the reproducer may create throwaway tests. The adapter supplies temporary
read-only inputs and schema-constrained `submit_pr_review_*` output, enforces
budgets, recovers validated submissions from empty final replies, and retries
format failures with original input and only the submit tool enabled.
Remove the temporary input directory after all phases; retain diagnostic artifacts.
Retain raw stdout/stderr, exit, timeout, denial, parse/schema diagnostics and
`failure_counts` (`parse_failure`, `schema_failure`, `timeout`, `rate_limited`,
`low_confidence_abstain`, `coverage_gap`). Missing/duplicate `reviewed_files`,
failed children, or abstention mean non-zero/degraded, never a clean review.

Other hosts use current sub-agent tools with `workflow.js`'s finder/skeptic
prompts (or the contracts in this body when the asset is absent). Budget:
one finder per unit, then tracer and only if needed reproducer per candidate;
10 finder messages and 8 skeptic messages, batched reads. Use the session model
unless `args.models = {finder, tracer, reproducer}` overrides it.
Save `<out_dir>/workflow-result.json` before reading; quote its `cost` block
(agents, prescreened, reproducers skipped, output tokens) in chat.

### Max verdict contract

Prescreen deduplicates, rejects non-changed files/off-hunk lines unless proven
newly reachable, and matches prior lessons/refutation memory at similarity ≥0.5;
security/data never lose the learned-suppression exemption, including after dedup.
Skeptics start by reading candidate hunks and relevant defs together. The tracer
sees no finder evidence/upstream/downstream and independently opens the validation
and consumer hops, including linked intent; the reproducer sees the whole candidate
and tracer verdict, attempts a throwaway test, targeted check or executable scenario,
and records command/output, then deletes throwaway files.

Prescreen refusal or `refuted=true` at confidence ≥70 kills; a tracer kill skips
reproduction. Inability to verify is not refutation: return `refuted=false`,
confidence ≤40, reason prefixed `미확인:`. Exclude those verdicts; fewer than two
usable verdicts leaves an abstain ≤50, summary-only. Otherwise both must fail to
refute; final confidence is the minimum of finder and non-refuting skeptics.
Partial refutations with a standing skeptic ≥70 become open questions.
Severity changes require evidence and rationale, at most one step; use corrected
line/suggestion values. Scores: 0–25 inferred/unverified, 50 definition-proven rare
case, 75 real reachable path, 90–100 reproduction or definitions with no escape.
No reproduction and no proof from definitions can refute a scenario; tool inability
alone cannot. Intent alone is not correctness.

Missing finders or incomplete/duplicate coverage block verify. Recover only failed units:

```bash
python3 <skill>/scripts/omo_driver.py --args <out_dir>/workflow_args.json \
  --phase verify --retry-failed-units
```

This repairs failed-unit results/diagnostics, rebuilds whole-stage dedup/prescreen/
coverage and persists `find-stage.json`. No tracers until coverage is complete;
failure exits non-zero. Never combine with skeptic-abstention retry below.

To rerun only candidates that were kept as `skeptics unavailable (abstain)` in a degraded run:

```bash
python3 <skill>/scripts/omo_driver.py --args <out_dir>/workflow_args.json \
  --phase verify --retry-degraded-from <out_dir>/workflow-result.json
```

This leaves the original result untouched and writes `<out_dir>/workflow-retry-result.json`.

### 3. Merge (you are the moderator)

Write `<out_dir>/findings.json` (schema: `post_review.py` docstring):

- Start from `gate.json → candidates` (keep their `source`/`metrics`/`pre_existing`/`minor`
  fields), then add the findings with ids `F1..` — at `max` from `workflow-result.json`
  (keep `skeptics_passed`, `upstream`, `downstream`); at the inline levels from
  `prescreened.json → candidates` (keep `upstream`/`downstream`; there is no
  `skeptics_passed`, and never invent one — `post_review.py` reads it as "both skeptics failed
  to refute this" and lowers the inline bar to 50 on the strength of it).
- The workflow's `partial` list (refuted candidates where a skeptic still stood at ≥ 70)
  becomes `open_questions`: one line each — the residual risk in the standing skeptic's words,
  the location, and what the author should confirm. Inline levels have no `partial`; put the
  hops you could not complete there instead.
- `verified_ok` entries stay as `{concern, why_ok, loc, thread}` objects; pick at most 8,
  preferring ones that contradict an existing bot thread (`thread` set).
- Drop a finding whose line already has a bot/human thread unless it contradicts that thread
  (then say so in `what`). Never repeat a claim in `prior_review_lessons`.
- Re-review of a moved head: `context.json → prior_review_threads` lists earlier threads
  this skill posted (either marker); resolved ones go to `verified_ok` as "이전 지적 Fn 해결 확인", unresolved ones are
  referenced, not re-posted.
- `verified_ok` = the risky-looking things inspectors traced and cleared, each with evidence.
- `rule_candidates` = each refutation that hinged on a project fact, as one Korean sentence
  naming the fact and the proving file.
- Verdict: `request_changes` if any critical/high; `approve` if nothing ≥ medium and the
  tests lens found the changed behavior covered; else `comment`.
- Korean prose; identifiers, paths, commands verbatim. Never quote secret values.
- Before posting, use `fluent-korean` when installed and polish every Korean prose
  field the agents produced — `summary`, `verified_ok`, `open_questions`,
  `rule_candidates`, and each finding's `title`/`what`/`why`/`how`. Sub-agent prose
  field. The polish pass is required even in an isolated copy: write complete,
  direct Korean sentences, remove filler/translationese, keep terminology stable,
  and preserve facts, evidence lines, identifiers, and commands exactly.

### 4. Post

```bash
python3 <skill>/scripts/post_review.py --context <out_dir>/context.json --findings <out_dir>/findings.json --gate <out_dir>/gate.json          # dry run
python3 <skill>/scripts/post_review.py ... --post                                                                                             # only when asked
```

Inline bar is severity-weighted: critical/high ≥ 50, medium ≥ 65, low ≥ 80, and any
finding both skeptics failed to refute (`skeptics_passed`) qualifies at ≥ 50. At most 8
inline, agent findings first; deterministic gate findings get one inline slot (the worst by
complexity) and the rest a table. Medium+ findings under the bar are shown in "저자 확인
요청" with their `what`, never folded away. Pre-existing and minor (≤ 10 LOC over, complexity
≤ 3) breaches are table-only.
Findings on non-diff lines are demoted to the summary with a warning (`--strict` to fail
instead). Secrets are masked. GitHub `approve` posts as `COMMENT` unless `--allow-approve`.
The script refuses a moved head, a closed MR, and a second post for the same head. Report
the read-back table it prints, not the POST responses.

When the user did not ask to post, the deliverable in chat is: the level that ran, verdict, the
"지적" table, "저자 확인 요청", the 자동 검사 table, "검토했으나 문제 없음", rule proposals, and one
line per refuted candidate (title + winning skeptic reason; at the inline levels the prescreen
reason from `prescreened.json`). Do not paste the inline bodies. The
summary's first paragraph must name only defects that appear in the tables or in "저자 확인
요청" — never mention a finding the reader cannot find below.

### 4b. Remember refutations (team memory)

```bash
python3 <skill>/scripts/record_refuted.py --result <out_dir>/workflow-result.json --context <out_dir>/context.json
```

Appends evidence-backed refutations (skeptic confidence ≥ 80) to `<repo>/.issueops/pr-review/refuted.jsonl`
— commit it with the repo. The next run's prescreen drops a same-file candidate whose title/what overlap
≥ 0.5 with a recorded refutation; `security`/`data` candidates are never suppressed. Prescreen kills are
not recorded (they carry no evidence).

### 4c. Re-review of a moved head

Run preflight with `--incremental`: when `<out_dir>` already holds `workflow-result.json` and
`context.prev.json` from the previous head, only units whose files changed since that head are
re-inspected and findings on untouched files are carried (`carried_from`). Findings on changed
files are dropped and re-found or not. `post_review.py` still validates every line against the
new diff.

### 5. Clean up

Read `context.json` before cleanup. Remove a worktree only when its non-null `worktree`
field resolves exactly to `<out_dir>/worktree`; a null field means preflight reused the
caller's checkout and it must never be removed. Remove an isolated review worktree with
`git worktree remove --force <out_dir>/worktree` on every exit path, including
`eligible=false` and validation failures. Delete throwaway specs the reproducer left.

## Scope and Disclosure

Only changed/newly reachable lines qualify; pre-existing debt needs explicit
evidence that this change worsened it. Name unread units and unverified
("probably/may/could") claims rather than presenting a complete/verified review.
Never approve through another path or post twice for one head.

## Stop and Optional Background

Done after the requested chat report or authorized post readback, plus cleanup.
No findings is valid with traced `verified_ok`; never pad. Missing evidence,
failed agents, or incomplete coverage must remain visible. Do not resolve
threads, merge, silently upgrade effort, or add a posting approval the user did
not give. In an IssueOps cycle return evidence to its owning stage for authenticated
recording and preserve its lifecycle/actor/generation/cwd and publication gates.

[Lenses](references/lenses.md) and [verification](references/verification.md)
provide optional detail; this body's effort, output, and posting rules govern.
