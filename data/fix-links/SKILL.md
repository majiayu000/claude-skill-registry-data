---
name: vault-fix-links
description: Find and repair broken wikilinks in vault. Triggers when user mentions "fix links", "broken links", "repair vault", "fix broken links".
auto_trigger: true
trigger_keywords:
  - "fix links"
  - "broken links"
  - "repair vault"
  - "fix broken links"
  - "repair links"
  - "find broken links"
  - "broken wikilinks"
  - "fix wikilinks"
  - "invalid links"
  - "dead links"
  - "link errors"
  - "repair connections"
  - "link problems"
  - "fix references"
  - "bad links"
allowed-tools: mcp__flywheel__find_broken_links, Task, TodoWrite
---

# Fix Broken Links

Preview broken wikilinks and spawn autonomous repair agent.

## When to Use

Invoke when you want to:
- Find all broken wikilinks in vault
- Preview what's broken and why
- Repair broken links automatically
- Improve vault link health

## Process

### 1. Find Broken Links
Call `mcp__flywheel__find_broken_links` to retrieve all broken wikilinks.

### 2. Analyze Break Patterns
Categorize broken links by type:

**Missing Notes** (create candidates):
- `[[New Topic]]` → No file exists
- High confidence if referenced multiple times
- Suggest creating note

**Typos** (fuzzy match):
- `[[Databrics]]` → Did you mean `[[Databricks]]`?
- Use Levenshtein distance
- Auto-fix if confidence >90%

**Case Mismatches** (exact match different case):
- `[[databricks]]` → Exists as `[[Databricks]]`
- Auto-fix (safe)

**Moved Notes** (search by title):
- `[[Old Path/Note]]` → Now at `[[New Path/Note]]`
- Search vault for matching title
- Suggest update

### 3. Show Preview
Display first 20 broken links with categorization:

```
Broken Links Analysis
═══════════════════════════════════════════════
Found 200 broken links across 50 notes

📊 Breakdown by Type:
  • Missing Notes: 80 (40%)
  • Typos: 40 (20%)
  • Case Mismatches: 30 (15%)
  • Moved/Renamed: 50 (25%)

🔍 Sample (showing 20 of 200):

Missing Notes:
1. [[API Guide]] (15 references)
   → Mentioned in: Projects, Tech Docs
   → Suggestion: Create tech/guides/API.md

Typos:
2. [[Databrics]] → [[Databricks]] (confidence: 95%)
   → Auto-fixable

Case Mismatches:
3. [[azure]] → [[Azure]] (exact match)
   → Auto-fixable

═══════════════════════════════════════════════

💡 Recommendations:
  • Auto-fix: 50 links (high confidence >90%)
  • User review: 60 links (medium confidence 50-90%)
  • Manual fix: 90 links (low confidence <50%)

🤖 Spawn autonomous repair agent?
  • Will process all 200 broken links
  • Auto-fix high confidence (>90%)
  • Present choices for medium confidence (50-90%)
  • Skip low confidence (<50%)

Type 'yes' to spawn link-repair agent
```

### 4. User Decision
Ask user if they want to:
- **Option A**: Spawn agent for autonomous fixing
- **Option B**: See full list (export to note)
- **Option C**: Fix specific folder only
- **Option D**: Cancel (just wanted to see the damage)

## Confidence Scoring

```
Typo Detection (Levenshtein Distance):
- Distance 1: 98% confidence
- Distance 2: 85% confidence
- Distance 3+: <70% confidence

Case Mismatch:
- Exact title match: 100% confidence
- Always safe to auto-fix

Missing Note Analysis:
- Referenced 20+ times: High priority (suggest create)
- Referenced 5-19 times: Medium priority
- Referenced 1-4 times: Low priority (might be scratch)

Moved Note Detection:
- Title exact match: 95% confidence
- Title fuzzy match: 60-85% confidence
- Search by content similarity: <60% confidence
```

## Output Format

Always use the branded format:

```
Broken Links Analysis
═══════════════════════════════════════════════

[Analysis content]

═══════════════════════════════════════════════
```

## Six Gates Compliance

| Gate | Implementation |
|------|----------------|
| 1. Read Before Write | Finds all broken links via MCP before any fixes |
| 2. File Exists | Validates target notes exist for link suggestions |
| 3. Chain Validation | Agent verifies each fix before proceeding |
| 4. Mutation Confirmation | Shows preview, requires explicit "yes" to proceed |
| 5. Health Check | Uses MCP find_broken_links for vault access |
| 6. Post Validation | Agent reports what was fixed after completion |

## Safety

- **Non-destructive**: Only suggests, doesn't auto-apply
- **User approval**: Requires explicit "yes" to spawn agent
- **Preview first**: Always show what's broken before fixing
- **Backup**: Agent will backup before batch edits

## Performance

- **Discovery**: 5-10 seconds (find_broken_links MCP call)
- **Analysis**: 10-20 seconds (categorize links)
- **Preview**: Instant (show first 20)
- **Total**: ~30 seconds before agent spawn decision
