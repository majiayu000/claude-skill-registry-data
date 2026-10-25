---
name: skill-audit
tags: [skills, audit, duplicates, cleanup, meta]
version: 1.0.0
author: Feb
category: hermes
metadata:
  hermes:
    tags: [skills, audit, duplicates, cleanup, meta]
    platforms: [linux]
---

# Skill Audit

Systematic audit of all skills in `~/.hermes/skills/`. Produces a triage report with concrete actions.

## When to use

- User says "audit skill" / "cek duplikat skill" / "rapikan skill"
- After creating many skills (accumulated cruft)
- Before a skill consolidation session
- Periodically (monthly) to catch drift

## Audit procedure

### Step 1: Count and categorize

```bash
cd ~/.hermes/skills
echo "=== TOTAL SKILLS ==="

echo "=== CATEGORY COUNTS ==="
for d in */; do
  echo "$count $d"
done | sort -rn

echo "=== ROOT-LEVEL (uncategorized) ==="
```

### Step 2: Find duplicates by description similarity

```bash
# Extract descriptions and find near-matches
cd ~/.hermes/skills

# Find exact duplicate descriptions
cut -d'|' -f1 /tmp/skill_descs.txt | sort | uniq -d | while read d; do
  echo "DUPLICATE: $d"
  grep "$d" /tmp/skill_descs.txt
  echo
done
```

### Step 3: Find keyword overlaps

```bash
# Skills mentioning the same key terms (potential overlap)
for keyword in "9router" "qoder" "tokenharbor" "farm" "gateway" "provider"; do
  echo "=== $keyword ==="
  echo
done
```

### Step 4: Size audit (oversized skills)

```bash
echo "=== SKILLS >50KB ==="
```

Skills >50KB are candidates for:
- Splitting detailed sections into `references/*.md` files
- Trimming historical notes that are no longer relevant
- Extracting repeated patterns into a shared reference

### Step 5: Linked files audit

```bash
echo "=== SKILLS WITH 0 LINKED FILES ==="
  if [ -z "$lf" ]; then echo "  $d"; fi
done
```

Skills with 0 linked files aren't necessarily bad — conceptual skills don't need them. But skills with complex procedures should have reference files.

### Step 6: Stale skill detection

Check for:
- Skills referencing deleted providers/services (e.g., B.AI deleted from 9router)
- Skills with backup timestamps in names (`*-backup-*`)
- Skills not mentioned in any recent session (check via `session_search`)
- Skills with version dates >6 months old

```bash
# Find backup-named skills

# Find skills referencing potentially deleted services
```

### Step 7: Archive check

```bash
echo "=== ARCHIVED SKILLS ==="
ls .archive/ 2>/dev/null
```

Archived skills are preserved — don't delete them. They serve as pattern references.

## Triage report format

After running all checks, produce a report with:

```
## Duplicate Pairs (archive the weaker copy)
| Skill A | Skill B | Action | Reason |
|---------|---------|--------|--------|

## Oversized Skills (>50KB)
| Skill | Size | Recommendation |
|-------|------|----------------|

## Stale Skills
| Skill | Reason | Action |
|-------|--------|--------|

## Uncategorized
| Skill | Suggested Category |
|-------|---------------------|
```

## Merge procedure (when duplicates found)

2. Identify unique sections in each (not present in the other)
3. Identify unique linked files (references/scripts/templates)
4. Copy unique linked files from the duplicate to the canonical skill
5. Add a cross-reference note in the canonical skill's "Related skills" section
6. `mv` the duplicate to `.archive/` (NEVER delete — preserve for reference)
7. Verify the canonical skill still loads: `skill_view(name=<canonical>)`

## Pitfalls

1. **Never delete skills — always archive to `.archive/`.** Patterns and references may be needed later. Archived skills don't count against active skill loading.
2. **Check linked files before archiving.** The duplicate may have unique `references/`, `scripts/`, or `templates/` that the canonical skill doesn't. Copy those first.
3. **Some duplicates are intentional.** A thin skill in `automation/` and a detailed skill at root level may serve different audiences (e.g., `ai-gateway-key-farming` deep recon vs `mass-account-api-key-farm` generic playbook). Use judgment — don't auto-merge everything.
4. **`bai-api-key-farming` is kept despite B.AI being deleted from 9router.** The recon methodology (bundle reverse, Turnstile, SIWE) is reusable for any similar target. Mark with a "Provider deleted, methodology still relevant" note rather than archiving.
5. **Size alone isn't a problem.** `9router-ops` at 67KB is large because it documents a complex system. Don't trim just for size — trim when content is genuinely stale or duplicated within the same file.
6. **Run the audit BEFORE creating new skills.** You might find an existing skill already covers what you're about to create.

## Related skills

- `skill-management` — lifecycle management (create, update, archive, delete)
- `skill-anti-duplicate` — automated duplicate detection and merge
- `skill-auto-organize` — auto-categorize and trim oversized skills
- `skill-strengthen` — improve existing skills with missing pieces
- `skill-auto-create` — auto-generate skills from session patterns
