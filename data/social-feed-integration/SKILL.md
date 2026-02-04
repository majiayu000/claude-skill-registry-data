---
name: social-feed-integration
description: Integrate and maintain the Instagram/Facebook social wall for case studies and blogs in this repo, including manual import workflows, Meta Graph API setup, compliance endpoints, and SEO/performance/security guardrails. Use when adding social posts, updating the importer, wiring UI placement, or handling Meta tokens and data deletion callbacks.
---

# Social Feed Integration

## Quick start
- Read references/current-state.md to see what is already implemented.
- Read references/workflows.md when importing or updating social posts.
- Read references/requirements-and-backlog.md for open items and gaps.
- Read references/research-summary.md for Meta Graph API setup and platform constraints.
- Read references/seo-marketing.md for SEO and marketing rules.
- Read references/network-architecture.md for trust boundaries and compliance endpoints.

## Workflow
1. Confirm scope (manual import vs live API, case studies vs blogs).
2. Validate Meta assets and secrets (Business app, system user token, env vars).
3. Run or extend the importer, download assets locally, update social-data.
4. Update UI placement and linking logic for the social wall.
5. Verify compliance endpoints, privacy copy, and env configuration.
6. Apply SEO and performance improvements (JSON-LD, ISO dates, lazy loading).
7. QA: verify links, images, schema, and no external Meta CDN URLs.

## Guardrails
- Never put Meta tokens in client code or VITE_ env variables.
- Do not ship Meta CDN URLs in social-data; always download and host locally.
- Keep structured data ISO dates; do not use relative labels in JSON-LD.
- Avoid third-party widgets that add branding or block rendering.
- Keep edits ASCII unless a file already uses Unicode and it is required.

## Repo touchpoints
- UI: client/src/components/sections/common/social-feed.tsx
- Data: client/src/data/social-data.ts
- Images: client/public/images/social and client/public/images/social/imported
- Importer: scripts/import-social.ts (npm run import:social)
- Compliance: server/routes.ts, client/src/pages/data-deletion.tsx, client/src/App.tsx
- Env template: .env.example
