---
name: senior-engineering-best-practices
description: >
  Use in any development session that benefits from a senior engineer's accumulated judgment,
  methodology, and runbooks — broader than any single category, most agents don't have these
  instincts by default. Concrete triggers: proposing a workaround/patch/shim for external code;
  answering from memory about what a library/SDK/framework supports; patching the same area of
  code a second or third time; treating an old "verified" finding as settled when it's currently
  blocking a fix; a guard/fix that has a passing test but hasn't been checked against real
  production data shape; assuming merged code is deployed code; a fix that generalizes beyond
  where it was found and needs to be propagated and audited for complete adoption; adding a new
  dependency; writing code whose failure would be undebuggable in production; taking an action
  whose reversibility/blast-radius hasn't been considered; planning high-stakes infrastructure
  or architecture for a system with broad blast radius. Routes to the matching runbook here, or
  to a more specific existing skill (TDD, SOLID, DDD, debugging, verification, code review,
  brainstorming, security) when one already covers the situation.
metadata:
  last_updated: "2026-08-23"
---

# Senior Engineering Best Practices

Most agents don't have the instincts a senior engineer builds over a career — not because the
instincts are secret, but because nobody wrote them down where an agent would find them at the
right moment. This skill is that: a growing, incident-anchored collection of judgment calls a
senior engineer makes by reflex, plus a router to the skills that already cover the ones with a
home elsewhere.

**This skill does not duplicate what already exists.** If a situation is already covered by
`test-driven-development`, `solid-principles`, `domain-driven-design`, or a `superpowers` skill,
route there — see [Route to an existing skill](#route-to-an-existing-skill) below. This skill's
own `references/` hold only instincts that had no home before it existed.

## Route to a runbook here

| Situation | Read |
| --- | --- |
| About to propose a workaround/patch/shim for third-party code, or answer from memory about what a library/SDK/framework supports | [`references/verify-before-acting.md`](references/verify-before-acting.md) |
| A bug's symptom recurred after being "fixed," or you're about to patch the same area again | [`references/progressive-root-cause-discipline.md`](references/progressive-root-cause-discipline.md) |
| You found the real root cause and fix — now decide where else it applies | [`references/extract-and-propagate-the-real-fix.md`](references/extract-and-propagate-the-real-fix.md) |
| Deciding how much ceremony/caution an action deserves | [`references/blast-radius-judgment.md`](references/blast-radius-judgment.md) |
| About to write new code, or code is showing a smell | [`references/prior-art-and-code-smells.md`](references/prior-art-and-code-smells.md) |
| Considering adding a third-party dependency | [`references/dependency-judgment.md`](references/dependency-judgment.md) |
| Writing code that could fail in production | [`references/observability-instinct.md`](references/observability-instinct.md) |
| Code touches a loop, a query, pagination, or I/O on a hot path | [`references/performance-pattern-matching.md`](references/performance-pattern-matching.md) |
| A bug just got fixed — is it a one-off or a systemic gap? | [`references/fix-the-process-not-just-the-instance.md`](references/fix-the-process-not-just-the-instance.md) |

**Planning high-stakes infrastructure or architecture?** No single runbook covers this — read
`blast-radius-judgment`, `prior-art-and-code-smells`, `dependency-judgment`, and
`observability-instinct` together; each contributes one facet (risk scaling, not reinventing what
already exists, dependency cost, and designing in debuggability before it ships).

## Route to an existing skill

Don't duplicate — these situations already have a home:

| Situation | Already covered by |
| --- | --- |
| Ambiguous requirements / new feature design | `superpowers:brainstorming` |
| Writing a feature or bugfix | `superpowers:test-driven-development` |
| Any bug, test failure, unexpected behavior — the mechanics of investigating it | `superpowers:systematic-debugging` |
| About to claim a task complete | `superpowers:verification-before-completion` |
| Receiving code review feedback | `superpowers:receiving-code-review` |
| Class/interface/module design | `agent-skills:solid-principles` |
| System/domain architecture | `agent-skills:domain-driven-design` |
| Auth/crypto/input-validation/secrets/external APIs | `security-review` |
| Editing an existing skill, runbook, or instruction file (`SKILL.md`, `AGENTS.md`, `CLAUDE.md`) | `agent-skills:agent-instructions` (`references/editing-discipline.md`) |
| Creating a brand-new skill from nothing | `superpowers:writing-skills` |

## Red flags — stop and reconsider

- "This library doesn't support X." → Verify. You probably haven't checked the current docs yet.
  See `verify-before-acting.md`.
- "I already fixed this once." → If the symptom is back, the first fix addressed a symptom, not
  the cause. See `progressive-root-cause-discipline.md`.
- "That was verified in an earlier investigation." → An old "verified" claim that's currently
  blocking a fix is a hypothesis to re-test, not settled fact. See
  `progressive-root-cause-discipline.md`.
- "The fix is merged." → Merged is not deployed. Verify the artifact actually running, not just
  the source. See `progressive-root-cause-discipline.md`.
- "I fixed it here, that's done." → If the same defect shape exists in three other places, "done"
  means auditing all of them, not just the one you started with. See
  `extract-and-propagate-the-real-fix.md`.
- "It has a passing test." → A passing test proves the test data shape works, not that production
  data has that shape. See `progressive-root-cause-discipline.md`.
- "I'll just add this dependency, it's small." → Check maintenance burden and removal cost first.
  See `dependency-judgment.md`.
- "It'll throw an error if it fails, that's enough." → Will the error say what was expected vs.
  what happened, to someone with no context, later? See `observability-instinct.md`.

## Growth protocol

A new runbook is added here only once there's a real incident to anchor it — grep or cite the
transcript, PR, or postmortem where its absence caused a failure, write the runbook, link it from
the table above. This mirrors the RED→edit→GREEN discipline in
`agent-skills:agent-instructions`'s `references/editing-discipline.md` — read that before adding
or revising a runbook here. No speculative runbooks — an unanchored "best practice" is exactly
the kind of padding this skill exists to avoid producing.
