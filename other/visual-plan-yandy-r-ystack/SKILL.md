---
name: visual-plan
description: 'Renders existing plans as interactive visual documents. Use when visualizing a text plan, creating a plan wireframe, or reviewing planned architecture visually.'
argument-hint: '[--share] <path/to/plan.md>'
allowed-tools:
  - Read
  - Write
  - Bash(ls:*)
  - Bash(cat:*)
  - Bash(test:*)
  - Bash(mkdir:*)
  - Bash(dirname:*)
  - Bash(env:*)
  - Bash(mktemp:*)
  - Bash(npx:*)
  - 'Bash(${CLAUDE_PLUGIN_ROOT}/skills/visual-plan/scripts/*.sh:*)'
  - 'Bash(${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/*.sh:*)'
---

# Visual Plan (Agent-Native Plans)

Turn an ordinary text plan into a structured, reviewable visual plan. Build the plan a reader would normally
skim in Markdown, but as a scannable document with editable blocks mixed in: inline diagrams, annotated code,
open questions, and an optional top visual review surface (wireframe canvas, live prototype, or both in tabs).
Architecture and backend plans stay document-only; UI and product plans start with the top canvas/prototype.

**Operational context:** Consume an existing plan without editing it, researching again, or dispatching planners. The shared --visual decorator hands off here; write only the derived visual/ output. Local-files mode is default; hosted sharing requires explicit --share consent.

`ycc:visual-plan` is the packaged entry point (slash command `/visual-plan`). It
**consumes an existing plan** handed to it — it does not research, dispatch, or
re-plan. Local-files mode uses the pinned Agent-Native Plans CLI and never
registers an MCP server; hosted sharing uses the Plan MCP connector only after
explicit consent. The install pin, auth/reconnect flow, connector names,
localhost bridge, block-catalog lookup, and egress policy are defined ONCE in
`${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/agent-native-setup.md`. Read
that file for any setup/auth/serve/egress detail rather than memorizing it here.

## Contract (read first)

This skill is the hand-off target of the shared `--visual` decorator. The full
contract lives in `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/visual-mode.md`.
The non-negotiable invariants:

- **Accept ANY plan path.** Never assume `docs/prps/plans` or any fixed
  location. The plan path is supplied by the caller and may live anywhere.
- **Derive `visual/` relative to the given plan path.** Output goes into a
  `visual/` sibling of the plan file — `<dirname of plan>/visual/` — computed
  from the path handed in, never hardcoded.
- **NEVER edit the plan file.** Read it; write only into the derived `visual/`
  directory. The plan artifact stays byte-for-byte intact.
- **NEVER re-run research or dispatch.** Only consume the existing plan.
- **Print exactly one resulting link to stdout** — a hosted shareable URL, a
  localhost preview `http://127.0.0.1:PORT/...`, or `local files only`.

## Arguments

Parse `$ARGUMENTS`:

- **`<path/to/plan.md>`** (required positional) — absolute or repo-relative path
  to the source plan. Read it; derive `visual/` from its directory.
- **`--share`** (optional, **consent flag**) — the explicit, named opt-in to
  hosted egress (destination `plan.agent-native.com`). Without it, the skill
  runs in **local-files** mode and no plan content is uploaded to hosted storage.
  See **Egress & consent** below.

## Mode selection (auto)

Choose the review surface from the source plan's content — do not add visual
chrome by default:

- **UI-first** — work is primarily product UI; review should start with screens.
  Top canvas is the primary surface (`create-ui-plan`).
- **prototype-first** — review should start with a functional live prototype;
  interaction is the main question (`create-prototype-plan`).
- **design-first** — review needs full-fidelity branded screens
  (`create-plan-design`).
- **visual-intake** — only when the user explicitly asks for a questionnaire
  before planning (`create-visual-questions`). Never run it as `/visual-plan`
  preflight.
- **document-only** — architecture, backend, data, refactor, or API plans get NO
  top canvas; inline `diagram` blocks sit next to the relevant prose
  (`create-visual-plan`).

The create-tool names above apply only to the consent-gated `--share` branch.
Default local-files mode uses the same surface choice to author portable MDX
directly and MUST NOT call an MCP tool.

When the source plan is already a Codex / Claude Code / Markdown / pasted plan,
use it as `planText` and build the review surface from it instead of starting
over. Preserve its useful intent and codebase facts; publish a clean standalone
proposal (no "this revision changes…" framing).

## Block vocabulary — resolve at USE TIME

> The MDX block vocabulary drifts upstream between releases. Do NOT author from a
> memorized tag list — not from this skill, not from the references.

At author time (use time), fetch the live block catalog FIRST:

- Hosted / connected: call the **`get-plan-blocks`** MCP tool.
- `local-files`: run
  `env AGENT_NATIVE_PLANS_MODE=local-files npx -y @agent-native/core@0.59.1 plan blocks --out <path>`
  (per `agent-native-setup.md`) and read that file. Do not call the MCP tool in
  this branch. If the pinned package is unavailable from cache or the registry,
  stop with the setup error; do not guess tags or switch to hosted tools.

Render plan MDX against the freshly-fetched list. The references in this skill
describe block _families_ and quality bars; the catalog is the authority on
exact tag names, required fields, and prop shapes.

## Core workflow

1. **Read the source plan.** Read the file at the given path (read-only). Derive
   the output dir with the thin helper (it computes the `visual/` sibling per the
   contract and never hardcodes a location). Invoke it directly, then capture its
   stdout as `OUT`:

   ```
   ${CLAUDE_PLUGIN_ROOT}/skills/visual-plan/scripts/derive-visual-dir.sh <plan> --mkdir
   ```

   Gather the plan's exact text — do not invent source content.

