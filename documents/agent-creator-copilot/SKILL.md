---
name: agent-creator-copilot
description: Guide for creating custom agents for GitHub Copilot (cloud agent on GitHub.com, Copilot CLI, VS Code, and other IDEs). Use this when building custom agent profiles (.agent.md files), configuring tools, models, handoffs, subagents, hooks, or MCP server integrations for Copilot.
license: MIT
---

# Copilot Agent Creator

Custom agents for GitHub Copilot are defined in `.agent.md` Markdown files called **agent profiles**. They encode a role, behavioral instructions, tool access, and optionally a model, without requiring extension development. The same profile can be used by Copilot cloud agent on GitHub.com, GitHub Copilot CLI, VS Code, JetBrains IDEs, Eclipse, and Xcode, but some properties only work on some surfaces.

> [!IMPORTANT]
> This skill was last verified in October 2026 against GitHub Copilot CLI v1.0.98. Always verify against the official docs before relying on a property. The canonical references are:
>
> - [Custom agents configuration (GitHub)](https://docs.github.com/en/copilot/reference/custom-agents-configuration)
> - [Custom agents in VS Code](https://code.visualstudio.com/docs/agent-customization/custom-agents)
> - [Custom agent file reference (VS Code)](https://code.visualstudio.com/docs/agents/reference/custom-agent-file-reference)
> - [Copilot CLI custom agents reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference#custom-agents-reference)

---

## When to Use This Skill

- Creating a new custom agent profile for Copilot cloud agent, Copilot CLI, or VS Code
- Configuring tools, model, handoffs, subagents, hooks, or MCP servers in a profile
- Choosing the right scope (repository, user, organization, enterprise)
- Designing multi-agent workflows
- Writing effective agent prompts

---

## Quick Decision Guide

| Need | Approach |
|---|---|
| Persistent persona with tool restrictions | **Custom agent profile** (this skill) |
| One-off reusable task instructions | Prompt file (`.prompt.md`) |
| Portable domain knowledge with scripts | Agent skill (`SKILL.md`) |
| Deterministic command at a lifecycle event | Hook |
| Deep VS Code IDE integration, custom UI | VS Code extension |
| Custom tools exposed via protocol | MCP server |

---

## Agent Profile Format

```markdown
---
name: readme-creator
description: Agent specializing in creating and improving README files
tools: ["read", "search", "edit"]
---

You are a documentation specialist focused on README files. ...
```

`description` is the only required property (GitHub.com and Copilot CLI). In VS Code the YAML header is optional. The Markdown body holds the instructions and can be at most **30,000 characters**.

> [!TIP]
> For the full property reference and a per-surface compatibility table, load `references/frontmatter-reference.md`.

---

## Where to Store Agent Profiles

| Scope | Location | Surfaces |
|---|---|---|
| Repository / workspace | `.github/agents/<name>.agent.md` | All |
| Repository (Claude format) | `.claude/agents/<name>.md` | VS Code, Copilot CLI |
| User | `~/.copilot/agents/` | VS Code, Copilot CLI |
| User (Claude format) | `~/.claude/agents/` | VS Code |
| Organization | `agents/<name>.md` in the org's `.github` or `.github-private` repo | GitHub.com, IDEs (VS Code discovers them by default; `github.copilot.chat.organizationCustomAgents.enabled` set to `false` turns that off) |
| Enterprise | `agents/<name>.md` in the `.github-private` repo of an org designated in enterprise settings | GitHub.com, IDEs |
| Plugin | `<plugin>/agents/` | Copilot CLI |

VS Code's file-locations table lists `.agent.md` or `.md` files for `.github/agents` and `~/.copilot/agents`; prefer `.agent.md`. The **Local** harness stores user-level agents in VS Code profile storage instead, separate from `~/.copilot/agents` and `~/.claude/agents`; move them to the folder the selected harness reads to reuse them.

The filename (minus `.md` / `.agent.md`) is the agent's ID and is used for deduplication. On name conflicts the lowest (most specific) level wins: repository over organization, organization over enterprise.

> [!NOTE]
> In Copilot CLI, a user-level agent (`~/.copilot/agents/`) overrides a project agent with the same ID. The full priority order is in `references/frontmatter-reference.md`.

---

## Tools

```yaml
tools: ["read", "search"]          # specific tools (least privilege)
tools: ["*"]                       # all tools (same as omitting tools)
tools: []                          # no tools
tools: ["read", "my-server/*"]     # alias + all tools from an MCP server
```

Portable aliases: `execute`, `read`, `edit`, `search`, `agent`, `web`, `todo`. Unrecognized tool names are ignored, so one profile can list surface-specific tools. Apply least privilege: start read-only and add write/execute tools only when required.

> [!TIP]
> For the alias table, VS Code tool sets and tool names, MCP namespacing, and CLI behavior, load `references/tools-reference.md`.

---

## Model

```yaml
model: Claude Sonnet 5                     # VS Code / IDEs: display name
model: ["Claude Opus 5", "GPT-5.5"]        # VS Code: prioritized fallback list
model: gpt-5.6-luna                       # Copilot CLI: model ID
reasoning-effort: high                     # VS Code, Copilot harness: low | medium | high | xhigh | max
```

Model names differ by surface (display names in VS Code, lowercase IDs in the CLI) and the model roster changes often. Check the [supported models](https://docs.github.com/en/copilot/reference/ai-models/supported-models) page, including its retirement table, before pinning a model.

---

## Handoffs (VS Code / IDEs)

Ignored on GitHub.com's cloud agent. In VS Code they apply to the **Local** harness only. After a response, handoff buttons let the user switch to another agent with a pre-filled prompt.

```yaml
handoffs:
  - label: Start Implementation
    agent: implementation
    prompt: Implement the plan outlined above.
    send: false
```

---

## Subagents (VS Code and Copilot CLI)

In VS Code, a coordinating agent lists allowed subagents in `agents` and must include the `agent` tool:

```yaml
tools: ["agent", "read", "search"]
agents: ["Researcher", "Implementer"]   # ["*"] or omit = all, [] = none
```

- `user-invocable: false` hides an agent from the picker (subagent/programmatic use only).
- `disable-model-invocation: true` stops other agents (VS Code) or the cloud agent (GitHub.com) from auto-selecting it. In VS Code, explicitly listing the agent in a coordinator's `agents` overrides this.
- In Copilot CLI, the main agent can run any custom agent as a subagent by inference. Add `include-custom-instructions: true` if the subagent should read `AGENTS.md` / `copilot-instructions.md` / `CLAUDE.md`.

---

## Writing the Prompt Body

```markdown
# Agent Name

You are a [role] focused on [domain]. Your scope is limited to [specific boundaries].

## Responsibilities

- [What it does]
- [What it hands off, not handles]

## Constraints

- Do not modify [out-of-scope files/systems]
- When [situation], [action]
```

Key principles: state scope explicitly, use imperative language, define handoff conditions, stay well under 30,000 characters.

> [!TIP]
> For detailed principles, anti-patterns, and guidance on what NOT to include, load `references/prompt-writing-guide.md`.

---

## Creating an Agent Profile: Step-by-Step

### Step 1: Plan

1. Define the role and domain (one sentence)
2. List responsibilities and what it does NOT do
3. Choose the surfaces (`target`) and scope (repository, user, org)
4. Identify required tools, starting read-only

### Step 2: Create the File

**VS Code:**

1. Select the agent harness you intend to use with the **Session Target** control, then open the Agent Customizations editor: **Open Customizations** in the Chat view title bar (or the **Customizations** panel in the Agents window), then **Agents**
2. Select **New Agent** (plus icon) next to the **Workspace** or **User** group, or run **Chat: New Custom Agent** from the Command Palette
3. To generate one with AI, describe the agent in the editor's **Overview** section, or, in a **Local** harness session, type `/create-agent <description>` in chat

**GitHub.com (cloud agent):**

1. Go to [github.com/copilot/agents](https://github.com/copilot/agents), select the repository (and optionally branch) in the prompt box
2. Click the Copilot icon → **Create an agent** to open a `my-agent.agent.md` template in `.github/agents`
3. For org/enterprise agents, remove the `.github/` part of the path so the file lives in the root `agents/` directory
4. Rename, configure, commit, and merge into the default branch

**Copilot CLI:**

1. In interactive mode, enter `/agent` → **Create new agent**
2. Choose **Project** (`.github/agents/`) or **User** (`~/.copilot/agents/`)
3. Let Copilot generate the profile or fill it in manually, choose tools, then restart the CLI

**Manually:** create `.github/agents/<name>.agent.md`. Filename characters: `.`, `-`, `_`, `a-z`, `A-Z`, `0-9`. Prefer lowercase with hyphens.

### Step 3: Write Frontmatter

```yaml
---
name: api-reviewer
description: Reviews REST API designs for correctness and security. Does not implement code.
tools: ["read", "search"]
---
```

### Step 4: Write the Prompt Body

Follow the template above. Be specific about scope and handoff conditions.

### Step 5: Test

1. Select the agent: VS Code agents dropdown, GitHub.com agents panel or issue assignment, or `copilot --agent <name>` / `/agent` in the CLI
2. Run representative prompts covering normal use and edge cases
3. Verify scope boundaries and tool restrictions are respected
4. Confirm handoffs and subagent delegation work where used
5. In VS Code, check load errors in the chat customization diagnostics (right-click the Chat view → **Diagnostics**)

---

## Security Considerations

- **Least privilege for tools.** Read-only agents cannot accidentally modify files or run commands.
- **Review shared agents.** Audit tool lists and prompts before committing to a repository.
- **Secrets in MCP config.** Use `${{ secrets.NAME }}` / `${{ vars.NAME }}` (configured as Agents secrets/variables). Never hardcode credentials.
- **Organization and enterprise agents.** They are available to every repo in scope. Review them carefully.
- **Added directories (CLI).** Agents under a directory added with `--add-dir` load as trusted configuration.

---

## Reference Files

| File | When to Load |
|---|---|
| `references/frontmatter-reference.md` | Full property tables, surface compatibility, model naming, handoffs, hooks, MCP config, CLI-only fields, Claude format |
| `references/tools-reference.md` | Tool aliases, VS Code tool sets, MCP namespacing, out-of-the-box MCP servers |
| `references/prompt-writing-guide.md` | Detailed prompt principles, anti-patterns, output format guidance |
| `references/workspace-agent-example.agent.md` | VS Code workspace agent with handoffs and model fallback |
| `references/user-profile-agent-example.agent.md` | Minimal personal agent |
| `references/cloud-agent-with-mcp-example.agent.md` | GitHub.com cloud agent with MCP config and metadata |

---

## Official Documentation

| Resource | URL |
|---|---|
| About custom agents | <https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-custom-agents> |
| Create custom agents (cloud agent) | <https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/create-custom-agents> |
| Configuration reference | <https://docs.github.com/en/copilot/reference/custom-agents-configuration> |
| Custom agents for Copilot CLI | <https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/create-custom-agents-for-cli> |
| Copilot CLI custom agents reference | <https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference#custom-agents-reference> |
| Custom agents in VS Code | <https://code.visualstudio.com/docs/agent-customization/custom-agents> |
| Custom agent file reference (VS Code) | <https://code.visualstudio.com/docs/agents/reference/custom-agent-file-reference> |
| Subagents in VS Code | <https://code.visualstudio.com/docs/agents/run/subagents> |
| Supported AI models | <https://docs.github.com/en/copilot/reference/ai-models/supported-models> |
| Awesome Copilot agents | <https://github.com/github/awesome-copilot/tree/main/agents> |
