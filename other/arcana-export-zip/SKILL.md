---
name: arcana-export-zip
description: >
  Export a Claude Code skill as a ZIP file for upload to claude.ai web interface.
  Analyzes the skill, bundles dependencies, transforms frontmatter, and creates
  a self-contained ZIP. Trigger phrases: "export for claude.ai", "create ZIP",
  "export skill", "download skill".
---

# Arcana Export ZIP: Export for claude.ai

Export a Claude Code skill as a ZIP file for upload to claude.ai.

## Path Convention

`{PLUGIN_ROOT}` = This plugin's root directory (where plugin.json lives)

## What This Does

1. Analyzes the skill to understand what it does
2. Identifies all files the skill needs
3. Transforms frontmatter (strips CC-only fields)
4. Validates for API compatibility
5. Creates a self-contained ZIP

## Workflow

### Step 1: Analyze the Skill

Read `{PLUGIN_ROOT}/lib/patterns/skill-analysis.md` for guidance.

1. **Read the SKILL.md** - Understand what it does
2. **Explore the skill directory** - Find supporting files
3. **Trace dependencies** - Find referenced files (see `{PLUGIN_ROOT}/lib/patterns/dependency-resolution.md`)

Build a file manifest of everything to bundle.

### Step 2: Transform Frontmatter

Read `{PLUGIN_ROOT}/lib/patterns/frontmatter-transform.md` for guidance.

1. Extract YAML frontmatter from SKILL.md
2. Remove Claude Code-only fields:
   - `allowed-tools`
   - `hooks`
   - `context`
   - `agent`
   - `model`
   - `user-invocable`
   - `disable-model-invocation`
3. Keep: `name`, `description`, `version`

### Step 3: Validate

Read `{PLUGIN_ROOT}/lib/references/validation-rules.md` for rules.

Check:
- **Name**: ≤64 chars, lowercase/numbers/hyphens, no "claude"/"anthropic"
- **Description**: 1-1024 chars, non-empty, no XML tags

If validation fails:
- Report the specific issue
- Suggest a fix
- Ask user how to proceed (don't auto-fix)

### Step 4: Prepare Files

1. Create a temp directory
2. Write the transformed SKILL.md
3. Copy all dependency files, preserving relative paths

### Step 5: Create ZIP

Use the zip tool with your file manifest:

```bash
python3 "{PLUGIN_ROOT}/lib/tools/zip_skill.py" \
  --name {skill-name} \
  --output ~/Downloads/{skill-name}.zip \
  --base-path {temp-directory} \
  {file1} {file2} {file3} ...
```

### Step 6: Report Result

```
Export complete!

Skill: my-skill
Output: ~/Downloads/my-skill.zip
Files: 5 files bundled

To upload to claude.ai:
1. Go to claude.ai
2. Click Settings → Features → Skills
3. Upload ~/Downloads/my-skill.zip
```

## Example Session

**User:** Export the hiivmind-corpus-atproto skill

**Claude:**
1. Reading skill at `/path/to/hiivmind-corpus-atproto/SKILL.md`...
2. This skill provides documentation lookup for AT Protocol.
3. Found dependencies:
   - `data/index.md` - Documentation index
   - `references/overview.md` - Overview document
4. Transforming frontmatter (stripping: allowed-tools, model)...
5. Validation passed: name OK, description OK
6. Creating ZIP with 4 files...

```bash
python3 lib/tools/zip_skill.py \
  --name hiivmind-corpus-atproto \
  --output ~/Downloads/hiivmind-corpus-atproto.zip \
  --base-path /tmp/transformed \
  SKILL.md data/index.md references/overview.md
```

**Export complete!**

## Error Handling

| Error | Resolution |
|-------|------------|
| SKILL.md not found | Check path, ask user to specify |
| Name validation failed | Suggest alternative name, ask user |
| Missing dependency | Warn and continue, or ask if critical |
| ZIP creation failed | Check disk space, permissions |

## Related Patterns

- `{PLUGIN_ROOT}/lib/patterns/skill-analysis.md` - How to analyze skills
- `{PLUGIN_ROOT}/lib/patterns/dependency-resolution.md` - How to find dependencies
- `{PLUGIN_ROOT}/lib/patterns/frontmatter-transform.md` - How to transform
- `{PLUGIN_ROOT}/lib/patterns/validation.md` - How to validate
