---
description: "Launch a swarm of bug-hunting agents against a target file, module, or topic."
---

# /bug-hunt

Launch a swarm of bug-hunting agents against a target file, module, or topic. Output is a **triaged candidate-issue list** ready to feed into `/create-issue` — not ratings, not architectural critique. The job is: find bugs that would make good GitHub issues.

This is the issue-filing flavor of `/swarm-audit`. Use it when your goal is "populate the backlog with concrete bugs from this code," not "evaluate the design."

## Arguments

- `$ARGUMENTS` - Optional configuration. Space-separated tokens:
  - First positional: target (file path, directory, or quoted topic like `"the auth flow"`). Required.
  - `hunters=N` — Number of hunter agents (default: 4, min: 3, max: 6)
  - `severity-floor=critical|major|minor` — Drop findings below this severity in the final list (default: `minor`)
  - `auto-file=critical|major|none` — Automatically file issues at this severity or above without asking (default: `none` — always confirm)
  - `output=DIR` — Output directory for the candidate list (default: `docs/bug-hunt/`). Pass `output=-` to skip writing.

Examples:
```
/bug-hunt src/payments
/bug-hunt "the websocket reconnection logic" hunters=5
/bug-hunt src/auth severity-floor=major auto-file=critical
/bug-hunt . hunters=6 output=docs/audit/pre-release
```

## Instructions

### 1. Parse Arguments and Resolve Target

```
TARGET          = first positional (file path, dir, or quoted topic)
HUNTER_COUNT    = extract from hunters=N (default: 4, clamp 3-6)
SEVERITY_FLOOR  = extract from severity-floor=X (default: minor)
AUTO_FILE       = extract from auto-file=X (default: none)
OUTPUT_DIR      = extract from output=DIR (default: docs/bug-hunt/, "-" skips write)
```

If TARGET is missing, refuse and ask the user what to hunt against — bug-hunt without a scope is too noisy.

### 2. Quick Context Pass

Before launching hunters, read enough to brief them properly (5-10 minutes max):

- Read the target file(s) or the entry point of the target topic
- Read `CLAUDE.md` if present (especially attribution policy, test conventions, persistence rules)
- Skim `README.md` for domain context
- Note the test framework so hunters can suggest concrete repro tests

Build a **shared briefing** (10-20 lines) that every hunter receives. This prevents three hunters from wasting tokens learning the same setup.

### 3. Select Hunter Panel

All hunters share the same job (find bugs) but bring different lenses. Always include Skeptic + Guardian + Tester. Add the rest based on what the target touches.

#### Core Hunters (always included)

| Hunter | Nickname | Lens | Personality |
|--------|----------|------|-------------|
| Logic | "Skeptic" | Logic errors, false assumptions, off-by-one, wrong operators, claims in comments that diverge from code | Cynical engineer who reads every line assuming it lies. Cross-references comments and docstrings against actual behavior. |
| Reliability | "Guardian" | Race conditions, data integrity, persistence corruption, error handling gaps, recovery paths, lazy-init that overwrites state | Paranoid SRE who has watched production data disappear. Specifically hunts the class of bug where a fix silently destroys persisted state (e.g., default-then-save instead of load-then-merge). |
| Edge Cases | "Tester" | Untested branches, boundary conditions (empty/null/max/zero/negative/unicode/concurrent), error paths, what happens when the happy path doesn't | QA engineer who believes every untested branch is a latent bug. Names specific inputs that would break each function. |

#### Extended Roster (pick by relevance to target)

| Hunter | Nickname | Lens | Include When |
|--------|----------|------|--------------|
| Security | "Adversary" | Injection, auth bypass, SSRF, path traversal, secret leakage, attack surface | Target touches auth, network code, user input, external APIs, file operations |
| UX | "Operator" | User-facing regressions, broken error messages, accessibility, confusing states, broken links/buttons | Target touches UI, output formatting, user-facing strings, error flows |
| Perf | "Profiler" | N+1 queries, accidental quadratic loops, missing indexes, unbounded growth, memory leaks, sync-in-async | Target touches data access, hot paths, request handling, large collections |
| Template Critic | "Auditor" | Generic templates that produce defective customized output (residual markers, attribution leaks, heading drift, length runaway, hallucinated examples) | Target is `generic/*.md` |

#### Selection Algorithm

```
1. Start with 3 core hunters (Skeptic, Guardian, Tester)
2. For each remaining slot up to HUNTER_COUNT:
   - Adversary if target touches auth/network/input/external IO
   - Operator if target touches UI/output/user-facing strings
   - Profiler if target touches data/hot paths/large collections
3. Stop when slots are full
```

State the selected panel and *why each was chosen* to the user before launching.

### 4. Launch Hunters

Launch all hunters in parallel using the Agent tool. Each hunter receives the shared briefing, the TARGET, their persona, and the **strict finding template** below — uniform output is critical for dedup in step 5.

**Hunter prompt template:**

````
You are "{NICKNAME}" — {PERSONALITY}

Your job is to **find bugs that would make good GitHub issues** in the following target. You are not grading the code. You are not proposing architectural changes. You are hunting concrete, fileable bugs.

