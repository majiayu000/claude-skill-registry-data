---
name: share-skill
description: Push a local skill to the Notion skills database. Load when user mentions "share skill", "export skill", "push to notion", "add skill to database", or after creating a new skill with create-skill.
---

# Export Skill to Notion

Push a local skill's metadata and file to the Beam Nexus Skills database in Notion.

## Purpose

This skill takes a local skill from `03-skills/` and creates a new entry in the company's Notion skills database. It handles:

- Validating SKILL.md format before upload
- Reading SKILL.md to extract metadata (including version)
- **Automatically uploading all skill files** via JSON bundle
- Mapping fields to Notion properties
- **MANDATORY user confirmation before pushing**
- Setting Owner from user-config.yaml
- Inferring appropriate Team (or creating new one)
- Creating the database entry with file attachment

**Typically used after `create-skill`** to share new skills with the company.

---

## CRITICAL RULES

1. **ALWAYS confirm with user before pushing** - Never auto-push
2. **ALWAYS set Owner** - Use notion_user_id from user-config.yaml
3. **ALWAYS upload the skill file** - Use Notion File Upload API (see Step 5)
4. **INFER appropriate Team** - Don't default to Solutions. Think about scope:
   - "General" for company-wide utility skills
   - "Solutions" for client-facing/implementation skills
   - "Engineering" for dev tools
   - Create new team if needed
5. **ALWAYS check for duplicates first** - Cannot overwrite others' skills
6. **NEVER delete skills from Notion** - Deletion must be done manually in Notion UI
7. **Use --as-new for improved versions** - Don't overwrite, create new entries

---

## Safeguards

### Pre-Flight Check (ALWAYS Run First)

Before ANY export operation, verify Notion setup:

```bash
python ../../notion-master/scripts/check_notion_config.py
```

**If configuration missing:**
- Option A: Run setup wizard: `python ../../notion-master/scripts/setup_notion.py`
- Option B: See [../../notion-master/references/setup-guide.md](../../notion-master/references/setup-guide.md)

**Expected output if configured:**
```
✅ ALL CHECKS PASSED
You're ready to use Notion skills
```

### SKILL.md Validation

The upload script automatically validates SKILL.md before uploading:

```
[INFO] Validating SKILL.md...
[OK] SKILL.md valid
```

**Validation checks:**
- YAML frontmatter exists (starts with `---`)
- Required fields present: `name`, `description`
- Description contains trigger phrases (contains "when")
- Version format is valid (semantic versioning: 1.0, 1.0.0)

**If validation fails:**
```
[ERROR] SKILL.md validation failed:
  ✗ Missing required field: description
  ✗ Description should include trigger phrases

Fix these issues or use --skip-validation to bypass.
```

### Duplicate Detection

**When skill name already exists in Notion:**

```
[ERROR] Skill 'my-skill' already exists in Notion!
  Owner: Jack Li
  Version: 1.0
  URL: https://notion.so/my-skill-abc123

Options:
  1. Use --as-new "new-name" to upload as improved version
  2. Delete existing skill in Notion first
```

**No overwriting allowed** - This prevents accidental data loss and maintains clear ownership.

### Prohibited Operations

| Operation | Status | Notes |
|-----------|--------|-------|
| Create new skill | ✅ Allowed | With confirmation |
| Create improved version | ✅ Allowed | Use --as-new flag |
| Overwrite existing | ❌ Blocked | Must delete in Notion first |
| Delete any skill | ❌ Blocked | Must use Notion UI |
| Bulk push | ❌ Blocked | One at a time only |


---

## Workflow

### Step 1: Read Local Skill

```bash
# Get skill metadata from SKILL.md
cat 03-skills/{skill-name}/SKILL.md
```

**Extract from YAML header:**
- `name` → Skill Name
- `description` → Description
- `version` → Version (defaults to 1.0)

**Extract from content:**
- Purpose section → Purpose field

### Step 2: Prepare Skill Bundle

The upload script automatically creates a JSON bundle containing all skill files:
- SKILL.md (required)
- scripts/ folder (optional)
- references/ folder (optional)
- assets/ folder (optional)

**Bundle format**: `{skill-name}.skill.json`

```json
{
  "skill_name": "my-skill",
  "version": "1.0",
  "bundle_format": "nexus-skill-bundle-v1",
  "created": "2025-12-10",
  "files": {
    "SKILL.md": "<base64-encoded content>",
    "scripts/script.py": "<base64-encoded content>",
    "references/guide.md": "<base64-encoded content>"
  }
}
```

**Note**: Notion File Upload API doesn't support .zip files, so we use JSON with base64-encoded file contents. This preserves the full skill structure including scripts and references.

### Step 3: Infer Team and Gather Info

