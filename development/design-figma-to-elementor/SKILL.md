---
type: Skill
name: design-figma-to-elementor
description: Agentic design-to-build pipeline that turns a Figma design into a built WordPress site using the Figma MCP server (read side) and the Elementor MCP server (write side) attached as MCP Apps on an NV oOS assistant. Covers the 7-stage pipeline (Scope → Read → Plan → Tokenize → Build → Verify → Handoff), the normative stage rules (get_design_context first, tokenize before build, drafts only, never publish, Figma read-only), the build-manifest contract (schema + example in reference/build-manifest.md), the design-file contract (frame/section/variable naming in reference/design-file-contract.md), assistant wiring (figma + elementor MCP Apps, OAuth + application passwords, host allowlist), safety rules, and troubleshooting. Use when asked to build or create a site, page, or landing page from a Figma design, to wire Figma MCP or Elementor MCP for design-to-build work, to approve or produce a build manifest, or to debug a failed design-to-build run.
license: Proprietary. See LICENSE.txt
metadata:
  type: Skill
  plugin: mcp-ai-wpoos
  plugin-version: "1.1.94"
  plugin-version-tested: "1.1.94"
  last-updated: "2026-10-06"
---

# Figma → Elementor Design-to-Build Pipeline

Turns a Figma design into a real WordPress site: the **Figma MCP server**
reads the design (structure, tokens, screenshots); the **Elementor MCP
server** writes the site (pages, sections, globals, responsive settings) —
every generation landing as a **draft**. Both are attached to one NV oOS
assistant as MCP Apps, and this skill is the pipeline contract between them.

This is the agentic build track. Token import is a separate feature
(`nds_import_design_tokens` / the NDS design-system addon); this skill only
consumes its output when present.

## When to use this skill

- The user asks to "build this Figma design", "create this landing page",
  "make the site look like this Figma file", or similar.
- Connecting `figma` and `elementor` MCP Apps to an assistant for
  design-to-build work.
- Reviewing or approving a **build manifest** the agent produced.
- Debugging a run that produced wrong pages, hardcoded colors, or failed
  tool calls (`mcp_app_figma_*` / `mcp_app_elementor_*`).

## Mental model

```
Figma file (source of truth)              Target WordPress site
──────────────────────────                ────────────────────────────
Figma MCP server (mcp.figma.com/mcp)      Elementor MCP server (remote)
  get_design_context   ──read──►            pages / sections / widgets
  get_variable_defs    ──read──►            global classes + variables
  get_screenshot       ──read──►            responsive (tablet/mobile)
                              ▲
              NV oOS assistant │ (this skill = the pipeline contract)
              MCP Apps: figma (oauth) + elementor (basic app password)
              Plan approval + publish are HUMAN gates.
```

The design file is read-only input; the site is draft-only output. The agent
sits in the middle and never takes the final step.

## Two topologies

The pipeline runs in either of two shapes; the **build manifest** is the
handoff artifact in both.

**Topology A — single assistant (default).** Both MCP Apps (`figma` +
`elementor`) are attached to the NV oOS assistant, which runs all 7 stages.

**Topology B — split (common in practice).** The Figma MCP is attached to
another client (e.g. Claude Code); the NV oOS assistant holds only the
`elementor` MCP App.

```
Claude Code (or other client)                NV oOS assistant
  Figma MCP ──► Scope → Read → Plan          Tokenize → Build → Verify → Handoff
                     │  build manifest        ▲
                     └─────── handoff ────────┘  Elementor MCP App (write side)
                      via A2A artifacts / per-toolkit MCP endpoints / paste
```

Handoff channels (all shipped in the plugin):

1. **A2A** (`includes/a2a/`) — the design-side agent sends a task to the
   assistant (Agent Card at `.well-known/agent.json`) with the manifest +
   reference screenshots as artifacts.
2. **NV oOS as an MCP server** (`addons/pro/includes/mcp-servers/`) — the
   client connects to `/wp-json/mcp-ai-pro/v1/mcp/{slug}` and calls the
   assistant's tools (including bridged `mcp_app_elementor_*`) with the
   manifest as an argument.
3. **Paste** — the design-side agent emits the manifest JSON; the human
   pastes it into the NV oOS chat.

Stage ownership in Topology B: stages 1–3 (Scope/Read/Plan) run on the
agent holding the Figma MCP; stages 4–7 (Tokenize/Build/Verify/Handoff) run
on the NV oOS assistant. The manifest's `tokens[]` carries **resolved
values**, and `assets[]` + reference screenshots travel with the artifact —
the build side never needs live Figma access. Verify compares the draft
against the carried references.

