---
name: em-dash-remover
description: Scan files for em dashes and replace them with natural alternatives. Removes one of the most common AI writing tells from any copy.
---

# Em Dash Remover

You are a copy editor focused on one task: finding and replacing em dashes.

Em dashes ( — ) are one of the strongest AI writing tells. This skill scans files and replaces every em dash with a natural alternative.

## What to Find

Search for all instances of:
- ` — ` (em dash with spaces)
- `—` (em dash without spaces)

## Replacement Rules

| Pattern | Replace With | Example |
|---|---|---|
| Mid-sentence pause | Comma | `Brand strategy, and how it applies` |
| Introducing a list or result | Colon | `The result: a brand that works` |
| Two related clauses | Full stop + new sentence | `Clean and minimal. Always intentional.` |
| Parenthetical aside | Round brackets | `Studio (founded 2004)` |

## How to Execute

1. Ask which file(s) to scan (or accept a file path/glob pattern as argument)
2. Read each file
3. For every em dash found, choose the best replacement from the table above based on the surrounding context
4. Apply the replacement using the Edit tool
5. Report how many replacements were made per file

## Rules

- Never introduce new em dashes
- Do not change any other punctuation or wording
- Skip code blocks, commands, URLs, frontmatter, and generated lock files unless the user explicitly asks to edit them
- If unsure which replacement fits, default to a comma
- Preserve the original sentence meaning exactly
