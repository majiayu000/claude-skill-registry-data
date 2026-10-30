---
name: tg-check
description: >
  Telegram inbox analysis: read per-channel folders in inbox/, extract findings
  (API keys, tools, services, freebies, attachments) and report to the user.
  Triggered by "check tg", "what's new in tg". This is the READ
  side: the fetcher is not run, only already-downloaded messages are analyzed.
---

# tg-check — Telegram inbox analysis

> ⚠️ **Automation gets you banned very often.** Telethon/user-session — **a
> reserve only, not the base**: priority is reading already-downloaded files,
> official/web paths without a user session. No write operations through a
> user-session without an explicit owner command.

> **Important:** this skill is the read side. Fetch runs regularly on its own
> via `python your-telegram-fetcher fetch`.
> Here we only **read** the per-channel folders and **hand over** a digest to the user.

## Briefly

1. Look at `inbox/.fetch_stats.json` — what arrived in the last fetch.
2. Read the newest part of the group's folder — `inbox/<safe_title>/<YYYY-MM-DD-NNN>.md` (see Step 2).
3. Optionally look into `inbox/<safe_title>/attachments/` (or `<topic>/attachments/`) if there were attachments.
4. Extract findings (API keys, tools, services, promocodes, freebies, files).
5. Report to the user per group + a general "what is worth checking".

Every inbox part is **under 100 KB** (`MAX_INBOX_BYTES`), so reading a whole part
is always safe — no truncation, no cut-off context.

---

## Step 0. Fetcher architecture (for reference)

The project has three independent TG scripts. The canonical one is `telegram_watcher.py`.

| Script | API | What it does | Per-group? |
|---|---|---|---|
| your Telegram fetcher (a local Telethon script) | Telethon, user-session | Monitors selected groups/PMs, writes **one folder per channel** `inbox/<safe_title>/` (one part per <100 KB, per-topic subfolders for forums; the forum feed goes to `1-General/`) + dashboard `telegram_group_inbox.md` + private DMs to `_signal.md`. **Media is not fetched** — `attach` pulls it on demand into `inbox/<safe_title>[/<topic>]/attachments/` | ✅ |
| ~~an old one-off poller~~ | Bot API | **Removed 2026-10-17** (a scripts reorganisation retired its one-off poller); writes went to a flat inbox file. Not per-group. | ❌ |
| ~~an old bot bridge daemon~~ | Bot API, daemon | **Removed 2026-09-27** (scripts review: no caller anywhere). There is no TG→agent command bridge today; sending is `your Telegram sender`, control of Freebuff Desktop is `the host's own control bot. | ❌ |

**`telegram_watcher.py` config** lives in the fetcher's config file
(NOT in the project root). Contains:
- `groups` — array of tracked dialogs (id, title, username, last_message_id, is_pm, fetch_limit).
- `last_fetch` — ISO time of the last run.
- `api_id`, `api_hash` — take from `my.telegram.org/apps`, fill in via
  `python telegram_watcher.py setup`.
- `discovered_topics`, `topic_names`, `topics` — forum groups only.
- `priority_topics` — topics to check first; also the source of the `label` used
  in topic folder names (`inbox/<channel>/<topic_id>-<label>/`). Separate
  `inbox/priority/*.md` files are no longer written.
- `topic_last_ids` (per group) — read cursor per topic (`{"4": 89710, "1": …}`).
  The main feed uses `last_message_id`; each topic keeps its own, so a run cut short
  by `--max-seconds` does not skip a topic's messages. Leave it alone by hand — it is
  written by the fetcher.
- `archive_hash_<name>` — service hashes against double archiving.

Session: the fetcher's session file (never committed, never shared) (Telethon, SQLite format;
**do not share, do not commit, in `.gitignore`**).

---

## Step 1. What is fresh

```bash
# Config freshness
python your-telegram-fetcher status

# Freshness of specific files
ls -lt inbox/*.md inbox/*/*.md inbox/*/*/*.md 2>/dev/null | head -40
```

Look at:

- the fetcher's config file → the `last_fetch` field (ISO).
- `inbox/.fetch_stats.json` → dict `{group_title: new_messages}` of the last fetch.
- `inbox/<safe_title>/` → parts by name (`YYYY-MM-DD-NNN.md`, newest = highest number).
- `inbox/<safe_title>[/<topic>]/attachments/` → fresh files (by mtime).

If `last_fetch` is more than 1 hour ago — the fetcher may be stuck. Not our
business in this skill, just mention it to the user.

---

## Step 2. Per-channel inbox folders

Each group/channel/DM has a folder `inbox/<safe_title>/` (name sanitised:
underscores instead of spaces, special characters stripped). Inside it the log is
split into parts `YYYY-MM-DD-NNN.md` — `NNN` is sequential inside the folder, so
the **newest part is the highest number** and each part is under 100 KB. Read the
newest part; add the previous one only if you need more context, or read the
parts in order for the whole history. **This is the canonical source of truth for
a group.**

Forum groups (and chats with configured topics) get one subfolder per topic:
`inbox/<safe_title>/<topic_id>-<label>/` (e.g. `inbox/<channel>/11-<topic>/`,
`inbox/<channel>/4-<topic>/`, `inbox/<channel>/597-<topic>/`). `<label>`
comes from `priority_topics` in the config, else the Telegram topic title, else
`topic-<id>`. The forum main feed and the general topic (id=1) are the same stream
and live in the **fixed** subfolder `inbox/<safe_title>/1-General/` (owner decision
2026-10-07). A forum's channel root holds **no `.md` part at all** — only topic
subfolders. (Root parts left over from before the change were moved once by
a one-shot migration script.)

Shape examples:
- `inbox/<channel>/` — one folder per tracked dialog.
- `inbox/<channel>/597-<topic>/` — a forum topic inside a channel.
- `inbox/<channel>/` plus topic subfolders `4-<topic>/`, `11-<topic>/`,
  `238-<topic>/`, `307-<topic>/`
- `inbox/telegram_group_inbox.md` — dashboard aggregator (NOT a channel folder; a merge of ALL groups).
- `inbox/_signal.md` — private messages via the bot (NOT a channel folder; PMs in one pile).
- Agent-written logs and digests (`inbox/keys_log.md`, `inbox/ai_tools_log.md`,
  `inbox/digest-latest*.md`) stay flat — they are not channel dumps. The 100 KB rule
  holds, but rotation is manual since 2026-10-17 (`inbox_log_append.py` is retired):
  copy the current content to `_archive/logs/<name>.<date>.md`, add a row to
  `_archive/logs/MANIFEST.tsv`, then append the new block to the emptied log. That
  manifest is how an archived log is found.

Format of each record in a channel/topic part:
```

