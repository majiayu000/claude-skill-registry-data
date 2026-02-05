---
name: detecting-privilege-escalation
description: Detects privilege escalation vulnerabilities including setuid/setgid abuse, permission check bypasses, and unsafe privilege management. Use when analyzing setuid binaries, permission checks, or investigating privilege escalation paths.
---

# Privilege Escalation Detection

## Detection Workflow

1. **Identify privileged operations**: Find setuid/setgid binaries, locate privilege checks, identify file operations with elevated privileges, map privilege boundaries
2. **Analyze permission model**: Understand intended permission model, identify all privilege boundaries, map privilege escalation paths, assess access control mechanisms
3. **Check validation**: Verify permission checks are correct, look for race conditions, assess validation completeness, identify TOCTOU issues
4. **Assess exploitability**: Can attacker bypass checks? Is there a usable escalation path? What's the impact of successful escalation?

## Key Patterns

- Setuid/setgid binaries: binaries with setuid/setgid bits set, unsafe operations in privileged binaries, environment variable usage, path traversal vulnerabilities
- Insecure permission checks: race conditions in permission checks, missing privilege validation, TOCTOU in file operations, weak access control implementations
- Environment-based escalation: environment variable manipulation, LD_PRELOAD/DT_RPATH abuse, PATH manipulation, IFS exploitation
- Resource manipulation: symlink attacks, hard link manipulation, file descriptor manipulation, /proc filesystem abuse

## Output Format

Report with: id, type, subtype, severity, confidence, location, binary_info (path, setuid, setgid, owner), vulnerability, attack_path, exploitable, impact, mitigation.

## Severity Guidelines

- **CRITICAL**: Direct path to root/admin access
- **HIGH**: Escalation to lower privileged user
- **MEDIUM**: Limited privilege escalation
- **LOW**: Information disclosure about privileges

## See Also

- `patterns.md` - Detailed detection patterns and exploitation scenarios
- `examples.md` - Example analysis cases and code samples
- `references.md` - CWE references and mitigation strategies