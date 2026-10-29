---
name: agentic-radar
description: "Map an agentic workflow's attack surface from source: agents, tools, edges between them, reachable resources and prompts, as an HTML report or graph JSON. Use before running a CrewAI, LangGraph, n8n, OpenAI Agents or AutoGen app you did not write. Not for live prompt probing (use garak) or model-file inspection (use model-file-audit)."
---

# Agentic Radar

Agentic Radar is SPLX's static analyser for agent workflows. It parses framework source, builds a graph of agents and tools, annotates the tools by capability category, and writes a report of what the agent can reach. The value is timing: you learn that a tool reads arbitrary files and another posts to a URL before the agent runs, not after it exfiltrates something.

This host has `agentic-radar` 0.14.1 at `~/.local/bin/agentic-radar`. The command surface changed from older releases: there is no `-d`, `--output` or `--format`. The current interface is `agentic-radar scan <framework> -i <dir> -o <file>`.

## When to use

| Goal | Command | Note |
| --- | --- | --- |
| Map a CrewAI project | `scan crewai -i ./src` | Python source in the input dir |
| Map a LangGraph app | `scan langgraph -i ./src` | graph nodes and conditional edges |
| Map n8n export | `scan n8n -i ./workflows` | JSON workflow files |
| Map OpenAI Agents SDK | `scan openai-agents -i ./src` | handoffs and tool bindings |
| Map AutoGen | `scan autogen -i ./src` | group chat topology |
| Reuse the graph in another tool | `--export-graph-json` | nodes, edges, agents, tools as JSON |
| Harden detected system prompts | `--harden-prompts` | sends prompts to a hosted model |
| Run the agent under test harnesses | `test <framework> "<cmd>"` | needs `OPENAI_API_KEY` |

Do not use it for: a live endpoint (there is nothing to parse), a model file, or a repository with no agent framework - it will report that no workflow was found.

## Prerequisites

- `agentic-radar --version` prints `SPLX Agentic Radar Version: 0.14.1`.
- Python 3.12 pipx venv. Framework packages are not required for scanning, but the tool warns `crewai_tools is not installed` / `CrewAI package is not installed` and then skips agent metadata enrichment. The graph of tools and edges is still produced.
- Source must be readable on disk. It does not execute the project; `test` does, and that is a separate command.
- Environment overrides exist for every scan option: `AGENTIC_RADAR_INPUT_DIRECTORY`, `AGENTIC_RADAR_OUTPUT_FILE`, `AGENTIC_RADAR_EXPORT_GRAPH_JSON`, `AGENTIC_RADAR_HARDEN_PROMPTS`.
- `--harden-prompts` and `test` require `OPENAI_API_KEY` or `AZURE_OPENAI_API_KEY` in the environment or a `.env` file.

## Core invocations

```sh
# 1. identity and command surface
agentic-radar --version
agentic-radar --help
agentic-radar scan --help

# 2. the standard first pass: framework, source dir, named report
agentic-radar scan crewai -i ./agent-src -o ./radar-crewai.html

# 3. LangGraph, written to an explicit path outside the analysed tree
agentic-radar scan langgraph -i ./app -o /tmp/radar-langgraph.html

# 4. OpenAI Agents SDK and AutoGen
agentic-radar scan openai-agents -i ./src -o /tmp/radar-oai.html
agentic-radar scan autogen -i ./src -o /tmp/radar-autogen.html

# 5. n8n workflow exports (JSON, not Python)
agentic-radar scan n8n -i ./n8n-workflows -o /tmp/radar-n8n.html

# 6. machine-readable graph instead of HTML
agentic-radar scan crewai -i ./agent-src -o /tmp/graph.json --export-graph-json
python3 -c "import json;d=json.load(open('/tmp/graph.json'));print(d.keys());print([n['name'] for n in d['nodes']])"

# 7. inspect the tool inventory and its categories from the graph
python3 -c "import json;d=json.load(open('/tmp/graph.json'));[print(t['name'], '->', t['category']) for t in d['tools']]"

# 8. inspect per-node vulnerability annotations
python3 -c "import json;d=json.load(open('/tmp/graph.json'));[print(n['name'], n['vulnerabilities']) for n in d['nodes'] if n['vulnerabilities']]"

# 9. default report name when you omit -o (timestamped, written to cwd)
mkdir -p /tmp/radar-out && cd /tmp/radar-out && agentic-radar scan langgraph -i /path/to/app

# 10. prompt hardening pass, which is the only mode that leaves the box
OPENAI_API_KEY=... agentic-radar scan crewai -i ./agent-src -o /tmp/hardened.html --harden-prompts

# 11. dynamic test harness for a runnable workflow (executes the app)
agentic-radar test crewai "python crew.py --dry-run" -c ./radar-test.yaml

# 12. environment-driven run, useful inside CI
AGENTIC_RADAR_INPUT_DIRECTORY=./agent-src AGENTIC_RADAR_OUTPUT_FILE=/tmp/ci-radar.html \
  agentic-radar scan openai-agents
```

