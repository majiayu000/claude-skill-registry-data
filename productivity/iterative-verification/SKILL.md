---
name: iterative-verification
description: >-
  "Is this ACTUALLY verified, or did I just say it is?" - Factual accuracy
  verification loop. Use when (1) claims require
  evidence not assumption, (2) verification must be demonstrable, (3)
  single-pass investigation insufficient, (4) factual accuracy is critical.
  Provides the loop logic: iterate until verification thresholds met. Does NOT
  trigger for: opinions, preferences, how-to instructions, or when user
  explicitly wants quick answer.
---

# Iterative Verification

**Seed question:** *Is this ACTUALLY verified, or did I just say it is?*

> *Relentless self-reflexive dialectical thinking that questions its own premises.*

## Core Principle

An iterative workflow keeps going until genuinely complete.
For facts: keep verifying until claims meet evidence thresholds.

**The anti-pattern this counters:**
```
❌ "I searched once, found something, called it verified"
❌ "The claim sounds right, I'll present it as fact"
❌ "I'm confident, so I don't need to check"
```

**The pattern this enforces:**
```
✅ Search → Label evidence tier → Check threshold → Iterate if gaps
✅ Claim is VERIFIED only when evidence supports it
✅ Keep iterating until criteria actually pass
```

## When This Applies

**TRIGGER:**
- Any claim that must be factually accurate
- Investigation outputs with evidence requirements
- Trust/reliability assessments
- Decisions based on facts, not preferences
- User asks "is this actually true?" or "can you verify?"

**DO NOT TRIGGER:**
- Opinion requests
- Preference questions
- How-to instructions
- User says "quick answer" or "don't need sources"
- Creative/generative tasks

## The Verification Loop

```
1. INVESTIGATE
   - Gather information
   - Make claims

2. LABEL
   - Assign evidence tier to each claim:
     * VERIFIED: Primary sources, court docs, regulatory filings
     * CREDIBLE: 3+ independent sources agree
     * ALLEGED: 1-2 independent sources; write the count (ALLEGED ×1, ALLEGED ×2)
     * SPECULATIVE: Inference, theoretical
   - Add [RELAY] to any claim taken from a summary, not the primary source

3. CHECK THRESHOLDS
   - ≥80% claims labeled?
   - ≥2 independent sources?
   - Flow traced ≥3 steps?
   - Evidence fresh (<2 years for reliability data)?

4. IF GAPS → ITERATE
   - Identify what's missing
   - Search for specific evidence
   - Return to step 1

5. IF ALL PASS → COMPLETE
   - Output with confidence
   - All claims have evidence basis
```

## Evidence Tier Definitions

| Tier | Definition | Examples |
|------|------------|----------|
| **VERIFIED** | Primary sources directly confirm | Regulatory filings, court documents, lab test results, official statements |
| **CREDIBLE** | 3+ independent sources agree | 3+ news outlets, consistent professional reports, corroborated accounts |
| **ALLEGED** | 1-2 independent sources, short of CREDIBLE | One article, one whistleblower, one study; two independent lab reports (ALLEGED ×2) |
| **SPECULATIVE** | Inference from patterns | "If X then probably Y", theoretical risk |

The count beside ALLEGED keeps one corroboration visible instead of reading
like a lone claim. It counts independent origins, not outlets: two papers
carrying one leak are ×1 (manufactured-consensus-detection). What a count
cannot see - shared stake, shared method, a contradicting primary - is open in
issue #244.

### The [RELAY] Rule

A claim that entered this investigation through an agent's summary, a quoted
digest, or any intermediary's compression — rather than through the primary
source itself — carries the tag `[RELAY]` next to its evidence tier until
someone in this investigation has read the primary source directly.

- `[RELAY]` stacks with any tier: `CREDIBLE [RELAY]` means "would be CREDIBLE
  if the relay is faithful — unverified that it is."
- A **load-bearing** claim (one a verdict, ranking, or recommendation depends
  on) MAY NOT remain `[RELAY]` in a final output. Verify it against the
  primary source, or demote it to a satellite claim.
- Removing the tag requires naming what was checked: "[RELAY] cleared — read
  the filing itself; the summary had dropped the qualifier 'alleged'."

Why this exists: an intermediary's summary is a *positioned compression* — it
keeps what its author found salient and silently drops the rest. The evidence
tier describes the SOURCE's quality; `[RELAY]` describes YOUR distance from
it. The two are independent, which is why the tag stacks instead of replacing. (Principle P1 (relayed-is-not-read).)

