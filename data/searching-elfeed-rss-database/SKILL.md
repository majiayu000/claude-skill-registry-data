---
name: Searching Elfeed RSS Database
description: Use to search emacs elfeed database for articles or analysis
---

# Searching Elfeed RSS Database

This skill provides access to the user's elfeed RSS feed database through a command-line interface. Elfeed is their primary information aggregation system, containing curated feeds from Reddit, blogs, YouTube channels, GitHub releases, and newsletters.

## When to Invoke This Skill

Use this skill when:
- **Topic research**: User asks about topics likely covered in their feeds (programming, AI, security, NixOS, Emacs, etc.)
- **Article recall**: User references "something I read" or "an article about..."
- **Pattern analysis**: Understanding what they've been reading recently
- **Context gathering**: Building background on topics from their curated sources
- **Unread triage**: Helping prioritize or summarize unread items

**Do NOT invoke** for:
- General web searches (use WebSearch instead)
- Information not likely in RSS feeds
- Real-time news (elfeed may not have fetched yet)

## Quick Start

The primary tool is `elfeed-cli` located at:
```
~/.claude/skills/elfeed/scripts/elfeed-cli
```

Or use the absolute path from this repo:
```
/home/markus/repos/nixos-config/nixos-shared/claude/skills/elfeed/scripts/elfeed-cli
```

**Most common usage:**
```bash
# Search recent unread items about a topic
elfeed-cli query "topic +unread @1-week-ago" simple 20

# Get database statistics
elfeed-cli stats

# List all feeds
elfeed-cli feeds

# List all tags
elfeed-cli tags
```

## Filter Syntax Quick Reference

Combine these operators to build queries:

| Operator | Meaning | Example |
|----------|---------|---------|
| `+tag` | Must have tag | `+unread`, `+programming`, `+reddit` |
| `-tag` | Must not have tag | `-unread`, `-youtube` |
| `@time` | Newer than time | `@1-week-ago`, `@3-days-ago`, `@1-month-ago` |
| `#N` | Limit to N entries | `#10`, `#50` |
| `text` | Title/link matches (regex) | `nixos`, `claude.*ai` |
| `!regex` | Title/link doesn't match | `!advertisement` |
| `=regex` | Feed URL/title matches | `=simonwillison` |
| `~regex` | Feed URL/title doesn't match | `~reddit` |

**Combine operators with spaces:**
```bash
"+programming +unread @1-week-ago #20"
"+reddit -unread ai.*agents"
"+github =anthropic"
```

## Common Workflows

### 1. Research a Topic
```bash
# Find recent articles about a topic
elfeed-cli query "topic-keyword +unread @2-weeks-ago" simple 30
```

### 2. Check Unread by Category
```bash
# Recent unread programming articles
elfeed-cli query "+programming +unread @1-week-ago" simple 20

# YouTube videos unwatched
elfeed-cli query "+youtube +unread" simple 10
```

### 3. Analyze Reading Patterns
```bash
# Get overall statistics
elfeed-cli stats

# See all feed sources
elfeed-cli feeds

# Check what tags are used
elfeed-cli tags
```

### 4. Find Specific Article
```bash
# Search by keyword across all entries
elfeed-cli query "specific-term" simple 50

# From specific source
elfeed-cli query "=simonwillison llm" simple 20
```

## Output Formats

The `query` command supports three formats:

1. **simple** (default, most readable):
   ```
   2025-10-19 14:30 | Blog Name | Article Title | https://example.com/article
   ```

2. **json** (for parsing):
   ```json
   [{"title":"...","link":"...","date":...,"tags":[...],"feed_title":"...","feed_url":"..."}]
   ```

3. **sexp** (Emacs s-expression):
   ```elisp
   ((:title "..." :link "..." :date ... :tags (...) :feed-title "..." :feed-url "..."))
   ```

## Important Notes

- **Requires running Emacs**: The CLI uses `emacsclient` to query the live database
- **Real-time data**: Queries reflect current database state (may include recently fetched items)
- **Tag system**: Feeds are tagged by category (programming, reddit, youtube, github, etc.)
- **No side effects**: Queries are read-only and don't modify read/unread status

## Advanced Usage

For detailed filter syntax, regex patterns, and complex query construction, see `reference.md`.

## Integration with Existing Command

The `/mh:elfeed-search` slash command is a convenience wrapper that calls this same tooling. You can invoke the skill autonomously or users can explicitly call the command.
