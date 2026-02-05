---
name: kit-cli-navigator
description: Run focused `kit` CLI commands (file-tree, symbols, search, semantic discovery, dependency analysis, and exports) to build high-signal repository context fast. Use when you need to understand an unfamiliar codebase, prep context for Claude, plan refactors, audit dependencies, or answer “where is X implemented?” without manually grepping.
---

# Kit CLI Navigator

Use the `kit` command-line interface to interrogate repositories with deterministic tooling before handing context back to Claude. `kit` bundles structure-aware commands (file trees, symbol extraction, semantic search, dependency graphs, exports) that make “context engineering” repeatable for any language mix. See the [reference sheet](reference.md) when you need flag-level detail.

## When to activate

- You or the user need a fast mental model of an unfamiliar repo.
- The task is “find where this behavior lives”, “trace symbol usage”, or “surface related code” or any similar request about any codebase.
- Preparing briefs for refactors, dependency upgrades, incident reviews, or onboarding guides.
- Creating exportable context bundles (JSON, DOT, Markdown) for Claude or collaborators.

## Prerequisites

1. Install/upgrade kit (requires Python ≥3.9):
   ```bash
   pipx install cased-kit  # or: pip install --upgrade cased-kit
   kit --version
   ```
2. Run commands from the repository root (or pass an absolute path).
3. For `kit search-semantic`, ensure `sentence-transformers` is available; kit prompts for installation if missing.
4. Optional: set `KIT_CACHE_DIR` when working across large monorepos to reuse indexes.

## Core workflow

Always pair this skill with `subagent-orchestration`: dispatch each `kit` CLI command to a focused subagent, have it run the command from the repo root, and post a concise result bundle (command, exit status, key findings, saved file paths) back to the main agent thread before proceeding.

1. **Confirm scope**

   - Ask which repo/directory matters and whether remote refs/tags are relevant.
   - Record success criteria (e.g., “find queue consumers”, “map Terraform modules”).

2. **Baseline snapshot**

   - Subagent: `kit git-info /abs/path` → capture branch, SHA, remotes and summarize back.
   - Subagent: `kit file-tree /abs/path --path src --output tree.json` → structural overview (pipe through `jq`/`less` for quick scans) and link the output file.
   - Subagent: `kit file-content /abs/path package.json` (or other manifest) to read dependencies without opening an editor; paste only the relevant snippet.

3. **Surface APIs and hotspots**

   - Subagent: `kit symbols /abs/path --format table` to list top-level functions/classes.
   - Narrow with `--file` when the repo is large; switch to `--format json` when Claude needs machine-readable structure (delegate each targeted run to its own subagent).
   - Subagent: `kit usages /abs/path ConfigLoader --type class` to see definitions + references and return a bulleted digest.
   - Subagent: `kit chunk-symbols /abs/path path/to/file.py` for precise copy/paste-ready blocks; attach only the relevant chunks.

4. **Search by text AND meaning**

   - Subagent: run literal filters (`kit search /abs/path "retryPolicy" --pattern "src/**/*.ts"` or `kit grep /abs/path "TODO" --include "*.py"`) and post paths with short excerpts.
   - Subagent: run semantic recall `kit search-semantic /abs/path "where do we sanitize user input" --top-k 10 --chunk-by lines`; include embedding settings + highlights.
   - Subagent: `kit context /abs/path api/routes.py 128` (± surrounding lines) instead of quoting entire files; return condensed snippets.

5. **Understand relationships**

   - Subagent: `kit dependencies /abs/path --language python --format dot --output deps.dot` to visualize imports/modules (render with Graphviz or open in VS Code plug-ins) and record where the asset lives.
   - For Terraform, spin a dedicated subagent with `--language terraform` and `--cycles` to smoke-test architectural issues.
   - Subagent: `kit index /abs/path --output repo-index.json` builds a full-text + symbol inventory for bulk analysis; report file size + location.

6. **Package and hand off context**

   - Subagent: run exports (`kit export /abs/path index out/index.json` or `kit export /abs/path symbol-usages out/queue.json --symbol QueueWorker`) and confirm saved path + checksum.
   - Subagent: create slices for Claude using `kit chunk-lines ... --max-lines 80`, returning only the refined snippets.
   - Store outputs under `debug/` or another ignored directory so they do not pollute Git, and have the subagent mention the folder.

7. **Cache + iterate**
   - Subagent: `kit cache warm /abs/path` (see `reference.md`) so heavy operations reuse embeddings/ASTs, then report cache status.
   - Keep a scratchpad of helpful commands for the session log; reuse them as new questions arise.

## Examples

### Example 1: Trace where auth tokens are validated

**Goal:** “Find every spot we touch `validateToken` and summarize behavior.”

1. `kit symbols /repo --file src/auth/index.ts --format json` → locate symbol signature.
2. `kit usages /repo validateToken --type function --output tmp/validate.json`.
3. `kit context /repo src/auth/middleware.ts 57` for a targeted snippet you can quote back to the user.
4. Summarize findings + attach the JSON so Claude can ingest it without rerunning expensive scans.

### Example 2: Prepare a refactor brief for Terraform modules

1. `kit file-tree /repo --path infra/terraform --output tmp/tree.json`.
2. `kit dependencies /repo --language terraform --cycles --llm-context --output tmp/terraform.md`.
3. `kit search-semantic /repo "state bucket" --top-k 5 --chunk-by symbols`.
4. Use the markdown export + semantic hits to outline which modules share remote state and where to sand down coupling.

### Example 3: Build a context pack for Claude

1. `kit index /repo --output tmp/index.json`.
2. `kit export /repo symbol-usages tmp/payment_init.json --symbol PaymentClient`.
3. `kit chunk-lines /repo services/payment.py --max-lines 60 --output tmp/payment_chunks.json`.
4. Feed the JSON bundle into Claude when answering synthesis questions (“Why do payments fail on retries?”).

## Best practices

- Prefer absolute repo paths so skills run consistently (`kit ... /Users/bleikamp/work/app`).
- Use subagents for every CLI run so commands execute in parallel without blocking; ensure each subagent returns the command, exit status, and key findings to the main thread.
- Capture command output snippets in markdown fences when relaying back to Claude; keep them concise.
- Combine literal + semantic search: run `kit search` first for obvious hits, fall back to `kit search-semantic` for conceptual matches.
- Export artifacts once per session and reuse them; kit’s deterministic CLI makes outputs easy to diff/share.
- Keep raw command transcripts outside SKILL context (store in `debug/kit/` and reference paths).

## Common pitfalls & recoveries

- **Running from the wrong directory** → Always pass the repo path explicitly or `cd` into it before invoking kit.
- **Huge outputs flooding Claude** → Use `--format json` + summarize, or `kit chunk-lines` to slice manageable blocks. Use subagents whenever possible to avoid polluting the main thread.
- **Semantic search unavailable** → Install `sentence-transformers` (kit prompts) or fall back to textual search.
- **Dependency visualization fails** → Ensure Graphviz (`brew install graphviz`) is available when using `--visualize`.
- **Stale caches** → `kit cache clear /repo` if outputs look outdated before rebuilding.
- **Silent subagents** → If a subagent finishes without reporting, explicitly ask for its summary so the main thread has authoritative context.

## References

- Command matrix and additional flags: [reference.md](reference.md)
- Kit CLI docs and release notes: https://kit.cased.com
