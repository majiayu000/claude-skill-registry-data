---
name: open-pr
description: Open a GitHub pull request with a thorough auto-generated summary. Use when the user asks to open, create, or draft a PR. Fetches origin/main, mandatorily runs all pre-commit checks and pytest (off the login node on HPC), mandatorily runs /thermo-nuclear-code-quality-review against the diff, spawns 1–2 additional review subagents that deeply review the diff, and posts their findings into the PR body.
argument-hint: "[base-branch (default: main)] [--draft]"
allowed-tools: Bash, Read, Grep, Glob, Agent, Write, Edit
---

# Open PR

End-to-end PR creation: diff against `origin/main`, run the project's quality gates (pre-commit + pytest) on a compute node when on HPC, run `/thermo-nuclear-code-quality-review` against the diff, spawn deep-review subagents, and post a rich PR description with everything stitched together.

**Two checks are mandatory on every invocation and cannot be skipped by the user:**

1. All pre-commit hooks defined in `.pre-commit-config.yaml` (if a config exists).
2. `/thermo-nuclear-code-quality-review`, run against the diff.

If the user asks you to "skip pre-commit", "skip thermo-nuclear", "skip the review", or any equivalent, refuse and explain that these gates are now mandatory for this skill. They can still skip `pytest` separately if they ask.

## Input

<args>
$ARGUMENTS
</args>

Parse `$ARGUMENTS` for an optional base branch (defaults to `main`) and a `--draft` flag. If the user already named a base branch in the conversation, use that.

## Step 0: Pre-flight

Run these in parallel:

```bash
git rev-parse --is-inside-work-tree
git rev-parse --abbrev-ref HEAD
git status --porcelain
git remote -v
gh auth status
```

Create a writable job directory for generated diff and gate logs:

```bash
JOB_DIR="${CLAUDE_JOB_DIR:-$(mktemp -d -t softnano-open-pr.XXXXXX)}"
```

Hard stops — refuse to continue and report back:

- Not a git repo.
- Current branch *is* the base branch (refuse to PR `main` into `main`).
- `gh` not authenticated.
- Uncommitted changes that would be silently excluded from the PR. Ask the user whether to commit them, stash them, or proceed anyway.

## Step 1: Fetch and diff against origin/main

```bash
git fetch origin <base-branch> --prune
BASE=$(git merge-base HEAD origin/<base-branch>)
git log --oneline "$BASE"..HEAD
git diff --stat "$BASE"..HEAD
git diff "$BASE"..HEAD              # full diff — save to $JOB_DIR/pr.diff if large
```

Save the full diff to `$JOB_DIR/pr.diff` if it's bigger than a few hundred lines — the review subagents will read it from disk.

Build a punch list of the diff: files touched, rough categories (feature, bugfix, refactor, test, docs, config), notable additions/deletions.

## Step 2: Run pre-commit and pytest — NOT on a login node

**Pre-commit is mandatory if `.pre-commit-config.yaml` exists.** You may not skip it, even if the user asks. If `pre-commit` is not installed, install it (`pip install pre-commit`) before continuing — do not silently bypass the gate.

Detect whether a pre-commit config and a test suite exist:

```bash
test -f .pre-commit-config.yaml && echo "has pre-commit"

# pytest needs a real signal — a test directory OR explicit pytest config.
# Do NOT use pyproject.toml/setup.cfg alone: those exist for packaging too,
# and running pytest in a repo with no tests exits 5 ("no tests collected"),
# which would fail the gate and block the PR for no reason.
has_pytest=no
{ test -d tests || test -d test; } && has_pytest=yes
test -f pytest.ini && has_pytest=yes
test -f pyproject.toml && grep -q '\[tool\.pytest' pyproject.toml && has_pytest=yes
test -f setup.cfg && grep -q '^\[tool:pytest\]' setup.cfg && has_pytest=yes
echo "has_pytest=$has_pytest"
```

If either exists, you must run them before opening the PR. **On an HPC login node these are forbidden — they spawn many subprocesses and burn shared CPU.** Invoke the `cluster-instructions` skill to detect the environment:

- If `cluster-instructions` reports you are on a **login node** (Isambard, CX3, HX1): submit the gate as an interactive or batch job per that skill's templates. Do not shell-run `pre-commit` or `pytest` directly. The command to wrap is:

  ```bash
  pre-commit run --from-ref "$BASE" --to-ref HEAD && pytest -q
  ```

  (Drop the `pre-commit` half if no config; drop the `pytest` half if no tests.)

- If you're on a **compute node** or a non-HPC workstation: run the gate directly in the foreground and capture output to `$JOB_DIR/gate.log`.

If `pre-commit` is not installed but a config exists, install it first (`pip install pre-commit`) — don't silently skip the gate.

**Do not open the PR if the gate fails.** Report the failure, surface the relevant log lines, and stop. The user fixes the failure, then re-runs the skill.

If the user explicitly says "skip tests", honour that for `pytest` only and call it out loudly in the PR body under a `## Skipped checks` heading. **Pre-commit cannot be skipped** — if the user asks, refuse and point them at this section.

## Step 2b: Run /thermo-nuclear-code-quality-review (mandatory)

