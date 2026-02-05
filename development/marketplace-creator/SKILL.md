---
name: marketplace-creator
description: Guide for creating and managing Claude Code marketplaces. Use when creating a new marketplace, updating marketplace configuration, adding plugins to a marketplace, or validating marketplace.json files.
license: Complete terms in LICENSE.txt
---

# Marketplace Creator

This skill provides comprehensive guidance for creating, managing, and validating Claude Code marketplace configurations.

## About Marketplaces

Marketplaces are curated collections of plugins that can be distributed and installed together. A marketplace is defined by a `marketplace.json` file that lists available plugins with their sources, versions, and metadata.

### What Marketplaces Provide

1. **Plugin Discovery** - Central catalog of related plugins
2. **Version Management** - Track plugin versions and updates
3. **Easy Distribution** - Users install from a single marketplace URL
4. **Curation** - Organize plugins by theme, purpose, or organization

## Marketplace Development Workflow

Follow these steps when working with marketplaces:

1. Understand marketplace requirements and scope
2. Initialize marketplace configuration
3. Add plugins to the marketplace
4. Validate marketplace structure
5. Test marketplace installation
6. Distribute marketplace

### Step 1: Understanding Marketplace Requirements

Before creating a marketplace, clarify:

- What plugins should be included?
- Who is the target audience (personal, team, public)?
- Will plugins be hosted on GitHub, local paths, or other sources?
- What categorization or organization makes sense?

Ask questions to gather concrete requirements:
- "What plugins should this marketplace include?"
- "Will this be for personal use, team distribution, or public sharing?"
- "Are the plugins already created, or do they need to be built?"
- "How should the plugins be categorized or grouped?"

### Step 2: Initialize Marketplace Configuration

Create a new `marketplace.json` file with the required structure.

**For detailed initialization steps:**
- See [references/marketplace-structure.md](references/marketplace-structure.md) for complete setup instructions and field requirements
- Use the `init_marketplace.py` script for quick setup:

```bash
python3 skills/marketplace-creator/scripts/init_marketplace.py
```

The script will:
- Create marketplace.json with proper structure
- Prompt for owner name and email
- Add example plugin entry (to be customized)
- Include comments explaining each field

**Minimum Required Fields:**
```json
{
  "name": "marketplace-name",
  "owner": {
    "name": "Owner Name",
    "email": "email@domain.com"
  },
  "description": "Marketplace description",
  "plugins": []
}
```

### Step 3: Add Plugins to the Marketplace

Add plugin entries to the `plugins` array. Each plugin requires:
- `name` - Plugin identifier
- `source` - Where to find the plugin (GitHub, local path, URL)
- `description` - What the plugin does
- `version` - Semantic version (e.g., "1.0.0")
- `author` - Plugin author information

**Helper script for adding plugins:**
```bash
python3 skills/marketplace-creator/scripts/add_plugin_to_marketplace.py
```

**For detailed plugin entry formats and source options:**
- See [references/marketplace-structure.md](references/marketplace-structure.md) for all source format examples

**Common Source Formats:**

1. **GitHub Repository (recommended for public plugins):**
   ```json
   "source": {
     "source": "github",
     "repo": "owner/repository"
   }
   ```

2. **Relative Path (local installations only):**
   ```json
   "source": "./plugins/my-plugin"
   ```

3. **Git Repository URL:**
   ```json
   "source": {
     "source": "url",
     "url": "https://gitlab.com/team/plugin.git"
   }
   ```

4. **Direct Marketplace URL:**
   ```json
   "source": "https://example.com/path/to/marketplace.json"
   ```

### Step 4: Validate Marketplace Structure

Use the validation script to check marketplace configuration:

```bash
python3 skills/marketplace-creator/scripts/validate_marketplace.py
```

The validator checks:
- JSON syntax validity
- Required fields are present
- Source format correctness (GitHub objects vs strings)
- No placeholder values remain
- Author format consistency
- Semantic versioning compliance

