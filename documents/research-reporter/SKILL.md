---
name: research-reporter
version: 1.2.3
author: Personify Labs
description: >
  Turns a feedback-synthesizer output into a stakeholder-ready report —
  exec summary, methodology, benchmark comparison, and prioritized
  recommendations — formatted for the audience reading it (markdown or
  Notion for internal readers, Word for formal/external stakeholders).
  Trigger when someone has synthesis output ready and wants it turned into
  something shareable, says "write this up," "make me a report," or "turn
  these findings into something I can send to leadership." Entry point 3 of
  the research loop (see research-loop).
tags:
  - user-research
  - ux-research
  - reporting
  - stakeholder-communication
license: CC-BY 4.0
---

# Research Reporter

Turns a synthesis file into something a stakeholder actually reads and
acts on. Does not re-analyze anything — feedback-synthesizer already did
the scoring, testing, and theming. This skill's job is presentation and
prioritization for a specific audience, not new analysis.

-----

## Step 0: Who's reading this?

Ask (or infer from context if it's obvious) before drafting:

1. **Audience:** internal team/PM (fast, working doc) vs. leadership or
   external stakeholder (formal, polished). Run
   `scripts/report_checks.py`'s `select_format(audience)` once you know
   which — `"internal"`, `"leadership"`, or `"external"` — rather than
   picking the format by feel.
2. **Format:** confirmed by the lookup above, or ask if the audience
   itself is genuinely unclear
3. **What decision is this report supporting?** Pull this from the
   original learning goal in `00-intake.md` if it exists — the report
   should visibly answer that question, not just summarize everything
   that was measured

If there's no synthesis file to point to and someone asks for a report
from scratch, stop and say synthesis needs to happen first — don't
fabricate scores or themes to fill a report shape.

-----

## Step 1: Structure

Every report gets these sections, scaled by audience (internal = terse,
formal = fuller prose):

### Executive summary
2–4 sentences. Leads with the answer to the stated learning goal, not a
recap of the method. State the headline score with its CI in plain
language ("SUS came in at 74, meaningfully above our 68 benchmark — not
just noise, the confidence interval doesn't overlap").

Keep three things distinct and never let one stand in for another:
**statistical significance** (did synthesizer's test actually return
significant?), **practical significance** (does the size of the
difference matter for the decision this study was run for — a
statistically significant 2-point movement on a huge sample may not be
worth acting on; say so when it applies), and **evidence confidence**
(how much to trust the conclusion overall, carried forward from
synthesis — see Step 3). A narrow CI is not evidence of high confidence;
a significant result is not automatically an important one.

### Methodology
Instrument used, n, collection window, and the low-confidence flag if
feedback-synthesizer raised one — carry that flag forward, never drop it
during formatting. Keep this section short for internal docs, fuller for
formal ones (formal audiences need to trust the number before acting on
it).

### Benchmark comparison
Pull the product's history from `/research/_benchmarks/<product>.md` and
show the trend, not just this wave's number in isolation — but only once
research-loop's `check_benchmark_comparability` (or feedback-synthesizer,
if it already ran this check) confirms the waves being compared actually
measured the same thing. When it reports a mismatch, present the waves
side by side with the mismatched fields named, instead of a trend line
that implies more comparability than the measurement conditions support.
A single score with no trend line is a weak report; a trend line built
on an apples-to-oranges comparison is a misleading one.

### Findings
Present the synthesis's qual-quant cross-references as-is — don't
soften a stated "no clear theme explains this" into a manufactured
narrative. If synthesis said a movement was unexplained, report it as
unexplained.

### Prioritized recommendations
Derived directly from feedback-synthesizer's severity tiers (Critical /
Notable / Minor) — this skill doesn't re-rank them, it translates tiers
into recommended actions and rough effort/impact framing for the
stakeholder. Critical tier findings go first, always.

-----

## Step 2: Audience-specific formatting

**Internal / markdown / Notion:**
- Terse, scannable, bullet-heavy
- Assume the reader already has product context — skip background
  explanation of what the product is
- Fine to reference raw synthesis file for anyone who wants to dig in

**Formal / docx:**
- Fuller prose, more framing/context for readers without daily product
  exposure
