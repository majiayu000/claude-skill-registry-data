---
name: managing-memory
description: "Guide for storing enriched memories that capture decisions, preferences, and context. Use when making significant decisions or learning user preferences."
allowed-tools:
  - mcp__shared-memory__add_memory
  - mcp__shared-memory__search_memory
  - mcp__shared-memory__list_memories
  - mcp__shared-memory__delete_memory
  - Bash
  - Read
---

# Managing Memory

## First-Run Setup Check

**IMPORTANT**: Before using memory tools, ensure the MCP server is built and configured:

```bash
# Check if built
ls ~/.claude/plugins/cache/brain-jar/shared-memory/*/dist/index.js 2>/dev/null || echo "NOT_BUILT"
```

If `NOT_BUILT`, run the setup:

```bash
node ~/.claude/plugins/cache/brain-jar/shared-memory/*/run.js &
sleep 15
```

Then check for Mem0 config:

```bash
cat ~/.config/brain-jar/config.json 2>/dev/null || echo "NOT_CONFIGURED"
```

If `NOT_CONFIGURED`, ask user for their Mem0 API key (get one at https://app.mem0.ai), then create config:

```bash
mkdir -p ~/.config/brain-jar
cat > ~/.config/brain-jar/config.json << 'EOF'
{
  "mem0_api_key": "USER_API_KEY_HERE",
  "default_scope": "global",
  "auto_summarize": true
}
EOF
```

Note: Local storage works without Mem0 config - cloud sync is optional.

After setup, user must restart Claude Code for MCP to register.

## When to Store Memories

Store memories when you observe:
- **Decisions** - User chooses one approach over another
- **Preferences** - User expresses likes/dislikes about tools, patterns, or approaches
- **Reactions** - Strong positive or negative responses (enthusiasm, frustration)
- **Context** - Important background about projects, goals, or constraints

## How to Write Enriched Memories

Bad (too dry):
```
User chose Neon for database.
```

Good (captures context and sentiment):
```
User chose Neon over Supabase for Postgres hosting - appreciated the more generous
free tier limits. Showed strong preference for managed solutions: "I'm not running
my own infra" - values simplicity and time savings over control.
```

## Memory Format

Include:
1. **The fact** - What was decided/learned
2. **The why** - Reasoning behind it
3. **The sentiment** - How they felt about it (quote if memorable)
4. **The implication** - What this suggests about future preferences

## Scope Selection

- `global` - Personal preferences, general learnings, cross-project patterns
- `project:<name>` - Specific to current project (detect from working directory)

Use `global` for preferences that apply everywhere. Use `project:` for architectural
decisions, tech choices, and patterns specific to one codebase.

## When to Recall Memories

Before:
- Starting a new feature (search for relevant past decisions)
- Making technology choices (search for preferences)
- Suggesting approaches (search for patterns they liked)

Use natural recall language:
- "Remember when you were working on X, you decided..."
- "You've mentioned before that you prefer..."
- "Based on your experience with Y..."

## Subagent Pattern for Large Retrievals

When searching or listing memories that could return many results (10+), dispatch a Haiku subagent to process and summarize:

**When to use subagent:**
- Broad searches: "find all memories about preferences"
- Timeline queries: "memories from last month"
- Pattern analysis: "what decisions have I made about databases?"

**How to dispatch:**

Use Task tool:
- `subagent_type`: "general-purpose"
- `model`: "haiku"
- `prompt`: "Search user memories and provide a summary.

TASK: [what user is looking for]

STEPS:
1. Call search_memory with query '[search terms]'
2. If many results, group by theme or tag
3. Return a 3-5 sentence summary highlighting:
   - Key patterns/preferences found
   - Notable decisions or quotes
   - Relevant context for the current task

OUTPUT: Concise summary, not raw memory dumps."

**Tell the user:** The subagent's summary. Don't dump all raw memories into context.

**When to use direct tools:**
- Specific lookups: "what was the exact decision about X?"
- Small result sets: known to be 1-3 memories
- When user explicitly asks for full details

**Example flow:**

```
User: What do I usually prefer for state management?

You: Let me search your memories for state management preferences...
[Dispatch Haiku subagent]

Subagent returns:
"Found 7 memories about state management. Key patterns:
- Strong preference for Zustand over Redux (called Redux 'too much boilerplate')
- Uses React Query for server state ('keeps server/client state separate')
- Avoids global state when possible - prefers component-level state
Notable quote: 'I want the simplest thing that works'"

You: Based on your past preferences, you tend to favor Zustand for client state
and React Query for server state. You've mentioned wanting "the simplest thing
that works" - should I keep that philosophy for this feature?
```

## Tags to Use

- `preference` - Likes/dislikes
- `decision` - Specific choices made
- `architecture` - System design patterns
- `personality` - Working style, communication preferences
- `project` - Project-specific context
- `session-summary` - End-of-session consolidation
- `profile-context` - Background context for profile preferences
- `profile-learning` - Observations that inform the user profile

## Related Skills

### Learning About You

For structured user profile management (name, role, tech preferences, working style),
use the `learning-about-you` skill instead of storing as freeform memories.

**Use memories for:**
- Rich context and reasoning behind preferences
- Specific quotes and reactions
- Project-specific decisions
- Session summaries

**Use profile for:**
- Structured data (name, timezone, role)
- Tech stack preferences (languages, frameworks)
- Working style settings (verbosity, pace)
- Personal goals and interests

The profile is queryable and shared across all brain-jar plugins. Memories provide
the context and "why" behind profile entries.
