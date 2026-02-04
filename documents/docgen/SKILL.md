---
name: docgen
description: |
  Generate comprehensive documentation for .NET/C# codebases including architecture 
  diagrams, API references, domain models, and getting started guides.
  Use when asked to: generate docs, document this, create documentation, write docs for,
  document a .NET project, create architecture documentation, document APIs.
---

# Documentation Generator

Generate comprehensive documentation for .NET/C# codebases.

## Prerequisites

Scripts in `scripts/`:
- `scan_dotnet.py` - Analyze project structure, patterns, frameworks
- `find_endpoints.py` - Extract ASP.NET API endpoints

## Workflow

### Phase 1: Analysis

#### 1.1 Scan Codebase Structure
```bash
python3 scripts/scan_dotnet.py /path/to/codebase
```

Output: JSON with solution structure, frameworks, packages, detected patterns (Repository, CQRS, DDD, MediatR).

#### 1.2 Extract API Endpoints (if web project)
```bash
python3 scripts/find_endpoints.py /path/to/codebase
```

Output: JSON with controllers, routes, parameters, response types.

#### 1.3 Identify Key Files

**Always read:**
- README.md, CLAUDE.md (existing context)
- Program.cs or Startup.cs (configuration)
- Domain entities (in Domain/Core projects)

**For Clean Architecture:** Domain → Application → Infrastructure layers
**For libraries:** Public API surface, extension methods, configuration classes

### Phase 2: Planning

Determine documents to generate:

| Document | When to Include |
|----------|-----------------|
| Architecture Overview | Always |
| Getting Started | Always |
| API Reference | Web project with endpoints |
| Domain Model | DDD patterns detected |
| Configuration Guide | Options/Configuration classes found |

Create progress tracker at `/path/to/codebase/docs/.docgen-progress.json`.

### Phase 3: Generation

For each document:
1. Read relevant source files
2. Generate markdown following templates in `references/`
3. Write to `/path/to/codebase/docs/`
4. Update progress tracker

### Phase 4: Finalization

1. Generate `docs/README.md` navigation
2. Generate `docs/GLOSSARY.md` (if DDD)
3. Mark progress complete

## Reference Templates

Detailed templates for each document type:
- **Architecture**: See [architecture.md](references/architecture.md)
- **API Reference**: See [api-reference.md](references/api-reference.md)
- **Domain Model**: See [domain-model.md](references/domain-model.md)
- **Getting Started**: See [getting-started.md](references/getting-started.md)

## Output Structure

```
docs/
├── README.md                 # Navigation index
├── GLOSSARY.md              # Domain terms (if applicable)
├── .docgen-progress.json    # Progress tracking
├── architecture/
│   └── overview.md
├── api/
│   └── README.md
├── domain/
│   └── models.md
└── getting-started.md
```

## Quality Standards

- Reference actual file paths and class names
- Include real code examples from the codebase
- Use Mermaid diagrams for architecture
- Define domain terms in glossary
- Cross-reference between documents
