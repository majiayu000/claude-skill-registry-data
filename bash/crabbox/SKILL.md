---
name: crabbox
description: Coordinate isolated remote or clean-machine validation while preserving trust and credential boundaries.
category: development
aliases: []
triggers:
- use crabbox
- run crabbox
keywords:
- crabbox
- development
- coordinate
- isolated
- remote
- clean
- machine
dependencies:
- optional:crabbox
risk: low
version: 1.0.0
source: custom
enabled: true
capabilities:
- crabbox
- development
inputs:
- task
- context
outputs:
- result
- report
lifecycle: enabled
author: Mr-Nobody-Anonymous
tags:
- coordinate
- crabbox
- development
- isolated
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Crabbox

## Purpose
Coordinate isolated remote or clean-machine validation while preserving trust and credential boundaries.

## When to Use
Use when you need to coordinate isolated remote or clean-machine validation while preserving trust and credential boundaries. or trigger commands matching use crabbox, run crabbox.

## When NOT to Use
Do not use outside permitted scope or when authorization is missing.

## Capabilities
- Coordinate isolated remote or clean-machine validation while preserving trust and credential boundaries.
- Deterministic step-by-step execution
- Structured artifact validation

## Inputs
Natural-language request, execution context, and configuration parameters.

## Workflow
1. Parse inputs and verify environment prerequisites.
2. Execute bounded operations with continuous validation.
3. Return verified results and logs.

## Tools
optional:crabbox

## Examples
Example usage:
```bash
# Invoke via skills CLI
python scripts/skills/skills.py route "use crabbox"
```

## Safety
Never perform destructive unconfirmed modifications. Adhere to zero-trust boundaries.

## Source
Imported from openclawskills.net.

## Notes
Maintained as part of canonical development category.
