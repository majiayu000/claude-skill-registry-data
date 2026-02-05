---
name: python-plan-optimization
version: 2.0.0
description: |
  6-phase read-only analysis workflow for Python code in markdown documents.
  Detects design principle violations, code smells, and suggests modern Python improvements.
  Applies project-type-aware thresholds (POC, MVP, Private, Enterprise, Open Source).
  Processes one or more documents, generating per-document analysis with summary.
allowed-tools: Read, Glob, Grep, WebSearch, WebFetch
---

# Analysis Workflow

Analyzes code blocks in design documents to identify improvement opportunities using established design principles, modern Python practices, and systematic code smell detection.

## Core Mission

Analyze Python code in planning documents to identify improvement opportunities by:
1. Detecting design principle violations (SOLID, DRY, KISS, YAGNI)
2. Identifying code smells and anti-patterns
3. Suggesting modern Python alternatives (type hints, dataclasses, etc.)
4. **Respecting explicit architectural decisions and chosen tooling**
5. Presenting findings as opportunities, not requirements

**Deliverable**: Analysis report with recommendations (documents are NOT modified).

## Constraints

**Read-Only Scope:**
- Do NOT modify any files
- Do NOT apply suggested changes automatically
- Present all findings as recommendations for consideration

**MUST Respect:**
- Explicit architectural decisions stated in the document
- Chosen tooling and library decisions with stated rationale
- Application-level design choices
- External dependencies and integrations as documented
- Intentional placeholders and incomplete sections (`# TODO`, `# ...`, stub implementations)

**MAY Suggest (as opportunities):**
- Internal code organization improvements
- Class hierarchy and composition alternatives
- Method extraction and decomposition patterns
- Modern Python idiom adoption
- Type annotation additions

**NEVER (will cause analysis failure):**
- Make claims about code without quoting the exact code (minimum 3 lines with line numbers)
- Report issues when a solution already exists in surrounding context (±20 lines)
- Conflate patterns from different code blocks/stages
- Misrepresent line counts—report logic lines separately from total (e.g., "60 lines of logic, 95 total" not "~95 lines")
- Recommend specific library APIs (imports, exceptions, classes, attributes, behavior) without WebSearch verification—package splits are common
- Recommend patterns for time-dependent data (age_days, timestamps) that would cache stale values (including `@cached_property`, `@computed_field`, memoization)
- Suggest type wrappers (enums, classes) when SDK already provides `Literal[...]` types, or over-constrain generics breaking valid use cases
- Cite features from unreleased Python versions

## 6-Phase Workflow

### Phase 0: Project Type Context

Before analyzing documents, determine the analysis configuration based on project type.

**Check for Project Type in Context:**
1. Look for `project_type:` in the conversation context (set by project-type-determination skill)
2. If found → use that type for threshold configuration
3. If not found → default to `private` (most permissive, matches pre-v2.0.0 behavior)

**Load Profile from `references/project-type-profiles.md`:**

| Type | Severities | Smell Categories | Web Verification | Special Mode |
|------|------------|------------------|------------------|--------------|
| poc | Critical only | None | Skip | Minimal report |
| mvp | Critical, High | Bloaters only | Critical claims | Standard report |
| private | All | All | Optional | Educational context |
| enterprise | All | All | **Required** | Cross-document checks |
| opensource | All | All + API design | Required | Types + docs required |

**Store Configuration:**
- `include_severities`: List of severities to report
- `include_smell_categories`: List of smell categories to check
- `require_web_verification`: Boolean or "critical_only"
- `educational_mode`: Boolean (explain "why" for each finding)
- `require_type_hints_public`: Boolean (opensource only)
- `require_docs_public`: Boolean (opensource only)

**Output for Report Header:**
```
project_type: [type]
project_type_source: [prompt|document|user|default]
analysis_mode: [description from profile]
```

### Phase 1: Discovery

Understand the codebase context and identify explicit decisions.

