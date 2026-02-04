---
name: Updating genealogy data
description: Updates person records in the auntruth genealogy database (3,004 people across 10 lineages) while maintaining bidirectional relationship consistency. Use when the user asks to update birth/death dates, add marriages, add children, or modify biographical information for any person in the database.
---

# Updating Genealogy Data

## When to Use This Skill

Use this skill when the user requests:
- Update death/birth dates or locations
- Add or modify marriage information
- Add children to family records
- Update contact information (email, phone, address)
- Modify biographical details (occupation, notes)
- Any change to person records in the `data/people/` directory

**Do NOT use** for reading/browsing person data or generating new HTML pages.

## Critical Constraints

1. **Source of truth**: JSON files in `data/people/{lineage}/{person_id}.json`
2. **NEVER edit HTML**: Files in `docs/new/htm/L*/` are auto-generated (CI/CD regenerates them)
3. **No backup files**: Use git for version control - NEVER create .backup files
4. **Bidirectional consistency**: Relationships must match both directions (if A is spouse of B, B must be spouse of A)
5. **Always validate**: Run validation script after every update before committing

## Database Structure

- **3,004 people** across **10 lineages**
- **Person IDs**: Format `XF###` (e.g., XF100, XF2451)
- **Lineages**: Hagborg-Hansson (L1), Nelson (L2), Pringle-Hambley (L3), Lathrop-Lothropp (L4), Ward (L5), Selch-Weiss (L6), Stebbe (L7), Lentz (L8), Phoenix-Rogerson (L9), Other (L0)

For detailed schema, see `REFERENCE.md` in this skill directory.

## Standard Workflow (Copy-Paste Checklist)

For every update request, follow these steps:

```
☐ 1. UNDERSTAND REQUEST
     Parse what needs updating and identify person ID(s)

☐ 2. FIND PERSON FILES
     grep -r '"id": "XF###"' data/people/
     Identify all affected files (person + related records)

☐ 3. READ CURRENT DATA
     Read all affected JSON files
     Show user current values and confirm changes

☐ 4. MAKE UPDATES
     Edit JSON files with new values
     Update metadata.lastUpdated: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
     Ensure bidirectional consistency for relationships

☐ 5. VALIDATE
     python3 PRPs/scripts/both/validate_json_data.py --input data/people/{lineage}/{person_id}.json
     Fix any validation errors before proceeding

☐ 6. COMMIT JSON DATA ONLY
     git add data/people/{lineage}/*.json
     git commit -m "Update XF###: [description]"
     git push

     IMPORTANT: Do NOT regenerate HTML pages manually!
     GitHub Actions will automatically regenerate ALL HTML pages on push.

☐ 7. REPORT
     Show summary: files changed, validation status
     Explain: GitHub Actions will auto-regenerate HTML pages within 3-5 minutes
     Tell user to wait for the automated workflow to complete before checking the live site
```

## Common Update Patterns

### Death Date Update (1 file affected)
**User request**: "Update XF100 death date to December 31, 1920 in Winnipeg, MB"

**Fields to update**:
- `deathDate`: "1920-12-31"
- `deathLocation`: "Winnipeg, MB"
- `deceased`: true
- `metadata.lastUpdated`: current ISO timestamp

**Example**:
```json
{
  "id": "XF100",
  "deathDate": "1920-12-31",
  "deathLocation": "Winnipeg, MB",
  "deceased": true,
  "metadata": {
    "lastUpdated": "2025-10-21T15:30:00Z"
  }
}
```

### Add Marriage (2 files affected - both spouses)
**User request**: "Add marriage between XF100 and XF101 on June 20, 1875"

**Files to update**:
1. `data/people/{lineage}/XF100.json` - add XF101 to spouses array
2. `data/people/{lineage}/XF101.json` - add XF100 to spouses array

**Critical**: Both files must reference each other with identical marriage date.

**Example spouse entry**:
```json
{
  "spouses": [
    {
      "id": "XF101",
      "name": "Spouse Full Name",
      "url": "/auntruth/new/htm/L1/XF101.htm",
      "marriageDate": "1875-06-20"
    }
  ]
}
```

### Add Child (3 files affected - mother, father, child)
**User request**: "Add child XF106 (Anna, born 1876-03-15) to parents XF100 and XF101"

**Files to update**:
1. Mother's file - add to `children` array
2. Father's file - add to `children` array
3. Child's file - set `mother` and `father` references

**Child entry in parent's file**:
```json
{
  "children": [
    {
      "id": "XF106",
      "name": "Anna Full Name",
      "url": "/auntruth/new/htm/L1/XF106.htm",
      "birthDate": "1876-03-15"
    }
  ]
}
```

**Parent reference in child's file**:
```json
{
  "mother": {
    "id": "XF100",
    "name": "Mother Name",
    "url": "/auntruth/new/htm/L1/XF100.htm"
  },
  "father": {
    "id": "XF101",
    "name": "Father Name",
    "url": "/auntruth/new/htm/L1/XF101.htm"
  }
}
```

## Finding Records

**Find person by ID**:
```bash
grep -r '"id": "XF100"' data/people/
# Returns: data/people/Hagborg-Hansson/XF100.json
```

**Find person by name** (case-insensitive):
```bash
grep -ri '"name":.*"johanna"' data/people/
```

**Get lineage directory number** for URL construction:
- See `REFERENCE.md` for complete lineage mapping (L0-L9)

## Validation & Safety

**Always run after updates** (EXECUTE this script):
```bash
python3 PRPs/scripts/both/validate_json_data.py --input data/people/{lineage}/{person_id}.json
```

**Validation checks**:
- ✓ JSON syntax valid
- ✓ Required fields present (id, name, lineage)
- ✓ ID matches pattern XF\d+
- ✓ Arrays are properly formatted
- ✓ URLs follow correct pattern

**If validation fails**: Fix errors before committing. Do NOT proceed with invalid data.

## URL Construction Pattern

All person URLs follow this pattern:
```
/auntruth/new/htm/L{lineage_num}/{person_id}.htm
```

Example: Person XF100 in Hagborg-Hansson (L1) lineage:
```
/auntruth/new/htm/L1/XF100.htm
```

## Timestamp Generation

Always update `metadata.lastUpdated` with current ISO timestamp:
```bash
date -u +"%Y-%m-%dT%H:%M:%SZ"
```

## Error Recovery

If updates fail:
1. Check validation output for specific errors
2. Fix schema issues (missing required fields, wrong types)
3. Verify bidirectional relationships match
4. Re-run validation
5. If still failing, use `git checkout` to revert (NO .backup files)

## Post-Update - Automated Workflow

After successful `git push`:
1. GitHub Actions workflow triggers automatically
2. Validates all JSON data (30 seconds)
3. Regenerates ALL 3,004 HTML pages from JSON (2-3 minutes)
4. Auto-commits regenerated HTML back to repo
5. Deploys to GitHub Pages (1-2 minutes)

**Total time**: 3-5 minutes from push to live site update

**IMPORTANT**: User does NOT need to manually regenerate HTML pages!
The workflow handles everything automatically.
