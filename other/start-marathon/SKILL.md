---
name: start-marathon
description: >
  Start marathon preparation from intake through reviewed implementation plans, honest contracts,
  disjoint lanes, MARATHON.yaml, preflight and dry-run. Use for "start marathon", "marathon", a
  marathon queue, or a viability check of marathon docs another session prepared. Route an
  ambiguous bare "marathon" here; ask which arc only if live evidence cannot identify one.
  Explicit fire/execute requests use the confirmed marathon command after this preparation.
  Legacy /marathon-triage requests use this same workflow. Requires the PROJECT lifecycle, RELEASES
  roadmap ledger and the resolved XYZ harness. Does not dispatch by default.
---

# Start marathon

Prepare an honest, runnable marathon plan without firing work. Treat `PROJECT/**` as the execution
record, GitHub as the live signal stream, and deterministic preflight output as stronger than prose.

## Routing

- **Primary — start or substantially revise an arc:** follow Steps 0–6, including intake review,
  contract review, implementation plan drafting and independent plan QA, lane computation, plan and
  YAML preparation, preflight, and dry-run. Choose real work with a per-item machine-checkable pass
  condition. At most one long-horizon marathon may be in flight; check the RELEASES roadmap's
  Immediate next-up and active marathon rows before preparing a competing arc.
- **Secondary — another session prepared the docs:** verify the existing issue, doc, review receipt,
  contract, and current commit. Run focused smoke checks, direct preflight, planner `--check`, and
  `marathon.sh --plan <file> --dry-run`. Repair a concrete stale input and recheck; do not rewrite a
  sound plan or duplicate its issue/ledger row. If required inputs are absent, enter the primary path
  at the first missing step.
- **Explicit firing:** `start-marathon` only prepares the exact command and evidence. The existing
  `/pre-marathon` command may fire after the operator confirms the dry-run-approved plan and order.
  A bare “marathon” is never implicit authorization to dispatch.

---

## Recite this — verbatim, as the first thing in your first response

> **Start-Marathon Discipline:**
> 1. **Resolve the harness and arm the guard (Step 0).** Run the locator block first — it exports `$HARNESS` and is the relay-xyz guard's proof-of-load; with the guard enabled and no prior proof-of-load, planner/preflight calls are cancelled with exit 2.
> 2. **Inventory and reconcile (Steps 1–2).** List every open issue and every `GH-*.md` capture; give each exactly one classification from live GitHub state, never from stale local text.
> 3. **Capture the intake that is missing (Step 3).** For each in-scope open issue with no capture doc, render it with the existing writer and park its ledger row; list what was written.
> 4. **Prepare and review (Steps 4–5).** Ground each contract and implementation plan in current code, obtain independent plan QA, compute disjoint lanes, prepare YAML, and run direct preflight plus the actual `marathon.sh --dry-run`. Record exits and repair bounded defects.
> 5. **Report with decisions (Step 6).** Report the classification, reviewed plans, exact verdicts, collision map, waves, and runnable command; state any blocker. Firing and closing stay behind the operator's exact-plan confirmation.
>
> **Overall Goal:** `/start-marathon`, an ambiguous “marathon,” or legacy `/marathon-triage` yields a reviewed, preflighted, dry-run-approved marathon proposal without dispatch.

Then begin work.

---

## Guardrails

- Read `ROUTER.md`, `AGENTS.md`, `GUIDING-PRINCIPLES.md`, the RELEASES DB (`releases roadmap list`), and `PROJECT/PDDA.md` first.
- **The default includes ordinary readiness computation.** `marathon_plan.py --dry-run --deep`
  publishes no plan file (`--dry-run` prints the report only; `--deep` delegates to
  `swarm-preflight.sh --dry-run` per ready item) and `swarm-preflight.sh --dry-run` publishes no
  packet — but neither is side-effect-free: preflight runs `git fetch --prune` on the target and adds
  then removes a detached temporary worktree at `target.ref` (`utils/py/swarm_preflight.py`
  `:1297`, `:1355-1361`, `:1378-1380`) before its dry-run exit. That is Git metadata and a transient
  worktree, not a published artifact. Run them; do not ask whether to. If the operator explicitly
  asks for a *strictly read-only audit*, that override covers the metadata effects too: skip Step 3's
  writes and report the captures you would have written, and either obtain readiness evidence from an
  authorised disposable clone or report it as **unavailable** — a skipped preflight is not a verdict.
