---
name: settings-system
description: "The Matrx user settings system (SettingsShell, useSetting, tab registry). Use when adding a preference or settings tab, binding a Redux slice to settings, wiring a settings deep link, or touching features/settings, components/official/settings, or components/user-preferences."
---

# Settings System

> **Feature doc:** `features/settings/FEATURE.md` — architecture source of truth. Start there for slice map, flows, and invariants.

Everything user-configurable flows through one system: a `SettingsShell` mounted via `WindowPanel` on desktop / Vaul drawer on mobile, backed by a registry of tabs that compose exactly one primitives library and read/write state only via `useSetting`.

**Reference implementations:**
- `features/settings/tabs/MessagingTab.tsx` — canonical tab (switches + slider + conditional rendering + browser permission).
- `features/settings/tabs/AppearanceTab.tsx` — crosses two slices (theme + userPreferences).
- `features/settings/tabs/WindowsTab.tsx` — action-only writes + live read-only status.
- `features/settings/tabs/EmailTab.tsx` — API-backed tab (the escape hatch).

---

## Golden rules

1. **Primitives own their layout.** No `className` prop anywhere in the primitives library. Variations are new enum values on existing props.
2. **Tabs compose only primitives.** Zero `@/components/ui/*` imports, zero `useSelector`/`useAppDispatch` for writable values. Read-only selectors are acceptable for derived state (see `WindowsTab`).
3. **`useSetting(path)` is the only write path.** Unless the underlying slice has no `write` binding yet (new feature day one) — then add a binding to `features/settings/slice-bindings.ts`.
4. **Tabs are lazy.** Every registry entry uses `lazyTab(() => import("./tabs/XYZ"))`. Never static-import a tab.
5. **Icons are Lucide.** No emojis in settings UI ever.
6. **Every tab works on mobile.** No `className="hidden md:..."`. The primitives are already mobile-ready; don't bypass them.
7. **A knob is not a preference.** Anything the platform or an org governs is a `platform.feature_knob` row rendered through `features/settings/universal`, never a slice and never a `UserPreferences` field. If you are about to add a threshold, ceiling, mode or policy to `defaultPreferences.ts`, stop — that is a knob.
8. **Admin gating is declarative.** Add `requiresAdmin: true` to the registry entry — the tree hides it, `getVisibleTabs(isAdmin)` filters it, and the shell passes `isAdmin` down automatically.

---

## Decision tree — "I want to add a setting"

🚨 **FIRST BRANCH — is this a PREFERENCE or is it CONFIGURATION?** This question comes before
every question below it, and getting it wrong is the most common mistake in this system. The tree
that follows is for *preferences*: things that belong to the person using the app. Anything the
platform or an organization governs is a **knob**, lives in `platform.feature_knob`, and never
becomes a Redux slice or a `UserPreferences` field.

```
Is the value governed by the PLATFORM or by an ORGANIZATION?
  (a limit, quota, ceiling, timeout, threshold, retry/batch size, mode, strategy,
   policy, or ANY behavioral choice someone other than this user should decide)
  Yes → it is a KNOB, not a setting. Seed a platform.feature_knob row and render it
        through features/settings/universal (KnobFieldControl / KnobRungOverrides).
        Then make the SECOND decision — who may override it — and default to NOBODY:
        overridable_by = '{}' is platform-locked and is a first-class answer.
        Law: common-docs/policies/limits-are-knobs-agents-set-them.md
        Machine: common-docs/systems/platform/feature-knobs/FEATURE.md
  No, it is genuinely this person's own preference ↓

Does the value already live in a registered slice?
  Yes → call `useSetting("slice.dotted.key")` from your tab. DONE.
  No  ↓

Is the value new but conceptually a "user preference"?
  Yes → extend `UserPreferences` in `lib/redux/slices/userPreferencesSlice.ts`:
        • add the field to the right module interface
        • add a default in `lib/redux/slices/defaultPreferences.ts`
        • call `useSetting("userPreferences.<module>.<field>")`.
        (The warm-cache sync policy handles IDB + localStorage + Supabase.)
  No  ↓

Is it genuinely new state (theme-ish, window-ish, feature-flag-ish)?
  Yes → create a slice where it belongs. Then add a binding in
        `features/settings/slice-bindings.ts` with `{ read, write, persistence }`.
        Flag persistence honestly:
          • "synced"     — backed by a sync policy (IDB + LS + Supabase)
          • "local-only" — Redux only, survives session but NOT reload
          • "session"    — transient; cleared on reload
```

