---
name: topic-glossary-writer
description: "Produces a plain-language glossary of essential terms for a complex or specialist topic, written so that a journalist, presenter, or producer with no prior expertise can understand and use the terms correctly before entering an interview or writing a script."
status: stable
category: pre-production
subcategory: pre-production
version: 1.0
eval_score: 4.2
tags: [glossary, terminology, research, briefing, pre-production]
---
# Topic Glossary Writer

## What This Skill Does
Produces a plain-language glossary of essential terms for a complex or specialist topic, written so that a journalist, presenter, or producer with no prior expertise can understand and use the terms correctly before entering an interview or writing a script.

## When To Use This Skill
- You are assigned to cover a specialist beat (finance, science, law, technology, medicine) and need to get up to speed before your first interview or deadline
- You are briefing a presenter or on-screen talent who needs to speak confidently about a technical subject without getting terminology wrong
- You are writing a script or article on a complex topic and want a reference document to keep definitions consistent throughout
- Your team is producing a series on an unfamiliar subject and needs shared vocabulary before production begins

## What You Need To Provide
**Required:** The topic or subject area, and the intended audience for the glossary (e.g. journalist preparing for an interview, TV presenter, general reader, production team).
**Optional:** The specific story angle or editorial focus, any terms you already know are relevant, the format of the final content (broadcast, print, online), and any terms you want defined even if they seem basic.

## How the Assistant Approaches This
1. Identifies the core terms a non-specialist must understand to follow the topic accurately — prioritising terms that are commonly misused, misunderstood, or used inconsistently across sources.
2. Writes each definition in plain language, at the level of a well-educated non-specialist. Avoids circular definitions ("a derivative is a type of financial derivative").
3. Adds a brief note where a term is frequently confused with another, or where common usage differs from technical usage — these distinctions are where errors most often occur in journalism.
4. Orders terms logically: foundational concepts first, then more complex terms that build on them. Not alphabetical, unless specifically requested.

## Output Format
A headed glossary of 10–25 terms. Each entry: the term in bold, a plain-language definition of 2–4 sentences, and (where relevant) a "Watch out" note flagging common misuse or confusion. Ends with a short list of 3–5 terms the journalist should avoid using unless they are certain of the meaning. Format is clean prose, not a table — readable on screen or printed as a briefing document.

## Quality Criteria
- [ ] Every definition is self-contained and understandable without reading the others first
- [ ] No definition uses the term being defined as part of its own explanation
- [ ] Common misuses or confusions are flagged explicitly, not assumed to be obvious
- [ ] The level of language matches the stated audience — not dumbed down, not unnecessarily technical
- [ ] Terms are ordered so the glossary can be read top-to-bottom as a learning sequence
- [ ] The "terms to avoid" section is specific and explains why each term is risky

## Example

### Input
Topic: Carbon markets and carbon offsetting. Audience: A journalist preparing to interview a climate policy economist for the first time. Story angle: Whether voluntary carbon markets are delivering real emissions reductions or functioning as a way for companies to avoid cutting their own emissions.

### Output

**Glossary: Carbon Markets and Carbon Offsetting**
*Prepared for journalist briefing — interview preparation*

---

**Carbon emissions**
The release of carbon dioxide (CO₂) and other greenhouse gases into the atmosphere, primarily through burning fossil fuels, industrial processes, and deforestation. In reporting, "carbon" is often used as shorthand for all greenhouse gases, measured in CO₂-equivalent units. This is standard practice but worth confirming when precision matters.

**Carbon market**
A trading system in which organisations buy and sell the right to emit a certain amount of greenhouse gas, or purchase credits representing emissions reductions made elsewhere. There are two main types: compliance markets (mandatory, regulated by governments) and voluntary markets (optional, used by companies making climate pledges). Your story focuses on the voluntary market — keep the distinction clear.

**Carbon offset / carbon credit**
A carbon offset (also called a carbon credit) represents one tonne of CO₂ that has theoretically been prevented from entering the atmosphere or removed from it. Companies purchase offsets to "cancel out" their own emissions. One credit = one tonne reduced or removed, in theory.
**Watch out:** The terms "offset" and "credit" are used interchangeably in practice, but some technical sources treat them differently. Ask your interviewee which term they use and follow their usage.

