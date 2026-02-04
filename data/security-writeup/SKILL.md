---
name: security-writeup
description: Document security research, CTF solutions, and malware analysis. Includes REPORT.md and STATUS.md templates.
---

# Security Writeup

Documentation standards for security research and CTF challenges.

## Document Types

| Document | Purpose | When to Create |
|----------|---------|----------------|
| STATUS.md | Progress tracking | Start of work, update throughout |
| REPORT.md | Technical writeup | After solution or significant progress |

## STATUS.md

Track progress for restartability. Update after:
- Starting work on a problem
- Finding key information (offsets, addresses)
- Failed attempts (document what didn't work!)
- Completing a phase (recon → analysis → exploit → docs)
- Session end

### Status Icons
- ✅ Solved
- 🔄 In Progress
- ❌ Not Started
- ⏸️ Blocked

## REPORT.md

Combine technical writeup with learning explanation.

### Required Sections
1. **Overview** - Accessible summary
2. **Binary Properties** - checksec output as table
3. **Vulnerability** - Type, location, root cause
4. **Exploitation** - Step-by-step approach
5. **Payload** - Structure and key addresses
6. **Flag** - The solution
7. **Mitigations** - How to prevent

### Writing Guidelines
- Technical enough to reproduce
- Accessible enough to learn from
- Include actual addresses and offsets
- Explain the "why" not just the "what"

## Multi-Problem Labs

For CTFs with multiple problems:

```
lab/
├── STATUS.md           # Overview of ALL problems
├── problem1/
│   ├── STATUS.md       # Detailed for this problem
│   ├── exploit.py
│   └── REPORT.md
└── problem2/
    └── ...
```

Root STATUS.md tracks overall progress; per-problem STATUS.md tracks details.

## Templates

- `templates/REPORT.md` - Full technical writeup
- `templates/STATUS.md` - Progress tracking