**AI should infer the Team based on skill purpose:**
- **General**: Utility skills usable by anyone (query tools, import/export, etc.)
- **Solutions**: Client implementation, onboarding, customer-facing
- **Engineering**: Developer tools, CI/CD, testing
- **Sales**: Sales-specific workflows
- **Other**: Ask user if unclear

**Present inference to user for confirmation:**
```
Based on the skill's purpose, I suggest Team: "General"
(This is a utility skill for querying Notion databases)

Is this correct, or would you prefer a different team?
```

### Step 4: Preview Before Push (MANDATORY)

**Use --dry-run to preview without uploading:**
```bash
python ../../notion-master/scripts/upload_skill.py 03-skills/{skill-name} --team General --dry-run
```

**Output:**
```
==================================================
[PREVIEW] Upload Summary
==================================================
  Skill Name:  my-skill
  Version:     1.0
  Team:        General
  Owner:       Fredrik Falk
  Bundle:      my-skill.skill.json
  Size:        4,521 bytes
  Files:       3
==================================================

[DRY-RUN] No changes made. Remove --dry-run to upload.
```

**WAIT FOR USER CONFIRMATION BEFORE PROCEEDING**

### Step 5: Create Notion Entry with File

**Use the upload script:**
```bash
python ../../notion-master/scripts/upload_skill.py 03-skills/{skill-name} --team General
```

**Optional parameters:**
```bash
# With integrations
python ../../notion-master/scripts/upload_skill.py 03-skills/my-skill --team General --integration "Beam AI,Linear"

# Dry run (preview without uploading)
python ../../notion-master/scripts/upload_skill.py 03-skills/my-skill --team General --dry-run

# Upload as new skill with different name (for improved versions)
python ../../notion-master/scripts/upload_skill.py 03-skills/my-skill --team General --as-new "my-skill-enhanced"

# Skip validation (not recommended)
python ../../notion-master/scripts/upload_skill.py 03-skills/my-skill --team General --skip-validation
```

**The script handles:**
1. Validating SKILL.md format
2. Reading SKILL.md metadata (including version)
3. Checking for duplicates
4. Creating JSON bundle with all files
5. Creating file upload object
6. Uploading file content
7. Creating database entry with attachment

### Step 6: Confirm Success

```
✅ Skill pushed to Notion!

📄 Skill Name: {skill-name}
📊 Version: 1.0
🔗 Notion URL: {url}
👥 Owner: {owner-name}
📁 Team: {team}
📎 Files in bundle: 3

The skill is now discoverable by anyone at Beam AI.
```

---

## Version Tracking

**Add version to SKILL.md frontmatter:**
```yaml
---
name: my-skill
description: Load when user says "do the thing"...
version: 1.0
---
```

### Version Format Standard

**Format**: `MAJOR.MINOR` or `MAJOR.MINOR.PATCH`

| Valid | Invalid |
|-------|---------|
| `1.0` | `v1.0` (no "v" prefix) |
| `1.1` | `1` (needs MAJOR.MINOR) |
| `2.0` | `latest` (must be numeric) |
| `1.0.0` | `1.0.0.0` (too many segments) |

### When to Increment

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| Bug fixes, typos | Increment MINOR | `1.0` → `1.1` |
| Minor improvements | Increment MINOR | `1.1` → `1.2` |
| New features added | Increment MINOR | `1.2` → `1.3` |
| **Breaking changes** | Increment MAJOR | `1.x` → `2.0` |
| **Complete rewrite** | Increment MAJOR | `2.x` → `3.0` |

### Version Tracking Locations

Version is tracked in 3 places:
1. **SKILL.md frontmatter** - Source of truth (`version:` field)
2. **JSON bundle** - Embedded in upload (`"version": "1.0"`)
3. **Notion database** - Displayed in `Version` column

### Uploading Improved Versions

**For significant improvements, use --as-new:**
```bash
python upload_skill.py 03-skills/my-skill --team General --as-new "my-skill-v2"
```

This creates a new database entry rather than overwriting (which is blocked).

---

## Field Mapping

**See complete database schema:**
- [../../notion-master/references/database-schema.md](../../notion-master/references/database-schema.md)

**Quick reference:**

| Local (SKILL.md) | Notion Property | Type | Required | Notes |
|------------------|-----------------|------|----------|-------|
| `name:` in YAML | Skill Name | title | Yes | |
| `description:` in YAML | Description | rich_text | Yes | |
| `version:` in YAML | Version | rich_text | Yes | Defaults to 1.0 |
| Purpose section | Purpose | rich_text | No | Extract from ## Purpose |
| AI infers + user confirms | Team | select | Yes | Create if doesn't exist |
| AI infers from content | Integration | multi_select | No | Beam AI, Linear, Notion, etc. |
| user-config.yaml | Owner | people | Yes | notion_user_id |
| Today's date | Created | date | Yes | Auto-set |
| JSON bundle | Skill | files | Yes | Auto-uploaded via File Upload API |

---

## Configuration

