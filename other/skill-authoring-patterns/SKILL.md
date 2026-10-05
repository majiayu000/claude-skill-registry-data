---
name: skill-authoring-patterns
description: 'The Apple/Swift-and-this-catalog layer for authoring or reviewing a SKILL.md, on top of superpowers:writing-skills. Use when writing or CR-ing a skill for this repo, wording a description so it routes precisely, splitting a skill into references/, or choosing granularity and naming. Adds: precision-router descriptions with framework API names, the Common-Mistakes + Review-Checklist bookends, two-tier references/, the Rationale/Deviation convention, evidence-based multi-reviewer CR. Does NOT cover general skill discipline (TDD-for-skills, when-not-to-create, token budgets) → superpowers:writing-skills.'
---

# Skill Authoring Patterns (Apple/Swift catalog layer)

This is a thin complement, not a replacement. **For the general discipline of writing a skill — whether a skill should exist at all, the test-first / RED-GREEN loop, matching the guidance form to the failure mode, and word-count budgets — use `superpowers:writing-skills` first.** This skill adds only what is specific to *this catalog* and to *Apple/Swift framework skills*: how to word descriptions so an agent routes to the right framework skill, the section conventions we standardize on, and how we review skills.

## When to invoke

- Writing a new `SKILL.md` for this repo (especially an Apple/Swift framework skill).
- Reviewing / CR-ing a skill for invocation precision and execution quality.
- A skill's `description` routes wrong (or over-fires); you're rewording it.
- A skill grew long and you're deciding what to move into `references/`.
- Choosing a new skill's name and granularity.

## Scope

This skill owns the *catalog-specific* and *Apple/Swift-specific* authoring conventions below. It does **not** own: the decision to create a skill, test-first skill development, or general prose-economy rules — route those to `superpowers:writing-skills`. Distribution/packaging (plugin vs marketplace, discovery) → `claude-skill-plugin-packaging`.

## Description as a precision router

The `description` is the only part of a skill that stays in the model's context by default (the body loads when the skill is invoked, and the description is length-capped). So spend its words on *routing*, not summary.

