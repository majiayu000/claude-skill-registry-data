---
name: HLS Troubleshooting
description: This skill should be used when the user mentions "HLS not working", "haskell-language-server issues", "Haskell LSP problems", "no completions in Haskell", "HLS diagnostics not showing", "troubleshoot HLS", "Haskell code analysis not working", or asks why HLS features aren't available in Claude Code.
---

# HLS Troubleshooting Guide

This skill provides guidance for diagnosing and resolving Haskell Language Server (HLS) issues in Claude Code.

## Overview

HLS provides LSP features for Haskell development: diagnostics, go-to-definition, completions, hover info, and code actions. When HLS isn't working, these features become unavailable for `.hs` and `.lhs` files.

## Quick Check

Before troubleshooting, run the status command to identify the problem:

```
/hls:status
```

This performs three checks: PATH availability, version info, and startup test.

## Progressive Troubleshooting

Diagnose issues from simple to complex. Most problems fall into one of three levels.

### Level 1: HLS Not Found in PATH

**Symptoms:**
- `/hls:status` reports PATH check failed
- "command not found" errors
- No LSP features available

**Diagnosis:**

Check if HLS is installed:

```bash
which haskell-language-server-wrapper
```

**Common Fixes:**

1. **Install via GHCup (recommended):**
   ```bash
   ghcup install hls
   ```

2. **Add GHCup to PATH** - Add to shell config (`.bashrc`, `.zshrc`):
   ```bash
   export PATH="$HOME/.ghcup/bin:$PATH"
   ```

3. **Verify installation location** - Check common paths:
   - `~/.ghcup/bin/haskell-language-server-wrapper`
   - `~/.local/bin/haskell-language-server-wrapper`
   - `~/.cabal/bin/haskell-language-server-wrapper`

4. **Restart Claude Code** after PATH changes

### Level 2: HLS Started But Unresponsive

**Symptoms:**
- `/hls:status` PATH check passes but startup test fails
- HLS process visible but no LSP responses
- Long delays before features appear

**Diagnosis:**

Check if HLS process is running:

```bash
ps aux | grep haskell-language-server
```

Check system resources:

```bash
# Memory usage
free -h

# CPU usage
top -b -n 1 | head -20
```

**Common Fixes:**

1. **Wait for initial indexing** - HLS may take several minutes on first load for large projects

2. **Check GHC version compatibility** - HLS version must match project's GHC:
   ```bash
   haskell-language-server-wrapper --version
   ghc --version
   ```
   Consult `references/hls-docs.xml` for the GHC version support matrix.

3. **Kill stuck processes:**
   ```bash
   pkill -f haskell-language-server
   ```

4. **Check available memory** - HLS requires significant RAM for large projects. Consider:
   - Closing other applications
   - Increasing swap space
   - Using a smaller project subset

5. **Review HLS logs** - Enable debug logging:
   ```bash
   claude --enable-lsp-logging
   ```
   Logs written to `~/.claude/debug/`

### Level 3: HLS Running But LSP Commands Failing

**Symptoms:**
- `/hls:status` all checks pass
- Some features work but others don't
- Intermittent errors or partial responses

**Diagnosis:**

Test specific LSP features manually. Check project configuration:

```bash
# Look for hie.yaml
ls -la hie.yaml

# Check cabal/stack files
ls -la *.cabal cabal.project stack.yaml 2>/dev/null
```

**Common Fixes:**

1. **Verify project builds** - HLS requires a buildable project:
   ```bash
   cabal build    # or
   stack build
   ```
   Fix any compilation errors first.

2. **Check hie.yaml configuration** - For multi-component projects, HLS needs to know which component each file belongs to. Generate implicit config:
   ```bash
   gen-hie > hie.yaml
   ```
   See `references/hls-docs.xml` for hie.yaml configuration details.

3. **Cradle errors** - If HLS reports cradle loading failures:
   - Ensure `cabal.project` or `stack.yaml` exists at project root
   - Run `cabal update` to refresh package index
   - Check for syntax errors in cabal files

4. **Enable verbose logging** for detailed diagnostics:
   ```bash
   claude --enable-lsp-logging
   ```
   Check `~/.claude/debug/` for HLS communication logs.

5. **Plugin-specific issues** - Some HLS plugins may fail independently. Consult `references/hls-docs.xml` for plugin configuration.

## Platform-Specific Notes

### Windows

- Use `where` instead of `which` for PATH checks
- PATH separator is `;` not `:`
- Common install location: `%APPDATA%\ghcup\bin`

### macOS

- GHCup installs to `~/.ghcup/bin`
- May need to allow in System Preferences > Security if blocked

### Linux

- GHCup installs to `~/.ghcup/bin`
- Ensure glibc compatibility for prebuilt binaries

## When to Consult Reference Documentation

For detailed information beyond this troubleshooting guide:

- **HLS configuration and features**: See `references/hls-docs.xml`
- **GHC version issues and compiler errors**: See `references/ghc-user.xml`
- **Cabal project setup and build issues**: See `references/cabal-docs.xml`

These references contain comprehensive documentation for complex issues not covered here.

## Summary Checklist

When HLS isn't working:

1. Run `/hls:status` for quick diagnosis
2. Level 1: Check PATH and installation
3. Level 2: Check process state and resources
4. Level 3: Check project configuration and builds
5. Enable `--enable-lsp-logging` for detailed debugging
6. Consult reference docs for complex issues
