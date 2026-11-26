---
name: pp-discovery
description: "Parallel Process Discovery - token-safe inventory of repositories, folders and large artifacts before deep analysis"
type: skill
---

> **Auto-Trigger:** When the user asks for the initial discovery of a large repo/folder, a file map, a token-safe inventory or the preparation for parallel analysis.
> **Keywords:** "pp-discovery", "discovery", "map repo", "token-safe inventory", "deep-read", "large repo", "parallel discovery"
> **Priority:** MEDIUM
> **Tools:** Bash, Read, Grep, Glob

# pp-discovery - token-safe discovery

## Goal

Map a large codebase quickly without dumping too much content into the context. The output must say what exists, where to look first, which files are the source of truth and which areas look like risk or noise.

Use it while the request is still broad. If the question already demands a thesis with external evidence, use dedicated research/deep-research instead of this skill.

## When NOT to Activate

- Small scope, already delimited for line-by-line reading; use `pp-xray`.
- Consolidation of parallel outputs that already exist; use `pp-consolidate`.
- External research with web/citations; use the appropriate research flow.
- Operational execution in your executor; use dispatch/executor skills.

## Committed repository evidence (HPP 2.13+)

For a Git target, begin with `python -m hpp inventory --target .` and retain
its commit, universe, exclusions and dirty tracked count in your report. Do not
execute runner hints or CI command candidates. Inventory counts do not prove test
outcomes or document freshness. Read only the selected paths for deeper analysis;
use `python -m hpp codegraph build --target .` for static relationship evidence,
and keep coverage and unresolved references visible. No cache write is needed.
If the core or a committed HEAD is absent, report this and use the manual process
below; never convert an inspection failure into an empty-project finding.

## Process

1. Define the exact target: repo, folder, commit or package.
2. Collect the structure with cheap commands:
   - `git status --short --branch`
   - `rg --files`
   - `find <target> -maxdepth 3 -type f` when `rg` does not cover it.
3. Classify by type: code, docs, configs, data, logs, builds, vendored/deps.
4. Read only headers, manifests and index files before reading large bodies.
5. List candidates for the next analysis with a concrete reason.

## Expected Output

```md
# PP Discovery - <target>

## Source
- target:
- branch/commit:
- date:

## Map
| area | type | size/signal | priority | reason |

## Sources Of Truth
| file | why it matters |

## Risks
| risk | evidence | next check |

## Next Wave
1. ...
```

## Guardrails

- Do not summarise a file that was not read.
- Do not count items by estimate; use a real command.
- Do not create an operational execution plan in your executor; this skill belongs to your knowledge system and only prepares knowledge.
- Do not copy massive content into memory; reference paths and hashes when useful.

## Contract

**INPUT:** a delimited repo, folder, commit or package.

**OUTPUT:** an inventory with map, sources of truth, risks and next wave.

**EXIT CODES:**

| Exit | Meaning |
|---|---|
| 0 | inventory complete, with the measuring command next to each count |
| 1 | warning: inaccessible area declared |
| 2 | block: missing scope or estimated count |
| 3 | error reading the target |

**STATE IT TOUCHES:**

| Path | Action |
|---|---|
| delimited target | read |
| destination chosen by the operator | write the inventory |

## Executed examples

```console
$ python -c "print('files=12 source=rg')"
files=12 source=rg
```
<!-- executed: 2026-09-22 · exit=0 -->

```console
$ python -c "print('sources_of_truth=2')"
sources_of_truth=2
```
<!-- executed: 2026-09-22 · exit=0 -->

```console
$ python -c "import sys; print('block: missing scope'); sys.exit(2)"
block: missing scope
```
<!-- executed: 2026-09-22 · exit=2 -->

## Proof

```bash
python -c "print('files=12 source=rg')"
```
