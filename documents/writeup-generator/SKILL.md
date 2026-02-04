---
name: writeup-generator
description: Generate comprehensive CTF writeups as blog articles. Use when solving a challenge, documenting solutions, or when /writeup command is invoked.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# CTF Writeup Generator

Generate comprehensive, blog-quality writeups for solved CTF challenges.

## When to Use

- After solving a CTF challenge
- When `/writeup` command is invoked
- When user asks to document a solution

## Output Location

**CRITICAL: Save writeup as `README.md` in the CURRENT WORKING DIRECTORY.**

The current working directory should be the challenge directory, e.g.:
- `challenges/alpacahack/daily/2024-12-14_challenge-name/README.md`
- `challenges/picoctf/2024/challenge-name/README.md`
- `challenges/hackthebox/challenges/pwn/challenge-name/README.md`

**DO NOT save to:**
- Repository root
- `writeups/` directory
- Any other location

```
challenges/platform/event/challenge-name/   ← CURRENT DIRECTORY
├── README.md      # ← CREATE THIS HERE (tracked)
├── solve.py       # Solution script (tracked)
├── dist/          # Challenge files (ignored)
└── work/          # Working files (ignored)
```

## CRITICAL: Use the Template

**You MUST use the template at [templates/writeup.md](templates/writeup.md).**

1. Read the template file first
2. Fill in EVERY section completely
3. Do NOT skip any section
4. Do NOT abbreviate content

## Required Sections Checklist

Every writeup MUST include ALL of these sections with substantive content:

| Section | Required Content |
|---------|------------------|
| Title | `# [Category] Challenge Name` with one-liner |
| Overview | Complete table with all 6 fields filled |
| Problem Statement | Original description + files + connection info |
| TL;DR | 3-5 bullet points summarizing the solution |
| Background Knowledge | Explain concepts beginners need to understand |
| Solution Step 1 | Initial reconnaissance with commands and output |
| Solution Step 2 | Vulnerability analysis with code snippets |
| Solution Step 3 | Exploit development with full commented code |
| Solution Step 4 | Flag capture with actual output |
| Tools Used | Table listing all tools and their purpose |
| Lessons Learned | What I Learned + Mistakes Made + Future Improvements |
| References | Links to resources consulted |
| Tags | Relevant tags for searchability |

## Quality Requirements

### Code Blocks
- Include ALL relevant code with syntax highlighting
- Add comments explaining each step
- Show actual command output where relevant

### Background Knowledge
- Target readers who are learning
- Explain concepts, don't just name them
- Include examples where helpful

### Solution Steps
- Use numbered steps with descriptive titles
- Explain the "why" not just the "what"
- Include failed attempts if they provide learning value

### Lessons Learned
- Be honest about difficulties encountered
- Focus on personal growth and learning
- Reference resources for further study

## Instructions

1. **Read the template**: `templates/writeup.md`
2. **Gather information**:
   - Read solve scripts in the challenge directory
   - Check `dist/` for challenge files
   - Check `work/` for notes and debug output
3. **Write the writeup**:
   - Copy template structure exactly
   - Fill in every section with detailed content
   - Include all code with comments
4. **Verify completeness**:
   - Check every section has substantive content
   - Verify code is syntax-highlighted
   - Ensure tags are relevant

## Format Specification

For detailed formatting rules, see [format.md](format.md).
