---
name: mobile-bottom-navbar
description: Standardized mobile bottom navigation implementation for internal Next.js applications. Provides role-based filtering, smooth animations, persistent state, and submenu expansion with accordion-based More menu. Supports Next.js 14+ with App Router, TypeScript, Zustand state management, and Framer Motion animations. Includes complete ready-to-use components with icon grid layouts, comprehensive documentation, and customization guides.
---

# Mobile Bottom Navbar

## Overview

This skill provides a complete, production-ready mobile bottom navigation system for Next.js 14+ applications with App Router. The implementation features:
- **3-Column Icon Grid Layouts** for submenus and More menu
- **Accordion-Based More Menu** with collapsible group sections
- **Submenu Dropdown** appearing above the navbar
- Role-based filtering and smooth animations

**📸 Visual Reference:** See `references/screenshots/` for actual UI examples from MyJKKN application.

### Key Features

- **Icon Grid Submenus**: 3-column grid layout with icons + labels (like iOS app grid)
- **Accordion More Menu**: Collapsible sections showing all overflow menu groups
- **Always Visible Design**: Full navbar always shown on mobile (no separate minimized state)
- **Role-Based Filtering**: Dynamic navigation based on user permissions
- **Smart Active Detection**: Automatically highlights current page
- **Submenu Expansion**: Click nav items to expand submenus with backdrop overlay
- **Overflow Handling**: "More" menu for navigation groups beyond primary 4 items
- **State Persistence**: Zustand with localStorage for cross-session state
- **Hydration Safety**: Prevents flash of incorrect state on page load
- **Smooth Animations**: Spring-based animations via Framer Motion
- **iOS Safe Area Support**: Respects notch and home indicator spacing
- **TypeScript First**: Fully typed for excellent DX
- **Customizable**: Colors, animations, layouts, and icons

### UI Pattern (Critical Design Elements)

#### ✅ Bottom Navbar
```
┌─────────────────────────────────────────────────────┐
│  [Icon]     [Icon]    [Icon]    [Icon]    [Icon]   │
│ Overview  User Mgmt   Apps    App Hub    More (5+) │
│    ─                                                │  ← Active indicator
└─────────────────────────────────────────────────────┘
```
- 4 primary items + "More" button with badge count
- Even spacing, icons with labels below
- Active state: primary color + underline indicator

#### ✅ Submenu Dropdown (Opens ABOVE navbar)
```
┌─────────────────────────────────────┐
│  ┌─────┐  ┌─────┐  ┌─────┐         │
│  │ 📊  │  │ 🤖  │  │     │         │  ← 3-column grid
│  │Dash │  │ AI  │  │     │         │
│  └─────┘  └─────┘  └─────┘         │
└─────────────────────────────────────┘
└─────────────────────────────────────┘ ← Navbar (below)
```
- Grid layout (3 columns)
- Icon + label cards
- Appears above navbar with backdrop

#### ✅ More Menu Modal (Accordion with Icon Grid)
```
┌─────────────────────────────────────┐
│ All Menus                        ✕  │
├─────────────────────────────────────┤
│ > Organization Management      9  ▼ │ ← Accordion header with count
│                                     │
│   ┌─────┐  ┌─────┐  ┌─────┐        │
│   │ 🏢  │  │ 🎓  │  │ 🔥  │        │ ← 3-column icon grid
│   │Inst │  │Degr │  │Dept │        │
│   └─────┘  └─────┘  └─────┘        │
│   ┌─────┐  ┌─────┐  ┌─────┐        │
│   │ 📚  │  │ 📅  │  │ 📖  │        │
│   │Prog │  │Seme │  │Sect │        │
│   └─────┘  └─────┘  └─────┘        │
│   ┌─────┐  ┌─────┐  ┌─────┐        │
│   │ 📝  │  │ 🗺️  │  │     │        │
│   │Cour │  │Maps │  │     │        │
│   └─────┘  └─────┘  └─────┘        │
│                                     │
│ > Finance Management           6  ▶ │ ← Collapsed section
│                                     │
└─────────────────────────────────────┘
```

