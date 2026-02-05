# Addon/Feature System Development Guide

**Version:** 1.0
**Purpose:** Enforce consistent patterns when creating new features/addons with proper feature gates

## 🎯 Quick Reference

When adding a new feature/addon to the platform, you MUST:
- ✅ Define a unique FEATURE_CODE
- ✅ Create feature file in `src/lib/features/`
- ✅ Create custom hook (`useXyzFeature`)
- ✅ Create Feature Gates (User + Admin)
- ✅ Use theme system for upgrade prompts
- ✅ Register feature in database

## 📚 Architecture Overview

```
Feature System Flow:
1. Database (feature_definitions) → Feature Code
2. Studio Subscription/Addon → Active Features
3. FeatureProvider → Context with hasFeature(), canUse()
4. Feature Gates → Conditional Rendering
5. Components → Protected Features
```

## 🔧 Step-by-Step: Creating a New Addon

### Step 1: Define Feature Code

```typescript
// src/lib/features/my-feature.tsx
'use client'

export const MY_FEATURE_CODE = 'my_feature_name'
```

**Naming Convention:**
- Use snake_case: `chat_messaging`, `studio_blog`, `checkin_system`
- Be descriptive: `video_on_demand` not `vod`
- Must match database entry in `feature_definitions.code`

### Step 2: Create Custom Hook

```typescript
// src/lib/features/my-feature.tsx
import { useFeatures } from './feature-context'

export function useMyFeature() {
  const { hasFeature, canUse, loading } = useFeatures()

  return {
    // Ist das Feature aktiviert?
    isMyFeatureEnabled: hasFeature(MY_FEATURE_CODE),

    // Kann Feature genutzt werden? (Aktiv + Subscription gültig)
    canUseMyFeature: canUse(MY_FEATURE_CODE),

    // Lädt noch?
    loading: loading,

    // Feature Code für andere Components
    featureCode: MY_FEATURE_CODE
  }
}
```

**What the hook returns:**
- `isMyFeatureEnabled`: Feature exists in studio's active features
- `canUseMyFeature`: Feature exists AND subscription is active
- `loading`: True während features geladen werden
- `featureCode`: Der Feature-Code für generic components

### Step 3: Create Feature Gates

#### A) Simple Feature Gate (für User/Frontend)

```typescript
// src/lib/features/my-feature.tsx
import React from 'react'

export function MyFeatureGate({ children }: { children: React.ReactNode }) {
  const { canUseMyFeature, loading } = useMyFeature()

  // Während Laden: nichts anzeigen
  if (loading) return null

  // Feature nicht aktiv: nichts anzeigen
  if (!canUseMyFeature) return null

  return <>{children}</>
}
```

#### B) Admin Feature Gate (mit Upgrade-Hinweis)

```typescript
// src/lib/features/my-feature.tsx
import { activeTheme } from '@/config/theme'
import { H3 } from '@/components/ui/Typography'

export function AdminMyFeatureGate({
  children,
  fallback
}: {
  children: React.ReactNode
  fallback?: React.ReactNode
}) {
  const { isMyFeatureEnabled, loading } = useMyFeature()

  // Während Laden: Render children (Page hat eigene Loading-States)
  if (loading) {
    return <>{children}</>
  }

  // Custom Fallback?
  if (!isMyFeatureEnabled && fallback) {
    return <>{fallback}</>
  }

  // Feature nicht aktiv: Upgrade-Hinweis
  if (!isMyFeatureEnabled) {
    return (
      <div className="p-8 text-center">
        <div className="max-w-md mx-auto">
          <svg
            className="w-16 h-16 text-[rgb(23,23,23)] mx-auto mb-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={1.5}
              d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
            />
          </svg>
          <H3 className="mb-2">
            My Feature nicht aktiviert
          </H3>
          <p className="text-[rgb(23,23,23)] mb-4">
            Dieses Feature ist in Ihrem aktuellen Tarif nicht enthalten.
          </p>
          <a
            href="/admin/einstellungen/tarife"
            className={\`inline-flex items-center px-4 py-2 bg-gradient-to-r \${activeTheme.gradient} text-white rounded-lg hover:opacity-90 transition-all\`}
          >
            Tarif upgraden
          </a>
        </div>
      </div>
    )
  }

  return <>{children}</>
}
```

