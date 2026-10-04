---
name: recruit
description: Analyze installed tools and existing assistant configurations to actively propose and create specialized LibrAgent assistants via agent__createAgent. Use when the user wants to recruit, create, or build a domain expert or specialist agent, utilizing a proactive "Architect" workflow that maps available inventory tools to functional gaps. Not for workspace agents.md (agent-init), teamwork/org, or registering MCP servers.
---

# Recruit (The Architect)

Create or propose **specialized assistant configurations** (specialists) by auditing the available tool inventory and analyzing gaps in the current assistant setup. 

Instead of passively asking the user what domain they want or waiting for exact specifications, **recruit** acts as an active **Architect** that maps installed tools to functional archetypes and proactively proposes tailored specialist configurations.

## Not This Skill

| Skill | Use for |
| --- | --- |
| **agent-init** | Generate `agents.md` / workspace guidelines |
| **teamwork** / **org** | Persistent multi-agent task forces |
| **delegate** | Spawn a child session with an existing assistant |
| **tool-installer** | Register external MCP servers |
| **boost** | Analyze and optimize **existing** assistants (audit, prune, or augment) |

## Three Layers (Do Not Mix)

| Layer | Examples | Set via `agent__createAgent`? |
| --- | --- | --- |
| **Core builtins** | `workspace`, `agent`, `tool`, `skills`, `scratchpad`, … | Always on — do not list redundantly |
| **Optional builtins** | `planning`, `browser`, `knowledge`, `setup-wizard`, `media`, `history` | `builtinCapabilities` — restricts/enables optional services |
| **External MCP** | GitHub, search, filesystem servers | `externalMcpServers` — **server IDs** from `tool__listServers`, not display names |
| **Bundled skills** | `docx`, `deep-research` | **Not** via `agent__createAgent` — suggest `@skill:name` separately |

---

## Workflow (Inventory-First Architect)

### 1. Inventory & Configs Audit

Before making proposals or asking the user questions, gather the system's current state:

1. **Audit Available Tools:**
   ```json
   tool__listServers({ "availability": "inventory" })
   ```
   Collect all external MCP servers (ID, display name, description) and optional builtins.

2. **Audit Existing Assistants:**
   ```json
   agent__listAgents({ "type": "configs" })
   ```
   Retrieve currently configured assistants to identify what roles are already covered.

### 2. Gap Analysis & Clustering (Implicit Logic)

Analyze the gathered inventory and existing configurations to identify gaps:

1. **Clustering:** Group available tools into **logical domains** (e.g., *DevOps/GitHub*, *Finance/Market Analysis*, *Research/Search*, *Document/Media Processing*). Do not propose specialists for individual, isolated tools unless they are highly specialized.
2. **Coverage Mapping:** Compare existing assistants against these clusters. (e.g., "We have a general Coding Expert, but we have a GitHub MCP server in inventory that isn't dedicated to a GitHub Specialist").
3. **Identify Gaps:** Find clusters that have powerful tools in the inventory but lack a specialized assistant to utilize them effectively.

### 3. Proactive Proposal Generation

Do **not** ask vague questions like "What kind of expert do you want?". Instead, present a structured proposal to the user:

* **Identify the Gap:** Point out which installed tools are currently underutilized.
* **Propose Specialists:** Suggest 1–2 specific specialist configurations.
* **Batch Mode Trigger:** If the inventory contains >5 distinct tool clusters, group proposals into a single batch summary (e.g., "I propose 3 specialists: DevOps, Research, and Finance") rather than asking one-by-one.
* **Draft Details:** For each proposed specialist, provide:
  - **Name:** (e.g., `GitHub Release Specialist`, `Exa Research Analyst`)
  - **Description:** A short description of its focus.
  - **Assigned Tools:** The specific optional builtins and MCP server IDs.
  - **Rationale:** Why this configuration is needed based on their inventory and current setup.

#### Example Proposal Format:
> Based on your tool inventory, I noticed you have the `github-mcp` server installed, but no dedicated GitHub assistant. I propose creating:
> 
> 1. **GitHub Specialist** (`agent__createAgent` proposal):
>    - **Description**: Manages pull requests, issues, and repository state.
>    - **MCP Servers**: `github-mcp` (ID: `cuid...`)
>    - **Builtins**: `["browser"]`
> 
> Would you like me to create this specialist?

### 4. Create the Assistant

Once the user approves or refines the proposal, execute the creation:

```json
agent__createAgent({
  "name": "GitHub Specialist",
  "description": "...",
  "systemPrompt": "...",
  "builtinCapabilities": ["planning", "browser"],
  "externalMcpServers": ["<mcp-server-id-from-inventory>"]
})
```

*Note: Ensure `externalMcpServers` contains only CUID IDs from `tool__listServers`, never display names or slugs. `planning` is optional — include it when the specialist needs goal/todo tools.*

### 5. Verification & Handoff

Confirm creation and instruct the user on how to initiate a session:

1. Verify:
   ```json
   agent__listAgents({ "type": "configs", "query": "<new name>" })
   ```
2. Inform the user of the new assistant's name and ID.
3. Provide instructions on starting a session: `agent__spawnSession(configId="...")` or via the UI.

---

## Guidelines

- **Active Proposing Over Asking:** Never respond to "make me an expert" with a blank question. Always audit the inventory first and propose a concrete specialist draft.
- **Evidence-Based Design:** Only attach MCP servers that are actually present in `tool__listServers` inventory.
- **English-Only System Prompts:** Write the `systemPrompt` in English for optimal LLM performance and token efficiency. The user-facing `description` can match the user's preferred language.
- **Minimal Tool Allocation:** Assign only the tools that are highly relevant to the specialist's domain. Do not over-provision tools, as it increases cognitive load and degrades performance.

## Builtin Tools

| Step | Tool |
| --- | --- |
| Inventory MCP + tools | `tool__listServers({ "availability": "inventory" })` |
| Find existing assistants | `agent__listAgents({ "type": "configs" })` |
| Create specialist | `agent__createAgent(...)` |
| Verify creation | `agent__listAgents({ "type": "configs" })` |
| Use specialist | `agent__spawnSession(configId="...")` |

## References

- [prompt-templates.md](references/prompt-templates.md) — system prompt skeletons

