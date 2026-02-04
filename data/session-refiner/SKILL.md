---
name: Session Refiner
description: Automatically bridge long technical sessions to keep context window small and costs low. Extracts key technical decisions, resolved bugs, active tasks, and essential code snippets from conversation history into a compact markdown summary (2,000–5,000 tokens). Use when reaching a project phase milestone, when Claude warns the context window is getting full, or to start a fresh session with minimal token cost while maintaining continuity.
---

# Session Refiner

Automatically create a compact bridge between long coding sessions to minimize token usage and costs while preserving essential context.

## Quick Start

When your conversation is getting long:

```
You: "Use Session Refiner to create a summary"
Claude: [Generates compact markdown summary and automatically saves it]
You: [Start fresh chat, paste summary at top of conversation]
```

That's it. You've reset your context window while keeping continuity.

**Automatic Saving:** Summaries are automatically saved to `.claude/session-summaries/` with timestamped filenames like `20251220-data-cleaning-plan.md` for easy reference and organization.

## What Gets Extracted

### Active Tasks
- [ ] Unchecked items from your todo list
- TODOs and FIXMEs from code
- Stated next steps and remaining work

### Key Technical Decisions
- Architectural choices made (JWT vs sessions, database selection, etc.)
- Design patterns chosen and why
- Rejected alternatives

### Resolved Issues
- Bugs that were fixed
- Errors that were debugged
- Problems that were solved

### Code References
- Essential snippets (not full files)
- Recently-changed patterns
- Important configurations
- File paths for context

### Key Findings
- Important discoveries
- Important notes and reminders
- Non-obvious insights

## Workflow

### Option 1: Ask Claude (Easiest)

Say in your chat: **"Use Session Refiner to create a summary"**

Claude will:
1. Scan the current conversation for key information
2. Extract essential details only
3. Generate a markdown summary
4. Automatically save it to `.claude/session-summaries/YYYYMMDD-brief-title.md`
5. Display the file path

Then:
1. Start a new chat session
2. Paste the summary at the top (or reference the file path in `.claude/session-summaries/`)
3. Say: "Here's where I left off. Continue from here."
4. Resume work with fresh context window

### Option 2: Run Script Locally (Most Control)

For maximum clarity, export your conversation and run the extraction script:

```bash
# Manually save conversation to a text file, then:
python .claude/skills/session-refiner/scripts/extract_session_summary.py \
  conversation.txt \
  --output my-summary.md \
  --max-tokens 5000
```

The script parses:
- Explicit `TODO:` and `FIXME:` markers
- Unchecked checkboxes: `- [ ] task`
- Code blocks (triple backticks)
- Decision statements: "Decided to...", "Using...", etc.
- Bug resolutions: "Fixed:", "Resolved:"

Edit the output markdown if needed, then paste into a fresh chat.

## When to Use

**Milestones:**
- Completing a major feature → summarize, start fresh for next feature
- After intense debugging → capture what was learned, move on
- Switching between codebases/projects → snapshot state, fresh session

**Token Warnings:**
- Claude mentions "conversation getting long"
- You see context window warnings
- You've had multiple back-and-forth debugging rounds

**Cost Optimization:**
- Before a pause in work (stop for the day)
- Before switching to a different developer/session
- When you notice the conversation history exceeding 50k tokens

## Token Budget

A complete summary uses **2,000–5,000 tokens**, leaving you:
- **Session 1**: 100k tokens used in long conversation
- **Summary**: 3,500 tokens
- **Session 2**: Start fresh with 3,500 tokens used, 196,500 tokens available

Without refining, Session 2 would start with 100k tokens already consumed.

## Best Practices

1. **Be explicit in chat**: Use clear markers in conversation:
   ```
   TODO: Fix login validation
   FIXME: Error handling in API
   - [ ] Add unit tests
   ```
   These make extraction more accurate.

2. **Review before reuse**: Skim the generated summary before pasting. Edit if anything seems incomplete or unclear.

3. **Keep originals**: Store full conversations separately in case you need to reference them later.

4. **Extract at good moments**: Extract after finishing a module, feature, or debugging session—not randomly mid-task.

5. **Add context notes**: If something in the summary seems vague, add a clarifying note directly in the markdown before pasting.

## Example Summary Output

```markdown
# Session Summary
**Generated**: 2025-12-18 14:30:00

## Current Status

### Active Tasks
- [ ] Add authentication middleware
- [ ] Implement password reset flow
- [ ] Write integration tests for auth

## Key Technical Decisions
- **JWT tokens with refresh rotation** for stateless auth
- **PostgreSQL** for user persistence (transaction support)
- **bcryptjs** for password hashing (OWASP compliant)

## Resolved Issues
- Fixed CORS error by adding credentials flag to fetch
- Resolved password validation regex (Unicode support)

## Code References

### JavaScript
\`\`\`javascript
const hashPassword = async (pw) => {
  return bcrypt.hash(pw, 10);
};
\`\`\`

### SQL
\`\`\`sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR UNIQUE NOT NULL,
  password_hash VARCHAR NOT NULL
);
\`\`\`

## Key Findings
- Session tokens need 15-min expiry for security
- User table indexes on email for login performance

## Next Steps
1. Review the active tasks above
2. Paste this summary into a fresh chat session
3. Continue from where you left off
```

## How Claude Uses This Skill

When you request a summary, Claude will:

1. **Scan the conversation** for patterns like:
   - `TODO:`, `FIXME:`, `[ ]` checkboxes → Active Tasks
   - Decision statements → Key Decisions
   - "Fixed", "Resolved" → Resolved Issues
   - Code blocks → Code References
   - Key findings statements → Insights

2. **Extract sparingly**: Only essential information, not entire files or repetitive content.

3. **Generate markdown**: Clean, copy-paste-ready format.

4. **Automatically save**: Write summary to `.claude/session-summaries/YYYYMMDD-brief-title.md`
   - Format: `YYYYMMDD` (ISO date) + `-` + brief title (kebab-case)
   - Example: `20251220-data-cleaning-plan.md`
   - Automatically creates directory if needed

5. **Hand to you**: You can paste the summary content or reference the saved file.

## Technical Details

See [workflow.md](references/workflow.md) for detailed step-by-step examples and advanced extraction techniques.

The extraction script (`scripts/extract_session_summary.py`) uses regex patterns to identify:
- Explicit TODO/FIXME markers
- Checkbox lists
- Code blocks with language markers
- Decision and resolution keywords
- Key finding statements

You can manually run it for programmatic extraction when needed.
