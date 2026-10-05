---
name: obsidian-cli
description: Use the official Obsidian CLI when a task needs Obsidian's running app, index, configured features, command registry, or developer runtime. Use for currently open notes and tabs, workspace state, daily notes, typed properties, tasks, links/backlinks, Bases queries, template resolution, link-aware moves, plugin commands, and plugin/theme debugging; do not use it for ordinary filesystem operations.
license: MIT
metadata:
  copilot-enabled-agents: opencode, claude, codex
  copilot-builtin-version: "2"
  copilot-upstream-revision: "a1dc48e68138490d522c04cbf5822214c6eb1202"
---

# Obsidian CLI

Use the CLI only for behavior that depends on Obsidian's running application,
indexes, settings, command registry, or developer runtime. Use normal shell
filesystem tools for ordinary file reads, writes, directory listing, and text
search.

## Capability probe and fallback

Copilot exposes the terminal-capable executable from the running Obsidian
installation as <code>COPILOT_OBSIDIAN_CLI</code> when it can resolve one.
Prefer that exact path over <code>obsidian</code> from <code>PATH</code>, and
always invoke it as a quoted executable rather than constructing a command
string. Before relying on the CLI, probe it using the active shell:

~~~bash
obsidian_cli="${COPILOT_OBSIDIAN_CLI:-obsidian}"
"$obsidian_cli" version
~~~

~~~powershell
$obsidianCli = if ($env:COPILOT_OBSIDIAN_CLI) { $env:COPILOT_OBSIDIAN_CLI } else { "obsidian" }
& $obsidianCli version
~~~

A command being present on PATH is not sufficient: the probe must exit
successfully. Use the selected executable in place of <code>obsidian</code> in
the examples below, resolving it again in a later shell call when necessary. If
the probe fails, continue with ordinary filesystem tools where they can satisfy
the request. Briefly tell the user only when the missing runtime capability
matters. Do not install Obsidian, change PATH, register the CLI, or raise the
plugin's minimum Obsidian version on the user's behalf.

The CLI requires a compatible Obsidian installer and a running app. Commands
can differ by version, so inspect live help before using a command whose syntax
is not already established:

~~~bash
obsidian help <command>
~~~

When a request truly needs the runtime capability and the probe fails, tell the
user to open Obsidian and enable **Settings → General → Command line
interface** using a compatible installer. Leave registration and any platform
repair steps to the user.

## Target precisely

Put <code>vault=&lt;name-or-id&gt;</code> before the command whenever the vault is
known. Use <code>path=</code> for an exact vault-relative path. Use
<code>file=</code> only when Obsidian's wikilink-style name resolution is
desired. Do not rely on the active vault or active file when a precise target
is available.

~~~bash
obsidian vault="My Vault" backlinks path="Projects/Plan.md" format=json
~~~

Parameters use <code>name=value</code>; boolean flags have no value. Quote
values containing spaces or shell-special characters.

## High-value indexed and configured operations

Use live help for exact parameters, then prefer these families when they add
meaning beyond raw files:

- Configured daily notes: <code>daily</code>, <code>daily:path</code>,
  <code>daily:read</code>, <code>daily:append</code>,
  <code>daily:prepend</code>.
- Typed properties and parsed metadata: <code>properties</code>,
  <code>property:read</code>, <code>property:set</code>,
  <code>property:remove</code>, <code>tags</code>, <code>tag</code>, and
  <code>aliases</code>. Supply a <code>type=</code> to
  <code>property:set</code> when the property is not plain text.
- Tasks: <code>tasks</code> for indexed listing and <code>task</code> with a
  stable <code>ref=path:line</code> or exact file/line for status changes.
- Link graph: <code>backlinks</code>, <code>links</code>,
  <code>unresolved</code>, <code>orphans</code>, and <code>deadends</code>.
- Bases: <code>bases</code>, <code>base:views</code>, and
  <code>base:query</code>. Prefer <code>format=json</code> for structured agent
  consumption.
- Templates: <code>templates</code> and <code>template:read ... resolve</code>
  when configured template resolution is required.
- Live workspace state: <code>tabs ids</code> lists the currently open tabs and
  their IDs, while <code>workspace ids</code> shows the workspace tree and its
  item IDs.
- Link-aware refactors: <code>move</code> and <code>rename</code> when the vault
  setting to update internal links should be honored.

### Inspect open notes

When the user asks about notes currently open in Obsidian:

~~~bash
obsidian vault="My Vault" tabs ids
obsidian vault="My Vault" workspace ids
~~~

Use <code>tabs ids</code> as the source of truth for open tabs. Keep entries
verbatim and classify them only when the output provides enough evidence:

