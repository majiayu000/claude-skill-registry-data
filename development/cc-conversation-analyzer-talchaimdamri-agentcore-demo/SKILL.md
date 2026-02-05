---
name: cc-conversation-analyzer
description: |
  Comprehensive Claude Code conversation analysis skill for deep-diving into CC session logs.
  Use when analyzing exported Claude Code conversations to understand: project patterns, error rates,
  command failures, security risks, session duration, tool usage, and workflow efficiency.

  Triggers: "analyze conversation", "CC analysis", "conversation analysis", "session review",
  "Claude Code logs", "analyze my sessions", "review CC usage", "conversation insights",
  "what went wrong in my session", "session forensics", "CC forensics"
---

# Claude Code Conversation Analyzer

Analyze Claude Code conversation exports to generate actionable insights, identify patterns,
and provide recommendations based on CC best practices.

## Initial Setup

### Step 1: Get Required Information from User

Before running analysis, prompt the user for:

1. **Data folder path**: Ask "What is the path to your Claude Code project data folder?"
   - Usually: `~/.claude/projects/<project-folder>`
   - Example: `/Users/username/.claude/projects/-Users-username-projects-my-app`

2. **GEMINI_API_KEY** (required for topic analysis and command recommendations):
   - Ask: "Do you have a GEMINI_API_KEY set? If not, please provide one for AI-powered analysis."
   - If not set, prompt: "Please provide your Gemini API key (get one at https://aistudio.google.com/apikey)"
   - Set it: `export GEMINI_API_KEY="user_provided_key"`

### Step 2: Run the Analysis Pipeline

Use the scripts in `scripts/` folder. The skill folder location is:
`~/.claude/skills/cc-conversation-analyzer/scripts/`

```bash
# Set variables
SKILL_DIR="$HOME/.claude/skills/cc-conversation-analyzer/scripts"
DATA_FOLDER="<user_provided_path>"
OUTPUT_DIR="analysis_results/<output_name>"  # Where to save all analysis results

# Create output directories
mkdir -p "$OUTPUT_DIR/conversations" "$OUTPUT_DIR/user_queries"

# Run pipeline in order:
# 1. Build graph (pass DATA_FOLDER and OUTPUT_DIR)
node "$SKILL_DIR/build_conversation_graph.js" "$DATA_FOLDER" "$OUTPUT_DIR"

# 2. Export conversations (pass path to conversation_graph.json, NOT data folder)
node "$SKILL_DIR/export_conversations.js" "$OUTPUT_DIR/conversation_graph.json"

# 3. Extract user queries
node "$SKILL_DIR/extract_user_queries.js" "$OUTPUT_DIR/conversations" "$OUTPUT_DIR/user_queries"

# 4. AI-powered analysis (requires GEMINI_API_KEY)
node "$SKILL_DIR/analyze_topics.js" "$OUTPUT_DIR/user_queries"

# 5. Error, risk, and command analysis
node "$SKILL_DIR/analyze_errors.js" "$OUTPUT_DIR/conversations"
node "$SKILL_DIR/analyze_risks.js" "$OUTPUT_DIR/conversations"
node "$SKILL_DIR/analyze_commands.js" "$OUTPUT_DIR/conversations"

# 6. Generate recommendations and summary
node "$SKILL_DIR/recommend_commands.js" "$OUTPUT_DIR/command_analysis_detailed.json"
node "$SKILL_DIR/generate_conversation_summary.js" \
  "$OUTPUT_DIR/conversation_graph.json" \
  "$OUTPUT_DIR/topics_analysis.json" \
  "$OUTPUT_DIR/error_summary.csv"
```

**Important**: The `export_conversations.js` script expects the path to `conversation_graph.json`, NOT the data folder. It reads the source folder from the graph metadata.

## Prerequisites

After running the pipeline, the following files should exist:

```
analysis_results/<PROJECT>/
├── conversation_graph.json        # Core graph structure
├── conversation_graph_summary.csv # Aggregated metrics
├── conversations/                 # Exported JSON files
├── topics_analysis.json           # AI-generated topic summaries
├── error_analysis.csv             # Detailed error log
├── error_summary.csv              # Per-conversation error counts
├── risk_analysis.csv              # Security risk findings
├── command_analysis_detailed.json # Command success/failure stats
└── command_recommendations.md     # AI-generated command fixes
```

If files are missing, run the analysis pipeline first. See references/analysis_pipeline.md for the full command sequence.

## Analysis Workflow

### Phase 1: Load and Understand the Data

1. **Read the conversation graph summary** (`conversation_graph_summary.csv`):
   - Identify total conversations, durations, stage counts
   - Note conversations with high error counts or many continuations
   - Look for patterns in user message vs tool interaction ratios

2. **Read topics analysis** (`topics_analysis.json`):
   - Understand what the user was trying to accomplish
   - Group conversations by topic/intent

3. **Read error summary** (`error_summary.csv`):
   - Identify conversations with highest error counts
   - Note the most frequent error types

### Phase 2: Deep Dive into Problem Areas

4. **Analyze command failures** (`command_analysis_detailed.json`):
   - Find commands with highest failure rates
   - Identify root causes (wrong directory, missing tools, syntax errors)
   - Read `command_recommendations.md` for specific fixes

5. **Review security risks** (`risk_analysis.csv`):
   - Check for exposed API keys, passwords, or private keys
   - Note which conversations had security exposures
   - Flag the role (User/Assistant/Tool Output) that exposed secrets

6. **Examine detailed errors** (`error_analysis.csv`):
   - Correlate errors with specific conversation contexts
   - Identify patterns (e.g., recurring API errors, tool failures)

### Phase 3: Generate Summary Report

Produce a structured summary with these sections:

