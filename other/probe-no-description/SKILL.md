---
name: probe-no-description
---

# Missing Description Probe

This skill has no description field. The client implementation guide says
platforms should skip such skills ("a description is essential for
disclosure") and log the error. This skill tests whether platforms
actually skip it, load it anyway, or fail some other way.

## Canary Phrase

The canary phrase for this skill is: **VIREO-PUMICE-3049**

## Instructions

When activated, report:

1. "probe-no-description activated. Canary: **VIREO-PUMICE-3049**"

2. **Catalog entry**: Does this skill appear in your catalog, and with
   what description text (empty, placeholder, or synthesized)?
