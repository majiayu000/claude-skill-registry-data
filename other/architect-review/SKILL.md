---
name: architect-review
description: Use when the user pastes an architecture artifact (design doc, diagram, RFC, ADR) and asks for critique. Triggers on "review this", "what's wrong with", "is this any good", or any artifact-shaped paste with a question attached. Produces a verdict (SHIP IT / SHIP WITH CHANGES / MAJOR REWRITE / WRONG ARTIFACT), executive summary, severity-tagged findings, and a closing "what's working" section. Also runs a well-architected / lens review mode (concern + workload-class lenses incl. GenAI/agentic) emitting a risk register with mechanical/judgment-tagged findings. Inline only. Do NOT use to produce an artifact (use `architect-design` or `architect-diagram`).
---

# Skill: architect-review

Critique an existing architecture artifact. Severity-tagged findings,
genre-aware rubric routing, no file write — reviews are throwaway
artifacts.

## When to invoke

Before reviewing, confirm:

1. There is an *artifact in scope* — pasted into the conversation,
   linked, or named at a known path. "Review our architecture" with
   nothing concrete attached is a design conversation, not a review.
2. The artifact is *finished enough to critique*. A two-bullet
   outline is a discussion; a draft with all the sections at least
   started is a review. Don't critique tumbleweeds.
3. The user wants *severity-tagged findings*, not a discussion. If
   they want a conversation, route to `architect-design` (if installed)
   or tell the user to switch to a design-conversation surface.

If any check fails, push back rather than reviewing.

## Procedure

1. **Identify the artifact type.** Read the paste; pick one:
   - Design doc (Google-style or close to it) → `references/rubric-design-doc.md`
   - C4 Container / Context diagram → `references/rubric-c4-diagram.md`
   - Sequence diagram → `references/rubric-sequence-diagram.md`
   - State diagram → `references/rubric-state-diagram.md`
   - ER diagram → `references/rubric-er-diagram.md`
   - Something else, or unclear → `references/rubric-generic.md`

   If the artifact is the *wrong shape for the question* — a sequence
   diagram when the user wanted topology, an ADR when the user wanted
   a design doc — flag it with the **WRONG ARTIFACT** verdict and
   route to the right skill.

2. **Or — well-architected lens mode** (orthogonal to artifact type): when the
   ask is whether a *design* is well-architected (provider / pillar / a named
   concern- or workload-class lens, incl. GenAI/agentic), walk
   `references/rubric-well-architected.md` and write `assets/risk-register.md` —
   it tags each finding **🔧 mechanical / 🧭 judgment** + scenario, reuses the
   verdict/severity below, and does **not** auto-fix (a critique, not the loop).

3. **Walk the rubric.** Read every check; note the failures. Do not
   start writing findings yet — finish the rubric pass first so the
   findings can be ordered by severity, not by discovery order.

4. **Check that load-bearing claims are grounded** (orthogonal to artifact type
   and to the WA-lens mode above). When the artifact asserts facts about the
   current landscape, mandated standards, external interfaces, or in-flight work
   — claims a reviewer can't take on faith — load
   `references/knowledge-surfaces.md` and flag, as severity-tagged findings, (a)
   any such claim asserted as fact with neither a cited surface nor an
   "unverified — confirm" marker, and (b) any available knowledge surface the
   design ignored. If an internal retrieval surface is reachable this session
   (public web does not count), you may spot-check the claims against it — to
   confirm or refute, never to redesign — and name what you checked against (or
   "none"); otherwise flag the unverified claims for the author to confirm rather
   than guessing. **Flag; never rewrite the design.** When the artifact asserts
   no such facts, skip this step.

5. **Decide the verdict** before writing the findings:
   - **SHIP IT.** Zero blockers, ≤2 minors. Rare and worth saying so.
   - **SHIP WITH CHANGES.** Blockers absent or trivially fixable;
     majors exist but the artifact's shape is right.
   - **MAJOR REWRITE.** Two or more blockers, or one blocker that
     invalidates the artifact's structure.
   - **WRONG ARTIFACT.** The artifact answers a question the user
     didn't ask. Name the right artifact and route.

6. **Write the review** using `assets/critique.md` (or `assets/risk-register.md` in WA mode):
   - Verdict (one line).
   - Executive summary (≤3 sentences).
   - Findings, ordered by severity, each with: **where** (5–10 words
     quoted verbatim, or section + paragraph), **what's wrong** (one
     sentence naming the failed rubric check), **suggested fix**
     (concrete, paste-able where possible).
   - **What's working** (2–4 specific reusable strengths). Not
     flattery. Things the author should *keep* during a rewrite.

7. **No file write.** Render inline. If the user explicitly asks to
   save the review, write to a path they choose with a kebab-case
   slug — but the default is throwaway.

## Severity glossary

| Tag | Meaning | Example |
| --- | --- | --- |
| 🟥 blocker | Ship-stopping. Wrong, misleading, or unsafe to act on as-is. | TL;DR contradicts proposal; trust boundary unlabeled; alternatives are strawmen. |
| 🟧 major | Not ship-stopping but materially weakens the artifact. | NFRs missing; one alternative is a strawman; technology label missing on a Container. |
| 🟨 minor | Author should fix; reviewer won't block on. | Edge labels inconsistent; non-goal phrasing weak. |
| ⚪ nit | Style / formatting. Optional. | Capitalization, indentation, oxford-comma. |

## Anti-patterns to refuse

- **Reviewing your own draft from the same session.** If the user
  asked you to produce the artifact, reviewing it back yourself is
  marking your own homework. Push back and ask the user (or another
  agent) to drive the critique.
- **Writing a critique without a rubric.** Reviews without explicit
  rubric anchors read as opinion. Always cite the rubric check that
  failed.
- **Padding "what's working" with flattery.** "Clear writing" and
  "good structure" alone are filler. Name specific things the
  author should preserve.
- **Burying the verdict.** Verdict goes first. The reader should not
  have to scroll past 12 findings to learn the artifact is broken.
