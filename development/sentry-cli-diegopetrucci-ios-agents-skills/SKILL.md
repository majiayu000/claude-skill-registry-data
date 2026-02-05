---
name: sentry-cli
description: Sentry CLI tool for error tracking and monitoring workflows. Use when working with Sentry for (1) Creating and managing releases, (2) Uploading debug symbols (dSYMs) for iOS/mobile crash reporting, (3) Uploading source maps for JavaScript/web applications, (4) Associating commits with releases for issue tracking, (5) Managing deploys across environments, (6) Validating debug information files, or any other Sentry-related development and deployment tasks. Assumes sentry-cli is installed via brew and user is authenticated.
---

# Sentry CLI

## Overview

Work with Sentry's error tracking and monitoring platform through the command-line interface. Handle release management, debug symbol uploads for crash reporting, source map uploads for JavaScript error tracking, and deployment tracking across environments.

## Quick Start

Determine which Sentry workflow you need:

**Release Management** → Creating new releases, associating commits, tracking versions
**Debug Symbols (iOS/Mobile)** → Uploading dSYMs for crash report symbolication
**Source Maps (Web/JavaScript)** → Uploading source maps for JavaScript error tracking
**Deploys** → Recording deployments to specific environments

All commands assume `SENTRY_ORG` and `SENTRY_PROJECT` are configured via environment variables or config file. If not, add `-o <org> -p <project>` flags to commands.

## Release Management

### Creating Releases

Create a release to track which code version is deployed:

```bash
# Auto-determine version from git
VERSION=$(sentry-cli releases propose-version)
sentry-cli releases new "$VERSION"

# Or use explicit version
sentry-cli releases new "1.0.0"

# Create and finalize immediately
sentry-cli releases new "$VERSION" --finalize
```

### Associating Commits

Link commits to releases for issue tracking and suspect commit identification:

```bash
# Automatic (requires repository integration)
sentry-cli releases set-commits "$VERSION" --auto

# Local git (no repository integration needed)
sentry-cli releases set-commits "$VERSION" --local

# Ignore missing commits (for rebased/amended commits)
sentry-cli releases set-commits "$VERSION" --auto --ignore-missing
```

### Finalizing Releases

Finalize after all build artifacts are uploaded:

```bash
sentry-cli releases finalize "$VERSION"
```

**When to finalize:** After uploading all debug symbols, source maps, and other artifacts. Finalization adds a timestamp that affects issue resolution tracking.

### Typical Release Workflow

```bash
# 1. Create release
VERSION=$(sentry-cli releases propose-version)
sentry-cli releases new "$VERSION"

# 2. Upload artifacts (debug symbols, source maps, etc.)
# ... see sections below ...

# 3. Associate commits
sentry-cli releases set-commits "$VERSION" --auto

# 4. Finalize
sentry-cli releases finalize "$VERSION"

# 5. Record deploy (see Deploys section)
```

## Debug Information Files (iOS/Mobile)

### Uploading Debug Symbols

Upload dSYMs and other debug files for crash symbolication:

```bash
# Basic upload (recursively scans directory)
sentry-cli debug-files upload /path/to/dsyms

# With server-side processing wait
sentry-cli debug-files upload --wait /path/to/dsyms

# iOS with BCSymbolMaps (for bitcode builds with hidden symbols)
sentry-cli debug-files upload \
  --symbol-maps /path/to/BCSymbolMaps \
  /path/to/dsyms

# With source bundles for source context
sentry-cli debug-files upload --include-sources /path/to/dsyms
```

### Validating Debug Files

Check if debug files are valid before uploading:

```bash
sentry-cli debug-files check /path/to/file.dSYM
```

### Finding Missing Debug Files

When crash reports show missing symbols:

```bash
sentry-cli debug-files find <debug-identifier>
```

### iOS Build Integration

For Xcode projects, typically integrate into build phases:

```bash
# After archive/export, upload dSYMs
DSYM_PATH="$DWARF_DSYM_FOLDER_PATH"
sentry-cli debug-files upload --wait "$DSYM_PATH"
```

## Source Maps (Web/JavaScript)

### Uploading Source Maps

Upload source maps for JavaScript error tracking:

```bash
# Basic upload
sentry-cli sourcemaps upload /path/to/build

# With URL prefix (maps file paths to deployed URLs)
sentry-cli sourcemaps upload \
  --url-prefix '~/static/js' \
  /path/to/build

# Strip common prefix for cleaner paths
sentry-cli sourcemaps upload \
  --url-prefix '~/static/js' \
  --strip-common-prefix \
  /path/to/build

# With distribution identifier (for multiple build variants)
sentry-cli sourcemaps upload \
  --dist "$BUILD_ID" \
  /path/to/build
```

### Key Options

- `--url-prefix`: Match deployed asset URLs (e.g., `~/static/js` or `https://example.com/js`)
- `--strip-common-prefix`: Simplify path mappings by removing common prefixes
- `--dist`: Differentiate build variants (use same value in Sentry SDK configuration)
- `--ignore-file`: Exclude files using `.sentryignore` patterns
- `--strict`: Fail if no source maps found
- `--validate`: Enable validation when using `--no-rewrite`

### Build Tool Integration

Typically integrate into build scripts:

```bash
# After production build
npm run build

# Upload source maps
sentry-cli sourcemaps upload \
  --url-prefix '~/static/js' \
  --strip-common-prefix \
  build/static/js
```

## Deploys

### Recording Deploys

Track when releases are deployed to environments:

```bash
# Basic deploy
sentry-cli deploys new \
  --release "$VERSION" \
  -e production

# With duration tracking
start=$(date +%s)
# ... deployment process ...
now=$(date +%s)
sentry-cli deploys new \
  --release "$VERSION" \
  -e production \
  -t $((now-start))
```

### Listing Deploys

```bash
sentry-cli deploys list --release "$VERSION"
```

## Configuration

### Verify Setup

```bash
sentry-cli info
```

### Environment Variables

Set these for automatic configuration:

```bash
export SENTRY_ORG="my-org"
export SENTRY_PROJECT="my-project"
export SENTRY_AUTH_TOKEN="your-token"
```

Or use config file `~/.sentryclirc`:

```ini
[auth]
token=your-token

[defaults]
org=my-org
project=my-project
```

### Command-Line Flags

Override config for specific commands:

```bash
sentry-cli -o my-org -p my-project releases new "$VERSION"
```

## Common Workflows

### iOS App Release

```bash
# 1. Create release
VERSION=$(sentry-cli releases propose-version)
sentry-cli releases new "$VERSION"

# 2. Upload dSYMs after archive
sentry-cli debug-files upload --wait "$DWARF_DSYM_FOLDER_PATH"

# 3. Associate commits
sentry-cli releases set-commits "$VERSION" --local

# 4. Finalize
sentry-cli releases finalize "$VERSION"

# 5. Record deploy
sentry-cli deploys new --release "$VERSION" -e production
```

### Web Application Release

```bash
# 1. Create release
VERSION=$(git rev-parse HEAD)
sentry-cli releases new "$VERSION"

# 2. Build application
npm run build

# 3. Upload source maps
sentry-cli sourcemaps upload \
  --url-prefix '~/static/js' \
  --strip-common-prefix \
  build/static/js

# 4. Associate commits
sentry-cli releases set-commits "$VERSION" --auto

# 5. Finalize
sentry-cli releases finalize "$VERSION"

# 6. Record deploy
sentry-cli deploys new --release "$VERSION" -e production
```

## Detailed Command Reference

For comprehensive command syntax, options, and additional examples, see [references/commands.md](references/commands.md).
