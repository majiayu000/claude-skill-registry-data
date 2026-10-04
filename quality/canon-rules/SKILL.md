---
name: canon-rules
description: >-
  Reference catalog of canon enforcement principles, epistemological operating
  rules, metascience diagnostic filters, adversarial validation protocols, and
  anti-patterns to avoid. Use as a reference when auditing fails, when a new idea
  conflicts with existing canon, when diagnosing inconsistency, or when user says
  "anti-patterns", "epistemology", "canon rules", "reasoning principles", "how do
  I check this", "what am I missing", "why is this inconsistent", "grill me harder",
  "adversarial review", "red team this", or "Russell Conjugation". Does NOT execute
  audits — use /auditing-physics or /auditing-canon for that.
model: haiku
effort: low
---

# Canon Rules — Epistemology, Adversarial Protocols & Anti-Patterns

## Quick Reference — The Five Operating Principles

1. **Mechanism over association** — state the causal chain or it's not proven
2. **First-principles over tropes** — derive from physics/biology, not genre convention
3. **Evidence hierarchy** — canon source > derived lore > cross-ref inference > "feels right"
4. **Anti-reductionism** — trace implications through every connected system
5. **Adversarial self-validation** — "what existing canon contradicts this?"

## Detailed References (load on demand)

- `references/epistemological-framework.md` — Full framework with named sources:
  Ioannidis corollaries, Garden of Forking Paths (Gelman), Aesthetic Fallacy
  (Hossenfelder), Humpty Dumpty Problem (Taleb), predictive power as ultimate
  metric (Broken Science Initiative), OODA Loop (Boyd)

- `references/adversarial-protocols.md` — Adversarial Red Teaming, Adversarial
  Collaboration (Kahneman protocol), Russell Conjugation stripping, Self-Correction
  Loop, Ensemble Thinking (Diversity Prediction Theorem)

- `references/metascience-canon-filters.md` — 6 diagnostic filters adapted from
  Ioannidis for worldbuilding: sample size, effect size, confirmation bias, flexible
  analysis, replication, survivorship bias

## Anti-Patterns (Quick List)

- **Vague Lore** — generic without checkable detail
- **Missing Locked Canon** — settled decisions not recorded
- **No Verification Step** — declaring clear without full-repo grep
- **Too Much in One Pass** — mixing physics + prose audits
- **Patching Forward** — 3+ contradictory fixes → revert, rethink
- **Flexible Analysis** — reinterpreting a rule to accommodate new lore
- **Trusting Without Location** — no file + line = reject the finding
- **The New Orthodoxy Trap** — the system itself becoming rigid dogma (see Weinstein critique)

## Out of Scope

This skill is a reference catalog. It does NOT execute audits (use /auditing-physics
or /auditing-canon), stress-test decisions (use /interrogating-design), or check wiki
structure (use /lint-wiki).
