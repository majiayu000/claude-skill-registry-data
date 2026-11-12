---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: grok-bot
description: >
  Delegate X (Twitter) work to the `grok-bot` subagent: search posts, read threads, look up
  users, export followers, following, likes or bookmarks as CSV, analyze an account. Grok Bot
  is a remote agent on its own cloud computer with Tommy's X account (@__morse) connected,
  plus a browser, shell, files, web search and image generation. Files it sends are saved on
  this Mac. Use when the user wants anything from X, or a long task that fits a cloud computer.
---

# Grok Bot subagent

`grok-bot` is a subagent backed by the Grok Bot bot **opencode** (model `grok-bot/opencode`, provider `opencode-grok-bot/` in the kimakivoice repo). It runs on **its own cloud computer**, with its own tools, memory and chat history. Tommy's X account **@__morse** is connected there, so it reads X with full access: search, threads, profiles, followers, following, likes, bookmarks.

Call it with the subagent tool, agent `grok-bot`, and a self-contained prompt:

```
Export ALL followers of my X account @__morse to a CSV (every follower, not a sample).
Columns: handle, name, bio, followers_count, following_count, verified, location, url, created_at.

Do all the work inside this turn: do not hand it off to a background job and do not reply
until the CSV is complete. Then send me the CSV file as an attachment in this chat and reply
with the row count and the follower count shown on the profile.
```

The reply comes back as text. A file the bot attaches shows as a line with its local path:

```
**File:** saved to `/Users/morse/Downloads/grok-bot/80526548/morse_followers_fresh.csv`
The fresh CSV has 7,907 rows. Your profile also shows 7,907 followers.
```

## Writing the prompt

The bot sees **only the prompt text**. It never sees AGENTS.md, the system prompt, skills or files on this Mac.

- **Say the exact output**: columns, format, counts, which fields to quote verbatim.
- **Ask for files as attachments**: "send me the file as an attachment in this chat". Only attachments reach this Mac. A path on its computer (`/workspace/x.csv`) is useless here.
- **Keep the work in one turn**: add "Do all the work inside this turn: do not hand it off to a background job". Otherwise the bot may reply "I'll send it when done", end its turn, and post the result later.
- **One task per prompt**, but batch related reads (three searches, one thread) in one prompt. Each call is a full bot turn.
- To give it local data, paste the text into the prompt. Attachments other than text files are not sent.

## Reading the result

- **Verify files** after the call. Count rows, check columns, dedupe:

  ```bash
  python3 -c "import csv,sys; r=list(csv.DictReader(open(sys.argv[1], encoding='utf-8'))); print(len(r), len({x['handle'] for x in r}))" '/Users/morse/Downloads/grok-bot/<hash>/<name>.csv'
  ```

- Files go to `~/Downloads/grok-bot/<first 8 chars of the file hash>/<name>`. Copy them where the user wants them.
- **Cards** arrive as text: a question with numbered options, or an approval with `approve` / `always` / `deny`. Answer by calling the same subagent session again with the option number or word. Forms, secrets and drafts must be done in the Grok Bot app: ask the user.

## Follow-ups and late results

Continue the same subagent session (pass its `sessionID`) for follow-ups: "now add their last post date", "send the file again". The next turn first shows everything the bot sent since the last one, under **Sent by the bot since the last message**. That is how a late background result reaches you: wait, then send a short follow-up like "Send the result now if it is done".

<details>
<summary>Limits that matter for callers</summary>

| Limit | What to do |
| --- | --- |
| One bot is one chat, shared by every session on `grok-bot/opencode` | Never run two `grok-bot` subagents in parallel. Their turns mix in the same chat. |
| No OpenCode tools, permissions or subagents | The bot uses its own tools on its own computer. Edits there do not touch this repo. |
| First turn can take up to 2 minutes | The cloud computer wakes up first. Do not retry: a retried prompt runs twice. |
| Usage and cost show as 0 | Normal. |
| Posting, DMs, likes, follows act on Tommy's real account | Only do it when the user asks. Drafts come back as cards to send in the app. |

</details>

## Example prompts

**Search posts** (X search operators work in the query):

```
Search X for "claude code" OR "opencode" since:2026-11-01 min_faves:50 lang:en -filter:replies,
latest first, 10 results. For each: post URL, author handle, date, full text verbatim, likes, reposts, views.
```

**Read a thread**:

```
Read the full thread of <post URL>, including replies
from the author. Return every post in order with its URL and full text verbatim.
```

**Profile and recent posts**:

```
Look up the X user @badlogicgames: bio, follower and following counts, join date, pinned post.
Then list his last 20 original posts (no replies, no reposts) with URL, date, text and likes.
```

**Export a list as CSV**: followers, following, likes, bookmarks or search results of any size. Use the prompt at the top and change the list and columns.

### X search operators

| Operator | Example |
| --- | --- |
| date | `since:2026-11-01` `until:2026-11-04` `within_time:24h` |
| user | `from:__morse` `to:__morse` `@__morse -from:__morse` `filter:verified` |
| engagement | `min_faves:50` `min_replies:10` `min_retweets:5` |
| type | `-filter:replies` `-filter:retweets` `filter:quote` `filter:self_threads` |
| media | `filter:images` `filter:videos` `filter:links` `url:github.com` |
| relations | `quoted_tweet_id:<id>` `conversation_id:<id>` |
| text | `"exact phrase"` `(A OR B)` `-word` `#tag` `$TSLA` |
| place, language | `near:"London" within:10km` `lang:en` |
