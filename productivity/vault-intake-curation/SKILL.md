---
name: vault-intake-curation
description: Use when handling raw sources, imported material, NotebookLM outputs, quick captures, or working-note restructuring inside a governed Obsidian vault. Applies when the task belongs to intake or curation layers and must preserve topic identity, source lineage, and registry state.
---

# Vault Intake And Curation

## Overview

This skill handles the working part of the vault: capturing raw material, normalizing structure, and curating draft knowledge without crossing into canonical space.

## Use For

- source imports
- NotebookLM landing notes
- `ProjectRaw/` updates
- topic-folder cleanup
- draft synthesis and topic indexes

## Do Not Use For

- direct canonical publication
- archive decisions
- topic merge decisions that require coordinator authority

## Workflow

1. Confirm target `topic_id`
2. Confirm target layer is `intake` or `curation`
3. Check registry for existing objects
4. Update or create files in working layers
5. Preserve source references
6. Log important changes
7. If the result looks long-lived, submit a promotion candidate instead of self-promoting

Read `references/intake-checklist.md` for the checklist.

## Required Outputs

- updated file path
- preserved source lineage
- registry-consistent topic linkage
- ledger entry for meaningful changes

## Common Mistakes

- moving raw notes into canonical directories
- dropping source references during cleanup
- restructuring topic folders without updating registry
- silently changing topic identity
