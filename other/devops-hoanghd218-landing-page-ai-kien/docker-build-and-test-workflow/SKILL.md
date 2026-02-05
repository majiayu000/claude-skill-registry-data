---
name: Docker Build and Test Workflow
description:
  Use this skill when building, testing, or working with Docker images in the
  agentic-container repository. Covers when to rebuild vs reuse images, how to
  leverage layer caching, and efficient iteration patterns.
allowed-tools: [Bash, Read, Grep, Glob]
---

# Docker Build and Test Workflow

This skill provides guidance for efficiently building, testing, and working with
Docker images in this repository.

## Core Principles

1. **Scripts rebuild by design** - The testing scripts prioritize reliability
   over speed by rebuilding images
2. **Docker layer caching is your friend** - Rebuilds are fast when only small
   changes occur
3. **Avoid unnecessary script invocations** - Reuse existing images when
   possible
4. **Manual cache management** - Only delete images as a last resort

## Understanding Script Behavior

### What the Scripts Actually Do

**`scripts/build-local.sh [target]`**

- Builds specified target (standard, dev, or stage)
- Relies on Docker layer caching for speed
- Securely handles GitHub token via `gh auth`
- Always performs a build, but uses cache when available

**`scripts/test-dockerfile.sh [target|dockerfile] [--cleanup]`**

- For **base targets** (standard/dev): Always rebuilds via `build-local.sh`
- For **cookbooks**: Smart about base (`ensure_base_image()` checks timestamps),
  but always rebuilds cookbook
- Runs comprehensive goss validation tests
- Keeps test images by default (use `--cleanup` to remove)

**`scripts/shell.sh [target|cookbook] [tag]`**

- Always rebuilds the specified target or cookbook
- Launches interactive shell in the container
- Auto-cleans container on exit (but keeps image)

### The One Smart Cache Check

The `ensure_base_image()` function (used for cookbook testing):

- Checks if `agentic-container:latest` exists
- Compares Dockerfile modification time vs image creation time
- **Only rebuilds base if Dockerfile is newer or image missing**
- This is the ONLY automatic cache optimization in the scripts

## Efficient Workflow Patterns

### Pattern 1: Initial Build + Iterative Testing

```bash
# Step 1: Initial build and test (will rebuild)
./scripts/test-dockerfile.sh standard

# Step 2: Iterate on goss tests WITHOUT rebuilding
# Edit goss/standard.yaml, then:
docker run --rm --user root \
  -v "$PWD/goss/base-common.yaml:/tmp/goss-base-common.yaml:ro" \
  -v "$PWD/goss/standard.yaml:/tmp/goss-base.yaml:ro" \
  test-standard:latest \
  bash -c 'goss -g /tmp/goss-base-common.yaml -g /tmp/goss-base.yaml validate --format documentation'

# Step 3: Final test with script (rebuilds to verify)
./scripts/test-dockerfile.sh standard --cleanup
```

### Pattern 2: Check Before Rebuilding

```bash
# Check what images exist
docker images | grep -E '(agentic|test-)'

# If test-standard:latest exists, use it directly
docker run --rm test-standard:latest python --version

# Only rebuild if you changed the Dockerfile
./scripts/build-local.sh standard agentic-container:latest
```

### Pattern 3: Cookbook Development

```bash
# Initial build and test (smart about base, rebuilds cookbook)
./scripts/test-dockerfile.sh docs/cookbooks/python-cli/Dockerfile

# The script built: test-dockerfile-TIMESTAMP image
# Find it:
docker images | grep test-dockerfile

# Debug with existing image (no rebuild)
docker run --rm -it test-dockerfile-1234567890 bash

# When done iterating, run final test with cleanup
./scripts/test-dockerfile.sh docs/cookbooks/python-cli/Dockerfile --cleanup
```

### Pattern 4: Quick Validation

```bash
# Instead of shell.sh (which rebuilds), use existing image:
docker run --rm -it test-standard:latest bash

# Or run a quick command:
docker run --rm test-standard:latest mise list
```

### Pattern 5: Prototyping Dockerfile Commands

When adding complex commands to Dockerfile, test them first in existing image:

```bash
# Step 1: Test interactively to develop the command
docker run --rm -it --user root test-dev:latest bash
# Inside container, try commands until they work:
# $ mkdir -p /some/path
# $ ln -sf source target
# $ command --version
# $ exit

# Step 2: Test as one-liner (how Dockerfile RUN works)
docker run --rm --user root test-dev:latest bash -c '
mkdir -p /some/path && \
ln -sf source target && \
command --version
'

# Step 3: If successful, add to Dockerfile
RUN mkdir -p /some/path \
    && ln -sf source target

# Step 4: Rebuild and verify changes persisted
./scripts/test-dockerfile.sh dev
docker run --rm test-dev:latest command --version
```

