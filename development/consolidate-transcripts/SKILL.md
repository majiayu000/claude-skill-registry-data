---
name: consolidate-transcripts
description: Consolidate transcripts from a channel into a single file, sorted by date (newest first), up to 800K tokens. Use when preparing transcripts for LLM context or bulk analysis.
---

# Consolidate Transcripts

**Why?** LLMs have context limits. This skill merges multiple transcripts into a single file with accurate token counting, so you can feed an entire channel's content to Claude or GPT without exceeding limits.

## Quick Start

```bash
python scripts/consolidate_transcripts.py <channel_name>
```

Output: `~/Documents/YTScriber/<channel_name>/<channel_name>-consolidated.md`

> [!NOTE]
> This feature is currently a standalone script. A `ytscriber consolidate` CLI command is planned for a future release.

---

## Workflow

### 1. Identify the Channel

List available channels:
```bash
ls ~/Documents/YTScriber/
```

### 2. Choose Token Limit

| Use Case | Recommended Limit | Flag |
|----------|-------------------|------|
| Claude (200K context) | 150000 | `--limit 150000` |
| GPT-4 Turbo (128K) | 100000 | `--limit 100000` |
| Full archive (Claude Pro) | 800000 | (default) |
| Quick sample | 50000 | `--limit 50000` |

> [!TIP]
> The default 800K limit leaves ~200K tokens for prompts and responses when using Claude's 1M context.

### 3. Run Consolidation

```bash
python scripts/consolidate_transcripts.py <channel_name> [--limit TOKENS] [--verbose]
```

**Examples:**

```bash
# Default (800K tokens)
python scripts/consolidate_transcripts.py library-of-minds

# Custom limit for GPT-4
python scripts/consolidate_transcripts.py aws-reinvent-2025 --limit 100000

# Verbose output showing all included files
python scripts/consolidate_transcripts.py dwarkesh-patel --verbose
```

### 4. Verify Output

Check the consolidated file was created:
```bash
ls -la ~/Documents/YTScriber/<channel_name>/*-consolidated.md
```

---

## Parameters

| Option | Description | Default |
|--------|-------------|---------|
| `channel_name` | Folder name in data directory | Required |
| `--limit, -l` | Maximum tokens to include | 800000 |
| `--verbose, -v` | Show detailed file list | False |

---

## Output Format

The consolidated file includes:

1. **Header** — Generation metadata, total transcripts, token/word counts
2. **Table of Contents** — Dates, titles, tokens, words per transcript
3. **Transcripts** — Full text with title, date, author, source URL

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `ModuleNotFoundError: tiktoken` | tiktoken not installed | `pip install tiktoken` |
| `No transcripts found` | Empty transcripts folder | Run `ytscriber download` first |
| `FileNotFoundError` | Channel doesn't exist | Check `ls ~/Documents/YTScriber/` for valid names |
| Output file is small | Few transcripts available | Use `--verbose` to see what was included |
| Token count seems wrong | Old tiktoken version | `pip install --upgrade tiktoken` |

---

## Common Mistakes

1. **Wrong channel name** — Use the folder name exactly as shown in `ls ~/Documents/YTScriber/`, not the YouTube channel name.
2. **Forgetting to download transcripts first** — Consolidation requires transcripts to exist. Run `ytscriber download` first.
3. **Using too high a limit** — If you exceed your LLM's context, you'll get truncation errors. Use the limit guide above.
4. **Expecting real-time updates** — Re-run consolidation after downloading new transcripts.

---

## Reference

- Transcripts sorted **newest first** (descending by date)
- Files without dates in filename are placed last
- Token counting uses `cl100k_base` encoding (GPT-4/Claude compatible)
- Consolidated files are gitignored (not committed)
- Re-running overwrites the previous consolidated file
