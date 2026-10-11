---
name: real-data-dev-bed
description: "Use when asked for real data in dev, a test bed of real assets, or some of the real repo but not the whole thing (files imported into a dev VCS with real authorship), or that import died part-way."
---

# Real-data dev bed

Materialise a bounded slice of a huge production repository as a working dev environment.

Assumes the layout survey already exists (see the `survey-remote-repo-layout` skill for
capturing a manifest without cloning). This skill covers what happens *after*: turning a
selection into a real, crawlable, committed bed.

## 1. Select whole units, never loose files

Pick complete assets/units, not files under a byte budget. A half-imported unit makes the
bed's derived data disagree with production, which defeats the point.

**Derive the selection from the real grouping logic, not a reimplementation.** If a
catalogue/index already ran over the full manifest, query *it* for unit → member-files.
That gives the production grouper's own output with zero duplicated rules, and lets you
assert the bed is a strict subset afterwards.

Budget with a **per-category cap**, not a flat total. Uncapped smallest-first lets one
heavy subtree eat the budget. Tune the cap to maximise unit count at the target size —
measured once: a 15 GB cap gave 956 units, a 10 GB cap gave 1,188 for the same 40 GB.

Commit the selection as a plain path list so the bed is reproducible.

## 2. Export resumably

- Pin the revision so bed and manifest describe the same tree.
- One export per file when the selection takes only part of some directories; whole-dir
  export pulls neighbours the budget excluded.
- **Resume by size, not existence.** A killed transfer leaves a short file; treating it as
  done imports a truncated binary and blames the exporter later.
- **Sweep the exporter's part-files before staging.** `svn export` writes `svn-<number>`
  beside its target and renames on success. A stray survives the resume check (it is not
  in the selection, so nothing accounts for it) and a filesystem-walking stage will commit
  it into the bed.

## 3. Import into the target VCS with real authorship

Commit **one commit per author**, grouped from the manifest. "Who touched this last",
collision detection, and people panels all read as a single name against a bed committed
by one identity.

Use a targets/response file — dozens of authors over thousands of files exceeds command
line limits.

### Traps that cost real time

- **`--repository <path>` says which repo; it does not define what a relative path means.**
  Relative paths resolve against the **working directory**. A targets file of
  repo-relative paths read from elsewhere matches nothing: stage exits 0 having staged
  nothing, and the failure surfaces one command later as commit's "Nothing staged" — a
  sentence about the wrong command. `Push-Location` into the workspace, in `try/finally`.
- **Never pipe a native command before reading its status.** `cmd | head; echo $?` reports
  `head`. Capture to a variable, then read the exit code immediately. This produced a
  false "exits 0" claim that contradicted observed behaviour.
- **Never swallow the tool's output.** Piping stage/commit to null yields "commit failed"
  with no reason — a script that must be edited before it can be debugged.

## 4. Make re-running safe end to end

Long imports get interrupted (a broker/server restart killed one 4 commits into 51, after
the full transfer). A script that answers that by refusing to start throws away the
transfer too.

- Detect an existing repository and carry on instead of failing to create one.
- Treat the tool's specific "nothing staged" text as **already committed**, not failure —
  otherwise a resumed run looks like N broken commits. Match the exact message only; every
  other failure text must still report. Verify by exercising several failure strings.
- Report `committed` and `already present` separately.
- Run the whole thing long-lived/detached; it will outlive the session.

## 5. Verify, and state what the bed cannot reproduce

- Crawl/index it and check unit and file counts match the selection exactly.
- Assert the bed's keys are a **strict subset** of the full survey's — read query output
  **line-wise**; splitting on whitespace silently breaks paths containing spaces and
  inflates counts.
- Workspace status with a forced rescan must be clean; unstaged leftovers show up here.

**Timestamps cannot be reproduced.** Most VCS stamp the commit with no backdating, so N
commits land in minutes: measured, 1,188 units sharing 49 distinct timestamps across
4m58s. Consequences to document *before* they look like bugs — "last touched by" reflects
import order rather than production history, and authors whose files are always
accompanied by a later-committed sibling never surface at all (48 names from 51 commits).

Faking dates means writing derived fields directly, which forfeits the property that makes
the bed trustworthy: a catalogue derived by crawling cannot disagree with the repository.
