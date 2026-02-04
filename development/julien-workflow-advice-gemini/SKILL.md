---
name: julien-workflow-advice-gemini
description: Get Gemini CLI's opinion on code, architecture, or implementation. Use when you want a second AI perspective during coding sessions.
triggers:
  - "ask gemini"
  - "gemini opinion"
  - "gemini review"
  - "what does gemini think"
  - "demande à gemini"
  - "avis de gemini"
  - "gemini pense quoi"
  - "get gemini feedback"
  - "gemini second opinion"
  - "google gemini review"
---

# Ask Gemini

Get feedback from Google's Gemini CLI on code, architecture decisions, or implementation approaches.

## Prerequisites

- Gemini CLI installed: `npm install -g @google/gemini-cli`
- Authenticated: run `gemini` once to login with Google account
- Verify: `gemini --version`

## When to Use

- Want a second opinion on code quality
- Need architectural review
- Comparing implementation approaches
- Code review before commit

## How to Invoke

The user will ask something like:
- "ask gemini what it thinks about this code"
- "get gemini's opinion on this approach"
- "demande à gemini de reviewer ce fichier"

## Execution

### For file review
```bash
gemini "Review this code and provide 3 specific improvements: $(cat <file_path>)"
```

### For architectural questions
```bash
gemini "<user's question about architecture or approach>"
```

### For comparing approaches
```bash
gemini "Compare these two approaches and recommend which is better: Approach A: <desc> vs Approach B: <desc>"
```

## Output Format

Present Gemini's response clearly to the user. If Gemini suggests improvements, summarize them as actionable items.

## Examples

### File review
**User**: "demande à gemini ce qu'il pense du semantic-skill-router.py"

```bash
gemini "Review this Python script for a semantic routing system. List 3 improvements for production use: $(cat scripts/semantic-skill-router.py)"
```

### Architecture question
**User**: "ask gemini if I should use Redis or in-memory cache"

```bash
gemini "Compare Redis vs in-memory caching for a CLI tool that routes user prompts. Consider: startup time, complexity, persistence needs."
```

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `gemini: command not found` | CLI not installed | `npm install -g @google/gemini-cli` |
| `Authentication required` | Not logged in | Run `gemini` interactively, login with Google |
| Response timeout | Large file or slow network | Reduce file size or retry |
| `Rate limit exceeded` | Too many requests | Wait 1 minute, retry |

## Notes

- Gemini has 1M token context window
- Default model: Gemini 2.5 Pro
- Timeout: allow up to 60s for response
- If response is cut off, Gemini may still be processing

## Skill Chaining

### Input Expected
- File path to review, OR
- Architecture/design question from user

### Output Produced
- **Format**: Markdown feedback from Gemini
- **Side effects**: None (read-only)

### Compatible Skills
- Can be used alongside `julien-workflow-advice-codex` for multiple AI opinions
- Use after writing code, before commit

### Tools Used
- `Bash` (usage: run gemini CLI command, timeout 60s)
