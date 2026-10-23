---
name: visual-recap
description: 'Builds local-only visual recaps from Git diffs. Use when recapping a finished branch, visualizing a commit range, or reviewing working-tree changes visually.'
argument-hint: '[base..head | branch]'
allowed-tools:
  - Read
  - Write
  - Bash(env:*)
  - Bash(mktemp:*)
  - Bash(npx:*)
  - 'Bash(${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/visual-recap-collect.sh:*)'
  - 'Bash(${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/visual-egress-guard.sh:*)'
---

# Visual Recap (LOCAL-ONLY)

`/visual-recap` builds a visual plan **from** a diff, not toward one. It is the reverse of
forward planning: instead of describing the change you are about to make, you describe the
change that was just made, at a higher altitude than line-by-line review. Schema, API,
file, and architecture changes become the same `data-model`, `api-endpoint`, `file-tree`,
and `diagram` blocks a forward plan would use, only now they summarize work that exists. A
reviewer scans the shape of the change before spending attention on the literal lines.

**Operational context:** Keep recap content local-only: write docs/prps/reviews/visual/ and preview through the localhost bridge; never upload code to hosted services. Accept a Git range, branch, or tracked working-tree diff; behavior is remote-agnostic.

## LOCAL-ONLY mandate — read this first

> This ycc port **inverts** the upstream BuilderIO `visual-recap` skill. Upstream
> ALWAYS publishes the recap to the hosted Agent-Native Plan database and FORBIDS
> inline output ("a recap's entire value is the hosted plan"). **This skill does the
> opposite.** It is permanently pinned to local-files mode and MUST NOT regress to
> any hosted Plan create tool.

Hard rules for this skill:

- **`AGENT_NATIVE_PLANS_MODE=local-files` prefixes every Agent-Native runtime
  command.** Do not rely on a process-wide export. The recap never writes to the
  hosted Plan database.
- **NEVER call a hosted Plan create/publish tool.** The hosted recap-create tool,
  `create-visual-plan`, `import-visual-plan-source`, `update-visual-plan`,
  `patch-visual-plan-source`, `get-plan-feedback`, `export-visual-plan`, and
  `set-resource-visibility` are all **disabled** in this skill. They are listed only
  to be explicitly excluded — do not invoke them.
- **The ONLY permitted Plan application request is the pinned block-catalog CLI command**
  (`env AGENT_NATIVE_PLANS_MODE=local-files npx -y @agent-native/core@0.59.1 plan blocks --out <path>`).
  It carries no recap content. Do not call the `get-plan-blocks` MCP tool; local-files
  mode does not register an MCP server. `npx` may contact the npm registry to resolve
  that exact package version, but it must never send plan or recap content.
- **The deliverable is local MDX** under `docs/prps/reviews/visual/<slug>/`, served via
  the localhost bridge
  (`env AGENT_NATIVE_PLANS_MODE=local-files npx -y @agent-native/core@0.59.1 plan local serve --open`,
  127.0.0.1, ephemeral port). There is no hosted link and no shareable URL.
- **Diffs are sourced through the shared collector**
  `${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/visual-recap-collect.sh`, which uses
  local git refs only — so it behaves identically against the public `github` remote and
  the private Forgejo `origin` (no vendor PR API, no hardcoded host or trunk branch).

For the pinned `@agent-native/*` install, the localhost-bridge command surface,
the hosted-only MCP connector, and the hosted-egress policy, read — do not duplicate —
`${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/agent-native-setup.md`.

## When to use

Build a recap when a change is large, multi-file, or touches schema, API contracts,
or architecture, and a reviewer would benefit from seeing the change mapped to
structured blocks before reading the raw diff. Skip it for small, single-file, or
obvious diffs when choosing proactively — a recap is review overhead, and a tiny
change reviews faster as plain diff. An explicit `ycc:visual-recap` or
`/visual-recap` invocation overrides this heuristic; honor the request.

## Phase 0 — Collect the diff (remote-agnostic, local refs only)

Drive the shared collector with `$ARGUMENTS`. Invoke it directly, then retain the
absolute path printed on stdout as the resolved bundle path:

```bash
# (none)         → tracked working-tree diff vs HEAD
# <base>..<head> → explicit range
# <branch>       → branch as head; base = merge-base against tracked upstream
${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/visual-recap-collect.sh $ARGUMENTS
```

