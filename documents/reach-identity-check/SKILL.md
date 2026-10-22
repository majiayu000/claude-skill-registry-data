---
name: reach-identity-check
description: Confirms that your sources are about the right person, with each source tested for same name and same organisation, namesakes set aside, the role confirmed or changed and a verdict of confirmed or not confirmed. Use for "run reach-identity-check", "identity check", "is this the right person", "same name different person", "check for a namesake", "confirm who this is", "is this source about them", "which one is the right person", part of the Claude Guide for Outreach Pack by Polar Bear.
---

# Identity Check

## When To Use
The search returns three people with the same name, and one of them has a career that would make a wonderful opening line. Run this before any research on a person. It answers one question: are these pages about the person I mean?

## When Not To Use
If you already know the person or have their own page from their organisation's site, identity is settled: go to Person Research Brief. If the doubt is about whether a claim is true, not who it is about, that is Source Check.

## Inputs
- The name and organisation you start from, and where you got them (your Contact Shortlist, an article, a programme).
- The pages that came up, or the ones you want read. Public pages only, never LinkedIn.
- Anything you know first hand: a role, a city of work, a talk they gave.
If you have none of this, I start from the name and organisation alone and say plainly how little that allows.

## Approach
Identity confirmation before any person research: a generic research discipline. A source counts only if it shows the same name and the same organisation, on the page itself. A namesake is the most embarrassing error in outreach, because the reader knows at once that nobody checked. When identity cannot be confirmed, the honest move is to say so and research the organisation only. Any browsing is read only: no clicking, typing or forms.

## Workflow
1. Ask at most three questions: the name and organisation you start from, where they came from, and what you know first hand that could tell two people apart.
2. Write the anchor: full name plus organisation. A name on its own is never an anchor.
3. Test each source on two questions and quote the evidence on the page: does it show the same name, and does it show the same organisation? Both must be on the page; a likely match is not a match.
4. Set namesakes aside in their own list with what gave them away (a different organisation, field or period). Nothing from a namesake is carried forward.
5. Check the role: does the most recent dated source still show the role you started from? If it shows another role or organisation, record the change with its date. People move, and an old page is not wrong, only old.
6. Give the verdict: confirmed (at least one dated source shows name and organisation together) or not confirmed.
7. If not confirmed, say what to do: research the organisation only, ask someone who knows them, or leave this person off the run.

## Output Format
```markdown
# Identity Check
Anchor: [full name] at [organisation] | Started from: [where the name came from] | Date: [date]
## Sources tested
| Source (link, date) | Same name? | Same organisation? | Evidence on the page | Counts |
|---|---|---|---|---|
| [link, date] | [yes / no] | [yes / no / not stated] | [the words on the page] | [yes / no] |
## Namesakes set aside
- [link]: [what showed it is someone else]
## Role
[Role confirmed as of [date], or changed: now [role] at [organisation], per [link, date].]
## Verdict
[Confirmed / not confirmed], on [number] sources.
## Decision
[Your name] decides by [date] whether to research this person, research the organisation only, or ask someone who knows them.
```

## Done When
- The anchor is a name plus an organisation.
- Every source has a yes or no on both questions, with the words from the page.
- Namesakes are listed separately and nothing from them is reused.
- The verdict is one of two words, and "not confirmed" comes with a next move.

## Quality Bar
- "Probably the same person" is recorded as not confirmed.
- A photo is never used to match people.
- The check establishes who a page is about and stops; it collects no facts about the person.
- A change of role is a dated fact, not a guess about why.
- If identity is not confirmed, nothing about the person is used; you decide what happens next.

## Next
Run reach-person-research-brief (Person Research Brief) to collect sourced facts about this person's work.

## About the makers

This pack is made by Polar Bear, a consultancy built by ex-McKinsey founders with a dream to make AI work for People, not instead of them. We help our clients build people systems and AI-first ways of working, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