The output file name is whatever you pass to `-o`. If it ends in `.html` while `--export-graph-json` is set, the report name is rewritten to `.json`; that rewrite is why you see JSON on disk with an `.html` argument.

## Flags that matter

| Flag | Command | Effect |
| --- | --- | --- |
| `<framework>` | scan, test | positional: `langgraph`, `crewai`, `n8n`, `openai-agents`, `autogen` |
| `-i, --input-dir` | scan | source directory, default `.` |
| `-o, --output-file` | scan | report path, default `report_<timestamp>.html` |
| `--export-graph-json` | scan | emit graph JSON and exit without the HTML report |
| `--harden-prompts` | scan | rewrite detected system prompts with a hosted model; needs a key |
| `-c, --config` | test | YAML test-suite definition |
| `<entrypoint>` | test | shell-quoted command that runs the workflow, with its args |

There is no `--format`, no `-d`, and no `--output`. If a document shows them, it predates 0.14.

**What the graph contains.**

- `nodes`: typed entries - `basic` for START/END, `agent` for an LLM actor, `tool` for a bound capability. Each carries `name`, `label`, `category` and a `vulnerabilities` list.
- `edges`: directed links with a `condition`. A `tool_call` edge from an agent to a tool is the capability grant; a tool-to-agent edge is the return path.
- `agents`: agent metadata when the framework package is importable, empty otherwise.
- `tools`: the capability inventory with a `category` such as `document_loader`, which is how a `FileReadTool` becomes visible as filesystem reach.

The HTML report renders the same graph plus vulnerability mappings, so it is the artefact to hand to a reviewer; the JSON is what you script against.

## Workflow

1. **Locate the source, not the repo root.** Point `-i` at the directory that holds the agent definitions. Whole-repo scans dilute the graph and slow the parse.
2. **Scan each framework separately.** A monorepo with a LangGraph service and a CrewAI service needs two runs with two output files.
3. **Read the tool inventory first.** Names and categories tell you what the agent can touch: filesystem, HTTP, shell, database, browser.
4. **Follow the edges.** An agent with a file reader is interesting; an agent with a file reader that feeds an HTTP tool is a data-exfiltration path.
5. **Check prompt provenance.** Prompts assembled from user input or from retrieved documents are the injection entry point; note where the concatenation happens in source.
6. **Compare graph to intent.** Anything reachable that the design never mentions - a default tool, a debug tool, a sub-agent with shell - is the finding.
7. **Only then run the app.** Do not start an agent with shell or filesystem tools until the graph says that is intended.
8. **Re-run after changes.** The scan is cheap; treat it as a pre-flight check, not a one-off audit.

## OPSEC and telemetry

- Scanning is local and static. Nothing is executed and nothing leaves the host in a plain `scan`.
- `--harden-prompts` sends detected system prompts to OpenAI or Azure OpenAI. That is a disclosure of your target's prompt text; use it only with authorization and a private endpoint.
- `test` executes the workflow, which means it will make the app's own network calls and may spend real tokens. Treat it as running the untrusted code.
- Reports embed file paths, agent names, prompt fragments and tool names. Keep them out of shared caches and public issues.
- Default report names are timestamped and land in the current directory; scanning in a repo root leaves artefacts in the tree.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| `No such option: -d` | older CLI syntax | use `scan <framework> -i <dir> -o <file>` |
| `didn't find any agentic workflow in input directory` | wrong framework or wrong directory | confirm the framework, point `-i` at the file that defines the agent |
| `crewai_tools is not installed` warnings | enrichment packages absent | graph still valid; install the framework only if you need agent metadata |
| Report written to a timestamped name | `-o` omitted | always pass `-o` |
| `--harden-prompts` exits with an auth error | no `OPENAI_API_KEY` or `AZURE_OPENAI_API_KEY` | export a key or drop the flag |
| `test` hangs | the entrypoint script waits for input or a server | run the entrypoint by hand first, pass non-interactive args |
| JSON missing when `-o` ended in `.html` | `--export-graph-json` rewrites the extension | look for the `.json` sibling |

## Verification

```sh
agentic-radar --version
# SPLX Agentic Radar Version: 0.14.1

agentic-radar scan crewai -i ./agent-src -o /tmp/radar.html
# "Report /tmp/radar.html generated"

agentic-radar scan langgraph -i ./agent-src -o /tmp/lg.html
# "Agentic Radar didn't find any agentic workflow in input directory" - wrong framework

ls -l /tmp/radar.html
# non-trivial HTML (hundreds of KB), containing the graph and vulnerability section
```

Evidence to keep: framework, input directory, report path, and the tool/edge list you based decisions on.

## Related skills

- [ai-security-testing](../ai-security-testing/SKILL.md) for the wider AI-target triage flow
- [garak](../garak/SKILL.md) when the agent is running and the question is behavioural
- [snyk-agent-scan](../snyk-agent-scan/SKILL.md) when the agent surface is installed on the host rather than in this source tree
- [model-file-audit](../model-file-audit/SKILL.md) for the artefacts the workflow loads
