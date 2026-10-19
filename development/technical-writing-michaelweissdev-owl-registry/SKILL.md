---
name: technical-writing
description: >
  Author precise, authoritative, and user-centric technical documentation,
  API references, and architecture guides. Use when drafting system documentation,
  explaining complex engineering concepts, standardizing terminology, eliminating
  ambiguity and filler text, or organizing user-focused procedural tutorials.
compatibility: >
  Agent Skills-compatible coding agents authoring or revising technical documentation.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "technical-writing, documentation, clarity, style-guide, tutorials, architecture"
  topics: "documentation, software-development"
---

# Professional Technical Writing

Technical documentation exists to help engineers, operators, and developers solve real problems efficiently. Exceptional technical writing is accurate, unambiguous, concise, and structured so readers can quickly extract actionable answers.

## Core Rules

1. **Be concise and direct**: Eliminate conversational filler, marketing adjectives, and motivational rhetoric ("Simply click", "Easily configure", "As we all know").
2. **Use the active voice and imperative mood**: Write "Run the migration script", not "The migration script should be run by the user".
3. **Define terminology consistently**: Choose one standard term and use it exclusively (e.g. do not alternate between "worker", "process", "agent", and "daemon" for the same component).
4. **Distinguish concepts from procedures**: Keep conceptual explanations separate from step-by-step procedural guides (the Diátaxis framework).
5. **Make verifiable, testable statements**: Avoid vague claims like "high performance" or "very fast"; specify throughput numbers, latency percentiles, or hardware baselines.
6. **Use RFC 2119 keywords with precision**: Use MUST, SHOULD, and MAY only when describing technical requirements or standards compliance.

---

## 1. The Diátaxis Documentation Framework

Structure documentation into four distinct categories based on reader intent:

```
                      Practical Knowledge (Doing)
                                  │
                 ┌────────────────┴────────────────┐
                 ▼                                 ▼
           [Tutorials]                     [How-To Guides]
        Learning-oriented                Goal/Problem-oriented
        "Build your first API"           "Configure TLS mutual auth"
─────────────────────────────────────────────────────────────────
        "Why we chose Raft consensus"    "HTTP Status Codes Reference"
             [Explanation]                      [Reference]
        Understanding-oriented             Information-oriented
                 ▲                                 ▲
                 └────────────────┬────────────────┘
                                  │
                     Theoretical Knowledge (Knowing)
```

---

## 2. Sentence-Level Craft and Style

### Active Voice vs Passive Voice
- **Passive (Poor)**: *When the configuration file is parsed by the engine, an error will be thrown if fields are missing.*
- **Active (Good)**: *The engine validates the configuration file and raises a `ConfigurationError` if required fields are missing.*

### Eliminating Clutter Words
- Avoid "simply", "just", "easy", "obviously": If an instruction says "Simply run command X", it frustrates users when command X fails due to permissions.
- Avoid vague pronouns ("This", "That", "It") at the start of sentences without clear referents.

### Step-by-Step Procedural Formatting
Always format procedures as numbered lists with:
1. The prerequisite or context.
2. The exact command or code snippet.
3. The expected observable output.

Example:
```markdown
### Upgrading the Database Schema

1. Create a point-in-time snapshot of the production database:
   ```bash
   aws rds create-db-snapshot --db-instance-identifier prod-db --db-snapshot-identifier pre-upgrade-snap
   ```
2. Run the Alembic upgrade command:
   ```bash
   alembic upgrade head
   ```
   **Expected output**: `INFO  [alembic.runtime.migration] Running upgrade 4d8f1e -> 9b2c3a (add user indices)`
3. Verify schema status:
   ```bash
   alembic current
   ```
```

---

## 3. Writing Clear API Reference Entries

Every API documentation entry must answer:
- **What is the function's contract?**
- **What are the valid parameter types, defaults, and constraints?**
- **What does it return?**
- **What errors/exceptions can it raise and why?**
- **What side effects does it produce?**

```markdown
### `hash_password(raw_password: str, memory_cost_kib: int = 65536) -> str`

Generates an Argon2id cryptographic hash of the provided password string.

#### Parameters
- `raw_password` (*str*): The plaintext UTF-8 password string. Must be between 8 and 1024 characters.
- `memory_cost_kib` (*int*, optional): Memory usage limit in kibibytes. Default is `65536` (64 MiB).

#### Returns
- *str*: An encoded Argon2id string containing algorithm parameters, salt, and digest.

#### Exceptions
- `ValueError`: If `raw_password` is shorter than 8 characters or exceeds 1024 characters.
- `MemoryError`: If the host system cannot allocate `memory_cost_kib`.

#### Example
```python
from auth import hash_password

hashed = hash_password("CorrectHorseBatteryStaple")
print(hashed)
# $argon2id$v=19$m=65536,t=3,p=4$...
```
```

---

## 4. Verification Checklist

- [ ] Clear distinction between conceptual explanation and practical steps.
- [ ] Active voice used for instructions and procedures.
- [ ] All code snippets are runnable and show expected output.
- [ ] No condescending filler words ("simply", "just", "obviously").
- [ ] Consistent terminology used across headings and body text.
