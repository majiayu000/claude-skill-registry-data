---
name: pubmed-field-validator
description: Validate PubMed search field tags against official NCBI documentation before implementing them. Use when adding new field tags to the query builder, debugging search queries, or verifying existing field tag implementations. Prevents invalid tags like [organism] and ensures compliance with NCBI PubMed standards.
---

# PubMed Field Tag Validator

## Overview

Provide systematic validation workflows for PubMed search field tags to ensure all implementations comply with official NCBI documentation. Prevent common mistakes like using long-form tags, non-existent fields, or deprecated syntax.

## When to Use This Skill

Use this skill when encountering:

- Implementing new field tags in `pubmed-client/src/pubmed/query/filters.rs`
- Adding search capabilities to the query builder system
- Debugging why PubMed API queries fail or return unexpected results
- Questions about whether a field tag exists or is valid
- Reviewing pull requests that add new search functionality
- Updating `CLAUDE.md` with validated or invalid field tags

## Validation Decision Tree

```
Is the task related to PubMed field tags?
├─ Yes → Continue with workflow below
└─ No → Exit skill

Are you implementing a NEW field tag?
├─ Yes → ⚠️ START WITH STEP 0 (Validation Workflow) - REQUIRED!
└─ No → Continue

Are you debugging a search query that fails?
├─ Yes → Jump to "Query Debugging Workflow"
└─ No → Continue

Are you auditing existing field tags?
├─ Yes → Jump to "Codebase Audit Workflow"
└─ No → Jump to "General Validation Workflow"
```

## ⚠️ Priority Checklist - Most Important Rules

Before implementing any field tag, verify these in order:

1. **Official Documentation Check** (Required for all new tags)
   - Have you checked https://pubmed.ncbi.nlm.nih.gov/help/#using-search-field-tags ?
   - → Jump to "Validation Workflow Step 1"

2. **Short Form Syntax** (90% of syntax errors)
   - Are you using `[ti]` not `[Title]`?
   - → Jump to "Validation Workflow Step 2"

3. **Known Invalid Tags** (Common mistakes)
   - Is this `[organism]` or other non-existent tag?
   - → Jump to "Invalid Tag Detection Workflow"

## Validation Workflow

**Scenario**: Need to validate a field tag before implementing it in code.

### Step 0: Check CLAUDE.md First

**Always check the project's CLAUDE.md** before proceeding to web validation - it contains pre-validated tags.

**Quick Reference Check**:

```bash
# From workspace root
grep -A 50 "Currently Validated Field Tags" CLAUDE.md
grep -A 20 "Invalid or Non-existent Tags" CLAUDE.md
```

**Decision Point**:

- Tag found in "Currently Validated Field Tags" → ✅ Safe to use, document in code
- Tag found in "Invalid or Non-existent Tags" → ❌ Do not use, suggest alternative
- Tag not found in either list → Continue to Step 1

### Step 1: Verify Against Official Documentation

**THE PRIMARY SOURCE** - All field tags must be verified against official NCBI documentation.

**Validation Process**:

1. **Use WebFetch to check official documentation**:
   ```
   WebFetch:
   - URL: https://pubmed.ncbi.nlm.nih.gov/help/#using-search-field-tags
   - Prompt: "Does the field tag [TAG_NAME] exist? If yes, provide its official description and examples."
   ```

2. **Check E-utilities documentation** (if needed for advanced usage):
   ```
   WebFetch:
   - URL: https://www.ncbi.nlm.nih.gov/books/NBK25499/
   - Prompt: "How should the field tag [TAG_NAME] be used in E-utilities API queries?"
   ```

3. **Run validation script** (for batch checking):
   ```bash
   python .claude/skills/pubmed-field-validator/scripts/validate_field_tags.py --tags "ti" "au" "organism"
   ```

**Expected Outcomes**:

