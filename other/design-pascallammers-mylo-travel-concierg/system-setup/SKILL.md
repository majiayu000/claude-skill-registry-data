---
name: system-setup
description: Validate and configure all dependencies required for VCV Rack Module Freedom System
allowed-tools:
  - Bash # For dependency checks and installation
  - Read # For checking existing config
  - Write # For creating system-config.json
  - Edit # For updating config
preconditions:
  - None - this is the entry point for new users
---

# system-setup Skill

**Purpose:** Validate and configure all dependencies required for VCV Rack module development in the VCV Rack Module Freedom System.

## Overview

This skill ensures new users can get started without friction by:
- Detecting the current platform (macOS, Linux, Windows)
- Checking for required dependencies (Python, build tools, Make, VCV Rack SDK)
- Offering automated installation where possible
- Guiding manual installation when automation isn't available
- Validating that all tools are functional
- Saving validated configuration for build scripts

**Target platforms:** macOS (arm64/x64), Linux (x64), Windows (x64)

**User experience:** Interactive, with clear choices between automated and guided setup

---

## Required Dependencies

### Python 3.8+
- **Purpose:** Build scripts and helper utilities
- **Check:** `python3 --version`
- **Minimum version:** 3.8
- **Auto-install (macOS):** Homebrew (`brew install python3`) or download from python.org
- **Auto-install (Linux):** apt/yum (`sudo apt install python3`)
- **Auto-install (Windows):** Download from python.org

### Build Tools
- **macOS:** Xcode Command Line Tools
  - **Check:** `xcode-select -p`
  - **Auto-install:** `xcode-select --install`
- **Linux:** GCC/Clang, build-essential
  - **Check:** `gcc --version`
  - **Auto-install:** `sudo apt install build-essential` (Debian/Ubuntu)
- **Windows:** MinGW-w64 or Visual Studio Build Tools
  - **Check:** `gcc --version` or `cl.exe`
  - **Auto-install:** Download MinGW-w64 from mingw-w64.org

### Make
- **Purpose:** Build system for VCV Rack modules
- **Check:** `make --version`
- **Minimum version:** 3.81+
- **Auto-install (macOS):** Included with Xcode CLI Tools
- **Auto-install (Linux):** `sudo apt install make`
- **Auto-install (Windows):** Included with MinGW or `choco install make`

### VCV Rack SDK 2.0+
- **Purpose:** Module development framework
- **Check:** Search standard locations, validate version in `include/rack.hpp`
- **Standard locations:**
  - `~/Rack-SDK`
  - `/usr/local/Rack-SDK`
  - `C:\Rack-SDK` (Windows)
- **Auto-install:** Download from VCV Rack website or GitHub releases

### Git (Optional but recommended)
- **Purpose:** Version control
- **Check:** `git --version`
- **Auto-install (macOS):** Included with Xcode CLI Tools
- **Auto-install (Linux):** `sudo apt install git`
- **Auto-install (Windows):** Download from git-scm.com

---

## Skill Entry Point

When invoked via `/setup` command:

**Check for test mode first:**
- If user provided `--test=SCENARIO` argument, set TEST_MODE variable
- Pass test mode to all system-check.sh invocations via `--test=$SCENARIO`
- Show test mode banner if active:
  ```
  [TEST MODE: $SCENARIO]
  Using mock data - no actual system changes will be made
  ```

1. **Welcome message:**
   ```
   System Setup - VCV Rack Module Freedom System

   This will validate and configure all dependencies needed for VCV Rack module development.

   How would you like to proceed?
   1. Automated setup (install missing dependencies automatically)
   2. Guided setup (step-by-step instructions for manual installation)
   3. Check only (detect what's installed, no changes)
   4. Exit

   Choose (1-4): _
   ```

2. **Store user choice and proceed to platform detection**

---

## Platform Detection

**Step 1: Detect platform**

