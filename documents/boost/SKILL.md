---
name: boost
description: Audit and optimize existing LibrAgent assistant configurations by adding role-appropriate tools and pruning unrelated, bloated, or redundant ones. Use when the user wants to boost, audit, tune, clean up, or optimize existing specialists (e.g. removing github from a finance agent, or adding search to a researcher). Not for creating new assistants.
---

# Boost (The Optimizer)

Audit and refine existing assistant configurations by comparing each agent's role (system prompt and description) to its attached tools. 

Instead of just blindly adding missing tools, **boost** operates as an **Optimizer** that prevents **Tool Bloat** by recommending both additions (**Add**) of missing essential tools and removals (**Remove**) of unnecessary or conflicting tools.

## Not This Skill

| Skill | Use for |
| --- | --- |
| **recruit** | Create a **new** specialist when none exists |
| **tool-installer** | Register or import MCP servers that are not in inventory yet |
| **skill-deployer** | Install or manage bundled skills (`docx`, `deep-research`, etc.) |
| **agent-init** | Generate workspace `agents.md` |
| **libragent-harness-reference** | LibrAgent prompt layers / session isolation facts |

## Critical API Rules

### `externalMcpServers` replaces the full list

`agent__updateAgent` **replaces** the `externalMcpServers` array entirely — it does not merge it.

When proposing updates:
* **Add:** Add the new tool IDs to the existing list.
* **Remove:** Filter out the bloated tool IDs from the existing list.

Compute the final list precisely:
```
next_external = (current_externalMcpServers + recommended_add_ids) - recommended_remove_ids
```
Never send only the added tools, or you will accidentally delete all pre-existing tools.

### Server IDs, not display names

Resolve names like `github` or `search` to **cuid2 server IDs** via `tool__listServers` before making updates.

---

## Workflow (Audit & Optimize)

### 1. Agent Audit

Scan the current state of assistants and tools:

1. **Retrieve Configurations:**
   ```json
   agent__listAgents({ "type": "configs", "verbose": true })
   ```
   For each assistant, record its `id`, `name`, `description`, `systemPrompt`, `externalMcpServers`, and `builtinCapabilities`.

2. **Retrieve Tool Inventory:**
   ```json
   tool__listServers({ "availability": "inventory" })
   ```
   Get all available tool servers in the environment.

### 2. Optimization Logic (Add & Remove)

For each assistant, perform a semantic check of its role against its current toolset:

* **Add (Augmentation):** If the assistant has a clear functional need (e.g., Finance Specialist) and a highly relevant tool is available in the inventory (e.g., Market Search API) but not attached, propose adding it.
* **Remove (Pruning / Tool Bloat Prevention):** If a tool is attached to the assistant but is completely unrelated to its domain (e.g., `github` attached to a Finance Agent, or `finance-api` attached to `Coding Expert`), propose removing it. 
  * *Reasoning:* Too many tools increase cognitive load, waste token context, and lead to tool selection errors. Propose removals under the banner of minimizing cognitive load.
* **Keep (Retention):** Retain core tools that are aligned with the assistant's primary focus.

**Explicit Calculation Step:**
Calculate the final tool list precisely using a mathematical union and difference to prevent accidental tool deletion:
```
final_list = (current_list + add_list) - remove_list
```
Double-check that all tools intended to be retained (`Keep`) are explicitly present in the resulting `final_list` payload for `agent__updateAgent`.

### 3. Draft Diagnostic Report

Before applying any changes, present a structured **Audit & Optimization Report** to the user:

```markdown
### [Assistant Name] (`[Assistant ID]`)
* **Role Summary:** [1-sentence summary of description/systemPrompt focus]
* **Proposed Optimization:**
  * **Keep:** `[tool-label-1]`, `[tool-label-2]`
  * **Add (Recommended):** `[tool-label-3]` (Reason: [brief explanation of domain relevance])
  * **Remove (Prune):** `[tool-label-4]` (Reason: High cognitive load / Irrelevant to core role)
* **Action:** Update `externalMcpServers` to `[final merged & pruned ID list]`
```

Provide a high-level summary of the overall status (e.g., "3 assistants audited, 1 needs additions, 2 need pruning").

### 4. Apply Updates

Once the user approves the optimization proposal:

For each assistant requiring changes:
```json
agent__updateAgent({
  "id": "<assistant-id>",
  "externalMcpServers": ["<final-resolved-id-1>", "<final-resolved-id-2>"],
  "builtinCapabilities": ["<final-resolved-builtins>"]
})
```

*Note: You cannot update the configuration of the assistant you are currently running as. Use a root/parent session or another agent (e.g., App Wizard) to run the update.*

### 5. Verification & Handoff

Verify that the changes were correctly applied:

1. Check the updated configurations:
   ```json
   agent__listAgents({ "type": "configs", "verbose": true })
   ```
2. Report the successful optimization to the user, highlighting the added and pruned tools. Tell them that existing sessions will pick up these changes upon restart or next configuration resolution.

---

## Guidelines

- **Prevent Tool Bloat Proactively:** Treat tool removal with equal importance to tool addition. Do not let assistants become "jack of all trades" with bloated tool lists.
- **Role-Tool Alignment:** Every tool attached to an assistant must be explicitly justified by its `description` or `systemPrompt`.
- **Atomic updates:** Ensure you calculate the union and difference correctly before calling `agent__updateAgent`. Never send an incomplete list that deletes required tools.
- **English Prompt Preservation:** Boost only modifies tool configurations (`externalMcpServers` and `builtinCapabilities`). Do not modify the `systemPrompt` text unless separately requested.

## Builtin Tools

| Step | Tool |
| --- | --- |
| List assistants | `agent__listAgents({ "type": "configs", "verbose": true })` |
| Inventory MCP | `tool__listServers({ "availability": "inventory" })` |
| Apply changes | `agent__updateAgent({ id, externalMcpServers, builtinCapabilities? })` |
| Create new specialist | **recruit** (separate workflow) |


