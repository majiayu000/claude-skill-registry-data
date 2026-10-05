---
name: ha:techdebt
description: Analyze Home Assistant (Python) technical debt — duplicates, refactoring opportunities, ruff findings. Use when asked about code quality, cleanup, or what to improve.
effort: medium
---

# Technical Debt Detection

Find and eliminate duplicate code patterns, anti-patterns, and refactoring opportunities in Home Assistant integrations (Python).

## Iron Laws - Never Violate These

1. **Search before refactoring** - Understand full scope of duplication before extracting
2. **Three strikes rule** - Extract shared code only after 3+ duplications
3. **Prefer composition** - Use mixins, shared base entity classes, and helper functions over inheritance-heavy abstractions
4. **Test coverage first** - Ensure tests exist before refactoring duplicated code

## Analysis Checklist

### 1. Run ruff for Automated Detection

Run `ruff check . --output-format json` and parse the output.

Focus on:

- Design/complexity issues (`C901` mccabe complexity, `PLR0911`/`PLR0912`/`PLR0915` too-many-returns/branches/statements)
- Consistency issues (`N` pep8-naming, `I` import ordering)
- Dead code and untyped escapes (`F401`/`F841` unused import/variable, `ARG` unused arguments, `ANN401` `Any` annotations) — dead/commented-out code is Iron Law P10 and must be deleted, not flagged for later

Also run `jscpd homeassistant/components/<domain>` for a dedicated copy-paste/duplicate-code report (percentage duplicated, exact clone locations).

### 2. Find Repeated Coordinator Fetches

Use Grep to search for fetch logic living outside the coordinator — direct client/library calls (`await client.`, `hass.async_add_executor_job`, `session.get(`) repeated across `homeassistant/components/**/*.py` platform and entity files.
The coordinator should own the fetch; entities read `coordinator.data`. Repeated fetches in multiple entities are the primary duplication smell (P11: library owns protocol, coordinator owns fetch).

### 3. Find Duplicate Entity Descriptions & Validators

Use Grep with `output_mode: "count"` to count `EntityDescription` subclass instantiations (`SensorEntityDescription(`, `BinarySensorEntityDescription(`, ...) in `homeassistant/components/**/*.py` — near-identical descriptions belong in one shared tuple.
Use Grep to find repeated voluptuous validators (`vol.Required`, `vol.Optional`, `cv.string`, `vol.Range`) that recur across `config_flow.py`, `services.py`, and schema modules — extract to a shared schema constant.

### 4. Find Copy-Pasted Service Handlers & Platform Setup

Use Grep to find repeated service registrations (`hass.services.async_register(`) and near-identical platform boilerplate (`async_setup_entry`, `async_add_entities`) across `homeassistant/components/**/*.py`.
Service actions should be registered once in `async_setup` (a `services.py` module — P18); repeated platform setup usually wants a shared entity base class.

## Common Duplication Patterns

| Pattern | Symptom | Solution |
|---------|---------|----------|
| Repeated fetches | Same client/library call in multiple entities or platforms | Centralize in the `DataUpdateCoordinator`; entities read `coordinator.data` (P11) |
| Duplicate entity descriptions | Same `EntityDescription` fields copied per entity | Extract to a module-level tuple of descriptions / shared base description |
| Repeated voluptuous validators | Same `vol.Required`/`cv.string` combos on every schema | Extract to a shared schema constant or `cv` helper |
| Similar platforms/services | Copy-pasted `async_setup_entry` or service handlers | Extract a shared entity base class; register services once in `services.py` (P18) |
| Repeated transforms | Same comprehensions / `.get()` chains | Extract to a helper function |
| Long functions/files | Methods or files exceeding ~400 lines, deep nesting (`C901` violations) | Split by responsibility; extract private helper methods |
| God coordinator/module | One coordinator or module doing unrelated things | Split by responsibility (see `integration-architecture` skill) |
| Dead / commented-out code | `ruff F401`/`F841`; grep commented-out blocks, restated framework defaults, unused translation keys | Delete now — Iron Law P10 (dead, unused, commented-out code is never allowed) |
| Stale TODO/FIXME | Grep for `TODO`/`FIXME`/`HACK` comments with no tracking issue | Convert to a tracked task or resolve now |

## Reporting Format

For each duplication found, report:

1. **Location**: File paths and line numbers
2. **Pattern**: What code is duplicated
3. **Extraction**: Suggested shared function / coordinator / entity description / schema
4. **Effort**: Low/Medium/High to fix

## Usage

Run `/ha:techdebt` to analyze the codebase and generate a prioritized report of technical debt with specific remediation steps.
