---
name: name-brand
description: Generates brand or product name candidates across naming territories with rationale and risk flags, and lists the trademark, domain and language checks still to do. Use when naming a product.
license: CC0-1.0
metadata:
  version: 1.0.0
  kind: prompt
  category: branding
  source: https://hermes-ide.com/prompts/name-brand
  catalog: 2026.1014.1
---

# Generate brand and product name candidates

## Inputs

- [DESCRIPTION] (required): What is being named, what it does, for whom, the markets and languages it will operate in, and competitors' names.
- [PERSONALITY] (optional): How the name should feel, and anything to avoid (sounds, words, styles, names already rejected). Optional.
- [COUNT] (optional; default: 20): How many candidates to generate, between 10 and 40.

Take each value from the invocation or the user’s message. If a required value is missing, ask for it once.

<context>
Name generators produce long lists of mashed-up words with no reasoning, cluster around the same obvious roots as every competitor, and imply that a name is available because it sounds new. A useful naming round starts from a brief, explores distinct territories, explains what each name does, flags obvious problems early, and is honest that availability and trademark clearance can only be established by searches and, for anything important, a trademark professional.
</context>

<task>
Generate [COUNT] name candidates.

<description>
[DESCRIPTION]
</description>
Only if [PERSONALITY] was provided: 
<personality>
[PERSONALITY]
</personality>

1. **Naming brief:** in 4 to 6 bullets, the positioning the name must support, the feeling, the markets and languages, what competitors' names have in common (so you can avoid sounding like them), and practical criteria (length, spelling from hearing, pronounceable in the target languages).
2. Generate the candidates across at least four territories, and label each:
   - **descriptive** (says what it does; clear but hard to protect),
   - **suggestive** (hints at a benefit; often the best balance),
   - **evocative or metaphor** (borrows an image or story),
   - **invented or coined** (new word; most protectable, needs the most marketing),
   - **compound or blend** (two roots combined).
3. For each candidate give: the name, territory, the idea behind it in one line, how it is pronounced if not obvious, and risk flags you can see: hard to spell from hearing, close to a well-known brand in the same field, a generic word that is weak as a trademark, or a possible unwanted meaning or sound in a target language (say "check" rather than asserting a meaning you are not sure of).
4. Shortlist the 5 strongest against the brief, with the reason and the main risk for each.
5. List the checks still to do for the shortlist, as a checklist: trademark searches in each target market and in the relevant Nice classes (for example the USPTO, EUIPO and WIPO Global Brand Database), domain availability and acceptable alternatives, social handles and app store names, a linguistic check with native speakers in each market, and a say-it-and-spell-it test with real people.
</task>

<constraints>
- Never state or imply that a name is available, unregistered, or that a domain is free. You cannot check. Say that these must be verified.
- This is a creative exercise, not legal clearance. Say once that a trademark attorney or agent should run a clearance search before the company invests in a name.
- Do not reuse or lightly alter famous brand names, and do not produce names that mock a group, language or culture.
- If [COUNT] is outside 10 to 40, use the nearest bound and say so. If the description is too thin to know what the product does, ask up to three questions and stop.
</constraints>

<output_format>
## Naming brief
## Candidates
| # | Name | Territory | Idea | Pronunciation | Risk flags |
## Shortlist
Numbered, 5 names, each with the reason and the main risk.
## Checks still to do
A checklist, then the one-line note about professional trademark clearance.
</output_format>
