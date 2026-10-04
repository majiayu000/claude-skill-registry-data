---
name: add-department-tab
description: Scaffold a new tab page under an existing department route
disable-model-invocation: true
---

# Add Department Tab Skill

## Purpose

Add a new tab to an existing department by creating the route page, updating the tab configuration, and wiring up data fetching.

## Process

### 1. Ask for tab details

- **department** — Which department (slug, e.g. `control-room`, `engineering`)
- **tab name** — URL slug (kebab-case, e.g. `maintenance-log`)
- **tab label** — Display name (e.g. `Maintenance Log`)
- **tab icon** — Lucide icon name (e.g. `ClipboardList`)
- **tab type** — What kind of page:
  - `dashboard` — Summary with KPI cards + data tables
  - `data-entry` — Form for submitting records (will also need `add-data-entry-form`)
  - `read-only` — Display-only list/table of records
  - `special` — Custom UI (satellite, SCADA, etc.)

### 2. Update `apps/portal/lib/departments.ts`

Add the tab to the appropriate tab constant:

- For standard departments: add to `DEPARTMENT_TABS`
- For control-room: add to `CONTROL_ROOM_TABS`
- For engineering: add to `ENGINEERING_TABS`
- For satellite-monitoring: add to `SATELLITE_MONITORING_TABS`

```typescript
{ name: "<tabName>", label: "<tabLabel>", icon: "<tabIcon>" },
```

### 3. Create the page file

Create `apps/portal/app/(departments)/[department]/<tabName>/page.tsx`:

**For dashboard/read-only tabs:**

```tsx
import { createServerSupabaseClient } from "@repo/supabase/server";
import { DEPARTMENTS } from "~/lib/departments";
import { notFound } from "next/navigation";
import { GlassCard } from "@repo/ui/GlassCard";

export default async function <TabName>Page({
  params,
}: {
  params: { department: string };
}) {
  const dept = DEPARTMENTS.find((d) => d.name === params.department);
  if (!dept) notFound();

  // Restrict to specific department if needed
  // if (params.department !== "<department>") notFound();

  const supabase = await createServerSupabaseClient();
  const { data: department } = await supabase
    .from("departments")
    .select("id")
    .eq("name", params.department)
    .single();

  if (!department) notFound();
  const deptId = department.id;
  const today = new Date().toISOString().split("T")[0];

  // Fetch data here
  // const { data } = await supabase.from("<table>").select("*").eq("department_id", deptId);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-medium text-[#fafafa]"><tabLabel></h2>
        <p className="text-[#898989] text-sm">
          {new Date().toLocaleDateString("en-ZA", {
            weekday: "long",
            year: "numeric",
            month: "long",
            day: "numeric",
          })}
        </p>
      </div>

      {/* KPI Summary */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <GlassCard>
          <p className="text-[#898989] text-xs uppercase tracking-wide">Metric</p>
          <p className="text-2xl font-medium text-[#fafafa] mt-1">Value</p>
        </GlassCard>
      </div>

      {/* Content */}
    </div>
  );
}
```

**For data-entry tabs**, also create a form component:

```tsx
// page.tsx — same setup, then pass data to form
// <tabName>/<TabName>Form.tsx — use add-data-entry-form skill
```

### 4. Department-only guard

If the tab should only appear for one department, add the guard at the top of the page:

```tsx
if (params.department !== "control-room") notFound();
```

### 5. Verify

1. Navigate to `/<department>/<tabName>` in the browser
2. Confirm the tab appears in the sidebar navigation
3. Confirm the page renders with correct department context
4. Commit changes

## Design System Reminders

- Use `font-medium` instead of `font-semibold` or `font-bold`
- Use `text-[#fafafa]` for primary text, `text-[#898989]` for muted, `text-[#b4b4b4]` for secondary
- Use `bg-[#171717]` for input/card backgrounds, `border-[#363636]` for borders
- Use `text-[#3ecf8e]` for accent/brand green, `text-emerald-400` for positive values
- Use `text-amber-400` for warning values, `text-red-400` for error/alert values
- Import Supabase from `@repo/supabase/server` (server components) or `@repo/supabase/client` (client components)
