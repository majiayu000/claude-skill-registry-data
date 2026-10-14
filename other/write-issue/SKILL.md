---
name: write-issue
description: File, groom (rewrite for pickup), or close a DeltaTrack GitHub issue. Use when creating an issue, rewriting an issue body so a newcomer can start on it, or closing/merging an issue.
---

# Writing a DeltaTrack issue

The rules live in the repo docs, so humans and agents follow the same ones. Read the
section for the job before writing:

| Job | Read |
|---|---|
| Filing a new issue | CONTRIBUTING.md "Filing an issue", "Filing from the command line", "Writing an issue others can read"; then the matching `.github/ISSUE_TEMPLATE/*.md`, or the skeleton in `docs/issue-analysis-template.md` for a defect you've analyzed |
| Grooming (rewriting for pickup) | `docs/issue-analysis-template.md` "Grooming: rewriting an issue for pickup"; CONTRIBUTING.md "Grooming an issue for pickup" |
| Closing or merging | `docs/issue-analysis-template.md` "Closing or merging an issue" |

The reader is a new team member without deep familiarity. Define project terms
inline, and make every `#n` self-describing.

## Workflow

1. **Search first.** Look for an open issue that already covers it; comment or extend
   that one instead of filing a duplicate.
2. **Verify on current `develop`.** Reproduce anything you state as current and stamp
   it with the date and short sha. If you didn't run it, don't state the number as
   current; put it under **Unverified**.
3. **Before attributing behaviour to an open PR, check its merge base** (or do a trial
   merge onto `develop` in a scratch worktree). Old branches differ from `develop` for
   reasons the PR didn't cause.
4. **Write the body** in the doc's shape. Keep every finding and decision from an old
   body when rewriting. Don't put priority or effort in the body.
5. **File with the type set.** `gh issue create --body-file` skips the templates and
   their `type:`; pass `--type Bug|Feature|Task` (epics stay untyped, with the `epic`
   label). Set the org-level **Priority** field only when grooming, not when filing.
6. **Close with a comment and a state reason** (`completed`, `not_planned`, or
   duplicate of the absorbing issue), and carry regression cases into the surviving
   issue on a merge.

Keep scratch files outside the repo checkout, and remove any worktree you add.
