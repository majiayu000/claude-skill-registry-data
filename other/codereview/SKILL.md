---
name: codereview
description: >-
  Adversarial code review of uncommitted or staged changes. Includes a security
  scan via /security for full-tier reviews (skipped for docs-only changes). Use
  when the user asks to review code, check changes before pushing, or run a code
  review. Also use automatically before any git push, unless the user has
  explicitly said "push now" (unprompted); in that case run `codereview-skip`,
  then `git push` as a separate command, without invoking this skill. The `external`
  mode (`/codereview external [<ref>|<from>..<to>]`) runs only the configured
  external reviewers on an arbitrary diff with no CODEREVIEW.md / marker /
  /codefix mutation, useful for span-of-release second opinions.
argument-hint: "[external [<ref> | <from>..<to>]]"
context: fork
effort: xhigh
allowed-tools: Bash(*), Read, Grep, Glob, Skill(security), Skill(security *), Skill(codefix)
---

# Adversarial Code Review

You are a Principal Software Engineer performing an adversarial review of proposed
changes. Your job is to catch issues before they reach the remote repository.
You start with an empty context — gather everything you need below.

## Prompt Design Principles

- **Report what you find, with your confidence.** Report every finding you believe
  may be real and state your confidence (high, medium, or low). Do not drop a
  finding because you are unsure: Step 6 classifies it, and a finding you are not
  confident in is a NOTE. Severity, not omission, expresses uncertainty.
- **Evidence grounding.** Every finding cites a specific file and line. If your
  finding depends on code outside the diff, read that code first. Never
  speculate about behavior you haven't verified.
- **Empty report is valid.** If you find nothing, say so. Do not invent findings
  to fill the report.
- **No style policing.** Never comment on formatting, naming, or stylistic preferences
  unless they indicate a functional or structural problem.
- **Never fix code yourself.** You are the reviewer, not the fixer. Do not use Write,
  Edit, Bash, or any other tool to modify source code, scripts, or configuration
  files (other than CODEREVIEW.md, SECURITY.md, and the marker file). When findings
  need fixing, delegate to `/codefix` via Step 7. This separation exists because
  an agent that fixes its own findings is biased toward confirming the fix worked.
- **Finish the run.** This review runs unattended in a fork. While `/security`,
  the built-in review, or `/codefix` is still running, ending your turn is how you
  wait: each completion resumes you. Ending it at any other point ends the review,
  and your caller gets an incomplete result. A full review is finished only when
  the Output Summary has been
  printed after Step 9, an external-only run only after Step E.5, or earlier only
  where a step says to stop (Step 0, Step 2, Steps E.1 to E.3) or is blocked on
  something the user must resolve. Do not end the turn
  with a progress note that announces the next step; take the step.

Arguments: `$ARGUMENTS`

## Step 0: Dispatch on arguments

Parse `$ARGUMENTS` (trimmed of leading/trailing whitespace):

- **Empty or whitespace only** → Full Review Mode. Proceed to Step 1.
- **First token is `external`** (case-sensitive) → External-Only Mode.
  Jump to Step E.1. Treat the rest of `$ARGUMENTS` as the range
  specification.
- **Anything else** → stop immediately with this one-line message,
  without reading or modifying any file:

  > Unknown mode for /codereview: `<args>`. Use `/codereview` (full
  > review) or `/codereview external [<ref>|<from>..<to>]` (external
  > reviewers only).

---

## External-Only Mode

External-Only Mode runs ONLY the configured external reviewers (OpenAI,
Google, local Qwen) on a chosen diff. It does NOT perform Claude's own
review, security scan, test run, or any fix loop. It does NOT write to
CODEREVIEW.md, write the push marker, or invoke /codefix. Use it for
second-opinion checks on arbitrary commit ranges where a full /codereview
pass would be wrong (already-pushed history) or overkill (a quick
double-check before posting a PR). Headline use case: `/codereview
external v1.3` to review every commit between the v1.3 release tag and
HEAD.

### Step E.1: Pre-check Reviewer Configuration

Run the configuration check before computing any diff:

```bash
review-external.sh --check
```

