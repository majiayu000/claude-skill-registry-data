---
name: module-lifecycle
description: Manage complete module lifecycle - install, uninstall, reset, destroy
allowed-tools:
  - Bash
  - Read
  - Edit # For MODULES.md updates
  - Write # For backup metadata
preconditions:
  - Varies by mode (see mode-specific preconditions)
---

# module-lifecycle Skill

**Purpose:** Manage the complete lifecycle of VCV Rack modules from installation to removal with proper state tracking and safety features.

## Overview

This skill handles all module lifecycle operations:

- **Installation (Mode 1)**: Copy module to VCV Rack plugins directory (`~/Documents/Rack2/plugins-[platform]-[arch]/`)
- **Uninstallation (Mode 2)**: Clean removal from plugins directory (preserves source code)
- **Reset to Ideation (Mode 3)**: Remove implementation, keep idea/mockups (surgical rollback)
- **Destroy (Mode 4)**: Complete removal with backup (nuclear option)

All operations include proper platform detection, state tracking, and safety features (confirmations, backups).

## Mode Dispatcher

This skill operates in different modes based on the invoking command:

| Mode | Operation | Command | Purpose |
|------|-----------|---------|---------|
| 1 | Installation | `/install-module` | Deploy to VCV Rack plugins folder |
| 2 | Uninstallation | `/uninstall` | Remove plugin, keep source |
| 3 | Reset to Ideation | `/reset-to-ideation` | Remove implementation, keep idea/mockups |
| 4 | Destroy | `/destroy` | Complete removal with backup |
| Menu | Interactive | `/clean` | Present menu, user chooses mode |

**Pattern:** Commands are thin routers that invoke this skill with a specific mode. The skill dispatches to the appropriate reference file for detailed implementation.

**Why this matters:**

VCV Rack scans the plugins directory for modules. Installing to the correct location ensures your module appears in VCV Rack's module browser.

**Plugin directories by platform:**

- **macOS (arm64)**: `~/Documents/Rack2/plugins-mac-arm64/`
- **macOS (x64)**: `~/Documents/Rack2/plugins-mac-x64/`
- **Linux (x64)**: `~/Documents/Rack2/plugins-linux-x64/`
- **Windows (x64)**: `%USERPROFILE%\Documents\Rack2\plugins-win-x64\`

---

## Installation Workflow

The complete installation process:

1. **Platform Detection** - Determine current platform (mac-arm64, mac-x64, linux-x64, win-x64)
2. **Build Verification** - Check that dist/[Module]-[version]-[platform].vcvplugin exists, offer to build if missing
3. **Plugin Location Detection** - Find VCV Rack plugins directory
4. **Old Version Removal** - Remove existing installations to prevent conflicts
5. **Copy to Plugins Folder** - Install .vcvplugin to VCV Rack plugins directory
6. **Extraction** - Extract plugin archive (VCV Rack will extract on next launch, but we verify structure)
7. **Verification** - Confirm installation with file checks
8. **MODULES.md Update** - Record installation status and locations

See **[references/installation-process.md](references/installation-process.md)** for complete implementation.

### Platform Detection

**Detect current platform:**

```bash
# Determine platform
PLATFORM=$(uname -s)
ARCH=$(uname -m)

case "$PLATFORM" in
  Darwin)
    if [[ "$ARCH" == "arm64" ]]; then
      RACK_PLATFORM="mac-arm64"
    else
      RACK_PLATFORM="mac-x64"
    fi
    ;;
  Linux)
    RACK_PLATFORM="linux-x64"
    ;;
  MINGW*|MSYS*|CYGWIN*)
    RACK_PLATFORM="win-x64"
    ;;
  *)
    echo "Unknown platform: $PLATFORM"
    exit 1
    ;;
esac

echo "Detected platform: $RACK_PLATFORM"
```

### Plugin Location

**Standard VCV Rack plugin directories:**

```bash
# Platform-specific plugin directories
case "$RACK_PLATFORM" in
  mac-arm64|mac-x64)
    PLUGINS_DIR="$HOME/Documents/Rack2/plugins-$RACK_PLATFORM"
    ;;
  linux-x64)
    PLUGINS_DIR="$HOME/Documents/Rack2/plugins-$RACK_PLATFORM"
    ;;
  win-x64)
    PLUGINS_DIR="$USERPROFILE/Documents/Rack2/plugins-$RACK_PLATFORM"
    ;;
