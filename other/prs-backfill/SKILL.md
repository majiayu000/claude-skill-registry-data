---
name: prs-backfill
description: >-
  Backfill and keep current the PRS four-axis ratings (pri/sev/appeal/effort, 1-100) on
  registered roadmap rows that are still unrated. Trigger on "/prs-backfill", "backfill PRS
  ratings", "rate the unrated issues", or a scheduled enrichment pass. A deterministic script
  inventories open issues against releases.db and builds bounded evidence packets; the agent
  proposes scores and a dated rationale under the start-task rating policy; an independent
  reviewer (different agent/model) must agree; the script freezes a hashed plan, and the
  operator's approval of that hash authorizes writes through `releases roadmap rate` only -
  never --force, never --ovr. Also runs the E0 blind calibration against already-rated rows.
  Does not register issues, write capture docs, admit work to Jog, or re-score rated rows.
  Requires gh, python3, releases.db at the repo root.
---

# /prs-backfill — complete and current PRS ratings, one writer, reviewed

PRS is the Product Release System, the RELEASES ledger
([definition](https://github.com/HiQS-Labs/XYZ-forge/blob/development/HOW-TO-USE.md#glossary--the-five-terms-youll-hit-first)).
This skill is the first duty of the foreman role in
[GH-1175](https://github.com/HiQS-Labs/XYZ-forge/issues/1175): small blast radius (rating
columns on already-registered rows), but it exercises the foreman's primitives — wake, change
detection, single instance, allowed-verb authority, propose → independent review → canonical
write, holds with reasons, receipts, budget, kill switch.

**Read the canonical rating policy first:**
[start-task → Task rating policy](../../1-hourly/start-task/SKILL.md#task-rating-policy). This
skill does not restate or amend it; where the two ever disagree, start-task wins.

## Guardrails (read first)

- **One writer.** Ratings are written only by `releases roadmap rate`, called by
  `prs_backfill.py apply`. Never edit `releases.db`, `releases.sql` or ROADMAP views by hand.
- **No re-scoring.** Already-rated rows are skipped, never `--force`d. An `already-rated`
  refusal is a final answer here. Re-scoring stays a deliberate operator act (start-task).
- **No new overrides.** The script never passes `--ovr`; existing `ovr` rows are never touched.
- **Appeal is 50** unless the operator supplies a value (`--appeal-map`). Never infer it.
- **Effort is cheapness** (100 = quick win). Never copy a PDDA effort value.
- **A rating does not admit work.** #522 admission (plan in the issue + reviewed PRS) still
  gates Jog. If an issue has no remediation plan, say so in the rationale's uncertainty; never
  write the plan.
- **Registration is out of scope.** `roadmap add` needs a capture doc, and the capture
  template belongs to HQ / weekly-prepare (#1022). Unregistered issues are reported only.
- **Legacy `cx/risk/eff` rows are held.** The writer refuses mixing vocabularies; conversion
  is deliberate operator work.
- **Kill switch:** `PRS_BACKFILL_DISABLE=1` stops every subcommand that writes anything —
  `scan`, `validate`, `apply`, `calibrate` (exit 4). `status` stays readable.
- **Sandbox off for `gh`** (TLS/keychain), as in the other GitHub-reading skills.

## Locating the script

Run from the repo being rated (harness root or a repo with vendored `.xyz/` and a Tier 2
`releases.db`):

```bash
PB="bash skills/2-daily/prs-backfill/prs-backfill.sh"        # harness clone
PB="bash .xyz/skills/2-daily/prs-backfill/prs-backfill.sh"   # vendored repo
$PB status
```

The wrapper runs `prs_backfill.py` from its own directory (skill-local: `utils/py/` is frozen by
the GH-777 inventory ratchet; the ledger is opened only via `releases_app.connect`) and rates the repo you run
it in (`--root` > `$PRS_BACKFILL_ROOT` > git toplevel > CWD). Pass `--repo <org>/<repo>` if
`origin` is not a github.com remote.

## Procedure

### 1. Scan (deterministic, read-only on the ledger)

```bash
$PB scan --mode backfill --limit 20     # E1: unrated rows, ascending issue number
$PB scan --mode changed  --limit 10     # E2: unrated rows, most recently updated first
$PB scan --mode calibrate --limit 15    # E0: stratified blind sample of rated rows
```

`--limit` is the model budget for the pass. The scan prints counts per state
(`rated`, `rated-ovr`, `unrated`, `unregistered`, `unregistered-with-doc`, `ambiguous-row`,
`legacy-vocabulary`), a report-only `stale` list (rows this skill rated whose issue CONTENT —
title, body, labels, comments — changed since; `updatedAt` alone is only the pre-filter), and
the run directory. An issue held earlier on the same `updatedAt` is not selected
again — no repeated model calls on unchanged evidence. `--include-held` overrides that for an
operator-attended re-rate (a reviewer disagreed and the rater re-scores); never on a schedule.

### 2. Rate (the agent's judgment)

For each `packets/GH-N.json` in the run directory, apply the start-task policy using the
packet's body, comments, labels and capture-doc excerpt. For recurrence, query the repo's
issues for the stated window (default last 14 days vs the preceding 14) with `gh`; missing
history is "unknown trend", never zero.

Write `proposals.json` from `proposals.template.json`, one object per packet:

```json
{
  "issue": 760, "pri": 40, "sev": 30, "appeal": 50, "effort": 60,
  "confidence": "high | medium | low",
  "rationale": {
    "consequence": "what breaks or is lost, for whom, how recoverable",
    "recurrence": "window, counts or examples, coverage limits",
    "uncertainty": "what would change the scores; missing plan; ambiguity"
  },
  "rater":  {"agent": "claude", "model": "<model id>"},
  "review": {"agent": "codex",  "model": "<model id>", "verdict": "agree", "notes": ""},
  "hold": null
}
```

Set `"hold": "<reason>"` instead of guessing when the issue is ambiguous, is an umbrella that
should be split, conflicts with other evidence, or names an operator preference you do not
have. `low` confidence is held automatically. Rationale fields together stay under 1,200
characters.

In E0 (calibrate), rate blind: do not read the row's scores from `releases.db`, `releases.sql`,
ROADMAP views or prior receipts before writing proposals. A calibrate packet carries no `rating_*`
columns and withholds every `rating:` frontmatter line and every `rated N/N/N/N` /
`pri/sev/appeal/effort N/N/N/N` token in the capture doc, the issue body **and** the comments
(`[rating withheld]`) — including this tool's own `--post-rationale` comments on already-rated rows.
Backfill/changed packets sanitize only the capture doc; a filer's suggested score in an unrated issue
is operator input, so it stays visible — weigh it, flag it in `uncertainty`, rate independently.

### 3. Independent review

Send each non-held proposal with its packet to a different agent/model (for example
`/consult --models codex` or `/relay-xyz`). The reviewer checks the scores against the same
policy and returns `agree`, `adjust` or `disagree` with notes. On `adjust`, revise and
re-review; record only the final verdict. The script holds any proposal whose reviewer is
missing, is the same agent+model as the rater, or did not `agree`.

`--no-review` exists only for an operator-attended E1 batch where the operator reviews the
plan line by line before approving. Never use it on a scheduled pass.

### 4. Validate → plan

```bash
$PB validate --run <run_id> [--appeal-map appeal.json]
```

Prints each item (`GH-N rated P/S/A/E confidence`) and each hold with its reason, then the
plan hash. Holds are recorded as receipts. Show the operator the full plan and holds.

### 5. Apply (operator-approved)

```bash
$PB apply --run <run_id> --approve <plan sha12> --dry-run              # preview every write
$PB apply --run <run_id> --approve <plan sha12> --post-rationale       # write + dated rationale on each issue
```

The start-task policy requires a short dated rationale **with each task's canonical issue or plan**,
not only in this tool's local receipts. `--post-rationale` is how an ordinary batch satisfies it;
leave it off only when the operator records the rationale on the canonical plan doc instead (say so
in the batch report). The 14 ratings of 2026-10-21 were applied without it — their rationales are
in `.tick/prs-backfill/receipts.jsonl` and can be posted with `comment` (below).

Before each write the script re-fetches the issue and holds it if it closed or its content
changed since the scan, and re-reads the row (skipped if already rated, held if ambiguous or
legacy). After each write it reads the row back and requires the exact scores with no `ovr`.
The first failed write or read-back stops the run with exit `3` and a `write-failed` receipt;
follow with `releases check`. A `write-failed` issue is selected again by the next scan (the
evidence did not change, the infrastructure did), unlike a judgment hold. Re-running the same
approval is idempotent.

`--post-rationale` comments the dated rationale on each issue only after the read-back verified the
write; a comment that fails or times out is recorded in the receipt (`commented: false`) and never
undoes or hides a verified write. The flag is off in the code so a scheduled pass cannot post without
an operator's say-so; the attended procedure above passes it.

**Post rationale later.** `apply` skips rows it already applied, so it cannot add a comment after
the fact. For ratings applied without `--post-rationale`, use the same plan approval:

```bash
$PB comment --run <run_id> --approve <plan sha12> --dry-run            # print each comment, post nothing
$PB comment --run <run_id> --approve <plan sha12> [--max-comments N]   # post, one `commented` receipt each
```

It comments only issues whose latest `applied` receipt for that plan is not yet commented, and holds
(`row-changed`) any whose ledger row no longer equals the planned rating. A failed post stops the
run with exit `3`; re-running retries only the uncommented issues.

### 6. Calibrate (E0 only)

```bash
$PB calibrate --run <calibrate run_id>
```

Reports MAE for pri/sev/effort, sev band agreement (low 1–39, mid 40–79, high 80–100),
high-band false-lows, false-highs, and how many proposals kept appeal at 50. Existing ratings
may themselves be agent-made, so agreement is consistency, not ground truth. The operator sets
the pass bar for moving to E1/E2.

## Phases (GH-1175)

| Phase | Mode | Writes | Review |
|---|---|---|---|
| E0 | `calibrate` | none | not required |
| E1 | `backfill` | operator-approved batches | reviewer agrees, operator approves plan hash |
| E2 | `changed` on a schedule | operator-approved, or pre-authorized policy (D3 in GH-1175) | reviewer required |

Scheduling (launchd on the operator's Mac, per #1168 and GH-1175's local-first plan) is not
shipped here; a scheduled pass runs steps 1–4 and leaves `apply` for the approval path.

## Files and exit codes

State lives under `<repo>/.tick/prs-backfill/` (gitignored): `runs/<run_id>/{scan.json,
packets/, proposals.template.json, proposals.json, plan.json, calibration.json}`,
`receipts.jsonl` (append-only provenance: rater, reviewer, rationale, content hash, issue
`updatedAt`, plan hash, writer output, read-back), and `lock`.

Exit codes: `0` ok · `2` usage · `3` refused (gh failure, approval mismatch, schema, or
`apply` stopped on a failed write) · `4` disabled · `5` busy (another instance holds the lock).

## Known limits

- **Provenance is local.** Receipts live in the gitignored `.tick/` of one checkout. GH-1175
  leaves open whether rating provenance moves into ledger columns or `work_events`; until
  then, `STALE` detection (#443) only sees rows this skill rated on this machine.
- **Unregistered issues are not rated.** On 2026-10-21, 182 of 265 open XYZ Forge issues had
  no ledger row and no capture doc; they wait for #1022 / `hq park`.
- **Packets are bounded.** Body 6,000 chars, last 10 comments at 1,000 chars, capture doc
  4,000 chars. A truncated body is flagged (`body_truncated`); read the issue when it matters.
