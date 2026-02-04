---
name: twitter-bookmarks
description: Automated Twitter bookmark processor with YAML-configurable categories and smart routing
homepage: https://x.com/alexhillman/status/2006420618091094104
metadata: {"clawdis":{"emoji":"🔖","requires":{"bins":["bird"]}}}
---

# Twitter Bookmarks Processor

Automated Twitter bookmark processing inspired by Alex Hillman's JFDI system. Checks bookmarks periodically, categorizes via LLM, and routes to configured destinations.

## Quick Start

```bash
# Build
go build -o twitter-bookmarks

# Process bookmarks
./twitter-bookmarks process

# Check status
./twitter-bookmarks status
```

## How It Works

1. **Fetch** - Get new bookmarks via `bird bookmarks`
2. **Analyze** - Read full tweet + thread context
3. **Classify** - Send to Gemini with your category definitions from YAML config
4. **Route** - Execute action based on category mapping (save, summarize, notify, discard)
5. **Track** - Update state to avoid reprocessing

## Configuration

Create `~/.twitter-bookmarks-config.yaml`:

```yaml
categories:
  # Define categories with descriptions and keywords (guides LLM classification)
  work:
    description: "Work-related tools, articles, and research"
    keywords: [enterprise, b2b, productivity, saas]
  
  personal:
    description: "Personal interests, hobbies, random finds"
    keywords: [hobby, interest, fun, learn]

routing:
  # Map categories to actions
  work:
    action: save_obsidian  # Options: save_obsidian, summarize, notify, save_file, unbookmark
    path: "Work/Research"  # Relative to Obsidian vault
    notify: true           # Send Telegram notification
  
  personal:
    action: summarize      # Extract & summarize URLs
    notify: true
```

## Available Actions

| Action | Description | Config |
|--------|-------------|--------|
| `save_obsidian` | Save to Obsidian vault | `path`: relative path in vault |
| `summarize` | Extract URL content, summarize, send via Telegram | N/A |
| `notify` | Send Telegram notification only | N/A |
| `save_file` | Append to text file | `path`: absolute file path |
| `unbookmark` | Remove bookmark after processing | N/A |
| `codex` | Create Codex prompt in `~/.codex-prompts/` | N/A |
| `razor` | Auto-implement or save to Obsidian | `path`: Obsidian path |

## Environment Variables

Required:
- `GEMINI_API_KEY` - For LLM classification

Optional:
- `TWITTER_BOOKMARKS_CONFIG` - Config file path (default: `~/.twitter-bookmarks-config.yaml`)
- `TWITTER_BOOKMARKS_STATE` - State file (default: `~/.twitter-bookmarks-state.json`)
- `TWITTER_BOOKMARKS_OBSIDIAN` - Obsidian vault path (if using `save_obsidian`)
- `BIRD_BIN` - bird CLI path (default: `bird`)
- `SUMMARIZE_BIN` - summarize CLI path (optional)
- `TWITTER_BOOKMARKS_QUIET_START` - Quiet hours start (default: `23:00`)
- `TWITTER_BOOKMARKS_QUIET_END` - Quiet hours end (default: `08:00`)

## Automation

### Cron (every 20 minutes)
```bash
*/20 * * * * cd /path/to/twitter-bookmarks && ./twitter-bookmarks process
```

### Clawdis Cron
```python
from clawdis_cron import add_job
add_job({
    'id': 'twitter-bookmarks',
    'schedule': '*/20 * * * *',
    'command': 'cd /path/to/twitter-bookmarks && ./twitter-bookmarks process'
})
```

## Example Workflows

### Workflow 1: Research Collection
```yaml
categories:
  research:
    description: "Academic papers, research tools, datasets"
    keywords: [research, paper, study, dataset, academic]

routing:
  research:
    action: save_obsidian
    path: "Research/Papers"
    notify: true
```

### Workflow 2: Auto-discard spam
```yaml
categories:
  spam:
    description: "Unwanted promotional content"
    keywords: [crypto, nft, airdrop, presale]

routing:
  spam:
    action: unbookmark  # Remove automatically
```

### Workflow 3: Recipe collection
```yaml
categories:
  recipes:
    description: "Cooking recipes and food content"
    keywords: [recipe, cook, bake, ingredient]

routing:
  recipes:
    action: save_file
    path: "/Users/you/recipes.md"
    notify: false
```

## State Tracking

File: `~/.twitter-bookmarks-state.json`

```json
{
  "lastProcessed": "2026-01-04T02:20:00Z",
  "processedIds": ["1234567890", "9876543210"],
  "categories": {
    "work": 15,
    "personal": 8,
    "spam": 3
  }
}
```

## Integration with Clawdis

When running as a Clawdis skill, the processor can:
- Send notifications to configured Telegram accounts
- Save to Obsidian vault (if path configured)
- Create Codex prompts for AI-assisted implementation
- Trigger other Clawdis skills based on content

## Requirements

- **bird CLI** (https://github.com/steipete/bird) - Authenticated Twitter access
- **Gemini API key** - For LLM classification
- **Obsidian vault** (optional) - Only if using `save_obsidian`
- **summarize CLI** (optional) - For URL content extraction
- **Telegram bot** (optional) - For notifications

## Tips

- Start with 3-5 categories max, refine based on actual bookmarks
- Use `discard` category + `unbookmark` action to auto-clean spam
- Set `notify: false` for high-volume categories
- Keywords guide LLM but aren't strict filters
- Check `./twitter-bookmarks status` to see category distribution

---

*Inspired by Alex Hillman's JFDI system*
