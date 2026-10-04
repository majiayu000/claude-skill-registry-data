---
name: tac-fourteen-laws
description: >-
  MANDATORY reference for any code change, install, or PR review in tac-express. Contains the Fourteen Laws, the forbidden-package list, the architecture flow rule, plus violation patterns and remediation snippets for each law. Load whenever uncertain whether something is allowed.
---

# TAC Express — The Fourteen Laws

These are **absolute laws**. No exceptions. No "just this once." Violating any of them blocks CI and is grounds for PR rejection. If a user asks you to violate a law, **STOP** and propose a compliant alternative.

> Authoritative source: `AGENTS.md` § 4 (which absorbed the former `PROJECT-RULES.md` in the May 2026 consolidation). This skill is the working reference for agents — same rules, with violation patterns + fixes.

---

## The Laws

### LAW 1 — No color value outside `globals.css`

| Pattern | Verdict | Fix |
|---|---|---|
| `className="bg-[#7c3aed]"` | ❌ raw hex | `className="bg-primary"` |
| `style={{ color: "rgb(...)" }}` | ❌ inline RGB | use semantic token utility |
| `border-color: oklch(...)` in component CSS | ❌ raw OKLCH | add a token to `globals.css` and reference it |
| `--my-color: oklch(...)` declared inside a component | ❌ scoped color literal | move to `globals.css` |

### LAW 2 — Icons via `@workspace/ui/icons` only (Remix Icon)

```tsx
// ❌ Forbidden:
import { ArrowRight } from "lucide-react"
import { IconArrowRight } from "@tabler/icons-react"
import { FiArrowRight } from "react-icons/fi"

// ✅ Required:
import { RiArrowRightLine } from "@workspace/ui/icons"
// or directly:
import { RiArrowRightLine } from "@remixicon/react"

<RiArrowRightLine className="size-5 text-muted-foreground" aria-hidden="true" />
```

### LAW 3 — Animation only via `motion` / `tw-animate-css` / `@keyframes` in globals.css

```tsx
// ❌ Forbidden (legacy package — name was changed):
import { motion } from "framer-motion"
import gsap from "gsap"
import { animate } from "@motionone/react"

// ✅ Required (the new motion/react package, which the project depends on):
import { motion } from "motion/react"

// ✅ Or pure utility classes:
<div className="animate-in fade-in-0 slide-in-from-bottom-4 duration-300" />

// ✅ Or @keyframes defined in packages/ui/src/styles/globals.css:
<div className="tac-scanline" />
```

### LAW 4 — Fonts declared only in the two `app/layout.tsx` files

```tsx
// ✅ The only legal places fonts are loaded:
//    apps/web/app/layout.tsx
//    apps/dashboard/app/layout.tsx
import { Plus_Jakarta_Sans, IBM_Plex_Mono, Lora } from "next/font/google"

// ❌ Forbidden — fonts loaded anywhere else:
//    packages/ui/fonts.ts                   ← legacy, removed
//    apps/web/components/some-component.tsx ← never
//    @import url("https://fonts.googleapis.com/...") in a CSS file ← never
```

### LAW 5 — UI components only in `packages/ui`

```
✅ packages/ui/src/components/primitives/button.tsx
✅ packages/ui/src/components/composed/shipments/shipment-card.tsx

❌ apps/web/components/MyButton.tsx          ← move to packages/ui
❌ apps/dashboard/components/data-grid.tsx   ← move to packages/ui

Acceptable in apps/<app>/components/ ONLY:
- Provider composition (providers.tsx wrapping QueryClient + ThemeProvider + Toaster)
- App-shell glue (idle-guard wrapper around a UI component)
- Page-level client wrappers that thread server props into a UI component
```

### LAW 6 — No DB calls in components

```tsx
// ❌ Forbidden in any component file:
const { data } = await supabase.from("shipments").select("*")
const { data } = useQuery(["x"], () => supabase.from("x").select())

// ✅ Components use service hooks:
import { useShipments } from "@workspace/services/hooks/use-shipments"
const { data, isLoading } = useShipments(filters)
```

### LAW 7 — No business logic in components

```tsx
// ❌ Computing rates / running validations / merging entities in render:
const shippingCost = baseRate * weight + zoneSurcharge - couponDiscount

// ✅ Service computes it; component just displays:
const { quote } = useQuote(input)  // hook calls quoteService.calculate(input)
<span>{formatCurrency(quote.total)}</span>
```