### Definition-Drift Check (a count is only stake-free while its definition holds still)

A reporter has no discretion over how many events happened and full discretion
over *what counts as one*. When the definition moves mid-series, every later
number is an honest count of a different thing; the series looks continuous and
the trend across the change is an artefact. Four moves: **threshold** (what is
big enough to enter), **perimeter** (which entities, channels, regions), **unit
or inclusion rule** (gross/net, messages/value, intra-group in or out), **base**
(growth against a revised prior year). Sibling: **coverage drift** — the
definition stands while the population it captures moves (a share of traffic on
one network changes meaning as flows leave the network).

Signals, strongest first: a level jump with no note; a growth rate you cannot
reproduce from the published levels; a series renamed, split or restarted.
Disclosure words — "restated", "like-for-like", "new methodology", "constant
perimeter", a series-break flag in the publisher's legend, Chinese 口径 (可比口径
"comparable basis", 全口径 "full basis") — mark only the *disclosed* case; their
absence is not stability. Search for the equivalents in the reporter's own language.

For any count, or any trend, share or ranking built from counts, that a
deliverable rests on:
1. Pull the method notes for the first and last edition in your window, and any edition where the level jumps.
2. Compare threshold, perimeter, unit and base; name who controls the definition and when it changed.
3. If it moved: each same-definition segment keeps its tier; the trend across the break is ALLEGED if the reporter states it, SPECULATIVE if you computed it, until a same-definition back-series exists from someone other than the reporter — a reporter's own back-cast is its own record and cannot clear its own break; name whose series clears it.
4. No method notes found: list "definition unverified" in the report's limits and demote the claim to satellite; the loop does not stay open for it.

Runs on every reporter, symmetrically (Principle P4 (counter-default)). Table,
full procedure and where the tells appeared: `references/definition-drift.md`.
(User-raised 2026-09-25; not yet run on a series.)

**Ratios: state both periods before computing** (one observation, 2026-09-16).
Write the period of the numerator and of the denominator explicitly. One year
of NDB disbursements ($2.7bn) over cumulative approvals ($43bn) read as failure
to deliver; the within-year ratio was 86%. Both figures were correct and
sourced; the defect lived only in the pairing, and a figure-level fact-check
passes it clean — it only shows at the ratio.

## Threshold Requirements

For factual accuracy tasks, iterate until:

| Metric | Threshold | Rationale |
|--------|-----------|-----------|
| Claims labeled | ≥80% | Most claims should have explicit evidence basis |
| Independent sources | ≥2 | Reduces single-point-of-failure. A stop rule for the search, not a grade: a claim can meet it and still be ALLEGED ×2 |
| Evidence freshness | <2 years | Prevents stale information in dynamic domains |
| Flow depth | ≥3 steps | Surface claims hide deeper realities |

## Iteration Examples

**Pass 1: Initial Investigation**
```
Claim: "Company X has good privacy practices"
Evidence tier: ALLEGED (marketing claims only)
Gap: No independent verification
→ ITERATE
```

**Pass 2: Targeted Search**
```
Search: "Company X privacy audit independent"
Found: Third-party security audit report
Claim: ALLEGED ×1 (the audit is the one independent source; marketing is the
  subject's own claim, not an independent source; CREDIBLE needs 3+)
Remaining gaps: Ownership chain unclear
→ ITERATE
```

**Pass 3: Ownership Verification**
```
Search: "Company X beneficial ownership SEC filings"
Found: SEC filing showing parent company
Claim: Ownership chain now VERIFIED
All thresholds pass
→ COMPLETE
```

## Fact-Verification Examples

### China: TikTok Algorithm Ownership Error (March 2026)

A report claimed the consortium "controls the algorithm" after TikTok's sale. Iterative verification revealed the opposite.

> **Report claimed:** "The consortium controls the algorithm, meaning it's no longer under ByteDance/Chinese government potential influence."
> **Verified against primary sources:** "This is factually wrong. ByteDance retains ownership of the recommendation algorithm. The US entity operates it under license but cannot own, independently transfer, or unilaterally modify the core IP." — Adversarial Critique, China tech/trade assessment
>
> **Verification gap:** Single-pass investigation accepted the "clean break" narrative. Iterative verification against NBC News, TechPolicy.Press, and Rest of World revealed the deal was "in direct tension with the explicit text of the divestment law." *Source: china-critique.md, ERROR 3*

### Iran: Beit Shemesh Casualty Count (March 2026)

A report stating "8 killed" in a missile strike was corrected through cross-source verification.