- **Writing a `1-INBOX` capture doc and parking its ledger row through the writer is intake.**
  Create the umbrella issue and a derived full clone for the selected arc during preparation; both
  are needed to make a YAML plan and dry-run concrete. Report their identifiers.
- The request authorizes reversible preparation: promote a selected capture under PDDA, write its
  reviewed plan, create a task branch in a fresh full clone where the repo SOP requires it, and write
  the planner file and YAML. Do not close issues or fire until the exact plan/order is confirmed.
  Preserve an existing plan and receipt unless evidence requires a revision.
- Incidental findings outside the marathon task go into root `PARKED/` under its README contract.
  Do not expand the arc or file an issue merely to park a finding. During triage, promote selected
  items through issue-first `PROJECT/1-INBOX/GH-*.md` capture and RELEASES roadmap registration;
  leave a promotion pointer in PARKED. A blocker to the selected marathon stays in its active plan.
- Recovery is bounded: diagnose a concrete failure with `workhorse`, then use `unstuck` if a session
  stalls or repeats a step without new evidence. Re-run the affected check once after a material
  correction. If the same condition persists, report the blocker; do not bypass a deterministic
  verdict, exceed `LANE_MAX_ATTEMPTS`, re-fire a parked lane, or fabricate readiness.
- Never override a deterministic PDDA or preflight finding with narrative judgment.
- Use the repo's standing target branch policy. Do not invent a branch or silently substitute a
  builder.
- If GitHub is unavailable, mark live-state evidence `UNKNOWN`; do not infer it from stale local text.
- **Orchestrator vs. review separation (GH-784).** The orchestrator cannot self-satisfy the review
  contract or attest review solely by observing test suites; it must mechanically invoke an
  independent peer/Codex QA turn before sign-off. Wave completion requires on-disk receipts under
  `relay-system/` and all wave checklist items checked.

---

## Drive loop — how an agent runs this skill end to end

Follow the steps in order; each has an exit contract and a next action. **Do not stop at the first
non-zero exit — classify it.** Every run ends in one of two report shapes (Step 6): a **complete
report**, or a **blocked report** that names the command, its exit code, the evidence that could not
be established and the next action. Asking the operator whether to run a step is neither.

| Step | Command / action | Exit → action |
|---|---|---|
| 0 | locator block below | locator not found → **blocked report** (install the skill or set `XYZ_HARNESS`); else continue |
| 1 | `gh issue list` + `find PROJECT/1-INBOX PROJECT/2-WORKING` | `gh` failure → live state `UNKNOWN`, continue with local docs |
| 2 | one classification per issue and per doc | — |
| 3 | render + park each missing capture | writer refusal → record it per issue, continue |
| 4 | reconcile contracts; draft/review implementation plans; run `marathon_plan.py --dry-run --deep` | `0` clean → continue · `2` usage → fix and retry once · `3` ledger error → block · `4` drift / `5` held → classify and repair selected items · `6` unavailable GitHub → mark UNKNOWN; other codes → block |
| 5 | direct `swarm-preflight.sh --dry-run` per candidate; audit collisions; prepare YAML; run `marathon.sh --plan <file> --dry-run` | Preflight: `0` READY, `3` NEEDS-CONTRACT, `4` CONTRACT-STALE, `5–7` BLOCKED; usage `2` → correct once. Dry-run failure → repair and retry once, then block |
| 6 | report | the **Done rule** below decides whether it may claim *completion*; otherwise it is a blocked report |
| 7 | firing boundary (operator-confirmed only) | recheck umbrella, ledger, clone and exact approved plan/order; then hand to `/pre-marathon` |

**Done rule:** claim a complete preparation only when (a) each in-scope issue and capture has one
classification and written captures have ledger rows; (b) selected items have current, reviewed
implementation plans and valid contracts; (c) every selected candidate has a direct preflight exit
and verdict; (d) the planner report or `--check` records waves, held items and drift; (e) audited
write-sets are disjoint within each wave; and (f) the exact YAML and `marathon.sh --dry-run` exit 0
are recorded. A failed or unavailable check yields a blocked report with command, exit, missing
evidence and next action, not fabricated readiness.

