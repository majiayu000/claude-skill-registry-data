---
name: sheet-ui-redesign
description: Redesigns character sheet display components to match the character creation card aesthetic. Use when updating any component in /components/character/sheet/ to use grouped sections, value pills, and the established dark-mode-first color system.
allowed-tools: Read, Grep, Glob, Edit, Write
user-invocable: true
---

# Character Sheet Component UI Redesign

Guides the redesign of character sheet display components to match the polished creation card aesthetic established in AttributesDisplay and SkillsDisplay.

## Process

When invoked with a component name (e.g., `/sheet-ui-redesign MagicDisplay`):

1. **Read the target component** to understand its current structure and data
2. **Read the canonical examples** for pattern reference:
   - `components/character/sheet/AttributesDisplay.tsx` — grouped sections, value pills, augmentation indicators, semantic colors
   - `components/character/sheet/SkillsDisplay.tsx` — grouped sections, value pills, specialization pills
3. **Read the target's test file** in `components/character/sheet/__tests__/`
4. **Identify the logical groupings** for the component's data
5. **Apply the patterns below** to redesign the component
6. **Update tests** to match the new markup

## Layout: Flat Structure → Grouped Sections

Replace any flat `<table>`, plain `<ul>`, or single-column list with logical groupings appropriate to the data (e.g., by category, type, or domain meaning). Each group has:

- **Section label:** `text-[10px] font-semibold uppercase tracking-wider text-zinc-500`
- **Sunken container** (one level deeper than card background):
  - Light: `bg-zinc-50 border border-zinc-200 rounded-lg`
  - Dark: `dark:bg-zinc-950 dark:border-zinc-800`
- Sections arranged with `flex flex-col gap-3` (or `gap-4` for wider components)

## Item Rows

Each data row uses a flex layout with label left, value right:

- **Row layout:** `flex items-center justify-between px-3 py-1.5`
- **Label text:** `text-[13px] font-medium text-zinc-800 dark:text-zinc-200`
- **Value pill:** mono font, centered in a rounded container
  - Neutral: `bg-zinc-200 text-zinc-900 dark:bg-zinc-800 dark:text-zinc-50`
  - Size: `min-w-[32px] h-7 rounded-md`, `font-mono font-bold text-[13px]`
- **Row hover:** `hover:bg-zinc-100 dark:hover:bg-zinc-700/30`
- **Row separators:** `[&+&]:border-t border-zinc-200 dark:border-zinc-800/50` (sibling borders, no first-row border)

### Choosing a Row Pattern

Pick the simplest pattern that fits the item's data complexity:

| Pattern            | When to use                                              | Example components                        |
| ------------------ | -------------------------------------------------------- | ----------------------------------------- |
| **Simple row**     | Scalar data, 1-2 values (name + rating)                  | ContactsDisplay, AdeptPowersDisplay       |
| **Expandable row** | Rich detail: summaries, effects, dynamic state, settings | QualitiesDisplay                          |
| **Hover-reveal**   | Single modifier/indicator on an otherwise simple row     | AttributesDisplay (augmentation tooltips) |

Default to simple rows. Only introduce expandable rows when an item has 3+ distinct detail fields that clutter the collapsed view.

## Expandable Rows

For items with rich detail content, use the chevron-driven expand/collapse pattern (established in QualitiesDisplay, follows GearRow from creation cards):

### State & Gating

```tsx
const [isExpanded, setIsExpanded] = useState(false);
const hasExpandableContent = /* check if any detail fields exist */;
```

### Collapsed Row (always visible)

Clickable row showing **name only** plus critical status indicators (e.g., pending badge):

```tsx
<div className="flex cursor-pointer items-center gap-1.5"
     onClick={() => setIsExpanded(!isExpanded)}>
  {hasExpandableContent ? (
    <button data-testid="expand-button"
            className="shrink-0 text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-300">
      {isExpanded ? <ChevronDown className="h-3.5 w-3.5" />
                   : <ChevronRight className="h-3.5 w-3.5" />}
    </button>
  ) : (
    <div className="w-3.5 shrink-0" />  {/* alignment spacer */}
  )}
  <span className="truncate text-[13px] font-medium text-zinc-800 dark:text-zinc-200">
    {name}
  </span>
  {/* Only critical inline badges here (e.g., pending approval) */}
</div>
```

### Expanded Section (conditional)

Indented container with left border accent, containing detail sub-sections:

