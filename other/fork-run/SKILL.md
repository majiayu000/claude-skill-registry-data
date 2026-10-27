---
name: fork-run
description: >
  Fork an existing ACE run at a phase or skill boundary via ace-web, copying upstream artifacts into
  a new run. Use to A/B test a skill change or re-run a phase tail without overwriting a run.
disable-model-invocation: false
---

# fork-run

Branches an ACE run at a point in its lifecycle. Artifacts upstream of that
point are copied into a new run under `ACE/<opp>/runs/<new-run-id>/`; the fork
point and everything after it are left empty so they re-run fresh.

Calls ace-web's REST fork endpoint — the server does the Drive copy (it holds
the user's Drive OAuth credentials, so they never reach the client).
Authenticates with `ACE_WEB_PAT_TOKEN` — ACE's own ace-web token by default — and
names the human it is acting for in `requested_by` (see
[`skills/_ace-web-attribution.md`](../_ace-web-attribution.md)).

> **A fork point is ONE concept with TWO spellings.** Name a **phase**
> (`fork_at_phase`) to re-run it whole, or a **skill** (`fork_at_skill`) to keep
> that phase's earlier artifacts and re-run from that skill onward. Exactly one
> is required; both resolve to the same internal `ForkPoint`.

## Inputs

Pipeline-only: forks an existing run at a phase boundary; the source run is the object (§ Process).

## When to use

- **Validate a code change against a prior run's upstream artifacts.** After
  fixing a Phase 6 recipe, fork at `qa-and-training` to get a fresh Phase 6 over
  the same PDD/apps/Connect opp.
- **Re-run the tail of a phase, keeping its earlier work.** Fork at
  `fork_at_skill: app-hq-settings` to redo Phase 3 from Step 2.65 while keeping
  the built + deployed apps. This is usually what you want when one late step in
  a phase was broken.
- **Compare two skill versions head-to-head.** Fork twice, diff the verdicts.
- **Investigate a phase-N failure without re-running 1..N-1.**

For "retry in place, overwrite history" — no fork record, tightest loop —
dispatch the phase subagent directly against the existing run
(`Agent(ace:<phase>)`).

## Verified contract

Verified against ace-web `origin/main` @ ace-web#736 (2026-08-27):
`apps/api/api.py:155`, `apps/opps/api.py` (`fork_opp_endpoint`,
`fork_status`, `_write_fork_progress`), `apps/opps/schemas.py`
(`OppForkIn`, `ForkProgress`), `apps/opps/opp_forker.py`,
`apps/opps/skills.py` (`resolve_fork_point`).

**Route** — workspace-scoped. The router mounts at `/w/{workspace_slug}/opps`:

```
POST ${ACE_WEB_BASE_URL}/api/w/<workspace_slug>/opps/<slug>/fork
```

**Body** — `OppForkIn` is a `StrictModel`, so any unknown key is a hard 422
`extra_forbidden`, not a silent ignore:

