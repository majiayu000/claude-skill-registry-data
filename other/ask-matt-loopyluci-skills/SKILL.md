---
name: ask-matt
description: Use when unsure which skill or flow fits your current situation
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [routing, navigation, skills, meta, workflow]
---

# Ask Matt

A router skill. If you don't remember every skill, ask.

## The main flow: idea to ship
The route most work travels:
1. Grill the idea (grill-with-docs or grill-me)
2. Prototype to answer specific questions (prototype)
3. Spec multi-session work (to-spec, to-tickets)
4. Implement (implement)
5. Review (code-review)

Key on-ramps: triage (for incoming issues), wayfinder (for new codebases).

Standalone skills cover: diagnosing-bugs, design-an-interface, domain-modeling, ubiquitous-language, qa, writing-* skills, teach, and more.

> **Note**: This skill references the original Matt Pocock skills ecosystem. Skills not present in Hermes Agent can be adapted from the source repository.

## Common Pitfalls

- **Not recognizing the meta nature**: This skill is a router - it does not execute work. Point to the right skill and let it handle the implementation.
- **Stale mental model of available skills**: The skill index evolves. Routers must be updated when skills are added or removed.

## Verification Checklist

- [ ] User's situation understood
- [ ] Correct skill or flow identified for their needs
- [ ] Direction provided, not implementation
