---
name: retrospective
description: Pause and reflect when you've been repeating the same actions or cycling through a failing loop. Produce a structured self-assessment with proposed config changes.
---

# Retrospective

Stop and reflect on your recent work before continuing.

## When to Invoke

Invoke this skill when you notice **either** of these patterns:

**Repetition pattern** — you've used the same category of action 5+ times in a row without a meaningful change in approach. Examples:
- Five or more consecutive DB queries (psql, direct SQL, Flyway inspection)
- Five or more consecutive file reads without acting on what you found
- Five or more consecutive search attempts (Grep/Glob) that return empty or unhelpful results
- Five or more consecutive service restarts or rebuilds
- Five or more consecutive API or MCP calls of the same type (e.g. repeated Jira fetches, repeated Sentry searches, repeated Smartsheet reads)

**Loop pattern** — you've cycled through the same sequence of actions more than once without net progress. Examples:
- Write migration → start services → test → migration fails → update migration → repeat
- Edit code → run tests → same failure → edit same code again → repeat
- Fetch data → analyze → reach same conclusion → fetch more data → same conclusion → repeat
- Call API or MCP tool → get unexpected result → adjust params → call again → same unexpected result → adjust again → repeat
- Fetch Jira/Sentry/Smartsheet data → form hypothesis → fetch more data to confirm → hypothesis doesn't hold → fetch more data → repeat

## What to Do

### Step 1: Reconstruct what just happened

Write out the last 5–10 actions you took as a numbered list. Be specific — include tool names and what you were trying to learn or accomplish with each.

### Step 2: Assess honestly

**Things I did well:**
- What actions moved me forward?
- What information did I successfully gather?
- What worked on the first try?

**Things I did poorly:**
- Where did I spin without making progress?
- What assumptions did I make that turned out to be wrong?
- What did I guess at when I should have read the source?
- Where did I go wide (many searches) when I should have gone deep (read one key file)?

**Root cause of the loop or repetition:**
- Was I missing a key piece of context I should have fetched first?
- Was I trying to confirm a hypothesis rather than test it?
- Was the approach fundamentally wrong and I kept patching instead of reframing?

### Step 3: Propose config/workflow changes

Suggest specific, actionable changes — skewed toward local user configuration (CLAUDE.md additions, settings.json hooks, new skills, memory entries) that would prevent this pattern in future sessions. Examples:
- "Add a note to sp-ux-service/CLAUDE.md that X is always found at Y"
- "Add a memory entry that says always read the Flyway migration before writing a DB query"
- "Add a new skill that triggers before any migration file is created"
- "Add this pattern to the UserPromptSubmit hook's high-miss skills list"

Be concrete. Don't propose "be more careful" — propose a specific file change or hook.

### Step 4: Present to user and incorporate feedback

Present your structured self-assessment:
1. What just happened (brief)
2. Did well / did poorly
3. Proposed config changes (with specific file paths and content)

Then **ask the user**: "Does this match your read? Anything to add or correct?"

**Wait for explicit approval before acting on any proposed changes.** Do not write to CLAUDE.md files, memory, or settings until the user confirms. They may reject, redirect, or reframe the proposals entirely.

## Anti-Patterns to Flag

- Guessing at column names, file paths, or API fields instead of reading the source
- Running the app to discover schema instead of reading migrations
- Making the same failing tool call with slightly different parameters
- Reading the same file multiple times in a session because you forgot what it contained
- Expanding scope to avoid admitting the current approach isn't working