- a Markdown note has an explicit vault path ending in <code>.md</code>
  (case-insensitive)
- another file-backed tab has an explicit vault path with a different extension
- a non-file view, such as search, graph, settings, or a plugin view, has no
  vault path

Do not infer a path from a display title, view type, or tab ID, and do not
discard entries that cannot be classified. For a request about open notes,
extract the Markdown paths while retaining the other tabs as workspace context.
Use <code>workspace ids</code> when tab groups or workspace hierarchy matter. Do
not substitute <code>recents</code>, which includes files that are no longer open.

If the tab output does not expose paths or view types clearly, correlate its tab
IDs with this read-only, structured workspace query:

~~~bash
obsidian vault="My Vault" eval code='JSON.stringify((()=>{const tabs=[];const active=app.workspace.getMostRecentLeaf();app.workspace.iterateAllLeaves(leaf=>{const path=leaf.view.file?.path??null;tabs.push({id:leaf.id,title:leaf.getDisplayText(),viewType:leaf.view.getViewType(),path,kind:path===null?"view":path.toLowerCase().endsWith(".md")?"markdown":"file",active:leaf===active})});return tabs})())'
~~~

The workspace query also returns sidebar and floating leaves. Only call an entry
an open tab when its ID appears in <code>tabs ids</code>; retain query-only
entries separately as workspace context. Preserve tab entries that have no
matching workspace entry instead of guessing their identity.

If the user asks for the single currently focused note and the tab output does
not identify it, use a read-only app query:

~~~bash
obsidian vault="My Vault" eval code="app.workspace.getMostRecentLeaf()?.view.file?.path ?? ''"
~~~

Use normal filesystem tools only for explicit paths returned by Obsidian, and
choose a reader appropriate to the file type. Do not read every open note when
paths or titles alone answer the request.

## Obsidian and plugin commands

<code>commands</code> lists registered command IDs, including commands provided
by plugins. Filter by an ID prefix, then execute the selected command with
<code>command id=&lt;command-id&gt;</code>. Never guess a command ID when it can be
discovered. Do not execute a discovered command whose effect is prohibited by
the host-session rules below.

~~~bash
obsidian vault="My Vault" commands filter="my-plugin:"
obsidian vault="My Vault" command id="my-plugin:run-action"
~~~

## Plugin and theme development

Use the CLI as the first choice for runtime verification after the normal build
or test command has produced artifacts:

1. For a plugin other than Copilot, reload with
   <code>plugin:reload id=&lt;plugin-id&gt;</code> when needed. Never reload the
   Copilot plugin from a Copilot-hosted agent session.
2. Inspect <code>dev:errors</code> and <code>dev:console level=error</code>.
3. Verify UI state with <code>dev:screenshot path=...</code>,
   <code>dev:dom selector=...</code>, and <code>dev:css selector=...</code>.
4. Use <code>dev:mobile on</code> only when mobile emulation is relevant, and
   turn it off afterward.

Read-only <code>eval</code> and <code>dev:cdp</code> queries are appropriate for
state that the documented inspection commands cannot expose. Keep expressions
small and return serializable values. Treat any expression or CDP call that
mutates application state as a risky operation requiring explicit user intent.

## Preserve the host session

Never reload or restart the Obsidian app or window from an agent session. Never
reload, disable, or uninstall the Copilot plugin that is hosting the agent. In
particular, do not use:

- any CLI command that reloads or restarts the app, window, or renderer
- any plugin reload, disable, or uninstall operation targeting Copilot
- any restricted-mode change
- a command ID, JavaScript expression, or CDP call that performs an equivalent
  app, window, renderer, or Copilot-plugin teardown

These actions terminate the in-flight agent and can discard its work. This is a
hard prohibition, not a confirmation-gated operation. If verification requires
one, finish all non-destructive checks and tell the user to perform the reload
manually after the agent session has ended.

## Risky operations require explicit intent

Do not perform the following merely because they are available:

- permanent deletion
- local-history or Sync restoration
- publishing or unpublishing
- plugin or theme installation/uninstallation
- mutating JavaScript evaluation or CDP calls

Confirm that the user's request clearly authorizes the exact target and effect.
Prefer reversible variants, such as trash-backed deletion, when they satisfy
the request. Explicit intent does not override the host-session prohibition
above.

## Exclusions

Do not teach or use the TUI, clipboard output, undocumented flags, platform
registration repairs, or CLI equivalents of generic filesystem operations in
this skill.

## Attribution

Adapted from <code>kepano/obsidian-skills</code> at revision
<code>a1dc48e68138490d522c04cbf5822214c6eb1202</code>. See <code>LICENSE</code>.
