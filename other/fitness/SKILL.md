---
name: fitness
description: Administer and score the HUMMBL Fitness Profile, the compatibility-preserving name for the existing Fitness Assessment instrument.
version: 1.0.0
execution-mode: advisory
argument-hint: '"SCOPE" [--format pdf|text|json]'
agent: hr-specialist
category: fleet-ops
status: candidate
---

# Fitness Profile

Fitness is the stable instrument identifier for the HUMMBL assessment formerly
invoked as `/fitness-assessment`. The legacy command remains supported
during migration and is semantically equivalent to this profile.

Use the existing instrument protocol and preserve the underlying BKI and
Fitness Profile theory. This alias changes the instrument-facing name only;
it does not rename the six-mode taxonomy or erase theory attribution.

## Usage

```
/fitness "SCOPE"
/fitness "individual"
/fitness "team" --format json
/fitness "organization"
```

Legacy compatibility:

```
/fitness-assessment "SCOPE"
```

The legacy invocation must continue to resolve to the same assessment until
the migration is explicitly retired through a separate compatibility decision.

## Canonical protocol

The full administration, scoring, and intervention protocol remains in
`skills/fitness-assessment/SKILL.md` during the additive migration phase.
Implementations must keep the two entry points behaviorally equivalent.
