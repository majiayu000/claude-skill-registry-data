---
name: demi
version: 0.1.0
license: MIT
description: Use before implementing, scaffolding, prototyping, or adding a feature when the work should start with the smallest useful code path, avoid speculative architecture, or prevent overbuilding before reduce would be needed.
---

# demi

A demi-glace starts concentrated. Nothing extra goes in just because the kitchen has it nearby. You do the same with code: build the smallest useful version that satisfies the ticket, fits the repo, and can be verified. Complexity has to earn its way into the pan.

**Core principle:** start simple enough that [reduce](../reduce/SKILL.md) should not be needed immediately afterward. Small means understandable and verifiable, not cramped. The shortest version that hides intent is not demi; it is just dense.

## The demi ladder

Before writing custom code, stop at the first rung that holds:

1. **Does this need to exist?** If the current behavior already satisfies the actual ask, skip the change and say why.
2. **Can the repo already do it?** Use existing commands, helpers, components, config, conventions, and tests before inventing new ones.
3. **Does the standard library cover it?** Prefer built-in language or framework features over custom code.
4. **Does the platform cover it?** Native browser, database, shell, operating system, framework, or deployment features beat owned code when they fit.
5. **Does an already-installed dependency cover it?** Use what is already in the project. Do not add a dependency for a few clear lines.
6. **Can one explicit local change do it?** One function, one component, one endpoint, one flag, one small data path.
7. **Only then:** write the minimum custom implementation that works and can be checked.

The ladder is quick. Do not turn it into a research project. If two rungs work, take the higher one unless it is less correct on edge cases.

## The demi pass

Run this before editing:

1. **Restate the actual ask.** One sentence. If the task is vague, choose the smallest useful interpretation that still satisfies it.
2. **Find the local pattern.** Read the nearest existing code, helpers, tests, and naming conventions. Prefer what the repo already uses.
3. **Climb the ladder.** Check existing behavior, repo primitives, standard library, platform, installed dependencies, and local one-change solutions before new infrastructure.
4. **Name the smallest useful slice.** Define the first complete behavior the user can actually run, click, test, or review.
5. **Cut speculative scope.** Remove features, settings, abstractions, options, data models, and UI states that are not required for that slice.
6. **Pick the boring implementation.** Use direct code, existing helpers, and local composition. New abstractions need evidence.
7. **Set a growth trigger.** Write down what future fact would justify expanding the design: a second consumer, a third repeated pattern, a measured performance limit, a public API boundary, or an explicit user requirement.
8. **Verify the slice.** Run the narrowest meaningful check through [check](../check/SKILL.md). If behavior is hard to pin down, use [taste](../taste/SKILL.md) for a focused test before expanding.

## Simplicity gates

Before adding a new layer, answer these. If any answer is no, keep it local.

- **Is this required by the current request?**
- **Does the repo already have a pattern for this?**
- **Is there a standard library, platform, or existing dependency path?**
- **Will at least two real callers use this now?** Three is better for shared abstractions.
- **Would a future maintainer understand this faster than the direct version?**
- **Can I verify the behavior after this change?**

## What to build first

Prefer these moves:

- One vertical slice over a broad scaffold.
- One explicit function over a generic utility.
- Existing components, commands, config, and test harnesses over new infrastructure.
- Clear local logic over premature indirection.
- A small typed data shape over a general schema system.
- A direct UI state path over a reusable state machine.
- A narrow CLI flag over an interactive prompt or new config file.
- A plain file or local module over a package, service, queue, plugin, or database.
- A small runnable check over a full testing framework when the repo does not already have one.

## What to refuse early

Do not build these unless the current task proves they are needed:

- Framework swaps.
- Plugin systems.
- Generic registries.
- New persistence layers.
- Background workers.
- Multi-provider abstractions.
- Config formats for a single value.
- Theme systems for one screen.
- Large component libraries for one view.
- Repository-wide rewrites.
- Public API reshapes.
- "Future-proof" abstractions without a future requirement.

## Not skimping

`demi` is not permission to be careless. Never simplify away:

- Trust-boundary validation.
- Error handling that prevents data loss.
- Security controls.
- Accessibility basics.
- Compatibility shims that protect real users.
- Calibration or tuning points for real hardware or external systems.
- Tests or checks for non-trivial branches, loops, parsers, money paths, auth paths, or security-sensitive logic.
- Anything the user explicitly asked for after you challenged the scope once.

A simple implementation without a check is not finished. Use the smallest meaningful check, not necessarily the biggest test harness.

## Shortcut notes

If the small version has a known ceiling, name it in the plan or final report. Add an inline comment only when future maintainers would otherwise mistake the simplification for ignorance.

Examples:

- `Global lock is fine for single-user CLI; move to per-account locks if concurrent accounts matter.`
- `Linear scan is fine below the current file sizes; index when measured input size makes it hot.`
- `Native date input is enough here; custom picker only if design or browser support requirements change.`

## The one-screen plan

For non-trivial work, write this before editing:

```markdown
## demi: <task>

Actual ask: <one sentence>
Smallest useful slice: <what will work when done>
Highest rung that holds: existing behavior | repo primitive | stdlib | platform | installed dependency | local change | custom code
Existing pattern to follow: <file/helper/test/component>
Cut from scope: <what is intentionally not being built>
Growth trigger: <what would justify expanding later>
Verification: <command/check/user-visible proof>
```

Keep it short. This is a guardrail, not a design doc.

## Mode

`demi` is apply-by-default. After the quick pass, implement the smallest slice unless the task is architectural, public-interface-heavy, security-sensitive, under-specified in a way that changes the outcome, or the user explicitly asks for options first. In those cases, report the demi plan and wait.

For large work, combine with [recipe](../recipe/SKILL.md): use `demi` to keep each recipe task small, vertical, and verifiable.

## Boundaries

- Use [mise](../mise/SKILL.md) when context is missing.
- Use [recipe](../recipe/SKILL.md) when the work needs sequencing.
- Use [taste](../taste/SKILL.md) when the slice needs tests before confidence.
- Use [check](../check/SKILL.md) before claiming done.
- Use [reduce](../reduce/SKILL.md) only after code exists and needs behavior-preserving cleanup.

## Common mistakes

| Mistake | Reality |
|---|---|
| Building a full framework because the feature might grow | Growth is a trigger, not a prediction. Ship the slice. |
| Adding config before there are real variants | One value can be code. Two may still be code. Three starts a conversation. |
| Creating a generic utility from one use | That is not reuse, it is disguise. Keep it local. |
| Scaffolding every future state | Build the path the user asked for and leave clean edges. |
| Calling fewer files "less complex" | A thousand-line god file is not demi. Small means understandable, not cramped. |
| Picking the shortest algorithm when it drops edge cases | Lazy means less owned code, not flimsier behavior. Correctness wins ties. |
| Skipping local pattern discovery | Simple in isolation can be weird in the repo. Match the kitchen. |
| Treating YAGNI as technical debt | YAGNI keeps quality high and scope small. Skimping leaves a mess for later. |
