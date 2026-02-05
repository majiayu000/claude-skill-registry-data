---
name: critical-bug-detector
description: Automatically performs critical pre-release checks when building installers, creating releases, or packaging VoiceLite. Prevents missing files, version mismatches, and configuration errors that have caused release failures.
---

# Critical Bug Detector

This skill prevents the disasters that happened in v1.0.95-96 where critical files were missing from releases.

## When This Skill Activates

- Building an installer or preparing a release
- Modifying installer configuration files (.iss)
- Working on packaging or distribution
- After significant changes to project structure

## Critical Checks Performed

### 1. Whisper Model Verification ⚠️ CRITICAL

**Check ggml-tiny.bin (FREE tier model - MUST be in installer)**
```bash
# File exists and correct size
test -f "VoiceLite/whisper/ggml-tiny.bin" || FAIL "Missing ggml-tiny.bin!"
size=$(stat -c%s "VoiceLite/whisper/ggml-tiny.bin" 2>/dev/null)
[ "$size" -eq 44048314 ] || WARN "ggml-tiny.bin size incorrect (expected 42MB)"

# Not ignored by git (v1.0.96 bug)
git check-ignore VoiceLite/whisper/ggml-tiny.bin && FAIL "Model ignored by git!"

# Included in installer script
grep -q "ggml-tiny.bin" VoiceLite/Installer/VoiceLiteSetup.iss || FAIL "Model not in installer!"
```

**Check whisper.exe**
```bash
# Executable present
test -f "VoiceLite/whisper/whisper.exe" || FAIL "Missing whisper.exe!"

# Verify size (whisper.cpp v1.7.6)
expected_size=480256
actual_size=$(stat -c%s "VoiceLite/whisper/whisper.exe" 2>/dev/null)
[ "$actual_size" -eq "$expected_size" ] || WARN "whisper.exe size mismatch (expected 469KB, got $(($actual_size / 1024))KB)"

# Verify SHA256 (v1.7.6)
expected_hash="b7c6dc2e999a80bc2d23cd4c76701211f392ae55d5cabdf0d45eb2ca4faf09af"
actual_hash=$(sha256sum VoiceLite/whisper/whisper.exe | cut -d' ' -f1)
[ "$actual_hash" = "$expected_hash" ] || WARN "whisper.exe hash mismatch - binary may have been modified!"
```

### 2. Version Consistency Check

All these files must have matching version numbers:
- `VoiceLite/VoiceLite/VoiceLite.csproj` → `<Version>X.X.X</Version>`
- `VoiceLite/Installer/VoiceLiteSetup.iss` → `AppVersion=X.X.X`
- `voicelite-web/package.json` → `"version": "X.X.X"`
- `voicelite-web/app/api/download/route.ts` → Default download version

### 3. Build Configuration Check

**Debug vs Release Mode**
```csharp
// WARNING: Building installer in Debug mode
// Check: VoiceLite.csproj should use Release configuration

// CRITICAL: Logging suppressed in Release (v1.0.94 bug)
// Verify: ErrorLogger doesn't have #if !DEBUG blocks
```

### 4. Dependency Verification

**Required files in installer**:
- [x] VoiceLite.exe (main application)
- [x] ggml-tiny.bin (42MB - free model)
- [x] whisper.exe (transcription engine)
- [x] VC++ Runtime installers
- [x] All required DLLs

### 5. Git State Check

```bash
# Uncommitted critical files
git status --porcelain | grep -E "(\.iss|\.csproj|package\.json)" && WARN "Uncommitted version files"

# Tag exists for this version
version=$(grep -oP '(?<=<Version>)[^<]+' VoiceLite/VoiceLite/VoiceLite.csproj)
git tag | grep -q "v$version" && WARN "Tag v$version already exists"
```

## Action Items Generated

When issues are detected:

1. **Missing Model File** → Add to git, update installer script
2. **Version Mismatch** → List all locations needing update
3. **Debug Mode** → Switch to Release configuration
4. **Git Issues** → Commit changes before building

## Historical Context

**v1.0.95-96 Disaster**: ggml-tiny.bin was in .gitignore, causing installer to ship without the model. This resulted in 100% failure rate for new installations.

**v1.0.94 Bug**: Logging was suppressed in Release builds with `#if !DEBUG`, making production debugging impossible.

## Quick Pre-Release Checklist

Before building installer:
1. [ ] Model file exists: `VoiceLite/whisper/ggml-tiny.bin` (42MB)
2. [ ] Model not in .gitignore
3. [ ] Whisper.exe present and correct hash
4. [ ] All version files match (`.csproj`, `.iss`, `package.json`)
5. [ ] Building in Release mode (not Debug)
6. [ ] No uncommitted version changes
7. [ ] Installer script includes all required files