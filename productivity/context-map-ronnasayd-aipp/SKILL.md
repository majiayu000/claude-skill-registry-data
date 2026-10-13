---
name: context-map
description: "Generate a map of all files relevant to a task before making changes. Works from a short or vague task description: expands it into concrete search seeds, locates code with rag-rat / codebase-memory / serena, traces dependencies and tests, and outputs a reviewed context map. Use when user says 'context map', 'map the files for this task', 'what files will this change touch', or before any non-trivial change."
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.2.0"
---

# Context Map

Before implementing any changes, map the files the task touches. Input may be one vague sentence: expand it into seeds, find **anchors** (code the task most directly changes), then expand outward from them. Every path in the map must be verified; absence of search results is not proof of absence.

## Task

{{task_description}}

## Workflow

Tool per question: [tool-selection.md](references/tool-selection.md). Never `cat` whole files — outline first, read excerpts. Run independent searches in parallel.

| #   | Phase                | Action                                                                                                                                                                                                                                                                                                        | Gate                                                                      |
| --- | -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| 0   | Expand task          | No tools. Write down: nouns → candidate symbols; verbs → behaviors; synonyms/naming variants (snake/camel, plural, abbrev); layer guess (UI/API/service/data/config/infra/docs); task type (feature/fix/refactor/config/docs); unknowns                                                                       | seeds listed before any search                                            |
| 1   | Memory + orientation | Parallel: `memory_query`/`memory_search` on top 2-3 seeds (prior decisions, gotchas); `repo_brief`/`get_architecture` (scope with `path` if obvious); read `AGENTS.md`/`CLAUDE.md` rules for touched file types                                                                                               | constraints noted                                                         |
| 2   | Locate anchors       | `semantic_search`/`search_graph` per concept seed (parallel); `symbol_lookup`/`find_symbol` per exact name; `grep` literals (config keys, error messages, CLI flags, env vars)                                                                                                                                | 1-5 anchors; confirmed = hit by 2+ independent searches, else "uncertain" |
| 3   | Clarify if blocked   | `AskUserQuestion` (several → `grilling`), offering found candidates as options. Only when: anchors split across unrelated areas; zero anchors after synonyms; task type changes map materially. Otherwise state the assumption and continue                                                                   | no stalling on answerable defaults                                        |
| 4   | Expand from anchors  | Per anchor, parallel: dependents (`find_callers`/`trace_path inbound`, depth 2); dependencies (`trace_callees`/outbound, depth 1-2, keep only contracts the change could break); `impact_surface` on changed signatures; outline files for exact functions; string-level consumers; implementations           | public/exported/cross-module hits flagged; depth cut-off noted            |
| 5   | Tests                | `find_callers`/`trace_path inbound` with `include_tests: true`; name/path match (`test_<mod>`, `<mod>.test.*`, `__tests__/`, `tests/`); `grep` anchor names under test dirs                                                                                                                                   | none found → record "no coverage" as risk, never invent a test            |
| 6   | Reference patterns   | 1-3 existing implementations of the same kind of change: `semantic_search` on the **pattern** ("another hook that blocks on lint failure"), not the domain; `search_graph` by same label/decorator/base; `query_graph` for "all X that do Y"; prefer recent, most-imported                                    | patterns cited by path                                                    |
| 7   | Verify + assemble    | `check_index_coverage` or direct outline on every cited path (drop or mark "unverified"); `grep` anchor names/config keys in `*.json\|yaml\|toml\|md` (indexers skip them); fill risks from evidence; list Assumptions + Not Checked; fill [output-template.md](references/output-template.md); run validator | validator exits 0; Risk Assessment evidence-based                         |

### Phase 4 detail

- **String-level consumers**: the call graph misses tool names, config keys, CLI names referenced as strings (hooks, prompts, docs, `pyproject.toml` entry points). `search_code`/`grep` the anchor name, mode `files`.
- **Implementations/overrides**: `find_implementations` when the anchor is an interface, base class, or hook.
- Stop at depth 2 unless blast radius is still growing.

## Output

Fill [output-template.md](references/output-template.md): Task Interpretation, Files to Modify, Dependencies, Test Files, Reference Patterns, Prior Decisions / Gotchas, Risk Assessment, Not Checked. ≤ 10 rows per table, ranked by impact.

## Validation

Save the map (e.g. `context-map.md`) and run the gate before handing it over. Fix every ERROR; fix or justify every WARN.

```bash
python3 skills/context-map/scripts/validate_context_map.py context-map.md --root . [--strict]
```

Checks: required sections, exact table columns, no placeholder rows, valid `Task type:` + `Anchors:`, checkbox risks, cited paths exist. Exit 0 pass, 1 violations, 2 usage error.

Do not proceed with implementation until this map is reviewed.

## Reference files

| File                                                       | Contents                                                         |
| ---------------------------------------------------------- | ---------------------------------------------------------------- |
| [tool-selection.md](references/tool-selection.md)          | question → rag-rat / codebase-memory / serena tool table + rules |
| [output-template.md](references/output-template.md)        | verbatim map template the validator enforces                     |
| [validate_context_map.py](scripts/validate_context_map.py) | deterministic structure check for the finished map               |
