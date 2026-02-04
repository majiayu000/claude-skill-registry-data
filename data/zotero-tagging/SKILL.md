---
name: zotero-tagging
description: Tag Zotero items with timestamp tags after generating bibliographies. Uses secure macOS Keychain storage for credentials. Claude Code only.
---

# Zotero Tagging Skill (Claude Code)

Automatically tag Zotero items with timestamp tags after search results or bibliography generation. Credentials stored securely in macOS Keychain.

## When to Use This Skill

Use this skill when:
- User has generated a bibliography using the Zotero MCP skill
- User wants to tag search results for later retrieval
- User needs to organize Zotero items by search session
- User asks to "tag these items" or "add tags to the bibliography"

## Core Philosophy

**Tag search results for traceability.** After generating bibliographies or search results:
- Automatically extract item keys from the output
- Tag all items with a timestamp tag format: `Zotero-MCP-Results-YYYY-MM-DD-HHMM`
- Enable easy re-finding of these exact items in Zotero later
- Track which searches generated which bibliographies

## Prerequisites

Before using this skill, ensure:

1. **Credentials are set up** - User must run `setup_credentials.py` once to store:
   - Zotero Library ID
   - Zotero API Key (with write access)

2. **Python environment** - Virtual environment with dependencies installed:
   - `pyzotero` - Zotero web API client
   - `keyring` - macOS Keychain integration

3. **Zotero Web API Access** - User needs:
   - API key from https://www.zotero.org/settings/keys/new
   - Write access enabled on the API key

## Security Model

**All credentials stored in macOS Keychain:**
- ✓ Encrypted by macOS system
- ✓ No plain text files
- ✓ No passwords in code
- ✓ System-managed authentication
- ✓ Viewable/manageable in Keychain Access.app

**Service name:** `zotero-tag-automation`

## Workflow

### Step 1: Check Setup

Before tagging, verify credentials are configured:

```bash
cd /Users/niyaro/Documents/Code/zotero-tag-automation
source venv/bin/activate
python -c "import keyring; print('Library ID:', keyring.get_password('zotero-tag-automation', 'library_id'))"
```

If credentials not found, guide user to run:
```bash
python setup_credentials.py
```

### Step 2: Extract Item Keys

From a bibliography markdown file, extract all Zotero item keys:

```bash
# Extract keys from bibliography file
grep -o 'zotero://select/library/items/[A-Z0-9]*' bibliography.md | \
  sed 's/.*items\///' | \
  sort -u > /tmp/item_keys.txt

# Show extracted keys
cat /tmp/item_keys.txt
```

### Step 3: Tag Items

Run the tagging script with extracted keys:

```bash
cd /Users/niyaro/Documents/Code/zotero-tag-automation
source venv/bin/activate
python tag_items.py $(cat /tmp/item_keys.txt)
```

**Output format:**
```
Tagging 23 items with: Zotero-MCP-Results-2025-10-25-1417

[1/23] ✓ W44VF3CG
[2/23] ✓ M4G5W339
...

Summary:
  Successful: 23/23
  Failed: 0/23
  Tag: Zotero-MCP-Results-2025-10-25-1417
```

### Step 4: Confirm and Report

After tagging, report to user:
- Total items tagged
- Tag name used
- Any errors encountered
- How to find these items in Zotero (search by tag)

## Common Usage Patterns

### Pattern 1: After Bibliography Generation

**User request:** "Find papers on X and create a bibliography"

**Workflow:**
1. Use Zotero MCP skill to search and generate bibliography
2. Save bibliography to file (e.g., `/Users/niyaro/Desktop/bibliography.md`)
3. Ask user: "Would you like me to tag all 23 items for easy retrieval later?"
4. If yes:
   - Extract item keys from bibliography
   - Run tagging script
   - Report tag name and success count

### Pattern 2: Tag Existing Bibliography File

**User request:** "Tag all the items from bibliography.md"

**Workflow:**
1. Check file exists
2. Extract item keys
3. Run tagging script
4. Report results

### Pattern 3: Tag Specific Items