**From `.env`:**
- `NOTION_API_KEY` - Your Notion integration token
- `NOTION_SKILLS_DB_ID` - Database ID: `2bc2cadf-bbbc-80be-af8a-d45dfc8dfa2e`

**From `user-config.yaml`:**
- `notion_user_id` - Your Notion user ID for Owner field
- `notion_user_name` - Display name

**Available Teams** (can create new):
- General (for utility/company-wide skills)
- Solutions (for client-facing skills)
- Engineering (for dev tools)
- Sales (for sales workflows)

**Available Integrations:**
- Beam AI
- Linear
- Notion

---

## Team Inference Rules

| Skill Type | Suggested Team | Reasoning |
|------------|----------------|-----------|
| Query/import/export tools | General | Used by everyone |
| Notion/Linear integrations | General | Cross-functional |
| Client onboarding | Solutions | Client-facing |
| Agent building/testing | Solutions | Implementation work |
| CI/CD, testing tools | Engineering | Dev-focused |
| Proposal generators | Sales | Sales-specific |
| Unknown | Ask user | When unclear |

---

## Example Usage

### Export a New Skill

```
User: "Push query-notion-db to Notion"

AI: [Validates SKILL.md - passes]
    [Checks for duplicates - none found]

    Based on the skill's purpose (querying Notion databases for any use),
    I suggest Team: "General"

    This is a utility skill that anyone at Beam AI could use.
    Is this correct? (yes/no/specify different)

User: "yes"

AI: Running dry-run preview...

    ==================================================
    [PREVIEW] Upload Summary
    ==================================================
      Skill Name:  query-notion-db
      Version:     1.0
      Team:        General
      Owner:       Fredrik Falk
      Bundle:      query-notion-db.skill.json
      Size:        4,521 bytes
      Files:       2
    ==================================================

    Do you want to push this to Notion? (yes/no)

User: "yes"

AI: ✅ Skill pushed to Notion!
    📄 Skill Name: query-notion-db
    📊 Version: 1.0
    🔗 https://notion.so/query-notion-db-abc123
    👥 Owner: Fredrik Falk
    📁 Team: General
```

### Export Improved Version of Existing Skill

```
User: "Push my improved version of setup-linear-onboarding-template"

AI: [Validates SKILL.md - passes]
    [Checks for duplicates]

    ⚠️ Skill "setup-linear-onboarding-template" already exists in Notion!
      Owner: Jack Li
      Version: 1.0

    Since you've made improvements, I recommend uploading as a new skill.
    Suggested name: "setup-linear-onboarding-template-enhanced"

    Would you like to:
    1. Upload as "setup-linear-onboarding-template-enhanced"
    2. Choose a different name
    3. Cancel

User: "1"

AI: ✅ Skill pushed to Notion!
    📄 Skill Name: setup-linear-onboarding-template-enhanced
    📊 Version: 1.0
    🔗 https://notion.so/setup-linear-onboarding-template-enhanced-def456
```

---

## Error Handling

**Common errors:**

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Check NOTION_API_KEY in .env |
| 400 Bad Request | Invalid property format | Check field mapping |
| Skill already exists | Duplicate in Notion | Use --as-new or delete in Notion |
| Missing notion_user_id | Not in user-config.yaml | Prompt to add it |
| Missing SKILL.md | Invalid skill path | Verify path |
| Validation failed | Invalid SKILL.md format | Fix issues or use --skip-validation |

**For detailed troubleshooting:**
- See [../../notion-master/references/error-handling.md](../../notion-master/references/error-handling.md)

---

## Notes

- **File upload**: Uses Notion's File Upload API (3-step process: create upload object → send file → attach to page). Skills are packaged as JSON bundles (`.skill.json`) containing all files with base64-encoded contents. This preserves the complete skill structure including scripts/, references/, and assets/ folders.
- **Validation**: SKILL.md is validated before upload. Use --skip-validation to bypass (not recommended).
- **Dry-run**: Use --dry-run to preview what would be uploaded without actually pushing.
- **Improved versions**: Use --as-new "new-name" to upload improved versions without overwriting.
- **Version tracking**: Add `version:` to SKILL.md frontmatter. Tracked in bundle AND Notion.
- **New teams auto-create**: If you specify a team that doesn't exist, Notion will create it automatically.
- **Owner is mandatory**: Always set from user-config.yaml to maintain audit trail.
- **Always confirm**: Never push without explicit user approval.

---

## Additional References

**For more details:**
- [../../notion-master/references/setup-guide.md](../../notion-master/references/setup-guide.md) - Initial setup
- [../../notion-master/references/api-reference.md](../../notion-master/references/api-reference.md) - File upload API
- [../../notion-master/references/database-schema.md](../../notion-master/references/database-schema.md) - Complete schema
- [../../notion-master/references/error-handling.md](../../notion-master/references/error-handling.md) - Troubleshooting
