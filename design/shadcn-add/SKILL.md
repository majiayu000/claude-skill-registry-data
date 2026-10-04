---
name: shadcn-add
description: Add or update shadcn/ui components for FixNow by running the official shadcn CLI. Never copy component source from the shadcn-ui/ui repo by hand. Use this when the user says "them component button", "cai shadcn select", "shadcn table", "init shadcn", or whenever a required component is missing from components/ui/.
---

# shadcn-add

shadcn/ui la SOURCE OF TRUTH cho UI primitives. KHONG copy code thu cong tu repo shadcn-ui/ui — luon dung CLI chinh thuc.

## Khi nao dung

- Lan dau setup: chua co `components.json` -> chay `init`.
- Mot trang/component can primitive moi (vd: `<Button>`, `<Select>`, `<Table>`).
- Muon nang cap mot primitive da co (re-add se overwrite, can confirm).

## Workflow

### 1. Verify init da chay

Kiem tra `components.json` o root. Neu chua co:

```bash
npx shadcn@latest init
```

Khi prompt:
- Style: `new-york` (clean, gon, hop voi FixNow).
- Base color: `slate`.
- CSS variables: `yes`.
- React Server Components: `yes` (vi Next.js App Router).
- Import alias: `@/*`.

### 2. Add component

```bash
npx shadcn@latest add <name>
```

Vi du:
```bash
npx shadcn@latest add button input label form card
npx shadcn@latest add select textarea dialog
npx shadcn@latest add table badge toast sheet
```

CLI se:
- Tao file vao `components/ui/<name>.tsx`.
- Cai deps neu can (radix primitives, cva, ...).
- KHONG ghi de neu file da ton tai (tru khi them `--overwrite`).

### 3. Bo components da co tren shadcn registry

| MVP need | Component |
|----------|-----------|
| Button, link CTA | button |
| Form input | input, label, form, textarea |
| Select | select |
| Card (dich vu, lich hen) | card |
| Status badge | badge |
| Toast thong bao | toast |
| Mobile drawer menu | sheet |
| Confirm modal | dialog |
| Bang lich hen admin | table |
| Filter dropdown | dropdown-menu |

### 4. KHONG sua file `components/ui/*` tay

- Generated boi CLI -> giu nguyen.
- Neu can extend behavior -> WRAP trong component moi tai `components/features/`:

```tsx
// components/features/primary-cta.tsx
'use client';
import { Button } from '@/components/ui/button';
import { ArrowRight } from 'lucide-react';

export function PrimaryCTA({ href, label }: { href: string; label: string }) {
  return (
    <Button asChild size="lg" className="w-full md:w-auto">
      <a href={href}>{label} <ArrowRight className="ml-2 h-4 w-4" /></a>
    </Button>
  );
}
```

### 5. Khi nang cap shadcn

```bash
npx shadcn@latest diff
npx shadcn@latest add <component> --overwrite
```

Confirm voi user truoc khi --overwrite vi co the mat custom changes (neu co lo).

## Liem ket khi component KHONG co tren shadcn

shadcn co `~50` core components. Neu can them complex pattern (date picker, multi-step form, charts) -> check:

1. shadcn registry mo rong (community blocks): https://ui.shadcn.com/blocks
2. Radix UI primitives truc tiep (vi shadcn dua tren radix).
3. Tu viet trong `components/features/` dung Tailwind + radix theo design system o `docs/ui-system.md`.

## Checklist sau khi add

- [ ] File da xuat hien o `components/ui/<name>.tsx`.
- [ ] Deps moi da cai (kiem tra `package.json`).
- [ ] Import bang `@/components/ui/<name>` o file su dung.
- [ ] Test render o trang 375px va 1280px.
- [ ] Khong sua truc tiep file ui/ -- wrap o features/.

## Khong lam

- KHONG `git clone shadcn-ui/ui` vao project.
- KHONG copy component source manually tu github.com/shadcn-ui/ui.
- KHONG sua file `components/ui/*.tsx` tay (tru khi dong bo voi CLI registry).
