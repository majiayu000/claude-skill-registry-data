---
name: repo-docs-wiki
description: Generate and maintain DeepWiki-style documentation for code repositories. Use when the user asks to generate docs for a repo, create full documentation, build a wiki for a codebase, create DeepWiki-style docs, sync docs with code, update documentation, refresh the wiki, or bring docs up to date. Creates structured markdown docs (ARCHITECTURE, INTERFACES, DEVELOPER_GUIDE, INDEX, concepts, module READMEs) without modifying source code.
license: Apache-2.0. Complete terms in LICENSE.txt
---

# Repository Documentation Wiki Builder

Generate and maintain comprehensive wiki-style documentation for any codebase.

## Modes

This skill operates in two modes:

| Mode | Trigger | When to Use |
|------|---------|-------------|
| **Full Generation** | "generate docs", "create documentation", "build wiki" | No existing docs structure |
| **Sync/Refresh** | "sync docs", "update documentation", "refresh wiki" | Docs exist, need updating |

**Auto-detection**: If intent is ambiguous, check for `docs/ARCHITECTURE.md`. If present → Sync mode. Otherwise → Full Generation.

## Constraints

**READ-ONLY for source code**:
- Analyze any file in the repository
- NEVER modify source code files
- ONLY create/update documentation files (Markdown)
- Default docs location: `/docs/` (respect existing conventions if present)

**No hallucination**:
- Base documentation strictly on actual code, configs, and tests
- Never invent features, APIs, or behaviors not present in code
- Say "unable to determine" rather than guess

**No secrets**:
- Never include API keys, passwords, tokens, or credentials
- Use placeholders like `<API_KEY>` in examples

---

## Full Generation Workflow

When no documentation structure exists:

### Step 1: Repository Analysis

Examine the codebase systematically:

```
1. Entry points: package.json, main files, index files
2. Languages & frameworks: File extensions, config files
3. Structure: Directory layout, naming patterns
4. Tests: Test directories, testing framework
5. Config: Environment files, CI/CD, deployment
6. External: APIs consumed, services integrated
```

### Step 2: Create Documentation Structure

Create files in this order:

| File | Template Reference |
|------|-------------------|
| `docs/ARCHITECTURE.md` | [architecture-template.md](references/architecture-template.md) |
| `docs/INTERFACES.md` | [interfaces-template.md](references/interfaces-template.md) |
| `docs/DEVELOPER_GUIDE.md` | [developer-guide-template.md](references/developer-guide-template.md) |
| `docs/INDEX.md` | [index-template.md](references/index-template.md) |
| `docs/concepts/*.md` | [concept-template.md](references/concept-template.md) |
| `src/*/README.md` | [module-readme-template.md](references/module-readme-template.md) |

### Step 3: Architecture Documentation

Read [architecture-template.md](references/architecture-template.md), then create `docs/ARCHITECTURE.md`:

1. **Overview**: 3-5 sentences on purpose and users
2. **Tech Stack**: All languages, frameworks, databases, services
3. **Structure**: Directory map with responsibilities
4. **Subsystems**: 3-7 major components described
5. **Key Flows**: 3-5 data/control flows documented
6. **Diagrams**: 1-2 Mermaid diagrams using real names

### Step 4: Interfaces Documentation

Read [interfaces-template.md](references/interfaces-template.md), then create `docs/INTERFACES.md`:

1. **Interface inventory**: Table of all public surfaces
2. **HTTP APIs**: Endpoints with methods, paths, auth, payloads
3. **Library APIs**: Public classes/functions with examples
4. **CLI**: Commands with flags and examples
5. **Events/Jobs**: Names, triggers, payloads
6. **Stability notes**: Mark stable vs experimental vs internal

### Step 5: Developer Guide

Read [developer-guide-template.md](references/developer-guide-template.md), then create `docs/DEVELOPER_GUIDE.md`:

1. **Purpose**: Project role and system context
2. **Setup**: Prerequisites, install, env vars (no secrets!)
3. **Workflow**: Linting, testing, branching conventions
4. **Safe areas**: Green/yellow/red zones for changes
5. **Common tasks**: 5-10 step-by-step task guides
6. **Conventions**: Naming, errors, logging patterns
7. **Future work**: Known improvement opportunities

### Step 6: Concept Pages

Read [concept-template.md](references/concept-template.md), then create `docs/concepts/`:

Identify 5-10 key concepts by examining:
- Database models/tables
- Core type definitions
- Service class names
- API resource nouns
- Event names

For each concept, create `docs/concepts/[Name].md` covering:
- Definition and purpose
- Code locations
- Key fields and invariants
- Lifecycle (if stateful)
- Relationships

### Step 7: Module READMEs

Read [module-readme-template.md](references/module-readme-template.md), then create READMEs for important directories.

**Priority order**:
1. Business logic (`services/`, `core/`)
2. Interface layer (`api/`, `routes/`)
3. Data layer (`models/`, `db/`)
4. Utilities (`utils/`, `lib/`)

Each README covers:
- Purpose (1-2 sentences)
- Directory structure
- Key files
- Dependencies (in/out)
- Conventions and patterns

### Step 8: Index and Cross-Links

Read [index-template.md](references/index-template.md), then create `docs/INDEX.md`:

1. Overview of documentation set
2. Links to ARCHITECTURE, INTERFACES, DEVELOPER_GUIDE
3. Module table with links to READMEs
4. Concept table with links to concept pages
5. "Start here" pathways for different reader goals
6. Validate all links are correct and working

---

## Sync Workflow

When documentation already exists:

### Step 1: Detect Existing Structure

Locate existing docs:
```
docs/
├── ARCHITECTURE.md    (check)
├── INTERFACES.md      (check)
├── DEVELOPER_GUIDE.md (check)
├── INDEX.md           (check)
└── concepts/          (check)
```

Note existing conventions (location, naming, style).

### Step 2: Identify Changes

Compare code against documentation:

| Check | How |
|-------|-----|
| New modules | Directories without README |
| New APIs | Undocumented endpoints/commands |
| New concepts | Models/types not in concepts/ |
| Removed items | Docs referencing deleted code |
| Changed items | Outdated descriptions or flows |

### Step 3: Update Incrementally

**Prefer section updates over full rewrites**:
- Add new sections for new features
- Update specific paragraphs for changes
- Remove sections for deleted functionality
- Preserve valuable manual prose

**For each doc type**, re-read the appropriate template:
- [architecture-template.md](references/architecture-template.md) for ARCHITECTURE.md
- [interfaces-template.md](references/interfaces-template.md) for INTERFACES.md
- [developer-guide-template.md](references/developer-guide-template.md) for DEVELOPER_GUIDE.md

### Step 4: Add New Documentation

Create new files as needed:
- New concept pages for new domain entities
- New module READMEs for new directories
- Update INDEX.md with new links

### Step 5: Validate Links

Ensure all cross-references work:
- Internal doc links (relative paths)
- Code file references
- Section anchors

Fix or remove broken links.

---

## Reference Files

Load these templates as needed:

| Template | When to Load |
|----------|--------------|
| [architecture-template.md](references/architecture-template.md) | Creating/updating ARCHITECTURE.md |
| [interfaces-template.md](references/interfaces-template.md) | Creating/updating INTERFACES.md |
| [developer-guide-template.md](references/developer-guide-template.md) | Creating/updating DEVELOPER_GUIDE.md |
| [index-template.md](references/index-template.md) | Creating/updating INDEX.md |
| [concept-template.md](references/concept-template.md) | Creating any concept page |
| [module-readme-template.md](references/module-readme-template.md) | Creating any module README |

---

## Success Criteria

Documentation is complete when:

- [ ] New developer can understand what the repo does
- [ ] Setup instructions are complete and accurate
- [ ] All public interfaces are documented
- [ ] Key concepts are explained with code locations
- [ ] Important modules have READMEs
- [ ] INDEX.md provides clear navigation
- [ ] All links are valid
- [ ] No source code was modified
- [ ] No secrets are exposed
