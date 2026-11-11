---
name: planning
description: How Jason plans work. Work out what he wants with options and a recommendation, write it down as a spec or design doc with a numbered decision log, break it into small shippable tasks, and file them as Linear issues someone can pick up cold. Use when planning a feature, project, refactor or roadmap; writing a spec, design doc or plan; recording or changing a decision; breaking work into tasks or milestones; or writing, filing or updating issues.
---

# Planning

Jason drives the design. You do the legwork, lay out the choices, and keep the written plan and the tracker honest.

Every part of the plan has one home:

- **What and why:** the spec or design doc. In a repo it's a file next to the code (`BASE.md` or `docs/`). In chat it's the reply, or a Claude Doc when he asks for a doc.
- **Status:** Linear. Plan and tracker point at each other and never disagree.

## 1. Work out what he wants

- Read what already exists before asking anything: the code, the docs, his notes, open issues. Check the code before you assume a planned feature exists.
- Ask only what changes the plan, and stop once you can write it down.
- For each real choice give two or three options, the trade-off of each in a line, and your recommendation. He picks; you don't decide for him.
- What he calls non-negotiable goes in the doc as a hard constraint.

## 2. Write it down

For anything bigger than one issue, write a design doc. The template is in [templates.md](templates.md). The rules:

- **Decisions are numbered** (D1, D2, ...) and dated, with the reason, in a table. Never renumber or delete one. A decision that changes becomes `**Superseded by D12.** ~~old text~~` and the new one gets the next number.
- Refer to decisions by number everywhere else: in other docs, issues, code comments and the repo's `CLAUDE.md`.
- **Open questions** are a section of their own. Once answered, an open question becomes a decision.
- **The build order** is numbered milestones, each one shippable and testable on its own.
- Keep the status line at the top true: what's built and what's still a plan.

## 3. Break it into tasks

- One task is one commit with its own check. Order tasks by dependency, critical path first.
- A task names the files it touches and how to tell it's done.
- An idea that comes up mid-task becomes a new task or issue, not extra scope, unless he says to do it now.

## 4. Issues

Use the Linear tools (the claude.ai connector, or a `linear` MCP server). If they aren't connected, say so and stop. Don't track the plan anywhere else instead. The issue template is in [templates.md](templates.md).

- **Where:** find the team and project in the repo's `CLAUDE.md`, the plan, or his notes. If it's still unclear, ask. Never guess a team.
- **Before filing:** search the project for issues that already cover it (a few phrasings). Comment on an existing one instead of filing a duplicate.
- **Splitting:** one problem or feature is one issue. Split only when the parts are independent, or one has to land first (then it's `blocked by`).
- **Priority:** Urgent only when something is broken for everyone now. High for broken behavior and the critical path. Medium by default, features included. Low for polish and nice-to-haves.
- **Labels and milestones:** only ones the project already has (Bug, Feature, Improvement). Ask before creating projects, milestones or labels.
- **Approval:** show the list you'd file (title, priority, milestone, blocked-by) and file only after he says yes.
- **After filing:** write each id back into the plan, as in `### Task 3: Parse the manifest (JGA-123)`, so the plan and Linear point at each other.

## 5. While the work happens

- Take the next task whose blockers are done. Move its issue to In Progress when you start, In Review when it's committed, and Done when a release ships it (or whatever the repo's workflow says).
- If the plan changes, update the doc first, then bring Linear in line: retitle, reprioritize or cancel, with the reason in the issue.
- Report filing and progress as a log: `+ JGA-123 <title>` for each issue filed, `→ JGA-123 → In Review` for each move.

## Don't

- File issues for a plan he hasn't approved.
- Put secrets, credentials or private data in a doc or issue.
- Rewrite a decision or an answered question in place. Append and supersede.
