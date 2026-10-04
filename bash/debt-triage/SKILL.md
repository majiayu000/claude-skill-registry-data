---
name: debt-triage
description: EM-PM ceremony to prioritize the debt backlog.
version: 1.0.0
allowed-tools: ["Read","Write","Edit","Bash","Grep","Glob","Agent","Skill","AskUserQuestion","TaskCreate","TaskUpdate","TaskGet","TaskList"]
---

<!-- Schema: state/debt-backlog/*.yaml (YAML per entry); closure via git mv to archive/debt-backlog/<YYYY-MM>/. -->

# Debt Triage — Backlog Review and Prioritization

**Announce at start:** "I'm using the coordinator:debt-triage skill to review the debt backlog."

An **EM-PM conversation**, not a dispatched agent — the EM reads the backlog, applies judgment,
and presents recommendations. Trigger on demand, at >20 open items, or after a refactor that may
have resolved several. Rationale, clustering detail, structural-probe calibration: wiki.

**On a PowerShell host, every CLI below takes its `.exe` launcher through the call operator**
(Shape W), never the `${...}` POSIX-shell form shown. Ladder and shapes:
`${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md`.

Run
`backlog-grind-assemble brief debt-triage` (per `${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md`)
before Step 1 — it returns, over `state/debt-backlog/`, `state/bug-backlog/`,
and `state/improvement-queue/`: open items with severity breakdown, `bug-backlog`
cross-reference (exact `surface`-field match), improvement-queue entries with clustering
evidence, and a batched PM-gate. The improvement leg is emitted (Step 1); the debt-backlog
steps (2, 3, 6, and 6b's debt-backlog governance) stay EM-performed.

## Step 0: Surface prior rejections

Check `tasks/out-of-scope/*.md` (skip silently if absent). For any concept overlapping the
triage, surface: *"This is similar to `tasks/out-of-scope/<concept>.md` — we rejected this
because [reason]. Still feel the same?"* — confirm, reconsider (delete the file), or override.

## Step 1: Read current state

Take the `brief` output as-is. Broader file-path/description-similarity overlap beyond the
`surface`-field match stays an EM judgment pass over the same evidence, applied before
presenting overlaps to the PM for a dedup decision (populate `evidence:` on both entries).

**Improvement-queue triage is emitted, not EM classification.** Pick an appetite (`hunt`,
`standard` or `sweep` — values in `coordinator/queue-profiles/improvement.yaml`). Emit with
`emit-dispatch-workflow --queue state/improvement-queue --profile improvement --appetite <a>
--out state/scratch/debt-triage/{run-id}/improvement.workflow.mjs --repo-root <abs repo root>`, per
`${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md`. There is no commit-readiness gate
to resolve for this leg. Fire with `Workflow({scriptPath})`, never `--fire` — firing authorizes
the in-run fixes and closes and the post-run hand-back (`coordinator/docs/wiki/ceremony-calibration/queue-terminus-doctrine.md`
§ Emitted-workflow triage). The run's triage is the only triage — the EM works Steps 2–4 on the
debt backlog while it runs. An emit refusal is reported, not routed around. The grind commits:
when a `/bug-blitz` runs in the same tree, its Phase 0.7 suite baseline is taken before this
grind fires, or after it finishes — never across it.

## Step 2: Verify relevance (emitted)

> **Do not ask whether to fire** — invoking this skill IS the request for the run this step
> names; it dissolves no gate this skill's own body names.

Debt-backlog rows only, emitted exactly as Step 1: `emit-dispatch-workflow --queue
state/debt-backlog --profile debt --appetite <a> --out
state/scratch/debt-triage/{run-id}/debt.workflow.mjs --repo-root <abs repo root>`, fired with
`Workflow({scriptPath})`. Never hand-dispatch verifiers. The relevance and evidence rules live
in `coordinator/queue-profiles/debt.yaml` (`relevance_first`, `defer_requires_evidence`), not
here. A row whose cited surface moved to another repo comes back as `cross-repo`: route it by
cross-repo memo, then close it here once the memo is delivered. Code that moved is not code
that was fixed. Hand-back types feed Step 5 exactly as the improvement leg's do.

## Step 3: Re-prioritize

Blocking other work → P0. In a D/F-graded system → P1. In a recently A/B-graded system → may
deprioritize to P2. >30 days with no activity → flag for PM attention (skill policy over entry frontmatter dates; the PM-altitude call is the point).

Query historical `nature: tech-debt` completions
(`query-completions --where "nature=tech-debt" --since "90d" --format json`, ranked descending on
`frontmatter.loe.agent_dispatches` as a number — the reader takes no `--sort` —
per `${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md`)
before grouping: high-LoE areas in the last 90d indicate festering complexity — escalate open
items there.

**Never rank on `loe.tshirt`.** Compared as strings, descending t-shirt order is
`XXL, XS, XL, S, M, L` — the smallest tier ranks second. Rank on a numeric field.
Zero-activity areas may reflect avoidance — flag: *"We have carried this debt for N days without
touching it — is that intentional?"* Present a one-paragraph summary before Step 4; zero-row
case: `(no tech-debt completions logged in last 90d — hot-zone analysis unavailable)`.

## Step 4: Group for execution

"System" is the brief's `debt-backlog groups` evidence: the first path cited in `surface`,
else in title/body, cut to two directories. The row's `system` field is free text and often
absent — never group on it.

```markdown
## Triage Results
### Closed (no longer applicable): N items
| ID | Reason |
### Recommended for immediate action: N items
| ID | System | Severity | Description | Effort |
### Can defer: N items
| ID | System | Severity | Reason to defer |
### Needs PM decision (YAGNI/scope): N items
| ID | System | Description | Question |
```

## Step 5: Present to PM

Ask for: (1) approval to close no-longer-applicable items; (2) YAGNI/scope calls; (3)
prioritization of immediate-action items; (4) agreement on deferral reasoning; (5) — item 5 goes to
`coordinator:apm`, not the PM: the improvement leg's hand-back types (`park`, `wont-do`, `yagni`,
`unclear-direction`, `needs-judgment`) are dispositioned by the APM (a code matter by
`coordinator:staff-eng`), which writes `pm_ruling: "<agent> (PM-delegated) ..."` on the row. Step
6b consumes that ruling; the PM sees the receipt. Only a matter marked `pm_only` (important, urgent,
no clear answer, or irreversible) reaches the PM. Engine-originated hand-back types (`budget-exhausted`, `verify-failed`,
and the rest) are reported by count; their rows stay open and are not presented here.

## Step 6: Update backlog

After PM decisions:
1. Close resolved items — stamp `status: closed`, `closed_at:`, `closed_by: <sha>`, then
   `mkdir -p archive/debt-backlog/<YYYY-MM>` and `git mv` the entry in. Never `rmdir
   state/debt-backlog/` even if it empties.
2. Update `severity` per PM direction.
3. Remove YAGNI items the same way as (1), `closed_by` referencing the PM decision.
4. For a **load-bearing rejection** (scope/doctrine conflict, cost-benefit, architectural veto —
   never a bug), write `tasks/out-of-scope/<concept>.md`, one file per concept (append "Prior
   requests" to an existing file rather than duplicating):

   ```markdown
   # Out of scope: <concept>
   **First raised:** YYYY-MM-DD
   **Status:** Rejected (open to reconsideration)
   ## What was proposed
   ## Why we rejected it
   ## Prior requests
   - YYYY-MM-DD: [how this came up]
   ## What would change our minds
   ```
5. Commit scoped, explicit-path: `git commit -m "debt-triage: reviewed N items, closed M, N
   remain open" -- <every touched path>`.

## Step 6b: Consume the improvement leg's hand-back

Runs over both emitted legs' APM-dispositioned hand-back (Step 5 item 5), after the runs; a
debt-leg `cross-repo` hand-back follows Step 2's memo-then-close route.

- `baton`: cluster per `coordinator/docs/wiki/ceremony-calibration/queue-terminus-doctrine.md` § Clustering, then mint
  solo or themed batons to `coordinator/docs/wiki/baton-lifecycle/baton-authoring-bar.md`'s bar, carrying
  triage's sizing evidence. There is no second gate. Stamp `initiative` on a themed baton and its
  member rows. Scaffold with `coordinator-doc-new`, then hand-edit `category` to
  `queue-derived-baton` if the scaffolder left `infra`. Close each source row.
- `route-to-learn-lessons`: run `coordinator-lesson-promote` once per row with `--title-file` and
  `--body-file` (the row's title and body), `--change-kind` (the row's), `--target-wiki unknown`
  (no row carries a target), and `--evidence` naming the archive destination path the closing
  rename lands at (or the row stem), never the pre-rename row path, which goes stale the instant
  the row is archived. Then close the source row with `closed_by` set to the settling commit sha
  (the outbox path goes in the commit message, not `closed_by`).
  - The step promotes only rows that later runs hand back. The `reconcile-343` plan promotes the
    existing central backlog once, via its C1 classification (ratified) and C4 execution, which
    produces the per-row disposition (including which rows already promoted to
    `state/lessons-outbox/`).
    This step's promote gates on that classification's output or its landed C4 — never on the
    `queue_scope: central` tag, which is evidence, not the disposition. Until reconcile-343's
    classification or C4 has landed, a `route-to-learn-lessons` hand-back is left open, untouched
    and unpromoted — no central-tagged row is promoted here, full stop — and Step 5's run summary
    reports it by count as "awaiting reconcile-343," never closed or presented to the PM.
  - A row whose change_kind the outbox enum refuses (exit 2) is left open and reported. It is
    never coerced.
- Park, won't-do and YAGNI keep their current rules and stamps, after Step 5.
- Source-row closure is an edit plus a plain rename to `archive/improvement-queue/<YYYY-MM>/`,
  with the committer staging both paths (A-PLAIN-MV-IS-THE-INTENDED-ROUTE-NOT-A-FALLBACK). The
  row-removal `--declared-revert` follows coordinator-content-repo-47's `/bug-blitz` post-run wording, so the
  two termini read the same.

**Commit shape:** batons, promotes and PM-gated closures are separate commits, each naming the
source ids. The run committed its own fixes and closes. Every hand closure here is followed by
`backlog-grind-assemble grind-row sweep` (`coordinator/docs/wiki/ceremony-calibration/queue-terminus-doctrine.md` § Emitted-workflow triage).

Skip this step entirely if no project-specific entries survived Step 5.

## Autonomous runs

No PM is present; the APM never writes `pm_ruling` in the PM's name, and no autonomous run does.
For each row:

1. Act on the APM's recommendation only where this skill already permits EM-autonomous action
   (closing a verified-resolved row, Step 2's `cross-repo` memo-then-close, re-prioritizing).
2. Otherwise record it as `apm_recommendation` on the row and leave the row open.
3. Continue; a pending recommendation never stops the run.

The report ends with ONE batched PM-confirmation list: every row with an unconfirmed
`apm_recommendation`, as row id, recommendation, one-line reason. The PM's confirmation writes
`pm_ruling` for Step 6b to consume.