| field | required | notes |
|---|---|---|
| `fork_at_phase` | **one of** | a `phase:` value from `agents/*.md` — re-runs the phase whole |
| `fork_at_skill` | **one of** | a skill name — keeps that phase's earlier artifacts, re-runs from this skill |
| `source_run_id` | no | defaults to the opp's latest run |
| `mode` | no | `keep-all` (default) or `keep-overrides-only` |
| `edits` | no | list of `{row_id, new_answer}` decision overrides applied during the fork |
| `feedback` | no | ≤8000 chars; seeded as the **first user turn** of the new run's working session |
| `requested_by` | **yes (ACE rule)** | email of the human this fork is for. Resolve it per [`_ace-web-attribution.md`](../_ace-web-attribution.md). ace-web (#845) records it next to `initiated_by` in run_state, on the working session, and echoes both in the 201 |

Exactly one of `fork_at_phase` / `fork_at_skill` — neither or both is a 422.

**What a fork does NOT carry: a pre-fork phase's `screenshots/` and
`videos/`.** Device-walk evidence from a phase STRICTLY BEFORE the fork point
is left in the source run (ace-web#758). It is not lost — a fork never deletes
from the source, and the training deck references those images by Drive FILE
ID, so a deck copied into the fork still renders them. Nothing at or after
Phase 7 consumes them: the manifest's consumers for the Phase 6 screenshot
artifacts are all Phase 6 skills.

The reason is that copying them made a deep fork fail. Forking
`spark-facilitator/20260907-1120` at Phase 7 queued 178 Drive copies; Phase 6's
`screenshots/journey-deliver/` alone held 35 of them, and the fork died at file
50 on a `userRateLimitExceeded`, stranding a half-populated run as the opp's
LATEST — which is what `source_run_id` defaults to. Copy volume grows with
phase depth, so the most valuable forks were the most likely to die. A skill
fork of the walk's OWN phase still keeps its media; the skip is strictly
upstream.

**What a fork DOES carry: `previews/`.** Output previews
(`<N>-<phase>/previews/<output-slug>/`, contract v1 — e.g. the Learn/Deliver app
screenshots Phase 6 writes into `3-commcare/previews/`) are not in the skipped
media subtrees. A fork that carries Phase 3 carries its app previews, which is
correct: they show the same apps the fork carries.

`copy_file` also retries a 429 now (five attempts, 2/4/8/16s) and still does
NOT retry a 5xx: a rate limit proves the write never ran, a 5xx does not, and
retrying that duplicates.

**How a skill fork trims.** Phases before the fork skill's phase copy whole;
phases after are empty. Within the fork skill's own phase, an artifact is kept
iff the skill that produced it has a lower ordinal. Attribution comes from
`lib/artifact-manifest.ts`'s `producedBy`, **not** from parsing
`<skill>_<role>.ext` filenames — so artifacts that don't follow the convention
(e.g. `deliver-connect-coverage.md`) aren't silently dropped. Anything the
manifest can't attribute is **kept**.

**`fork_at_phase` values** (`phase:` in `agents/*.md` frontmatter — grep it, don't
trust this table):

| ordinal | `fork_at_phase` |
|---|---|
| 1 | `idea-to-design` |
| 2 | `scenarios-and-acceptance` |
| 3 | `commcare-setup` |
| 4 | `connect-setup` |
| 5 | `ocs-setup` |
| 6 | `qa-and-training` |
| 7 | `synthetic-data-and-workflows` |
| 8 | `solicitation-management` |
| 9 | `execution-management` |
| 10 | `closeout` |

**`mode`:**

- `keep-all` (default) — every upstream row (phases before the fork) stays
  LIVE, both AI defaults and overrides. Use when iterating on one downstream phase.
- `keep-overrides-only` — only human-ruled rows (`overridden` /
  `human-decided`) stay live; every AI default is RETIRED (below) so
  downstream re-derives it. Use when you suspect upstream AI defaults shaped
  downstream phases badly.

**What the fork does to `decisions.yaml` — the history is kept, never
dropped (ace#2582, operator decision 2026-10-02).** A row the fork does not
keep live is RETIRED by ace-web (`opp_forker.py::_retire_decision_rows`):

- its id moves to `<id>-<source-run-id>`, so the canonical id is FREE for the
  re-run producer (`decisions_append_rows` skips an existing id — which is how
  inherited rows used to beat the re-run);
- it gets `superseded_by: <id>` — the plugin's own supersession field
  (ace#1421), so `liveDecisions`, the decisions Doc, the
  run-summary page and carry-forward all already read it as history. The
  target is absent until the phase re-runs; then the chain is ordinary;
- it gets `inherited_from_run: <source-run-id>` (declared in
  `lib/decisions-schema.ts` so appends preserve it), and the Doc labels it
  *inherited, not this run's choice*.

Retired: every row whose `<N>-` phase tag is at or after the fork phase (on a
skill fork, the fork phase's rows whose `skill` ran before the fork skill stay
live, like their artifacts). Never retired: human rulings, and pre-fork rows,
which carry forward byte-for-byte. Contract test:
`test/lib/decisions-fork-retired.test.ts` (fixture = the real
`spark-facilitator/20261001-2208` rows run through ace-web's transform).
Before this, ace-web resolved the row's `phase` tag (`3-commcare`) against
AGENT names (`commcare-setup`), matched nothing, and kept every row live — the
trim never fired on any real run. A fork made on a deploy older than ace-web's
fix shows it: no `inherited_from_run` anywhere, and Phase 3+ rows live under
their canonical ids.

**The plugin checks it, and repairs it (schema v6, `docs/decisions-contract.md
§ Re-runs`).** After the fork returns, read the new run's `decisions.yaml`. If
no row carries `inherited_from_run` while a live row's phase ordinal is at or
after the fork point, the fork came from an old deploy — retire those rows
BEFORE the re-run starts, the same transform ace-web applies:

```bash
node "$ACE_ROOT/node_modules/tsx/dist/cli.mjs" "$ACE_ROOT/scripts/decisions-retire-for-rerun.ts" \
  --decisions <local decisions.yaml> --from-ordinal <fork phase ordinal> \
  --label <source_run_id> --out <local out>
```

then `drive_update_file localFilePath`. A fork that already RE-RAN with the
inherited rows live (every fork before ace#2582 — `spark-facilitator/20261001-2208`
is the reference case) is repaired after the fact by
`scripts/backfill-decisions-contract.ts`, which supersedes each inherited row
onto the re-run row that replaced it.

**Response** — `OppForkOut`: `{slug, run_id, working_session_slug}`. Note the
field is `run_id`, not `new_run_id`.

**The POST BLOCKS for the whole Drive copy.** This is the single most
important thing on this page, and this doc said the opposite ("forks are
async") until ace-web#734. There is one Drive `copy_file` per artifact at
~150 ms, so a six-phase fork runs for **minutes** and can outlive a client
or proxy read timeout. Always pass `--max-time`, and treat a timeout as
"still running", never as "didn't start".

**Never retry a POST that didn't come back.** A retry mints a *second* run
and copies everything again. Recover the run-id from the status poll
instead (below) — that is what it is for.

**Progress** — poll `GET /api/w/<ws>/opps/<slug>/fork/status`, optionally
with `?source_run_id=<id>`; omit it and you get whichever fork of this opp
reported most recently, which is what you want when your POST timed out and
you have no run-id. Response is `ForkProgress`:

| field | notes |
|---|---|
| `status` | `unknown \| counting \| copying \| finalizing \| done \| error` |
| `new_run_id` | **populated from the moment the run folder exists**, not just on `done` — this is your recovery handle |
| `new_slug` | the opp slug (unchanged; a fork stays within its opp) |
| `files_copied` / `files_total` | counts, not `copied` / `total` |
| `progress` | 0.0–1.0 |
| `error` | set with `status: error` |

`status: unknown` means genuinely nothing has reported — no fork started, or
its 10-minute cache entry expired. It is **not** what an in-flight fork
looks like. (Before ace-web#736 it was the only thing this endpoint could
ever say, on any fork: the forker emitted field names the strict response
model rejected. If you see `unknown` throughout a fork you can watch
happening in Drive, you are on an ace-web older than #736.)

**An interrupted fork is still a run.** ace-web writes `run_state.yaml`
before the first artifact is copied, so a fork that dies mid-copy leaves a
resumable-but-incomplete run: `/ace:run <opp>/<run-id>` picks it up and
re-derives what is missing. Don't hand-author state, and don't assume a
partial fork is garbage.

## Env vars

- `ACE_WEB_BASE_URL` — e.g. `https://labs.connect.dimagi.com/ace`. Source: `.env`.
- `ACE_WEB_PAT_TOKEN` — ACE's own ace-web token, written by `/ace:setup`
  (or your own, if you minted one with `/ace:ace-web-pat-mint`).
- `requested_by` — not in `.env`. The human this fork is for; see
  [`_ace-web-attribution.md`](../_ace-web-attribution.md).
- `workspace_slug` — **not** in `.env`. Resolve it from `GET /api/workspaces`,
  or read it off any ace-web run URL (`/ace/opps/<workspace>/<opp>/runs/...`).
  For the Dimagi tenant it is `dimagi-team`.

Both env vars are pre-flighted by `/ace:doctor` `[Auth liveness]`.

## Process

1. **Pre-flight env.** Read both from `$CLAUDE_PLUGIN_DATA/.env`. Halt naming
   the missing var and the fix:

   ```
   ACE_WEB_PAT_TOKEN not set. Run /ace:setup (it writes ACE's own
   ace-web token), then retry.
   ```

   Then resolve `requested_by` per
   [`_ace-web-attribution.md`](../_ace-web-attribution.md). With no
   resolvable human, stop and ask. Never omit the field.

2. **Resolve `workspace_slug`** if the caller didn't supply it (see above).

3. **Validate inputs.** `opp_slug` non-empty, and exactly one of
   `fork_at_phase` / `fork_at_skill`. A phase must appear as a `phase:` value in
   `agents/*.md`; a skill must be a `skills/<name>/` directory. Check locally —
   it's the most common failure, and checking here turns a round-trip into an
   instant, specific error.

4. **POST.** Send only the fields in the table above:

   ```bash
   set -o pipefail
   url="${ACE_WEB_BASE_URL%/}/api/w/${workspace_slug}/opps/${opp_slug}/fork"
   body=$(jq -n \
     --arg phase "${fork_at_phase:-}" \
     --arg skill "${fork_at_skill:-}" \
     --arg src "${source_run_id:-}" \
     --arg mode "${mode:-keep-all}" \
     --arg fb "${feedback:-}" \
     --arg rb "${requested_by:?requested_by is required — see skills/_ace-web-attribution.md}" \
     '{mode: $mode, requested_by: $rb}
      + (if $phase == "" then {} else {fork_at_phase: $phase} end)
      + (if $skill == "" then {} else {fork_at_skill: $skill} end)
      + (if $src   == "" then {} else {source_run_id: $src} end)
      + (if $fb    == "" then {} else {feedback: $fb} end)')
   # --max-time bounds the wait; the POST blocks for the whole copy, so
   # pick generously (600s) and treat exit 28 as "still running".
   resp=$(curl -sS --max-time 600 -w '\n%{http_code}' -X POST "$url" \
     -H "Authorization: Bearer $ACE_WEB_PAT_TOKEN" \
     -H "Content-Type: application/json" \
     -d "$body")
   curl_rc=$?
   http_code=$(printf '%s\n' "$resp" | tail -1)
   payload=$(printf '%s\n' "$resp" | sed '$d')
   ```

   **If `curl_rc` is 28 (timed out) — or you got no response at all — do
   NOT re-run this step.** Go to step 4b.

4b. **Recover a timed-out POST.** The fork is almost certainly still
   running or already finished; you just lost the response. Poll for the
   run-id rather than minting a second run:

   ```bash
   surl="${ACE_WEB_BASE_URL%/}/api/w/${workspace_slug}/opps/${opp_slug}/fork/status"
   for _ in $(seq 1 60); do
     st=$(curl -sS --max-time 30 -H "Authorization: Bearer $ACE_WEB_PAT_TOKEN" "$surl")
     printf '%s\n' "$st" | jq -r '"\(.status) \(.files_copied // 0)/\(.files_total // 0) \(.new_run_id // "-")"'
     case $(printf '%s\n' "$st" | jq -r .status) in
       done|error) break ;;
     esac
     sleep 10
   done
   ```

   Read `new_run_id` off any payload once the run folder exists. On
   `error`, that run folder is still resumable (it has a `run_state.yaml`)
   — report the `error` string and the run-id, and let the operator choose
   between `/ace:run <opp>/<run_id>` and trashing it. If the poll says
   `unknown` for a full minute, and only then, is "nothing started" a safe
   conclusion.

5. **Branch on status.** Errors are problem+json; the machine-readable code is
   in **`detail`** (`title` is prose, `status` is the HTTP code):

   | status | `detail` | meaning |
   |---|---|---|
   | 2xx | — | success — parse `run_id` + `working_session_slug` |
   | 400 | `invalid-mode` | `mode` not one of the two literals |
   | 400 | `invalid-fork-point` | neither or both of `fork_at_phase` / `fork_at_skill` |
   | 400 | `unknown-phase` | `fork_at_phase` isn't a registered phase (or a stale `ACE_PLUGIN_PATH`) |
   | 400 | `unknown-skill` | `fork_at_skill` isn't in the skill registry |
   | 404 | `source-not-found` | `opp_slug` not in Drive |
   | 404 | `no-runs` | opp has no `runs/` folder — old single-run layout |
   | 404 | `source-run-not-found` | `source_run_id` not under `runs/` |
   | 422 | `extra_forbidden` in `extras.errors[].type` | you sent a field the schema doesn't have |
   | 401/403 | — | token invalid/revoked → `/ace:setup` (ACE's token) or `/ace:ace-web-pat-mint` (yours) |
| 400 | `extras.code: requested_by_forbidden` | a HUMAN token sent a `requested_by` other than its owner. Drop it, or use ACE's token |
| 422 | `requested_by` in `extras.errors[]` | `requested_by` is not a valid email |
   | HTML body | — | **wrong route.** An unrouted path falls through to the SPA catch-all and returns a bare HTML 404, not JSON. Check `/api/w/<ws>/opps/...`. |
   | *no response* | — | **not an error.** The POST blocks; you timed out, the fork didn't. Go to step 4b — never re-POST. |

6. **Check the typed handoffs crossed the fork (ace#1888 / ace#2341). Not optional.**
   ace-web now carries each copied phase's `products` block (ace-web#760) and a
   skill fork's kept steps (ace-web#765) — on the DEPLOYED ace-web, which can
   lag the merge (see § Known issues). A phase marked `done` with no `products`
   is asserting a completion it cannot back — and every existing fence reads it
   green. So audit it here, where the fork just happened and the source run is
   still in hand; exit 0 is the expected result on a current deploy:

   ```bash
   # read costs zero context with writeToPath; then classify locally
   ACE_ROOT="${CLAUDE_PLUGIN_ROOT:-$(python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/plugins/installed_plugins.json'))); print(d['plugins']['ace@ace'][0]['installPath'])")}"
   node "$ACE_ROOT/node_modules/tsx/dist/cli.mjs" "$ACE_ROOT/scripts/check-products-gap.ts" \
     /tmp/forked_run_state.yaml --label "<run_id>"
   ```

   (`/tmp/forked_run_state.yaml` comes from
   `drive_read_file(fileId: <the new run's run_state.yaml>, writeToPath: ...)`.)

   Exit 0 = clean. Exit 1 = **BLOCKING**: phases remain pending and at least one
   upstream phase owes a handoff. Exit 2 with a `products-gap ADVISORY` status
   = gaps exist but nothing is left to dispatch.

   **On a non-zero exit, do not report the fork as ready.** Seed each named
   phase's `products` block **verbatim from the source run** —
   `update_yaml_file` with `merge: 'deep'`, one phase at a time — and record
   what you did and where it came from in a top-level `seeded_products_note`.
   Never re-derive a products value by hand: it is a record of what another
   system did, and a plausible-looking substitute is the "close the loop to the
   source of truth" failure (CLAUDE.md § Conventions). Then re-run the check
   until it exits 0.

7. **Report.**

   ```
   Forked ACE/<opp>/runs/<source_run_id>/ → runs/<run_id>/
   Fork point: <phase|skill> (earlier work copied; from here on re-runs)
   Mode: <mode>
   Products handoffs: <clean | seeded N phase(s) from <source_run_id>>
   Workbench: <ACE_WEB_BASE_URL>/chat/<working_session_slug>

   Next: /ace:run <opp>/<run_id> to resume there.
   ```

## Known issues

**`products` blocks now cross the fork — ace#1888 CLOSED (ace-web#760,
2026-09-08) for phase forks, ace#2341 CLOSED (ace-web#765, 2026-09-10) for
skill forks.** Both take effect on the ace-web DEPLOY that carries them, not on
the merge (ace-web deploys are `workflow_dispatch` on `main`) — so read the
forked `run_state.yaml`, never the PR state, to know which behaviour you got.
What each fixed:

- **Phase fork** (ace-web#760): every copied phase's `products` block is
  carried verbatim. Before it, a forked run's phases carried
  `status: done, verdict: seeded` and no typed handoff, so a downstream phase
  that dereferenced one (`demo-data-setup(ace-run)` reads
  `phases.connect-setup.products.connect.opportunity.connect_int_id`) got a
  confusing empty result rather than a clean halt.
- **Skill fork** (ace-web#765): the fork-point phase's `steps.<skill>` entries
  BELOW the fork skill (plus their `-qa`/`-eval` companions) are carried
  verbatim, the fork skill and later steps are `pending`, the phase reads
  `status: in_progress` with a `fork_note`, and `verdict`/`completed_at` are
  omitted so the phase must re-complete. Before it, the whole block was reset
  to `steps: pending, products: {}` and the kept artifacts were orphaned —
  `demo-data-setup` re-ran, and the live labs workflows named in
  `products.synthetic.workflows{}` became orphans (measured 2/2 on
  `spark-facilitator/20260909-2242` and `/20260910-0541`).

  **The skill fork carries `products` BY ATTRIBUTION** (ace#2354). The plugin
  declares which skill writes each products key — `PRODUCT_PRODUCERS` in
  `lib/phase-products-schema.ts`, dotted keys, emitted as
  `phases.<phase>.productProducers` in `docs/phase-products-schema.json` — and
  ace-web's `apps/opps/skills.py::product_producers` reads it, so the forker
  keeps only the keys whose producer ran BELOW the fork skill. `products.synthetic`
  is written by three parties and is attributed one level down: a Phase 7 fork
  at `demo-narrative` carries `synthetic.source` / `.labs_opp_id` /
  `.workflows` / `.provider` / `.render_code_patched_this_run`
  (`demo-data-setup`) and DROPS `synthetic.narrative` (`demo-narrative`) and
  every `synthetic.ddd_*` (the Phase 7 agent). A key the map does not cover is
  carried and NAMED in `fork_note` — never dropped silently. Against an ace-web
  older than the consuming PR, or a plugin older than 0.13.1431, the forker
  falls back to carrying the block whole with an `UNATTRIBUTED` note; on such a
  run, re-derive `narrative` / `ddd_*` rather than trusting the carried value.
  Contract: `agents/orchestrator-reference.md § Product-key producers`.

The gap was easy to miss because **every fence read it green.**
`verify_phase_artifacts` passes (the Drive files really were copied),
`classify_phase_writeback` reads `ok` (the status block really is well-formed),
and `verify_phase_products` returns `ok:true` on a *wholly absent* block for
any phase with no entry in `REQUIRED_PRODUCT_KEYS` — measured on
`hh-poverty-targeting/20260901-1932`: `idea-to-design` ok=true, `ocs-setup`
ok=true, both with no `products` key at all. Step 6 above stays as the
regression check for exactly that class: on a fork made after the deploy it
should exit 0, and a non-zero exit means the deploy is behind the merge.
*Enforced:* `lib/upstream-products-gap.ts` +
`test/lib/upstream-products-gap.test.ts`, whose controls are transcribed from
the forked run and its source.

*(This section read "None currently open" while the skill was 100% broken —
see § History. If you're relying on it, spot-check the contract against
ace-web source instead.)*

## History — why this file is source-verified

This skill was **100% non-functional** from 2026-04-20 to 2026-07-27, and its
Known-issues section read *"None currently open"* the whole time (ace#985).

**What actually happened:** ace-web had two fork implementations.
`apps/opps/fork.py` did skill-granular forks with a seeded working session —
which is exactly what this doc described, and it was real. It was deleted in
`289ee20` ("run forking gone with multi-run") because it trimmed by a
`steps/<NN>-<skill>/` layout the multi-run redesign replaced. The older
phase-level `opp_forker.py` survived, so *a* fork endpoint still existed and
nothing noticed ACE was pointing at a corpse. The later `/api/v2/ → /api/`
rename moved the route again.

So the doc wasn't fiction — it documented a real endpoint that was removed, and
no test on either side noticed for three months.

**Restored in ace-web#698** (2026-07-27): skill-granular forking and `feedback`
seeding are back, unified onto the surviving endpoint. A fork point is now one
concept with two spellings rather than two competing implementations.

**A prior fix attempt made it worse.** ace#978 corrected one row of the old
skill-name table without noticing skill names were the wrong vocabulary for
*that* endpoint — raising the doc's confidence while it stayed broken. Fixing
the map while the road was out.

**Preventer:** `test/fork-run-phase-references.test.ts` asserts every fork point
this file offers resolves in the agent registry. It does **not** yet assert the
route exists — that's the half that actually broke here, and it wants a contract
check (POST an invalid body, assert a JSON 4xx rather than the SPA's HTML 404).

## History — the second failure, 2026-08-27 (ace-web#734)

The untested half broke again, and this file's "forks are async" line was
part of why it hurt. A phase-level fork of `hh-poverty-targeting` copied all
six phase folders, then stalled before writing `run_state.yaml` — so the
result was a folder, not a run. Three compounding defects on the ace-web
side, all fixed in ace-web#736:

1. **`run_state.yaml` was written last.** It is what makes a folder a run
   (`/ace:run` derives execution order from `phases.*.status`), so a stall
   in the tail wasted the whole copy. It is now written *first*, before any
   artifact — which is why an interrupted fork is now resumable.
2. **`fork/status` could never report.** `ForkProgress` is a strict model;
   the forker emitted `copied` / `total` / `opp_slug` against its
   `files_copied` / `files_total` / `new_slug`. Not one payload could
   validate, on any fork, ever. Seven polls across five minutes all said
   `unknown` while folders were visibly landing in Drive.
3. **The poll's cache key didn't match the writer's** when
   `?source_run_id=` was omitted — precisely the caller recovering from a
   hung POST, who has no run-id to poll with.

**What this file got wrong:** it said forks are async. They are not; the
POST blocks for the whole copy. Combined with (2), an agent following this
doc saw a hung POST and an inert poll and had every reason to retry —
which mints a second partial fork. Documenting the blocking contract, the
`--max-time` bound, and the never-retry rule is the ace-side half of the
fix.

**Lesson for this file specifically:** "verified against ace-web source"
covered the request shape and the error codes, but not the *timing* or the
*response* contract of the companion endpoint. When a skill documents an
async-looking pair (start + poll), verify the poll actually returns
something a caller can act on — not just that the route exists.

## Related

- `upload-transcript` — same shape (POST to ace-web with PAT), same env vars.
- `/ace:ace-web-pat-mint` — provisions `ACE_WEB_PAT_TOKEN`.
- `agents/orchestrator-reference.md § Fork Points` — the per-opp vs per-run
  artifact design this endpoint implements.
- ace-web source: `apps/opps/api.py`, `apps/opps/schemas.py`,
  `apps/opps/opp_forker.py`.

## Change Log

| Date | Change | Author |
|---|---|---|
| 2026-10-03 | **Build memo retired — decisions.yaml is the review artifact (schema v6).** Step 6b (re-compose the memo after a fork past Phase 4) and the report's `Build memo:` line are removed — a fork's review artifact is its decisions log, whose re-run rows are already retired and re-emitted per phase. Contract: docs/decisions-contract.md. | ACE team |
| 2026-10-02 | **A fork keeps the decision history but retires what it re-runs (ace#2582).** Rows at/after the fork point are moved to `<id>-<source-run-id>` and marked `superseded_by: <id>` + `inherited_from_run` by ace-web, instead of staying live under their canonical ids (where they silently beat the re-run's appends) — `spark-facilitator/20261001-2208` carried 33 Phase 4/5/8 rows it never ran and hand-minted 27 `-2208` corrections. Schema declares `inherited_from_run`; the Doc labels such rows as inherited. | ACE team |
| 2026-10-01 | **Step 6b: re-compose the build memo after a fork past Phase 4.** `spark-facilitator/20260926-1800` (forked from 20260925-1536) carried its source's memo titled "run 20260925-1536", and its `products.connect.build_memo` pointed at the SOURCE run's Doc rather than the copy in its own `4-connect/` — so the run page showed a memo for a different run, and build-memo-eval flagged the label. `/ace:step build-memo <opp>/<run_id>` now runs after any fork whose `connect-setup` is done; the report states it. | ACE team |
