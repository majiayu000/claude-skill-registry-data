---
name: Twitter/X
description: >
  Access Twitter/X via the Bird CLI. Two accounts available: @KostaMilov65517
  (SFW, local MacBook) and @elsunari (NSFW, Mac Mini via SSH). Use whenever
  the user mentions Twitter, X, tweets, timeline, mentions, trending, bookmarks,
  or anything Twitter-related. Triggers on: "check twitter," "my timeline,"
  "my mentions," "search twitter," "what's trending," "read this tweet,"
  "my bookmarks," "who do I follow," "tweet this," "reply to," "trending topics,"
  "what's happening on X," "show me the thread," or any request involving
  Twitter/X data.
---

# Twitter/X via Bird CLI

Bird is installed on both machines at `/opt/homebrew/bin/bird` (v0.8.0).

## Accounts

| Account | Machine | How to run | Cookie source |
|---------|---------|------------|---------------|
| @KostaMilov65517 (Kosta Milovanovic) | MacBook (local) | `bird <command>` | Chrome default profile |
| @elsunari (Broski) | Mac Mini (SSH) | `ssh mini "bird <command>"` | Safari |

When the user says "my twitter" or "my timeline" without specifying, use the **local @KostaMilov65517** account. Use @elsunari when the user mentions "elsunari," "broski," "the other account," or "NSFW."

## Base Patterns

```bash
# Local (SFW — @KostaMilov65517)
bird <command> [options] --json

# Mac Mini (NSFW — @elsunari)
ssh mini "bird <command> [options] --json"
```

- `--json` for structured output (preferred for processing)
- `--plain` for stable, no-emoji, no-color text output
- `-n <count>` limits result count on most commands
- `--all` fetches all pages (use with caution)

## Timeline & Feed

```bash
# Home timeline ("For You")
bird home -n 20 --json

# Chronological "Following" feed
bird home --following -n 20 --json

# A specific user's tweets
bird user-tweets USERNAME -n 20 --json
```

## Search & Discovery

```bash
# Search tweets
bird search 'query here' -n 10 --json

# My mentions
bird mentions -n 10 --json

# Mentions of another user
bird mentions -u USERNAME -n 10 --json

# Trending topics / AI-curated news
bird trending --json
bird news --json

# Account info
bird about USERNAME --json
```

## Read Tweets & Threads

```bash
# Read a single tweet (by ID or URL)
bird read TWEET_ID_OR_URL --json

# Full conversation thread
bird thread TWEET_ID_OR_URL --json

# Replies to a tweet
bird replies TWEET_ID_OR_URL --json
```

## Collections

```bash
# Bookmarks
bird bookmarks -n 20 --json

# Liked tweets
bird likes --json

# Twitter lists
bird lists --json

# List timeline
bird list-timeline LIST_ID_OR_URL --json
```

## Social Graph

```bash
# Who I follow
bird following --json

# My followers
bird followers --json
```

## Write Operations (USE WITH CAUTION)

**WARNING**: Bird uses unofficial X APIs. The developer warns that accounts using unofficial APIs for posting have reported suspensions. Always confirm with the user before any write operation.

```bash
# Post a tweet
bird tweet 'tweet text here'

# Reply to a tweet
bird reply TWEET_ID_OR_URL 'reply text'

# Tweet with media (up to 4 images or 1 video)
bird tweet 'text' --media /path/to/image.jpg --alt 'alt text'

# Follow/unfollow
bird follow USERNAME
bird unfollow USERNAME
```

**Note:** All examples above use the local account. For @elsunari, prefix with `ssh mini "..."` instead.

## Pagination

Many commands support pagination:
- `-n <count>` — number of results per page
- `--max-pages <N>` — stop after N pages
- `--cursor <string>` — resume from a previous cursor
- `--all` — fetch everything (paged automatically)

## Guidelines

- **Read operations are safe** — timeline, search, mentions, bookmarks, read, thread, etc. Run freely without confirmation.
- **Always confirm before posting** tweets, replies, follows, or unfollows. Warn about the suspension risk.
- **Prefer read-only use** — Bird is best as a monitoring/research tool.
- When displaying tweet results, summarize key fields (author, text, date, engagement) rather than dumping raw JSON.
- Use `-n` to limit results and avoid flooding output.
- Local commands run directly. For @elsunari, if SSH fails, check that the Mac Mini is reachable (`ssh mini "echo ok"`).
- `--json` output includes tweet text, author info, metrics (likes, retweets, replies, views), and URLs.