**Why This Matters:**

- Catches path issues, permission problems, and syntax errors before build
- Validates that commands work in the actual environment
- Much faster than rebuild cycles for iteration
- Helps understand what files/directories already exist

**Common Use Cases:**

- Creating symlinks (test paths are correct)
- Setting up configuration files
- Verifying package installations work
- Testing permission requirements

### Pattern 6: Debugging Multi-Stage Builds

When packages or files are missing from final image but work in build stage:

```bash
# Step 1: Build the intermediate stage directly
./scripts/build-local.sh npm-globals-stage test-npm-globals:latest

# Step 2: Inspect what the stage actually contains
docker run --rm test-npm-globals:latest bash -c 'ls -la /path/to/expected/files'

# Step 3: Check for symlinks (Docker COPY follows them!)
docker run --rm test-npm-globals:latest bash -c 'ls -la /path/to/bin/'

# Step 4: Compare to final image
docker run --rm test-dev:latest bash -c 'ls -la /path/to/bin/'

# Step 5: Identify what's different
# - Symlinks become regular files when COPY'd
# - Permissions may change
# - Files might be in different locations
```

**Common Multi-Stage Issues:**

- **Docker COPY follows symlinks** - Converts them to regular files, breaking
  relative paths
- **Files exist in stage but not in final** - Check COPY commands copy the right
  paths
- **Permissions change between stages** - RUN commands in final stage may run as
  different user
- **ARG not passed to stage** - Re-declare ARG in each stage that needs it

**Solution Patterns:**

- For symlinks: Recreate them in final stage with RUN command
- For missing files: Verify COPY source path includes the files
- For permissions: Run chmod in final stage after COPY

## When Rebuilds Are Required

### You MUST Rebuild When:

- Dockerfile content changed (RUN, COPY, ADD, etc.)
- ARG versions updated (NODE_VERSION, PYTHON_VERSION, etc.)
- Base image dependencies changed
- Files copied into image (COPY/ADD) have changed

### Layer Cache Makes These Fast When:

- Only bottom layers changed (Dockerfile ordered well)
- System packages unchanged (apt-get install cached)
- Language installations unchanged (mise installations cached)
- Only scripts or configs changed

### You DON'T Need to Rebuild When:

- Only goss test files changed (mount them at test time)
- Documentation changed (\*.md files)
- CI configuration changed (.github/workflows/\*.yml)
- Comments in Dockerfile changed

## Layer Cache Optimization

### Understanding Image vs Layer Cache

**CRITICAL: Deleting an image DOES NOT clear layer cache!**

```bash
# This removes the image tag but layers persist:
docker rmi test-dev:latest

# Build will still show CACHED for unchanged layers:
./scripts/test-dockerfile.sh dev

# To actually clear layer cache:
docker builder prune -f

# Nuclear option (clears everything including unused images):
docker system prune -f && docker builder prune -f
```

**Why This Matters:**

- Docker stores layers separately from image tags
- Multiple images can share the same layers
- Removing an image only removes the tag, not the layers
- Layer cache persists across branches and image deletions

### Understanding Layer Invalidation

Docker rebuilds from the first changed layer onward. Order matters:

```dockerfile
# ✅ GOOD: Infrequently changing items first
FROM ubuntu:24.04
RUN apt-get update && apt-get install -y curl
ARG NODE_VERSION=24.8.0
RUN mise use -g node@${NODE_VERSION}
COPY scripts/ /usr/local/bin/  # Changes frequently

# ❌ BAD: Frequently changing items first
FROM ubuntu:24.04
COPY scripts/ /usr/local/bin/  # Changes frequently, invalidates all below
RUN apt-get update && apt-get install -y curl
```

### Checking Cache Effectiveness

```bash
# Watch build output for "CACHED" vs "RUN" steps
./scripts/build-local.sh standard agentic-container:test | grep -E '(CACHED|RUN|COPY)'

# If you see mostly CACHED, layer cache is working well
# If you see mostly RUN, something early in Dockerfile changed
```

### When Layer Cache Causes Problems

**Symptom:** Build shows "CACHED" but you changed the Dockerfile **Cause:**
Layer hash collision or cache from different branch/state

**Solutions:**

1. **Make a small change to force cache bust** - Add/modify a comment in the RUN
   command
2. **Clear builder cache** - `docker builder prune -f` (fast, selective)
3. **Use --no-cache** - Only as last resort (slowest, rebuilds everything)

**Example Cache Bust:**

```dockerfile
# Before (keeps showing CACHED even after adding commands):
RUN mise use -g node@${NODE_VERSION} \
    && your-new-commands-here

# After (change comment to bust cache):
# v2: Added symlink creation
RUN mise use -g node@${NODE_VERSION} \
    && your-new-commands-here
```

