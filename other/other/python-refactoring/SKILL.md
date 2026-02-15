---
name: python-refactoring
description: "Python refactoring catalog with 83 patterns covering immutability, class design, control flow, architecture, OO metrics, and Python idioms. Analyze code for smells and apply numbered refactoring patterns with before/after examples. Use when the user invokes /refactor or explicitly asks to refactor, clean up, or improve Python code quality."
---

# Python Refactoring Skill

83 refactoring patterns from Contieri's series, Fowler's catalog, OO metrics literature, and Python idioms.

## Modes

**Active Analysis** (default when given code): Identify smells -> map to patterns -> load relevant references -> apply refactorings with before/after -> note trade-offs.

**Reference Lookup** (when asked about a pattern by number/name): Load the relevant reference file -> present the pattern.

## Smell-to-Pattern Map

| Code Smell | Patterns | File |
|---|---|---|
| Setters / half-built objects | SC101, SC104 | state.md |
| Mutable default args | SC701 | idioms.md |
| Unprotected public attributes | SC103 | state.md |
| Magic numbers / constants | SC601 | hygiene.md |
| Variables that never change | SC102 | state.md |
| Boolean flags for roles/states | SC105 | state.md |
| Stale cached/derived attributes | 030 | state.md |
| Long function, multiple concerns | SC201, 010 | functions.md |
| Comments replacing code | 005 | functions.md |
| Comments explaining what code does | 011 | hygiene.md |
| Generic names (result, data, tmp) | SC202 | functions.md |
| Duplicated logic | SC606 | hygiene.md |
| Near-duplicate functions | 050 | functions.md |
| Long related parameter lists | SC206, 052 | functions.md |
| Query + modify in same function | SC207 | functions.md |
| Static functions hiding deps | 020 | functions.md |
| `input()` in business logic | SC203 | functions.md |
| Getters exposing data | 027 | functions.md |
| Need to test private methods | 037 | functions.md |
| Unused function parameters | SC208 | functions.md |
| Long lambda expressions | SC209 | functions.md |
| Type-checking if/elif chains | SC302 | types.md |
| `isinstance()` dispatch | 060 | idioms.md |
| Dicts as objects (stringly-typed) | 012 | types.md |
| Raw primitives with implicit rules | 019, 044 | types.md |
| Raw lists, no domain meaning | 038 | types.md |
| Boilerplate `__init__/__repr__/__eq__` | SC304 | idioms.md |
| Related functions without a class | SC301 | types.md |
| Sibling classes with duplicate behavior | 022 | types.md |
| Inheritance without "is-a" | 023 | types.md |
| Constructor needs descriptive name | 048 | types.md |
| Scattered `None` checks | 015, SC204 | types.md |
| Lazy class (too few methods) | SC306 | types.md |
| Temporary fields (used in few methods) | SC307 | types.md |
| Deep nesting | SC402 | control.md |
| Imperative loops with accumulation | SC403 | control.md |
| Complex boolean expressions | SC404 | control.md |
| Long expressions, no named parts | 043 | control.md |
| Loop doing two things | 046 | control.md |
| Parse/compute/format mixed | 047 | control.md |
| Clunky algorithm | 049 | control.md |
| Boolean flag controlling loop | SC405 | control.md |
| Complex if/elif dispatch | 056 | control.md |
| Related statements scattered | 053 | control.md |
| Missing default else branch | SC407 | control.md |
| Complex comprehensions | SC406 | control.md |
| Singleton / global state | SC303, SC106 | architecture.md |
| Same exception for biz + infra | 035 | architecture.md |
| Chained `.attr.attr.attr` | SC502 | architecture.md |
| No fail-fast assertions | 045 | architecture.md |
| Dead code / commented blocks | SC401 | hygiene.md |
| Unused exceptions | SC602 | hygiene.md |
| Empty catch blocks | SC605 | hygiene.md |
| Giant regex | 025 | hygiene.md |
| Excessive decorators | SC205 | hygiene.md |
| String concatenation for multiline | SC603 | hygiene.md |
| Inconsistent formatting | 032 | hygiene.md |
| Cryptic error messages | 031 | hygiene.md |
| Sequential IDs leaking info | SC107 | architecture.md |
| Error codes instead of exceptions | SC501 | architecture.md |
| Blocking calls in async functions | SC703 | idioms.md |
| Manual try/finally cleanup | SC702, SC604 | idioms.md |
| Full lists when streaming works | 059 | idioms.md |
| Indexing tuples by position | SC305 | idioms.md |
| Shotgun surgery (wide call spread) | SC505 | architecture.md |
| Deep inheritance tree | SC308 | types.md |
| Wide hierarchy (too many subclasses) | SC309 | types.md |
| Inappropriate intimacy | SC506 | architecture.md |
| Speculative generality (unused ABCs) | SC507 | architecture.md |
| Unstable dependency | SC508 | architecture.md |
| Low class cohesion (LCOM) | SC801 | metrics.md |
| High coupling between objects (CBO) | SC802 | metrics.md |
| Excessive fan-out | SC803 | metrics.md |
| High response for class (RFC) | SC804 | metrics.md |
| Middle man (excessive delegation) | SC805 | metrics.md |

