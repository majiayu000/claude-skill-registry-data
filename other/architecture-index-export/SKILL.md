---
name: architecture-index-export
description: >
  Export an architecture as an index bundle (sa-index/1) for an architecture MCP server — the
  chunks a server embeds for search, the facts ledger its exact tools answer from, and one build
  pack per container the handoff kit covers (spec, interface contracts, assets byte for byte,
  flows and budgets, governing ADRs in force, open questions, an ordered build plan), so a developer's IDE
  can ask the architecture and build one component from its spec. By code; calls no model and no
  vector store; reads nothing compliance writes.
triggers:
  - export architecture index
  - export the architecture index
  - architecture index bundle
  - index the architecture
  - build packs
  - export build packs
  - architecture MCP bundle
  - publish architecture index
  - test the architecture index
  - publish a draft index
  - load the architecture into the knowledge base
  - start the local architecture index
---

# Architecture Index Export

Writes the bundle an architecture MCP server loads. One script, `scripts/export-index.js`; this skill runs it and reports.

## Steps

1. **Resolve `plugin_dir`**: `bun ~/.claude/plugins/marketplaces/shadowx4fox-solution-architect-marketplace/scripts/plugin-root.ts --plugin sa-delivery`.
2. **Export**: `bun [plugin_dir]/skills/architecture-index-export/scripts/export-index.js <project_root>`. Options: `--out <dir>` (default `.cache/sa-skills/index/<version>/`, or `…/index/draft/` for a draft), `--project-key <key>` (default: the architecture's name, slugified — keep it the same across releases, it is part of every chunk id), `--server <mcp_url>` (the server's URL, written into each pack's binding; without it the binding names none), `--previous <bundle>` (the last bundle the server holds — usually the previous release's: writes `changes.json`, what changed for each container since it), `--draft` (the draft channel whatever git says — what a test publish uses), `--no-kit-check` (development only: packs a kit without its gate).
3. **Report** what the script printed: the channel, the chunk counts by kind, each build pack with its open questions, every skipped component with its reason, every warning. Exit 1 means the bundle failed its own check — report the findings, never hand the bundle on.

The bundle is checked again on its own with `export-index.js --check <bundle_dir>`; a server or a CI job runs that before loading it. `export-index.js --diff <older_bundle> <newer_bundle> [--component <slug>] [--json]` compares any two bundles of one project — the reference for the server's `what_changed` — including two bundles of the same version, when a second publish replaced build packs (`same_version: true`).

## Test while writing

To try an architecture in the MCP before it is released (say "test the architecture index"):

1. **Publish the draft**: `bun [plugin_dir]/skills/architecture-index-export/scripts/publish-index.js <project_root> --up`. The script:
   - exports the bundle as a draft (`--draft`), even from a tree that equals its release tag, and runs the same check as CI;
   - posts it to the server's draft slot and waits until search is ready.

   `--up` starts the local server when nothing answers at `http://localhost:8080`: `local/compose.yaml` runs the MCP server — Alia — from the image its CI publishes (`ghcr.io/shadowx4fox/alia-mcp-server`, pinned by `SA_INDEX_SERVER_TAG`; `SA_INDEX_SERVER_REF=<branch|commit>` builds that one from source instead, `local/compose.source.yaml`) with the `file` engine (no Qdrant; the vectors stay on disk, so a restart re-embeds nothing) in Docker, embedding through the host's Ollama by default — the machine's GPU when it has one, about twenty chunks a second. Docker with the compose plugin (2.20 or later) is the only requirement; Ollama on the host is what makes it fast. The first start pulls the image and the embedding model. The script checks that a container can reach that Ollama (on Linux it must listen beyond localhost: `OLLAMA_HOST=0.0.0.0`); when it cannot, or the host has none, it says so with the fix and starts the `cpu` profile's Ollama container instead (about one chunk a second). `SA_INDEX_OLLAMA` overrides the choice. `SA_INDEX_ESCALATION_PROJECT` and `SA_INDEX_ESCALATION_REPOSITORY` (`SA_INDEX_ESCALATION_HOST`, `…_SERVER`) add `local/compose.escalation.yaml`: the server files that project's escalations on its git host, so an IDE agent's `preview_escalation` returns the issue to file — without it the server files none (10.6.1).
2. **Report** what it printed: the chunks and build packs, the components without one, and the line to add the server to Claude Code (`claude mcp add --transport http alia <server>/mcp`, once). Then ask with the project key and version `"draft"`.
3. **On the first publish** the script writes `.sa-skills/index.json` (`server`, `project_key`). Tell the user to commit it: the key must not change between publishes, and CI reads it when `SA_INDEX_PROJECT_KEY` is unset.

