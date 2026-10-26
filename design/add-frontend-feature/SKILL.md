---
name: add-frontend-feature
description: Build new frontend features (pages, components, forms) following TheSmartHost project conventions and patterns.
---

# Add Frontend Feature

> **Instructions for building new UI features, pages, and components following established patterns**

Use this skill when building:
- New pages (dashboard views, detail pages)
- New components (modals, forms, tables)
- New UI features (buttons, dropdowns, cards)

---

## File Structure Conventions

### Component Organization
```
src/
├── components/
│   ├── [resource]/               # Group by resource/feature
│   │   ├── create/
│   │   │   └── create[Resource]Modal.tsx
│   │   ├── update/
│   │   │   └── update[Resource]Modal.tsx
│   │   ├── delete/
│   │   │   └── delete[Resource]Modal.tsx
│   │   └── preview/
│   │       └── preview[Resource]Modal.tsx
│   └── shared/                   # Reusable components
│       ├── modal.tsx
│       ├── notification.tsx
│       └── TableActionsDropdown.tsx
```

**Rules:**
- Component folders use **lowercase with hyphens** (e.g., `property/`, `client-agreement/`)
- Action folders are always: `create/`, `update/`, `delete/`, `preview/`
- Component files use **PascalCase** and descriptive names
- Modal components always end with `Modal.tsx`
- Use `'use client'` directive for all interactive components

### Page Organization
```
src/
└── app/
    ├── (prelogin)/              # Public pages (login, signup)
    │   ├── login/
    │   │   └── page.tsx
    │   └── signup/
    │       └── page.tsx
    └── (user)/                  # Protected pages
        └── property-manager/    # Role-based routes
            ├── dashboard/
            │   └── page.tsx
            ├── properties/
            │   └── page.tsx
            └── clients/
                └── page.tsx
```

**Rules:**
- Route groups use parentheses: `(prelogin)/`, `(user)/`
- Role-based routes: `property-manager/`, `admin/`, `client/`
- Each route has a `page.tsx` file
- Pages use **Server Components by default**, add `'use client'` only when needed

### Services Organization
```
src/
├── services/
│   ├── [resource]Service.ts     # API call wrappers
│   └── types/
│       └── [resource].ts        # TypeScript interfaces
```

**Rules:**
- Service files use **camelCase** with `Service.ts` suffix
- Type files match service names (e.g., `propertyService.ts` → `property.ts`)
- Always export named functions (not default exports)

### State Management
```
src/
└── store/
    └── use[Name]Store.ts        # Zustand stores
```

**Rules:**
- Store files use **camelCase** with `Store.ts` suffix
- Hook names start with `use` (e.g., `useUserStore`, `useNotificationStore`)
- Use Zustand `persist` middleware for data that should survive refresh

---

## Component Naming Patterns

### Modals
```
create[Resource]Modal.tsx    # e.g., createPropertyModal.tsx
update[Resource]Modal.tsx    # e.g., updateClientModal.tsx
delete[Resource]Modal.tsx    # e.g., deletePropertyModal.tsx
preview[Resource]Modal.tsx   # e.g., previewPropertyModal.tsx
```

### Shared Components
```
modal.tsx                    # Generic modal wrapper
notification.tsx             # Toast notifications
TableActionsDropdown.tsx     # Three-dot menu for tables
```

### Pages
```
page.tsx                     # Always named "page.tsx" (Next.js convention)
layout.tsx                   # Layout wrapper
```

---

## TypeScript Conventions

### Always Define Types in `services/types/`

**Interface over Type:**
```typescript
// ✅ Use interface
export interface Property {
  id: string
  name: string
  isActive: boolean
}

// ❌ Avoid type alias for objects
export type Property = {
  id: string
  name: string
}
```

### Common Type Patterns

**Entity Interface:**
```typescript
export interface Property {
  id: string
  name: string
  address: string
  province: string
  propertyType: 'STR' | 'LTR'
  hostawayListingId: string
  commissionRate: number
  isActive: boolean
  createdAt: string
  updatedAt: string | null
  owners: PropertyOwner[]
}
```

**Nested Interface:**
```typescript
export interface PropertyOwner {
  clientId: string
  clientName: string
  isPrimary: boolean
  commissionRateOverride: number | null
}
```

**Request Payload:**
```typescript
export interface CreatePropertyPayload {
  clientId: string
  name: string
  address: string
  province: string
  propertyType: 'STR' | 'LTR'
  hostawayListingId: string
  commissionRate: number
  commissionRateOverride?: number
}
```

**API Response Wrapper:**
```typescript
export interface PropertyResponse {
  status: 'success' | 'failed'
  message?: string
  data: Property
}

export interface PropertiesResponse {
  status: 'success' | 'failed'
  message?: string
  data: Property[]
}
```

---

## State Management Patterns

### When to Use Zustand vs Local State

**Use Zustand for:**
- Global user state (profile, authentication)
- Cross-component notifications
- Persisted data (survives page refresh)

**Use Local State (`useState`) for:**
- Form inputs
- Modal open/close state
- Component-specific UI state

### Zustand Store Pattern
```typescript
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface UserProfile {
  id: string
  fullName: string
  role: 'ADMIN' | 'PROPERTY-MANAGER' | 'CLIENT'
  email?: string
}

interface UserStore {
  profile: UserProfile | null
  isAuthenticated: boolean
  setProfile: (profile: UserProfile) => void
  clearProfile: () => void
}

export const useUserStore = create<UserStore>()(
  persist(
    (set) => ({
      profile: null,
      isAuthenticated: false,
      setProfile: (profile) => set({ profile, isAuthenticated: true }),
      clearProfile: () => set({ profile: null, isAuthenticated: false }),
    }),
    {
      name: 'user-storage',
      partialize: (state) => ({
        profile: state.profile,
        isAuthenticated: state.isAuthenticated
      })
    }
  )
)
```

---

## Styling Conventions

### Tailwind CSS Utility Classes

**Always use Tailwind directly on JSX** (no CSS modules, no styled-components).

**Common Patterns:**

**Layout:**
```tsx
<div className="flex justify-between items-center">
<div className="grid grid-cols-2 gap-4">
<div className="space-y-4">
```

**Spacing:**
```tsx
<div className="p-6">        {/* Padding */}
<div className="mt-4 mb-2">  {/* Margin */}
<div className="gap-3">      {/* Grid/Flex gap */}
```

**Colors:**
```tsx
<div className="bg-white text-black">
<div className="bg-blue-600 text-white">
<div className="border border-gray-300">
```

**Interactive States:**
```tsx
<button className="hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed">
<input className="focus:outline-none focus:ring-2 focus:ring-blue-500">
```

**Responsive Design:**
```tsx
<div className="w-11/12 max-w-2xl">  {/* Responsive width */}
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
```

---

## For More Details

- **Component patterns with full code examples:** See `component-patterns.md`
- **Form patterns with validation examples:** See `form-patterns.md`
- **Styling guide with Tailwind examples:** See `styling-guide.md`

---

**Last Updated:** November 4, 2025
