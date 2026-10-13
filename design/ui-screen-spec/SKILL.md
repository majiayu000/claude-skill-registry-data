---
name: ui-screen-spec
description: Turn an approved blueprint and system spec into a screen-level implementation contract — mapping components to regions, defining data dependencies, and specifying state ownership — before any component or code work begins. Use this skill after ui-blueprint and ui-system are approved, and before ui-component-spec. It is the missing bridge between layout decisions and implementation.
status: draft
---

# UI Screen Spec

A skill for turning an approved blueprint into a screen-level contract that an implementer can build from without guessing. Where the blueprint answers "what is on the screen and where", the screen spec answers "what component fills each region, what data it needs, and how it behaves in every meaningful state."

This is the document that prevents the most common handoff failure: a developer reading a blueprint wireframe and making silent decisions about component boundaries, data flow, and error handling that the designer never intended.

## When to use this skill

Use this skill when:
- A blueprint exists and has `status: approved`.
- The user is ready to think about component placement, data flow, and state ownership before writing any component specs or code.
- **Spec Recovery:** An implementation exists but no screen spec was created. Use this skill retrospectively to bridge layout and implementation decisions.
- A previous implementation had the right layout but wrong state handling, empty states, or loading behavior — a screen spec should be produced retrospectively before reworking it.
- The feature involves more than two interactive regions — this is where the coordination cost justifies a screen spec.

Do **not** use this skill when:
- No blueprint exists. Run `ui-blueprint` first.
- The screen is a single static component with no state (e.g. a simple `<header>` with a logo and two links). For trivial screens, `ui-component-spec` alone is sufficient.
- The user only wants to document one component in isolation. Use `ui-component-spec` directly.
- A screen spec already exists and is current. Read it rather than re-running this skill.

## Core principle

**A screen spec is a coordination document, not a design document.** Its job is to prevent implementers from making architecture decisions that belong to the designer/product side. Every question a developer might silently answer — "What shows here when there's no data?" "Who owns this loading spinner?" "What happens to the sidebar when the user doesn't have permission?" — should be answered in the screen spec before code starts.

## Pre-flight check

Before drafting, confirm you have:

1. **An approved blueprint.** The screen spec traces directly to a blueprint. If the blueprint is still in draft, the screen spec will inherit its uncertainty — run `ui-blueprint` first.
2. **A system spec or design tokens.** Component names and token references in the screen spec must match the system. If `ui-system` has not been run, mark all token references as `⚠️ TBD`.
3. **The primary user and primary device.** These come from the brief. The screen spec's component choices and density should reflect the device the primary user uses.
4. **A clear list of regions from the blueprint.** Every region in the screen spec must correspond to a named region in the blueprint's wireframe. Do not invent regions not shown in the wireframe.

If any of the four is missing, ask the user or read the upstream document before proceeding.

## Observed vs. Target (Spec Recovery protocol)

When using this skill for **Spec Recovery**, distinguish between the current implementation and the desired contract:

- **Observed:** How the current implementation handles component boundaries, data flow, and state ownership.
- **Target:** The intended or improved contract (what an implementer *should* follow).
- **Gap:** Any missing states, data flow errors, or architectural mismatches in the current implementation.

Use this pattern to ensure the recovered screen spec is a coordination document of intent, not just a description of the current (potentially accidental) architecture.

## Workflow

### Step 1 — Enumerate regions from the blueprint

List every named region in the blueprint wireframe (Header, Sidebar, Main Content, Footer, Modal, Drawer, etc.). These become the top-level sections of the screen spec. Do not add regions the blueprint does not show.

### Step 2 — Assign component instances to each region

For each region, list every non-trivial component that appears in it. For each component, record:
- What the component is called (use a PascalCase name you will reuse in component-specs)
- What data or props it needs
- Where that data comes from (page context, URL param, API call, global store, parent prop)
- Whether it needs its own `ui-component-spec` file (yes for interactive or stateful components; no for pure display wrappers)

### Step 3 — Define state ownership

For every region, declare which of the four mandatory states it must handle: **Ideal**, **Loading**, **Error**, **Empty**. Then answer:
- Which component in the region is responsible for each state?
- Does the loading/error state affect the whole region, or only a sub-area?
- Are any states shared across regions (e.g. a single page-level error banner that replaces all regions)?

Use the state taxonomy from `shared/references/state-taxonomy.md`.

### Step 4 — Map data dependencies

