---
name: domain-modeling
description: >
  Build and sharpen a project's shared vocabulary while designing: challenge fuzzy or conflicting terms, test them against concrete scenarios and the code, and record each settled term in GLOSSARY.md as it is settled. Trigger on "what do we call this", "define our terms", "these names are inconsistent", or when writing or editing a GLOSSARY.md. For recording a decision, use the draft-adr skill.
license: MIT
metadata:
  upstream: mattpocock/skills@49dd158d skills/engineering/domain-modeling
---

# Domain modeling

Actively build and sharpen the project's domain model as you design. This is the _active_ discipline: challenging terms, inventing edge-case scenarios, and writing the glossary down the moment a term crystallises. Merely _reading_ `GLOSSARY.md` for vocabulary is not this skill; any skill can do that. Use this one when you are changing the model, not just consuming it.

## File structure

Most repos have a single context:

```
/
├── GLOSSARY.md
├── docs/
│   └── adr/
└── src/
```

If a `GLOSSARY-MAP.md` exists at the root, the repo has multiple contexts. The map points to where each one lives:

```
/
├── GLOSSARY-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   └── GLOSSARY.md
│   └── billing/
│       └── GLOSSARY.md
```

Create files lazily: only when you have something to write. If no `GLOSSARY.md` exists, create one when the first term is resolved. If the repo already keeps its vocabulary somewhere else, use that place and its format.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `GLOSSARY.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y. Which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account': do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible. Which is right?"

### Update GLOSSARY.md inline

When a term is resolved, update `GLOSSARY.md` right there. Don't batch these up: capture them as they happen. Use the format in [glossary-format.md](references/glossary-format.md).

`GLOSSARY.md` holds no implementation details. It is not a spec, a scratch pad, or a place for implementation decisions. It is a glossary and nothing else.

### Offer ADRs sparingly

Offer to record a decision only when all three are true:

1. **Hard to reverse**: the cost of changing your mind later is meaningful.
2. **Surprising without context**: a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off**: there were genuine alternatives and you picked one for specific reasons.

If any of the three is missing, skip it. When all three hold, use the `draft-adr` skill to write the record, and use the glossary's terms in it.
