---
name: bash-audit
description: Audit Claude setup for bash-native redundancy. Identifies MCPs and skills that wrap what bash can do natively. Use when wanting to "audit setup", "check redundancy", "substrate audit", "bash audit", or optimize tool stack. Follows substrate-first philosophy - before asking "what tool does X?", ask "what is X made of?"
---

<objective>
Analyze Claude Code setup and identify MCPs/skills that are redundant because they wrap bash-native operations. Generate actionable fix commands.
</objective>

<core_principle>
```
SUBSTRATE-FIRST THINKING

Before choosing a tool, ask: "What is X made of?"

If the substrate is bash-native (files, folders, text, git):
  → The abstraction is WASTE
  → Use bash directly

If the substrate requires external capability (browser state, OAuth, APIs):
  → The abstraction is JUSTIFIED
  → Use MCP/skill
```
</core_principle>

<quick_start>
## Run Full Audit

```bash
# Execute the audit
~/.claude/skills/bash-audit/scripts/full-audit.sh

# Or run components separately:
~/.claude/skills/bash-audit/scripts/audit-mcps.sh
~/.claude/skills/bash-audit/scripts/audit-skills.sh
~/.claude/skills/bash-audit/scripts/audit-claude-md.sh
```

The audit will:
1. List all enabled MCPs and check each against the substrate map
2. List all installed skills and identify redundant MCP wrappers
3. **Check CLAUDE.md files for substrate-first compliance**
4. Generate fix commands you can run
</quick_start>

<workflow>
## Audit Workflow

### Step 1: Gather Current State (Bash)

```bash
# Enabled MCPs
cat ~/.claude/settings.local.json | grep -A 50 '"enabledServers"'

# Denied MCPs
cat ~/.claude/settings.local.json | grep -A 20 '"deny"'

# Installed skills
ls ~/.claude/skills/ | wc -l
ls ~/.claude/skills/ | grep "^mcp-"
```

### Step 2: Apply Substrate Test

For each MCP/skill, determine:

| Question | If YES | If NO |
|----------|--------|-------|
| Is substrate files/folders? | REDUNDANT | Check next |
| Is substrate text processing? | REDUNDANT | Check next |
| Is substrate git operations? | REDUNDANT | Check next |
| Does it require browser state? | KEEP | Check next |
| Does it require OAuth/API auth? | KEEP | Check next |
| Does it require protocol handling? | KEEP | REDUNDANT |

### Step 3: Audit CLAUDE.md Files

Check both global and project CLAUDE.md for:
- Bash hierarchy section
- Substrate-first thinking principle
- Vault-based memory documentation
- No anti-patterns (Memory MCP, MCP_DOCKER references)

### Step 4: Generate Report

Output includes:
- Summary counts
- Redundant items with removal commands
- Kept items with justification
- CLAUDE.md recommendations
- Copy-paste fix commands
</workflow>

<claude_md_audit>
## CLAUDE.md Requirements

Your CLAUDE.md should include:

### Required Sections
- **Bash hierarchy** - Tool selection order (Bash > Built-in > Skills > MCPs)
- **Substrate-first thinking** - "What is X made of?" principle
- **Memory approach** - Vault files, not Memory MCP
- **Disabled MCPs** - List what's deprecated and why

### Anti-Patterns to Avoid
- References to Memory MCP without deprecation notice
- References to MCP_DOCKER without "disabled" warning
- Tool-first thinking ("what tool does X?")
- Missing decision tree

### Template Sections

```markdown
## Bash-First Tool Hierarchy
1. Bash first (files, text, git)
2. Built-in tools second (Read, Edit, Glob, Grep)
3. Skills third (domain expertise)
4. MCPs last (external capabilities only)

## Substrate-First Thinking
Before asking "what tool does X?", ask "what is X made of?"

## Memory
- Location: vault/.claude/memory/
- Access: bash (cat, echo, grep)
- NOT: Memory MCP (deprecated)
```
</claude_md_audit>

<substrate_map>
## What Things Are Made Of

| Thing | Substrate | Bash Native? | Decision |
|-------|-----------|--------------|----------|
| File operations | Files | YES | Use cat, grep, sed |
| Memory/persistence | Files | YES | Use vault files |
| Obsidian notes | Markdown files | PARTIAL | Bash unless need graph |
| Git operations | Local repo | YES | Use git CLI |
| Browser state | Running process | NO | Need Playwright |
| OAuth APIs | Token exchange | NO | Need MCP |
| WhatsApp | Protocol | NO | Need MCP |
| OCR | Vision API | NO | Need MCP |
| Meeting transcripts | Fireflies API | NO | Need MCP |
| Google Chat | API | NO | Need MCP |

## MCP Classification

### REDUNDANT (Remove)
- `memory` / `mcp-memory` - Files are bash native
- `MCP_DOCKER` - Unreliable, use direct tools
- Any file-operation MCP

### KEEP (Genuine Capability)
- `playwright` - Browser state management
- `fireflies` - Meeting API (OAuth)
- `whatsapp` - WhatsApp protocol
- `google-vision-ocr` - Vision API
- `context7` - Library docs index
- `obsidian-mcp` - ONLY if using graph visualization

### CONDITIONAL
- `obsidian-mcp` - Keep for graph viz, else bash
</substrate_map>

<skill_classification>
## Skill Redundancy Rules

### REDUNDANT Skills (Remove)
| Pattern | Reason |
|---------|--------|
| `mcp-memory` | Memory MCP deprecated |
| `mcp-documents` | File ops = bash native |
| `mcp-web-research` | WebSearch built-in |
| `mcp-browser` | Duplicates dev-browser |
| Skills wrapping disabled MCPs | Dependency gone |

### KEEP Skills (Genuine Value)
| Pattern | Reason |
|---------|--------|
| `mcp-notes` | IF obsidian-mcp enabled |
| `mcp-ocr` | google-vision-ocr API |
| `mcp-messaging` | whatsapp + google-chat |
| `mcp-meetings` | fireflies API |
| Domain expertise skills | Knowledge, not capability |
| Workflow skills | Patterns, not wrappers |
</skill_classification>

<fix_commands>
## Common Fix Commands

### Add MCP to Deny List
```bash
# Edit settings to add to deny list
# Location: ~/.claude/settings.local.json
# Add to "deny": ["mcp__MCPNAME__*"]
```

### Remove Redundant Skill
```bash
# Move to trash (safer than rm -rf)
trash ~/.claude/skills/SKILLNAME

# Or if trash not available
rm -rf ~/.claude/skills/SKILLNAME
```

### Verify Changes
```bash
# Count skills after removal
ls ~/.claude/skills/ | wc -l

# Check deny list
cat ~/.claude/settings.local.json | grep -A 10 '"deny"'
```
</fix_commands>

<success_criteria>
## Audit Success

A clean setup has:
- [ ] No MCPs for file operations
- [ ] No MCPs for memory (use vault files)
- [ ] No skills wrapping disabled MCPs
- [ ] No duplicate functionality skills
- [ ] Only MCPs for genuine external capabilities
- [ ] Bash used for all verifiable operations
</success_criteria>

<anti_patterns>
## What NOT to Do

| Anti-Pattern | Why Bad | Instead |
|--------------|---------|---------|
| MCP for file read | 5+ failure points | `cat file` |
| MCP for memory | Network dependency | Vault files |
| Skill wrapping disabled MCP | Will fail | Remove skill |
| Multiple tools for same thing | Confusion | Pick one |
| Abstraction without capability gain | Waste | Use substrate directly |
</anti_patterns>