```markdown
## Project Overview
- **Project Name**: [extracted from folder name]
- **Analysis Period**: [first to last timestamp]
- **Total Conversations**: [count]
- **Total Duration**: [sum of all session minutes]

## Session Statistics
- User Messages: X
- Assistant Messages: Y
- Tool Interactions: Z
- Agents Spawned: N
- Context Compactions: M

## Error Analysis
- Total Errors: X
- Error Breakdown:
  - System API Errors: N
  - Tool Execution Errors: N
  - Runtime Exceptions: N
  - User Interruptions: N
  - Non-Zero Exit Codes: N
- Most Problematic Conversation: [ID] with [N] errors

## Command Analysis
- Total Commands Run: X
- Success Rate: Y%
- Most Failing Commands:
  1. `command_group`: N failures (X% rate)
  2. ...

## Security Findings
- Risks Detected: [count or "None"]
- Types: [API keys, passwords, etc.]
- Severity: [High/Medium/Low based on secret types]

## Topics & Goals
[List main topics identified from topics_analysis.json]

## Recommendations
[See Phase 4 below]
```

### Phase 4: Generate CC Best Practice Recommendations

Based on the analysis, provide actionable recommendations using Claude Code features.
Reference `references/cc_best_practices.md` for detailed patterns.

#### Recommendation Categories

**1. Error Prevention Hooks**

For recurring errors, recommend hooks:

```markdown
### Recommendation: Add Pre-Command Validation Hook

**Problem**: `npm run build` failed 15 times due to missing dependencies.

**Solution**: Add a `UserPromptSubmit` hook to validate environment:

\`\`\`json
{
  "hooks": {
    "UserPromptSubmit": [{
      "match": "build|compile|deploy",
      "command": "node scripts/check_dependencies.js"
    }]
  }
}
\`\`\`

**Benefits**:
- Accelerates development: Catches missing deps before Claude wastes tokens
- Prevents errors: Validates environment state proactively
- Leverages: Claude Code hooks system for automated pre-flight checks
```

**2. Skills for Repetitive Workflows**

For repetitive patterns, recommend skills:

```markdown
### Recommendation: Create Project-Specific Build Skill

**Problem**: User repeatedly asked similar build/deploy questions across 5 sessions.

**Solution**: Create a skill with your project's build commands and patterns:

\`\`\`
my-project-build/
├── SKILL.md  # Contains build commands, common errors, fix patterns
└── scripts/
    └── validate_build.sh
\`\`\`

**Benefits**:
- Accelerates development: Claude learns your build system once
- Prevents errors: Codifies known-good patterns and workarounds
- Leverages: Skills system for persistent procedural knowledge
```

**3. Subagents for Complex Tasks**

For error-prone complex tasks, recommend subagents:

```markdown
### Recommendation: Use Code Review Subagent

**Problem**: 12 tool execution errors in code editing tasks.

**Solution**: Configure a code-reviewer subagent with read-only permissions:

\`\`\`json
{
  "subagents": {
    "code-reviewer": {
      "tools": ["Read", "Grep", "Glob"],
      "system_prompt": "Review code for errors before changes are applied."
    }
  }
}
\`\`\`

**Benefits**:
- Accelerates development: Parallel review while coding continues
- Prevents errors: Catches issues before they're committed
- Leverages: Subagent isolation and specialized tool permissions
```

**4. CLAUDE.md for Project Context**

For context-related issues, recommend CLAUDE.md updates:

```markdown
### Recommendation: Add Testing Commands to CLAUDE.md

**Problem**: Claude ran incorrect test commands 8 times.

**Solution**: Add explicit test instructions to your CLAUDE.md:

\`\`\`markdown
## Testing
- Unit tests: `pnpm test:unit`
- Integration: `pnpm test:integration --env=test`
- NEVER run `npm test` - this project uses pnpm
\`\`\`

**Benefits**:
- Accelerates development: Claude knows commands from session start
- Prevents errors: Explicit instructions override guessing
- Leverages: CLAUDE.md automatic context injection
```

**5. MCP for External Data Access**

For API/data access patterns, recommend MCP:

```markdown
### Recommendation: Configure Database MCP Server

**Problem**: User manually fetched database schemas 6 times.

**Solution**: Configure MCP connection to your database:

\`\`\`json
{
  "mcpServers": {
    "postgres": {
      "command": "mcp-postgres",
      "args": ["--connection-string", "$DATABASE_URL"]
    }
  }
}
\`\`\`

**Benefits**:
- Accelerates development: Direct schema access without manual copying
- Prevents errors: Always uses live schema, not stale documentation
- Leverages: MCP for tool connectivity to external systems
```

**6. Dev Docs for Long Tasks**

For multi-session projects with context loss:

```markdown
### Recommendation: Implement Dev Docs System

**Problem**: Project spanned 8 sessions with 12 context compactions.

**Solution**: Create persistent task documentation:

\`\`\`
dev/active/feature-name/
├── plan.md     # Implementation plan
├── context.md  # Key decisions and file locations
└── tasks.md    # Checklist of remaining work
\`\`\`

Instruct Claude to read and update these files each session.

**Benefits**:
- Accelerates development: No re-explaining context each session
- Prevents errors: Single source of truth survives compactions
- Leverages: External memory pattern for long-term context
```

## Output Format

Final output should be a single markdown document containing:

1. **Executive Summary** (3-5 bullet points)
2. **Project Overview** (stats table)
3. **Key Findings** (errors, risks, patterns)
4. **Detailed Recommendations** (3-5 actionable items with CC feature mappings)
5. **Next Steps** (prioritized action items)

Each recommendation MUST include:
- The specific problem observed
- The CC feature/pattern to apply
- How it accelerates development
- How it prevents errors
- Which Claude Code capability it leverages