Each publish replaces the project's draft; the server re-embeds only the chunks that changed. Options:
- `--server <url>` or `SA_INDEX_SERVER`: a shared test server instead of the local one;
- `SA_INDEX_TOKEN`: the bearer token, when the server needs one;
- `SA_INDEX_PUBLIC_URL`: the base URL the local server builds each pack part's `download_url` from (`ARCHINDEX_PUBLIC_URL`, default `http://localhost:8080`) — the raw download `BUILD.md` tells the IDE agent to copy assets with; a shared server sets `ARCHINDEX_PUBLIC_URL` on its own deployment, or lists no `download_url`;
- `--project-key <key>`;
- `--no-wait`;
- `--timeout <seconds>` (default 1800).

Exit codes: 1 the bundle failed its check or the server refused it · 3 no server · 4 still indexing at the timeout. A laptop never publishes a released version; that is CI's job. To stop the local server: `docker compose -f [plugin_dir]/skills/architecture-index-export/local/compose.yaml down` (add `-v` to drop its data).

## In CI

`ci/publish-index.sh` is the step every pipeline runs: the plugin at a pinned tag (`SA_PLUGIN_REF`), the previous bundle from the server, the export, `--check`, then `POST` to the server. Examples to copy into the architecture's repository: `ci/github-actions.yml`, `ci/gitea-actions.yml`, `ci/azure-pipelines.yml`; on GitHub, `architecture-lifecycle`'s `ci/architecture-release.yml` chains the tag, phase 1 and the dispatch of the handoff regeneration (`ci/architecture-handoff.yml`) after a release PR is merged. Each one needs a project key, the server URL and a token.

A release publishes twice:

1. **At the tag `architecture-v<version>`**: the chunks and the ledger, so search goes live with the release. There are no build packs yet, because `lifecycle.js apply` tags before the kit can carry the new version.
2. **When the regenerated kit is committed** (`generate dev handoff`, then commit `handoffs/`): the same version again, with its build packs. It must carry the same chunks, the same ledger and every pack the server already holds for that version; it may add packs and replace them. The ledger carries no clock, so the same commit gives the same ledger, byte for byte.

A run whose architecture differs from its tag, or has uncommitted files, is a draft: built, not published, unless `SA_INDEX_ALLOW_DRAFT=true`. CI never generates the kit, because that needs Claude's agents. After a release, `lifecycle.js status` lists the kit as stale until it is regenerated.

