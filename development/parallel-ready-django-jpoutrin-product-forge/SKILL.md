---
name: parallel-ready-django
short: Audit Django project for parallel agent development
description: Audit and prepare a Django codebase for parallel multi-agent development. Use when asked to check if a Django project is ready for parallelization, prepare a repo for multi-agent work, audit codebase structure, set up orchestration infrastructure, or identify blockers for parallel development. Analyzes Django apps, models, migrations, and module boundaries.
when: User wants to check Django parallelization readiness, prepare Django project for multi-agent development, audit Django app structure, identify parallel development blockers, or set up orchestration infrastructure for Django
---

# Django Parallel Readiness Assessment

Audit and prepare a Django codebase to support parallel development with multiple Claude Code agents.

## Quick Start

Run the full assessment:

```
1. Analyze Django project structure and app organization
2. Score each readiness dimension
3. Identify blockers and risks
4. Generate remediation plan
5. Set up orchestration infrastructure
```

## Automated Analysis

Run the analysis script from project root:

```bash
# From project root (default: analyzes 'apps/' directory)
python analyze-readiness.py

# Specify custom apps directory
python analyze-readiness.py src/apps

# Output saved to .claude/readiness-report.md
```

The script analyzes:
- **App Boundaries**: Cross-app imports, circular dependencies, god apps
- **Shared State**: Global variables, Django signals, mutable state
- **Contracts**: Mypy config, OpenAPI, serializer `__all__` usage
- **Tests**: Test file count, pytest config, Factory Boy usage
- **Documentation**: CLAUDE.md, README, linting config
- **Dependencies**: Lock files, pinned versions, migration count

See `references/analyze-readiness.py` for the full script.

## Assessment Dimensions

### 1. Django App Boundaries (Critical)

**Check for:**
- Clear app separation with single responsibility
- Minimal cross-app model imports
- No circular dependencies between apps
- Proper use of app namespacing

**Red flags:**
- God app that contains most models/views
- Heavy cross-app foreign keys
- Shared models across multiple apps
- Deeply nested cross-app imports

**Scoring:**
- ✅ Good: Each domain has dedicated app, <10% cross-app model imports
- ⚠️ Fair: Some separation exists, 10-30% cross-imports
- ❌ Poor: Single app structure, heavy coupling, >30% cross-imports

**Detection commands:**
```bash
# Count models per app
find . -name "models.py" -exec grep -l "class.*Model" {} \;

# Find cross-app imports
grep -r "from.*\.models import" --include="*.py" | grep -v "__pycache__"

# Check for circular imports
python -c "import sys; sys.setrecursionlimit(50); import myapp"
```

### 2. Shared State & Settings (Critical)

**Check for:**
- Global variables in settings.py
- Shared caches without isolation
- Signals causing side effects across apps
- Thread-local storage usage

**Red flags:**
- Mutable globals in apps
- Signals modifying models in other apps
- Shared file writes across apps
- Global middleware state

**Scoring:**
- ✅ Good: No global mutable state, dependency injection used
- ⚠️ Fair: Limited globals, documented shared resources
- ❌ Poor: Heavy global state, signals everywhere

**Detection commands:**
```bash
# Find global variables
grep -r "^[A-Z_]*\s*=" --include="*.py" | grep -v settings.py

# Find signal usage
grep -r "@receiver\|\.connect(" --include="*.py"

# Find cache usage
grep -r "cache\.\(get\|set\|delete\)" --include="*.py"
```

### 3. API Contracts & Serializers (High)

**Check for:**
- DRF serializers with explicit fields
- OpenAPI/Swagger documentation
- Type hints on views and serializers
- Versioned API endpoints

**Red flags:**
- `fields = "__all__"` in serializers
- Untyped view functions
- Undocumented internal APIs
- Implicit serializer behavior

**Scoring:**
- ✅ Good: Full OpenAPI spec, typed serializers, versioned APIs
- ⚠️ Fair: Partial typing, some documented endpoints
- ❌ Poor: No contracts, `__all__` fields everywhere

**Detection commands:**
```bash
# Find serializers with __all__
grep -r 'fields\s*=\s*"__all__"\|fields\s*=\s*.__all__.' --include="*.py"

# Check for OpenAPI setup
grep -r "SpectacularAPIView\|swagger\|openapi" --include="*.py"

# Find untyped views
grep -r "def .*request.*:" --include="views.py" | grep -v ": HttpRequest"
```

### 4. Test Infrastructure (High)

**Check for:**
- pytest-django or Django TestCase setup
- Factory Boy or model fixtures
- Test isolation (TransactionTestCase where needed)
- CI pipeline with test coverage

**Red flags:**
- Tests that share database state
- Order-dependent tests
- Missing migration tests
- No integration test capability

**Scoring:**
- ✅ Good: Full test suite, isolated tests, >80% coverage
- ⚠️ Fair: Partial coverage, some test infrastructure
- ❌ Poor: Minimal tests, no CI

