---
name: obsidian-shaper
description: This skill should be used when the user asks to "create a note in Obsidian", "add to my vault", "search notes by tag", "find orphaned notes", "list recent notes", "analyze vault connections", "parse frontmatter", or needs to work with any Obsidian vault or markdown folder.
---

# Obsidian Shaper - Shape Your Vault

Shape any Obsidian vault or markdown folder - create notes, search content, and analyze connections. No external dependencies required.

## IMPORTANT: First-Run Setup

**Before running ANY vault operation, you MUST check if the vault is configured.**

**Setup Flow (Steps Must Be Sequential):**
```
Step 1: Check status
   ↓
   ├─ ready → Skip to Step 5 (proceed with operation)
   └─ needs_setup or suggest_folders → Continue below

Step 2: Ask user for vault path + Scan path
   ↓ (MUST continue to Step 3)

Step 3: Show scan results + Ask user to confirm settings
   ↓ (MUST wait for user response)

Step 4: Write config with user-confirmed settings
   ↓
Step 5: Proceed with original request
```

**⚠️ You CANNOT skip steps. Each step must complete before proceeding to the next.**

### Step 1: Check Setup Status

```bash
uv run python skills/obsidian-shaper/scripts/setup_check.py
```

This returns JSON with a `status` field:

| Status | Meaning | Required Next Step |
|--------|---------|-------------------|
| `ready` | Vault configured and valid | Skip to Step 5 (proceed with operation) |
| `needs_setup` | No vault configured | **MUST** proceed to Step 2 → Step 3 → Step 4 |
| `suggest_folders` | Vault path set, folders not configured | **MUST** proceed to Step 3 → Step 4 |

### Step 2: If `needs_setup` - Ask User for Vault Path

Use AskUserQuestion to ask:

**Question:** "Where is your Obsidian vault or notes folder located?"

**Options:**
- `~/Desktop/Vault`
- `~/Documents/Obsidian`
- `~/Obsidian`
- Other (let user enter path)

Then scan the path to detect patterns:

```bash
uv run python skills/obsidian-shaper/scripts/setup_check.py scan "<USER_PATH>"
```

**⚠️ STOP - Do not proceed to Step 4 yet. You MUST complete Step 3 first.**

### Step 3: Show Scan Results and Ask User to Confirm (REQUIRED)

**After running the scan above**, examine the JSON output for detected folders.

**You MUST ask the user the following question, regardless of whether folders were detected:**

Use AskUserQuestion with this format:

**If folders were detected:**
- Question: "I found these folders in your vault: [list detected folders]. Should I use these settings?"
- Options: "Yes, use detected settings" / "No, use vault root for everything" / "Let me customize"

**If no folders were detected:**
- Question: "I didn't detect any special folders. Where should new notes be saved?"
- Options: "Use vault root for everything" / "Let me specify folders"

**DO NOT proceed to Step 4 until the user responds.**

### Step 4: Write Configuration

**⚠️ Only execute this step AFTER receiving the user's response in Step 3.**

Based on the user's choice from Step 3, construct the command:

**If user chose "Yes, use detected settings":**
```bash
uv run python skills/obsidian-shaper/scripts/setup_check.py write "<VAULT_PATH>" \
  --templates "<DETECTED_TEMPLATES>" \
  --output "<DETECTED_OUTPUT>"
```

**If user chose "No, use vault root" or "Use vault root for everything":**
```bash
uv run python skills/obsidian-shaper/scripts/setup_check.py write "<VAULT_PATH>"
```
(Omit both `--templates` and `--output` flags)

**If user chose "Let me customize" or "Let me specify folders":**
Ask follow-up questions for folder names, then include those in the command.

**WARNING:** Only include `--templates` and `--output` flags if the user explicitly confirmed those settings in Step 3.

### Step 5: Proceed with Original Request

Once setup is complete, run the original command the user requested.

---

## Core Operations

### Create Note

```bash
uv run python skills/obsidian-shaper/scripts/note_creator.py "Note Title" \
  --tags tag1 tag2 \
  --content "Note content here" \
  --subfolder "Subfolder"  # Optional
```

### Search by Tag

```bash
uv run python skills/obsidian-shaper/scripts/vault_ops.py search --tag <TAG>
```

### List Notes

```bash
uv run python skills/obsidian-shaper/scripts/vault_ops.py list
uv run python skills/obsidian-shaper/scripts/vault_ops.py list --recent 7
uv run python skills/obsidian-shaper/scripts/vault_ops.py list --folder "Subfolder"
```

### Parse Frontmatter

```bash
uv run python skills/obsidian-shaper/scripts/vault_ops.py frontmatter "path/to/note.md"
```

### Extract Links

```bash
uv run python skills/obsidian-shaper/scripts/vault_ops.py links "path/to/note.md"
```

### Find Orphaned Notes

```bash
uv run python skills/obsidian-shaper/scripts/link_analyzer.py orphans
```

### Suggest Links

```bash
uv run python skills/obsidian-shaper/scripts/link_analyzer.py suggest "path/to/note.md"
```

### Find Related Notes

```bash
uv run python skills/obsidian-shaper/scripts/link_analyzer.py related "path/to/note.md"
```

### Build Knowledge Graph

```bash
uv run python skills/obsidian-shaper/scripts/link_analyzer.py graph --output graph.json
```

---

## Common Workflows

### Document Something New

1. Create note with relevant tags
2. Use `suggest` to find related notes
3. Add wikilinks to connect content

### Clean Up Orphans

1. Run `orphans` to find disconnected notes
2. For each orphan, run `suggest` to get link recommendations
3. Add connections to integrate into knowledge graph

### Explore a Topic

1. Search by tag to find relevant notes
2. Use `related` to find notes with shared tags
3. Build graph to visualize connections

---

## Reference Files

- **`references/command-reference.md`** - Complete CLI reference
- **`references/advanced.md`** - Python API and troubleshooting

## Scripts

- **`setup_check.py`** - Setup verification and auto-detection
- **`vault_ops.py`** - List, search, frontmatter, links
- **`note_creator.py`** - Create notes with frontmatter
- **`link_analyzer.py`** - Analyze connections, orphans, suggestions