```tsx
{
  isExpanded && hasExpandableContent && (
    <div
      data-testid="expanded-content"
      className="ml-5 mt-2 space-y-2 border-l-2 border-zinc-200 pl-3 dark:border-zinc-700"
    >
      {/* Detail rows: extra info chips, value pills, summaries, effect badges, etc. */}
    </div>
  );
}
```

### Key Rules

- **Collapsed = name only.** Move all value pills, summaries, effect badges, and action buttons into the expanded section.
- **No hover-reveal actions** on expandable rows — use the expanded section instead.
- **Critical status** (e.g., pending badge) stays inline in the collapsed row for at-a-glance visibility.
- **Import** `ChevronDown`, `ChevronRight` from `lucide-react`.

## Semantic Color Accents

When items have distinct semantic meaning (damage types, magic traditions, special stats), assign each a color config:

| Element | Dark Mode                            | Light Mode                         |
| ------- | ------------------------------------ | ---------------------------------- |
| Icon    | `{color}-500` (or `-400` for light)  | `{color}-600`                      |
| Label   | one shade lighter than icon (`-400`) | `{color}-700`                      |
| Pill bg | `{color}-500/15` (or `-400/12`)      | `bg-{color}-50 border-{color}-200` |

Established palette: `amber`, `emerald`, `cyan`, `purple`, `sky`, `rose`, `orange`. Prefer colors already used in AttributesDisplay before introducing new ones.

## Secondary/Modifier Indicators

When items have modifiers, bonuses, or secondary values:

- **Only render when value > 0** — no empty brackets or zero indicators
- **Positive modifier pill:** `bg-emerald-500/15 text-emerald-400`, mono `text-[11px] font-semibold`, shows `+N` with directional icon (10px)
- **Modified main pill:** swap neutral for tinted: `bg-emerald-500/12 text-emerald-300 border border-emerald-500/20`
- **Negative modifiers:** use `rose` instead of `emerald`

## Tooltips & Interactive Elements

- Use `<TooltipTrigger>` + `<Tooltip>` from `react-aria-components` for detail popups
- Trigger must be a focusable element (`<Button>` from `react-aria-components`)
- Wrap tooltip triggers in `<span onClick={e => e.stopPropagation()}>` if the row is clickable
- Tooltip content: `bg-zinc-900 border-zinc-700 rounded-lg p-2 text-[12px]`
- Multi-source tooltips: list each source, `border-zinc-600` separator + summary when >1 source

## Conditional Rendering

- Only render sections/items that have data — no empty groups
- Clickable items fire `onSelect` (or established callback)
- Display-only items get no click handler, may use wider pill (`w-12`) and custom formatting (`.toFixed(2)`)

## Testing Notes

- `vi.mock("react-aria-components")` in shared test helpers is **hoisted by vitest** — any test importing from that file gets the mock
- The shared mock must include **all** react-aria-components exports used (e.g., `Button`, `Link`, `Tooltip`, `TooltipTrigger`)
- Never use `new Proxy()` for `vi.mock("lucide-react")` — use explicit named icon exports
- Test files with JSX (even in mock factories) must use `.tsx` extension
- `ChevronDown` and `ChevronRight` are already in `LUCIDE_MOCK` in `test-helpers.tsx`

### Expandable Row Test Pattern

Tests for detail content (karma pills, summaries, effects, settings buttons) must **expand the row first**:

```tsx
function expandFirstRow() {
  const btn = screen.getAllByTestId("expand-button")[0];
  fireEvent.click(btn);
}

// Detail assertions require expansion
it("renders karma pill when expanded", () => {
  renderWith({ ... });
  expandFirstRow();
  expect(screen.getByTestId("karma-pill")).toHaveTextContent("4");
});

// Name and critical badges are visible WITHOUT expansion
it("shows name in collapsed row", () => {
  renderWith({ ... });
  expect(screen.getByText("Ambidextrous")).toBeInTheDocument();
});
```

Key test IDs: `expand-button`, `expanded-content`, `quality-row`.

New tests to include: collapsed row hides details, expand shows content, collapse hides content, chevron icon toggles between `icon-ChevronRight` and `icon-ChevronDown`.

## Canonical Examples

Always read these before starting a redesign:

```
components/character/sheet/AttributesDisplay.tsx   — grouping, value pills, aug indicators, special attr colors
components/character/sheet/SkillsDisplay.tsx        — skill group sections, rating pills, specialization pills
components/character/sheet/QualitiesDisplay.tsx     — expandable rows, chevron pattern, collapsed name-only
```
