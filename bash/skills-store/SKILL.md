---
name: skills-store
description: >
  Cheshire Skills Store index — curated Agent Skills packages for Cheshire Terminal
  (API, PostHog, Google Agent Registry, Skill Hub onchain, Stripe, Solana common errors,
  NOXA) plus the community skills collection. Use when installing store skills, browsing
  the store catalog, or wiring cheshireterminal.ai/skills-store.
---

# Cheshire Skills Store

Install curated packages:

```bash
npx skills add Solizardking/cheshire-terminal --path skills-store
# or local
npx skills add ./skills-store
```

First-class store skills also ship as top-level hub entries: `cheshire-api`, `cheshire-noxa`,
`google-agent-registry`, `posthog-cheshire`, `skillhub-onchain`, `solana-common-errors`, `stripe`.

Pack also includes `scanner/` (security scanner) and `scripts/` (validate/index tooling). Nested store packages (`cheshire-api`, `google-agent-registry`, `stripe`, …) ship here for the Cheshire pack; the hub also catalogs them as top-level skills.

Cheshire Terminal mesh — all of these talk to this store:

| Surface | Path |
|---------|------|
| Client UI | `client/` → `/skills-store` |
| CLI | `cli/` → `skills:store` / `GET /api/skills-store` |
| Server | `server/routes/skills-store.ts` reads this directory |
| Community dump | `skills/` via `imported-skills.json` |
| Google registry | `registry/google/` + `google-agent-registry` |

See `catalog.json` and `imported-skills.json` for the full community index.
