---
name: context
description: "Skill for the Context area of Securacy. 4 symbols across 4 files."
---

# Context

4 symbols | 4 files | Cohesion: 50%

## When to Use

- Working with code in `securacyfrontend/`
- Understanding how useAuth, DashboardPage, AuthPage work
- Modifying context-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `securacyfrontend/context/AuthContext.tsx` | useAuth |
| `securacyfrontend/app/home/page.tsx` | DashboardPage |
| `securacyfrontend/app/(auth)/page.tsx` | AuthPage |
| `securacyfrontend/app/home/settings/_components/account-form.tsx` | AccountForm |

## Entry Points

Start here when exploring this area:

- **`useAuth`** (Function) — `securacyfrontend/context/AuthContext.tsx:85`
- **`DashboardPage`** (Function) — `securacyfrontend/app/home/page.tsx:11`
- **`AuthPage`** (Function) — `securacyfrontend/app/(auth)/page.tsx:12`
- **`AccountForm`** (Function) — `securacyfrontend/app/home/settings/_components/account-form.tsx:8`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `useAuth` | Function | `securacyfrontend/context/AuthContext.tsx` | 85 |
| `DashboardPage` | Function | `securacyfrontend/app/home/page.tsx` | 11 |
| `AuthPage` | Function | `securacyfrontend/app/(auth)/page.tsx` | 12 |
| `AccountForm` | Function | `securacyfrontend/app/home/settings/_components/account-form.tsx` | 8 |

## How to Explore

1. `gitnexus_context({name: "useAuth"})` — see callers and callees
2. `gitnexus_query({query: "context"})` — find related execution flows
3. Read key files listed above for implementation details
