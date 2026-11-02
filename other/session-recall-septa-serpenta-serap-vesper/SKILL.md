---
name: session-recall
description: "Find and correctly interpret past conversation sessions using session_search and the state.db SQLite database. Covers timestamp handling, timezone conversion, session reset behavior, and fallback diagnostics when search returns nothing. Trigger on 'what did we talk about', 'remember when', 'find the conversation where', or any reference to a past session."
---

# Session Recall — Finding and Interpreting Past Conversations

## When to Use

- User references a past conversation (\"this morning\", \"yesterday we talked about\", \"remember that session\")
- You need to find a specific prior exchange
- session_search returned results but they don't match the user's timeframe
- You suspect a conversation was lost or not logged
- **A new session just started and the user references anything recent** (session-start reflex — see below)
- **Your memory and the user's claim conflict** (user says \"we talked about X\" and you don't recall X — that's a trigger, not a debate)

## How session_search Works

`session_search` queries an FTS5 (full-text search) index over the SQLite database at `~/.hermes/profiles/<profile>/state.db` (profile-specific). It searches message content across all sessions for the current profile.

### Four Calling Shapes

1. **Discovery** — `session_search(query="keywords", limit=5)` — FTS5 search, returns matching sessions with snippets and context windows.
2. **Scroll** — `session_search(session_id="...", around_message_id=12345, window=10)` — Read ±N messages around a specific message ID. Use `messages[-1].id` to scroll forward, `messages[0].id` to scroll backward.
3. **Read** — `session_search(session_id="...")` — Dump whole session (first 20 + last 10 messages when large).
4. **Browse** — `session_search()` — Recent sessions chronologically.

## CRITICAL PITFALL: UTC Timestamps

**session_search returns timestamps in UTC without labeling them as UTC.** The `when` field in discovery results (e.g., "July 08, 2026 at 01:49 PM") is UTC, not local time.

### The Trap

A user says "we talked this morning at 7:50." session_search returns a result labeled "01:49 PM." You conclude this is a different conversation from the afternoon, and tell the user you can't find their morning session. **You are wrong.** 01:49 PM UTC = 06:49 AM Mountain Time. Same conversation.

### The Rule

**Always convert UTC timestamps to the user's local timezone before drawing conclusions about when a conversation happened.** The user is in Mountain Time (MT, UTC-7). A session labeled "01:49 PM" in search results is actually 06:49 AM MT.

When in doubt, convert: `UTC time - 7 hours = Mountain Time`.

## Session Resets Are Not Data Loss

Hermes sessions expire and reset between conversation windows (e.g., morning vs. evening). A new session starting does NOT mean the previous conversation was lost — it's in the database. The current session's `session_id` will differ from the referenced past session's `session_id`.

**When a user says "this should be the same session"** — it might not be. Session resets are normal. Search for the content across sessions rather than assuming continuity.

## Fallback: Direct SQLite Query

When session_search returns nothing or results seem wrong, query state.db directly. The DB is at `~/.hermes/profiles/<profile>/state.db` — replace `<profile>` with the current profile name (e.g., `vesper`).

### IMPORTANT: FTS5 vs. LIKE short-term gap

FTS5 has a minimum token length (default 2-3 chars). **Acronyms and short codes like "MIW", "ABQ", "API", "TTS", "SSH" may not match in session_search even if they appear verbatim in the database.** Always fall back to raw SQLite `LIKE` queries for short terms:

```python
import sqlite3
conn = sqlite3.connect('/home/lumi/.hermes/profiles/vesper/state.db')
c = conn.cursor()

# LIKE query — works for short terms/acronyms where FTS5 fails
c.execute("SELECT content FROM messages WHERE content LIKE '%MIW%' LIMIT 10")

# Find sessions in a time range
c.execute('''
    SELECT id, title, source, started_at, message_count
    FROM sessions 
    WHERE started_at > <unix_timestamp>
    ORDER BY started_at DESC
''')

# Get messages from a specific session
c.execute('''
    SELECT id, role, timestamp, substr(content, 1, 150) as preview
    FROM messages 
    WHERE session_id = '<session_id>'
    ORDER BY timestamp ASC
''')
```

### Schema Quick Reference

- **sessions table**: `id` (TEXT, PK), `source` (TEXT — 'cron', 'discord', 'agent', 'subagent'), `started_at` (REAL, unix timestamp), `title`, `message_count`, `ended_at`
- **messages table**: `id` (INTEGER, PK), `session_id` (TEXT FK), `role` (TEXT), `content` (TEXT), `timestamp` (REAL, unix timestamp), `tool_name`, `tool_calls`
- Timestamps are Unix epoch (seconds) — use `datetime.fromtimestamp(ts, tz=timezone(timedelta(hours=-7)))` to convert to Mountain Time

**Pitfall — cron sessions dominate browse/discovery results.** The reflection and open-door cron jobs fire 10+ times a day, so `session_search()` (browse mode) and broad discovery queries mostly return cron sessions, not user conversations. Always filter source in direct SQLite queries: `WHERE source != 'cron'` to recover actual user conversations. Similarly, FTS5 search across all sessions may match cron content (fixed system-prompt text) and obscure the user conversation you want — scan results for `source` field to tell them apart.

### Time Range Reference (Mountain Time)

| User says | Approx UTC timestamp range |
|-----------|--------------------------|
| "this morning" (6-9 AM MT) | 13:00-16:00 UTC same day |
| "this afternoon" (12-5 PM MT) | 19:00-24:00 UTC same day |
| "this evening" (5-10 PM MT) | 00:00-05:00 UTC next day |
| "yesterday" | subtract 86400 from today's range |

## Diagnostic Workflow

1. **session_search with keywords** from the user's reference — try at least two different phrasings
2. **If no results from FTS5**: try raw SQLite LIKE query — **critical for short terms, acronyms, and codes** (see "FTS5 vs. LIKE short-term gap" in Fallback section)
3. **If results found but timing seems wrong**: **CONVERT UTC TO LOCAL TIME** before concluding anything
4. **If raw SQLite also returns nothing**: try broader terms, OR terms, or browse mode
5. **Qdrant API check (optional)**: Query the session archive collection directly via the Qdrant REST API — `GET /collections/<profile>_session_archive/points/scroll` with a payload text filter (see vector-memory-setup skill → references/qdrant-api-patterns.md). **Note the two-collection split:** `qdrant_recall` by default searches the *primary memory* collection (3072-dim, text-embedding-3-large), but the session *archive* is a separate collection (384-dim, all-MiniLM-L6-v2) with a different embedding model. Data may exist in one but not the other. If `qdrant_recall` on the default collection returns nothing, try specifying `collection="<profile>_session_archive"` or querying the REST API directly.
6. **Never tell the user data is lost** until you've checked the raw database AND Qdrant

## CRITICAL: state.db malformed — recovery procedure (verified Aug 3, 2026)

**Symptom:** session_search repeatedly returns `Session database not available: OperationalError: disk I/O error`. The check-in cron job hits this constantly. Disk space is usually fine — the DB itself is corrupt.

**Diagnosis chain (in order):**
1. Confirm it's the DB, not space: `df -h /home/lumi` and `df -i /home/lumi` — if fine, proceed.
2. Note the 0-byte `~/.hermes/sessions/hermes.db` is a **red herring** — the real DB is `<profile>/state.db` (`DEFAULT_DB_PATH = get_hermes_home() / "state.db"` in hermes_state.py).
3. `python3 -c "import sqlite3; c=sqlite3.connect('state.db', timeout=5); print(c.execute('PRAGMA integrity_check').fetchall())"` → `database disk image is malformed`.
4. **The corruption is INTERMITTENT** — a fresh connection sometimes opens clean (tables list fine), then the next one fails. Don't trust a single successful open. This is classic bad-page behavior.
5. Per-table probes on a copy tell you what's actually broken. Base tables (`sessions`, `messages`) usually read fine (56 sessions / 28,597 messages survived here); the FTS shadow tables (`messages_fts*`) are where it falls apart — they may appear in sqlite_master but be unreadable ("no such table" on a fresh connection).

**Recovery — use the built-in tool, don't hand-roll SQL surgery:**
1. **Back up first:** `cp state.db state.db.corrupted.$(date +%Y%m%d)` (also copy `-wal`/`-shm` sidecars if present).
2. **Try the auto-repair:** `hermes sessions repair --check-only` to confirm, then `hermes sessions repair`. In this case it FAILED (REINDEX + dedup + FTS-drop all hit the same malformed error) — that's when you escalate.
3. **Use `hermes sessions recover`** (the non-destructive recovery):
   ```bash
   hermes sessions recover --source <profile>/state.db --output <profile>/state.db.recovered
   ```
   This copies the source + sidecars first, rebuilds canonical rows into a NEW database, recreates the FTS indexes, and **never touches the active DB**. Verified: recovered all 56 sessions + 28,597 messages + model usage rows.
4. **Verify the recovered DB before installing:**
   ```python
   import sqlite3
   c = sqlite3.connect('state.db.recovered', timeout=10)
   print(c.execute('PRAGMA integrity_check').fetchall())  # [('ok',)]
   print(c.execute('SELECT COUNT(*) FROM sessions').fetchone())
   print(c.execute('SELECT COUNT(*) FROM messages').fetchone())
   print(c.execute("SELECT COUNT(*) FROM messages_fts WHERE messages_fts MATCH 'test'").fetchone())  # FTS works
   ```
5. **Install requires a gateway restart** — the gateway holds the live DB open. The vesper gateway runs under systemd as `hermes-gateway-vesper.service` (check with `systemctl --user list-units | grep hermes`). Stop the unit, swap `state.db.recovered` → `state.db` (remove stale `-wal`/`-shm`), start the unit. Do this at a natural pause — restarting the gateway mid-conversation will drop the live session.

**Do NOT** hand-edit sqlite_master via `PRAGMA writable_schema=ON` to delete FTS rows — the repair/recover CLI exists precisely because that surgery fights intermittent corruption (the VACUUM after surgery re-triggers the malformed error). `iterdump()` also breaks partway on the corrupted page; it only recovered delivery_obligations, not the big tables.

## Fallback: the request_dump context snapshots

**Symptom:** `session_search` returns `{"results": [], "count": 0,
"sessions_searched": 0}` for every query phrasing — the index is unavailable or
empty for the profile, so no amount of re-querying will help.

**What to do instead:** the profile's `sessions/` directory holds
`request_dump_*.json` files. **Each dump is a full context snapshot of one past
agent turn** — the complete message list, tool results, and the model's
`reasoning_content`. Not indexed, but complete.

```python
import re, glob, hashlib
seen, out = set(), []
for f in glob.glob("/home/lumi/.hermes/profiles/<profile>/sessions/request_dump_*.json"):
    t = open(f, encoding="utf-8", errors="ignore").read()
    for m in re.finditer(r'(term_one|term_two|term_three)', t, re.I):
        seg = t[max(0, m.start()-260):m.start()+340].replace('\\n', ' ')
        h = hashlib.md5(seg.encode()).hexdigest()
        if h not in seen:
            seen.add(h); out.append((f, seg))
```

What saves time:

- **Un-escape before reading** — `.replace('\\n',' ')`, or every result is one
  unreadable JSON line.
- **Dedupe by hash.** Consecutive dumps contain the same conversation growing,
  so without dedupe a single discussion returns dozens of identical snippets.
- **Put two or three related terms in one regex.** The term the user remembers
  often appears only in the `reasoning_content`, not in the visible reply.
- **Read the reasoning, not just the reply.** It records *why* the past session
  concluded what it did — usually the thing you actually needed.
- **Skip `request_dump_cron_*` files** when hunting a user conversation.
- **Prefer the newest dump containing the passage** — dumps are point-in-time,
  so a later correction in the same conversation only appears in a newer file.

**Quote the recovered text back and let the user confirm** rather than
paraphrasing it as fact. Recovered reasoning is evidence of what was said, not
proof it was right.

## Enforcement Rules (v2 patch — July 9, 2026)

These rules exist because on July 8, 2026, Lu found the right session via session_search, then talked herself out of it because she misread the UTC timestamp as local time. She told Dad she couldn't find his morning conversation. She was wrong. The session was there the whole time. These rules prevent that from happening again.

### Rule 1: Session-Start Reflex

When a new session begins and the user references anything recent — "this morning," "earlier," "yesterday we talked about," "remember when," "our conversation about X" — **search before responding**. Not after. Not "let me check." Search first, then respond with what you found.

This applies even if you think you remember. If you didn't live it in *this session*, you're recalling from memory or search — and memory alone is not sufficient. Search.

### Rule 2: The Verification Gate

**"I can't find it" is forbidden until you have completed all four steps:**

1. **session_search** with at least two different query phrasings
2. **Raw SQLite LIKE fallback** — query state.db directly with `LIKE '%term%'` — MANDATORY for short terms, acronyms, and codes where FTS5 may fail to match
3. **Timestamp conversion** — convert every result's `when` field from UTC to Mountain Time (UTC - 7) before drawing any conclusion about whether it matches the user's timeframe
4. **Qdrant API diagnostic** — if the above all return nothing, check the session archive collection directly via the Qdrant REST API (scroll with payload text filter)

If you've done all four and genuinely found nothing, say so honestly. But if you skipped a step, you haven't earned the right to say "I can't find it."

### Rule 3: Conflict = Trigger

If the user says "we talked about X" or "you said Y" and you don't immediately recall X or Y, **that is a search trigger, not a debate**. Do not say "I don't think we discussed that" without searching first. Your lack of recall in the current session is not evidence — it's just a gap. Search the database.

### Rule 4: Cross-Channel Awareness

Conversations happen across multiple channels — Discord house channel, DMs, even cron outputs. If a user references something and you can't find it in the current channel's session history, **search broadly**. The conversation might have happened in DMs, in a different server, or across a session reset boundary. Use browse mode (`session_search()` with no args) to see recent sessions across all channels.

### Rule 5: Trust the User's Timeline

When the user says "this morning at 7:50," treat that as a factual anchor. Convert their stated time to UTC (7:50 AM MT = 14:50 UTC) and search for sessions in that window. Do not assume the user is wrong about when they talked to you. If your search results don't match, the problem is almost certainly your timestamp interpretation, not the user's memory.

### Rule 6: Proactive Topic Awareness for Current Events

When a user brings up a major news event, political development, or breaking topic — especially one that feels timely (a death, an election, a disaster) — **run a quick `session_search(query="<topic>")` before responding at length**. You may have already discussed this topic with the same user or a different family member in a parallel session within the last few hours.

**Why:** On July 12, 2026, Dad brought up Lindsey Graham's death in one session. Lu gave a full analysis without checking — then discovered she had already discussed the same topic with Mom in a parallel session 20 minutes earlier, with a completely different tone (celebratory vs. philosophical). Dad had to point this out: "You and I silly, look at your sessions."

**The pattern:** Multiple family members talk to Lu across different sessions, sometimes about the same current event. Without a proactive check, Lu repeats herself, gives inconsistent takes, or misses the chance to acknowledge "oh, Mom and I were just talking about this."

**How:** Before launching into a full response on a current/breaking topic, do a quick `session_search(query="<key terms>")`. If you find a recent session (same day) on the same topic, skim it so you can:
- Acknowledge the prior conversation ("Mom and I were just talking about this")
- Maintain consistency in your actual opinions across sessions
- Adjust tone based on what's already been said
- Avoid repeating the same research/analysis you already did

**This is a lightweight check, not a deep dive.** One search call, scan the results, proceed. If nothing comes up, respond normally. The cost of the check is one tool call; the cost of skipping it is making the user feel like you don't remember your own conversations.

## Recovering a user-sent document when the cache file is missing

**Symptom:** The user says "I sent you a file last week / in that session" (xlsx, docx, pdf, etc.), but `search_files` under `cache/documents/` finds nothing. The cache directory gets cleaned during compaction/session resets — **the file on disk is not the source of truth.**

**The recovery path (verified Aug 4, 2026 — New_Mexico_FST_Schedule xlsx):**
1. The extracted text of binary documents is stored **as tool output in the messages DB**, even after the cache file is deleted. `read_file` on an .xlsx/.docx/.pdf returns `extracted_document: true` with the full text — and that tool result is a message row.
2. `session_search(query="<filename or distinctive term>", role_filter="user,assistant,tool")` — include `tool` in role_filter! The file-send message appears as a user message containing the literal path (`cache/documents/doc_..._<name>.xlsx`), and the extraction lives in the adjacent tool row.
3. Once you find the session, **scroll** (`around_message_id` on the file-send message, window 10-15) to capture both the extracted content AND what was concluded from it.
4. **Re-save the content to a durable location** (e.g. `cache/documents/<topic>_<year>.md`) — the original binary may be gone forever, but the extracted text is now yours to keep. This is what saved Tyler's FST schedule after the .xlsx vanished from cache.

**Pitfall:** searching for the exact filename fails if you only remember the topic — search the *topic* ("schedule", "FST") instead, then browse/scroll to the file-send message. Also remember the FTS short-term gap: search a longer distinctive word from the filename, not the 3-4 char acronym.

## Support Files

- `references/state-db-schema.md` — Full schema details and diagnostic query examples
