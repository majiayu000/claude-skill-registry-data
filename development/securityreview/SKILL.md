---
name: security/review
description: Security Code Review security skill
---

# Security Code Review

Systematic checklist for reviewing C code for security vulnerabilities.

## Review Checklist

**Memory:**
- [ ] All array accesses bounds-checked
- [ ] Integer overflow checked before allocation/indexing
- [ ] No use-after-free potential
- [ ] Strings null-terminated after operations

**Input:**
- [ ] All external input validated at trust boundary
- [ ] Path inputs canonicalized and checked
- [ ] No user data in format strings
- [ ] Lengths validated before use

**Functions:**
- [ ] No banned functions (strcpy, sprintf, gets, etc.)
- [ ] Buffer sizes passed to all string operations
- [ ] Return values checked

**Secrets:**
- [ ] No credentials in logs or error messages
- [ ] Config file permissions verified
- [ ] Secrets scrubbed from memory when done

**Files:**
- [ ] No TOCTOU races (access then open)
- [ ] Symlinks handled safely (O_NOFOLLOW)
- [ ] Temp files use mkstemp

**Grep for red flags:**
```bash
grep -rn 'strcpy\|sprintf\|gets\|strcat\|mktemp' src/
grep -rn 'printf.*%s.*user\|system(\|popen(' src/
```
