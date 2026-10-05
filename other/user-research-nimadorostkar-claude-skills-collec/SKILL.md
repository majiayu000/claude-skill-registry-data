---
name: user-research
description: Use when planning, running, or synthesizing user research. Covers interview questions that produce evidence rather than opinions, usability testing, and turning transcripts into findings.
metadata:
  category: business
  version: 1.0.0
  tags: [research, interviews, usability, synthesis, discovery]
---

# User Research

## Purpose

Learn what users actually do, as opposed to what they say they would do. The distinction is everything: people are unreliable narrators of their own future behavior and reliable narrators of their own past.

## When to Use

- Planning interviews or a usability test.
- Writing an interview guide.
- Synthesizing transcripts or session notes into findings.
- Deciding whether a feature idea is worth building.

## Capabilities

- Study design and participant selection.
- Interview questions that elicit behavior rather than opinion.
- Usability-test design and moderation.
- Synthesis: from transcripts to themes to recommendations.
- Distinguishing what users said from what they did.

## Inputs

- The question the research must answer.
- Access to actual users, not proxies.
- The decision this informs.

## Outputs

- Findings grounded in observed behavior.
- Themes supported by multiple participants.
- Recommendations with a confidence level.

## Workflow

1. **Ask what decision this informs** — Research with no decision attached is a hobby. The decision determines who you talk to and what you ask.
2. **Ask about the past, not the future** — "Tell me about the last time you needed to do X" produces evidence. "Would you use a feature that does X?" produces politeness. Nobody can predict their own behavior, and everybody says yes.
3. **Ask for the story, then dig** — What happened, what did you do, what happened next, what did you do instead when it did not work. The workaround is the finding.
4. **In usability tests, give a task and shut up** — "Buy a red one, size medium." Then do not speak. Every hint you give destroys the data you came for.
5. **Synthesize across participants, not within** — One person's complaint is an anecdote. The same behavior in five of eight participants is a finding.
6. **Report behavior, and separate it from opinion** — "Six of eight participants abandoned at the address form" is evidence. "Participants said the form was confusing" is a report of what they said.

## Best Practices

- Never ask "would you use this?" The answer is yes, it is always yes, and it means nothing. Ask what they did last time, and what it cost them.
- The workaround is the strongest signal in user research. A user who has built a spreadsheet to do what your product should do has told you exactly what to build, and has demonstrated that they will invest effort to get it.
- In a usability test, silence is the method. The urge to help is overwhelming and it invalidates the test.
- Five to eight participants surfaces most usability problems. Beyond that, findings repeat. Do not delay research waiting for a large sample.
- Separate observation from interpretation in the notes. "Clicked 'Continue' three times" is an observation. "Was confused by the button" is an interpretation, and it may be wrong.
- Watch what they do, not what they say. When the two conflict, the behavior is the truth.

## Examples

**Questions that produce evidence, and questions that do not:**

```text
DO NOT ASK                                  ASK INSTEAD

"Would you use a feature that                "Tell me about the last time you
 automatically categorizes expenses?"         had to categorize expenses. Walk me
                                              through exactly what you did."
  -> Everyone says yes. It costs them
     nothing to say yes.                        -> Produces: what they actually do,
                                                   how long it takes, what they
                                                   have already tried, and whether
                                                   it hurts enough to change.

"How often do you use the reports?"          "When did you last open a report?
                                              What were you trying to find out?"
  -> Produces a made-up number, biased
     upward.                                    -> Produces a date and a real
                                                   motivation, or "I never have",
                                                   which is the finding.

"Is the interface easy to use?"              [Give them a task. Say nothing.]

  -> Produces politeness.                       -> Produces the truth in 90 seconds.

"What features do you want?"                 "What's the most frustrating part of
                                              your week, in this area?"
  -> Produces a wish list of features
     from other products.                       -> Produces the problem, which is
                                                   yours to solve, rather than
                                                   their guess at a solution.
```

**Synthesis that separates behavior from opinion:**

```markdown
## Study: expense categorization — 8 participants

### Observed behavior (this is the evidence)

- 6 of 8 maintain a spreadsheet ALONGSIDE the product, to do categorization the
  product already claims to do. Five had built it themselves; one inherited it.
- Average time spent on the spreadsheet: 40 minutes per week, self-reported,
  and two participants showed us the file with a modification history that
  supports the estimate.
- 7 of 8 could not find the existing bulk-categorization feature when given
  the task. It is two levels deep in a settings menu.
- 3 of 8 said, unprompted, that they did not know the feature existed.

### What they said (this is context, not evidence)

- All 8 said categorization was "important". This tells us nothing; nobody says
  their own workflow is unimportant.
- 5 said they would "definitely use" an automatic categorization feature.
  Discount this entirely — see the spreadsheets, which are the real evidence
  that the need exists.

### Finding

The need is proven, not by what they said, but by the fact that six of eight
built and maintain a manual workaround costing 40 minutes a week. That is
revealed preference, and it is far stronger than any stated one.

The product ALREADY HAS the feature. Seven of eight could not find it.

This is not a feature gap. It is a discoverability failure, and building the
"new" automatic categorization feature on the roadmap would be building a
second thing that nobody can find.

### Recommendation (high confidence)

Surface bulk categorization in the main workflow, at the point where the user
is looking at uncategorized expenses. Measure: feature discovery rate, and the
number of users who stop maintaining an external spreadsheet.
```

## Notes

- The finding in the example — "we already built it and nobody can find it" — is one of the most common outcomes of real user research, and it is invisible from analytics alone, because a feature nobody finds shows zero usage exactly like a feature nobody wants.
- Revealed preference (they built a spreadsheet) beats stated preference (they said they'd use it) every time. When the two conflict, believe the behavior.
- Five to eight participants is genuinely sufficient for usability findings. The instinct to gather more is usually an instinct to delay.
