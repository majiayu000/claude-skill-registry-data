---
name: nomos-compilation-debugging
description: Systematic debugging guide for Nomos compilation failures. Use this when compilation fails, providers won't start, references are unresolved, or builds produce unexpected output.
---

# Nomos Compilation Debugging

This skill provides a systematic approach to debugging Nomos compilation failures, from provider issues to reference resolution errors.

## When to Use This Skill

- `nomos build` command fails with errors
- Provider-related failures (not found, connection refused)
- Reference resolution errors (`unresolved reference`)
- Import cycle detection failures
- Unexpected compilation output or determinism issues
- Provider initialization or fetch errors

## Diagnostic Process

Follow these steps in order for systematic troubleshooting:

### Step 1: Identify Error Category

Compilation errors fall into these categories:

1. **Provider Errors** - Provider binary issues, connection failures
2. **Reference Errors** - Unresolved references, invalid paths
3. **Import Errors** - Cycle detection, missing imports, parse failures
4. **Syntax Errors** - Invalid .csl syntax
5. **Configuration Errors** - Missing lockfile, invalid provider config
6. **Determinism Issues** - Non-reproducible builds

### Step 2: Check Provider Configuration

#### Verify Lockfile Exists

```bash
# Check for providers lockfile
ls -la .nomos/providers.lock.json

# If missing, run init:
nomos init config.csl
```

**Expected lockfile structure:**
```json
{
  "providers": [
    {
      "alias": "configs",
      "type": "file",
      "version": "0.2.0",
      "os": "darwin",
      "arch": "arm64",
      "path": ".nomos/providers/file/0.2.0/darwin-arm64/provider",
      "checksum": "sha256:..."
    }
  ]
}
```

#### Verify Provider Binaries Installed

```bash
# Check provider directory structure
find .nomos/providers -type f -name "provider"

# Expected structure:
# .nomos/
#   providers/
#     file/
#       0.2.0/
#         darwin-arm64/
#           provider         # Must be executable

# Verify binary is executable
ls -l .nomos/providers/file/0.2.0/darwin-arm64/provider
# Should show: -rwxr-xr-x (executable flag)

# If not executable:
chmod +x .nomos/providers/file/0.2.0/darwin-arm64/provider
```

#### Test Provider Binary Manually

```bash
# Run provider directly - should print PORT
.nomos/providers/file/0.2.0/darwin-arm64/provider
# Expected output: PORT=<number>

# If it crashes or prints errors, provider is broken
# Solution: Re-download with nomos init --force
```

### Step 3: Debug Provider Connection Failures

**Symptom:** `failed to start provider` or `connection refused`

#### Check Provider Startup

```bash
# Enable verbose logging if available
# Run build with provider debugging
nomos build config.csl 2>&1 | tee build.log

# Look for:
# - "Starting provider: <alias>"
# - "Provider port: <port>"
# - Connection errors
```

#### Verify Provider Protocol

Provider must:
1. Listen on `127.0.0.1` (localhost only)
2. Print `PORT=<number>` to stdout
3. Start gRPC server before returning
4. Implement all required RPCs (Init, Fetch, Info, Health, Shutdown)

**Test with minimal config:**
```nomos
source:
  alias: 'test'
  type: 'autonomous-bits/nomos-provider-file'
  version: '0.2.0'
```

### Step 4: Debug Reference Resolution Errors

**Symptom:** `unresolved reference: reference:alias:path`

#### Verify Source Declaration

Check that provider alias is declared:

```nomos
source:
  alias: 'configs'  # Must match reference alias
  type: 'autonomous-bits/nomos-provider-file'
  version: '0.2.0'

app:
  name: reference:configs:app.name  # Alias must match
```

#### Verify Reference Path Exists

Test provider Fetch manually if possible:

```bash
# For file provider, verify file exists
ls -la ./data/app.name  # or whatever the file path should be
```

#### Check Provider Init Configuration

Ensure provider receives correct configuration:

```nomos
source:
  alias: 'configs'
  type: 'autonomous-bits/nomos-provider-file'
  version: '0.2.0'
  directory: './data'  # Provider-specific config
```

**Common Issues:**
- Missing required config fields (e.g., `directory` for file provider)
- Incorrect config types (string vs number)
- Relative paths that don't resolve correctly

#### Enable AllowMissingProvider Mode

For debugging, continue compilation without provider:

```bash
# This will show warnings but not fail
nomos build --allow-missing-provider config.csl
```

### Step 5: Debug Import Errors

**Symptom:** `cycle detected` or `failed to resolve import`

#### Check Import Statements

Verify import syntax:

```nomos
import:base:./base.csl  # Correct format: import:<alias>:<path>
```

#### Detect Import Cycles

```
A imports B
B imports C
C imports A  ← Cycle!
```

**Solution:** Refactor to break cycle
- Extract shared config to separate file
- Remove circular dependencies
- Use references instead of imports where possible

#### Verify Import Paths

```bash
# Check that imported files exist
ls -la ./base.csl
ls -la ./shared/common.csl

# Verify paths are relative to importing file or absolute
```

### Step 6: Debug Syntax Errors

**Symptom:** Parse errors with line/column numbers

#### Read Error Messages Carefully

Parser errors show:
```
config.csl:15:3: SyntaxError: expected ':' after key
```

**Location format:** `<file>:<line>:<column>`