> **Report stated:** "8 killed" in Beit Shemesh strike.
> **Actual:** "9 killed (including three teenage siblings: Yaakov 16, Avigail 15, Sarah 13 Bitton). Multiple sources confirm: Al Jazeera, Jerusalem Post, Times of Israel, Euronews." — Adversarial Critique, Iran assessment
>
> **Lesson:** In a report claiming VERIFIED evidence tiers, even minor numerical errors undermine the tier system. Cross-referencing against 4 independent sources caught the discrepancy. *Source: iran-critique.md, Challenge 6*

### Iran: Russia's Role Understated (March 2026)

A report characterized Russia/China support as "muted criticism only," which iterative verification contradicted.

> **Report claimed:** Russia showed "limited actual support to Iran" with "muted criticism only."
> **Counter-evidence found:** "Russia IS providing satellite intelligence on US troop positions (CNN, March 6, confirmed by US officials). Russia delivered Su-35 fighter jets ($6.5B order) and $590M in air defense systems before the war." — Adversarial Critique, Iran assessment
>
> **Result:** Evidence tier downgraded from CREDIBLE to ALLEGED/INCOMPLETE. A single pass accepted the "muted" characterization; the verification loop surfaced active intelligence sharing and substantial pre-war arms deliveries. *Source: iran-critique.md, Challenge 4*

## Convergence Warning Protocol

When all sources agree quickly, this is a signal, not a conclusion. Flag it explicitly:

```
WARNING: All sources converge on [X]. This may be correct, but rapid
convergence can indicate:
  (a) genuine consensus,
  (b) groupthink,
  (c) manufactured consensus (same original source),
  (d) our own confirmation bias.
Testing with adversarial search.
```

After flagging, actively search for dissent. If dissent exists: investigate it. If no dissent exists after adversarial search: convergence is likely genuine, but note the flag in your output.

## Probability Distribution Requirement

Never present a single scenario as the outcome. Present a probability distribution:

```
Scenario A (50%): [Most likely outcome] because [evidence]
Scenario B (30%): [Second most likely] because [evidence]
Scenario C (15%): [Contrarian case] because [evidence]
Scenario D (5%):  [Tail risk] because [structural possibility]
```

The contrarian case MUST receive non-zero allocation unless genuinely impossible. Binary framing (X will/won't happen) almost always collapses a spectrum into a false dichotomy.

For actionable investigations: never recommend 100% allocation to any single scenario. A 50/30/20 split is almost always better than 100/0/0.

## Steel-Man Obligation

After reaching any conclusion in the verification loop, steel-man the strongest possible contrarian argument:

- If the investigation leans toward crisis: What is the strongest case for quick resolution? Quantify it.
- If the investigation leans toward stability: What is the strongest case for escalation? Quantify it.
- If the investigation identifies a villain: What is the most charitable interpretation of their actions?

This is not about fairness — it is about testing whether the conclusion survives its best counter-argument. If you cannot articulate the contrarian case with genuine force, your verification is incomplete.

### Verdict-Tier Check

Completion requires: verdict tier matches evidence tier. "No mainstream confirmation" = UNVERIFIED, not FALSE. Escalate to DISCONFIRMED only with specific counter-evidence.

## Self-Check Questions

Before claiming completion, ask:

1. **"Did I label this claim, or did I assume it?"**
   - Every factual claim needs an evidence tier

2. **"Is my source independent?"**
   - Affiliate content, marketing, and SEO-gamed reviews don't count

3. **"When was this verified?"**
   - Old evidence may not reflect current reality

4. **"Did I search for counter-evidence?"**
   - Confirmation bias finds what you expect; search adversarially

5. **"Would this pass falsification criteria?"**
   - Check against `FALSIFICATION-CRITERIA.md` if available

6. **"Did I steel-man the contrarian case?"**
   - The strongest counter-argument must be articulated and tested

7. **"Am I presenting a distribution or a single scenario?"**
   - Binary conclusions are almost always wrong; present probabilities

8. **"Is this skill's framework limiting what I can verify?"**
   - These evidence tiers, thresholds, and protocols are tools, not truths — if they're channeling you away from something real, override them and say why

9. **"I verified it — did I re-read it?"**
   - A sourcing checkmark suppresses semantic re-reading: once a line is
     verified, attention releases it. After verification, run the value
     question as its own separate step — what does this line MEAN for the
     question asked, as distinct from whether it is accurately quoted? (Principle P2 (verified-is-not-understood).)

10. **"Did an external correction just land?"**
    - If yes: treat the whole salience map as suspect, not just the corrected
      point. Regenerate the ranking/summary from scratch with the correction
      in hand. A correction is evidence about the process that produced the
      output, not only about the point it names — patching locally preserves
      the tilt that made the error. (Principle P3 (inherited-salience-is-not-importance) — the map, not the point, is suspect.)

11. **"Did I discount — or credit — any source by its label instead of a named defect?"**
    - A dismissal is a claim too: it needs the specific factual defect (which
      claim, what is wrong, on what evidence). "Biased / fringe / propaganda"
      with nothing named is the frame talking — and it fires before reading;
      a source that was never opened has a void dismissal. Same requirement,
      symmetric, for crediting by halo. (Kin: the Verdict-Tier Check — "no
      mainstream confirmation" = UNVERIFIED, not FALSE. Full counter:
      engage-the-disfavored.)

12. **"Did the method change since the earliest conclusions?"**
    - If yes: re-run the matured checks against those early conclusions
      before claiming completion (Principle P8 (the-method-matures-backward)). Early conclusions passed a
      weaker gate than late ones — that gradient is invisible unless
      checked.

13. **"Did I apply the stake rule to only one side?"**
    - When a stake demotes one source's own figures (a central bank's
      settlement share), run the same rule over every other source in the same
      deliverable before shipping — a messaging network's own traffic share is
      the same kind of figure. Demoting one camp's records and passing the
      other's as plain data is the frame talking (Principle P4 (counter-default);
      source-dossier symmetry gate). Caught by the user, 2026-09-25.

