---
name: compact-nav-menus
description: "Sizing tokens for compact sidebars, nav panels, and menu lists. Use when building or refactoring a sidebar, settings menu, category list, filter bar, or expandable nav tree, or when a sidebar looks too wide, too padded, or wastes space."
---

# Compact Navigation & Menu Panels

Canonical sizing and spacing rules for navigation sidebars, list panels, and compact menus across the project. Every value below is a hard default — deviate only with justification.

## Sizing Tokens

### Sidebar Container
| Property | Value | Notes |
|----------|-------|-------|
| Width | `w-36` to `w-44` | Never wider than `w-44` (~176px). Use `w-36`–`w-40` when labels are short. |
| Background | `bg-muted/30` | Subtle tint, not solid `bg-card`. |
| Border | `border-r border-border/60` | 60% opacity, not full `border-border`. |
| Visibility | `hidden md:flex` | Always hidden on mobile; use `MobileDock` or stacked list instead. |
| Scroll | Wrap content in `<ScrollArea className="h-full w-full">` | Never `overflow-y-auto` on the aside itself. |

### Nav Item — Top-Level (Flat or Parent)
| Property | Value |
|----------|-------|
| Font | `text-xs` (12px) |
| Padding | `px-3 py-1.5` |
| Gap | `gap-2` |
| Icon | `h-3.5 w-3.5` |
| Active BG | `bg-accent text-accent-foreground font-medium` |
| Active icon | `text-primary` |
| Inactive | `text-muted-foreground hover:text-foreground` |
| Hover BG | `hover:bg-muted/80` |
| Shape | **No rounded corners** on rows — full-bleed highlight. |

### Nav Item — Child (Second Tier)
| Property | Value |
|----------|-------|
| Font | `text-[11px]` |
| Padding | `pl-8 pr-3 py-1` |
| Gap | `gap-1.5` |
| Icon | `h-3 w-3` |
| Active | `text-primary font-medium` (no background) |
| Inactive icon | `text-muted-foreground/60` |

### Section Headers (Grouped Lists)
| Property | Value |
|----------|-------|
| Font | `text-[10px] font-medium uppercase tracking-wider` — the ONE sanctioned 10px use (uppercase overline chrome; see `ui-dense` data-dense-rules "Absolute minimums") |
| Color | `text-muted-foreground/70` |
| Padding | `px-3 pt-3 pb-1` |
| Separator | `border-t border-border/40` above the header, not `<Separator>` components. |

### Filter Bar / Chip Row
| Property | Value |
|----------|-------|
| Container | `px-3 py-1.5 flex items-center gap-1.5 flex-wrap` |
| Chip (active) | `px-2 py-0.5 rounded text-xs bg-primary text-primary-foreground` |
| Chip (inactive) | `px-2 py-0.5 rounded text-xs bg-muted/60 text-muted-foreground hover:bg-muted` |
| Search input | `h-7 text-xs pl-8` with icon at `h-3.5 w-3.5` |
| Select dropdown | `h-6 px-1.5 rounded text-xs bg-muted/60 border-0` |

### Footer / Status Bar
| Property | Value |
|----------|-------|
| Padding | `px-4 py-1.5` or `px-4 py-2` |
| Font | `text-xs` (status text is content — never below 12px) |
| Background | `bg-muted/20` |
| Border | `border-t border-border/60` |
| Buttons | `h-7 text-xs gap-1 px-2.5` |

## Anti-Patterns

These are the exact mistakes to fix when refactoring existing sidebars:

| Bad | Fix |
|-----|-----|
| `w-52`, `w-64`, or wider | Reduce to `w-36`–`w-44` |
| `text-sm` on nav items | Use `text-xs` |
| `py-2`, `py-3` on nav rows | Use `py-1.5` (top-level) or `py-1` (child) |
| `gap-3` between icon and label | Use `gap-2` (top-level) or `gap-1.5` (child) |
| `h-4 w-4` icons in nav | Use `h-3.5 w-3.5` (top-level) or `h-3 w-3` (child) |
| `rounded-md` on nav rows | Remove — use full-bleed row highlights |
| `bg-primary text-primary-foreground` active | Use `bg-accent text-accent-foreground` |
| `p-3`, `p-4` wrapper padding inside sidebar | Use `py-1` with no horizontal padding on the wrapper; let rows handle `px-3` |
| `space-y-6` between groups | Use `border-t border-border/40` separator + tight header |
| `<Separator>` component | Replace with a `border-t` on the section header |
| `bg-card` sidebar background | Use `bg-muted/30` |
| `border-border` (full opacity) | Use `border-border/60` |
| `text-lg` sidebar title | Remove header entirely or use `text-xs uppercase` section label |

