---
name: content-creation
description: Use when producing content for a public channel (a post, a thread, a video, a newsletter, a talk) starting from work that was actually done rather than from a topic.
---

# content-creation

Business layer (`business/README.md`), communication. Pairs with `business/social-publishing`, which
owns the approval and the act of publishing; this block owns whether the thing is worth publishing.

The starting point is the part templates can't supply: **relevance comes from having done something.**
A generated post about a topic reads like every other generated post about that topic, and the reader
can tell. What can't be generated is the number you measured, the trap you fell into, the reason you
rejected the obvious approach.

Which is convenient, because the dev pipeline already produces that material and then throws it away.

## When
When a channel needs content and someone is about to start from a topic or a calendar slot; when a
piece of work finishes and might be worth telling; when repurposing something that already exists.

## Steps

### 1. Decide what we're credible about
1. **List what we've actually done** — shipped, measured, migrated, broken and fixed. That list is the
   editorial line; everything else is commentary anyone could write.
2. **Say who it's for**, specifically: developers on the same stack, technical buyers, candidates. These
   want different things and the same piece rarely serves two.
3. **Name what we don't post about.** Client work without written permission, anything the security or
   legal owner hasn't cleared, and predictions about a market we don't operate in.
4. **A piece nobody on the team would want to read is not fixed by better distribution.**

### 2. Mine the work already done, don't invent a topic
The pipeline's own artefacts are the raw material, and they're already written and already accurate:

| Already exists | Becomes |
|---|---|
| An ADR (`skills/documentation-adr`) | the post people search for: the alternatives and why they lost |
| A release note (`business/release-communication`) | the announcement, and a short demo of the thing working |
| An incident follow-up (`business/incident-communication`) | the highest-trust content available — if its owner approves |
| A measurement (`skills/webperf`) | a numbers post, published **with** the measurement conditions |
| A migration or an upgrade | the write-up that didn't exist when you needed it |
| A rejected approach (`skills/over-engineering-review`) | "why we deleted it", which is rarer and better than "why we built it" |

1. **Start from the artefact, not from a blank page.** The facts are already checked.
2. **Strip what's internal** before anything else: project names, client names, infrastructure,
   colleagues (rule C, `CONVENTIONS.md`). If the story doesn't survive that, it isn't publishable.
3. **Keep the specific detail** — that's the whole value. A generic version of a specific story is worth
   less than not posting.

### 3. Make it worth someone's time
1. **One idea per piece.** Two ideas means neither lands, and the piece can't be titled honestly.
2. **The first line earns the second.** Say what the reader gets, then deliver it. On most networks the
   first line is also the whole preview.
3. **Show the failure, not only the result.** The wrong turn is the part with information in it, and the
   part nobody else publishes.
4. **Concrete beats adjectives**: the number, the error message, the ten lines of code.
5. **A hook is a promise the piece has to keep.** Where honesty stops: a number you didn't measure, a
   story that didn't happen, manufactured outrage, fake vulnerability, and "comment to get the link".
   Those borrow attention against future trust, and the audience worth having notices first.
6. **If a person's name is on it, that person read it.** Publishing generated text under someone's byline
   without them reading it is the fastest way to lose the credibility this block exists to build.
7. **Editing is where it gets good.** Cut a third. The cut third is almost always the introduction.
8. **Read the draft for machine-writing tells** with `business/ai-prose-tells`: clusters, not single words,
   and a rewrite never adds a fact.

### 4. Adapt per network without diluting
1. **Write the substance once**, then re-hook per network (`social-publishing` §2). Same claim, different
   opening and length.
2. **Format mechanics — character sweet spots, whether links are penalised, thumbnail and title
   conventions, aspect ratios — are volatile and community-observed**, not written in any platform's
   documentation. They live in `references/social-platforms.md`, dated, and get re-checked rather than
   remembered (`skills/source-freshness`).
3. **Never let the format flatten the point.** If a network can't carry the idea, publish it where it fits
   and link to it from there.
4. **Native beats cross-posted.** A reformatted post that nobody re-read is where the internal codename
   and the broken link ship.

### 5. Cadence that survives
1. **A rhythm you can hold beats a burst.** Three months of silence after a launch reads as a company that
   stopped.
2. **Batch from one piece of work**: one migration can carry a long-form write-up, a thread, a short video
   and a talk abstract. That's four pieces from one set of facts, all true.
3. **Keep an idea list** fed from finished work, so nobody starts from a blank calendar slot.
4. **Drop what doesn't work.** A channel nobody on the team wants to write for will not survive being
   scheduled.

### 6. Hand off to publish
Everything produced here goes through `business/social-publishing`: named owner, human approval of the
exact content, alt text and captions, media and personal data cleared, links checked logged out. Claims
about the product go through `business/product-marketing` §2 first — every factual claim carries a source.

### 7. Deeper material

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Content trusted by readers and by search engines: people-first, visible expertise, sources, dates, generated and scaled content, link labelling | the piece lives on a page meant to be found through search, or a page's editorial quality is audited | [`01-search-and-trust.md`](./references/01-search-and-trust.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: the piece traced to real work, internal detail
stripped, one idea with a hook the piece keeps, every number carrying its measurement, and a named human
who read it before it goes to `social-publishing`.

## Guardrails
- **Never invent a number, a story, a customer or a result.** This is `default = failure` outside code:
  no source, it doesn't ship (`business/product-marketing` §2).
- **Never publish client or employer work without written permission**, and never internal names, code or
  infrastructure detail.
- **Never publish generated text under a person's byline they haven't read.**
- **Never use engagement bait**, and never manufacture a conflict for reach.
- Never post an incident story before the affected customers have been told and the owner has approved.
- **Never publish generated text nobody fact-checked**, including its title, description and alt text
  (`references/01-search-and-trust.md` §1.12).
- This block doesn't own brand voice or campaign strategy. Where someone does, they decide.

## Origin
Reviewed for this: an MIT open-source marketing skill collection (34 skills — SEO, content writing,
repurposing, thread writing, per-network content, ads, analytics; API keys all optional), a LinkedIn
growth skill set (hook reverse-engineering, re-hooking content from another platform, publishing cadence),
a YouTube creator skill set (retention scripts, hooks, thumbnail briefs, Shorts, channel audits), and
several repurposing skills that fan one artefact out into many formats. The **repurposing insight is taken**
— one piece of source material legitimately becomes several — as is the observation that per-network work
differs mainly in hook and length.

Two things they don't have, and both are the point of this block: **no mechanism for reviewing or
fact-checking a claim before it ships**, and no notion of where the material should come from — they start
from a topic. Ours: start from the artefact the dev pipeline already produced (§2 is a mentis-specific
table), the line where a hook stops being honest (§3.5), and the byline rule. Verified 2026-08-06.

Widened 2026-10-02: `references/01-search-and-trust.md` restates, as editorial questions and habits, the
public guidance of a search provider (helpful, reliable, people-first content; spam policies on keyword
stuffing, scaled content abuse and link schemes; the page on generative AI content; qualifying outbound
links), all read on 2026-10-02. The documentation text is licensed for reuse with attribution; none is
copied, and no ranking factor or number is stated. The owner's direction that the framework serves more
than one agent harness is why this editorial material, earlier set aside as out of scope, is now written.
