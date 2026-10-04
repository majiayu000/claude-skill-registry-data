---
name: surface-authoring
description: "Lifecycle for AI Matrx agent-aware UI surfaces. Use when creating a surface in features/surfaces/manifests/, or completing or repairing one that is partial, stubbed, unregistered, missing runtime context or context menus, or not agent-wired. NOT for certifying a surface (use surface-check)."
---

# Surface authoring

This is the ONE surface lifecycle skill. It owns the manifest contract, layered registration, runtime emission, canonical-menu rollout, Pro inputs, bindings, DB sync, and verification. Reference consumer for every registration layer: **`features/transcription-cleanup/`** (`/transcripts/cleanup`).

## Completion states and required receipt

**The agent assigned to finish the surface owns its implementation and focused sync/check through this receipt. Do not reassign that work to an unnamed coordinator.** A named coordinator may explicitly retain one bounded external step; name that dependency, its owner, and its next action, and keep the overall claim incomplete.

There are three distinct states:

1. **Authoring integration** proves this surface works: source, selected live mirror, runtime/menu, and each applicable helper-context seam. A surface type never makes a helper binding `N/A`; native and resident agents instead require isolation evidence.
2. **Independent full certification** is the separate S1–S18 candidate and fresh verifier process owned by `surface-check`. It alone permits `certified` / final ledger claims.
3. **Release admission** is the release script's read-only committed-candidate `--check --registration-only` check for required registration keys. It neither performs authoring sync nor requires full certification. A partial source change may ship only if admission passes, and must remain honestly partial.

Fill this receipt, rather than replacing it with a narrative. For a read-only assessment, fill unexecuted steps as `NOT RUN`, retain the exact commands with the surface placeholder, and name the evidence that execution must collect; do not omit the receipt because execution is unavailable:

```md
## Surface integration receipt — <client>/<local>
- Assigned implementer: <name>; source commit: <SHA>
- Focused sync: `pnpm exec tsx scripts/sync-surface-manifests-direct.ts --surface <client>/<local>`
  - Result: <PASS/FAIL/NOT RUN>; time: <UTC timestamp>; reason if not run: <reason>
- Full live check: `pnpm exec tsx scripts/sync-surface-manifests-direct.ts --check --surface <client>/<local>`
  - Result: <PASS/FAIL/NOT RUN>; time: <UTC timestamp>; parent + values/roles/write-targets/client-tools + metadata + system/public: <result or reason>
- Runtime/menu proof: <each editable/presentational region, actual controlled-state mutation, current live values, terminal UI result>
- Contract truth: <all routes sharing identity checked for Always keys; async values belong to current inputs; source attribution names the actual product>
- Helper-context proof: <agent/job, surface, purpose, mode: none|named_inputs|approved_surface_context, allowed names or approved snapshot, approval provenance, save receipt, launch request, persisted variables or native/resident isolation evidence>
- Readiness: <partial|verified>; note: <exact remaining condition or why earned>
- Remaining work: <none OR exact work>; owner: <name>; boundary/next action: <text>
- Independent certification: <not requested|candidate ref|verifier name, timestamp, evidence>
```

## Rationalizations

| Excuse (verbatim) | Reality (one line) |
|---|---|
| “not ready for certification or release” | Certification and release admission differ; partial source may release, never as functioning or certified. |
| “owns the remaining emitter repair” | The trial assigned this to an unnamed coordinator; the assigned implementer retains ordinary completion. |
| “exclude this surface from the train unless the verifier passes” | A verifier is required for certification, not for a clearly labeled partial source change to enter the pre-launch release. |

## Red flags

- Assigning remaining implementation to a coordinator who never accepted it.
- Replacing concrete sync/check and binding receipts with “focused checks”.
- Making a verifier's certification verdict a blanket release prerequisite.

## Choose the path

- **Agent-native or resident-agent surface:** run the same context-contract
  analysis. Outside helpers may work on any page, including Chat and Agent
  Builder. The native subject agent receives only engineered inputs. Permanent
  residents have no automatic inheritance but may use named inputs or approved
  surface context under their deliberate job contract; placement or binding
  alone never approves inheritance.
