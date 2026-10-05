---
name: vault-project-archiving
description: Use when archiving an already-maintained engineering project into a governed Obsidian vault, especially when the project has active code, docs, ADRs, roadmaps, repo metadata, or working notes that should become structured vault knowledge instead of a raw code dump.
---

# Vault Project Archiving

## Overview

Use this skill when an existing software or engineering project should enter the vault as structured knowledge. The vault should preserve project understanding, not become a second source repository.

## Use For

- archiving an existing codebase into the vault
- converting repo documentation into governed project notes
- creating a project index from README, docs, ADRs, changelogs, and roadmaps
- bringing an active engineering effort into intake, curation, and optional canonical layers

## Do Not Use For

- copying the full source tree into Obsidian
- replacing the git repository
- bulk-ingesting build artifacts
- silently publishing work notes into canonical knowledge

## Standard Flow

1. Confirm the project source:
   - local repo path
   - repository URL
   - existing exported project docs
2. Create or resolve `topic_id`
3. Choose archive depth:
   - light
   - standard
   - deep
4. Extract project knowledge inputs:
   - README
   - docs
   - ADRs or decision logs
   - changelog
   - roadmap
   - top-level manifests
   - deployment or CI notes
5. Write intake archive files for source mapping and import manifest
6. Write curation project notes for overview, architecture, risk, and current state
7. If a stable project summary already exists, route it to `$vault-canonical-promotion` instead of self-promoting

Read `references/project-archiving-pattern.md` before archiving.

## Required Outputs

- project archive manifest
- project source map
- project index note
- project overview note
- architecture summary note
- current state and risk note

## Common Mistakes

- dumping source code into the vault instead of project knowledge
- skipping repo lineage and commit context
- treating project docs as canonical without curation
- merging active project work and durable knowledge into one note
