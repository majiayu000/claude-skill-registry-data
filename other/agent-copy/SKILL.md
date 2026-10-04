---
name: agent-copy
description: "Compact two-icon Copy / Copy-for-AI controls (components/agent-copy). Use when adding copy buttons to a row, card, list, or record; merging duplicate Copy/JSON/AI controls; continuing the copy rollout; or writing a Copy-for-AI payload. NOT for markdown content actions (use rich-document-actions)."
---

# agent-copy — copy data (human + AI) anywhere

> **Current UI (2026-09-27):** `<CopyButtons>` renders the package-owned Alchemy
> copy menu (`MatrxCopyMenu` from `@ai-matrx/design-system/content-transfer`, one
> icon since 2026-09-12). Where this skill says "two-icon pair", read "the
> canonical CopyButtons menu" — never hand-build two icons beside it. The
> payload rules below are unchanged.

A reusable primitive for putting **Copy**, **Copy JSON**, **Copy for AI**, and
export actions behind a compact two-icon pair on any row, card, list, or record. It is the
orchestration glue between raw page data and an AI agent: today it copies to the
clipboard so a human pastes into an agent; the end state (see Roadmap) is the
agent reading that context directly and acting on the page.

Source + full docs: [`components/agent-copy/README.md`](../../../components/agent-copy/README.md).
**Sibling skill (doctrine twin):** aidream
`../aidream/.claude/skills/copy-for-ai/SKILL.md` — its
cx-explorer implementation is the platform's best-of-breed reference; keep the
two skills and the two `AiCopyMenu`s in step.

**Not this primitive:** the live-chat message bar (`AssistantActionBar` /
`messageActionRegistry`) or markdown content actions (the `rich-document-actions` skill).

**Branches (read only when the run needs them):**

- Assigned a whole feature/module, not one page → read [module-audit.md](module-audit.md) before wiring.
- Before wiring or editing any existing surface, continuing the rollout, checking whether a surface is already wired, or paying down known raw-dump debt → read [rollout-status.md](rollout-status.md), and update it as you go.
- Wiring any surface in files, image-manager, podcasts, audio, or pdf → read [docs/handoffs/agent-copy-media-cluster.md](../../../docs/handoffs/agent-copy-media-cluster.md) first (no signed URL or storage path ever reaches a payload); research, rag, cms, or api-integrations → read [docs/handoffs/agent-copy-data-knowledge-cluster.md](../../../docs/handoffs/agent-copy-data-knowledge-cluster.md) first.

---

## 🚨 THE MISSION — a Copy-for-AI is an AI context source, not a copy button

The user clicks it because they are **getting AI help with what they are doing
right now**. Before writing any payload, answer: _"what is the user doing on
this page the moment they click this?"_ — then hand the agent exactly that.

- **THE WHAT-I-SEE LAW (Arman, 2026-08-12, in anger):** the PRIMARY payload is
  the **rendered surface converted to data** — never a raw record/snapshot
  dump. A payload that dumps 50k chars of adjacent data while missing the red
  error the user is staring at is a defect, not a copy button.
- **Errors first.** Blockers, warnings, red validation text — the exact
  sentences rendered — are the highest-value content. Capture them verbatim.
- **Mirror the page's leading KPIs.** If the page opens with a metric strip
  ("5 blockers · 3 own access · 1 nested"), every payload from that page —
  including section/panel payloads — carries those same numbers, verbatim, in
  the body AND the envelope `attributes`. Nothing on the page is interpretable
  without what the page leads with, and the agent must never recompute what
  the user already sees.
- **LIVE state, never saved rows.** Build the payload inside the click handler
  from current inputs/drafts. A form-heavy page's form values ARE the payload;
  copying the fetched row after the user edited a field is lying to the agent.
  Include an explicit `unsaved_changes` diff vs the saved record. (Broke twice
  on 2026-08-12 alone: access planner, agent-settings.)
- **Mirror the content extractor.** Reuse the view's own formatter/extractor so
  the export is what the user actually sees, not a parallel re-derivation.
