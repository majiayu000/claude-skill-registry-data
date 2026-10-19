---
name: este
description: Use when the user runs /este. Computes the adherence pulse — a marker-based, per-item scorecard (with confidence tiers) of how faithfully the skadi config's rules and skills are followed across all config roots — appends the run to history, renders a Henneth dashboard, and prints its URL. Read-only over transcripts; never writes to a tracker or repo. Runs on demand; wrap in /loop or cron for a standing cadence.
purpose: Computes an adherence pulse scoring how faithfully the skadi config's rules and skills are kept.
user_invocable: true
stage: watch
composes: henneth:dispatch
---

# Estë — The Adherence Pulse

Estë, the Vala of healing and rest, measures the health of the work: how
faithfully the config's rules and skills are kept. One run scans every config
root's transcripts, scores each rubric item, and lays a dashboard in the Henneth
window.

## Run

    python3 ~/.claude/hooks/pulse-scan.py

This walks Claude `projects/**/*.jsonl` and Codex `sessions/**/*.jsonl` beneath
the default, personal, and work config roots (read-only), appends a line to
`~/.skadi/pulse/history.jsonl`,
writes the board channel `~/.skadi/board/pulse.json`, and renders
`~/.skadi/henneth/adherence-pulse.html`. It prints the headline overall.

Then ensure the Henneth window is up (boot it with `/henneth` if not) and surface
the dashboard URL inline — the page follows the folder, so the pulse appears on its
own once rendered.

## Notes

- **Read-only.** The pulse reads transcripts; it never writes to a tracker or repo.
- **Markers only.** The first cut scores machine-checkable signals — per-skill
  completion and grammar rate. Two rule items (commit-footer, PR assignee) are
  defined but marked `pending` until their git/forge probes are built.
- **Subagent-backed rows under-report in Codex.** Claude exposes child
  transcripts beside the parent session; Codex rollouts do not currently expose
  the same parent-to-child path to this scanner. Separately, a skill that posts
  its verdict only in a tracker — `/council`'s `[COUNSEL]`, `/celebrimbor`'s
  `[GWAITH]` — leaves no marker in the main transcript, so those rows also read
  low. These are known limitations, not failures of the skills.
- **Only a segment that authored something owes a review.** `_owes_review`
  bills a segment when it carries an Edit/Write or a `sed -i`, and excludes
  one whose whole mutation was `git commit`, `mkdir`, `install.sh`, or a
  build log piped through `tee` — such a segment changed no file the review
  could read, and its diff, where one exists, belongs to work weighed in an
  earlier segment. Before this, 163 such segments sat in the denominator —
  30% of it, complying 1% of the time — so the row was largely scoring the
  config for not reviewing commits and directories. **Read the resulting jump
  (11% → 15%) as a mended denominator, not as improved conduct:** the
  correction removes a nearly all-failing population, so it flatters the
  number without any change in behaviour. It errs the other way too — a
  segment that authored only through a shell redirect, or removed a tracked
  file with `rm` or `git mv`, is excluded though it arguably owed a review.
  The same predicate governs the row's `SKIPPED` count and `review.verdict`'s
  `unreviewed` count, so all three describe one population.
- **A rendered verdict closes the task segment.** Waiting only for a
  read-only lull merged two tasks run back to back, and that merge did not
  merely under-bill — it inverted the reading: the first task's marker no
  longer followed the segment's last edit, so a properly reviewed task
  scored a miss, while the unreviewed task after it hid inside the same
  segment and was never billed at all. 58 of the 390 segments owing a review
  sat in that state — as many as the fold credited in total, its complied
  count being 58 as well.
  Closing on the verdict credits the first and exposes the second, and it is
  the *stricter* rule — a marker rendered mid-task now closes there, so the
  edits after it open a fresh segment owing a verdict of its own, where
  before one marker could cover any length of later work. It is not
  circular: over half the segments carry no marker at all and are closed by
  the lull rule as before, and the reviewer-verdict requirement still
  refuses a marker typed unearned. **This moved the rate 15% → 24% with no
  change in conduct** — the third mending of this row's arithmetic in one
  day, and like the others a truer denominator rather than improvement.
- **Compliance Review bills per task segment, not per prompt turn.**
  `rule.compliance-review` folds consecutive mutating runs (the user steering
  between edits) plus their read-only wind-down into one segment — CLAUDE.md
  owes the review once per task, "before the done report", not after every
  turn that touched a file. Known trade-off: two tasks back-to-back with no
  read-only run between them merge and bill once. A `since` date on the
  rubric entry drops runs from before the rule existed. A segment closing with
  an explicit `Compliance Review: SKIPPED (reason: …)` is excluded from both
  sides — a reasoned waiver is no silent omission — and its count stands beneath
  the row, so the exclusion is named rather than hidden.