The collector writes a bundle under `docs/prps/reviews/visual/<slug>/`:

- `diff.patch` — full unified diff (local refs only)
- `files.txt` — changed-file name list
- `metadata.txt` — range / base / head / remote provenance (every remote URL via
  `git remote get-url`, never a hardcoded host)

The printed path is the slug directory the recap MDX is written into.
Read `diff.patch` and `files.txt` to ground every block. **Print the resolved
range and remote provenance from `metadata.txt` before authoring** so it is obvious
which refs the recap covers. If both `diff.patch` and `files.txt` are empty, stop
and report that there are no tracked changes to recap; do not author an empty
artifact.

## Phase 1 — Scope the work unit

Default scope is the whole change in the collected range, not only the most recent
edit. Separate the changes that belong to this work unit from unrelated pre-existing
dirty work. If the scope is genuinely ambiguous, state the assumption or ask a concise
question before authoring.

Make a short surface/state inventory from the diff before writing any block: changed
routes, components, popovers/dialogs, role/access states, empty/error/loading states,
and shared abstractions. The final recap must either represent each meaningful item
with a block or intentionally omit it as tiny/redundant/not-user-visible.

## Phase 2 — Fetch the block catalog (the one permitted network call)

> GOTCHA: The MDX block vocabulary drifts upstream between releases. Do NOT author
> from memorized JSX tags — they silently produce wrong tags that error on import.

Before writing any structured MDX, invoke `mktemp` and retain the absolute path
printed on stdout. Substitute that resolved temp path in the catalog command;
do not rely on shell-variable persistence across tool calls:

```bash
env AGENT_NATIVE_PLANS_MODE=local-files npx -y @agent-native/core@0.59.1 plan blocks --out <resolved-temp-path>
```

Read that file first. The command calls the public no-auth block-catalog route and
sends no recap content. If the pinned package is unavailable from cache or the
registry, stop with the setup error; do not guess tags or register a fallback MCP.

Author every block against the tags and schemas that call returns. The catalog is
temporary runtime data, not part of the recap bundle; do not commit it.

## Phase 3 — Map the diff to blocks

Derive every structured block mechanically from the real diff (real paths, real fields,
real method/path, real before/after text). The names below are CONCEPTUAL block types;
resolve each to its exact tag + props via the fetched temporary catalog.

- **Schema / migration change** → `data-model` for the resulting entities, fields, and
  relations. Flag each field/entity with `change: "added" | "modified" | "removed" |
"renamed"`; for a changed type set `was` to the prior value. The diff-aware
  `data-model` is the headline; add a split `diff` of literal SQL only when the exact
  statement still matters.
- **API / action / route change** → `api-endpoint` with the post-change method, path,
  params, request, and responses. Flag each changed param/response with `change` (and
  `was` when a type/shape changed); set `change` on the endpoint root for a wholly added
  or removed route; mark removed routes `deprecated: true`. Author each request/response
  example as a single valid JSON value.
- **Files added / removed / renamed** → `file-tree` with each entry's `change` flag
  (`added`, `removed`, `modified`, `renamed`) and a short `note`.
- **Any meaningful code hunk** → `diff` with **split view as the default** (`mode:
"split"`), carrying the real `before`/`after` text plus `filename`/`language`. Give
  every `diff` a one-line `summary`; attach a few high-signal `annotations` to the key
  files. Reserve `mode: "unified"` for a genuinely narrow standalone hunk. Group the key
  files under a `## Key changes` heading in a single horizontal `tabs` block (one file
  per tab) so the selected split diff gets full document width.
- **Brand-new file with no meaningful "before"** → `annotated-code` rather than a
  one-sided split `diff`.
- **Rendered UI / interaction change** → `wireframe` blocks (see below) showing the
  visible delta before any code.
- **Architecture or data-flow shift** → `diagram` (`data.html`/`data.css` two-panel
  before/after, layered, or swimlane; or `mermaid` for a quick graph). Use `--wf-*`
  theme tokens and `.diagram-*` primitives — never hex, rgb/hsl, or `font-family`. Do
  not use `diagram` as a stand-in for rendered UI; UI changes need `wireframe`.
- **Outcome-first narrative** → `rich-text` for the "what changed and why": the
  objective, key decisions visible in the diff, and risks. This is the only place the
  model writes freely.