- ✅ **Valid tag**: Documentation confirms existence and provides description
- ❌ **Invalid tag**: Not found in documentation
- ⚠️ **Deprecated tag**: Found but marked as deprecated (e.g., `[lang]` → use `[la]`)
- ❓ **Unknown tag**: Ambiguous or unclear from documentation

**If tag is valid**, proceed to Step 2.
**If tag is invalid**, jump to "Invalid Tag Detection Workflow".
**If tag is deprecated**, note the recommended alternative and proceed to Step 2.
**If tag is unknown**, request additional clarification from user before proceeding.

### Step 2: Verify Syntax Rules

**PubMed field tags must follow specific syntax conventions.**

**Syntax Checklist**:

- [ ] Tag uses **short form** (e.g., `[ti]` NOT `[Title]`)
- [ ] Tag is **lowercase** (standard convention)
- [ ] Tag appears **after** search term (e.g., `cancer[ti]` NOT `[ti]cancer`)
- [ ] For phrases, use **quotes** (e.g., `"breast cancer"[ti]`)
- [ ] No **spaces** before brackets (e.g., `cancer[ti]` NOT `cancer [ti]`)

**Common Syntax Errors**:

```rust
// ❌ WRONG - Long form not supported
query.title("Title")

// ✅ CORRECT - Short form
query.title("ti")

// ❌ WRONG - Uppercase
query.filter("CANCER[TI]")

// ✅ CORRECT - Lowercase
query.filter("cancer[ti]")
```

**If syntax is correct**, proceed to Step 3.
**If syntax is incorrect**, fix and re-validate.

### Step 3: Update Documentation

**After validating a field tag, update project documentation to prevent re-validation.**

**Update CLAUDE.md**:

1. **For valid tags**, add to "Currently Validated Field Tags" section:
   ```markdown
   - `[TAG]` - Description from official docs
   ```

2. **For invalid tags**, add to "Invalid or Non-existent Tags" section:
   ```markdown
   - `[TAG]` - Does not exist, use [ALTERNATIVE] instead
   ```

3. **For deprecated tags**, note the alternative:
   ```markdown
   - `[TAG]` - Deprecated, use [ALTERNATIVE] instead
   ```

**Example Edit**:

```markdown
### Currently Validated Field Tags

The following field tags have been verified against NCBI documentation:

- `[ti]` - Title
- `[au]` - Author

* `[gr]` - Grant Number # ← Add newly validated tag
```

### Step 4: Implement in Code

**Only after validation, implement the field tag in the appropriate module.**

**Implementation Locations**:

- **Basic filters**: `pubmed-client/src/pubmed/query/filters.rs`
- **Advanced filters**: `pubmed-client/src/pubmed/query/advanced.rs`
- **Date filters**: `pubmed-client/src/pubmed/query/dates.rs`

**Implementation Example**:

````rust
impl SearchQuery {
    /// Search by grant number.
    ///
    /// Uses the `[gr]` field tag.
    ///
    /// # Example
    /// ```
    /// use pubmed_client::pubmed::query::SearchQuery;
    ///
    /// let query = SearchQuery::new()
    ///     .grant_number("R01CA123456")
    ///     .build();
    /// ```
    pub fn grant_number(mut self, grant: &str) -> Self {
        self.add_term(&format!("{}[gr]", grant));
        self
    }
}
````

**Implementation Checklist**:

- [ ] Method name is clear and descriptive
- [ ] Documentation includes field tag reference (e.g., "Uses the `[gr]` field tag")
- [ ] Example usage provided in doc comment
- [ ] Field tag syntax is correct
- [ ] Link to official documentation in comments (optional but recommended)

## Invalid Tag Detection Workflow

**Scenario**: Tag is not found in official documentation or is known to be invalid.

### Step 1: Identify the Issue

**Common invalid tags and why they don't work:**

