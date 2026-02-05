---
name: journal-capture
description: Proactively captures significant work into the journal for future reference
when_to_use: Use this skill when you complete significant work, solve important problems, make key decisions, or implement notable features. This helps build a searchable history of accomplishments.
---

# Journal Capture Skill

You have the ability to proactively capture significant work into the user's journal.

## When to Use This Skill

Use this skill **automatically and proactively** when you:

1. **Complete a significant feature or task**
   - Implemented new functionality
   - Fixed a complex bug
   - Refactored important code
   - Set up infrastructure or tooling

2. **Make important technical decisions**
   - Chose between architectural approaches
   - Selected libraries or frameworks
   - Decided on implementation strategies
   - Resolved design tradeoffs

3. **Solve challenging problems**
   - Debugged difficult issues
   - Overcame technical obstacles
   - Found non-obvious solutions
   - Learned something valuable

4. **Make progress on projects**
   - Completed a phase of work
   - Reached a milestone
   - Integrated multiple components
   - Finished testing or deployment

## How to Capture

Use the `journal_auto_capture` MCP tool:

```
journal_auto_capture(
  title="Brief title of what was accomplished",
  description="The goal (what we were trying to do) and what was done"
)
```

The tool automatically:
- Determines the project (if in a git repo)
- Adds the "auto-capture" tag
- Generates relevant tags based on content
- Creates a structured journal entry

## Examples

**Example 1: Feature implementation**
```
User: "Add authentication to the API"
[You implement OAuth2 with JWT tokens]
→ journal_auto_capture(
    title="Implemented OAuth2 authentication",
    description="User requested API authentication. Implemented OAuth2 flow with JWT tokens for secure user sessions."
  )
```

**Example 2: Bug fix**
```
User: "The cache is leaking memory"
[You identify and fix the leak]
→ journal_auto_capture(
    title="Fixed cache memory leak",
    description="User reported memory leak in cache. Identified and fixed by implementing automatic clearing of stale entries."
  )
```

**Example 3: Technical decision**
```
User: "Should we use Redis or PostgreSQL for caching?"
[Discussion leads to Redis choice]
→ journal_auto_capture(
    title="Chose Redis for caching",
    description="Evaluated Redis vs PostgreSQL for caching needs. Selected Redis due to better performance for our use case."
  )
```

**Example 4: Infrastructure setup**
```
User: "Set up CI/CD pipeline"
[You configure GitHub Actions with tests and deployment]
→ journal_auto_capture(
    title="Set up GitHub Actions CI/CD",
    description="User requested CI/CD pipeline. Configured GitHub Actions with automated tests and deployment workflow."
  )
```

## What NOT to Capture

Don't capture:
- Trivial changes (typo fixes, formatting)
- Failed attempts or abandoned approaches
- Purely informational exchanges
- User questions without implementation

## Timing

Capture entries:
- **Immediately after** completing significant work
- **Before** moving to the next major task
- **At natural breakpoints** in the conversation
- **When the auto-capture hook triggers** (every 30 min or 3+ messages)

This ensures the journal stays current and useful for future context recovery.

## Responding to Auto-Capture Hook

When you see a message from the auto-capture hook:
```
🕐 Journal auto-capture triggered
   N messages exchanged since last capture
   Project: <project-name>

📝 Please capture this session to the journal:
   - Summarize the goal (what we were trying to do)
   - Summarize what was accomplished
   - Use journal_auto_capture with a brief summary

⚠️  Claude: You MUST respond to this trigger, even if you decide not to capture.
   Either create a journal entry OR explain why you're not capturing.
```

**You MUST respond to this trigger every time.** Follow these steps:

1. **Acknowledge the trigger** - Let the user know you saw the auto-capture signal
2. **Analyze the conversation** - Review what happened since the last capture
3. **Decide and act:**
   - **If significant work occurred:** Call `journal_auto_capture` with an appropriate title and description
   - **If nothing substantial happened:** Explicitly explain why you're not capturing (e.g., "Only trivial Q&A since last capture, nothing substantial to record")

**IMPORTANT:** Never silently ignore the hook trigger. The user needs visibility into your decision-making process, even if you decide not to capture.

## Benefits

Proactive capture helps:
- Rebuild context after `/clear`
- Track progress across sessions
- Remember past solutions
- Build institutional knowledge
- Generate progress reports
