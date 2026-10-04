---
name: premium-stats-component
description: Pattern for creating premium statistics card components in JKKN COE Next.js application. This skill should be used when adding dashboard statistics, scorecards, metrics display, or summary cards to entity pages. Automatically triggers when user mentions 'stats', 'statistics', 'scorecard', 'metrics', 'dashboard cards', 'summary cards', or 'counts display'.
---

# Premium Stats Component Skill

This skill provides patterns for creating consistent, visually appealing statistics card components in the JKKN COE application.

## When to Use This Skill

Use this skill when:
- Adding summary statistics to entity listing pages
- Creating dashboard metric cards
- Displaying count-based information (Total, Active, Inactive, New)
- Building scorecards for data overview
- Implementing loading states for statistics

## File Locations (Following project-structure)

```
components/stats/
├── premium-[entity]-stats.tsx   # Entity-specific stats component
```

## Component Structure

### Basic Stats Component

```tsx
import { Card, CardContent } from "@/components/ui/card"
import { Building2, CheckCircle, XCircle, TrendingUp, LucideIcon } from "lucide-react"

interface Entity {
  id: string
  is_active: boolean
  created_at: string
  [key: string]: any
}

interface StatConfig {
  label: string
  value: number
  icon: LucideIcon
  iconBg: string
  iconColor: string
  valueColor: string
}

interface PremiumEntityStatsProps {
  items: Entity[]
  loading?: boolean
}

export function PremiumEntityStats({ items = [], loading = false }: PremiumEntityStatsProps) {
  // Calculate statistics
  const total = items.length
  const active = items.filter((i) => i.is_active).length
  const inactive = items.filter((i) => !i.is_active).length
  const newThisMonth = items.filter((i) => {
    const itemDate = new Date(i.created_at)
    const currentDate = new Date()
    return (
      itemDate.getMonth() === currentDate.getMonth() &&
      itemDate.getFullYear() === currentDate.getFullYear()
    )
  }).length

  // Define stat configurations
  const stats: StatConfig[] = [
    {
      label: "Total Entities",
      value: total,
      icon: Building2,
      iconBg: "bg-blue-50 dark:bg-blue-900/20",
      iconColor: "text-blue-600 dark:text-blue-400",
      valueColor: "text-slate-900 dark:text-slate-100",
    },
    {
      label: "Active",
      value: active,
      icon: CheckCircle,
      iconBg: "bg-emerald-50 dark:bg-emerald-900/20",
      iconColor: "text-emerald-600 dark:text-emerald-400",
      valueColor: "text-emerald-600 dark:text-emerald-400",
    },
    {
      label: "Inactive",
      value: inactive,
      icon: XCircle,
      iconBg: "bg-red-50 dark:bg-red-900/20",
      iconColor: "text-red-600 dark:text-red-400",
      valueColor: "text-red-600 dark:text-red-400",
    },
    {
      label: "New This Month",
      value: newThisMonth,
      icon: TrendingUp,
      iconBg: "bg-purple-50 dark:bg-purple-900/20",
      iconColor: "text-purple-600 dark:text-purple-400",
      valueColor: "text-purple-600 dark:text-purple-400",
    },
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {stats.map((stat, index) => (
        <div key={index} className="card-premium-hover p-2">
          <Card>
            <CardContent className="p-3">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-slate-600 dark:text-slate-400">
                    {stat.label}
                  </p>
                  {loading ? (
                    <div className="h-9 w-20 bg-slate-200 dark:bg-slate-700 animate-pulse rounded mt-1" />
                  ) : (
                    <p
                      className={`text-3xl font-bold mt-1 font-grotesk ${stat.valueColor}`}
                      aria-label={`${stat.label}: ${stat.value}`}
                    >
                      {stat.value}
                    </p>
                  )}
                </div>
                <div
                  className={`h-12 w-12 rounded-xl flex items-center justify-center ${stat.iconBg}`}
                  aria-hidden="true"
                >
                  <stat.icon className={`h-6 w-6 ${stat.iconColor}`} />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      ))}
    </div>
  )
}
```

## Color Scheme Reference

### Standard 4-Card Layout

| Card | Color | Icon | Use Case |
|------|-------|------|----------|
| Total | Blue | Building2/Package/Users | Total count |
| Active | Green/Emerald | CheckCircle | Active items |
| Inactive | Red | XCircle | Inactive items |
| New | Purple | TrendingUp | New this month |

### Color Classes