The server contract the script calls: `GET {server}/bundles/{key}/before/{version}` (the newest older bundle, or 404) and `POST {server}/bundles/{key}/{version}?channel=released|draft` (201 stored · 200 a version held, the body naming the packs `added`, `replaced` and `unchanged` · 409 refused, the body's `reason` `chunks_differ`, `ledger_differs` or `packs_missing` with the packs). The script prints the packs on a 200 and the reason on a 409, and fails the pipeline on a 409.

## What the script decides

| Rule | Why |
|---|---|
| **Channel** `released` when the tag `architecture-v<version>` exists, `ARCHITECTURE.md`, `docs/`, `adr/`, `tdr/` at HEAD equal the tag's, the status is Released and nothing there or in `handoffs/` is uncommitted; anything else is `draft` | the kit lands after the tag and the version stays released; a server serves released versions by default |
| **Chunks** one per unit: `ARCHITECTURE.md` by H2, each H2 / H3 of a section file, every principle, flow, phase and `I-nn` block wherever it sits, each component descriptor, each docs/05 row without a block, each ADR / TDR (by H2 when over 6,000 characters); over 24,000 characters a unit is cut at blank lines, a long table by rows with its header | a search hit is one unit of meaning, small enough to embed |
| **Chunk text** opens with a context line (project › visible headings); HTML comments dropped; a Mermaid block replaced by `[Mermaid diagram — file:line]` | a chunk read alone says what it is about |
| **Chunk id** a UUID from the project key, the file and the anchor path (anchors where they exist); `content_hash` the text's | ids hold across releases, so a server re-embeds only what changed |
| **Metadata** components and ADRs from the ledger and the headers — a classified block names its own; exact names only | filters a server can trust |
| **Build pack** only from `handoffs/.manifest.json` of this architecture version, the component's own entry of this version, and `kit-check.js` clean on the shared documents and on every file of the pack | a developer never builds from an outdated or failing kit |
| **Security** the kit's `assets/NN-<slug>/security.md` (`security-obligations.js`) as its own part `security`, second in the plan: who may call, each interface's authentication, the Security by Design principle, the institutional ADRs the security section cites, the STRIDE findings, the Data Sensitivity flows, the security tests; `BUILD.md` carries its Inbound table | a contract with no security scheme is never read as a public operation; an interface without documented authentication fails closed |
| **Technical debt** (10.10.3) the TDRs the container's descriptor names on its `**Technical Debt:**` line, each a `tdr:TDR-NNN` part under `tdrs/`, read with the specification whose § 7 lists them; `pack.json` `tdrs` | the builder reads the workaround in force, not only its id |
| **Links** in a Markdown part, rewritten to the part's path in the pack when their target travels in it (an ADR, a TDR, an interface, a shared document), `#anchor` kept, `sha256` taken after; any other link as written | a link the builder follows resolves inside the pack |
| **Open questions** every `[NOT DOCUMENTED` line of the component's spec, security obligations, interfaces and assets | the builder asks; it never fills a gap |
| **What changed** per container between two bundles, by hash and ledger only: its facts (name, type, technology, internal name, component version, system), contracts and interfaces added / removed / changed, governing ADRs, its spec, its security obligations, its build instructions and the shared documents, the pack's revision (the `sha256` of its `pack.json` in the manifest; `pack_revised` when it moved), the flows it takes part in from each version's ledger (target, each phase's budget and hops — with or without a pack), the integrations naming it with each changed field, the chunks naming it, open questions new and resolved. `action_required` when the code must move: removed, a name / type / technology / internal name, a contract, an interface, an integration row naming it, a flow or budget it runs in, the spec or the security obligations — a component version alone, or build instructions that moved alone (the MCP URL of the binding), is listed, not an action | `what_changed` tells a developer what to update, and what can wait |
| **`BUILD.md`** per pack, from `templates/BUILD.md`: the `.architecture.json` binding (with a `pack_revision` the agent records from `get_build_pack` — the export cannot write it, since it is the hash of the pack that carries the binding — and passes to `what_changed` as `from_revision`), eight rules (contracts exactly, each asset kept byte for byte under `architecture/` in the service repository — `sha256` checked, overwritten and committed alone before the code on an update, so the IDE and the pull request show the contract diff natively —, the architecture's names, never fill a gap, security never a gap — deny by default, fail closed —, standards and ADRs, budgets, the team's template for the stack, record the version and the revision, and — 10.6.1 — what only the architect can answer: on a RUN-team project (`support` in `.sa-skills/project.json`) a question that blocks the build is escalated with `preview_escalation` — its `request` the developer's task in their words, never their yes (10.6.3) — → the user's yes → `file_with` → `record_escalation`, never kept in a local file; otherwise it goes to the architects through the team's channel; and — 10.7.0, a RUN-team project only — rule 10: a Tier 0 write (a workaround's TDR, a TDR move, a Proposed ADR, a doc fix) is requested with `preview_tier0` → the user's yes → `file_with` → `record_tier0`, never made in the service repository; the bundle's `support` carries `tier0_kinds`, `tdr_moves`, `tdr_statuses` and `tdr_drivers` for that preview), the plan with every part, the security table, interfaces, flows and budgets, open questions, a done list — English, the instructions of an agent; titles carry canonical names; **an unattended build** (10.10.0 — a CI job or a platform's agent, declared by `"supervision": "unattended"` in `.architecture.json`) turns a question into a `TODO(architecture)`, files its escalations with its own identity, files a Tier 0 request **without** `architecture-tier0` (a person applies it — the approval; the workflow refuses a bot and `SA_TIER0_AGENTS`), and lists all of it under *Architecture requests* in its pull request (`docs/RUN_TEAMS.md` § Who consumes the index) | the instructions the server hands an IDE agent, or an unattended build agent, through `get_build_instructions` |

Never read: `compliance-docs/`. The plugin calls no embedding model and no vector store — that is the server's.

## Output

```
manifest.json        schema sa-index/1, project, architecture, channel, git, counts, build packs, skipped, warnings, files + sha256
chunks.jsonl         { id, content_hash, text, meta: { project, architecture_version, channel, doc_language, kind, file, lines,
                       title, anchor, components, adrs, … } }   kind: overview section principle flow phase integration component adr tdr
ledger.json          the facts ledger (arch-facts.js), without the absolute project path
changes.json         with --previous: { from, to, same_version, components: [{ component, action_required, facts, contracts, interfaces, adrs,
                     documents, flows, integrations, sections, open_questions, pack, pack_revised, pack_revision: { from, to } }] }
buildpacks/<slug>/   pack.json { component, parts, plan, flows, interfaces, adrs, open_questions, instructions } + BUILD.md, spec.md,
                     security.md, interfaces/, assets/, adrs/, cross-cutting-standards.md, runtime-view.md
```

## Permissions

`Bash(bun *)`, `Bash(git *)`, `Write(.cache/sa-skills/*)`, `Write(.sa-skills/index.json)`. `--up` runs `docker compose` from inside the script; no separate grant is needed.
