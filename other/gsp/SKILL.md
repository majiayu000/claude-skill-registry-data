---
name: gsp
description: Administer and score the HUMMBL Governance Sense-Making Profile (GSP), the compatibility-preserving name for the existing Biocognitive OS Assessment instrument.
version: 1.0.0
execution-mode: advisory
argument-hint: '"SCOPE" [--format pdf|text|json]'
agent: hr-specialist
category: cognitive
status: candidate
---

# Governance Sense-Making Profile (GSP)

GSP is the stable instrument identifier for the HUMMBL assessment formerly
invoked as `/biocognitive-assessment`. The legacy command remains supported
during migration and is semantically equivalent to this profile.

Use the existing instrument protocol and preserve the underlying BKI and
Biocognitive OS theory. This alias changes the instrument-facing name only;
it does not rename the six-mode taxonomy or erase theory attribution.

## Usage

```
/gsp "SCOPE"
/gsp "individual"
/gsp "team" --format json
/gsp "organization"
```

Legacy compatibility:

```
/biocognitive-assessment "SCOPE"
```

The legacy invocation must continue to resolve to the same assessment until
the migration is explicitly retired through a separate compatibility decision.

## Canonical protocol

The full administration, scoring, and intervention protocol remains in
`skills/biocognitive-assessment/SKILL.md` during the additive migration phase.
Implementations must keep the two entry points behaviorally equivalent.