**Critical Pattern Elements:**
1. **Sheet Component**: Bottom sheet with rounded top (`rounded-t-3xl`)
2. **Accordion**: `type="multiple"` with all groups expanded by default
3. **Group Headers**: Icon badge + label + count + chevron
4. **Submenu Grid**: 3-column layout with icons and labels
5. **Active Highlighting**: Primary color ring and background

### When to Use This Skill

Use this skill when:
- Implementing mobile navigation for Next.js 14+ App Router applications
- Needing role-based or permission-based navigation filtering
- Building internal applications with consistent navigation patterns
- Requiring persistent navigation state across sessions
- Supporting iOS devices with safe area insets
- Wanting smooth, professional animations without performance issues
- **Need accordion-style More menu with icon grid submenus**

## Quick Start

### 1. Install Dependencies

```bash
npm install zustand framer-motion lucide-react clsx tailwind-merge
```

Required shadcn/ui components:
```bash
npx shadcn@latest add sheet accordion scroll-area
```

### 2. Copy Core Files

Copy all files from `assets/` to your project:

```
assets/
├── components/BottomNav/
│   ├── bottom-navbar.tsx           → components/BottomNav/
│   ├── bottom-nav-item.tsx         → components/BottomNav/
│   ├── bottom-nav-submenu.tsx      → components/BottomNav/
│   ├── bottom-nav-more-menu.tsx    → components/BottomNav/ ✨ KEY COMPONENT
│   ├── bottom-nav-minimized.tsx    → components/BottomNav/
│   ├── types.ts                    → components/BottomNav/
│   └── index.ts                    → components/BottomNav/
└── hooks/
    ├── use-bottom-nav.ts           → hooks/
    └── use-mobile.tsx              → hooks/
```

**⚠️ IMPORTANT:** Always use the complete `bottom-nav-more-menu.tsx` from assets to ensure proper accordion + icon grid pattern.

### 3. Integrate with Layout

```typescript
// app/(routes)/layout.tsx
'use client';

import { cn } from '@/lib/utils';
import { useIsMobile } from '@/hooks/use-mobile';
import { BottomNavbar } from '@/components/BottomNav';

export default function MainLayout({ children }) {
  const isMobile = useIsMobile();

  return (
    <>
      <main className={cn(
        'min-h-screen bg-background',
        isMobile && 'pb-20'  // Bottom padding for navbar
      )}>
        {children}
      </main>

      <BottomNavbar />
    </>
  );
}
```

### 4. Configure Navigation Structure

Create or update `lib/sidebarMenuLink.ts`:

```typescript
import { LucideIcon, Home, Users, Building, /* ... */ } from 'lucide-react';

interface MenuItem {
  href: string;
  label: string;
  icon: LucideIcon;
  active: boolean;
  submenus: Array<{ href: string; label: string; active: boolean }>;
}

interface MenuGroup {
  groupLabel: string;
  menus: MenuItem[];
}

// Example navigation structure
export function GetRoleBasedPages(
  pathname: string,
  userRole?: CustomRole | null
): MenuGroup[] {
  return [
    {
      groupLabel: 'Overview',
      menus: [
        {
          href: '/dashboard',
          label: 'Dashboard',
          icon: Home,
          active: pathname === '/dashboard',
          submenus: [
            { href: '/dashboard', label: 'Dashboard', active: pathname === '/dashboard' },
            { href: '/ai-assistant', label: 'AI Assistant', active: pathname === '/ai-assistant' }
          ]
        }
      ]
    },
    {
      groupLabel: 'User Management',
      menus: [
        {
          href: '/users',
          label: 'Users',
          icon: Users,
          active: pathname.startsWith('/users'),
          submenus: [
            { href: '/users/list', label: 'User List', active: pathname === '/users/list' },
            { href: '/users/roles', label: 'Roles', active: pathname === '/users/roles' }
          ]
        }
      ]
    },
    // ... first 4 groups appear in navbar
    // Groups 5+ appear in More menu with accordion + grid layout
    {
      groupLabel: 'Organization Management',
      menus: [
        {
          href: '/organization',
          label: 'Organization',
          icon: Building,
          active: pathname.startsWith('/organization'),
          submenus: [
            { href: '/organization/institutions', label: 'Institutions', active: false },
            { href: '/organization/degrees', label: 'Degrees', active: false },
            { href: '/organization/departments', label: 'Departments', active: false },
            { href: '/organization/programs', label: 'Programs', active: false },
            { href: '/organization/semesters', label: 'Semesters', active: false },
            { href: '/organization/sections', label: 'Sections', active: false },
            { href: '/organization/courses', label: 'All Courses', active: false },
            { href: '/organization/mappings', label: 'Course Mappings', active: false }
          ]
        }
      ]
    }
  ];
}
```

