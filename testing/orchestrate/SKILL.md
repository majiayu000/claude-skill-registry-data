---
name: orchestrate
description: End-to-end feature workflow - branch, implement, improve, PR, wait, pr-fix
argument-hint: <feature description>
---

# Orchestrate Feature

Full end-to-end pipeline: sync the base branch, cut a new working branch, implement the feature, run improve cycles, open a PR, then auto-fix CI once its checks finish.

## Arguments

- `$ARGUMENTS` - Feature, fix, or chore description. This doubles as the branch name source and the input to the implementation step.

## Step 1: Detect Base Branch and Sync

The base branch is NOT always `main`. Ask GitHub for the repo's configured default branch, falling back to the local `origin/HEAD` symref when `gh` is not authenticated or the repo has no remote on GitHub:

```bash
BASE_BRANCH=$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name 2>/dev/null || git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')
echo "BASE_BRANCH=$BASE_BRANCH"
```

If it prints an empty name, STOP and ask the user which branch to base the work on — do NOT guess. Otherwise record the printed name as `BASE_BRANCH` and write it in place of `<BASE_BRANCH>` from here on: the Bash tool keeps no variables between calls.

Sync the base branch:

```bash
git fetch origin
git checkout <BASE_BRANCH>
git pull --ff-only origin <BASE_BRANCH>
```

If the working tree is dirty when this runs, STOP and ask the user how to proceed (do NOT stash or discard their changes).

## Step 2: Create Feature Branch

Derive a slug from `$ARGUMENTS`:
- lowercase
- spaces and non-alphanumeric characters → `-`
- trim leading/trailing `-`
- truncate to ~50 chars

Prefix based on intent parsed from `$ARGUMENTS`:
- `fix/` for bug fixes
- `feat/` for features
- `refactor/` for refactors
- `chore/` for maintenance
- `docs/` for docs

Create the branch, replacing `feat/` with the chosen prefix:

```bash
SLUG=<computed slug>
BRANCH="feat/$SLUG"
git checkout -b "$BRANCH"
```

## Step 3: Assess Complexity

Based on `$ARGUMENTS` and a quick scan of the affected areas, classify the work into ONE of these buckets and record the cycle count:

| Complexity | Signals | Cycles |
|---|---|---|
| Small fix | One-line/trivial bug fix, typo, copy change, single file | 1 |
| Small feature | New small endpoint, isolated utility, simple UI component | 2 |
| Medium feature | Multi-file change, touches a domain, new integration | 3 |
| Big feature | Cross-cutting, new subsystem, migrations, API changes, many files | 4 |
| Huge feature | Architecture-level, multiple domains, data model changes | 5 |

If the description is ambiguous, pick the HIGHER bucket - extra review cycles are cheaper than missed issues.

Record the choice as `CYCLES=N` and state the rationale in one sentence before proceeding.

## Step 4: Implement the Feature

Invoke the **consolidation** skill, which loads the full orchestration cycle (planner → verifier → parallel architects → consolidator → reviewer → verifier) into your context. You become the conductor and dispatch each stage:

```
Skill(skill="skills:consolidation", args="## Task\n$ARGUMENTS\n\n## Constraints\n- TDD where project has tests\n- Follow project conventions\n- Commit logically-grouped changes\n- No TODOs, no placeholders\n\n## Working directory\n[cwd]")
```

This replaces the old pattern of a single architect + separate improve cycles. The skill runs in *your* context: you conduct it (the consolidation skill decides whether to delegate workstreams to `conductor` subagents).

After the cycle finishes, verify:
```bash
git status
git log --oneline origin/<BASE_BRANCH>..HEAD
```

If the working tree is dirty (uncommitted changes), commit them before moving on.

## Step 5: Run improve (optional additional cycles)

If the complexity assessment calls for additional review cycles beyond what the consolidation cycle performed, invoke improve:

```
Skill(skill="skills:improve", args="<CYCLES - 1>")
```

For most tasks the consolidation skill's built-in reviewer + verifier cycle is sufficient. Only run additional improve cycles for Big/Huge features.

## Step 6: Run pr

Invoke the `skills:pr` command to commit anything still pending, push, and open the PR:

```
Skill(skill="skills:pr")
```

**Capture the PR URL from the skill's output.** Store it as `PR_URL`. If the skill output does not include a URL, run `gh pr view --json url -q .url` on the current branch to fetch it.

## Step 7: Wait for CI

CI needs time to start and report results. Wait for the checks on the pushed head to finish before running pr-fix:

```bash
if [ -z "${PR_URL:-}" ] || [ -z "${REPO:-}" ]; then echo 'set PR_URL and REPO first'; exit 2; fi
HEAD_SHA=$(git -C "$REPO" rev-parse HEAD) || exit 2
PREVIOUS_COUNT=0
for _ in $(seq 1 30); do
  PR_HEAD=$(gh pr view "$PR_URL" --json headRefOid --jq .headRefOid)
  CHECK_COUNT=0
  if [ "$PR_HEAD" = "$HEAD_SHA" ]; then
    CHECK_COUNT=$(gh pr checks "$PR_URL" --json name --jq length 2>/dev/null || echo 0)
  fi
  if [ "$CHECK_COUNT" -gt 0 ] && [ "$CHECK_COUNT" = "$PREVIOUS_COUNT" ]; then break; fi
  PREVIOUS_COUNT=$CHECK_COUNT
  sleep 10
done
if [ "$CHECK_COUNT" -gt 0 ]; then
  exec gh pr checks "$PR_URL" --watch --fail-fast --interval 30
fi
if [ "$PR_HEAD" != "$HEAD_SHA" ]; then
  echo "PR head ${PR_HEAD:-unknown} never matched local HEAD $HEAD_SHA"
  exit 4
fi
echo "No CI checks registered for $HEAD_SHA after 5 minutes"
exit 3
```

Run the block in one Bash call with `run_in_background: true`, with the PR URL and the checkout's absolute path assigned on the line before it, for example `PR_URL=https://github.com/owner/repo/pull/123 REPO=/Users/me/Local/repo`. Both values are required because the Bash tool keeps no variables between calls and a subagent's cwd resets.

Exit codes: 0 means all checks passed; 1 means a check failed (`--fail-fast`) or `gh` failed during the watch; 3 means no checks registered within 5 minutes (the repo may have no CI); 4 means the PR head never matched the local HEAD: push, or fix the `gh pr view` error it printed, and run again; any other non-zero means the block could not start (unset `PR_URL` or `REPO`, or a path that is not a checkout): fix it and run again. Monitor is the alternative when per-check events are wanted.

Do NOT skip this wait - running pr-fix immediately races CI and sees no failures to fix.

While waiting, you may summarize progress to the user, but do not start new work that modifies the branch.

## Step 8: Run pr-fix

Invoke the `skills:pr-fix` command with the captured PR URL and both flags enabled:

```
Skill(skill="skills:pr-fix", args="$PR_URL checks=true comments=true")
```

If Step 7 exited 3 (no CI), pass `checks=false comments=true` instead. This will iterate on failing checks and address any review comments already posted.

## Step 9: Final Report

After pr-fix completes, report:

```
## Orchestrate Summary

- **Feature:** <description>
- **Base branch:** <BASE_BRANCH>
- **Feature branch:** <BRANCH>
- **Complexity:** <bucket> (<CYCLES> review cycles)
- **PR:** <PR_URL>
- **Review cycles run:** <CYCLES>
- **PR-fix iterations:** <count from pr-fix>
- **Final CI state:** <pass/fail>
```

## Hard Rules

1. **DO NOT STOP MID-WORKFLOW** - Run all steps through to pr-fix completion unless a hard blocker appears.
2. **DO NOT RUN pr-fix BEFORE CI FINISHES** - pr-fix is useless without CI results to analyze.
3. **DO NOT DESTROY USER WORK** - If the working tree is dirty at Step 1, stop and ask.
4. **DO NOT GUESS THE BASE BRANCH** - Use the detection logic; ask if it fails.
5. **ROUND COMPLEXITY UP, NOT DOWN** - Extra review cycles are cheap insurance.
6. **USE THE Skill TOOL FOR SUB-SKILLS** - Do not inline improve / pr / pr-fix logic; call them so their own updates are automatically picked up.
