---
name: debate-state-summary
description: "Produces a structured, neutral summary of the current state of a public debate or controversy — mapping the main positions, the actors behind them, the evidence each side cites, and the unresolved questions — so a journalist can get up to speed quickly and identify the underreported angles."
status: stable
category: research
subcategory: background
version: 1.0
eval_score: 4.5
tags: [research, debate, controversy, positions, analysis, background]
---
# Debate State Summary

## What This Skill Does
Produces a structured, neutral summary of the current state of a public debate or controversy — mapping the main positions, the actors behind them, the evidence each side cites, and the unresolved questions — so a journalist can get up to speed quickly and identify the underreported angles.

## When To Use This Skill
- You are new to a story and need to understand the landscape of a public debate before reporting on it
- You need to brief an editor or producer on a controversy and want to present all sides fairly
- You are writing a backgrounder or explainer and need a clear framework for the competing positions
- You suspect the media narrative oversimplifies the debate and want to map its actual complexity

## What You Need To Provide
**Required:** The topic or question at the centre of the debate (be specific — "Should gig-economy workers be classified as employees?" is better than "gig economy debate"); the jurisdiction or context if relevant.

**Optional:** Your current understanding of the main positions; specific actors or organisations you know are involved; the media narrative you have seen so far (helps the assistant identify what is being underreported); the audience for your output (general public, specialist readership, editorial team).

## How the Assistant Approaches This
1. **Defines the core question.** Distils the debate to a single, precise question that the competing positions are answering differently. This prevents the summary from drifting into adjacent issues.

2. **Maps the main positions.** Identifies 3–5 distinct positions in the debate (not just "for" and "against" — most real debates have more nuance). For each position, describes: the argument in 2–3 sentences, the types of actors who hold it, and the evidence or reasoning they cite.

3. **Identifies the points of agreement.** Notes where opposing sides actually agree — these are often overlooked in coverage and can be the most revealing elements of a debate.

4. **Flags the unresolved questions.** Lists the specific factual or analytical questions that remain genuinely contested — where the evidence is ambiguous, missing, or disputed. These are the questions a journalist should investigate rather than assume answers to.

5. **Highlights the underreported angles.** Based on the positions mapped, identifies 2–3 aspects of the debate that receive less media attention than they deserve — minority positions, overlooked stakeholders, or evidence that complicates the dominant narrative.

## Output Format
600–900 words. Four sections: **Core Question** (one sentence), **Positions Map** (3–5 positions, each with argument, actors, and evidence), **Points of Agreement** (2–3 bullet points), and **Unresolved Questions and Underreported Angles** (combined section, 4–6 bullet points). Tone: strictly neutral — the summary should not reveal which position the journalist or the assistant favours. Language: accessible to a non-specialist reader, with technical terms defined on first use.

## Quality Criteria
- [ ] Core question is specific and debatable — not a truism or a loaded question
- [ ] Positions map includes at least three genuinely distinct positions — not just "yes" and "no"
- [ ] Each position is described with enough detail to be recognisable to its proponents — no straw men
- [ ] Points of agreement are genuinely shared across positions, not trivial
- [ ] Unresolved questions are specific enough to investigate — not vague ("more research is needed")
- [ ] Underreported angles are genuinely underreported, not just the journalist's preferred framing
- [ ] Tone is neutral throughout — no position is described more sympathetically than another
- [ ] Output could be published as-is as a briefing document for an editorial team

## Example

### Input
**Topic:** Whether national governments should mandate algorithmic transparency for social media platforms — specifically, requiring platforms to publish the criteria their recommendation algorithms use to rank and promote content
**Jurisdiction:** Primarily a Western democratic context, but the debate is global
**Media narrative seen so far:** Most coverage frames it as "regulators vs. big tech" — regulators want transparency, platforms resist

### Output

**Core Question**

Should governments require social media platforms to publicly disclose the specific criteria and weighting factors their recommendation algorithms use to rank, filter, and promote content to users?

**Positions Map**

*Position 1 — Full algorithmic disclosure*
Platforms should be legally required to publish the complete logic of their recommendation algorithms, including the specific signals used (engagement metrics, user behaviour, advertiser preferences) and how they are weighted. Proponents argue that content recommendation is a form of editorial decision-making with enormous public impact, and that editorial decisions at this scale require public accountability. This position is held by many digital rights organisations, some academics in media studies and computer science, and several legislative proposals in democratic countries. Evidence cited: research showing that recommendation algorithms amplify divisive content, increase political polarisation, and can promote health misinformation at scale.

