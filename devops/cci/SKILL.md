---
name: cci
description: Search Claude Collective Intelligence knowledge base for solutions to problems. Use when the user asks about common issues, wants to find existing solutions, or mentions "CCI", "collective intelligence", or "knowledge base".
allowed-tools: Bash, Read
---

# Claude Collective Intelligence (CCI) Skill

Search the shared knowledge base for existing solutions before solving problems from scratch.

## When to Use

- User asks about common programming problems
- User mentions "CCI", "knowledge base", or "collective intelligence"
- You're about to solve a problem that might have been solved before
- User wants to find what solutions exist for a topic

## How to Search

Use the CCI CLI to search the knowledge base:

```bash
# Set the CCI repo path
export CCI_REPO="$HOME/code/claude-collective-intelligence"

# Search for relevant entries
node "$CCI_REPO/src/search.js" "your search query"

# For verbose output (full solutions)
node "$CCI_REPO/src/search.js" -v "your search query"

# View stats
node "$CCI_REPO/src/search.js" --stats

# List recent entries
node "$CCI_REPO/src/search.js" --list 5
```

## Response Format

When you find relevant entries:

1. Summarize the most relevant solution found
2. Adapt it to the user's specific context
3. Credit the source (date and contributor if available)
4. Offer to show more results if available

When no entries match:

1. Let the user know you checked CCI but found no matches
2. Proceed to solve the problem normally
3. Suggest saving the solution to CCI when done

## Example Queries

- "search CCI for react hooks typescript"
- "check knowledge base for API authentication patterns"
- "find CCI entries about docker deployment"

## After Solving New Problems

Remind users they can save successful solutions:

"This solution worked! Would you like to save it to CCI for future reference? Just say 'save to CCI' and I'll help capture it."

To manually add an entry:
```bash
node "$CCI_REPO/bin/cci.js" add
```