### LAW 8 — `@supabase/supabase-js` only in `packages/database`

```ts
// ❌ Forbidden anywhere in apps/ or other packages/:
import { createClient } from "@supabase/supabase-js"

// ✅ The single legal home:
//    packages/database/src/client.ts (browser + server)
//    packages/database/src/middleware.ts
//    packages/database/src/admin.ts (service-role)

// Consumers import factories:
import { createBrowserClient } from "@workspace/database"
```

### LAW 9 — No hardcoded spacing / radius / shadow

```tsx
// ❌ Forbidden:
className="p-[17px] rounded-[6px] shadow-[0_2px_8px_rgba(0,0,0,0.1)]"
style={{ padding: "17px", borderRadius: "6px" }}

// ✅ Use scale tokens:
className="p-4 rounded-none shadow-sm"   // shadow-sm = brutalist 3px offset
className="p-4 shadow-[var(--shadow-brutal)]"  // alias to shadow-md (6px)
```

### LAW 10 — No Tailwind color classes

```tsx
// ❌ Forbidden:
className="bg-blue-500 text-red-400 border-green-300"

// ✅ Semantic tokens only:
className="bg-primary text-accent-danger border-accent-success"
```

Status mapping (memorize):
- delivered / paid / healthy → `bg-accent-success` / `text-accent-success`
- in-transit / due-soon / attention → `bg-accent-warning`
- delayed / breached / error → `bg-accent-danger` / `text-accent-danger`
- data signal / info → `bg-accent-info` (= primary violet)

### LAW 11 — No arbitrary Tailwind values

```tsx
// ❌ Forbidden:
className="w-[347px] h-[52px] m-[13px] gap-[7px]"

// ✅ Scale tokens only:
className="w-80 h-12 m-3 gap-2"

// Need a special width? Add a token to globals.css; don't inline it.
```

### LAW 12 — `pnpm` only

```bash
# ❌ Forbidden:
npm install
yarn add foo
npx some-tool

# ✅ Required:
pnpm install
pnpm add foo
pnpm dlx some-tool
```

### LAW 13 — Straight lines only

```
❌ rounded-full / rounded-2xl / rounded-lg with non-zero radius
❌ SVG paths with curve commands: C, S, Q, T, A
❌ border-radius: 50% / 9999px
❌ Wavy decorations / blob shapes / organic gradients

✅ rounded-none everywhere (var(--radius) = 0rem)
✅ SVG paths with M / L / H / V / Z only
✅ Crosshairs, brackets, hazard stripes, scanlines, grids
```

### LAW 14 — Wrap shadcn primitives, never rebuild

```tsx
// ❌ Forbidden — rolling your own modal:
<div role="dialog" onKeyDown={handleEsc}>...</div>

// ✅ Always wrap the shadcn primitive (which wraps the Radix primitive):
import { Dialog, DialogContent, DialogTrigger } from "@workspace/ui/components/primitives/dialog"
```

If a primitive doesn't exist yet, run `pnpm dlx shadcn@latest add <name>` from the workspace root — it installs into `packages/ui/`, never into apps.

---

## Forbidden Packages (Never Install — Ever)

```
lucide-react              framer-motion (legacy package name)
@motionone/react          gsap
styled-components         @mui/material
antd                      chakra-ui
react-icons               @tabler/icons-react
moment                    lodash
axios                     classnames
clsx                      ← use cn from @workspace/ui/lib/utils
```

`motion` (the new package — same publisher as framer-motion) IS allowed. `@anthropic-ai/sdk`, `recharts`, `react-hook-form`, `@hookform/resolvers`, `zod`, `@upstash/ratelimit`, `@upstash/redis`, `@tanstack/react-query` are all allowed in their phase-gated locations (see `AGENTS.md` § 11).

---

## Architecture Flow

```
UI Component
   ↓  (props / hooks only)
packages/services/   ← business logic per domain
   ↓  (typed function calls only)
packages/database/   ← @supabase/* SDK lives here, factory pattern
   ↓
Supabase (cloud)
```

No skipping. No shortcuts. Ever.

---

## Response Protocol When Asked to Violate a Law

> "I can't do that — it violates **LAW [N]** from `AGENTS.md`. Here's the compliant approach: [alternative]."

Don't soften, don't apologize, don't ask for permission to break it. Show the fix.
