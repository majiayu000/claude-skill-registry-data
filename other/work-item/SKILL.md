---
name: work-item
description: >
  Drafts a well-formed work item with testable acceptance criteria, then creates it in whatever
  tracker is connected, when the user asks for that explicitly. Applies the same standard to tighten
  an existing work item. Use when the user invokes /work-item, or asks to draft, write up, create, or
  fix up a ticket, issue, task, story, bug report, or sub-task, for Jira, GitHub, Azure DevOps,
  Linear, or any other tracker. Use it even when the user names no tracker and never says "ticket",
  as in "log a bug for...", "file an issue about...", "write up a task for...", "can you create a
  story for...", and "this ticket has no acceptance criteria, can you add some". Do NOT use it for
  general prose writing, a PR description, or a commit message, because those follow different
  conventions.
argument-hint: "[one-line description of the work]"
---

# Work Item

Draft a work item in the shape that already dominates well-formed real work items. That shape has three parts. It uses bold-text section headers instead of markdown `##` headers. It has a framing section, chosen by the nature of the work item. It has acceptance criteria, written as testable and observable outcomes. Never write a vague criterion such as "works correctly". The same standard applies when you draft a new work item from scratch. It applies when you fix up an existing one that is missing a piece, most often the acceptance criteria. Treat both as the same content problem.

This skill defines content only. It has no opinion on which tracker or tool creates or updates the work item. Tool selection is a runtime decision, taken at the point of creation, based on whatever is connected in the current session. The tool can be a Jira MCP tool, `gh issue create`, or an Azure DevOps or Linear API.

When the user invokes `/work-item`, treat `$ARGUMENTS` as a one-line description of the work, and ask follow-up questions to fill any gap. When the conversation triggered this skill instead, use the context that the conversation already established. Do not ask again for what the user already said.

## Execution steps

1. Determine the nature of the work. Ask whether it reports a defect, which means that something is broken, or whether it describes new or changed work. That answer chooses the framing section, described in `assets/work-item-template.md`.
2. Determine whether the item is standalone or a child of a larger parent item. The test is under "Applies to" below. That answer decides whether the acceptance criteria are mandatory.
3. Draft the content, following `assets/work-item-template.md`, in the plain English that "Writing style" below describes. Read that file for the full template and the worked examples before you write. Do not rely on a remembered shape, because the exact section names and casing matter. For example, "Acceptance criteria" carries a lowercase c, it is bold, and it has no colon. When you fix up an existing work item, keep what is already there, and add or rewrite only the pieces that are missing or vague.
4. Sometimes the user asked you to draft or write up the work item, and not to create or update it. Then present the drafted content for review, and stop there.
5. When the user asked you explicitly to create or update the work item, proceed directly. Pick whichever tool fits the destination tracker at that moment, and apply the change. The request itself is the go-ahead, so no extra confirmation gate is needed once the content is drafted.

## Writing style

A triager next quarter, or a reader outside the team, must understand the work item on one read. Write short sentences in the active voice, define a term that such a reader can miss at its first use, and cut filler.

Keep every quoted error message, identifier, and value exactly as it is. When a plain-English writing skill such as `simple-english` is available, invoke it and apply its rules to the draft, before you present or create the item.

## Applies to

These two questions are about the work itself, and not about matching the type field of a tracker. A "task" in Jira, a plain issue in GitHub, and a "user story" in Azure DevOps are all standalone items by this test. The same logic applies whatever the destination tracker calls its types.

A standalone item is the top-level thing being tracked, and it always gets the full treatment: a framing section, plus mandatory acceptance criteria.

A child item is something broken out under a larger parent, whatever the tracker calls it. It can be a Jira sub-task, a GitHub sub-issue, an Azure DevOps child work item, or a Linear sub-issue. A child item is conditional. It needs its own framing and its own acceptance criteria only when someone can verify it independently. Independent verification means its own deploy, its own test, and its own "done" state. An example is one of several services migrating off a queue, where each service cuts over and gets verified separately. A child item that is only a granular checklist entry under a parent, whose acceptance criteria already cover it, stays minimal. Do not manufacture an acceptance criteria section that the item does not need.

See `assets/work-item-template.md` for the full template, the exact content shape, and the worked examples that cover each variant.
