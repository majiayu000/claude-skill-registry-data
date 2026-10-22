---
name: reach-source-check
description: Checks the source behind each fact for who published it, whether it is the original, the date on the page and whether the page says what the fact claims, with disagreements shown side by side and a keep, fix or drop per fact. Use for "run reach-source-check", "source check", "check my sources", "is this source reliable", "verify this fact", "where did this fact come from", "fact check my research", "SIFT check", part of the Claude Guide for Outreach Pack by Polar Bear.
---

# Source Check

## When To Use
A fact sounds right and you cannot say where it came from, or two pages disagree about the same thing. Run this on the facts you actually plan to use. It answers: would this fact survive the reader checking it?

## When Not To Use
If the question is whether a page is about the right person, that is Identity Check. If you have no fact list yet, start with Company Fact List; this skill checks sources, it does not collect.

## Inputs
- Your Company Fact List, or the facts you plan to use with their links.
- Which facts matter most: the two or three you may mention in a message or a call.
If you have none of this, I start from one fact and one link you paste, and mark the output as a first draft.

## Approach
SIFT, the four moves Mike Caulfield describes (stop, investigate the source, find better coverage, trace claims to the original), with lateral reading as the Digital Inquiry Group teaches it in Civic Online Reasoning: leave the page and see what other sources say about its publisher. Both were built for news claims. For a company fact the original is usually the organisation's own page or a filing, which is primary and still promotional. Any browsing is read only and never on LinkedIn. The failure it prevents: quoting a number from an article that copied it from a press release that never said it.

## Workflow
1. Ask at most three questions: which facts you plan to use, how old is too old for you, and whether any source is one you already trust and why.
2. Stop: for each fact, say in one line what exactly is being claimed. Vague claims cannot be checked, so I rewrite them as one checkable statement or flag them.
3. Investigate the source: who published the page, and what others say about that publisher. A page that describes itself is not evidence about itself.
4. Trace to the original: is this page the origin of the claim or a copy of it? If it is a copy, find the original and read what it actually says.
5. Compare: the date on the page against your window, and the wording on the page against the wording of the fact. A fact that says more than its source is marked "fix", with the narrower wording the page supports.
6. Find better coverage when a fact rests on one weak page. Where two sources disagree, show both side by side and do not pick one.
7. Give each fact a verdict for you to confirm: keep, fix (with the corrected claim) or drop.

## Output Format
```markdown
# Source Check
Facts checked: [number] | From: [Company Fact List, date] | Too old means: [your limit]
## Check per fact
| # | Claim, in one line | Published by | Original or copy | Date on page | Page says what the fact claims? | Verdict |
|---|---|---|---|---|---|---|
| F1 | [claim] | [publisher] | [original / copy of: link] | [date] | [yes / says less: wording] | [keep / fix / drop] |
## Fixed claims
- F[number]: was "[claim]", the source supports "[narrower claim]"
## Disagreements
| Fact | Source A says | Source B says |
|---|---|---|
| [fact] | [wording, link, date] | [wording, link, date] |
## Decision
[Your name] confirms each keep, fix or drop and decides which facts the brief may cite, by [date].
```

## Done When
- Every fact you plan to use has a publisher, a date and an original-or-copy answer.
- Every "fix" shows the old claim and the narrower one.
- Disagreements are shown side by side, with neither chosen for you.
- Dropped facts are removed from the numbered list you carry forward.

## Quality Bar
- The check is about the source and the claim, never about a person.
- A primary source is still a party to the story: an organisation's own page shows what it says, not what is true.
- "Could not find the original" is a result, and usually means drop.
- Old is not wrong: an old fact is kept as background and labelled with its date.
- A fact that cannot be traced to a source is dropped, never softened; you decide what is kept.

## Next
Run reach-company-research-brief (Company Research Brief) to write half a page from the facts that passed.

## About the makers

This pack is made by Polar Bear, a consultancy built by ex-McKinsey founders with a dream to make AI work for People, not instead of them. We help our clients build people systems and AI-first ways of working, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
