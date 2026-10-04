---
name: adr
description: Audit, write, or revise Architecture Decision Records (ADRs), including the decision of whether one is warranted. Use when an architecturally significant decision needs recording, when reviewing an existing ADR collection, or when adding ADRs to a project that has none. Detects existing template (Nygard or MADR) and defaults to Nygard for new repos. Gates comparison ADRs through a decompose-and-verify interview before drafting.
---

# ADR

References:

- <https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions> — Nygard, original.
- <https://adr.github.io/madr/> — MADR, structured variant.
- <https://adr.github.io/> — umbrella, organisational guidance.

## Is one warranted?

- Yes: architecturally significant *and* hard to reverse — sets
  precedent others will follow, locks in a dependency, shapes a public
  API, picks between non-trivial alternatives.
- No: tactical implementation choice, easily reversed, personal style,
  framework-default behaviour. A commit message or PR description
  carries it better.
- If not warranted, say so and stop. ADR sprawl makes the collection
  worth less.

## Template

Detect, don't impose:

1. If the repo already has ADRs (`docs/adr/`, `doc/adr/`,
   `docs/decisions/`, `docs/explanation/adr/`), read one and match
   shape.
2. If repo-local `CLAUDE.md` names a template ("ADRs use MADR"),
   respect it.
3. Otherwise: **Nygard** for a single decision; escalate to **MADR**
   only when alternatives analysis is genuinely load-bearing (3+
   options worth comparing across multiple drivers). Call that case a
   *comparison ADR*.

### Nygard skeleton

- **Title** — `# N. <imperative phrase>` (e.g. "Use PostgreSQL").
- **Status** — `Proposed` initially; user promotes to `Accepted`,
  `Superseded by NNNN`, or `Deprecated`. Don't pre-mark `Accepted`.
- **Context** — forces in play, constraints, what made this a
  decision.
- **Decision** — `We will <do X>`. Active voice.
- **Consequences** — what becomes easier *and* harder; positive,
  negative, neutral.

### MADR

Use the upstream template at <https://adr.github.io/madr/>; don't
re-derive it here. Sections that earn their weight: Decision Drivers,
Considered Options (with pros/cons), Decision Outcome.

## Decompose and verify

Comparison ADRs only; a single-decision Nygard record skips it.

A comparison ADR that starts from an inherited conclusion
reverse-justifies it with abstract drivers ("cross-surface leverage",
"maintenance burden") and never examines the facts that decide it. Run
this interview with the user before any Context, driver, or outcome
prose exists:

1. **Options** — name the concrete candidates under comparison.
2. **Requirements** — get the targets from the user, enumerated. Not
   from memory, not inferred from the options.
3. **Option × requirement** — for each pair, state the fact and where
   it came from. Reachability, feasibility, and cost decide most tool
   choices; verify those pairs first. Anything assumed, recalled, or
   unchecked is a blocker: search it before continuing, and never
   write the Decision Outcome over an open one.
4. **Inherited answer** — name the option that arrived pre-chosen, if
   any. Check whether each driver tests that option or flatters it; a
   driver only the pre-chosen option satisfies is there to justify it.
5. **Draft** — every Decision Driver cites a verified fact from step
   3. Cut any driver that can't; don't hedge it.

## Location and filename

- Default `docs/adr/` for new repos. Match existing layout if present.
- Filename: `NNNN-kebab-title.md`, NNNN is the next 4-digit sequence
  (`0001`, `0002`, ...).
- If no ADRs exist yet, scaffold `0000-record-architecture-decisions.md`
  first (the meta-ADR establishing the practice itself).

## Procedure

1. Decide warranted vs. not. If not, stop.
2. Detect template and location from existing ADRs or repo `CLAUDE.md`.
3. For a comparison ADR, run *Decompose and verify* before drafting.
4. Compute next sequence number. If first ADR, scaffold the meta-ADR
   too.
5. Surface chosen template, location, and a one-line decision summary
   before drafting full content. Apply after agreement.
6. Default Status to `Proposed`. The team promotes it after the
   decision is actually made.
