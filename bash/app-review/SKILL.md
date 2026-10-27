---
name: app-review
description: >
  Internal /ace:run step — Review the built apps as CommCare apps; route defects to builder, brief or platform.
user-invocable: false
disable-model-invocation: false
---

# App review (Phase 3 Step 1.8)

The `pdd-to-*-app-eval` skills ask **"was the brief built?"** This step asks the question
none of them asks: **"is the result a good CommCare app?"** It judges the app the way a field
worker meets it and the way an app builder would read it, then routes every defect to the
layer that can fix it. An app can pass every eval and still ship a case type nothing ever
opens, a question that is a paragraph long, and twenty hidden fields doing arithmetic.

The rubric is hal's `commcare-app-review` (§§2-5 and the §9 catalog), applied per build
(P12, approved by Jonathan 2026-10-23). **Report-only: nothing here blocks the build**, and
nothing here edits the app.

**Not `app-ux-eval`.** That grades screenshots off an emulator against PDD journeys, in deep
QA. This reads the blueprint, with no emulator and no PDD, and judges the app on its own terms.

## Inputs

Pipeline-only: it reviews a run's built pair against that run's Step 1.4 snapshots and Step 1.6 eval verdicts, which exist only inside a Phase 3 pass. To review an arbitrary Nova app outside a run, use hal's `commcare-app-review`.

| Source | Artifact | Used for |
|---|---|---|
| Phase 3 Step 1.4 | `nova_snapshot` per app (`nova-app-snapshot_<app>.json`, as rewritten by the latest re-lint) | every read in this step |
| Phase 3 | `3-commcare/pdd-to-{learn,deliver}-app_summary.md` | `nova_app_id` per app |
| Phase 3 Step 1.6 | the eval verdicts | marking each defect `already flagged by an eval` or `new` |

## Step 1 — one freshness check per app, then no Nova reads

If Step 1.7 attached any media, re-run the Step 1.4 lint with `--snapshot-out` first (every
write is followed by a re-lint, and that rewrites the snapshot). Then, once per app:

```bash
ACE_ROOT="${CLAUDE_PLUGIN_ROOT:-$(python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/plugins/installed_plugins.json'))); print(d['plugins']['ace@ace'][0]['installPath'])")}"
TSX="node $ACE_ROOT/node_modules/tsx/dist/cli.mjs"
$TSX "$ACE_ROOT/scripts/nova-app-snapshot.ts" --snapshot <nova_snapshot> --app <nova_app_id> --check
```

Exit 0 `FRESH` → use it. Exit 4 `STALE` → re-run `nova-app-lint --snapshot-out` and use the new
file. Exit 3 `UNKNOWN` → the same: one fresh read. **Never review a snapshot that is not
`FRESH`**; a review of a pre-edit app reports defects the app no longer has. After this step,
read forms only through `--outline` and `--form <formUuid>`, never `get_form`.

## Step 2 — the structural checks, in code

```bash
$TSX "$ACE_ROOT/scripts/nova-app-review.ts" \
  --learn <learn snapshot> --deliver <deliver snapshot> \
  --out <run>/3-commcare/app-review.json --md <scratch>/app-review_structural.md
```

`lib/nova-app-review.ts` decides what a function can decide: case types created but never
acted on, types opened but never created, follow-up case lists with no search, question labels
past 250 characters, inlined languages (§9-A), and the §9-B/C/E workaround signatures. Exit 3 =
a snapshot is partial. Re-read it; never report it as clean. **Do not re-derive these checks by
hand.** The script owns them, and a second copy in prose drifts.

## Step 3 — the judgment passes, reading the same snapshot

These are the parts code cannot decide. Pull `--outline` once, then `--form` only for the forms
each pass needs: the Deliver forms a worker fills in at a visit, and the Learn assessment plus
one teaching module. Do not walk every form.

**§2 Field-worker pass (Deliver).** Read each visit form top to bottom as the person holding the
phone, standing at a door, on a 5-inch screen:
- **Ordering:** does the sequence follow the visit (arrive, greet, consent, then data), or the
  data model?
- **Dead ends:** a required question with no valid answer for a real case (no phone, refuses,
  structure vacant) strands the worker before submit.