### Step 4: Use in Components

#### Option A: With Custom Feature Gate

```typescript
// In your component
import { MyFeatureGate } from '@/lib/features/my-feature'

export default function MyPage() {
  return (
    <MyFeatureGate>
      {/* This only renders if feature is active */}
      <div>Feature Content</div>
    </MyFeatureGate>
  )
}
```

#### Option B: With Generic FeatureGate

```typescript
import { FeatureGate } from '@/components/features/FeatureGate'

export default function MyPage() {
  return (
    <FeatureGate feature="my_feature_name">
      <div>Feature Content</div>
    </FeatureGate>
  )
}
```

#### Option C: Conditional Rendering with Hook

```typescript
import { useMyFeature } from '@/lib/features/my-feature'

export default function MyComponent() {
  const { canUseMyFeature, loading } = useMyFeature()

  if (loading) return <LoadingSpinner />
  if (!canUseMyFeature) return null

  return <div>Feature Content</div>
}
```

### Step 5: Stripe Product erstellen

**WICHTIG:** Jedes Addon braucht ein Stripe Product, damit bei Studio-Erstellung keine neuen Produkte erstellt werden!

#### A) Stripe Product anlegen

```javascript
// Via Node.js Script oder Stripe Dashboard
require('dotenv').config({ path: '.env.local' });
const Stripe = require('stripe');
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

const product = await stripe.products.create({
  name: 'Bookicorn My Feature Name',  // Prefix "Bookicorn " für Konsistenz
  metadata: {
    feature_code: 'my_feature_name',  // Muss mit DB code übereinstimmen!
    type: 'addon'
  }
});

console.log('Product ID:', product.id);  // z.B. prod_TnXXXXXXXXXX
```

**Oder via Stripe Dashboard:**
1. Dashboard → Products → Add Product
2. Name: `Bookicorn [Feature Name]`
3. Metadata hinzufügen: `feature_code` = `my_feature_name`, `type` = `addon`

### Step 6: Database Setup

#### A) Register Feature Definition (mit Stripe Product ID!)

```sql
INSERT INTO feature_definitions (
  code,
  name,
  description,
  category,
  addon_price_monthly,
  addon_price_yearly,
  is_active,
  metadata
) VALUES (
  'my_feature_name',          -- Must match FEATURE_CODE
  'My Feature Name',
  'Description of what this feature does',
  'content',                   -- Category: core, content, marketing, etc.
  9.99,                        -- Monthly price (if sold as addon)
  99.99,                       -- Yearly price
  true,
  '{"status": "available", "stripe_product_id": "prod_TnXXXXXXXXXX"}'::jsonb
  --                          ↑ WICHTIG: Stripe Product ID hier eintragen!
);
```

#### Alternative: Bestehendes Feature updaten

```sql
UPDATE feature_definitions
SET metadata = metadata || '{"stripe_product_id": "prod_TnXXXXXXXXXX"}'::jsonb
WHERE code = 'my_feature_name';
```

#### B) Add to Subscription Plan (Optional)

```sql
-- Include feature in a plan
UPDATE subscription_plans
SET included_features = included_features || ARRAY['my_feature_name']
WHERE code = 'professional';
```

#### C) Or Create as Addon

```sql
-- Studio can buy as addon
INSERT INTO studio_feature_addons (
  studio_id,
  feature_id,
  status,
  billing_cycle,
  price_override
) VALUES (
  'studio-uuid',
  (SELECT id FROM feature_definitions WHERE code = 'my_feature_name'),
  'active',
  'monthly',
  NULL
);
```

## 📁 File Structure

```
src/
├── lib/
│   └── features/
│       ├── feature-context.tsx        # Admin/Studio Feature Provider
│       ├── member-feature-context.tsx # Member Dashboard Feature Provider (NEW)
│       ├── my-feature.tsx             # Your new feature
│       ├── chat-feature.tsx           # Example: Chat (Admin)
│       ├── blog-feature.ts            # Example: Blog
│       └── checkin-feature.tsx        # Example: Check-in
├── components/
│   └── features/
│       └── FeatureGate.tsx            # Generic Feature Gate
└── app/
    └── admin/
        └── my-feature/                # Admin pages for feature
            └── page.tsx
```

