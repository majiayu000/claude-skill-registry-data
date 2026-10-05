---
name: ha:boundaries
description: Analyze Home Assistant integration boundaries and coupling via Python import analysis (grep, python -c, pylint, hassfest). Use when checking cross-integration imports, validating manifest dependencies, before splitting integrations, or reviewing architecture.
effort: medium
argument-hint: [--assess|--fix]
allowed-tools: Read, Grep, Glob, Bash
---

# Home Assistant Integration Boundary Validation

Analyze integration dependencies to ensure clean separation between integrations,
the integration↔library boundary, and proper architectural layering.

## Usage

```
/ha:boundaries              # Check for violations
/ha:boundaries --assess     # Score integration health (0-100)
/ha:boundaries --fix        # Suggest fixes for violations
```

## `--assess` Mode: Integration Health Score

Evaluate overall boundary health with a quantified score.

### Metrics Calculated

| Metric | Healthy Range | Red Flag | Weight |
|--------|---------------|----------|--------|
| Files per integration | 4-15 | >20 or <3 | 20% |
| Public surface (helpers/const exports) | shared-only | single-use symbols | 15% |
| Fan-out (integrations imported) | 0-2 | >4 | 20% |
| Fan-in (integrations that import it) | 0-6 | >10 | 15% |
| Circular imports | 0 | >0 | 15% |
| Boundary violations (P11 / P4 / manifest) | 0 | >0 | 15% |

### Commands for Assessment

Use Glob to count `.py` files per integration directory under `homeassistant/components/*/`.
Use Grep to count the shared constants in `const.py` and cross-integration imports (its public surface — what other integrations reach for).
Run `grep -rn "homeassistant\.components\.awesome" homeassistant/components --include="*.py"` for reverse-dependency (fan-in) analysis, and `grep -n "^from \|^import " homeassistant/components/awesome/*.py` for fan-out.
Run `python3 -c "import homeassistant.components.awesome"` and `pylint --rcfile pyproject.toml homeassistant/components/awesome` (R0401) for circular-import detection.
Run `python3 -m script.hassfest --domain awesome` to validate manifest dependencies against actual imports.

### Output Format

```markdown
## Integration Health Assessment

### Overall Score: 82/100 (Good)

| Integration | Files | Surface | Fan-Out | Fan-In | Score |
|-------------|-------|---------|---------|--------|-------|
| awesome     | 8     | 3       | 0       | 0      | 95 |
| big_hub     | 24    | 12      | 5       | 3      | 62 |
| shared_base | 3     | 8       | 0       | 11     | 78 |

### Issues Found

1. **big_hub** - Too large (24 files, 9 platforms)
   - Consider: a new integration ships one platform, Bronze tier (PR2)

2. **big_hub** - High fan-out (5 integrations)
   - Consider: are all cross-integration imports declared in the manifest?

### Recommendations

- Move protocol/parsing code out of big_hub into its PyPI library (P11)
- Declare the `bluetooth` dependency in big_hub's manifest `dependencies`
```

## Iron Laws - Never Violate These

