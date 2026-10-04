---
name: arcana-upload-api
description: >
  Upload a Claude Code skill to the Anthropic Skills API for workspace-wide availability.
  Analyzes the skill, bundles dependencies, transforms frontmatter, validates, and uploads.
  Tracks uploads for future updates. Trigger phrases: "upload to API", "publish skill",
  "sync to API", "upload skill".
---

# Arcana Upload API: Upload to Messages API

Upload a Claude Code skill to the Anthropic Skills API.

## Path Convention

`{PLUGIN_ROOT}` = This plugin's root directory (where plugin.json lives)

## Prerequisites

- `ANTHROPIC_API_KEY` environment variable must be set
- Python 3.8+ with `requests` and `pyyaml` packages

## What This Does

1. Analyzes the skill to understand what it does
2. Identifies all files the skill needs
3. Transforms frontmatter (strips CC-only fields)
4. Validates for API compatibility
5. Creates a ZIP file
6. Uploads to Anthropic Skills API
7. Tracks the upload for future updates

## Workflow

### Step 1: Check Prerequisites

Verify API key is set:

```bash
if [ -z "$ANTHROPIC_API_KEY" ]; then
  echo "ANTHROPIC_API_KEY not set"
fi
```

If not set, ask user to set it.

### Step 2: Check State

Read `{PLUGIN_ROOT}/lib/patterns/state-tracking.md` for guidance.

Check if this skill has been uploaded before:

```bash
python3 "{PLUGIN_ROOT}/lib/tools/state.py" get {skill-name}
```

If found:
- Inform user: "Skill already uploaded (v2). Will create new version."
- Use stored skill_id for version creation

If not found:
- Inform user: "New skill. Will create."

### Step 3: Analyze the Skill

Same as export-zip - read `{PLUGIN_ROOT}/lib/patterns/skill-analysis.md`.

1. Read the SKILL.md
2. Explore the skill directory
3. Trace dependencies
4. Build file manifest

### Step 4: Transform Frontmatter

Same as export-zip - read `{PLUGIN_ROOT}/lib/patterns/frontmatter-transform.md`.

Strip CC-only fields, keep name/description/version.

### Step 5: Validate

Same as export-zip - read `{PLUGIN_ROOT}/lib/references/validation-rules.md`.

Validate name and description.

### Step 6: Create ZIP

Same as export-zip:

```bash
python3 "{PLUGIN_ROOT}/lib/tools/zip_skill.py" \
  --name {skill-name} \
  --output /tmp/{skill-name}.zip \
  --base-path {temp-directory} \
  {files...}
```

### Step 7: Upload to API

Read `{PLUGIN_ROOT}/lib/references/api-spec.md` for API details.

**For new skill:**

```bash
python3 "{PLUGIN_ROOT}/lib/tools/api.py" upload /tmp/{skill-name}.zip \
  --title "{Skill Title}"
```

**For existing skill (new version):**

```bash
python3 "{PLUGIN_ROOT}/lib/tools/api.py" version {skill_id} /tmp/{skill-name}.zip
```

### Step 8: Update State

Record the upload:

```bash
python3 "{PLUGIN_ROOT}/lib/tools/state.py" set {skill-name} \
  --skill-id {skill_id} \
  --source-path {original-skill-path}
```

### Step 9: Report Result

**New skill:**
```
Upload complete!

Skill: my-skill
ID: skill_01AbCdEfGhIjKlMnOpQrStUv
Version: 1
Status: Created

To use in Messages API:
{
  "container": {
    "skills": [
      {
        "type": "custom",
        "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
        "version": "latest"
      }
    ]
  }
}
```

**Updated skill:**
```
Upload complete!

Skill: my-skill
ID: skill_01AbCdEfGhIjKlMnOpQrStUv
Version: 3 (updated from v2)
Status: New version created

The latest version is now active for "version": "latest"
```

## Example Session

**User:** Upload the github-helper skill to the API

**Claude:**
1. Checking ANTHROPIC_API_KEY... ✓ Set
2. Checking state... Not found (new skill)
3. Reading skill at `/path/to/github-helper/SKILL.md`...
4. This skill helps with GitHub operations.
5. Found dependencies: 2 files
6. Transforming frontmatter (stripping: allowed-tools, hooks)...
7. Validation passed
8. Creating ZIP...
9. Uploading to API...

```bash
python3 lib/tools/api.py upload /tmp/github-helper.zip --title "GitHub Helper"
```

```json
{
  "id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
  "title": "GitHub Helper",
  "version": 1
}
```

10. Recording state...

**Upload complete!**

## Error Handling

| Error | Resolution |
|-------|------------|
| API key not set | Ask user to set ANTHROPIC_API_KEY |
| 401 Unauthorized | Check API key is valid |
| 422 Validation error | Check name/description, report specific issue |
| 429 Rate limited | Wait and retry |
| Network error | Retry with backoff |

## Cleanup

After successful upload, optionally delete the temporary ZIP:

```bash
rm /tmp/{skill-name}.zip
```

## Related Patterns

- `{PLUGIN_ROOT}/lib/patterns/skill-analysis.md` - How to analyze skills
- `{PLUGIN_ROOT}/lib/patterns/state-tracking.md` - How to track uploads
- `{PLUGIN_ROOT}/lib/references/api-spec.md` - API specification