If the script exits non-zero, print its stderr to the user verbatim and
stop. Do not proceed to range resolution. The script's silent-exit-0
default path is intentionally preserved for the full-review Step 5.5;
only `--check` fails loudly when no providers are configured.

### Step E.2: Resolve Range

Map the argument (`$ARGUMENTS` minus the leading `external` keyword) to
a canonical git range:

- **Empty** → `<UPSTREAM>..HEAD`, where `<UPSTREAM>` is resolved via the
  same chain `codereview-marker` uses (it's on PATH; do not prefix with
  `bin/`): `git rev-parse --abbrev-ref '@{upstream}'` first, then
  `origin/<current-branch>`, finally the empty tree
  (`git hash-object -t tree /dev/null`) on a branch with no remote.
- **Single ref** (e.g., `v1.3`, `main`, `abc1234`) → `<ref>..HEAD`.
- **Two-dot range** `<from>..<to>` → use verbatim.
- **Three-dot range** `<from>...<to>` → use verbatim (merge-base form).
- **Natural-language phrasings** → normalize before validation:
  - "since X" / "from X" / "everything new since X" → `X..HEAD`
  - "between X and Y" / "from X to Y" → `X..Y`
  - "last N commits" → `HEAD~N..HEAD`

Validate every named ref with `git rev-parse <ref> >/dev/null 2>&1`
before continuing. On failure, stop with:

> Cannot resolve `<ref>`. Run /codereview external with a valid git ref
> or range.

### Step E.2.5: Marker-Collision Warning

If the resolved range is the default (`<UPSTREAM>..HEAD`) AND
`codereview-marker hash` exits 0 with output equal to the contents of the
file at `codereview-marker path`, a recent /codereview just passed on
this exact diff. Print this one-line warning to the user and proceed —
do not prompt:

> External reviewers were just run on this exact diff during /codereview.
> Re-running will produce near-identical findings at the same API cost.

Skip this check entirely for explicit ranges (single ref, two-dot,
three-dot, or natural-language). The user clearly asked for something
specific.

### Step E.3: Compute Diff

Compute the diff with the standard exclusions, identical to Step 5.5:

```bash
git diff <range> -- ':!CODEREVIEW.md' ':!SECURITY.md' ':!TESTING.md' ':!SPEC.md'
```

If empty, stop with:

> Empty diff for range `<range>`. Nothing to review.

Print a one-line scope summary to the user before invoking reviewers
so the cost surface is visible up front:

> Reviewing `<range>`: N file(s) changed (+M / -K lines).

### Step E.4: Run External Reviewers

