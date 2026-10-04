---
name: upwork-profile-optimizer
description: Audit and improve an Upwork freelancer profile. Use when the user pastes their profile (title, overview, portfolio list, skills, stats) and wants it scored and fixed, or asks why they aren't getting invitations or search visibility. Triggers include "review my Upwork profile", "why am I not getting invites", "improve my profile", "profile title help", "optimize my overview". Returns a prioritized fix list, biggest lever first. Companion to upwork-proposal-writer (the proposal earns the profile visit; the profile closes it).
---

# Upwork Profile Optimizer

The proposal's only job is to earn a profile visit. The profile does the actual closing, and it also decides search visibility before any proposal is sent: Upwork's AI search ranks freelancers on profile relevance, buyer intent, the client's history, and price fit, and clients can preview the whole profile from search results without clicking through. A half-filled profile loses twice: weaker preview, weaker ranking. Method from Upwork's published guidance plus a Top Rated Plus profile as the worked example.

## Inputs

1. **Title**, exact text.
2. **Overview**, full text.
3. **Portfolio list**: titles and niche of each piece, in their current order.
4. **Skills tags**, as listed.
5. **Stats and badges**: JSS if visible, badge tier, total earnings bracket, response stats.
6. The user's niche and the kind of client they want next. The audit is against that target, not against a generic ideal.

Profile shortcut: if a stored profile file exists (`upwork-profile.md` in the working directory or `~/.claude/`), read it first and audit against it; ask only for sections the file lacks or states vaguely (a rate line that says "ask me" means ask). If a stored profile file and a fresh paste both exist, the paste is ground truth for scoring and the file is background context. Flag any mismatch between the two as a finding.

When tags or stats are missing from both sources, audit what's present now and end by requesting exactly those two. Don't block the audit waiting for them.

## Stage first (do this before scoring anything)

Half of this method is about levers a new freelancer does not have yet. Scoring a profile against them produces a list of failures instead of a fix list, which is useless and discouraging. So establish the stage before auditing, from the stats or by asking one question:

- **No history**: no completed contracts, no reviews, no badge.
- **Early**: some completed work, few reviews, Rising Talent or no badge.
- **Established**: Top Rated or above, JSS visible.

**If the stage is no-history or early, skip section 5 as a scoring dimension.** Do not mark JSS, badge tier, or earnings "missing" or "weak"; they are not weak, they do not exist yet, and saying so is the difference between an audit and a scolding. Audit sections 1 through 4 and 6 in full, since those are entirely within a beginner's control and are the whole game at this stage, then close with the no-history note below instead of the mechanics scoring.

**The no-history close.** State plainly which levers are locked and what unlocks each one, so the user knows what they are working toward rather than what they lack:

- A JSS appears only after enough completed contracts carry feedback. Until then the profile is judged on its content alone, which means sections 1 through 4 carry more weight for a beginner than for anyone else, not less.
- Rising Talent is the first badge and the first real filter a beginner can pass; it is worth naming as the near-term target instead of Top Rated, which is years away.
- The advice that dominates section 5, protect the score by declining bad-fit work, **partly inverts here.** Someone with zero reviews needs their first few completed contracts to exist at all, so the calculus is different: still refuse the scams and the impossible briefs, but a small, clearly-scoped, slightly-underpaid first contract that ends in a genuine 5-star review can be worth more than holding out. Say this as a tradeoff, not as permission to work cheap forever.
- Honesty requirement: this method was extracted from an established Top Rated Plus profile. Where beginner-stage guidance is reasoned inference rather than lived experience, say so in the audit, the same way the skill already flags disagreements between official guidance and field results.

## Audit, in funnel order

### 1. Title (the search surface, 70-character cap)

The proven formula: role + specialty + result or credential ("UI/UX Designer | SaaS Dashboards | Top Rated Plus"). An outcome-led variant works when it's specific (the method author runs "Making Complex Things Simple and Easier to Use"), but it's the advanced move: it trades searchability for memorability, so pair it with skills tags that carry the search load. Instant fails: "Jack of all trades," "Hire me," anything that names no specialty.

### 2. Overview (the pitch, not the resume)

Proof first: open with the strongest credential or outcome in one line ("Top 3% on Upwork, 5+ years in SaaS design"), then two or three concrete outcomes, then tools. Clients scan; the first two lines do the work. A chronology of past jobs is a resume, and nobody hires a resume. Every profile section filled, because search previews expose the gaps.

