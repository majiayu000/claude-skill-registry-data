---
name: new-component
description: Use when creating a new React component — scaffolds with ZAO OS conventions (use client, dark theme, mobile-first, Tailwind v4)
disable-model-invocation: true
argument-hint: "[feature/ComponentName] e.g. music/TrackCard"
---

# New Component — Scaffold a ZAO OS Component

Creates a new component following all conventions from `.claude/rules/components.md`.

## Usage

```
/new-component music/TrackCard
```

Creates `src/components/music/TrackCard.tsx`.

## Scaffold Template

```tsx
"use client";

import { useState } from "react";
// Use @/ alias for ALL project imports, e.g.:
// import { someUtil } from "@/lib/utils";
// import { SomeComponent } from "@/components/shared/SomeComponent";

interface TrackCardProps {
  /** Define props here */
  title: string;
}

export default function TrackCard({ title }: TrackCardProps) {
  return (
    <div className="bg-[#0a1628] text-white rounded-lg p-3 sm:p-4 md:p-6">
      <h2 className="text-sm sm:text-base md:text-lg font-semibold text-[#f5a623]">
        {title}
      </h2>
    </div>
  );
}
```

## Rules (ALL are mandatory — every generated component MUST satisfy each one)

1. **`"use client"` directive** — ALWAYS include `"use client";` as the very first line. Every scaffolded component is interactive.
2. **Dark theme colors in markup** — The root element MUST use `bg-[#0a1628]`. Use `text-[#f5a623]` for primary accent elements (headings, icons, active states). Do NOT omit these hex values or substitute other colors.
3. **`@/` import alias** — ALL project imports MUST use the `@/` path alias (e.g., `@/lib/`, `@/components/`, `@/hooks/`). NEVER use relative paths like `../../`. Only external packages (react, next) use bare specifiers.
4. **TypeScript props interface** — ALWAYS define an `interface [ComponentName]Props` with at least one typed prop. Destructure props in the function signature.
5. **Responsive prefixes in className** — ALWAYS include at least one Tailwind responsive prefix (`sm:`, `md:`, or `lg:`) on an actual element's className. Do NOT rely on comments alone — the responsive class must appear in rendered markup (e.g., `p-3 sm:p-4 md:p-6`).

### Additional conventions

- Use `next/dynamic` with `{ ssr: false }` for heavy components
- Use Tailwind CSS v4 classes — no inline styles or CSS modules
- PascalCase file names matching the component name
- Ask the user what the component should do before writing
