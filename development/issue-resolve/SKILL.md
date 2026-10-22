---
name: issue-resolve
description: >-
  Takes one triaged tracker issue to a fix by the right route: `quick-fix` for something
  small, the `feature-*` pipeline for anything bigger. Drafts the tracker resolution once
  the fix lands. Use once you've decided to act on a triaged issue.
user-invocable: true
argument-hint: <issue ID> [notes on how you want it fixed, optional]
---

# issue-resolve

Bridges a triaged issue into an actual fix, using the mechanisms this plugin already has —
it doesn't write the fix itself. `quick-fix` handles something small; the full pipeline
handles anything bigger. Once the fix lands, this closes the loop back on the tracker as a
draft, never a live action.

## Scope

- IN: pull the issue and its triage read, route to the right existing fix mechanism, seed it
  with the issue's content and your notes, draft the tracker resolution once the fix lands.
- OUT: writing the fix itself (that's `quick-fix`'s inline edit, or the pipeline's `builder`),
  reclassifying an issue that's already triaged, posting or closing anything on the tracker
  without your say-so.

## Preflight

1. Resolve the tracker the same way `issue-triage` does — read `CLAUDE.md`'s `## Issue
   tracker` section. If it's missing, nothing's been triaged yet either; send the user to
   `issue-triage` first rather than re-running that interview here.
2. Resolve the issue ID from the argument. If more than one ID is given, stop — this skill
   resolves one issue at a time. A fix touches code and git history, and running several at
   once against the same working tree is exactly the kind of collision worktrees exist to
   prevent; unlike triage, this isn't a fan-out job.
3. Get a triage read, never moving straight to fixing an issue nobody's actually read:
   - This session already has an `issue-triage` report for it → use that.
   - The issue has no state label (see `issue-triage`'s State labels) → invoke `issue-triage`
     (Skill tool) for that one issue first.
   - It has a state label but this session has no report → dispatch one `issue-triager`
     subagent for a fresh read, with the inputs `issue-triage`'s Dispatch section lists.
     Don't change its labels.
4. **A security flag stops everything here.** If the triage read says `security: true`,
   stop and follow `issue-triage`'s Security reports section.
5. **A linked open PR stops the build route.** If the triage read, or a fresh check, shows an
   open PR from the reporter or another outside contributor already attached to the issue,
   don't route to a fix lane below — the fix is already written, not something to build. Hand
   off to `pr-review` with that PR number instead and stop.
6. A `state/needs-info` issue isn't ready. Say what's missing and stop, unless the user's
   notes supply it. Likewise a `state/needs-decision` issue, unless the notes give the
   maintainer's yes, and a `state/blocked` issue, unless the notes ask for a workaround.
7. Capture any notes given in the argument — how the user wants it fixed, constraints,
   anything the triage didn't know. These get folded into whichever lane runs next; they don't
   replace it.

## Routing

Use the triage's own read of size (`recommended action`, `likely area`) as the starting call,
but the real judgment stays where it already lives:

- **Cause unknown** — a `state/needs-investigation` issue, whatever the user's notes say, or
  any bug where neither the triage nor the user's notes say what's causing it → invoke
  `investigate-bug` (Skill tool) with the issue first. It hands back its report, a drafted
  issue update, and a suggested route.
  - **Cause proven:** take its route as the starting call below, and pass the report on as
    the lane's starting material. Its drafted notes go into the `state/in-progress` comment
    below, so the reporter gets one comment, not two.
  - **No proven cause:** no lane starts. Show its drafted update, apply it only on the
    user's yes, and stop.

- **Already fixed on another version line** — the cause is proven and a merged commit or PR
  on another line of the package already fixes it → invoke `change-backport` (Skill tool) with that
  commit or PR and the issue's line as the target.
- **Looks small** — a single concern, the kind `quick-fix`'s own scope section describes →
  invoke `quick-fix` (Skill tool) with a description built from the issue's title/body, the
  triage's likely-area finding, the repro, and the user's notes. `quick-fix` still makes its own
  escalation call if the fix turns out bigger once someone's actually in the code; this skill
  doesn't override that.
- **Looks bigger, or `quick-fix` escalates** → invoke `feature-explore` (Skill tool) with the
  issue as its starting material: the issue's title and body, the triage's findings, the
  repro, and the user's notes as constraints or success criteria. `feature-explore` owns `BRIEF.md`, so it writes
  the brief from that and only asks about what's still missing. From there the normal pipeline
  runs: `feature-explore` → `feature-design` → `feature-plan` → `feature-build`.

Either way, this skill hands off and waits — it does not write the fix itself. When a lane
starts, propose moving the issue to `state/in-progress` with a comment, following
`issue-triage`'s Tracker comments section. Apply both only on the user's yes.

Either way, give the lane the bug's repro, as the check the fix must pass: from
`investigate-bug`'s report if it ran, or else from the issue's latest `Notes for the fix`.
If the issue is a bug and neither has one, say so, and let the lane write one before it
changes code (`quick-fix` does this in its own loop).

Either way, ask the lane to fix the cause, not just the reported spot. A reported bug often has
siblings with the same cause (other endpoints missing the same check, other components with
the same pattern), especially when the same kind of bug has been reported before. `quick-fix`
searches for them in its own loop. For the pipeline route, include "find other places with
the same cause" in what you hand `feature-explore`, so the brief can bring them into scope or
list them as follow-ups.

## Closing the loop

Once the fix is committed — right after commit for `quick-fix`, or once `feature-build`
finishes and the PR is open for the pipeline route:

1. Check the lane reported the repro passing through the real entry point. If it didn't, run
   it now, as `feature-build`'s "Smoke the real entry point" step describes. Don't draft the
   resolution until it passes, unless the user accepts it as not verified end to end; then
   say that in the comment's notes.

2. If the tracker is GitHub Issues in the same repo as the code, `git-workflow`'s `Closes
   #123` convention (in the commit/PR body) already closes it on merge. Confirm the reference
   made it in, and still draft the "Fix landed" comment from `issue-triage`'s Tracker
   comments section, so the reporter hears what changed, not just a close.
3. Otherwise — a separate tracker, or a different repo than the source — draft a resolution
   comment following `issue-triage`'s Tracker comments section: what changed for the
   reporter, in their terms, and a link to the commit or PR. Propose a status (resolved/fixed,
   pending release, needs the reporter to confirm) using whatever states that tracker actually
   has; don't invent one it doesn't support.
4. Show the draft to the user. Only post the comment or change the status if they say to —
   same rule as `issue-triage`: a draft is the default output, posting is a separate, explicit
   step.
5. **Find every follow-up.** Gather each follow-up mentioned anywhere: the lane's hand-off,
   review findings left out of scope, the PR description, places with the same cause, and
   the chat. List them and ask where each one goes: a new issue (drafted with
   `git-workflow`'s issue template), its own PR, or dropped. Never leave one only in a PR
   description or the chat; it's lost when the chat ends. Name each filed one in the "Fix
   landed" notes' **Left out** field.
6. **Other version lines.** If `CLAUDE.md` lists more than one supported version line and
   the bug exists on another line still in an active phase, offer `change-backport` with
   the fix's commit or PR.

## Rules

- One issue per run. No fan-out, no subagent batch — this writes code, indirectly, via the
  mechanisms it calls, and that only happens on one working tree at a time.
- Never post a tracker comment or change its status without explicit confirmation.
- Don't change an issue's state label except to `state/in-progress`, and only on the user's
  yes.

## Hand off

Report which lane it took (`quick-fix`, the pipeline, or `pr-review` for a linked PR) and why,
then whatever that lane's own hand-off says. Once code is committed, report the draft tracker
resolution and wait for confirmation before posting it.

- **If another skill started this one** (such as `issue-backlog`'s fix stage), return once the
  lane finishes or hands off, and stop. That skill decides what runs next.

- **If another skill started this one**, return once the resolution is posted or declined,
  and stop. That skill decides what runs next.