- **Compliance Review requires a reviewer's filed verdict, not just the closing
  line.** A segment only complies when a review agent filed its own
  `Compliance Review: PASS|FAIL` within that segment, at or before the turn
  bearing the closing marker (which itself must follow the segment's last
  mutating turn). The literal marker alone does not suffice — a model could
  type it unearned. Neither does a bare `Agent` tool call, which this check
  once accepted: an unrelated Explore search satisfied it as readily as a
  review did, and one credited segment in five sat in a session that had filed
  no verdict at all. The window opens at the segment's start rather than its
  last edit, because CLAUDE.md's order is review, then mend the findings (more
  mutating turns), then verify, then the verdict — so the review routinely
  precedes the segment's last edit.
- **`review.verdict` traces the FINAL result, not the reviewer's first draft.**
  Where `rule.compliance-review` asks whether the review was performed at all,
  this row asks how sound the work that shipped actually was: the rate is
  (PASS, or FAIL judged mended) over every Compliance Review agent dispatched.
  The verdict is still read from the reviewer's own transcript
  (`<session>/subagents/agent-*.jsonl`), never the thread's closing line — the
  thread never writes FAIL, since CLAUDE.md's order is review, then mend the
  findings, then report, so scoring that line would ask the summarizer to
  grade itself and could only ever read 100%. But a raw FAIL is not the same
  question as a *sound outcome*: a finding that gets fixed before the report
  is the review doing its job, not a miss against it. So a FAIL folds back in
  as compliant once a mend-judge — reading the reviewer's own findings beside
  what the segment did afterward, cached in `mend-verdicts.json` — calls it
  `mended`; one it calls `unmended`, or one it could not reach at all, stays a
  miss. `review.recovered` isolates that FAIL population on its own and names
  the recovery rate this row folds in but does not show by itself. A mutating
  segment that closed with no review behind it is neither credited nor
  penalized: a review never run is no verdict on the work. That excluded
  population is reported beneath the row rather than hidden, split into
  silent and explicitly `SKIPPED` — counted per segment, where the rate itself
  counts reviews, since one task may draw several audits or none. Three
  approximations hold it in the heuristic tier: the segment fold behind that
  excluded count, `byModel` attributing a review to the model that authored
  the *session* under review rather than the run, and the mend-judge's own
  call on whether a FAIL's findings were actually addressed.
- **`review.recovered` is the FAIL-only twin: of the reviews that misfired, how
  many were caught and fixed?** review.verdict's final-result framing means a
  low number there does not, by itself, distinguish "reviews are working —
  findings get fixed" from "findings are shipping unfixed." This row answers
  that directly: applied is every FAIL located inside a task segment (one
  outside any segment — a review dispatched during a purely read-only run,
  before any edit exists to mend — has nothing to show a mend in, and is
  absent rather than guessed at); complied is the ones the same mend-judge
  calls `mended`. A FAIL the judge could not reach is excluded from both sides
  and named beneath the row as `unjudged`, the same discipline as
  `plan.accepted`'s abandoned count. Heuristic tier for the same reason
  `plan.accepted` and `plan.bug-reported` are: the call is a model's judgment,
  cached per review so a closed transcript is never re-judged.
- **`plan.bug-reported` names each completion by its request, and its rate leans
  high.** The row asks whether a finished piece of work drew a bug report later in
  the same session, so a *high* rate is the good reading. Two things shape it.
  First, a task segment opens at its *mutating* run, and under the Free-Form Gate
  that is the run the user's assent begins — so a completion's own opening prompt
  is "proceed", which no judge can pin a later bug report to. The candidate list
  therefore describes each completion by the request standing before the gauge,
  which is what the gate proposed. Second, a report the judge calls a real bug but
  cannot pin to any candidate is dropped rather than guessed at, and the
  completion it silently described stays counted clean — so the rate reads high by
  up to the unattributed count, which stands beneath the row rather than hiding
  behind the ⓘ. Both approximations hold the row in the heuristic tier.
- **`verify.test` and `verify.lint` ask how often the code, as produced,
  cleared the check on its first submission.** One task segment yields one
  verdict, taken from the *first* readable run of the suite or the linter in
  that segment. Only the first: the re-runs that follow a failure describe
  the repair, not the work, and folding them in would let one stubborn bug
  outvote a dozen clean segments. The verdict is the `tool_result`'s own
  error flag and nothing else — no output text is parsed, so no per-tool
  string pattern can silently rot.
