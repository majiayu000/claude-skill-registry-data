---
name: jargon-translator
description: "Rewrites scientific, legal, financial, or technical jargon into plain language suitable for a general news audience — preserving accuracy while making the meaning immediately clear to a non-specialist reader."
status: stable
category: research
subcategory: academic
version: 1.0
eval_score: 4.56
tags: [research, jargon, plain-language, translation, accessibility, academic]
---
# Jargon Translator

## What This Skill Does
Rewrites scientific, legal, financial, or technical jargon into plain language suitable for a general news audience — preserving accuracy while making the meaning immediately clear to a non-specialist reader.

## When To Use This Skill
- You are writing an article and need to explain a technical concept without dumbing it down or getting it wrong
- You have a quote from an expert that is technically accurate but incomprehensible to your readers, and you need a plain-language paraphrase for context
- You are editing a piece that is too technical for its intended audience and need to identify and replace the jargon
- You are preparing for an interview and want to confirm you understand the terminology well enough to ask follow-up questions

## What You Need To Provide
**Required:** The jargon-heavy text you want translated — a passage, sentence, or list of terms. Specify the field the jargon comes from if it is not obvious (medical, legal, financial, scientific, technological, military, bureaucratic).

**Optional:** The target audience (general reader, semi-specialist, young adult); the publication context (news article, broadcast script, social media post — each has different register requirements); specific terms you find most confusing; whether you want term-by-term translations, a full rewrite, or both.

## How the Assistant Approaches This
1. **Identifies every piece of jargon in the text.** Flags every term, phrase, or construction that a general reader would not immediately understand — including acronyms, initialisms, technical terms, discipline-specific idioms, and Latinate constructions common in legal and medical language.

2. **Provides a plain-language equivalent for each.** For every flagged term, gives a one-sentence definition written in conversational English. Where a single word can replace a technical phrase without losing meaning, provides the substitution. Where simplification would distort the meaning, explains the concept in a short phrase and notes the trade-off.

3. **Rewrites the full passage.** Produces a complete plain-language version of the original text that a general reader could understand on first reading. Preserves the original meaning and factual content — does not add interpretation or opinion.

4. **Flags where simplification involves a trade-off.** Marks any point where the plain-language version is less precise than the original and explains what nuance was lost. This lets the journalist make an informed choice about whether the simplification is acceptable for their context.

5. **Provides the "one sentence for readers" version.** Distils the entire passage into a single sentence that captures the essential meaning — usable as a summary paragraph, a social media post, or a broadcast intro line.

## Output Format
Three components delivered in sequence: **Glossary** (a table or list of jargon terms with plain-language equivalents), **Full Rewrite** (the complete passage in plain language), and **One-Sentence Summary** (the core meaning in a single sentence). Any trade-offs between simplicity and precision are noted in brackets within the rewrite. Tone: conversational, clear, accurate. Length depends on the input — the rewrite should be roughly the same length as the original or shorter, never significantly longer.

## Quality Criteria
- [ ] Every piece of jargon in the input is identified and translated — nothing is missed
- [ ] Plain-language equivalents are genuinely accessible to a non-specialist — not just slightly less technical
- [ ] The rewrite preserves the factual meaning of the original — simplification does not introduce inaccuracy
- [ ] Trade-offs between simplicity and precision are explicitly flagged
- [ ] The one-sentence summary captures the essential meaning without distortion
- [ ] The output does not talk down to the reader — plain language is not the same as patronising language
- [ ] Field-specific nuance is preserved where it matters (e.g., "associated with" is not silently replaced with "causes")

## Example

### Input
**Text:** "The phase III randomised, double-blind, placebo-controlled trial demonstrated non-inferiority of the novel therapeutic agent relative to the standard-of-care comparator on the primary endpoint of progression-free survival (HR 0.87, 95% CI 0.74–1.02, p=0.09), with a clinically meaningful improvement in the secondary endpoint of objective response rate (42% vs. 31%, p=0.003)."