**Verifying Changes Persisted:**

```bash
# Check if your changes made it into the image:
docker history test-dev:latest --no-trunc | grep "your-command"

# Or inspect the actual files:
docker run --rm test-dev:latest ls -la /path/to/your/files
```

## Working with Test Images

### Test Image Naming Conventions

- Base targets in local mode: `test-standard:latest`, `test-dev:latest`
- Cookbooks in local mode: `test-dockerfile-TIMESTAMP` (timestamped)
- CI mode: Pre-built images with specific tags

### Retaining vs Cleaning Up

```bash
# Default: Keep test images for inspection
./scripts/test-dockerfile.sh standard
docker run --rm -it test-standard:latest bash  # Debug it

# Cleanup when done
docker rmi test-standard:latest

# Or use --cleanup flag (auto-removes after tests pass)
./scripts/test-dockerfile.sh standard --cleanup
```

## Troubleshooting

### RUN Command Not Working

**Symptom:** Added commands to Dockerfile but they don't seem to execute or
changes don't persist

**Debugging Steps:**

```bash
# 1. Check if command is in image history
docker history test-dev:latest --no-trunc | grep "your-command"

# 2. If found, check if changes actually exist in image
docker run --rm test-dev:latest ls -la /path/to/expected/files

# 3. If not found or layer shows CACHED, try cache bust
# Edit Dockerfile: add/change a comment in the RUN command

# 4. Test the command manually first (Pattern 5)
docker run --rm --user root test-dev:latest bash -c 'your-command'
```

**Common Causes:**

- Layer cache hiding your changes (try cache bust)
- Command fails silently in `&&` chain (test commands individually)
- Wrong user (check if RUN runs as root but final image is non-root)
- Path issues (prototype in existing image first)

### Files Missing in Final Image

**Symptom:** Files exist in build stage but not in final multi-stage image

**Debugging Steps:**

```bash
# 1. Build and inspect the intermediate stage
./scripts/build-local.sh your-stage test-stage:latest
docker run --rm test-stage:latest ls -la /expected/path

# 2. Compare to final image
docker run --rm test-dev:latest ls -la /expected/path

# 3. Check if symlinks are involved
docker run --rm test-stage:latest bash -c 'ls -la /path/ | grep "^l"'
```

**Common Causes:**

- Docker COPY follows symlinks (recreate them in final stage)
- COPY path doesn't include the files you expect
- Files in different location than you think
- ARG not declared in the stage where COPY happens

### Build Shows CACHED But You Changed Dockerfile

**Symptom:** Modified Dockerfile but build output shows "CACHED" for your layer

**Solutions:**

```bash
# Option 1: Force cache bust with small change
# Add or modify a comment in the RUN command

# Option 2: Clear builder cache
docker builder prune -f

# Option 3: Verify your change is actually different
git diff Dockerfile  # Did the change actually save?
```

**Why This Happens:**

- Docker layer cache persists beyond image deletion
- Layer hash collision (rare but possible)
- Changes don't affect layer hash (comment-only changes)

### Build is Slow

1. **Check if layer cache is working**: Look for "CACHED" in build output
2. **Identify what changed**: Compare to last build
3. **Consider if rebuild is necessary**: Can you test with existing image?
4. **Last resort**: This is normal for FROM scratch builds or major changes

### Tests Failing After Dockerfile Changes

1. **Test with existing image first**: Isolate if it's a Dockerfile vs test
   issue
2. **Check goss test validity**: Can tests pass with old image?
3. **Rebuild and test**: `./scripts/test-dockerfile.sh`

### Image Doesn't Exist

```bash
# Check what you have
docker images | grep -E '(agentic|test-)'

# Build what you need
./scripts/test-dockerfile.sh dev  # Builds test-dev:latest
```

### Cache Seems Corrupted

**Symptoms:**

- Build errors with "snapshot does not exist"
- Inconsistent build results
- Cache-related build failures

**Only as last resort:**

```bash
# Nuclear option: clear all cache and rebuild
docker system prune -f && docker builder prune -f

# Rebuild from scratch (will take several minutes)
./scripts/test-dockerfile.sh dev
```

## Common Commands Reference

### Building

```bash
# Build base standard target
./scripts/build-local.sh standard agentic-container:latest

# Build dev target
./scripts/build-local.sh dev agentic-container:dev

# Build specific stage
./scripts/build-local.sh python-stage python-only:latest
```

### Testing

```bash
# Test base target (rebuilds)
./scripts/test-dockerfile.sh standard

# Test with cleanup
./scripts/test-dockerfile.sh standard --cleanup

# Test cookbook
./scripts/test-dockerfile.sh docs/cookbooks/python-cli/Dockerfile

# CI mode (use pre-built image)
./scripts/test-dockerfile.sh standard test-standard:latest
```