esac

# Verify directory exists
if [[ ! -d "$PLUGINS_DIR" ]]; then
  echo "VCV Rack plugins directory not found: $PLUGINS_DIR"
  echo "Is VCV Rack 2 installed?"
  exit 1
fi
```

### Build Verification

**Check for built plugin:**

```bash
# Extract version from plugin.json
VERSION=$(jq -r '.version' "modules/$MODULE_NAME/plugin.json")

# Expected plugin file
PLUGIN_FILE="modules/$MODULE_NAME/dist/$MODULE_NAME-$VERSION-$RACK_PLATFORM.vcvplugin"

if [[ ! -f "$PLUGIN_FILE" ]]; then
  echo "Plugin file not found: $PLUGIN_FILE"
  echo ""
  echo "Would you like to build it now?"
  echo "1. Yes, build and install"
  echo "2. No, exit"
  echo ""
  read -p "Choose (1-2): " choice

  if [[ "$choice" == "1" ]]; then
    # Invoke build-automation skill
    echo "Building module..."
    make -C "modules/$MODULE_NAME" dist

    # Check if build succeeded
    if [[ ! -f "$PLUGIN_FILE" ]]; then
      echo "Build failed. Check logs/[ModuleName]/build_*.log"
      exit 1
    fi
  else
    exit 0
  fi
fi
```

### Installation Steps

**1. Remove old versions:**

```bash
# Find existing installations
OLD_PLUGINS=$(find "$PLUGINS_DIR" -name "$MODULE_NAME-*.vcvplugin" -o -type d -name "$MODULE_NAME")

if [[ -n "$OLD_PLUGINS" ]]; then
  echo "Removing old versions..."
  echo "$OLD_PLUGINS" | while read -r old_plugin; do
    rm -rf "$old_plugin"
    echo "  Removed: $old_plugin"
  done
fi
```

**2. Copy plugin file:**

```bash
# Copy to plugins directory
cp "$PLUGIN_FILE" "$PLUGINS_DIR/"

echo "✓ Installed: $PLUGINS_DIR/$(basename $PLUGIN_FILE)"
```

**3. Verification:**

```bash
# Verify installation
INSTALLED_PLUGIN="$PLUGINS_DIR/$(basename $PLUGIN_FILE)"

if [[ -f "$INSTALLED_PLUGIN" ]]; then
  FILE_SIZE=$(ls -lh "$INSTALLED_PLUGIN" | awk '{print $5}')
  echo "✓ File present: $FILE_SIZE"

  # Check modification time (should be recent)
  MOD_TIME=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M:%S" "$INSTALLED_PLUGIN")
  echo "✓ Modified: $MOD_TIME"
else
  echo "✗ Installation verification failed"
  exit 1
fi
```

### Post-Installation

**No cache clearing needed:**

VCV Rack automatically detects new plugins on launch. No cache clearing is required unlike DAW plugins.

**Update MODULES.md:**

```markdown
**Status:** 📦 Installed
**Version:** [X.Y.Z]
**Last Updated:** [YYYY-MM-DD]
**Installation:**
- Platform: [mac-arm64 | mac-x64 | linux-x64 | win-x64]
- Location: ~/Documents/Rack2/plugins-[platform]/[ModuleName]-[version]-[platform].vcvplugin
```

---

## Uninstallation Workflow

Complete uninstallation process:

1. **Locate Plugin Files** - Find installed .vcvplugin files and extracted directories
2. **Confirm Removal** - Ask user to confirm deletion
3. **Remove Files** - Delete from plugins folder (source code preserved)
4. **Update MODULES.md** - Change status back to ✅ Working
5. **Confirmation** - Display uninstallation summary

See **[references/uninstallation-process.md](references/uninstallation-process.md)** for complete implementation.

### Uninstallation Steps

**1. Platform detection:**

```bash
# Detect platform (same as installation)
PLATFORM=$(uname -s)
ARCH=$(uname -m)
# ... (platform detection code)
```

**2. Find installed files:**

```bash
# Plugins directory
PLUGINS_DIR="$HOME/Documents/Rack2/plugins-$RACK_PLATFORM"

