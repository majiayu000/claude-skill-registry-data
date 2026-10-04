---
name: atomic-page-builder
description: Build pages using ONLY existing atomic-design components. REQUIRES atomic-design skill. Use for composing pages, creating views/features from existing components.
---

# Atomic Page Builder

Critical rule: Figma is source of truth. NEVER guess layout. ALWAYS extract EXACT page specs from Figma first.

## Rules

| Forbidden | Required |
|---|---|
| Creating new atoms/molecules/organisms | Use existing components only |
| Guessing layout values | Extract from Figma |
| External UI libs (MUI, Chakra) | Design system imports only |
| Hardcoded values (#333, 24px) | CSS Modules + tokens |
| Rounding values | Exact Figma values |

## Skill Switching

| Situation | Action |
|---|---|
| Missing atom/molecule/organism | -> atomic-design |
| Need new tokens | -> atomic-design |
| Token value changed in Figma | -> atomic-design (update first) |
| Composing from existing | Stay here |

## Workflow

Step 0: EXTRACT FROM FIGMA (mandatory)
- Use Figma MCP: get_node
- Extract: grid, gaps, padding, margins
- Identify components used
- Note page-specific overrides
- Compare with tokens: check spacing tokens match Figma; if different -> UPDATE tokens (Figma wins)

Step 1: INVENTORY (scan existing components)

Step 2: GAP ANALYSIS (map requirements to components)

Step 3: BUILD OR STOP
- All exist? -> Compose page, matching Figma layout 1:1, NO "improvements"
- Missing? -> STOP, report gaps, switch to atomic-design

## Page Composition

```tsx
/**
 * Dashboard Page
 * @figma https://figma.com/file/xxx?node-id=123
 * @extracted 2024-01-15
 * Layout specs from Figma - DO NOT MODIFY
 */

import { DashboardLayout } from '@/templates/DashboardLayout';
import { Card } from '@/molecules/Card';
import { DataTable } from '@/organisms/DataTable';
import styles from './Dashboard.module.css';

export const Dashboard = () => (
  <DashboardLayout>
    <div className={styles.statsGrid}>
      <Card title="Revenue">$12,450</Card>
    </div>
    <DataTable columns={columns} data={data} />
  </DashboardLayout>
);
```

```css
/* Dashboard.module.css - ALL values from Figma */
.statsGrid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);  /* From Figma */
  gap: var(--spacing-6);                   /* From Figma */
}

@media (max-width: 768px) {
  .statsGrid {
    grid-template-columns: 1fr;            /* Figma mobile */
    gap: var(--spacing-4);
  }
}
```

## Import Pattern

```tsx
import { Button } from '@/design-system/atoms/Button';
import { Card } from '@/design-system/molecules/Card';
import { Header } from '@/design-system/organisms/Header';
import { DashboardLayout } from '@/design-system/templates/DashboardLayout';
```

## Details

- Figma extraction steps: references/figma-extraction-guide.md
- Component inventory format: references/component-inventory-template.md
- Layout/composition patterns: references/page-composition-patterns.md

## Output Checklist

- [ ] Page specs extracted from Figma
- [ ] Layout values match Figma exactly
- [ ] Responsive matches Figma
- [ ] Visual comparison 0% difference
- [ ] Figma link documented
- [ ] All imports from design system
- [ ] Zero hardcoded values
- [ ] Zero new components