**Permission-classifier blocks:** if a harness permission layer cancels a planner or preflight call,
first check that Step 0 actually ran in this session (the `relay-xyz guard — STOP` message means it
did not); then retry the identical command once before escalating.

---

## Workflow

### 0. Resolve the harness root — this is also the guard's proof-of-load

**Run this block as the first Bash call of the session.** Besides exporting `$HARNESS`, a Bash call
that runs `find-harness.sh` is what the relay-xyz guard hook
(`relay-automation/hooks/relay-xyz-guard.sh`) accepts as proof the skill stack is loaded.
`marathon-plan` and `swarm-preflight` are Tier-A entrypoints (Bash shims and Python twins alike).
With the guard enabled and no prior proof-of-load in this session, calls to them are blocked with
exit 2 and the message `relay-xyz guard — STOP` (the hook is fail-open and session-scoped; a session
that already loaded `relay-xyz` is not blocked). The remedy is to run this block, not to ask the
operator.

```bash
L=""
for candidate in "${XYZ_HARNESS:+$XYZ_HARNESS/skills/1-hourly/relay-xyz/find-harness.sh}" \
                 "$HOME/.claude/skills/relay-xyz/find-harness.sh" \
                 "$HOME/.codex/skills/relay-xyz/find-harness.sh" \
                 "$HOME/.gemini/config/skills/relay-xyz/find-harness.sh" \
                 "$HOME/.gemini/antigravity/skills/relay-xyz/find-harness.sh" \
                 "$HOME/.gemini/antigravity-cli/skills/relay-xyz/find-harness.sh" \
                 "$(git rev-parse --show-toplevel 2>/dev/null)/.claude/skills/relay-xyz/find-harness.sh" \
                 "$(git rev-parse --show-toplevel 2>/dev/null)/skills/1-hourly/relay-xyz/find-harness.sh"; do
  [ -n "$candidate" ] && [ -f "$candidate" ] && { L="$candidate"; break; }
done
[ -n "$L" ] || { echo "relay-xyz: locator not found — install the skill or set XYZ_HARNESS" >&2; exit 1; }
eval "$("$L" --env)"
```

Reference every script below as `$HARNESS/utils/swarm-preflight.sh`,
`$HARNESS/utils/py/marathon_plan.py` and `$HARNESS/utils/hq/hq-lib.sh` — not bare `utils/...` paths,
which resolve to nothing (or to an unrelated `utils/` directory) in a vendored `.xyz/` install.

### 1. Inventory intake and active work

List open issues and all issue capture docs in deterministic order:

```bash
gh issue list --state open --limit 200 --json number,title,labels \
  --jq 'sort_by(.number) | .[] | "\(.number)\t\(.title)\t[\(.labels|map(.name)|join(","))]"'

find PROJECT/1-INBOX PROJECT/2-WORKING -maxdepth 1 -type f \
  -name 'GH-[0-9]*.md' -print | LC_ALL=C sort -V
```

Read the ledger's parked pointers (`releases roadmap list`) and each candidate's frontmatter, status table, acceptance criteria, and
`Swarm Preflight Contract`. Do not treat a title match as a contract.

### 2. Reconcile each issue document

Query each issue number with one batched `gh issue list` or `gh issue view`. Assign exactly one
classification:

| Classification | Meaning | Recommendation |
|---|---|---|
| `STALE-CLOSED` | Capture is active but the issue is closed | Reconcile outcome; move to `3-COMPLETED` only if shipped, otherwise `4-MISC` |
| `READY` | Open, promoted, valid contract, dry-run exit 0 | Candidate for ranking |
| `CONTRACT-STALE` | Preflight exit 4 says the fix already landed | Verify delivery evidence; propose reconciliation |
| `NEEDS-PROMOTE` | Open, contract exists, still in `1-INBOX` | Propose promotion and full active-doc contract |
| `NEEDS-CONTRACT` | Open, no valid preflight JSON contract | Propose bounded acceptance and write-set contract |
| `NEEDS-CAPTURE` | Open, in scope, and no `GH-<n>-*.md` exists in `1-INBOX` or `2-WORKING` | **Write the capture now (Step 3)**, then classify as `NEEDS-CONTRACT` |
| `BLOCKED` | Preflight exits 5, 6, or 7 | Report the exact blocker; do not queue |
| `NOT-A-WORK-ITEM` | Feedback, report, duplicate, deferred, or meta-only | Exclude and explain |
| `UNKNOWN` | GitHub or required evidence unavailable | Exclude until verified |

