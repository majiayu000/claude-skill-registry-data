---
name: obsidian-cli
description: "Automate your Obsidian vault via CLI. Use when user wants to: migrate or reorganize notes, assign properties/frontmatter, create Obsidian Bases (.base files), generate Templater templates, bulk rename or move files, search vault content or analyze links, manage plugins/themes/workspaces, or perform batch vault operations. Trigger phrases: 'organize my vault', 'move my notes', 'add properties to my notes', 'tag all notes in', 'create a Base', 'set up a daily note template', 'search my vault', 'clean up my vault', 'rename notes in', 'list everything in my vault', 'manage my plugins', 'set frontmatter on'. Only trigger when the user references their Obsidian vault, notes within a vault, or Obsidian-specific concepts (Bases, Templater, daily notes, vault properties, workspaces). Do not trigger for generic file operations, general markdown editing, or coding tasks that happen to mention notes or frontmatter without an Obsidian or vault context. Specifically, if the user asks to 'write a script', 'create a script', or 'build a tool' that works with frontmatter or markdown files, that is a coding task — do not trigger."
---

# Obsidian CLI Skill

Batch automation of your Obsidian vault using the Obsidian CLI. Analyzes notes, assigns properties based on content, and orchestrates migrations, base creation, template generation, and other vault operations.

## Instructions

1. **Read config first.** Before any operation that depends on property schema, batch settings, or vault preferences, read the user's config:
   ```
   ~/.claude/plugins/marketplaces/obsidian-cli-skill/plugins/obsidian-cli/config.yaml
   ```
   If `config.yaml` does not exist, fall back to `config.yaml.example` in the same directory.

2. **Always consult reference files before constructing any command.** Never guess syntax, parameter names, or examples. Commands use `param=value` parameters plus bare flags (`total`, `verbose`, `silent`). Avoid GNU-style `--flag` syntax except where Obsidian explicitly documents it as global behavior. Use the command routing table below to find the right reference.

3. **Propose before executing.** Present changes for user review and get explicit approval before modifying any files. Follow [output-format-standard.md](../../references/output-format-standard.md) for all output formatting.

4. **If a command isn't in the references, it may not exist.** Consider native Obsidian workflows instead — see [native-workflows.md](../../references/native-workflows.md).

## Workflow

All operations follow this pattern:

1. **Analyze** — Read notes/requirements and config.yaml
2. **Propose** — Present changes for review (follow output format standard)
3. **Approve** — User reviews and approves before any files are modified
4. **Execute** — Run approved operations via Obsidian CLI

**Approval mode** is controlled by `batch_settings.approval_mode` in config.yaml:
- **`batch`** — Approve the entire phase at once, then all operations execute without further prompts
- **`single`** — Approve each note individually before proceeding

**Batch splitting:** If notes exceed `batch_settings.max_batch_size`, split into multiple batches — propose and get approval for each batch separately.

## Command Routing

Before proposing any command, read the corresponding reference file:

| Operation | Reference File |
|-----------|---------------|
| File create/read/move/delete | [obsidian-cli-files.md](../../references/obsidian-cli-files.md) |
| Property set/read/remove | [obsidian-cli-properties.md](../../references/obsidian-cli-properties.md) |
| Search, links, backlinks | [obsidian-cli-search.md](../../references/obsidian-cli-search.md) |
| Bases (.base files) | [obsidian-cli-bases.md](../../references/obsidian-cli-bases.md) |
| Daily notes | [obsidian-cli-daily.md](../../references/obsidian-cli-daily.md) |
| Templates | [obsidian-cli-templates.md](../../references/obsidian-cli-templates.md) |
| Publish | [obsidian-cli-publish.md](../../references/obsidian-cli-publish.md) |
| Plugins | [obsidian-cli-plugins.md](../../references/obsidian-cli-plugins.md) |
| Tags, aliases | [obsidian-cli-tags-aliases.md](../../references/obsidian-cli-tags-aliases.md) |
| Tasks | [obsidian-cli-tasks.md](../../references/obsidian-cli-tasks.md) |
| Vault info, folders | [obsidian-cli-vault.md](../../references/obsidian-cli-vault.md) |
| Workspace, tabs, layouts | [obsidian-cli-workspace.md](../../references/obsidian-cli-workspace.md) |
| Web viewer, unique notes | [obsidian-cli-web-unique.md](../../references/obsidian-cli-web-unique.md) |
| All other operations | [command-routing.md](../../references/command-routing.md) |

## Workflows

### Migrate and Enrich Notes

Two-phase workflow: property assignment → rename/move. Read config.yaml for batch and approval settings, then follow [migration-workflow.md](../../references/migration-workflow.md) for the complete process, proposal formats, and rules.

### Create Obsidian Bases

Read config.yaml for property schema, consult [obsidian-bases.md](../../references/obsidian-bases.md) for `.base` structure and CLI commands. Propose the base structure for approval before creating.

### Generate Templater Templates

Consult [templater-plugin.md](../../references/templater-plugin.md) for syntax and patterns. Propose template content for approval before creating.

## Execution Strategy

For batch operations (>5 files), split reasoning from execution:

1. **Plan phase** (current model): Read notes, analyze content, build the proposal, get user approval
2. **Execute phase**: Delegate to the `batch-executor` agent to execute approved CLI commands. This agent runs on Haiku with Bash-only tool access for fast, low-cost execution.

The planning model handles all decisions. The execution agent receives a numbered list of pre-approved commands and runs them sequentially, reporting results per the output format standard.

For single-file operations or operations requiring judgment (e.g., choosing property values), execute directly without delegation.

**Fallback:** If subagent delegation is not available (e.g., on Claude.ai web), execute commands directly in sequence.

## Error Handling

If an `obsidian` CLI command fails:
1. Report the failure inline using the error format from the output format standard
2. Continue with remaining operations — do not stop the entire batch for one failure
3. Include all failures in the final summary
4. If the CLI binary is not found, stop and tell the user to enable Obsidian CLI (requires Obsidian 1.12.1+)

## Examples

**User:** "Migrate my Research notes to Notes with properties"
**Action:** Read config.yaml → read all files in Research/ → analyze content → present compact property proposal → on approval, set properties → present rename & move proposal → on approval, move files. Follow [migration-workflow.md](../../references/migration-workflow.md).

**User:** "Add type: reference to all files in my Docs folder"
**Action:** Read [obsidian-cli-properties.md](../../references/obsidian-cli-properties.md) → list files in Docs/ → present proposal → on approval, run `obsidian property:set` for each file.

**User:** "Create a Base that shows all how-to notes by topic"
**Action:** Read config.yaml for property schema → read [obsidian-cli-bases.md](../../references/obsidian-cli-bases.md) → propose `.base` file structure → on approval, create the file.
