---
name: dev-swarm-flutter-installation
description: Install and configure Flutter SDK. Use when setting up a Flutter development environment.
---

# Flutter SDK Installation and Setup

This skill assists in installing and configuring the Flutter SDK for cross-platform mobile, web, and desktop development.

## When to Use This Skill

- User needs to set up Flutter development environment
- User wants to install or update Flutter SDK
- User asks to configure Flutter for their platform

## Prerequisites

**macOS:**
- Xcode command-line tools
- `curl` and `unzip`

**Linux:**
- `curl`, `git`, `unzip`, `xz-utils`, `zip`, `libglu1-mesa`

**Windows:**
- Git for Windows
- PowerShell

## Your Roles in This Skill

- **DevOps Engineer**: Install and configure Flutter SDK. Detect operating system and download the appropriate Flutter version. Extract and set up Flutter in the recommended location. Configure PATH environment variables. Verify installation and run flutter doctor. Update project documentation to reflect environment setup.

## Role Communication

As an expert in your assigned roles, you must announce your actions before performing them using the following format:

As a {Role} [and {Role}, ...], I will {action description}

This communication pattern ensures transparency and allows for human-in-the-loop oversight at key decision points.
## Instructions

### 1. Check Existing Installation

Before installing, check if Flutter is already installed.

```bash
flutter --version
```

If installed, display the current version and ask the user for confirmation before reinstalling or updating.

### 2. Detect Operating System

Determine the user's platform:

```bash
# macOS/Linux
uname -s
uname -m

# Windows (PowerShell)
$env:OS
[System.Environment]::Is64BitOperatingSystem
```

### 3. Install Prerequisites

**macOS:**
```bash
xcode-select --install
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt-get update -y && sudo apt-get upgrade -y
sudo apt-get install -y curl git unzip xz-utils zip libglu1-mesa
```

**Windows:**
Ensure Git for Windows is installed. If not, guide user to download from: https://git-scm.com/download/win

### 4. Download Flutter SDK

**Important:** The Flutter SDK download URLs follow this pattern:
- macOS (Intel): `https://storage.googleapis.com/flutter_infra_release/releases/stable/macos/flutter_macos_<version>-stable.zip`
- macOS (Apple Silicon): `https://storage.googleapis.com/flutter_infra_release/releases/stable/macos/flutter_macos_arm64_<version>-stable.zip`
- Linux: `https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_<version>-stable.tar.xz`
- Windows: `https://storage.googleapis.com/flutter_infra_release/releases/stable/windows/flutter_windows_<version>-stable.zip`

To get the latest stable version, check: https://docs.flutter.dev/release/archive

For simplicity, use the latest download links:

**macOS (Intel):**
```bash
cd ~/Downloads
curl -O https://storage.googleapis.com/flutter_infra_release/releases/stable/macos/flutter_macos-stable.zip
```

**macOS (Apple Silicon/ARM64):**
```bash
cd ~/Downloads
curl -O https://storage.googleapis.com/flutter_infra_release/releases/stable/macos/flutter_macos_arm64-stable.zip
```

**Linux:**
```bash
cd ~/Downloads
curl -O https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux-stable.tar.xz
```

**Windows (PowerShell):**
```powershell
cd $env:USERPROFILE\Downloads
Invoke-WebRequest -Uri "https://storage.googleapis.com/flutter_infra_release/releases/stable/windows/flutter_windows-stable.zip" -OutFile "flutter_windows-stable.zip"
```

### 5. Extract Flutter SDK

**macOS:**
```bash
# Create recommended directory
mkdir -p ~/develop

# Extract (adjust filename based on architecture)
unzip ~/Downloads/flutter_macos-stable.zip -d ~/develop/
# OR for Apple Silicon:
# unzip ~/Downloads/flutter_macos_arm64-stable.zip -d ~/develop/
```

**Linux:**
```bash
# Create recommended directory
mkdir -p ~/develop

# Extract
tar -xf ~/Downloads/flutter_linux-stable.tar.xz -C ~/develop/
```

