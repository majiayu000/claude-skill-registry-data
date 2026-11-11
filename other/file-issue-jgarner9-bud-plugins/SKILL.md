---
name: file-issue
description: Turns a problem report or feature request (often sent from bud's <leader>ai / <leader>aB keys, with editor context attached) into one or more well-formed Linear issues. Proposes them as a bud-issues JSON block first and files only after an explicit "File these" message. Use when asked to file, report or log an issue, bug or feature request in Linear.
---

# Filing an issue from a report

A report arrives as a short note from someone in the middle of other work: a problem, or a feature they want. It comes with context: the file and lines they were on, diagnostics there, recent editor errors, versions. Your job is to turn it into issues someone can pick up cold. Work in two rounds, and never file in the first.

Use the Linear MCP tools (the claude.ai Linear connector, or a `linear` MCP server where there's no connector). If they aren't available, say so in one line and stop. If the `linear` server isn't logged in yet, say to run `bud agent` and log in with `/mcp`, and stop.

## Run by hand

When someone runs `/bud-ide:file-issue <report>` in a terminal instead of sending it from bud's editor keys, the rounds are the same, but propose the issues as a readable list rather than the `bud-issues` block, and file them once they say yes. If no team or project is given, look in the repo's `CLAUDE.md` and memory for the project's Linear project, and ask if it's still unclear.

## Round 1: propose

1. **Target.** The message names the Linear team and, usually, the project. Use exactly those; never guess another. If none is given, ask for one in `notes` and propose nothing.
2. **Understand it.** Decide whether it's a problem (something behaves wrongly) or a feature request (something new, or a change to behavior that works as built). Read the attached context, then look in the code (Read, Grep, and Serena or cocoindex-code when they're there) for where the problem lives, or where the feature would go and what it would build on. Name files and functions in the description; don't fix or build anything. For a feature, the editor context is often just where the reporter happened to be: use it only when it bears on the request.
3. **Duplicates.** Search the target project for open issues that already cover it (`list_issues` with a query, a few phrasings). If one does, propose a comment on it (`duplicate_of`) instead of a new issue.
4. **Split or not.** One problem or feature is one issue. Split only when the report mixes independent ones, or one fix clearly has to land before another (then `blocked_by`). Two or three issues is a lot for one report.
5. **Each issue:**
   - `title`: short. For a problem, imperative or a plain statement of the bug ("Dashboard drops the last project row on narrow terminals"); for a feature, what to add or change ("Remember the tree pane's width per project").
   - `description`: Markdown. Keep the reporter's own words in a quote. For a problem: what happens, what should happen, how to reproduce it (from the context), where in the code it likely lives, and how to tell it's fixed. For a feature: what the reporter wants to do and why (the use case), the behavior they're asking for, where it would fit in the code and what it builds on, open questions, and how to tell it's done.
   - `priority`: 1 Urgent only when something is broken for everyone now; 2 High for broken behavior or the critical path; 3 Medium by default, features included; 4 Low for polish and nice-to-haves.
   - `labels`: only labels the team already has (`list_issue_labels`), e.g. Bug for a problem, Feature for something new, Improvement for a change to something that works.
   - `milestone`: the project's current milestone if one clearly fits, else null.
6. **Reply** with one line saying what you found, then exactly one fenced block:

```bud-issues
{
  "team": "JGA",
  "project": "Bud IDE",
  "issues": [
    {
      "key": "a",
      "title": "...",
      "description": "...",
      "priority": 3,
      "labels": ["Bug"],
      "milestone": null,
      "blocked_by": [],
      "duplicate_of": null
    }
  ],
  "notes": "anything the reporter should know, or a question"
}
```

`key` is a local name ("a", "b") that `blocked_by` refers to. With `duplicate_of` set ("JGA-42"), the issue is a comment on that one: `description` is the comment.

## Round 2: file

Only when the next message starts with "File these". It carries the block back, possibly edited by the reporter: file what it says, not your first draft. Create the issues in `blocked_by` order (state: the team's backlog or triage default), set the relations, post the comments for duplicates, then reply with one `→` line per issue (`→ JGA-130 filed: <title>`, or `commented`/`failed`) and exactly one fenced block:

```bud-filed
[{"key": "a", "id": "JGA-130", "url": "https://linear.app/...", "title": "...", "action": "filed"}]
```

`action` is "filed" or "commented". If one fails, file the rest and give it `"action": "failed", "error": "..."`.

If the next message says the reporter dropped them, reply "Dropped." and file nothing.

## Don't

- Create, edit or comment on anything in Linear before "File these".
- Edit the repo: this is reporting, not fixing or building.
- Copy secrets, tokens or private data from the context into an issue.
