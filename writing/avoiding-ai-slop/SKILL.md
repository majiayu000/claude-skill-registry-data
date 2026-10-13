---
name: avoiding-ai-slop
description: >
  Detects and eliminates AI-slop from text, prose, and image prompts using a
  76-rule structural pattern corpus, a 237-term tiered ban lexicon, and an
  image-slop negative-prompt pack, with a slopcheck.py linter for scan,
  calibrate, and allowlist workflows. Activates on: de-slop this, deslop,
  anti-slop, AI slop, sounds like AI, reads like ChatGPT, AI tells, humanize
  this, make this sound human, remove AI words, overused AI words, banned
  words check, slop scan, slopcheck, cliché check, AI writing check, delve,
  tapestry, em-dash overuse, negative parallelism, it's not X it's Y, image
  slop, negative prompts for AI images, calibrate slop thresholds, refresh the
  slop list. Also applies silently as writing constraints when drafting
  outward-facing prose — blog posts, LinkedIn, newsletters, docs, marketing
  copy. NOT for attributing third-party text to AI (no authorship claims) and
  NOT for icon slop (use purging-icon-slop).
version: "5.0.0"
---

# Avoiding AI Slop

Structural pattern rules beat word blacklists: vocabulary decays once
publicized ("delve" usage *dropped* after early-2024 mockery — Kobak,
arXiv 2406.07016), but sentence shapes persist across model generations.
This skill enforces 76 pattern rules + a tiered lexicon in three modes.

## Quick-Start Decision Tree

```
What's the task?
  ├─ WRITING new prose ──────────── Mode A: apply the constraint digest below, silently
  ├─ REVIEWING/de-slopping a draft ─ Mode B: lint it, then rewrite every hit
  ├─ CI / pre-publish gate ───────── Mode B: scripts/slopcheck.py --scan, exit-code wired
  ├─ IMAGE prompt or image review ── Mode C: references/image-slop.md pack + checklist
  └─ Thresholds feel wrong ───────── Calibrate: --calibrate on 10 known-good docs
```

## Usage Examples

**Example 1 — "De-slop this LinkedIn draft."**
→ Run `python3 scripts/slopcheck.py --scan draft.md`. Rewrite every BAN hit
using the `fix:` guidance per rule; adjudicate FLAG hits in context; deliver
the rewrite, not a description of it.

**Example 2 — "Write a blog post about our n8n migration."**
→ No slop-review was requested; Mode A applies silently. Draft under the
constraint digest. Before delivering, self-scan mentally against the eight
pattern families — no negative parallelism, no tailing significance clauses,
no editorial framing.

**Example 3 — "Does this read like AI wrote it?"**
→ Scan, report the specific rule IDs that fired with line numbers, and say
what the hits are — evidence, not vibes. Never extend this to an authorship
claim about a third party; the corpus detects style, not provenance.

---

## Mode A — Generation-time constraints (the digest)

Apply when writing any outward-facing prose. This digest is the injection
payload; do NOT paste the full lexicon into a generation context — long
ban-lists trigger ironic-rebound usage and burn context. Patterns generalize.

**Contrast templates — never:**
- "It's not X, it's Y" / "not just X, but Y" reframes (CT-01/02)
- "The result? ..." fake Q&A cadence; "Here's the thing" pivots (CT-04/05)
- Rule-of-three triplet lists as default rhythm; em-dash saturation (CT-06/07)

**Tailing clauses — never:**
- ", highlighting/underscoring/showcasing/reflecting..." significance tails (TL-01)
- "stands as a testament to", "plays a crucial role in", "cemented its
  status", "lasting impact", "marks a significant shift" (TL-03..09)
- End the sentence at the fact. Prove significance in its own sentence or cut.

**Editorializing — never:**
- "It's important/worth noting", "In today's fast-paced world", "Whether
  you're a X or a Y", "Let's dive in", "In conclusion" scaffolds (ED-01..07)

**Hedging — never:**
- "Experts argue" / "widely regarded as" without a named, cited source (HG-01/02)
- "a plethora/myriad of", "has the potential to", stacked modals (HG-04/06/07)

**Promo puffery — never:**
- "nestled in the heart of", "rich tapestry", "game-changer", "unlock/
  unleash/harness the power of", "navigate the complexities", "evolving
  landscape", "embark on a journey", "foster a culture of" (PR-01..12)

**Structure:**
- No emoji as bullets/headers. No bold-leadin bullet scaffolds as default.
  No "Introduction/Conclusion/FAQ" headers on short pieces. Vary paragraph
  and sentence length — kill the 2–3-sentence metronome (ST-01..10).

**Artifacts — never ship:**
- "As an AI model", knowledge-cutoff disclaimers, "I hope this helps",
  "[insert X]" placeholders, oaicite/[cite: N]/turn0search debris (AR-01..07)

**Fiction:**
- No chills down spines, breaths they didn't know they were holding, eyes
  widening in surprise, voices barely above whispers, air thick with
  anything, "couldn't help but", "little did they know" (FX-01..12)

