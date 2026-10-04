---
name: compiling-entities
description: >-
  Compiles a comprehensive entry for a named entity by scanning ALL files,
  gathering every mention, and assembling a structured profile. Use when building
  out a full entry for any character, species, location, or concept, or when user
  says "compile", "flesh out", "full entry for", or "everything about [entity]".
  Does NOT extract multiple entities from one source — use /extracting-entities.
model: sonnet
effort: high
context: fork
---

# Compiling Entities

Assemble all information about a named entity from across the entire repo.

## Process

1. Search GLOSSARY.md, then grep all .md files for the entity name
2. Read FULL content of every file mentioning the entity
3. Compile into structured profile with sources cited
4. Flag contradictions between sources
5. Present for author review — do NOT write without approval

## Out of Scope

Does NOT extract multiple entities from one source (use /extracting-entities).
Does NOT write original content (use /writing-worldbuilding).
