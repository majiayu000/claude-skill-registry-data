---
name: claude-code-internals
description: Claude Code internals explorer
---

# Claude Code Internals Explorer

Analyze Claude Code's minified source to understand internal behavior and discover features.

## Important Caveats

- **Minified code**: Variable names are obfuscated (e.g., `UnB`, `cT0`)
- **Version-specific**: Findings may change between versions
- **Unofficial**: Discovered features may be unsupported/unstable
- **Token-intensive**: Mitigated via subagent delegation (see Workflow Phase 0)

## Quick Start

1. **Delegate exploration** to Explore subagent:
```
Task tool (subagent_type: Explore)
Prompt: "Run ~/.claude/skills/claude-code-internals/scripts/find_installation.sh,
        then search for [keyword] in cli.js. Report file paths and matching lines."
```

2. **Analyze findings** in main context (subagent returns summary)

3. **Iterate** with follow-up delegation if deeper investigation needed

## Workflow

### 0. Delegate Context Gathering

**Principle**: Initial exploration consumes tokens in subagent context, preserving main context for analysis.

Call Task tool with:
- `subagent_type`: `Explore`
- `prompt`: Specify search target and expected output format

Example delegation:
```
Find Claude Code installation path using ~/.claude/skills/claude-code-internals/scripts/find_installation.sh.
Then search for patterns related to [feature] in cli.js.
Return: installation path, version, matching lines with context.
```

The subagent will:
1. Execute shell scripts and grep commands
2. Filter and summarize findings
3. Return structured results to main context

Main agent then performs interpretation and decision-making.

### 1. Locate Source

Run `scripts/find_installation.sh` to find:
- `cli.js` path (minified JavaScript source, ~9.9MB)
- Current version
- Binary location

Typical path: `~/.npm/_npx/*/node_modules/@anthropic-ai/claude-code/cli.js`

### 2. Choose Investigation Type

| Goal | Approach |
|------|----------|
| **Specific feature** | Search for known keywords |
| **New version changes** | Compare with `known-features.md`, check release notes |
| **Hidden settings** | Search for setting patterns |
| **Beta features** | Search for beta headers |

### 3. Search Strategies

For minified code, search **string literals** (not variable names).

Quick example:
```bash
grep -E "anthropic-beta|context-management" cli.js
```

See `references/search-patterns.md` for comprehensive patterns by category.

### 4. Analyze Findings

When you find relevant code:

1. Note line numbers: `grep -n "pattern" cli.js`
2. Extract context: `sed -n 'LINE-10,LINE+10p' cli.js`
3. Trace related code by searching for adjacent strings
4. Compare with `references/known-features.md`

### 5. Document Discoveries

Update `references/known-features.md` with:
- New features found
- Changed defaults/thresholds
- New beta headers
- Corrected information

## Common Investigations

| Task | Approach |
|------|----------|
| Check feature enabled | `grep -n "feature_name" cli.js` -> examine conditional logic |
| Find default values | See `references/search-patterns.md` Settings section |
| Discover new commands | See `references/search-patterns.md` Commands section |
| Compare release notes | Search mentioned features -> compare with `references/known-features.md` |

## Resources

- **scripts/find_installation.sh**: Locate Claude Code installation
- **references/search-patterns.md**: Comprehensive grep patterns by category
- **references/known-features.md**: Baseline of known features for comparison

## Tips

1. **Start narrow**: Search specific terms before broad exploration
2. **Use line numbers**: `-n` flag helps locate code for context reading
3. **Chain searches**: Find one string, search nearby for related code
4. **Save findings**: Update known-features.md to track discoveries
5. **Version awareness**: Note version when documenting findings
