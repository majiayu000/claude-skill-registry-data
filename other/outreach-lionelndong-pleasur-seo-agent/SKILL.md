---
name: outreach
description: Off-page playbook (Lesson 10, outreach). Turns a vetted link-prospect list into them-focused outreach drafts that earn links without spamming. Picks the RIGHT people (those who LINKED to or MENTIONED our topic — never "people who tweeted it"), gives each a real "excuse" (fresh-angle / new-proof / ego-bait), keeps to ≤1 follow-up, and never makes a pushy link ask. Drafts only — every outward send is operator-gated. Outreach is a tool, not a strategy.
allowed-tools: Read, Write, Edit, Bash, mcp__ahrefs__*
---

# Outreach — the link-earning playbook

> **This is a PLAYBOOK the off-page sub-agent runs, not a live pipeline step,** and it runs only once the off-page phase is open (blogs proven + traffic rising — `STRATEGY.md` "Off-page (later)" + `examples/off-page-subagent-AGENTS.md`). It produces **drafts**; it does **not** send. Every outward-facing message is gated on operator approval (charter guardrails). Outreach is *a tool* in service of links, never the strategy itself (`STRATEGY.md` Lesson 10).

Outreach has a deservedly bad reputation because most of it is spam: a generic template blasted at a scraped list, asking strangers to add a link they get nothing from. We do the opposite. The whole skill is two disciplines: **reach the right person**, and **give them a real reason to care that isn't "please link to me."**

> **Data layer (light): Ahrefs MCP** (`mcp__ahrefs__*`) — used only to identify *linkers/mentioners* and to pull the prospect's context. Read [`../research/references/ahrefs-mcp-cheatsheet.md`](../research/references/ahrefs-mcp-cheatsheet.md) first (string params, `select`+`country`, `doc {tool:"..."}` for unfamiliar tools). The prospect list itself comes from `/linkbuild-competitor-mining`; this skill personalizes and drafts.

> **When to use `/oversubscribed` (Daniel Priestley) — read it before a guest-post / link-demand push (Lesson 9).** When the goal shifts from a single link to **building demand for our guest articles** — a queue of bloggers who *want* to run our content — apply Priestley's demand>supply model (`/oversubscribed`):
> - **Demand > supply ("pitch MORE than you can handle").** Don't pitch one editor and wait; build a *pipeline* of qualified prospects so more sites want our guest post / data study than we can place. The aim is to be **oversubscribed on guest slots** — that's what lets us pick the relevant, on-brand placements and hold standards, instead of begging any site that'll have us. (This rides on, not against, the far-right "fewer people, better" effort rule below — more *qualified* prospects, each still a real, personalized, them-focused note.)
> - **The 7-Hour Rule (~11 educate/entertain touches before any ask).** A cold "will you run my guest post?" converts poorly. Warm the best targets first with **~7 hours / ~11 touches of genuinely useful, no-ask value** (our data studies, benchmarks, useful threads — 80/20 educate/entertain) so that by the time we propose a guest article, they already know and trust the work. **Signal, don't sell** — ask for the signal of interest, not the link.
> - **Products-for-prospects.** Our **data studies / linkable assets ARE the products-for-prospects** — the free, high-value things that build demand and earn the right to pitch. `/linkable-asset` produces them; outreach uses them as the warming touches and the citable hook (this is exactly why **new-proof** is our strongest excuse). 
>
> This is a *lens for the demand-building push*, layered on top of — never replacing — the anti-spam, ≤1-follow-up, operator-gated rules below. More demand does **not** mean more volume of cold asks; it means more *warmed, qualified* prospects who want what we have.

## Input

