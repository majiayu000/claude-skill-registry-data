---
name: hackage-upload
description: Upload Haskell packages to Hackage. Use when the user asks to publish, release, or upload to Hackage.
---

# Hackage Upload

## Instructions

When the user asks to publish or upload to Hackage:

1. **Get the current version** from `claude.cabal`:
   ```bash
   grep "^version:" claude.cabal
   ```

2. **Create the source distribution**:
   ```bash
   cabal sdist
   ```

3. **Upload to Hackage** (replace X.Y.Z with actual version):
   ```bash
   cabal upload --publish dist-newstyle/sdist/claude-X.Y.Z.tar.gz
   ```

## Pre-release checklist

Before uploading, ensure:
- Version in `claude.cabal` has been bumped
- `CHANGELOG.md` has an entry for this version
- All tests pass (`cabal test`)
- Code compiles without warnings (`cabal build`)

## Notes

- The `--publish` flag publishes immediately. Without it, the package is uploaded as a candidate.
- You must have Hackage credentials configured (typically in `~/.cabal/config`).
- First-time uploads of a package require manual approval on Hackage.
