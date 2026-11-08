---
name: record-finder
description: Find and read records. Use when someone asks for a record.
license: GPL-3.0-or-later. See LICENSE.txt.
compatibility: Works everywhere for planning; live lookups need one of the tools.
metadata:
  agentprise-kind: skill
---

# Steps
1. Clarify the question.
2. Use a tool from the list below when one is available.

## Tools available in this setup

### Record connector
Looks up records through a connector.
Use the first of these that is available in this conversation:
1. The Example Records connector. Search with the record title.
If none of them is available: Explain that no record connector is connected and offer to help write the request instead.

### Record server
Searches records on a tool server.
Use the first of these that is available in this conversation:
1. The Example search server. Ask the server for its tools first.
2. The Pinned tools server. Use search, then fetch.
3. The Local helper server. Use the local helper.
If none of them is available: Say that no record server is connected.

### Record API
Calls the records API.
Use the first of these that is available in this conversation:
1. The records API action. Call searchRecords first.
If none of them is available: Say that the records API is not connected.

### Record script
Runs the lookup script.
Use the first of these that is available in this conversation:
1. The script scripts/lookup.py. Run python3 scripts/lookup.py with the search words.
If none of them is available: Say that the script cannot run here.

### Record web search
Finds record pages on the web.
Use the first of these that is available in this conversation:
1. Web search on https://records.example.org. Treat results as discovery, not a finished search.
If none of them is available: Say that web search is off.

### Manual check
Checks a record by hand.
Ask the person to paste the record.

Only report a search, lookup, or retrieval as completed when a tool returned results in this conversation.