**Windows (PowerShell):**
```powershell
# Create recommended directory (avoid paths with spaces/special characters)
New-Item -Path "$env:USERPROFILE\develop" -ItemType Directory -Force

# Extract
Expand-Archive -Path "$env:USERPROFILE\Downloads\flutter_windows-stable.zip" -Destination "$env:USERPROFILE\develop\"
```

### 6. Configure PATH Environment Variable

**macOS (Zsh - default shell):**
```bash
# Add to ~/.zprofile
echo 'export PATH="$HOME/develop/flutter/bin:$PATH"' >> ~/.zprofile

# Apply changes (or restart terminal)
source ~/.zprofile
```

**Linux (Bash):**
```bash
# Add to ~/.bash_profile
echo 'export PATH="$HOME/develop/flutter/bin:$PATH"' >> ~/.bash_profile

# Apply changes (or restart terminal)
source ~/.bash_profile
```

**Linux (Zsh):**
```bash
# Add to ~/.zshenv
echo 'export PATH="$HOME/develop/flutter/bin:$PATH"' >> ~/.zshenv

# Apply changes (or restart terminal)
source ~/.zshenv
```

**Linux (Fish):**
```bash
# Add to PATH
fish_add_path -g -p ~/develop/flutter/bin
```

**Windows (PowerShell as Administrator):**
```powershell
# Get current user PATH
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")

# Add Flutter to PATH
$flutterPath = "$env:USERPROFILE\develop\flutter\bin"
if ($currentPath -notlike "*$flutterPath*") {
    [Environment]::SetEnvironmentVariable(
        "Path",
        "$flutterPath;$currentPath",
        "User"
    )
    Write-Host "Flutter added to PATH. Please restart your terminal."
}
```

**Alternative for Windows (Manual):**
1. Press Windows + Pause (or right-click This PC → Properties)
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Under "User variables", find and select "Path"
5. Click "Edit"
6. Click "New"
7. Add: `%USERPROFILE%\develop\flutter\bin`
8. Click OK three times
9. Restart terminal/IDE

### 7. Verify Installation

After configuring PATH, close and reopen all terminal windows and IDEs, then verify:

```bash
flutter --version
dart --version
```

### 8. Run Flutter Doctor

Flutter includes a diagnostic tool to check your environment:

```bash
flutter doctor
```

This command checks for:
- Flutter SDK installation
- Required dependencies
- Connected devices
- IDE plugins

Follow any recommendations from `flutter doctor` to complete the setup.

### 9. Save User Preferences

After successful installation, save the Flutter setup information to `dev-swarm/user_preferences.md` for future reference.

**Example:**

Create or update `dev-swarm/user_preferences.md` with:

```markdown
## Flutter Development
- **Flutter SDK**: Installed and configured (version X.X.X)
- **Dart**: Included with Flutter SDK
- **Installation path**: ~/develop/flutter
```

## Troubleshooting

**Command not found after installation:**
- Ensure PATH was properly configured
- Restart all terminal windows and IDEs
- Verify the Flutter binary exists at the expected path:
  - macOS/Linux: `~/develop/flutter/bin/flutter`
  - Windows: `%USERPROFILE%\develop\flutter\bin\flutter.bat`

**Permission errors (macOS/Linux):**
```bash
# Ensure proper permissions
chmod -R u+w ~/develop/flutter
```

**Windows PATH issues:**
- Ensure no spaces or special characters in installation path
- Run PowerShell as Administrator when modifying system variables
- Move Flutter PATH entry to the top of the list in Environment Variables

## Next Steps

After installation, users typically need to:
1. Install platform-specific tooling (Xcode for iOS, Android Studio for Android)
2. Set up an editor/IDE with Flutter plugins (VS Code, Android Studio, IntelliJ)
3. Create a new Flutter project: `flutter create my_app`
4. Run the app: `cd my_app && flutter run`
