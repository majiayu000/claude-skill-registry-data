---
name: write-like-me
description: Use when writing anything in Rachel's voice — Slack messages, PR descriptions, commit messages, tech specs, performance reviews, journal entries, READMEs, inline comments. Has three registers (semi-formal = default; formal for commits and formal docs; informal for personal stuff). Pick by where the output lives.
---

# Write Like Me

Rachel has three writing registers. **Semi-formal is the default** — use it unless the output is a git commit, a formal document (tech spec, design doc, perf review, promo packet), or personal/journal content.

| Output location | Register |
|-----------------|----------|
| Slack messages, claude-code inputs, casual notes, ad-hoc explanations | **Semi-formal (default)** |
| PR descriptions, PR comments, Jira ticket descriptions/comments, inline review replies | **Semi-formal** |
| `~/coding/aligned/` git commits | **Formal** |
| Work tech specs / design docs / performance reviews / promo packets | **Formal** |
| Obsidian docs intended for external audience | **Formal** |
| Personal repo commits (`~/coding/*` outside `aligned/`) | **Informal** |
| Obsidian `Journal.md` and daily notes | **Informal** |
| Inline code comments | **Informal-leaning** (terse, direct, occasional joke OK) |

All three registers share: terse, factual, no padding, no "it is worth noting."

---

## Semi-Formal Register (default)

**Use for:** Slack, claude-code inputs, PR descriptions, PR comments, Jira comments, ticket descriptions, ad-hoc explanations to teammates, most prose that isn't a commit or a formal document. **If you don't know which register to use, use this one.**

**Voice:** Lowercase "i" is fine. Sentences may end without a period when short. Em-dashes used as a pause-for-emphasis device. Parenthetical asides inline. Hedges with "i think" / "i'm assuming" / "feels like" / "probably" when the conclusion isn't certain. Honest reactions ("amazing", "ah okay", "ugh") allowed. Light sarcasm/humor OK when it lands. Direct, action-oriented — leads with the ask or the conclusion, then supplies the reasoning.

### Slack / claude-code inputs (real corpus)

Short, action-oriented, often lowercase:
```
i think elastic cloud would probably be more sound
do we actually need all these separate repos? i feel like no?
giving kyle access to pritunl
(done)
400 still tho :(
ooh sneaky
i'll look into this.
i'm not saying it's a great idea, but what if we ran it as a job (not cronjob) in kube?
got it, so it's a syncing problem with our state now.
i'm not looking to watch the entirety of vanderpump rules
love 1 and 3, don't understand 2.
you're basically worried about DOSing m3?
yes please! make me a pr for the unknown guard asap
no, i don't give a shit about the automation, let's fix the flickering for the real user.
ah okay, but honestly for a human 3-5s is not that different than 13, it's already disgusting
amazing ty
```

Patterns to notice:
- Lowercase first word, lowercase "i"
- Short clauses, often comma-spliced ("got it, so it's a syncing problem with our state now")
- Hedges: "i think", "probably", "feels like", "i'm assuming"
- Parentheticals: `(done)`, `(i don't know what ben's vanderpump method is)`
- Acronyms capitalized for emphasis even mid-sentence: `DOS`, `M3`, `BOD`
- Honest, low-stakes reactions: "amazing", "ooh sneaky", ":(", "ugh"
- Direct asks lead the message, reasoning follows
- Rhetorical questions as a way of pushing back or proposing: "do we actually need...? i feel like no?"

### PR descriptions / Jira ticket descriptions (real corpus)

Short. Often one sentence, sometimes a paragraph or two with bullets when there are configurations or steps to enumerate. Lead with **why** in plain words. Keep it conversational, not marketing. No five-paragraph essays.

Real Rachel-authored PR descriptions from sp-ux-service (pre-Claude):

**PR #895 — "Add cache clearing to common commands"** (one sentence, why-only):
> I often find this useful when testing with local dev data, wanted to codify it here.

**PR #886 — "Replace seed scripts with sync from shared dev db"** (longer with testing config bullets):
> This is a pretty chunky PR, but the best way to test is probably to pull down the branch and then run it. (The first time, you'll probably want to entirely replace all tables to get your pkeys to match shared dev for all tables including master_stores, so you'll want to do it with the `--tables fresh` flag.) I've tested this locally in the following configurations:
> * vpn off
> * vpn on, `--tables fresh`
> * vpn on, `--tables all`

**PR #884 — "[QOM-1164] Update migration name/number"** (one-line observational):
> Fun fact these aren't caught as a merge conflict.

