---
name: redaction-and-cleanup
description: Use when user says "redact", "clean up for sharing", "remove sensitive info", "prepare for external", when sharing .forge/ artifacts with investors or external reviewers, when sanitizing documents before external publication, or when pricing/credentials/strategy must be removed before sharing.
---

# Redaction and Cleanup

## Overview

Prepare `.forge/` documents for external sharing by copying them to `.forge/redacted/` and replacing sensitive information with consistent placeholders. Original files are NEVER modified. The redaction manifest documents every change for internal reference.

## When to Use

- Sharing documents with investors, advisors, or partners
- Preparing materials for external review or cross-validation
- Publishing case studies or documentation based on internal artifacts
- Any situation where internal data must not leave the organization

## When NOT to Use

- Documents are already public — no redaction needed
- User wants to delete files — that's not redaction
- The sensitive data IS the deliverable (e.g., a security audit for the client)

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "I'll just manually remove the sensitive parts" | Manual redaction misses things. Automated scan + manifest catches more |
| "It's fine, the recipient is trusted" | Trust the person, redact the document. People forward things |
| "I'll edit the originals and restore later" | You won't. Original files must be untouched — copy first, always |
| "Only pricing needs redacting" | Credentials, internal metrics, employee names, strategy details — audit first |
| "A quick find-and-replace is enough" | Inconsistent placeholders leak information through correlation |

## Red Flags

- Original files modified in place (SAFETY VIOLATION — must copy first)
- Placeholder values are inconsistent (same entity gets different placeholders)
- Grep after redaction still finds sensitive terms
- Manifest is missing (no record of what was changed)
- Redaction categories not defined before scanning (ad-hoc misses patterns)

## SAFETY RULE

**NEVER modify original files in place.** All redaction happens on copies in `.forge/redacted/`. Original files in `.forge/` must remain untouched. If you are about to edit a file outside `.forge/redacted/`, STOP.

## Core Process

### Step 1: Define redaction categories

With the user, define what to redact and what to keep:

**Redact** (typical):
- Pricing, margins, unit economics
- API keys, credentials, connection strings
- Internal strategy, competitive positioning details
- Employee names, internal team structure
- Specific customer names (unless public case study)
- Internal metrics, revenue numbers

**Keep** (typical):
- Public pricing from competitors
- Architecture patterns and technology choices
- General cost categories (without specific numbers)
- Role titles (without names)
- Publicly available data

### Step 2: Define placeholder format

Use consistent, identifiable placeholders:
- Company names: `[COMPANY-A]`, `[COMPANY-B]` (consistent across all docs)
- Prices: `[PRICE-TIER-1]`, `[PRICE-TIER-2]`
- People: `[TEAM-MEMBER-1]`, `[TEAM-MEMBER-2]`
- Metrics: `[INTERNAL-METRIC]`
- Credentials: `[CREDENTIAL-REDACTED]`

Consistency rule: the same entity gets the same placeholder everywhere.

### Step 3: Scan all files

Scan every file in `.forge/` for matches against redaction categories. For each match, record:
- File path
- Line number
- Original content (summary, not full text)
- Redaction action (replace with which placeholder)

### Step 4: Generate manifest

Write `.forge/redaction-manifest.md`:
- Redaction categories defined
- Placeholder mapping (which entity → which placeholder)
- Per-file change list
- Total changes count

### Step 5: Copy and redact

1. Create `.forge/redacted/` directory
2. Copy all files from `.forge/` to `.forge/redacted/` (preserving structure)
3. Apply redactions to the copies only
4. Do NOT copy `.forge/redaction-manifest.md` to redacted/ (it contains the mapping)

### Step 6: Verify

Run grep on `.forge/redacted/` for every term in the redaction categories. Zero matches required. If any remain, fix and re-verify.

### Step 7: Sync check

If documents are updated later, the redacted copies are stale. Note in the manifest: "Redacted on [date]. If originals change, re-run redaction."

## Output

- `.forge/redaction-manifest.md` — what was redacted, placeholder mapping
- `.forge/redacted/*` — cleaned copies of all documents

## Verification

- [ ] Original files in `.forge/` are unchanged
- [ ] All files copied to `.forge/redacted/` before any edits
- [ ] Placeholders are consistent (same entity → same placeholder across all files)
- [ ] Grep confirms zero remaining matches for redacted terms in `.forge/redacted/`
- [ ] Manifest documents every change with file and line reference
- [ ] Redaction manifest is NOT copied to `.forge/redacted/`
- [ ] `.forge/redaction-manifest.md` written
