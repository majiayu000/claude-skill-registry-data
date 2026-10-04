---
name: vercel
description: Vercel deploy patterns — preview/production environments, vercel inspect gate
category: Deploy
level: library
engineer: deploy-engineer
gate: "vercel inspect"
bundles: []
allowed-tools: Read, Glob, Grep
---


# Vercel

Composition metadata carrier — frontmatter is the product (see
`commands/apply/references/skill-metadata-schema.md`). Body intentionally minimal. Do not
delete: `compose_stack` hard-fails without this registration.