**Additionality**
The principle that a carbon offset project must represent emissions reductions that would not have happened without the funding from carbon credit sales. If a forest would have been protected anyway, credits from that forest are not "additional" — they represent no real-world benefit.
**Watch out:** This is the central credibility question in carbon markets. Many disputed offset projects fail the additionality test. It is worth asking your interviewee directly how additionality is verified.

**Permanence**
Whether an emissions reduction or carbon removal will last. A forest that absorbs carbon but is later cut down or burns in a wildfire is not permanent. Permanence is a major challenge for nature-based offset projects.

**Leakage**
When protecting one area of forest causes deforestation to shift to a neighbouring unprotected area. The protected forest earns credits, but net emissions don't fall. A common and underreported problem in offset project assessments.

**Verification / validation**
The process by which an independent third party checks that an offset project is real, measurable, and additional. Standards bodies such as Verra and Gold Standard accredit verifiers and certify projects. Verification does not guarantee quality — it means the project met the standard's criteria, which are themselves disputed.

**Net zero**
A state in which an organisation's total greenhouse gas emissions are balanced by an equivalent amount of removal or reduction elsewhere. Many corporate "net zero" commitments rely heavily on purchased offsets rather than internal emissions cuts — this is the core tension in your story.
**Watch out:** "Net zero" and "carbon neutral" are often used as synonyms but have different technical meanings. "Carbon neutral" typically refers to CO₂ only; "net zero" covers all greenhouse gases. Ask which one your interviewee means.

**Carbon neutral**
A claim that an organisation's carbon dioxide emissions are fully offset by reductions or removals elsewhere. Does not necessarily cover other greenhouse gases such as methane or nitrous oxide.

**Scope 1, 2, and 3 emissions**
A classification system for where a company's emissions originate. Scope 1: direct emissions from operations the company owns. Scope 2: emissions from purchased energy. Scope 3: all other indirect emissions, including those from suppliers and customers — typically the largest category and the hardest to reduce. Many companies set net-zero targets that exclude Scope 3.

**Greenwashing**
The practice of making misleading claims about environmental credentials. In the context of carbon markets, it most often refers to companies claiming to be "carbon neutral" or "net zero" through offset purchases while making little effort to reduce their own emissions.

---

**Terms to avoid unless certain of the meaning:**

- **"Carbon neutral"** — check whether the claim covers CO₂ only or all greenhouse gases, and whether it relies on offsets or actual reductions.
- **"Net zero"** — the term is used loosely. Ask for the specific target date, which gases are included, and what proportion of the target is met by offsets versus internal cuts.
- **"Verified"** — verification means a project met a standard's criteria, not that the standard is rigorous or that the credits are credible. Be specific about which standard.
- **"Offset" as a verb** ("the company offsets its flights") — implies the emissions are genuinely cancelled out, which is the claim under scrutiny in your story. Use "purchases offsets to claim cancellation of" or similar until the story's conclusion is established.
- **"Climate positive"** — a marketing term with no agreed technical definition. Avoid without a precise explanation.

## Known Limitations
- The assistant's knowledge of specific offset standards, verification bodies, and market mechanisms reflects its training data. For breaking regulatory developments or recently updated standards, cross-check with a specialist source or the relevant standards body's published documentation.
- Glossaries work best for topics with relatively stable terminology. In fast-moving fields (AI regulation, emerging financial instruments), terms may shift in meaning between the assistant's training cutoff and your publication date.
- This skill defines terms; it does not assess which claims in your story are accurate. Use the glossary as a foundation for questions, not as a substitute for expert review of your final copy.

## Related Skills
- [fact-sheet-writer](../fact-sheet-writer/SKILL.md)
- [story-pitch-writer](../story-pitch-writer/SKILL.md)
- [tailored-interview-questions](../tailored-interview-questions/SKILL.md)
