---
name: standardize-panel
description: Migrate any left-panel to the Cinema panel standard — animated tab bar, always-visible search, filter icon toggle, thick rows, blue accent. Use when standardizing existing panels or building new ones.
argument-hint: <PanelName>
---

# Standardize Panel to Cinema Pattern

Migrate a left-sidebar panel to the unified Cinema panel standard. All preset-browsing panels should follow this pattern for UX consistency.

## The Standard

Every standardized panel follows this structure:

```
┌─────────────────────────────────┐
│ [Tab1] [Tab2] [Tab3]           │ ← animated icon tab bar (if multi-tab)
├─────────────────────────────────┤
│ [🔍 Search presets...] [⚙] [?] │ ← always-visible search + filter icon + optional extras
├─────────────────────────────────┤
│ PanelCategoryTabs + controls   │ ← shown when filter icon toggled (hidden by default)
├─────────────────────────────────┤
│ ┌ None ───────────────────┐    │ ← "None" row (Ban icon) for disable/deselect
│ └─────────────────────────┘    │
│ ┌ Preset Name ────── tag ─┐    │ ← thick rows (scrollable body)
│ │ Description text         │    │
│ └─────────────────────────┘    │
│ ...                             │
├─────────────────────────────────┤
│ [Footer action button]         │ ← optional fixed footer
└─────────────────────────────────┘
```

## Shell Template

```tsx
import { useState, useMemo } from 'react'
import { Search, SlidersHorizontal, Ban } from 'lucide-react'
import { PanelCategoryTabs } from '@/components/ui/panel-controls'
import { cn } from '@/lib/utils'

const TABS = [
  { id: 'tab1', label: 'Tab 1', icon: Icon1 },
  { id: 'tab2', label: 'Tab 2', icon: Icon2 },
] as const
type TabId = (typeof TABS)[number]['id']

const CATEGORIES = [
  { id: 'all', label: 'All' },
  { id: 'cat1', label: 'Category 1' },
  // ...
]

export function MyPanel() {
  const [activeTab, setActiveTab] = useState<TabId>('tab1')
  const [search, setSearch] = useState('')
  const [filtersOpen, setFiltersOpen] = useState(false)
  const [categoryFilter, setCategoryFilter] = useState('all')

  const q = search.toLowerCase().trim()

  const filtered = useMemo(() => {
    let result = PRESETS
    if (categoryFilter !== 'all') result = result.filter(p => p.category === categoryFilter)
    if (q) result = result.filter(p => p.name.toLowerCase().includes(q))
    return result
  }, [categoryFilter, q])

  return (
    <div className="flex flex-col h-full overflow-hidden">
      {/* ── Animated Icon Tab Bar ── */}
      <div className="shrink-0 flex items-center gap-1 px-3 py-2 border-b border-white/5">
        {TABS.map((tab) => {
          const isActive = activeTab === tab.id
          const Icon = tab.icon
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              title={tab.label}
              style={{
                flex: isActive ? 2 : 1,
                transition: 'flex 300ms cubic-bezier(0.25, 1, 0.5, 1), background-color 200ms, color 200ms, padding 200ms',
              }}
              className={cn(
                'relative h-8 rounded-lg flex items-center justify-center gap-1.5 overflow-hidden',
                isActive ? 'bg-white text-black px-2' : 'text-gray-400 hover:text-white hover:bg-[#2a2a2a]',
              )}
            >
              <Icon size={16} className="shrink-0" />
              <span
                style={{ transition: 'max-width 300ms cubic-bezier(0.25, 1, 0.5, 1) 50ms, opacity 200ms ease 60ms' }}
                className={cn('text-[11px] font-medium truncate', isActive ? 'max-w-[80px] opacity-100' : 'max-w-0 opacity-0')}
              >
                {tab.label}
              </span>
            </button>
          )
        })}
      </div>

      {/* ── Search + Filter Toggle ── */}
      <div className="shrink-0 px-3 py-2">
        <div className="flex items-center gap-1.5">
          <div className="relative flex-1">
            <Search size={14} className="absolute left-2.5 top-1/2 -translate-y-1/2 text-zinc-500" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search presets..."
              className="w-full pl-8 pr-3 py-2 bg-zinc-800 rounded-lg text-sm text-zinc-200 placeholder-zinc-600 border border-white/5 focus:border-[#4a7eff]/30 focus:outline-none"
            />
          </div>
          <button
            onClick={() => setFiltersOpen(!filtersOpen)}
            className={cn(
              'shrink-0 w-8 h-8 rounded-lg flex items-center justify-center transition-colors relative',
              filtersOpen ? 'bg-[#4a7eff]/20 text-[#4a7eff]' : 'text-zinc-500 hover:text-zinc-200 hover:bg-[#2a2a2a]',
            )}
          >
            <SlidersHorizontal size={14} />
            {categoryFilter !== 'all' && (
              <span className="absolute -top-0.5 -right-0.5 w-2 h-2 rounded-full bg-[#4a7eff]" />
            )}
          </button>
        </div>
      </div>

      {/* ── Filter panel (hidden by default) ── */}
      {filtersOpen && (
        <div className="shrink-0 px-3 pb-2">
          <PanelCategoryTabs
            tabs={CATEGORIES}
            activeTab={categoryFilter}
            onChange={(id) => setCategoryFilter(id)}
            compact
          />
        </div>
      )}

      {/* ── Scrollable content ── */}
      <div className="flex-1 overflow-y-auto px-3 py-2">
        {filtered.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-16 text-gray-600">
            <TabIcon size={28} className="mb-3" />
            <span className="text-sm text-gray-400">No presets found</span>
            <span className="text-xs text-gray-600 mt-1">Try a different keyword</span>
          </div>
        ) : (
          <div className="space-y-1">
            {/* None row */}
            <button
              onClick={() => handleDisable()}
              className={cn(
                'w-full px-3 py-2.5 rounded-lg text-left transition-colors border flex items-center gap-2',
                isDisabled ? 'bg-[#4a7eff]/10 border-[#4a7eff]/30' : 'bg-[#2a2a2a] border-white/5 hover:bg-[#3a3a3a]',
              )}
            >
              <Ban size={14} className="shrink-0 text-gray-500" />
              <div>
                <div className="text-xs font-medium text-gray-200">None</div>
                <div className="text-[9px] text-gray-500 mt-0.5">Disabled</div>
              </div>
            </button>
            {/* Preset rows */}
            {filtered.map((preset) => (
              <button
                key={preset.id}
                onClick={() => handleSelect(preset)}
                className={cn(
                  'w-full px-3 py-2.5 rounded-lg text-left transition-colors border',
                  isActive(preset) ? 'bg-[#4a7eff]/10 border-[#4a7eff]/30' : 'bg-[#2a2a2a] border-white/5 hover:bg-[#3a3a3a]',
                )}
              >
                <div className="text-xs font-medium text-gray-200">{preset.name}</div>
                <div className="text-[9px] text-gray-500 mt-0.5">{preset.description}</div>
              </button>
            ))}
          </div>
        )}
      </div>

      {/* ── Optional footer ── */}
      <div className="shrink-0 px-3 py-2 border-t border-white/5">
        <button className="w-full flex items-center justify-center gap-2 py-2 rounded-lg text-[11px] font-medium ...">
          Footer Action
        </button>
      </div>
    </div>
  )
}
```

