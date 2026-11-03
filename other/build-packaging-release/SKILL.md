---
name: build-packaging-release
description: >
  Modify build scripts, packaging configuration, or CI/CD release workflows for
  open-bc with full support for Windows (MSI via WiX), Linux .deb (Ubuntu/Debian),
  Linux Flatpak, and Linux .rpm (Fedora/RHEL). Use this skill whenever a user
  asks to change the build pipeline, add a package format, update package metadata,
  version-bump a release, or add platform-specific CI steps.
---

# Build, Packaging & Release Skill for OpenBC

## Platform Support Matrix

OpenBC produces four artifact types across two platforms:

| Platform | Package | Tool chain | Runner |
|----------|---------|-----------|--------|
| Linux (Ubuntu/Debian) | `.deb` | `cmake --build` + CPack DEB | `ubuntu-24.04` |
| Linux (all) | `.flatpak` | `flatpak-builder` (KDE/Qt runtime) | `ubuntu-24.04` |
| Linux (Fedora/RHEL) | `.rpm` | `cmake --build` + CPack RPM | Fedora container on `ubuntu-24.04` |
| Windows | `.msi` | MSYS2 UCRT64 + WiX 3 | `windows-2022` |

**Every build or release change MUST be reviewed for all four targets.**

---

## Repository Build Layout

```
open-bc/
  scripts/
    build.sh              # Main orchestrator: -c (clean), -p (win|lin), -s (deb|rpm|flatpak)
    packaging/
      io.github.devopsnextgenx.open-bc.yml  # Flatpak manifest (KDE/Qt6 runtime)
  CMakeLists.txt          # Version, CPack, Qt/Rust integration
  Cargo.toml              # Workspace root
  Cargo.lock
  .github/
    workflows/
      release.yml         # GitHub Actions: linux (deb+flatpak), rpm, msi, release jobs
  xtask/                  # Rust build driver (cargo xtask)
```

---

## Version Bump Protocol

The version is declared ONCE in `CMakeLists.txt`:
```cmake
set(CPACK_PACKAGE_VERSION "1.0.3")
```

**ALWAYS update this first.** The release workflow validates that the pushed tag matches:
```bash
v="$(tr -d '\r' < CMakeLists.txt | sed -n 's/^set(CPACK_PACKAGE_VERSION "\(.*\)")/\1/p' | head -1)"
[ "v$v" = "${GITHUB_REF_NAME}" ] || { echo "tag mismatch"; exit 1; }
```

Steps for a version bump:
1. Update `set(CPACK_PACKAGE_VERSION "X.Y.Z")` in `CMakeLists.txt`
2. Verify `build.sh` does not hard-code the version anywhere (it should read from CMake)
3. Commit, then `git tag vX.Y.Z && git push origin vX.Y.Z`

---

## `scripts/build.sh` -- Key Flags

```bash
# Full Windows MSI build:
./scripts/build.sh -c -p win

# Linux .deb (clean build):
./scripts/build.sh -c -p lin -s deb

# Linux Flatpak (no clean -- reuses host build artifacts for speed):
./scripts/build.sh -p lin -s flatpak

# Linux .rpm:
./scripts/build.sh -c -p lin -s rpm
```

When modifying `build.sh`:
- **Windows path convention**: always use `/c/msys64/ucrt64/bin` -- NOT `C:\msys64`
  - MSYS2 Git Bash maps Windows drives: `C:` -> `/c`
  - This is hardcoded in `build.sh` and referenced in `CLAUDE.md`
- **Required env for Windows dev builds**:
  ```bash
  export PATH="/c/msys64/ucrt64/bin:/c/msys64/usr/bin:$PATH"
  export OPENSSL_DIR=/c/msys64/ucrt64
  ```
- **Flatpak build is sandboxed** -- it does NOT reuse the host's Rust build cache
- The `deb` step runs BEFORE `flatpak` in CI so the `.deb` artifact stays in `build/lin/packages/`

---

## GitHub Actions -- `release.yml` Structure

### Job: `linux` (ubuntu-24.04)
Builds `.deb` and `.flatpak`:
```yaml
- name: Free disk space
  run: sudo rm -rf /usr/share/dotnet /opt/ghc ...   # GH runners have limited space

- name: Install build + flatpak dependencies
  run: |
    sudo apt-get install -y \
      build-essential cmake ninja-build pkg-config perl \
      qt6-base-dev qt6-declarative-dev qt6-declarative-dev-tools qt6-multimedia-dev \
      libqt6opengl6-dev libgl1-mesa-dev \
      libssl-dev zlib1g-dev liblzma-dev \
      flatpak flatpak-builder appstream

- name: Allow user namespaces    # Required for flatpak-builder sandbox on Ubuntu 24.04
  run: sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0

- name: Build .deb
  run: ./scripts/build.sh -c -p lin -s deb

- name: Build Flatpak
  run: ./scripts/build.sh -p lin -s flatpak      # no -c: reuses host build
```

