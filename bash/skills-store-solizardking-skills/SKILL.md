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

Pack also includes `scanner/` (security scanner) and `scripts/` (validate/index tooling).

See `catalog.json` and `imported-skills.json` for the full community index.