`/outreach <asset-slug>` — the linkable asset (a data study, a definitive guide, a free tool) we're earning links **for**. Reads:
- `content-pipeline/off-page/link-prospects.csv` — the vetted prospects from `/linkbuild-competitor-mining`.
- The asset itself (`content-pipeline/.../{asset-slug}.md` or the live URL) — so the excuse is grounded in what the asset actually offers.
- `brand-config.md` — our voice/register, the off-page sender identity + reply-to email (the sub-agent's own mailbox — charter §"Its own email"), and the affiliate-suppression note.
- `content-pipeline/off-page/outreach-log.csv` if present — who we've already contacted + when (so we never double-contact and we honor the ≤1-follow-up rule).

## WHO to reach (and who to ignore)

The single biggest determinant of reply rate is **picking people who have already shown they link to / write about this topic.** In priority order:

1. **Linkers** — people who **linked** to a competing/older resource on our topic (straight from `link-prospects.csv`: superfans, power-linkers, fresh-link authors). They have, demonstrably, added a link on this subject before. Highest hit-rate.
2. **Mentioners** — people who **wrote about / mentioned** our topic, a related stat, or an outdated figure, **without** linking to a good source. They've shown topical interest and have an *unfilled* citation slot our asset fills.
   - Find unlinked mentions via Ahrefs `content-explorer` (`doc` it for the current params) for our topic/stat, filtered to pages with few outbound links to sources; or mentions of a now-outdated number our data updates.

**Who we deliberately do NOT reach (anti-pattern):**
- **"People who tweeted/shared it" / pure social engagers.** A like or a tweet is not a link and rarely becomes one — chasing social sharers is low-yield noise (`STRATEGY.md` Lesson 10: reach **linkers and mentioners**, not social sharers).
- Anyone on the **suppression list** (already links to us) or any **affiliate-program** prospect Alex owns — those go through Alex, not cold outreach (charter §"Coordination with Alex").
- Anyone with **no real human / no editorial contact** (the `no_contact` flag) — there's no one to persuade.

## The "excuse" — three templates (why they should care)

Cold outreach only works with a genuine **excuse**: a reason the email is about *them and their page*, not about us. No excuse = spam (`STRATEGY.md` Lesson 10). Pick the template that fits what we actually have for that specific prospect:

1. **Fresh-angle** — *their page is good but misses an angle we cover.* "You cover X thoroughly; the one thing readers still ask is Y — we put together [asset] that answers it, in case it's useful for your readers." Use when our asset adds a sub-topic or perspective their page lacks.
2. **New-proof** — *their page cites an old/weaker stat or no source; we have fresh first-party data.* "You cite [old figure] — we just ran [N] tests / pulled [our own data] and got [updated figure]; sharing in case you want a current number." Use when our **own data / experiment** (a linkable asset — `STRATEGY.md` Lesson 7) updates something they reference. **Strongest excuse in the adult niche** because data is brand-safe and genuinely citable.
3. **Ego-bait** — *we featured / praised them, and we're letting them know.* "We included your [tool/post/quote] in [asset] as one of the best examples of X — thought you'd want to see it." Use when the asset authentically references the prospect (a roundup, a "best of," a methodology that credits them). Never fake the feature — the link must really exist before the email goes out.

Each template is a **starting structure, personalized per prospect** from `competitor_evidence` + `anchor_seen` in the prospect row — never a mail-merge blast. The prospect's *own page* is named and referenced specifically; if you can't say something true and specific about their page, they're the wrong prospect.

## The outreach ↔ spam EFFORT spectrum (the mental model)

The difference between outreach and spam is **effort per recipient**, on a spectrum:

```
SPAM  ◄─────────────────────────────────────────────────────►  OUTREACH
mass-blast,           segmented           one real, specific note per person,
no excuse,            template,           grounded in THEIR page, with a genuine
"please link",        light personal,     excuse, no pushy ask, easy to ignore
nag follow-ups        some excuse         (≤1 gentle follow-up, then stop)
```

We operate at the far-right end **only**. The cost of that is we contact *fewer* people, *better* — which is correct: 10 personalized notes beat 1,000 blasts on both yield and on not torching our sender reputation / the brand. (`STRATEGY.md` anti-pattern #15: spam communities / mass-blast / push for links / nag.)

## Process

1. **Load + segment prospects.** Read `link-prospects.csv`; split into **linkers** (already typed) and go find **mentioners** for `<asset-slug>` (unlinked-mention search above). Drop anything in `outreach-log.csv` (already contacted), the suppression list, `no_contact`, and affiliate-suppressed rows.
2. **Match an excuse per prospect.** For each, pick fresh-angle / new-proof / ego-bait based on the *evidence we actually have* about their page. If none of the three is honestly true for a prospect, **remove them** — no excuse, no email.
3. **Draft, them-focused, one per prospect.** Short (a few sentences). Structure: name their page + one specific true observation about it → the excuse (what we have that's relevant to *them*) → a soft, optional offer ("in case it's useful," "no worries either way"). **No demand to link, no "please add our link," no "let me know by [date]," no fake urgency.** Sign as the off-page sub-agent's identity with its real reply-to mailbox. Make it trivially easy to ignore — that's what keeps it from being spam.
4. **Self-check each draft against the anti-pattern list** (below) before it's eligible to send.
5. **Write drafts to disk for operator approval — do NOT send.** `content-pipeline/off-page/outreach-drafts/{asset-slug}/{prospect-domain}.md`, plus a manifest. The operator (and, per charter, the approval gate) reviews and explicitly approves before *any* message leaves the mailbox.
6. **On approval + after sending (logged by the sub-agent):** record `domain, contact, excuse_type, asset, sent_at, channel` in `outreach-log.csv`.
7. **Follow-up — at most ONE, and only if warranted.** If no reply after ~5–7 days, **one** short, friendly, no-pressure nudge is allowed ("bumping this once in case it slipped by — totally fine to ignore"). **Then stop. Forever.** A second follow-up is nagging = spam (`STRATEGY.md` Lesson 10 "≤1 follow-up"; anti-pattern #15 "nag with follow-ups"). Mark the prospect `closed` either way.

## Output
- `content-pipeline/off-page/outreach-drafts/{asset-slug}/*.md` — one personalized draft per prospect (+ a manifest listing each prospect, excuse type, and the one-line rationale). **Drafts only — operator-gated send.**
- `content-pipeline/off-page/outreach-log.csv` — the contact ledger (who, when, excuse, follow-up status) so we never double-contact and the ≤1-follow-up rule is enforceable.

## Quality checklist
- [ ] Every recipient is a **linker or mentioner** — zero "social sharer / tweeted-it" contacts in the list.
- [ ] Every draft names the prospect's **own page** and says something specific + true about it (no generic openers).
- [ ] Every draft maps to one of the three excuses, and that excuse is **honestly true** for that prospect (ego-bait only when the feature really exists).
- [ ] **No pushy ask** anywhere — no "please link," no deadline, no fake urgency, no "Reply STOP." It's an easy-to-ignore, them-focused note.
- [ ] ≤ 1 follow-up is structurally enforced via `outreach-log.csv`; no prospect can receive a 2nd nudge.
- [ ] No draft is addressed to a suppression-list domain or an affiliate prospect owned by Alex.
- [ ] Nothing is queued to actually send without an operator-approval step recorded.
- [ ] **For a guest-post / link-demand push: the `/oversubscribed` lens is applied — a pipeline of qualified prospects (demand>supply), best targets warmed with ~11 no-ask value touches (7-Hour Rule) before any guest-article ask, and our data studies used as the products-for-prospects — WITHOUT increasing cold-ask volume or breaking the ≤1-follow-up / operator-gate rules.**

## DO / DON'T
**DO**
- Reach **people who linked to / mentioned** the topic (they fill a real citation slot) — `STRATEGY.md` Lesson 10.
- Lead with a genuine **excuse** that's about *their* page; personalize every message.
- Lean on **new-proof** (our own data/experiments) as the primary adult-niche-safe excuse — data is citable where a product pitch isn't.
- Keep it short, soft, easy to ignore; ≤ 1 gentle follow-up, then stop.
- Treat outreach as **a tool that earns links**, measured by opened/clicked/replied → links accrued.

**DON'T**
- Don't mass-blast, don't email without an excuse, don't be pushy, don't nag with a 2nd follow-up (`STRATEGY.md` anti-pattern #15; Lesson 10 DON'Ts).
- Don't chase social sharers / "people who tweeted it" — that's the explicitly-named wrong audience.
- Don't fake an ego-bait feature, fabricate a stat, or invent a contact — if the excuse isn't true, drop the prospect.
- Don't pitch the affiliate program cold — route affiliate-shaped prospects to Alex (charter §"Coordination with Alex").
- Don't send anything without operator approval — this skill **drafts**; the human gate decides.

## Winning =
Messages that get **opened, clicked, and replied to** — and, over time, **links that accrue** (`STRATEGY.md` Lesson 10 "Winning = opened/clicked/replied; links accrue"). Combined with `/linkbuild-competitor-mining`, the off-page wing's whole north star is the same as Lesson 9's: a **steady stream of manual referring domains** that lifts our DR, which unlocks higher-KD keystones — feeding straight back into the on-page strategy's winnability ladder (`STRATEGY.md` §2). Outreach that torches sender reputation or annoys the niche is *negative* progress, even if it lands a link.
