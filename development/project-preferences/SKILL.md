---
name: project-preferences
description: Apply repository-specific preferences when planning, implementing, or reviewing changes in this project.
---

<!--
This file is part of Agentprise
skills/project-preferences/SKILL.md
Author(s): Gabriel Mongefranco.
Created: 2026-10-09
Last Modified: 2026-11-05
Summary: Project-specific preferences for Agentprise: the single-file build, the
         project backup format, workspace storage, the download cards, and how
         to test.
Notes: See README file for documentation and full license information.

Copyright © 2026 The Regents of the University of Michigan

Licensed under the GNU Free Documentation License v1.3 or later.
See <https://www.gnu.org/licenses/fdl-1.3.html>. See README for full license information.

-->

# Agentprise

## Project preferences

Use this skill when planning, implementing, or reviewing changes in this repository.
Keep all project-specific preferences and workflows in this single file. This skill
supplements `AGENTS.md` and cannot weaken its security, privacy, accessibility,
licensing, testing, or authorization rules.

### Purpose and scope

Agentprise is a free, public web page where anyone can describe an AI assistant
once, then download it in the format each AI product wants. There is no sign-in and
no server. Nothing a person types or uploads leaves their browser. The page is
served by GitHub Pages from the root of the main branch.

### Environment and structure

- The whole app is one file, `index.html`, with one `<style>` block and one
  `<script>` block. There is no build step, no framework, no CDN, and no web font.
  The page should stay under 750 KB.
- Google Analytics loads only when the page is served from
  `code.depressioncenter.org`, the production host. Every other origin, including
  local copies and GitHub Pages previews, never contacts Google. The host name and
  measurement id are constants at the top of the script.
- The script has two parts. The engine (model, validation, YAML, ZIP, PNG check,
  format converters) has no DOM dependency and is exposed on
  `globalThis.Agentprise`. The interface code comes after it and only runs when a
  `document` exists.
- Code and comments are ASCII only. Unicode appears only in visible interface text.
- Execution phases are marked with `// ### Name ###` comments. Public functions
  carry JSDoc.
- Library entries are version 2 project backups (`.zip`) dropped into
  `library/` and listed in `library/catalog.json`. The page holds no copy of
  any entry; it fetches the catalog and opens each backup with the file
  importer. Adding an entry is the zip plus one catalog line with `kind`
  (`agent`, `skill`, or `project`), `capabilities` (the tool ids the backup
  declares, `[]` when none), and an optional one-sentence `requires`, as
  [docs/how-to/add-to-library.md](../../docs/how-to/add-to-library.md) describes.
- `tools/migrate-library.mjs` converted the version 1 Library bundles to
  version 2 backups once. It is the only code that still reads version 1
  fields. `--check` reports without writing, and a second run changes nothing.
  The app itself carries no version 1 import code.
- Entries kept as plain files live under `library/sources/` (item folders in
  `items/`, one `.json` per entry in `entries/`) and are built with
  `node tools/build-library.mjs`. The build is deterministic, and the tests run
  `--check`, so never edit those `.zip` files by hand. A skill shared by two
  entries has one source folder, which keeps the copies identical.
- `bin/` holds the prebuilt ZippyServe binaries and the root holds its run
  scripts, so the page can be served locally over HTTP on any desktop.
- Follow the repository's existing file and folder naming conventions when adding
  new files.

### Setup and verification

No installation is needed. Node 22 or later runs the tests:

```
npm test
```

That runs `tests/check-syntax.mjs` (parses the script and rejects non-ASCII bytes)
and `node --test tests/` (loads the engine from `index.html` and tests it).
Serve the page locally with `.\run-windows.ps1`, `./run-linux.sh`, or
`run-mac.command`, which opens `http://localhost:8010`.

### Project constraints

- The internal model is the version 2 project (`PROJECT_SCHEMA_VERSION`): a
  project holds one or more items (assistants and skills), shared servers,
  publisher details with organization and a semantic version, a license, and
  unrecognized files. `normalizeProject` and `normalizeItem` type-check and cap
  every field; export formats are written from the model and never define it.