## 👤 Member Dashboard Feature Gates

**WICHTIG:** Das Member Dashboard hat ein SEPARATES Feature System (`MemberFeatureContext`), weil:
- Ein Kunde kann bei MEHREREN Studios Mitglied sein
- Features werden über ALLE Studios aggregiert
- Feature ist aktiv wenn MINDESTENS EIN Studio es hat

### MemberFeatureContext vs FeatureContext

| Aspekt | FeatureContext (Admin) | MemberFeatureContext (Member) |
|--------|------------------------|-------------------------------|
| Scope | Einzelnes Studio | Alle Studios des Users |
| Provider | `FeatureProvider` | `MemberFeatureProvider` |
| Hook | `useFeatures()` | `useMemberFeatures()` |
| Logik | Studio hat Feature? | Irgendein Studio hat Feature? |

### Member Feature Hook erstellen

```typescript
// src/lib/features/member-feature-context.tsx enthält:

// 1. Feature Codes Definition
export const MEMBER_FEATURE_CODES = {
  CHAT: 'chat_messaging',
  CHECKIN: 'checkin_system',
  // Neues Feature hier hinzufügen
  MY_FEATURE: 'my_feature_code',
} as const

// 2. Convenience Hooks existieren bereits:
export function useMemberChatFeature() { ... }
export function useMemberCheckinFeature() { ... }

// 3. Neuen Convenience Hook hinzufügen:
export function useMemberMyFeature() {
  const { hasFeature, hasFeatureInStudio, getStudiosWithFeature, loading } = useMemberFeatures()
  const featureCode = MEMBER_FEATURE_CODES.MY_FEATURE

  return {
    isMyFeatureEnabled: hasFeature(featureCode),
    hasMyFeatureInStudio: (studioId: string) => hasFeatureInStudio(featureCode, studioId),
    studiosWithMyFeature: getStudiosWithFeature(featureCode),
    loading,
    featureCode
  }
}
```

### Member Feature Gate erstellen

```typescript
// In member-feature-context.tsx oder eigene Datei

export function MemberMyFeatureGate({ children }: { children: React.ReactNode }) {
  return (
    <MemberFeatureGate feature={MEMBER_FEATURE_CODES.MY_FEATURE} silent>
      {children}
    </MemberFeatureGate>
  )
}
```

### Verwendung im Member Dashboard

```typescript
// src/app/dashboard/page.tsx oder Member-Komponenten

import { useMemberMyFeature, MEMBER_FEATURE_CODES } from '@/lib/features/member-feature-context'

export default function MemberDashboard() {
  // Option A: Mit spezifischem Hook
  const { isMyFeatureEnabled } = useMemberMyFeature()

  // Option B: Mit generischem Hook
  const { hasFeature } = useMemberFeatures()
  const hasMyFeature = hasFeature(MEMBER_FEATURE_CODES.MY_FEATURE)

  // Option C: Prüfen für spezifisches Studio
  const { hasFeatureInStudio } = useMemberFeatures()
  const studioHasFeature = hasFeatureInStudio('my_feature_code', studioId)

  return (
    <>
      {/* Bedingt rendern */}
      {isMyFeatureEnabled && (
        <MyFeatureSection />
      )}

      {/* Oder mit Gate Component */}
      <MemberMyFeatureGate>
        <MyFeatureSection />
      </MemberMyFeatureGate>
    </>
  )
}
```

### Navigation Items bedingt anzeigen

```typescript
// src/components/member/shared/MemberNavigation.tsx

export function MemberSidebar({ ... }: MemberNavigationProps) {
  // Feature von Props oder aus Context
  const hasChatAddon = props.hasChatAddon // Vom Dashboard durchgereicht

  return (
    <nav>
      {/* Immer sichtbare Items */}
      <NavItem icon={Home} label="Home" ... />
      <NavItem icon={Calendar} label="Kursplan" ... />

      {/* Bedingt sichtbar basierend auf Feature */}
      {hasChatAddon && (
        <NavItem icon={MessageSquare} label="Nachrichten" ... />
      )}
    </nav>
  )
}
```

### Wichtig: Studios mit MemberFeatureContext synchronisieren