# Find all installations of this module
INSTALLED_FILES=$(find "$PLUGINS_DIR" -name "$MODULE_NAME-*.vcvplugin" -o -type d -name "$MODULE_NAME")

if [[ -z "$INSTALLED_FILES" ]]; then
  echo "Module not found in plugins directory"
  exit 0
fi

echo "Found installations:"
echo "$INSTALLED_FILES"
```

**3. Confirm removal:**

```bash
echo ""
echo "Remove these files?"
echo "1. Yes, uninstall"
echo "2. No, cancel"
echo ""
read -p "Choose (1-2): " choice

if [[ "$choice" != "1" ]]; then
  echo "Cancelled"
  exit 0
fi
```

**4. Remove files:**

```bash
echo "Uninstalling..."
echo "$INSTALLED_FILES" | while read -r file; do
  rm -rf "$file"
  echo "  Removed: $file"
done

echo "✓ Uninstallation complete"
```

**5. Update MODULES.md:**

Change status from 📦 Installed to ✅ Working:

```markdown
**Status:** ✅ Working
**Version:** [X.Y.Z]
**Last Updated:** [YYYY-MM-DD]
```

---

## Reset to Ideation Workflow (Mode 3)

Surgical rollback that removes implementation but preserves ideation artifacts:

**What gets preserved:**
- Creative brief (the original idea)
- UI mockups (all versions)
- Parameter specifications

**What gets removed:**
- Source code (src/ directory)
- Build configuration (Makefile)
- Implementation docs (architecture.md, plan.md)
- Build artifacts (dist/ directory)
- Installed plugins

**Use case:** Implementation went wrong, but the concept and panel design are solid. Start fresh from Stage 0.

See **[references/mode-3-reset.md](references/mode-3-reset.md)** for complete implementation.

### Reset Steps

**1. Verify module exists:**

```bash
if [[ ! -d "modules/$MODULE_NAME" ]]; then
  echo "Module not found: $MODULE_NAME"
  exit 1
fi
```

**2. Check status (block if in development):**

```bash
STATUS=$(grep -A 3 "^### $MODULE_NAME$" MODULES.md | grep "Status:" | awk '{print $2}')

if [[ "$STATUS" == "🚧" ]]; then
  echo "Cannot reset module that is still in development"
  echo "Complete or cancel the workflow first with /continue"
  exit 1
fi
```

**3. Create backup before reset:**

```bash
BACKUP_DIR="backups/$MODULE_NAME-reset-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp -r "modules/$MODULE_NAME" "$BACKUP_DIR/"
echo "✓ Backup created: $BACKUP_DIR"
```

**4. Preserve ideation artifacts:**

```bash
# Keep these directories/files
PRESERVE_FILES=(
  ".ideas/creative-brief.md"
  ".ideas/mockups/"
  ".ideas/parameter-spec.md"
  "res/*.svg"  # Panel designs
  "plugin.json"  # Basic module info
)

# Create temporary directory
TEMP_DIR=$(mktemp -d)
for file in "${PRESERVE_FILES[@]}"; do
  if [[ -e "modules/$MODULE_NAME/$file" ]]; then
    mkdir -p "$TEMP_DIR/$(dirname $file)"
    cp -r "modules/$MODULE_NAME/$file" "$TEMP_DIR/$file"
  fi
done
```

**5. Remove implementation:**

```bash
# Remove everything
rm -rf "modules/$MODULE_NAME"

# Restore preserved files
mkdir -p "modules/$MODULE_NAME"
cp -r "$TEMP_DIR/"* "modules/$MODULE_NAME/"
rm -rf "$TEMP_DIR"

echo "✓ Implementation removed, ideation artifacts preserved"
```

**6. Uninstall from VCV Rack:**

```bash
# Remove from plugins directory
PLUGINS_DIR="$HOME/Documents/Rack2/plugins-$RACK_PLATFORM"
find "$PLUGINS_DIR" -name "$MODULE_NAME-*" -exec rm -rf {} \;
```

**7. Update MODULES.md:**

```markdown
**Status:** 💡 Ideated
**Version:** -
**Last Updated:** [YYYY-MM-DD]
**Note:** Reset to ideation - implementation removed, concept preserved
```

---

## Destroy Workflow (Mode 4)

Complete removal with backup for abandoned modules:

**What gets removed:**
- Everything: source code, binaries, build artifacts, MODULES.md entry
- Optionally: troubleshooting docs mentioning the module

**Safety features:**
- Timestamped backup created before deletion
- Requires typing exact module name to confirm
- Blocks if status is 🚧 (protects in-progress work)

**Use case:** Abandoned experiment, complete failure, duplicate by mistake. Never using this module again.

See **[references/mode-4-destroy.md](references/mode-4-destroy.md)** for complete implementation.

### Destroy Steps

**1. Verify module exists:**

```bash
if [[ ! -d "modules/$MODULE_NAME" ]]; then
  echo "Module not found: $MODULE_NAME"
  exit 1
