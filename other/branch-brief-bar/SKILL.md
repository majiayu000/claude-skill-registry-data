---
name: branch-brief-bar
description: Turn the current git branch into a crisp review-ready brief with local status, touched areas, changed files, recent commits, and the next PR action.
---

# Branch Brief Bar

Use this skill when the user wants a local git-first handoff from terminal work into async review, standup notes, or PR updates without rebuilding branch context from a stack of commands.

Default product shapes:
- a compact menu-bar brief that surfaces branch health, touched areas, and the next action before you switch to GitHub or chat
- a deterministic local helper that renders the current branch as prompt, markdown, plain text, or JSON and can copy it to the clipboard

## Quick Start

1. Confirm whether the user wants a one-off brief, clipboard copy, or a real menu-bar utility surface.
2. Use `python skills/branch-brief-bar/scripts/branch_brief.py current --format prompt` for a concise review-ready summary from the current repo.
3. Use `python skills/branch-brief-bar/scripts/branch_brief.py current --format markdown --max-files 8` when the reviewer handoff should include a short changed-file preview with committed, staged, unstaged, or untracked state.
4. Use `python skills/branch-brief-bar/scripts/branch_brief.py copy --format markdown` when the next step is pasting the brief into chat, notes, or a PR.
5. By default the helper prefers a main-like review base such as `origin/HEAD`, `origin/main`, or `origin/trunk` when your upstream is only the same feature branch on the remote, so the brief stays PR-oriented instead of push-oriented.
6. Use `--base-ref origin/main` or another ref when the brief should compare against a specific branch instead of the default review-base heuristic.
7. Use `--repo /path/to/repo` when the current shell is not already inside the target checkout.
8. Use `--format json` when another agent or script needs structured status instead of prose.
9. Use the SwiftUI starter in `prototype/` when the user wants a real menu-bar shell instead of only a generated brief.

## Accepted Inputs

- the current repo in the working directory or an explicit `--repo` path
- an optional compare target such as `origin/main`, `main`, or another explicit ref
- desired output format: `prompt`, `markdown`, `plain`, or `json`
- how many recent commits to surface in the brief
- how many changed files to preview before the summary gets noisy
- whether the result should be printed or copied to the clipboard
- whether the user wants a one-off branch summary or a reusable macOS utility shell

## Workflow

### Keep the brief local and honest

- Read branch, upstream, ahead or behind state, working tree changes, and recent commits from local git only.
- Prefer an explicit `--base-ref` when the review target is known and should not be inferred.
- When the upstream already points at a different review branch such as `origin/main` or `origin/release/x`, use it directly.
- When the upstream is only the same feature branch on the remote, prefer `origin/HEAD`, `origin/main`, `main`, `origin/master`, `master`, `origin/trunk`, or `trunk` before falling back to the same-name upstream or `HEAD~1`.
- If there is no upstream, say so instead of guessing the PR target.
- If the folder is not a git repo, stop and explain the boundary rather than fabricating a branch summary.
- Treat GitHub, CI, and reviewer state as out of scope unless the user explicitly provides that context through another tool.

### Lead with handoff signal

- Show the branch name, upstream relation, dirty or staged counts, touched areas, status-aware changed-file previews, and recent commits before secondary details.
- End the brief with the next recommended action so the output is ready to paste into review or standup context.
- Use prompt or markdown mode when the output is heading into chat, docs, or a PR description.

### Keep the boundary narrow

- This is a branch relay, not a GitHub dashboard, CI monitor, or code review bot.
- Do not invent PR numbers, reviewers, merge status, or remote comments from local git alone.
- Keep the summary compact enough to scan in a menu-bar popover or copy into another app without editing.

## Local Helper

Use `scripts/branch_brief.py` when a deterministic local brief is useful:

```bash
python skills/branch-brief-bar/scripts/branch_brief.py current --format prompt
python skills/branch-brief-bar/scripts/branch_brief.py current --format markdown --max-commits 6
python skills/branch-brief-bar/scripts/branch_brief.py current --format markdown --max-files 8
python skills/branch-brief-bar/scripts/branch_brief.py current --format markdown --base-ref origin/main
python skills/branch-brief-bar/scripts/branch_brief.py copy --format markdown
python skills/branch-brief-bar/scripts/branch_brief.py current --repo /path/to/repo --format json --base-ref main
```

The helper reads local git state, derives upstream distance when available, summarizes touched areas, previews the most important changed files with local state labels, and lists recent commits against the chosen compare base. It surfaces why it picked that compare base, so the brief makes it obvious whether it is using an explicit ref, a main-like review branch, or a fallback. It renders prompt, markdown, plain-text, or JSON output and can also copy the rendered brief with `pbcopy`. It does not use network access or GitHub APIs.

If the user needs to understand or override the compare-base rule, read `references/review-base-behavior.md`.

## Prototype

- SwiftUI starter files live in `prototype/`.
- The prototype sketches a menu-bar shell with a branch snapshot card, a review-base-aware compare lane, a touched-area list, a status-aware changed-file preview, a commit strip, and one primary copy action.

## Example Prompts

- `Use $branch-brief-bar to summarize this repo's current branch as a prompt-ready review brief with upstream status, touched areas, recent commits, and the next action.`
- `Use $branch-brief-bar to build a compact macOS menu-bar utility that shows branch status, a handoff summary, and a one-click copy brief action.`
- `Use $branch-brief-bar to keep the handoff local and git-first; do not invent GitHub or CI state.`

## Resources

- `references/review-base-behavior.md`: compact explanation of the compare-base selection order and when to pin `--base-ref`
- `scripts/branch_brief.py`: local git status summarizer for prompt, markdown, plain-text, or JSON branch briefs with a changed-file preview
- `prototype/`: menu-bar-first SwiftUI starter for a compact branch handoff utility

## When extending

- Add more depth only when it improves the branch handoff itself.
- If the skill grows, keep the menu-bar path short and the reviewer brief readable at a glance.
