---
name: add-data-entry-form
description: Scaffold a Supabase data entry form with validation, shift toggle, and glass-morphism styling
disable-model-invocation: true
---

# Add Data Entry Form Skill

## Purpose

Generate a client-side data entry form component that inserts records into Supabase, following Arch Systems patterns for state management, validation, styling, and shift handling.

## Process

### 1. Ask for form details

- **table** — Supabase table name (e.g. `operational_delays`)
- **fields** — List of fields with: name, type (`text` | `select` | `textarea` | `number` | `time` | `date` | `shift`), required (boolean), options (for select fields)
- **department** — Which department slug this form belongs to
- **include shift** — Should the form include a day/night shift toggle? (default: true for operational forms)
- **redirect after submit** — Stay on page or redirect? (default: stay, show success message)

### 2. Generate the form component

Create `apps/portal/app/(departments)/[department]/<tabName>/<FormName>Form.tsx`:

```tsx
"use client";

import { useState } from "react";
import { createClient } from "@repo/supabase/client";
import { useRouter } from "next/navigation";
import { GlassCard } from "@repo/ui/GlassCard";
import { cn } from "@repo/ui/lib/utils";

// Auto-detect current shift
const getCurrentShift = (): "day" | "night" => {
  const hour = new Date().getHours();
  return hour >= 6 && hour < 18 ? "day" : "night";
};

interface <FormName>FormProps {
  departmentId: string;
  departmentSlug: string;
}

export function <FormName>Form({
  departmentId,
}: <FormName>FormProps) {
  const router = useRouter();
  const supabase = createClient();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [status, setStatus] = useState<"idle" | "success" | "error">("idle");
  const [error, setError] = useState<string | null>(null);

  const [formData, setFormData] = useState({
    // ... field initial values
  });

  const validate = (): Record<string, string> => {
    const errors: Record<string, string> = {};
    // ... validation logic
    return errors;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const errors = validate();
    if (Object.keys(errors).length > 0) {
      setError(Object.values(errors).join(", "));
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      const { error: insertError } = await supabase
        .from("<table>")
        .insert({
          department_id: departmentId,
          ...formData,
        });

      if (insertError) throw insertError;

      setStatus("success");
      router.refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to submit");
      setStatus("error");
    } finally {
      setIsSubmitting(false);
    }
  };

  if (status === "success") {
    return (
      <GlassCard>
        <p className="text-[var(--accent-green)] text-sm font-medium">
          Record submitted successfully
        </p>
        <button
          onClick={() => setStatus("idle")}
          className="mt-2 text-[var(--accent-blue)] hover:underline text-sm"
        >
          Submit another
        </button>
      </GlassCard>
    );
  }

  return (
    <GlassCard>
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Shift toggle (if included) */}
        <div className="flex gap-2">
          {(["day", "night"] as const).map((shift) => (
            <button
              key={shift}
              type="button"
              onClick={() => setFormData({ ...formData, shift: shift })}
              className={cn(
                "flex-1 py-2 rounded-lg text-sm font-medium transition-colors",
                formData.shift === shift
                  ? "bg-white/80 shadow-card text-[var(--text-heading)]"
                  : "bg-white/40 text-[var(--text-secondary)] border border-black/[0.08]",
              )}
            >
              {shift === "day" ? "Day Shift (06:00–18:00)" : "Night Shift (18:00–06:00)"}
            </button>
          ))}
        </div>

        {/* Form fields — generated based on field list */}
        {/* Text input pattern: */}
        <div>
          <label className="block text-sm text-[var(--text-secondary)] mb-1"><Label></label>
          <input
            type="text"
            value={formData.<field>}
            onChange={(e) => setFormData({ ...formData, <field>: e.target.value })}
            className="w-full bg-white/70 border border-black/[0.08] rounded-lg px-3 py-2.5 text-[var(--text-primary)] text-sm focus:outline-none focus:border-[var(--accent-blue)] transition-colors"
            required
          />
        </div>

        {/* Select pattern: */}
        <div>
          <label className="block text-sm text-[var(--text-secondary)] mb-1"><Label></label>
          <select
            value={formData.<field>}
            onChange={(e) => setFormData({ ...formData, <field>: e.target.value })}
            className="w-full bg-white/70 border border-black/[0.08] rounded-lg px-3 py-2.5 text-[var(--text-primary)] text-sm focus:outline-none focus:border-[var(--accent-blue)] transition-colors"
            required
          >
            <option value="">Select...</option>
            {/* options from props */}
          </select>
        </div>

        {/* Textarea pattern: */}
        <div>
          <label className="block text-sm text-[var(--text-secondary)] mb-1"><Label></label>
          <textarea
            value={formData.<field>}
            onChange={(e) => setFormData({ ...formData, <field>: e.target.value })}
            rows={3}
            className="w-full bg-white/70 border border-black/[0.08] rounded-lg px-3 py-2.5 text-[var(--text-primary)] text-sm focus:outline-none focus:border-[var(--accent-blue)] transition-colors resize-none"
          />
        </div>

        {/* Error display */}
        {error && <p className="text-[var(--accent-red)] text-sm">{error}</p>}

        {/* Submit button */}
        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full bg-[var(--accent-blue)] hover:brightness-110 disabled:bg-black/[0.06] disabled:text-[var(--text-muted)] text-white font-medium py-2.5 px-6 rounded-lg transition-all"
        >
          {isSubmitting ? "Submitting..." : "Submit"}
        </button>
      </form>
    </GlassCard>
  );
}
```

### 3. Wire into the page component

In the corresponding `page.tsx`, import the form and pass required props:

```tsx
import { <FormName>Form } from "./<FormName>Form";

// ... inside the page component, after fetching data:
<<FormName>Form
  departmentId={deptId}
  departmentSlug={params.department}
/>
```

### 4. Verify

1. Navigate to the tab page in the browser
2. Test form submission with valid data
3. Test form validation with missing required fields
4. Test shift toggle (if included)
5. Commit changes

## Design System Reminders

- **Theme**: Light-only macOS Sonoma. Never use dark hex colors (`#171717`, `#363636`, `#fafafa`).
- **Input styling**: `w-full bg-white/70 border border-black/[0.08] rounded-lg px-3 py-2.5 text-[var(--text-primary)] text-sm focus:outline-none focus:border-[var(--accent-blue)] transition-colors`
- **Textarea**: add `resize-none`
- **Submit button**: `w-full bg-[var(--accent-blue)] hover:brightness-110 disabled:bg-black/[0.06] disabled:text-[var(--text-muted)] text-white font-medium py-2.5 px-6 rounded-lg transition-all`
- **Shift toggle active**: `bg-white/80 shadow-card text-[var(--text-heading)]`
- **Shift toggle inactive**: `bg-white/40 text-[var(--text-secondary)] border border-black/[0.08]`
- **Labels**: `text-sm text-[var(--text-secondary)]`
- **Error text**: `text-sm text-[var(--accent-red)]`
- Import Supabase from `@repo/supabase/client` (browser) for forms
- Use `cn()` from `@repo/ui/lib/utils` for conditional classes