---
name: agent-card
description: |
  Project processkit agent-card Artifacts into canonical public
  agent-card JSON files. Use when publishing an agent identity,
  endpoint, capability, or interoperability card from repository
  context into a runtime-visible file.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-agent-card
    version: "2.0.0-alpha.1"
    created: 2026-04-30T00:00:00Z
    category: processkit
    layer: 3
    provides:
      primitives: [Artifact, Actor]
      mcp_tools: [project_agent_card]
---

# Agent Card

## Intro

Agent cards describe a runnable or externally visible agent in a
provider-neutral JSON shape. Store the canonical source as an Artifact
with `spec.kind=agent-card`; use `project_agent_card` to render the
public JSON file and return a checksum.

The source Artifact may put the card under `spec.card`, or it may store
YAML/JSON card content in the Markdown body. Optional Actor data can
augment the projected card with runtime interfaces.

## Overview

`project_agent_card` reads an agent-card Artifact, validates the card
payload, writes the projected JSON file, and records projection metadata
such as path and checksum on the source Artifact. The projection is a
runtime file; the Artifact remains the reviewable source of truth.

## Gotchas

- Do not edit projected card JSON as the canonical source. Update the
  Artifact and re-project.
- Do not put secrets in public card payloads. Use private configuration
  outside the projected interoperability file.
- Re-project after endpoint, capability, or identity changes so the
  checksum stays useful.

## Full reference

### MCP tools

- `project_agent_card`

### Source entity

Use `Artifact(spec.kind=agent-card)` with card content in `spec.card`
or the Markdown body.