- **The pipeline caveat is what governs these two rows' coverage.** A bare
  pipeline returns only its last stage's status: `flutter analyze 2>&1 | tail
  -6` hands back `tail`'s, and `tail` succeeds whatever the analyzer found.
  Measured raw, 99% of piped lint runs read clean against 77% of unpiped ones
  — a 22-point gap that is the pipe manufacturing passes, not the code being
  cleaner. Such a run is therefore *excluded* and counted beneath the row as
  `unmeasured`, never credited as a pass. `set -o pipefail` restores the
  check's own status, so a piped run carrying it is readable again — which is
  why CLAUDE.md now asks for that prefix, and why these rows' coverage grows
  as the habit takes hold. The `unmeasured` count doubles as a read on how
  widely that rule is being kept.
- **Both `verify.*` rows are `structural`, not `deterministic`.** The read
  itself is mechanical, but *which* runs are visible is not neutral: output
  is trimmed most often on the largest suites, so the measured population
  skews toward smaller, faster checks until pipefail closes the gap. An
  existence probe (`command -v golangci-lint`) is not a run and never counts;
  this repo's own `hooks/lint.sh` and `*.test.sh` gates are classified
  alongside the standard tools. `verify.lint` carries the thinnest
  denominator on the board — read its short-run movement with care.
- **A `PostToolUse` hook's own runs never entered either row, and still
  don't.** Both scorers walk `bash_commands` off assistant turns only
  (`pulse-scan.py:592`), and a hook fires outside that stream entirely —
  `read_turns` drops every record type but `user`/`assistant`
  (`pulse-scan.py:232`). So when `hooks/flutter-analyze.sh` (deleted
  2026-08-14) still ran `flutter analyze` and the whole `flutter test` suite
  silently after every `.dart` write, neither row ever saw it; and today's
  `hooks/eslint-check.sh`, which still lints every web edit automatically, is
  equally invisible. Removing the hook's analysis and test calls therefore
  changed nothing either row measured — what it changed is that the model
  itself now runs both, as CLAUDE.md's "Analysis and tests have named
  moments" names. Read these two rows' denominators growing since
  2026-08-14 as coverage of a discipline made explicit, not as a shift in
  conduct; the `since` gate on both entries stays at 2026-08-12 because the
  metric's *definition* never changed, only what it now has occasion to see.
  `verify.lint`'s `match` also gained `tsc` (anchored to an invocation, not a
  bare word, so a stray `grep tsc` mention can't fabricate a pass) and an
  `exclude` for `*.test.sh` — without it, running this repo's own
  `hooks/eslint-check.test.sh` registered as a lint pass off the bare word
  `eslint` in its filename, a false positive the same commit introduced by
  adding that file. `verify.test` needs no such exclude: a `*.test.sh` run is
  a genuine test run there.
- **First-shot rate measures the model, not a rule.** `model.first-shot` asks a
  different question from every other row: not "did the model keep the config's
  rule" but "how good is the model" — what fraction of task segments landed
  without the user coming back to correct it. Within a segment (the same task
  fold `rule.compliance-review` uses), a *rework* run is a mutating run after
  the first whose opening prompt reads as a correction (`rework` regex — "no,
  the arrow points left"; both English and Chinese cues). An *additive*
  follow-up ("also commit and push") is progress, not a miss, and does not
  count. A segment is first-shot when its rework count stays within
  `threshold` (default 0 — strict). Read the `byModel` split, not the overall
  rate: the point is comparing Opus / Sonnet / Fable. The tone regex is a
  keyword heuristic — a mixed-language or oddly-phrased correction can slip it,
  so the row reads slightly optimistic; it sits in the heuristic tier for that
  reason.
- **Success/failure is one click away.** Every rubric item carries a plain-language
  `criterion` — what counts as a pass, what counts as a miss (✓ … · ✗ …). On the
  dashboard each row bears an ⓘ button; clicking it unfolds the criterion beneath
  the row, clicking again folds it. The text is the single source: it lives on the
  rubric entry, flows into the page's data, and reads the same as this skill's notes.
- **Honest tiers.** Each item carries a confidence tier, and the headline shows a
  figure per tier; a single cross-tier average is shown too, but always labelled as
  such and never standing alone.
- **Standing cadence.** The skill arms nothing. For a recurring pulse, wrap it:
  `/loop 6h /este`, or a cron.
- **Tests ride beside the hook** — `pulse-scan.test.sh` runs offline via injected
  fixture roots (`PULSE_ROOTS`).