A contract exists only when valid JSON appears under a heading matching `Preflight Contract` and
satisfies `$HARNESS/utils/swarm-preflight.sh`'s current schema (Step 0). Run the script rather than
hand-validating it.

### 3. Capture the intake that is missing — with the existing writers

For every `NEEDS-CAPTURE` issue, produce the same two artifacts `hq park --create` produces for a
new issue, using the same functions it uses. Never hand-author frontmatter, never add a second
write path:

```bash
source "$HARNESS/utils/hq/hq-lib.sh"      # hq_render_capture, hq_roadmap_line, hq_slug
NUM=<n>; URL="https://github.com/<org>/<repo>/issues/$NUM"
TITLE="$(gh issue view "$NUM" --json title --jq .title)"
BODY="$(gh issue view "$NUM" --json body --jq .body)"
CREATED="$(gh issue view "$NUM" --json createdAt --jq '.createdAt[0:10]')"
DOC="PROJECT/1-INBOX/GH-${NUM}-$(hq_slug "$TITLE" | tr '[:lower:]' '[:upper:]').md"

# <num> <src> <title> <created> <doc_type> <project> <repo> <request> — ratings default to
# ratings_provisional: true, which marathon-plan already parks out of active waves.
hq_render_capture "$NUM" "$URL" "$TITLE" "$CREATED" bugfix <project> <org>/<repo> "$BODY" > "$DOC"

python3 "$HARNESS/utils/py/releases_app.py" roadmap add \
  --issue-num "$NUM" --issue-url "$URL" --title "$TITLE" --created "$CREATED" --doc-path "$DOC" \
  --raw-text "$(hq_roadmap_line "$NUM" "$TITLE" "$CREATED" "$DOC" "$(basename "$DOC")" "$URL")"
python3 "$HARNESS/utils/py/releases_app.py" roadmap list | grep "GH-$NUM"     # read the row back
```

Use `feedback` instead of `bugfix` for a non-defect capture. A doc written here is a capture, not
an active-work doc: it carries no `## Status` table until promotion. Record each `(issue, doc path,
ledger gid)` for the report. If `roadmap add` fails, the intake is **half-complete** (doc exists, no
row) — report it as such with the writer's error, never as success. `NOT-A-WORK-ITEM` issues get no capture and are listed with
the reason.

### 4. Review contracts, draft plans, then compute

For each selected member, read the issue's current body/comments, the active doc, actual code entry
points and writes, and relevant tests. Reconcile acceptance, dependencies, target branch, fix probes,
`artifacts`, `artifacts_new`, and lanes against that evidence. Use `recon` for unfamiliar stateful
code and `swe` for plan quality. Revise a stale contract in the canonical doc and rerun preflight;
a syntactically valid JSON contract with dishonest paths is still blocked.

For work beyond a simple edit, finish the implementation plan in its canonical `PROJECT/2-WORKING`
doc: goal, scope, current-state map, blast radius, one ordered phase list, explicit write-sets and
dependencies, per-phase acceptance and QA, rollback for Costly changes, and final integration gate.
Use Phase 0 for uncertainty that prevents a truthful contract; write its findings back before later
phases. Review an existing plan for freshness before rewriting it. Run independent plan QA with
`relay-xyz` (Agy or Codex per operator choice); resolve findings and record the review artifact and
verdict. A self-reviewed plan is not complete QA. Missing runtime capability becomes a separate
parked dependency and holds its lane.

Check RELEASES ratings and the PDDA risk gate. `ratings_provisional: true` and `risk > 2` prevent
automatic selection. #443 owns the fuller PRS freshness gate; until it lands, inspect rating and
issue update timestamps and hold uncertain ratings rather than claiming planner verification.

