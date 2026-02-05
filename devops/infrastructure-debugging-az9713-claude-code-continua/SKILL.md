---
name: infrastructure-debugging
description: Troubleshooting dependencies, installations, environment issues, and platform-specific problems. Use when facing npm/pip/package errors, installation failures, environment setup issues, or platform compatibility problems.
---

# Infrastructure Debugging

## Dependency Resolution Strategy

### When Facing Package Errors

1. **Read the full error**: Scroll up to find the root cause, not just the final message
2. **Check version compatibility**: Many issues stem from version mismatches
3. **Clear caches first**: `npm cache clean --force` or `pip cache purge`
4. **Try fresh install**: Delete lock files and node_modules/venv, reinstall
5. **Check peer dependencies**: Especially for React, TypeScript, and build tools

### Common Package Manager Issues

**npm/yarn/pnpm**:
- `ERESOLVE` errors: Try `--legacy-peer-deps` or update conflicting packages
- `EACCES` permission errors: Don't use sudo, fix npm permissions instead
- Phantom dependencies: Use `pnpm` for stricter resolution

**pip/poetry/uv**:
- Version conflicts: Use virtual environments, always
- Build failures: Check for missing system dependencies (gcc, python-dev)
- Wheel issues: Try `--no-binary :all:` or update pip

## Environment Setup

### Best Practices

1. **Isolate environments**: Use venv, nvm, containers
2. **Document versions**: Pin exact versions for reproducibility
3. **Check PATH**: Many issues come from wrong binary being used
4. **Verify installation**: Test imports/commands after installing

### Platform-Specific Issues

**Windows**:
- Path length limits (260 chars): Enable long paths or use shorter paths
- Line endings: Configure git to handle CRLF/LF properly
- Native modules: May need Visual Studio Build Tools
- WSL vs native: Know which environment you're targeting

**macOS**:
- Xcode Command Line Tools required for many packages
- Homebrew vs system Python: Be explicit about which
- M1/M2 ARM: Some packages need Rosetta or ARM builds

**Linux**:
- Missing system dependencies: Check package manager (apt, yum, etc.)
- Permission issues: Avoid sudo for user packages
- Library paths: Check LD_LIBRARY_PATH if linking fails

## Troubleshooting Checklist

1. [ ] What exact error message?
2. [ ] What OS and version?
3. [ ] What package manager and version?
4. [ ] What Node/Python/runtime version?
5. [ ] Is this a fresh install or upgrade?
6. [ ] What changed recently?

## Accumulated Learnings

See [learnings.md](learnings.md) for session-learned insights about infrastructure issues.
