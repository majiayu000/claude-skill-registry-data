---
name: docker
description: Docker deploy patterns — image build, compose stacks, docker build --check gate
category: Deploy
level: library
engineer: deploy-engineer
gate: "docker build --check ."
bundles: []
allowed-tools: Read, Glob, Grep
---


# Docker

Composition metadata carrier — frontmatter is the product (see
`commands/apply/references/skill-metadata-schema.md`). Body intentionally minimal. Do not
delete: `compose_stack` hard-fails without this registration.