| Invalid Tag  | Why It Fails            | Recommended Alternative              |
| ------------ | ----------------------- | ------------------------------------ |
| `[organism]` | Not a field tag         | Use MeSH terms: `"Homo sapiens"[mh]` |
| `[Organism]` | Long form not supported | Use MeSH terms: `"Homo sapiens"[mh]` |
| `[Title]`    | Long form not supported | Use short form: `[ti]`               |
| `[Author]`   | Long form not supported | Use short form: `[au]`               |
| `[keyword]`  | Not a field tag         | Use text word search: `[tw]`         |
| `[subject]`  | Not a field tag         | Use MeSH terms: `[mh]`               |

### Step 2: Suggest Alternative

**Based on user intent, recommend the appropriate valid tag:**

**For organism searches**:

```rust
// ❌ WRONG - [organism] does not exist
query.filter("Homo sapiens[organism]")

// ✅ CORRECT - Use MeSH terms
query.mesh_term("Homo sapiens")
// Generates: "Homo sapiens"[mh]
```

**For subject/topic searches**:

```rust
// ❌ WRONG - [subject] does not exist
query.filter("cancer[subject]")

// ✅ CORRECT - Use MeSH terms
query.mesh_term("Neoplasms")
// Generates: "Neoplasms"[mh]
```

**For general text searches**:

```rust
// ❌ WRONG - [keyword] does not exist
query.filter("therapy[keyword]")

// ✅ CORRECT - Use text word search
query.text_word("therapy")
// Generates: therapy[tw]
```

### Step 3: Update Invalid Tags List

**Add the invalid tag to CLAUDE.md** to prevent future attempts:

```markdown
### Invalid or Non-existent Tags

These tags do NOT exist in PubMed and should not be used:

- `[organism]` - Use MeSH terms with `[mh]` instead

* `[keyword]` - Use text word search `[tw]` instead # ← Add newly discovered invalid tag
```

**Also update** `scripts/validate_field_tags.py` INVALID_FIELD_TAGS dictionary:

```python
INVALID_FIELD_TAGS = {
    "organism": "Use MeSH terms with [mh] instead",
+   "keyword": "Use text word search [tw] instead",  # ← Add to script
}
```

## Query Debugging Workflow

**Scenario**: PubMed API query fails or returns unexpected results.

### Step 1: Extract Field Tags from Query

**Identify all field tags used in the failing query.**

**Manual Inspection**:

```rust
// Example failing query
let query = SearchQuery::new()
    .title("cancer")
    .author("Smith J")
    .filter("therapy[unknown_tag]")  // ← Suspicious
    .build();
```

**Automatic Scanning** (if query is in code):

```bash
# From workspace root
python .claude/skills/pubmed-field-validator/scripts/validate_field_tags.py \
    --scan pubmed-client/src/pubmed/query/
```

### Step 2: Validate Each Tag

**Run validation for all extracted tags**:

```bash
python .claude/skills/pubmed-field-validator/scripts/validate_field_tags.py \
    --tags "ti" "au" "unknown_tag"
```

**Review output** for invalid, deprecated, or unknown tags.

### Step 3: Fix Invalid Tags

**Replace invalid tags with correct alternatives**:

```rust
// ❌ BEFORE - Using invalid tag
.filter("therapy[keyword]")

// ✅ AFTER - Using valid tag
.text_word("therapy")  // Generates: therapy[tw]
```

### Step 4: Test with Real API

**After fixing, test the corrected query**:

```bash
# Run integration test with real API
cd pubmed-client
PUBMED_REAL_API_TESTS=1 cargo test --features integration-tests --test pubmed_api_tests

# Or test manually via CLI
cargo run -p pubmed-cli -- search "cancer[ti] AND therapy[tw]"
```

**Verify**:

- Query executes without errors
- Results match expected criteria
- No NCBI API error messages

## Codebase Audit Workflow

**Scenario**: Review all field tags in the codebase for correctness.

### Step 1: Scan Codebase for Field Tags

**Use the validation script to find all tags**:

```bash
# From workspace root
python .claude/skills/pubmed-field-validator/scripts/validate_field_tags.py \
    --scan pubmed-client/src/
```

