---
name: architect-review
description: "Design and code review: boundaries, coupling, cohesion, naming, complexity, code reuse, comment hygiene, refactor strategy. Use for a code, design or architecture review, refactor planning, or tech debt."
license: MIT
metadata:
  display-name: "Architect Review"
  version: "2.0"
  platforms: "claude-code codex"
  tags: "review architecture refactoring clean-code reuse comments"
---

# Architect review

Evaluate structure and intent, not just whether the feature ships. Read across files, not inside one.

## Checklist

- **Boundaries:** one reason to change per module; small intentional public surface; cycles are structural smells, break them by extracting the shared concept or inverting the dependency.
- **Coupling:** depend on abstractions the consumer controls. Business logic does not import the HTTP client or DB driver; inject them, along with config, clocks, randomness and IO.
- **Cohesion:** a file or class whose parts touch disjoint data is two units. A `utils` file of unrelated helpers is a smell.
- **Abstraction levels:** one level per function; policy and SQL do not share a body. Abstract at three real instances, not two; tolerate no fourth copy.
- **Naming:** a name says what a thing represents, not its type or caller. Reject `data`, `info`, `manager`, `handler`, `helper`, `util`. A good name deletes the comment that was about to explain it.
- **Dependency direction:** inward, toward stable abstractions. UI imports domain, never the reverse.
- **Complexity:** split functions above roughly 10 branches; flatten nesting beyond 3 with early returns; more than 4 parameters means an unnamed object; a flag parameter usually means two functions.
- **Errors:** failures are part of the domain, so use typed results or exceptions. Do not catch what you cannot handle. No empty `catch`.
- **Tests as feedback:** a function needing 9 mocks does 9 things. Tests that break on every refactor assert implementation, not behavior.

## Reuse

Assume the function, hook or component already exists. Grep for the concept, not the name you would give it, and check existing dependencies before hand-rolling.

- Name the search you ran ("grepped `debounce`, `throttle`: none"); "nothing else did this" is not checkable.
- Extend, do not fork: a near-duplicate with one different line needs a parameter, unless the parameter is a boolean switch, which is two functions.
- Not reuse: a wrapper with one call site, a re-export with no behavior, a grab-bag import, a new dependency to save five lines.
- Delete the code the reuse replaced. Two coincidental copies are not duplication; forcing a shared helper couples them.

## Comments

The default is zero. Keep a comment only when removing it would let a competent reader introduce a bug: a hidden constraint, a subtle invariant, a named-bug workaround, a surprising behavior. Flag in review:

- restating the code, narrating a change, provenance or caller notes, ticket or PR references, banners, commented-out code;
- a bare `TODO` with no owner or condition;
- docstrings that repeat the signature; keep only units, ranges, side effects, throws.

One line, phrased as the reason, directly above the surprising line.

## Method

1. Read the diff once, top to bottom, and form a hypothesis of what it really does.
2. Place it: which layer, which boundary, does dependency direction hold?
3. List concerns by severity; give the smallest change that resolves each. "Extract these 3 lines as `x`" beats "rewrite the module".
4. Note what is good so the pattern repeats.

Severity: Blocker (correctness, security, data loss) / Should-fix (compounding design debt) / Nit.

Refactors preserve behavior, one per commit, tests green after each step. A behavior change is its own change.

Not a style pass: formatting belongs to the formatter. The stress pass that follows is `adversarial-review`.