**When adding a new Linux dependency (apt package):**
- Add to the `apt-get install` list in the `linux` job
- Check if the package is also needed in the RPM job (Fedora package name will differ)

### Job: `rpm` (Fedora container on ubuntu-24.04)
```yaml
rpm:
  runs-on: ubuntu-24.04
  container: fedora:latest
  steps:
    - name: Install build dependencies
      run: |
        dnf install -y git gcc-c++ make cmake ninja-build rust cargo rpm-build which perl-core \
          qt6-qtbase-devel qt6-qtdeclarative-devel qt6-qtmultimedia-devel \
          mesa-libGL-devel libxkbcommon-devel \
          openssl-devel zlib-devel xz-devel
    - run: ./scripts/build.sh -c -p lin -s rpm
```

**Fedora package naming differences from Ubuntu:**
| Ubuntu | Fedora |
|--------|--------|
| `qt6-base-dev` | `qt6-qtbase-devel` |
| `qt6-multimedia-dev` | `qt6-qtmultimedia-devel` |
| `libssl-dev` | `openssl-devel` |
| `zlib1g-dev` | `zlib-devel` |
| `liblzma-dev` | `xz-devel` |
| `libgl1-mesa-dev` | `mesa-libGL-devel` |
| `pkg-config` | `pkgconf` |

### Job: `msi` (windows-2022, MSYS2)
```yaml
msi:
  runs-on: windows-2022
  steps:
    - uses: msys2/setup-msys2@v2
      with:
        msystem: UCRT64
        release: false    # reuse preinstalled C:\msys64
        update: true
        install: >-
          git make
          mingw-w64-ucrt-x86_64-toolchain
          mingw-w64-ucrt-x86_64-cmake
          mingw-w64-ucrt-x86_64-ninja
          mingw-w64-ucrt-x86_64-rust
          mingw-w64-ucrt-x86_64-qt6-base
          mingw-w64-ucrt-x86_64-qt6-declarative
          mingw-w64-ucrt-x86_64-qt6-tools
          mingw-w64-ucrt-x86_64-qt6-multimedia
          mingw-w64-ucrt-x86_64-openssl
          mingw-w64-ucrt-x86_64-zlib
          mingw-w64-ucrt-x86_64-xz
          mingw-w64-ucrt-x86_64-pkgconf

    - name: Install WiX 3.14 (at C:\msys64\opt\wix -- build.sh looks here)
      shell: pwsh
      run: |
        Invoke-WebRequest https://github.com/wixtoolset/wix3/releases/download/wix3141rtm/wix314-binaries.zip -OutFile wix.zip
        Expand-Archive wix.zip -DestinationPath C:\msys64\opt\wix

    - name: Build MSI
      shell: msys2 {0}
      run: |
        ./scripts/build.sh -c -p win
        v="$(tr -d '\r' < CMakeLists.txt | sed -n 's/^set(CPACK_PACKAGE_VERSION "\(.*\)")/\1/p' | head -1)"
        mv build/win/packages/openbc-installer.msi "build/win/packages/openbc-${v}-windows-x64.msi"
```

**When adding a new MSYS2 package:**
- All MSYS2 packages for UCRT64 are prefixed `mingw-w64-ucrt-x86_64-`
- Search at https://packages.msys2.org/ for the UCRT64 package name
- Add to the `install:` block in the `msys2/setup-msys2@v2` step

### Job: `release` (tags only)
```yaml
release:
  if: startsWith(github.ref, 'refs/tags/v')
  needs: [linux, rpm, msi]
  runs-on: ubuntu-24.04
  permissions:
    contents: write
  steps:
    - uses: actions/download-artifact@v4
      with:
        pattern: pkg-*
        path: dist
        merge-multiple: true
    - name: Checksums
      run: cd dist && sha256sum * > SHA256SUMS && cat SHA256SUMS
    - uses: softprops/action-gh-release@v2
      with:
        files: dist/*
        generate_release_notes: true
```

---

## CMakeLists.txt -- Key Packaging Sections

```cmake
# Version (single source of truth):
set(CPACK_PACKAGE_VERSION "X.Y.Z")

# CPack DEB config:
set(CPACK_DEBIAN_PACKAGE_MAINTAINER "...")
set(CPACK_DEBIAN_PACKAGE_DEPENDS "libqt6core6, libqt6multimedia6, ...")

# CPack RPM config:
set(CPACK_RPM_PACKAGE_REQUIRES "qt6-qtbase, qt6-qtmultimedia, ...")

# Desktop integration:
install(FILES resources/io.github.devopsnextgenx.open-bc.desktop DESTINATION share/applications)
install(FILES resources/io.github.devopsnextgenx.open-bc.metainfo.xml DESTINATION share/metainfo)
install(FILES resources/icons/io.github.devopsnextgenx.open-bc.png DESTINATION share/icons/hicolor/256x256/apps)
```

When adding a new runtime library dependency:
- Add to `CPACK_DEBIAN_PACKAGE_DEPENDS` for `.deb`
- Add to `CPACK_RPM_PACKAGE_REQUIRES` for `.rpm`
- Add to Flatpak manifest `finish-args` or `modules` if it is not in the KDE/Qt6 runtime

