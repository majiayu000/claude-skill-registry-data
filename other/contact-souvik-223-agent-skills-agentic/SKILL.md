---
name: contact
description: "Skill for the Contact area of Securacy. 5 symbols across 1 files."
---

# Contact

5 symbols | 1 files | Cohesion: 100%

## When to Use

- Working with code in `securacyfrontend/`
- Understanding how POST work
- Modifying contact-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `securacyfrontend/app/api/contact/route.ts` | isValidEmail, getResendErrorMessage, escapeHtml, validateBody, POST |

## Entry Points

Start here when exploring this area:

- **`POST`** (Function) — `securacyfrontend/app/api/contact/route.ts:86`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `POST` | Function | `securacyfrontend/app/api/contact/route.ts` | 86 |
| `isValidEmail` | Function | `securacyfrontend/app/api/contact/route.ts` | 20 |
| `getResendErrorMessage` | Function | `securacyfrontend/app/api/contact/route.ts` | 25 |
| `escapeHtml` | Function | `securacyfrontend/app/api/contact/route.ts` | 43 |
| `validateBody` | Function | `securacyfrontend/app/api/contact/route.ts` | 51 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `POST → IsValidEmail` | intra_community | 3 |

## How to Explore

1. `gitnexus_context({name: "POST"})` — see callers and callees
2. `gitnexus_query({query: "contact"})` — find related execution flows
3. Read key files listed above for implementation details