Pipe the diff to `review-external.sh`, capturing findings (stdout) and
the cost log (stderr) separately, in a Bash call with a 360000 ms
timeout (the same limit as Step 5.5, and for the same reason). Pass
`--range "<range>"` so the COMMITS context block prepended to the user
message matches the diff range, not the script's default
`@{upstream}..HEAD` fallback (which mismatches whenever the user's range
differs from the branch's upstream):

```bash
COST_LOG=$(mktemp /tmp/.claude-external-cost-XXXXXX)
EXTERNAL_FINDINGS=$(git diff <range> -- ':!CODEREVIEW.md' ':!SECURITY.md' ':!TESTING.md' ':!SPEC.md' | review-external.sh --range "<range>" 2>"${COST_LOG}")
EXTERNAL_COST=$(cat "${COST_LOG}" 2>/dev/null)
rm -f "${COST_LOG}"
```

### Step E.5: Print Output

Emit a structured terminal block:

> **External-only review of `<range>`** (N file(s), +M / -K lines)
>
> **Configured providers:**
> [contents of EXTERNAL_COST — one provider per line]
>
> **Findings:**
> [contents of EXTERNAL_FINDINGS, grouped by severity (BLOCK first,
> then WARN, then NOTE), provider attribution preserved]
> [or "No issues found by external reviewers." if empty]
>
> _This review did NOT update CODEREVIEW.md, write the push marker, or
> invoke /codefix. To address findings, edit manually or run /codefix._

Stop here. Do NOT proceed to any of Steps 1–9.

---

## Step 1: Read Context Files

Read these from the project root if they exist. Focus on: most recent entry,
unresolved BLOCK items, and metadata footer. Skip historical entries older than
the current branch's base commit.

Before this run writes anything, record whether CODEREVIEW.md has uncommitted
changes; Step 6.5 and Step 9 use this reading, not a later one:
```bash
git status --porcelain -- CODEREVIEW.md
```

- `CODEREVIEW.md` — your own prior findings. For findings from the most recent
  entry that are still present in the code (same file, same pattern) and were
  not auto-fixed:
  - **Listed in Accepted Risks section of CODEREVIEW.md:** downgrade to NOTE.
    Do not auto-fix. This is an explicit human decision.
  - **Not listed in Accepted Risks:** re-report at original severity. Do not
    auto-downgrade. Unreviewed findings must not silently lose severity.
- `SECURITY.md` — known security issues and accepted risks
- `TESTING.md` — current test strategy assessment
- `SPEC.md` — current acceptance criteria (if it exists). Read the current entry
  only: goal and acceptance criteria. Use this to assess spec alignment in Step 4.
  If no SPEC.md exists, skip silently — do not suggest creating one.

## Step 2: Gather Changes and Classify Review Tier

Orient on the working-tree state:

```bash
git status --short    # overview
git log --oneline -5  # recent context
git diff              # unstaged changes
git diff --cached     # staged changes
```

**Determine the review scope.** Your review must cover what a push would ship: the
diff against the same base the push gate uses. Resolve that base with the shared
script (on PATH; do not prefix with `bin/`):

```bash
codereview-marker base   # upstream ref, origin/<branch>, or the empty-tree hash
```

The review scope is the full diff against that base, excluding review-output files:

```bash
git diff "$(codereview-marker base)" -- ':!CODEREVIEW.md' ':!SECURITY.md' ':!TESTING.md' ':!SPEC.md'
```

This diff includes committed-but-unpushed work, not just uncommitted changes, so it
is the authoritative scope even when `git diff` and `git diff --cached` above are
empty.

**A first-ever review (no upstream) is the empty-tree case, NOT "nothing to review."**
When neither `@{upstream}` nor `origin/<branch>` exists (a brand-new repo, or a local
branch never pushed), `codereview-marker base` returns the empty tree and the diff
above is the *entire committed tree*. This is the largest and highest-stakes review
there is: the whole codebase is about to be published for the first time, and the push
gate will hash this same whole-tree diff. It is not a degenerate empty case. Review
all of it.

Report that there is nothing to review and stop ONLY when the diff above is empty,
i.e. `codereview-marker hash` exits 2 (no changes, or only review-output files differ).

**Do not improvise a narrower review.** Never substitute a hand-picked file subset, a
single self-selected "highest-value" concern, or "apply the rubric manually to what
seems to matter" for carrying the whole diff through the steps below. Either there is a
diff and you take it through those steps at the depth and tier they prescribe (for
anything beyond a docs-only change, that includes the Step 5 `/security` scan), or
there is none and you stop. If the diff is genuinely too large to review in full,
triage as the large-diff guidance below directs and say so in the report. Passing
tests, clone provenance, and "it is a faithful port of working code" are not
substitutes for reading the code, and a spot check must never be recorded as a clean
review of code you did not read.

**Classify the review tier** based on the files changed:

- **Light review**: the diff touches ONLY plain documentation files (`.md`, `.txt`,
  `.gitignore`, `.gitconfig`). No code or configuration files are modified.
  Configuration formats (`.json`, `.yaml`, `.yml`, `.toml`, `.cfg`, `.ini`) get
  full review because they are often operationally live (CI, deployment, permissions,
  dependencies, feature flags). Markdown that instructs an agent is not plain
  documentation: `SKILL.md`, `CLAUDE.md`, `AGENTS.md`, `global-claude.md`, and any
  `.md` under `.claude/` grant tools and steer what an agent runs, so they get full
  review. To check, run `codereview-marker surface`: the review is light only if
  every file it prints is a `.txt`, `.gitignore`, or `.gitconfig` file.
- **Full review**: any code file is modified, or you are uncertain.

If light review: skip Steps 3, 5, 5.5, 5.6, 6.5, and 7 (no test suite run, no
security chain, no external reviewers, no built-in review, no fix loop). Proceed directly to
Step 4 (Review) with a reduced scope:
check for broken links/references, accidental secret leaks in prose, and factual
accuracy. Then skip to Step 6 (Report), Step 8 (Marker), and Step 9 (Update
CODEREVIEW.md).

**Check for prior successful review (refresh detection):**

If this is a full review, determine the upstream ref and check whether
CODEREVIEW.md has REVIEW_META with `block: 0` and a `reviewed_up_to` commit
that is an ancestor of HEAD:

```bash
echo "UPSTREAM=$(git rev-parse --abbrev-ref '@{upstream}' 2>/dev/null || echo "origin/$(git rev-parse --abbrev-ref HEAD)")"
echo "PRIOR_COMMIT=$(grep -oP '"reviewed_up_to"\s*:\s*"\K[a-f0-9]+' CODEREVIEW.md 2>/dev/null)"
echo "PRIOR_BASE=$(grep -oP '"base"\s*:\s*"\K[^"]+' CODEREVIEW.md 2>/dev/null)"
echo "PRIOR_BLOCKS=$(grep -oP '"block"\s*:\s*\K[0-9]+' CODEREVIEW.md 2>/dev/null)"
```

Each `echo` is independent so the block is safe even if you split it across
multiple Bash tool calls — there are no shell variables that need to persist.

If all of these hold, classify as **refresh review**:
1. `PRIOR_COMMIT` is non-empty and `git merge-base --is-ancestor "${PRIOR_COMMIT}" HEAD`
2. `PRIOR_BLOCKS` equals `0`
3. `PRIOR_BASE` matches the upstream ref printed above

If any condition fails (missing fields, prior BLOCKs, rebase changed the base,
commit no longer exists), fall back to full review.

For a refresh review, compute two file sets (each diff is self-contained — the
upstream and prior-commit references are derived inline so the block survives
splitting across Bash tool calls):
```bash
# Focus set: files changed since the prior review
git diff --name-only "$(grep -oP '"reviewed_up_to"\s*:\s*"\K[a-f0-9]+' CODEREVIEW.md 2>/dev/null)"..HEAD -- ':!CODEREVIEW.md' ':!SECURITY.md' ':!TESTING.md' ':!SPEC.md'
# Full set: all files changed since upstream
git diff --name-only "$(git rev-parse --abbrev-ref '@{upstream}' 2>/dev/null || echo "origin/$(git rev-parse --abbrev-ref HEAD)")" -- ':!CODEREVIEW.md' ':!SECURITY.md' ':!TESTING.md' ':!SPEC.md'
```

- **Focus set**: files in FOCUS (new or re-modified since the prior review)
- **Already-reviewed set**: files in FULL but not in FOCUS

If a file appears in both the prior review's diff and the focus set (it was
reviewed before AND modified again since), it stays in the focus set and gets
full-depth review.