```typescript
// src/components/member/hooks/useMemberData.ts

export function useMemberData({ userId }: UseMemberDataProps) {
  // Context für Feature Sync holen
  const { setStudios } = useMemberFeatures()

  const loadDashboardData = async () => {
    // ... Studios laden ...

    const allStudios = Array.from(allStudiosMap.values())
    setMyStudios(allStudios)

    // WICHTIG: Studios mit MemberFeatureContext synchronisieren
    setStudios(allStudios.map((s: any) => ({ id: s.id, name: s.name })))
  }
}
```

## 🎨 Complete Example: Video-on-Demand Feature

```typescript
// src/lib/features/vod-feature.tsx
'use client'
import React from 'react'
import { useFeatures } from './feature-context'
import { activeTheme } from '@/config/theme'
import { H3 } from '@/components/ui/Typography'

// 1. Define Feature Code
export const VOD_FEATURE_CODE = 'video_on_demand'

// 2. Custom Hook
export function useVodFeature() {
  const { hasFeature, canUse, loading } = useFeatures()

  return {
    isVodEnabled: hasFeature(VOD_FEATURE_CODE),
    canUseVod: canUse(VOD_FEATURE_CODE),
    loading: loading,
    featureCode: VOD_FEATURE_CODE
  }
}

// 3. User Feature Gate (simple)
export function VodFeatureGate({ children }: { children: React.ReactNode }) {
  const { canUseVod, loading } = useVodFeature()

  if (loading) return null
  if (!canUseVod) return null

  return <>{children}</>
}

// 4. Admin Feature Gate (with upgrade prompt)
export function AdminVodGate({
  children,
  fallback
}: {
  children: React.ReactNode
  fallback?: React.ReactNode
}) {
  const { isVodEnabled, loading } = useVodFeature()

  if (loading) {
    return <>{children}</>
  }

  if (!isVodEnabled && fallback) {
    return <>{fallback}</>
  }

  if (!isVodEnabled) {
    return (
      <div className="p-8 text-center">
        <div className="max-w-md mx-auto">
          <svg
            className="w-16 h-16 text-[rgb(23,23,23)] mx-auto mb-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={1.5}
              d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"
            />
          </svg>
          <H3 className="mb-2">
            Video-on-Demand nicht aktiviert
          </H3>
          <p className="text-[rgb(23,23,23)] mb-4">
            Das VOD Feature ist in Ihrem aktuellen Tarif nicht enthalten.
          </p>
          <a
            href="/admin/einstellungen/tarife"
            className={\`inline-flex items-center px-4 py-2 bg-gradient-to-r \${activeTheme.gradient} text-white rounded-lg hover:opacity-90 transition-all\`}
          >
            Tarif upgraden
          </a>
        </div>
      </div>
    )
  }

  return <>{children}</>
}
```

**Usage in Component:**

```typescript
// app/admin/videos/page.tsx
import { AdminVodGate } from '@/lib/features/vod-feature'

export default function VideosPage() {
  return (
    <AdminVodGate>
      <div>
        {/* VOD Content here */}
      </div>
    </AdminVodGate>
  )
}
```

## ✅ Checklist: New Addon/Feature

Before submitting/completing a new feature, verify:

### Code
- [ ] Feature Code defined (`MY_FEATURE_CODE`)
- [ ] Custom hook created (`useMyFeature`)
- [ ] User Feature Gate created (`MyFeatureGate`)
- [ ] Admin Feature Gate created with upgrade prompt (`AdminMyFeatureGate`)
- [ ] Theme system used (`activeTheme.gradient`)
- [ ] Typography components used (`H3` from `@/components/ui/Typography`)
- [ ] No hardcoded colors (use `activeTheme`)
- [ ] No hardcoded text (use translations if user-facing)

### Stripe (WICHTIG!)
- [ ] Stripe Product erstellt (Name: `Bookicorn [Feature Name]`)
- [ ] Product Metadata: `feature_code` und `type: addon`
- [ ] Product ID notiert: `prod_TnXXXXXXXXXX`

### Datenbank
- [ ] Feature in `feature_definitions` registriert
- [ ] `metadata.stripe_product_id` eingetragen!
- [ ] `metadata.status` = `available`
- [ ] `addon_price_monthly` und `addon_price_yearly` gesetzt
- [ ] Feature added to plan OR available as addon

