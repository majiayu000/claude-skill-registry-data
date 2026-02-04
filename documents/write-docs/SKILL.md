---
name: write-docs
description: |
  Use when user requests automated documentation generation from requirements file. Triggers include:
  - Korean: "문서 작성해줘", "write-docs 실행해줘", "자동 문서 생성"
  - English: "write documentation", "run write-docs", "generate from requirements"
  - Context: User has run prepare-docs and has docs/doc-requirements.md file ready

  This skill focuses on Step 2 of automated workflow: Reading requirements file and generating
  documentation automatically with per-sentence accuracy tracking and rationale for low-confidence statements (< 70%).
---

# Automated Documentation Generation Skill (Automated Workflow - Step 2)

## Overview

This skill generates technical documentation **automatically from requirements file** with per-sentence accuracy tracking:
- Reads `docs/doc-requirements.md` (from prepare-docs)
- Rationale mandatory for accuracy **< 70%**
- Inline source citations with relative paths
- No user interaction required

**When to use this skill:**
- User says "write-docs 실행해줘" or "자동 문서 생성"
- After running prepare-docs skill
- Fully automated generation

**Prerequisites:**
- Must have `docs/doc-requirements.md` file from prepare-docs skill

---

## ⚠️ CRITICAL RULES (Read Before Every Task)

Before starting documentation generation, verify you understand these **2 non-negotiable** rules:

### 1. Citation Format (MANDATORY)
- [ ] **Every statement** has `([Source](URL)) [accuracy%]` format
- [ ] Local files use **relative paths from document location**: `../src/file.rs#L50` (NO `file://` prefix)
- [ ] Statements with `accuracy < 70%` **MUST have rationale blockquote** below

### 2. Accuracy Calculation (MANDATORY)
- [ ] **90-100%**: Direct facts from source code/docs
- [ ] **70-89%**: Clear inference combining multiple facts
- [ ] **Below 70%**: Speculation involved → **MUST include rationale explaining confidence breakdown**

**⚠️ If you forget these rules during generation, STOP and re-read this section.**

---

## 📋 Recommended Practices

Use GitHub's rich formatting features for clearer, more expressive documentation:

- **Mermaid diagrams**: Visual representation of architecture, data flow, sequences
- **Tables**: Structured parameter lists, type definitions, comparison charts
- **GitHub alerts**: Highlight important notes, warnings, deprecations (`> [!NOTE]`, `> [!WARNING]`)
- **LaTeX math**: Mathematical formulas and equations (`$inline$` or `$$block$$`)
- **Code highlighting**: Language-specific syntax highlighting
- **Collapsible sections**: Hide detailed content until needed (`<details>`)

These formats improve readability and make complex information easier to understand.

---

## Workflow: Documentation Generation

### Step 0: Load Requirements File

**Read `docs/doc-requirements.md`** created by prepare-docs skill.

The requirements file contains:
- Document type (API Reference, System Overview, Tutorial, Custom)
- All discovered sources (core + related)
- Document structure (sections to include)
- **Content map** (what to document from where) ← **Critical for generation**
- Coverage analysis and remaining gaps

**Pay special attention to the Content Map** - it shows:
- What to document (functions, types, concepts)
- Primary source for each item
- Related sources (tests, examples, design docs)
- Coverage status (complete, partial, gaps)

The Content Map guides your documentation generation - use it to ensure you document all items with their primary and related sources.

**Verify file exists:**
```bash
# File should exist at docs/doc-requirements.md
```

If file doesn't exist, stop and inform user to run prepare-docs first.

---

### Step 1: Access Sources

From requirements file, you have complete source list.

**Access sources using:**
- Read (local files)
- WebFetch (web/remote URLs)
- MCP (Google Drive/Notion if available)
- `gh` (PR comments)

---

### Step 2: Analyze Sources and Write Documentation

Read sources thoroughly and write documentation. For each statement you write, calculate its accuracy:

| Accuracy | Criteria | Example |
|----------|----------|---------|
| **90-100%** | Direct fact from source | "Function `parse()` accepts `String`" (visible in signature) |
| **70-89%** | Clear inference from multiple facts | "Module handles auth" (from function names + module name) |
| **50-69%** | Speculation, pattern-based | "Likely retries on failure" (pattern but not documented) |
| **0-49%** | Mostly speculation | "Probably uses caching" (no evidence) |

