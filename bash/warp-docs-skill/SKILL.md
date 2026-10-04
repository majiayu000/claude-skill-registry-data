---
name: warp-docs-skill
description: USE THIS SKILL for any question about Warp terminal — agents, AI features, configuration, keybindings, workflows, or the Warp platform API. This skill has complete local documentation — do not use web search or WebFetch instead.
---

# Warp Terminal Documentation Skill

**Intelligent documentation access for Warp - the modern, AI-powered terminal.**

## Path Resolution

Use `${CLAUDE_SKILL_DIR}` to reference this skill's directory — it resolves automatically whether the skill is symlinked or local.

## Overview

This skill provides smart-routed access to comprehensive Warp documentation:

- **92 pages** of official documentation from docs.warp.dev
- **11 sections** covering agents, code, terminal, integrations, and more
- **3-tier architecture** for optimal context usage and fast lookups

## Documentation Update Requests

When user requests to update documentation (trigger: "update warp documentation"):

### Update All Documentation

```bash
"${CLAUDE_SKILL_DIR}/scripts/update-docs.sh"
```

**What Gets Updated:**

1. **Quick Reference** - Tier 1 (~19KB) - Key features from priority pages
2. **Section Index** - Tier 2 (~25KB) - Organized section summaries
3. **Full Documentation** - Tier 3 (~940KB) - Complete documentation with grep markers

**Duration:** ~60 seconds (fetches all pages with rate limiting)

**Error Handling:**

- Script logs each page fetch status
- Failed pages are skipped with warnings
- Aborts if <10 pages fetched (critical failure)

**After Update:**

1. Confirm all tiers generated
2. Report page count and any failures
3. New documentation immediately available (hot-reload)

## 3-Tier Routing

### Tier 1: Quick Reference

- **File:** `references/quick-reference.md` (~19KB)
- **Covers:** Getting started, keyboard shortcuts, agent basics, terminal essentials
- **Use when:** Quick answers, common features, getting started questions

**Example queries:**

- "How do I install Warp?"
- "What are the keyboard shortcuts in Warp?"
- "How do I use Warp agents?"
- "What shells does Warp support?"

**Access pattern:**

```bash
# Read the quick reference directly
cat references/quick-reference.md
```

### Tier 2: Section Index

- **File:** `references/section-index.md` (~25KB)
- **Covers:** All 92 pages organized by section with titles and descriptions
- **Use when:** Finding specific topics, understanding documentation structure

**Example queries:**

- "What features are in the Terminal section?"
- "Where is documentation about Warp Drive?"
- "What integrations does Warp support?"
- "List all agent-related documentation"

**Access pattern:**

```bash
# Find pages in a section
grep -A 30 "## AGENTS" references/section-index.md

# Find a specific topic
grep -i "keyboard" references/section-index.md
```

### Tier 3: Full Documentation

- **File:** `references/full-docs.txt` (~940KB)
- **Covers:** Complete documentation with grep markers per page
- **Use when:** Detailed information, specific page content, deep dives

**IMPORTANT:** Never load entire file. Use grep markers for targeted extraction.

**Example queries:**

- "How do I configure SSH in Warp?"
- "What are all the options for custom themes?"
- "Explain Warp's block system in detail"
- "How does the Agent API work?"

**Access patterns:**

```bash
# Find and extract a specific page
grep -A 100 "^PAGE: /terminal/blocks" references/full-docs.txt

# Find all pages in a section
grep "^PAGE:" references/full-docs.txt | grep "/agents/"

# Search for a keyword across all docs
grep -n "keyboard shortcut" references/full-docs.txt

# Extract complete page between separators
sed -n '/^PAGE: \/getting-started\/keyboard-shortcuts/,/^═\{80\}$/p' references/full-docs.txt
```

## Section Coverage

| Section                     | Pages | Description                                                      |
| --------------------------- | ----- | ---------------------------------------------------------------- |
| AGENTS                      | 24    | AI-powered terminal agents for command generation and automation |
| AMBIENT-AGENTS              | 5     | Background agents with scheduled tasks and secrets               |
| CODE                        | 9     | Code editing, review, and codebase context features              |
| COMMUNITY                   | 2     | Community programs and preview features                          |
| GETTING-STARTED             | 8     | Installation, setup, keyboard shortcuts, shell configuration     |
| INTEGRATIONS                | 5     | GitHub Actions, Linear, Slack integrations                       |
| KNOWLEDGE-AND-COLLABORATION | 15    | Warp Drive, notebooks, workflows, teams, sharing                 |
| PLATFORM                    | 13    | Agent API, SDK, CLI, and platform development                    |
| PRIVACY                     | 3     | Privacy policies and data handling                               |
| SUPPORT-AND-BILLING         | 12    | Billing, plans, troubleshooting                                  |
| TERMINAL                    | 59    | Terminal features: blocks, themes, input, windows, more          |

## Query Routing Examples

```
"How do I get started with Warp?"
→ Tier 1: quick-reference.md (Getting Started section)

"What keyboard shortcuts are available?"
→ Tier 1: quick-reference.md (Keyboard Shortcuts section)

"What's in the Terminal section?"
→ Tier 2: section-index.md (scan TERMINAL section)

"How do I configure custom themes?"
→ Tier 3: grep "^PAGE: /terminal/appearance/custom-themes" full-docs.txt

"Explain how Warp agents work"
→ Tier 1 first, then Tier 3 for details: grep "^PAGE: /agents/" full-docs.txt

"What MCP servers work with Warp?"
→ Tier 3: grep "^PAGE: /ambient-agents/mcp-servers" full-docs.txt
```

## Response Format

**Always cite tier and source:**

- "From Quick Reference: ..."
- "From Section Index (Agents): ..."
- "From Full Docs (/terminal/blocks): ..."

**Provide context:**

- Include relevant keyboard shortcuts when applicable
- Mention related features or pages
- Link to official docs URL when appropriate: https://docs.warp.dev/path

## Best Practices

### DO

- Start with Tier 1 (quick-reference.md) for common questions
- Use Tier 2 (section-index.md) to find relevant pages
- Use targeted grep/sed for Tier 3 (never load full file)
- Cite sources in responses
- Mention keyboard shortcuts when relevant

### DON'T

- Load entire full-docs.txt file
- Answer from memory - always check current docs
- Skip tier routing (always start with appropriate tier)
- Ignore section organization when searching

## File Locations

```
warp-docs-skill/
├── SKILL.md
├── README.md
├── references/
│   ├── quick-reference.md     # Tier 1 (~19KB)
│   ├── section-index.md       # Tier 2 (~25KB)
│   └── full-docs.txt          # Tier 3 (~940KB)
└── scripts/
    └── update-docs.sh         # Wrapper (calls shared doc-builder)
```

## Maintenance

### Update Schedule

| Frequency                | Reason                                    |
| ------------------------ | ----------------------------------------- |
| Monthly                  | Warp releases new features regularly      |
| On request               | When user asks about features not in docs |
| After major Warp updates | New features and changes                  |

### Update Command

```bash
"${CLAUDE_SKILL_DIR}/scripts/update-docs.sh"
```

## Version

**Skill Version:** 1.0.0
**Documentation Source:** https://docs.warp.dev
**Total Pages:** 92
**Last Updated:** 2026-03-01

---

**Remember:** Check Tier 1 first → Check Tier 2 to find topics → Use Tier 3 for deep details
