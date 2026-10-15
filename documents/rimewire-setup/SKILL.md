---
name: rimewire-setup
description: Set up or reconfigure Rimewire's local project board for a new or existing project. Survey its plans, tracker, Git conventions, and agent instructions; customize project config and tracker content; and add managed board instructions without replacing existing files. Use when the user asks to initialize, configure, or rerun Rimewire setup.
---

# Rimewire setup

Customize the current project's board. All project choices belong in its
`.rimewire/config.toml` and tracker, never in the installed Rimewire package or
this skill. Preserve existing files and the user's established conventions.

## Find the project and runtime

Resolve the target checkout from the user's request or current working directory.
In a Git worktree, keep setup and journal writes in that checkout; do not silently
switch to the main repository. Read the applicable agent instructions first.

Use the installed CLI: inside the Claude plugin, run
`node "${CLAUDE_PLUGIN_ROOT}/dist/cli.js"`; elsewhere use global `rimewire`.
If it is absent from PATH, read the harness's Rimewire registration: Codex MCP
`command` and `args`, OpenCode's registered local plugin path, or Pi's extension
path resolve the installed package and its `dist/cli.js`. Use the registered
Node executable plus that absolute CLI path. Do not assume a build in the target
project.
Claude substitutes the plugin path in this skill's body before loading it; use
that resolved literal CLI path in commands, reference examples, and delegated
worker instructions. Do not rely on a Bash environment variable for this path.
Require Node.js 24 or newer. The plugin includes its runtime; do not download
dependencies with `npx`, build Rimewire inside the target project, or assume the
project has a `dist/cli.js`. Read [installation](references/installation.md) when
installation is requested or the runtime is missing.

When MCP is available, call `board_url` and `board_overview`. Refer to tools by
their bare names (`board_overview`, `get_package`, `post_update`, `list_updates`,
`board_url`); use the available harness's registered tool names when calling them.
Check that the tools describe the target project before posting. A missing tracker
on first setup or unavailable MCP does not prevent local CLI setup. Return the
actual board URL after verification, rather than guessing a port.

## Survey and choose customization

Read existing `.rimewire/config.toml`, roadmaps, trackers, plans, and relevant docs.
Inspect Git status, branches, and worktrees when available. Discover applicable
agent files throughout the project's own source: `AGENTS.md`, `AGENTS.override.md`,
`CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`, `.cursor/rules/*`, and
other instruction files used by its harnesses. Include nested instruction files;
exclude dependencies, generated output, and other checkouts. A rules directory
is not a file: pass its applicable Markdown or MDC files individually.

Infer the display name, tracker path, ID pattern, branch prefixes, status words,
phases, and platform buckets from that survey. State the choices briefly and
proceed under the user's setup request. Ask only when competing trackers, unclear
project scope, or another consequential choice cannot be inferred. Do not ask for
another approval of already authorized setup edits.

Read [configuration](references/configuration.md) before preparing config or
adapting a tracker. Keep existing IDs, branches, status meanings, and document
links. Match roadmap milestones to actual phase headings. Choose platforms that
describe this project; a single shared bucket is sensible for work without
platform distinctions. Do not copy another project's phases or OS assumptions.

## Apply setup with the deterministic helper

The helper owns config creation, absent-tracker creation, journal ignore rules,
and managed instruction blocks:

```text
rimewire setup --repo PATH [--config JSON_FILE] [--agent-file PATH]... --json
```

For the Claude plugin, the same operation is:

```sh
node "${CLAUDE_PLUGIN_ROOT}/dist/cli.js" setup --repo "/absolute/path/project" --json
```

Use `--config` for an absent config with newly inferred customization, or when
the user requests changes to an existing config. Write a temporary UTF-8 JSON
object using the schema in the reference. For existing config changes, carry
forward all its settings and apply the intended edits: supplied JSON is validated
as a complete config input, not a patch merged into the old file. Remove only
the temporary input you created after successful setup; retain it for a local
retry if an actual write denial prevents completion.

