---
name: cx-knowledge-base-audit
description: Use to audit a help centre or knowledge base against the conversations customers actually have, finding coverage gaps, stale articles and unused content. Trigger for "what should we write help articles about", "audit our knowledge base", KB coverage gaps, self-service deflection content, or preparing a knowledge base to ground an AI support agent.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: analysis
---

# Auditing a knowledge base against real contacts

One question: **what are customers contacting you about that your knowledge base
does not cover?**

That gap is the ceiling on self-service deflection, and it is the ceiling on any AI
agent grounded in the KB. An agent cannot answer what the KB does not contain, so
**KB coverage is a leading indicator of AI agent performance**, not a documentation
chore. Teams routinely buy an AI agent, point it at a KB that covers 60% of their
contact drivers, and are surprised by a 60% containment ceiling.

Read-only.

## What it checks

| Check | Finding |
| --- | --- |
| Coverage | Share of conversations with no article that plausibly answers them |
| Gap terms | The vocabulary appearing in uncovered conversations — the gaps, named |
| Stale articles | Not updated recently, **ordered by how much they are used** |
| Unused articles | Matched no conversation |
| Metadata gaps | Articles missing `updated_at` or view counts |

The stale ordering matters more than the count. A stale article nobody reads is
untidy. **A stale article customers hit constantly is actively harmful**, because
agents and AI agents are grounding answers in out-of-date content.

## Usage

```bash
node scripts/audit-coverage.mjs ./out/zendesk --articles ./kb/articles.jsonl
```

**Arguments**

- `--articles <path>` — JSONL, one article per line:
  `{ id, title, body, updated_at?, url?, views? }`
- `--out <dir>` — where to write `coverage-gaps.jsonl`. Default `./out/kb-audit`.
- `--stale-days <n>` — staleness threshold. Default 365.

The conversation side is a canonical export from any platform export skill, so
this works identically whichever helpdesk you run.

**Include `views` if your platform provides it.** Without view counts you cannot
distinguish "nobody needs this article" from "this article is quietly preventing
contacts", and those lead to opposite decisions.

**Message bodies are required.** Matching on subjects alone badly understates
coverage, because subjects are short and often generic ("Help", "Question"). The
script warns when `messages.jsonl` is absent.

## How matching works, and why it is conservative

Each conversation's first public customer message is compared against every
article using **IDF-weighted asymmetric containment**:

- **Asymmetric**, because an article is far longer than a question. Jaccard
  similarity punishes that length difference so heavily that a perfectly good
  article scores near zero. What matters is what share of the *question's* terms
  the article covers.
- **IDF-weighted**, so boilerplate present in every article ("contact", "support",
  "account") stops propping up scores. Terms absent from the whole KB carry the
  maximum weight — a word nowhere in your KB is the strongest evidence of a gap.
- **Minimum matched terms**, because a single shared generic noun ("order") clears
  any ratio threshold on a short question. Without this rule a completely
  uncovered topic gets reported as weakly covered, which is the failure mode that
  makes this kind of audit useless.

Conversations land in `covered`, `weak`, or `uncovered`.

**Matching is lexical, not semantic.** An article that answers a question in
different words scores low. So treat `uncovered` as **a list to review**, not a
verdict — read the samples before commissioning content. The output is a
prioritised reading list, and that is genuinely useful; it is not an oracle.

## Coverage is necessary, not sufficient

An article can exist and still deflect nothing:

- It is unfindable — search does not surface it for the words customers use.
- It is out of date, so following it fails.
- It is wrong.
- It is written for the wrong reader.

And for an AI agent, **a wrong article is worse than a missing one**: a missing
article produces a handoff, a wrong article produces a confident wrong answer.
So a coverage number rising is not on its own evidence that self-service improved.

## Present results to the user

1. **The uncovered rate, and the named gap terms.** The terms are the actionable
   output — "cryptocurrency, wallet, transfer" is a content brief; "23% uncovered"
   is not.
2. **Uncovered samples.** These make the gap concrete and let a human confirm the
   matching is not simply wrong.
3. **Stale articles ordered by usage**, with the point made explicitly that a
   heavily-used stale article is the priority.
4. **Unused articles, with the caveat attached.** Never present these as a
   deletion list — an unmatched article may be preventing the very contacts that
   would make it appear used. Check views first.
5. **The lexical-matching limitation**, before anyone commissions writing based on
   the output.
6. **Metadata gaps**, since missing `views` or `updated_at` silently disables two
   of the five checks.
7. **If this is for an AI agent project**, frame the uncovered rate as the
   approximate containment ceiling. That reframing usually changes the priority of
   KB work from "nice to have" to "prerequisite".

## Troubleshooting

**Coverage looks implausibly high** — check whether `messages.jsonl` was present.
Subject-only matching inflates coverage. Also check that your articles have real
`body` text rather than just titles.

**Coverage looks implausibly low** — your KB may use different vocabulary from your
customers, which is itself a finding (a findability problem). Read the uncovered
samples: if articles clearly exist for them, the issue is wording, and the fix is
adding customer language to titles rather than writing new content.

**Everything is "weak"** — often a KB of very long articles that share a lot of
boilerplate. IDF weighting mitigates this, but a KB where every article contains
the same 500-word footer will still score oddly. Strip boilerplate before export.

**Gap terms are meaningless words** — the stopword list is generic. Add
domain-specific noise words (your product names appear in everything) by
pre-processing the article and message text.

**No gap terms reported** — gaps below 5 conversations are suppressed as noise.
That is either good news or a sign that your uncovered conversations are highly
varied one-offs, which is a different problem from a missing article.
