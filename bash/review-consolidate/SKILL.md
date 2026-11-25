---
name: review-consolidate
description: >
  Review many repos under every lens — one OS process per (repo × lens), all in
  parallel — then consolidate every findings.json into ONE cross-repo document
  grouped by severity then repo. Spawns subprocesses, never subagents.
  Trigger: /review-consolidate <repo> [<repo>...] --out <file.md>,
  "review these repos and consolidate the findings".
argument-hint: "<repo> [<repo>...] --out <file.md> [--lenses a,b,c] [--no-run] [--all]"
---

# review-consolidate — run the matrix, then write one document

Two jobs, in order: **fan out the reviews as parallel subprocesses**, then
**merge their findings into one document**. You review no code yourself.

**Subprocesses, not subagents.** Never use the `Agent` tool. Every review runs
as its own `claude -p` process, one per (repo × lens), launched by
`BASE_DIR/bin/run-matrix.sh` (ADR 0004).

**Shared assets base dir** (`BASE_DIR` below) —
`~/.claude/skills/adversarial-review/`: `CONTEXT.md` (glossary), `agents/`
(reviewer, challenger, judge role packs), `lenses/` (15 lenses), `bin/run-matrix.sh`
(the matrix launcher).

## Phase 0 — Arguments (repos and --out are required)

Parse the argument string:

- **repo paths** — one or more, positional. **Required.** At least one.
- `--out <file>` — the consolidated document path. **Required.**
- `--lenses a,b,c` — restrict the matrix to these lenses. Default: every lens
  except the change-only ones (`test-surface`, `blast-radius`).
- `--no-run` — skip Phase 1; consolidate reports already on disk.
- `--all` — include every report found, not just the newest per (repo, lens).

Stop immediately, with usage, if no repo path is given or `--out` is missing:

> review-consolidate needs repos and an output path:
> `/review-consolidate <repo> [<repo>...] --out <file.md>`

Never guess a default output path and never default the repo list to the
current directory — a consolidated doc written somewhere unexpected, or built
from the wrong repo set, is worse than an error.

Resolve every repo path to absolute. A path that does not exist is a hard error
(name it, list the ones that do). Accept a directory prefix (`307`) only if it
resolves to exactly one directory; if it matches zero or several, error and list
what it matched.

Pick a run stamp (`date +%Y%m%d-%H%M%S`) and a log dir next to `--out`:
`<dirname of --out>/review-matrix-<stamp>.logs`.

## Phase 1 — Run the matrix (parallel subprocesses)

Skip this phase entirely when `--no-run` was passed.

Run the launcher — ONE command, one bash call, it blocks until every child is
done. Do not hand-roll the fan-out and do not launch the children one at a time:

```bash
BASE_DIR/bin/run-matrix.sh --runner claude --log-dir <logdir> \
  [--lenses a,b,c] <repo> [<repo>...]
```

`--runner claude` is required: the launcher defaults to `pi`.
What the script does, so you do not re-implement it:

- one `claude -p` review process per (repo × lens),
  every one launched before it waits — unbounded parallelism, by design;
- one log per pairing at `<logdir>/<repo>-<lens>.log`;
- `<logdir>/manifest.tsv` with `repo, lens, exit, seconds, report, log`, where
  `report` is the `REPORT: ` path each child printed (`none` if it printed none).

The run is long. Use a generous timeout on the bash call and do not poll,
interrupt, or re-run it — a second launch doubles the load on every repo.

Read `manifest.tsv` when it returns. A non-zero `exit` or a `none` report is a
failed pairing: keep its repo, lens, and log path for the **Not consolidated**
section. Never silently drop it and never re-run it — a report that says "the
security lens failed here" is honest; a report missing the security lens lies.

## Phase 2 — Collect the sidecars

For each repo, list `<repo>/.gbencke/adversarial-review/reports/*.findings.json`.

- Prefer the sidecar next to each `report` path from the manifest (same basename,
  `.findings.json`) — that is exactly this run's output.
- With `--no-run`, or for a pairing whose manifest report is `none`, fall back to
  the **newest sidecar per lens slug** (the
  `<stamp>-<target>-<lens>.findings.json` basename carries both). `--all` keeps
  every sidecar instead.