## Design Tokens

| Token | Value | Used for |
|-------|-------|----------|
| Active bg | `bg-[#4a7eff]/10` | Selected preset row |
| Active border | `border-[#4a7eff]/30` | Selected preset row |
| Filter active | `bg-[#4a7eff]/20 text-[#4a7eff]` | Filter icon when open |
| Blue dot | `bg-[#4a7eff]` | Filter active indicator |
| Row bg | `bg-[#2a2a2a]` | Default preset row |
| Row hover | `hover:bg-[#3a3a3a]` | Row hover state |
| Row border | `border-white/5` | Default row border |
| Section divider | `border-white/5` | Between header/body/footer |
| Tab active | `bg-white text-black` | Active tab |
| Tab inactive | `text-gray-400` | Inactive tab |
| Tab bar animation | `cubic-bezier(0.25, 1, 0.5, 1)` | Flex expansion |

## Decision Guide

### Tabs or no tabs?

- **2-3 distinct browsing modes** → Use animated tab bar (Cinema, MixedMedia, AnimStyle)
- **Single-purpose panel** → No tab bar, just search + filter (Transitions)
- **4+ tabs** → Too many. Split into separate panels or group more tightly.

### Thick rows or visual grid?

- **Text-heavy presets** (name + description) → Thick rows (`space-y-1`, full-width buttons)
- **Preview-heavy content** (transitions, thumbnails) → 2-col grid (`grid-cols-2 gap-2`)
- Rule: if users need to SEE it to understand it, use grid. If they can READ it, use rows.

### Browser or workflow?

- **Browser** = tabs + search + rows/grid. User browses and picks. (Cinema, MixedMedia, AnimStyle, Transitions)
- **Workflow** = sequential steps (upload → configure → process → result). (VideoStyleTransfer)
- **Never mix** browsers and workflows in the same panel. Extract workflows to their own panel.

### Filter area contents

- Always: `PanelCategoryTabs` for category filtering
- Optional: domain-specific controls (PanelSlider for opacity/intensity) below categories
- Keep it compact — this area should collapse cleanly

### "None" row rules

- Always the first item in the list
- Uses `Ban` icon from lucide-react
- Click disables the feature / clears the selection
- Active when nothing is selected or feature is disabled
- No toggle behavior on preset rows — clicking always selects. "None" is the only way to deselect.

## Migration Checklist

When converting an existing panel:

1. [ ] Remove `PanelLayout` import and wrapper
2. [ ] Remove `PanelSection` wrappers (sections become tabs or inline content)
3. [ ] Remove custom glass/card wrappers (backdrop-blur, shadow-inner, etc.)
4. [ ] Add `flex flex-col h-full overflow-hidden` shell
5. [ ] Add animated tab bar (if multi-mode panel)
6. [ ] Add always-visible search input
7. [ ] Add SlidersHorizontal filter icon with blue dot indicator
8. [ ] Move category filters behind filter toggle using `PanelCategoryTabs`
9. [ ] Convert grid layouts to thick rows (unless preview-heavy)
10. [ ] Add "None" row with Ban icon
11. [ ] Change accent color to blue (`#4a7eff`) if using green or other
12. [ ] Add empty state (centered icon + text)
13. [ ] Move `overflow-y-auto` to body div only (not outer shell)
14. [ ] Verify no workflow UX is mixed with browser UX — extract if needed

## Reference Panels

| Panel | Tabs | Content | Has filter? | Has footer? |
|-------|------|---------|-------------|-------------|
| CinemaStudioPanel | 3 (Quick/Genre/Cinema) | Thick rows | Yes (per-tab categories) | Yes (Camera Settings) |
| MixedMediaPanel | 2 (Overlays/Styles) | Thick rows | Yes (categories + slider) | No |
| AnimStylePanel | 2 (Presets/Custom) | Rows + sliders | No (search only) | Yes (Apply Style) |
| TransitionsPanel | None | 2-col visual grid | Yes (categories) | Yes (hint text) |
| VideoStyleTransferPanel | None | Workflow (upload→process) | No | No |
