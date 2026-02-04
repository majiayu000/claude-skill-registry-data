---
name: justfile-maturity-model
description: Five-level maturity progression - assessment criteria, upgrade paths, YAGNI enforcement
---

# Justfile Maturity Model

Five levels. Start at 0. Add levels as needed. YAGNI enforcement.

## Levels

### Level 0: Baseline (EVERY project)

**Commands:** 9 required
- `default`, `dev-install`, `format`, `lint`, `typecheck`, `test`, `coverage`, `check-all`, `clean`

**Criteria:**
- All commands present (stub or implement)
- Exact comment strings
- check-all runs format → lint → typecheck → coverage
- `just check-all` succeeds or fails meaningfully

**When:** All projects, no exceptions

**Skill:** `justfile-interface`

### Level 1: Quality Gates (CI matters)

**Commands:** +4
- `test-watch` - Continuous test execution
- `integration-test` - Integration tests, no threshold, never blocks
- `complexity` - Detailed complexity report
- `loc` - Largest files by lines of code

**Criteria:**
- Test separation (unit vs integration)
- Integration tests marked/tagged
- Complexity reporting (informational, not blocking)

**When:**
- Setting up CI/CD
- Multiple developers
- Need fast feedback loop

**Skill:** `justfile-quality-patterns`

### Level 2: Security (Deploying)

**Commands:** +4
- `vulns` - Vulnerability scanning
- `lic` - License compliance
- `sbom` - Software bill of materials
- `doctor` - Environment health check

**Criteria:**
- Multi-tier scanning (critical/medium/high)
- License checking (prod vs dev separation)
- SBOM generation (CycloneDX format)
- Environment validation

**When:**
- Deploying to production
- Security requirements
- Compliance needs

**Skill:** `justfile-security-patterns`

### Level 3: Advanced (Production systems)

**Commands:** +6+
- `test-smart` - Git-aware test execution
- `deploy` - Deploy to environment
- `deploy-api`, `deploy-web` - Partial deploys
- `migrate` - Database migrations
- `logs` - Service logs
- `status` - Deployment health

**Criteria:**
- Git-aware testing (conditional execution)
- Deployment integration (cloud provider)
- Migration management
- Observability commands

**When:**
- Production deployment workflows
- Database-backed applications
- Cloud-native systems

**Skill:** `justfile-advanced-patterns`

### Level 4: Polyglot (Multi-language)

**Structure:** Root + subprojects

**Root commands:** Subset (orchestration)
- `dev-install`, `check-all`, `clean`, `build`, `deps`, `vulns`, `lic`, `sbom`
- Delegates to subprojects via `_run-all`

**Subproject commands:** Full interface
- Each subproject implements level 0+ independently

**Criteria:**
- Root orchestrates, doesn't duplicate
- Each subproject standalone (`cd api && just check-all`)
- `_run-all` fails fast
- Clean delegation pattern

**When:**
- Multiple languages (Python + JavaScript, etc.)
- Microservices architecture
- Monorepo structure

**Skill:** `justfile-polyglot-patterns`

## Assessment

### Check Current Level

**Level 0:**
```bash
# All 9 baseline commands present?
for cmd in default dev-install format lint typecheck test coverage check-all clean; do
  grep -q "^$cmd:" justfile || echo "Missing: $cmd"
done

# check-all correct?
grep -q "^check-all: format lint typecheck coverage$" justfile || echo "check-all wrong"

# Comments exact?
# (check against justfile-interface skill)
```

**Level 1:**
```bash
# Quality commands present?
grep -q "^test-watch:" justfile
grep -q "^integration-test:" justfile
grep -q "^complexity:" justfile
grep -q "^loc:" justfile
```

**Level 2:**
```bash
# Security commands present?
grep -q "^vulns:" justfile
grep -q "^lic:" justfile
grep -q "^sbom:" justfile
grep -q "^doctor:" justfile
```

**Level 3:**
```bash
# Advanced commands present?
grep -q "^test-smart:" justfile
grep -q "^deploy:" justfile
grep -q "^migrate:" justfile
```

**Level 4:**
```bash
# Polyglot structure?
test -f justfile && test -f api/justfile && test -f web/justfile
grep -q "_run-all" justfile
```

## Progression

### When to Stop

**Don't add level if:**
- Not using feature (no CI → skip level 1)
- No deployment → skip level 3
- Single language → skip level 4

**YAGNI applies.**

### Non-Linear Progression

Can add specific patterns without full level:

```bash
# At level 0, add test-smart only
/just-upgrade test-smart

# At level 1, add deployment only
/just-upgrade deploy
```

### Typical Paths

**Web application:**
0 → 1 → 2 → 3 (quality → security → deployment)

**Library:**
0 → 1 → 2 (quality → security, no deployment)

**Monorepo:**
0 → 1 → 4 → 2 → 3 (baseline → quality → polyglot → security → deployment)

**Solo project:**
0 → 2 (baseline → security, skip quality overhead)

## Upgrade Strategy

### Assess First

Always run `/just-assess` before upgrade. Shows:
- Current level
- Missing commands for current level
- Non-standard comment strings
- Recommended next level or patterns

### Incremental Addition

```bash
# Complete current level first
/just-assess
# Output: Level 0 (8/9 commands, missing: integration-test)

/just-refactor
# Adds missing baseline command

# Then upgrade
/just-upgrade 1
# Adds level 1 quality commands
```

### Pattern-Specific

```bash
# Add single pattern
/just-upgrade test-smart
# Adds test-smart from level 3, doesn't add full level 3

# Add multiple patterns
/just-upgrade test-smart deploy
# Adds both patterns
```

## Validation

Each level has success criteria:

**Level 0:** All baseline present, check-all works
**Level 1:** Test separation enforced, integration-test never blocks
**Level 2:** Security scans run, licenses checked
**Level 3:** Deployment works, migrations tracked
**Level 4:** All subprojects pass check-all independently

## Anti-Patterns

**Don't:**
- Skip level 0 (baseline non-negotiable)
- Add all levels (YAGNI)
- Mix implementations (pick one stack)
- Ignore exact comments (validation depends on these)
- Block on integration tests (always report-only)

**Do:**
- Complete current level before advancing
- Add patterns as needed
- Validate after each change
- Stub unimplemented commands
- Follow stack-specific implementations