Invoke `/thermo-nuclear-code-quality-review` against the current diff. This is non-negotiable on every PR — do not skip it, even if the user asks, even on small diffs, even on diffs that "obviously" don't need it.

The skill returns a structured maintainability review. Capture its full report verbatim — you will paste it into the PR body in Step 4 under `## Thermo-nuclear review`.

If `/thermo-nuclear-code-quality-review` flags a **blocker**, open the PR as `--draft` regardless of whether the user passed the flag, and call out the blocker(s) at the top of the PR body.

## Step 3: Spawn deep-review subagents (in parallel)

These run *in addition to* `/thermo-nuclear-code-quality-review` from Step 2b — that pass covers maintainability and structural quality; these lenses cover correctness, security, performance, etc. Do not pick a lens that overlaps with thermo-nuclear (e.g., "maintainability" or "abstraction quality" — that's already covered).

Launch 1–2 subagents in parallel when the host supports them (Claude `Agent`, Codex multi-agent tools, or an equivalent local subagent mechanism). Use `subagent_type=general-purpose` (or `code-reviewer` if the host project defines one). Each agent gets the full diff path and a distinct lens — overlap is wasted budget. If no subagent mechanism is available, perform the two review passes yourself before composing the PR body.

Recommended lenses (pick the two most relevant to the diff):

- **Correctness & logic** — does the code do what the commits claim? Off-by-ones, error paths, race conditions, dropped exceptions, dead branches.
- **API / interface** — public-surface changes, breaking renames, missing deprecation paths, type-signature regressions.
- **Tests & coverage** — are the new code paths exercised? Are tests asserting behaviour or just running it? Any obviously missing edge cases?
- **Security & data handling** — secrets, injection, unsafe deserialisation, PII paths.
- **Performance** — hot-path allocations, quadratic loops introduced, large tensors materialised, blocking IO on async paths.

Prompt template for each subagent (self-contained — the agent has no conversation history):

> You are reviewing a pull request in `<repo path>`, branch `<head>` against `<base>`. The full diff is at `$JOB_DIR/pr.diff` and `git log "$BASE"..HEAD` shows the commits. Read the diff and the touched files in the repo. Focus only on `<lens>` — other reviewers cover the rest, don't duplicate them.
>
> Return findings as a short markdown list. Each finding: **severity** (blocker / should-fix / nit), `file:line`, one-sentence problem, one-sentence suggested fix. If you find nothing, say so explicitly — empty reports are valid. Cap the report at ~400 words.

Collect both reports. Don't paraphrase — paste them verbatim into the PR body under attributed headings.

## Step 4: Compose the PR body

Title: short (under 70 chars), imperative mood, derived from the commit log — not the branch name. Examples: "Add open-pr skill", "Fix race in monitor-jobs polling".

Body template (use a HEREDOC, see "Creating pull requests" in the system instructions):

```markdown
## Summary
- <1–3 bullets, the *why*, derived from commits + diff>

## Changes
- <file-group>: <what changed>
- ...

## Quality gates
- pre-commit: <pass | fail>   <!-- never "skipped"; mandatory -->
- pytest: <N passed, M failed | skipped — reason>
- thermo-nuclear review: <ran — N blockers, M should-fix, K nits>
- Ran on: <hostname / cluster / compute-node-job-id>

## Thermo-nuclear review
<verbatim report from /thermo-nuclear-code-quality-review>

## Reviewer notes — <lens A>
<verbatim subagent report A>

## Reviewer notes — <lens B>
<verbatim subagent report B>

## Test plan
- [ ] <concrete check the human reviewer should run>
- [ ] ...

Generated with the SoftNano plugin.
```

## Step 5: Push and open the PR

```bash
# Check whether the branch already has an upstream. Never re-point an existing
# upstream — in fork workflows that silently changes which remote subsequent
# pulls/pushes hit. `-u` *sets* upstream; only use it when none exists.
if git rev-parse --abbrev-ref --symbolic-full-name '@{u}' >/dev/null 2>&1; then
  git push                       # honour the existing upstream; abort on non-FF, don't force
else
  git push -u origin HEAD        # first push of this branch — set tracking to origin
fi

gh pr create --base <base-branch> [--draft] --title "<title>" --body "$(cat <<'EOF'
<rendered body>
EOF
)"
```

Use `--draft` if the user asked for one, if `/thermo-nuclear-code-quality-review` or any review subagent flagged a **blocker**, or if `pytest` was skipped.

Return the PR URL to the user. Do not also paste the body back — they can read it on GitHub.

## Notes

- **Never** force-push. Never run `git reset --hard`. If the local branch and remote have diverged, stop and ask the user.
- **Never** edit code to silence a hook or test failure as part of opening the PR — that is a separate fix the user must approve.
- If the diff is empty (`$BASE..HEAD` has no commits), refuse — there's nothing to PR.
- If the repo has a `PULL_REQUEST_TEMPLATE.md`, prefer its section ordering over the template above, but still inject the **Quality gates** and **Reviewer notes** sections.
- Keep subagent reports verbatim. Summarising them defeats the point of an independent review.