2. **Resolve blocks by mode.** With `--share`, call `get-plan-blocks`. In the
   default local-files branch, invoke `mktemp`, capture its stdout as `BLOCKS`,
   then run
   `env AGENT_NATIVE_PLANS_MODE=local-files npx -y @agent-native/core@0.59.1 plan blocks --out <BLOCKS>`
   and read that temporary catalog. Never call an MCP tool in the local branch
   or write the catalog into the portable plan directory.
3. **Author portable files locally.** Use the chosen surface to write `plan.mdx`
   into the derived `visual/` dir, plus `canvas.mdx` for a canvas and
   `prototype.mdx` for a prototype. For UI/product plans, compose the top canvas
   first with the primary wireframes and annotated states. For non-visual plans,
   skip the top surface and place native document blocks next to the relevant
   prose.
4. **Validate locally.** Run
   `env AGENT_NATIVE_PLANS_MODE=local-files npx -y @agent-native/core@0.59.1 plan local check --dir <OUT>`.
   In default local-files mode, this direct MDX authoring path is the complete
   creation flow; do not call a create, feedback, import, export, or update MCP
   tool.
5. **Publish only with explicit consent.** When `--share` is present, run the
   egress guard against `<OUT>` first. Only after it passes, call the
   mode-matched hosted create tool from Mode selection, passing the source plan
   and authored content in the shape that tool requires. Use its returned URL.
6. **Surface the link.** Without `--share`, run
   `env AGENT_NATIVE_PLANS_MODE=local-files npx -y @agent-native/core@0.59.1 plan local serve --dir <OUT> --open`
   using the host's long-running-process support. Capture the first localhost
   URL and keep the bridge process alive; do not relay incidental CLI logs as
   result output. Print that one URL, or `local files only` if serving is
   unavailable. With `--share`, print the hosted URL returned by the create
   tool.
7. **Review and revise by mode.** In local-files mode, treat file/chat feedback
   as authoritative, edit the MDX directly, and rerun the pinned local check and
   serve commands from steps 4 and 6. With `--share`, read hosted comments using
   `get-plan-feedback` and apply targeted `update-visual-plan` content patches;
   when a full replacement is unavoidable, read and preserve the complete source
   and every surface first.

## Quality references — read before authoring

These are provider-neutral quality bars. Read the relevant one IN FULL before
authoring; do not paraphrase from memory:

- `${CLAUDE_PLUGIN_ROOT}/skills/visual-plan/references/document-quality.md` — read
  before authoring any plan document: the
  plan-document quality bar and block families.
- `${CLAUDE_PLUGIN_ROOT}/skills/visual-plan/references/canvas.md` — read before
  building a canvas surface: canvas /
  artboard / annotation mechanics and patch ops.
- `${CLAUDE_PLUGIN_ROOT}/skills/visual-plan/references/wireframe.md` — read before
  authoring wireframe blocks: the HTML
  wireframe quality bar (`.wf-*` tokens, surfaces, icons, skeletons).
- `${CLAUDE_PLUGIN_ROOT}/skills/visual-plan/references/exemplar.md` — read when
  checking composition or anti-patterns: a worked
  example plus the anti-patterns to avoid.

## Planning is read-only

Make NO source edits while building or reviewing the visual plan, and never edit
the input plan file. Begin editing code only after the user approves the
direction. The plan is the approval gate: surface it, name which files/areas the
work touches, and request sign-off.

## Egress & consent (default OFF)

Hosted upload is **OFF by default** and **consent-gated**. The full policy lives
in `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/agent-native-setup.md`;
the operational rules for this skill:

- **Default = `local-files`.** Set `AGENT_NATIVE_PLANS_MODE=local-files`. In this
  mode the runtime reads/writes plan files locally and never uploads them to the
  hosted Plan database. The schema-only catalog request and browser UI shell may
  contact the configured Plan app. Preview via the localhost bridge
  (`env AGENT_NATIVE_PLANS_MODE=local-files npx -y @agent-native/core@0.59.1 plan local serve --dir <OUT> --open`),
  which binds 127.0.0.1 on an ephemeral port and performs no hosted DB writes;
  the UI reads MDX from localhost rather than hosted storage.
- **`--share` is the only opt-in.** It names the destination host
  `plan.agent-native.com`. Only when the operator passes `--share` may any plan
  content leave the machine.
- **Route all hosted egress through the guard.** Before any MDX/diff payload is
  uploaded, run:

  ```
  ${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/visual-egress-guard.sh \
    --payload <OUT> --destination plan.agent-native.com \
    --consent plan.agent-native.com
  ```

  The guard scans the payload for secrets, refuses non-public/private remotes,
  and requires a consent token matching the destination. If it exits non-zero,
  STOP — do not upload; report the gate that failed.

## Setup, auth, and the localhost bridge

For the pinned install version, the one-time per-client reconnect, the hosted
`plan` MCP connector (legacy alias `agent-native-plans`), local-files mode, and
the localhost bridge, read
`${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/agent-native-setup.md`. If a
hosted Plans tool returns `needs auth` / `Unauthorized` / `Session terminated`
in the `--share` branch, stop and give the user the reconnect step from that
reference — never reinstall from scratch to fix auth, and never use hosted tools
as a fallback for local-files mode.

## Output

Exactly one of the following is printed to stdout, per the `visual-mode.md`
contract:

- a hosted shareable URL under `https://plan.agent-native.com` (only with
  `--share`, after the egress guard passes), or
- a localhost preview `http://127.0.0.1:PORT/...` (default local-files mode), or
- `local files only` when no server/host is available.

The calling planning skill surfaces whatever link this skill prints.
