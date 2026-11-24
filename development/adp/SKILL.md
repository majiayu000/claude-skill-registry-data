---
name: adp
description: "ADP (Artifacts Done Properly) is a protocol and framework for structured Claude Artifacts and Sites pages: a thin shell, the record in the artifact's database mapped to the page's parts, changes sent as records instead of republishes, and pages built from a shared catalog of kits, themes and templates. Load it FIRST, before writing any HTML and before calling the Artifact or ArtifactData tools, whenever the user wants a new artifact page, board, tracker, dashboard, assistant or record that will be kept or changed again; wants to edit, republish or answer comments on an ADP artifact; says ADP, adp.py, catalog, kit, theme, template, part id, watch the artifact, requests or presence; wants an existing artifact put on ADP; or is setting ADP up for the first time. Skipping it means republishing and rebuilding by hand what the record and the catalog already hold."
license: Apache-2.0
metadata:
  version: "2.3.0"
---

# ADP: Artifacts Done Properly

## What ADP is

A protocol and a framework for structured artifacts. The page is a thin shell. The record lives in the artifact's database, mapped to the page's regions (parts). Changes are records, not republishes. Because it runs on claude.ai's own features (conversations, comments anchored to parts, the watcher, the picker), a person and an agent edit the same page together.

## How it runs

1. Publish: one Artifact call publishes the shell with its seed packs beside it. The page expands them into its database on its first open by an editor, its inbox applies the proposals, and it maintains its own `catalog.json`. Nothing else.
2. Edit: work locally in `.adp/`, as if it were the artifact itself. One command computes the diff by part and file hash and writes a seed-like JSON. That goes in through ArtifactData. No republish.
3. Build: write kits, templates, themes, patterns, viz, components and pages, reusing what the catalog already has, with the page's own style in its custom CSS. Kits are versioned, files hashed, and headers carry the metadata that ties the system together.

Why it is efficient: the agent never retypes, re-reads or republishes what the system already holds. It sends small hashed records, and the page does the conversion, publishing and bookkeeping itself.

Where each change goes:
- The page's own files and parts (`index.html`, `adp.js`, `parts/`, `styles/`) are recorded in `manifest/current`. They change by the loop: `adp.py export`, edit in `.adp/`, `adp.py propose`, one ArtifactData batch. The page's inbox classifies the proposal against the manifest and applies it.
- Kits, templates, themes, patterns and viz change as catalog entries, by proposal. A page's own look goes in its custom CSS, not into a kit.
- `catalog.json` is the catalog page's own: it updates it after applying a kit. Never send it.
- Concurrency is claude.ai's own: `if_version` pins each ArtifactData write and `ifMatch` each published file, so a stale write is refused, and the inbox holds a proposal whose files moved.

Nothing here is a gap to work around by hand or by a republish. If a step seems missing, read `adp.js` and the inbox (`kit/patterns/inbox.js`) before adding one.

Every piece of the page is a part with a stable id and a content hash, comments anchor to part ids, and one ArtifactData layout holds the record. claude.ai's version pins (`if_version` on a db write, `ifMatch` on a file) let several editors work on one page safely. New artifacts use the adp/2 layout (a thin shell plus files per part, copy stored as data). `adp.py` computes hashes and diffs and prints the exact Artifact and ArtifactData calls, so nothing is retyped by hand.

## Run the tool

`adp.py` lives in `scripts/` of THIS skill's folder. Run it as:

`python3 -I <this skill's folder>/scripts/adp.py <subcommand>`

Use `--help` or a subcommand with no arguments to see its usage; do not guess a subcommand, a guessed one does not exist and costs a turn.

For local Claude/Codex messages, presence and Codex chat delivery, read
[the local bus guide](refs/local-bus.md). Its commands, diagrams and verification
limits are maintained there; run the separate `scripts/adp_bus.py` helper.

## First run: check before anything else

1. Is `~/.adp/config.json` or `./.adp/config.json` present? If yes, ADP is set up: go to the table.
2. If not, run `adp.py setup --dry-run`, then ask the user ONE question: which scope (`user`, `project` or `local`). Run `adp.py setup --scope <answer>`. When nobody can answer (an unattended session), use `user` and say so in your report. It copies the four road skills into the skills folder, writes the config and puts the shipped catalog into `~/.adp/catalog` (never overwriting a file that is there); a road skill folder already there that differs (an older release, or local edits) is replaced by the packaged one, so run it again after installing a newer `adp.skill`. In a plugin install (this skill is listed as `artifacts-done-properly:adp`) it copies none: the plugin serves the road skills itself, so they follow its updates and a copy would only go stale. A config that already exists is kept: setup only adds the keys it lacks and overwrites no value. A real run needs `--scope`: without it, or with `--help`, setup prints its usage and sets nothing up. It only prints the lines it would add to CLAUDE.md; add them with `--yes` only if the user agrees.
3. To onboard just a project folder, run `adp.py init [DIR]`. `init` and `setup --scope project|local` also register the project (name, scope, absolute path) in `~/.adp/projects/<name>/config.json`; `adp.py projects` lists the registered projects, so a project is found from any folder.

## Which road

Choose the host as well as the road. For a Sites page, read [ADP on Sites](refs/sites.md)
before creating, editing or publishing. That guide applies to both Claude and Codex;
use native Sites source/record tools in place of the roads' Claude host calls.

| The user wants | Load skill |
|---|---|
| a new artifact page, board, tracker, assistant or record | `adp-new` |
| to find, use, take or add a catalog component, theme or template | `adp-catalog` |
| to edit or publish an artifact others also work on, or answer its comments | `adp-edit` |
| an existing artifact put on ADP (adopt it, move it to adp/2) | `adp-adopt` |

In a plugin install the road names carry the plugin's prefix, for example `artifacts-done-properly:adp-new`. Each road is also a plain file: `../<road>/SKILL.md` beside this skill's folder in a plugin install (for example `../adp-new/SKILL.md`), `refs/<road>/road.md` in a zip install. When the Skill tool does not know a road, read that file; setup is not needed for it. Each road is complete on its own; the full standard is `~/.adp/catalog/kit/guides/artifact-dataplane.md` (setup puts it there; read it only when a road leaves a question open). Run `adp.py` with no arguments for the real command list; if a road names a command it does not list, the command does not exist.

When a page documents a repository, [source review drift](refs/source-drift.md)
maps committed file changes to affected chapters/parts without model calls.
Use it to report review needs; catalog header drift and runtime integrity check
different boundaries.

## Log

Every `adp.py` command appends one JSON line to `log.jsonl`: in `./.adp/` when a project config exists, else in `~/.adp/`. Show recent lines with `adp.py log -n 20`. Read it first when asked what was done or why something failed.

## Always

- Work from the live record: `adp.py export` before you edit. claude.ai refuses a stale write by itself (`if_version` on every ArtifactData write, a conflict on a publish over a newer version, `ifMatch` on each published file): re-read and redo, never force.
- Say what a command or a read did not confirm when you tell the user, so they know what to check; this includes whether this session is watching an artifact (only the publish result or the ArtifactComments tool says so). A publish result that says live subscription is not supported from this session means you are not watching: tell the owner in one line, read `requests/` when they say go, and carry on.
