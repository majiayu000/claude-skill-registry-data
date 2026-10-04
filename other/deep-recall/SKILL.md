---
name: deep-recall
description: |-
  4-layer recall procedure (durable → semantic → PostgreSQL → daily notes) before claiming "no context".
  Invoke when user explicitly asks "do you remember", "what did we discuss about X", "search history".
  NOT a general assistant — only fires when recall is the explicit task. Drop the prior "use proactively" rule.
  Triggers: "do you remember", "what did we discuss", "when did", "find that conversation about".
---

# Deep Recall

**Rule: Never say "I don't have context" without searching all sources first.**

## Search Order (mandatory, in sequence)

### 1. Memory Search (semantic)
```
memory_search(query="<topic>")
```
Searches MEMORY.md + memory/*.md + indexed session transcripts.

### 2. Session Search (FTS + PostgreSQL + daily notes)
```bash
python3 tools/session_search.py "<query>" --limit 10 --days 30
```
Full-text search across SQLite FTS5 index, WhatsApp DB, and daily notes.

### 3. PostgreSQL Direct (for specific conversations)
```python
import os, psycopg2
conn = psycopg2.connect(os.environ['PA_DB_URL'])
cur = conn.cursor()
cur.execute("""
    SELECT body, ts, chat_id, is_from_me 
    FROM messages 
    WHERE body ILIKE %s 
    AND ts > NOW() - INTERVAL '30 days'
    ORDER BY ts DESC LIMIT 10
""", ('%keyword%',))
```

### 4. Daily Notes Grep (for dated events)
```bash
grep -rn "<keyword>" memory/daily/ | tail -20
```

### 5. WhatsApp DM Context Files
```bash
grep -rn "<keyword>" memory/whatsapp/dms/*/context.md
```

## When to Trigger

- Any question starting with "did we", "when did", "what about", "do you remember"
- Before saying "I don't have context on this"
- Before saying "I'll need to check"
- When the owner references something from a past conversation
- When another PA asks about a previous interaction

## Output Rules

- If found: cite the source (file:line or timestamp)
- If not found after all 5 searches: say "I searched memory, WhatsApp history, and daily notes — no match found"
- Never say "I don't remember" without running all searches
- If partial match: share what was found and ask for clarification

## Common Recall Failures to Avoid

- Saying "let me check" and then not actually checking
- Searching only one source and giving up
- Assuming something wasn't discussed because it's not in MEMORY.md (check PostgreSQL!)
- Forgetting that WhatsApp group messages exist in the DB too
- Not checking DM context files in `memory/whatsapp/dms/`
