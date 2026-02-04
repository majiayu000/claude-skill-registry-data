---
name: ext-outline-docs
description: Outline extension implementing protocol for documentation domain
implements: pm-workflow:workflow-extension-api/standards/extensions/outline-extension.md
user-invocable: false
allowed-tools: Read
---

# Documentation Outline Extension

> Extension implementing outline protocol for documentation domain.

Provides domain-specific knowledge for deliverable creation in documentation tasks. Implements the outline extension protocol with defined sections that phase-3-outline calls explicitly.

## Domain Detection

This domain is relevant when:
1. `doc/` or `docs/` directory exists
2. Request mentions "AsciiDoc", "ADR", "interface specification", "documentation"
3. Files have `.adoc` extension
4. Request mentions updating README or technical documentation

---

## Assessment Protocol

**Called by**: phase-3-outline Step 3
**Purpose**: Determine which workflow applies (simple vs complex)

### Workflow Selection Criteria

| Indicator | Result | Rationale |
|-----------|--------|-----------|
| Single document update | **simple** | Isolated change |
| ADR creation with supersedes | **simple** | Logically one unit |
| Interface spec with code traceability | **simple** | One deliverable for spec |
| Cross-document refactor | **complex** | Multiple files affected |
| Documentation sync with code | **complex** | Dependencies on code deliverables |
| "reorganize" keyword | **complex** | Cross-cutting structure change |

### Conditional Standards

None - documentation domain has no additional standards to layer.

---

## Simple Workflow

**Called by**: phase-3-outline Step 4 (when assessment = simple)
**Purpose**: Create deliverables for isolated documentation changes

### Domain-Specific Patterns

**Grouping Strategy**:
| Scenario | Grouping |
|----------|----------|
| Single document update | One deliverable |
| ADR creation with related updates | One deliverable for all related ADRs |
| Interface spec with code traceability | One deliverable for spec, separate for code |

**Change Type Mappings**:
| Request Pattern | change_type | execution_mode |
|-----------------|-------------|----------------|
| "add", "create", "new" ADR/doc | create | automated |
| "update", "fix" documentation | modify | automated |
| "supersede" ADR | modify | automated |

**Standard File Paths**:
- ADRs: `doc/adr/ADR-NNN-{title}.adoc`
- Interfaces: `doc/interfaces/IF-NNN-{title}.adoc`
- Architecture: `doc/architecture/{topic}.adoc`
- General: `doc/{topic}/`
- README: `README.md` or `README.adoc`

**Verification Commands**:
- AsciiDoc validation: Check for proper formatting and structure
- Link verification: Validate all internal cross-references
- ADRs: Check ADR numbering sequence and status consistency
- Interfaces: Check interface numbering and completeness

---

## Complex Workflow

**Called by**: phase-3-outline Step 4 (when assessment = complex)
**Purpose**: Create deliverables for cross-document changes

### Domain-Specific Patterns

**Grouping Strategy**:
| Scenario | Grouping |
|----------|----------|
| Documentation sync with code | Doc deliverable depends on code deliverable |
| Reorganize docs | One deliverable per logical section |

**Change Type Mappings**:
| Request Pattern | change_type | execution_mode |
|-----------------|-------------|----------------|
| "reorganize" docs | refactor | manual |
| "sync" with code | modify | automated |

**Batch Analysis**:
- Process related documents together (e.g., ADR and its superseded docs)
- Check cross-references when modifying any document
- Validate heading hierarchy in modified documents

---

## Discovery Patterns

**Called by**: Both workflows during file enumeration
**Purpose**: Provide domain-specific Glob/Grep patterns

### Grep Patterns

| Change Type | Discovery Command |
|-------------|-------------------|
| Broken xrefs | `grep -r 'xref:' doc/*.adoc` |
| ADR supersedes | `grep -r 'Superseded by' doc/adr/` |
| Interface refs | `grep -r 'IF-[0-9]' doc/` |
| README links | `grep -r '\[.*\](.*\.adoc)' README.md` |

### Glob Patterns

| Component Type | Glob Pattern |
|----------------|--------------|
| All AsciiDoc | `doc/**/*.adoc` |
| ADRs | `doc/adr/ADR-*.adoc` |
| Interfaces | `doc/interfaces/IF-*.adoc` |
| Architecture | `doc/architecture/*.adoc` |

### Comprehensive Discovery

For cross-cutting documentation changes:
```bash
# Find all AsciiDoc files
find doc/ -name "*.adoc" -type f

# Check ADR sequence
ls -1 doc/adr/ADR-*.adoc 2>/dev/null | sort

# Check interface specs
ls -1 doc/interfaces/IF-*.adoc 2>/dev/null | sort
```
