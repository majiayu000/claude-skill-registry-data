---
name: robust-dependency-installation
description: Use when implementing dependency installation systems - covers bundled portable executables in MSI installers, unified detection/execution code paths, and Windows installer best practices
---

# Robust Dependency Installation

> **See also:** For the full DMG/MSI/DEB packaging workflow, GitHub Actions release automation, and Homebrew updates, see the `build-cross-platform-packages` skill.

## When to Use This Skill

Use this skill when:
- Building Windows MSI installers that need to include external dependencies
- Implementing unified dependency detection and execution systems
- Working with portable executable distributions
- Users report dependencies not being found despite successful installation

## Core Principles

### 1. Bundled Dependencies Over External Package Managers

**Modern approach: Bundle portable executables directly in the installer.**

```
Traditional Approach (DEPRECATED):
Layer 1: Scoop/Chocolatey with DNS fallback
Layer 2: Alternative package manager
Layer 3: Public DNS retry
Layer 4: Manual instructions

Modern Approach (RECOMMENDED):
Layer 1: Bundled portable executables in MSI
  - No network required during installation
  - Specific tested versions
  - ~100% installation success rate
  - No dependency on external package managers
```

**Why bundled dependencies:**
- ✅ Works offline (no network required)
- ✅ Predictable versions (regression testing possible)
- ✅ Single infrastructure (your releases)
- ✅ No DNS/firewall/VPN issues
- ✅ Instant installation (no downloads)
- ✅ ~100% success rate

**Trade-offs:**
- ❌ Larger installer size (~50-200 MB)
- ❌ Must update bundled versions manually
- ❌ Legal compliance overhead (license tracking)

### 2. Bundled Dependency Architecture (Proven in Production)

**Complete workflow from download to MSI:**

```yaml
# GitHub Actions workflow
jobs:
  prepare-bundled-deps:
    runs-on: ubuntu-latest
    steps:
      - name: Download portable dependencies
        run: |
          # ExifTool (portable Perl)
          curl -L https://exiftool.org/exiftool-13.41_64.zip -o exiftool.zip

          # Tesseract (Windows installer, extract with 7z)
          curl -L https://github.com/UB-Mannheim/tesseract/.../tesseract.exe -o tesseract.exe

          # FFmpeg (static build)
          curl -L https://github.com/BtbN/FFmpeg-Builds/.../ffmpeg.zip -o ffmpeg.zip

          # ImageMagick (portable)
          curl -L https://github.com/ImageMagick/.../ImageMagick.7z -o imagemagick.7z

      - name: Extract and organize
        run: |
          mkdir -p deps/{exiftool,tesseract,ffmpeg,imagemagick}
          unzip exiftool.zip -d deps/exiftool/
          7z x tesseract.exe -o deps/tesseract/
          unzip ffmpeg.zip && cp bin/* deps/ffmpeg/
          7z x imagemagick.7z -o deps/imagemagick/

      - name: Create single ZIP
        run: |
          cd deps
          zip -r ../deps-windows.zip .

      - name: Upload as artifact (not release asset)
        uses: actions/upload-artifact@v4
        with:
          name: bundled-deps-windows
          path: deps-windows.zip
          retention-days: 7

  build-msi:
    needs: prepare-bundled-deps
    runs-on: windows-latest
    steps:
      - name: Download bundled deps artifact
        uses: actions/download-artifact@v4
        with:
          name: bundled-deps-windows
          path: .

      - name: Extract for WiX
        run: |
          Expand-Archive deps-windows.zip -Destination target/bundled-deps

      - name: Build MSI
        run: wix build installer/app.wxs
```

**Key points:**
- Deps uploaded as GitHub Actions artifact (7-day retention)
- NOT uploaded to release page (reduces user confusion)
- MSI downloads from workflow artifacts, not release assets
- All deps embedded in final MSI

### 3. WiX Installer Structure

**Directory structure in MSI:**

```xml
<Package Name="myapp" Version="1.0.0">
  <StandardDirectory Id="ProgramFiles64Folder">
    <Directory Id="INSTALLFOLDER" Name="myapp">
      <!-- Application binaries -->
      <Directory Id="DEPSFOLDER" Name="deps">
        <Directory Id="EXIFTOOLFOLDER" Name="exiftool" />
        <Directory Id="TESSERACTFOLDER" Name="tesseract" />
        <Directory Id="FFMPEGFOLDER" Name="ffmpeg" />
        <Directory Id="IMAGEMAGICKFOLDER" Name="imagemagick" />
      </Directory>
    </Directory>
  </StandardDirectory>

  <!-- ExifTool Component -->
  <DirectoryRef Id="EXIFTOOLFOLDER">
    <Component Id="ExifToolDep">
      <File Source="target\bundled-deps\exiftool\exiftool.exe" KeyPath="yes" />
      <Environment Id="PATH_EXIFTOOL"
                   Name="PATH"
                   Value="[EXIFTOOLFOLDER]"
                   Permanent="yes"
                   Part="last"
                   Action="set"
                   System="yes" />
    </Component>
  </DirectoryRef>

  <!-- Similar for Tesseract, FFmpeg, ImageMagick -->
</Package>
```