#### Common Syntax Mistakes

1. **Missing colons:**
   ```nomos
   # ❌ Wrong
   database
     host: localhost
   
   # ✅ Correct
   database:
     host: localhost
   ```

2. **Invalid reference syntax:**
   ```nomos
   # ❌ Wrong
   app: reference:configs.app.name
   
   # ✅ Correct
   app: reference:configs:app.name
   ```

3. **Empty source alias:**
   ```nomos
   # ❌ Wrong
   source:
     alias: ''
   
   # ✅ Correct
   source:
     alias: 'myalias'
   ```

### Step 7: Debug Determinism Issues

**Symptom:** Same input produces different output on repeated builds

#### Test Reproducibility

```bash
# Build twice and compare
nomos build config.csl -o output1.json
nomos build config.csl -o output2.json
diff output1.json output2.json

# Should be identical (exit code 0)
```

#### Common Causes

1. **Provider non-determinism:** Provider returns different data
   - Solution: Fix provider to be deterministic or use caching

2. **Timestamp injection:** Metadata includes timestamps
   - Solution: Remove timestamps or make them optional

3. **Map iteration order:** Go maps iterate in random order
   - Solution: Sort keys before serialization (compiler does this)

4. **Concurrent provider fetches:** Race conditions
   - Solution: Enable provider caching (compiler does this)

#### Verify File Order

Nomos processes files in lexicographic order (UTF-8):

```bash
# Check file discovery order
find . -name "*.csl" -type f | sort

# Should match compilation order in build output
```

### Step 8: Check Configuration Merge Behavior

**Symptom:** Unexpected values in final output

#### Understand Merge Semantics

Nomos deep-merge rules:
- **Maps:** Recursive merge, combining keys
- **Scalars:** Last-wins (newer value replaces older)
- **Arrays:** Last-wins (entire array replaced)

```nomos
# base.csl
database:
  host: localhost
  port: 5432

# override.csl
import:base:./base.csl
database:
  host: prod-server  # Overrides localhost
  # port: 5432 preserved from base
```

#### Trace Value Provenance

Enable metadata tracking if available to see where values came from.

### Step 9: Verify Platform-Specific Issues

**Symptom:** Works on one OS/arch but not another

#### Check Provider Platform

Provider binaries are platform-specific:

```bash
# Verify correct binary for your platform
uname -sm
# Darwin arm64 → darwin-arm64
# Linux x86_64 → linux-amd64

# Check lockfile matches:
cat .nomos/providers.lock.json | grep -A 5 '"os"'
```

#### Cross-Platform Installation

Install providers for different platforms:

```bash
# Install for Linux on macOS development machine
nomos init --os linux --arch amd64 config.csl

# Then push .nomos/ directory to Linux CI
```

## Common Error Messages and Solutions

### "provider binary not found"

**Cause:** Provider not installed or wrong path in lockfile

**Solution:**
```bash
nomos init --force config.csl  # Re-download
```

### "connection refused"

**Cause:** Provider failed to start or wrong port

**Solution:**
1. Test provider manually: `.nomos/providers/.../provider`
2. Check provider prints `PORT=<number>`
3. Verify provider doesn't exit immediately

### "unresolved reference"

**Cause:** Reference path doesn't exist in provider data

**Solution:**
1. Verify source alias matches reference
2. Check provider configuration (e.g., directory path)
3. Test provider data manually
4. Use `--allow-missing-provider` to debug

### "cycle detected"

**Cause:** Circular import chain

**Solution:**
1. Map import chain: A → B → C → A
2. Extract shared config to break cycle
3. Use references instead of imports

### "invalid checksum"

**Cause:** Provider binary modified or corrupted

**Solution:**
```bash
# Re-download provider
nomos init --force config.csl

# Or manually verify checksum
shasum -a 256 .nomos/providers/.../provider
# Compare with lockfile checksum
```

## Advanced Debugging

### Enable Verbose Logging

If Nomos supports verbose mode:

```bash
nomos build -v config.csl       # Verbose output
nomos build -vv config.csl      # Very verbose (debug level)
```

### Inspect Provider gRPC Communication

Use gRPC debugging tools if needed:

```bash
# Find provider port
ps aux | grep provider

# Connect with grpcurl (if provider running)
grpcurl -plaintext localhost:<port> list
grpcurl -plaintext localhost:<port> nomos.provider.v1.ProviderService/Info
```

### Test Components Individually

1. **Parse only:** Verify .csl syntax
2. **Init only:** Test provider installation
3. **Build without providers:** Use `--allow-missing-provider`
4. **Build single file:** Isolate problematic config

## Prevention Best Practices

1. **Commit lockfile:** Check `.nomos/providers.lock.json` into git
2. **Pin versions:** Use explicit version in source declarations
3. **Test providers:** Verify provider works before using in config
4. **Validate syntax:** Use editor tooling for .csl files
5. **Run CI builds:** Catch determinism issues early
6. **Document references:** Comment expected provider data structure

## Reference Documentation

For more details, see:
- [Nomos CLI Documentation](../../apps/command-line/README.md)
- [Compiler Library Documentation](../../libs/compiler/README.md)
- [Provider Authoring Guide](../../docs/guides/provider-authoring-guide.md)
- [External Providers Architecture](../../docs/architecture/nomos-external-providers-feature-breakdown.md)