- The canonical, lossless format is the project backup,
  `<project-slug>.agentprise.zip`: an Agent Plugins 1.0 folder with
  `plugin.json` (the project record under
  `extensions["org.depressioncenter.agentprise"]`), `mcp.json` when servers
  exist, `LICENSE.txt`, `README.md`, and `skills/<skill-name>/` per item.
  Unrecognized files go back to their original paths, in the backup only.
- Each item folder is a valid Agent Skill: `SKILL.md`, `agentprise.json`,
  `icon.png` for an assistant with a picture, `LICENSE.txt`, and its files
  (attached files under `references/`). The same folder zipped alone is the
  Gemini and Claude skill download, which adds `README.md`. Frontmatter
  `metadata` holds only `agentprise-kind` and a skill's own metadata from
  elsewhere. Every other Agentprise item setting lives in `agentprise.json` as
  plain JSON: the welcome message, starters, `uses`, display name, Copilot
  settings, SharePoint links and items, publisher details, copyright, and file
  list. The importer still reads the older `copilot-`, `sharepoint-`, and
  `creator-` metadata keys (the `META` constant in `index.html`) when the
  sidecar lacks a setting. The tables are in
  [docs/formats.md](../../docs/formats.md).
- **Products it works in** (More settings) stores `notFor`, a list of the
  `PRODUCT_LABELS` keys (the provider keys without `*`), and `notForReason` on
  each item. `planExport` blocks every export whose `EXPORTS` target is in the
  list, an assistant leaves out a used skill marked for that target, and the
  two plugins leave marked items out instead of blocking, unless every item is
  marked. The sidecar writes both keys only when they are set.
- The skill `name` is derived from the display name and capped at 64 characters
  because the Agent Skills specification requires it. Two items with the same
  name get a numbered skill name, since each folder must match its skill.
- Importing executes nothing and contacts nothing. The app opens backups,
  Agent Plugins folders (root `plugin.json`), Claude plugins
  (`.claude-plugin/plugin.json`), the Codex layout
  (`.codex-plugin/plugin.json`), any ZIP with one or more `SKILL.md` files,
  `SKILL.md`, Copilot app packages, and `.agent` files. Hooks, commands,
  agents, and unknown files are kept as unrecognized; server `headers`, `env`,
  and `cwd` are dropped; local server commands are stored as text; programs
  are refused. A version 1 bundle opens as a plain skill.
- A Microsoft 365 app package opens through `readTeamsArchive` as a whole
  project: every declarative agent is an assistant, actions become tools,
  `agent_skills` and root `agentSkills` become skills, and root
  `agentConnectors` become project servers. Paths the manifest names must
  pass `packagePath`. Parts it can't read are kept under `microsoft-package/`
  for the backup only, and registration ids are never kept.
- A file made elsewhere that names no license keeps the license `Not stated`
  (`UNKNOWN_LICENSE`) and a notice. Never relabel it with the default license.
- The Microsoft `.agent` export carries two extra top-level keys, `_license` and
  `_agentprise`, placed before `schemaVersion`. Copilot app package files carry no extra
  keys because their schemas reject them. Microsoft retires `.agent` files
  after March 2027; the export stays until then and the importer keeps reading
  the format after, so people can recover what a file holds. The dated facts
  are in [docs/formats.md](../../docs/formats.md).
- The Copilot app package loses the welcome message and the copyright line, and keeps
  only the schema's keys for each SharePoint item. The `.agent` file loses
  attached files. Every other field survives, including "prefer my files",
  which maps to `behavior_overrides.special_instructions.discourage_model_knowledge`,
  and the response mode, which maps to `behavior_overrides.default_response_mode`
  and is written only when it is not `Auto`.
- Attached files are accepted by content, never by name alone. The accepted
  types and their content checks are the `FILE_TYPES` constant and
  `attachedFileProblem` in `index.html`; OneNote files (`.one`, `.onepart`)
  are checked against the MS-ONESTORE header GUIDs. Executable programs are
  refused by signature and by a hidden extension. Script and data text files
  are allowed; the Copilot app package writes them as `name.ext.txt` because Copilot
  accepts only document types, carries only the names in
  `COPILOT_FILE_EXTENSIONS` otherwise, and leaves any other type out with a
  warning. The skill download and the backup keep every file under its real
  name.