**Installation result:**
```
C:\Program Files\myapp\
├── myapp.exe
├── myapp-gui.exe
└── deps\
    ├── exiftool\exiftool.exe
    ├── tesseract\tesseract.exe
    ├── ffmpeg\ffmpeg.exe + ffprobe.exe
    └── imagemagick\magick.exe
```

**Each directory automatically added to system PATH during installation.**

### 4. Unified Dependency Detection and Execution

**THE CRITICAL RULE:** Detection and execution MUST use identical path resolution.

**Problem:** Split code paths cause "detected but won't execute" bugs.

```rust
// ❌ WRONG - Duplicate logic
fn is_tool_available() -> bool {
    Command::new("tool").output().is_ok()  // PATH only
}

fn use_tool() {
    Command::new("tool")...  // Different code path!
}
```

**Solution:** Single source of truth for path resolution.

```rust
#[derive(Debug, Clone, PartialEq)]
pub enum Dependency {
    ExifTool,
    Tesseract,
    FFmpeg,
    ImageMagick,
}

impl Dependency {
    pub fn name(&self) -> &str {
        match self {
            Dependency::ExifTool => "exiftool",
            Dependency::Tesseract => "tesseract",
            Dependency::FFmpeg => "ffmpeg",
            Dependency::ImageMagick => "imagemagick",
        }
    }

    /// Directory name where MSI installs the tool
    fn bundled_dir_name(&self) -> &str {
        match self {
            Dependency::ExifTool => "exiftool",
            Dependency::Tesseract => "tesseract",
            Dependency::FFmpeg => "ffmpeg",
            Dependency::ImageMagick => "imagemagick",
        }
    }

    /// Actual executable name (may differ from directory name)
    fn exe_name(&self) -> &str {
        match self {
            Dependency::ExifTool => "exiftool",
            Dependency::Tesseract => "tesseract",
            Dependency::FFmpeg => "ffmpeg",
            Dependency::ImageMagick => "magick",  // ImageMagick v7+ uses magick.exe
        }
    }

    /// Find executable path - checks bundled location FIRST
    pub fn find_executable(&self) -> Option<PathBuf> {
        #[cfg(windows)]
        {
            // Priority 1: Bundled MSI location
            if let Ok(programfiles) = std::env::var("PROGRAMFILES") {
                let bundled_dir = PathBuf::from(&programfiles)
                    .join("myapp")
                    .join("deps")
                    .join(self.bundled_dir_name());

                let exe_path = bundled_dir.join(format!("{}.exe", self.exe_name()));
                if exe_path.exists() {
                    return Some(exe_path);
                }
            }
        }

        // Priority 2: System PATH
        if which::which(self.exe_name()).is_ok() {
            return Some(PathBuf::from(self.exe_name()));
        }

        // Priority 3: Fallback names (e.g., "convert" for ImageMagick)
        for name in self.fallback_names() {
            if which::which(name).is_ok() {
                return Some(PathBuf::from(name));
            }
        }

        None
    }

    /// Create Command - ALWAYS uses find_executable()
    pub fn create_command(&self) -> Option<Command> {
        self.find_executable().map(Command::new)
    }

    /// Check availability - uses create_command()
    pub fn is_available(&self) -> bool {
        if let Some(mut cmd) = self.create_command() {
            let result = match self {
                Dependency::ExifTool => cmd.arg("-ver").output(),
                Dependency::Tesseract => cmd.arg("--version").output(),
                Dependency::FFmpeg => cmd.arg("-version").output(),
                Dependency::ImageMagick => cmd.arg("-version").output(),
            };
            result.map(|o| o.status.success()).unwrap_or(false)
        } else {
            false
        }
    }

    fn fallback_names(&self) -> &[&str] {
        match self {
            Dependency::ImageMagick => &["magick", "convert"],
            _ => &[],
        }
    }
}
```

**Usage in application code:**

```rust
// ✅ CORRECT - Unified code path
fn run_ocr(image_path: &Path) -> Result<String> {
    let mut cmd = Dependency::Tesseract
        .create_command()
        .context("Tesseract not available")?;

    let output = cmd
        .arg(image_path)
        .arg("stdout")
        .output()?;

    Ok(String::from_utf8(output.stdout)?)
}
```

