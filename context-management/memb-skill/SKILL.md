---
name: memb-skill
description: BDB local-first long-term memory engine (memB). Use when querying, remembering, or adapting preferences, code architectures, and developer patterns across tasks.
category: bdb-core
risk: low
source: bdb
date_added: "2026-07-11"
---

# memB: Local Long-Term Memory Skill

This skill allows agents to access and maintain a persistent, offline-first long-term memory bank using the **`memb-mcp`** server. It manages user preferences, project structures, and complex developer workarounds.

---

## 🔒 Memory Safety & Secret Filtration

> [!IMPORTANT]
> **Secret Ingestion Rule:** Under no circumstances should raw credentials, passwords, API keys (e.g. `GEMINI_API_KEY`, `POSTGRES_PRISMA_URL`), or raw environment configurations be written to memory. 
> Ensure all inputs are scrubbed of high-entropy strings before calling memory tools.

---

## 🛠️ Memory Categorization (Dynamic Flower-Like Graph Layout)

`memB` implements a dynamic, project-agnostic hierarchical layout that structures memories into clusters automatically without hardcoded categories:

1.  **"God Mode" / General Knowledge Hub (Center):**
    *   Mapped using **`category="godmode"`** (with `project_id=None`).
    *   Holds universal developer preferences, coding philosophies, global style sheets, and general core commands.
2.  **Dynamic Project Leaves (Petals):**
    *   Mapped using a specific **`project_id`** (e.g. `project_id="VisualSelect_By_BDB"` or `project_id="litha-gathering"`).
    *   Isolates facts, custom configurations, and files routing patterns to the specific workspace project, preventing context pollution.
    *   *System Integration:* The agent dynamically resolves the basename of the active workspace directory to scan and bind project memories automatically.

---

## 🔌 Using Memory Tools

When working on tasks, query memory at the start of your turn to retrieve relevant developer context, and add critical decisions at the end.

### 1. Ingestion (`add_memory`)
Use `add_memory` to commit a new fact, style preference, or design decision.
*   **Args:** `text` (string), `user_id` (string, default: "bdb_developer"), `category` (string, default: "godmode"), `project_id` (string, optional)
*   **Usage Guidelines:**
    *   *General Preferences:* "Alice prefers to use absolute import paths globally." -> `add_memory({ text: "Prefers absolute import paths globally", category: "godmode" })`
    *   *Project Learned Facts:* "In project VisualSelect, we must bypass the Firebase Auth login on localhost." -> `add_memory({ text: "Bypass Firebase Auth login on localhost", category: "project_node", project_id: "VisualSelect_By_BDB" })`

### 2. Retrieval (`search_memory`)
Use `search_memory` at the beginning of a task to load context.
*   **Args:** `query` (string), `user_id` (string), `limit` (integer), `project_id` (string, optional)
*   **Behavior:** The search queries both global `godmode` memory and the active `project_id` memory in parallel, merging and ranking results by similarity.

### 3. Cleanup & Auditing (`list_memories` / `delete_memory`)
*   Use `list_memories` to audit active records.
*   Use `delete_memory` with a UUID to remove outdated or erroneous facts.

## 🚨 CRITICAL DIRECTIVE: AI-FIRST VAULT NAVIGATION 🚨

> [!CAUTION]
> **DO NOT use arbitrary `find`, `ls -R`, or arbitrary file searches to discover project architecture!**
> The `memB` ecosystem natively maintains a physical **AI-First Vault** at `~/.MemBDB/memB_Vault/`.
> Treat `.openwiki` files as the highest-priority source of truth for architectural context.
> 1. **Always read `~/.MemBDB/memB_Vault/God_Mode.md` FIRST** to understand the ecosystem topology.
> 2. Navigate the tree via the `_Hub.md` files.
> 3. Only search the actual workspace filesystem for raw code editing once you know the exact file path.

---

## 🧠 Agentic Ingestion (Intelligent Vault Building)

