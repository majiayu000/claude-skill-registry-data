---
name: add-department
description: Scaffold a full department with route, tabs, migration, and hub entry
disable-model-invocation: true
---

# Add Department Skill

## Purpose

Scaffold a complete new department in the Arch Systems portal, including route folder, tab pages, database migration, and hub registration.

## Process

### 1. Ask for department details

- **name** — URL slug (kebab-case, e.g. `surveying`)
- **displayName** — Human-readable name (e.g. `Surveying`)
- **icon** — Lucide icon name (e.g. `Compass`)
- **description** — One-line description for the hub card
- **color** — Tailwind color: `amber`, `emerald`, `blue`, `violet`, `red`, `orange`, `cyan`, or `indigo`
- **tabs** — List of tab names and slugs (e.g. `[{ name: "dashboard", label: "Dashboard", icon: "BarChart2" }, ...]`)
- **restricted** — Is this department restricted to specific roles? (default: no)

### 2. Update `apps/portal/lib/departments.ts`

Add the department to the `DEPARTMENTS` array:

```typescript
{
  name: "<name>",
  displayName: "<displayName>",
  icon: "<icon>",
  description: "<description>",
  color: "<color>",
  status: "active",
  stats: { label: "<statLabel>", value: "<statValue>" },
}
```

Add the tab configuration constant:

```typescript
export const <NAME>_TABS = [
  { name: "dashboard", label: "Dashboard", icon: "BarChart2" },
  // ... tabs from user input
] as const;
```

Add the condition in `getDepartmentTabs()`:

```typescript
if (departmentName === "<name>") {
  return <NAME>_TABS;
}
```

Add the type export:

```typescript
export type <Name>Tab = typeof <NAME>_TABS[number];
```

### 3. Update the hub sidebar

In `apps/portal/app/(hub)/layout.tsx`, add the department to the sidebar nav if needed (most departments appear automatically via the `DEPARTMENTS` array).

If the department should appear in the "Advanced Systems" section instead of "Departments", add it manually like the satellite-monitoring entry.

### 4. Create route folder and page stubs

Create `apps/portal/app/(departments)/[department]/` page files for each tab:

**Dashboard page** (`apps/portal/app/(departments)/[department]/page.tsx`):

```tsx
import { createServerSupabaseClient } from "@repo/supabase/server";
import { GlassCard } from "@repo/ui/GlassCard";
import { DEPARTMENTS } from "~/lib/departments";
import { notFound } from "next/navigation";

export default async function <Name>DashboardPage({
  params,
}: {
  params: { department: string };
}) {
  const dept = DEPARTMENTS.find((d) => d.name === params.department);
  if (!dept) notFound();

  const supabase = await createServerSupabaseClient();
  const { data: department } = await supabase
    .from("departments")
    .select("id")
    .eq("name", params.department)
    .single();

  if (!department) notFound();

  const deptId = department.id;
  const today = new Date().toISOString().split("T")[0];

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-medium text-[var(--text-heading)]">{dept.displayName} Dashboard</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <GlassCard>
          <p className="text-[var(--text-muted)] text-sm">Status</p>
          <p className="text-2xl font-medium text-[var(--accent-green)] mt-1">Operational</p>
        </GlassCard>
      </div>
    </div>
  );
}
```

**Sub-page** (e.g. `daily-log/page.tsx`):

```tsx
import { createServerSupabaseClient } from "@repo/supabase/server";
import { DEPARTMENTS } from "~/lib/departments";
import { notFound } from "next/navigation";

export default async function <Name><Tab>Page({
  params,
}: {
  params: { department: string };
}) {
  const dept = DEPARTMENTS.find((d) => d.name === params.department);
  if (!dept) notFound();

  const supabase = await createServerSupabaseClient();
  const { data: department } = await supabase
    .from("departments")
    .select("id")
    .eq("name", params.department)
    .single();

  if (!department) notFound();

  const deptId = department.id;

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-medium text-[var(--text-heading)]"><TabLabel></h2>
      {/* Add content here */}
    </div>
  );
}
```

### 5. Create database migration

Create a migration file in `packages/database/migrations/`:

```sql
-- Insert department
INSERT INTO departments (name, display_name, description)
VALUES ('<name>', '<displayName>', '<description>')
ON CONFLICT (name) DO NOTHING;
```

If the department needs new tables, use the `create-migration` skill to generate them with proper RLS policies.

### 6. Post-creation steps

1. Run `pnpm --filter @repo/database supabase:push` to apply the migration
2. Verify the department appears in the portal at `/<name>`
3. Verify tab navigation works
4. Commit all changes

## Design System Reminders

- **Theme**: Light-only macOS Sonoma. Never use dark hex colors (`#171717`, `#363636`, `#fafafa`).
- **Text**: `text-[var(--text-heading)]` for headings, `text-[var(--text-primary)]` for body, `text-[var(--text-secondary)]` for labels, `text-[var(--text-muted)]` for metadata.
- **Backgrounds**: `bg-white/70 backdrop-blur-xl` for glass surfaces. Cards use the `GlassCard` component.
- **Shadows**: Use `shadow-card` / `shadow-diffusion-*` tokens. Never use Tailwind `shadow-*` or raw `box-shadow`.
- **Never use `font-bold` or `font-semibold`** — use `font-medium` for emphasis.
- **Accent**: `var(--accent-blue)` (`#007aff`). Never use green accent colors.
- Always use `cn()` from `@repo/ui/lib/utils` for class merging.
- Import Supabase clients from `@repo/supabase/*`, never `@supabase/supabase-js`.