```bash
# Detect platform and architecture
PLATFORM=$(uname -s)
ARCH=$(uname -m)

case "$PLATFORM" in
  Darwin)
    PLATFORM_NAME="macOS"
    if [[ "$ARCH" == "arm64" ]]; then
      PLATFORM_FULL="mac-arm64"
    else
      PLATFORM_FULL="mac-x64"
    fi
    ;;
  Linux)
    PLATFORM_NAME="Linux"
    PLATFORM_FULL="linux-x64"
    ;;
  MINGW*|MSYS*|CYGWIN*)
    PLATFORM_NAME="Windows"
    PLATFORM_FULL="win-x64"
    ;;
  *)
    echo "Unknown platform: $PLATFORM"
    exit 1
    ;;
esac

# Get OS version
case "$PLATFORM_NAME" in
  macOS)
    OS_VERSION=$(sw_vers -productVersion)
    ;;
  Linux)
    OS_VERSION=$(lsb_release -rs 2>/dev/null || cat /etc/os-release | grep VERSION_ID | cut -d'"' -f2)
    ;;
  Windows)
    OS_VERSION=$(cmd.exe /c ver | grep -oP '\d+\.\d+\.\d+')
    ;;
esac

echo "Detected: $PLATFORM_NAME $OS_VERSION ($PLATFORM_FULL)"
```

**Step 2: Confirm with user**

```
Detected platform: macOS 14.0 (mac-arm64)

Is this correct?
1. Yes, continue
2. No, let me specify

Choose (1-2): _
```

---

## Dependency Validation Workflow

For each dependency (in order):

1. **Check if already installed and functional**
2. **If found:**
   - Display version and path
   - Validate it meets minimum requirements
   - Save to config
   - Continue to next dependency
3. **If not found:**
   - **Automated mode:** Offer to install automatically
   - **Guided mode:** Show manual installation instructions
   - **Check-only mode:** Report as missing, continue

### 1. Python Validation

**Check command:**
```bash
# Check for python3
if command -v python3 >/dev/null 2>&1; then
  PYTHON_PATH=$(which python3)
  PYTHON_VERSION=$(python3 --version | awk '{print $2}')
  PYTHON_FOUND=true

  # Check minimum version (3.8)
  PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
  PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

  if [[ $PYTHON_MAJOR -ge 3 && $PYTHON_MINOR -ge 8 ]]; then
    PYTHON_MEETS_MIN=true
  else
    PYTHON_MEETS_MIN=false
  fi
else
  PYTHON_FOUND=false
fi
```

**If found and valid:**
```
✓ Python 3.11.5 found at /usr/local/bin/python3
```

**If not found (automated mode):**
```
✗ Python 3.8+ not found

Would you like me to install Python 3 via [package manager]?
1. Yes, install automatically
2. No, show me manual instructions
3. Skip Python (not recommended)

Choose (1-3): _
```

**If user chooses automated install (macOS):**
```bash
# Check if Homebrew is installed first
if ! command -v brew >/dev/null 2>&1; then
  echo "Installing Homebrew..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install Python
brew install python3

# Verify installation
python3 --version
```

**If user chooses automated install (Linux):**
```bash
# Debian/Ubuntu
sudo apt update
sudo apt install -y python3 python3-pip

# Verify installation
python3 --version
```

**If user chooses manual instructions:**
Display content from platform-specific installation guide.

### 2. Build Tools Validation

**macOS:**
```bash
# Check for Xcode Command Line Tools
if xcode-select -p >/dev/null 2>&1; then
  XCODE_PATH=$(xcode-select -p)
  XCODE_VERSION=$(pkgutil --pkg-info=com.apple.pkg.CLTools_Executables | grep version | awk '{print $2}')
  XCODE_FOUND=true
else
  XCODE_FOUND=false
fi
```

**If found:**
```
✓ Xcode Command Line Tools found (version 15.0)
```

**If not found (automated mode):**
```
✗ Xcode Command Line Tools not found

These are required for compiling C++ code on macOS.

Would you like me to install them?
1. Yes, install automatically
2. No, show me manual instructions
3. Skip (build will fail)

Choose (1-3): _
```

**Automated install:**
```bash
xcode-select --install
# Wait for installation dialog
echo "⏳ Please complete the Xcode Command Line Tools installation dialog."
echo "Press Enter when installation is complete..."
read
```

**Linux:**
```bash
# Check for GCC
if command -v gcc >/dev/null 2>&1; then
  GCC_PATH=$(which gcc)
  GCC_VERSION=$(gcc --version | head -n1 | awk '{print $NF}')
  GCC_FOUND=true
else
  GCC_FOUND=false
fi
```

**Automated install (Linux):**
```bash
# Debian/Ubuntu
sudo apt install -y build-essential

# Verify
gcc --version
```

**Windows:**
```bash
# Check for MinGW gcc
if command -v gcc >/dev/null 2>&1; then
  GCC_PATH=$(which gcc)
  GCC_VERSION=$(gcc --version | head -n1 | awk '{print $NF}')
  GCC_FOUND=true
else
  GCC_FOUND=false
fi
```

