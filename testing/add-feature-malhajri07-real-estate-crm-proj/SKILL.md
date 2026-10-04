---
name: add-feature
description: Build a complete vertical slice for a new feature — Prisma model + API route + react-query hook + UI page + sidebar entry + vault Features note. Use when the user asks for "a full new feature", "add X end-to-end", or "scaffold a feature".
---

# add-feature

The big one. Use this when the user asks for a brand-new feature, not just a tweak. It chains the smaller scaffold skills in the right order and ensures the vault and memory stay in sync.

## Inputs to gather

- **Feature name** in English + Arabic
- **One-line problem statement** ("agents need to track X because Y")
- **Primary user role(s)** that will use it
- **Data model sketch** — fields, relations
- **API endpoints needed**
- **Pages / UI surfaces** affected

If any of these are missing, ask before scaffolding. **Do not guess the data model.**

## Steps

Follow this order — earlier steps unblock later ones:

1. **Schema** → run `/add-prisma-model` for each new table. Push and generate.
2. **API** → run `/add-api-route` for each route. Verify org isolation.
3. **Hook** → run `/add-react-query` for each endpoint the UI will call.
4. **Page** → run `/add-page` for each new screen. Wire it to the hooks.
5. **Sidebar** → add the navigation entry.
6. **Seed** → if the feature needs sample data to demo, append to `apps/api/seed.ts`.
7. **Tests** → add at least one Playwright happy-path test under `apps/web/tests/e2e/`.
8. **Vault**:
   - Create `Aqarkom_Knowledge/Features/{Feature Name}.md` (use sibling Features notes as templates)
   - Update `Aqarkom_Knowledge/Architecture/Database Schema.md` and `API Routes.md`
   - If the feature involved a meaningful trade-off, run `/add-adr`
9. **Memory** → save a `feedback` or `project` memory if the user gave guidance during the build (e.g., "always do X this way").
10. **Commit** → run `/commit-and-track` so the changelog and timeline stay current.

## Verification checklist

- [ ] All sub-skill checklists pass
- [ ] `/typecheck` clean
- [ ] `/audit-org-isolation` clean
- [ ] `/audit-rtl` clean
- [ ] At least one Playwright test green
- [ ] Vault Features note exists and is linked from `Home.md`

## Anti-patterns

- Don't ship the page before the route — leads to broken loading states being committed
- Don't add a sidebar entry until the page actually renders
- Don't skip the vault step — the next session will be flying blind
- Don't bundle two unrelated features into one PR