**For complete validation checklist:**
- See validation section in [references/marketplace-structure.md](references/marketplace-structure.md)

### Step 5: Test Marketplace Installation

Test the marketplace locally before distribution:

```bash
# Install from local marketplace.json
claude plugin install /path/to/marketplace.json

# Or install specific plugin from marketplace
claude plugin install /path/to/marketplace.json --plugin plugin-name
```

Verify:
- All plugins install correctly
- Skills/commands/agents are available
- No configuration errors or warnings

### Step 6: Distribute Marketplace

Choose distribution method:

**Option 1: Git Repository**
- Commit marketplace.json to repository
- Users install via: `claude plugin install https://github.com/user/repo/marketplace.json`

**Option 2: Direct URL**
- Host marketplace.json on web server
- Users install via: `claude plugin install https://domain.com/marketplace.json`

**Option 3: Local/Team Distribution**
- Share marketplace.json file or repository
- Users install from local path

## Common Issues and Solutions

### Issue: GitHub URL as String

**Problem:** GitHub repository URLs as strings are not supported in marketplace.json

```json
// ❌ WRONG
"source": "https://github.com/username/plugin-name"

// ✅ CORRECT
"source": {
  "source": "github",
  "repo": "username/plugin-name"
}
```

### Issue: Relative Paths for Public Distribution

**Problem:** Relative paths only work for local installations

```json
// ⚠️ WARNING - local only
"source": "./plugins/my-plugin"

// ✅ CORRECT - for public distribution
"source": {
  "source": "github",
  "repo": "username/plugin-name"
}
```

### Issue: Inconsistent Author Format

**Problem:** Author should use consistent object format

```json
// ❌ WRONG - string format
"author": "Username"

// ✅ CORRECT - object format
"author": {
  "name": "Username"
}
```

### Issue: Placeholder Values

**Problem:** Template placeholders must be replaced

```json
// ❌ WRONG
"owner": {
  "name": "Your Name",
  "email": "your.email@example.com"
}

// ✅ CORRECT
"owner": {
  "name": "AnthonyKazyaka",
  "email": "anthony@domain.com"
}
```

## Updating Existing Marketplaces

When updating an existing marketplace.json:

1. **Adding a Plugin:**
   - Use `add_plugin_to_marketplace.py` script
   - Or manually add entry to `plugins` array
   - Validate with `validate_marketplace.py`

2. **Updating Plugin Version:**
   - Locate plugin entry in `plugins` array
   - Update `version` field
   - Ensure plugin source reflects new version

3. **Removing a Plugin:**
   - Remove plugin entry from `plugins` array
   - Validate configuration

4. **Reorganizing Plugins:**
   - Consider creating multiple marketplace.json files
   - Or use plugin descriptions for categorization

## Best Practices

- **Use semantic versioning** - Follow semver (major.minor.patch)
- **Provide clear descriptions** - Help users understand what each plugin does
- **GitHub sources for public plugins** - More reliable than direct URLs
- **Test before distributing** - Install marketplace locally first
- **Version your marketplace** - Track changes to marketplace itself
- **Document plugin requirements** - Note dependencies or prerequisites

**For detailed structure information:**
- See [references/marketplace-structure.md](references/marketplace-structure.md) for:
  - Complete marketplace.json schema
  - All source format options
  - Field requirements and validation rules
  - Example marketplace configurations

**For step-by-step creation guidance:**
- See [references/marketplace-creation-process.md](references/marketplace-creation-process.md) for:
  - Detailed workflow for each step
  - Decision trees for source format selection
  - Testing strategies
  - Distribution best practices

## Resources

This skill includes:

- **scripts/validate_marketplace.py** - Automated validation script
- **scripts/init_marketplace.py** - Initialize new marketplace.json
- **scripts/add_plugin_to_marketplace.py** - Add plugin entries interactively
- **references/marketplace-structure.md** - Complete schema and examples
- **references/marketplace-creation-process.md** - Detailed step-by-step guide
