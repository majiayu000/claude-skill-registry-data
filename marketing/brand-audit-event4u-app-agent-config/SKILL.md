---
model_tier: inherit
name: brand-audit
description: "Audit how a brand is currently expressed across touchpoints and flag drift from its defined tokens, voice, and strategy. Use to inventory and critique an existing brand before changing it."
domain: engineering
personas:
  - brand-strategist
workspaces:
  - engineering
packs:
  - brand
trust:
  level: professional
install:
  removable: true
scope:
  write: []
  verification_reason: "execution declares no handler, so this skill runs nothing of its own — every write is the calling agent's, under the rules that govern it. No command can prove a scope the skill never executes."
execution:
  type: manual
---

# brand-audit

Method skill. Inventories current brand expression across touchpoints and flags drift against defined brand tokens, voice, and strategy. For the UI surface it leans on `existing-ui-audit` rather than re-implementing component inventory. Output is a drift findings list — not a redesign.

## When to use

- Before a rebrand or brand refresh — establish the baseline first.
- When auditing brand consistency across touchpoints (web, decks, docs, ads, copy).
- To create an evidence base before running `brand-strategy`.
- When "is this on-brand?" needs a systematic answer across many assets, not a gut call.

## Procedure

1. **Gather the source of truth.** Collect the consumer brand's defined tokens (palette, type scale, logo rules), voice profile, and strategy doc if they exist. Consumer brand definition is authoritative; corpus defaults are gap-fill only.
2. **Inventory current expression per touchpoint.** Cover logo usage, colour palette, typography, voice/copy tone, imagery style, and iconography across the relevant surfaces (site, app, decks, marketing, docs).

   **Personal and company profile surfaces, including LinkedIn, X, and GitHub
   organization profiles, are deliberately excluded regardless of whether their
   content is fetched, pasted, or supplied as a file, pending a written
   public-profile-field privacy floor defining what may be processed.**

   Recorded so the next reader does not re-derive the gap, which has already
   happened once. The exclusion is about **handling**, not retrieval: a pasted
   profile is mechanically a different thing from a network fetch, but the
   missing artefact is a field-level classification saying which profile fields
   are brand surface (logo, palette, bio messaging) and which are PII-adjacent
   (employment history, contributor names, location). A profile's About text
   carries both in one field. Without that classification the skill cannot
   distinguish them, and no test can assert that it did. AI council 2/2,
   2026-08-25. Include user-supplied profile inputs once a written, testable
   field-level privacy floor exists; include fetched inputs only after both that
   floor and a host-agent fetch contract exist.
3. **UI surface.** Invoke `existing-ui-audit` for UI component inventory. Do not re-implement it here — take its output as an input to this audit.
4. **Compare observed vs. defined.** For each touchpoint value, check it against the matching token or voice rule.
5. **Classify each finding.** Three buckets: `on-brand` (matches the defined token), `drift` (observed value diverges from the token), `undefined` (no token exists to audit against — this is a governance gap, not automatically wrong).
6. **Rank drift findings** by visibility (how prominent the touchpoint is) multiplied by frequency (how often it appears). Surface the top items first.
7. **Verify completeness.** Confirm every inventoried touchpoint is classified (`on-brand` / `drift` / `undefined`) — the audit is complete only when the classified count equals the inventoried count, and `existing-ui-audit` has run for every in-scope UI surface. Ensure each drift finding cites BOTH the defined value and the observed value; a finding missing either side is not yet verified.
8. **Output the findings list** (see Output format). Do not redesign or author replacements — hand drift findings to `brand-identity` or `brand-strategy`.

## Two constraints on platform-specific guidance

Both are constraints on what this skill may assert, not machinery, and neither
is a registry.

- **Any platform-specific guidance carries a source tier and a review date.**
  Platform conventions — an image aspect ratio, a character limit, where a
  profile crops a banner — change without notice, so a number stated here
  without a date and a source is a claim that quietly stops being true. Tier it
  (`platform-doc` / `observed` / `inferred`) and date it, or take it from the
  platform's own current spec at audit time instead of stating it.
- **No engagement metric is stated as fact.** Reach, impression and
  best-time-to-post figures are platform- and account-specific and are not
  auditable from a brand token. Where such a figure is load-bearing to a
  finding, attribute it; never assert it as a general truth.

## Output format

1. **Source-of-truth summary** — what brand tokens, voice rules, and strategy exist and where they were found (or "none defined" if absent).
2. **Drift findings** — table-style list: `touchpoint | defined value | observed value | severity (high/medium/low)`.
3. **Undefined gaps** — values with no token to check against; listed separately so they can feed a token-creation pass.
4. **Ranked top drift** — ordered list of the highest-severity drift items to fix first, with a one-line rationale per item.

## Do NOT

- Redesign or author replacement assets — that is `brand-identity` work, not audit work.
- Re-implement UI component inventory — call `existing-ui-audit` and consume its output.
- Invent a "correct" value where none is defined — mark the finding `undefined` and surface it as a governance gap.
- Treat corpus defaults as the consumer's source of truth — consumer brand definition always wins.

## Gotcha

- `undefined` is a real finding. A value with no token to check against is a governance gap that deserves its own section, not a pass.
- Drift severity is visibility times frequency, not personal taste. A rarely-seen off-palette icon ranks lower than a wrong primary colour used on every page header.
- Consumer brand tokens outrank any corpus default. If the consumer has defined a token, audit against that; ignore what the corpus suggests.

## See also

- [`existing-ui-audit`](../existing-ui-audit/SKILL.md) — the UI-surface inventory this skill reuses.
- [`brand-strategy`](../brand-strategy/SKILL.md) — where drift findings feed a refreshed strategy.
- [`brand-identity`](../brand-identity/SKILL.md) — defines the tokens audited against.
- [`brand`](../brand/SKILL.md) — the corpus of brand defaults (gap-fill only).