### 5. Verify Implementation

Test checklist:

- ✅ Navbar appears on mobile (< 1024px width)
- ✅ Hidden on desktop (≥ 1024px width)
- ✅ Active nav item highlighted
- ✅ Submenu expands ABOVE navbar in 3-column grid
- ✅ More menu opens as bottom sheet
- ✅ More menu shows accordion sections with icon grid
- ✅ All accordion groups expanded by default
- ✅ Group headers show icon + label + count
- ✅ Navigation works correctly
- ✅ State persists across refreshes
- ✅ iOS safe area insets respected

## Critical Implementation Notes

### ⚠️ More Menu Pattern - MUST FOLLOW

The More menu MUST use this exact pattern:

```typescript
// bottom-nav-more-menu.tsx
<Sheet open={isOpen} onOpenChange={(open) => !open && onClose()}>
  <SheetContent side="bottom" className="h-[80vh] rounded-t-3xl">
    <SheetHeader>
      <SheetTitle>All Menus</SheetTitle>
    </SheetHeader>

    {/* Accordion with ALL groups expanded by default */}
    <Accordion type="multiple" defaultValue={groups.map(g => g.id)}>
      {groups.map((group) => (
        <AccordionItem key={group.id} value={group.id}>
          <AccordionTrigger>
            <div className="flex items-center gap-3">
              {/* Icon badge */}
              <div className="p-2 rounded-lg bg-muted">
                <GroupIcon className="h-4 w-4" />
              </div>
              {/* Label */}
              <span className="font-medium text-sm">{group.groupLabel}</span>
              {/* Count */}
              <span className="text-xs text-muted-foreground ml-auto mr-2">
                {group.menus.length}
              </span>
            </div>
          </AccordionTrigger>

          <AccordionContent>
            {/* 3-column icon grid */}
            <div className="grid grid-cols-3 gap-2 pt-2 pb-3">
              {group.menus.map((item) => (
                <button
                  key={item.href}
                  onClick={() => handleItemClick(item.href)}
                  className="flex flex-col items-center p-3 rounded-lg"
                >
                  <Icon className="h-5 w-5 mb-1" />
                  <span className="text-[10px] text-center line-clamp-2">
                    {item.label}
                  </span>
                </button>
              ))}
            </div>
          </AccordionContent>
        </AccordionItem>
      ))}
    </Accordion>
  </SheetContent>
</Sheet>
```

**Key Requirements:**
1. `Accordion type="multiple"` - Allows multiple sections open simultaneously
2. `defaultValue={groups.map(g => g.id)}` - All groups expanded by default
3. 3-column grid (`grid-cols-3`) for submenu items
4. Icon + label for each item
5. Group header shows count of items

### Common Mistakes to Avoid

❌ **DON'T** create flat list More menu:
```typescript
// WRONG - Flat list layout
<div>
  {groups.map(group => (
    <div key={group.id}>
      <h3>{group.groupLabel}</h3>
      <ul>
        {group.menus.map(item => (
          <li>{item.label}</li>
        ))}
      </ul>
    </div>
  ))}
</div>
```

✅ **DO** use accordion with icon grid (see above)

❌ **DON'T** place submenu below navbar:
```typescript
// WRONG - Submenu below navbar
<nav>...</nav>
<Submenu />  // Wrong position
```

✅ **DO** place submenu inside navbar, above items:
```typescript
<nav>
  <Submenu />  // Correct - inside nav, above items
  <div className="flex">...</div>
</nav>
```

## File Organization

After implementation:

```
your-project/
├── components/
│   └── BottomNav/
│       ├── bottom-navbar.tsx          (Main orchestrator)
│       ├── bottom-nav-item.tsx        (Individual nav button)
│       ├── bottom-nav-submenu.tsx     (3-column grid dropdown)
│       ├── bottom-nav-more-menu.tsx   (Accordion + grid modal) ✨
│       ├── bottom-nav-minimized.tsx   (Optional minimized state)
│       ├── types.ts                   (TypeScript definitions)
│       └── index.ts                   (Barrel export)
├── hooks/
│   ├── use-bottom-nav.ts              (Zustand store)
│   └── use-mobile.tsx                 (Mobile detection)
├── lib/
│   ├── sidebarMenuLink.ts             (Navigation structure)
│   └── utils.ts                       (cn utility)
└── app/
    └── (routes)/
        └── layout.tsx                 (Integration point)
```

## Resources

### References (`references/`)

1. **`screenshots/`** - Visual reference from MyJKKN app
   - `myjkkn-dashboard.png` - Main navbar view
   - `myjkkn-submenu-dropdown.png` - 3-column submenu grid
   - `myjkkn-more-menu.png` - Accordion More menu with icon grid
   - `README.md` - Detailed visual documentation

2. **`complete-implementation.md`** - Full step-by-step implementation guide
3. **`component-reference.md`** - Complete API documentation
4. **`customization-guide.md`** - Theming and styling guide
5. **`integration-guide.md`** - Auth and layout integration
6. **`troubleshooting.md`** - Common issues and solutions

### Assets (`assets/`)

1. **`components/BottomNav/`** - Complete component implementations
2. **`hooks/`** - State management and utilities
3. **`examples/`** - Implementation examples

## Usage Patterns

### For New Projects

1. Copy all files from `assets/` to appropriate locations
2. Install dependencies
3. Configure navigation structure
4. Integrate with main layout
5. Test on mobile devices
6. Verify accordion More menu pattern

### For Existing Projects

1. Review `references/screenshots/` for visual pattern
2. Copy latest components from `assets/`
3. Update More menu to use accordion + grid pattern
4. Test for feature parity with screenshots
5. Gradual rollout with feature flags

### Troubleshooting Wrong UI Pattern

**Problem:** More menu shows flat list instead of accordion grid

**Solution:**
1. Verify you copied latest `bottom-nav-more-menu.tsx` from `assets/`
2. Check accordion configuration:
   ```typescript
   <Accordion type="multiple" defaultValue={groups.map(g => g.id)}>
   ```
3. Check grid layout in AccordionContent:
   ```typescript
   <div className="grid grid-cols-3 gap-2">
   ```
4. Verify shadcn/ui accordion component is installed

**Problem:** Submenu appears below navbar

**Solution:**
1. Check submenu placement in `bottom-navbar.tsx`
2. Ensure submenu is INSIDE `<nav>` element, BEFORE nav items
3. Verify z-index layering

## Best Practices

1. **Always Use Latest Components**: Copy from `assets/` folder, not custom implementations
2. **Reference Screenshots**: Check `references/screenshots/` for correct UI pattern
3. **Test Icon Grid**: Verify 3-column grid layout in submenus and More menu
4. **Verify Accordion**: Ensure all groups expanded by default in More menu
5. **Wait for Hydration**: Prevent flash of incorrect state
6. **Test on Real Devices**: Responsive mode doesn't catch all mobile issues
7. **Clean Up Event Listeners**: Prevent memory leaks in useEffect
8. **Memoize Computations**: Use useMemo for expensive transformations
9. **Handle Nested Routes**: Use startsWith for route matching
10. **Document Customizations**: Track theme changes for consistency

## Summary

This skill provides a standardized mobile bottom navbar with:

- ✅ **Complete working code** with accordion More menu pattern
- ✅ **Visual reference screenshots** showing exact UI
- ✅ **3-column icon grid** for submenus and More menu
- ✅ **Accordion sections** in More menu (all expanded by default)
- ✅ **Comprehensive documentation** for all scenarios
- ✅ **Multiple examples** for different use cases
- ✅ **Customization guides** for branding
- ✅ **Integration guides** for auth systems
- ✅ **Troubleshooting guide** for common issues

**Start with Quick Start section above, reference screenshots in `references/screenshots/`, and use the complete components from `assets/` to ensure the correct UI pattern.**