### What about `/api/*` endpoints that aren't in Redux?

See `EmailTab.tsx`. Use local `useState` + `useEffect(fetch)`, compose primitives as usual, flag `persistence: "local-only"` in the registry entry until the API is migrated behind a slice+sync policy. Leave a TODO comment pointing to the migration.

---

## Recipe — "Add a new settings tab"

Five files max. Usually three.

### Step 1 — Build the tab

`features/settings/tabs/MyTab.tsx`:

```tsx
"use client";

import { Sparkles } from "lucide-react";
import {
  SettingsSwitch,
  SettingsSlider,
  SettingsSection,
  SettingsSubHeader,
} from "@/components/official/settings";
import { useSetting } from "../hooks/useSetting";

export default function MyTab() {
  const [enabled, setEnabled] = useSetting<boolean>("userPreferences.myModule.enabled");
  const [level, setLevel]     = useSetting<number>("userPreferences.myModule.level");

  return (
    <>
      <SettingsSubHeader title="My feature" description="Short description." icon={Sparkles} />
      <SettingsSection title="Behaviour">
        <SettingsSwitch label="Enable X" checked={enabled} onCheckedChange={setEnabled} />
        <SettingsSlider
          label="Level"
          value={level}
          onValueChange={setLevel}
          min={0}
          max={10}
          step={1}
          last
        />
      </SettingsSection>
    </>
  );
}
```

### Step 2 — Register it

`features/settings/registry.ts`:

```ts
const MyTab = lazyTab(() => import("./tabs/MyTab"));

export const settingsRegistry: SettingsTabDef[] = [
  // ...existing entries
  {
    id: "general.myFeature",          // dotted — matches parentId.child
    label: "My feature",
    icon: Sparkles,                   // Lucide only
    parentId: "general",              // attaches under the General category
    description: "Short tooltip/description.",
    searchKeywords: ["x", "toggle"],  // improves search hits
    component: MyTab,
    persistence: "synced",
  },
];
```

### Step 3 — Done

The tree picks it up. Search picks it up. Admin gating picks it up (no `requiresAdmin` → visible to everyone). Mobile push-nav picks it up. Breadcrumb picks it up.

### Step 4 — (Optional) Add a slice binding if you used a brand-new slice

`features/settings/slice-bindings.ts`:

```ts
export const sliceBindings: Record<string, SliceBinding> = {
  // ...existing bindings
  myFeature: {
    read: (state, key) => readDotted(state.myFeature, key),
    write: (key, value) => {
      if (key === "enabled") return myFeatureSlice.actions.setEnabled(Boolean(value));
      if (key === "level")   return myFeatureSlice.actions.setLevel(Number(value));
      throw new Error(`myFeature has no writable key "${key}"`);
    },
    persistence: "synced",           // or "local-only" / "session"
  },
};
```

---

## Primitive catalog

Every primitive accepts the same base props via `SettingsCommonProps`:

```ts
type SettingsCommonProps = {
  label: string;                     // required
  description?: ReactNode;
  warning?: ReactNode;               // amber, inline below description
  error?: ReactNode;                 // red, inline below description
  badge?: SettingsBadge;             // {label,variant} — default|new|beta|experimental|deprecated|admin
  icon?: LucideIcon;                 // left of the label
  disabled?: boolean;
  modified?: boolean;                // blue dot indicator
  id?: string;                       // auto from label if omitted
  helpText?: ReactNode;              // tooltip via HelpCircle
};
```

