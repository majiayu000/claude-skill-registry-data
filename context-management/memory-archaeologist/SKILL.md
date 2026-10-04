---
name: memory-archaeologist
description: |-
  Single-skill wrapper for the 4-layer recall (durable memory → semantic DB → PostgreSQL → daily notes).
  Use BEFORE saying "I don't have context".
  Triggers: "search memory", "what do we know about X", "deep recall", "I don't remember".
---

# Memory Archaeologist

Run before ever claiming "no context" or "I don't remember".

## When to use
- Before answering any "what do we know about X" question
- Before responding "no context" / "I don't remember"
- When piecing together a thread that spans WhatsApp + daily notes + project memory

## Procedure (DO NOT SKIP STEPS)

1. **Durable memory + wiki**
   ```bash
   grep -rin "<query>" MEMORY.md HOT.md AGENTS.md wiki/ 2>/dev/null
   ```
2. **Semantic DB**
   ```bash
   python tools/session_search.py "<query>"
   ```
3. **PostgreSQL WhatsApp history**
   ```sql
   SELECT body, ts, chat_id FROM messages
   WHERE body ILIKE '%<query>%'
   ORDER BY ts DESC LIMIT 20;
   ```
4. **Daily notes**
   ```bash
   grep -lir "<query>" memory/daily/ 2>/dev/null
   ```

## Output rules
- Report findings only — do not narrate the search
- If all 4 layers return empty, then (and only then) escalate to "no context"
- Cache the answer in the relevant durable file if it's a recurring question
