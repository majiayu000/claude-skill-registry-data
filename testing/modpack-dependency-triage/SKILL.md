---
name: modpack-dependency-triage
description: "Maps modpack dependency and loader compatibility before changing a modded Minecraft instance. Use when a pack has hundreds of mods or conflicting version constraints."
---

# Modpack Dependency Triage

## Use when
Adding or updating one mod creates cascading failures because version, loader, Java, library, or dependency constraints are not mapped.

## Workflow
1. Capture Minecraft version, loader/version, Java runtime, pack manifest, mod filenames, config overrides, and recent changes.
2. Resolve declared dependencies, required/optional integrations, duplicate jars, loader mismatches, and known exclusion rules from trusted metadata.
3. Compare the current working state with the failing state and change one dependency group at a time.
4. Produce a proposed change set with rollback instructions and a minimal test world/server start checklist.

## Required output
A dependency graph, compatibility findings, proposed changes, confidence labels, and rollback plan.

## Validation
- Every claimed conflict is tied to metadata, logs, or a reproducible test.
- Client-only and server-required components are distinguished.
- The original modpack manifest and saves remain untouched during triage.

## Guardrails
Do not delete mods or configuration as a first fix; back up the instance and change the smallest proven cause.