## Two-Tier Expandable Pattern

For sidebars where a top-level item reveals sub-items (like Settings > Preferences):

```tsx
const isExpanded = isActive && !!item.children;

{/* Parent */}
<Link href={item.children ? `${item.href}?tab=${item.children[0].param}` : item.href}
  className={cn(
    'flex items-center gap-2 px-3 py-1.5 transition-colors text-xs',
    'hover:bg-muted/80',
    isActive ? 'bg-accent text-accent-foreground font-medium'
             : 'text-muted-foreground hover:text-foreground',
  )}
>
  <span className={cn('shrink-0', isActive ? 'text-primary' : 'text-muted-foreground')}>
    {item.icon}
  </span>
  <span className="truncate">{item.title}</span>
</Link>

{/* Children — only when expanded */}
{isExpanded && (
  <div className="py-0.5">
    {item.children.map(child => (
      <Link key={child.param}
        href={`${item.href}?tab=${child.param}`}
        className={cn(
          'flex items-center gap-1.5 pl-8 pr-3 py-1 transition-colors text-[11px]',
          'hover:bg-muted/80',
          isChildActive ? 'text-primary font-medium'
                        : 'text-muted-foreground hover:text-foreground',
        )}
      >
        <span className={cn('shrink-0',
          isChildActive ? 'text-primary' : 'text-muted-foreground/60',
        )}>{child.icon}</span>
        <span className="truncate">{child.title}</span>
      </Link>
    ))}
  </div>
)}
```

## Grouped Sections Pattern

For sidebars with categorized groups (like a file manager):

```tsx
<aside className="hidden md:flex w-40 shrink-0 border-r border-border/60 bg-muted/30">
  <ScrollArea className="h-full w-full">
    <nav>
      {groups.map((group, i) => (
        <div key={group.label}>
          {/* Section header — acts as separator */}
          <div className={cn(
            'px-3 pt-3 pb-1 text-[10px] font-medium uppercase tracking-wider text-muted-foreground/70',
            i > 0 && 'border-t border-border/40',
          )}>
            {group.label}
          </div>
          {group.items.map(item => (
            <Link key={item.href} href={item.href}
              className={cn(
                'flex items-center gap-2 px-3 py-1.5 transition-colors text-xs',
                'hover:bg-muted/80',
                isActive ? 'bg-accent text-accent-foreground font-medium'
                         : 'text-muted-foreground hover:text-foreground',
              )}
            >
              <item.icon className={cn('h-3.5 w-3.5 shrink-0',
                isActive ? 'text-primary' : 'text-muted-foreground',
              )} />
              <span className="truncate">{item.label}</span>
            </Link>
          ))}
        </div>
      ))}
    </nav>
  </ScrollArea>
</aside>
```

## Refactoring Checklist

When converting an existing sidebar to this system:

1. **Container**: `w-36`–`w-44`, `bg-muted/30`, `border-r border-border/60`
2. **Remove wrapper padding**: No `p-3`/`p-4` on the scroll content wrapper
3. **Items**: `text-xs`, `px-3 py-1.5`, `gap-2`, icons `h-3.5 w-3.5`
4. **Active state**: `bg-accent text-accent-foreground font-medium` (not `bg-primary`)
5. **No rounded rows**: Remove `rounded-md` from item classes
6. **Section separators**: Replace `<Separator>` and `space-y-6` with `border-t border-border/40` on headers
7. **Remove sidebar titles**: Drop `text-lg font-semibold` headers; use section labels if grouping is needed
8. **Icons**: Lucide React only, `h-3.5 w-3.5` for top-level, `h-3 w-3` for children
9. **ScrollArea**: Wrap nav content in `<ScrollArea>`, not `overflow-y-auto`
10. **Mobile**: `hidden md:flex` on the aside; provide `MobileDock` or stacked list alternative
