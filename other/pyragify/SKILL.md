---
metadata:
  name: pyragify
  class: toolboxes
  type: skill
  version: '1.0'
  schema_version: '1.0'
  freshness:
    status: active
    sync_count: 0
    last_synced_by: daemon
    last_synced: '2026-06-27T00:00:00'
credentials:
  maturity: "hardened"
  description: "Convert any code repository or document directory into clean, semantically-chunked .txt files optimized for NotebookLM ingestion."
  when_to_use: "Use this skill when the task involves pyragify"
  triggers: ["chunk codebase", "prepare for rag", "preprocess for notebooklm", "pyragify", "chunk documents"]
  inputs: ["repo_path", "output_dir", "config.yaml"]
  outputs: ["chunked .txt files by type", "metadata.json", "hashes.json"]
---

# pyragify Skill

## Source
- **Repo**: https://github.com/ThomasBury/pyragify
- **PyPI**: `pip install pyragify`
- **Version**: v0.2.0 (April 2026)
- **License**: Unlicense (fully free)

## What It Does
Converts any code repository or document directory into clean, semantically-chunked `.txt` files optimized for NotebookLM ingestion. Run this BEFORE uploading to NotebookLM.

## Setup
```bash
pip install pyragify
```

## Usage
**CRITICAL:** Always use relative portable paths to execute the OS Engine so the workspace can be ported to new machines without breaking:

```bash
# With a config file (recommended)
.\.venv\Scripts\pyragify.exe --config-file config.yaml

# Or inline
.\.venv\Scripts\pyragify.exe \
  --repo-path /path/to/repository \
  --output-dir /path/to/output \
  --max-words 200000 \
  --skip-dirs "__pycache__" \
  --skip-dirs "node_modules" \
  --verbose
```

## Example `config.yaml`
```yaml
repo_path: c:\Users\BAB AL SAFA\Desktop\open-workspace
output_dir: c:\Users\BAB AL SAFA\Desktop\open-workspace\.core\toolbox_library\core.toolbox\notebooklm\skills\pyragify\output
max_words: 200000
max_file_size: 10485760  # 10 MB
skip_patterns:
  - "*.log"
  - "*.tmp"
skip_dirs:
  - "__pycache__"
  - "node_modules"
  - ".git"
verbose: false
```

## Output Structure
```
output/
  python/      ← Python functions, classes, comments
  markdown/    ← Markdown sections split by headers
  html/        ← HTML script and style chunks
  css/         ← CSS rule chunks
  other/       ← All other readable file types
  remaining/   ← Overflow chunks after word limit
  metadata.json
  hashes.json  ← MD5 hashes for incremental re-runs (only reprocesses changed files)
```

## Supported Inputs
- `.py` — chunked by function/class/comment
- `.md`, `.markdown` — split by header sections
- `.html` — script and style chunks
- `.css` — CSS rule chunks
- All other UTF-8 readable files — included as plain text

## Workflow with notebooklm-py
```bash
# Step 1: Preprocess the workspace
pyragify --config-file config.yaml

# Step 2: Upload output chunks to NotebookLM
notebooklm create "Workspace Analysis"
notebooklm use <notebook_id>
notebooklm source add "./output/markdown/chunk_0.txt"
notebooklm source add "./output/python/chunk_0.txt"

# Step 3: Query and generate
notebooklm ask "What are the architectural gaps in this workspace?"
```
