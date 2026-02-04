---
name: reporting-standards
description: Standards for security documentation and writeups
---

# Reporting Standards

## CTF Challenge Reports

### README.md (Simple Explanation)

Write for accessibility - a motivated high school student should understand.

```markdown
# Challenge Name

## The Bug

[1-2 sentences: What's wrong with the program?]

Example: "The program uses `gets()` to read user input into a small buffer.
This function doesn't check how much data you're giving it, so you can
write past the end of the buffer."

## The Exploit

[Step-by-step, plain English]

1. First, I send a lot of 'A' characters to find out how many it takes
   to crash the program (72 bytes)
2. After the crash point, I put the address of a function that prints
   the flag
3. When the function returns, instead of going back to where it was
   called from, it goes to the flag-printing function

## Key Concepts

- **Buffer Overflow**: Writing more data than a buffer can hold
- **Return Address**: Where a function goes when it's done
- **ROP**: Using existing code pieces to do what you want
```

### REPORT.md (Technical Writeup)

Detailed enough that another security professional could reproduce.

```markdown
# Challenge: [Name]
**Category**: Binary Exploitation
**Points**: XX
**Solves**: XX

## Summary

[One paragraph technical summary]

## Analysis

### Binary Properties
| Property | Value |
|----------|-------|
| Arch | x86-64 |
| NX | Enabled |
| Canary | Disabled |
| PIE | Disabled |
| RELRO | Partial |

### Vulnerability

- **Type**: <vulnerability_type>
- **Location**: <function_name> at <address>
- **Trigger**: <how_to_trigger>

### Relevant Addresses
| Symbol | Address |
|--------|---------|
| <function_name> | <address> |
| <gadget_name> | <address> |

## Exploitation

### Strategy
1. <step_1>
2. <step_2>

### Payload Structure
```
[padding: <offset> bytes][<gadgets/addresses>]
```

### Exploit Code
```python
# Include working exploit or link to file
```

## Flag
`<flag_format>`

## Mitigations

This vulnerability could be prevented by:
- Using `fgets()` instead of `gets()`
- Enabling stack canaries
- Address space layout randomization (ASLR)
```

## Malware Analysis Reports

### SUMMARY.md Structure

```markdown
# Malware Analysis: [Sample Name]

## Executive Summary

[2-3 sentences for non-technical readers]
- What it does
- How dangerous it is
- Key finding

## Sample Information

| Property | Value |
|----------|-------|
| Filename | sample.exe |
| MD5 | abc123... |
| SHA256 | def456... |
| File Type | PE32 executable |
| Size | 45,056 bytes |

## Behavioral Analysis

### Execution Flow
1. [Step 1]
2. [Step 2]
3. ...

### Capabilities
- [ ] Persistence
- [ ] Data exfiltration
- [ ] Lateral movement
- [ ] C2 communication

### Network Indicators
| Type | Value | Purpose |
|------|-------|---------|
| IP | x.x.x.x | C2 server |

### Host Indicators
| Type | Value | Purpose |
|------|-------|---------|
| File | /path/file | Dropped payload |

## Technical Details

### Encryption/Obfuscation
[Details on crypto used]

### C2 Protocol
[Communication format and protocol]

### Anti-Analysis
[Evasion techniques observed]

## Recommendations

1. [Detection suggestion]
2. [Mitigation suggestion]

## Appendix

### YARA Rule
```yara
rule SampleMalware {
    strings:
        $s1 = "unique_string"
    condition:
        all of them
}
```

### Decryption Script
[Link to script]
```

## STATUS.md (Progress Tracking)

Update throughout analysis:

```markdown
# Status

## Working
- [x] <completed_step>
- [x] <completed_step>

## Not Working
- [ ] <blocked_item> - <reason>

## Next Steps
1. <next_action>
2. <next_action>

## Notes
- <key_finding>: <value>
- <key_finding>: <value>

## Timeline
- <time> - <milestone>
```
