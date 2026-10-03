---
name: ls-shopify-storefront
description: Guide Shopify Storefront API and Hydrogen storefront work. Use for Storefront
  GraphQL, product data, carts, checkout, and theme/headless integration.
metadata:
  version: '1.0'
extensions:
  external_skill:
    source_kind: native-reference
    source_url: https://github.com/Shopify/agent-skills
    source_path: shopify-storefront-graphql/SKILL.md
    source_commit: 6b9ed0552d5116ee33d0e211dfa6681f2f5bdffe
    source_ref: main
    source_sha256: 5d51ef38d5d357ec856c9a55e21996acf0d739acd4f19d2d1c4f83c60c9e5df6
    license: NO_REPO_LICENSE_FOUND
    import_date: '2026-07-03'
    vetting_status: provenance-recorded-no-bundled-tooling-executed
---

# Shopify Storefront

Use this skill when working on Shopify Storefront tasks.

## Workflow

- Inspect Storefront API version, token scope, Hydrogen/theme stack, product model, cart flow, and checkout handoff.
- Keep admin tokens and private app credentials out of client bundles; use Storefront-scoped tokens appropriately.
- Validate GraphQL queries against the pinned API version and test cart, variant, localization, and inventory edge cases.

## Boundaries

- Inspect the target repository before making changes.
- Prefer existing project patterns, declared package managers, and documented validation commands.
- Do not expose secrets, credentials, private user data, or production account identifiers in source, examples, or logs.
- When external APIs or current vendor behavior matter, verify against official docs before implementation.


## License Boundary

The upstream repository snapshot did not expose a top-level license file during this run. This skill is LocalSetup-native guidance and does not copy upstream body text or bundled assets.

## Provenance

- Source: `https://github.com/Shopify/agent-skills`
- Ref: `main` at `6b9ed0552d5116ee33d0e211dfa6681f2f5bdffe`
- Source path: `shopify-storefront-graphql/SKILL.md`
- License classification: `NO_REPO_LICENSE_FOUND`
- Source SHA-256: `5d51ef38d5d357ec856c9a55e21996acf0d739acd4f19d2d1c4f83c60c9e5df6`