## Target
{TARGET}

## Shared Briefing
{BRIEFING}

## Your Lens
{LENS}

## Rules

1. READ actual source code. Verify each finding against the code, not against vibes.
2. Every finding must be **concrete and reproducible**. "This might fail" is rejected. "Calling foo() with input=null on line 42 hits the unguarded `.length` on line 47 and throws" is accepted.
3. Stay in your lens. If you stray into other hunters' lanes (e.g., Tester writing security findings), dedup later eats your work.
4. Do NOT suggest fixes longer than 1-2 lines. Issue authors decide the fix; you describe the bug.
5. If you find nothing in your lens, return an empty findings list with a one-line "lens swept, no bugs in scope" note. Empty is honest. Padded is harmful.

## Output (use this exact format for each finding)

```yaml
- title: "bug(scope): concise description"        # issue-ready, lowercased verb
  severity: critical | major | minor              # see severity rubric below
  location: path/to/file.ext:LINE                 # primary site; add more in evidence
  symptom: |
    One-paragraph description of what goes wrong from the user's or system's perspective.
  repro: |
    Concrete steps to trigger it. Inputs, state, sequence. A test author could write this.
  evidence: |
    file:line citations + 1-3 short quoted lines of relevant code.
  hypothesis: |
    Why this happens in one sentence.
  fix_sketch: |
    1-2 lines on the likely fix direction (e.g., "Add null check before .length" or "Use load-then-merge in save()").
  dedup_key: "<short stable phrase>"              # e.g., "null-deref-in-charge-handler"
```

## Severity Rubric

- **critical**: Data loss, security boundary breach, complete feature outage, or production-down class.
- **major**: Wrong result for plausible input, silent corruption of non-critical state, UX broken for common path, performance cliff.
- **minor**: Edge case, cosmetic, narrow-input failure, missing input validation that is defensive only.

Cap your findings at 6. Quality over quantity.
````

**Run hunters as foreground Agent calls.** If HUNTER_COUNT > 4, batch: first 4 in parallel, then the rest.

**Delegation tiers (cost discipline — do not strip):**

Roles per `/tiered-delegation`: **workhorse** = one tier below the session ceiling, **mechanical** = cheapest available tier. Concrete model names live only in that skill's CUSTOMIZE-marker ladder — never here.

- **Hunters run at the workhorse tier by default.** Bug-hunting breadth is workhorse work; do not spawn hunters at the ceiling. The orchestrator's dedup/triage (step 5) and the user-facing report are where the expensive judgment lives.
- **Mechanical passes at the mechanical tier.** The step-5 dedup key matching, severity-floor filtering, and any pre-filter over candidate files run at the mechanical tier at low effort.
- **Sample-verify instead of up-tiering.** If hunter findings look noisy, re-check a ~10% sample with a stronger tier before filing anything; a finding that fails its sample check sends the whole batch back for verification, not for a full re-run up-tier.
- **Fan-out budget: ~12 workhorse/ceiling subagents per run.** The budget counts workhorse- and ceiling-tier agents (the hunters); mechanical-tier passes and the ~10% sample-verify checks do not count against it. Exceeding 12 requires an explicit one-line justification in the report; **20 is a hard ceiling that includes every refute/verify agent, and no justification lifts it** (≤3 refuters per finding — queue rounds rather than widen). The 6-hunter maximum sits well inside this budget.

### 5. Dedup and Triage

After hunters return, build the unified candidate list:

1. **Parse every hunter's YAML findings.**
2. **Dedup** by:
   - Exact `dedup_key` match → merge (combine evidence, take highest severity, list all reporting hunters)
   - Same `location` (file + line within ±3) AND overlapping symptom keywords → merge
   - Otherwise keep separate
3. **Drop** any finding below `SEVERITY_FLOOR`.
4. **Sort** by severity (critical → major → minor), then by hunter-agreement count (more hunters = more confidence).
5. **Check for existing issues** — for each candidate, run a quick `gh issue list --search "<title keywords>" --state all --json number,title --limit 3` to flag possible duplicates of already-filed issues. Annotate each candidate with `possible_duplicates: [...]` if any.

### 6. Build the Candidate List Document

Unless `output=-`, write to `${OUTPUT_DIR}/<slugified-target>-<YYYYMMDD>.md`:

```markdown
# Bug Hunt: {TARGET}

**Date:** {today}
**Hunters:** {nicknames}
**Severity floor:** {SEVERITY_FLOOR}
**Candidates:** N (after dedup and floor)

## Summary Table

| # | Severity | Title | Location | Hunters | Possible Dupes |
|---|----------|-------|----------|---------|----------------|
| 1 | critical | bug(payments): charge handler null-derefs on missing currency | src/payments/charge.ts:47 | Skeptic, Guardian | — |
| 2 | major | ... | ... | ... | #1834 |
| ... | ... | ... | ... | ... | ... |

## Candidate Details

{For each candidate, render the merged finding in the template below.}

### #N — {title}

**Severity:** {severity} | **Hunters:** {nicknames} | **Possible duplicates:** {issue#s or "—"}

**Symptom**
{symptom paragraph}

**Reproduction**
{repro steps}

**Evidence**
{file:line citations + quoted code}

**Hypothesis**
{one sentence}

**Fix sketch**
{1-2 lines}

---
```