### Canonical shape

A strong recap follows one skeleton, top to bottom:

1. UI-impact headline — wireframes first, when the diff changed rendered UI.
2. Short outcome narrative (`rich-text`): what changed and why, 1–3 paragraphs.
3. `data-model` / `api-endpoint` blocks for schema and contract changes.
4. `file-tree` of the changed files with `change` flags.
5. `## Key changes` — one horizontal `tabs` block of `diff` / `annotated-code`
   (3–8 focused tabs; prefer under ~150 lines per tab).

Keep the body lean: no boilerplate intro/disclaimer/provenance prose. Add prose only
when it tells the reviewer something the structured blocks do not.

## UI impact requires wireframes (MANDATORY)

When the diff changes rendered UI, layout, density, visual state, interaction
affordances, navigation, controls, menus, dialogs, or design tokens, the recap **MUST**
include one or more `wireframe` blocks. Prose and file diffs are not a substitute for
showing what changed visually.

Before authoring ANY wireframe, **read
`${CLAUDE_PLUGIN_ROOT}/skills/visual-recap/references/wireframe.md` in full** — it is the
single source of truth for HTML wireframe quality (`.wf-*` classes, `[data-icon]` Tabler
set, `surface` presets, `--wf-*` tokens, before/after comparability, skeleton states).
Do not author wireframes from memory. Show the changed entry point, the main changed
interaction surface, and the resulting/destination state; for UI-heavy changes a single
before/after of the entry surface is not enough.

## Phase 4 — Write and serve the local recap

Write the recap as a local MDX folder inside the collected bundle directory:

- `docs/prps/reviews/visual/<slug>/plan.mdx` (required), optional `canvas.mdx`, and
  optional `.plan-state.json`. Set `kind: "recap"` and `localOnly: true` in the source
  frontmatter/state.

Validate, then serve via the localhost bridge:

```bash
env AGENT_NATIVE_PLANS_MODE=local-files npx -y @agent-native/core@0.59.1 plan local check --dir <resolved-bundle-path>
env AGENT_NATIVE_PLANS_MODE=local-files npx -y @agent-native/core@0.59.1 plan local serve --dir <resolved-bundle-path> --kind recap --open
```

Run `serve` with the host's long-running-process support, capture its first localhost
URL, and keep the bridge process alive without relaying incidental CLI logs as result
output. It binds **127.0.0.1** on an ephemeral CLI-chosen port, performs **no DB writes
and sends no recap content to any server**, and renders the on-disk MDX through the
localhost bridge. Report the URL from stdout (or `<slug>/.plan-url`, a local token file —
do not commit it). The URL is not shareable across machines.

Treat review feedback as file/chat feedback: edit the MDX directly, rerun
the pinned local check and serve commands above, and report the new local bridge URL.
Hosted comments, sharing, screenshots, and PR sticky-comment publishing are
intentionally unavailable.

## Grounding & security

- **Grounding rule.** `diff`, `data-model`, `api-endpoint`, and `file-tree` blocks must
  be built mechanically from the real changed lines — never inferred, rounded, or
  invented. Mark anything the model inferred (not extracted) as inferred in prose. When
  the diff does not contain a fact, leave it out.
- **Never transcribe secrets.** A diff can contain API keys, tokens, webhook URLs,
  signing secrets, or `.env` values. Never copy these into any block, snippet, caption,
  or note — redact them (`sk-•••`). This mirrors the repo's hardcoded-secret rule.
- **No egress.** This skill performs no hosted upload. The shared
  `${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/visual-egress-guard.sh` exists for the
  consent-gated hosted path used by `ycc:visual-plan`; it is NOT invoked here because
  this recap never leaves the machine.

## Output

- Local MDX recap under `docs/prps/reviews/visual/<slug>/` (`plan.mdx` + bundle).
- A `127.0.0.1` localhost-bridge preview URL printed to stdout.
- **No hosted link, no shareable URL, no PR comment, no GitHub/Forgejo Action.**

## Related

- `ycc:visual-plan` — forward planning; faithful hosted+local MDX workflow with
  consent-gated egress. Shares the wireframe quality bar word-for-word.
- `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/agent-native-setup.md` — runtime
  contract (install pin, connector, bridge, egress policy).
