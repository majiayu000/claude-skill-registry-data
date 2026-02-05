---
name: using-perplexity-for-context
description: "Automatically use Perplexity search for personalized context enrichment. Use when facing unfamiliar technologies, decision points, learning questions, or preference-dependent choices."
allowed-tools:
  - mcp__perplexity-search__perplexity_search
  - Bash
  - Read
---

# Using Perplexity for Context

## First-Run Setup Check

**IMPORTANT**: Before using perplexity tools, ensure the MCP server is built and configured:

```bash
# Check if built
ls ~/.claude/plugins/cache/brain-jar/perplexity-search/*/dist/index.js 2>/dev/null || echo "NOT_BUILT"
```

If `NOT_BUILT`, run the setup:

```bash
node ~/.claude/plugins/cache/brain-jar/perplexity-search/*/run.js &
sleep 10
```

Then check for API key config:

```bash
cat ~/.claude/perplexity-search/config.json 2>/dev/null || echo "NOT_CONFIGURED"
```

If `NOT_CONFIGURED`, create the config (ask user for their Perplexity API key first):

```bash
mkdir -p ~/.claude/perplexity-search
echo '{"apiKey": "USER_API_KEY_HERE", "defaultMaxResults": 5}' > ~/.claude/perplexity-search/config.json
```

After setup, user must restart Claude Code for MCP to register.

## When to Use

Automatically invoke the `perplexity_search` tool in these situations:

### 1. Unfamiliar Territory
- Libraries, frameworks, or tools not in training data or recently updated
- New APIs, technologies, or patterns
- Example: "How do I use Bun's new test runner?"

### 2. Decision Points
- Choosing between architectural approaches where user preference matters
- Library selection (e.g., "Should I use Zustand or Redux?")
- Pattern choices (REST vs GraphQL, SQL vs NoSQL)

### 3. Learning Questions
- User asks "how does X work", "what is X", "explain Y"
- Exploratory questions about concepts or implementations
- Example: "How does React Server Components work?"

### 4. Preference-Dependent Choices
- Multiple valid approaches exist and user's style/preference affects the decision
- Code structure, naming conventions, testing approaches
- Example: Deciding between verbose/explicit vs concise/implicit code

### 5. Context Enrichment
- Answering could benefit from knowing user's background
- Technical explanations that should match user's knowledge level
- Example: Explaining advanced concepts to someone learning vs expert

## How to Use

When any trigger condition is met:

1. Invoke `perplexity_search` tool with the query
2. Review results and citations
3. Integrate findings into response naturally
4. Include source citations in response

**Do NOT announce usage** unless user explicitly asks.

## Subagent Pattern (Recommended)

For better token efficiency, dispatch a Haiku subagent to run the search:

Use Task tool:
- subagent_type: "general-purpose"
- model: "haiku"
- prompt: "Search for information about [topic] using the perplexity_search tool.

Return results in this format:

**TL;DR:** [1-2 sentence summary of the key finding]

**Full Results:**
[Complete Perplexity response with all citations]

Keep the full response - don't over-summarize. The TL;DR is for quick scanning,
but the full context is valuable for serendipitous discoveries."

**Why use subagent:**
- Model efficiency: Haiku handles the API call, saving Opus tokens
- TL;DR format: Quick summary at top for scanning
- Full results preserved: Serendipity matters - don't over-filter

**When to skip subagent:**
- Quick, simple lookups where you need immediate inline response
- When user is in the middle of a rapid back-and-forth conversation

**Example output:**

```
**TL;DR:** React Server Components render on the server and stream HTML to the client,
reducing bundle size and improving initial load time.

**Full Results:**
React Server Components (RSC) are a new paradigm for building React applications...
[full Perplexity response with citations]
```

## Example

```
User: "What's the best way to handle state in React?"

[Trigger: Preference-dependent choice]
[Invoke: perplexity_search with query enriched by user profile]
[Profile context: "I prefer TypeScript, I'm learning React, I work on B2B SaaS apps"]
[Results: Personalized recommendations based on user's context]
[Response: Integrated answer with citations]
```

## Integration with Profile

The tool automatically:
- Loads user profile from `~/.config/brain-jar/user-profile.json` (shared with shared-memory plugin)
- Enriches queries with personal context
- Returns results with superior citations
- Updates profile when user mentions preferences (silent)
- Refreshes profile every 2 days from conversation history (automatic)

**Note**: The profile is now shared across all brain-jar plugins. Use the shared-memory plugin's
`learning-about-you` skill for comprehensive profile management and onboarding.