**For each document:**
1. Read the document completely
2. Identify all Python code blocks (fenced with ``` or indented)
3. Catalog the purpose of each code example
4. Note dependencies between code examples
5. Identify the Python version targeted (assume 3.10+ unless specified)
6. **Identify explicit architectural decisions and tooling choices**

**Error Handling:**
- If a document cannot be read: mark as failed, record reason, continue to next
- If no code blocks found: mark as skipped, record reason, continue to next

**Cross-Document Tracking (when multiple documents):**
- Note shared patterns across documents
- Track common dependencies
- Flag potential inconsistencies between documents

**Discovery Questions:**
- What is the purpose of this code?
- What external dependencies exist?
- Are there constraints mentioned in surrounding text?
- How do code blocks relate to each other?
- **What explicit decisions have been made and why?**
- Are there patterns shared across documents?

### Phase 2: Assessment

Evaluate code against design principles and identify issues. **Apply project type filters from Phase 0.**

**Pre-Assessment: Apply Type Filters**

Before evaluating findings, apply the project type configuration:
- **Severity Filter**: Only assess issues at or above the threshold (e.g., POC = Critical only)
- **Smell Category Filter**: Only check included categories (e.g., MVP = Bloaters only)
- **Open Source Checks**: If `opensource`, also check for missing type hints and docs on public API

**For EACH potential finding, you MUST:**
1. Quote the exact code (minimum 3 lines, include line numbers)
2. Trace data flow to verify the problem causes incorrect behavior (pattern match alone is insufficient)
3. Check ±20 lines for an existing solution
4. Confirm you're analyzing the correct file/stage
5. For third-party library claims: WebSearch the exact API name—only include if documentation confirms it exists (no confirmation = do not claim)

**If ANY verification step fails, do NOT include the finding.**

**Principle Checklist:**

| Principle | Check For | Quick Fix |
|-----------|-----------|-----------|
| SRP | Class has 2+ unrelated reasons to change (multiple methods ≠ multiple responsibilities) | Extract class/function |
| OCP | Modification required for extension | Use abstraction/strategy |
| LSP | Substitutability violations | Fix hierarchy design |
| ISP | Implementing unused methods | Split interface |
| DIP | Direct concrete dependencies | Inject abstractions |
| DRY | Same logic repeated 3+ times (2 occurrences may be acceptable locality) | Extract shared logic |
| KISS | Unnecessary complexity | Simplify approach |
| YAGNI | Speculative features | Remove unused code |

**Code Smell Categories:**

| Category | Common Smells |
|----------|---------------|
| Bloaters | Long methods, large classes, primitive obsession, long parameter lists |
| OO Abusers | Switch statements, parallel inheritance, refused bequest |
| Change Preventers | Divergent change, shotgun surgery |
| Dispensables | Dead code, speculative generality, duplicate code |
| Couplers | Feature envy, inappropriate intimacy, message chains |

See `references/design-principles.md` and `references/code-smells.md` for detailed detection patterns.

### Phase 3: Planning

Prioritize findings and organize recommendations. **Apply project type severity filters.**

**Planning Steps:**
1. Prioritize issues by impact (Critical > High > Medium > Low)
2. **Filter to included severities** based on project type (from Phase 0)
3. Group related issues that should be addressed together
4. Filter out suggestions that conflict with explicit architectural decisions
5. Organize recommendations by code block
6. **If enterprise/opensource**: Mark findings that need web verification

**Severity Assessment:**

| Severity | Description | Context Requirement |
|----------|-------------|---------------------|
| Critical | Demonstrated architectural impact | Issue manifests in described/default deployment |
| High | Significant principle violations | Impact traceable in actual code flow |
| Medium | Code smells affecting maintainability | Would cause issues under normal usage |
| Low | Style issues, minor improvements | Improvement is clear, no risk |

**Before assigning severity, ask:**
1. Under what deployment conditions does this issue actually manifest?
2. Is this demonstrated in the code flow, or only theoretical?
3. Does fixing this actually improve the code, or just satisfy a pattern?

### Phase 4: Recommendations

Generate improvement suggestions with alternatives.

**Recommendation Approach:**
1. Present one principle/pattern improvement at a time
2. Show before/after code examples (as suggestions, NOT applied)
3. Explain the benefit of each suggested change
4. Note any tradeoffs or considerations
5. **Clarify these are opportunities, not requirements**

**Modern Python Practices:**

| Feature | Old Syntax | Modern Syntax |
|---------|------------|---------------|
| Type hints | `# type: str` | `def foo(x: str) -> int:` |
| Optional | `Optional[str]` | `str \| None` |
| Lists | `List[str]` | `list[str]` |
| Data containers | Manual `__init__` | `@dataclass` |
| Pattern matching | if/elif chains | `match/case` |
| Formatting | `.format()` | f-strings |
| File paths | `os.path` | `pathlib.Path` |

See `references/modern-python.md` for detailed guidance.

### Phase 5: Report

Generate comprehensive analysis report. **Include project type context in header.**

**Output Format:**

```markdown
## Analysis Report

**Project Type:** [type] (source: [prompt|document|user|default])
**Analysis Mode:** [description from profile]

---

### Summary

| Metric | Count |
|--------|-------|
| Documents Analyzed | [count] |
| Documents Skipped | [count] |
| Total Code Blocks | [count] |
| Total Issues Found | [count] |
| Total Recommendations | [count] |

### Severity Distribution

| Severity | Count |
|----------|-------|
| Critical | [n] |
| High | [n] |
| Medium | [n] |
| Low | [n] |

---

## Document: [path/to/document.md]

**Status:** SUCCESS|PARTIAL|SKIPPED|FAILED
**Code Blocks Analyzed:** [count]
**Issues Found:** [count]
**Architectural Decisions Respected:** [count]

### Architectural Context

[List of explicit decisions recognized in this document]

### Code Block Analysis

#### Block 1: [description]

**File/Stage:** [explicit identifier - e.g., "Stage 2: execute_search"]

**Architectural Context:**
[Decisions that apply to this block - these are respected]

**Finding 1:** [issue title]

**Code (lines X-Y):**
```python
# Exact code being critiqued (minimum 3 lines)
```

**Issue:** [What the problem is]

**Suggested Improvement:**
```python
# Recommended alternative
```

**Rationale:** [Why this could help]

---

[Repeat for additional documents...]

---

## Cross-Document Observations

[If multiple documents: patterns, inconsistencies, shared opportunities]

---

**Important:** This is a read-only analysis. No files have been modified.
```

**Report Guidelines:**
- Present summary first for quick overview
- Generate per-document sections with findings
- Note cross-document patterns when analyzing multiple files
- Use collapsible sections for lengthy findings if needed

## Respecting Architectural Decisions

When the document contains explicit architectural decisions or tooling choices:

**Recognition Patterns:**
- "We chose X because Y"
- "The decision to use X was made due to"
- "Given the constraints, we selected"
- "The architecture uses X for..."
- Explicit technology/library choices with rationale

**Handling:**
1. **Acknowledge** the decision in the analysis
2. **Do NOT suggest** replacing the chosen approach
3. **MAY suggest** improvements within the chosen framework
4. **Clarify** that suggestions are opportunities, not requirements

**Example:**
If document says "We use SQLAlchemy for ORM because of existing team expertise":
- ✅ Suggest: "Consider using SQLAlchemy's hybrid properties for computed fields"
- ❌ Do NOT suggest: "Consider switching to Tortoise ORM for async support"

## Behavioral Compatibility Notes

When suggesting changes, note potential behavioral impacts:

| # | Consideration |
|---|---------------|
| 1 | Would function/method signatures change? |
| 2 | Would return types or values be affected? |
| 3 | Would side effects be altered? |
| 4 | Would exception behavior change? |
| 5 | Would public attributes be affected? |

See `references/behavioral-compatibility.md` for detailed guidance.

## Concurrency Verification

These terms are NOT interchangeable—verify via WebSearch before making claims:

| Term | Meaning | Example |
|------|---------|---------|
| Async-safe | Safe for concurrent coroutines (single thread) | `asyncio.Lock()` |
| Thread-safe | Safe for concurrent threads | `threading.Lock()` |
| Process-safe | Safe across worker processes | Redis, database, file locks |

In-memory caches and locks do NOT provide safety across worker processes (e.g., uvicorn/gunicorn workers).

## Ambiguity Handling

When encountering ambiguous cases:
- Note the ambiguity in the report
- Present multiple possible interpretations if relevant
- Flag areas needing clarification with `<!-- CLARIFY: reason -->`
- When in doubt, acknowledge uncertainty in the analysis

## Additional Resources

### Reference Files

Consult for detailed guidance:
- **`references/project-type-profiles.md`** - Project type thresholds and filtering configuration
- **`references/design-principles.md`** - Complete SOLID, DRY, KISS, YAGNI guidance with Python examples
- **`references/modern-python.md`** - Modern Python features, type hints, dataclasses, idioms
- **`references/code-smells.md`** - Comprehensive code smell catalog with detection and fixes
- **`references/behavioral-compatibility.md`** - Detailed 13-point checklist with verification strategies

## Success Metrics

Analysis succeeds when:
- **Project type is identified** (from context or defaults to private)
- **Thresholds are applied** according to project type profile
- All provided documents are processed (or errors reported)
- Each document's code blocks are analyzed
- Explicit architectural decisions are recognized and respected
- Findings are presented as opportunities, not mandates
- Suggested alternatives are practical within stated constraints
- Report includes project type and analysis mode in header
- Report is comprehensive but actionable
- **No documents are modified**