```bash
python3 "$HARNESS/utils/py/marathon_plan.py" --dry-run --deep
```

`--dry-run` prints the report and writes no `MARATHON-PLAN-*.md`; `--deep` runs
`swarm-preflight.sh --dry-run` for every ready item and folds the verdicts in. Quote the waves, the
held items and any drift lines in the report. Handle the exit code per the drive loop table; `3`
(ledger unparseable) turns the run into a blocked report, as does any other unmet Done-rule
After contract and candidate review, if a current `MARATHON-PLAN-*.md` already exists, run the
planner with `--check` first: `--check` reports whether it is in sync, reporting drift without
overwriting it. Write the canonical plan with the planner **without** `--dry-run` only when the file
is absent, inspect its diff, and run `--check`. Revise an existing plan only when concrete evidence
or operator review explicitly justifies the revision; drift is a finding for the report, not an
automatic reason to regenerate or overwrite an in-flight or reviewed plan. This is reversible
preparation authorized by a start request; a mismatch is drift, not success.

#### Wave Lifecycle Contract & /start-task Step-8 Parity (GH-784)

Marathon batch execution must strictly enforce the `/start-task` double-relay protocol per wave
rather than collapsing execution into a single build-and-push loop:

1. **Wave Plan QA (Step 6 parity):** Before coding a wave, conduct independent plan QA via
   `relay-xyz` (Codex reviewer default). Commit review inputs so isolated reviewers can see them.
2. **Wave Build & Proof-of-Done:** Implement the wave's changes within its declared allowlist.
   Execute the wave's Proof of Done test suite green (runnable command + test exit 0).
3. **Wave Post-Build Codex QA Relay (Step 8 parity):** Before pushing feature branches or opening
   PRs, execute an independent Codex review turn against the committed wave diff and test receipts.
   Record the on-disk receipt under `relay-system/<YYYY-MM-DD>/<label>.codex.md`.
4. **Adjudication:** Adjudicate and resolve all findings from the Codex QA turn and CodeRabbit / Peer
   Review.
5. **Orchestrator vs. Review Protocol Separation:** The Orchestrator (the Claude dispatch/tool
   driver) cannot self-satisfy the review contract or attest review solely by observing passing test
   suites. It must mechanically invoke an independent peer/Codex QA turn before sign-off.

#### Acceptance & Quality Checklist Contract

Every marathon plan (`PROJECT/2-WORKING/MARATHON-PLAN-*.md`) must mandate an explicit per-wave
verification section:

```markdown
## Acceptance & Quality Checklist

### Wave 1
- [ ] Wave 1 Proof of Done Test Suite Green (runnable command + test exit 0)
- [ ] Wave 1 Post-Build Codex QA Relay executed (receipt recorded under `relay-system/<YYYY-MM-DD>/<label>.codex.md`)
- [ ] Wave 1 CodeRabbit / Peer Review findings adjudicated
```

Mechanical check: set `TARGET_ROOT` to the absolute root of the repository whose plan is being
executed, `CANONICAL_PLAN` to its absolute plan path, and `WAVE` to the positive wave number being
admitted. Bind both commands to that consumer root:
```bash
python3 "$HARNESS/utils/pdda/check_marathon_qa.py" --root "$TARGET_ROOT" --pre-pr --wave "$WAVE" --doc "$CANONICAL_PLAN"
# or via pdda.sh (also binds the activity log to the consumer):
PDDA_REPO_ROOT="$TARGET_ROOT" "$HARNESS/utils/pdda/pdda.sh" marathon-qa --root "$TARGET_ROOT" --pre-pr --wave "$WAVE" --doc "$CANONICAL_PLAN"
```
Use a positive wave number and one explicit plan. Every declared wave must retain its mandatory
checklist structure; only the selected wave must be complete for this PR. Future waves remain
honestly pending. For final closeout, omit `--wave` from the same command to require all waves.
Completed docs always require all waves, even if a selector is supplied.

Checked receipt citations must resolve on disk under the consumer root. Codex receipts for checked
or required items must have a first `STATUS:` header of `Approved` or `Closed`; ordinary Markdown
links and backticked paths are supported. Empty, missing, nonterminal and placeholder receipts
fail. This checks recorded terminal status, not independent authorship or exact reviewed SHA;
the independent review and head verification above remain required. Routine aggregate scans warn
on pending items in active plans.