**What to read depends on the review tier:**

- **Full review (no prior review, or refresh conditions not met):** Read the full
  content of every modified file (not just diff hunks) to understand surrounding
  context.
- **Refresh review:** Read the full content of every file in the focus set. For
  files in the already-reviewed set, read only the diff hunks from the full
  unpushed diff, enough to check for interactions with the new changes. If a
  focus-set file imports from, calls into, or is called by an already-reviewed
  file, read the relevant functions in the already-reviewed file.

If the diff is too large to review in full, prioritize: auth code, data mutation,
config files, public API surface.

For a full or refresh review, launch the Step 5 security scan now, before Step 3.

## Step 3: Run Test Suite (if available)

*Skipped for light review.*

Look for test infrastructure: pytest.ini, setup.cfg, pyproject.toml [tool.pytest],
Makefile test targets, package.json scripts, jest.config, etc. If found, run the
test suite and record the baseline pass/fail counts. Note if no tests exist, that
is itself a finding.

Then launch the Step 5.6 built-in review in the background before starting Step 4.

## Step 4: Review

**Refresh review scoping:** Apply all 6 dimensions at full depth to files in the
focus set. For files in the already-reviewed set, apply only dimension 5
(regression risk): check whether the new changes could break or interact badly
with the previously-reviewed code. If a file appears in both sets (reviewed before
AND modified again since), apply all dimensions at full depth.

Evaluate every change against these dimensions:

1. **Correctness** — Does the code do what it claims? Off-by-one errors, null/undefined
   handling, edge cases, race conditions.
2. **Code quality** — Readability, dead code, duplication, appropriate abstraction level.
3. **Solution approach** — Is this the right approach? Is there a simpler or more robust
   alternative? Is the fix proportional to the problem?
4. **Spaghetti detection** — Does one change fix exactly one issue? Are unrelated changes
   bundled? Flag mixed-concern commits hard, they should be split. Preparatory
   refactoring that enables the main change is not a mixed concern.
5. **Regression risk** — Could this break existing functionality? Are there adequate tests
   for the changed behavior? For changes to shared functions or public APIs, trace at
   least the primary callers; a regression-risk finding names the callers it traced.
6. **Spec alignment** — If SPEC.md exists: do the changes move toward the stated
   acceptance criteria, or do they contradict or ignore the spec? This is not a
   BLOCK/WARN source on its own (the agent may be doing preparatory or refactoring
   work that does not directly advance a criterion). Note alignment or misalignment
   when relevant. If no SPEC.md exists, skip this dimension silently.

For light review, only dimensions 1 (factual accuracy of docs) and 3 (is this the
right change to make) apply.

## Step 5: Security Review

*Skipped for light review.*

`/security` runs as a background fork at `effort: max` and is usually the longest
part of a review, but it needs only the scope from Step 2. Launch it at the end of
Step 2, before Step 3, so it runs alongside the test suite, the inline review, and
the other finders, and collect it here.

The security surface is every changed file except the review-output files and
plain markdown. Markdown that instructs an agent (`SKILL.md`, `CLAUDE.md`,
`AGENTS.md`, `global-claude.md`, anything under `.claude/`) is code and is part
of it. `codereview-marker surface [<ref>]` lists the surface files that differ
between `<ref>` (default: the review base) and the working tree, so committed,
staged, and unstaged changes all count. Use it for every file list in this step;
do not hand-edit its output.

**Launch (end of Step 2).** Check whether a recent scan already covers the
current state, then invoke `/security` or skip it:

1. Read `SECURITY.md` and extract the `commit` field from `SECURITY_META`.
2. If the commit field exists and resolves in git, check for code changes since
   that commit:
   ```bash
   codereview-marker surface <meta-commit>
   ```
3. **If no code changes since the last scan** (empty output): verify the prior
   scan covers the current security surface before skipping:
   ```bash
   codereview-marker surface
   ```
   Treat the output as `NEEDED`.
   - Prior scope is `"full"`, or `NEEDED` is empty: skip.
   - Prior scope is `"paths"` with `scanned_files` in SECURITY_META: skip only
     if every file in `NEEDED` appears in `scanned_files`.
   - Otherwise (`"changes-only"`, or `scanned_files` missing): invoke
     `/security $NEEDED` to cover the full security surface.

   When skipping, carry forward existing findings, noting:
   "Security: no code changes since last scan (commit abc1234), N BLOCK /
   N WARN / N NOTE carried forward." Use the counts from SECURITY_META.
4. **If there are code changes, or no valid SECURITY_META exists:** determine the
   security surface.

   **First push (no prior scan, empty-tree base):** if there is no valid
   SECURITY_META and `codereview-marker base` returns the empty tree, the whole
   repository is the surface and is about to be published. Invoke `/security`
   with no arguments for a full audit (scope `"full"`, which also scans docs for
   committed secrets), and skip the file-list computation below.

   Otherwise, compute the files that need scanning:
   ```bash
   if [valid SECURITY_META commit]; then
     codereview-marker surface <meta-commit>   # changes since last scan
   else
     codereview-marker surface                 # no prior scan: surface vs base
   fi
   ```
   Treat the output as `SCAN_FILES`.
   Invoke `/security $SCAN_FILES` with the computed file list. This covers
   both committed and uncommitted changes since the last scan without
   re-scanning files the prior review already covered.

Its completion arrives later as a task notification (Step 7 says how to wait).
If it arrives before Step 4 is done, set the report aside and finish Step 4
first, so your own review is not shaped by it.

**Collect (here).** If the `/security` completion has not arrived, wait for it;
do not poll. Incorporate its findings into the final report, or the
carried-forward counts when the scan was skipped.