List every external data dependency the screen needs to render:
- API endpoint or data source
- When it is fetched (on mount, on interaction, on scroll, on route change)
- What happens if it fails
- What the empty case looks like (no results vs. no data yet vs. no permission)

### Step 5 — Define permission states

If the screen has any access-control logic, document every permission variant:
- Which regions or components are hidden, disabled, or replaced for each role/permission level
- What the user sees instead of a hidden component (placeholder, upgrade prompt, empty space, redirect)

If there are no permission differences, write "No permission variants — screen is identical for all roles."

### Step 6 — Document responsive composition changes

For each non-primary breakpoint (from the blueprint's responsive table), describe which components move, collapse, or disappear — and what replaces them if anything. Use the reflow verbs from `shared/references/responsive-patterns.md`: `stack`, `collapse`, `hide`, `move`, `resize`, `swap`.

### Step 7 — Flag components that need their own ui-component-spec files

End with a checklist of every interactive or stateful component identified in the screen spec. Each one that cannot be fully specified by the screen spec alone should be flagged for a `ui-component-spec` run.

### Step 8 — Confirm with the user

End with a numbered list of every assumption made and every open question. Ask for sign-off before moving to `ui-component-spec`.

## Output template

Always produce output in this exact structure. Save it as `screen-spec.md` inside the feature's spec package folder. Do not rename it.

```markdown
---
spec_type: screen-spec
spec_id: <slug — should match brief and blueprint>
based_on: blueprint.md
created: <YYYY-MM-DD>
status: draft
---

# Screen Spec: <descriptive screen title>

## 1. Implied or referenced upstream docs
- **Brief:** `brief.md` — goal: <one sentence from brief>
- **Blueprint:** `blueprint.md` — primary device: <device>, layout paradigm: <paradigm>
- **System:** `system.md` — <present / absent — if absent, token references are TBD>

## 2. Region map

_One section per region in the blueprint wireframe._

### Region: <Region Name> (`<semantic HTML element or ARIA landmark>`)

| Component | Data / props needed | Source | Needs component-spec? |
|---|---|---|---|
| `<ComponentName>` | `<prop list>` | `<source>` | Yes / No |

**State handling:**
| State | Responsible component | Behavior |
|---|---|---|
| Ideal | `<ComponentName>` | <what renders> |
| Loading | `<ComponentName>` | <skeleton / spinner in which sub-area> |
| Error | `<ComponentName>` | <what renders — inline message, banner, retry button?> |
| Empty | `<ComponentName>` | <empty state message or illustration> |

_Repeat for each region._

---

## 3. Data dependencies

| Data / endpoint | Fetched when | Failure behavior | Empty case |
|---|---|---|---|
| `<endpoint or data name>` | <on mount / on interaction / …> | <error state description> | <empty state description> |

## 4. Permission variants

<Either a table of role-based differences, or the statement: "No permission variants — screen is identical for all roles.">

| Role / permission | Affected region or component | Change |
|---|---|---|
| <role> | <region or component> | <hidden / disabled / replaced with …> |

## 5. Responsive composition changes

| Breakpoint | Region / component | Change | Reflow verb |
|---|---|---|---|
| Tablet (768–1023px) | <region> | <description> | stack / collapse / hide / move / resize / swap |
| Mobile (<768px) | <region> | <description> | <verb> |

**Critical rule:** The primary action component (<ComponentName>) must remain in the top half of the viewport at every breakpoint.

## 6. Component-spec checklist

The following components require a dedicated `ui-component-spec` file before implementation begins:

- [ ] `<ComponentName>` — reason: <interactive / complex state / shared across screens>
- [ ] `<ComponentName>` — reason: …

Components that do NOT need a dedicated component-spec (pure display, no state, no interactivity):
- `<ComponentName>` — <brief description>

## 7. Open questions
- <Numbered, specific, answerable.>

## 8. Assumptions made
- ⚠️ <Each assumption flagged.>
```

## Examples

### Example 1 — settings page, two regions

**Blueprint:** `settings-page/blueprint.md` — sidebar nav + main form area, desktop primary.

**Correct screen spec behavior:**

The spec identifies two regions: `Sidebar` and `MainContent`.

For the Sidebar region, it assigns `NavigationMenu` (receives `activeSection` from page context) and `UserProfileBadge` (requires user object). It notes `NavigationMenu` is stateful and needs a component-spec; `UserProfileBadge` is display-only and does not.

For the MainContent region, it assigns `SettingsForm` and `SettingsSaveButton`. State handling: Ideal = form rendered with current values from API; Loading = skeleton replacing form fields; Error = inline banner "Failed to load settings — try again"; Empty = not applicable (admin always has settings).

Data dependency: `GET /api/user/settings` — fetched on mount, failure triggers error state for MainContent region, empty case not applicable.

---

### Example 2 — analytics dashboard, four regions

**Blueprint:** four-region layout: top KPI bar, left filter panel, main chart, bottom data grid.

**Correct screen spec behavior:**

The spec maps all four regions. State handling is region-specific: the KPI bar has its own loading skeleton independent of the chart. The data grid has an Empty state ("No data for selected filters") separate from the Error state ("Failed to load — check connection"). The filter panel has no Loading or Error state — it renders from local state only.

Permission variant: users on the free tier see the data grid region replaced by an `UpgradePrompt` component. The KPI bar still renders. The filter panel is disabled (all controls `aria-disabled`).

---

## Anti-patterns

1. **Do not invent regions not in the blueprint.** The screen spec derives from the blueprint. If the blueprint shows three regions, the screen spec has three regions. If you think a fourth region is missing, surface it as an open question — do not add it silently.
2. **Do not leave any region without all four state entries.** "N/A" is acceptable for Empty state only when the data genuinely cannot be absent (e.g. the user's own profile always exists). Loading and Error must always be handled — document how.
3. **Do not copy paste component names without data dependencies.** A region map with component names but no "source" column is not actionable. An implementer reading "renders `DataGrid`" cannot build it without knowing where the data comes from.
4. **Do not mix responsive behavior into the region map.** Responsive changes go in Section 5, not inline in the region descriptions. Mixing them makes both sections harder to read.
5. **Do not defer permission handling to "later".** If the brief mentions any role-based access, document every permission variant in Section 4. Skipping it means the implementer invents the behavior.

## Acceptance criteria for this skill's output

A screen spec produced by this skill is acceptable only if every one of these is true:

- [ ] Every region shown in the blueprint wireframe has a corresponding section in the screen spec — no regions are missing, no regions are invented.
- [ ] Every component listed in a region table has a "data/props needed" column and a "source" column filled (not blank, not TBD unless system spec is genuinely absent).
- [ ] Every region has all four states accounted for: Ideal, Loading, Error, Empty. A state may be marked "N/A" only with a one-sentence justification.
- [ ] The data dependency table lists every external data source the screen needs, with a failure behavior and empty case for each.
- [ ] If the brief or blueprint implies any role or permission differences, a Permission variants section is present and non-empty.
- [ ] Responsive composition changes are documented for every non-primary breakpoint from the blueprint's responsive table.
- [ ] The component-spec checklist explicitly flags every interactive or stateful component for a `ui-component-spec` run.
- [ ] No assumptions are made silently — every assumption is listed in Section 8 with a ⚠️ marker.
- [ ] The frontmatter `based_on` field names `blueprint.md` and the `spec_id` matches the upstream brief slug.

If any check fails, revise before delivering.

---

## Promotion checklist

Complete every item before changing `status: draft` to `status: stable`.

### Evidence on the settings-page fixture

- [ ] Running this skill against `examples/settings-page/` (brief + blueprint + system) produces a `screen-spec.md` that passes every item in the Acceptance criteria above.
- [ ] All regions visible in `examples/settings-page/blueprint.md` appear as sections in the output — no region is missing or renamed without justification.
- [ ] The component-spec checklist in the output flags at least the profile-form component (present in `examples/settings-page/component-specs/`).

### Evidence on the spec-recovery-create fixture

- [ ] Running this skill against `examples/spec-recovery-create/` produces output consistent with `examples/spec-recovery-create/screen-spec.md`.
- [ ] The output correctly notes the three open items that block approval (AI timeout, channel ordering, mobile layout).
- [ ] Each open item references its corresponding entry in `brief.md §9` by number.

### Regression: all four states per region

- [ ] Given a screen spec with a data-fetching region, the output includes Ideal, Loading, Error, and Empty states for that region. None is silently omitted.
- [ ] A region with no async data (e.g., a static heading) has Loading/Empty marked as N/A with a one-sentence justification.

### Skill integration

- [ ] `validate-skill.py` passes for this skill with `status: stable` (no missing sections).
- [ ] `skills.json` entry for `ui-screen-spec` has been updated to `"status": "stable"`.
- [ ] README Skill Map table has been updated to show `stable`.
