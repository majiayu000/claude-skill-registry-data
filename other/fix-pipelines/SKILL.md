---
name: fix-pipelines
description: Use when CI jobs are red on a Gramax branch and need diagnosing/fixing — failed pipeline, broken build/tests, flaky jobs, a job that has been red for a while, "почини пайплайн", "почини все пайплайны", "сломанные джобы", "failed CI jobs", "pipeline red", "fix the pipeline".
---

# Fixing Gramax CI pipelines

Diagnose and repair red CI jobs on a branch of the Gramax product repo
(`ics/doc-reader`, id `155`). Sweep the branch's **recent pipeline history** —
not just the newest pipeline — build a worklist of every distinct broken job,
then fix them all in one run.

Runs headless in CI (see the `ci` skill for the shared environment) or locally
from the team workspace. Non-interactive when headless: decide and act.

**Harness run recipes + env + gotchas live in `REFERENCE.md` — read it before
reproducing anything.**

## Target branch

- CI: `$CI_COMMIT_BRANCH`.
- Local: current checked-out gramax branch —
  `git -C gramax rev-parse --abbrev-ref HEAD`.

## Algorithm

### 1. Sweep the pipeline history — build the worklist

Scan the last **20 pipelines** on the branch (`$SWEEP_DEPTH`, default 20). One
pipeline is not enough: a job can be red for weeks, be skipped by `rules:` in
the newest run, or fail only intermittently. History is what tells those apart.

```sh
BRANCH=${CI_COMMIT_BRANCH:-$(git -C gramax rev-parse --abbrev-ref HEAD)}
DEPTH=${SWEEP_DEPTH:-20}

# 1. recent pipelines for the ref
glab api "projects/155/pipelines?ref=$BRANCH&per_page=$DEPTH" \
  | jq -r '.[]|"\(.id)\t\(.status)\t\(.updated_at)\t\(.sha[0:8])"'

# 2. every failed job across ALL of them — the raw sweep
for PID in $(glab api "projects/155/pipelines?ref=$BRANCH&per_page=$DEPTH" | jq -r '.[].id'); do
  glab api "projects/155/pipelines/$PID/jobs?per_page=100" \
    | jq -r --arg p "$PID" '.[]|select(.status=="failed")|"\($p)\t\(.id)\t\(.name)\t\(.created_at)"'
done | tee /tmp/failed-jobs.tsv

# 3. per job name: how many pipelines it failed in (frequency = flaky signal)
cut -f3 /tmp/failed-jobs.tsv | sort | uniq -c | sort -rn

# 4. decisive error for one occurrence — newest first
glab api "projects/155/jobs/$JOB_ID/trace" | tail -50
```

**Group by job name, not by job id** — the same broken `next-e2e-pw` across 8
pipelines is *one* worklist item, not eight. For each distinct job name record:

- **Failure rate** over the swept window (`failed pipelines / pipelines that ran it`).
- **First bad pipeline** — the oldest consecutive failure; the commit between it
  and the preceding green one is the suspect.
- **Decisive error line**, read from the newest occurrence.
- **Root cause class** (below). Different error signatures under the same job
  name = separate worklist items.

**Classify each into one root cause:**

- **code bug** — an app-source change broke the build or a test.
- **test bug** — the test is wrong/stale; product code is fine.
- **runner infra** — OOM, timeout, native-module rebuild failure, image/tag
  mismatch, external-dependency outage.
- **flaky** — fails intermittently across the window while the same commit also
  passed. History proves this; a single pipeline never can.

Then order the worklist: **persistent breaks before flaky ones, oldest break
first.** Report the full worklist before starting — an item you skip must be
named with a reason, never dropped silently.

### 2. Work the list — reproduce, fix, verify (per item)

For **each** worklist item, in order:

1. **Reproduce.** Follow the `REFERENCE.md` recipe for that harness — it
   documents the preflight (`install-deps.sh`, native `better-sqlite3` rebuild,
   the `gramax-core.node` addon) and the exact run command. **Confirm the same
   failure locally before touching code.** Can't reproduce → mark the item
   `unreproducible`, report the env gap, move to the next item. Don't guess.
2. **Fix.** Apply the **narrowest** change for the cause class (targeted guard
   at the call site, not a global/config change).
3. **Verify.** Re-run that harness locally, confirm green. Not green → the item
   is unfixed; say so, don't count it as done.

Finish the whole list before landing anything. One hard item does not cancel the
easy ones — a blocked item is reported, the rest still ship.

### 3. Land all fixes in ONE commit

**All verified fixes from the run go into a single commit** — not one per item.

| Target branch          | CI / test fixes only | Batch contains any app-code fix |
| ---------------------- | -------------------- | ------------------------------- |
| `release/*`, `develop` | push direct          | whole batch → one MR            |
| any other branch       | push direct          | push direct                     |

The batch is atomic: one app-code fix on `release/*`/`develop` sends **the whole
commit** through an MR (title English, body Russian, `## Notes`; use the
`merge-request` skill). Never split the batch to route parts differently.

Commit message lists every fixed job by name, one line each, plus the items left
unfixed and why.

- All writes bot-authored (`GITLAB_CLAUDE_ACCESS_TOKEN`) + initiator credit
  (`.claude/scripts/gitlab-initiator` → `Co-Authored-By: <Full Name> <Email>`).

### 4. Report

Final output = the worklist with an outcome per item: `fixed` / `unreproducible`
/ `flaky, not patched` / `external, not ours`. Nothing disappears from the list.

## Cause → action

| Cause | Action |
| --- | --- |
| code bug | fix source; land per table (MR on release/develop) |
| test bug | fix/adjust the test; it's a CI/test fix → push direct |
| flaky | history already shows whether it recurs — intermittent across the window and never reproducible locally → report it, don't patch product code on a guess |
| runner infra (ours) | fix CI config/resources (timeout, memory, native rebuild) → push direct |
| runner infra (external outage) | report, do not patch — nothing to fix in our code |

## Red flags — stop

- Looking at only the newest pipeline. Sweep the window — that's the point.
- Stopping after the first fixed item while the worklist still has entries.
- Dropping an item from the report because it was hard. Name it + say why.
- One commit per fix, or splitting a mixed batch across a push and an MR.
- Pushing a fix you never reproduced/verified locally.
- Patching product code for a flaky failure.
- A broad global/config change to silence one job — prefer the narrowest layer.
- Editing enterprise/`ges` harnesses — out of scope (see `REFERENCE.md`).
