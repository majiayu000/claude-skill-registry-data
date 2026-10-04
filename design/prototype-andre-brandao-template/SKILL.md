---
name: prototype
description: Scaffold a feature prototype under docs/prototype/<feature> — a PROTOTYPE.md (UX, features, high-level data model) with self-contained .html mockups, plus an optional PLAN.md technical companion written in a later step. Use when the user wants to prototype, spec, or mock up a feature before implementing it.
---

# Prototype

Scaffold a design-first prototype for a feature. Everything lands under `docs/prototype/<feature>/` — no app code is touched. The format below is the complete spec; do not look for an existing prototype to copy (there may be none).

Two documents, two altitudes:

- **`PROTOTYPE.md`** — the prototype itself: HTML mockups, user experience, features, and the data model's field surface in plain language. This is what `/prototype <feature>` produces.
- **`PLAN.md`** — the technical companion: real schema code, SQL, permissions, API surface. Not part of prototyping; write it only after the user has reviewed the prototype and validated it, and asks for the plan (`/prototype plan <feature>` or "write the plan for X"). Never chain prototype → plan in one go.

Arguments are the feature name and optionally a description. If the first argument is `plan`, run the **Plan workflow** for an existing prototype. If no arguments were given, ask for the feature name before doing anything.

Once the prototype is validated, the `prototype-app` skill can build the feature's frontend vertical inside the real app against an in-memory mock — a separate, also user-initiated step.

Both documents are served by the viewer: `bun prototype` (from repo root) renders every `docs/prototype/*/PROTOTYPE.md` at `http://localhost:4400/<feature>/`, with iframes embedded, `mermaid` fences drawn, and frontmatter feeding the index page.

The dashboard serves the same docs at `/dev/prototype/<feature>` while `bun dev` runs — every `.md` in the folder as a tab, mockups live in their iframes, diagrams through the app's own renderer.

## Prototype workflow

1. **Name the directory.** Kebab-case the feature name: `docs/prototype/<feature>/`. If the directory already exists, update its contents in place instead of duplicating.

2. **Study the app, not the backend.** Find the app's global stylesheet (in this template: `apps/dashboard/src/app.css`) for design tokens — colors, radius, fonts — and glance at one existing feature's screens so the mockups feel like the real product. Skip schema/API research — that belongs to the plan step.

3. **Write `PROTOTYPE.md`** following this skeleton exactly (sections in this order — the doc opens with the visuals):

   ````markdown
   ---
   title: Notification Center
   description: One-line summary shown on the prototype index.
   status: draft
   date: 2026-08-11
   ---

   # Notification Center

   ## Prototypes

   ### list-view.html

   One paragraph: which screen/flow this mockup shows and what to try clicking.

   <iframe
     src="./list-view.html"
     width="100%"
     height="600"
     style="border:1px solid #ccc;border-radius:8px"
   ></iframe>

   [Open list-view.html](./list-view.html)

   ## Overview

   What the feature is and why — a few sentences of product framing. No file paths.

   ## Features

   **Group per user flow**

   - Bulleted capabilities, concrete enough to build the mockup from.

   > [!NOTE]
   > Open questions go inline like this, rather than deciding silently.

   ## Data model

   One line for the shared system columns (id, created/updated/deleted
   timestamps, created_by — whatever every table in the repo carries).

   ```mermaid
   erDiagram
     NOTIFICATION }o--|| USER : "for"

     NOTIFICATION {
       ref user FK "required - the recipient"
       text title "required"
       text body
       enum kind "mention | assignment | system"
       date read_at "null until read"
     }
   ```

   - Bullets only for what the diagram can't show: lifecycle rules,
     read-only fields, derived values.

   ## Out of scope

   - What this prototype deliberately does not cover.
   ````

   Rules on top of the skeleton:
   - Frontmatter is plain `key: value` lines, no nesting. `title` and `description` are required; `status` (draft/review/approved) and `date` (creation date, absolute) are optional index badges.
   - **Prototypes**: one subsection per HTML file, iframe embed plus plain-link fallback (not every markdown renderer allows iframes).
   - **Features**: where a flow has real branching (state machines, multi-step wizards), draw it — a `mermaid` flowchart/stateDiagram fence or a small ASCII sketch in a plain code fence.
   - **Data model**: the complete field surface, no implementation detail. Every entity and every field appears in the `erDiagram` as `type name [PK|FK|UK] "comment"` attributes — plain types only (`text`, `enum`, `money`, `date`, `list`, `ref`), with required/optional, enum values, and reference targets in the comment string. No ORM code, no SQL, no indexes. Once a plan exists, end the section with `Full schema, permissions, and the API surface live in [PLAN.md](./PLAN.md).`

