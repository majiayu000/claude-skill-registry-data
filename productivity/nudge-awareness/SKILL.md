---
name: nudge-awareness
description: How agents check for and surface relevant context when a developer is working without a spec.
compatibility: opencode
metadata:
  audience: agents
  purpose: context-awareness
---
## What I do

Teach agents how to use the `hero relevant` command to surface relevant conventions, past work, and in-flight specs when a developer works directly without using `/design` or `/deliver`.

## When to use me

Load this skill when an agent is about to do implementation work that was not initiated through the spec workflow (no `/design`, no `/deliver`). This applies most often to the `engineer` agent receiving a direct task.

## How nudging works

The `hero relevant` command checks the spec corpus index for context relevant to the files being touched and returns a message calibrated to the team's configured nudge level.

### Nudge levels (configured in hero.json)

| Level | Behavior |
|---|---|
| `off` | No nudge output. Agent works silently. |
| `gentle` | Short summary: convention names, past spec count, in-flight spec names. One-liner references with a pointer to `hero relevant` for more detail. |
| `assertive` | Full context block: convention descriptions with paths, past work titles, in-flight spec warnings, and a recommendation to use `/design`. |

The level is set in `hero.json` under `team.nudge_level`. Default is `gentle`.

### Running the nudge

Before writing code for a direct task, identify the files you intend to change and run:

```
hero relevant --files src/api/users.ts src/db/queries/users.sql
```

### Interpreting the output

- **If empty** — no relevant context exists. Proceed normally.
- **If conventions are listed** — follow them in your implementation, even without a spec.
- **If past specs are listed** — be aware of prior design decisions. Don't contradict them without reason.
- **If in-flight specs are listed** — warn the developer that someone else may be working on overlapping files. Suggest coordinating.

### Presenting the nudge to the developer

Include the nudge output in your response, clearly separated from your implementation work. Do not lecture or moralize. The nudge is a factual summary of what exists in the corpus, not a judgment about how the developer chose to work.

Good:
```
## Implementation
[your code changes]

---
Hero found relevant context for the files you're touching:
- Convention: api-response-format
- 2 past specs touched these files
- In-flight spec: add-user-search (delivering)

Run `hero relevant --files <paths>` for full details.
```

Bad:
```
You should have used /design first! Let me show you what you missed...
```

### When the developer ignores the nudge

That's fine. The nudge is advisory. The developer may have good reasons to skip the spec workflow for small, low-risk changes. Do not re-nudge or escalate.

## Relationship to context injection

Nudging is the lightweight complement to context injection:

- **Context injection** (via `hero relevant`) is the full-power version used by delivery leads during `/deliver`. It generates a structured block with conventions, past work, decisions, and known risks.
- **Nudging** (via `hero relevant`) is the lightweight version used by agents working directly. It surfaces the same information in a shorter format, appropriate for ad-hoc work.

If a nudge reveals significant context (many conventions, in-flight conflicts), the agent should suggest that the developer consider using `/design` to get full context injection. But this is a suggestion, not a requirement.
