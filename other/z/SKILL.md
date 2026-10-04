---
name: z
description: Quick status dashboard — what's happening, what needs attention, ready to close?
disable-model-invocation: false
---

# Z — Quick Status Dashboard

Fast pulse check. Run everything in parallel, report concisely. Target: under 30 seconds.

## Context to Gather

Run ALL of these in parallel:

```
Branch:              !`git branch --show-current`
Recent commits:      !`git log --oneline -5`
Git status:          !`git status --short`
Unpushed:            !`git log @{upstream}..HEAD --oneline 2>/dev/null || echo "no upstream"`
Dev server:          !`lsof -ti:3000 > /dev/null 2>&1 && echo "running on :3000" || echo "not running"`
Build dir:           !`test -d .next && echo "exists" || echo "missing"`
Research count:      !`ls research/ | wc -l`
Open PRs:            !`gh pr list --head $(git branch --show-current) --json number,state,title,url --jq '.[] | "#\(.number) \(.state) — \(.title)"' 2>/dev/null || echo "gh not available"`
Merged PRs:          !`gh pr list --head $(git branch --show-current) --state merged --json number,mergedAt --jq '.[] | "#\(.number) merged \(.mergedAt)"' 2>/dev/null || echo ""`
Branch merged:       !`git branch --merged origin/main 2>/dev/null | grep -q "$(git branch --show-current)" && echo "merged into main" || echo "not merged"`
Vercel status:       !`gh api repos/$(gh repo view --json nameWithOwner -q .nameWithOwner)/deployments --jq '.[0] | "\(.environment) \(.state) \(.created_at)"' 2>/dev/null || echo "unavailable"`
```

Then scan for TODOs — ONLY in files listed by `git status` (modified/staged files):

```
TODOs in changed files: !`git diff --name-only | xargs grep -n 'TODO\|FIXME\|HACK' 2>/dev/null || echo "none"`
```

## Output Format

Respond with EXACTLY this structure. Total output MUST be under 300 words.

```
## ZAO OS Status

**Branch:** {branch} | **Files changed:** {count from git status} | **Research docs:** {count}

### Recent (last 5 commits)
- {commit 1}
- {commit 2}
- ...

### Needs Attention
- {uncommitted files, if any — list file paths}
- {TODOs found in changed files, with file:line and comment text}
- Dev server: {running on :3000 / not running}
- {".next/ missing — run `npm run build`" if build dir missing, otherwise omit}

### Ready to Close?
- Uncommitted changes: {✓ clean / ✗ N files modified}
- Unpushed commits: {✓ synced / ✗ N commits ahead}
- Open PRs (this branch): {✓ #N merged / ✗ #N open — waiting for review / ✓ none}
- Vercel deploy: {✓ ready / ✗ building / ✗ failed / — unavailable}
- **Verdict: {✅ GOOD TO CLOSE / ⚠️ NOT YET — [list reasons]}**

### Quick Actions
- `/catchup` for full context restore
- `/standup` for build-in-public note
- `npm run build` to check for errors
```

## Verdict Logic

**✅ GOOD TO CLOSE** when ALL of these are true:
- No uncommitted changes (git status clean)
- No unpushed commits (synced with upstream)
- No open (unmerged) PRs from this branch, OR no PR was created
- Vercel deploy is "ready" or status unavailable (don't block on deploy check failures)

**⚠️ NOT YET** when ANY of these are true:
- Uncommitted changes exist → "uncommitted changes"
- Unpushed commits exist → "unpushed commits"  
- Open PR from this branch → "PR #N still open"
- Vercel deploy failed → "deploy failed"

List all failing reasons after the verdict.

If nothing needs attention (clean tree, no TODOs, server running), replace the Needs Attention bullet list with: "All clear."

## NOT YET → Offer to Fix

When the verdict is **⚠️ NOT YET**, use AskUserQuestion to offer to resolve the blockers.
Present lettered options based on what's actually blocking:

- **Uncommitted changes** → offer: "Commit changes and push" / "Stash changes for later" / "Discard unneeded files"
- **Unpushed commits** → offer: "Push now"
- **Open PR** → offer: "Merge PR #N" / "Leave it open — I'll review later"
- **Deploy failed** → offer: "Check Vercel logs"

Combine into a single AskUserQuestion with the relevant options. Example:

> You have uncommitted changes and an open PR. Want me to clean up before you close?
>
> A) Commit the skill updates + push (Recommended)
> B) Stash everything — I'll deal with it next session
> C) Just the PR — leave local changes alone
> D) I'll handle it manually

After the user picks, execute the chosen action. Then re-run the Ready to Close checks
to confirm the verdict flips to ✅ GOOD TO CLOSE.

If the verdict is already ✅ GOOD TO CLOSE, skip this step entirely.

## Rules

- The status report is read-only — NEVER modify files during the scan phase
- After the user chooses a fix action, you MAY execute git commands (commit, push, stash)
- MUST complete the scan in under 30 seconds — no deep file reading
- MUST be under 300 words for the status report (fix actions are separate)
- NO reading full file contents — only git commands, port checks, gh CLI, and quick scans
- Run git commands, port check, gh commands in parallel for speed
- Omit the build dir line from Needs Attention if .next/ exists
- Quick Actions section is always the same 3 bullets — do not change them