### 3. Portfolio (the close)

- Lead with the 4 best pieces **matched to the target client**, order is part of the argument.
- Three pieces minimum before expecting invitations at all.
- Niche the portfolio harder than feels comfortable: a logos-only portfolio wins logo work faster than a we-do-everything portfolio wins anything.
- Photo: in focus, high resolution, plain background, an actual photograph (illustrated avatars violate policy).

### 4. The specialist question (be honest with the user here)

Three independent sources in Upwork's own guidance converge on the same claim: clients trust specialists over generalists, in both hiring and search ranking. If the user's profile lists four unrelated service lines, say so plainly and recommend either narrowing or splitting via specialized profiles (separate profile per category, built for exactly this). The one legitimate exception: operators deliberately running an agency-style breadth, who accept weaker search fit as the cost of range. Name the tradeoff, let the user choose it consciously.

### 5. Mechanics (the score behind the score)

- JSS recalculates every two weeks. The private "would you recommend, 1-10" question feeds it alongside the public stars, which is why a politely unhappy client can dent a score without a bad public review.
- The badge ladder (Rising Talent → Top Rated → Top Rated Plus → Expert-Vetted) shows next to every proposal. Protecting it beats decorating it: declining bad-fit work protects the score better than any overview edit, which is the job of the upwork-job-qualifier skill.
- Rate is a signal, not just a price. A rate far below the niche's range reads as a quality warning to exactly the clients worth having.
- Activity feeds visibility: regular logins, proposals, and fast invitation responses (see upwork-invitation-responder; unanswered invites are a visible stat).

### 6. The machine readers (AEO, the layer nobody else audits)

A profile now has three readers, not one: the classic keyword search, Upwork's AI ranking (Uma: relevance, buyer intent, client history, price fit), and, since Upwork's official ChatGPT app, **an LLM synthesizing talent recommendations inside a chat window** where the client never sees the search results page at all. The exact retrieval mechanics are not public; the writing principles that win LLM retrieval are stable anyway:

- **Entity density beats vibes.** Named tools, industries, deliverables, and credentials in natural sentences ("SaaS dashboard design in Figma for fintech clients") are what a model extracts and quotes. Clever positioning language extracts as nothing.
- **This demotes the outcome-led title.** A poetic title works on a human scanning a page; it is nearly invisible to a model matching "find me a [niche] designer." In the AI-search era, the role + specialty + credential formula is no longer just the default, it is the machine-legible option.
- **Answer-shaped first lines.** The overview's opening should literally answer "who is this and what are they best at" in extractable form, which is the proof-first structure already required above; the machine reader just raises the price of getting it wrong.
- **Consistency across surfaces.** Models cross-reference: the title, overview, skills tags, and portfolio piece names should tell one story in the same vocabulary. Contradictions that a human skims past read as noise to a retriever.

Audit note: label this layer honestly when reporting. The principles are sound inference from how LLM retrieval works; nobody outside Upwork has verified the connector's internals, so present it as "the direction the platform is moving," not as measured ranking factors.

## Output format

Score each section strong / weak / missing, then a **prioritized fix list, biggest lever first**, maximum five items, each with the reason in one sentence. Rewrite the title and the overview's first two lines yourself as part of the audit; those two edits move more than everything else combined for most profiles.

## Voice rules (hard)

- Specific rewrites, not adjectives. "Change X to Y because Z," never "make it more compelling."
- No em dashes. Plain words.
- If the profile is already strong, say so and stop. Manufactured critique erodes trust in the real critique.

## Sources and provenance

Worked example: a Top Rated Plus (top 3%) profile. Official guidance, recommended reading:

- 15 Tips To Make Your Freelancer Profile Stand Out: https://www.upwork.com/resources/freelancer-profile-tips
- Freelancer Headlines: https://www.upwork.com/resources/freelancer-headlines
- Designer Profile Tips: https://www.upwork.com/resources/designer-profile-tips
- How To Differentiate Yourself as a Freelancer: https://www.upwork.com/resources/how-to-differentiate-yourself-as-a-freelancer
- Top Rated Freelancer Tips: https://www.upwork.com/resources/top-rated-freelancer-tips
- Upwork's algorithm explainer video (2026), on Upwork's official channel.

This skill is not affiliated with or endorsed by Upwork.