## Step 5.5: External Reviewers (optional)

*Skipped for light review.*

If the inline review (Step 4) or `/security` (Step 5, including findings it
carried forward) reports a secret, credential, or private key in the diff, skip
the external reviewers: the script would send that secret to OpenAI and Google
with the diff. Record `Skipped (secret in diff).` in Step 9 and say so in the
report.

Otherwise, if `review-external.sh` is on PATH, run it synchronously with the
diff, in a Bash call with a 360000 ms timeout:

```bash
COST_LOG=$(mktemp /tmp/.claude-external-cost-XXXXXX)
EXTERNAL_FINDINGS=$(git diff "$(codereview-marker base)" -- ':!CODEREVIEW.md' ':!SECURITY.md' ':!TESTING.md' ':!SPEC.md' | review-external.sh 2>"${COST_LOG}")
EXTERNAL_COST=$(cat "${COST_LOG}" 2>/dev/null)
rm -f "${COST_LOG}"
```

The script gives each provider up to 300 seconds, and a 3,000-line diff takes
close to two minutes, so the Bash tool's 2-minute default would cut the call off
and move it to the background.

If the script is not on PATH, or produces no output, skip silently: print no
status echoes, no "running external reviewers" preamble, and no empty-findings
block. The sole record of the no-reviewer case is one line in the "External
reviewers" section (Step 9): `None configured.`. If it produces findings,
include them in your report (Step 6) with provider tags preserved, and include
the cost log lines in the "External reviewers" section of CODEREVIEW.md
(Step 9).

External reviewers run once at initial review. Do NOT re-run them during
fix/re-review cycles (Step 7).

## Step 5.6: Built-in /code-review (second finder)

*Skipped for light review.*

Claude Code's built-in `/code-review` runs as a second, independent finder. It is
launched right after Step 3 and collected here, so it runs alongside Steps 4 and 5
and rarely adds wall-clock time. It is fail-open: if it is unavailable, fails, or
times out, the review continues without it.

**Launch (after Step 3, before Step 4).** If `command -v claude` succeeds, create
the output file and take a working-tree reading in one Bash call:

```bash
mktemp /tmp/.claude-builtin-review-XXXXXX; { git status --porcelain -- ':!CODEREVIEW.md' ':!SECURITY.md' ':!TESTING.md' ':!SPEC.md'; git diff -- ':!CODEREVIEW.md' ':!SECURITY.md' ':!TESTING.md' ':!SPEC.md'; } | sha256sum
```

Then start the review in a second Bash call with `run_in_background` and a
15-minute timeout, substituting the path the first call printed:

```bash
claude -p "/code-review high" --output-format json --disallowedTools "Edit,Write,NotebookEdit" > <output-file> 2>/dev/null
```

Keep the tool restriction and the redirect exactly as shown. /codereview is
verifier-only, and the child needs no edit tools (`--fix` is never passed). The built-in's findings must not reach your
context before Steps 4 and 5 are done: reading them earlier would anchor your own
review on them, and two independent finders are the point. If `claude` is not on
PATH, skip silently and record `Not available.` under "Built-in review" in Step 9.

**Collect (here).** Completion is delivered by the harness as a task notification,
the same as the Step 5 and Step 7 forks. Wait for it; do not poll for completion
(no `until`/`while` + `sleep` loops, no `pgrep`, no reading the file before the
notification arrives). Then read the result and remove the file:

```bash
jq -r 'select(.is_error | not) | .result // empty' <output-file>; rm -f <output-file>
```

Re-run `{ git status --porcelain -- ':!CODEREVIEW.md' ':!SECURITY.md' ':!TESTING.md' ':!SPEC.md'; git diff -- ':!CODEREVIEW.md' ':!SECURITY.md' ':!TESTING.md' ':!SPEC.md'; } | sha256sum` (the review files are excluded because /security writes SECURITY.md while the built-in runs). If the hash differs
from the launch reading, the tree changed while the built-in ran: discard its
findings, record `Failed (tree changed).` in Step 9, and tell the user.
If the result is empty or unparseable, or the run timed out, skip silently and
record `Failed (skipped).` in Step 9. Otherwise the result lists findings, usually
as a JSON array of `{file, line, summary, failure_scenario}`. Carry each into
Step 6 tagged `(claude-code)`. They have no severity; Step 6 classifies them.

