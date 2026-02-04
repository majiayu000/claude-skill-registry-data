---
name: understanding-context-entropy
description: Decide how to codify knowledge for reuse. Use when evaluating whether a pattern, solution, or insight should be formalized—and in what form (types, code structure, CLAUDE.md, README, skill, or code comments).
---

# Understanding Context Entropy

## The Model

LLMs solve low-entropy problems well. Context engineering reduces entropy.

**Entropy** in this context means the information-theoretic complexity of a problem space—how many valid solutions exist, how much exploration is needed, how much domain knowledge is required to navigate the space.

**Context reduces entropy by:**
- Pre-computing domain knowledge (skills, docs, examples encode expertise)
- Constraining solution space (types make invalid states unrepresentable)
- Providing exemplars (existing code serves as templates)
- Encoding terminology (consistent vocabulary reduces ambiguity)

The more entropy you remove through context, the more reliably an LLM can solve problems in that domain.

## The Entropy Reduction Hierarchy

Not all knowledge should become skills. Choose the most appropriate mechanism:

| Priority | Mechanism | When to use | Why preferred |
|----------|-----------|-------------|---------------|
| 1 | **Types/Protocols** | Knowledge can be compiler-enforced | Zero runtime cost, impossible to forget, self-documenting |
| 2 | **Code structure** | The right path can be made obvious through design | Guides without requiring documentation |
| 3 | **CLAUDE.md** | Small, stable, project-wide context | Visible, low overhead, always loaded |
| 4 | **Skill** | Recurring, stable, non-obvious patterns needing detailed guidance | Progressive disclosure, discoverable |
| 5 | **README** | Human-facing documentation | For humans, not agents |
| 6 | **Code comments** | Rare but complex inline knowledge | Co-located with relevant code |

**Prefer higher-priority mechanisms.** Types beat prose. Code structure beats documentation. Only reach for skills when the knowledge genuinely needs detailed, reusable guidance.

### Examples

| Knowledge | Best mechanism | Why |
|-----------|---------------|-----|
| "Always validate before saving" | Type: `ValidatedModel` that can only be created through validation | Compiler-enforced |
| "Date formatters are expensive, reuse them" | CLAUDE.md section | Small, stable, project-wide |
| "Use `.lighthouse` for design tokens" | Skill (`styling-project-ui`) | Recurring, needs examples and guidance |
| "This workaround exists because of iOS bug rdar://12345" | Code comment | Rare, context-specific |
| "The coordinator pattern in this app" | Skill (`using-uikit-in-project`) | Complex, recurring, needs detailed explanation |

## Codification Readiness Criteria

Before formalizing knowledge in *any* form, all four conditions should be true:

1. **Recurrence:** The pattern has appeared 3+ times with consistent form
2. **Stability:** The knowledge is not actively evolving or experimental
3. **Non-obviousness:** Not already clear from code, types, or existing docs
4. **Onboarding value:** Someone new would benefit from not having to discover it

If any condition is false, wait. Premature codification creates maintenance burden.

## Why Codification Decisions Cannot Be Automated

Deciding what to codify—and how—is itself a high-entropy task. It requires judgment about:
- **Novelty:** Is this knowledge actually new vs. already encoded?
- **Stability:** Is this pattern settled or still evolving?
- **Generality:** Specific to one case or broadly applicable?
- **Form:** What mechanism best captures this knowledge?

The auditor agents work because they enforce *pre-established* standards—the hard decisions were already made by humans. This skill helps you make those decisions; it does not automate them.

## The Abstraction Ladder

When you do codify, choose the right level:

| Level | What it captures | Example |
|-------|-----------------|---------|
| **Principle** | General truths | "Prefer composition over inheritance" |
| **Pattern** | Reusable approaches | "Use `ApolloQueryCoastGraphQLRequest` for single-fetch queries" |
| **Concrete** | Exact commands/steps | "Run `make build/app` to build" |

Most documentation combines levels—principles at the top, patterns in the middle, concrete examples at the bottom.

## Anti-Patterns: What NOT to Codify

- **Temporary workarounds:** Will be removed when the underlying issue is fixed
- **One-off solutions:** Specific to a unique situation, won't recur
- **Type-obvious knowledge:** Already encoded in the codebase's types and structure
- **Actively evolving patterns:** Still being refined; codifying too early creates stale guidance
- **Obvious domain knowledge:** Claude already knows; don't waste tokens

## Decision Flowchart

```
Has this pattern appeared 3+ times?
├─ No  → Wait. Track informally if promising.
└─ Yes → Is the pattern stable (not actively changing)?
         ├─ No  → Wait. Let it settle.
         └─ Yes → Is it already obvious from code/types/existing docs?
                  ├─ Yes → Don't codify. Types are better than prose.
                  └─ No  → Would someone new benefit from not discovering it?
                           ├─ No  → Don't codify. Not worth the maintenance.
                           └─ Yes → Choose the right mechanism:
                                    ├─ Can types enforce it? → Add types/protocols
                                    ├─ Small and project-wide? → Add to CLAUDE.md
                                    ├─ Needs detailed guidance? → Create/update a skill
                                    ├─ Human-facing? → Add to README
                                    └─ Rare but complex? → Add code comment
```

## Integration

- **How to write a skill:** See [writing-agent-skills](../writing-agent-skills/SKILL.md)
- **When to reflect on work:** Use the `context-opportunity-detector` agent after complex sessions
- **For examples:** See [REFERENCE.md](REFERENCE.md)