- Route section copy (headers, section framing, any narrative
  transitions) through **thought-leadership-writer** if the doc is going
  to leadership or an external audience and needs a stronger narrative
  voice; route any UI-facing copy referenced in findings through
  **righter** for consistency with product copy standards
- Use the docx skill for actual file generation and formatting

-----

## Step 3: What never changes between formats

Regardless of audience, these must survive unchanged from the synthesis
file:

- The headline score and its confidence interval
- Whether a difference was statistically significant
- The low-confidence flag, if one was raised
- Severity tier assignments, **including a stated override reason** when
  `override_reason` is set — never present just the final "Critical"
  label as if the frequency math alone produced it
- Evidence confidence (the categorical rating, not a re-derived number)
- Each finding's claim-strength level — never let "correlated" read as
  "caused" in the prose, even when the report's tone is more confident
  than the synthesis's
- Any "no clear theme found" / "cannot determine" statements

Reformatting for readability is fine. Softening a caveat, dropping a CI
because it "clutters" the exec summary, upgrading "directional" to
"confirmed," or upgrading a claim-strength level, is not.

**Before finalizing, run these checks from `scripts/report_checks.py`:**
`validate_report_structure(report_text)` to confirm all five required
sections are present; `check_preserved_values(synthesis, report_text)`
to confirm the CI, low-confidence flag, severity tiers, evidence
confidence, and claim-strength labels survived into the text unchanged;
`check_no_unsupported_causal_language(synthesis, report_text)` to catch
causal-sounding verbs ("caused," "led to," "drove") appearing without a
theme that actually carries `claim_strength="causal"`. All three are
structural/textual checks — they catch a dropped number, a missing
section, or an unsupported causal verb, but **they cannot catch a report
that keeps every number yet quietly reframes "directional" as
"confirmed" in prose, or "correlated" as "clearly caused by" without
using the word "caused."** That specific failure mode needs an actual
read-through; don't treat a clean script pass as proof the report is
honest, only as proof it isn't missing pieces or an obviously upgraded
verb.

Write `/research/<study-name>/03-report.json` alongside the `.md`/
`.docx` — run `validate_report_json(report)` first and fill in anything
it reports missing. The `.json` is canonical, same convention as every
other artifact in this system.

-----

## Rules

Priority when rules interact: **STOP** > **MUST NOT** > **MUST** >
**SHOULD** > **MAY** — see `ux-research/README.md` for the full
precedence explanation.

- **STOP** if there's no synthesis file to point to and someone asks for
  a report from scratch — say synthesis needs to happen first, don't
  fabricate scores or themes to fill a report shape.
- **MUST NOT** re-score, re-test, or re-theme anything — that's
  synthesizer's job.
- **MUST NOT** drop a confidence interval, low-confidence flag, evidence
  confidence rating, or claim-strength label to make the report cleaner.
- **MUST NOT** upgrade a claim-strength level in prose (e.g. "correlated"
  read as "caused") — `check_no_unsupported_causal_language` is the
  enforcement point; don't work around it by rewording instead of fixing
  the substance.
- **MUST NOT** re-order severity tiers based on its own judgment, or
  present an overridden tier without its override reason.
- **MUST NOT** present a benchmark trend when the waves aren't
  comparable — present them side by side instead.
- **MUST NOT** write UI or public-facing copy without routing through
  righter or thought-leadership-writer as appropriate.
- **MUST NOT** manufacture a narrative explanation for a score movement
  synthesis explicitly said was unexplained.
- **MUST** present a benchmark trend, not just this wave's score in
  isolation, when comparable prior waves exist.

-----

## Quick reference

| Audience | Format | Tone |
|---|---|---|
| Internal team / PM | Markdown / Notion | Terse, bullet-heavy, assumes context |
| Leadership / external | Word doc (docx) | Fuller prose, more framing |
| Report going external/public | Docx + thought-leadership-writer pass | Narrative voice |
| Findings reference UI copy | Route through righter | Copy standard consistency |
| No synthesis file exists | Stop, redirect to feedback-synthesizer | — |

## Maintaining this skill

`evals/` is the regression suite. After touching
`scripts/report_checks.py`, run `python3 -m unittest discover -s evals -v`
(CI runs the same). After touching this file's prose, re-check the cases
in `evals/qualitative_cases.md` by hand.