**Output shows**:

- All field tags found in source code
- Validation status for each tag
- Suggestions for fixing invalid tags

### Step 2: Review Unknown Tags

**For any tags marked "unknown"**:

1. Check if it's a typo or intentional
2. Validate against official documentation (Step 1 of Validation Workflow)
3. Update CLAUDE.md with the result

### Step 3: Update Test Data

**Ensure test queries use only valid tags**:

```bash
# Scan test files specifically
python .claude/skills/pubmed-field-validator/scripts/validate_field_tags.py \
    --scan pubmed-client/tests/
```

### Step 4: Generate Audit Report

**Document findings for code review or PR**:

```markdown
# PubMed Field Tag Audit Report

## Valid Tags Found: XX

- [ti], [au], [mh], ...

## Invalid Tags Found: XX

- [organism] → Should use [mh]
- [keyword] → Should use [tw]

## Unknown Tags: XX

- [xyz] → Needs validation

## Recommendations:

1. Replace invalid tags in filters.rs:123
2. Update test_queries.rs:456 with valid syntax
3. Add validated tags to CLAUDE.md
```

## Quick Reference: Common Commands

### Validate Single Tag

```bash
python scripts/validate_field_tags.py --tags "ti"
```

### Validate Multiple Tags

```bash
python scripts/validate_field_tags.py --tags "ti" "au" "organism"
```

### Validate Tags from File

```bash
echo -e "ti\nau\norganism" > tags.txt
python scripts/validate_field_tags.py --file tags.txt
```

### Scan Codebase

```bash
python scripts/validate_field_tags.py --scan pubmed-client/src/
```

### Check Official Docs

Use WebFetch tool with:

- URL: `https://pubmed.ncbi.nlm.nih.gov/help/#using-search-field-tags`
- Prompt: `"Does the field tag [TAG] exist? Provide its description and examples."`

### Update CLAUDE.md

```bash
# From workspace root
$EDITOR CLAUDE.md
# Add to "Currently Validated Field Tags" or "Invalid or Non-existent Tags"
```

## Resources

### scripts/

**validate_field_tags.py**: Comprehensive validation tool that checks field tags against known valid/invalid lists, provides recommendations for alternatives, and scans codebases for tag usage. Run with `--tags` for manual validation or `--scan` for codebase audit.

### references/

**pubmed_field_tags.md**: Detailed reference containing all validated field tags organized by category (author, date, content, etc.), known invalid tags with alternatives, syntax rules, search examples, and grep patterns for finding tags in code. Load this into context when:

- Implementing new query builder features
- Writing comprehensive tests for search functionality
- Debugging complex multi-field queries
- Creating documentation or examples

**When to load references/pubmed_field_tags.md**:

- Adding 5+ new field tags at once
- Implementing entire new filter category (e.g., all date filters)
- Deep-dive debugging of query builder
- Writing PubMed query syntax documentation

## Success Indicators

After following these workflows, verify:

- ✅ All field tags appear in official NCBI documentation
- ✅ Tags use short form syntax (e.g., `[ti]` not `[Title]`)
- ✅ CLAUDE.md updated with validated or invalid tags
- ✅ Code implementation includes doc comments with field tag reference
- ✅ Test queries execute successfully against PubMed API
- ✅ No invalid or deprecated tags in codebase
- ✅ Validation script returns no errors

If any of these fail, revisit the appropriate workflow above or consult `references/pubmed_field_tags.md` for comprehensive tag listings and examples.

## Integration with Development Workflow

### Before Implementing

1. Run validation workflow for new tag
2. Update CLAUDE.md with results
3. Implement in appropriate module
4. Add tests with validated tag

### During Code Review

1. Check PR for new field tags
2. Run codebase audit workflow
3. Verify CLAUDE.md updated
4. Confirm tests use valid tags

### When Debugging

1. Extract tags from failing query
2. Run query debugging workflow
3. Fix invalid tags
4. Re-test with real API