```typescript
// Blue (Total)
iconBg: "bg-blue-50 dark:bg-blue-900/20"
iconColor: "text-blue-600 dark:text-blue-400"
valueColor: "text-slate-900 dark:text-slate-100"

// Green/Emerald (Active)
iconBg: "bg-emerald-50 dark:bg-emerald-900/20"
iconColor: "text-emerald-600 dark:text-emerald-400"
valueColor: "text-emerald-600 dark:text-emerald-400"

// Red (Inactive)
iconBg: "bg-red-50 dark:bg-red-900/20"
iconColor: "text-red-600 dark:text-red-400"
valueColor: "text-red-600 dark:text-red-400"

// Purple (New/Trending)
iconBg: "bg-purple-50 dark:bg-purple-900/20"
iconColor: "text-purple-600 dark:text-purple-400"
valueColor: "text-purple-600 dark:text-purple-400"

// Orange (Warning/Pending)
iconBg: "bg-orange-50 dark:bg-orange-900/20"
iconColor: "text-orange-600 dark:text-orange-400"
valueColor: "text-orange-600 dark:text-orange-400"

// Indigo (Special)
iconBg: "bg-indigo-50 dark:bg-indigo-900/20"
iconColor: "text-indigo-600 dark:text-indigo-400"
valueColor: "text-indigo-600 dark:text-indigo-400"
```

## Icon Reference

Common icons for stats cards:

```typescript
import {
  Building2,      // Institutions
  GraduationCap,  // Students/Education
  BookOpen,       // Courses
  Users,          // Users/Groups
  UserCheck,      // Active Users
  UserX,          // Inactive Users
  CheckCircle,    // Active/Complete
  XCircle,        // Inactive/Failed
  TrendingUp,     // Growth/New
  TrendingDown,   // Decline
  Calendar,       // Time-based
  Clock,          // Pending
  AlertTriangle,  // Warning
  Award,          // Achievements
  Package,        // Items/Products
  FileText,       // Documents
  Settings,       // Configuration
} from "lucide-react"
```

## Usage in Page

```tsx
import { PremiumEntityStats } from "@/components/stats/premium-entity-stats"

export default function EntityPage() {
  const [items, setItems] = useState<Entity[]>([])
  const [loading, setLoading] = useState(true)

  return (
    <div className="flex flex-1 flex-col gap-3 p-4 pt-0">
      {/* Breadcrumb */}

      {/* Premium Stats Cards */}
      <PremiumEntityStats items={items} loading={loading} />

      {/* Data Table Card */}
    </div>
  )
}
```

## Responsive Grid Classes

```tsx
// 4 cards (standard)
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">

// 3 cards
<div className="grid grid-cols-1 md:grid-cols-3 gap-4">

// 5 cards
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">

// 6 cards (2 rows of 3)
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
```

## Loading State Pattern

```tsx
{loading ? (
  <div className="h-9 w-20 bg-slate-200 dark:bg-slate-700 animate-pulse rounded mt-1" />
) : (
  <p className={`text-3xl font-bold mt-1 font-grotesk ${stat.valueColor}`}>
    {stat.value}
  </p>
)}
```

## Custom Calculations

### Percentage Calculation

```typescript
const activePercentage = total > 0
  ? Math.round((active / total) * 100)
  : 0

// Display as "85%"
{
  label: "Active Rate",
  value: `${activePercentage}%`,
  // ...
}
```

### Filtered Count

```typescript
const pendingApproval = items.filter((i) =>
  i.status === 'pending' && i.submitted_at
).length
```

### Date-Based Count

```typescript
const newThisWeek = items.filter((i) => {
  const itemDate = new Date(i.created_at)
  const weekAgo = new Date()
  weekAgo.setDate(weekAgo.getDate() - 7)
  return itemDate >= weekAgo
}).length
```

## Accessibility

```tsx
<p
  className={`text-3xl font-bold mt-1 ${stat.valueColor}`}
  aria-label={`${stat.label}: ${stat.value}`}
>
  {stat.value}
</p>

<div
  className={`h-12 w-12 rounded-xl flex items-center justify-center ${stat.iconBg}`}
  aria-hidden="true"
>
  <stat.icon className={`h-6 w-6 ${stat.iconColor}`} />
</div>
```

## Complete Example: Course Stats

See `references/course-stats-example.md` for a complete implementation with custom metrics.

## Testing Checklist

- [ ] Stats display correct counts
- [ ] Loading state shows skeleton
- [ ] Responsive layout on mobile/tablet/desktop
- [ ] Dark mode colors correct
- [ ] Accessibility labels present
- [ ] New this month calculation accurate
- [ ] Active/Inactive counts match data
