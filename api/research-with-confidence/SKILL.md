---
name: research-with-confidence
description: |
  Investigates a question systematically before answering — verifying claims through sources, distinguishing known facts from inferences, and calibrating expressed confidence to actual certainty. Use when asked to research a topic, verify a claim, evaluate a technology, or answer a question where accuracy matters more than speed.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-research-with-confidence
    version: "1.0.0"
    created: 2026-04-08T00:00:00Z
    category: product
    layer: 2
    commands:
      - name: pk-research
        args: "research question or topic"
        description: "Research a topic with explicit confidence labelling on all claims."
---

# Research with Confidence

## Intro

The default failure mode for AI agents is overconfidence: stating a
plausible-sounding answer without checking it. This skill enforces
a discipline: gather before claiming, distinguish facts from
inferences, and express uncertainty honestly. The goal is not
hesitancy — it is calibration. Confident where warranted; explicit
about gaps where not.

## Overview

### The research protocol

Apply this sequence before answering any factual question:

1. **Clarify the question** — What exactly is being asked? What
   does "right answer" look like? What would make the answer useful
   versus technically correct but not helpful?

2. **Inventory what you already know** — Before searching, write
   down what you know and how confident you are. Mark uncertain
   items as hypothesis, not fact.

3. **Identify what you don't know** — List the gaps. Be specific:
   "I don't know the current version number" is better than "I need
   to check this."

4. **Gather from authoritative sources** — Prioritize: primary
   sources (official docs, original research, direct measurements)
   over secondary (articles, summaries, Stack Overflow). For each
   claim, note the source.

5. **Synthesize with uncertainty labels** — Present findings with
   explicit confidence levels (see below). State what is confirmed,
   what is inferred, and what remains unknown.

6. **Surface the residual uncertainty** — End with a clear statement
   of what you verified, what you couldn't verify, and what the
   user should validate themselves if the stakes are high.

### Confidence levels

Label claims explicitly when the stakes matter:

| Label | Meaning | Example |
|---|---|---|
| **Confirmed** | Verified against a primary source in this session | "Confirmed: Python 3.12 was released October 2, 2023 (python.org)" |
| **Likely** | Consistent with multiple secondary sources or strong inference from first principles | "Likely: this API is rate-limited to 100 req/min based on the docs" |
| **Possible** | One source, or plausible inference, not verified | "Possible: the library uses lazy evaluation here — I haven't confirmed in source" |
| **Unknown** | Not established — do not present as fact | "Unknown: whether this behavior applies to the v2 API endpoint" |

Never present a "Possible" or "Unknown" as "Confirmed". Resist the
urge to fill gaps with confident-sounding guesses.

### Distinguishing types of claims

Different claims need different verification approaches:

**Factual / current state** (library version, API behavior, pricing):
- Must be verified against primary sources
- Has a shelf life — note when the information was gathered
- Example: "As of April 2026, the latest stable release is..."

**Conceptual / structural** (how a system works, design patterns):
- Can be reasoned from first principles + verified against docs
- Less time-sensitive, more stable
- Example: "JWT tokens work by encoding a signed payload..."

**Comparative / evaluative** (A vs B, which is better):
- Requires defining the evaluation criteria explicitly
- Different answers for different contexts — state the context
- Example: "For read-heavy workloads under 1M requests/day, Postgres is typically preferred because..."

**Predictive** (what will happen, what will work):
- Highest uncertainty category — present as estimate with reasoning
- Example: "Based on current trajectory, I'd estimate..."

### Red flags to pause and verify

Stop and check before asserting when:

- The claim involves a specific version number, date, or price
- The claim is about a library or API that has changed recently
- The claim contradicts something the user has said
- The claim is in a domain where you know your training data may be outdated
- The claim sounds exactly right without any caveats — that's often when it's wrong

This skill also provides the `/pk-research` command for direct
invocation — see `commands/pk-research.md`.

### Structuring the output

```
## Findings: [Question]

**Summary:** [1-2 sentence answer at the right confidence level]

**Confirmed:**
- [Claim] (source: [where you verified])
- [Claim] (source: [where you verified])

**Likely / inferred:**
- [Claim] (reasoning: [why you think this])

**Unknown / not verified:**
- [Gap] — [what the user would need to check to fill it]

**Note:** This research was conducted on [date]. [X] may have changed
since then — verify against [source] if currency matters.
```

## Gotchas

Agent-specific failure modes — provider-neutral pause-and-self-check items:

- **Presenting inferences as confirmed facts.** The most common research failure: stating a plausible-sounding claim without checking it. Before finalizing any factual claim, ask: "Did I actually verify this in a source, or am I inferring it from general knowledge?" Label accordingly.
- **Citing sources without checking whether the source confirms the claim.** Attaching a URL to a claim is not verification — the URL must actually support the specific claim. A document that discusses a topic tangentially does not confirm a specific fact from it. Read the source; don't cite by proximity.
- **Not dating time-sensitive information.** API behavior, library versions, pricing, and company policies change. Any claim in these categories must be dated: "As of [month year]..." If you cannot establish when the information was current, say so.
- **Treating absence of contradicting information as confirmation.** Not finding evidence against a claim is not the same as finding evidence for it. If you searched and found nothing disconfirming, report it as "no contradicting evidence found" — not as "confirmed."
- **Skipping the residual uncertainty summary.** Research that ends with a conclusion without noting what was not verified gives the user false confidence. Always end with: what was confirmed, what could not be confirmed, and what the user should validate independently if stakes are high.
- **Stopping research as soon as the first plausible answer appears.** A quick hit on a credible-looking source feels like a complete answer but often isn't. At minimum, check whether a second source agrees, whether the source is primary, and whether the claim is still current.
- **Expressing calibrated uncertainty in ways that sound like hedging.** "It's possible that maybe perhaps..." reads as unhelpful vagueness. Use specific labels ("Likely", "Confirmed", "Unknown") with brief reasoning, not stacked qualifiers. Honesty about uncertainty is valuable; vague waffling is not.

## Full reference

### Research tools and when to use them

| Tool | Best for |
|---|---|
| Official documentation | Version-specific facts, API behavior, configuration |
| Primary research papers | Scientific claims, benchmark data |
| GitHub repo source code | Actual behavior vs. documented behavior |
| GitHub issues / PRs | Known bugs, recent changes not yet in docs |
| Changelog / CHANGELOG.md | What changed in which version |
| Stack Overflow | Common usage patterns, community-known gotchas |
| Web search | Current events, recent releases, pricing |

### Cross-referencing checklist

Before presenting research findings:
- [ ] Each claim has a source label (or is marked as inference)
- [ ] Time-sensitive claims are dated
- [ ] The most important claims are verified against primary sources
- [ ] Contradictions between sources are noted and reasoned about
- [ ] What I don't know is explicitly listed

### Handling conflicting sources

When two authoritative sources disagree:
1. Note both sources and their positions
2. Check publication date — prefer more recent
3. Check which is closer to primary (official docs > blog post)
4. If still conflicting, present both and note the conflict
5. Do not silently pick one — the conflict is itself useful information