4. **Build the HTML prototypes.** One `.html` file per distinct screen or flow (list view, detail view, creation flow, etc.), sitting next to `PROTOTYPE.md`. Rules:
   - Fully self-contained: inline `<style>` and `<script>`, zero external requests — no CDNs, no fonts, no images from the network. They must render from `file://`.
   - Interactive where it matters: mock data as inline JS arrays, working filters/tabs/forms via vanilla JS, so the flow can be clicked through. No frameworks.
   - Match the app's look: reuse its design tokens as CSS variables so the mock feels like the real product. Support light and dark via `prefers-color-scheme` (the viewer's theme toggle propagates into the iframes).
   - Realistic content, not lorem ipsum — mock data should read like real usage of the feature.

5. **Finish.** List the created files, summarize any open questions raised in the spec, and point at the viewer (`bun prototype` → `http://localhost:4400/<feature>/`) so the user can review. The prototype now waits for their feedback: iterate on it as they react, and only move to PLAN.md once they've validated the prototype and asked for the plan. Do not create app code, migrations, or tests.

## Diagrams

Diagram fences are rendered by [`beautiful-mermaid`](https://npmjs.com/package/beautiful-mermaid), which
implements a subset of Mermaid. Stick to these six.

| Fence header          | Use it for                                                      |
| --------------------- | --------------------------------------------------------------- |
| `flowchart` / `graph` | Branching flows, wizards, decision points (`TD`/`LR`/`BT`/`RL`) |
| `stateDiagram-v2`     | Lifecycles and state machines                                   |
| `sequenceDiagram`     | Message/call order between actors or services                   |
| `classDiagram`        | Type shapes and their relationships                             |
| `erDiagram`           | The **Data model** section — entities and fields                |
| `xychart-beta`        | Bar/line charts for volumes, growth, sizing                     |

`linkStyle` works in flowcharts and state diagrams for per-edge colour and stroke width.

**Not available** — do not reach for these, they will not draw: `gantt`, `journey`, `pie`,
`mindmap`, `timeline`, `quadrantChart`, `gitGraph`, `sankey-beta`, `block-beta`, `kanban`,
`requirementDiagram`, `C4Context`, `architecture-beta`, `packet-beta`, `radar-beta`, `treemap-beta`.
For a roadmap or timeline, use a table; for a journey, a `flowchart` with one node per step.

The `bun prototype` viewer still loads full Mermaid from a CDN, so an unsupported fence may draw
there while rendering as plain source everywhere else. Do not rely on it — author for the six.

Colours come from the surrounding page's CSS variables, so diagrams follow the light/dark toggle —
never hardcode colours in a fence.

## Plan workflow (later step, on request)

1. **Only on an explicit ask, for a validated prototype.** The plan implements what the prototype shows, so the prototype must exist and the user must have reviewed it — if it doesn't exist, say so and offer to prototype first; if it exists but the user hasn't looked at it yet, confirm they're happy with the prototype before planning. Read `docs/prototype/<feature>/PROTOTYPE.md` in full; unresolved `> [!NOTE]` questions in it are prompts to ask the user now, not decisions to make silently.

2. **Study the codebase** so the plan matches how this repo actually builds features — read one existing slice end to end rather than inventing conventions. In this template:
   - Data models: Drizzle tables in `packages/core/src/<slice>/<slice>.sql.ts`, shared column helpers from `packages/core/src/drizzle/types`, snake_case column names per CLAUDE.md.
   - Permissions: `packages/core/src/permission.ts` and how `Actor.check` is called from core bodies.
   - API: SvelteKit remote functions in `apps/dashboard/src/lib/features/<slice>/api/*.remote.ts`. Endpoints are remote query/command signatures, not REST routes, unless the feature genuinely needs an HTTP route (webhooks, public API).
   - Slices: core logic in `packages/core/src/<slice>/` (`<slice>.sql.ts` + `index.ts`); UI in `apps/dashboard/src/lib/features/<slice>/`. Name where each piece lands.

3. **Write `PLAN.md`** next to the prototype, with frontmatter (`title`, `date`) and:
   - An opening line linking back to `PROTOTYPE.md`, plus the slice layout (which files, which packages).
   - **Data model** — schema definitions in a `ts` block (the repo's ORM style), the equivalent `CREATE TABLE` SQL in a `sql` block, relations, indexes, and a **Permissions** subsection.
   - **API** — one subsection per endpoint: signature (name, input schema, return shape), which slice owns it, and auth/actor expectations.
   - Open questions as `> [!NOTE]` blocks.

4. **Finish.** Link the plan into PROTOTYPE.md's Data model section if not already, and note the viewer renders it at `http://localhost:4400/<feature>/PLAN.md`.