## Reference Files

Load **only** the file(s) matching detected smells:

- `references/state.md` -- Immutability, setters, attributes (SC101, SC102, SC103, SC104, SC105, 030)
- `references/functions.md` -- Method extraction, naming, parameters, CQS (SC201, 005, SC202, 010, 020, SC203, 027, SC206, 037, SC207, 050, 052, SC208, SC209)
- `references/types.md` -- Class design, reification, polymorphism, nulls (SC301, 012, SC302, 015, 019, 022, 023, SC204, 038, 044, 048, SC306, SC307, SC308, SC309)
- `references/control.md` -- Guard clauses, pipelines, conditionals, phases (SC402-SC404, 043, 046, 047, 049, 053, SC405, 056, SC406, SC407)
- `references/architecture.md` -- DI, singletons, exceptions, delegates (SC303, SC106, SC107, 035, 045, SC501, SC502, SC505, SC506, SC507, SC508)
- `references/hygiene.md` -- Constants, dead code, comments, style (SC601, SC602, 011, SC606, SC401, 025, 031-032, SC205, SC603, SC605)
- `references/idioms.md` -- Context managers, generators, unpacking, protocols, async (SC701, SC702, SC703, 059, 060, SC304, SC305, SC604)
- `references/metrics.md` -- OO metrics: cohesion, coupling, fan-out, response, delegation (SC801, SC802, SC803, SC804, SC805)

## Automated Smell Detector

`scripts/detect_smells.py` runs the smell detector with 56 automated checks (41 per-file + 10 cross-file + 5 OO metrics). It ships with a bundled copy of the smellcheck package — no pip install required.

```bash
# Works immediately after skill install — no pip required
python3 scripts/detect_smells.py src/
python3 scripts/detect_smells.py myfile.py --format json

# Look up rule documentation (description + before/after example)
python3 scripts/detect_smells.py --explain SC701
python3 scripts/detect_smells.py --explain SC4    # list a family
python3 scripts/detect_smells.py --explain all    # list all rules

# Caching (enabled by default — skips unchanged files on repeat scans)
python3 scripts/detect_smells.py src/ --no-cache       # fresh scan
python3 scripts/detect_smells.py --clear-cache         # purge cache

# Or use the pip-installed CLI directly
pip install smellcheck
smellcheck src/ --min-severity warning --fail-on warning
```

**Per-file detections** (41): SC101 setters, SC201 long functions, SC601 magic numbers, SC602 bare except, SC202 generic names, SC301 extract class, SC102 UPPER_CASE without Final, SC103 public attrs, SC302 isinstance chains, SC104 half-built objects, SC105 boolean flags, SC303 singleton, SC401 dead code after return, SC106 global mutables, SC203 input() in logic, SC107 sequential IDs, SC204 return None|list, SC205 excessive decorators, SC206 too many params, SC603 string concatenation, SC402 deep nesting, SC403 loop+append, SC207 CQS violation, SC404 complex booleans, SC501 error codes, SC502 Law of Demeter, SC405 control flags, SC701 mutable defaults, SC702 open without with, SC703 blocking calls in async, SC304 dataclass candidate, SC305 sequential indexing, SC604 contextlib candidate, SC210 cyclomatic complexity, SC208 unused parameters, SC605 empty catch block, SC209 long lambda, SC406 complex comprehension, SC407 missing else, SC306 lazy class, SC307 temporary field.

**Cross-file detections** (10): SC606 duplicate functions (AST-normalized hashing), SC503 cyclic imports (DFS), SC504 god modules, SC211 feature envy, SC505 shotgun surgery, SC308 deep inheritance, SC309 wide hierarchy, SC506 inappropriate intimacy, SC507 speculative generality, SC508 unstable dependency.

**OO metrics** (5): SC801 lack of cohesion, SC802 coupling between objects, SC803 fan-out, SC804 response for class, SC805 middle man.

Run the detector first for a quick scan, then use the reference files to understand and apply the suggested refactorings.

## Workflow

1. Optionally run `detect_smells.py` on the target code for automated findings
2. Receive code -> scan for smells using table (manual or from script output)
3. Map smells to pattern numbers
4. Read **only** the relevant reference file(s)
5. Present: "Found N smells -> applying SCxxx, SCyyy, SCzzz"
6. Show refactored code with explanations
7. Note trade-offs and breaking changes

## Guidelines

- Prioritize structural refactorings over cosmetic
- Preserve existing tests -- refactoring changes structure, not behavior
- Group related changes when multiple patterns apply
- Flag changes to public API (breaking vs non-breaking)
- For large code, suggest incremental order rather than all-at-once
- When patterns conflict, explain the trade-off and recommend
