---
name: standards
description: Index of official Android/Kotlin/Gradle docs, Now in Android and JetSnack references, and house patterns (UI events, actions holder).
user-invocable: false
---

# Android standards reference

Use this to pick the authoritative source for a question. For a standard, quote its anchor in
`references/source-anchors.md` instead of fetching the page. Look up deadlines, deprecations and versions
when you use them (`android docs search` / `android docs fetch` or WebFetch), because they change between
anchor checks. Do not answer those from memory.

| Question | Read |
|---|---|
| Layering, state, offline-first | `references/official-docs.md` §Architecture, then `references/nia.md` |
| Navigation 2 or Navigation 3 | `references/official-docs.md` §Architecture, then the `navigation-3` skill |
| One-shot ViewModel → UI events (navigation, snackbar) | `references/ui-events.md` (house pattern + why it differs from the official state-based guidance) |
| Too many composable callbacks / parameters | `references/ui-events.md` §Actions holder |
| What tests a change needs and the journey (E2E) format | `references/testing.md` |
| Design system, theming, custom components | `references/jetsnack.md` |
| Build, AGP, Gradle, catalogs, shrinking | `references/official-docs.md` §Build |
| Security controls, pinning, storage | `references/official-docs.md` §Security |
| Play policy, target API, integrity | `references/official-docs.md` §Play |
| Compose performance and API shape | `references/official-docs.md` §Compose |
| A skill a playbook names is missing, or how to install it | `references/companions.md` |

Guardrails when applying any reference to this repo:
- target repos are often hybrid legacy apps (XML + Compose). Recommend the blueprint pattern for new code. Do not propose rewriting working
  XML/LiveData screens unless the ticket is a migration (`migrate-xml-views-to-jetpack-compose` skill).
- Now in Android pragmatism (maintainers' discussion #1273): ViewModels may call repositories directly, use cases
  need no interface each, a domain layer is optional and DI at module boundaries is enough.
- A reference may be older than the toolchain. State the version the source targets.
