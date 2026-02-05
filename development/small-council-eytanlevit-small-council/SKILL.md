---
name: small-council
description: Consult the Small Council - a multi-LLM deliberation system that gathers independent answers from multiple frontier AI models, has them anonymously rank each other's responses, then synthesizes a consensus answer. Use for complex coding questions, architectural decisions, code reviews, debugging challenges, or when you want multiple expert perspectives. Trigger when user mentions "small council", "ask the council", "consult the council", or wants multi-model deliberation on code.
allowed-tools: [Task, Bash, BashOutput, Read, Grep, Glob, TaskOutput]
---

# Small Council Consultation

Get expert guidance on coding questions through multi-LLM deliberation.

## How It Works

The Small Council uses a 3-stage deliberation process:

1. **Stage 1**: 5 frontier LLMs (GPT-5.2, GPT-5.2-pro, Gemini 3 Pro, Claude Sonnet 4, Grok 4) independently answer your question
2. **Stage 2**: Each model anonymously ranks all responses
3. **Stage 3**: Claude Opus 4.5 as chairman synthesizes the final consensus answer

This approach leverages the collective intelligence of multiple AI models, ensuring well-rounded, thoroughly-vetted answers.

## When to Use Small Council

The Small Council is ideal for:
- **Architectural decisions**: "Should we use microservices or a monolith?"
- **Code reviews**: "Review this implementation for bugs and improvements"
- **Complex debugging**: Multi-model analysis of tricky bugs
- **Design patterns**: "What pattern best fits this use case?"
- **Performance optimization**: Get diverse optimization strategies
- **Best practices**: "What's the recommended approach for X?"

Not for simple questions - use when you want multiple expert perspectives synthesized.

## Prerequisites

- `OPENROUTER_API_KEY` set in `~/.claude/skills/small-council/.env`
- Small Council CLI installed: `uv tool install small-council`

## Process

### 1. Think Deeply About the Question

**This step is critical.** The quality of the prompt determines the quality of the deliberation.

Before proceeding, consider:
- What specifically are we trying to figure out?
- What makes this problem worthy of multi-model deliberation?
- What context do the models need?
- What would a genuinely helpful response look like?

Formulate a clear, comprehensive question that:
- Explains the core problem or decision
- Provides relevant background and constraints
- States what you've already tried (for bugs)
- Asks for specific insights or guidance

**Examples of well-crafted prompts:**

Bad: "How do I fix authentication?"

Good: "We're getting intermittent 401 errors on token refresh after deploying the new JWT middleware. Tokens validate correctly in unit tests but fail in production under load. The error only occurs for about 5% of requests. What could cause this discrepancy between test and production behavior?"

Bad: "Should I use microservices?"

Good: "We're deciding whether to split our monolithic API into microservices. Current system: 50k daily active users, 10-person team, deploying 3x/week. Main pain points: shared database bottlenecks, long CI times. Constraints: can't hire more DevOps, need to maintain current deployment velocity. What are the trade-offs and which approach fits our situation better?"

### 2. Identify Relevant Context Files

Based on the question, determine what code/files the council needs to analyze.

Use the Explore agent to find relevant files:
```
Task(
  subagent_type=Explore,
  prompt="Find files related to [specific area from your prompt]",
  thoroughness="medium"
)
```

Extract the file paths from the Explore agent's response. This context is crucial for quality deliberation.

### 3. Show What Will Be Sent

Display to user:
- The comprehensive prompt you crafted
- List of files to include
- Brief message: "Consulting the Small Council..."

### 4. Execute Small Council (Tmux-Based)

**IMPORTANT**: Always use the tmux-based approach. This ensures the council process survives even if Claude's session gets killed (common in non-interactive/batch mode).

#### Step 4a: Start Council in Tmux

```bash
~/.claude/skills/small-council/council-tmux-start.sh \
  -p "Your comprehensive prompt here" \
  -f "file1.ts" -f "file2.ts"
```

This outputs JSON with session info:
```json
{
  "session": "council-1234567890-12345",
  "output": "/tmp/council-1234567890-12345.out",
  "done": "/tmp/council-1234567890-12345.done"
}
```

**Capture the session ID from this output!**

#### Step 4b: Wait for Completion (Long Timeout)

```bash
# Wait up to 30 minutes, polling every 30 seconds
~/.claude/skills/small-council/council-tmux-wait.sh "council-SESSIONID" 1800 30
```

**IMPORTANT**: Use a 10-minute timeout (600000ms, the Bash tool maximum) and loop if needed:

```bash
# First attempt - wait up to 10 minutes
Bash(
  command: "~/.claude/skills/small-council/council-tmux-wait.sh 'council-SESSIONID' 600 30",
  timeout: 600000,
  description: "Waiting for Small Council response"
)
```

If still running after 10 minutes, call again:
```bash
# Continue waiting another 10 minutes
Bash(
  command: "~/.claude/skills/small-council/council-tmux-wait.sh 'council-SESSIONID' 600 30",
  timeout: 600000,
  description: "Continuing to wait for Small Council response"
)
```

Repeat until complete or 30 minutes total elapsed.

#### Step 4c: Check Status (Quick, Non-Blocking)

If you need to check without waiting:

```bash
~/.claude/skills/small-council/council-tmux-status.sh "council-SESSIONID"
```

Or list all sessions:
```bash
~/.claude/skills/small-council/council-tmux-status.sh --list
```

#### Resuming After Context Refresh

If Claude's context was refreshed mid-wait:

1. List existing sessions:
   ```bash
   ~/.claude/skills/small-council/council-tmux-status.sh --list
   ```

2. Check/wait for the session:
   ```bash
   ~/.claude/skills/small-council/council-tmux-wait.sh "council-SESSIONID" 600 30
   ```

3. If completed, the output file persists at `/tmp/council-SESSIONID.out`

### 5. Present the Council's Wisdom

When the council responds:
- Summarize the key consensus findings
- Highlight any dissenting opinions or trade-offs mentioned
- Extract actionable recommendations
- Note any follow-up questions to explore
- If relevant, mention which aspects had strong agreement vs. varied perspectives

## Technical Notes

- Council sessions run in tmux at `council-<timestamp>-<pid>`
- Output captured to `/tmp/council-<session>.out`
- Completion marker at `/tmp/council-<session>.done`
- Sessions survive Claude process termination
- Cleanup old sessions: `~/.claude/skills/small-council/council-tmux-cleanup.sh`
- The tool supports glob patterns: `-f "src/**/*.ts"` and multiple file flags

## Troubleshooting

### Tmux Session Issues

**Find existing sessions:**
```bash
~/.claude/skills/small-council/council-tmux-status.sh --list
```

**View session output in real-time:**
```bash
tmux attach -t council-SESSIONID
# Ctrl-B D to detach without killing
```

**Kill stuck session:**
```bash
tmux kill-session -t council-SESSIONID
```

**Cleanup old sessions:**
```bash
~/.claude/skills/small-council/council-tmux-cleanup.sh --older-than 2
```

### API Key Issues

- Ensure `OPENROUTER_API_KEY` is set in `~/.claude/skills/small-council/.env`
- Check API key is valid and has credits at openrouter.ai
- The council queries 4 models in parallel + 1 chairman, so ensure sufficient rate limits
