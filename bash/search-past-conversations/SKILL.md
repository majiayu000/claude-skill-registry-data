---
name: search-past-conversations
description: Grep prior conversation summaries by query string; ranked by recency + match score. Use when Alex assumes prior context that isn't in the current conversation.
allowed-tools:
  - "Bash(grep:*)"
  - "Bash(bash /datapool/bigweld-portal/skills/search-past-conversations/grep.sh:*)"
  - "Read"
---

# /search-past-conversations <query>

When Alex says something like "as we discussed last week" or "the SOQL we wrote for X" and you don't have it in the current conversation, invoke this skill before asking him to repeat himself.

## Implementation

The skill is a Bash script at `skills/search-past-conversations/grep.sh`. It:
1. Greps `conversations/*/*.summary.md` (the LLM-generated per-conversation summaries) for the query string (case-insensitive).
2. For each match, prints filename + 3 lines of context.
3. Returns top-20 matches.

## Invocation

```bash
bash /datapool/bigweld-portal/skills/search-past-conversations/grep.sh "<query>"
```

Or, if you're already in `/datapool/bigweld-portal/`:

```bash
bash skills/search-past-conversations/grep.sh "<query>"
```

## Output handling

Read the matches, identify the most-recent + most-relevant conversation, and:
- If a single match is clearly relevant → quote the relevant summary section back to Alex with a "from <date>" lead-in.
- If multiple matches are relevant → list them briefly (date + 1-line gist) and ask which one.
- If no matches → tell Alex "I don't see this in past conversation summaries — can you remind me?"

Do NOT pretend to remember if grep returned nothing.
