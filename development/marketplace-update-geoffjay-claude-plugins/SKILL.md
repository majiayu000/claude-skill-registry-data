---
name: marketplace-update
description: Updates the .claude-plugin/marketplace.json file when plugins are added, modified, or removed. Use when creating or updating plugin entries in the marketplace catalog.
---

# Marketplace Update Skill

This skill provides functionality to update the `.claude-plugin/marketplace.json` file when plugins are added, modified, or removed from the marketplace.

## Purpose

Maintain the marketplace catalog by:

- Adding new plugin entries
- Updating existing plugin metadata
- Removing obsolete plugins
- Validating marketplace structure
- Ensuring consistency across the catalog

## When to Use

Use this skill when:

- A new plugin is created and needs to be registered
- An existing plugin's components change (agents, commands, skills added/removed)
- Plugin metadata needs updating (version, description, keywords, etc.)
- A plugin is being removed from the marketplace
- Validating marketplace.json structure

## Marketplace Structure

The marketplace.json file follows this schema:

```json
{
  "name": "marketplace-name",
  "owner": {
    "name": "Owner Name",
    "email": "email@example.com",
    "url": "https://github.com/username"
  },
  "metadata": {
    "description": "Marketplace description",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "plugin-name",
      "source": "./plugins/plugin-name",
      "description": "Plugin description",
      "version": "1.0.0",
      "author": {
        "name": "Author Name",
        "url": "https://github.com/username"
      },
      "homepage": "https://github.com/username/repo",
      "repository": "https://github.com/username/repo",
      "license": "MIT",
      "keywords": ["keyword1", "keyword2"],
      "category": "category-name",
      "strict": false,
      "commands": ["./commands/command-name.md"],
      "agents": ["./agents/agent-name.md"],
      "skills": ["./skills/skill-name"]
    }
  ]
}
```

## Operations

### Add Plugin

Add a new plugin entry to the marketplace:

```python
# Use the provided Python script
python marketplace_update.py add \
  --name "plugin-name" \
  --description "Plugin description" \
  --version "1.0.0" \
  --category "category-name" \
  --agents "agent1.md,agent2.md" \
  --commands "command1.md,command2.md" \
  --skills "skill1,skill2"
```

**Required Fields:**

- `name` - Plugin name (hyphen-case)
- `description` - Brief plugin description
- `version` - Semantic version (e.g., "1.0.0")

**Optional Fields:**

- `category` - Plugin category (default: "general")
- `agents` - Comma-separated list of agent files
- `commands` - Comma-separated list of command files
- `skills` - Comma-separated list of skill directories
- `keywords` - Comma-separated list of keywords
- `license` - License type (default: "MIT")
- `strict` - Strict mode flag (default: false)

### Update Plugin

Update an existing plugin entry:

```python
python marketplace_update.py update \
  --name "plugin-name" \
  --description "Updated description" \
  --version "1.1.0" \
  --add-agent "new-agent.md" \
  --remove-command "old-command.md"
```

**Update Operations:**

- `--description` - Update description
- `--version` - Update version
- `--category` - Update category
- `--keywords` - Update keywords (replaces all)
- `--add-agent` - Add agent file
- `--remove-agent` - Remove agent file
- `--add-command` - Add command file
- `--remove-command` - Remove command file
- `--add-skill` - Add skill directory
- `--remove-skill` - Remove skill directory

### Remove Plugin

Remove a plugin from the marketplace:

```python
python marketplace_update.py remove --name "plugin-name"
```

### Validate Marketplace

Validate the marketplace.json structure:

```python
python marketplace_update.py validate
```

This checks:

- JSON syntax validity
- Required fields presence
- File path existence
- Component reference validity
- Duplicate plugin names

## Python Script

The skill includes a Python script at `marketplace_update.py` that provides command-line interface for all operations.

### Usage from Claude Code

When invoked as a skill:

1. **Read Plugin Structure**

   - Scan plugin directory for components
   - Extract metadata from frontmatter
   - Build component lists

2. **Execute Python Script**

   - Call marketplace_update.py with appropriate arguments
   - Pass plugin details
   - Handle success/error responses

3. **Validate Result**
   - Verify marketplace.json is valid
   - Confirm plugin entry is correct
   - Report success or errors

## Examples

### Example 1: Add New Plugin