On a rerun with no new config choices, omit `--config`; the helper preserves the
existing TOML, including comments. Without config or explicit input it creates
project defaults. The helper creates only an empty table scaffold when the
configured tracker is absent, with no invented IDs. The model must then create
real packages or adapt the existing tracker; the helper never overwrites it.

Pass each discovered additional agent file with a repeated `--agent-file`;
paths are relative to the target checkout. The helper also discovers known root
agent files and existing `.cursor/rules/*.md` and `*.mdc`; pass nested or other
instruction files explicitly. For example:

```sh
rimewire setup --repo "/absolute/path/project" \
  --config "/absolute/path/project/.rimewire/setup-input.json" \
  --agent-file GEMINI.md --agent-file .cursor/rules/project.mdc --json
```

The helper always creates or updates both root `AGENTS.md` and `CLAUDE.md`, even
if one imports the other. Update the other applicable files too. Existing prose,
imports, and rule frontmatter stay outside the managed replacement. Replace only
the content delimited by `<!-- rimewire:begin -->` and `<!-- rimewire:end -->`;
append a block when neither marker exists. If markers are malformed, preserve the
file and report the helper's precise error rather than guessing a replacement
boundary.

Managed instructions must tell every agent and subagent to read the configured
tracker and board before work; use real package IDs; and post concrete progress,
blockers, decisions, and acceptance evidence. Include all five bare MCP names and
the installed CLI fallback, with `--checkout` for commands outside that checkout.
An explicit `ready` completes work; later progress or blockers reopen it. Process
exit, a hook, or 100% progress alone cannot establish completion. Never put
secrets, credentials, or private prompt contents in board updates.

Ensure the configured journal directory is ignored in the checkout's `.gitignore`.
Keep the config and tracker eligible for version control; do not ignore all of
`.rimewire/` merely to hide its journal.

## Adapt the tracker and verify

After the helper, customize tracker content using the project survey and
[tracker template](assets/tracker.md). Add or remove template lanes and rows to
match the actual plan. Preserve existing prose, task titles, IDs,
statuses, dependencies, links, and extra columns. Make the smallest structural
changes needed for parsing. If an existing source format cannot be represented
in place, create a compatible tracker that links to it and preserves its task
identity. Resolve an ambiguous source of truth before creating a competing one.

Replace template variables with real project values. Use work already defined
by the project or requested by the user. If a fresh project has no plan, track
the actual board setup and verification work rather than inventing product
deliverables. Never post to an example ID or mark an unrelated package ready.

Hooks default to disabled. Enable them when requested using `[hooks]` settings
and an explicit, actual tracker package. Hooks write fixed lifecycle notes only;
automatic progress could reopen completed work. Agents still post their own
progress and explicit completion evidence.

Inspect the helper's JSON (`changed`: project-relative file paths; `config`:
effective validated settings) and your tracker/config edits. Check
that managed blocks occur once in each applicable file and preserve the content
outside their markers. A rerun with the same helper inputs should report no
changes. Run the installed CLI's `list --json --checkout PATH` to check config
and journal access. With MCP, verify the parsed lanes, IDs, statuses, phases, and
platforms through `board_overview` and inspect a real package with `get_package`.
If MCP is unavailable, use the installed CLI's `serve --repo PATH` to inspect the
board and obtain its printed URL; journal updates remain local and need no HTTP.

Record setup evidence on the package for this work when one exists, and use
`list_updates` or CLI `list` to verify the entry. Use `ready` only for the setup
package whose checks passed. Keep tracker status current when completion should
persist across machines; journals remain local.

If an actual sandbox or filesystem denial prevents a write, finish independent
allowed work and give the exact failed path and local command the user must run.
Do not invent a permission gate before attempting authorized setup. For unavailable
installation or helper features, report the installed version's limitation and
use the installation reference; do not improvise an external runtime download.

Finish with every file changed (including your edits beyond the helper's list),
the resulting customization, checks performed, and the verified board URL or
the concrete command needed to start it. Identify any work blocked by an actual
failure.