---
**{group_title}** | {YYYY-MM-DD HH:MM:SS} | ot @{sender} [#{message_id}]:
{text}
[📎 сохранено: `inbox/{channel}[/{topic}]/attachments/...`]

```

**Algorithm:**

1. From `inbox/.fetch_stats.json` take the list of groups with `count > 0`.
2. For each group:
   - `ls -t inbox/<safe_title>/` → read the newest `YYYY-MM-DD-NNN.md` part(s),
     plus the topic subfolders that matter (`read_files` works on any part).
   - Extract findings.
3. If `.fetch_stats.json` is absent or empty — read the newest part of every
   channel folder where `last_fetch` is fresh (`ls -lt inbox/*/*.md`).
4. The legacy flat inbox was reorganised once by
   `python migrate-inbox-to-folders` (one-shot tool, `--dry-run`
   available). Do not re-run it against the current folder layout.

---

## Step 3. Attachments (on demand, not by the fetcher)

The fetcher downloads **no media at all** (owner decision 2026-10-07: a download
burst is a ban risk for the account). A record keeps only the type marker
(`[📷 Фото]`, `[📎 Файл: name]`, `[🎬 Видео]`) plus the message id `[#id]`.

Attachments are pulled on demand — they sit next to the log they belong to:

```bash
python your-telegram-fetcher attach "<channel>" --topic <topic-id> --limit 3
python your-telegram-fetcher attach "<channel>" --msg <message-id>
python your-telegram-fetcher attach "<channel>"            # whole channel, newest
```

It takes ≤ `--limit` files (default 10) with a `--delay` pause (default 2 s)
between them, and names each file `msg<id><ext>` — so a second run sees the file
and skips it instead of downloading again. Files land in:

```
inbox/<safe_title>/attachments/msg<id>.<ext>                    # feed/channel-level
inbox/<safe_title>/<topic_id>-<label>/attachments/msg<id>.<ext>  # topic-level
```

Feed-level media is main-feed/general-topic media; topic media goes into that
topic's own subfolder. In markdown the record is marked:

```
[📎 сохранено: `inbox/<safe_title>[/<topic>]/attachments/<file>`]
```

Files > 50 MB are always skipped.

**Attachment search priority (ALWAYS in this order):**

1. **`~/Downloads/Telegram Desktop/`** — where Telegram Desktop puts files the
   user downloaded manually. **LOOK HERE FIRST.** The user often downloads
   files themselves (via the app), and they do not land in the inbox
   — only here. The file name usually matches the original (`<archive>.zip`).
2. `inbox/<safe_title>[/<topic>]/attachments/` — what the fetcher downloaded (≤50 MB).
3. `~/Downloads/` — general downloads (if the file was downloaded from a
   browser, not from TG).

If a file is being searched by name/context from TG — first
`ls ~/Downloads/Telegram Desktop/`, then the channel's `attachments/`. Do not write
Telegram download scripts until the file has been checked in the Telegram
Desktop downloads.

**What to do with attachments:**
- `.md`, `.txt`, `.json`, `.csv`, `.py`, `.sh` — read and distill the essence
  into the report.
- `.pdf` — mention the file name, do not try to parse.
- `.jpg/.png/.webp` — mention, do not analyze without an explicit request.
- `.zip/.7z/.tar.gz` — ask the user to confirm extraction, do not do it yourself.

---

## Step 4. Analysis and categorization

| Type | What to look for | Action |
|-----|-----------|----------|
| API keys | `sk-...`, `hf_...`, `AIza...`, `ghp_...`, `glpat-...`, `xoxb-...` | Tell the user immediately. **Do not write the full key into the report or logs** — only a mask like `sk-...AbCd`. |
| Tools | GitHub links (`github.com/...`), npm packages, bots | If new — briefly propose: "worth a look" |
| Free services | Free APIs, promocodes, trial credits | Check the deadline/terms, mention in "worth checking" |
| System prompts / jailbreaks | Large texts with model instructions | Save to `knowledge/wiki/code/` or `unfiltered/jb-archive/` |
| `.md/.txt` attachments with content | Save locally (the fetcher already did) | Read and distill the essence |
| Scam | Template "$1 ChatGPT Plus", "KYC method", indo-pack flood | Warn, **do not recommend paying** |

---

## Step 5. Report to the user

Format (SHORT, not a wall of text):

```
📬 TG snapshot at <last_fetch>

<Group 1> (<N> new):
  • <finding 1 briefly>
  • <finding 2 briefly>

<Group 2> (<N> new):
  • <finding>
  • attachment: inbox/<channel>[/<topic>]/attachments/<file>

🔥 Most interesting:
  • <what to check first>
```

If `last_fetch` is recent and `.fetch_stats.json` is empty/absent — write "nothing
new, the fetcher is silent since <time>". Do not make things up.

---

## Exceptions and gotchas

- **Do not run the fetcher from this skill.** It is the read side. If you want
  fresh messages — let the user say "fetch" separately.
- **Do not send messages to TG** from this skill. Read only. Sending is
  `send_telegram.py` or `send_to_telegram.py` on explicit request.
- **Do not delete** old inbox parts — they are needed for history/context.
  Archiving is a separate command `python your-telegram-fetcher archive`.
- **If a group is not in `<fetcher-config>.groups`** — its channel folder
  (or a legacy flat file) is stale. Look for data in `telegram_group_inbox.md`,
  **but mark** it as "probably stale".
- **Folders outside the fetcher's config** (for example `inbox/<manual-zone>/`)
  — landing zones for manual inserts
  (NOT watcher-generated; the user puts things there by hand).
- **`inbox/priority/` no longer exists** — the former priority topics are
  ordinary topic subfolders now (see Step 2). Old notes and cron configs still
  pointing at `inbox/priority/*.md` are dead paths.
- **In a forum, never look for channel-root parts** — they are all in
  `1-General/` (feed) or a topic subfolder. `--no-attachments` on `fetch` is an
  obsolete no-op: media has not been fetched since 2026-10-07.
- **If fetch failed with an error** (403, FloodWait, etc.) — record it in the
  notes, continue with the next group.
- **This skill must not be autonomous** (see heartbeat/oper-workflow) — heavy
  actions (archive extraction, paying for something) always belong to the user.

---

## Hands and feet: how to read files without pain

| Need | Command |
|---|---|
| Tail of a channel's newest part (last 80 lines) | `powershell -Command "Get-Content (Get-ChildItem 'inbox/<safe_title>/*.md' \| Sort-Object Name \| Select-Object -Last 1) -Tail 80"` |
| Newest part of a channel | `ls -t inbox/<safe_title>/` |
| Freshness of all parts | `ls -lt inbox/*/*.md` |
| Freshness of attachments | `ls -lt inbox/<safe_title>/attachments/` |
| Size of the whole inbox | `du -sh inbox/` |
| Archive all inbox parts (hash-dedup) | `python your-telegram-fetcher archive` |
| Reorganise a legacy flat inbox into folders (one-shot, dry-run first) | `python migrate-inbox-to-folders --dry-run` |
| Move leftover forum-root parts into `1-General/` (one-shot, dry-run first) | `python migrate-forum-root-to-general --dry-run` |
| Download attachments on demand (≤limit, with pauses) | `python your-telegram-fetcher attach "<channel>" [--topic N] [--msg ID] [--limit K]` |
| Append to an agent log (manual 100 KB rotation) | append to `inbox/<log>.md`; when it passes 100 KB first copy it to `_archive/logs/<name>.<date>.md` and record the row in `_archive/logs/MANIFEST.tsv` |
| Find an archived agent log | grep `_archive/logs/MANIFEST.tsv` |
| Clean the inbox | Do not run from the read-side skill; archiving and data deletion require separate owner authorization |