Plus `last?: boolean` on every row primitive (removes trailing border — use on the final row in a `SettingsSection`).

### Form primitives

| Primitive | Use for | Key control props |
|---|---|---|
| `SettingsSwitch` | App-level boolean toggle | `checked`, `onCheckedChange` |
| `SettingsCheckbox` | Consent / opt-in | `checked`, `onCheckedChange` |
| `SettingsSelect<T>` | Enum dropdown | `value`, `onValueChange`, `options[]`, `size`, `width`, `stacked` |
| `SettingsSegmented<T>` | 2–4 mutually exclusive | `value`, `onValueChange`, `options[]`, `size`, `fullWidth` |
| `SettingsRadioGroup<T>` | 2–5 rich-option cards | `value`, `onValueChange`, `options[]`, `orientation` |
| `SettingsSlider` | Numeric range | `value`, `onValueChange`, `min`, `max`, `step`, `precision`, `unit`, `minLabel`, `midLabel`, `maxLabel` |
| `SettingsNumberInput` | Exact numeric | `value`, `onValueChange`, `min`, `max`, `step`, `integer`, `unit`, `size`, `width` |
| `SettingsTextInput` | Single-line text | `value`, `onValueChange`, `type`, `commitOnBlur`, `maxLength`, `size`, `width`, `stacked` |
| `SettingsTextarea` | Multi-line text | `value`, `onValueChange`, `rows`, `maxLength`, `commitOnBlur`, `showCount` |
| `SettingsColorPicker` | Color hex | `value`, `onValueChange`, `presets[]` |
| `SettingsMultiSelect<T>` | Tag-style multi-pick | `value`, `onValueChange`, `options[]`, `max`, `countOnly` |
| `SettingsButton` | Action | `actionLabel`, `onClick`, `kind`, `size`, `actionIcon`, `loading`, `stacked` |
| `SettingsLink` | External link / route | `href`, `actionLabel`, `external` |
| `SettingsKeybinding` | Shortcut capture | `value: KeybindingValue \| null`, `onValueChange`, `clearable` |
| `SettingsModelPicker` | AI model from registry | `value`, `onValueChange`, `scope: "all"\|"active"\|"inactive"` |

### Layout primitives

| Primitive | Use for | Key props |
|---|---|---|
| `SettingsSubHeader` | Top-of-tab title | `title`, `description`, `icon`, `divider` |
| `SettingsSection` | Titled group of rows | `title`, `description`, `icon`, `collapsible`, `defaultOpen`, `emphasis`, `action` |
| `SettingsCallout` | Info / warning / error / success banner | `tone`, `title`, `children`, `action` |
| `SettingsGrid` | 2- or 3-col dense layout | `columns`, `gap` |
| `SettingsReadOnlyValue` | Key/value info row | `value`, `copyable`, `mono` |

---

## Anti-patterns

❌ **Passing `className` to a primitive**
```tsx
<SettingsSwitch className="my-4" ... />   // WRONG — primitives don't accept className
```
✅ If you need spacing, use a `SettingsSection`. If you need a new variant, add a prop to the primitive.

❌ **Direct Redux dispatch in a tab**
```tsx
const dispatch = useAppDispatch();
dispatch(setPreference({ module: "prompts", preference: "temperature", value }));   // WRONG
```
✅ `const [temperature, setTemperature] = useSetting("userPreferences.prompts.defaultTemperature")`.

❌ **Importing shadcn in a tab**
```tsx
import { Switch } from "@/components/ui/switch";   // WRONG
```
✅ `import { SettingsSwitch } from "@/components/official/settings";`

❌ **Ad-hoc row divs**
```tsx
<div className="flex items-center justify-between px-4 py-3.5 border-b">
  <Label>…</Label>
  <Switch />
</div>                                                // WRONG
```
✅ `<SettingsSwitch label="…" checked={…} onCheckedChange={…} />`