### 3. Make Validation

**Check command:**
```bash
if command -v make >/dev/null 2>&1; then
  MAKE_PATH=$(which make)
  MAKE_VERSION=$(make --version | head -n1 | awk '{print $NF}')
  MAKE_FOUND=true

  # Check minimum version (3.81)
  MAKE_MAJOR=$(echo $MAKE_VERSION | cut -d. -f1)
  MAKE_MINOR=$(echo $MAKE_VERSION | cut -d. -f2)

  if [[ $MAKE_MAJOR -ge 3 && $MAKE_MINOR -ge 81 ]]; then
    MAKE_MEETS_MIN=true
  else
    MAKE_MEETS_MIN=false
  fi
else
  MAKE_FOUND=false
fi
```

**If found and valid:**
```
✓ Make 4.3 found at /usr/bin/make
```

**If not found (automated mode):**
```
✗ Make not found

Make is required for building VCV Rack modules.

Would you like me to install Make?
1. Yes, install automatically (included with build tools)
2. No, show manual instructions
3. Skip (build will fail)

Choose (1-3): _
```

**Note:** Make is typically included with build tools (Xcode CLI Tools on macOS, build-essential on Linux).

### 4. VCV Rack SDK Validation

**This is the most important check for VCV Rack development.**

**Step 1: Search standard locations**
```bash
# Standard SDK locations by platform
SDK_SEARCH_PATHS=(
  "$HOME/Rack-SDK"
  "/usr/local/Rack-SDK"
  "$HOME/Documents/Rack-SDK"
)

# Windows additional paths
if [[ "$PLATFORM_NAME" == "Windows" ]]; then
  SDK_SEARCH_PATHS+=("C:/Rack-SDK")
fi

# Search for SDK
RACK_SDK_FOUND=false
for path in "${SDK_SEARCH_PATHS[@]}"; do
  if [[ -f "$path/include/rack.hpp" ]]; then
    RACK_DIR="$path"
    RACK_SDK_FOUND=true

    # Extract version from rack.hpp
    RACK_VERSION=$(grep "RACK_VERSION" "$path/include/rack.hpp" | head -n1 | awk '{print $3}' | tr -d '"')
    break
  fi
done
```

**If found in standard location:**
```
✓ VCV Rack SDK 2.5.2 found at ~/Rack-SDK
```

**If not found, ask about custom location:**
```
✗ VCV Rack SDK not found in standard locations

Searched:
- ~/Rack-SDK
- /usr/local/Rack-SDK
- ~/Documents/Rack-SDK

VCV Rack SDK is required for module development.

Do you have VCV Rack SDK 2.0+ installed in a custom location?
1. Yes, let me provide the path
2. No, install it for me (automated mode only)
3. No, show me how to install it manually

Choose (1-3): _
```

**If user provides custom path:**
```
Enter the full path to your VCV Rack SDK:
(e.g., /Users/username/Development/Rack-SDK)

Path: _
```

Validate the provided path:
```bash
# Check for rack.hpp
if [[ -f "$USER_PROVIDED_PATH/include/rack.hpp" ]]; then
  RACK_DIR="$USER_PROVIDED_PATH"
  RACK_VERSION=$(grep "RACK_VERSION" "$USER_PROVIDED_PATH/include/rack.hpp" | head -n1 | awk '{print $3}' | tr -d '"')
  echo "✓ VCV Rack SDK $RACK_VERSION found at $RACK_DIR"
else
  echo "✗ Invalid VCV Rack SDK at provided path"
  echo "Expected: $USER_PROVIDED_PATH/include/rack.hpp"
fi
```

**Automated VCV Rack SDK installation:**
```
Installing VCV Rack SDK to ~/Rack-SDK...

⏳ Downloading VCV Rack SDK from vcvrack.com...
```

```bash
# Determine platform-specific SDK download
case "$PLATFORM_FULL" in
  mac-arm64)
    SDK_URL="https://vcvrack.com/downloads/Rack-SDK-2.5.2-mac-arm64.zip"
    ;;
  mac-x64)
    SDK_URL="https://vcvrack.com/downloads/Rack-SDK-2.5.2-mac-x64.zip"
    ;;
  linux-x64)
    SDK_URL="https://vcvrack.com/downloads/Rack-SDK-2.5.2-lin-x64.zip"
    ;;
  win-x64)
    SDK_URL="https://vcvrack.com/downloads/Rack-SDK-2.5.2-win-x64.zip"
    ;;
esac

# Download and extract
cd ~
curl -L -o Rack-SDK.zip "$SDK_URL"
unzip -q Rack-SDK.zip
mv Rack-SDK-* Rack-SDK
rm Rack-SDK.zip

# Verify
if [[ -f ~/Rack-SDK/include/rack.hpp ]]; then
  echo "✓ VCV Rack SDK installed successfully"
  RACK_DIR="$HOME/Rack-SDK"
else
  echo "✗ Installation failed"
  exit 1
fi
```

