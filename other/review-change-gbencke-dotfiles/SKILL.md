---
name: review-change
description: >
  Adversarial review of a change: a PR, a branch diff, or a patch file. Runs
  inline in a single process — blast radius, then per-lens propose → kill →
  judge — and writes a PR-comment-ready report plus findings.json under
  .gbencke/adversarial-review/reports/. Spawns no subagents.
  Trigger: /review-change <pr-url|pr-number|branch|patch-file> [base],
  "adversarial review of this PR/branch/patch".
argument-hint: "<pr-url|pr-number|branch|patch-file> [base]"
---

# review-change — adversarial review of a PR / branch / patch

Run the adversarial loop yourself, in this process. You are the **reviewer, the
challenger, and the judge, in that order** — three roles, one process, strict
phase separation.

**No subagents.** Never use the `Agent` tool in this skill. Parallelism is the
caller's job: batch runners launch one process per (target × lens) — see
ADR 0004.

**Shared assets base dir** (`BASE_DIR` below) —
`~/.claude/skills/adversarial-review/`: `CONTEXT.md` (glossary), `agents/`
(reviewer, challenger, judge role packs), `lenses/` (15 lenses), `bin/run-matrix.sh`
(the matrix launcher).

## Phase 0 — Resolve the change

Parse the argument (first token = target, second = optional base, default
`main`):

- **PR URL or number** → `gh pr diff <n>` and `gh pr view <n> --json title,body`
  (the title/body is the *change intent* — keep it for the judge). If `gh`
  fails, tell the user and stop.
- **Branch name** → `git diff <base>...<branch>`; intent = the branch's commit
  messages (`git log <base>..<branch> --oneline`).
- **Patch file path** → read the file; intent = none (solution-fit degrades to
  correctness-only; note this in the report).

Also resolve the repo root (absolute) as `TARGET_DIR`. Save the diff to a temp
file. If the diff is empty, say so and stop.

### Phase 0b — JIRA requirements (when credentials exist)

The stated requirement is what SOLUTION_FIT is judged against, so pull it when
you can. Skip this step entirely if `$JIRA_EMAIL` or `$JIRA_TOKEN` is unset.

1. Collect ticket keys (`[A-Z][A-Z0-9]+-\d+`) from the branch name, the commit
   subjects from Phase 0, and the PR title/body. De-duplicate.
2. Fetch each key. Use API v2, not v3 — v2 returns `description` as plain text
   while v3 returns ADF JSON:

   ```bash
   curl -s -u "$JIRA_EMAIL:$JIRA_TOKEN" \
     "https://raintreeinc.atlassian.net/rest/api/2/issue/<KEY>?fields=summary,description,status,issuetype,parent"
   ```

3. Append each ticket to `{{INTENT}}` as `KEY [status] summary` followed by the
   description, ahead of the commit messages. The ticket is the stronger
   statement of intent; commit messages describe what was done, not what was
   asked for.

Degrade quietly and record which case applied, because it changes how the judge
must read SOLUTION_FIT:

- credentials unset → note "JIRA not consulted (no credentials)" in the report
- no ticket key found → note "no ticket key in branch or commits"
- fetch fails or 404 → note the key and the HTTP status, keep the commit
  messages as intent, and carry on. Never stop the review over JIRA.

Requirements the ticket states but the diff does not implement are
SOLUTION_FIT findings, not correctness findings.

## Phase 1 — Blast radius (mechanical first)

1. Extract changed symbols from the diff: function/class/type names, exported
   identifiers, API routes, schema/migration definitions, feature flags.
2. Build the reverse import/caller graph over `TARGET_DIR`: for each changed
   exported symbol, find files that import or reference it. Use ast-grep
   (`sg`) when available, `grep -rn` as fallback. Skip test files in the graph
   but record which tests reference the changed symbols (feeds test-surface).
3. Produce: `{symbol → direct dependents[]}`, count of affected packages/dirs.

## Phase 2 — Lens selection (never ask)

