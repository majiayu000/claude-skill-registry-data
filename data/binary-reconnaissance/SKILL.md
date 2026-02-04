---
name: binary-reconnaissance
description: Initial reconnaissance on binaries including checksec, file analysis, strings, and symbols. First step for any new target.
---

# Binary Reconnaissance

First-look analysis of any new binary target. Run these checks before deeper analysis.

## Checklist

1. **File type**: `file target`
2. **Security mitigations**: `checksec target`
3. **Symbols**: `nm target` or `readelf -s target`
4. **Strings**: `strings target | grep -i flag\|win\|shell`
5. **Disassembly**: `objdump -M intel -d target > target.asm`

## Checksec Interpretation

| Protection | Enabled | Disabled | Bypass |
|------------|---------|----------|--------|
| NX | Can't execute shellcode on stack | Shellcode works | ROP, ret2libc |
| Canary | Stack smash detected | No protection | Leak canary, brute force |
| PIE | Addresses randomized | Fixed addresses | Leak code address |
| RELRO | GOT protected | GOT writable | Can't use GOT overwrite |

## Quick Wins to Look For

- Functions named `win`, `get_flag`, `shell`, `backdoor`
- Strings containing `flag`, `/bin/sh`, `cat flag`
- `system()` or `execve()` in PLT
- No canary + no PIE = likely simple overflow

## Output

Produce `context/binary-info.md` using the template.