**Top-40 word bans (Tier 1, all inflections):** delve, tapestry,
multifaceted, synergy, holistic, embark, unwavering, unparalleled,
meticulous, intricacies, pivotal, garner, glean, bolster, spearhead,
showcase, supercharge, unleash, revolutionize, transformative,
groundbreaking, breathtaking, captivating, mesmerizing, bustling, indelible,
ever-evolving, fast-paced, beacon, cornerstone, culmination, epitome,
quintessential, veritable, undoubtedly, invaluable, paramount, utilize,
whilst, game-changer. Full 117-term list + replacements:
`references/lexicon.yaml`.

**Register calibration:** tiers assume technical/MSP-consulting writing.
`robust`, `significant`, `end-to-end`, `turnkey`, `roadmap`, `framework` are
Tier 2/3 (context/density), never banned — they're working vocabulary in
engineering, stats, and MSP delivery.

## Mode B — Lint-time

```bash
python3 scripts/slopcheck.py --self-test          # corpus integrity (run after any edit)
python3 scripts/slopcheck.py --scan draft.md      # BAN=error, FLAG=warn, DENSITY vs thresholds
python3 scripts/slopcheck.py --scan draft.md --overrides overrides.yaml --allow allow.yaml
```

Exit codes: 0 clean · 1 findings · 2 config error. DENSITY tiers are skipped
under 150 words (per-1000 rates are noise on small samples). Matching is
inflection-aware (delve→delving, tapestry→tapestries, game-changer→game
changers); -ness/-ation variants are out of scope by design.

**Calibration workflow (do once before trusting DENSITY tiers):**

```bash
python3 scripts/slopcheck.py --calibrate good1.md good2.md ... > overrides.yaml
```

Feed ~10 documents you consider clean; any threshold they breach gets a
suggested replacement (observed max × 1.25). Shipped thresholds are
reasoned defaults, not measurements — calibrate before wiring into CI.

**Allowlist:** per-project exemptions in `allow.yaml`:

```yaml
allow: [ST-05, "framework", "key takeaways"]   # rule ids and/or terms
```

## Mode C — Image prompts and review

`references/image-slop.md`: six negative-prompt groups (skin, lighting,
grade, composition, tech-cliché motifs, prompt-boilerplate bans) — pick
groups per job, don't stuff all of them. Then the 12-point review checklist;
any "no" = regenerate. Icon layer belongs to `purging-icon-slop`; brand
tokens to the Abstrekkt/design-brief gates. No duplication here.

---

## Reference Map (progressive disclosure)

| Need | Open |
|---|---|
| A specific rule's regex, examples, fix | `references/patterns.yaml` (76 rules, 8 categories, BAN/FLAG/DENSITY) |
| Full ban list, context notes, ~95 replacements | `references/lexicon.yaml` (117 ban / 70 flag / 50 density) |
| Image negatives + audit checklist | `references/image-slop.md` |
| Lint, calibrate, allowlist mechanics | `scripts/slopcheck.py --help` |
| Trigger evals | `evals/evals.md` |
| What changed 2.0→5.0 | `CHANGELOG.md` |

## Refresh Protocol (quarterly)

1. `--self-test` must pass before and after any corpus edit.
2. Re-scan 3 recent frontier-model outputs; add new tells as rules (patterns
   preferred) or terms (exactly one tier each).
3. Retire vocabulary that has stopped appearing — decay is expected; note
   retirements in CHANGELOG.
4. Re-run `--calibrate` if your own writing register shifted.
5. Bump versions independently: SKILL.md, patterns.yaml `meta.version`,
   lexicon.yaml `meta.version`, slopcheck `__version__` — components version
   separately, no forced sync.

## Self-Verification (before delivering de-slopped or new prose)

1. Scan ran (or digest applied) — zero unadjudicated BAN hits
2. FLAG hits reviewed in context, not blanket-rewritten
3. Paragraph rhythm varies (ST-10 — the one check regex can't do)
4. No artifact-tier leakage (openers, closers, placeholders, citation debris)
5. Rewrites carry the content forward — de-slopping never deletes facts
6. Images: checklist run, any "no" regenerated

## CLAIMS
- Pattern rules outlive word lists; the delve-decay evidence is the load-bearing argument (Kobak, arXiv 2406.07016)
- Density thresholds shipped here are [GENERATED] defaults — uncalibrated until run against the user's own clean corpus
- Style detection is not authorship detection; this skill never supports "prove X used AI" claims

## COUNTEREXAMPLE
- Aggressive pattern-banning can produce stilted avoidance-voice — a different, detectable slop; Mode A's restraint (digest, not full lexicon) is the mitigation
- A human who genuinely writes "testament to" gets flagged; FLAG-tier adjudication exists precisely because the corpus has false positives

## CONTRADICTIONS
- "Ban these words" vs "don't paste ban-lists into prompts" (ironic rebound) — resolved by splitting generation-time digest from lint-time full corpus, but the tension is real
- Register calibration says `significant` is fine in stats while Tier-3 caps it — a stats-heavy doc will warn on legitimate usage until calibrated