❌ **Hardcoding colors**
```tsx
<div className="bg-blue-500 text-white">…</div>       // WRONG
```
✅ `<SettingsCallout tone="info">…</SettingsCallout>` or use design tokens (`bg-primary`, `text-foreground`, etc.).

❌ **Adding category-only entries without a `parentId`-less root**
```ts
{ id: "foo.child", label: "Child", parentId: "foo", ... }   // child only — orphan!
// Missing:
// { id: "foo", label: "Foo", ... }                         // category parent
```
✅ Every `parentId` must refer to an existing registry entry. Orphans are silently promoted to roots (bad UX).

❌ **Treating `persistence` as decorative**
It drives the badge in the shell and signals migration work. Be honest:
- `"synced"` only when an actual sync policy handles the slice.
- `"local-only"` when the value lives in Redux only and survives the session.
- `"session"` when reload wipes it.

---

## Path syntax for `useSetting`

`useSetting<T>("slice.rest.of.key")` — the first segment selects the slice binding, everything after is passed to that binding's `read`/`write`.

| Slice | Path shape | Example |
|---|---|---|
| `userPreferences` | `userPreferences.<module>.<preference>` | `userPreferences.messaging.notificationVolume` |
| `theme` | `theme.<key>` | `theme.mode` |
| `adminPreferences` | `adminPreferences.<key>` | `adminPreferences.serverOverride` |
| `layout` | `layout.<key>` | `layout.layoutStyle` |
| `windowManager` | `windowManager.<action>` (write-only keys) | `windowManager.toggleHidden`, `windowManager.restoreAll` |

---

## Mobile parity

Do nothing special. `SettingsShell` flips to `SettingsDrawerNav` under `useIsMobile()`. The push-nav renders each tab through `SettingsTabHost`. Because every tab is built from primitives, touch targets, `text-base` input font-size, and `pb-safe` are already correct.

Never:
- Add a mobile-only branch inside a tab.
- Render a `<Tabs>` component inside a settings tab (stack vertically instead).
- Use `h-screen` / `min-h-screen` inside a tab (primitives + shell handle viewport already).

---

## Deep-linking + the legacy URL

- `?panels=user_preferences` → `initUrlHydration` opens the overlay.
- `/settings/preferences?tab=<legacy>` → redirects to `/dashboard` AND dispatches the overlay with the legacy tab id remapped (see `LEGACY_TAB_ALIASES`).
- The overlay id on the receiving side is always `userPreferencesWindow`. The modal id `userPreferences` is a legacy alias the adapter also listens for.

If you add a new tab with an alternate "short" id for external deep-linking, add it to:
1. `SettingsShellOverlay.LEGACY_TAB_MAP` — overlay data mapping.
2. `app/(authenticated)/settings/preferences/page.tsx` → `LEGACY_TAB_ALIASES` — URL query mapping.

---

## Checklist — before you open a PR

- [ ] Every new row is composed from primitives in `@/components/official/settings`.
- [ ] Tab file contains no `@/components/ui/*` import.
- [ ] Tab file contains no `useAppDispatch` / `setPreference` / direct Redux write.
- [ ] No `className` prop passed to any primitive.
- [ ] Registry entry added with `id`, `label`, Lucide `icon`, `parentId` if nested, `component: lazyTab(...)`, honest `persistence`.
- [ ] Any new slice has a binding in `features/settings/slice-bindings.ts`.
- [ ] FEATURE.md Change log updated if you added/removed a tab or slice binding.
- [ ] Verified on `http://localhost:3000/settings-shell-demo` (desktop) AND at mobile viewport width.

---

## When this skill does NOT apply

- Per-agent settings (`features/agents/components/settings-management/*`) — that's context-aware agent config, not user preferences. Separate system, separate skill.
- Profile / Organization / Team pages (`app/(authenticated)/settings/profile`, `/organizations`, …) — they're route-based pages, not preference tabs.
- Anything inside `app/(authenticated)/admin/*` that manages platform config.