fi
```

**2. Check status (block if in development):**

```bash
STATUS=$(grep -A 3 "^### $MODULE_NAME$" MODULES.md | grep "Status:" | awk '{print $2}')

if [[ "$STATUS" == "🚧" ]]; then
  echo "Cannot destroy module that is still in development"
  echo "Complete or cancel the workflow first with /continue"
  exit 1
fi
```

**3. Confirmation (require exact name):**

```bash
echo "⚠️  WARNING: This will completely remove $MODULE_NAME"
echo ""
echo "This will delete:"
echo "- Source code (modules/$MODULE_NAME/)"
echo "- Installed plugin (if any)"
echo "- MODULES.md entry"
echo ""
echo "A timestamped backup will be created first."
echo ""
echo "To confirm, type the module name exactly: $MODULE_NAME"
read -p "> " confirmation

if [[ "$confirmation" != "$MODULE_NAME" ]]; then
  echo "Confirmation failed. Destruction cancelled."
  exit 0
fi
```

**4. Create timestamped backup:**

```bash
BACKUP_DIR="backups/$MODULE_NAME-destroyed-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp -r "modules/$MODULE_NAME" "$BACKUP_DIR/"
echo "✓ Backup created: $BACKUP_DIR"
```

**5. Remove everything:**

```bash
# Remove source
rm -rf "modules/$MODULE_NAME"
echo "✓ Removed source code"

# Remove from plugins directory
PLUGINS_DIR="$HOME/Documents/Rack2/plugins-$RACK_PLATFORM"
find "$PLUGINS_DIR" -name "$MODULE_NAME-*" -exec rm -rf {} \;
echo "✓ Removed installed plugin"

# Remove from MODULES.md
sed -i.bak "/^### $MODULE_NAME$/,/^### /{ /^### $MODULE_NAME$/d; /^### /!d; }" MODULES.md
echo "✓ Removed MODULES.md entry"
```

**6. Optional: Remove troubleshooting docs:**

```bash
echo ""
echo "Remove troubleshooting docs mentioning this module?"
echo "1. Yes, clean up docs"
echo "2. No, keep docs for reference"
echo ""
read -p "Choose (1-2): " choice

if [[ "$choice" == "1" ]]; then
  # Find and remove docs mentioning this module
  grep -rl "$MODULE_NAME" troubleshooting/ | while read -r doc; do
    rm "$doc"
    echo "  Removed: $doc"
  done
fi
```

**7. Final confirmation:**

```
✓ Module destroyed: [ModuleName]

Backup location: backups/[ModuleName]-destroyed-[timestamp]/

To restore from backup:
  cp -r backups/[ModuleName]-destroyed-[timestamp]/[ModuleName] modules/
  # Then rebuild: make -C modules/[ModuleName]
```

---

## Interactive Menu (Mode: Menu)

When invoked via `/clean [ModuleName]`, present interactive menu:

```
Module cleanup options for [ModuleName]:

1. Uninstall - Remove from VCV Rack plugins folder (keep source code)
2. Reset to ideation - Remove implementation, keep idea/mockups
3. Destroy - Complete removal with backup (IRREVERSIBLE except via backup)
4. Cancel

Choose (1-4): _
```

**Menu logic:**
- Read current module status from MODULES.md
- Show appropriate options based on status
- Route to selected mode
- Handle cancellation gracefully

---

## Error Handling

Common error scenarios with troubleshooting:

- **Build Files Not Found**: Guide to build module or check dist/ directory
- **VCV Rack Not Installed**: Check if ~/Documents/Rack2/ exists, suggest VCV Rack installation
- **Permission Denied**: Check file permissions, disk space
- **Module Doesn't Appear in VCV Rack**: Restart VCV Rack, check plugins directory, verify plugin.json

See **[references/error-handling.md](references/error-handling.md)** for all error scenarios and fixes.

---

## Decision Menu After Installation

After successful installation:

```
✓ [ModuleName] installed successfully

