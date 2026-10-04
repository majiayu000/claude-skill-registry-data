---
name: spec-file-governance
description: Create and maintain a project-root SPEC.md that captures main intent and project definition while referring out to authoritative wiki pages. Use when bootstrapping or updating a project repo so there is always a concise in-repo specification entrypoint linked to the fuller GitHub wiki documentation.
---

# SPEC.md governance

## Rule
Every project should have a root `SPEC.md` maintained by Spec.

## Purpose of SPEC.md
`SPEC.md` is the in-repo entrypoint for project intent.
It should:
- state the main intent of the project
- summarize the core project definition
- link to the authoritative wiki pages for deeper product, solution, and architecture material
- stay aligned with the current project direction

## What belongs in SPEC.md
- project purpose
- intended users or operators
- scope summary
- non-goals summary
- links to key wiki pages
- current high-level delivery intent

## What does not belong only in SPEC.md
Do not treat `SPEC.md` as the sole home for deep design truth.
Detailed product definition, architecture, and evolving assumptions should still live in the wiki.

## Ownership
- Spec creates and maintains `SPEC.md`
- Spec keeps it aligned with wiki truth and merged code changes