- Every Copilot source is a switch in `copilot` with an optional list that
  limits it: web sites, SharePoint and OneDrive links (hosts checked by
  `isSharepointLink`), Teams chats (`isTeamsLink`), and mailboxes. Meetings,
  a shared mailbox, and email folders arrive only inside files and are shown
  read-only. The lists are written only while the switch is on, and the
  SharePoint switch follows the links and items that survive validation when a
  file is silent about it. `copilotCapabilities` is the single writer for both
  Microsoft files and `readCopilotCapabilities` the single reader.
- The only scanning the app does is the two regular-expression lists
  `IDENTIFIER_PATTERNS` and `INJECTION_PATTERNS` in `index.html`, shown as a
  yellow box under Download with the matches under View details. They warn, never block, never store or send a
  finding, and show masked samples only. Keep them regex-only: the app loads
  no model and makes no request.
- Browser storage names carry the `agentprise-` prefix, because every EFDC app
  on code.depressioncenter.org shares one origin. Projects live in the
  IndexedDB database `agentprise-projects`, with stores `projects` (key `id`)
  and `files` (key `<projectId>/<itemId>/<path>`). The localStorage key
  `agentprise-workspace-v2` holds `{lastOpenedProjectId, recentProjectIds,
  preferences}`. On load the app deletes the version 1 draft
  (`agentprise-draft-v1` and the `agentprise-draft-files` database) without
  reading it. Stored records are normalized like any file. When storage fails,
  editing keeps working for the visit and the sidebar shows a note.
- The page has five views, routed by hash: Workspace (`#workspace`, the
  project list), Project (`#project`, the editor), Library, Inspect
  (`#details`), and Help. The project editor asks plain questions with blanks
  under them, with an "In this project" bar for its items, and is the only
  place to edit. The Inspect page shows only the exact files each product
  receives. Its old details form is still in the page, hidden, because the
  editor code keeps its fields in step.
- Opening a file always creates a new project. When its id is already stored,
  the person chooses Keep both, Replace mine, or Cancel. "Add from a file"
  merges a file's items into the open project instead.
