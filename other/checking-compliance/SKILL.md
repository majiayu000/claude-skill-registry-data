---
name: checking-compliance
description: Generates compliance requirements from CE/FCC/UL standards for a device description. Use when starting a new embedded product, checking regulatory compliance, or generating initial SYS-REQ entries from applicable directives.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Write, WebSearch, WebFetch
  argument-hint: [device-description]
  stability: stable
  content-hash: sha256:70309f2eb68a0ceeef78777b3d23182c63a63ac3a4828b5278c407df0158ff83
  last-verified-cc-version: 1.0.34
---

# Compliance Requirements Generation

**Target**: $ARGUMENTS

Generate a compliance checklist and initial requirements file from applicable regulatory standards based on the device description.

## References (MUST READ)

Read these before proceeding:

- `references/compliance-standards.md` — Applicable directives, standards, and their scope
- `references/requirement-hierarchy.md` — SYS-REQ → PRD-REQ → SW-REQ ID conventions

## Workflow

1. **Parse device description** — Identify device type, markets (EU/US/both), wireless capability, power source, intended use
2. **Select applicable directives:**
   - EU: LVD (2014/35/EU) + EMC (2014/30/EU) + RED (2014/53/EU if wireless) + RoHS + REACH
   - US: UL 62368-1 + FCC Part 15 (+ Part 18 if ISM)
3. **WebSearch** for latest standard revisions if unsure about current edition
4. **Generate compliance checklist** at `docs/compliance-checklist.md` with:
   - Each applicable directive/standard
   - Specific clauses relevant to the device type
   - Test requirements (pre-compliance and certification)
5. **Generate requirements file** at `docs/requirements.md` with SYS-REQ entries:
   - One SYS-REQ per applicable standard clause
   - Include norm reference in each entry (e.g., `SYS-REQ-001: EN 55032 Class B conducted emission limits`)
6. **Output next steps** — Explain how to break SYS-REQ into PRD-REQ and SW-REQ, then use `implementing-firmware`

## Output Format

### Compliance Checklist

```markdown
# Compliance Checklist: <Device Name>

## Markets: <EU / US / Both>

### EU Directives
- [ ] LVD 2014/35/EU — IEC 62368-1:2023
  - Clause 5.4: Electrically-caused fire
  - Clause 6.3: Electric shock
- [ ] EMC 2014/30/EU — EN 55032:2015+A1:2020
  ...
```

### Requirements File

```markdown
# Requirements: <Device Name>

## System Requirements (SYS-REQ)

| ID | Description | Norm Reference | Status |
|----|-------------|----------------|--------|
| SYS-REQ-001 | Device shall meet EN 55032 Class B conducted emission limits | EN 55032:2015+A1:2020 §5 | open |
```

## Rules

- Always include norm version numbers — never reference a standard without its edition
- When in doubt about applicability, include the standard and note it as "to be confirmed"
- Separate safety (LVD/UL) from EMC from environmental (RoHS/REACH) requirements
- Do NOT generate PRD-REQ or SW-REQ — that is the user's refinement step
