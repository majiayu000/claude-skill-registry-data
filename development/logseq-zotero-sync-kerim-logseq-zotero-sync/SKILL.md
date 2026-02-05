---
name: logseq-zotero-sync
description: Sync Logseq pages tagged with #zotero to Zotero by adding 'in_logseq' tag. Uses batch checking for efficiency. Claude Code only.
---

# Logseq to Zotero Sync Skill

Automatically synchronize Logseq literature notes with Zotero by tagging referenced items with `in_logseq`.

## When to Use This Skill

Use this skill when the user wants to:
- Tag Zotero items that are referenced in Logseq
- Maintain sync between Logseq #zotero pages and Zotero library
- Identify which Zotero items have been added to their Logseq knowledge base
- Periodically update the `in_logseq` tag for new literature notes

**Keywords**: logseq, zotero, sync, tagging, literature notes, bibliography, knowledge management

## Overview

This skill syncs Logseq pages tagged with #zotero to Zotero by:

1. **Query Logseq**: Uses Logseq CLI to find all pages with #zotero tag and Zotero URL property
2. **Extract Keys**: Parses Zotero URLs to get item keys (e.g., "M2QGSQA9")
3. **Batch Check**: Queries Zotero for items already tagged with `in_logseq`
4. **Smart Diff**: Compares lists to find only items that need tagging
5. **Tag**: Adds `in_logseq` tag to items that don't have it

**Key Feature**: Idempotent batch processing - safe to run repeatedly, only tags what's needed.

## Requirements

### System Requirements
- **Logseq Desktop app** (CLI doesn't work with browser version)
- **@logseq/cli** installed globally (`npm install -g @logseq/cli`)
- Python 3.7+
- macOS (for Keychain credential storage)

### Python Dependencies
```bash
pip3 install pyzotero keyring
```

### Credentials
Shares credentials with `zotero-tag-automation` skill via macOS Keychain (service: `zotero-tag-automation`).

If credentials aren't set up yet:
```bash
python /Users/niyaro/.claude/skills/zotero-tag-automation/setup_credentials.py
```

## Usage

### Basic Command

```bash
cd /Users/niyaro/Documents/Code/logseq-zotero-sync
python sync_logseq_to_zotero.py
```

Auto-detects the most recent Logseq DB graph.

### Specify Graph

```bash
python sync_logseq_to_zotero.py "2025-10-26 Logseq DB"
```

## How It Works

### Batch Check Approach (Efficient)

Instead of checking each item individually, this script:

1. Gets **all** Logseq items with Zotero URLs in one query
2. Gets **all** Zotero items with `in_logseq` tag in one query
3. Compares the two sets to find the difference
4. Only makes API calls to tag items that need it

This is much more efficient than checking each item one-by-one, especially as the library grows.

### Logseq CLI Query

The script runs this datalog query via Logseq CLI:

```clojure
[:find (pull ?b [:block/title {:user.property/ZoteroURL-om1JHnZv [:block/title]}])
 :where [?b :user.property/ZoteroURL-om1JHnZv]]
```

This finds all pages/blocks with the Zotero URL property and extracts the URLs.

### URL Parsing

Zotero URLs have the format:
```
zotero://select/library/items/M2QGSQA9
```

The script extracts the item key (`M2QGSQA9`) using regex pattern matching.

### Zotero API

Uses pyzotero to:
- Query items by tag: `zot.items(tag='in_logseq')`
- Get item data: `zot.item(item_key)`
- Update tags: `zot.update_item(item)`

## Claude Code Integration

When the user asks to sync Logseq to Zotero or tag items in Zotero based on Logseq:

1. **Verify credentials exist** (check keychain or prompt user to run setup)
2. **Identify the graph** (ask user or auto-detect)
3. **Run the script** using Bash tool
4. **Report results** to user with summary

### Example Workflow

```
User: "Tag all my Logseq literature notes in Zotero"

Claude:
1. Checks if credentials are set up
2. Lists available Logseq graphs
3. Asks user to confirm graph name
4. Runs: python sync_logseq_to_zotero.py "GraphName"
5. Shows summary of tagged items
```

## Idempotency

The script is **idempotent** - running it multiple times has no negative effects:

- Items already tagged are skipped (with ⊙ symbol)
- Only new items get tagged
- No duplicate tags
- Safe to run daily/weekly as part of workflow

## Output Format

```
==============================================================
Logseq to Zotero Sync
==============================================================

Querying Logseq graph: 2025-10-26 Logseq DB
Found 14 items in Logseq with Zotero URLs
Querying Zotero for items with 'in_logseq' tag...
Found 10 items already tagged with 'in_logseq'

Found 4 items that need tagging:
  - AA8CFB7Y
  - DUF7Q2B6
  - M2QGSQA9
  - ZTSWUK3C

Tagging 4 items with 'in_logseq'...

[1/4] ✓ AA8CFB7Y: Here we are together
[2/4] ✓ DUF7Q2B6: Reflections on Orthography
[3/4] ✓ M2QGSQA9: Taiwan Archaeology
[4/4] ✓ ZTSWUK3C: Who owns "the culture"

==============================================================
Summary:
  Successful: 4/4
  Failed: 0/4
  Tag: in_logseq
==============================================================
```

## Troubleshooting

### "Graph not found"

**Problem**: Logseq CLI can't find the graph
**Solutions**:
- User is using browser version (CLI only works with Desktop)
- Run `logseq list` to see available graphs
- Make sure Logseq Desktop app is installed

### "Credentials not found"

**Problem**: No credentials in Keychain
**Solution**: Run setup script:
```bash
python /Users/niyaro/.claude/skills/zotero-tag-automation/setup_credentials.py
```

### "Command not found: logseq"

**Problem**: @logseq/cli not installed
**Solution**:
```bash
npm install -g @logseq/cli
logseq --version  # verify
```

### Empty Results from Logseq

**Problem**: Query returns 0 items but user says items exist
**Possible causes**:
- Property name changed (check actual property name in Logseq)
- Wrong graph selected
- Items are blocks not pages (query targets pages)
- Graph is file-based not DB-based (different query needed)

## File Structure

```
/Users/niyaro/Documents/Code/logseq-zotero-sync/
├── sync_logseq_to_zotero.py    # Main script
├── requirements.txt             # Python dependencies
├── README.md                    # User documentation
├── SKILL.md                     # This file (skill documentation)
└── .gitignore                   # Git ignore rules
```

## Related Skills

- **logseq-cli**: Interface with Logseq DB graphs
- **zotero-tag-automation**: Tag items after search
- **zotero-mcp**: Semantic search in Zotero
- **zotero-mcp-agents**: Autonomous Zotero search agents

## Use Cases

1. **Weekly Sync**: Run script weekly to tag new literature notes
2. **After Import**: Run after importing items to Logseq
3. **Curation**: Use `in_logseq` tag in Zotero to see which items are in knowledge base
4. **Workflow Integration**: Part of literature review workflow

## Future Enhancements

Potential improvements:
- Bidirectional sync (remove tag if removed from Logseq)
- Support multiple Logseq graphs
- Sync other metadata (notes, highlights)
- Web interface for manual sync
- Scheduled automatic sync

## Security

- Credentials stored in macOS Keychain (encrypted)
- Shares keychain service with zotero-tag-automation
- No credentials in code or config files
- API key never displayed in output

## Notes

- **Claude Code only**: This skill requires CLI access and Python execution
- **Desktop only**: Logseq browser version not supported by CLI
- **Batch efficient**: Uses smart diffing to minimize API calls
- **Idempotent**: Safe to run repeatedly without side effects