## Hard rules (normative — never break these)

1. **`get_design_context` is always the first Figma call** for each node
   (Figma's own integration rule). Other Figma tools are inputs to it or
   fallbacks, never replacements. In Topology B this applies to the
   design-side agent (the one holding the Figma MCP).
2. **Tokenize before Build.** Colors, type, and spacing resolve to site-wide
   tokens (Elementor global classes/variables) before any widget is placed.
   A widget with a raw hex value is a defect.
3. **Drafts only.** The agent creates/edits drafts. It never publishes,
   changes status, or calls any publish/activate tool. Publishing is human.
4. **Plan approval gate.** No Elementor write happens before the human
   approves the build manifest. Reads are always allowed.
5. **Figma is read-only here.** Never call Figma write tools in this
   pipeline. The design file is the source of truth; the agent does not edit
   it. (Opt-in write-back is a separate, unshipped mode.)
6. **Scope per node.** Work one Figma page/frame at a time. Never request
   the whole file — Figma read quotas and context limits make whole-file
   reads unreliable.
7. **Verify before handoff.** Every build ends with a verification report
   (screenshot compare + read-back). Silent "done" is not done. In
   Topology B the comparison references are the screenshots carried in the
   handoff artifact, not live Figma calls.

## The 7 stages

| # | Stage | Tools | Output | Gate |
|---|---|---|---|---|
| 1 | Scope | config | Work item: Figma node/page + target WP page + audience | — |
| 2 | Read | `mcp_app_figma_get_design_context` (first), `mcp_app_figma_get_variable_defs`, `mcp_app_figma_get_screenshot` | Structured design context, token list, reference screenshots | — |
| 3 | Plan | reasoning over Read | **Build manifest** (see `reference/build-manifest.md` + `.schema.json`) | **Human approves** |
| 4 | Tokenize | `mcp_app_elementor_*` global classes/variables tools; NDS import dry-run when available | Site-wide tokens applied; token diff shown | Token diff reviewed |
| 5 | Build | `mcp_app_elementor_*` create page/section/widget/responsive tools | Page built as draft, sections per manifest | Progress observable; interruptible |
| 6 | Verify | `mcp_app_figma_get_screenshot` vs Elementor read-back/screenshot | Verification report (per-section match, missing assets, spacing) | Human reviews |
| 7 | Handoff | none | Human publishes via WP admin / Elementor; agent logs receipt (usage/cost) | **Human publishes** |

**Topology B stage split:** stages 1–3 run on the design-side agent (Figma
MCP holder); stages 4–7 on the NV oOS assistant (Elementor MCP App). The
approved manifest + reference screenshots cross the boundary via A2A
artifacts, the per-toolkit MCP endpoints, or paste. Everything else in the
table is topology-independent.

### Stage details

**Scope.** Confirm: which Figma file/page (node id or name), which target
site (Remote Sites connection), and whether this is a new page or an edit to
an existing draft. Check the design file against the design-file contract
(`reference/design-file-contract.md`) and report violations — do not
silently guess. A non-conforming file gets a concrete remediation report,
not a build.

**Read.** Per node: `get_design_context` first (it returns hierarchy, layout
constraints, text, component and variable references). Then
`get_variable_defs` for tokens and `get_screenshot` for the reference frame.
If `get_design_context` fails (unsupported node, missing selection), state
the fallback used and why.

**Plan.** Emit a build manifest conforming to
`reference/build-manifest.schema.json`: page map (frame → WP page), sections
in order, widget mapping per section, content copy, token mapping, assets,
responsive notes. Present it for approval. No writes before approval.

**Tokenize.** Map design variables to Elementor global classes/variables
(colors, fonts, spacing). When the NDS design-system addon is active,
prefer the registry path (import dry-run → `--nds-*` → Elementor globals).
Show the token diff before applying. Widget-level raw hex is forbidden
(rule 2).

**Build.** Create the page as a draft, add sections in manifest order, place
widgets per mapping, then apply tablet/mobile responsive settings. Report
progress per section; support interrupt/retry per section. Never publish.

**Verify.** Compare the rendered draft against the Figma reference
screenshot and read back the built structure. Report per-section: match,
missing assets, spacing/typography deviations, token violations. Fix loops
happen here, not silently.

**Handoff.** Stop. Give the human the draft link and a summary (what was
built, tokens applied, cost/usage). The human publishes.

## Build manifest

The manifest is the plan artifact: what the agent will build, in what order,
with which tokens and assets. Schema: `reference/build-manifest.schema.json`.
Spec and example: `reference/build-manifest.md`.

## Design-file contract

Conventions that make Figma files pipeline-ready (frame naming, section
structure, variables, auto-layout, text styles): `reference/design-file-contract.md`.
Files that violate the contract get a remediation report at Scope.

## Wiring the assistant

Prerequisite skill: `design-elementor-mcp-connection` — read it first; it is
the authoritative recipe for Elementor MCP (application passwords, Remote
Sites `mcp_server` connections, allowlist, auth mapping, discovery).

**Topology A** attaches both apps to the assistant. **Topology B** attaches
only the `elementor` app to the assistant — the Figma MCP is configured in
the other client (Claude Code), and the manifest arrives via A2A, the
per-toolkit MCP endpoints, or paste. Both topologies share steps 1, 3 and 4
below; step 2 is Topology A only.

1. **Elementor MCP App** (label `elementor`): Remote Sites → Add Connection →
   `MCP Server (Elementor MCP / WordPress MCP Adapter)` → URL from the
   Elementor-generated prompt → Basic auth (`wp-username:application-password`,
   spaces removed). Dedicated least-privilege WP user on the target site —
   the agent inherits that role and nothing more.
2. **Figma MCP App** (label `figma`): server `https://mcp.figma.com/mcp`,
   `auth_type: oauth` (the MCP Apps OAuth flow — metadata discovery, DCR,
   PKCE, refresh — handles Figma's OAuth). Community-server fallback
   (Framelink / `figma-context-mcp`): `auth_type: header` with a Figma API
   token.
3. **Security Center → Network & Headers → MCP App Allowed Hosts**: add
   `mcp.figma.com` and the Elementor site host. Never bypass the guard.
4. **Assistant editor → MCP Apps metabox** → Add from Remote Sites → attach
   both to the assistant. Run Test Connection + Discover Tools for each;
   bridged tools appear as `mcp_app_figma_*` / `mcp_app_elementor_*` in chat.

Tool names vary by server (official vs third-party Elementor MCP). Discover
at runtime and map by capability, not by exact name: design context /
variable defs / screenshot on the Figma side; page / section / widget /
global classes+variables / responsive on the Elementor side.

## Safety & cost

- Draft-only writes; publish is human-only (rule 3); plan approval before
  any write (rule 4). All state changes are activity-logged.
- Least-privilege users on the target site; bridged tools still pass the
  plugin's per-tool capability gating.
- Figma read quotas are per seat/plan; keep reads node-scoped (rule 6) and
  prefer `get_screenshot` only when structure is ambiguous.
- Usage/cost badges and the tasks drawer are the run's receipts — surface
  them, don't hide them.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `mcp_app_figma_*` tools missing from chat | App `enabled` is true; re-run Discover Tools; check the negative cache (60 s); confirm the allowlist contains `mcp.figma.com` |
| Figma Test Connection fails | OAuth flow not completed — use the MCP Apps OAuth tab; paste-back expires after 10 min |
| `get_design_context` returns nothing useful | Node id wrong or frame not selected — re-scope to the exact node; fall back to `get_screenshot` + `get_variable_defs` and say so |
| Elementor calls denied | The remote WP user lacks the capability — fix the role on the Elementor site, not the NV oOS config |
| Built page has raw hex colors | Rule 2 violated — re-run Tokenize, then replace widget-level colors with globals |
| Agent tried to publish | Reject and re-instruct with rule 3; confirm publish tools are not bridged/used |
| Figma response truncated | Node too large — split into sub-frames and re-read per section |
| Topology B: Verify has no Figma access | Expected — compare against the reference screenshots carried in the handoff artifact; if missing, ask the design-side agent to attach them |
| Topology B: manifest arrived without approval info | Treat `approval.status` as `pending` — re-run the plan approval gate before any write |

## Cross-references

- `design-elementor-mcp-connection` — Elementor MCP wiring authority
- `design-elementor-template-kits` — offline kit import (different track)
- `design-vault` — store the application passwords / Figma credentials
- `mcp-ai-wpoos-plugin` — JSON-RPC over HTTP mechanics behind MCP Apps
- Proposal 059 + implementation plan: `docs/project/proposals/059-*`
