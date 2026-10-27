---
name: copilot-cli-tools-inventory-refresh
description: '**REFRESH SKILL** — Keep `tools/inventory.yaml` (the workspace cross-runtime tools inventory) accurate and up to date, grounded in the latest GitHub Copilot CLI. USE FOR: refreshing/updating the tools inventory after CLI updates; validating the inventory YAML schema; checking that CLI, VS Code, and GitHub Copilot tool spellings are current; detecting drift between the inventory and the live CLI surface (--available-tools/--excluded-tools, agent tools: aliases, built-in MCP servers); recording cli_version and last_verified metadata. DO NOT USE FOR: authoring new Copilot CLI customization files (use copilot-cli-agent-customization instead); general coding; VS Code toolset authoring (use the workspace publish-toolsets flow); OpenSpec spec maintenance.'
metadata:
  author: arisng
  version: 0.1.0
---

# Copilot CLI Tools Inventory Refresh

Maintain `tools/inventory.yaml` — the workspace's single source of truth for cross-runtime tool concepts, aliases, defaults, and runtime caveats — grounded in the latest GitHub Copilot CLI.

## Relationship to Other Skills

| Skill | Owns |
|-------|------|
| **copilot-cli-tools-inventory-refresh** (this skill) | The *inventory*: keeping `tools/inventory.yaml` accurate, validated, and fresh |
| `copilot-cli-agent-customization` | *Authoring*: creating/updating CLI customization files (agents, skills, hooks, plugins, instructions) |
| `copilot-cli-subsession` | *Invocation*: spawning programmatic CLI sub-sessions |

If the task is "refresh the tools inventory" → this skill. If the task is "create or fix a CLI customization file" → `copilot-cli-agent-customization`.

## Grounding Sources

The inventory is refreshed against **two** independent grounding sources (see `references/grounding-sources.md` for the full corpus):

1. **Official documentation** — GitHub Copilot CLI command reference ("Tool availability values" section) and the custom-agents-configuration reference. Fetch via `web_fetch`.
2. **Local CLI introspection** — `copilot version`, `copilot --help`, and `copilot plugins list`. These reflect the actually-installed binary and are the fastest freshness check.

Both must be consulted; the drift report merges their signals. Record the CLI version (`cli_version`) and verification date (`last_verified`) in the inventory metadata after a refresh.

## Workflow

### 1. Capture CLI Version and Date

```powershell
copilot version
Get-Date -Format "yyyy-MM-dd"
```

Record these; they become `cli_version` and `last_verified` in the inventory metadata.

### 2. Gather Grounding

- Run `copilot --help` and `copilot plugins list` (local).
- Fetch the official CLI command reference page and custom-agents-configuration page (docs).
- Review the workspace corpus: `.docs/reference/copilot/cli/cli-agent-valid-tool-aliases.md`, `.docs/reference/copilot/cli/copilot-cli-customization-matrix.md`, and `.docs/reference/copilot/cli/copilot-cli-help.md`.

### 3. Drift Diff

Compare the grounding signals against the current `tools/inventory.yaml`:

- **Concrete CLI built-ins** (the `cli:` lists on `cli-surface` families and core built-ins): any tool names observed in the CLI command reference's tool availability values that are missing from the inventory → high-confidence **additions** to review.
- **Agent `tools:` aliases** (the `official_alias` conceptual surface vs. the CLI-frontmatter set `bash`/`view`/`edit`/`search`): flag if the docs changed which aliases are valid.
- **Built-in MCP servers** (`github-mcp-server`, `playwright/*`): whether they are still listed as built-ins.
- **`default` / `notes`**: only update when the grounding source actually changed behavior.

The script `scripts/refresh-inventory.ps1` automates steps 1–3 and emits a drift report plus the `last_verified`/`cli_version` values to apply.

**Diff confidence:** the report treats *observed-in-grounding-but-not-in-inventory* names as high-confidence additions. Names *in the inventory but not observed* are listed as "not confirmed" (informational only) — absence from a docs HTML page or from `--help` (which lists flags, not tools) does **not** prove removal. Never auto-delete based on the "not confirmed" list; verify against the actual tool-availability section first.

### 4. Apply Edits (Curated)

