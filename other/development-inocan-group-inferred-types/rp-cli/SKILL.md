---
name: rp-cli
description: Reference for rp-cli usage patterns. Consult before calling rp-cli via Bash.
---

# rp-cli Reference

Quick reference for rp-cli commands. rp-cli is a proxy MCP client that lets AI agents access RepoPrompt's tools through shell commands.

## Prerequisites

- RepoPrompt must be running on your Mac
- MCP Server must be enabled in RepoPrompt settings
- CLI installed via Settings → MCP Server → "Install CLI to PATH"

## Basic Usage

```bash
rp-cli -e '<command>'                    # Execute single command
rp-cli -e '<cmd1> && <cmd2>'            # Chain commands
rp-cli -w <id> -e '<command>'           # Target specific window
```

## Common Commands

### Context Builder (Planning)

```bash
rp-cli -e 'builder "YOUR_INSTRUCTIONS" --response-type plan'
```

Creates implementation plan. Returns chat_id for follow-up.

### Chat (Continue Conversation)

```bash
rp-cli -e 'chat "YOUR_MESSAGE" --mode plan'
rp-cli -e 'chat "YOUR_MESSAGE" --chat-id "CHAT_ID" --mode plan'
```

Modes: `chat`, `plan`, `edit`

### Chat History

```bash
rp-cli -e 'chats list --limit 10'
rp-cli -e 'chats log --chat-id "CHAT_ID" --limit 10'
```

### File Selection

```bash
rp-cli -e 'select add path/to/file.ts'
rp-cli -e 'select remove path/to/file.ts'
rp-cli -e 'select set path/to/file1.ts path/to/file2.ts'
rp-cli -e 'select clear'
rp-cli -e 'select promote path/to/codemap.ts'   # Upgrade to full file
rp-cli -e 'select demote path/to/large.ts'      # Downgrade to codemap
```

### Workspace Context

```bash
rp-cli -e 'context'
rp-cli -e 'context --include prompt,selection,tokens'
```

### File Tree

```bash
rp-cli -e 'tree'
rp-cli -e 'tree --mode auto'
rp-cli -e 'tree --folders'
```

### Search

```bash
rp-cli -e 'search "pattern"'
rp-cli -e 'search "pattern" --extensions .ts'
```

### Code Structure

```bash
rp-cli -e 'structure src/auth'
rp-cli -e 'map src/components'
```

### Read Files

```bash
rp-cli -e 'read path/to/file.ts'
rp-cli -e 'read path/to/file.ts --start-line 45 --limit 100'
```

### Workspace Management

```bash
rp-cli -e 'workspace list'
rp-cli -e 'workspace tabs'
rp-cli -e 'workspace tab "TAB_NAME"'
rp-cli -e 'workspace switch "PROJECT_NAME"'
```

## Chaining Commands

```bash
rp-cli -e 'workspace MyProject && select set src/ && context'
```

## Output Redirection

```bash
rp-cli -e 'context > /tmp/context.md'
```

## Bash Execution Notes

- Use single quotes around the `-e` argument
- Escape single quotes in instructions: replace `'` with `'\''`
- No sandbox required (communicates via local socket)

## Parsing Chat Log

When fetching chats with `chats log`:
- `role: "user"` = task context (ignore)
- `role: "assistant"` = architectural plan (parse this)
- Always use the **last** assistant message

## Troubleshooting

**Connection failures**: Ensure RepoPrompt is running and MCP Server is enabled

**Command not found**: Run `rp-cli --version` to verify installation

**Operations need approval**: Some operations require approval in RepoPrompt UI

## More Information

- Help: `rp-cli --help`
- Command details: `rp-cli -d <command>`