### 5. Preflight, form lanes, and dry-run the actual marathon

Run preflight **directly for every candidate** that is not `NOT-A-WORK-ITEM` or `UNKNOWN`, including
the ready items `--deep` already touched — deep delegation discards preflight output and only
handles exits 4/5/6/7, so it cannot supply a candidate's recorded exit and verdict. Use paths for
inbox docs and issue numbers for promoted docs:

```bash
"$HARNESS/utils/swarm-preflight.sh" --project-doc PROJECT/1-INBOX/GH-<n>-<slug>.md --dry-run
"$HARNESS/utils/swarm-preflight.sh" --gh-issue <n> --dry-run
```

Record the exact exit and verdict: ready `0`, usage `2`, invalid contract `3`, already landed `4`,
not ready `5`, blocked target `6`, or ambiguous `7`. Every code maps to a classification in Step 2;
none is a reason to stop.

Audit `artifacts`, `artifacts_new`, and `lanes` against the issue's actual scope. Flag placeholder,
missing, over-broad, or unrelated write-sets; a ready exit does not make a dishonest write-set safe.

Ranking and waves: apply the PDDA selection rule — gate on `risk <= 2`, then rank by lowest
`effort + complexity`, then fewest `phases`. Do not store a new composite score. Place lanes together
only when their declared and audited write-sets are disjoint and all zone caps hold. Shared ledgers
such as the RELEASES DB and `CHANGELOG.md` collide. Kernel paths obey the repo's
one-kernel-lane-per-wave cap.

For the selected arc, create or reuse the umbrella issue and RELEASES marathon row before preparing
executable YAML. Keep one `PROJECT/2-WORKING/<arc>/MARATHON.yaml` and phase briefs. Use the current
checked-in YAML examples and `marathon.sh` parser for supported keys: `name`, ordered `phases`,
unique `id`, `brief`, exact `artifact`, builder/reviewer, `depends_on` where needed, and round/time
bounds. Record member issues and umbrella identity in comments and briefs. Preserve sound existing
YAML. Audit real writes, generated files and shared ledgers before declaring lanes disjoint.

Run focused smoke checks for changed plan/brief paths, then run the no-dispatch command from a
disposable full clone on the intended task branch:

```bash
"$HARNESS/relay-automation/marathon.sh" --plan PROJECT/2-WORKING/<arc>/MARATHON.yaml --dry-run
```

Inspect its complete output and exit, including worker availability, branch, dependencies,
collisions, paths and gates. The secondary route runs the same command after existing-doc review
and `marathon_plan.py --check`. A per-phase `marathon-drive.sh --dry-run` is not a substitute for
the full YAML dry-run. A failed dry-run holds the plan. An active marathon or parked lane cannot be
overridden with `--force`; replan through the standing queue.

### 6. Report

Return one of the two shapes. A **complete report** (the Done rule holds) contains:

1. Classification table with issue, doc, live state, contract state, and reason — one row per open
   issue and per `GH-*.md` doc.
2. Captures written in Step 3: issue, doc path, ledger gid; and the issues excluded with reasons.
3. Reviewed implementation plans and QA receipts, the planner output (waves, held, drift), and each
   selected candidate's direct preflight exit and verdict.
4. Collision map, YAML path, focused smoke result, and the exact full-plan dry-run command and exit.
5. Decisions needed — one **default recommendation per item**, not a flat symmetric list of
   options the operator has to weigh unaided. For each item that needs a call, emit:

   ```
   RECOMMEND: <the single default action — commit captures | archive | close | revise contract | unblock | confirm exact plan and fire | hold>
   BECAUSE:   <the evidence behind it — live state, preflight verdict, rating, collision risk>
   UNLESS:    <the specific condition under which the operator should override the default>
   ```

   The operator starts from the recommendation and only overrides when the `UNLESS` clause
   holds — never from a blank menu. Reserve a bare options list only for genuinely balanced
   calls where no default is defensible, and say so explicitly.

A **blocked report** contains everything above that *was* established, plus one line per
unmet requirement: the command run, its exit code, the evidence that could not be established, and
the next action. It never contains fabricated waves or verdicts.