- **Arithmetic at the doorstep:** if the worker computes a band, total or score, that is a
  defect.
- **Register:** is it written to be read aloud, or to be complied with?

**§4 Content pass (Learn), and the seam (§1).**
- Does each assessment item test a behaviour the Deliver app requires, or recall of the
  training's own wording? Map items to Deliver forms. Items that map to nothing are trivia.
  Deliver behaviours with no item are the real gap.
- Does a passing score mean the worker is ready? Does the training describe a flow the Deliver
  app actually has?

**§3 What the script flagged.** For each `case-type-never-opened` / `-never-created` /
`case-list-no-search` finding, read the PDD's data model once and say whether it is **correct
by design** (a record type a Labs report reads; participants imported from a census) or a real
defect. A finding you clear stays in the report, marked `cleared: <reason>`. Silently dropping
it hides the reasoning.

## Step 4 — route every defect (§5)

| Layer | The defect is theirs when | What happens to it |
|---|---|---|
| **builder** (Nova) | the blueprint cannot express the correct app, so any agent would produce the same workaround | known catalog item (`knownIssue` set) → cite it, do not refile. New → **hand to hal** (Step 5) |
| **brief** (ACE) | Nova could express it and the brief did not ask, or asked for the wrong thing | an ace issue when the cause is in a skill or prompt; otherwise a decisions row for this run |
| **platform** (CommCare/Connect) | the constraint is real, upstream, and correct to work around | note it; do not file it |

**When in doubt between builder and brief, it is brief.** One run cannot prove a missing
primitive. That takes the same workaround built independently in an unrelated opportunity,
and that cross-opportunity comparison is hal's job, not this step's. Mark each defect
`eval: flagged` if a Step 1.6 eval already named it, else `eval: new`. The `new` count is
what this step adds.

## Step 5 — builder findings go to hal, never to commcare-nova

**ACE does not file on commcare-nova.** A new builder finding is a hypothesis. Hal's
`commcare-app-review` §6/6b/6c verifies it against Nova `origin/main`, against Classic's own
source, and against Nova's reachable surfaces, and checks it across opportunities before
anything is filed. Of the first five Nova issues filed without that check, three were wrong.

Write the new builder findings into `app-review.json` under `forVerification`. If there are
any, open **one** issue on `dimagi-internal/hal`, which hal drains every turn. First search
for an open one for this run, so a re-run adds nothing:

```bash
gh issue list -R dimagi-internal/hal --state open --search "app-review <opp>/<run-id> in:title" --json number
gh issue create -R dimagi-internal/hal \
  --title "app-review <opp>/<run-id>: <N> Nova-routed finding(s) to verify (§6)" \
  --body-file <scratch>/app-review_hal.md
```

In the body, give each finding's app id, module, form, field ids, the symptom, and why it looks
like a missing primitive rather than a brief choice. Add the run's Drive link to
`app-review.json`. Zero new builder findings → no issue.

## Products

- `3-commcare/app-review.md` has three parts. First, what the apps are: the shape table from
  Step 2. Second, the defects worst-first, grouped by layer, each with evidence, `eval:
  flagged|new` and its route. Third, what the apps got right. On a Nova-built app that list is
  long, and leaving it out makes the review read as a complaint rather than a measurement.
- `3-commcare/app-review.json` holds the script's findings, the judgment findings appended in
  the same shape, and `forVerification`.
- `run_state.yaml` → `phases.commcare-setup.steps.app-review`: `status`, `findings`
  (by layer), `new_vs_evals`, `hal_issue` (URL or null).

## Traps

| Trap | What to do |
|---|---|
| Calling a Nova gap from one run | route it to hal (Step 5); the cross-opportunity check decides it |
| `get_form` "just to be sure" | the snapshot IS what `get_form` returned; a live re-read is what P12 removed |
| Grading against the PDD | that is the evals' job. This grades the app as an app; the PDD is read only to clear §3 findings |
| Repairing what you found | report-only. A real blocker is the evals' and the lint's to gate |
| Filing "the form is too long" | not actionable; name the fields and the primitive that would remove them |