**Detection commands:**
```bash
# Find test files
find . -name "test*.py" -o -name "*_test.py" | wc -l

# Check for pytest
grep -r "pytest" pyproject.toml setup.cfg requirements*.txt 2>/dev/null

# Check for factories
grep -r "factory.Factory\|FactoryBoy" --include="*.py"
```

### 5. Documentation & Conventions (Medium)

**Check for:**
- CLAUDE.md or contributing guide
- Type hints (mypy configuration)
- Code formatters (ruff, black, isort)
- Architecture documentation

**Red flags:**
- No documented conventions
- Inconsistent patterns across apps
- Missing setup instructions
- No type checking

**Scoring:**
- ✅ Good: CLAUDE.md exists, mypy strict, ruff configured
- ⚠️ Fair: Some docs, partial linting
- ❌ Poor: No conventions documented

**Detection commands:**
```bash
# Check for config files
ls -la pyproject.toml setup.cfg mypy.ini .ruff.toml 2>/dev/null

# Check for type hints
grep -r "-> " --include="*.py" | head -20

# Check for CLAUDE.md
ls -la CLAUDE.md .claude/ 2>/dev/null
```

### 6. Migration & Dependency Management (Medium)

**Check for:**
- Migration squashing strategy
- Clear migration dependencies
- requirements.txt or pyproject.toml with pinned versions
- No phantom dependencies

**Scoring:**
- ✅ Good: Squashed migrations, pinned deps, reproducible installs
- ⚠️ Fair: Some migration issues, mostly pinned deps
- ❌ Poor: Migration conflicts, unpinned deps

**Detection commands:**
```bash
# Count migrations per app
find . -path "*/migrations/*.py" -not -name "__init__.py" | cut -d/ -f3 | sort | uniq -c

# Check for merge migrations
find . -path "*/migrations/*.py" -exec grep -l "merge" {} \;

# Check dependency pinning
grep -E "^[a-zA-Z].*==" requirements*.txt 2>/dev/null | wc -l
```

## Assessment Output

Generate `.claude/readiness-report.md`:

```markdown
# Django Parallelization Readiness Report

## Overall Score: X/100

## Dimension Scores
| Dimension | Score | Status |
|-----------|-------|--------|
| App Boundaries | X/20 | ✅/⚠️/❌ |
| Shared State | X/20 | ✅/⚠️/❌ |
| API Contracts | X/20 | ✅/⚠️/❌ |
| Test Infrastructure | X/15 | ✅/⚠️/❌ |
| Documentation | X/15 | ✅/⚠️/❌ |
| Migrations & Deps | X/10 | ✅/⚠️/❌ |

## Blockers (Must Fix)
1. [Critical issue]

## Risks (Should Fix)
1. [High-risk issue]

## Recommendations
1. [Improvement suggestion]

## Django-Specific Notes
- Apps suitable for parallel work: [list]
- Apps requiring sequential work: [list]
- Migration conflict risk: [assessment]

## Parallelization Potential
- Estimated parallel tracks: N
- Suggested app boundaries: [list]
- Sequential dependencies: [list]
```

## Remediation Actions

After assessment, apply fixes. See `references/remediation-checklist.md` for detailed steps.

### Quick Fixes (Do Immediately)

1. **Create .claude/ directory structure**
2. **Create/update CLAUDE.md** with Django conventions
3. **Add ruff/mypy config** if missing
4. **Document existing API endpoints**

### Structural Fixes (Plan Required)

1. **Split god apps** into smaller domain apps
2. **Refactor cross-app signals** into explicit service calls
3. **Add serializer type hints** and explicit fields
4. **Set up integration test harness**

## Infrastructure Setup

After remediation, set up orchestration:

```
project/
├── .claude/
│   ├── readiness-report.md    # Assessment results
│   ├── architecture.md        # System design
│   ├── tasks/                 # Task specs
│   └── contracts/             # Interface definitions
├── CLAUDE.md                  # Project conventions
├── pyproject.toml             # Dependencies & tool config
└── apps/
    ├── users/                 # Example: User domain app
    ├── orders/                # Example: Order domain app
    └── shared/                # Shared utilities only
```

See `references/infrastructure-setup.md` for setup scripts.

## Django-Specific Considerations

### Migration Coordination

When parallel agents modify models in different apps:
- Each agent works on a separate app with isolated migrations
- Use `--merge` only during integration phase
- Consider migration squashing before parallel work
- Document migration dependencies in task specs

### App Isolation Strategies

**Strong isolation (preferred):**
- Each agent owns entire app(s)
- Cross-app communication via services/APIs
- No direct model imports across boundaries

**Soft isolation:**
- Shared read-only models in `shared/` app
- Write operations only in owning app
- Explicit service layer for cross-app writes

### Signal Handling

- Avoid cross-app signals during parallel development
- Convert signals to explicit service calls
- Document signal side effects in contracts