**Key principle**: Be honest. If guessing, accuracy should be low. Below 70% **MUST** have rationale (non-negotiable).

---

#### Writing with Citations

Every statement format:
```markdown
Statement ([Source](URL)) [accuracy%]
```

**Local file citation (relative path from document location):**
```markdown
The Parser struct implements recursive descent algorithm ([Source](../src/parser.rs#L120)) [93%]
```

If document is at `docs/api-reference.md` and source is at `src/parser.rs`, use `../src/parser.rs#L120`.

**If accuracy is below 70%, add rationale (MANDATORY):**
```markdown
Statement ([Source](URL)) [accuracy%]
> Rationale: [Explain inference process: what evidence led to this conclusion, and why confidence is low]
```

**Example with rationale (below 70%):**
```markdown
The parser likely implements error recovery ([Source](../src/parser.rs#L200-250)) [65%]
> Rationale: Code shows try-catch patterns and continues after errors, but no explicit error recovery documentation found. Inference based on code structure only.
```

**High-confidence statement (no rationale needed):**
```markdown
The `calculate()` function performs matrix multiplication ([Source](https://github.com/org/repo/blob/main/src/math.rs#L45)) [95%]
```

---

#### Handling Contradictions and Gaps

As you write documentation, you may encounter contradictions or information gaps. Handle them immediately.

**Contradictions Between Sources:**

1. **Document both claims** with their sources
2. **Add TODO comment** for human verification
3. **Never auto-resolve conflicts**

Example:
```markdown
The `parse()` function returns `Result<AST, ParseError>` on failure ([Source](../src/parser.rs#L50)) [95%]

<!-- TODO: Conflict detected
- Code (src/parser.rs#L50): Returns Result<AST, ParseError>
- Docs (design.md#L30): Claims it returns Option<AST>
Please verify which is correct. Code is likely more authoritative. -->

> [!WARNING]
> Conflicting information found between code and documentation. Recommend verifying with maintainer.
```

When to use Analysis Gaps:
- Important information is **completely missing** from all sources
- Cannot make even a speculative statement with available sources

When NOT to use Analysis Gaps:
- You have a low-confidence statement (< 70%) → Use rationale instead
- Information exists but requires inference → Document with low accuracy + rationale

Example - Analysis Gap:
```markdown
## Performance Characteristics

<!-- Analysis Gap: Unable to determine performance characteristics with sufficient confidence
Sources analyzed: src/parser.rs, tests/
Recommendation: Check for benches/ directory or ask maintainer for benchmark data -->

> [!NOTE]
> Performance characteristics could not be determined from available sources. Further investigation recommended.
```
---

### Step 3: Verify Source Links

After completing document generation:

1. **Check all source links** for validity
   - Local files: Verify relative paths resolve correctly from document location
   - Remote URLs: Verify URLs are accessible
   - Line numbers: Verify line ranges exist in source files

2. **Fix broken links** before finalizing
   - Update paths if files moved
   - Remove line numbers if file changed significantly
   - Flag links that cannot be verified

3. **Report any unverifiable links** to user

---

## Tips for Effective Generation

1. **Read sources thoroughly** - Don't skim. Read entire relevant sections to understand context and avoid missing critical details.

2. **Use rationale for transparency** - For all statements with accuracy below 70%, explain the inference process and why confidence is low, so readers understand the limitations.

3. **Follow project conventions** - Match existing terminology and style from the codebase. If code uses "handler", use "handler" not "processor".

---

## Conclusion

After completing this generation workflow, you should have:

✅ Loaded requirements from `docs/doc-requirements.md`
✅ Analyzed all sources thoroughly
✅ Generated documentation with per-sentence citations and accuracy scores
✅ Used relative paths for local file citations (from document location)
✅ Added rationale for all statements with accuracy below 70%
✅ Flagged contradictions with TODO comments
✅ Documented analysis gaps in-place (no separate summary)
✅ Verified all source links are valid