### Interactive Debugging

```bash
# Using shell.sh (rebuilds)
./scripts/shell.sh standard

# Using existing image (no rebuild)
docker run --rm -it test-standard:latest bash

# Run a command in existing image
docker run --rm test-standard:latest python --version
```

### Image Management

```bash
# List all images
docker images | grep -E '(agentic|test-)'

# Remove test images
docker rmi $(docker images -q 'test-*')

# Check image age
docker image inspect agentic-container:latest --format '{{.Created}}'

# Check Dockerfile age
ls -l Dockerfile
```

### Debugging

```bash
# Inspect layer history
docker history test-dev:latest --no-trunc | grep "your-command"

# Test command manually as root
docker run --rm --user root test-dev:latest bash -c 'your-command'

# Interactive debugging session
docker run --rm -it --user root test-dev:latest bash

# Check if file exists in image
docker run --rm test-dev:latest ls -la /path/to/file

# Check for symlinks
docker run --rm test-dev:latest bash -c 'ls -la /path/ | grep "^l"'

# Compare files between stages
docker run --rm test-stage:latest ls -la /path
docker run --rm test-dev:latest ls -la /path
```

### Cache Management

```bash
# Clear builder cache (recommended)
docker builder prune -f

# Clear all Docker cache (nuclear option)
docker system prune -f && docker builder prune -f

# Check builder cache size
docker system df

# Remove specific image (doesn't clear layers!)
docker rmi test-dev:latest
```

## Decision Tree

```
Need to work with Docker image?
├─ Developing new Dockerfile commands?
│  ├─ Step 1: Prototype in existing image (Pattern 5)
│  ├─ Step 2: Add to Dockerfile
│  └─ Step 3: Test with ./scripts/test-dockerfile.sh
│
├─ RUN command not working as expected?
│  ├─ Check: docker history IMAGE | grep "command"
│  ├─ Test manually: docker run --user root IMAGE bash -c 'command'
│  └─ If CACHED: Add comment to bust cache
│
├─ Files missing in final image?
│  ├─ Build intermediate stage: ./scripts/build-local.sh STAGE
│  ├─ Inspect: docker run STAGE-IMAGE ls -la /path
│  └─ Check for symlinks: ls -la | grep "^l"
│
├─ Build shows CACHED but you changed Dockerfile?
│  ├─ Try: Modify a comment in the RUN command
│  ├─ Or: docker builder prune -f
│  └─ Verify: docker history IMAGE --no-trunc
│
├─ Making Dockerfile changes?
│  ├─ Yes → Run test-dockerfile.sh (will rebuild with cache)
│  └─ No ↓
│
├─ Making goss test changes only?
│  ├─ Yes → Use existing image with docker run + volume mounts
│  └─ No ↓
│
├─ Need interactive shell?
│  ├─ Image exists? → docker run -it IMAGE bash
│  └─ No image → ./scripts/test-dockerfile.sh TARGET
│
├─ Testing if something works?
│  ├─ Image exists? → docker run IMAGE your-test-command
│  └─ No image → ./scripts/test-dockerfile.sh TARGET
│
└─ Just want to build?
   └─ ./scripts/test-dockerfile.sh TARGET (preferred, includes tests)
   └─ Or: ./scripts/build-local.sh TARGET TAG (build only)
```

## Key Takeaways

1. **First run is always slower** - Subsequent runs use layer cache
2. **Scripts prioritize correctness** - They rebuild to ensure clean state
3. **Reuse images between script runs** - Docker's layer cache + manual reuse
4. **Don't fight the scripts** - They're designed to be reliable, not fast
5. **Layer cache is automatic** - You get it for free with Docker
6. **Manual cache management is rare** - Only needed when truly broken
7. **Test iterations don't need rebuilds** - Mount goss files and test directly

## When to Use This Skill

Invoke this skill when:

- User asks to build or test Docker images
- User asks how to iterate on Dockerfiles efficiently
- User complains about slow builds
- User asks about Docker cache
- User asks which script to use (build-local.sh vs test-dockerfile.sh vs
  shell.sh)
- User wants to test changes without rebuilding
- User needs to debug Docker images
- **RUN command not working** - Guide to test commands manually before adding to
  Dockerfile
- **Files missing in final image** - Debug multi-stage builds by inspecting
  intermediate stages
- **Build shows CACHED but Dockerfile changed** - Explain image vs layer cache
  difference
- **Symlinks or special files not working** - Docker COPY follows symlinks
  behavior
- **Permission errors in containers** - Test with --user root to debug
- **Prototyping new features** - Use existing images to test before modifying
  Dockerfile
- **Multi-stage build debugging** - Build and inspect intermediate stages