### Testing
- [ ] Tested with feature enabled
- [ ] Tested with feature disabled (shows upgrade prompt)
- [ ] Studio-Erstellung getestet: Kein neues Stripe Product erstellt

## 🚨 Common Mistakes to Avoid

### ❌ WRONG: Hardcoded Colors

```typescript
<div className="bg-blue-500">...</div>
```

### ✅ RIGHT: Use Theme

```typescript
<div className={\`bg-gradient-to-r \${activeTheme.gradient}\`}>...</div>
```

### ❌ WRONG: No Loading State

```typescript
export function MyFeatureGate({ children }) {
  const { canUseMyFeature } = useMyFeature()  // Missing loading!
  if (!canUseMyFeature) return null
  return <>{children}</>
}
```

### ✅ RIGHT: Handle Loading

```typescript
export function MyFeatureGate({ children }) {
  const { canUseMyFeature, loading } = useMyFeature()
  if (loading) return null  // ← Important!
  if (!canUseMyFeature) return null
  return <>{children}</>
}
```

### ❌ WRONG: Feature Code Mismatch

```typescript
// File: chat-feature.tsx
export const CHAT_FEATURE_CODE = 'messaging'  // ❌

// Database: feature_definitions.code = 'chat_messaging'  // ❌ Doesn't match!
```

### ✅ RIGHT: Matching Codes

```typescript
// File: chat-feature.tsx
export const CHAT_FEATURE_CODE = 'chat_messaging'  // ✅

// Database: feature_definitions.code = 'chat_messaging'  // ✅ Matches!
```

## 🔧 Feature Context Reference

The `FeatureProvider` provides these helper functions:

```typescript
const {
  // Subscription & Plan
  subscription,    // StudioSubscription | null
  plan,           // SubscriptionPlan | null

  // Features
  features,       // Set<string> - All active feature codes
  featureList,    // Feature[] - Full feature objects
  addons,         // FeatureAddon[] - Active addons

  // Limits
  limits,         // Record<string, number | null>
  usage,          // Record<string, LimitUsage>

  // Helpers
  hasFeature,     // (code: string) => boolean
  canUse,         // (code: string) => boolean
  hasLimit,       // (code: string) => boolean
  getRemainingLimit,  // (code: string) => number | null
  isNearLimit,    // (code: string, threshold?: number) => boolean
  isAtLimit,      // (code: string) => boolean

  // State
  loading,        // boolean
  error,          // string | null

  // Actions
  refreshFeatures // () => Promise<void>
} = useFeatures()
```

## 📊 Database Schema Reference

### feature_definitions

```sql
id                  uuid PRIMARY KEY
code                varchar UNIQUE         -- 'chat_messaging', 'studio_blog'
name                varchar                -- 'Chat & Messaging'
description         text
category            varchar                -- 'core', 'content', 'marketing'
addon_price_monthly numeric(10,2)          -- Monatspreis als Addon
addon_price_yearly  numeric(10,2)          -- Jahrespreis als Addon
is_active           boolean DEFAULT true
metadata            jsonb                  -- WICHTIG: Enthält stripe_product_id!
created_at          timestamptz

-- metadata Struktur:
-- {
--   "status": "available",              -- oder "coming_soon"
--   "stripe_product_id": "prod_TnXXX",  -- PFLICHT für Addons!
--   "featured": false,
--   "includes": ["Feature 1", "Feature 2"]
-- }
```

### studio_feature_addons

```sql
id              uuid PRIMARY KEY
studio_id       uuid REFERENCES studios
feature_id      uuid REFERENCES feature_definitions
status          varchar                -- 'active', 'cancelled', 'cancelling'
billing_cycle   varchar                -- 'monthly', 'yearly', 'usage'
price_override  numeric(10,2)
valid_until     timestamptz            -- For 'cancelling' status
created_at      timestamptz
```

## 🎯 When This Skill Activates

This skill should be loaded when:
- Creating a new feature/addon
- Keywords: `addon`, `feature`, `feature gate`, `subscription`
- Working in `src/lib/features/`
- Creating feature-gated pages
- Setting up premium features

---

**Remember:** Consistency is key! Every addon should follow this exact pattern.
