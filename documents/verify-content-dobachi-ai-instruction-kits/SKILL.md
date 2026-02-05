---
name: verify-content
description: Integrated skill for fact-checking and reference verification. Covers claim identification, source verification, and reference management. Use for document review, article proofreading, report verification, and academic paper checking.
---

# Content Verification Skill

Provides an integrated workflow for ensuring content reliability.

## Workflow Overview

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Step 1     │    │  Step 2     │    │  Step 3     │
│  Scan       │ → │  Verify     │ → │  Reference  │
│             │    │             │    │             │
└─────────────┘    └─────────────┘    └─────────────┘
```

See detailed guides:
- [scan.md](scan.md) - Identify statements requiring verification
- [verify.md](verify.md) - Verify facts with external sources
- [reference.md](reference.md) - Manage references and citations

## Quick Start

### Run Full Workflow

```
User: Verify the content of this document
```

### Run Specific Steps

```
User: Identify statements that need fact-checking in this article
User: Fact-check this numerical data
User: Organize the reference list
```

## Step 1: Scan

Analyze the entire text to identify statements requiring verification.

### Check Categories

| Category | Examples |
|----------|----------|
| Factual statements | Historical facts, scientific facts, regulations |
| Quantitative claims | Numbers, statistics, dates, rankings |
| Definitive expressions | "always", "the only", "the largest" |
| Citations | Quotes, document references |
| Comparisons | "better than", "generally" |

### Output Format

```markdown
## Verification Targets

### Priority: High
| # | Statement | Type | Verification Needed |
|---|-----------|------|---------------------|
| 1 | "..." | Numerical | Verify source |
```

See [scan.md](scan.md) for details.

## Step 2: Verify

Verify identified statements using reliable external sources.

### Verification Process

1. **Identify sources**: Gather candidates via web search
2. **Retrieve actual content**: Use WebFetch or curl to confirm
3. **Judge**: Check consistency, accuracy, context, currency

### Important: Don't Trust AI Search Results Blindly

```bash
# When WebFetch is blocked
curl -s -L "https://example.com/page" | head -200

# Check Wayback Machine for archived versions
curl -s "https://archive.org/wayback/available?url=example.com/page"
```

### Verdict Criteria

| Verdict | Condition |
|---------|-----------|
| ✅ Accurate | Confirmed by reliable source, content matches |
| ⚠️ Needs Revision | Mostly accurate but requires minor corrections |
| ❌ Incorrect | Contradicts facts or significantly misleading |
| ❓ Unverifiable | No reliable source found or inaccessible |

See [verify.md](verify.md) for details.

## Step 3: Reference

After verification, manage references according to project specifications.

### Tasks

1. **Check project specifications**: Citation style, placement
2. **Add to reference list**: Register confirmed sources
3. **Add cross-references**: Footnotes/inline/numbered references

### Citation Format Examples

```markdown
<!-- Footnote style -->
Japan's population is approximately 120 million[^1].
[^1]: Statistics Bureau of Japan "Population Estimates" 2024

<!-- Inline style -->
Japan's population is approximately 120 million (Statistics Bureau of Japan, 2024).
```

See [reference.md](reference.md) for details.

## Verifying Existing References

When the document already has references, also check:

### Checklist

- [ ] Links are alive (no 404 errors)
- [ ] Cited content matches the source
- [ ] Citations are used in proper context
- [ ] Source information is current

### Handling Broken Links

```bash
# Check status code
curl -s -o /dev/null -w "%{http_code}" "https://example.com/page"

# Get alternative URL from Wayback Machine
curl -s "https://archive.org/wayback/available?url=example.com/page"
```

## Usage Examples

```
User: Verify the content of README.md and organize references
```

```
User: Check if the citations in this paper are correct
```

```
User: Verify the items identified in Issue #45
```

## Output Report Format

```markdown
# Content Verification Report

## Target File
- path/to/document.md

## Verification Summary
| Items | ✅ Accurate | ⚠️ Needs Revision | ❌ Incorrect | ❓ Unverifiable |
|-------|-------------|-------------------|--------------|-----------------|
| 10    | 7           | 2                 | 0            | 1               |

## Detailed Results
[Verification results for each item...]

## Reference Management Status
- [ ] Reference list updated
- [ ] Cross-references added in text
- [ ] Links verified
```
