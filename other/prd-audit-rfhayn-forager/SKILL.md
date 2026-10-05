---
name: prd-audit
description: Audit a PRD against the current codebase before implementation. Verifies entity names, property names, and API signatures are still accurate. TRIGGER when the user says "audit the PRD", "check the PRD", "is the PRD still accurate", or when starting implementation of a PRD that is more than 2 weeks old.
argument-hint: <path to PRD>
---

# PRD Freshness Audit

**PRD to audit**: $ARGUMENTS

If a PRD is >2 weeks old, it may reference names, properties, or APIs that have changed. This audit verifies accuracy before implementation.

## Step 1: Read the PRD

Read the specified PRD file completely.

## Step 2: API/Interface Verification

For each function, method, or API referenced in the PRD:
- Search the actual source file for the signature
- Verify parameter names, types, and return values match
- Check if the function still exists or was renamed/removed

### Step 3: Entity Verification (Core Data)

For each Core Data entity referenced in the PRD:
- Search `Models/<EntityName>+CoreDataProperties.swift` for actual property names and types
- Compare with what the PRD describes
- Flag any mismatches

## Step 4: File Structure Verification

For each file or module referenced in the PRD:
- Verify the file exists at the stated path
- Check if the structure matches the PRD description
- Note any new or removed files since the PRD was written

### Step 5: Save Count Verification

Count the number of `context.save()` calls described in the PRD flow and compare with the actual service implementation. Mismatched save counts indicate architectural drift.

## Step 6: Report

```markdown
## PRD Audit: [PRD Name]

### PRD Age
- Created: [date]
- Last updated: [date]
- Age: [days]

### Entity Accuracy
- [Entity]: [MATCH / MISMATCH — details]

### API Accuracy
- [Module.function()]: [MATCH / MISMATCH — details]

### File Accuracy
- [FileName]: [MATCH / MISMATCH — details]

### Save Count Accuracy
- PRD describes: [N] saves
- Actual code: [N] saves
- [MATCH / MISMATCH]

### Recommended PRD Updates
- [List of specific corrections needed]
```
