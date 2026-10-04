---
name: import-project
description: Adopt an EXISTING project — codebases, recordings, documents, loose notes — into this Omnia Vault. Use when the user says "import my project", "bring in this repo", "build the vault from what we already have", or drops folders/files into the vault root and wants them wired into the knowledge system.
---

# Import Project — build the vault around what already exists

Goal: end with (1) every code repo graphed and gitignored, (2) every valuable
document/recording captured as a Raw source and compiled into Wiki notes,
(3) a project note + topic hub that tie it together, (4) a green maintenance
gate, (5) a stamped relay baton. Work incrementally and commit as you go.

## Step 1 — Inventory

Have the user place (or confirm) the material in the vault root: repo folders,
media files, document folders. Then:

```bash
python scripts/setup_vault.py --inventory
```

This writes `_relay/IMPORT-INVENTORY.md` (repos / media / documents / loose
markdown). Review it WITH the user: confirm what to import now, what to skip,
and what order matters. Don't ingest everything blindly — value first.

## Step 2 — Code repos → graphify (Layer 1)

For each confirmed repo:

1. Keep outside code out of the vault's git:
   `python scripts/setup_vault.py --gitignore-repos`
2. Build its graph + browsable notes (see the `graphify` skill):
   `/graphify <repo> --obsidian --obsidian-dir graphify/<repo>` — or CLI:
   `graphify <repo-path> --obsidian --obsidian-dir graphify/<repo>`.
3. Install the auto-rebuild hook inside the repo: `graphify hook install`
   (re-run after any fresh clone).
4. Snapshot refresh from now on is `python scripts/sync_graphs.py` (part of
   `save`).
5. Convention that ties code to knowledge: compiled Wiki notes carry a
   `## Code Graph` section linking to `[[graphify/<repo>/_COMMUNITY_…]]` (or
   node) notes. Use **path-qualified** links — community names collide across
   repos.

## Step 3 — Project + topic seed

```bash
python scripts/setup_vault.py --name "<Project Name>" --topic "<domain>"
```

Fill the project note's Goal / Status / Next Steps from what the user tells
you — this note is the hub the whole import hangs off.

## Step 4 — Documents & notes → Raw sources → Wiki

For each confirmed document (per `llm-wiki-ingest`):

1. Capture cleaned Markdown in `Raw/Sources/<date>-<slug>.md` with source
   frontmatter. PDFs/Word docs: extract text faithfully; web pages: use the
   `defuddle` skill; images/diagrams: transcribe content to text, image itself
   to `assets/`.
2. `search-catalog` first; enrich existing notes over duplicating.
3. Compile short, focused Wiki notes (right folder + tag, one idea each),
   `sources` + `source_count` accurate, `[[wikilinks]]` into the topic/project.
4. Loose `.md` files at the vault root: either move into `Raw/Sources/` with
   frontmatter (if they're source material) or compile their content into Wiki
   notes and delete the original (if they're informal notes). Nothing valuable
   stays unfiled at the root.

## Step 5 — Recordings → video-ingest

Meetings, demos, screen captures, reference videos from the inventory's media
list: run the `video-ingest` skill per file (background extraction, frames ⇄
transcript correlation, Raw source + compiled notes + screenshots).

## Step 6 — Gate, baton, commit

```bash
python scripts/wiki_tool.py doctor
python scripts/wiki_tool.py build
python scripts/wiki_tool.py lint
python scripts/wiki_tool.py source-scan --update --accept-covered
python scripts/wiki_tool.py source-lint
python scripts/audit_public.py
```

Then hand off per the `relay` skill (STATE.md rewritten + stamped) and commit.
Suggest `python scripts/setup_vault.py --prune-demo` once real content stands
on its own.

## Rules

- **Never commit outside repos into the vault's git** (and never commit vault
  tooling into theirs — use `.git/info/exclude` inside a repo if needed).
- **Big binaries stay out**: media stays where it lives (or `Raw/Files/`,
  gitignored); only curated screenshots go to committed `assets/`.
- **Import is compilation, not relocation**: the win is short linked notes +
  graphs, not a pile of moved files.
- Secrets: redact on capture; `audit_public.py` is the backstop, not the plan.
