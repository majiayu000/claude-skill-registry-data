---
name: agent-tools-browsing
description: '**UTILITY SKILL** — Browse the tool names a runtime accepts in a custom agent''s `tools:` frontmatter and produce a validated, minimal allowlist; and how to invoke a runtime''s tools to get a task done. USE FOR: choosing or tightening an agent''s tools list; finding valid tool names for the Copilot CLI, VS Code Agent Host, extension host, or GitHub.com cloud agent; telling a conceptual alias apart from a concrete built-in; debugging an agent whose tools list is ignored, too broad, or too narrow; naming MCP server tools in an allowlist; designing read-only, implementer, reviewer, or orchestrator tool profiles; running a task that needs runtime tools, such as creating a nested session in the Agents window. DO NOT USE FOR: authoring the agent file itself, frontmatter keys other than `tools:`, installing MCP servers, or VS Code UI customization. INVOKES: file system tools, browse_tools.py. FOR SINGLE OPERATIONS: to validate one candidate list, run scripts/browse_tools.py check instead of loading this skill.'
metadata:
  version: 0.2.0
---

# Agent Tools Browsing

Two questions, one skill:

| Question | Axis | Workflow |
|---|---|---|
| Which tool names may go in an agent's `tools:` allowlist? | **allowlist** | [below](#workflow-pick-a-tools-allowlist) |
| Which tools do I call, and in what order, to get a task done? | **usage** | [below](#workflow-run-a-task-with-runtime-tools) |

Pick the axis first. They have different failure modes: a bad allowlist fails silently, while a bad procedure fails loudly but late.

## Why this needs a skill

The `tools:` field is runtime-local. The same list can be correct in one runtime and meaningless in another. Three traps cause most bad lists:

- **A conceptual alias and a concrete built-in are different surfaces.** `read` and `view` are not interchangeable spellings of one thing.
- **Unknown names are silently ignored**, so a typo widens the agent instead of narrowing it, with no error to notice.
- **`*` anywhere in the list grants every tool.** `["view", "*"]` is an unrestricted agent.

## Workflow: pick a `tools:` allowlist

### 1. Establish the runtime and the intent

Ask, or infer from the file being edited:

- Which runtime loads this agent file? `cli`, `agent-host`, `vscode`, or `github-copilot`.
- What may the agent do? One sentence, with a boundary. "Read and search the code" or "change files and run the tests".

If the runtime is unstated, ask. Guessing produces a list that is silently wrong.

### 2. Browse the valid names

```bash
python3 scripts/browse_tools.py runtimes
python3 scripts/browse_tools.py list --runtime cli
python3 scripts/browse_tools.py list --runtime vscode --kind alias
```

Each name shows its kind and an evidence tier: `shipped` (the runtime's own built-in agents use it), `documented` (vendor docs), `reported` (direct testing only), `rejected` (tested and has no effect).

Prefer `shipped` and `documented` names. Treat `reported` as advisory.

### 3. Start from a profile

```bash
python3 scripts/browse_tools.py profile --runtime cli --profile read-only --format yaml
```

Profiles: `read-only`, `read-only-with-shell`, `implementer`, `reviewer`, `orchestrator`, `research`. See [allowlist-profiles.md](references/allowlist-profiles.md) for the rationale and for how to tighten an existing list.

Treat a profile as a starting point, not the answer.

### 4. Validate before writing

```bash
python3 scripts/browse_tools.py check --runtime cli --names "view,search,edit,bash"
```

Exits 1 when it finds a problem. It flags unknown names, the `*` wildcard, advisory names, and names with no effect in that runtime.

### 5. Emit the block

Report the runtime, the final list, and anything the validator flagged. If a name was rejected, say which one and what replaced it.

## Workflow: run a task with runtime tools

Use this axis when the goal is to **do** something with a runtime's tools, not to allowlist them.

### 1. Find the scenario

```bash
python3 scripts/browse_tools.py scenarios --runtime agent-host
```

Each scenario is one procedure with its own gates and failure modes. Read the reference file for the one that matches the goal.

### 2. Follow the procedure

```bash
python3 scripts/browse_tools.py scenario agent-host-nested-session
```

The scenario file gives the steps, the gates to clear first, how to verify the result, and the pitfalls. Follow it in order — the steps are ordered by dependency, not by importance.

### 3. Verify

Each scenario ends with a verification step. Run it. A tool call that returns without error has not necessarily done what you asked.

### Host-provided tools

Some runtime tools are **host-provided**: the host registers them per session, and they are not nameable in an agent's `tools:` frontmatter. No agent file grants them. The scenario file says which kind a tool is. See [naming-rules.md](references/naming-rules.md) §7b.

## Examples

**Read-only Copilot CLI agent**

```yaml
---
name: locator
description: Inspects the codebase and answers questions without changing files.
tools: [view, search]
---
```

**The same intent in VS Code** — different names, because the vocabulary differs:

```yaml
tools: [read, search]
```

**A reviewer that may run the test suite** — the shell is the escape hatch, so it is not a containment boundary:

```yaml
tools: [view, search, bash]
```

**An orchestrator that delegates** — `task` is the CLI delegation tool, `agent` its VS Code and cloud-agent equivalent:

```yaml
tools: [view, search, edit, bash, task]
```

**Adding one MCP server tool**:

```yaml
tools: [view, search, github-mcp-server/get_commit]
```

**Creating a nested session in the Agents window** — a usage task, not an allowlist. See [references/usage/agent-host-nested-session.md](references/usage/agent-host-nested-session.md):

```json
{ "name": "create_session", "arguments": { "relationship": "currentSession", "title": "review-the-auth-flow", "prompt": "..." } }
```

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| The agent can still write files after you removed the write tools | `bash` can also write, or `*` is in the list | Remove `*`; remove the shell tool too |
| A tool in the list does nothing | The name is not valid for that runtime | Run `check` for the runtime and use a name it reports as `OK` |
| The list was ignored | The runtime rejects the whole file, or the file is not in a discovery path | Confirm the file location and the `tools:` key name |
| The agent has no tools at all | `tools: []`, or every name was rejected | Check the exit code of `check` |
| The request failed with too many tools | A VS Code request may carry at most 128 tools | Narrow the list, or use tool sets and `toolSearch` |

## MCP tool names

| Name form | Runtime | Grants |
|---|---|---|
| `serverName/toolName` | all | one tool from a configured MCP server |
| `serverName/*` | all | every tool from that server |
| `github/*`, `playwright/*` | `github-copilot` | the out-of-the-box cloud servers |
| `extensionName.some-extension/some-tool` | `vscode` | tools proxied by an installed extension |

A slash in a name always means MCP or extension, never a built-in. The script needs no MCP server: it reads a local vocabulary file, and it degrades to the local file if no server is configured.

## Rules that decide the answer

Full reasoning in [naming-rules.md](references/naming-rules.md). The short form:

- **Alias vs built-in.** The command reference's "Tool availability values" table documents `--available-tools` and `--excluded-tools`, not the agent `tools:` list. The CLI's own shipped agents use concrete built-ins such as `grep`, `glob`, `read_bash`, `lsp`, so both forms work there. Prefer an alias when one covers the capability.
- **`create` and `apply_patch`** are documented CLI built-ins that no shipped agent uses; `create` was reported as silently ignored. Use `edit`, which covers file creation.
- **`*` anywhere** means every tool. `tools: []` means no tools. Omitting `tools:` means every tool.
- **Case sensitivity**: `cli` and `agent-host` are case sensitive; `vscode` and `github-copilot` are not.
- **The Agent Host is not the extension host.** The Agent Host runs the Copilot SDK harness and speaks the CLI vocabulary; the extension host speaks the `category/tool` vocabulary.
- **Cloud agent gaps**: `todo` has no effect, and there is no local development context.

## Resources

| File | Purpose |
|---|---|
| [scripts/browse_tools.py](scripts/browse_tools.py) | `list`, `profile`, `check`, `mcp`, `scenarios`, and `scenario` modes |
| [references/runtime-vocabularies.yaml](references/runtime-vocabularies.yaml) | Machine-readable per-runtime vocabulary, evidence tiers, and profiles |
| [references/naming-rules.md](references/naming-rules.md) | The rules, the traps, and the reasoning behind them |
| [references/allowlist-profiles.md](references/allowlist-profiles.md) | Capability profiles and how to tighten an existing list |
| [references/usage/README.md](references/usage/README.md) | Usage-scenario catalog: how to invoke runtime tools to accomplish a task |
| [references/usage/catalog.yaml](references/usage/catalog.yaml) | Machine-readable scenario index |

## Guardrails

- Never emit a name that the `check` mode rejected without saying so.
- Never add `*` to a list that is meant to be scoped.
- Do not write the agent file unless asked. This skill produces the `tools:` value; `copilot-cli-agent-customization` owns the file.
- Do not install or configure MCP servers. Only name the tools the server already exposes.
- Prefer the narrowest list that satisfies the intent. A capability reachable through two names still needs both removed from a read-only agent.
- Do not invent a procedure. If no scenario covers the goal, say so and follow the runtime's own documentation instead of improvising a tool sequence.
- When a scenario's status is `reported` rather than `verified`, tell the reader which parts are unverified.

