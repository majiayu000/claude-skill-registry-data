---
name: phxstack-counselors
description: Get three independent read-only opinions on a consequential technical or product decision.
---

# phxstack-counselors

Use this for consequential architecture, database, API, dependency, migration,
security, or build-versus-buy decisions. Do not use it for small reversible
implementation choices.

Write one self-contained brief containing:

```text
QUESTION
RELEVANT CONTEXT
RELEVANT FILES
CONSTRAINTS
REQUIRED ANSWER FORMAT
```

When the current harness supports three independent read-only opinions, send
the same brief to each in isolation and preserve all three answers before
reading them. Otherwise, report that the harness cannot provide an independent
council and stop; never invent additional opinions.

Synthesize only after all answers are available:

```text
VERDICT
COUNCIL
DISAGREEMENTS
```

Name the deciding constraint and any dissent. Acting on the verdict remains a
developer decision.