14. **"Did the definition move under any count, trend, share or ranking I rely on?"**
    - A count is only stake-free while what-gets-counted holds still; run the
      Definition-Drift Check on any series a verdict rests on.

## The "One More" Sweep Rule

After believing verification is complete and all thresholds pass, do ONE MORE sweep:

1. Pick the perspective you are **least sympathetic to**
2. Search that perspective's sources for your topic
3. If this changes nothing: you are genuinely done
4. If this changes something: you are not done — return to the verification loop

This catches the blind spot that all previous passes share: your own position. The perspective you instinctively dismiss is the one most likely to contain what you missed.

## Dialectic Spiral for Contested Claims

When claims are contested (sources disagree, evidence tiers conflict), apply the dialectic spiral within the verification loop:

```
Round 1: THESIS — Present the claim with evidence tier
Round 2: ANTITHESIS — Search for counter-evidence.
         The original claim must REBUT with evidence, not assertion.
Round 3: RESOLUTION — What survives the test? Note what was abandoned.
Round 4+: GENERATE the exact opposite of the resolution.
         Don't look for an existing counterpoint — produce one.
         Then search: does anyone anywhere articulate it?
         Does reality support it?
         Continue until generating the opposite yields nothing meaningful.
```

**The key move is generative, not classificatory.** Pre-mapped "opposing views" limit the dialectic to existing positions. Generating the opposite of a synthesis can produce positions that don't exist in any source category — that's where novel insight comes from. "Who bears costs / who captures benefits" is one useful lens for generation, not the only one.

Exit when generating the next antithesis produces nothing that changes the synthesis. Minimum 4 rounds for contested claims.

Reference: `METHODOLOGY-comprehensive-investigation.md` Section 6 for extended protocol with agent team structure.

## Integration with Ralph-Wiggum

This skill provides the verification loop logic that ralph-loop enforces through persistence.

**Without ralph-loop:** User invokes this skill, follows methodology manually
**With ralph-loop:** Agent runs in loop until completion promise satisfied

Both achieve the same goal: iterate until genuinely verified.

## Output Pattern

```markdown
## Verification Status

### Claims Assessed
1. [Claim] - [TIER] [RELAY if unverified relay] - [Source]
2. [Claim] - [TIER] - [Source]
...

### Threshold Check
- Evidence labeling: [X]% (threshold: 80%) [✅/❌]
- Independent sources: [X] (threshold: 2) [✅/❌]
- Evidence freshness: [status] [✅/❌]
- [Other criteria...]

### Verification Status
[COMPLETE: All thresholds met] or [INCOMPLETE: Gaps identified]

### If Incomplete: Next Iteration
- Gap: [what's missing]
- Search: [what to look for]
```

---

## Vasana

A vasana is a pattern that persists across unrelated contexts. If during
this task you notice such a pattern emerging, it may be worth capturing.
This skill works best alongside the `vasana` skill and `vasana` hook
from the Vasana System plugin.

Modify freely. Keep this section intact.

**Integration:** Use the `/ralph-loop` command from the ralph-loop plugin for automated iteration.
