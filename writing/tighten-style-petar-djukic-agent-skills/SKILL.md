---
name: tighten-style
description: >-
  Tighten prose against a rule catalog: cut needless words, restore buried
  verbs and the active voice, and give paragraphs a spine. Checks sentence-level
  rules (needless words, intensifiers, hedge stacks, negative form,
  nominalizations) and paragraph-level structure (topic sentence, one topic,
  consequent order), citing rule IDs. Tightens toward the author's measured
  density, never past it. Triggers: tighten, tighten style, omit needless words,
  wordy, too wordy, cut the fat, edit for concision, copyedit, style rules,
  paragraph structure, active voice.
argument-hint: 'Path to the markdown or LaTeX file to tighten'
---

# tighten-style

Cuts what does not earn its place and gives paragraphs a spine, against the
catalog in [references/style-rules.md](./references/style-rules.md). Every
finding cites a rule ID, so the report reads as a copyedit keyed to a document
you can argue with rather than a list of opinions.

The rules are ours. They cover the ground Strunk covered and the ground he
could not — he wrote before markdown and before a machine could produce fluent
prose with nothing behind it.

## The floor

**Tightening stops at the target register's own density.** Shorter is not the
target. Cutting past the measured function-word ratio manufactures the
clipped, aphoristic register that reads as machine-written — the failure
`filter-tells` calls overshoot. Where a `writing-voice/` corpus exists,
`match-structure` supplies that floor; without one, stop at each rule's stated
threshold.

**The floor is venue-keyed (GH-338).** By default it is the author's own
density. With `--venue <name>`, the venue profile
(`writing-voice/venues/<name>.yaml`, see the writing-voice rule) supplies it
instead: the profile's `targets` (`sentence_length_mean`/`stdev`) become the
sentence floor — a whitepaper tightened to newsletter density reads clipped —
and its `hedge_policy` keys the TS-08 threshold: `zero` flags every hedge
(book voice, rule 10), `minimal` flags pairs, `calibrated` keeps single
calibrated hedges on empirical claims and only flags stacks. An explicit
`--sent-floor` still wins over the profile. No `--venue`, no change.

Never touch a direct quotation, a normative requirement, a citation, or a
number.

## Procedure

```bash
python3 <tighten-style>/scripts/check_style.py <file> [--json] [--hedge-policy zero|minimal|calibrated]
python3 <tighten-style>/scripts/tighten.py --article <file> [--venue <name>]   # the rewrite, via Ollama
python3 <tighten-style>/scripts/tighten.py --article <file> --check-only   # plan without model calls
python3 <tighten-style>/scripts/tighten.py --article <file> --jobs 1        # sequential; default 4 (TIGHTEN_STYLE_JOBS), same draft (GH-433)
# A verify-clean candidate that raises the paragraph's nominalizations or colons is not
# spliced (record field register_refused, GH-458): tightening must not bury verbs.
# The summary's `register:` line and the `.tighten.json` sidecar give nominalization
# counts beside the per-1,000 rate, and which paragraphs were refused (GH-466): cutting
# words raises the rate even when no nominalization is added, so quote both.
```

1. **Run the checker** for the findings and the reading pass for the judgment
   rules (TS-06, TS-07, TS-09, TS-11) it cannot see.
2. **Run the tightener for the rewriting.** It selects the instead→do pairs
   for the rules each paragraph fired, prompts the second model family with
   the pairs — never the rule prose — and gates every candidate with
   match-voice's verify step. Paragraphs that fail the gate keep their
   original text.
3. **Read the register markers it prints** (passive, agentive, nominalization,
   connectives, before → after). Rising markers on a shrinking draft mean the
   pass moved toward the assistant register, which is the failure this design
   exists to prevent.
4. **Do not tighten by hand-applying the rules with the drafting model.**
   The full evidence is in
   [references/hand-tightening-regression.md](./references/hand-tightening-regression.md).
   GH-222 measured what that does: a paper excerpt moved from distance 26.1 to
   6.5 from the AI-draft fingerprint under a faithful rules pass, overshooting
   the draft's own passive rate. The rules read as instructions by an
   instruction-tuned model ARE that model's register. The catalog stays for
   understanding and for the checker; the pairs are its delivery.

The stopping rules are unchanged: the author-density floor, and never touching
quotations, normative text, citations, or numbers — now enforced by the gate
rather than by discipline.

## Where the rules are enforced

| layer | rules | licence |
|---|---|---|
| deterministic | TS-14 | rewrite it |
| lexical | TS-01, TS-03, TS-05, TS-08, TS-15 | propose; context can excuse |
| per-sentence | TS-02 (agentive passive, or 2+ bare), TS-04 (3+ nominalizations) | propose; the rules' own exceptions apply |
| metric | TS-04 doc-level, TS-10, TS-12, TS-13, TS-16 | flag; a reader decides |
| judgment | TS-06, TS-07, TS-09, TS-11 | flag and explain; never auto-fix |

Metric rules delegate to `match-structure`, which already measures passive
density, nominalization density, list ratio, and the paragraph-schema signals
(topic overlap, cohesion, subject churn) that TS-10 is built on. Those signals
were first written to detect an AI tell; what they actually measure is whether
a paragraph has a spine, which is why they serve here too.

## Boundary with filter-tells

`filter-tells` removes what should not be there. `tighten-style` compresses
what remains and structures it. `match-voice` restores how it should sound.
Run tighten-style *before* match-voice — tightening changes sentence shapes,
and there is no point matching voice on prose about to be rewritten.

**The parallelism collision, explicitly:** `filter-tells` flags parallel
*cadence* as an AI tell; TS-12 requires parallel *form* for coordinate
content. If both fire on one passage, ask whether the ideas are genuinely
coordinate. If they are, keep the form and dismiss the tell. If they are not,
the cadence is the problem and TS-12 does not apply.

## What the checker will not tell you

It reads lists, densities, and now the per-sentence passive and
nominalization shapes (GH-223 — a paragraph of textbook passives once returned
zero findings while the description promised "restore the active voice"). It
still cannot tell whether a paragraph earns its
place in the argument, whether the concrete detail is the *right* detail, or
whether a hedge is honest calibration or evasion. On prose that is already
lexically clean — which the author's own tends to be — nearly all the
remaining work is the reading pass, and the script's silence is not a verdict.

## Dependencies

`match-structure` for the metric rules and the density floor, `match-voice`'s
verify step for the gate, and the shared paragraph extractor. The checker
itself is stdlib.