1. **Entry points read `coordinator.data`** - config-flow steps, entities, and service handlers never call the vendor library or do I/O directly; the coordinator owns the fetch
2. **The integration is thin** - protocol, transport, parsing, and device semantics live in a published PyPI library, not in the integration (P11)
3. **Integrations own their entities/coordinator** - don't import another integration's internal modules; import from the component root (CONTESTED #5)
4. **Explicit dependencies only** - cross-integration deps must be declared in manifest `dependencies`/`after_dependencies`
5. **DO NOT refactor integration boundaries without mapping imports first** — refactoring without the import graph creates new violations; run the grep / `python -c` / pylint / hassfest checks before moving code

## Dependency Rules

| Layer | Can Call | Cannot Call |
|-------|----------|-------------|
| Config flow / platform setup | Coordinator, `runtime_data`, HA helpers | Vendor library transport directly, blocking I/O |
| Entities | `coordinator.data`, `EntityDescription`, HA helpers | Direct I/O, vendor library protocol calls |
| Coordinator | The PyPI library, HA helpers | Web/entity internals of other integrations |
| PyPI library | Protocol / transport / parsing | HA internals (state class, entity concepts) — P11 runs both ways |

## Analysis Commands

### Check Integration Dependencies

Run `grep -n "^from \|^import " homeassistant/components/awesome/*.py` to see the full import surface, and `python3 -c "import homeassistant.components.awesome"` to confirm the graph resolves. For an optional visual graph, `pydeps homeassistant/components/awesome` (if `pydeps` is installed).

### Find What Depends on an Integration

Run `grep -rn "homeassistant\.components\.awesome" homeassistant/components --include="*.py" | grep -v "^homeassistant/components/awesome/"` — this reports every integration that imports into `awesome`, i.e. what depends on it.

### Find What an Integration Imports

Run `grep -rn "from homeassistant.components\." homeassistant/components/awesome --include="*.py" | grep -v "components.awesome"` to see the other integrations `awesome` depends on. For a single symbol (e.g. "who uses `AwesomeDataUpdateCoordinator`"), grep is module-granular — fall back to `grep -rn "AwesomeDataUpdateCoordinator" homeassistant tests --include="*.py"` or a small `ast`-based caller search (see the `call-tracing` skill) for function-level precision.

### Check for Circular Imports

Run `python3 -c "import homeassistant.components.awesome"` (a hard cycle raises ImportError / partially-initialized errors) and `pylint --rcfile pyproject.toml homeassistant/components/awesome` (R0401 cyclic-import).

## Red Flags to Detect

| Issue | Detection Command | Fix |
|-------|------------------|-----|
| Protocol/transport in the integration | `grep -rn "struct\.\|socket\.\|checksum\|payload" homeassistant/components/awesome --include="*.py"` | Move to the PyPI library (P11) |
| Blocking I/O on the event loop | `grep -rnE "def (async_\|_async)" homeassistant/components/awesome -A20 \| grep -E "open\(\|requests\.\|time\.sleep"` | Use the executor / an async library (P4) |
| Cross-integration deep import | `grep -rn "from homeassistant.components\.[a-z_]*\." homeassistant/components/awesome \| grep -v "components.awesome"` | Import from the component root (CONTESTED #5) |
| Undeclared manifest dependency | `grep -n "dependencies\|after_dependencies" homeassistant/components/awesome/manifest.json` + `python3 -m script.hassfest --domain awesome` | Declare the dependency in the manifest |

## Boundary Verification Process

1. Run `grep -n "^from \|^import " homeassistant/components/awesome/*.py` for the import overview (check fan-out and fan-in)
2. Check for cross-integration coupling (imports reaching into another integration's submodules)
3. Verify no direct vendor-library I/O from config-flow, entities, or platform setup (P4)
4. Ensure protocol/transport/parsing lives in the PyPI library, not the integration (P11)
5. Validate every cross-integration import is declared in the manifest (`dependencies`/`after_dependencies`) — confirm with hassfest

### Frontend Layering (ha-frontend, FS13)

For ha-frontend work, `src/components` must never import from `src/panels`;
domain/WebSocket logic lives in `src/data/<domain>.ts`, generic helpers in
`src/common`. Detect with:

```bash
grep -rn "from ['\"]\.\./panels\|from ['\"].*src/panels" src/components
```

## Delegate to import-analyzer Agent

For a full import-graph sweep with fan-in/fan-out, cross-integration coupling,
and manifest-dependency validation, delegate to the `import-analyzer` agent:

```
Agent(subagent_type: "import-analyzer", prompt: "Analyze import boundaries for homeassistant/components/awesome")
```

It runs the grep / `python -c` / pylint / hassfest checks and reports P11
library-boundary violations, CONTESTED #5 component-root import guidance, and
FS13 frontend layering (`components` never import from `panels`).

## Next Steps

Always end with actionable follow-up — findings without a plan
get lost:

```
- `/ha:plan` — Create a plan to fix violations (recommended for 3+ issues)
- `/ha:quick` — Fix a single boundary violation directly
- `/ha:review` — Review specific integrations for deeper issues
```

## References

For detailed patterns, see:

- `${CLAUDE_SKILL_DIR}/references/context-design.md` - Integration design principles
- `${CLAUDE_SKILL_DIR}/references/refactoring-boundaries.md` - Fixing boundary violations
