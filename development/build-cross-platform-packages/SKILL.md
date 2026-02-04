---
name: build-cross-platform-packages
description: Use when building professional installers for desktop applications - covers macOS DMG with app bundles, Windows MSI with WiX, Linux DEB packages, GitHub Actions automation, and SLSA attestations
---

# Build Cross-Platform Packages

Build professional distributable packages for macOS, Windows, and Linux for Rust GUI applications.

**Quick reference for common tasks:**
- macOS DMG with app bundle and CLI tools included
- Windows MSI with Start Menu shortcuts and PATH configuration
- Linux DEB with desktop integration and dependency management
- Automated GitHub Actions workflows for all platforms
- SLSA attestations for supply chain security
- Homebrew formula auto-updates via repository_dispatch

## macOS DMG Package

**What this creates**: Professional drag-to-install DMG with app bundle containing both GUI and CLI binaries.

### Icon Requirements
- **Size**: 512x512 PNG minimum, transparent background recommended
- **Generate**: Use Ideogram (https://ideogram.ai) or AI generator for professional quality
- **Convert**: `convert icon.jpg -resize 512x512 icon.png` or native macOS: `sips -z 512 512 icon.png`
- **Convert to ICNS**: `mkdir AppIcon.iconset && sips -z 512 512 icon.png --out AppIcon.iconset/icon_512x512.png && iconutil -c icns AppIcon.iconset`
- **Place**: `docs/AppIcon.png` (referenced in Info.plist without extension)
- **Tip**: macOS automatically handles Retina @2x icons when using .icns format

### App Bundle Structure
```
YourApp.app/Contents/
├── Info.plist           # Application metadata
├── MacOS/
│   ├── your-gui-binary  # Main executable (launches GUI)
│   └── bin/
│       └── your-cli-binary  # CLI tool (accessed via PATH)
└── Resources/
    └── AppIcon.icns     # Application icon
```

**Why this structure?**
- GUI launches when app is double-clicked
- CLI accessible system-wide when app is in /Applications
- Single DMG distributes both tools

### Info.plist Template
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key><string>YourApp</string>
    <key>CFBundleDisplayName</key><string>Your App</string>
    <key>CFBundleIdentifier</key><string>com.yourcompany.yourapp</string>
    <key>CFBundleVersion</key><string>1.0.0</string>
    <key>CFBundleShortVersionString</key><string>1.0.0</string>
    <key>CFBundleExecutable</key><string>your-gui-binary</string>
    <key>CFBundleIconFile</key><string>AppIcon.icns</string>
    <key>CFBundlePackageType</key><string>APPL</string>
    <key>LSMinimumSystemVersion</key><string>10.13</string>
    <key>NSHighResolutionCapable</key><true/>
</dict>
</plist>
```

### Create DMG
```bash
# Create directory structure
mkdir -p dmg-temp/YourApp.app/Contents/{MacOS,Resources,MacOS/bin}

# Copy binaries
cp target/release/your-gui dmg-temp/YourApp.app/Contents/MacOS/
cp target/release/your-cli dmg-temp/YourApp.app/Contents/MacOS/bin/
chmod +x dmg-temp/YourApp.app/Contents/MacOS/*

# Copy metadata and resources
cp Info.plist dmg-temp/YourApp.app/Contents/
cp AppIcon.icns dmg-temp/YourApp.app/Contents/Resources/

# Create drag-to-install link
ln -s /Applications dmg-temp/Applications

# Build DMG (UDZO = compressed)
hdiutil create -volname "YourApp" -srcfolder dmg-temp -ov -format UDZO YourApp.dmg

# Cleanup
rm -rf dmg-temp
```

**Result**: Users drag YourApp.app to Applications, instantly getting both GUI and CLI.

### Advanced DMG with Custom Appearance

For professional DMGs with custom window layout and background:

```bash
# Create temporary read-write DMG
hdiutil create -volname "YourApp" -srcfolder dmg-temp -ov -format UDRW temp.dmg

# Mount it
device=$(hdiutil attach -readwrite -noverify -noautoopen "temp.dmg" | egrep '^/dev/' | sed 1q | awk '{print $1}')

# Customize appearance with AppleScript
echo '
  tell application "Finder"
    tell disk "YourApp"
      open
      set current view of container window to icon view
      set toolbar visible of container window to false
      set the bounds of container window to {100, 100, 700, 500}
      set position of item "YourApp.app" of container window to {150, 200}
      set position of item "Applications" of container window to {450, 200}
      delay 2
    end tell
  end tell
' | osascript

# Finalize (with race condition handling)
chmod -Rf go-w /Volumes/YourApp
sync

# IMPORTANT: Wait for Finder to release the volume
sleep 5

# Retry loop handles "Resource busy" race condition
for i in {1..5}; do
  if hdiutil detach ${device} 2>/dev/null; then
    break
  fi
  echo "Detach attempt $i failed, retrying..."
  sleep 2
done

# Force detach if still mounted
hdiutil detach ${device} -force || true

# Convert to compressed read-only DMG
hdiutil convert temp.dmg -format UDZO -imagekey zlib-level=9 -o YourApp.dmg
rm -f temp.dmg
```

**Why the retry logic?**
- macOS Finder may still be accessing the mounted DMG even after AppleScript completes
- This causes `hdiutil: couldn't eject "disk6" - Resource busy` errors
- The retry loop with delays solves this race condition
- Affects both Intel and Apple Silicon builds in GitHub Actions
- Without this fix, DMG creation randomly fails with exit code 16

**Result**: Users drag YourApp.app to Applications, instantly getting both GUI and CLI.

### DMG Creation Troubleshooting: "Resource Busy" Errors

**Problem**: DMG creation randomly fails in GitHub Actions with:
```
hdiutil: couldn't eject "disk2" - Resource busy
hdiutil: convert failed - Resource temporarily unavailable
Error: Process completed with exit code 1
```

**Root Cause**: Background processes (Spotlight indexing, mdworker, Finder) hold file handles on the mounted DMG volume even after AppleScript completes. This prevents `hdiutil detach` from succeeding, which blocks the final `hdiutil convert` step.

**Why It's Intermittent**: The race condition timing varies based on:
- System load during CI execution
- Spotlight indexing speed
- Number of files in the DMG
- macOS runner state

**Solution**: Multi-strategy unmount with progressive escalation (gentle → force):

```bash
# Create temporary read-write DMG
hdiutil create -volname "YourApp" -srcfolder dmg-temp -ov -format UDRW temp.dmg

# Mount it
device=$(hdiutil attach -readwrite -noverify -noautoopen "temp.dmg" | egrep '^/dev/' | sed 1q | awk '{print $1}')

# Customize appearance with AppleScript (your existing code here)
echo '...' | osascript

# Finalize DMG
chmod -Rf go-w /Volumes/YourApp
sync

# ROBUST UNMOUNT: Progressive escalation with verification
echo "Attempting to unmount ${device}..."

# Strategy 1: Try gentle unmount with retries
for i in {1..3}; do
  if hdiutil detach ${device} 2>/dev/null; then
    echo "Successfully detached on attempt $i"
    break
  fi
  echo "Detach attempt $i failed, waiting..."
  sleep 3
done

# Strategy 2: Check if still mounted and use diskutil
if diskutil info ${device} >/dev/null 2>&1; then
  echo "Device still mounted, using diskutil unmount force..."
  diskutil unmountDisk force ${device} || true
  sleep 2
fi

# Strategy 3: Final force detach
if diskutil info ${device} >/dev/null 2>&1; then
  echo "Device STILL mounted, using hdiutil detach -force..."
  hdiutil detach ${device} -force || true
  sleep 3
fi

# Verify device is unmounted
if diskutil info ${device} >/dev/null 2>&1; then
  echo "WARNING: Device may still be mounted, checking for blocking processes..."
  lsof | grep ${device} || true
fi

# Extra sync and wait for filesystem
sync
sleep 5

# Remove existing output DMG if it exists
rm -f YourApp.dmg

# Convert to compressed read-only DMG
echo "Converting temp.dmg to final DMG..."
hdiutil convert temp.dmg -format UDZO -imagekey zlib-level=9 -o YourApp.dmg

# Clean up temp files
rm -f temp.dmg
```

**Why This Works**:
1. **Progressive escalation**: Starts with gentle unmount, escalates to force only if needed
2. **Verification between steps**: Uses `diskutil info` to check mount status before each strategy
3. **Multiple tools**: Combines `hdiutil detach` and `diskutil unmountDisk` (different unmount mechanisms)
4. **Diagnostic output**: Shows `lsof` output if unmount fails to help debug persistent issues
5. **Multiple sync calls**: Ensures filesystem writes complete before attempting unmount
6. **Longer delays**: Gives background processes time to release file handles

**Implementation Location**: `.github/workflows/release.yml` in the "Create DMG installer (macOS only)" step, lines ~328-377.

**Applies To**: Both Intel (x86_64-apple-darwin) and Apple Silicon (aarch64-apple-darwin) DMG builds.

**Testing**: After implementing this fix, DMG creation should succeed consistently even under system load. Monitor with:
```bash
gh run watch
gh run list --workflow=release.yml --limit 5
```

**Historical Context**: This fix addresses random DMG creation failures due to the race condition.

## Windows Icon Embedding

**What this does**: Embeds your application icon directly in the .exe file so it appears in Task Manager, file explorer, and shortcuts. This happens at compile time via build.rs.

### Setup winres
```toml
# Cargo.toml - Only needed for Windows builds
[target.'cfg(windows)'.build-dependencies]
winres = "0.1"  # Embeds Windows resources (icon, version info)

[package]
include = ["src/**/*", "assets/**/*", "Cargo.toml", "build.rs"]  # Ensure assets included in package
```

### build.rs
```rust
fn main() {
    #[cfg(windows)]  // Only run on Windows builds
    {
        let mut res = winres::WindowsResource::new();
        res.set_icon("assets/app.ico");  // Path to multi-resolution ICO file
        res.set("ProductName", "YourApp");  // Shown in Task Manager
        res.set("FileDescription", "Description");  // Shown in file properties
        res.set("LegalCopyright", "Copyright (c) 2025");
        res.compile().expect("Failed to compile Windows resources");
    }
}
```

**Tip**: The build.rs runs during `cargo build`, embedding the icon into the compiled .exe before the MSI installer packages it.

### Create Multi-Resolution ICO
```bash
# ImageMagick converts PNG to ICO with multiple resolutions
# Windows automatically picks the right size for each context
magick convert app.png \
  \( -clone 0 -resize 256x256 \) \  # Large icons (file explorer)
  \( -clone 0 -resize 128x128 \) \  # Medium icons
  \( -clone 0 -resize 64x64 \) \    # Small icons
  \( -clone 0 -resize 48x48 \) \    # Taskbar
  \( -clone 0 -resize 32x32 \) \    # Title bar
  \( -clone 0 -resize 16x16 \) \    # System tray
  -delete 0 -colors 256 app.ico     # Reduce to 256 colors for compatibility
```

**Why multi-resolution?** Windows picks different icon sizes depending on context (taskbar, file explorer, system tray). Single-size ICOs look pixelated when scaled.

## Cargo Workspace Assets

**Why this issue occurs**: `cargo package` packages each workspace member independently, but `include_bytes!("../../assets/")` tries to reach outside the package directory during build. The packaged .crate file doesn't include parent directory assets.

### Problem: include_bytes!() with Workspace Assets
```rust
// Fails during cargo package because ../../ escapes the package boundary
let logo = include_bytes!("../../assets/logo.png");
```

**Error**: `couldn't read src/../../assets/logo.png`

### Solution: Copy to Package (Recommended)
```bash
# Copy assets into the package that needs them
cp assets/logo.png yourapp-gui/assets/
```

```rust
// Update code to use local path (within package)
let logo = include_bytes!("../assets/logo.png");  // ../assets relative to src/
```

```toml
# Cargo.toml - Tell cargo to include assets in the packaged .crate
include = ["src/**/*", "assets/**/*", "Cargo.toml", "build.rs"]
```

**Why this works**: Each package becomes self-contained with its own assets, allowing `cargo package` and `cargo publish` to succeed.

### Verify Before Publishing
```bash
# List files that will be included in the package
cargo package -p package-name --list | grep assets

# Inspect the actual .crate archive
tar -tzf target/package/package-name-*.crate | grep assets
```

**Expected output**: Should show `assets/logo.png` in the package contents.

## Windows MSI Installer

**What this creates**: Professional Windows installer that adds Start Menu shortcuts, configures PATH, and handles upgrades cleanly.

> **See also:** For bundling external dependencies (FFmpeg, ExifTool, Tesseract, etc.) in your MSI with unified detection/execution code paths, see the `robust-dependency-installation` skill.

### WiX v6 Setup
```powershell
dotnet tool install --global wix  # Microsoft's official installer framework
```

### Key WiX v6 Syntax Changes
| v3/v4 | v6 | Reason |
|-------|-----|--------|
| `<Directory Id="ProgramFilesFolder">` | `<StandardDirectory Id="ProgramFiles64Folder">` | Clearer 64-bit intent |
| `<Custom>NOT Installed</Custom>` | `<Custom Condition="NOT Installed" />` | Condition is an attribute now |

### MSI Template (yourapp.wxs)
```xml
<Wix xmlns="http://wixtoolset.org/schemas/v4/wxs">
  <!-- Package metadata -->
  <Package Name="YourApp" Version="1.0.0" Manufacturer="Your Company"
           UpgradeCode="GUID-HERE" Language="1033">  <!-- UpgradeCode: NEVER CHANGE! Used to detect previous installations -->
    <MajorUpgrade DowngradeErrorMessage="Newer version installed." />  <!-- Auto-uninstall old version -->
    <MediaTemplate EmbeddingCompressionLevel="high" />  <!-- Compress to reduce file size -->

    <!-- What to install -->
    <Feature Id="ProductFeature" Title="YourApp" Level="1">
      <ComponentGroupRef Id="ProductComponents" />
    </Feature>

    <!-- Where to install -->
    <StandardDirectory Id="ProgramFiles6432Folder">  <!-- C:\Program Files\ -->
      <Directory Id="INSTALLFOLDER" Name="YourApp">  <!-- C:\Program Files\YourApp\ -->
        <Component Id="MainExecutable" Bitness="always64">
          <File Id="GUI" Source="target\release\yourapp-gui.exe" KeyPath="yes">
            <Shortcut Id="StartMenu" Directory="ProgramMenuFolder" Name="YourApp" />  <!-- Start Menu shortcut -->
          </File>
          <File Id="CLI" Source="target\release\yourapp.exe" />  <!-- CLI tool -->
        </Component>
        <Component Id="PathEnvironment" Bitness="always64">
          <!-- Add install dir to system PATH so CLI is accessible from any terminal -->
          <Environment Id="PATH" Name="PATH" Value="[INSTALLFOLDER]"
                       Permanent="no" Part="last" Action="set" System="yes" />
        </Component>
      </Directory>
    </StandardDirectory>
  </Package>

  <!-- Component registry -->
  <Fragment>
    <ComponentGroup Id="ProductComponents" Directory="INSTALLFOLDER">
      <ComponentRef Id="MainExecutable" />
      <ComponentRef Id="PathEnvironment" />
    </ComponentGroup>
  </Fragment>
</Wix>
```

**Critical**: Generate UpgradeCode once and NEVER change it: `uuidgen` or https://www.uuidgenerator.net/

**Why UpgradeCode matters**: Windows uses it to detect existing installations. Changing it creates a separate product that won't upgrade the old one.

### Build MSI
```bash
wix build yourapp.wxs -o YourApp.msi
```

**Version handling**: Update `Version="1.0.0"` in .wxs for each release. MajorUpgrade handles uninstalling the old version automatically.

## Linux DEB Package

### Debian Directory
```
debian/
├── control          # Package metadata
├── rules            # Build script
├── changelog        # Version history
├── copyright        # License
├── compat           # Debian level (13)
├── yourapp.desktop  # Desktop entry
└── source/format    # "3.0 (quilt)"
```

### ⚠️ Common Mistake: Placeholder Emails
Replace `your@email.com` and `maintainer@example.com` in ALL files:
- `debian/control` - Maintainer
- `debian/copyright` - Upstream-Contact
- `debian/changelog` - All entries

```bash
# Find placeholders
grep -r "example.com" debian/

# Replace (adjust pattern)
sed -i 's/your@email.com/youractual@email.com/g' debian/{control,copyright,changelog}
```

**Best practice**: Match email in `Cargo.toml` authors.

### debian/control
```
Source: yourapp
Section: utils
Priority: optional
Maintainer: Your Name <your@email.com>
Build-Depends: debhelper-compat (= 13), cargo, rustc, pkg-config, libleptonica-dev, libtesseract-dev
Standards-Version: 4.6.0
Homepage: https://github.com/yourname/yourapp

Package: yourapp
Architecture: amd64
Depends: ${shlibs:Depends}, ${misc:Depends}, libimage-exiftool-perl, tesseract-ocr, ffmpeg
Description: Short description
 Long description.
```

### debian/rules
```makefile
#!/usr/bin/make -f
export DEB_BUILD_MAINT_OPTIONS = hardening=+all  # Enable security hardening (ASLR, stack protection, etc.)

%:
	dh $@  # Use debhelper to handle most packaging tasks

override_dh_auto_build:
	cargo build --release --workspace  # Build all workspace members

override_dh_auto_install:
	# Install binaries to /usr/bin with executable permissions
	install -D -m 755 target/release/yourapp-gui debian/yourapp/usr/bin/yourapp-gui
	install -D -m 755 target/release/yourapp debian/yourapp/usr/bin/yourapp

	# Install desktop entry for application menu integration
	install -D -m 644 debian/yourapp.desktop debian/yourapp/usr/share/applications/yourapp.desktop

	# Install icon to BOTH locations for maximum compatibility:
	# - /usr/share/pixmaps/ (legacy, used by older desktop environments)
	# - /usr/share/icons/hicolor/512x512/apps/ (freedesktop standard, preferred)
	install -D -m 644 yourapp-gui/assets/yourapp.png debian/yourapp/usr/share/pixmaps/yourapp.png
	install -D -m 644 yourapp-gui/assets/yourapp.png debian/yourapp/usr/share/icons/hicolor/512x512/apps/yourapp.png
```

**Icon paths**: Use package directory (`yourapp-gui/assets/`), not workspace root.

### debian/yourapp.desktop
```ini
[Desktop Entry]
Type=Application
Name=YourApp
Comment=Description
Exec=/usr/bin/yourapp-gui
Icon=yourapp
Terminal=false
Categories=Utility;
```

### debian/changelog
```
yourapp (1.0.0-1) unstable; urgency=medium

  * Initial release

 -- Your Name <your@email.com>  Mon, 01 Jan 2024 12:00:00 +0000
```

### Linux Build Dependencies (Rust + Tesseract/Leptonica)
```bash
sudo apt-get install -y pkg-config libleptonica-dev libtesseract-dev libclang-dev clang
```

**PKG_CONFIG_PATH Fix** (Ubuntu/Debian multiarch):
```bash
export PKG_CONFIG_PATH="/usr/lib/x86_64-linux-gnu/pkgconfig:$PKG_CONFIG_PATH"
cargo build --release
```

**GitHub Actions**:
```yaml
- run: sudo apt-get install -y pkg-config libleptonica-dev libtesseract-dev libclang-dev clang
- run: |
    export PKG_CONFIG_PATH="/usr/lib/x86_64-linux-gnu/pkgconfig:$PKG_CONFIG_PATH"
    cargo build --release
```

### Build DEB
```bash
dpkg-buildpackage -us -uc -b
lintian ../yourapp_1.0.0-1_amd64.deb
```

## GitHub Actions: Automated Release

**What this does**: Automatically builds installers for all platforms when you push a git tag, creates a GitHub release, and generates checksums + attestations.

### Auto-Trigger on Tag Push
```yaml
name: Release
on:
  push:
    tags: ['v*.*.*']  # Triggers when you push v1.0.0, v0.5.1, etc.
  workflow_dispatch:  # Manual trigger fallback if needed
    inputs:
      tag: {required: true, type: string}

jobs:
  create-release:
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.get_version.outputs.version }}  # Share version with build jobs
    steps:
      - uses: actions/checkout@v4
      - id: get_version
        run: |
          # Extract version from tag (v1.0.0 → 1.0.0)
          if [ "${{ github.event_name }}" = "push" ]; then
            echo "version=${GITHUB_REF#refs/tags/}" >> $GITHUB_OUTPUT
          else
            echo "version=${{ inputs.tag }}" >> $GITHUB_OUTPUT
          fi
      - run: gh release create ${{ steps.get_version.outputs.version }} --draft  # Create draft release
        env: {GH_TOKEN: ${{ github.token }}}

  build:
    needs: create-release  # Wait for release to be created
    strategy:
      matrix:  # Build all platforms in parallel
        include:
          - {os: macos-latest, target: x86_64-apple-darwin, archive: dmg}    # macOS Intel
          - {os: macos-latest, target: aarch64-apple-darwin, archive: dmg}   # macOS Apple Silicon
          - {os: windows-latest, target: x86_64-pc-windows-msvc, archive: msi}  # Windows
          - {os: ubuntu-latest, target: x86_64-unknown-linux-gnu, archive: deb}  # Linux
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
        with: {targets: ${{ matrix.target }}}

      # Platform-specific builds happen here (DMG, MSI, DEB creation)

      # Generate checksums with unique filenames to avoid artifact collisions
      - run: sha256sum * | tee checksums-${{ matrix.target }}.txt
      - uses: actions/upload-artifact@v4
        with:
          name: yourapp-${{ matrix.target }}  # Unique artifact name per platform
          path: |
            *.dmg
            *.msi
            ../*.deb
            checksums-*.txt
```

**Tip**: Use `matrix.target` in artifact names to prevent collisions when uploading from parallel jobs.

### SLSA Attestations
```yaml
# Add supply chain security attestations to prove build provenance
- uses: actions/attest-build-provenance@v1
  with: {subject-path: 'yourapp.${{ matrix.archive }}'}
```

**What this adds**: Cryptographic proof that the artifact was built by this repo's workflow. Users can verify authenticity:
```bash
gh attestation verify yourapp.dmg --owner yourname
```

**Shows**: Exact commit SHA, workflow run, and timestamp that built the artifact.

## Homebrew Auto-Update

### Cross-Repo Trigger (repository_dispatch)
**Step 1**: Target workflow (homebrew-yourapp)
```yaml
on:
  workflow_dispatch:
    inputs: {version: {required: true, type: string}}
  repository_dispatch:
    types: [update-formulae]

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - id: get-version
        run: |
          if [ "${{ github.event_name }}" = "repository_dispatch" ]; then
            echo "version=${{ github.event.client_payload.version }}" >> $GITHUB_OUTPUT
          else
            echo "version=${{ inputs.version }}" >> $GITHUB_OUTPUT
          fi
      - uses: actions/checkout@v4
      - run: gh release download "v${{ steps.get-version.outputs.version }}" --repo yourname/yourapp --pattern "checksums.txt"
        env: {GH_TOKEN: ${{ github.token }}}
      - id: checksums
        run: |
          echo "arm64_sha=$(grep aarch64-apple-darwin checksums.txt | awk '{print $1}')" >> $GITHUB_OUTPUT
          echo "x86_64_sha=$(grep x86_64-apple-darwin checksums.txt | awk '{print $1}')" >> $GITHUB_OUTPUT
      - run: |
          sed -i "s/version \".*\"/version \"${{ steps.get-version.outputs.version }}\"/" Formula/yourapp.rb
          # Update URLs and SHAs...
      - run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add Formula/ Casks/
          git commit -m "chore: update to v${{ steps.get-version.outputs.version }}"
          git push
```

**Step 2**: Send dispatch from main repo
```yaml
update-homebrew:
  needs: [create-release, build, checksums]
  runs-on: ubuntu-latest
  if: ${{ !contains(needs.create-release.outputs.version, '-') }}  # Skip pre-releases
  steps:
    - run: |
        VERSION=${{ needs.create-release.outputs.version }}
        curl -L -X POST \
          -H "Authorization: Bearer ${{ secrets.HOMEBREW_DISPATCH_TOKEN }}" \
          https://api.github.com/repos/yourname/homebrew-yourapp/dispatches \
          -d "{\"event_type\":\"update-formulae\",\"client_payload\":{\"version\":\"${VERSION#v}\"}}"
```

**⚠️ Important**: Use Personal Access Token (`HOMEBREW_DISPATCH_TOKEN`) with `repo` scope, not `GITHUB_TOKEN` (can't trigger cross-repo workflows).

## Complete Automation
Single command release:
```bash
cargo release patch --execute
```

**Automation chain**:
1. cargo-release → version bump, crates.io publish, tag push
2. Tag push → GitHub Actions (release creation, platform builds)
3. Builds complete → Checksums, SLSA attestations uploaded
4. repository_dispatch → Homebrew formula update

### ⚠️ cargo-release Tag Naming (Universal Limitation)

**Issue**: cargo-release tags workspace members as `package-v0.6.14` (not `v0.6.14`), which doesn't match standard `v*.*.*` GitHub Actions triggers.

**This is intentional cargo-release behavior** - it's designed to handle monorepos with independently versioned packages. For single-version workspaces, you must manually create the simple tag.

**Symptom**: After `cargo release patch --execute`, workflow doesn't trigger even though tags were pushed.

**Verification**:
```bash
git tag --sort=-version:refname | head -5
# Shows: yourapp-v0.6.14, yourapp-gui-v0.6.14 (wrong)
# Should show: v0.6.14 (correct)
```

**Workaround**: Manually create and push the simple `vX.Y.Z` tag:
```bash
# Create simple tag (disable GPG signing if needed)
GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0='tag.gpgSign' GIT_CONFIG_VALUE_0='false' \
  git tag -a v0.6.14 -m "Release v0.6.14 - Description here"

# Push the tag
git push origin v0.6.14 --no-verify

# Verify workflow triggered
gh run list --workflow=release.yml --limit 1
```

**Root cause**: cargo-release uses package names in tags for workspace members. The GitHub Actions workflow triggers on `v*.*.*` pattern which doesn't match `package-v*.*.*`.

**Alternative**: Configure `release.toml` to customize tag format (not yet tested).

**Checklist**:
- [ ] `on: push: tags: ['v*.*.*']` in release workflow
- [ ] Version extraction handles both `push` and `workflow_dispatch`
- [ ] Homebrew workflow listens for `repository_dispatch`
- [ ] Main workflow sends dispatch after successful build
- [ ] `release.toml` configured
- [ ] **After cargo-release, manually create `v*.*.*` tag**

**Monitor**:
```bash
gh run watch
gh run list --limit 5
```
