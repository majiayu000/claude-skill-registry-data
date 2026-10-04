---
name: bonfire
description: Post episodes to the ZABAL Bonfire knowledge graph, or look up how Bonfire works. Bonfire is ZAO's knowledge-graph memory at zabal.bonfires.ai - meetings, decisions, captures flow in as natural-language episodes. The API key lives in ~/.zao/zao.env locally AND on the VPS at /root/cowork-zaodevz/agent/.env (key migration landed 2026-05-24, doc 754). This skill SSHes the VPS as the original architecture, which still works; the /meeting skill posts locally because the key is on the mac. Use when the user types /bonfire, asks to push something to the knowledge graph, asks "what is in our Bonfire", or asks how Bonfire posting works.
allowed-tools: Read Write Edit Bash
---

# /bonfire - ZABAL Bonfire knowledge graph

Post natural-language episodes into the ZABAL Bonfire so the knowledge graph
always has full context. Bonfire's auto-extraction turns each episode body into
graph nodes + edges.

Design doc: `research/agents/717-meeting-bonfire-posting-via-vps`. Bonfire
deep-dive: `research/agents/665-bonfires-deep-dive-zao-integration`. Bridge
design: `research/agents/680-meeting-skill-bonfire-bridge`.

## The key constraint - why this skill SSHes the VPS

The Bonfire API key (`BONFIRE_API_KEY`) is in TWO places as of 2026-05-24:
locally in `~/.zao/zao.env` (mac) AND on the VPS in
`/root/cowork-zaodevz/agent/.env`. The on-mac copy was an intentional
ergonomics move so local skills can curl Bonfire directly (see doc 754
which reverses doc 717 decision #3).

This skill still SSHes the VPS because (a) it was the original architecture
(doc 717), (b) callers running ON the VPS itself (ZOE / Hermes) have the
VPS env naturally, and (c) the SSH transport keeps working. For posting
from the mac, the `/meeting` skill takes the simpler local path via
`bonfire-episode.sh` (doc 754 patch).

| Fact | Value |
|------|-------|
| VPS | `root@187.77.3.104` (override with `BONFIRE_VPS`) |
| Key env file (on VPS) | `/root/cowork-zaodevz/agent/.env` - has `BONFIRE_API_KEY`, `BONFIRE_ID`, `BONFIRE_API_URL` |
| Key env file (local mac, since 2026-05-24) | `~/.zao/zao.env` - same vars; used by `/meeting` skill via `bonfire-episode.sh` (doc 754) |
| API base | `https://tnt-v2.api.bonfires.ai` |
| Write endpoint | `POST /knowledge_graph/episode/create` - works with the non-admin key |
| Read endpoint | `POST /vector_store/search` - works but returns `[]` until an admin runs labeling (doc 680) |
| ZAO's bonfire | `zabal.bonfires.ai` |

## When to fire

- The user types `/bonfire`
- "push this to the knowledge graph", "post this to Bonfire", "add this to our Bonfire"
- "what is in our Bonfire", "how does Bonfire posting work"
- After a `/meeting` run, to post the meeting episodes (the `/meeting` skill
  also does this itself via `bonfire-episode.sh`)

## Posting episodes

### Step 1 - build an episodes JSON

Write `/tmp/bonfire-episodes.json` in this shape:

```json
{
  "episodes": [
    {"name": "<stable unique id>", "body": "<self-contained natural-language prose>", "source_tag": "<short source label>"}
  ]
}
```

Rules for episode bodies:
- **Self-contained prose.** Each body must make sense alone - name the people,
  the date, the project. Bonfire auto-extraction reads prose, and a graph node
  must stand on its own. Good: "On 2026-05-19, Zaal and Arthur decided X."
  Bad: "decided X" (no context).
- **One idea per episode.** One decision, one action, one fact. Atomic episodes
  make a cleaner graph than one giant blob.
- **`name` is stable + unique.** A re-post with the same `name` updates rather
  than duplicates. Use a pattern like `meeting:2026-05-19:decision-1`.

### Step 2 - post via the VPS

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/bonfire-post.sh /tmp/bonfire-episodes.json
```

`bonfire-post.sh`:
1. Validates the JSON and **secret-scans every body locally** - aborts if any
   body contains a key-shaped string. Nothing leaves the machine until it is clean.
2. SSHes to the VPS, ships the episodes + the remote poster to `/tmp/` there.
3. Runs the POST on the VPS, where `/root/cowork-zaodevz/agent/.env` supplies
   the key. Cleans up the remote temp files.
4. Prints `Bonfire: N posted, M failed (of T)`.

Best-effort: a Bonfire failure prints `FAIL` per episode but never aborts a
larger workflow.

## Reading / querying Bonfire

The read path (`POST /vector_store/search`) works but currently returns `[]` -
the ZABAL bonfire's episodes are not searchable until an admin runs labeling
(`/labeling/hybrid` is 403 for the non-admin key). This is a known gate (doc
680). Until then, Bonfire is write-mostly: episodes ingest and grow the graph,
but programmatic recall is not yet live. ZOE's `bot/src/zoe/recall.ts`
`recall()` already handles this gracefully (falls back to a manual relay).

When the read path opens up, querying is `POST /vector_store/search` with
`{bonfire_ref: BONFIRE_ID, search_string: "<query>", limit: N}` - run it on the
VPS the same way (the key constraint is identical).

## Scripts

- `scripts/bonfire-post.sh` - local: validate + secret-scan + ship to VPS + run + report
- `scripts/bonfire-remote-post.sh` - runs ON the VPS: sources the env, curl-POSTs each episode

## Guardrails

- **Never read or print `BONFIRE_API_KEY`.** The skill only ever needs the file
  path, never the value. The key stays on the VPS.
- **Secret-scan every episode body before it leaves the machine.** A meeting
  transcript or a pasted note could carry a key.
- Do not commit episodes JSON with secrets. `/tmp/` only.
