---
name: documentation-audit
description: Systematic documentation audit that validates every documentation claim against code and identifies undocumented features - executable as a repeatable Claude Code skill (project)
---

# Documentation Audit Skill

## Purpose

Audit and repair markdown documentation in codebases to ensure documentation claims match actual code behavior while maintaining documentation structure and completeness.

## Success Criteria

1. **Accuracy**: All documentation claims verified against code
2. **Navigation**: Clear structure with functioning cross-links and README files where needed
3. **Currency**: Obsolete documentation archived or removed
4. **Completeness**: All significant features documented

## Scope

**Included**:
- Markdown documentation files (*.md)
- Text-based diagrams (Mermaid, PlantUML, Graphviz, ASCII)
- Documentation structure and navigation

**Excluded**:
- Code comments and language-specific doc comments (godoc, JSDoc, etc.)
- Image-based diagrams
- Point-in-time documents (docs/plans/*)

## When to Use This Skill

Use this skill when:
- Auditing documentation accuracy after significant code changes
- Onboarding to a new codebase and discovering documentation gaps
- Preparing for releases to ensure documentation is current
- Maintaining documentation as part of regular code health practices

## Architecture: Multi-Pass Progressive Refinement

The skill operates in four passes, each building on the previous.

### Pass 0: Repository Indexing

Build a comprehensive index of the repository before verification begins.

**Create TodoWrite tasks** for:
- Extract symbol graph using symbolic code analysis tools
- Identify API contracts from canonical sources (OpenAPI, protobuf, GraphQL schemas, configuration files)
- Map documentation cross-links and navigation files
- Index ownership metadata and last modification dates

**Activities**:
1. Use `mcp__serena__find_symbol` to extract exported symbols from each package
2. Use `Glob` to find canonical sources: `**/*.proto`, `**/openapi.yaml`, `**/*.graphql`, config schemas
3. Use `Grep` to map documentation links (search for `[.*](.*\.md)` patterns)
4. Note: Keep this pass lightweight - index only what's needed for verification

**Output**: Notes on repository structure, canonical sources found, and documentation topology.

### Pass 1: Discovery and Classification

Discover all markdown files and classify them by purpose and lifecycle.

**Create TodoWrite tasks** for:
- Find all markdown files recursively
- Classify documents by type and lifecycle
- Identify obsolete candidates for archival

**Activities**:
1. Use `Glob` with pattern `**/*.md` to find all documentation
2. Classify using multiple signals:
   - **Path heuristics**: docs/archive/*, files with dates in names
   - **Commit recency**: Use `Bash` with `git log --format=%ci --max-count=1 -- <file>` to check last update
   - **Link graph centrality**: Documents frequently linked from others are likely living docs
   - **YAML frontmatter**: Look for `status: living|archival|planned`
3. Apply decision rules:
   - docs/plans/* are point-in-time (never updated)
   - High recency + clear structure = living documentation
   - Archived paths + low recency = obsolete candidate

**Output**: Classified document inventory with assessment of which docs to audit vs archive.

**Safety**: Move obsolete documents to docs/archive/ rather than delete. Ask user before archiving documents with ambiguous classifications.

### Pass 2: Claim Extraction and Investigation Planning

Extract verifiable claims from living documentation and plan verification strategy.

**Create TodoWrite tasks** for each document section being validated.

**Activities**:
1. For each living documentation file:
   - Use `Read` to load the document
   - Extract claims by type:
     - **Behavioral**: "Service retries three times"
     - **Structural**: "Class implements Interface"
     - **API**: "Endpoint returns JSON with schema X"
     - **Configuration**: "Setting defaults to value Y"
     - **Usage**: "Run command with flag --foo"
2. Record claim metadata: doc_path, line_range, type, referenced_symbols
3. Identify text-based diagrams and classify:
   - **Normative**: Must match code structure exactly (UML class diagrams)
   - **Illustrative**: Conceptual, verify broad relationships only
4. Analyze codebase structure for documentation gaps:
   - Packages/modules without documentation
   - Exported APIs without usage examples
   - Directories lacking README files
5. Build investigation plan grouping claims by symbol/module for batch efficiency

**Output**: List of claims to verify, organized by module/package for efficient verification.

**Optimization**: Group related claims together to share context during verification.

### Pass 3: Verification and Investigation

Verify claims against code using risk-appropriate methods.

**Create TodoWrite tasks** for each investigation batch.

**Verification Hierarchy** (use highest confidence method available):
1. **Canonical sources**: Verify against OpenAPI specs, protobuf definitions, GraphQL schemas, configuration schemas
2. **Symbolic analysis**: Verify structural claims using `mcp__serena__find_symbol`, `mcp__serena__find_referencing_symbols`, `mcp__serena__search_for_pattern`
3. **Deep investigation**: Use `mcp__zen__analyze`, `mcp__zen__debug`, or `mcp__zen__thinkdeep` for complex behavioral claims

**Activities**:
1. Process investigation batches from Pass 2
2. For each claim:
   - Select verification method based on claim type and available evidence
   - Start with symbolic analysis to narrow scope before deep investigation
   - Document findings with evidence trails (file paths, line numbers, symbol names)
   - Record whether claim is verified, contradicted, or requires user review
3. Verify diagrams:
   - Parse diagram syntax to extract assertions about code structure
   - Compare against symbol graph (normative) or verify broad structure (illustrative)
4. Create documentation for identified gaps:
   - Missing README files in documented directories
   - Undocumented features found in Pass 0 indexing
5. Handle conflicts:
   - Apply authority hierarchy: canonical sources > generated docs > top-level README > service READMEs
   - Record conflicts with context (version, environment, feature flags)
   - Annotate rather than delete when conflicts may be contextual

**Output**: Verified claims with corrections noted, new documentation drafts for gaps, conflict records.

**Risk Management**:
- Assign confidence to all verifications (exploring, low, medium, high, very_high, almost_certain, certain)
- Flag low-confidence verifications for user review
- Prefer static verification over runtime checks (safer, more deterministic)
- Never auto-fix based on weak evidence

### Pass 4: Risk-Tiered Repair and Reporting

Apply corrections based on risk assessment.

**Risk Tiers**:

**Auto-fix** (apply immediately):
- Broken internal links (update paths)
- Typos in code references (symbol renamed in codebase)
- Outdated paths (files moved)
- Missing table of contents
- Diagram syntax errors

**User approval required** (present for review):
- Substantive technical corrections (behavior claims)
- Claim deletions or rewrites
- Document reclassifications
- Structural changes
- Conflict resolutions

**User review required** (flag but don't auto-fix):
- Low-confidence verifications
- Conflicting claims across documents
- Planned features (add disclaimers, don't verify behavior)
- Destructive actions (archival, removal)

**Activities**:
1. Apply auto-fixes immediately using `Edit` or `Write` tools
2. For user-approval changes:
   - Present diff preview
   - Show evidence trails (code spans, symbols verified, canonical sources)
   - Include confidence scores and rationale
   - Wait for user approval before applying
3. Move obsolete documents to docs/archive/ (after approval)
4. Create new README files for undocumented directories
5. Insert gap documentation using `Write` or `Edit`
6. Update navigation indexes
7. Generate summary report:
   - Changes by category and risk tier
   - Coverage metrics (claims verified / total claims)
   - Remaining manual review items
   - Confidence distribution

**Output**: Applied fixes, pending changes for review, archived documents, comprehensive summary.

## Authority Hierarchy

When multiple documents make conflicting claims:

1. Canonical sources (OpenAPI, protobuf, schemas)
2. Generated documentation (godoc, JSDoc)
3. Top-level README.md
4. Service/module READMEs
5. Design documents
6. Ad-hoc notes

## Document Classification Heuristics

**Living Documentation** (keep current):
- High commit frequency (updated within last 6 months)
- Clear ownership or maintenance signals
- Linked from README or navigation
- Path patterns: README.md, CONTRIBUTING.md, ARCHITECTURE.md, top-level docs

**Point-in-Time** (never update):
- Under docs/plans/
- Contains specific dates or version numbers
- Marked with status: plan or status: archival
- Low change frequency (<2 updates ever)

**Obsolete** (archive):
- No updates in 12+ months
- References removed code
- Superseded by newer documentation
- Marked with DRAFT or TODO

## Skill Parameters

Accept these parameters when invoked:

- `dry_run` (default: true): Generate report without applying changes
- `risk_tier` (default: user_approval): Maximum risk tier to auto-apply (auto_fix | user_approval)
- `verification_method` (default: auto): Force specific verification approach (auto | canonical | symbolic | deep)
- `focus_paths` (default: all): Restrict to specific directories (e.g., "docs/", "README.md")
- `skip_gap_analysis` (default: false): Skip documentation gap detection

## Usage Workflow

### Step 1: Announce and Initialize

```
"I'm using the documentation-audit skill to verify documentation accuracy."
```

Create TodoWrite tasks for all four passes plus a completion task.

### Step 2: Execute Pass 0 - Repository Indexing

Follow Pass 0 activities above. Keep this lightweight - just enough to understand repository structure and find canonical sources.

### Step 3: Execute Pass 1 - Discovery and Classification

Follow Pass 1 activities above. Classify all markdown files and identify obsolete candidates.

### Step 4: Execute Pass 2 - Claim Extraction

Follow Pass 2 activities above. Extract all verifiable claims and create investigation plan.

### Step 5: Execute Pass 3 - Verification

Follow Pass 3 activities above. Verify each claim using appropriate verification hierarchy.

### Step 6: Execute Pass 4 - Repair

Follow Pass 4 activities above. Apply fixes according to risk tiers and present changes for review.

### Step 7: Summary

Provide conversational summary:
- Total claims verified
- Auto-fixes applied
- Changes requiring approval
- Items requiring manual review
- Overall documentation health assessment

## Tools Available

- **Serena symbolic tools**: `mcp__serena__find_symbol`, `mcp__serena__find_referencing_symbols`, `mcp__serena__search_for_pattern`, `mcp__serena__get_symbols_overview`
- **Zen investigation tools**: `mcp__zen__analyze`, `mcp__zen__debug`, `mcp__zen__thinkdeep`, `mcp__zen__codereview`
- **File operations**: `Read`, `Write`, `Edit`, `Glob`, `Grep`
- **Version control**: `Bash` with git commands for commit history

## Token Efficiency Strategies

1. **Index once, reuse**: Pass 0 creates repository knowledge for later passes
2. **Batch similar claims**: Group by symbol/module to share context
3. **Retrieval-augmented**: Fetch only relevant code spans for verification
4. **Prefer static**: Use symbolic analysis before deep investigation
5. **Focused reading**: Use `mcp__serena__get_symbols_overview` before reading full files

## Safety Mechanisms

1. **Evidence trails**: Every change documents source claim, verification method, evidence
2. **Confidence scoring**: Low confidence blocks auto-fixes
3. **Diff previews**: Show changes before applying
4. **Archival over deletion**: Move obsolete docs, don't delete
5. **Risk tiers**: Separate auto-fixable issues from those requiring approval

## Edge Cases

**Feature flags**: Claims may be contextual (true when flag enabled). Record context, don't mark as contradicted.

**Multiple versions**: Documentation for different versions may coexist. Partition claims by version.

**Planned features**: Add disclaimer banners, mark verification: not_applicable. Don't attempt behavioral verification.

**External dependencies**: Claims about external APIs may be stale. Verify against canonical sources if available, otherwise flag for review.

**Runtime behavior**: Claims requiring execution (performance, flakiness) are fragile. Prefer symbolic verification or mark for manual testing.

## Example Execution

```
User: Run documentation audit on docs/ with auto-fixes enabled

Claude:
1. "I'm using the documentation-audit skill to verify documentation accuracy."
2. Creates TodoWrite for 4 passes + summary
3. Pass 0: Indexes repository (symbols, canonical sources, doc links)
4. Pass 1: Finds 23 markdown files, classifies 3 as obsolete candidates
5. Pass 2: Extracts 156 claims from 20 living docs, groups into 12 investigation batches
6. Pass 3: Verifies claims using symbolic analysis (78%), canonical sources (12%), deep investigation (10%)
   - Finds 8 contradicted claims, 12 documentation gaps
7. Pass 4:
   - Auto-fixes: 3 broken links, 1 outdated path
   - Presents for approval: 8 technical corrections, 12 new documentation sections
   - Flags for review: 2 low-confidence verifications
8. Summary: "Verified 156 claims with 95% confidence. Applied 4 auto-fixes, 20 changes await approval, 2 require manual review."
```

## Anti-Patterns

❌ **Don't skip symbolic analysis** - Use serena tools before reading full files
❌ **Don't auto-fix low-confidence findings** - Flag for user review instead
❌ **Don't delete documents** - Archive to docs/archive/ instead
❌ **Don't batch all changes** - Apply auto-fixes immediately, present substantive changes for review
❌ **Don't verify point-in-time documents** - Leave docs/plans/* alone
❌ **Don't skip TodoWrite** - Track progress through all four passes

## Summary

This skill performs rigorous documentation audits through four systematic passes:
1. Index repository structure and canonical sources
2. Classify documents by lifecycle and purpose
3. Extract and group verifiable claims
4. Verify claims and apply risk-tiered repairs

90% of effort is verification against code, 10% is structure and quality.