*Position 2 — Structured transparency to regulators, not the public*
Platforms should be required to disclose algorithmic criteria to an independent regulator or auditor, but not to the general public. This position argues that full public disclosure would expose trade secrets, enable manipulation by bad actors (who could game the algorithm), and provide little practical benefit to ordinary users who cannot interpret technical specifications. Held by some technology policy researchers, certain industry-aligned think tanks, and some regulators who prefer audit-based models. Evidence cited: precedent in financial regulation, where banks disclose risk models to regulators rather than the public.

*Position 3 — Outcome-based regulation, not process disclosure*
Instead of mandating transparency about how algorithms work, governments should set measurable standards for what outcomes algorithms must produce (e.g., limits on the amplification of verified misinformation, minimum exposure to diverse viewpoints) and hold platforms accountable for results. Proponents argue that algorithmic systems are too complex and fast-changing for static disclosure to be meaningful, and that outcomes are what actually matter to users. Held by some computer scientists, AI policy researchers, and platform companies that prefer performance standards to structural disclosure. Evidence cited: the rapidly evolving nature of machine-learning systems that makes any snapshot of algorithm logic obsolete within months.

*Position 4 — No government mandate*
Algorithmic transparency should be voluntary, driven by market competition and user choice rather than regulation. Government mandates risk stifling innovation, creating compliance costs that benefit large incumbents over smaller competitors, and setting precedents for government control over information systems. Held by platform industry trade associations, some libertarian-leaning think tanks, and certain technology executives. Evidence cited: the history of regulatory capture in other industries, the difficulty of defining "algorithm" in a legally precise way, and the risk that transparency mandates in democratic countries legitimise censorship mandates in authoritarian ones.

**Points of Agreement**

- All positions acknowledge that recommendation algorithms significantly shape what information users see and that this has real consequences for public discourse.
- All positions agree that some form of accountability is necessary — the disagreement is over the mechanism (public disclosure, regulatory audit, outcome standards, or market forces).
- No mainstream position argues that platforms should have zero obligations regarding content recommendation — even the anti-mandate position typically supports voluntary transparency initiatives.

**Unresolved Questions and Underreported Angles**

- **Can algorithmic disclosure actually be meaningful to the public?** The technical complexity of modern recommendation systems means that even full disclosure might produce documents no non-specialist can interpret. Is this an argument against disclosure or an argument for intermediary institutions (academics, journalists, auditors) who can translate?
- **What counts as an "algorithm" for regulatory purposes?** Machine-learning systems are not static rule sets — they evolve continuously based on data. How would a transparency mandate handle a system that changes daily? This definitional question is largely unaddressed in current legislative proposals.
- **The global jurisdiction problem.** If one country mandates disclosure, platforms may comply minimally or restructure operations to avoid the requirement. How do national mandates interact with global platform architectures? Coverage rarely addresses this.
- **Small platform impact.** Most coverage focuses on the largest platforms. Would transparency mandates disproportionately burden smaller competitors that lack the compliance infrastructure of major companies? The startup and open-source community perspective is underreported.
- **The manipulation risk is real but unquantified.** Platform companies argue that disclosing algorithm criteria would enable bad actors to game the system. Is there evidence from other domains (search engine optimisation, financial regulation) about how disclosure affects manipulation, or is this a theoretical concern being used to resist accountability?

## Known Limitations
- The assistant's knowledge of the debate is limited to its training data. For fast-moving policy discussions, positions may have evolved, new actors may have entered, or legislative proposals may have advanced since the assistant's last update. The journalist should verify the current state against recent reporting.
- The summary maps positions as they are most commonly articulated in public discourse. Internal industry positions, private government deliberations, and emerging academic arguments may not be captured. The summary is a starting point, not a substitute for original reporting.
- Neutrality is a goal, not a guarantee. Despite the assistant's best efforts to present positions evenhandedly, the framing of "core question" and the selection of positions inevitably involve editorial choices. The journalist should adjust the framing to fit their editorial context.

## Related Skills
- [policy-decision-maker-mapper](../../people/policy-decision-maker-mapper/SKILL.md) — map the decision-makers behind the positions identified in this summary
- [legislative-history-brief](../legislative-history-brief/SKILL.md) — trace the legislative history of any proposals mentioned
- [historical-precedent-finder](../historical-precedent-finder/SKILL.md) — find historical analogies for the regulatory debate
- [claim-origin-tracer](../../fact-checking/claim-origin-tracer/SKILL.md) — trace the origin of specific claims made in the debate