- Apply YAML edits **by hand**, guided by the drift report. Do NOT blind-auto-rewrite the file.
- Safe mechanical updates (`cli_version`, `last_verified`) may be applied automatically via `refresh-inventory.ps1 -ApplyMetadata`.
- Tool-name additions/removals must be reviewed: propose additions while preserving curation — do not blindly adopt the entire live tool surface.

### 5. Validate

```powershell
python3 .github/skills/copilot-cli-tools-inventory-refresh/scripts/validate-inventory.py
```

The validator enforces the schema (required keys, unique ids, category membership, `default` enum, non-empty sources, accepted encodings for `runtime-dependent`/`(closest)`/`runtime-specific`) and cross-checks that referenced `tools/vscode/toolsets/*.jsonc` and `.docs/...` paths exist.

### 6. Cross-check VS Code Toolsets

If a VS Code spelling changed, verify `tools/vscode/toolsets/*.toolsets.jsonc` and update them per the workspace `tools/README.md` authoring rules.

## Value Encoding Rules

These rules keep the YAML parseable and lossless (enforced by the validator):

- **`[]`** = verified no equivalent in that runtime.
- **`"runtime-dependent"`** = present but not a guaranteed built-in (sentinel string inside the list).
- **`(closest)` / `(closest equivalent)` qualifiers** → keep the list values and move the qualifier to `notes`.
- **`official_alias: runtime-specific`** → omit the `official_alias` field and record "runtime-specific" in `notes`.
- **Prose values** (e.g. "partially split across editor, memory, and runtime tooling") → move verbatim to `notes`.

## Guardrails

- **Alias vs concrete built-in distinction is critical.** Agent `tools:` frontmatter aliases (`bash`, `view`, `edit`, `search`, `task`, `web`, `todo`, `github/*`) are NOT the same surface as concrete built-ins accepted by `--available-tools`/`--excluded-tools` (`create`, `apply_patch`, `read_*`, `write_*`, `stop_*`, `list_*`, `sql`, `lsp`, `web_fetch`, `update_todo`). Never merge the two.
- **Do not delete entries** during a refresh without an explicit grounding-source change that justifies it. When in doubt, keep the entry and flag it in the drift report.
- **Do not auto-rewrite tool lists.** Only `-ApplyMetadata` (cli_version/last_verified) is safe to automate.
- **Keep `default` in the closed enum**: `enabled if available`, `enabled if configured`, `runtime-dependent`, `n/a`.
- **`.issues/` historical records** reference `inventory.md`; do not update them — they are history.
- **Do not regenerate `copilot-cli-help.md`** from this skill; it is a historical snapshot. The drift report may flag it as stale, but regenerating it is out of scope here.

## Common Pitfalls

**Colons in notes break YAML.** A `tools:` or `foo: bar` sequence inside an unquoted `notes:` value is a YAML mapping error. Avoid `: ` sequences in unquoted strings, or quote the value.

**The inventory counts 31 entries across 7 categories.** Verify after conversion/refresh that the category taxonomy is intact: `core-built-in`, `limited-applicability`, `builtin-mcp`, `custom-mcp`, `cli-surface`, `vscode-surface`, `agent-host`. In particular, no `cli-surface` family (`cli-shell-session-family`, `cli-file-write-family`, `cli-agent-management-family`, `cli-search-and-fetch-family`, `cli-orchestration-and-state-family`) or `vscode-surface` family (`vscode-terminal-family`, `vscode-memory`, `vscode-user-interaction`, `vscode-editor-control-family`) was dropped. Do not reintroduce a catch-all bucket such as the old `runtime-only` category; a runtime's concrete tool inventory belongs in that runtime's `*-surface` category, and an MCP tool set belongs in `custom-mcp`.

**`create` is a valid concrete CLI built-in but NOT a valid agent `tools:` alias.** Both facts must survive in the inventory (see `cli-file-write-family` entry vs. `.docs/reference/copilot/cli/cli-agent-valid-tool-aliases.md`).

## References

- [Grounding Sources](references/grounding-sources.md) — official doc URLs, local CLI commands, and the workspace corpus to cross-check
- [Validation Script](scripts/validate-inventory.py) — schema + cross-reference validation
- [Refresh Script](scripts/refresh-inventory.ps1) — version capture, drift report, optional metadata apply
