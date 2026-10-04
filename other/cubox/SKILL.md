---
name: Cubox Integration
description: Save web pages and memos to Cubox using the Open API
---

# Cubox Integration Skill

This skill enables saving content to Cubox using the Open API. Cubox is a read-it-later and bookmarking service that supports saving web URLs and quick memos.

## Prerequisites

1. **Cubox Premium Membership** - The Open API is a premium feature
2. **API Key** - Get your API URL from Cubox settings:
   - Go to Cubox Preferences > Extension Center and Automation > API Extension
   - Enable "API Link" to get your personal API URL
   
> ⚠️ **Security**: Your API URL is a unique credential. Keep it private and never share it.

## Environment Setup

Set the `CUBOX_API_URL` environment variable with your personal API URL:

```bash
export CUBOX_API_URL="https://cubox.pro/c/api/save/YOUR_TOKEN"
```

## Available Tools

### 1. Save URL (`scripts/save_url.py`)

Save a web page URL to Cubox.

```bash
python scripts/save_url.py <url> [--title "Title"] [--description "Description"] [--tags "tag1,tag2"] [--folder "Folder Name"]
```

**Parameters:**
- `url` (required): The web page URL to save
- `--title`: Optional title for the bookmark
- `--description`: Optional description
- `--tags`: Comma-separated list of tags
- `--folder`: Target folder name (defaults to Inbox)

**Example:**
```bash
python scripts/save_url.py "https://example.com/article" --title "Great Article" --tags "tech,reading" --folder "Articles"
```

### 2. Save Memo (`scripts/save_memo.py`)

Save a quick memo/note to Cubox.

```bash
python scripts/save_memo.py <content> [--title "Title"] [--description "Description"] [--tags "tag1,tag2"] [--folder "Folder Name"]
```

**Parameters:**
- `content` (required): The memo text content
- `--title`: Optional title (Cubox will auto-generate if not provided)
- `--description`: Optional description
- `--tags`: Comma-separated list of tags
- `--folder`: Target folder name (defaults to Inbox)

**Example:**
```bash
python scripts/save_memo.py "Remember to review the quarterly report" --title "Todo" --tags "work,reminder"
```

## API Rate Limits

- Premium users: **500 API calls per day**

## Notes

- After saving, Cubox cloud will automatically process the content (article parsing, snapshot archiving, etc.), which may take some time
- If title or description is not specified, Cubox will attempt to generate them automatically
- If no folder is specified, content will be saved to your Inbox by default