The built-in review runs once at initial review. Do NOT re-run it during
fix/re-review cycles (Step 7).

## Step 6: Report

For refresh reviews, begin the report with a scope line:
> **Review scope:** Refresh review. Focus: N file(s) changed since prior review
> (commit abc1234). M already-reviewed file(s) checked for interactions only.

Classify every finding:

- **BLOCK** — Must fix before pushing. Bugs, data loss risks, security vulnerabilities,
  broken tests, spaghetti commits mixing unrelated concerns.
- **WARN** — Should fix. Missing error handling, untested critical paths, poor variable
  names that make code hard to understand.
- **NOTE** — Informational only. Optional improvements, alternative approaches to
  consider, and findings you are not confident in. Do not auto-fix these.

Classify the built-in review's `(claude-code)` findings from Step 5.6 with the same
definitions. Drop any that are about style or writing conventions (No style
policing) or about the review-output files (CODEREVIEW.md, SECURITY.md, TESTING.md,
SPEC.md). Confirm each against the code before classifying it; one you cannot
confirm is a NOTE. One that matches an Accepted Risks entry is a NOTE, as in Step 1.
On a refresh review, one in an already-reviewed file stays above NOTE only if it
concerns an interaction with the new changes. When you and the built-in reported
the same issue, keep one finding and tag it `(also claude-code)`, so CODEREVIEW.md
records which finder caught what.

Format each finding:
```
[SEVERITY] file:line — description
  Evidence: [specific code or pattern observed]
  Suggested fix: [concrete recommendation]
```

## Step 6.5: Write Preliminary CODEREVIEW.md

*Skipped for light review if no BLOCK/WARN findings.*

If BLOCK or WARN findings exist, write (or update) CODEREVIEW.md with the current
findings NOW, before the fix loop. The `/codefix` skill reads CODEREVIEW.md as its
input spec, so findings must be on disk before it is invoked. Use the same format
as Step 9 but mark the entry as preliminary (it will be overwritten with the final
state after the fix loop completes).

If no BLOCK/WARN findings exist, skip this step. CODEREVIEW.md will be written
once in Step 9.

## Step 7: Fix/Re-review Loop

*Skipped for light review.*

If BLOCK or WARN findings exist (and CODEREVIEW.md has been written in Step 6.5),
invoke `/codefix` to apply fixes. The codefix skill runs in a separate forked
context: it reads CODEREVIEW.md findings as a spec and applies minimal fixes
without self-evaluation.

Before each `/codefix` invocation, record the working tree so you can tell
exactly what codefix changed:
```bash
git stash create
```
It prints a commit holding the current working tree without changing anything,
or nothing when the tree matches HEAD; call the printed commit (or `HEAD`)
`PRE_FIX`.

Codefix completion is delivered by the harness: the Skill invocation either
returns the result directly or, when the fork runs as a background task, a
task notification arrives when it finishes. Wait for that delivery and
do not poll for completion: no `until`/`while` + `sleep` loops, no `pgrep`,
no watching task-output files. The harness signal always arrives, and a polling
loop can outlive the review as an orphaned process. The same
applies to the `/security` invocation in Step 5 and to the security re-check
below.

After codefix completes, re-review its changes and re-check their security:

- **Security re-check.** List the files codefix changed:
  ```bash
  codereview-marker surface <PRE_FIX>
  ```
  If the list is not empty, invoke `/security post-fix <files>` when this
  review has already written a SECURITY.md entry (Step 5 scanned, or an
  earlier cycle's re-check ran; it updates that entry in place), or
  `/security <files>` when it has not. No codefix change reaches
  the push without a security pass, and SECURITY.md stops listing fixed
  findings as open. It runs as a background fork; do the re-review and the
  test run below while it runs, then wait for its completion before deciding
  on the next cycle.
- **Re-review.** This is a refresh review within the current context: re-read
  the modified files, check whether findings are resolved, and check for new
  issues introduced by the fixes.

Do NOT invoke `/codefix` again without updating CODEREVIEW.md first.

If the test suite exists, re-run it after each codefix pass. Compare pass/fail
counts against the Step 3 baseline. If tests regressed, the fix cycle fails.

If the re-review or the security re-check finds remaining or new BLOCK/WARN
findings, update CODEREVIEW.md with the new findings before invoking `/codefix`
again.

**Cycle limit: 3.** Each cycle is one CODEREVIEW.md update, one `/codefix`
invocation, one security re-check, and one re-review. If BLOCKs remain after 3 cycles, or tests
regressed, report remaining issues as "requires manual intervention." Do not
attempt further fixes.

## Step 8: Write Marker File

Only if all BLOCKs are resolved AND tests did not regress, run the deterministic
marker script in a single Bash invocation:

```bash
codereview-marker write
```

The script is on PATH (do not prefix with `bin/`). It hashes the same diff the
pre-push hook checks and writes the marker where the hook looks for it.

Do NOT write the marker if any BLOCK items remain or tests regressed.

## Step 9: Update CODEREVIEW.md

Update (or create) `CODEREVIEW.md` in the project root. Keep only:
- The current entry
- A one-paragraph summary of the previous entry (if one exists)

Carry forward the Accepted Risks section from the prior entry. Remove entries
whose code is no longer present in the diff. If the human added new entries
between reviews, preserve them.

**Uncommitted prior entry.** Condensing is safe only when git history holds the
full prior entry. Use the `git status --porcelain -- CODEREVIEW.md` reading
taken in Step 1, before this run wrote anything; this run's own writes (Step
6.5, Step 7) always make the file look modified. A preliminary entry written by
this run is always overwritten, never carried forward. Empty Step 1 output:
condense as above. Non-empty output (untracked, modified, or
staged): the prior entry has no copy in git history, and condensing it would
destroy the only full copy, including any resolution notes added since the last
review. Instead of the prior-summary line, write the heading
`## Prior review carried forward (uncommitted; not current findings)` followed
by the file content as it stood before this run, verbatim, including any block
an earlier uncommitted run carried forward. Drop only its `REVIEW_META` footer: the file
must contain exactly one `REVIEW_META` line, because Step 2 and `/pr merge`
grep its fields file-wide. State the carry-forward in the Output Summary so the
user knows to commit CODEREVIEW.md. The next run after a commit condenses
normally.

Format:
```markdown
## Review — YYYY-MM-DD (commit: abc1234)

**Summary:** [1-2 sentence summary of what was reviewed]

**External reviewers:**
[Cost log lines from Step 5.5, or "None configured.", "Skipped (light review).",
or "Skipped (secret in diff)."]

**Built-in review:**
[`/code-review high`: N findings, M kept after Step 6; or "Not available.",
"Failed (skipped).", "Failed (tree changed).", or "Skipped (light review)."]

### Findings

[findings list, or "No issues found."
Preserve the (provider) tag on any external reviewer findings, and the
(claude-code) or (also claude-code) tag on built-in review findings.]

### Fixes Applied

[list of auto-fixes with provider attribution if the finding came from an
external reviewer, or "None."]

### Accepted Risks

[carried-forward findings the human has explicitly accepted, or "None."]

---
*Prior review (YYYY-MM-DD): [one sentence summary of prior findings and status]*

<!-- REVIEW_META: {"date":"YYYY-MM-DD","commit":"abc1234","reviewed_up_to":"<full-HEAD-sha>","base":"<upstream-ref>","tier":"full|refresh|light","block":N,"warn":N,"note":N} -->
```

## Output Summary

If auto-fixes were applied in this run, print them first (skip this block entirely
if no fixes occurred). Collect the list from every `/codefix` invocation's Step 4
report across all cycles, deduplicating if the same finding was touched twice:

```
Fixes Applied (this run):
  [SEVERITY] file:line — one-line description of the change
  [SEVERITY] file:line — one-line description of the change
```

Then end with a summary table:

| Severity | Found | Auto-fixed |
|----------|-------|------------|
| BLOCK    | N     | N          |
| WARN     | N     | N          |
| NOTE     | N     | —          |

Final verdict:
- All BLOCKs resolved, tests stable: **"Changes are ready to push."**
- BLOCKs remain or tests regressed: **"BLOCKED: N issue(s) require manual intervention."**