**Where this differs from `superpowers:writing-skills`**: that skill's description rule says
to write ONLY the trigger ("Use when…"), never what the skill does, aiming for under 500
characters. Its evidence is real but narrower than the rule it's stated as: an agent that
reads a description *summarizing a workflow's steps* will follow the description instead of
the body (this catalog's own gate encodes the same boundary as the "description may summarize
workflow" MINOR). The official Claude Code and Agent Skills docs, by contrast, specify
`description` as covering both *what* the skill does and *when* to use it. This catalog
follows the official contract: one verb-anchored **capability** sentence (the result, not the
steps) + trigger scenarios + a negative boundary when needed. A capability statement ("Resolve
Swift 6 concurrency errors…") is not a workflow summary, so writing one doesn't reproduce the
failure mode superpowers is guarding against — it still never enumerates workflow steps or
numeric thresholds in the description. This catalog's `DESC_MAX` (800 chars) is also
independent of superpowers' <500-char target; both are stricter than the official 1,536-char
listing cap for unrelated reasons.

- **Verb-anchored to observable intent:** "Resolve Swift 6 concurrency errors…", "Audit SwiftUI runtime performance…".
- **Embed the framework symbols / APIs that should trigger it** — `Sendable`, `@MainActor`, `MetricKit`, `AccessibilityFocusState`. This is the highest-leverage delta for *framework* skills: an agent routing on "I'm getting a Sendable error" only lands here if `Sendable` is in the description.
- **Chain trigger scenarios** as a short list ("Use when … ; when … ; when …").
- **Add a negative boundary when over-firing is a real risk** (e.g. "discussing screens" vs "generate a mockup") — name when NOT to fire.
- **If the trigger is really *a file type*** (`*.xcstrings`, `Package.swift`), prefer the official `paths:` frontmatter over a prose file trigger — it takes glob patterns, and Claude then loads the skill automatically only when working with matching files. `mise run check` flags prose file-triggers as `candidate for paths:`.
- Routing is the model's judgment, not literal string matching — write for a reader deciding "is this my situation?", not for a regex.

```
BAD:  description: Helps with accessibility.
GOOD: description: VoiceOver / Dynamic Type / touch-target implementation for SwiftUI & UIKit.
      Use when adding or auditing user-facing UI; when asked "make this accessible" / "VoiceOver
      doesn't read this" / "does this pass WCAG"; before an App Review a11y pass. Covers
      accessibilityLabel/value/hint/traits, Dynamic Type + minimumScaleFactor, 44pt targets.
      Does NOT cover deep Rotor/Focus APIs — see <sibling>.
```

## The listing budget is catalog-wide, not per-skill

Every enabled skill's `description` is always-on context, shared by a catalog-wide budget, not
a per-skill one — so before adding a skill, ask "is this trigger phrase worth permanently
occupying part of every session's listing budget?", not just "does this description fit under
800 chars". For the exact mechanism (the 1% context-window budget, the 1,536-char per-entry
cap, least-used-first truncation, the `when_to_use` field, and the measurement tools), read
`references/listing-budget.md`.

## Section conventions we standardize

Order the middle by the topic's pedagogy, but keep these conventions. All four bookends below
are required for **new** skills; none of them are retrofitted onto pre-existing skills — the
gaps in the "today" column are historical debt, not evidence the convention is optional:

| Heading | Purpose | Retrofit status | Today (of 38 skills) |
|---|---|---|---|
| `## Rationale` | *why* this default was chosen. Unique to this catalog. | Not retrofitted | 20/38 |
| `## Deviation considerations` | *when to override* the default, and the cost (e.g. "Drop to iOS 18 when an existing user base still runs it — every Liquid Glass API then needs an availability guard, and the pre-26 chrome must be snapshot-tested separately"). Also ours. | Not retrofitted | 22/38 |
| `## Common Mistakes` | concrete, anti-pattern-named items ("Using `DateFormatter()` in `body`"), as many as are real — do not pad to a number. | Not retrofitted; older skills express this as inline anti-pattern sections instead. | 10/38 |
| `## Review Checklist` | a `- [ ]` list at the **end**, runnable top-to-bottom. | Not retrofitted; older skills use a prose `## Verification checklist` instead. | 26/38 (incl. the older prose form; `mise run check`'s section matrix) |

- **`## Related skills`** — siblings by name.

Use a **scope-boundary** line in the body wherever a sibling is close ("owns X; does NOT own Y → route to `<sibling>`") — this is what stops two framework skills both claiming the same request.

### Skeleton (assembled)

```markdown
---
name: <kebab-matches-folder>
description: <precision router — see above>
---
# <Title>
<1-paragraph scope: what it implements/reviews + target version>
## When to invoke
## Scope            ← what it does NOT own → sibling
## <body: triage/workflow → decision table → rules → code>
## Rationale
## Deviation considerations
## Common Mistakes
## Review Checklist
## References        ← only if it has references/
## Related skills
```

## Structure aids (use where they fit — not universal)

- **Lead with a triage/workflow** ("Step 1 capture context → 2 smallest fix → 3 verify") for *procedural* skills. Skip it for pure reference/glossary skills — don't manufacture a procedure.
- **Front-load a decision table** (situation→fix, or option/best-for/complexity) wherever the agent must choose a path before implementing.
- **Add a `## Contents` TOC only for genuinely long skills** that a reader jumps around in — not by default; for a short linear skill it just costs tokens.

## Two-tier depth (references/)

Keep `SKILL.md` scannable: decision logic, short paired WRONG/RIGHT snippets (one point each), quick tables. Move long migrations, full API references, and big samples into `references/*.md` and **point to them from `SKILL.md` with a plain instruction** ("for the full guide, read `references/<topic>.md`"). This is a documentation convention — the agent reads those files via normal file reads when your `SKILL.md` tells it to; there is no automatic lazy-load. It keeps the always-in-context cost low while letting depth exist.

## Naming & granularity

- `name` is kebab-case; **our consistency gate requires `name` to equal the directory** (run `mise run check`) for clean cross-references and tooling. This is more than tooling hygiene: in a **plugin** skill — how every skill in this catalog ships — a `name` ≠ directory mismatch silently renames the command a user types; that's the failure our gate exists to block. For exactly how Claude Code derives a skill's command name in each install path, read `references/official-docs.md`.
- **One surface area per skill.** First-party skills in this catalog use a "topic + stance" compound name — `storekit2-iap-defaults`, `swift6-concurrency`, `swiftui-navigation-architecture`, `cloudkit-schema-source-of-truth` — rather than the bare Kit name. Bare Kit names (`widgetkit`, `storekit`, `swift-concurrency`) are already taken by the aggregated `apple-skills` plugin, so the compound name is also what keeps the two catalogs from routing to the same command. For cross-cutting topics use a descriptive compound at the right altitude — `swiftui-navigation-architecture`, not the too-broad `swiftui` nor the too-narrow `swiftui-observable`.

## Reviewing a skill (CR)

When you CR a skill or a batch, apply the evidence-based, multi-lens doctrine (it caught real errors in this catalog):

- **Diverse lenses, not one reviewer** — for a batch, dispatch reviewers with distinct expertise (correctness, a11y, security, performance, skill-authoring). Different lenses catch what redundancy can't.
- **Evidence for every falsifiable claim** — a reviewer flagging "this API/version is wrong" cites the source (Apple docs / Swift Evolution / WCAG), not "looks off"; each lists "what I did NOT verify + confidence".
- **Reviewers can be wrong → the Leader adjudicates** — don't take the union on faith. Verify disputed falsifiable claims yourself before accepting or overruling.

## Common Mistakes

1. **Vague one-line `description`** — the agent can't route to it. Use the precision-router form with API names.
2. **No negative boundary** on a skill that can over-fire — it produces unwanted artifacts.
3. **Description as summary, not router** — it restates the body instead of naming trigger conditions.
4. **No scope-boundary line** — two adjacent framework skills both claim the same request.
5. **Decisions buried in prose** instead of a table/triage when the agent must choose a path.
6. **Deep reference material inlined** into `SKILL.md`, bloating always-in-context cost — move to `references/`.
7. **Generic Common-Mistakes** ("write good code") instead of concrete, anti-pattern-named items.
8. **Project-specific workaround presented as general guidance** (e.g. "avoid `.task`, our build has bug #361") — ships wrong advice to every consumer.
9. **Stale/unverified API or version claim** — cite the source; a wrong version gate emits needless `#available` guards or won't compile.

## Review Checklist

- [ ] (General discipline per `superpowers:writing-skills`, **except** its description rule — see §Description as a precision router.)
- [ ] `name` equals the directory; `mise run check` passes.
- [ ] `description` is router form: verb-anchored, embeds the triggering framework APIs, lists trigger scenarios; a negative boundary if it could over-fire.
- [ ] A scope-boundary line names what the skill does NOT own and routes to the sibling.
- [ ] Choices the agent must make are in a table/triage, not prose.
- [ ] Deep material is in `references/*.md` with an in-body pointer; `SKILL.md` stays scannable.
- [ ] (New skills) `Rationale` + `Deviation` present; code uses current APIs with version gates marked inline.
- [ ] `Common Mistakes` are concrete and anti-pattern-named; no padding.
- [ ] No project-specific workaround dressed up as general guidance.
- [ ] Every falsifiable API/version claim spot-checked against an authoritative source (cite it).

## Related skills

- `superpowers:writing-skills` — **read first** for the general discipline this skill deliberately does not repeat.
- `claude-skill-plugin-packaging` — packaging/distribution/discovery of the authored skill.
- `subagent-review-cycles` — the round structure the evidence-based CR plugs into.
- Official sources: when verifying or updating a factual or version-sensitive claim, read `references/official-docs.md`.
