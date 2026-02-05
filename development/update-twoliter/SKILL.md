---
name: update-twoliter
description: Update all Bottlerocket repositories to a new Twoliter version
---

# Skill: Update Twoliter Version

## Purpose

Update all repositories in the forest to a new version of Twoliter. This creates git commits in core-kit, kernel-kit, and bottlerocket repositories with the updated version and SHA256 checksums.

## When to Use

- Testing a new Twoliter release candidate
- Updating to a new stable Twoliter release
- Preparing pull requests to trigger CI testing with a new Twoliter version

## Prerequisites

- All repositories cloned in the forest
- Git configured with author information
- Network access to GitHub releases

## Procedure

### 1. Fetch SHA256 checksums for the new version

Replace `X.Y.Z` with the target version (e.g., `0.13.0` or `0.13.0-rc1`):

```bash
# For x86_64
curl -sSL "https://github.com/bottlerocket-os/twoliter/releases/download/vX.Y.Z/twoliter-x86_64-unknown-linux-musl.tar.xz.sha256"

# For aarch64
curl -sSL "https://github.com/bottlerocket-os/twoliter/releases/download/vX.Y.Z/twoliter-aarch64-unknown-linux-musl.tar.xz.sha256"
```

### 2. Update all kits

For each kit in the worktree (e.g., `bottlerocket-core-kit`, `bottlerocket-kernel-kit`), edit the `Makefile`:

```makefile
TWOLITER_VERSION ?= "X.Y.Z"
TWOLITER_SHA256_AARCH64 ?= "<aarch64-sha256>"
TWOLITER_SHA256_X86_64 ?= "<x86_64-sha256>"
```

Commit each kit:
```bash
cd kits/<kit-name>
git add Makefile
git commit -m "chore: bump to twoliter X.Y.Z"
cd ../..
```

### 3. Update bottlerocket

Edit `bottlerocket/Makefile.toml` in the worktree (note the `v` prefix):

```toml
TWOLITER_VERSION = "vX.Y.Z"
TWOLITER_SHA256_AARCH64 = "<aarch64-sha256>"
TWOLITER_SHA256_X86_64 = "<x86_64-sha256>"
```

Commit:
```bash
cd bottlerocket
git add Makefile.toml
git commit -m "chore: bump to twoliter X.Y.Z"
```

## Validation

Verify commits were created in all kits and bottlerocket:

```bash
# Check each kit
for kit in kits/*/; do
  echo "=== $(basename $kit) ==="
  (cd "$kit" && git show HEAD --stat)
done

# Check bottlerocket
(cd bottlerocket && git show HEAD --stat)
```

Each should show:
- Commit message: `chore: bump to twoliter X.Y.Z`
- 1 file changed, 3 insertions(+), 3 deletions(-)

## Common Issues

**SHA256 checksum not found:**
- Verify the release exists: `https://github.com/bottlerocket-os/twoliter/releases/tag/vX.Y.Z`
- Check that binary artifacts are attached to the release

**Wrong version format:**
- Kits use `"X.Y.Z"` (no `v` prefix) in their Makefiles
- bottlerocket uses `"vX.Y.Z"` (with `v` prefix) in Makefile.toml

**Amending commits:**
If you need to update an existing commit (e.g., moving from RC to stable):
```bash
# Make the file changes, then:
git add <file>
git commit --amend -m "chore: bump to twoliter X.Y.Z"
```

## Related Skills

- None (standalone skill)

## Notes

- This skill does NOT push commits or create pull requests
- After creating commits, you can push them and create PRs manually
- PRs will trigger CI to test the new Twoliter version
- Schema version changes are rare; only update if release notes specify
