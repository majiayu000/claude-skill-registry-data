---
name: julien-ref-doc-review
description: Simplified document review methodology with 4 core tags (@FIX, @TODO, @VERIFY, @OK) and [MACRO] flag for systemic impact. Use for annotating and reviewing documentation.
triggers:
  - relire ce document
  - annoter un fichier
  - marquer ce qui est à corriger
  - trouver les TODO
  - review this document
  - proofread this file
  - check my documentation
  - flag issues in documentation
  - document review
  - annotation tags
---

# Document Review Methodology

**Version**: 2.0 (Simplified)

---

## Overview

- Annotate documentation with **4 simple tags**
- Parse comments automatically with Claude
- Distinguish micro (local) vs macro (systemic) changes
- Apply verified modifications from sources

**Philosophy**: 4 core tags + 1 flag = maximum clarity, minimum confusion

---

## Tag System

### CORE Tags (4 essential)

| Tag | Hotstring | Usage | Examples |
|-----|-----------|-------|----------|
| `<!-- @FIX: -->` | `;fix` | Correct factual error | Typo, incorrect formula, false info |
| `<!-- @TODO: -->` | `;tod` | Add/modify content (generic) | Rephrase, add example, complete section |
| `<!-- @VERIFY: -->` | `;ver` | Verify against sources | Check formula, test link, cross-check data |
| `<!-- @OK: -->` | `;okk` | Light validation | Section read, no obvious issue |

### SPECIAL Tags (particular use)

| Tag | Hotstring | Usage | Context |
|-----|-----------|-------|---------|
| `[MACRO]` | `;mac` | Systemic impact flag | Add AFTER description if macro change |
| `<!-- @LOCKED: -->` | `;lck` | Lock content | Forbid modification during session |
| `<!-- @APPROVED: -->` | `;app` | Formal validation | NEVER modify unless explicit request |

---

## [MACRO] Impact Flag

### Principle

**Default**: Any tag = **MICRO** change (local, no systemic impact)
**If systemic impact**: Add `[MACRO]` AFTER the description

### Syntax

```markdown
<!-- @FIX: Incorrect Amount formula [MACRO] affects 3 databases -->
<!-- @TODO: Rename field [MACRO] verify all references -->
<!-- @VERIFY: Workflow change [MACRO] test 4 user roles -->
```

### When to use [MACRO]?

| Trigger | Example | Why MACRO |
|---------|---------|-----------|
| **Modified formula/calc** | Change formula used elsewhere | Calculation propagation |
| **Rename field/variable** | Rename "Budget" → "Allocation" | Multiple references |
| **Workflow/process** | Add "Cancelled" state | Rights/validations impact |
| **Cross-system relation** | Modify DB1 → DB2 link | Referential integrity |
| **External API/sync** | Test sync with ERP | External regression risk |

### Comparative Examples

#### MICRO (no flag)
```markdown
<!-- @FIX: Typo "budjet" → "budget" -->
<!-- @TODO: Rephrase - Section too technical for non-expert -->
<!-- @TODO: Example - Add typical contract amount -->
<!-- @VERIFY: Formula - Check against JSON source -->
```

#### MACRO (flag required)
```markdown
<!-- @FIX: Formula Amount = A21*A23 incorrect [MACRO] should be if(A20="Manual",A21,A23), affects Budget Remaining in 3 files -->

<!-- @TODO: Rename "Budget Remaining" → "Budget Available" [MACRO] check 3 databases + API sync -->

<!-- @VERIFY: Workflow add state "Cancelled" [MACRO] test impact on 4 user roles + reporting -->
```

---

## Review Workflow

### Phase 1: Annotation (User)

1. Open `.md` file
2. Read section by section
3. Annotate with hotstrings:
   - Typo → `;fix` Typo "budjet" → "budget"
   - Rephrase → `;tod` Rephrase - Too technical
   - Incorrect formula → `;fix` Incorrect formula `;mac`
   - Section OK → `;okk` Glossary section
4. Save

### Phase 2: Parsing (Claude)

```bash
"Parse comments from [folder/file]"
"Generate comment tracking report"
"Process all @FIX from [folder]"
```

### Phase 3: Processing (Claude)

1. **Extraction**: Recursive `.md` scan, tag extraction
2. **Impact detection**:
   - Explicit `[MACRO]` flag → Impact analysis required
   - Change aggregation → Auto cumulative macro detection
3. **Verification**: `@VERIFY` → Check sources
4. **Proposal**: Changes with evidence
5. **Impact Analysis**: If `[MACRO]` → detailed report generation
6. **Validation**: User approves/refuses
7. **Application**: Changes + tag removal
8. **Commit**: Detailed report

#### Tag removal after processing

- Processed tags: **REMOVED**
- `@OK` and `@APPROVED`: **KEPT** with date only
- Format: `<!-- @OK: 2025-10-21 -->` or `<!-- @APPROVED: 2025-10-21 -->`

#### Precautions

- Files on disk = source of truth (not Claude memory)
- `@LOCKED` never modified
- `@APPROVED` modified only on explicit request
- Non-invention principle: Extract from sources, NEVER invent

---

## Report Format

```markdown
## Comment Processing Report - [Date]

### Statistics
- Total: 15 comments
- @FIX: 3 (including 1 [MACRO]) | @TODO: 8 (including 2 [MACRO])
- @VERIFY: 3 | @OK: 1

### By file
- file1.md: 6 (2 MACRO)
- file2.md: 5 (1 MACRO)
- file3.md: 4 (0 MACRO)

### By priority

#### High priority (@FIX + [MACRO])
1. **@FIX [MACRO]** - `file.md:L34`
   **Before**: Formula Amount = A21*A23
   **After**: if(A20="Manual",A21,A23)
   **Impact**: 3 files use this result
   **Tests**: Verify calculations in file2, file5, file7
   **Action**: Edit L34 + cross-check

#### Medium (@TODO)
2. **@TODO** - `file.md:L12`
   **Action**: Add typical amount example
   **Impact**: Local

#### Low (@VERIFY simple)
3. **@VERIFY** - `file.md:L67`
   **Action**: Check formula against JSON
   **Result**: Confirmed correct
```

---

## Migration from Old Tags

| Old Tag | New Equivalent |
|---------|----------------|
| `@CLARIFY` | `@TODO: Rephrase - [description]` |
| `@MISSING` | `@TODO: Add - [description]` |
| `@ADD-EXAMPLE` | `@TODO: Example - [description]` |
| `@SUGGEST` | `@TODO: Suggestion - [description]` |
| `@QUESTION` | `@TODO: Question - [description]` |
| `@NOTE` | `@TODO: Note - [description]` |
| `@CHECK-FORMULA` | `@VERIFY: Formula - [description]` |
| `@CHECK-LINK` | `@VERIFY: Link - [description]` |
| `@METHODOLOGY` | `@TODO: Methodology - [description]` |

---

## Related Skills

- **julien-ref-doc-production**: Use before reviewing to create documentation with proper structure and templates
