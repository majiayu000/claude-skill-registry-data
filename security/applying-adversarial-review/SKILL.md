---
name: applying-adversarial-review
description: >
  Applies Kyle's adversarial review methodology to consequential outputs.
  Forces every recommendation, audit, plan, or claim through three checks
  before shipping: a CLAIMS / COUNTEREXAMPLE / CONTRADICTIONS footer,
  [SOURCED] vs [GENERATED] provenance labeling, and an agreement-streak
  flag at three consecutive consequential agreements.
  Activates when finishing an audit, writing a recommendation, delivering
  a plan, drafting a decision memo, or producing any high-stakes deliverable.
  Also triggers when explicitly asked to pressure-test, stress-test,
  steelman, play devil's advocate, fight an idea, or check for blind spots.
  Triggers on: adversarial review, anti-sycophancy, claims footer, stress
  test this, steelman this, pressure test, devil's advocate, am I missing
  anything, what could go wrong, sourced vs generated, agreement streak,
  push back on this, where am I wrong, review this PR, pull request review,
  code review, PR feedback.
metadata:
  version: "1.1.1"
---

# Applying Adversarial Review

**Three layers, applied in order: provenance labels → CLAIMS footer → streak flag.**

Prevent the most expensive mistake in advisory work: confident agreement that turns out to be wrong. Every consequential output gets the appropriate review tier before shipping. Full templates: see `templates/`. Worked examples: see `examples/`.

---

## Activation Decision Tree

```
Is this consequential? (User might act on it. Could be wrong in ways that matter.)
  ├─ No (lookup, transformation, casual chat) ─── Do NOT activate. Just answer.
  └─ Yes
       ├─ Low-stakes (movie pick, draft phrasing) ─── LITE:     Footer only
       ├─ Medium (recommendation, audit, plan) ────── STANDARD: All three layers
       └─ High (security, financial, medical, legal) HEAVY:    All three + escalation framing
```

**Streak override:** Agreement count crosses 3 → the streak flag fires regardless of tier, even on LITE.

Detailed gray-zone calls: `references/decision-rubric.md`.

---

## Tier Summary

| Tier     | Provenance labels       | CLAIMS footer  | Streak tracking  | Use when                                    |
|----------|------------------------|----------------|------------------|---------------------------------------------|
| LITE     | One-line attribution    | Skip           | Active           | Small recommendations, casual decisions     |
| STANDARD | Per-section or inline   | Required       | Active           | Audits, plans, technical recommendations    |
| HEAVY    | Per-assertion inline    | Required + redirect to qualified sources | Active | Auth, payments, medical, legal, named-individual claims |

---

## REQUIRED OUTPUT SCHEMA

Every adversarial review response must contain these sections in this order.

**CLAIMS**
Every claim labeled [SOURCED] (with citation) or [GENERATED] (reasoned estimate). No unlabeled assertions.

**COUNTEREXAMPLE**
At least one concrete scenario where the recommendation fails or the opposite is defensible.

**CONTRADICTIONS**
Prefix each with `!`. Minimum one. If none found after genuine search: state "CONTRADICTIONS: None found — [reason why]."

**AGREEMENT STREAK CHECK**
If this is the 3rd+ consecutive agreement with the user's position on a consequential topic: flag ⚠ and offer a challenge pass. Otherwise omit this section.

---

## The Three Layers

### Layer 1 — Provenance labels