**If download fails:**
Fall back to manual instructions with direct link to VCV Rack website.

### 5. Git Validation (Optional)

**Check command:**
```bash
if command -v git >/dev/null 2>&1; then
  GIT_PATH=$(which git)
  GIT_VERSION=$(git --version | awk '{print $3}')
  GIT_FOUND=true
else
  GIT_FOUND=false
fi
```

**If found:**
```
✓ Git 2.42.0 found at /usr/bin/git
```

**If not found:**
```
⚠ Git not found (optional but recommended)

Git is used for version control. It's highly recommended for tracking changes.

Would you like to install it?
1. Yes, install automatically
2. No, skip (can install later)

Choose (1-2): _
```

---

## Configuration Persistence

After all dependencies are validated, create `.claude/system-config.json`:

```bash
# Generate config file
cat > .claude/system-config.json <<EOF
{
  "platform": "$PLATFORM_FULL",
  "platform_name": "$PLATFORM_NAME",
  "platform_version": "$OS_VERSION",
  "arch": "$ARCH",
  "python_path": "$PYTHON_PATH",
  "python_version": "$PYTHON_VERSION",
  "build_tools": {
    "xcode_path": "$XCODE_PATH",
    "xcode_version": "$XCODE_VERSION",
    "gcc_path": "$GCC_PATH",
    "gcc_version": "$GCC_VERSION"
  },
  "make_path": "$MAKE_PATH",
  "make_version": "$MAKE_VERSION",
  "rack_dir": "$RACK_DIR",
  "rack_version": "$RACK_VERSION",
  "git_path": "$GIT_PATH",
  "git_version": "$GIT_VERSION",
  "validated_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
```

**Add to .gitignore if not already present:**
```bash
grep -q "system-config.json" .gitignore || echo ".claude/system-config.json" >> .gitignore
```

**Set RACK_DIR environment variable:**

```bash
# Add to shell profile
case "$SHELL" in
  */zsh)
    PROFILE="$HOME/.zshrc"
    ;;
  */bash)
    PROFILE="$HOME/.bashrc"
    ;;
  *)
    PROFILE="$HOME/.profile"
    ;;
esac

# Add RACK_DIR export if not already present
if ! grep -q "RACK_DIR" "$PROFILE"; then
  echo "" >> "$PROFILE"
  echo "# VCV Rack SDK path" >> "$PROFILE"
  echo "export RACK_DIR=\"$RACK_DIR\"" >> "$PROFILE"
  echo "✓ Added RACK_DIR to $PROFILE"
  echo ""
  echo "⚠ Please restart your terminal or run: source $PROFILE"
fi
```

---

## System Report

After configuration is saved, display comprehensive summary:

```
✓ System Setup Complete

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Platform: macOS 14.0 (mac-arm64)

Dependencies validated:
✓ Python 3.11.5 (/usr/local/bin/python3)
✓ Xcode Command Line Tools 15.0
✓ Make 4.3 (/usr/bin/make)
✓ VCV Rack SDK 2.5.2 (~/Rack-SDK)
✓ Git 2.42.0 (/usr/bin/git)

Environment:
✓ RACK_DIR set to ~/Rack-SDK
  (Added to ~/.zshrc - restart terminal to activate)

Configuration saved to:
.claude/system-config.json

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

What's next?
1. Create your first module (/dream)
2. View available commands (type /? or press Tab)
3. Read the documentation (@README.md)
4. Run system check again (/setup)
5. Exit

Choose (1-5): _
```

**Handle user choice:**
- Choice 1: Invoke module-ideation skill (same as `/dream`)
- Choice 2: Show command list via `ls .claude/commands/`
- Choice 3: Display README.md
- Choice 4: Re-run system-setup skill
- Choice 5: Exit with message

---

## Error Handling

### Automated Installation Failures

If any automated installation fails:

1. **Capture error output**
2. **Display error message**
3. **Fall back to guided mode**