**Critical details:**
1. Bundled location checked FIRST (highest priority)
2. Detection (`is_available()`) uses same code as execution (`create_command()`)
3. Handles case where directory name ≠ executable name (imagemagick/magick.exe)
4. Works even if PATH not yet updated (MSI-spawned processes)

### 5. GUI PATH Setup for Bundled Dependencies

**Problem:** GUI launched from MSI inherits old environment before PATH refresh.

**Solution:** Prepend bundled directories to PATH at application startup.

```rust
// In main.rs - call before any dependency usage
fn setup_path() {
    use std::env;

    let current_path = env::var("PATH").unwrap_or_default();

    let mut additional_paths: Vec<String> = if cfg!(windows) {
        let mut paths = Vec::new();

        // Bundled MSI installer dependencies (HIGHEST PRIORITY)
        if let Ok(programfiles) = env::var("PROGRAMFILES") {
            paths.push(format!("{}\\myapp\\deps\\exiftool", programfiles));
            paths.push(format!("{}\\myapp\\deps\\tesseract", programfiles));
            paths.push(format!("{}\\myapp\\deps\\ffmpeg", programfiles));
            paths.push(format!("{}\\myapp\\deps\\imagemagick", programfiles));
        }

        paths
    } else {
        vec![]
    };

    // Build new PATH
    if cfg!(windows) {
        let new_path = if additional_paths.is_empty() {
            current_path
        } else {
            format!("{};{}", additional_paths.join(";"), current_path)
        };
        env::set_var("PATH", new_path);
    }
}

fn main() {
    setup_path();  // Call FIRST
    // Rest of application logic...
}
```

**Why this works:**
- Runs at application startup before any dependency checks
- Doesn't rely on system PATH being updated
- Works for MSI-spawned processes with stale environment
- Bundled locations have highest priority

## Legal Compliance for Bundled Dependencies

**When bundling portable executables, you MUST comply with licenses:**

### License Verification Checklist

- [ ] Verify all licenses allow redistribution:
  - GPL: ✅ Allowed with source code availability
  - LGPL: ✅ Allowed with source/link
  - Apache 2.0: ✅ Allowed with attribution
  - MIT: ✅ Allowed with attribution
  - Proprietary: ❌ Check terms carefully

- [ ] Create `/LICENSES/` directory with license texts
- [ ] Create `/third_party/<dep>/NOTICE` attribution files
- [ ] For LGPL (FFmpeg): Include source link or code
- [ ] Update README.md with third-party attributions
- [ ] Create `.gitignore` in `/deps/` (never commit binaries to git)

**REUSE spec structure:**
```
project/
├── LICENSES/
│   ├── GPL-3.0-or-later.txt
│   ├── Apache-2.0.txt
│   └── MIT.txt
├── third_party/
│   ├── exiftool/
│   │   └── NOTICE
│   ├── tesseract/
│   │   └── NOTICE
│   └── ffmpeg/
│       └── NOTICE (include source link for LGPL)
└── README.md (attribution section)
```

**Example NOTICE file:**
```
ExifTool by Phil Harvey
License: GPL-1.0-or-later OR Artistic-2.0
Homepage: https://exiftool.org
Bundled version: 13.41

Copyright (c) 2003-2024 Phil Harvey
```

## Implementation Checklist

### Bundled Dependency Setup
- [ ] Create GitHub Actions workflow to download portable executables
- [ ] Organize deps into directory structure (one folder per tool)
- [ ] Create single ZIP artifact (not release asset)
- [ ] Add download-artifact step in MSI build job
- [ ] Extract to `target/bundled-deps/` before WiX build

### WiX Installer Configuration
- [ ] Define directory structure with DEPSFOLDER
- [ ] Create Component for each dependency with File elements
- [ ] Add Environment PATH entries for each directory
- [ ] Set Permanent="yes" for PATH changes
- [ ] Include all Components in Feature

### Application Code
- [ ] Create Dependency enum with all external tools
- [ ] Implement bundled_dir_name() and exe_name() methods
- [ ] Implement find_executable() checking bundled location first
- [ ] Add create_command() and is_available() using find_executable()
- [ ] Replace ALL Command::new("tool") with Dependency::Tool.create_command()
- [ ] Add setup_path() function in main.rs (GUI applications)

### Legal Compliance
- [ ] Verify all dependency licenses allow redistribution
- [ ] Create LICENSES/ directory with license texts
- [ ] Create third_party/ notices
- [ ] Update README with attributions
- [ ] Add .gitignore for deps/ directory

### Testing
- [ ] Test MSI installation on clean Windows VM
- [ ] Verify dependencies installed to Program Files\myapp\deps\
- [ ] Verify system PATH updated with dependency directories
- [ ] Test GUI launched from MSI (before PATH refresh)
- [ ] Test CLI from terminal (after PATH refresh)
- [ ] Verify all dependencies detected as available
- [ ] Test actual execution (not just detection)