### 7. Confirm and File

Present the summary table to the user. Then, depending on `AUTO_FILE`:

- **`auto-file=none` (default):** Ask which candidates to file. Accept ranges like `1,3,5-7` or `all` or `none`. Skip anything with `possible_duplicates` unless the user confirms.
- **`auto-file=major`:** File every `critical` and `major` candidate that has no `possible_duplicates` without asking. Then ask about the rest.
- **`auto-file=critical`:** File every `critical` candidate that has no `possible_duplicates` without asking. Then ask about the rest.

For each candidate the user accepts, file an issue using the same shape as `/create-issue`:

```bash
gh issue create \
  --title "${TITLE}" \
  --label "bug,from-review" \
  --body "$(cat <<EOF
## Symptom
${SYMPTOM}

## Reproduction
${REPRO}

## Evidence
${EVIDENCE}

## Hypothesis
${HYPOTHESIS}

## Fix sketch
${FIX_SKETCH}

## Source
Found during /bug-hunt on $(date +%Y-%m-%d). Reported by: ${HUNTERS}.
EOF
)"
```

**Verify labels exist** before using them. Skip missing labels rather than failing.

This repo's label set is the GitHub default plus `from-review` — there is **no** `from-bug-hunt` label, so findings are filed as `bug,from-review` (the repo's only provenance label). Available: `bug`, `documentation`, `duplicate`, `enhancement`, `good first issue`, `help wanted`, `invalid`, `question`, `wontfix`, `from-review`. Do not invent a new label inline — `gh issue create` fails on an unknown label; create it with `gh label create` first if one is genuinely needed.

### 8. Commit Candidate List (only if files were written)

**Stage explicit paths.** `git status --short` first, then `git add` the report files you just
wrote, **by name**. Never `git add -A`, `git add .`, `git add -u`, `git add <dir>/`, or
`git commit -a`. A trailing-slash directory add is a bulk add: the working copy is shared with
concurrent sessions, so `${OUTPUT_DIR}/` may also hold a stale report from another run or a file
that is not yours. `-u` is not the safe one: it restages every *tracked* file whose worktree copy
differs, including files a clean/smudge filter rewrote without you touching them — that is how
`git add -u` turned a tracked 21KB `.docx` into a git-lfs pointer and committed it as an edit.

```bash
git status --short "${OUTPUT_DIR}"
git add "${OUTPUT_DIR}/<report-file-1>.md" "${OUTPUT_DIR}/<report-file-2>.md"   # name each file you wrote
git commit -m "docs: bug-hunt of <target> (<N> candidates, <M> filed)"
```

Do NOT push. Do NOT commit if `output=-`.

### 9. Report to User

Output a final summary:

```markdown
## Bug Hunt Complete: {target}

| Metric | Value |
|---|---|
| Hunters | {N} ({nicknames}) |
| Raw findings | {pre-dedup count} |
| Candidates | {post-dedup, post-floor count} |
| Issues filed | {filed count} |
| Possible duplicates flagged | {dupe count} |

### Filed Issues
{table of #issue → title}

### Skipped (your decision or duplicate)
{table of skipped candidates}

### Recommended Next Step
{usually: /tackle-issues with the new issue numbers, or run /bug-hunt on a related area}
```

## Configuration

### Severity Rubric

| Severity | Meaning |
|:---------|:--------|
| critical | Data loss, security breach, full outage class. File immediately. |
| major | Wrong result for plausible input, silent corruption of non-critical state, broken common-path UX. |
| minor | Edge case, cosmetic, narrow-input failure, defense-in-depth gaps. |

### Hunter Behavior Rules

- Hunters MUST be concrete. Every finding has a file:line, a repro, and evidence. No "code smells."
- Hunters MUST NOT propose architectural changes. That is `/project-audit` territory.
- Hunters MUST cap findings at 6. Quality over noise.
- Hunters MUST stay in their lens. Strays cost tokens and produce dedup noise.
- Hunters SHOULD return empty if their lens finds nothing — empty is a valid result.

## Examples

```
/bug-hunt src/payments
/bug-hunt "the websocket reconnection logic" hunters=5
/bug-hunt src/auth severity-floor=major
/bug-hunt . hunters=6 auto-file=critical
/bug-hunt src/storage hunters=3 output=-
```

## Comparison to Sister Skills

| Goal | Use |
|---|---|
| "Find bugs to file as issues" | `/bug-hunt` |
| "Map an unfamiliar repo first" | `/recon` |
| "Rate the whole project" | `/project-audit` |
| "Audit a design doc / RFC" | `/swarm-audit` |
| "Review this PR before merge" | `/agentic-audit` |

A typical pipeline: `/recon src/payments` → `/bug-hunt src/payments` → `/tackle-issues` on the newly-filed issues.
