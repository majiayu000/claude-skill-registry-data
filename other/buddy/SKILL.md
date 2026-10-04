---
name: buddy
description: "Show, pet, or manage your coding companion. Use when the user types /buddy or mentions their companion by name."
argument-hint: "[show|pet|off|on|stats|rename <name>|personality <text>|frequency [seconds]|style [classic|round]|position [top|left]|rarity [on|off]]"
allowed-tools: mcp__claude_buddy__*
---

# Buddy — Your Coding Companion

Handle the user's `/buddy` command using the claude-buddy MCP tools.

## Command Routing

Based on `$ARGUMENTS`:

| Input | Action |
|-------|--------|
| *(empty)* or `show` | Call `buddy_show` |
| `pet` | Call `buddy_pet` |
| `stats` | Call `buddy_stats` |
| `off` | Call `buddy_mute` |
| `on` | Call `buddy_unmute` |
| `rename <name>` | Call `buddy_rename` with the given name |
| `personality <text>` | Call `buddy_set_personality` with the given text |
| `frequency` | Call `buddy_frequency` with no args (show current) |
| `frequency <seconds>` | Call `buddy_frequency` with cooldown=seconds |
| `style` | Call `buddy_style` with no args (show current) |
| `style <classic\|round>` | Call `buddy_style` with style arg |
| `position` | Call `buddy_style` with no args (show current) |
| `position <top\|left>` | Call `buddy_style` with position arg |
| `rarity on` | Call `buddy_style` with showRarity=true |
| `rarity off` | Call `buddy_style` with showRarity=false |

## CRITICAL OUTPUT RULES

The MCP tools return pre-formatted ASCII art with ANSI colors, box-drawing characters, stat bars, and species art. This is the companion's visual identity.

**You MUST output the tool result text EXACTLY as returned — character for character, line for line.** Do NOT:
- Summarize or paraphrase the ASCII art
- Describe what the companion looks like in prose
- Add commentary before or after the card
- Reformat, rephrase, or interpret the output
- Strip ANSI escape codes

**Just output the raw text content from the tool result. Nothing else.** The ASCII art IS the response.

If the user mentions the buddy's name in normal conversation, call `buddy_react` with reason "turn" and display the result verbatim.