- **New or structurally changed surface:** follow this file from identity through layered registration.
- **Existing surface that needs completion or repair:** read [`references/runtime-rollout.md`](./references/runtime-rollout.md), then close every applicable contract here.
- **Context-menu wiring or repair:** invoke `context-menu-v3`; its skill owns wrapper choice, per-row delegation, `contentSource`, `entity`, and no-fake-menu proof. This skill owns making that canonical menu part of a complete surface.
- **Full certification:** invoke `surface-check`; it drives the S1–S18 checklist and ledger.
- **Binding-service internals** (`packages/chat/src/surfaces/services/bind-agent-to-surface.service.ts` itself) and **context-menu primitive internals** are not this skill — this skill consumes them.

## Branch references — read only when the run reaches that branch

- **Creating a brand-new manifest file** (template, scope-builder placement, registry wiring, confirming `ui_client`, focused mirror sync) → read [`references/new-manifest.md`](./references/new-manifest.md).
- **`inheritsFrom`, a parent surface, or fixing a family's shadows** → read [`references/inheritance.md`](./references/inheritance.md).
- **Writing launch code, Locate anchors, or hierarchy chrome** → read [`references/runtime-emission.md`](./references/runtime-emission.md).
- **Overlay/window panel surface** → read [`references/overlay-surfaces.md`](./references/overlay-surfaces.md).
- **Surface declares `writeTargets`** → read [`references/write-targets.md`](./references/write-targets.md).
- **Adding/removing/changing values on an existing manifest, or deleting a manifest** → read [`references/update-or-remove.md`](./references/update-or-remove.md).
- **Adding live scope or a canonical v3 menu to UI that already exists — including a page or window being registered as a surface for the first time — or completing/repairing any existing surface** → read [`references/runtime-rollout.md`](./references/runtime-rollout.md) (its menu contract and live completion gate: canonical submenu label, no `INERT MENU` / `VALUE MAPPING GAP`, real `extraSections` handlers, focused `--surface` sync).
- **Looking up where a type, helper, service, route, or check lives** → read [`references/file-map.md`](./references/file-map.md).
- **Working the surface campaign (making many surfaces agent-readable in batches), or coordinating it** → a worker reads [`references/campaign-worker.md`](./references/campaign-worker.md) and nothing else; a coordinator reads [`references/campaign-coordinator.md`](./references/campaign-coordinator.md). Tools: `pnpm surface:census` (the one list) and `pnpm surface:probe` (verify a surface on the live site, no dev server). Open gaps: `docs/handoffs/surface-campaign.md`.

This list names every reference file; a run that reaches none of these branches needs only this file.

Adding a surface is **code-first, DB-mirror**. Code is the single source of truth — the DB is a synced reflection. Get the manifest right and everything downstream (binding UIs, chrome labels, drift report, RLS-gated agent + tool bindings, the runtime resolver) just works.

## What a surface is — and the recursion that trips people up

A **surface** can give a specifically approved outside helper highly specific
context. Agent-native hosts do not remove that capability: they require an
documented integration contract so the subject agent and residents keep their
own engineered context.

**A context item in one surface can itself BE a surface — and then its context is its own parts, not itself.** This is the model that confuses people:

- In the **chat** surface, the working document and the scratchpad are **context items** — whole values handed to the conversation's agent.
- **Step inside** one and it stops being a context item. It becomes its **own surface**, and its context items are its **parts**: the body text, the selection, the id, the title. You would never attach the whole document as its own surface's context — that's circular. The parts are the context.
- **Zoom back out from inside:** the conversation the document hangs off is **not** its context either — it's a **reference** (`conversation_id`) plus whatever the host chooses to pass through the link (`conversation_context`). A reference, not an embed.

**Purpose flips when you step inside.** Outside, the scratchpad is "the user's private notes the cloud agent only reads." Inside, it is **just text** — a context-menu agent there can absolutely edit it (bullet it, tabulate it, clean it up). The read-only-ness was a fact of the *outer* surface, not an intrinsic property of the text.

**Boundaries are a perspective you choose, then commit to.** The chat sidebar (list of chats + agents) and the open chat (one `conversation_id`) can be modeled as **two surfaces** (a list surface + a single-conversation surface) **or one** (a chat surface with an active conversation *and* a list of the others). Both are valid. Pick the framing that matches how agents will be bound, then design to it.