Read every `BASE_DIR/lenses/*/lens.md` + the repo overlay
(`.gbencke/adversarial-review/lenses/`, merge same-named). For a change review ALL
signal-matched lenses apply, and `test-surface` + `blast-radius` ALWAYS
apply. Language lenses (glob signals like `*.go`, `*.ts`) match only if the
diff touches matching files.

- **Run every matched lens. Never prompt.** There is no lens picker; the
  matched set is the selection. State the names in chat and continue. A prompt
  would hang non-interactive callers (`claude -p`).
- `--lenses a,b,c` in the argument overrides the matched set with exactly those
  lenses. That is the only way to narrow it.
- Compute `LENS_SLUG`: the lens name when exactly one lens is selected,
  otherwise `multi`. It goes in the report basename (Phase 5) so concurrent
  per-lens reviews of the same target do not overwrite each other.

## Phase 3 — The loop, one lens at a time

Read `BASE_DIR/agents/reviewer.md`, `BASE_DIR/agents/challenger.md`, and
`BASE_DIR/agents/judge.md`. These are **role packs**: the stance, contract, and output
schema you adopt for each phase. Process lenses **sequentially**; for each:

1. **Propose** — adopt `BASE_DIR/agents/reviewer.md` with the lens's merged `rules.md`.
   Scope = the FULL diff, plus the Phase-1 graph for `blast-radius`. Read any
   file under `TARGET_DIR` for context — full-repo access is what keeps false
   positives down. Emit findings in the role pack's JSON shape.
2. **Kill** — switch to `BASE_DIR/agents/challenger.md` for that lens's findings: try to
   disprove each against the actual code (callers, middleware, framework
   defaults, config). Emit `VALID` / `INVALID` / `AMBIGUOUS` with the kill
   attempts you actually made. No new findings while wearing this hat.
3. Keep ONLY the challenger JSON before moving to the next lens. Your context is
   the budget now that no subagent absorbs it; the diff stays, the context files
   you grepped do not.

## Phase 4 — Judge (dual verdict)

Adopt `BASE_DIR/agents/judge.md` and rule on the Phase-3 challenger output only — never
re-read code to invent findings here:

- `{{MODE}}`: `change`
- `{{INTENT}}`: the change intent from Phase 0 (or "unknown")
- `{{FINDINGS}}`: all challenger outputs
- `{{CONTEXT}}`: target, base, diff stat, Phase-1 blast-radius graph summary
- Write into `<repo>/.gbencke/adversarial-review/reports/`:
  - `<yyyymmdd-hhmmss>-<target-slug>-<LENS_SLUG>.md` — PR-comment-ready report:
    dual verdict first (IMPLEMENTATION_CORRECTNESS × SOLUTION_FIT → overall
    SHIP / FIX-THEN-SHIP / DO-NOT-SHIP), then findings by severity, then the
    blast-radius section, then the NOT-REVIEWED list.
  - `<same-basename>.findings.json` — the sidecar.

## Phase 5 — Summary

Chat reply ONLY: dual verdict line, severity counts, top-5 findings (one line
each), blast-radius headline (N direct dependents, risk tier), report path.

Last line, on its own, absolute, prefixed exactly `REPORT: ` — batch callers
parse that instead of guessing from directory mtimes.

## Hard rules

- Never use the `Agent` tool. One process, three roles, phases in order.
- Keep the phases honest: propose, then kill, then judge. The judge role never
  rescues a finding the challenger killed, and the kill phase is never skipped
  because a finding "looks obvious" (ADR 0001, ADR 0004).
- Never modify the repo except the reports dir.
- Concurrency: other reviews of this repo may run in parallel. `mkdir -p` the
  reports dir, write only your two files, never delete/overwrite/prune others,
  keep scratch files in the system temp dir, and never run a mutating `git`
  command (`add`, `stash`, `checkout`, `clean`).
- Never execute repo code, tests, builds, or network/cloud calls
  (`gh`/`git diff`/JIRA fetch for input gathering are the only exceptions).
- Every finding must cite file:line and a concrete failure condition.
