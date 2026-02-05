---
name: meteor-addon
description: Meteor Client addon development for Minecraft. Use when creating, updating, or working with Meteor Client addons - a Fabric mod framework for Minecraft. Covers workspace setup from the template repository, updating addons when Minecraft/Meteor versions change, finding reference implementations from verified addons, and understanding Meteor's addon structure and APIs.
---

# Meteor Client Addon Development

This skill provides guidance for developing addons for Meteor Client, a Fabric-based Minecraft utility mod.

## Key Resources

- **Template Repository**: https://github.com/MeteorDevelopment/meteor-addon-template
- **Meteor Client Source**: https://github.com/MeteorDevelopment/meteor-client
- **Addon Database**: https://raw.githubusercontent.com/cqb13/meteor-addon-scanner/refs/heads/addons/addons.json

## Workflow Overview

1. **Setup**: Start from the template or clone existing addon
2. **Update Check**: Verify template is current with Meteor/Minecraft versions
3. **Development**: Implement features following Meteor patterns
4. **Reference**: Use filter_addons.py to find examples from verified addons when needed

When you need to find reference implementations, always use the filter_addons.py script to search the addon database rather than manually browsing GitHub or guessing repository URLs.

## Starting a New Addon

### From Template

Clone the meteor-addon-template and customize:

```bash
git clone https://github.com/MeteorDevelopment/meteor-addon-template my-addon
cd my-addon
```

Check if template needs updating by comparing against meteor-client:
1. Clone meteor-client temporarily to workspace: `git clone --depth=1 https://github.com/MeteorDevelopment/meteor-client`
2. Compare key files: `build.gradle`, `gradle.properties`, dependencies, Fabric/Minecraft versions
3. Update your addon's files to match current versions

### Key Files to Configure

- `gradle.properties`: Set Minecraft version, Fabric API version, Meteor dependency
- `build.gradle`: Configure repositories, dependencies, build settings
- `src/main/resources/fabric.mod.json`: Define mod metadata, entrypoint
- `src/main/java/com/example/addon/Addon.java`: Main addon class

## Updating Existing Addons

When Minecraft or Meteor updates:

1. **Clone meteor-client for reference**:
```bash
cd /path/to/workspace
git clone --depth=1 https://github.com/MeteorDevelopment/meteor-client
```

2. **Check version changes**:
   - Minecraft version in `gradle.properties`
   - Fabric API version
   - Meteor Client version/dependency format
   - Java version requirements

3. **Update breaking changes**:
   - Check meteor-client commit history for API changes
   - Look for deprecated methods or refactored classes
   - Update imports and method calls

4. **Find updated examples**: Use `scripts/filter_addons.py` to find verified addons on current version

## Finding Reference Implementations

The addon database contains metadata about all known Meteor Client addons. Use the filter_addons.py script to find high-quality examples for reference.

### Basic Usage

```bash
# Find verified addons for a specific Minecraft version
python scripts/filter_addons.py --mc-version 1.21.11 --verified

# Find all addons for a version (including unverified)
python scripts/filter_addons.py --mc-version 1.21.11 --no-verified

# Limit results
python scripts/filter_addons.py --mc-version 1.21.11 --verified --limit 10

# Get JSON output for programmatic use
python scripts/filter_addons.py --mc-version 1.21.11 --verified --json
```

### Advanced Filtering

```bash
# Find addons with specific features
python scripts/filter_addons.py --feature-type modules --feature-name "AutoTotem"

# Filter by minimum stars
python scripts/filter_addons.py --mc-version 1.21.11 --min-stars 50

# Sort by different criteria
python scripts/filter_addons.py --mc-version 1.21.11 --sort-by last_update

# Include archived repositories (normally excluded)
python scripts/filter_addons.py --mc-version 1.21.11 --include-archived
```

### Important Notes

1. **supported_versions field**: Some addons list multiple compatible versions in their custom.supported_versions field. The filter script checks both mc_version and supported_versions when filtering.

2. **None handling**: The addon database may contain null values for features lists or supported_versions. The filter script handles these gracefully.

3. **Default behavior**: Without --no-verified, the script only shows verified addons by default.

### Quality Filtering Rules

**Always follow these rules when searching references**:

1. **Skip archived addons** - Unless specifically porting legacy code
2. **Prefer verified addons** - Only use unverified if no verified examples exist
3. **Match versions** - Ensure addon's Meteor/Minecraft versions are compatible with your project
4. **Consider stars** - Higher star count often indicates better maintained code

### Cloning References

Clone addons for analysis (stores in `ai_reference/` or similar):

```bash
# Single addon
python scripts/clone_for_analysis.py https://github.com/owner/addon-name

# Multiple from filter results
python scripts/filter_addons.py --mc-version 1.21.1 --verified --limit 5 --json | \
    python scripts/clone_for_analysis.py --from-json

# Custom target directory
python scripts/clone_for_analysis.py https://github.com/owner/addon --target ./my_refs
```

**Best practice**: If an `ai_reference/` directory exists in workspace, use it for storing cloned repos and keep them there (don't cleanup automatically).

## Common Addon Structure

Meteor addons typically include:

- **Modules** (`extends Module`): Features that can be toggled on/off
- **Commands** (`extends Command`): Chat commands for addon functionality
- **HUD Elements** (`extends HudElement`): On-screen display components
- **Categories**: Organize modules in Meteor's GUI

## Checking for Breaking Changes

When updating to newer Minecraft/Meteor versions:

1. **Clone meteor-client** to workspace temporarily
2. **Check commit history**: Look for "breaking" or version bump commits
3. **Compare API surfaces**: Check if methods you use still exist
4. **Look at migration examples**: Find other addons that updated successfully

Example workflow:
```bash
cd /workspace
git clone --depth=1 https://github.com/MeteorDevelopment/meteor-client
cd meteor-client
git log --oneline --grep="breaking" -20
```

## Working with Legacy Versions

If working with older Minecraft/Meteor versions:

1. Use `--include-archived` flag when searching if truly necessary
2. Specify exact `--mc-version` when filtering
3. Check addon's `custom.supported_versions` field for compatibility
4. Be cautious - legacy code may use deprecated patterns

## Troubleshooting

### Template is Outdated

1. Clone meteor-client for current API reference
2. Use filter_addons.py to find recently updated verified addons
3. Compare their gradle files and dependencies
4. Update your project's files to match

### Can't Find Version-Compatible Examples

1. Check if the version exists in the database: `python scripts/filter_addons.py --mc-version X.XX.XX --no-verified`
2. Remove --verified flag temporarily (less ideal but may be necessary)
3. Sort by --sort-by last_update to find recently maintained addons
4. Check meteor-client source directly for official examples

### Need Specific Feature Implementation

1. Search by feature type: `python scripts/filter_addons.py --feature-type modules --feature-name YourFeature`
2. Look at multiple implementations for best practices
3. Clone top 3-5 verified addons for comparison

### Script Issues

If filter_addons.py encounters errors:
- Ensure you have internet connectivity (script fetches from GitHub)
- Check that Python 3 is installed and available
- The script handles None values gracefully, but very old addon entries may have unexpected data formats
- If a specific addon looks corrupted, use --limit to skip past it

## Best Practices

- Keep addon updated with latest Minecraft/Meteor versions
- Follow Meteor's code style and patterns
- Use verified addons as reference when possible
- Store cloned references in `ai_reference/` for easy access
- Check meteor-client source for authoritative API documentation
- Test with multiple Minecraft versions if supporting ranges