**Same shape ≠ same surface.** Two surfaces can share an identical value set and still be two surfaces when the *purpose* — and therefore the bound agents — differ. `matrx-user/working-document` and `matrx-user/scratchpad` share one value set (`_conversation-document.manifest.ts`) but stay separate because a co-author agent belongs on one and not the other. Conversely, only merge kinds into one surface when the values AND the relevant agents are ~identical.

## THE NAMING LAW — one canonical label, everywhere

**`SurfaceManifest.label` is REQUIRED.** It is the ONE canonical human display name for the surface — unique per client (case-insensitive; `pnpm check:surface-drift` fails on a missing or clashing label). Every value's `label` and every group's `label` is equally canonical.

- **No chrome may hand-type, override, or re-derive a surface/value/group label.** The `surfaceLabel` runtime override prop was DELETED; ESLint bans it (`surfaceLabelOverrideBan` in `eslint.config.mjs`).
- Chrome derives the surface name via **`getSurfaceDisplayLabel(surfaceName)`** from `packages/chat/src/surfaces/utils/surface-display.ts` (static + synchronous; safe in server and client components). `labelFromName` slug fallback is for manifest-less DB surfaces ONLY.
- **On-page section titles and field labels for declared values render via `surfaceValueLabels(manifest)` / `surfaceGroupLabels(manifest)`** (same file) — byte-identical to the manifest. A page that hand-writes "Page intent" next to values grouped under `page_intent` is a defect; render `G.page_intent`.
- `label` is mirrored to `ui_surface.label` by manifest sync (ALWAYS written); DB drift shows in the drift report as `surfaceLabelDrifts`.
- **Labels never enter agent feeds.** aidream's manifest feed carries machine names + `group_key` only — agents see `name`, humans see `label`.

## THE COMPLETENESS LAW — declare everything the page loads

**Every piece of data/state a page loads MUST be declared as a surface value.** Individual fields AND their natural composite/group values are both mandatory — e.g. `marketing-page` declares the composite `page_intent` object alongside its four constituent fields. Optional convenience packs are the only discretionary part.

Undeclared runtime keys show loudly in the Surface Context window under **"Undeclared (runtime only)"** — every entry there is a defect: either declare the value or stop emitting it. Use `autoContext: false` to keep declared-but-rarely-needed values out of automatic agent context; never use non-declaration for that.

## READINESS TRACKING — the campaign field

Every manifest declares `readiness: "verified" | "partial" | "stub"` (REQUIRED — the compiler enforces it) plus `readinessNote` saying what's missing whenever it isn't `verified`. This is the platform's tracker for "which surfaces are verified correct and complete". Rules:

- `verified` is EARNED: full completeness audit against the live page, curated groups, emitter wired, checklist green. Never stamp it aspirationally.
- Any change that adds page data without declaring it, or declares without emitting, demotes the surface — update `readiness` in the same edit.
- Mirrored to `ui_surface.readiness`; the admin board at `/administration/ui/surfaces` rolls up Verified / Partial / Stub / Unregistered (DB rows with no manifest). Readiness is code-owned — never edited in the DB.

## OVERLAY SURFACES — windows are surfaces too

**Overlay/window panel surfaces only (`overlayId`, provider inside the window and AROUND its context menu) → read [`references/overlay-surfaces.md`](./references/overlay-surfaces.md).**

## The 4-step add (canonical)

```
1. Make sure ui_client row exists       (matrx-user / matrx-admin / matrx-public / chrome-extension)
2. Add the manifest file + register     (features/surfaces/manifests/...)
3. Sync that surface's DB mirror        (direct transactional `--surface` command)
4. Verify its live mirror              (matching `--check --surface` command)
```

Then in the surface's code: emit an `ApplicationScope` via `createXxxScope(...)` and pass `runtime: { surfaceName: "<client>/<local>" }` to `launchAgentExecution`.

## Naming contract

