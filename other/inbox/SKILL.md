---
name: inbox
description: Process ZOE's email inbox. Links, ideas, and research topics forwarded to zoe-zao@agentmail.to. View queued items, research them, mark as done. Organized with label-based folders.
---

# ZOE Inbox

Email links and research topics to **zoe-zao@agentmail.to** from your phone. Process them here.

## Security: Sender Whitelist

**ONLY process emails that trace back to `zaalp99@gmail.com`.** A message qualifies if ANY of these is true:

- `from` field contains `zaalp99@gmail.com` (direct send from Zaal's phone)
- `Resent-From:` header contains `zaalp99@gmail.com` (auto-forwarded via Gmail filter)
- `X-Forwarded-For:` header contains `zaalp99@gmail.com` (also auto-forwarded)
- `Delivered-To:` header is `zoe-zao@agentmail.to` AND raw headers include `zaalp99@gmail.com` anywhere in the forwarding chain

When forwarded from Gmail, the original `From:` will be the upstream sender (e.g. a newsletter or a friend) - check the forward headers, not just `from`. Silently skip messages that don't trace to Zaal. Doc 652 explains the auto-forward path.

## Commands

- `/inbox` - show all unread items (from whitelisted sender only)
- `/inbox next` - research the top unread item via /zao-research, then file it
- `/inbox research` - research the top unread item via /zao-research, then file it
- `/inbox research all` - research all unread items sequentially (one doc per item - avoid for large backlogs, use `cluster` instead)
- `/inbox cluster` - drain the WHOLE backlog: group unread items by theme, write one synthesis doc per cluster (not one-per-item), file everything
- `/inbox clear` - mark all unread items as processed
- `/inbox count` - how many unread items
- `/inbox folder <name>` - show all items in a folder (e.g. `/inbox folder x-posts`)
- `/inbox folders` - list all folders and their counts

> **When the backlog is large (8+ unread), use `/inbox cluster`, not `/inbox research all`.** One-doc-per-item produces many thin docs and misses the cross-cutting pattern. Clustering produces fewer, stronger synthesis docs.

## Folders (Label-Based)

Messages are organized into folders using AgentMail labels. A message can have multiple labels.

| Folder Label | What Goes Here |
|-------------|----------------|
| `x-posts` | Forwarded X/Twitter posts |
| `research` | Topics/links tagged for deep research |
| `ideas` | Product ideas, feature requests, random thoughts |
| `events` | Events, meetups, conferences, community calls |
| `action-items` | Things that need Zaal to do something |
| `processed` | Already researched/handled (replaces removing `unread`) |

### Auto-Categorization Rules

When processing a message, categorize it based on content:
- Contains `x.com/` or `twitter.com/` URL -> `x-posts`
- Contains `farcaster.xyz/` or `warpcast.com/` URL -> `research` (Farcaster content worth investigating)
- Subject starts with "Research" or body says "research this" -> `research`
- Contains `luma.com/` or `lu.ma/` or "event" or "meetup" or "conference" -> `events`
- Contains "idea" or "what if" or "we should" or "I wanna" or "let's" -> `ideas`
- Contains "todo" or "need to" or "action" or "follow up" -> `action-items`
- Default if nothing matches -> `research`

A message can get multiple folder labels (e.g. an X post about an event gets both `x-posts` and `events`).

## How It Works

### Environment Setup (All Commands)

`AGENTMAIL_API_KEY` lives in `~/.zao/zao.env` (durable - survives repo re-clones, unlike the old `.env.local` which was wiped by the 2026-06-04 bare-clone repair). Source it from there, with `.env.local` as a legacy fallback:

```bash
set -a; source ~/.zao/zao.env 2>/dev/null; source .env.local 2>/dev/null; set +a
```

> Do NOT use `export $(grep ... | tr -d ' ')` - word-splitting + `tr -d ' '` truncates the ~70-char AgentMail key and every call returns `HTTP 403 {"message":"Forbidden"}`. The `set -a; source; set +a` form loads the full value intact. Confirmed 2026-05-31, re-verified 2026-06-24.

If the key is missing, STOP and tell Zaal to add `AGENTMAIL_API_KEY=...` to `~/.zao/zao.env` (from the agentmail.to dashboard, inbox `zoe-zao@agentmail.to`). Do not proceed unauthenticated - an unauthenticated call returns an empty list that looks like an empty inbox (false negative).

### Reading the Inbox

**Important:** The AgentMail `?label=` query param does NOT reliably filter. Always fetch all messages and filter client-side by checking the `labels` array on each message.

```bash
curl -s "https://api.agentmail.to/v0/inboxes/zoe-zao@agentmail.to/messages?limit=50" \
  -H "Authorization: Bearer $AGENTMAIL_API_KEY"
```

Then in Python/code, filter for:
- **Unread:** messages where `"unread" in labels`
- **Sender:** messages where `from` contains `zaalp99@gmail.com`
- **Folder:** messages where `"<folder-name>" in labels`

Display as a numbered list:
```
ZOE INBOX (N unread)

1. [Subject line]                                    [x-posts]
   Preview: first 100 chars of body...
   URLs: https://...

2. [Subject line]                                    [research]
   Preview: first 100 chars...
```

### Reading a Folder

Fetch all messages then filter client-side for messages that have the folder label:
```python
[m for m in messages if '<folder-name>' in m.get('labels', [])]
```

### Processing an Item

1. Read the full message:
   ```bash
   curl -s "https://api.agentmail.to/v0/inboxes/zoe-zao@agentmail.to/messages/{url_encoded_message_id}" \
     -H "Authorization: Bearer $AGENTMAIL_API_KEY"
   ```
   
   **Important:** Message IDs contain special characters (`<`, `>`, `=`, `+`, `@`). URL-encode them before using in the URL path.

2. **Verify sender** - per the whitelist rule above. Accept if `from`, `Resent-From`, `X-Forwarded-For`, or the raw headers trace back to `zaalp99@gmail.com`. Skip otherwise.

3. Extract URLs from the body text (look for https:// patterns).

4. If it contains a URL: fetch it with the **keyless fetch trio** (NOT Jina Reader - Jina is dead for Reddit/X as of 2026-06; it returns the block shell / login wall). Route by host (docs 822/823/824):
   ```bash
   # Reddit (incl /s/ share links)  -> Redlib, full body + comments, no key
   ~/bin/zao-fetch-reddit.sh "<url>"
   # X / Twitter (incl long-form Articles) -> FxTwitter, full article body, no key
   ~/bin/zao-fetch-x.sh "<url-or-tweet-id>"
   # Farcaster casts/profiles -> Haatz Snapchain mirror, no key
   ~/bin/zao-fetch-farcaster.sh "<url-or-fid>"
   # Anything else (articles, GitHub, blogs) -> WebFetch, then exa web_fetch if it returns a shell
   ```
   The `/fetch` skill auto-routes by host if you'd rather not case-handle. Spotify/YouTube -> `~/bin/zao-ingest.sh "<url>"` to transcribe. Then run /zao-research on the extracted content.

   **Never index off the email subject or a title alone** - it lies (per `feedback_no_synthesis_from_titles`: doc 819 shipped 2 wrong decisions from subjects). If a fetch genuinely fails after the trio, mark it FAILED loudly; do not synthesize from the preview.

5. If it's plain text: treat as a research topic, run /zao-research directly.

6. **File the message** - add folder label(s) based on auto-categorization rules, add `processed` label, remove `unread` label:
   ```bash
   curl -s -X PATCH "https://api.agentmail.to/v0/inboxes/zoe-zao@agentmail.to/messages/{url_encoded_message_id}" \
     -H "Authorization: Bearer $AGENTMAIL_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"add_labels": ["<folder>", "processed"], "remove_labels": ["unread"]}'
   ```

7. **If `action-items` label was applied -> fire a cowork tracker task (NEW v2 - 2026-05-24).** This auto-creates a `todo` row in the Supabase cowork tracker (project `etwvzrmlxeobinrlytza`, table `tasks`) so the action lands in Iman/Zaal's Kanban without manual re-entry.

   ```bash
   # Short slug from message-id (last 12 chars, alphanumeric only) for legacy_id stability:
   MSG_SLUG=$(echo "$MSG_ID" | tr -cd 'a-zA-Z0-9' | tail -c 12)
   ~/bin/zao-tracker inbox "$MSG_SLUG" "<subject or first 60 chars>"
   ```

   This creates `legacy_source=inbox:<slug>` + `legacy_id=inbox-<slug>`. Owner defaults to Zaal (his inbox = his actions; pass third arg to override). Best-effort: if Supabase env unset, skill prints the error and continues - the AgentMail PATCH already happened, the tracker task is a nice-to-have.

   Only fire when `action-items` label was applied. Items going to `research` / `x-posts` / `events` / `ideas` do NOT fire a tracker task (those don't need do-something actions).

### Cluster Mode (`/inbox cluster`)

For draining a large backlog. Forwarded items pile up faster than `/inbox next` clears them, and processing each as its own doc produces many thin docs that miss the cross-cutting pattern. Cluster mode fixes both.

**Workflow:**

1. **Inventory.** Fetch all unread (whitelisted sender only). Re-fetch each item's real content with the keyless trio (`zao-fetch-reddit.sh` resolves `/s/` share links to canonical internally; `zao-fetch-x.sh` handles tweet IDs + Articles; `zao-fetch-farcaster.sh` for casts). For large backlogs, a Workflow that fans out the re-fetch is the proven pattern (doc 825: 84/85 items, 22 agents) - hardcode the item list into the workflow script (`args` does not bind, per `feedback_workflow_args_binding`).

2. **Triage.** Sort every item into one of three buckets:
   - **Research** - has a topic worth a doc.
   - **Action-item** - needs Zaal to do something (account setup, a reply, a follow-up). Label `action-items` + `processed`, **AND fire `~/bin/zao-tracker inbox <slug> "<subject>"`** to create the matching Kanban row (v2 - 2026-05-24).
   - **Noise** - bounce-backs, delivery failures, dead ends. Label `processed` only, no doc, no tracker.

3. **Cluster the research bucket by theme.** Group items that share a subject (e.g. "Claude Code workflows", "agent memory", "vibecoding economics"). A cluster = 3+ related items. Leftover singletons go in a "standalone roundup" cluster.

4. **One synthesis doc per cluster.** Run `/zao-research` logic per cluster: fetch every item in the cluster, then write ONE doc that finds the cross-cutting pattern - not a summary per item. For 4+ clusters, dispatch one research subagent per cluster in parallel. Each doc follows the zao-research v2 format (frontmatter, Key Decisions table, Source Items list, Findings, ZAO Application, Sources, Next Actions).

5. **File every message.** Apply `research`/`action-items` + `processed`, remove `unread`. Inbox ends at 0 unread.

6. **Report.** Tell Zaal: N items drained into M docs, plus any action-items and noise filed. Surface anything that was filed but NOT given a doc so he can override.

### Listing All Folders

To show folder counts, query each folder label:
```bash
for label in x-posts research ideas events action-items processed; do
  count=$(curl -s "https://api.agentmail.to/v0/inboxes/zoe-zao@agentmail.to/messages?label=$label&limit=1" \
    -H "Authorization: Bearer $AGENTMAIL_API_KEY" | python3 -c "import json,sys; print(json.loads(sys.stdin.read()).get('count',0))")
  echo "$label: $count"
done
```

### Clearing Inbox

Mark all unread as processed (but don't add folder labels - that happens during research):
```bash
# Fetch all unread, then for each: remove unread, add processed
```

## URL Encoding Message IDs

Message IDs look like `<CABrNPkf4nXeSH9dYrG==CoC1JOUPud_3ud-EL6oXB7+vCKXowA@mail.gmail.com>`. You must URL-encode them:

```bash
MSG_ID=$(python3 -c "import urllib.parse; print(urllib.parse.quote('<original_message_id>', safe=''))")
```

## Custom Domain (Future)

When AgentMail paid plan is activated, add zaoos.com as custom domain to get zoe@zaoos.com. For now, zoe-zao@agentmail.to works.