```python
# Plugin: golang-development
# Components: 3 agents, 1 command, 4 skills

python marketplace_update.py add \
  --name "golang-development" \
  --description "Go language development tools" \
  --version "1.0.0" \
  --category "languages" \
  --keywords "golang,go,development" \
  --agents "golang-pro.md,gin-pro.md,charm-pro.md" \
  --commands "golang-scaffold.md" \
  --skills "async-golang-patterns,golang-testing-patterns,golang-packaging,golang-performance-optimization"
```

### Example 2: Update Plugin Version

```python
# Update version and add new agent

python marketplace_update.py update \
  --name "golang-development" \
  --version "1.1.0" \
  --add-agent "gorm-pro.md"
```

### Example 3: Remove Plugin

```python
python marketplace_update.py remove --name "obsolete-plugin"
```

## Integration with Commands

The `/claude-plugin:create` and `/claude-plugin:update` commands should invoke this skill automatically:

### From /claude-plugin:create Command

After creating a new plugin:

```
1. Scan plugin directory for components
2. Extract metadata from agent/command frontmatter
3. Invoke marketplace-update skill:
   - Operation: add
   - Plugin name: [from user input]
   - Components: [scanned from directory]
   - Metadata: [extracted from frontmatter]
```

### From /claude-plugin:update Command

After updating a plugin:

```
1. Determine what changed (added/removed/modified)
2. Invoke marketplace-update skill:
   - Operation: update
   - Plugin name: [from user input]
   - Changes: [specific updates]
```

## Error Handling

### Plugin Already Exists (Add)

```
Error: Plugin 'plugin-name' already exists in marketplace.
Suggestion: Use 'update' operation instead.
```

### Plugin Not Found (Update/Remove)

```
Error: Plugin 'plugin-name' not found in marketplace.
Suggestion: Use 'add' operation to create it.
```

### Invalid JSON

```
Error: marketplace.json contains invalid JSON.
Suggestion: Fix JSON syntax before proceeding.
```

### Component File Missing

```
Warning: Component file './agents/agent-name.md' not found.
Suggestion: Create the file or remove from plugin entry.
```

### Validation Failure

```
Error: Marketplace validation failed:
  - Plugin 'plugin-a' missing required field 'description'
  - Plugin 'plugin-b' references non-existent agent 'missing.md'
Suggestion: Fix errors and validate again.
```

## Best Practices

1. **Always Validate After Changes**

   - Run validate after add/update/remove
   - Fix any warnings or errors
   - Ensure all referenced files exist

2. **Scan Plugin Directory**

   - Don't manually list components
   - Scan directory to detect agents/commands/skills
   - Extract metadata from frontmatter

3. **Semantic Versioning**

   - Patch: Bug fixes, documentation updates (1.0.0 → 1.0.1)
   - Minor: New components, enhancements (1.0.0 → 1.1.0)
   - Major: Breaking changes, removals (1.0.0 → 2.0.0)

4. **Consistent Metadata**

   - Keep descriptions concise (< 100 chars)
   - Use relevant keywords
   - Maintain consistent author information
   - Use appropriate categories

5. **Backup Before Changes**
   - Create backup of marketplace.json
   - Test changes in development first
   - Validate before committing

## Categories

Common plugin categories:

- `languages` - Language-specific tools (Python, Go, Rust, etc.)
- `development` - General development tools
- `security` - Security scanning and analysis
- `testing` - Test generation and automation
- `operations` - DevOps and operations tools
- `infrastructure` - Cloud and infrastructure tools
- `documentation` - Documentation generation
- `architecture` - Architecture and design tools
- `workflow` - Workflow orchestration
- `general` - General purpose tools

## File Structure

```
plugins/claude-plugin/skills/marketplace-update/
├── SKILL.md                    # This file
├── marketplace_update.py       # Python implementation
└── references/                 # Optional examples
    └── examples.md
```

## Requirements

- Python 3.8+
- No external dependencies (uses standard library only)
- Access to `.claude-plugin/marketplace.json`
- Read/write permissions on marketplace file

## Success Criteria

After running this skill:

- ✓ marketplace.json is valid JSON
- ✓ Plugin entry is correct and complete
- ✓ All referenced files exist
- ✓ No duplicate plugin names
- ✓ Required fields are present
- ✓ Validation passes without errors