- A repo with no reports dir or no sidecars is not an error — record it as
  `NO REPORTS` and keep going. It is a signal (the review failed or never ran),
  and hiding it would make the doc lie about coverage.
- A sidecar that is not valid JSON is recorded as `UNPARSEABLE` with its path.
  Never guess at its contents.

Load them mechanically — this is data movement, not judgment:

```bash
for f in <repo>/.gbencke/adversarial-review/reports/*.findings.json; do
  jq -c --arg src "$f" '{src:$src, target, mode, date, counts,
    findings: [.findings[] | {severity, lenses, labels, file, line, title,
      failure_condition, suggestion}]}' "$f"
done
```

Report the tally before writing: repos in, pairings run, sidecars read, findings
loaded, pairings failed.

## Phase 3 — Merge

1. Tag every finding with its repo (directory basename) and its lens (from
   `lenses[]`, falling back to the sidecar's lens slug).
2. **Within a repo**, collapse duplicates: same `file` + same defect (same
   title or same root cause) → one entry, lenses merged, highest severity kept.
   The same file gets reviewed by several lenses, so duplicates are expected.
3. **Across repos**, never merge — each repo owns its own fix. Instead, when the
   same defect class appears in ≥2 repos, label every occurrence
   `[CROSS-REPO: n repos]`. That label is the reason this document exists:
   a defect in three repos is a platform problem, not three tickets.
4. Preserve severities as ruled. Never re-severity a finding here — the judging
   already happened, and you no longer have the code in front of you.

## Phase 4 — Write the document to `--out`

Order is fixed: severity first, repo second. Someone reading the top of this
document must see the worst thing across the whole estate.

```markdown
# Consolidated review — <yyyy-mm-dd hh:mm>

Repos: <n> · Lenses: <n> · Findings: <n> (P0 <n> · P1 <n> · P2 <n> · P3 <n>)

## Summary

| Repo | Lenses | P0 | P1 | P2 | P3 | Total | Verdict |
|------|--------|---:|---:|---:|---:|------:|---------|

<one row per repo, then a TOTAL row. Verdict = worst per-lens health.>

## Coverage

| Repo | Lens | Exit | Time | Report | Status |
|------|------|-----:|-----:|--------|--------|

<one row per (repo, lens) from manifest.tsv: exit code, seconds, report
filename, and OK / FAILED / NO REPORTS / UNPARSEABLE. Every requested repo
appears here even with nothing to show.>

## P0 — ship blockers

### <repo>
- **<title>** — `<file>:<line>` · lens(es) · label(s)
  - Fails when: <failure_condition>
  - Fix: <suggestion>

## P1 — real defects
## P2 — structural
## P3 — nits

## Cross-repo themes

<Defect classes present in ≥2 repos, worst severity first: one line per theme
with the repo list. Skip the section entirely if there are none.>

## Not consolidated

<Failed pairings (repo, lens, exit code, log path), repos with no reports,
unparseable sidecars. This section keeps the coverage claim honest.>
```

Rules for the file itself:

- `mkdir -p` the parent of `--out`. Overwrite `--out` if it exists (the caller
  chose the path; a stamped path is the caller's job).
- Write nothing into the reviewed repos yourself. The child processes own their
  reports dirs; you only read them.
- Empty findings across every repo is a valid document: write it with the
  summary and coverage tables and say so. A silent no-op looks like a crash.

## Phase 5 — Summary

Chat reply ONLY: the counts line, pairings run / failed, the worst 5 findings
across all repos (one line each, with repo), and the output path.

Last line, on its own, absolute, prefixed exactly `CONSOLIDATED: `.

## Hard rules

- Never use the `Agent` tool. Parallelism is `BASE_DIR/bin/run-matrix.sh` and its
  child
  processes (ADR 0004).
- Never run the launcher twice in one invocation.
- Never open a source file in the reviewed repos. Sidecars are the only input
  for findings; if a sidecar is thin, the fix belongs upstream in the review.
- Never invent, re-severity, or drop a finding. Consolidation is arrangement.
