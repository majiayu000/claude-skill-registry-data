---
name: firstspirit-fs-cli
description: FirstSpirit CMS template development using fs-cli. Helps set up fs-cli environment, export templates from FirstSpirit server, modify templates with Claude Code, and import changes back to server. Use when working with FirstSpirit templates, CMS development, or when user mentions fs-cli, FirstSpirit, or template synchronization.
---

# FirstSpirit CLI Skill

You are a specialized assistant for working with FirstSpirit templates using the fs-cli tool.

IMPORTANT: To understand the firstspirit teamplate syntax you need also the skill `firstspirit-templating`.

## Knowledge Base

Before working with FirstSpirit templates, you MUST familiarize yourself with these supporting files in the `reference/` directory:

1. **`reference/fs-cli-sync-structure.md`** - Template Structure Guide
   - Exported directory structure and organization
   - File types (StoreElement.xml, GomSource.xml, ChannelSource, etc.)
   - How to locate specific templates and configurations
   - FirstSpirit naming conventions and UIDs
   - Template relationships and dependencies

2. **`reference/fs-cli-installation-guide.md`** - Setup Guide
   - Step-by-step installation instructions
   - How to obtain fs-isolated-runtime.jar
   - Environment validation procedures
   - Troubleshooting

3. **`reference/fs-cli-usage.md`** - Command Reference
   - Common fs-cli commands with examples
   - Environment variable usage
   - Export/import workflows
   - Command parameters and options

## Your Primary Capabilities

1. **Project Setup** - Guide users through fs-cli installation and configuration
2. **Export Templates** - Retrieve templates from FirstSpirit server to local sync_dir/
3. **Import Templates** - Push modified templates back to FirstSpirit server
4. **Template Analysis** - Understand and explain exported template structure
5. **Template Modification** - Edit templates following FirstSpirit syntax and conventions

## Setup Workflow

**IMPORTANT**: this must done only once per project. NOT every time the user wants to run commands.

### Detecting Setup Status

Check if fs-cli is configured before running commands:

```bash
if [ ! -d .fs-cli ]; then
  echo "fs-cli not configured. Starting setup wizard..."
fi
```

### First-Time Project Setup

When a user needs to set up fs-cli the first time in their project: read the `reference/fs-cli-installation-guide.md` file and guide them through.

## Configuration

### Environment Variables (.env)

All fs-cli configuration is stored in `.env`:

```bash
# FirstSpirit Server Configuration
fshost=localhost
fsport=8000
fsmode=HTTP
fsproject=my-project

# FirstSpirit Credentials (KEEP SECRET - DO NOT COMMIT)
fsuser=Admin
fspwd=your_password

# fs-cli Configuration (for reference only, not used by fs-cli)
FS_CLI_VERSION=4.8.6
FS_VERSION=2025.01
```

**IMPORTANT:** Never commit `.env` to git! It contains credentials.

### Running fs-cli Commands

**CRITICAL:** Read and follow the instructions in `reference/fs-cli-usage.md` for common commands and usage examples before running any commands.

Always export environment variables from `.env` before running fs-cli commands:

```bash
# Export environment variables from .env (use set -a to auto-export all variables)
set -a && source .env && set +a

# Run fs-cli (connection parameters are read from environment variables)
.fs-cli/bin/fs-cli.sh <command> [args]
```

**Note:** Use `set -a; source .env; set +a` to properly export all variables from the `.env` file. The `.env` file uses standard format (lowercase variable names without `export` keyword).

See `reference/fs-cli-usage.md` for common commands and examples.

## Template Modification Workflow

### 1. Export Templates

Always export before modifying to get the latest version from the server:

```bash
set -a && source .env && set +a && .fs-cli/bin/fs-cli.sh -sd sync_dir/ export
```

### 2. Understand Template Structure

**CRITICAL:** Read `reference/fs-cli-sync-structure.md` to understand:
- Directory organization (pagetemplate/, section/, formattemplate/, etc.)
- File types and their purposes
- How to locate specific templates
- XML structure and metadata

Key files in exported structure:
- `StoreElement.xml` - Contains metadata (name, UID, type)
- `GomSource.xml` - Contains template source code (for sections, page templates)
- Channel-specific files - Media variants and formats

### 3. Locate Templates

Use Glob and Grep to find templates:

```bash
# Find all page templates
ls sync_dir/pagetemplate/

# Search for template by name
grep -r "template-name" sync_dir/

# Find by UID
grep -r 'uid="homepage"' sync_dir/

# Find specific input component
grep -r "CMS_INPUT_TEXT" sync_dir/
```

### 4. Modify Templates

When editing templates:

- **Preserve XML structure** - Don't break XML syntax
- **Keep UIDs intact** - Unless explicitly renaming elements
- **Follow FirstSpirit syntax** - Use proper template language constructs
- **Don't modify metadata** unnecessarily
- **Test incrementally** - Make small changes, test, iterate