## Dependency-Specific Notes

### ExifTool
- **Format:** Portable Perl executable (single .exe)
- **Source:** https://exiftool.org/exiftool-{version}_64.zip
- **License:** GPL-1.0-or-later OR Artistic-2.0
- **Installation:** Extract .exe to deps/exiftool/

### Tesseract OCR
- **Format:** Windows installer (.exe), extract with 7z
- **Source:** https://github.com/UB-Mannheim/tesseract/releases
- **License:** Apache-2.0
- **Installation:** `7z x tesseract-setup.exe -o deps/tesseract/`
- **Note:** Include tessdata/ directory for OCR languages

### FFmpeg
- **Format:** Static build ZIP
- **Source:** https://github.com/BtbN/FFmpeg-Builds/releases
- **License:** LGPL-2.1 (must include source link or code)
- **Installation:** Extract bin/ffmpeg.exe and bin/ffprobe.exe
- **Version pinning:** Use specific release tags (e.g., `autobuild-2024-11-04-12-55`)

### ImageMagick
- **Format:** Portable 7z archive
- **Source:** https://github.com/ImageMagick/ImageMagick/releases
- **License:** Apache-2.0
- **Installation:** Extract all .exe and .dll files
- **Note:** v7+ uses magick.exe (not imagemagick.exe)

## Anti-Patterns to Avoid

### ❌ Uploading Deps to GitHub Release Page

```yaml
# WRONG - Visible to end users, causes confusion
- name: Upload to release
  uses: softprops/action-gh-release@v2
  with:
    files: deps-windows.zip
```

**Problem:** Users think they need to download both MSI and ZIP.

**Solution:** Use GitHub Actions artifacts instead.

### ❌ Split Detection and Execution Logic

```rust
// WRONG - Duplicate logic
fn is_tool_available() -> bool {
    Command::new("tool").output().is_ok()
}

fn use_tool() {
    Command::new("tool")...  // Different path!
}
```

**Problem:** Detection succeeds but execution fails.

**Solution:** Both use Dependency::Tool methods.

### ❌ Checking PATH Only

```rust
// WRONG - Fails for MSI-spawned processes
pub fn find_executable(&self) -> Option<PathBuf> {
    which::which(self.name()).ok()
}
```

**Problem:** MSI-spawned GUI has stale PATH.

**Solution:** Check bundled location FIRST, then PATH.

### ❌ Directory Name = Executable Name Assumption

```rust
// WRONG - Assumes directory matches executable
let path = bundled_dir.join(format!("{}.exe", self.name()));
```

**Problem:** ImageMagick installed to `imagemagick/` but executable is `magick.exe`.

**Solution:** Separate bundled_dir_name() and exe_name().

## Real-World Results

**From production deployment (bundled dependency architecture):**

✅ **Installation success rate: ~100%** (up from ~90% with Scoop/Chocolatey)
- No network failures
- No DNS resolution issues
- No firewall/VPN interference
- Works in air-gapped environments

✅ **Instant dependency availability**
- No download time during installation
- Predictable performance

✅ **Version control**
- ExifTool 13.41, Tesseract 5.5.0, FFmpeg 7.1, ImageMagick 7.1.2-8
- Regression testing possible
- No "works on my machine" version mismatches

✅ **Detection reliability**
- GUI detects dependencies immediately when launched from MSI
- Works before PATH environment refresh
- Unified code path prevents detection/execution split

**Common issue resolved:** GUI showing "dependencies missing" despite successful MSI installation.

**Root cause:** MSI-spawned GUI inherited old environment without updated PATH.

**Solution:** Bundled location checked first, GUI setup_path() prepends at startup.

## Summary

Modern dependency installation uses **bundled portable executables** embedded in MSI installers.

**Key principles:**
1. Bundle portable executables in MSI (no external package managers)
2. Check bundled location FIRST in path resolution
3. Unified detection and execution code paths
4. GUI prepends bundled directories at startup
5. Legal compliance with license attribution
6. GitHub Actions artifact (not release asset)

**Directory structure:**
```
C:\Program Files\myapp\deps\
├── exiftool\exiftool.exe
├── tesseract\tesseract.exe (+ tessdata/)
├── ffmpeg\ffmpeg.exe + ffprobe.exe
└── imagemagick\magick.exe (+ DLLs)
```

**Detection priority:**
1. Bundled MSI location (`C:\Program Files\myapp\deps\`)
2. System PATH
3. Fallback names (magick vs convert)

**Result:** ~100% installation success, instant availability, version control, no network dependency.