**User request:** "Tag items W44VF3CG and M4G5W339"

**Workflow:**
```bash
python tag_items.py W44VF3CG M4G5W339
```

### Pattern 4: First-Time Setup

**User request:** "Set up Zotero tagging"

**Workflow:**
1. Guide user to get API key from Zotero
2. Run setup script:
   ```bash
   cd /Users/niyaro/Documents/Code/zotero-tag-automation
   source venv/bin/activate
   python setup_credentials.py
   ```
3. Verify credentials stored successfully
4. Explain usage

## Error Handling

### Credentials Not Found

**Error:** "Credentials not found in Keychain"

**Solution:**
```bash
python setup_credentials.py
```

Guide user through entering:
- Library ID (from Zotero settings)
- API Key (from https://www.zotero.org/settings/keys/new with write access)

### API Key Permissions Error

**Error:** "403 Forbidden" or "Write access denied"

**Solution:**
- API key needs write access enabled
- Create new API key at https://www.zotero.org/settings/keys/new
- Check both:
  - ✓ Allow library access
  - ✓ Allow write access
- Re-run setup with new key

### Item Not Found

**Error:** "404 Not Found" for specific item

**Possible causes:**
- Item key is invalid
- Item was deleted from Zotero
- Library ID mismatch

**Solution:**
- Verify item exists in Zotero
- Check Library ID in Keychain is correct

### Version Conflict

**Error:** "PreConditionFailed" or version conflict

**Solution:**
- Item was modified elsewhere
- Script will skip and continue with next items
- Re-run script to retry failed items

## Tag Format

**Format:** `Zotero-MCP-Results-YYYY-MM-DD-HHMM`

**Examples:**
- `Zotero-MCP-Results-2025-10-25-1417`
- `Zotero-MCP-Results-2025-10-26-0930`

**Benefits:**
- Sortable by date/time
- Clearly indicates source (MCP search)
- Unique per search session
- Easy to search in Zotero

## Integration with Zotero MCP Skill

This skill complements the Zotero MCP skill:

1. **Zotero MCP Skill** - Search and generate bibliographies
2. **Zotero Tagging Skill** - Tag the items from those bibliographies

**Recommended workflow:**
```
User: "Find papers on Indigenous language certification"
  ↓
Use Zotero MCP Skill → Generate bibliography → Save to file
  ↓
Ask: "Tag these 23 items for later retrieval?"
  ↓
Use Zotero Tagging Skill → Extract keys → Tag items → Report success
```

## File Locations

**Script location:** `/Users/niyaro/Documents/Code/zotero-tag-automation/`

**Key files:**
- `setup_credentials.py` - One-time credential setup
- `tag_items.py` - Reusable tagging script
- `venv/` - Python virtual environment
- `README.md` - User documentation

**Credentials location:** macOS Keychain (service: `zotero-tag-automation`)

## Important Notes

- **Claude Code only** - This skill is designed for Claude Code environment
- **Requires setup** - User must run setup_credentials.py once before first use
- **Write access required** - API key must have write permissions
- **Web API only** - Uses Zotero web API, not local API (local API is read-only)
- **No plain text credentials** - All credentials encrypted in macOS Keychain
- **Timestamps are local** - Tags use system time in YYYY-MM-DD-HHMM format

## Quick Reference Commands

**Setup (one-time):**
```bash
cd /Users/niyaro/Documents/Code/zotero-tag-automation
python3 -m venv venv
source venv/bin/activate
pip install pyzotero keyring
python setup_credentials.py
```

**Tag from bibliography:**
```bash
source venv/bin/activate
grep -o 'items/[A-Z0-9]*' bibliography.md | sed 's/items\///' | xargs python tag_items.py
```

**Tag specific items:**
```bash
source venv/bin/activate
python tag_items.py W44VF3CG M4G5W339 IQBVNCGF
```

**Check credentials:**
```bash
security find-generic-password -s "zotero-tag-automation" -a "library_id"
```

---

**Remember: Always activate the virtual environment (`source venv/bin/activate`) before running Python scripts.**
