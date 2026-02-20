---
name: esper:continue
description: Resume an interrupted build. Reads the active plan, assesses what is done vs remaining from git history, and picks up where the last session left off.
---

You are resuming an interrupted implementation session.

## Step 1: Check setup

Run `esperkit config check`. If it exits non-zero, tell the user to run `/esper:init` first and stop.

Run `esperkit plan list --dir active --format json` to get active plans. Count the entries:
- **None found**: Tell the user "No active plan to continue. Run `/esper:apply` to start a new plan." and stop.
- **Multiple found**: Tell the user there are multiple active plans (shouldn't happen) and list them. Ask which one to work on, or suggest cleaning up manually. Stop until resolved.
- **Exactly one found**: Continue — this is the plan to resume.

The JSON output includes the frontmatter fields (`id`, `title`, `type`, `branch`, `phase`). Also read the active plan file's full content from `.esper/plans/active/<filename>` for all sections.

## Step 2: Assess current state

Run `git branch --show-current` to see the current branch.

If the current branch does not match the plan's `branch:` field:
- Print a warning: "Warning: you are on branch `<current>` but the plan expects `<plan branch>`. Switch branches before continuing."
- Use `AskUserQuestion` to ask: "Switch to the correct branch now, or continue on the current branch anyway?"
  - **Switch**: run `git checkout <plan branch>` and proceed
  - **Continue anyway**: proceed on the current branch (user accepts the discrepancy)

Run `git status --porcelain` to see uncommitted changes.

Run `git log --oneline -10` to see recent commits.

Read the plan's `## Approach` section and `## Files to change` section.

Read the plan's `## Progress` section (if it exists) to see what was recorded as done in prior sessions.

Cross-reference:
- Which Approach steps have corresponding files in `git status` (modified/new) or recent commits?
- Which files listed in `## Files to change` already exist and have been modified?

Summarize what appears done and what appears remaining.

## Step 3: Report and confirm

Show the user:
```
Resuming plan #<id> — <title>

Branch: <branch>
Uncommitted changes: <N files, or "none">

What appears done:
  ✓ <step or file that looks complete>
  ✓ ...

What appears remaining:
  · <step or file not yet started>
  · ...
```

Use `AskUserQuestion` to ask: "Does this assessment look right? Proceed with the remaining steps?"
- **Yes, proceed**: continue to Step 4
- **No, I'll guide you**: ask the user to describe what's actually done and what remains, then proceed accordingly

## Step 4: Continue implementation

Resume from the remaining Approach steps. Follow the same rules as `/esper:apply`:
- Read each file before modifying it
- Follow existing code patterns
- Do not add features beyond what the plan describes
- Update `## Approach` or `## Files to change` in the plan file if something unexpected is found

After each logical group of steps is complete, commit:
```bash
git add <specific files>
git commit -m "$(cat <<'EOF'
<feat|fix|chore>: <what was just done>

Plan: #<id> — <title>
EOF
)"
```

## Step 5: Verification

Run verification steps from the plan's **Verification** section.

Run `esperkit config get commands` to get the commands object as JSON. For each of `test`, `lint`, `typecheck`:
- Skip if empty or missing
- Run if non-empty; capture exit code

If all commands are empty, print: "No verification commands configured — skipping." and continue.

If any non-empty command fails, stop and report the failure. Do NOT proceed until fixed.

## Step 6: Update Progress section

Add or update the `## Progress` section in the active plan file:

```markdown
## Progress
- Resumed from: [what was already done per prior session]
- Completed in this session: [what was done now]
- Modified: [list of files changed]
- Verification: [passed / failed with details]
```

## Step 7: Wrap up

Print a summary of what was completed in this session.

If the plan's Approach is fully implemented and verification passed:
- Print: "Implementation complete. Run `/esper:finish` to verify, commit, and archive this plan. Then `/esper:ship` to push and open a PR."

If there is still work remaining (you stopped early):
- Print: "Partial progress committed. Run `/esper:continue` again to resume."