| Thing | Rule | Enforced by |
|---|---|---|
| `ui_client.name` | Lowercase kebab. One of `matrx-user`, `matrx-admin`, `matrx-public`, `chrome-extension` (current set). New clients are rare — confirm with the user. | DB |
| `ui_surface.name` | `"<client>/<local>"` — single slash, kebab-case both halves. e.g. `matrx-user/notes`, `matrx-admin/system-agents/agents`. | DB FK + `scripts/check-surface-drift.ts` |
| `SurfaceManifest.label` | REQUIRED. Canonical display name, unique per client (case-insensitive). | Drift check + sync mirror |
| `SurfaceValue.name` | `^[a-z][a-z0-9_]*$` — lower snake_case, must be unique within the surface. Becomes the key in `ApplicationScope`. | DB CHECK constraint + drift check |
| `SurfaceValueGroup.key` | `^[a-z][a-z0-9_]*$`; `general` / `baseline` / `inherited:*` are RESERVED (registry-synthesized). | Registry throws + drift check |
| Manifest filename | `<local-slug>.manifest.ts` (the part after the slash). Same kebab as the surface. | Convention |
| Exported manifest const | `<localSlug>Manifest` (camelCase from kebab). | Convention |

If the user asks for a surface name that doesn't match `^[a-z][a-z0-9-]*\/[a-z0-9-/]+$`, push back before writing anything — the drift script will fail otherwise.

## Required reading before editing manifests

These are short — read them when the task is non-trivial:

- `packages/chat/src/surfaces/types.ts` — `SurfaceValue`, `SurfaceValueGroup`, `SurfaceManifest`, `ValueMapping`, `SurfaceScopePayload`
- `features/surfaces/manifests/_baseline.manifest.ts` — `BASELINE_VALUES`, `pickBaseline`, `mergeBaselineValues`
- `features/surfaces/manifests/registry.ts` — register your manifest in **`RAW_MANIFESTS`**; `ALL_MANIFESTS` is derived from it (inheritance resolved, baselines injected, provenance + groupKey stamped) and is what everything consumes
- `features/surfaces/manifests/marketing-page.manifest.ts` — **THE reference implementation**: 40+ values, 7 curated groups, full contract, `inheritsFrom` chain (marketing-site → marketing-brand), scope builder in a separate runtime module (`features/marketing/lib/marketing-page-scope.ts`), emitter in `PageWorkspace.tsx`
- `features/surfaces/manifests/notes-editor.manifest.ts` — the simple case (baseline + specific + in-file scope helper)