Every consequential assertion is `[SOURCED]` (traceable to a tool result, document, prior turn) or `[GENERATED]` (model's own inference, framing, synthesis). Mixed statements get split.

**Quick rule:** "If this is wrong, where is the error?" Source error → `[SOURCED]`. Reasoning error → `[GENERATED]`. Both → split.

Full labeling guide and edge cases: `references/labeling-guide.md`.

### Layer 2 — CLAIMS / COUNTEREXAMPLE / CONTRADICTIONS footer

Three named sections. Template: `templates/footer-template.md`.

- **CLAIMS** — 2-4 load-bearing assertions the user would push back on if wrong
- **COUNTEREXAMPLE** — for each major claim, a specific named scenario where it breaks
- **CONTRADICTIONS** — internal, against prior context, or against user's stated goals

If you cannot find a real counterexample, the response is too shallow to need the footer. Skip to LITE.

### Layer 3 — Agreement streak flag

Track consecutive consequential agreements per conversation. At the third in a row, prepend the flag. Template: `templates/streak-flag-template.md`. Mechanics: `references/streak-tracking.md`.

---

## Output Structure

Every STANDARD/HEAVY response follows this shape:

```
[Streak flag, if applicable]

[Body of response with [SOURCED]/[GENERATED] labels]

---

[SOURCED] One-line summary of what came from where
[GENERATED] One-line summary of what is inference

**CLAIMS / COUNTEREXAMPLE / CONTRADICTIONS**

- *Claim:* [load-bearing assertion 1]
  *Counterexample:* [specific failure scenario]
- *Claim:* [load-bearing assertion 2]
  *Counterexample:* [specific failure scenario]
- *Contradiction:* [tension surfaced]
```

LITE skips the CLAIMS block. HEAVY adds an explicit redirect-to-qualified-source line above the footer.

---

## Usage Examples

**LITE — Small recommendation**
User: "Should I use Postgres or MySQL for a side project?"
→ Body: 3-bullet comparison + recommendation.
→ One-line attribution: "[GENERATED] based on your stated needs; [SOURCED] feature notes from official docs."
→ No footer. Streak counter increments if agreement.
→ Full example: `examples/01-lite-side-project.md`

**STANDARD — Audit**
User: "Audit my deployment pipeline."
→ Body: 8-bullet audit, 3 risks, 2 quick wins, with inline `[SOURCED]`/`[GENERATED]`.
→ Footer: 3 claims, 3 counterexamples, 1 contradiction (user's "ship fast" goal vs. proposed staging gate).
→ Streak counter increments if user agrees.
→ Full example: `examples/02-standard-audit.md`

**HEAVY — Security recommendation**
User: "Should I store API keys in Vercel env vars or use AWS Secrets Manager?"
→ Body: comparison + recommendation + explicit "I'm not your security architect" redirect.
→ Per-assertion `[SOURCED]`/`[GENERATED]` labels.
→ Full footer + escalation note pointing to qualified review before production.
→ Full example: `examples/03-heavy-security.md`

**Streak flag fires**
After three consecutive consequential agreements, the next response prepends the flag. The flag does not commit to disagreement — it commits to harder scrutiny.
→ Full example: `examples/04-streak-flag-fires.md`

**Skip — non-consequential**
User: "What's the syntax for a Python list comprehension?"
→ Direct answer, no labels, no footer, streak counter unchanged.
→ Full example: `examples/05-skip-justified.md`

---

## Anti-Patterns

1. **Theater footer.** Generic "this could be wrong" instead of named failure modes. → Force a specific scenario or skip to LITE.
2. **Label-washing.** Tagging inference as `[SOURCED]` because it sounds authoritative. → If the model produced it, it is `[GENERATED]`.
3. **Streak amnesia.** Forgetting the count carries across the whole conversation. → Track explicitly.
4. **Universal application.** Applying the footer to every response devalues the signal. → Trust the decision tree.
5. **Comfortable contradictions.** A contradiction exists and was not surfaced. → Failure regardless of how minor.
6. **Hedging instead of sourcing.** "I think" or "probably" replacing `[GENERATED]`. → Label explicitly, then state the view.

---

## Self-Verification

Before shipping any consequential response:

1. [ ] Tier selected via decision tree (LITE / STANDARD / HEAVY)
2. [ ] Provenance labels applied at the granularity the tier requires
3. [ ] CLAIMS section has 2-4 load-bearing assertions, not platitudes (STANDARD/HEAVY)
4. [ ] Each COUNTEREXAMPLE names a specific concrete failure scenario (STANDARD/HEAVY)
5. [ ] CONTRADICTIONS were searched for, not just declared absent (STANDARD/HEAVY)
6. [ ] HEAVY tier includes redirect-to-qualified-source line
7. [ ] Streak count updated; flag prepended if streak ≥ 3
8. [ ] Output line stated: tier + streak count

**Output line:**
```
Tier: [LITE|STANDARD|HEAVY]. Streak: [N]. [Flag fired | No flag.]
```

---

## Skill Interactions

- **engineering-staff-workflows / applying-sparc-methodology:** When inside an Implement phase, the adversarial review applies to the outputs (recommendations, design choices), not the intermediate code.
- **code-auditor / code-transfer:** Audit outputs are STANDARD-tier by default. Code mechanics (transfers, refactors) are non-consequential and skip review.
- **debug-like-expert:** Hypothesis ranking gets `[GENERATED]` labels. Confirmed root causes get `[SOURCED]` from the evidence chain.
- **generating-social-posts:** Voice rules win over adversarial labels in published copy. Apply review to strategic claims about tools/people only, not to the post itself.

---

## Iteration

After shipping a reviewed response, do not ask the user to validate the footer. The footer is for them to use, not approve. If they push back on a claim, treat the pushback as streak-resetting feedback and re-apply the tier on the response.

---

## CLAIMS

- [GENERATED] Forced provenance labeling reduces the rate at which inference smuggles itself into apparent fact
- [GENERATED] Specific named counterexamples are operationally more useful than generic uncertainty hedges
- [GENERATED] An agreement-streak flag breaks sycophancy spirals that pure self-criticism misses
- [SOURCED] Three-tier scope gating mirrors Kyle's existing SCOPE_MODE LITE/STANDARD/FULL pattern from prior conversations

## COUNTEREXAMPLE

- The footer can become performative theater: a model that always produces three plausible-sounding counterexamples may be hallucinating epistemic rigor rather than practicing it
- Streak flagging assumes the user wants disagreement. In creative brainstorming or emotional-support contexts, the streak is the point and flagging it is friction
- Tier selection itself is `[GENERATED]` — the model judges its own consequential-vs-non call, which is the exact judgment the methodology is meant to scrutinize

## CONTRADICTIONS

- "Apply only when consequential" relies on a judgment the methodology is meant to scrutinize. The skill must trust its own decision tree — circular, but operationally necessary
- Per-assertion inline labeling on HEAVY tier conflicts with prose readability; in practice this is often relaxed into per-section labeling, weakening the strict standard