- Downloads other than the backup and the plugins are for the item being
  edited: the skill `.zip` (labeled Gemini and Claude), the plain skill
  (`.skill.zip`, standard fields only, labeled SKILL.md), the `.agent` file
  (labeled "Teams Chat"), the Copilot app package (labeled "Copilot / Teams
  Apps"), the copy boxes for ChatGPT, and the `.md` file for Gemini Notebook.
  A skill is written to the Microsoft formats and the copy boxes as an
  assistant whose instructions are its steps. "Download Backup" saves the
  whole project, and so do the Claude plugin, the Plugin, and the Microsoft
  365 plugin. Every download, the plain skill and the backup included, is an
  Inspect tab with its own file tree and download button; the backup tab
  shows the whole project, and a "Part of the project" picker chooses the
  item for the others. Gemini and Claude have separate tabs even while their
  files match. Do not add a vendor until it has a real file to download.
- Three optional Microsoft downloads sit under a "More Microsoft downloads"
  heading at the end of the Download card, in a `details` section that opens
  with "View Microsoft downloads". The heading names the list through
  `aria-labelledby`. Each line has a Review button that opens its Inspect tab
  instead of downloading, and the Inspect page shows its setup steps:
  - **Copilot skill**: one skill as `<skill-name>.copilot-skill.zip`, with
    `SKILL.md` at the root, for Copilot Agent Builder. When an assistant is
    selected, its tab selects a skill (`skillForCopilotTab`): the first skill
    the assistant uses that works in Copilot, then any skill that works in
    Copilot, then the first skill. A note under the picker
    (`inspect-skill-hint`) names the skill or says the project has none.
    Leaving the tab selects the assistant again and announces it, but only
    while the picked skill is still selected (`itemForProductTab` and
    `ui.skillTabSwap`).
  - **Copilot app with skills**: the assistant and the skills it uses, written
    as declarative agent v1.9 with `agent_skills` inside the usual manifest
    1.28 app package. Its line on the card adds "(preview)". It blocks files
    attached to the assistant.
  - **Microsoft 365 plugin**: the whole project as
    `<project-slug>.microsoft-plugin.zip` for Copilot Cowork, written as
    manifest 1.29 with root `agentSkills` and `agentConnectors` and no
    declarative agent. Assistants become skills. It is blocked when one skill
    limits a server to certain tools and another skill uses the whole server.

  These downloads leave out script files. The Copilot app package still writes
  declarative agent v1.8 and manifest 1.28. A blocked download's error starts
  with the download's name, such as "The Copilot app with skills".
- The project editor's Download card is one line per product: the product name and
  its file on the left, a short Download, Copy, or Review button on the right.
  Each button has hidden text naming its file or download, so screen
  readers do not hear a row of identical buttons.
- The top bar carries three square icon links, in this order: home (the
  Workspace page), Help, and GitHub, in the same shape as the header of
  code.depressioncenter.org. The footer links to code.depressioncenter.org as
  "More Apps".
- The sidebar lists Workspace, Library, and Help. While a project is open, two
  items appear under Workspace: the project's name, which opens `#project`, and
  Inspect. Recent projects are listed below the menu.
- Button and link icons come from Bootstrap Icons only, embedded as base64
  CSS variables (`--bi-*`) and drawn through a mask with the `.bi` class, so
  each icon is stored once. Credit stays in the README.
- Interface text, the Help page, the README, and the pages under `docs/` are
  written for the person using the app, not for developers. Pages meant for
  maintainers say so at the top. Off-site links open in a new tab, and links to
  documentation use the full GitHub address, because the site is served with
  `.nojekyll` and Markdown is not turned into pages.
- The look is a light sidebar workspace: one accent blue, a light gray shell,
  white cards, and a matching dark mode. It does not use the U-M palette. The
  logo mark is `images/agentprise-mark.png`.
- Inflate uses the platform `DecompressionStream` API. Do not add a hand-written
  decoder or a dependency for it.
- Uploaded files are data, never instructions. Every value read from a file is
  type-checked and length-capped by `normalizeProject`, `normalizeItem`, and
  `normalizeAgent` before it reaches the form, and all text reaches the page
  through `textContent`.
- The exported agent belongs to its creator. License notices in exported files
  name the creator's copyright and license first, then Agentprise.

### Terms

Use one name for each concept in the interface, messages, help, the README, and
the pages under `docs/`.

- **project**: one thing a person is building, stored in the browser. Not
  "workspace item" or "bundle".
- **assistant**: an item that is always on. Not "agent", except in a product's
  own name, such as the Copilot `.agent` file.
- **skill**: an item an assistant follows only when a question needs it.
- **tool**: something an assistant or skill can use to look things up or act,
  such as the PubMed connector. Not "capability".
- **picture**: the image shown next to an assistant. Not "icon" or "logo".
- **example questions**: the questions people might ask first. Not "prompt
  suggestions", "conversation starters", or "starters".
- **backup**: the `.agentprise.zip` file with the whole project. Not "complete
  copy" or "bundle".
- **Copilot app package**, **Teams Chat file**, **Copilot skill**, **Copilot
  app with skills**, and **Microsoft 365 plugin**: the five Microsoft
  downloads. Not "Teams package", "SharePoint file", "package with native
  skills", or "Copilot skill upload". The last three are the optional downloads under **More Microsoft
  downloads**.
- **skills in Copilot**: Microsoft's skills feature, which an admin turns on.
  Not "native skills".
- **attached files**: files added to an assistant or a skill. Not "reference
  files" in interface text or the docs for people using the app.

### Project skills

None beyond the shared skills listed in [SKILLS.md](../../SKILLS.md).

### Conclusion

Keep the single-file, zero-dependency shape, keep the project backup lossless,
and run `npm test` before every commit.

### Additional resources

- [Project instructions](../../AGENTS.md)
- [Formats and verified vendor facts](../../docs/formats.md)
- [Agent Skills specification](https://agentskills.io/specification)