**`intro` — the surface's self-introduction.** A single XML-ish block (`<surface_intro>…`) telling the agent what this surface IS, what the user does here, and how to read its values. Written from a close understanding of the surface's PURPOSE — this is the first surface-context item the agent sees. Mirrored to `ui_surface.intro`. Every Tier-1 surface should have one. It describes the SURFACE and the user — never the model: no "You are the agent for…" / "Your job is…" framing (the bound agent's identity and rules live in the DB agent; `pnpm check:hardcoded-prompts` flags intros that assign the model a role — say "You are on…" / "The work here is…").

For `agentRoles`, `configNamespaces`, `evidenceSources`, and `skipBaselineValues`, follow **End-to-end layered registration** below.

## Value groups — canonical sections

`SurfaceManifest.groups` declares `SurfaceValueGroup { key, label, sortOrder, description? }`:

- **Curated groups author `sortOrder` 0–899.** Everything above is reserved for registry-synthesized groups.
- Every `SurfaceValue.group` must reference a declared group key. Ungrouped own values land in the synthesized `general` group.
- **Reserved keys `general`, `baseline`, `inherited:*` may NOT be declared** — the registry synthesizes them (throws at module init if you try).
- The registry stamps every resolved value with **provenance** (own / inherited / baseline) and a `groupKey`, synthesizes `inherited:<parent>` groups ("Inherited from <parent label>") and the `baseline` group ("Generic baselines"), and **sorts values by (group sortOrder, value sortOrder): curated groups first, inherited next, baselines LAST.**
- Groups mirror to `ui_surface.value_groups` (JSONB) and per-value `ui_surface_value.group_key` on sync; DB drift shows as `valueGroupsDrifts`.
- Group like the page reads: identity, intent, evidence, content — see `marketing-page.manifest.ts`'s 7 groups.

## The `SurfaceValue` shape — every field matters

```ts
interface SurfaceValue {
  name: string;              // snake_case, unique in surface, regex-checked
  label: string;             // canonical human label — THE NAMING LAW applies
  description: string;       // 1-2 sentences. WHEN it's populated AND what it represents
  valueType: "string" | "number" | "boolean" | "object" | "array" | "document";
  alwaysAvailable: boolean;  // true ONLY if the surface guarantees it on every launch
  typicalCharCount: number;  // avg stringified size — drives context-window warnings
  autoContext?: boolean;     // default true — auto-added to agent context; false = bindable-only
  group?: string;            // key of a declared SurfaceValueGroup; omitted = general
  sortOrder?: number;        // optional, defaults to 1000 in DB; orders within the group
}
```

Each field has rules. Don't half-fill the manifest — binding UIs, on-page chrome, and the LLM all consume this.

### `name`

- Lower snake_case. The regex is `^[a-z][a-z0-9_]*$`.
- Becomes the key the surface emits in `ApplicationScope`. **Match what the surface actually puts in the bag.**
- Prefer reuse from `BASELINE_VALUES` (`selection`, `content`, `context`, `text_before`, `text_after`) — that's how the v3 context menu and existing agent shortcuts keep working without remapping.

### `label`

- 2-4 words, sentence case. THE canonical name — the mapping editor, the Surface Context window, and on-page section/field chrome (via `surfaceValueLabels`) all render exactly this string.
- Examples: "Current selection", "Active note id", "Open file path".

### `description`

- 1-2 sentences. Must cover **WHEN** it's populated and **WHAT** it represents.
- Mention the empty case explicitly. The mapping UI shows this on hover; the LLM uses it when the binding goes through.
- Good: `"UUID of the note the user has open. Empty when no note is open (e.g. on the notes list)."`
- Bad: `"The current note."`

### `valueType`

- Drives the mapping editor's input affordance and validation.
- Almost everything stringifies for LLMs at runtime — pick what reflects the JS shape the surface emits, not what the LLM "sees."
- `array` for ID lists, tab lists, file lists.
- `object` for free-form bags and for composite group values (like `page_intent`) — prefer named values over an unstructured `object`.

### `alwaysAvailable` — get this right

This is the most-abused field. Only set `true` when the surface code **literally always** writes this key on every single launch, regardless of UI state.

| Case | Verdict |
|---|---|
| `open_tab_ids` in an editor (could be empty array but always an array) | `true` |
| `current_file_id` in an editor that requires a file open | `true` |
| `current_file_id` in an editor where the user might be on an empty workspace | `false` |
| A utility-only value on a manifest shared by several routes | `false` unless every route emits it; inspect every mount, not only the edited page |
| `selection` anywhere | `false` |
| `content` (full file body) | `false` (only `true` if you guarantee non-null) |

The `createXxxScope` TS helper uses this to mark keys as required (no `?`) vs optional (`?`). Lying here defeats the "a UI cannot lie" enforcement.

### `autoContext` — signal vs noise

Declaring many values is MANDATORY (THE COMPLETENESS LAW); auto-shipping them all to the agent is NOT. Ask: *what does an agent on this surface truly need?* (a note surface: id, content, cursor, open tabs — not everything you could enumerate). Those keep `autoContext: true` (default); everything an agent could **look up from an id** is "inconvenient but resolvable" → `autoContext: false` (bindable-only). Mirrored to `ui_surface_value.auto_context`.

### `alwaysAvailable` is earned by ROUTING

A value can only be *guaranteed* when the surface's identity lives in the URL. `notes/[id]` can promise `id`, `content`, `cursor_position`, `selection` on every launch (even when empty) — a surface whose active record is component state cannot. **Tab test:** tab-as-route → surface values are guaranteed and precise; tab-as-state → they're useless. The ideal shape is list page → `[id]` page → per-tab routes → URL params. When authoring a manifest for a surface without solid dynamic routing, flag the routing gap to the user — moving the surface toward routed identity is often worth more than more values.

### `typicalCharCount`

- Estimate after stringification (numbers → `"42"`, objects → `JSON.stringify`).
- Used by binding UIs to warn agent engineers when they bind a variable to something big enough to blow LLM context.
- Don't be precise. Reasonable bands:
  - IDs / short labels: 36 (UUID), 60–120 (titles)
  - Selections / snippets: 200–500
  - Lists of IDs: `(36 + 2) * typical_count`
  - Full document bodies: 5000–20000

### `sortOrder`

- Optional. Defaults to 1000 in the DB. Orders values **within their group**.
- The baseline values are 100/110/120/200/9999 — leave headroom around them and increment by 10 within your own values (300, 310, 320…).

### Baselines are auto-injected — opting out

The registry **injects the full baseline set into every manifest** (`withInjectedBaselines` in `registry.ts`) so agent authors can bind generic values on any surface. A same-named value you declare wins over the injected one; baseline-named values always land in the synthesized `baseline` group. Passing `[]` to `mergeBaselineValues` does NOT skip baselines — the registry re-adds them. A surface with genuinely no text/content concept (e.g. a metadata-only widget) opts out with **`skipBaselineValues: true`** on the manifest.

## Write targets — the WRITE half of a surface (v1, 2026-07-29)

**Surfaces that declare `writeTargets` only → read [`references/write-targets.md`](./references/write-targets.md).**

## The manifest file (full-contract template)

**New manifest file only (template, scope builder placement, registry wiring, `ui_client` confirmation, focused mirror sync) → read [`references/new-manifest.md`](./references/new-manifest.md).**

## THE FAMILY DOCTRINE — what a parent conveys, what a child owns

**`inheritsFrom`, parent surfaces, or fixing a family (the five rules + marketing worked example) → read [`references/inheritance.md`](./references/inheritance.md).**

## Runtime side — making the surface actually emit values

**Launch code, `data-surface-value` Locate anchors, hierarchy chrome → read [`references/runtime-emission.md`](./references/runtime-emission.md).**

## Updating an existing manifest

**Adding/removing/changing a value on an existing manifest, or removing a manifest entirely → read [`references/update-or-remove.md`](./references/update-or-remove.md).**

## Things to avoid

- **Stuffing everything into `context`.** It's escape-valve only. Each named field is queryable in binding UIs; `context` is opaque to the LLM in mapping previews. If the surface emits 5 obvious things, declare 5 SurfaceValues.
- **Hand-typing a label anywhere.** THE NAMING LAW: chrome and on-page section/field text render through `getSurfaceDisplayLabel` / `surfaceValueLabels` / `surfaceGroupLabels` — never a string literal that duplicates a manifest label.
- **Leaving loaded data undeclared.** THE COMPLETENESS LAW: an "Undeclared (runtime only)" entry in the Surface Context window is a defect.
- **Lying about `alwaysAvailable`.** This breaks the scope-builder type guarantee. If the surface code has any `if` branch that skips writing a key, that key is `false`.
- **Generic descriptions.** "The user's note" tells the LLM nothing. "Markdown body of the note the user has open. Empty when no note is open." is correct.
- **Declaring a reserved group key.** `general` / `baseline` / `inherited:*` are registry-synthesized; declaring one throws at module init.
- **Mismatched `surfaceName`.** `ui_surface.name`, the manifest's `surfaceName`, and the runtime `runtime.surfaceName` must be byte-identical. Binding edges reference the surface by uuid (`platform.associations.target_id`), so a name mismatch doesn't break stored bindings — it silently resolves NO bindings at launch.
- **Skipping the scope helper.** `dispatch(launchAgentExecution({ runtime: { applicationScope: { selecton: "..." } } }))` — typo, no TS error, silent miss at runtime. Always go through the scope builder.
- **Inventing a baseline-style key.** If you find yourself adding `selection` or `content` to `surfaceSpecific` instead of spreading from baseline, stop — you'll fork the description and confuse mappings. Spread from `BASELINE_VALUES` and override only when the surface's semantics genuinely differ.
- **Forgetting to update the helper signature when `alwaysAvailable` changes.** The signature is hand-maintained; the drift script doesn't verify it.

## Quick reference — file map

**Path lookup for types, helpers, services, APIs, admin UI, and checks → read [`references/file-map.md`](./references/file-map.md).**

## Pre-flight checklist

Before you say a surface is added:

- [ ] `ui_client` row exists for the client
- [ ] `<local-slug>.manifest.ts` created in `features/surfaces/manifests/`
- [ ] Manifest imported + included in `RAW_MANIFESTS` in `registry.ts`
- [ ] Full contract present: `label` (canonical, unique per client), `urlPattern`, `intro`, `groups` (curated band 0–899), `inheritsFrom` where true
- [ ] **Completeness sweep**: every piece of data the page loads is declared — fields AND natural composites; no "Undeclared (runtime only)" entries in the Surface Context window
- [ ] Every `SurfaceValue` has: a snake_case `name`, a canonical `label`, a 1-2 sentence `description` covering the empty case, a correct `valueType`, an honest `alwaysAvailable`, a sensible `typicalCharCount`, and a `group`
- [ ] Scope builder exists (in-file for simple surfaces, runtime module for complex ones); required (no `?`) keys match every `alwaysAvailable: true` value INCLUDING inherited ones
- [ ] On-page section/field chrome renders via `surfaceValueLabels` / `surfaceGroupLabels` — no hand-typed label strings
- [ ] Page elements tagged `data-surface-value` anchors for Locate
- [ ] `pnpm check:surface-drift` passes
- [ ] `pnpm check:surface-routes` passes — no phantom mapping, and this route is not silently undeclared
- [ ] Focused transactional sync applied and its `--check` passes
- [ ] Each launch records its context mode. Outside helpers use approved named inputs or approved surface context; native launches have isolation evidence and only engineered inputs; residents have their deliberate contract.

If anything in the checklist is unclear, re-read the relevant section above (or the reference file its pointer names) instead of guessing — the resolver is unforgiving when the contract drifts.

---

# End-to-end layered registration

Registering a surface is a LAYERED recipe — layers may land incrementally, but the completion state and receipt above govern what may be claimed. A manifest with no emitter may ship as partial; it is not a functioning integration. Layer 1 (the manifest) is everything above, including the reference files it points to. **Read first:** `features/surfaces/FEATURE.md` (binding model, inheritance, roles/config) · `features/surfaces/manifests/README.md`.

## Layer 2 — Agent roles + config namespaces

- **Agent role** = a named position the surface PLUGS an agent into (`agentRoles`; cleanup's `clean` + `custom_slot`, scribe's `assistant`). `defaultAgentId` = platform default; users/orgs override in `ui_surface_agent_pref`, resolved `manifest → global → org-by-membership → user` by `services/surface-config.service.ts`. **A system agent's role sets `mandateKey` (e.g. `"masterwork.scout"`) INSTEAD of `defaultAgentId`** — the Holder resolves live from `agent.mandate` (sourceTier `"mandate"`); never freeze an agent UUID in a manifest for a job that has a Mandate (drift check refuses both set at once; reference: `masterwork-rulebook.manifest.ts`). Roles with a resolved agent surface automatically in the shell header Agents menu (`SurfaceAgentsHeaderButton` → `SurfaceBoundAgentsList` "Surface roles") and launch with the page's live scope — never build a bespoke per-page agent menu. **Disclosure never adds chips, badges, labels, rosters, or any other visible page content.** Pages read via `hooks/useSurfaceConfig.ts` / `useSurfaceAgentRoles`. **Never store a per-surface agent choice in `userPreferences` / `useSetting`** — that's the exact legacy this system deleted (`scribeAssistantAgentId`).

  🚨 **THE DISCLOSURE LAW is top-menu-only metadata, never page UI.** Register only a fixed AI job a surface already runs through `agentRoles` or UI-free `useDeclaredSurfaceMandates`, and open its mandate IN PLACE via `useOpenMandateWindow()` rather than linking to a mandate route. Never add an agent chip, badge, label, roster, callout, or section to the surface. Disclosure does not authorize context inheritance. **Invoke the `agent-disclosure` skill** for the full boundary and verification. Guard: `pnpm check:agent-disclosure`.
- **Config namespace** = a typed JSONB bucket in `ui_surface_config` (`dictionary`, `session_defaults`). Adding one = a PURE handler (validate/merge/empty) in `config/namespace-registry.ts` + a manifest `configNamespaces` line. Zero SQL.
- Surfaces with ≥1 role or namespace automatically appear in the user hub at **`/surfaces`**.

## Layer 3 — Registry + drift gate

- Import + add to `RAW_MANIFESTS` in `manifests/registry.ts`, then **`pnpm check:surface-drift` and `pnpm check:surface-routes`** must both pass before anything ships.

## Layer 4 — DB sync (a manifest not synced is not registered)

- A `ui_client` row must exist first. The focused sync creates or updates the selected `ui_surface` row; it never creates clients.
- Run `pnpm exec tsx scripts/sync-surface-manifests-direct.ts --surface <client>/<local>` after the manifest is registered. It changes only that surface and its declared children, in one transaction; it deletes and sweeps nothing.
- Prove the live mirror with `pnpm exec tsx scripts/sync-surface-manifests-direct.ts --check --surface <client>/<local>`. It compares the surface metadata and every declared value, role, write target, and client tool, including system ownership and public visibility.
- Release independently runs `--check --registration-only` from an isolated archive of the committed candidate before tag/push. A failure is a runtime dependency failure, not advisory quality debt.

## Layer 5 — Runtime emitter (`buildScope`)

- An outside helper assembles only its approved scope at **trigger time** (read live refs, not stale state) and launches with the recorded `none`, `named_inputs`, or `approved_surface_context` mode — via the v3 context menu (`EditableContextMenu` / `NonEditableContextMenu`) `surfaceName=` + `getApplicationScope`, `useAgentLauncher().launchAgent`, or `useAiPostProcess`. Approved surface context may be explicit mappings or a user-approved task-relevant snapshot. Cleanup's emitter: `CleanupPad.tsx` `buildScope()`.
- A native subject launch never inherits ambient or ad-hoc surface scope from provider placement or binding; it receives only engineered inputs. A permanent resident launch also has no automatic inheritance and requires its deliberate contract. Prove both boundaries in the invocation evidence.
- Baseline `selection`/`text_before`/`text_after` are captured by the menu itself — don't duplicate.

## Layer 6 — Bindings + verification

Bindings are **`platform.associations` edges** (agent → surface, tier-encoded `role`, `value_mappings` in edge metadata), written ONLY through `services/bind-agent-to-surface.service.ts` — UI paths: `SurfaceAgentBindPanel`, the 5-panel `/agents/[id]/surfaces` shell, or the batch editor. Never write an edge by hand.

Binding availability can be saved independently. Before an actual helper data
handoff, record: agent/job, surface, purpose, context mode (`none`,
`named_inputs`, or `approved_surface_context`), allowed names or approved
snapshot, approval provenance, and evidence. A documented integration contract
or an explicit user choice persists until scope changes; it is not a per-run
prompt. A binding is transport metadata, never approval for a data handoff. Do
not claim runtime enforcement from this record alone: the
current header sends full scope and the mapper can deliver unmapped fields, so
prove the effective request and persisted variables. Native subject agents use
only engineered inputs and require isolation proof. Permanent residents,
including window panels, have no automatic inheritance and use their deliberate
`none`, `named_inputs`, or `approved_surface_context` contract.

Verify like the owner does:

1. For an outside helper, bind a test agent with **deliberately non-matching names** (cleanup's template: agent `Cleanup Surface Demo Reporter` 42971fe0, `working_text` ← `raw_transcript_text`) so name-heuristics can't mask a broken mapping.
2. Launch from the surface; confirm the mapped variables arrived: `cx_conversation.variables` is the DB forensics.
3. **The Matrx-vs-matrix test** (Arman's standard): put "Matrx is the product name (not matrix)" in a bound context value, feed input containing "matrix", check the output spells **Matrx**. If it doesn't, the context never reached the agent — a silently-skipped binding, the exact bug class this system exists to kill.
4. Recovery layers must be **LOUD** (console.warn/error + toast) — a silent skip is how the org-tier bug survived.

## Registration ship checklist

- [ ] `readiness` stamped honestly (verified only after the full checklist; note required otherwise); overlay surfaces carry `overlayId`
- [ ] Manifest + scope builder; required `label`; groups declared + every value grouped; completeness sweep clean; honest values; baselines not duplicated
- [ ] Roles/namespaces declared where the surface plugs in agents/config
- [ ] Registered in `registry.ts`; `pnpm check:surface-drift` AND `pnpm check:surface-routes` green
- [ ] Focused DB sync AND matching full `--check` receipt passed
- [ ] Completion receipt lists every helper/native/resident invocation contract and its evidence; no blanket N/A/exclusion
- [ ] Route prefix in `utils/route-to-surface.ts` (more-specific prefixes ABOVE their parent)
- [ ] Emitter wired; an explicitly deferred emitter keeps `readiness: "partial"` with its remaining boundary named and cannot support a functioning-integration, `verified`, or certification claim
- [ ] Outside helper: non-matching-name binding + Matrx-vs-matrix test passed live; native: only engineered inputs and no ambient/ad-hoc surface values; resident: no automatic inheritance and its deliberate contract only