Example:
```
✗ Failed to install Make via package manager

Error: Package manager not found.

Falling back to manual instructions...

[Display manual Make installation steps]

Press Enter to continue with manual installation...
```

### Missing Critical Dependencies

If critical dependencies are missing and user skips them:

```
⚠ Warning: Critical dependencies are missing

The following required dependencies were not installed:
- Make (required for building)
- VCV Rack SDK 2.0+ (required for module development)

You will not be able to build modules until these are installed.

Would you like to:
1. Go back and install missing dependencies
2. Save current configuration anyway (not recommended)
3. Exit without saving

Choose (1-3): _
```

### Version Too Old

If a dependency is found but version is too old:

```
✗ Make 3.79 found, but version 3.81+ is required

Would you like to:
1. Update Make via package manager (automated)
2. Show manual update instructions
3. Continue anyway (build may fail)

Choose (1-3): _
```

### Permission Errors

If installation fails due to permissions:

```
✗ Failed to write to /usr/local: Permission denied

This usually means you need sudo access.

Would you like to:
1. Retry with sudo (will prompt for password)
2. Install to ~/local instead (no sudo required)
3. Show manual instructions

Choose (1-3): _
```

### RACK_DIR Not Set After Setup

If user's shell doesn't source profile automatically:

```
⚠ RACK_DIR environment variable not detected

The variable was added to your shell profile, but your current terminal
session doesn't have it yet.

To activate RACK_DIR:
1. Restart your terminal
2. Or run: source ~/.zshrc

To verify: echo $RACK_DIR
Should output: ~/Rack-SDK
```

---

## Checkpoint Protocol Integration

This skill follows the checkpoint protocol:

**After each major validation step:**
1. Display what was found/installed
2. Present numbered decision menu
3. Wait for user response
4. Execute chosen action

**Major checkpoint moments:**
- After platform detection
- After each dependency validation
- After configuration is saved
- At final system report

**Always use inline numbered menus, never AskUserQuestion tool.**

---

## Integration Points

**Invoked by:**
- `/setup` command (primary entry point)
- New user onboarding
- When build scripts detect missing dependencies (RACK_DIR not set)

**Reads:**
- `.claude/system-config.json` (if exists, to show current config)

**Creates:**
- `.claude/system-config.json` (validated dependency paths)
- Adds RACK_DIR to shell profile (~/.zshrc, ~/.bashrc, etc.)

**May invoke:**
- `module-ideation` skill (if user chooses to create module after setup)

---

## Success Criteria

Setup is successful when:

- All required dependencies are detected or installed
- All versions meet minimum requirements
- All tools are validated as functional (not just present)
- RACK_DIR environment variable is set and points to valid SDK
- Configuration is saved to `.claude/system-config.json`
- User receives clear system report
- Decision menus presented at appropriate points
- Errors are handled gracefully with fallback options

---

## Notes for Claude

**CRITICAL REQUIREMENTS:**

1. **ALWAYS check before installing** - Never install if dependency already exists
2. **ALWAYS validate versions** - Don't assume found dependency meets minimum
3. **ALWAYS test functionality** - Run version check to ensure executable works
4. **ALWAYS get confirmation** - Present menu before any automated installation
5. **ALWAYS provide fallback** - If automation fails, offer manual instructions
6. **ALWAYS set RACK_DIR** - This is critical for VCV Rack builds

**Automated vs Guided Mode:**

- **Automated mode:** Attempt installation with confirmation, fall back to guided if fails
- **Guided mode:** Show manual instructions immediately, no automation
- **Check-only mode:** Report what's found, make no changes

**Path handling:**

- Convert all paths to absolute paths
- Validate paths exist before saving to config
- Expand `~` to actual home directory path
- Check that RACK_DIR contains expected files (include/rack.hpp)

**VCV Rack-specific notes:**

- RACK_DIR is the single most important configuration
- SDK must match platform (mac-arm64, mac-x64, linux-x64, win-x64)
- SDK version 2.0+ required (check rack.hpp)
- Must add RACK_DIR to shell profile for persistence

**Common pitfalls to AVOID:**

- Installing without checking if already present
- Not validating versions meet minimums
- Proceeding when critical dependencies missing
- Using relative paths in configuration
- Not testing if executables actually run
- Auto-proceeding without user confirmation
- Using AskUserQuestion instead of inline menus
- Forgetting to set RACK_DIR environment variable
- Not checking if shell profile sources correctly
