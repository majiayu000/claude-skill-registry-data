---
name: repository-capability-map
description: "Turns repository structure and demonstrated behavior into a capability map organized around user tasks, not folder names or marketing language."
---

# Repository Capability Map

## Purpose

Turns repository structure and demonstrated behavior into a capability map organized around user tasks, not folder names or marketing language.

## When to use

Identify which user workflows a repository actually supports and what evidence justifies each capability.

## Required inputs

Source inventory, selected revision, docs/tests/examples, and user task categories.

## Workflow

1. Use the source inventory and lock the map to its selected revision.
2. Group evidence into user tasks such as configuring, building, testing, migrating, troubleshooting, extending, integrating, and releasing only where supported.
3. For every capability, record source paths, tests/examples, prerequisites, interface boundaries, and limits.
4. Label each capability as test-demonstrated, documented only, inferred, planned, deprecated, or unverified.
5. Compare the map with likely user intents and list uncovered areas without inventing features.

## Validation checklist

Every capability has a source reference and status; planned work is not presented as implemented behavior.
- [ ] Source revision, paths, and authorized scope are recorded.
- [ ] Every material claim has a source reference or explicit uncertainty label.
- [ ] At least one neighboring/negative case has been checked.
- [ ] Validation describes what actually ran and does not treat a plan as a pass.

## Required output

Capability-to-evidence matrix, prerequisites, confidence/status labels, gaps, and candidate user tasks.

## Boundaries and failure handling

Do not infer guarantees from a folder name or roadmap. Keep private details and credentials out of public output unless authorized.
If source access, evidence, permissions, or provenance is insufficient, stop and return blockers rather than inventing details. Preserve originals and seek human review for ambiguous licensing or semantic boundaries.

## Trigger examples

- **Positive:** Map this repository's actual capabilities to user tasks and cite supporting tests/docs.
- **Negative:** Invent a feature list from naming conventions without inspecting evidence.