Keep the default report inline. If the operator requests a persisted report, write a dated
`PROJECT/1-INBOX/START-MARATHON-YYYY-MM-DD.md` with `doc_type: report`, source/provenance, and
`roadmap_exempt: true`. If promoted to `2-WORKING`, add the full PDDA frontmatter, exact status table,
and the ledger pointer. Never execute the marathon from this skill.

### 7. Firing boundary — umbrella identity and derived full clone

Create or reconcile umbrella identity during preparation. Before firing, verify the selected plan,
ledger row, clone, dry-run evidence and order still match the operator's confirmation. Dispatch only
after that exact confirmation.

#### 7a. Every marathon has an umbrella tracking issue

**A marathon without a GitHub umbrella issue does not start.** The umbrella is the marathon's
identity: waves, clone folder, ledger row and closeout all key off its number.

Today this is under-enforced and the gap is measurable: `releases_app.py marathon add` requires
`--tracking-issue` (`utils/py/releases_app.py:4901`) and `marathons.tracking_ref_id` is `NOT NULL`
(`:479`) — but the executor never reads either. `marathon_drive.py` has no `--tracking-issue` flag
and the `MARATHON.yaml` schema has no field for one, so the requirement binds only if someone
chooses to create the ledger row. Most runs have not: **at least eight marathons are visible in
committed transcripts and `marathon-system/`, against two rows in the `marathons` table.**

Procedure, before the selected marathon fires:

1. Open the umbrella issue. Title it for the arc, not the first item. Body lists the candidate
   member issues, the wave sketch, and the acceptance rule for the marathon as a whole.
2. Register it in the ledger immediately:
   ```bash
   python3 "$HARNESS/utils/py/releases_app.py" marathon add \
     --tracking-issue https://github.com/<org>/<repo>/issues/<n> --status planned
   ```
   Offline, `TMP-XXXXXX` is an accepted placeholder — but reconcile it before the marathon closes,
   or the ledger row permanently names an issue that does not exist. The token is **shape-checked
   only** (`check_tracking_token`, `:1675-1694`); GitHub is never queried, so a typo in the URL is
   accepted silently.
3. Dial every member issue into the same release, and link them to this marathon.

Carry the umbrella number into every downstream artifact: the clone folder name (7b), the plan
doc, each phase brief, and the closeout. If you cannot name the umbrella issue, the marathon is not
ready to fire — the triage report is where that arc gets decided.

#### 7b. Marathons run in a full clone, deterministically named

**Two rules, both currently unenforced by code.** State them explicitly in the plan so a reviewer
can check them.

**A full clone, never a linked worktree and never the primary checkout.** The mechanism that makes
this necessary is real but indirect: `validate.sh:16-53` refuses to run inside a linked worktree
(GH-45, exit 2), and `driver_lock_path_for_repo` (`relay-automation/driver-lock-lib.sh:20-35`)
resolves a linked worktree's lock to its **parent's** `.git/relay-driver.lock`, so a worktree
cannot run a second driver concurrently. Nothing refuses a marathon launched from the primary
checkout — `test/gh35-test-tiers.sh:367-370` proves the primary checkout runs the gate normally —
so this rule is on the operator, not the harness.

**Clone folder name is derived, not chosen:**

```
marathon-gh-<umbrella-issue-number>-<short-description>
```

`<short-description>` is lowercase, hyphen-separated, three words or fewer, describing the arc —
not a wave label, not a phase number. One clone per marathon; a second attempt at the same arc
reuses the name with a `-r2` suffix rather than inventing a new slug.

```bash
CLONE="$HOME/marathon-clones/marathon-gh-${UMBRELLA}-${SLUG}"
git clone <remote> "$CLONE"
```

This replaces the current free-form convention, which has drifted badly and is the reason a
salvage operation once could not find its own artifacts: live folders are `gh271-waveA`,
`gh396-phase0` and `gh405-mock-board` — a wave label, a phase number and a feature name, three
different meanings under one shape — while committed transcripts also show `gh-8-…` and `gh-115-…`
with a different separator, plus a `gh-115-clean` retry folder with no stated relationship to its
original.