---

## Flatpak Manifest -- `scripts/packaging/io.github.devopsnextgenx.open-bc.yml`

Key conventions:
- Base runtime: `org.kde.Platform` + matching SDK (track the Qt6 version used)
- App ID must match: `io.github.devopsnextgenx.open-bc` (also must match `.desktop` file `StartupWMClass` and `QGuiApplication::setDesktopFileName`)
- `finish-args` must include display/audio/filesystem permissions for features used
- New native libraries should be added as `modules` entries; prefer shared-modules where possible

---

## Platform-Specific Code in the Codebase

All OS-specific C++ code must be guarded:
```cpp
#ifdef Q_OS_WIN
    // Windows-only: Media Foundation backend, console attachment, etc.
    qputenv("QT_MEDIA_BACKEND", "windows");
#endif
#ifdef Q_OS_LINUX
    // Linux-only code here
#endif
```

From `AGENTS.md` -- file path and user conventions:
```cpp
// CORRECT:
const QString username = qEnvironmentVariable("USER",
    qEnvironmentVariable("USERNAME", "unknown"));  // USERNAME on Windows
QString logPath = QDir::homePath() + "/.config/open-bc/...";

// WRONG:
const char* home = "/home/user";   // never hard-code
```

Console output (Windows GUI-subsystem binary):
```cpp
// Use printToConsole() for --help, --version, errors before Qt starts
// It attaches to the parent console on Windows (AttachConsole API)
printToConsole("message\n");    // NOT printf, NOT std::cout
```

---

## Checklist for Every Build/Packaging Change

### Always verify all four targets:

**Windows MSI:**
- [ ] MSYS2 UCRT64 package list updated if new native dependency added
- [ ] WiX `.wxs` file updated if new files/directories installed
- [ ] `build.sh` Windows path conventions preserved (`/c/msys64/...`)
- [ ] No POSIX-only shell syntax (test in Git Bash via MSYS2 shell)

**Linux .deb:**
- [ ] `CPACK_DEBIAN_PACKAGE_DEPENDS` updated for new runtime deps
- [ ] `apt-get install` list in `linux` job updated for new build-time deps
- [ ] Desktop/AppStream metadata up to date

**Linux .rpm:**
- [ ] `CPACK_RPM_PACKAGE_REQUIRES` updated for new runtime deps
- [ ] `dnf install` list in `rpm` job updated (Fedora package naming -- see table above)
- [ ] Fedora container version (`fedora:latest`) still provides needed Qt6 version

**Linux Flatpak:**
- [ ] New libraries added as Flatpak modules or available in the base runtime
- [ ] `finish-args` updated if new system permissions needed (audio, network, etc.)
- [ ] User namespace sandbox sysctl step still present in `linux` job
- [ ] `flatpak-builder` `--share` / `--socket` permissions documented

### General CI hygiene:
- [ ] `cargo check --workspace` passes on all platforms
- [ ] `release` job `needs:` list includes all build jobs
- [ ] Artifact upload names (`name: pkg-<format>`) match `download-artifact` pattern `pkg-*`
- [ ] `SHA256SUMS` still covers all produced files
- [ ] `generate_release_notes: true` preserved in `softprops/action-gh-release`
- [ ] Disk space `Free disk space` step still removes large unused toolchains on Linux runner
- [ ] `Allow user namespaces` sysctl step present on ubuntu-24.04 Flatpak job

---

## Adding a New Package Format

To add a new Linux package format (e.g. AppImage):

1. Add a new flag to `build.sh` (e.g. `-s appimage`)
2. Add a new step (or new job) in `.github/workflows/release.yml`
3. Upload artifact with a unique name (e.g. `name: pkg-appimage`)
4. Ensure the artifact name matches the `pattern: pkg-*` download in the `release` job
5. Add build dependencies to the appropriate job's install step
6. Document in this skill

---

## Common Mistakes to Avoid

| Mistake | Correct approach |
|---------|-----------------|
| Hard-coding version in `build.sh` | Read from `CMakeLists.txt` via `sed` (already done) |
| Using `apt` package names in the Fedora job | Use `dnf` + Fedora package names (see table) |
| Using Windows backslash paths in `build.sh` | MSYS2 shell uses POSIX paths (`/c/msys64/...`) |
| Adding a dep to Linux job but not RPM job | All three Linux targets need build+runtime deps checked |
| Forgetting `release: false` in msys2 action | Saves ~10 min; preinstalled toolchain is sufficient |
| Skipping disk space cleanup on Linux | GH ubuntu-24.04 runners may fail with out-of-space errors |
| Using `softprops/action-gh-release@v1` | Use `@v2` (v1 deprecated) |
| Forgetting to update `CPACK_*DEPENDS` in CMakeLists.txt | Package installs fine but runtime breaks on user machines |
| Adding a `release` job dependency without the job existing | Workflow fails at queue time |