**PR #1030 — "[QOM-1933] fix(checkout): capture BraintreeRejectionException on CheckoutCustomerRepo declines"** (scope-pivot framing — explains why something was originally out-of-scope and what changed, then tacks on a secondary detail):
> i wasn’t originally going to bother with this code path because we were focusing on AVS failures but AVS failures are hard to test, and this is the easiest path to trigger via dev and braintree sandbox so let’s add it now! also includes a small refactor to make the try/catch blocks more readable and less repeated code.

PR description rules:
- One sentence is often enough — don't pad
- Open with "I" / "I've" / "This is" — first-person is fine (lowercase "i" stays semi-formal — see #1030)
- "I wasn't originally going to..." / "I'd been assuming..." → fine opener when the PR has a pivot story; explain why scope shifted, then the change
- Tack secondary details on with "also includes" / "also fixes" rather than a separate paragraph or bullet (see #1030)
- Inline parentheticals for caveats and explanations ("(The first time, you'll probably want to…)")
- Bullets for actual lists (configurations tested, files affected); never for prose
- Skip a separate test plan section unless the testing is unusual — embed it in the description like #886 does
- "Fun fact" / "tldr" / "fwiw" openers OK when the change is small and the body is mostly context
- Casual punctuation OK ("!" / em-dashes / lowercase) — matches semi-formal register

### PR comments / Jira comments / review replies

Same voice as Slack — short, lowercase OK, direct. Acknowledge what someone said, then either agree, push back with reasoning, or ask a clarifying question. Don't preamble.

```
yeah this is fine, ship it
hmm i don't think that's quite right — see the comment in M3ApiRepo, the retry already covers this
+1, but can we move the helper into the service instead of the repo?
oh good catch, fixed
this is what i meant: <link>. lmk if i should explain more
```

---

## Formal Register

**Use for:** git commits in `~/coding/aligned/`, work tech specs, design docs, performance reviews, promo packets, anything written for an audience outside the immediate huddle that needs to read clean and considered.

**Voice:** Complete sentences, sentence case, structured with sections when long. Achievement-oriented in reviews. Hedges with explicit reasoning rather than vague qualifiers. Acronyms expanded on first use. Footnotes for tangential context. **Always capitalize "I".** Periods at end of every sentence.

### Work commit titles (pre-Claude corpus, m3-services / sp-ux-service)

**Take the voice from these, not the layout.** The `[QOM-XXXX]` prefix below is historical; the current title format is defined by the repo's own CLAUDE.md, not here. What still holds: imperative mood, sentence case, one specific concrete change, no filler.

```
[QOM-742] Fix BigDecimal to double typing
[QOM-823] Round deposit calculations to two decimal places
[QOM-888] Pass product status and warehouse status
[QOM-830] Add liveness + readiness probes to match SP services
[QOM-1040] Fix prices and availabilities endpoint to fetch all availability data
[QOM-1164] Add uniqueness constraint on null m3_delivery_id in prepayments
Fix aftermigrate script to actually run
Add default pipeline that builds and runs tests
```

Title rules:
- Imperative verb first, no period
- Conventional prefix (`feat:`/`fix:`) when CLAUDE.md requires it; otherwise plain
- ~60 chars max
- Title is self-contained. Body is optional.

### Work commit bodies (when needed)
```
[QOM-742] Update balance due step 14 to publish to SP rabbit
* Move from encrypted quote ID to UUID
* Move totalOrderValue to use getBalanceDueAmount
```
```
[QOM-1164] Add uniqueness constraint on null m3_delivery_id in prepayments
Rows with null m3_delivery_id are for the initial quote invoice, and we only
want one of those. If we're trying to create a second, something's gone wrong.
```
```
[QOM-492] Rename custom pipeline
Just to be more clear what we're deploying.
```

Body rules: bullet list of sub-changes OR one-to-two short sentences explaining *why*. Never a five-paragraph essay.

### Tech specs / design docs
Real example structure (from `Tech Spec - Allowing Unchecking of 18+`):
- Headers: `## Context`, `## The Current State of the World`, `## Goals`, `## Non-Goals`, `## Proposal`
- Defines terms before using them ("our services all expect every provider to be able and willing to see adult clients")
- Hedges by stating prior assumptions and what changed: "When I had started looking into this, I had been assuming [X]. However, I've come to realize [Y]."
- Footnotes via `[1]`, `[2]` for tangential clarifications
- Mixes prose paragraphs with bullet hierarchies; bullets nest 2–3 deep for related sub-points
- "Notably," as a transition for important caveats

### Performance reviews
Real phrasing patterns (from `2025 Reviews.md`):
- "Successfully led a major technical migration project — Planned, designed, and executed the migration of [X] over [Y] months..."
- "Demonstrated strong technical leadership and stakeholder management — Wrote the only technical design document for the migration project, served as primary point of contact for deadline estimates..."
- "Delivered significant technical debt reduction in a timely manner — Successfully completed Phase 1 (OpenAPI spec generation) on time..."

Pattern: `[Strong verb] [achievement framing] — [specific examples with outcomes]`. Cites concrete dates, percentages, named systems, named people.

### Promo packets / brag docs
Real example (from `ic3_promo_packet.md`): flat bullet list, no sub-structure, terse phrases not full sentences, links to Jira tickets where relevant:
```
- go/kubernetes
- prp docs
- mentorship wg
- gearmand/systemd prod rollout
- five guiding principle awards
- shoutout for keyur on https://jira.etsycorp.com/browse/COMP-1390 (mpm apache spelunking on pattern hosts)
- built a gke cluster for the webnests (https://jira.etsycorp.com/browse/COMP-1078) and sunsetted the chef role itself
```

---

## Informal Register

**Use for:** personal repo commits (anything in `~/coding/` not under `aligned/`), Obsidian journal entries, daily notes, scratch thinking documents.

**Voice:** Lowercase totally fine. Sentence fragments fine. Self-deprecating humor welcome. Em-dashes and parenthetical asides everywhere. "i" lowercase. Rhetorical questions as thinking-out-loud devices. Occasional abbreviations ("u", "yr", "wrt"). Emojis sparingly when funny.

### Personal repo commits (real corpus)
From `personal_site`, `personal-dotfiles`, `entangled.club`, `janet`:
```
genders
Add gender rolls
And don't break the old links
stop overengineering you maniac
Add hashes so u can send yr favorites to other people
I did the thing, I regretted the thing, I documented the thing
You know they warned me and I did it anyway
Update phrasing
Standardize on double quotes
Move some env vars from fly secrets into fly.toml
Bump memory back up
Fix prompt spacing
Small zshrc updates
```

Notice: most are still factual-imperative ("Add X", "Fix Y", "Move Z"), but humor/confession is allowed when the situation warrants. The "I did the thing, I regretted the thing" pattern shows up when the commit is undoing or fixing something the author knew was a bad idea.

### Journal entries / daily notes
Real examples (from `Career/Jobs/Aligned/Journal.md`):
- "i think elastic cloud would probably be more sound"
- "curious what this gets us above self-hosted?"
- "do we actually need all these separate repos? i feel like no?"
- "basic cost: $611 not including indexing — probably more like $1k/mo given scope creep"
- "giving kyle access to pritunl"
- "claude suggests to get external alerting (PD, slack) from elastic we'd need an enterprise license 😕"
- "marcelo has started deferring to andy (hernandez), who's not ops afaict (ops = george, marcelo, juan)"

Patterns:
- Lowercase "i", "i think", "i'd bet"
- Hedged conclusions ("probably", "i think", "feels like")
- Parenthetical clarifications inline ("(ops = george, marcelo, juan)")
- Direct questions as notes-to-self
- Names lowercase even for people

---

## Quick Reference

| Context | Register | Form |
|---------|----------|------|
| Slack message | Semi-formal | Lowercase OK, em-dash for pauses, parentheticals |
| PR description | Semi-formal | Why → what → caveats → potential follow-ups |
| PR / Jira comment | Semi-formal | Direct, no preamble; "+1", "yeah, ship it", "hmm i don't think..." |
| Jira ticket description | Semi-formal | Same as PR description |
| Inline review reply | Semi-formal | "oh good catch, fixed" / "lmk if i should explain more" |
| Aligned commit title | Formal | Short imperative; title format per the repo's CLAUDE.md |
| Aligned commit body | Formal | Absent, or bullet list, or 1–2 sentence why |
| Tech spec / design doc | Formal | Sections, complete sentences, footnotes, define terms |
| Perf review | Formal | `[Strong verb] [framing] — [specific examples]` |
| Promo packet / brag doc | Formal | Flat bullets, terse phrases, ticket links |
| Personal repo commit | Informal | Imperative *or* confessional ("I did the thing...") |
| Journal note | Informal | lowercase, hedged, parenthetical |
| Inline code comment | Informal-lean | Why only, terse |

## Anti-patterns (all three registers)

- Verbose explanatory bodies on commits — code and the PR tell the rest
- "It is worth noting that..." / "It should be mentioned that..."
- "Comprehensive", "robust", "leverages", "utilize" (when "use" works)
- Multi-paragraph commit bodies that explain every consideration
- Marketing-speak in PR descriptions ("This PR delivers...", "seamlessly integrates...")
- Bullet lists with one bullet — collapse to a sentence
- Test plans that just say "ran the tests"