What's next?
1. Test in VCV Rack (recommended) → Launch VCV Rack and test module
2. Create another module → /dream
3. Document this module → Create user manual
4. Share module (export build) → Package for distribution
5. Other

Choose (1-5): _
```

**Handle responses:**

- **Option 1:** Provide VCV Rack testing guidance
- **Option 2:** Invoke `module-ideation` skill
- **Option 3:** Suggest creating user manual in `.ideas/`
- **Option 4:** Provide plugin distribution instructions
- **Option 5:** Ask what they'd like to do

---

## Integration Points

**Invoked by:**

- `/install-module [ModuleName]` → Mode 1 (Installation)
- `/uninstall [ModuleName]` → Mode 2 (Uninstallation)
- `/reset-to-ideation [ModuleName]` → Mode 3 (Reset)
- `/destroy [ModuleName]` → Mode 4 (Destroy)
- `/clean [ModuleName]` → Interactive menu
- `module-workflow` skill → After Stage 6 (offers installation)
- `module-improve` skill → After successful changes (offers reinstallation)
- Natural language: "Install [ModuleName]", "Remove [ModuleName]", "Clean up [ModuleName]"

**Invokes:**

- None (terminal skill, doesn't invoke others)

**Updates:**

- `MODULES.md` → Status changes to 📦 Installed, adds installation metadata

**Creates:**

- Plugin installations (non-git-tracked):
  - `~/Documents/Rack2/plugins-[platform]-[arch]/[ModuleName]-[version]-[platform].vcvplugin`

**Blocks:**

- None (installation is optional, modules can be tested without installing)

---

## Success Criteria

Installation is successful when:

- ✅ Plugin file copied to VCV Rack plugins directory
- ✅ File is correct format (.vcvplugin)
- ✅ Verification shows recent timestamp (< 60 seconds ago)
- ✅ File size is reasonable (> 1 KB typically)
- ✅ MODULES.md updated with 📦 status and installation location
- ✅ User knows next steps (restart VCV Rack to see module)

**NOT required for success:**

- Module appearing in VCV Rack immediately (requires restart)
- Multiple platform builds (single platform is fine for development)

---

## Notes for Claude

**When executing this skill:**

1. Always detect platform first - installation paths vary by platform
2. Check for built plugin in dist/ directory - offer to build if missing
3. Remove old versions before installing (prevents conflicts)
4. No cache clearing needed (VCV Rack auto-detects on launch)
5. Verification checks should be comprehensive (timestamp, size)
6. MODULES.md status update is part of success criteria
7. Provide clear next steps after installation

**Common pitfalls:**

- Forgetting platform detection (wrong plugins directory)
- Not removing old versions (VCV Rack may load wrong version)
- Not checking if VCV Rack is installed
- Missing MODULES.md update (state tracking incomplete)

## Platform-Specific Notes

### macOS (arm64 and x64)

- Plugins directory: `~/Documents/Rack2/plugins-mac-[arch]/`
- Plugin format: `.vcvplugin` (ZIP archive)
- VCV Rack auto-extracts on launch
- No code signing required for development

### Linux (x64)

- Plugins directory: `~/Documents/Rack2/plugins-linux-x64/`
- Plugin format: `.vcvplugin` (ZIP archive)
- VCV Rack auto-extracts on launch
- No special permissions needed

### Windows (x64)

- Plugins directory: `%USERPROFILE%\Documents\Rack2\plugins-win-x64\`
- Plugin format: `.vcvplugin` (ZIP archive)
- VCV Rack auto-extracts on launch
- May need to allow in Windows Defender

## VCV Rack Plugin Structure

**Plugin archive (.vcvplugin) contains:**

```
ModuleName/
├── plugin.json          # Module metadata
├── plugin.so/.dylib/.dll # Compiled module
└── res/                 # Resources
    └── *.svg            # Panel designs
```

**VCV Rack extracts on launch:**

When VCV Rack launches, it automatically extracts `.vcvplugin` archives to the same directory, creating a folder with the module contents. Both the archive and extracted folder coexist.