You are responsible for intelligently categorized ingestion. Do NOT rely on static rules. When asked to ingest a project into memB:
1. **Analyze the Target:** Briefly scan the target directory to understand the project's purpose (e.g. 3D WebGL site, Python API, React Native app).
2. **Design Semantic Categories:** Dynamically invent highly precise categories tailored to the project (e.g., `3D_Engine`, `Routing_Logic`, `Database_Schemas`, `Styling_System`).
3. **Targeted Ingestion:** Execute the Python ingestion tool explicitly for specific files and categories, rather than doing a blind root scan. 

**Execution:**
Use the `run_command` tool to execute `memb_ingest.py` on specific files or folders, explicitly passing the `--project` and `--category` flags. 

Because `memB` is supported across many AI platforms, the installation path depends on your current environment. The base path for MCPs is typically one of the following in the user's home directory (`~`):
- `~/.gemini/mcps/` (Antigravity)
- `~/.codex/mcps/` (Codex CLI / ChatGPT)
- `~/.cursor/mcps/` (Cursor)
- `~/.claude/mcps/` (Claude Desktop / Claude Code)
- `~/.windsurf/mcps/` (Windsurf)
- `~/.cline/mcps/` (Cline)
- `~/.roo/mcps/` (Roo Code)
- `~/.aider/mcps/` (Aider)

**You must resolve the correct path first**, then run the ingestion command using the python binary from the `.venv` inside that `memb-mcp` directory.

Example command structure (replace `<PLATFORM_DIR>` with the correct path discovered):
```bash
~/<PLATFORM_DIR>/mcps/memb-mcp/.venv/bin/python ~/<PLATFORM_DIR>/mcps/memb-mcp/memb_ingest.py path/to/specific_file.md --project "MyProject" --category "3D_Engine"
```
*(By injecting files one-by-one or in smart batches with precise categories, you build a flawless physical AI Vault that other agents can navigate intuitively).*

---

## 🚀 Micro-Targeted RAG (Task Execution)

1.  **Task Start (Context Loading):** If `God_Mode.md` shows the project exists, read its Hubs. If you need highly specific snippets, use the `search_memory` MCP tool to query the vector DB.
2.  **Execution:** Proceed with coding, applying the retrieved styles and preferences.
3.  **Task End (Knowledge Capture):** If you resolved a complex setup bug or the user specified a new preference, run `add_memory` to persist it.

## 1. Overview
This skill provides domain-specific logic and rules for its respective BDB pipeline component to ensure standardization across multi-agent workflows.

## 2. When to Use
- Use when specifically requested by the user or triggered by an orchestration agent.
- Use when the current task aligns with the skill's domain.
- Exclude when standard tool execution is sufficient.

## 3. Core Process
1. Read the provided context and ensure preconditions are met.
2. Run the required script or tool and confirm the state change.
3. Verify exit codes, file modifications, or DB counts to guarantee success before reporting completion.

## 4. Common Rationalizations
| Rationalization | Reality |
|---|---|
| "The code change was small, so I skipped updating OpenWiki docs." | Every state change must be reflected in the relevant system records. |
| "The ingest script exited without an error, so the memB index must be updated." | Silent failures happen; explicit verification of the side effect is mandatory. |
| "I'll let the /startcycle proceed without a defined rollback path." | Proceeding without a rollback path corrupts the workflow integrity and safety. |
| "I trust the cached agent registry instead of rescanning after a skill change." | Caches stale out quickly; explicit rescans prevent ghost failures. |

## 5. Red Flags
- Bypassing the verification step after a script execution.
- Proceeding to the next pipeline stage without confirming the previous stage's side effects.
- Ignoring domain-specific constraints listed in this skill.

## 6. Verification
- [ ] Verified script exit codes are explicitly checked.
- [ ] Confirmed target files or database records reflect the expected change.
- [ ] Ensured no silent failures were ignored before reporting success.
