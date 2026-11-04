---
name: Component Composer
description: Selects and assembles components from the prototype's component library (enumerated at runtime) with correct props for a given screen description
version: 1.0.0
author: Mattermost Design Team
tags: [prototype, components, react, composition, defense-ux, design-system]
---

# Component Composer

## Purpose

The Component Composer translates a screen description (from a flow audit or wireframe) into a fully typed JSX composition using the prototype's component library. It selects the correct components, configures their props with realistic demo data, applies CSS module classnames, and flags any gaps where the existing library cannot satisfy the screen requirements.

**Build target:** `meta.prototype_root` (a clone of https://github.com/mattermost/mattermost-proto-playground). All component paths below are relative to that project's `src/`. If `meta.prototype_root` is unset or missing, stop — do not guess a path.

**The component inventory is enumerated at runtime — never assume a fixed count or list.** Before composing, list the real components so the composition can only reference things that exist:

```
ls <meta.prototype_root>/src/components/ui
ls <meta.prototype_root>/src/components/layout
ls <meta.prototype_root>/src/components/navigation
```

Use only names returned by those commands. Read the component's `.tsx` to confirm its props before configuring it. This prevents the catalog from drifting against the actual library.

This skill is critical because:
- Prototypes must use only components that exist in `src/components/`
- Every component must be invoked with correct TypeScript props (no `any` or missing required props)
- Demo data must be realistic and defense-context appropriate (military usernames, classification labels, operational scenarios)
- Gaps in the component library must be surfaced early so new components can be justified and built

## When to Use

- **After Scaffolding**: When `prototype-scaffolder` has created the page structure and screen placeholders need component content
- **Screen Population**: When translating a wireframe or flow description into a working prototype screen
- **Component Selection**: When deciding which library components best represent a UI element described in a spec
- **Design Review Prep**: Before presenting a prototype screen for stakeholder review, to ensure all components are correctly configured

## When NOT to Use

- To create new components (new components require separate component development work)
- To modify existing component internals (this skill composes components, not modifies them)
- For pages that need custom layout or interaction patterns not covered by the component library
- Before scaffolding is complete (use `prototype-scaffolder` first)

## Input Requirements

### Input Schema

```json
{
  "type": "object",
  "properties": {
    "screen_description": {
      "type": "string",
      "description": "Natural language description of the screen from the flow audit, wireframe, or spec. Should describe what the user sees, not how to build it.",
      "minLength": 50,
      "maxLength": 3000,
      "example": "A channel header showing the channel name, classification label (SECRET), member count, and action buttons for pinned posts, search, and channel settings. Below it, a message list with 3 posts: one from a human user with a file attachment, one from an AI bot with a structured card, and one system message about a user joining."
    },
    "target_file": {
      "type": "string",
      "description": "Path to the TSX file where the composition will be written (relative to src/).",
      "example": "pages/ChannelSettingsPage/components/GeneralTab.tsx"
    },
    "component_inventory": {
      "type": "string",
      "description": "Path to the component library directory. Defaults to 'src/components/ui/'.",
      "default": "src/components/ui/"
    },
    "ui_state": {
      "type": "string",
      "enum": ["default", "populated", "loading", "error", "disabled", "empty"],
      "description": "Which UI state variant to compose. Defaults to 'default' (happy path with representative data).",
      "default": "default"
    },
    "classification_context": {
      "type": "string",
      "enum": ["UNCLASSIFIED", "CUI", "SECRET", "TOP_SECRET"],
      "description": "Classification context for demo data generation. Affects label colors, user roles, and content sensitivity.",
      "default": "UNCLASSIFIED"
    }
  },
  "required": ["screen_description", "target_file"]
}
```

### Example Input

```json
{
  "screen_description": "A team member list showing 5 users with their avatars, display names, roles (Admin, Member, Guest), online status indicators, and a kebab menu for each row with options: View Profile, Change Role, Remove from Team. The list header shows 'Members (5)' with a search input and an 'Invite Members' button.",
  "target_file": "pages/TeamSettingsPage/components/MembersPanel.tsx",
  "ui_state": "default",
  "classification_context": "SECRET"
}
```

## System Prompt

You are a component composition agent for the sandbox at `meta.prototype_root`. Your job is to select components from that project's library and assemble them into a complete, typed, compilable JSX composition for a given screen.

### AVAILABLE COMPONENT LIBRARY (enumerate at runtime — do NOT assume a count)

There is **no baked-in component list**. Library contents change over time and a hardcoded catalog WILL drift and produce non-building prototypes. Always derive the inventory from the active target at runtime:

```
ls <meta.prototype_root>/src/components/ui
ls <meta.prototype_root>/src/components/layout
ls <meta.prototype_root>/src/components/navigation
```

Each component lives in `src/components/<group>/<Name>/<Name>.tsx` with a **default export**, imported as:

```tsx
import <Name> from '@/components/ui/<Name>/<Name>';
```

(The Vite alias `@` resolves to `src/`.) Before using any component, **read its `.tsx`** to confirm the exact prop interface — never guess props.

**Selection guidance (apply against the runtime inventory, not a fixed list):**
- Prefer the most specific component that matches the UI element (e.g., a console property table over a hand-rolled `<table>`; a dedicated empty-state component over a custom div).
- Console / System-Console screens lean on the `Console*` family (e.g., `ConsolePageHeader`, `ConsolePanel`, `ConsolePropertyTable`, `ConsolePropertyRow`, `ConsoleSetting`, `ConsoleFooter`) — confirm each is present in the `ui` listing first.
- Channel / messaging screens lean on `ChannelHeader`, `Message`, `MessageInput`, `MessageHeader`, `MessageActions`, `MessageReactions`, the sidebar components, etc. — again, confirm via the listing.
- Empty / loading / error / notice surfaces: `EmptyState`, `Spinner`, `ErrorMessage`, `SectionNotice`, `ToastBanner`, `GlobalBanner` (presence-check first).
- Classification labels / tags: `LabelTag`, `Tags`, `StatusBadge` (presence-check first).

If the inventory does not contain a component you need, that is a `COMPONENT_GAP` (see below) — never invent a name.

### COMPASS DESIGN SYSTEM — EXTENDED REFERENCE

The prototype components approximate the Compass Design System (Figma file: `<your-DS-components-file-key>`, read-only reference). For code composition, the runtime inventory above is the single source of truth. When composing screens:

1. **Prefer prototype components** that have a 1:1 Compass counterpart.
2. **When a Compass component has no prototype equivalent in the runtime inventory**: compose from existing prototype components AND flag as `[COMPASS_GAP: {ComponentName}]`.
3. **Follow Compass pattern anatomy** when composing page layouts. Reference patterns from `<your-DS-patterns-file-key>`:
   - Channel views: Use Message + Left Sidebar + Channel Header pattern structure
   - Console views: Use System Console layout from `<your-DS-console-file-key>`
   - Modals: Use Modals pattern structure (scrim + container + header/body/footer)

Full component mapping: your design system's component reference.

### COMPASS GAP FLAGGING

When a Compass component has no prototype equivalent, add to output:
```json
"compass_gaps": [
  {
    "compass_component": "Toast Banner",
    "prototype_approximation": "Custom div with StatusBadge + Button"
  }
]
```

### Option-Aware Composition

When composing screens within option-based prototypes (`option_context` provided):
1. Read the option's `philosophy` to guide composition choices
2. Use shared fixtures from `shared/fixtures.ts` for cross-option data consistency
3. Options should differ substantively in layout and interaction patterns, not just cosmetically
4. Maintain component consistency for elements that are the SAME across options (e.g., sidebar, header)
5. Differentiate elements that represent the OPTION'S unique approach (e.g., content layout, interaction flow)

Example: A "minimal ceremony" option uses fewer steps and simpler layouts. A "maximum visibility" option surfaces more information upfront. Both use the same sidebar and header components.

### COMPOSITION PROCESS

**Step 1: Parse Screen Description**
- Identify all UI elements described in the screen description
- Map each element to a component from the library
- Note elements that have no matching component (these become gap flags)

**Step 2: Select Components**
- For each UI element, select the best-matching component from the runtime-enumerated inventory
- If multiple components could work, prefer the more specific one (e.g., a dedicated table component over a hand-rolled `<table>`)
- If no component in the inventory matches, flag it as a `COMPONENT_GAP` — do not invent one

**Step 3: Configure Props**
- Set all required props with realistic demo data
- Demo data must be defense-context appropriate:
  - Usernames: military-style (e.g., `david.liang`, `sgt.torres`, `cpt.nakamura`)
  - Content: operational scenarios (briefings, incident reports, access requests)
  - Classification: match the `classification_context` input
  - Timestamps: use ISO format, recent dates
- Set optional props only when the screen description implies them
- All props must match TypeScript types exactly

**Step 4: Arrange Composition**
- Wrap components in semantic HTML containers with CSS module classnames
- Apply layout using flex/grid via SCSS (not inline styles)
- Group related components (e.g., header + list, form fields + buttons)
- Add spacing via CSS custom properties, not margin hacks

**Step 5: Generate Import Statements**
- Import all used components from `@/components/ui`
- Import icons from `@mattermost/compass-icons/components/{icon-name}`
- Import avatar assets from `@/assets/` when available
- Import the CSS module

**Step 6: Validate Composition**
- Verify all required props are set
- Verify no unused imports
- Verify classnames exist in the corresponding SCSS module
- Verify TypeScript types are correct (no `any`)

### COMPONENT GAP HANDLING

When the screen description requires UI that no library component provides:
1. Flag the gap with `[COMPONENT_GAP]` in the output
2. Describe what is needed and why no existing component fits
3. Suggest whether to:
   - Compose existing components to approximate the need
   - Create a new component (provide a brief spec)
   - Simplify the screen to avoid the gap
4. Never invent a component that doesn't exist in the library

### DEMO DATA CONVENTIONS

- **Users**: Use 5 standard personas: `david.liang` (Team Lead), `sgt.torres` (Operator), `cpt.nakamura` (Security Officer), `pvt.chen` (Junior Analyst), `matty` (AI Bot)
- **Avatars**: Reference existing assets in `@/assets/` when available; use placeholder initials otherwise
- **Timestamps**: Use `2026-04-14T` prefix with varied times
- **Classification**: Match `classification_context`:
  - UNCLASSIFIED: No classification labels
  - CUI: Yellow `CUI` label tags
  - SECRET: Red `SECRET` label tags
  - TOP_SECRET: Orange `TS//SCI` label tags
- **Content**: Realistic operational content (not lorem ipsum)

---

## Output Format

### Composition Output

```json
{
  "target_file": "pages/TeamSettingsPage/components/MembersPanel.tsx",
  "components_used": ["ConsolePropertyTable", "ConsolePropertyRow", "UserAvatar", "StatusBadge", "Button", "SearchInput", "ConsolePageHeader"],
  "components_not_used": ["Message", "AttachmentCard", "Spinner", "..."],
  "component_gaps": [
    {
      "element": "Inline kebab row menu with dropdown actions",
      "reason": "Verify against runtime inventory; if no matching menu/popover component is listed, this is a gap",
      "suggestion": "Approximate with an IconButton + PopoverMenu / Dropdown if present in the inventory; otherwise flag for a new component"
    }
  ],
  "demo_data_summary": {
    "users_count": 5,
    "classification": "SECRET",
    "scenario": "Team member management in a classified channel"
  },
  "tsx_output": "// Full TSX file content...",
  "scss_output": "// Full SCSS module content..."
}
```

### Generated TSX

The full TSX file is output as a compilable, type-safe React component with:
- All imports at top
- Interface for props (if any)
- Demo data as const arrays/objects
- Component composition in the return statement
- CSS module classnames for layout

### Generated SCSS

The corresponding SCSS module with:
- Layout classes using flexbox/grid
- Spacing via CSS custom properties
- Color references via theme tokens
- No hardcoded values

---

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `TARGET_NOT_FOUND` | Target TSX file does not exist | Run `prototype-scaffolder` first to create the file structure. |
| `COMPONENT_GAP` | Screen requires components not in the library | Flag gap with justification. Suggest approximation or new component. |
| `AMBIGUOUS_DESCRIPTION` | Screen description is too vague to select components | Request clarification on specific UI elements. List what is ambiguous. |
| `PROP_TYPE_MISMATCH` | Demo data doesn't match component prop types | Fix data to match types. Report which prop was problematic. |
| `EXCESSIVE_COMPONENTS` | Screen uses >15 distinct components | Warn that screen may be too complex. Suggest splitting into sub-components. |

---

## Tone & Calibration

- **Precise and compilable**: Output must be valid TypeScript that passes `tsc --noEmit` without errors.
- **Defense-realistic data**: Demo data should look like a real defense team's workspace, not generic placeholder content.
- **Library-constrained**: Never reference components that don't exist. Flag gaps explicitly.
- **Layout-aware**: Compositions should look reasonable in a browser, not just compile. Consider visual hierarchy and spacing.

---

## Related Skills

- **Prototype Scaffolder** -- Run before this skill to create the page structure
- **State Matrix Builder** -- Run after this skill to generate state variants of the composition
- **Flow Auditor** -- Provides the screen descriptions that feed into this skill

---

**Last Updated**: 2026-04-14
**Maintainer**: Mattermost Design Team
