---
name: manage-concepts-db
description: Manage the concepts database - verify, add, update, and check for duplicates before modifying concepts. MANDATORY for all concept operations.
allowed-tools: Bash, Read, Edit, Write, Grep, Glob
---

# Manage Concepts Database

This skill provides workflows for working with the concepts SQLite database to prevent duplicates and maintain data quality.

## MANDATORY RULES

1. **ALWAYS verify before adding a new concept**
   - Run `npx tsx scripts/verify-concept.ts` BEFORE creating any new concept JSON file
   - Minimum 90% confidence that concept doesn't exist
   - If confidence ≥70%, manually review potential duplicates

2. **ALWAYS update database after concept changes**
   - After adding/editing concept JSON: run `npx tsx scripts/sync-concepts-db.ts`
   - Database must stay in sync with JSON files

3. **NEVER skip duplicate checks**
   - Even if you think it's unique, run verification
   - All checks are logged for audit trail

## Available Scripts

All scripts are TypeScript and should be invoked with `npx tsx`:

| Script                      | Purpose                                        | When to Use                         |
| --------------------------- | ---------------------------------------------- | ----------------------------------- |
| `init-concepts-db.ts`       | Initialize and populate database               | First time setup or rebuild         |
| `verify-concept.ts`         | Check if concept exists before adding          | BEFORE creating any new concept     |
| `sync-concepts-db.ts`       | Sync database with JSON files                  | AFTER adding/editing any concept    |
| `merge-duplicates.ts`       | Merge duplicate concepts                       | When duplicates confirmed           |
| `find-duplicates.ts`        | Scan all concepts for potential duplicates     | Periodic cleanup / data quality     |

## Workflow: Adding a New Concept

### Step 1: Verify Concept Doesn't Exist

```bash
npx tsx scripts/verify-concept.ts \
  --name "Concept Name" \
  --summary "Brief summary" \
  --aliases "Alias 1,Alias 2" \
  --related-notes "https://notes.dsebastien.net/..."
```

**Interpret Results:**
- **Confidence ≥90%**: STOP - concept likely exists. Review suggested duplicates.
- **Confidence 70-89%**: REVIEW manually. Check suggested duplicates. Decide if truly different.
- **Confidence <70%**: PROCEED with caution. Log decision reasoning.

### Step 2: If Approved, Create Concept JSON

Only proceed if confidence <90% OR you've manually verified it's unique.

Create `/home/dsebastien/wks/concept-cards/src/data/concepts/{id}.json` following schema in AGENTS.md.

### Step 3: Sync Database

```bash
npx tsx scripts/sync-concepts-db.ts
```

Verify concept was added to database successfully.

## Workflow: Updating an Existing Concept

### Step 1: Edit Concept JSON

Make changes to `/home/dsebastien/wks/concept-cards/src/data/concepts/{id}.json`

### Step 2: Sync Database

```bash
npx tsx scripts/sync-concepts-db.ts
```

Database will automatically update based on content hash change.

## Workflow: Merging Duplicates

### Step 1: Identify Duplicates

```bash
# Scan all concepts for duplicates
npx tsx scripts/find-duplicates.ts --threshold 80
```

### Step 2: Review and Decide

- Compare concepts side-by-side
- Decide which to keep (target) and which to merge (source)
- Choose merge strategy

### Step 3: Execute Merge

```bash
npx tsx scripts/merge-duplicates.ts \
  --source {source-id} \
  --target {target-id} \
  --strategy merge-fields
```

This will:
- Combine data from both concepts
- Update cross-references
- Delete source JSON file
- Update database

### Step 4: Sync Database

```bash
npx tsx scripts/sync-concepts-db.ts
```

### Step 5: Verify

```bash
# Check target concept exists
cat /home/dsebastien/wks/concept-cards/src/data/concepts/{target-id}.json

# Check source concept deleted
ls /home/dsebastien/wks/concept-cards/src/data/concepts/{source-id}.json  # should error
```

## Common Scenarios

### Scenario 1: User Asks to Add Concepts from MoC

1. For EACH concept to add:
   - Run `verify-concept.ts` with name and summary
   - If confidence <90%, proceed with creation
   - If confidence ≥90%, inform user of existing concept and ask if they want to update it instead
   - After creating concept, run `sync-concepts-db.ts`

2. Run final sync after all concepts added:
   ```bash
   npx tsx scripts/sync-concepts-db.ts
   ```

### Scenario 2: Bulk Import from Multiple MoCs

1. Create a temporary script that:
   - Reads each MoC note
   - For each potential concept, calls `verify-concept.ts`
   - Logs all HIGH confidence duplicates
   - Only creates LOW/MEDIUM confidence concepts
   - Outputs report of skipped duplicates

2. Review report with user
3. Manually handle high-confidence duplicates
4. Run final sync

### Scenario 3: User Reports Duplicate Concepts

1. Run similarity check:
   ```bash
   npx tsx scripts/verify-concept.ts --name "Concept Name" --summary "..."
   ```

2. If duplicates confirmed, merge:
   ```bash
   npx tsx scripts/merge-duplicates.ts --source {id1} --target {id2} --strategy merge-fields
   npx tsx scripts/sync-concepts-db.ts
   ```

## Database Maintenance

### Check Database Health

```bash
# View database stats
sqlite3 /home/dsebastien/wks/concept-cards/concepts.db "
  SELECT
    (SELECT COUNT(*) FROM concepts) as total_concepts,
    (SELECT COUNT(*) FROM concept_aliases) as total_aliases,
    (SELECT COUNT(*) FROM concept_tags) as total_tags,
    (SELECT COUNT(*) FROM duplicate_checks) as total_checks;
"
```

### Rebuild Database from JSON

If database gets corrupted or out of sync:

```bash
# Delete database
rm /home/dsebastien/wks/concept-cards/concepts.db

# Reinitialize
npx tsx scripts/init-concepts-db.ts
```

## Troubleshooting

**Issue**: verify-concept.ts shows false positives

**Solution**: Adjust similarity thresholds in script. Review and tune weights.

**Issue**: Database out of sync with JSON files

**Solution**: Run `npx tsx scripts/sync-concepts-db.ts`

**Issue**: Need to force-add concept despite high confidence match

**Solution**: Add `--force` flag to skip duplicate check (use sparingly, document why)

## Documentation References

- **Implementation plan**: `/home/dsebastien/wks/concept-cards/documentation/plans/sqlite-duplicate-detection-plan.md`
- **Database reference**: `/home/dsebastien/wks/concept-cards/documentation/plans/concepts-database.md`
- **AGENTS.md**: Complete concept schema and guidelines

## Key Principles

1. **Prevention over correction**: Always verify BEFORE creating
2. **Automatic sync**: Run sync after every change
3. **Audit trail**: All verification checks are logged
4. **Conservative thresholds**: 90%+ confidence = reject
5. **User control**: High-confidence matches require user decision

## Example: Complete Workflow

```bash
# 1. Verify concept doesn't exist
npx tsx scripts/verify-concept.ts \
  --name "Parkinson's Law" \
  --summary "Work expands to fill time available"

# Output shows: Confidence: 15% - No strong matches found. Safe to add.

# 2. Create concept JSON file
# (Create /home/dsebastien/wks/concept-cards/src/data/concepts/parkinsons-law.json)

# 3. Sync database
npx tsx scripts/sync-concepts-db.ts

# Output: ✓ Added parkinsons-law to database
```
