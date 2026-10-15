---
name: memory-capture
description: Automatically classify, route, and retrieve agent outputs, findings, policies, or troubleshooting logs into OKF or ChromaDB RAG.
---

# Memory Capture & Retrieval Skill

Use this skill whenever you synthesize key findings, architecture decisions, coding standards, bug root causes, or reusable technical knowledge during a task, or when querying historical agent memory.

## Environment & Path Variable Setup

Export (or in Windows, set) the memory system path environment variables:

### Linux / macOS (Bash/Zsh)
```bash
export MEMORY_SYSTEM_ROOT="$HOME/memory_system"
export MEMORY_DB="$MEMORY_SYSTEM_ROOT/db"
export MEMORY_OKF="$MEMORY_SYSTEM_ROOT/knowledge/okf"
export MEMORY_INBOX="$MEMORY_SYSTEM_ROOT/inbox"
```

### Windows (PowerShell)
```powershell
$env:MEMORY_SYSTEM_ROOT = "$HOME\memory_system"
$env:MEMORY_DB = "$env:MEMORY_SYSTEM_ROOT\db"
$env:MEMORY_OKF = "$env:MEMORY_SYSTEM_ROOT\knowledge\okf"
$env:MEMORY_INBOX = "$env:MEMORY_SYSTEM_ROOT\inbox"
```

### Windows (CMD)
```cmd
set MEMORY_SYSTEM_ROOT=%USERPROFILE%\memory_system
set MEMORY_DB=%MEMORY_SYSTEM_ROOT%\db
set MEMORY_OKF=%MEMORY_SYSTEM_ROOT%\knowledge\okf
set MEMORY_INBOX=%MEMORY_SYSTEM_ROOT%\inbox
```

---

## Automatic Initialization

**IMPORTANT**: When calling or executing this skill, the environment **MUST** check if the memory system storage exists. If the directory `~/memory_system` (or `$MEMORY_SYSTEM_ROOT`) does not exist, initialize it immediately before proceeding:

```bash
python ~/memory_system/init_storage.py
```

This will automatically create:
- **ChromaDB Storage**: `~/memory_system/db` (`$MEMORY_DB`)
- **OKF Storage**: `~/memory_system/knowledge/okf` (`$MEMORY_OKF`)
- **Inbox Directories**: `~/memory_system/inbox/` (`$MEMORY_INBOX`) (`processed/`, `error/`)

---

## Instructions for AI Harnesses

### 1. Ingestion & Classification

When completing a task or documenting a decision:

1. **Format the Output**:
   Write the knowledge summary into a temporary file or directly into `~/memory_system/inbox/<filename>.md` (or `$MEMORY_INBOX/<filename>.md`).
   - Use descriptive lowercase slugs for `<filename>` (e.g. `raw_master_preservation_and_viewable_separation.md`).
   - Do **not** prefix filenames with dates (e.g. avoid `2026-10-04-`); capture dates are tracked automatically by the filesystem and indexing metadata.

2. **Specify Classification Hint (Header Standard)**:
   Always provide a descriptive title directly on the header line to guarantee clean display in memory inspection and search tools:
   - For **Source of Truth / Rules / Policies**:
     ```markdown
     # OKF Decision: <Descriptive Title>
     Type: Policy / Architecture Standard
     Domain: <Optional Domain Area>
     Summary: <Concise executive summary>
     ```
   - For **Logs / Bug Fixes / Technical Snippets**:
     ```markdown
     # Chroma Context: <Descriptive Title>
     Type: Troubleshooting / Bug Report
     Domain: <Optional Domain Area>
     Summary: <Concise description of the fix or learning>
     ```

3. **Trigger Processing**:
   Ensure memory system is initialized, then run:
   ```bash
   python ~/memory_system/capture_knowledge.py <path_to_file>
   ```
   Or place the file into `~/memory_system/inbox/` for automatic background processing.

### 2. Memory Retrieval Architecture (RAG Integration)

When querying historical agent memory:

- **Unified Agent Pre-Flight (`--preflight`)**: Run pre-flight memory retrieval before starting any development or maintenance task:
  ```bash
  python3 ~/memory_system/inspect_memory.py --preflight .
  ```
  This automatically checks repository fork guardrails, displays matching OKF architectural standards, and loads recent lessons learned.
- **OKF Direct Search (Rules & Policies)**: Perform keyword or regex search across `~/memory_system/knowledge/okf/*.md` (`$MEMORY_OKF/*.md`) or use:
  ```bash
  python3 ~/memory_system/inspect_memory.py --okf -q "<topic>"
  ```
- **Chroma Vector Retrieval (Troubleshooting & Context)**: Query the persistent ChromaDB collection at `~/memory_system/db` (`$MEMORY_DB`) using semantic similarity search or:
  ```bash
  python3 ~/memory_system/inspect_memory.py --chroma -q "<error_message>"
  ```
- **Metadata Filtering**: Filter vector queries using `filter={"type": "Troubleshooting"}` or `filter={"type": "Policy"}` to isolate specific domain contexts.

## Classification Standard
- **OKF (`~/memory_system/knowledge/okf`)**: High-level rules, team standards, architectural design decisions, and security policies.
- **CHROMA (`~/memory_system/db`)**: Specific bug fixes, terminal outputs, error tracebacks, API snippets, and step-by-step guides.