- **A section payload states what it belongs to.** Specifics are only valid
  with their parent context (record identity + the page's KPIs) in the
  envelope.
- **The acceptance test:** put your payload beside a screenshot. Could an agent
  reconstruct what the user sees — every error, every KPI, the current form
  values? If not, it fails. Run this before reporting done.

## 30-second mechanics

- **`buildAgentPayload(input)`** — pure util. Wraps any data in an xml-ish block
  with `<context>` (auto-injected live `url`, `route`, `copied-at` + your
  `location`/`description`/`context`) and a `<data format="json">` body.
  `attributes` carry counts (`rows`, `blockers`, `total_messages`) — the
  payload self-describes so a future agent can decide what to fetch.
- **`<CopyButtons>`** — the UI. Renders one responsive two-icon pair, owns clipboard (with
  legacy fallback) + success toasts + click-propagation stopping. You pass
  `human` (readable text) and `agent` (an `AgentPayloadInput`, a prebuilt
  string, or a builder fn) + a `label`. Sizes: `"xs"` (h-5 — dense items,
  metric cards, per-field), `"icon"` (h-7 — rows/cards), `"sm"` (larger header
  target). **Every size is icon-only.** Pass `human`/`agent` as **functions** —
  resolved at click time.
- **Copy exists at EVERY granularity** — field/entry, item, row, list, record,
  page. Never display data the user can't copy. Dense surfaces hide the control
  until hover (`opacity-0 group-hover/x:opacity-100 focus-within:opacity-100`).
- **Exactly the canonical compact two-icon copy/export pair:** one icon-only human Copy control plus one icon-only CopyForAiIcon menu,
  ordered Copy JSON → Copy for AI → shaped AI variants →
  downloads/destinations. Large or visibly labeled top-level copy buttons are
  banned. Keep JSON inside the Copy-for-AI menu; never create a third top-level
  control. Scalars skip JSON. Copy-for-AI is NEVER just JSON in an envelope.
  **`CopyButtons` owns the pair** — pass `export` for downloads and
  destinations, `hide` to drop any category (cards: omit `export` or
  `hide={["export"]}`). A menu item may
  `onSelect` / `modal` instead of copying. Do not also render `ExportMenu`
  beside it.
- **`CopyForAiIcon` is canonical.** `Sparkles`, `Sparkle`, bot, face, star, or
  any substitute is banned for AI copy. Tooltips/accessibility names carry the
  words; visible Copy/JSON/Copy-for-AI text is forbidden.
- **Every data surface offers EXPORT** (`ExportMenu` + `export.ts`): lists and
  tables get JSON + CSV downloads; pages get their data JSON. Copy without
  export is half the job.
- **Truncated lists must offer the rest** — a "top 8" with no show-all toggle
  is a defect; copy/export always cover ALL rows, not the visible slice.

## Sized to data — most Copy-for-AI controls are DROPDOWNS

It is impossible to guess what the user wants to share when there is real
data. Judge the size class for EVERY surface — a judgment call about the
page's usage, never a global rule:

| Data                                                                                | Control                                                      | Menu contents                                              |
| ----------------------------------------------------------------------------------- | ------------------------------------------------------------ | ---------------------------------------------------------- |
| **Small / bounded** (one record, short list)                                        | two icons; AI is direct only when exactly one AI action exists | Copy + JSON when structured + faithful AI                  |
| **Medium** (focused list, digestible page)                                          | Copy icon + AI menu                                        | Copy + JSON + faithful AI + 2–5 shaped variants            |
| **Massive** (can reach ~10k+ chars: conversations, big tables, multi-section pages) | Copy icon + AI menu + **custom workspace**                 | Copy + JSON + AI variants + downloads + tunable custom     |

- **A single button on a payload that can reach ~10k chars is a defect** —
  thousands of tokens the user can't see or control.
- **The default (plain click) is the what-I-see variant.** Wire `agent` = the
  focused rendered-view payload, label it via `agentVariant`
  (`position:"first"`); the raw full dump is the "Everything" menu variant,
  never the default.
- **Variants are shaped by USAGE, not arbitrary slices.** Think through what is
  non-optional on this page vs optional. Good menus: "Overview + counts" /
  "Overview + summaries" / "Transcript focus" / "Everything" (cx-explorer
  bundle); "Schema + sample" / "This view (md)" / "Column profile" /
  "Full rows" (cx-explorer tables).
- **Custom composer levers, by data shape** (offer the ones that fit — never
  blind truncation): format (Markdown/CSV/JSON/key-value) · row count
  (All/5/25/100/custom) · which rows (first/last/sample) · per-cell char cap ·
  visible-columns-only · drop-empty-columns · stub-JSON-cells · include-nulls ·
  schema header · strip binary — and for narrative data: per-message caps,
  include thinking / tool calls / tool results, last-N, model-visible-only.
  Multi-table bundles get a **per-section level dial** (Full / Trunc / Per-row /
  Summary / Counts / Off) with the overview header recommended always-on.
- **Live char / ~token / byte counts in every dialog** — the user must know
  what they're getting into. The chrome (`AiCopyMenu`) renders these free.
- **A stub is honest:** it states what was omitted and how big it was, so the
  agent knows to ask. Shortened variants are lossy in DATA, never in ambient
  context — envelope `context` + KPIs identical across variants.
- **"With prompt" variants:** where a payload has one obvious next action,
  offer a sibling variant that wraps the faithful payload in an instruction
  brief. Canonical: Error Inspector — "Error(s)" (`agentVariant`, first) +
  "Error(s) with prompt" (`lib/diagnostics/buildCapturedErrorPayload.ts`:
  prompt before, payload in its own XML tag, reminder after). Same family:
  the dead-ends / lint-debt consoles' paste-ready repair-brief buttons
  (`features/admin/*/fix-prompt.ts`).
- Shortening logic lives in **pure per-data builders**
  (`(data, opts) => { text, ...counts }`, no React) in a `*AiSources.ts` /
  `copy.ts` module — never in the chrome, never inline at callsites. Derive
  preset variants from an existing section list (Backlinks does
  `applyGroomerPreset` over its groomer sections — never a second list).
  `MatrxDataTable` takes `copy.aiVariants`/`copy.aiCustom` for the toolbar
  view copy.
- **The Groomer is an item inside the page-level Copy-for-AI menu.** It
  opens a WindowPanel where the user grooms the whole-page payload: sections with
  `full/compact/brief/off` dials, Everything/Balanced/Minimal presets, live
  size (chars + ~tokens), live preview. Full contract in the README. The
  page-level "everything" is **composed from the per-section builders**, never
  a parallel implementation. Pass `groomer={getGroomerConfig}` to
  `CopyButtons`. **Never render `AgentCopyGroomerLauncher` beside it.**
- The **"Copy for AI" button is a deliberate seam**: when the surfaces-registry
  - tool-injection layer lands, it flips from "copy to clipboard" to "hand
    context + callable actions to the agent" and every existing callsite comes
    along for free. Keep `kind` slugs stable and `attributes` meaningful.

## Exemplars — study before building, best first

1. **aidream cx-explorer** (admin dashboard, `/cx-explorer`) — the platform's
   best. `apps/dashboard/src/components/agent-copy/`: `tableRowsAiSources.ts`
   (generic any-table variants + custom export), `conversationBundleAiSources.ts`
   ("Open composer…" per-table level dials), `conversationAiSources.ts`
   (transcript levers), `conversationTranscript.ts` (reference pure builder),
   `features/cx-explorer/model-context/wire-ai-source.ts` (honest stubs +
   mirrored metrics). Its payload shaping is the reference; consolidate its
   legacy separate JSON-copy control into the canonical Copy-for-AI menu.
2. **Backlinks** — `features/marketing/components/backlinks/BacklinksWorkspace.tsx`:
   full-granularity page (cards + dimension lists + table + groomer), presets
   derived from the groomer sections.
3. **Error Inspector** — the "with prompt" sibling-variant pattern (above).
4. **Access planner** — `features/admin/relationships/access-planner/copy.ts` +
   `buildPanelView` in `AccessPlannerImpl.tsx`: what-I-see panel payload from
   LIVE form state with `unsaved_changes`, blockers verbatim, KPI framing;
   full dump demoted to "Everything".

## How to wire a surface (the whole job)

```tsx
import { CopyButtons } from "@/components/agent-copy/CopyButtons";

// per-row / per-card — one compact two-icon pair:
<CopyButtons
  size="icon"
  label={`Sandbox ${row.sandbox_id}`}      // used in toast + tooltip
  human={() => summary(row)}               // page/feature-specific readable text
  agent={() => ({
    kind: "sandbox-instance",              // STABLE root xml tag/identifier
    location: "AI Matrx Admin — Sandbox Management",
    description: "A single sandbox instance row.",
    data: row,                             // rendered-view data (see MISSION)
    summary: summary(row),                 // optional <summary> block
    attributes: { id: row.id, status: row.status },
  })}
/>

// whole-list / whole-page — the same icon-only pair in the header/toolbar:
<CopyButtons
  size="sm"
  label="All sandboxes"
  human={() => list.map(summary).join("\n\n")}
  json={() => list} // becomes the second menu item, never another icon
  agent={() => ({ kind: "sandbox-instances", location, description,
                  data: list, attributes: { count: list.length },
                  context: { filter, total } })}
/>
```

### Tables: use the built-in config, never hand-wire rows

`MatrxDataTable` takes a `copy` config (`rowKind`/`listKind`/`humanRow`/…) and
delivers ALL of: per-row two-icon action pairs, a toolbar this-view pair
(Copy + JSON + AI + JSON/CSV/Excel downloads + Google Sheets), a record control
in the row-window header, and per-field hover controls in `DataRowInspector`
(side panel + window). Page KPIs,
warnings, and live filters that must survive a zero-row view go in
`copy.listContext`; mirror the same scalar counts in `listAttributes` and
`rowAttributes`. Also pass
`window={{ title }}` so rows open the record window.
Domain-specific row AI actions (for example a paste-ready repair brief) go in
`copy.rowAiVariants`; the table threads them into that same row menu in cards,
desktop rows, side panels, and windows. Never add an action column or another
copy control for the variant.
**Page already has its own header row above the table?** Set
`copy.showToolbar: false` and put one `CopyButtons` with `export` IN that row —
otherwise the table renders a near-empty toolbar row holding only copy icons
(the exact mess Arman flagged on backlinks). Table titles are user words
("Backlinks"), never internal ("Stored backlink rows"); counts are a subtle
muted `tabular-nums` beside the title, never a sentence pushing the search.
`JsonInspector` takes `agentCopy` for raw-JSON surfaces.

### Whole-page: one pair, Groomer inside the AI menu

Page header gets one icon-only `CopyButtons` pair. Its AI menu contains
JSON, the what-I-see payload, Everything, shaped variants, and the Groomer
custom workspace whose sections mirror the page's areas. Declare sections once
and derive the quick payload from `sections.build("full")` — never maintain two
section lists or place another launcher beside the control. Supply the workspace
through `groomer={getGroomerConfig}` on that same `CopyButtons`.

### Step-by-step

1. **Find where the list actually renders.** Most `/administration/*` pages are
   thin wrappers (9–25 lines) that delegate to a feature component — the `.map()`
   lives in `features/*`, not the page. Wire it in the **feature component** so
   admin AND user surfaces both benefit. (Quick check: `wc -l` the page; <30
   lines ⇒ it's a wrapper, go find the component it renders.)
2. **Answer the MISSION question** for this surface: what is the user doing
   here, what does the page lead with, where do errors render, what is live
   form state? That answer IS the primary payload spec. Then judge the size
   class per the table above.
3. **Add a shared `human` summary** in the feature's `format.ts`/`copy.ts`
   (e.g. `lib/sandbox/format.ts`, `features/ai-models/format.ts`). Reuse it for
   both the row and the list. **Never duplicate** the summary across files.
4. **Per-row:** drop `<CopyButtons size="icon" …>` in the row's action cell.
5. **Whole-list:** drop `<CopyButtons size="sm" …>` in the toolbar/header,
   guarded by `list.length > 0`.
6. **Detail/record pages:** one `<CopyButtons size="sm">` in the header that
   copies the rendered record view — live URL + full CURRENT state is the
   highest-value capture.
7. Set a stable `kind`, a clear `location` (include the route), and useful
   `attributes`/`context` (counts + the page KPIs).
8. **Run the acceptance test** (payload vs screenshot), then
   `pnpm exec tsc --noEmit` the touched files; commit per page/component.

## Module-audit protocol — sweep a feature BEFORE wiring

**Assigned a whole feature/module (not one page) → read [module-audit.md](module-audit.md)**
before wiring: enumerate surfaces, classify each element, size its AI control, audit existing
payloads against the MISSION, and emit the coverage table before writing code.

## Pitfalls (these will bite you)

- **Clickable rows:** if the `<tr>`/row has an `onClick` (navigate/select),
  wrap `<CopyButtons>` in `<span onClick={(e) => e.stopPropagation()}>` (or put
  it in a cell that already stops propagation) so copying doesn't also
  select/navigate. See `AiModelTable` RowActions and the invitation-requests
  cell for the pattern.
- **Don't reinvent the envelope.** The agent flavor is `buildAgentPayload` only.
  Don't hand-roll xml or a JSON dump at the callsite (that anti-pattern is what
  this primitive replaced on the admin sandbox page).
- **Never remove a working feature.** Consolidate duplicate AI buttons into ONE
  dropdown; never delete an existing copy / download / redaction affordance.
- **Skip non-record surfaces.** Tools/composers/visualizers (email composer, SQL
  workbench, schema visualizer, markdown tester, component demos) have no
  copyable record — don't force buttons there. Copy belongs on lists & records.
- **Don't overwhelm.** Favor per-row + copy-all on lists; a single whole-record
  copy on detail pages. More than that clutters.
- **`size="icon"` is h-7 w-7;** if a row uses denser actions (h-6) it'll be a
  hair larger — acceptable, don't fight it with overrides.

## Rollout status

**Continuing the rollout, checking whether a surface is already wired, or touching a known
offender → read [rollout-status.md](rollout-status.md)** (what is done, law-compliant form
surfaces, known raw-dump debt, open per-item gaps) — and update that file as you go.

## Roadmap — from "copy" to "connect"

The full vision lives in [`components/agent-copy/README.md`](../../../components/agent-copy/README.md):
page-level state capture, integration with the **surfaces registry**
(`features/surfaces/`, see the `surface-authoring` skill), automatic screenshots
(`hooks/useScreenCapture.ts`), and **dynamic tool injection** (register a page's
state + callbacks so an agent can call them with args). Keep `kind`/`attributes`
stable now so they become the tool vocabulary later. Extraction stays a pure
function of (data, options) so AI features can call the same builders with no
clicking; payloads self-describe (summary + counts) so a future agent can fetch
just the slice it wants.
