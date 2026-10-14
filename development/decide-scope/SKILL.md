---
name: decide-scope
description: When to keep a package small (micro) vs let it grow (macro). The scope spectrum.
---

# Skill: Package Scope

> "We would rather have a small package with one very polished feature, than a large package that tries to cover all possible edge cases."

## The Decision

**Micro when:**
- Single, well-defined problem
- First package attempt (start small, learn the craft)
- Feature can stand alone without other concerns
- Low configuration surface area

**Macro when:**
- Multiple tightly-coupled concerns (`medialibrary`: upload + conversion + responsive images)
- Splitting would force users to install multiple packages for basic functionality
- Domain is inherently complex (`backup`: sources + destinations + notifications + cleanup)
- The package has become an ecosystem (`permission`: roles + permissions + guards + teams)

**Platform when:**
- The package IS the platform, not a feature on top of one
- Filament's model: composable packages (`forms`, `tables`, `actions`) that work independently but integrate into a host (`panels`)
- Monorepo with subtree splits for independent installation
- Plugin system that enables third-party extensions
- This is rare and deliberate -- most packages should not aim for platform scope

## The Lifecycle

Packages graduate through scope tiers:

1. **Micro** -- Solve one problem well. Ship it.
2. **Macro** -- Tightly-coupled concerns grow organically. Embrace it when splitting would confuse users.
3. **Graduate to core** -- If the community builds the same feature repeatedly, it belongs in the framework. Tim MacDonald's principle: the best packages make themselves obsolete by proving a concept worthy of framework adoption.
4. **Platform** -- Rare. The package becomes the foundation others build on.

## The Heuristic

Ask: *"Would a user be confused about which package to install?"*

If splitting creates a "which one do I need?" moment, keep it together.

## The Quick Test

| Ask                                        | Answer | Use                             |
|--------------------------------------------|--------|---------------------------------|
| Can this feature stand completely alone?   | Yes    | Micro                           |
| Would splitting confuse users?             | Yes    | Macro                           |
| Are the concerns tightly coupled?          | Yes    | Macro                           |
| Is this your first package?                | Yes    | Micro                           |
| Does core functionality require all parts? | Yes    | Macro                           |
| Can you explain it in one sentence?        | Yes    | Micro                           |
| Does it define a plugin/extension system?  | Yes    | Platform (proceed with caution) |

## Real-World Examples

See [examples.md](examples.md).
