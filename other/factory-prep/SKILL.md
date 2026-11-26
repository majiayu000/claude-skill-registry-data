---
name: factory-prep
description: Make a Linear ticket ready to build when it moves into Todo or In Progress. An independent agent checks the ticket's assumptions against the code, writes the state model and a commit-pinned code map into the working doc, and returns a verdict (Ready, Split, Blocked, Needs decision) so open questions get answered before the work session starts.
argument-hint: "[issue-id | sweep] (issue auto-detected from branch; sweep = every Todo / In Progress ticket without a current prep)"
---

# Factory prep

Prep turns a ticket from an idea into work that's safe to start. Its job is not documentation. It answers the ticket's open questions while the ticket waits, so the work session opens on a checked foundation and the operator's decisions are already made.

**When it runs:** when a ticket enters **Todo** or **In Progress**. Backlog stays cheap; a ticket nobody has committed to gets no review.

- `sweep` (no issue): list the team's Todo and In Progress tickets (scoped to `projectId` if set) and prep each one that has no `## Prep` section or whose prep is stale. Run it at cycle planning, or when `factory-standup.md` reports unprepped tickets. Answer every ticket's **Needs you** in one pass from the `Needs decision` view.
- `<issue-id>`: prep one ticket.
- `factory-entry.md` runs prep itself when the ticket has no current prep, then moves it to In Progress.

Linear doesn't notify the agent when an operator drags a ticket to Todo. Until a scheduled `sweep` is wired up, the sweep and entry are the triggers.

## Configuration

`.factory-kit/linear.json` (legacy `.claude/linear.json` as fallback): `states.todo` and `states.inProgress` name the trigger states (defaults `"Todo"`, `"In Progress"`). Agent-state labels and the working doc follow `factory-log.md`.

## What to do

1. **Load the ticket**: description, comments, parent, sub-issues, relations, and the working doc if one exists.

2. **Skip or refresh.** If the doc has a `## Prep` section, check its stamp (`read at <short-sha> · <timestamp>`) against both inputs to the verdict:
   - **Ticket inputs:** the title or description edited, operator replies posted, or any parent, sub-issue or blocking issue changed state since the timestamp. Any of these makes the prep stale as a whole: re-run steps 3–4 so the assumptions and the verdict are judged again. A cached **Blocked** or **Split** must not outlive the condition that caused it.
   - **Code inputs:** files cited in `## Prep` or `## Codebase` changed between the `read at` commit and HEAD on the default branch. If only these moved, re-check the assumptions and map lines on those files, record what moved in `## Findings`, and re-derive the verdict.

   If neither moved, the prep is current: stop and print the one-line output.

3. **Review the code independently.** Run the review as a read-only subagent when the host has one. Give it the ticket and the repo, not the creator's conclusions: its value is the read the ticket's author couldn't do on their own work. It returns:
   - **Assumptions**: every claim the ticket makes or quietly depends on ("this endpoint exists", "status is only set here", "nothing else reads this field"), each marked `✓` confirmed, `✗` refuted, or `?` unsettled, with the `file:line` that settles it.
   - **Code map**: entry points, how the flow works today, constraints (invariants, prior decisions, callers that lock the shape), and blast radius. One line each, `file:line` first.
   - **State model**: current → target, per `factory-state-modeling.md`. A change with no state (copy, config, dependency bump) gets one line saying so.

4. **Reach a verdict.** Exactly one:
   - **Ready**: every assumption holds or doesn't matter; the work fits one session.
   - **Split**: the work spans more than one reviewable change. Propose sub-issues, one line each, titled per `factory-voice.md`.
   - **Blocked**: it depends on work that isn't done. Name the issues, or the missing thing if no issue exists yet.
   - **Needs decision**: a `✗` or `?` changes the scope or the contract, and only the operator can call it.
   - **Shipped**: the outcome the ticket asks for is already on the default branch. Cite the commit that shipped it (short SHA, plus the PR if known) and the `file:line` that proves it. Partially shipped is not Shipped: that's Needs decision (close, or rescope to the remainder).
   - **Duplicate**: another open or done ticket covers the same outcome. Cite it. Overlap alone is not a duplicate; the other ticket must make this one unnecessary.

   `Shipped` and `Duplicate` are claims someone else will act on, possibly by closing the ticket automatically (`factory-autopilot.md`), so the evidence must be checkable, not a paraphrase.

5. **Write the working doc** (create it per `factory-log.md` if absent):
   - `## Prep`: `**Verdict:** <verdict> · read at <short-sha> · <ISO timestamp>`, then `**Assumptions:**` as one line each, then the proposed split or the blockers if any. At most 12 lines.
   - `## Codebase`: the code map. At most 12 lines. It's a cache pinned to the `read at` commit; entry refreshes it by diff.
   - `## State model`: on first prep, write it. Once the ticket has a `## Plan`, the target model is the reviewed contract from `factory-entry.md`: never replace it. If the refresh shows the current state moved or the target no longer fits, add one line to `## Findings` and a **Needs you** item proposing the exact change (`reply <n> go`); edit the section only after `go`, via `factory-log resolve`.
   - **Now block**: each `✗` or `?` that needs the operator, each proposed split (`reply <n> go`), and each proposed blocking relation (`reply <n> go`) becomes a **Needs you** item. Replace only the items an earlier prep added; leave every other item in place and number the new ones after them.
     - **First prep** (no `## Plan` yet, no agent label): the status line is `**Now:** prepped: <verdict>, not started`. Label `Needs decision` if anything is owed, otherwise none.
     - **Refresh of a ticket already in work**: keep the `**Now:**` status line as it is and add the verdict to it only if it changed (e.g. `… · prep: now Blocked`). Derive the label from the combined block per `factory-log.md` § Agent state, so `Working` and `Blocked` stay unless the combined state calls for something else.

6. **Don't touch the issue itself.** The description, sub-issues and relations stay the operator's until they reply `go`. Then create exactly what was proposed and record it in `## Decisions` via `factory-log resolve`.

7. **Write no plan.** Planning happens at entry, on this foundation.

## Output

One line per ticket:

```
KAI-329 · prep: Split (3) · needs you: 1 item → <doc link>
```

## Rules

- **Read-only on code.** Prep never edits the repo, creates branches, or runs migrations.
- **Assumptions are the core.** A prep with a code map and no assumption check has missed the point. Every `✗` must change the verdict, a **Needs you** item, or the state model; otherwise it wasn't load-bearing and doesn't belong.
- **No sensitive data.** Cite paths, symbols and test names only; Linear is an external service.
- Follow `factory-voice.md` and the budgets in `factory-log.md`.

## Related

- `factory-log.md`: the working doc, Now block, labels and `resolve`.
- `factory-entry.md`: runs prep if missing or stale, then plans on top of it.
- `factory-state-modeling.md`: the state model recipe.
- `factory-standup.md`: flags Todo and In Progress tickets without a current prep.