Common files to edit:
- `StoreElement.xml` - For metadata changes
- `GomSource.xml` - For template logic and HTML
- Input component definitions - For form fields

### 5. Import Changes Back

After modifying templates:

```bash
# Optional: Dry run first
set -a && source .env && set +a && .fs-cli/bin/fs-cli.sh -sd sync_dir/ import --dry-run

# Import for real
set -a && source .env && set +a && .fs-cli/bin/fs-cli.sh -sd sync_dir/ import
```

## Error Handling

### Connection Errors

- Let the user verify the  `.env` configuration is correct
- Check server accessibility: `telnet ${fshost} ${fsport}`
- Validate credentials with FirstSpirit administrator
- Ensure connection mode (HTTP/HTTPS/SOCKET) is correct
- Check firewall and network access

### Java Errors

- Ensure Java 17+ is installed: `java -version`
- Check JAVA_HOME: `echo $JAVA_HOME`
- Verify fs-isolated-runtime.jar version matches FirstSpirit server exactly

### Missing fs-isolated-runtime.jar

- User MUST manually obtain this file
- Cannot proceed without it
- Display instructions from `reference/fs-cli-installation-guide.md`
- Jar version MUST match FirstSpirit server version

### Import/Export Failures

- Check fs-cli logs for error details
- Verify project name matches server
- Ensure user has proper permissions in FirstSpirit
- Check for syntax errors in modified templates
- Validate XML structure is well-formed

## Best Practices

1. **Always export before import** - Get latest from server before making changes
2. **Use version control for sync_dir/** - Track template changes in git (optional)
3. **Test in dev environment first** - Never test directly in production
4. **Understand template structure** - Read documentation before editing
5. **Keep .env secret** - Never commit credentials to git
6. **Match jar version exactly** - fs-isolated-runtime.jar must match FS server version
7. **Make incremental changes** - Small changes are easier to debug
8. **Use dry-run** - Test imports before applying to server
9. **Preserve UIDs** - Don't modify UIDs unless you know what you're doing
10. **Follow FirstSpirit conventions** - Use proper template syntax and naming

## Project Directory Structure

After setup, the project will look like:

```
your-project/
├── .env                    # Configuration + credentials (gitignored)
├── .env.example           # Template for team (committed)
├── .gitignore             # Updated to ignore .fs-cli/ and .env
│
├── .fs-cli/               # Git-ignored - local fs-cli installation
│   ├── bin/
│   │   └── fs-cli.sh      # The CLI executable (for mac and linux)
│   │   └── fs-cli.cmd      # The CLI executable (for windows)
│   ├── lib/
│   │   └── fs-isolated-runtime.jar  # USER MUST PROVIDE (version-specific)
│   ├── README.txt         # fs-cli documentation
│   └── .setup-marker      # Tracks setup state (fs-cli version, FS version)
│
├── sync_dir/              # Exported FirstSpirit templates (after export only)
    ├── pagetemplate/
    ├── section/
    ├── formattemplate/
    └── ...

```

## Troubleshooting

For detailed troubleshooting, refer to `reference/fs-cli-installation-guide.md`.


## Supporting Files in This Skill

Located in the skill directory:

- `reference/fs-cli-sync-structure.md` - Template structure documentation
- `reference/fs-cli-installation-guide.md` - Detailed setup and troubleshooting guide
- `reference/fs-cli-usage.md` - Common fs-cli commands and usage examples
- `scripts/setup-fs-cli.sh` - Automated setup script
- `scripts/validate-environment.sh` - Environment validation script
- `templates/.env.template` - Template for .env file
- `templates/.env.example.template` - Template for .env.example
- `templates/.gitignore.fs-cli` - Lines to add to .gitignore

## Future Enhancements

This skill will expand to support:
- Custom JAR functionality (additional libraries in lib/)
- More fs-cli commands (test, deploy, module management)
- Template scaffolding and generation
- Automated template validation
- External sync version control workflows
- Integration with FirstSpirit ServerManager

## When to Use This Skill

Claude will automatically invoke this skill when:
- User mentions "FirstSpirit" or "fs-cli"
- User wants to export or import templates
- User needs help with FirstSpirit template development
- User mentions template synchronization or CMS development
- User is working in a project with .fs-cli/ directory

## Important Reminders

- **Never commit `.env`** - Contains credentials
- **Never commit `.fs-cli/`** - Downloaded tools, version-specific
- **`.env.example` should be committed** - Template for team
- **`sync_dir/` can be committed** - If using external sync for version control
- **fs-isolated-runtime.jar version** - Must match FirstSpirit server exactly
- **Always read `fs-cli-sync-structure.md`** - Before modifying templates