**Field:** Medical / clinical trials
**Audience:** General newspaper reader
**Need:** Glossary, full rewrite, and one-sentence summary

### Output

**Glossary**

| Term | Plain-Language Equivalent |
|------|--------------------------|
| Phase III trial | The final and largest stage of testing a new treatment before it can be approved for general use |
| Randomised | Patients were assigned to treatment groups by chance (like a coin flip) to ensure a fair comparison |
| Double-blind | Neither the patients nor the doctors knew who was getting the real treatment and who was getting the dummy pill |
| Placebo-controlled | One group received a dummy treatment (placebo) to compare against the real treatment |
| Non-inferiority | The study was designed to show the new treatment is at least as good as the existing treatment — not necessarily better |
| Novel therapeutic agent | The new drug being tested |
| Standard-of-care comparator | The existing treatment that patients currently receive |
| Primary endpoint | The main outcome the study was designed to measure |
| Progression-free survival | How long patients lived without their disease getting worse |
| HR 0.87 | Hazard ratio — a measure of relative risk. 0.87 means patients on the new drug had a 13% lower rate of disease progression, but... |
| 95% CI 0.74–1.02 | ...the confidence interval crosses 1.0, meaning the result could be due to chance |
| p=0.09 | The statistical test for the main outcome did not reach the conventional threshold for significance (p<0.05) — the result is suggestive but not conclusive |
| Secondary endpoint | A supporting outcome the study also measured, but not the main one |
| Objective response rate | The percentage of patients whose tumours shrank measurably |

**Full Rewrite**

In the final stage of testing, the new drug was compared to the current standard treatment in a rigorously designed trial involving [number not specified] patients. Neither the patients nor their doctors knew who received which treatment, and patients were assigned to groups at random.

On the study's main measure — how long patients lived without their disease worsening — the new drug performed similarly to the existing treatment. Patients on the new drug had a 13% lower rate of disease progression, but this result did not reach statistical significance [meaning it could be due to chance rather than a real difference].

On a secondary measure — the percentage of patients whose tumours shrank — the new drug showed a clearer advantage: 42% of patients responded to the new drug compared to 31% on the existing treatment. This difference was statistically significant.

[Trade-off note: The original text describes the primary result as "non-inferiority," which has a specific statistical meaning — the study was designed to show the new drug is "not worse" rather than "better." This is a meaningful distinction in regulatory terms: a drug that meets non-inferiority standards may be approved even without proving superiority, particularly if it has other advantages such as fewer side effects or easier administration. The plain-language version simplifies this to "performed similarly," which is accurate for a general audience but loses the regulatory nuance.]

**One-Sentence Summary**

A large clinical trial found that a new drug was roughly as effective as the current treatment at slowing disease progression, and may be better at shrinking tumours, but the main result was not statistically conclusive.

## Known Limitations
- Simplification always involves trade-offs. The assistant flags where precision is lost, but the journalist must decide whether the simplification is acceptable for their audience and context. In some cases, the technical term is genuinely the only accurate way to express the concept.
- For highly specialised fields (quantum physics, advanced mathematics, certain areas of law), the "plain language" version may still require some reader effort. There is a floor below which complex ideas cannot be simplified without becoming misleading.
- The assistant translates the jargon as written. If the original text contains errors, unclear phrasing, or ambiguous technical language, the translation may reproduce those problems. When in doubt, the journalist should verify the translation with a domain expert.

## Related Skills
- [scientific-paper-summarizer](../scientific-paper-summarizer/SKILL.md) — summarise a full paper, including methodology and findings
- [study-methodology-evaluator](../study-methodology-evaluator/SKILL.md) — evaluate whether the study design supports the claims being made
- [legal-framework-brief](../../fact-checking/legal-framework-brief/SKILL.md) — translate legal jargon in the context of a specific legal framework
- [debate-state-summary](../../background/debate-state-summary/SKILL.md) — understand the broader debate the technical language refers to
