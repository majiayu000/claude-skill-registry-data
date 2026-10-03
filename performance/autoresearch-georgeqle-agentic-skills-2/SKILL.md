---
name: autoresearch
description: Autonomous experiment loop — iteratively mutate code, measure a metric, keep only improvements (hill-climbing ratchet)
type: orchestrator
version: v0.0
invocation: orchestrator
argument-hint: "[path/to/program.md]"
---

# Autoresearch

Autonomous experiment loop inspired by Karpathy's autoresearch pattern. Reads a `program.md` research program, proposes one hypothesis per iteration, implements it within a declared sandbox, measures a single metric, and keeps only improvements. Git branches isolate experiments; a TSV log tracks all results.

## When to Use

When the user wants to autonomously optimize a measurable codebase property: benchmark throughput, bundle size, test coverage, load time, memory usage, build speed, or any metric expressible as a shell command that prints a number.

## Preconditions

- A `program.md` file exists (default: `./program.md`, or path from `$ARGUMENTS`). If missing, recommend `/autoresearch-prep` to scaffold one.
- Git working tree is clean (no uncommitted changes)
- The metric command runs successfully and prints a parseable number

## program.md Format

The user creates this file. Required sections:

```markdown
# Research Program

## Metric
command: <shell command that prints a single number to stdout>
direction: higher-is-better | lower-is-better

## Budget
max_iterations: <number>

## Sandbox
files:
  - <glob patterns of files the agent may modify>
exclude:
  - <glob patterns to never touch>

## Research Directions
1. <direction one>
2. <direction two>
```

Optional sections:

```markdown
## Test Command
command: <shell command that must exit 0 before measuring>
required: true

## Budget
metric_timeout_seconds: <default 300>

## Context
<free-form notes about the codebase, prior work, constraints>
```

## Process

### 0. Validate Preconditions

1. Resolve `program.md` path from `$ARGUMENTS` (default: `./program.md`). If the file does not exist, stop and recommend `/autoresearch-prep`.
2. Parse and validate required fields: `Metric.command`, `Metric.direction`, `Budget.max_iterations`, `Sandbox.files`.
3. Verify git working tree is clean (`git status --porcelain` is empty). Stop if dirty.
4. Create `.autoresearch/` directory if it does not exist.
5. Record the current branch as the **base branch**.
6. Add `.autoresearch/` to `.gitignore` if not already present.

### 1. Establish Baseline

1. Run the metric command from the project root.
2. Parse the last number from stdout (strip non-numeric lines).
3. Record as iteration 0 in `.autoresearch/results.tsv`:
   ```
   iteration	timestamp	hypothesis	metric_value	delta	delta_pct	status	branch	commit	notes
   0	<ISO-8601>	baseline	<value>	0	0.00%	baseline	<base-branch>	<HEAD-sha>	initial measurement
   ```
4. Set `best_value = baseline_value`.

### 2. Check Stop Conditions

Before each iteration, check in order:

1. **Stop file**: if `.autoresearch/stop` exists, log "stop file detected" and go to step 9.
2. **Iteration limit**: if current iteration > `max_iterations`, go to step 9.
3. **Re-read program.md**: pick up any user edits to directions, budget, or context mid-run.

### 3. Propose Hypothesis

1. Read: research directions, past results from `.autoresearch/results.tsv`, current sandbox file contents, and context section.
2. Propose exactly **one** specific, testable hypothesis. Prefer untried directions. Avoid repeating failed approaches.
3. The hypothesis must name: what to change, which file(s), and the expected effect on the metric.
4. Log the hypothesis before implementing.

### 4. Create Experiment Branch

1. Ensure base branch is checked out and clean.
2. Create and checkout: `autoresearch/iter-{N}-{slug}` where `{slug}` is a 2-4 word kebab-case summary of the hypothesis.

### 5. Implement the Change

1. Modify **only** files matching the sandbox glob patterns.
2. Never modify files matching exclude patterns.
3. **Never modify**: the metric command/script, benchmark suite, test harness, evaluation code, or anything outside the sandbox.
4. Keep changes minimal and focused on the single hypothesis.
5. Commit on the experiment branch with message: `autoresearch: iter {N} — {hypothesis summary}`.

### 6. Validate Build/Tests

1. If a test command is configured and `required: true`:
   - Run the test command.
   - If it fails: log `status: test-failed`, checkout base branch, delete experiment branch, record in results.tsv, continue to next iteration.
2. If no test command is configured, skip this step.

### 7. Measure

1. Run the metric command with the configured timeout (default 300s).
2. Parse the last number from stdout.
3. If the command fails or times out: log `status: measure-failed`, checkout base branch, delete experiment branch, record in results.tsv, continue to next iteration.

### 8. Evaluate (Ratchet)

Compare measured value to `best_value` using the configured direction:

**If improved:**
1. Checkout base branch.
2. Fast-forward merge the experiment branch: `git merge --ff-only autoresearch/iter-{N}-{slug}`.
3. Update `best_value`.
4. Record `status: kept` with the delta and delta percentage in results.tsv.
5. Delete the experiment branch (it's merged).

**If not improved (or equal):**
1. Checkout base branch.
2. Record `status: reverted` with the delta in results.tsv.
3. Delete the experiment branch.

Always ensure the working tree is clean before proceeding to the next iteration.

### 9. Report Final Status

When the loop ends (stop file, iteration limit, or all directions exhausted):

1. Write `.autoresearch/summary.md`:
   - Baseline value → final best value and total improvement (absolute + percentage).
   - Per-iteration table (from results.tsv).
   - Directions attempted vs. untried.
   - Top 3 most impactful kept changes.
2. Print a summary table to the terminal.
3. Do **not** push to remote — all work stays local for user review.

## Output

- `.autoresearch/results.tsv` — append-only experiment log
- `.autoresearch/summary.md` — written at loop end

## Constraints

- **Sandbox is absolute**: never modify files outside declared sandbox globs.
- **Never touch eval**: never modify the metric command, benchmark suite, or test harness.
- **One hypothesis per iteration**: no bundling multiple changes.
- **Clean state between iterations**: never leave dirty working tree.
- **No remote push**: all work stays local.
- **No GitHub Actions**: do not create CI workflows.
- **Autonomous**: no user approval per iteration. User steers by editing `program.md` or creating `.autoresearch/stop`.

## Failure Recovery

If the agent finds itself on an experiment branch with uncommitted changes between iterations:
1. `git checkout -- .` to discard changes.
2. `git checkout <base-branch>`.
3. Delete the orphaned experiment branch.
4. Record `status: crashed-recovered` in results.tsv.
5. Continue from the next iteration.

## Shipping

This skill does **not** follow the shared shipping contract. All work stays local and unpushed. The user reviews results and decides what to keep and push.

**Next work:** none — loop is self-contained
**Recommended next command:** `git log --oneline` to review kept changes, then push when satisfied
