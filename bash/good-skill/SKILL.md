---
name: good-skill
description: Use when the request mentions `.lando.yml`, `lando rebuild` or a fixture runner and you need a contract-compliant example skill. For anything real use the plugin skills.
license: MIT
compatibility: Filesystem agent with bash and node
metadata:
  author: fixtures
  version: 1.0.0
disable-model-invocation: false
---

# Good skill

## When to use

- The validator test suite needs a skill that satisfies every rule.

## Inputs required

- Nothing; this is a fixture.

## Procedure

1. Run `node scripts/check.mjs` from this folder.
2. Read [the deep dive](references/deep-dive.md) when more detail is needed.

```bash
node scripts/check.mjs --help
```

## Verification

- `node scripts/check.mjs` exits 0.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Validator reports an error for this fixture | A rule changed | Update the fixture together with the rule |

## Escalation

- Ask the maintainer of the validator.
