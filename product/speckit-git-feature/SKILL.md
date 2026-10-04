---
name: speckit-git-feature
description: Create a feature branch + worktree and a linked GitHub issue numbered
  to match the spec
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: git:commands/speckit.git.feature.md
---

# Create Feature Branch

Create and switch to a new git feature branch for the given specification, materialise its dedicated worktree, and open a tracking GitHub issue whose number drives the spec/branch numbering. This command handles **branch + worktree + tracking-issue creation** — the spec directory and files are created by the core `/speckit-specify` workflow.

## GitHub Issue Integration (Required)

`gh` **MUST** be installed and authenticated for this command to run. If `gh` is missing or `gh auth status` fails, the script errors out and creates nothing — there is no silent fallback.

When numbering is sequential, the script:

1. Creates a stub GitHub issue *before* numbering the branch.
2. Uses the issue number as `FEATURE_NUM` so the spec dir, branch, and issue all share the same identifier (e.g. `specs/008-user-auth/`, branch `008-user-auth`, issue `#8`).
3. After the branch + worktree are materialised, prefixes the issue title with `NNN: ` and writes `source_issue` into the new worktree's `.specify/feature.json` so `/speckit-git-pr`, `/speckit-git-commit`, `/speckit-archive-feature`, and `/speckit-git-clean` automatically pick up the linked issue. That is the file's only field and it is gitignored. When a run creates no issue, an *inherited* (still-tracked) file is removed so the previous feature's issue can't leak forward, while a file this worktree already owns is preserved — so re-running against an existing branch keeps its linkage. Everything else about the feature is derived from git at read time (issue #33).

If the issue's number ends up below the next free spec number (e.g. issue #5 created while `specs/008-*` already exists), the branch is still numbered using the next free spec number and the issue title is updated to match — so the alignment stays visible.

The issue body is intentionally a stub; `/speckit-git-issue` fills it in with the rendered spec content because `source_issue` is already set. That command runs automatically on the `after_specify` hook, so the stub is replaced as soon as the spec exists — no preset required.

The stub is also left **unlabelled** on purpose. Priority (`p0`..`p3`) and kind (`bug`/`feature`) are set by `/speckit-git-issue` on that same hook, once there is a spec to judge them from — this command only knows the one-line description, which is not enough to ask a human a useful question about. Those labels are what orders `/speckit-autopilot-run`'s backlog.

Issue creation is bypassed (and numbering falls back to the normal sequential / timestamp logic) only when the caller has explicitly opted out of issue-driven numbering:
- `--timestamp`, `--number`, or `GIT_BRANCH_NAME` is in effect
- `--source-issue N` is passed (see below)
- `--dry-run` is set

In every other case `gh` is mandatory: a missing binary, an unauthenticated session, or a failing `gh issue create` is a hard error.

## Binding to an issue that already exists: `--source-issue N`

Pass `--source-issue N` when the tracking issue was filed by a human (or by another
tool) and this run must bind to it rather than open a duplicate. The script then:

- skips `gh issue create` entirely,
- writes `{"source_issue": N}` into the new worktree's gitignored `.specify/feature.json` itself,
- numbers the branch from `N` (subject to the same next-free-slot guard) unless
  `GIT_BRANCH_NAME`, `--number`, or `--timestamp` already fixes the name,
- leaves the issue **title alone** — the `NNN: ` prefix is only applied to stub
  issues this script created, never to a pre-existing one.

This exists so a caller binding an existing issue never has to post-patch
`.specify/feature.json` in a second step. Under `GIT_BRANCH_NAME` alone the script
has no issue number, so it removes the inherited file and leaves the worktree
unlinked; every such caller previously had to write the linkage back itself, and
forgetting to left downstream commands pointed at the previous feature's issue
(issue #44).

```bash
GIT_BRANCH_NAME="090-automatic-arrival" \
  .specify/extensions/git/scripts/bash/create-new-feature.sh \
    --json --source-issue 90 --short-name "automatic-arrival" "Automatic arrival detection"
```

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Environment Variable Override

If the user explicitly provided `GIT_BRANCH_NAME` (e.g., via environment variable, argument, or in their request), pass it through to the script by setting the `GIT_BRANCH_NAME` environment variable before invoking the script. When `GIT_BRANCH_NAME` is set:
- The script uses the exact value as the branch name, bypassing all prefix/suffix generation
- `--short-name`, `--number`, and `--timestamp` flags are ignored
- `FEATURE_NUM` is extracted from the name if it starts with a numeric prefix, otherwise set to the full branch name

## Execution

Generate a concise short name (2-4 words) for the branch — this is the **only** non-deterministic step you perform:
- Analyze the feature description and extract the most meaningful keywords
- Use action-noun format when possible (e.g., "add-user-auth", "fix-payment-bug")
- Preserve technical terms and acronyms (OAuth2, API, JWT, etc.)

Then run the script exactly once, passing the short name and the feature description:

- **Bash**: `.specify/extensions/git/scripts/bash/create-new-feature.sh --json --short-name "<short-name>" "<feature description>"`
- **PowerShell**: `.specify/extensions/git/scripts/powershell/create-new-feature.ps1 -Json -ShortName "<short-name>" "<feature description>"`

Everything deterministic is handled by the script:
- Detecting whether the working directory is a git repo (warns and skips branch creation if not)
- Reading `branch_numbering` from `.specify/extensions/git/git-config.yml` (falling back to `.specify/init-options.json`, then to `sequential`) — pass `--timestamp` **only** if the user explicitly asked for timestamp numbering for this single invocation
- Creating the tracking GitHub issue and reconciling its number against the next free spec/branch slot
- Materialising the worktree and writing (or removing) the gitignored `.specify/feature.json`

**IMPORTANT**:
- Do NOT pass `--number` — the script determines the correct next number automatically
- Always include the JSON flag (`--json` for Bash, `-Json` for PowerShell) so the output can be parsed reliably
- You must only ever run this script once per feature
- The JSON output will contain `BRANCH_NAME` and `FEATURE_NUM` (and `SOURCE_ISSUE` / `ISSUE_URL` when an issue was created)

## Output

The script outputs JSON with:
- `BRANCH_NAME`: The branch name (e.g., `003-user-auth` or `20260319-143022-user-auth`)
- `FEATURE_NUM`: The numeric or timestamp prefix used
- `WORKTREE_PATH`: The absolute path of the materialised feature worktree
- `SOURCE_ISSUE` (when an issue was created): The numeric GitHub issue id (also the sole contents of the worktree's `.specify/feature.json`)
- `ISSUE_URL` (when an issue was created): The full URL of the tracking issue