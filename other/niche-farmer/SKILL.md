---
name: niche-farmer
description: Find "boring-monetized" niches for indie hackers — groups already paying for bad solutions — using 6 bulletproof principles (PROVEN PAYMENT, DOLLAR PAIN, REACHABLE AUDIENCE, SCHLEP MOAT, WORKFLOW LOCK-IN, 24-HOUR SALE TEST). Use when the user wants to hunt for a startup idea, find a side project to monetize, validate a niche before building, or asks "what should I build", "find me a niche", "find an idea", "indie hacker ideas", "boring business ideas", or "niche research". Not for brainstorming new features for an existing product.
allowed-tools: WebSearch, WebFetch, Write, AskUserQuestion, Bash, Read, Grep
---

# Niche Farmer

Find niches where people already pay for bad solutions. Not ideation. Hunting.

A niche must pass **5 hard gates**. A 6th gate (24-HOUR SALE TEST) downgrades rather than kills.

| # | Principle | Hard kill test |
|---|-----------|----------------|
| 1 | **PROVEN PAYMENT** — someone already pays for a worse version | Can't name ≥3 existing paid solutions (Fiverr / consulting / old SaaS / Excel templates) → KILL |
| 2 | **DOLLAR PAIN** — pain measurable in $/hours | Can't state "if unsolved, costs $X/month or wastes Y hours" with a cited anchor → KILL |
| 3 | **REACHABLE AUDIENCE** — ≥3 venues with 100+ buyers clustered | Can't name 3 specific subreddits / Discords / associations / trade groups → KILL |
| 4 | **SCHLEP MOAT** — core value is dirty work other builders avoid | Entire product LLM-clonable in a week → KILL |
| 5 | **WORKFLOW LOCK-IN** — migration cost rises each week of use | No accumulating data / integration / habit lock-in → KILL |
| 6 | **24-HOUR SALE TEST** — $1 from a stranger within 60 days (soft gate) | Can't design a 60-day path-to-paid → DOWNGRADE (not kill) |

4/5 hard gates is not "promising." 4/5 is KILLED. No exceptions.

## When to Activate

- "find me a niche" / "what should I build" / "hunt for an idea"
- "indie hacker ideas" / "side project idea" / "boring business idea"
- "validate this niche" / "is there demand for X"
- "find underserved markets" / "who's paying for bad solutions"

Do NOT activate for: feature ideation on an existing product, market sizing (use `market-research`), YC-style office hours on a pre-existing idea (use `office-hours`).

## Intake Phase

Batch ALL intake questions in a SINGLE `AskUserQuestion` call. Do not ask one at a time. If the user invoked with no context, ask all six. If a seed was provided, skip what's already known.

| # | Header | Question | Options |
|---|--------|----------|---------|
| 1 | Mode | "How should I hunt?" | "Cold hunt — no constraints" / "Constrained — I have a domain/audience in mind" / "Validate — pressure-test a specific niche I'll describe" |
| 2 | Domain | "Any domain or audience you want to focus on?" | Free text or "No preference" |
| 3 | Segment | "B2B or B2C?" | "B2B (businesses, pros, operators)" / "B2C (individuals, hobbyists, prosumers)" / "Either" |
| 4 | Geo/Lang | "Geography / language constraint?" | "English global" / "US only" / "EU" / "Specific country" / "Non-English market" / "No constraint" |
| 5 | Skills | "What can you build solo in 2 weeks?" | "Web app" / "Chrome extension" / "AI wrapper/agent" / "Scraper + API" / "Mobile" / "No-code" / "Info product" / "Any" |
| 6 | Budget | "Willingness to spend before first dollar?" | "$0 (scrappy)" / "<$500" / "<$5k" / "Time, not money" |

After intake, restate the hunting brief in 3-4 lines and confirm before running the hunt.

## Hunt Phase

Run searches in parallel. Every claim cites a URL.

### Source → Principle map (ranked by user-voice purity)

Not all sources are equal. A "complaint" on Twitter is 90% performance. A 1-star review on G2 is 90% real pain. The skill ranks evidence by **how likely the author had zero incentive to perform**. Sources where writing takes effort and no one is watching > sources where the author is building a personal brand.

**Core insight:** The biggest lie of indie-hacker source hunting is that the goldmine is r/SaaS, r/Entrepreneur, r/SideProject, Twitter, or Indie Hackers. Those are **founder echo chambers** — people selling to each other. The real goldmine is **vertical pro subs and industry forums** where members don't know the word "indie hacker" — they're just complaining about tools they use every day. Examples: `r/PropertyManagement`, `r/Bookkeeping`, `r/Esthetics`, `r/Veterinary`, `r/Plumbing`, `r/Mortgages`, `r/dentistry`, `r/accounting`, `r/LawFirm`, `r/RealEstate`, `r/HumanResources`.

#### TIER 1 — 90%+ pure (no performance incentive)

Use these as the **primary** evidence for P1/P2/P5. Every QUALIFIED niche needs at least 2 P-signals anchored in a Tier-1 source.

| Source | Why clean | How to hunt |
|--------|-----------|-------------|
| **GitHub Issues** | Writing an issue is pure cost; author gets zero reward | `site:github.com/{repo}/issues "{pain keyword}"` → WebFetch. Filter: `is:issue label:bug OR label:feature-request` with 👍 count ≥ 3 |
| **App Store 1-3★ reviews** (iOS) | User paid money and is still angry = real pain, quantified spend | `site:apps.apple.com {app}` → WebFetch review page; extract 1-3★ with ≥200 chars |
| **Google Play low-star reviews** | Same — money-in-hand + still angry | `site:play.google.com/store/apps {app}` → WebFetch; filter low-star |
| **G2 / Capterra 1-2★ reviews** | B2B user paying $X/seat and writing a long negative = quantified pain | `site:g2.com/products/{slug}/reviews` / `site:capterra.com/p/{id}/reviews` → WebFetch |
| **Trustpilot long negatives (≥200 chars)** | 200-word rant = real pain, not performance | `site:trustpilot.com/review/{domain}` → WebFetch; filter 1-2★ long-form |
| **Stack Overflow bountied unanswered** | User spent reputation → unmet technical need | `site:stackoverflow.com {tag} "bounty"` + no accepted answer |
| **Upwork repeat-gig listings with budgets** | Real money moving to humans for the same task = demand proven | `site:upwork.com {task}` → count open jobs + sum budgets |
| **Chrome Web Store / Shopify App Store / Notion Marketplace 1-2★** | Paid user + still negative | `site:chromewebstore.google.com` / `site:apps.shopify.com` / `site:notion.so/marketplace` → WebFetch review pages |

#### TIER 2 — 50-80% pure (filter needed)

Use as secondary corroboration, not primary evidence. Prefer **deep comments over top-level posts** because comments are cheaper to write and less branded.

| Source | Note + hunt pattern |
|--------|----------------------|
| **Reddit comments in vertical pro subs** | Members don't know what "indie hacker" means — they just vent. `site:reddit.com/r/{vertical-pro-sub} "I hate" OR "wish" OR "every week"`. Read comments **under** top posts, not the posts. |
| **YouTube comments on "best X tool" videos** | Comments under tool-review videos often say "tried X, still wish it did Y" | `site:youtube.com "{incumbent} review" OR "best {category} tool"` → WebFetch top videos → scan comments |
| **Hacker News comments (not Show HN posts)** | Comment section is 10× more honest than submissions. `site:news.ycombinator.com {domain}` → WebFetch thread → comments with ≥3 children |
| **Substack paid-newsletter comments** | Paying audience = high-quality signal | `site:substack.com "{domain}"` → WebFetch; read comments on tool-coverage posts |
| **Discord help/support channels** | Private + asking for help = real unmet need. **Not auto-crawlable** — use P3 user-supplied fallback; ask user to paste pain-rich quotes |

#### TIER 3 — <30% pure (mostly marketing/performance — AVOID)

Do **not** use as primary evidence. If a niche's only support comes from these sources, it's KILLED on P1. If cited at all, flag as `[TIER-3]` in `shortlist.md`.

| Source | Why dirty |
|--------|-----------|
| Reddit top-level posts in meta-subs (r/SaaS, r/Entrepreneur, r/SideProject, r/startups) | 30%+ is founder shilling + SEO; another 30% is ideation theater |
| Twitter / X | 90% performative. "I wish there was" = building personal brand, not paying |
| LinkedIn posts | ~100% performative |
| Indie Hackers *posts* (the comments can be OK) | Founders plugging each other; selection bias toward "I'm shipping!" |
| Product Hunt | 100% launch marketing. "Looks amazing!" ≠ will pay |
| Medium / dev.to listicles | SEO-farmed "top 10 tools for X" content |
| Quora | Overrun with AI slop |
| Any "Alternatives to X" marketing page | SEO-bait, often paid placement |

Use Twitter/LinkedIn/ProductHunt only for **tertiary confirmation** of a specific claim (e.g., you already have Tier-1 evidence and want one more data point). Never as the anchor.

#### TIER 1/2 Chinese-market sources

Activate when intake specifies non-English market OR user requests 中文. Same purity tiering applies.

**TIER 1:**
| Source | Why clean | Hunt pattern |
|--------|-----------|--------------|
| App Store 中区 / 酷安 1-3★ | Paid + angry | `site:coolapk.com {app}` → WebFetch; 苹果中区 via iTunes RSS |
| GitHub Issues on Chinese-maintainer repos | Same purity as EN | `site:github.com {repo} is:issue` + 中文 keyword |
| V2EX 吐槽 / 求助帖 | Dev community, low performance incentive in `/t/` threads | `site:v2ex.com/t "{domain}" ("吐槽" OR "求助" OR "替代")` |
| 小众软件 / 少数派 tool-review long comments | Long-form negatives under tool reviews | `site:appinn.com {tool}` / `site:sspai.com {tool}` → read comments, not post |

**TIER 2:**
| Source | Note |
|--------|------|
| 知乎 长负面回答 (≥500 字 且反对多) | Long contrarian answers are real; short vote-farming answers are noise. Filter: `site:zhihu.com "{domain}"` → WebFetch → answers with ≥500 chars and clearly negative |
| B 站 视频评论区 "最好的 {category} 工具" | Comments under tool-review videos | `site:bilibili.com "{category} 工具 对比"` → WebFetch → comments |
| 豆瓣小组 (vertical interest groups) | Members are enthusiasts, not founders | `site:douban.com/group "{niche}"` |

**TIER 3 (AVOID):** 小红书 planted posts, 即刻 founder circle, 36Kr / 虎嗅 (全是 PR 稿), 脉脉 职场表演, 微博 大V 营销.

### WebFetch depth pass

For each promising hit, WebFetch the actual thread/review and extract **verbatim quotes** (no paraphrasing) for:

- Pain expressions ("I hate that I have to...")
- Payment evidence ("we pay $X/mo for...", "I've been paying $X/job on Fiverr for...")
- Hour/cost quantification ("takes me 6 hours every Monday", "costs us $800/mo for two seats")
- Community URLs + approx member count

### Hunt execution

Per candidate niche: 3-7 parallel `WebSearch` calls → 2-4 `WebFetch` calls on highest-signal pages → extract evidence → score → log → next.

### P3 community fallback (user-supplied venues)

Discord, Slack, and closed Facebook Groups are not publicly indexed — `WebSearch` cannot verify them. If WebSearch cannot produce ≥3 qualifying community URLs with buyer-density evidence for a candidate niche, **pause and ask the user** via a single `AskUserQuestion` call:

> "I found {0|1|2} public venues for this niche. Can you name Discord servers, Slack workspaces, FB groups, or private forums where ≥100 buyers cluster? (One venue per line. If none you know of, this niche fails P3 and will be killed.)"

Rules:
- User-supplied venues count toward P3 only if the user confirms buyer density (not just "members").
- The skill still records the community URL in `shortlist.md` but marks `[USER-SUPPLIED]` alongside it for audit.
- If the user can name fewer than 3 after search + prompt → **P3 = 0 → KILLED**. No exceptions.

## Scoring Rubric

### Five hard gates (each scored 0 or 1)

| Gate | 1 if… | 0 if… |
|------|-------|-------|
| **P1 PROVEN PAYMENT** | Named ≥3 existing paid solutions with URLs (Fiverr / SaaS / consulting / Excel template store) | Fewer than 3, or only aspirational ("I wish") |
| **P2 DOLLAR PAIN** | Wrote the sentence "If unsolved, costs $X/month or wastes Y hours" with a cited anchor (e.g., "3 Reddit users report 4-8 hrs/week on this") | Pain is vague, unquantified, or only emotional |
| **P3 REACHABLE AUDIENCE** | Named ≥3 specific venues with URL + ~member count ≥ 100 buyers each (not 100 visitors — 100 *buyers*). Auto-hunted via Tier-1 sources; if <3 found, fallback to user-supplied Discord/Slack/FB via AskUserQuestion (see P3 community fallback). | Still <3 after search + user prompt, or venues are broad consumer spaces |
| **P4 SCHLEP MOAT** | Core value requires dirty work an LLM-in-a-weekend can't replicate: weird API integrations, data labeling, compliance lift, domain ontology, manual intake, human-verified data, relationship moats | Pure LLM wrapper / prompt / standard CRUD |
| **P5 WORKFLOW LOCK-IN** | Named a specific lock-in mechanism: accumulating data (history, records, templates), deep integrations (calendar, inbox, git), habit formation (daily ritual), team/social adoption, proprietary workflow artifacts | Use-once-and-done; no compounding artifact |

**Sum must equal 5.** 4/5 → KILLED. 5/5 → QUALIFIED (subject to soft gate below).

### Soft gate (downgrade, not kill)

| Gate | Pass | Fail |
|------|------|------|
| **P6 24-HOUR SALE TEST** | You can sketch a concrete 60-day path-to-paid: specific channel → specific offer → specific price → realistic % → first $1 inside 60 days from a stranger | Only "build audience first, monetize later" — DOWNGRADE to secondary shortlist |

### Secondary scores (0-5 each; rank within the 5/5 QUALIFIED set)

| Dimension | Notes |
|-----------|-------|
| Paid-demand strength | ($/customer) × (plausible reachable n). Cite the anchor. |
| Community accessibility | Can you reach them without ads? Posting rules allow builders? |
| Build feasibility | MVP shippable in ≤2 weeks by a solo dev with the stated skills? |
| Schlep depth | How ugly is the dirty work? Uglier = better moat. |
| Lock-in strength | How many weeks of use before switching is painful? |

### Anti-signal flags (any one → KILLED regardless of 5/5)

- Requires VC-scale capital (marketplace liquidity, hardware, field sales)
- Regulated (HIPAA / FINRA / ITAR) beyond a weekend of due diligence
- Network effects required to deliver value on day one
- B2B enterprise with procurement cycles (>$5k ACV with security review)
- Depends on future behavior change ("once everyone adopts X...")
- Incumbent is free + ad-funded and good enough
- Incumbent is a FAANG-owned feature (they'll squash you)

## Anti-Patterns (Kill List)

Kill immediately if the pitch contains:

- "It would be cool if..." — nobody's paying (P1 fail)
- "I wish there was..." — aspiration, not demand (P1 fail)
- "People would love..." — speculation
- "A better [huge consumer app]" — needs education + scale (P3 fail)
- "AI for [general population]" — undifferentiated, zero distribution (P3, P4 fail)
- "A platform where..." — marketplace, chicken-and-egg
- "Like X but for Y" without evidence Y pays (P1 fail)
- "Once we get to scale..." — no viable wedge (P6 fail)
- "Pure LLM wrapper that just formats X prettier" — LLM-clonable (P4 fail)
- "Use-it-once utility" — no lock-in (P5 fail)
- "I'll build an audience first and monetize later" — P6 downgrade, move to secondary shortlist
- Founder has the problem but can't name one community of others with it (P3 fail)

## Iteration Loop

Per session, hunt N candidate niches (default 8; user overrides via `Iterations: N`).

Each iteration:

1. **Pick** next unexplored angle from intake + prior learnings
2. **Hunt** — parallel searches per Source map
3. **Extract** — verbatim quotes with URLs
4. **Score** — 5 hard gates + soft gate + secondary dims + anti-signals
5. **Classify**
   - **QUALIFIED**: 5/5 + P6 pass + no anti-signals + secondary ≥ 15/25
   - **QUALIFIED-DOWNGRADED**: 5/5 + P6 fail + no anti-signals → secondary shortlist
   - **DEEPER**: 4.5/5 (one gate weak, not zero) → one more targeted search before verdict
   - **KILLED**: anything else
6. **Log** to `candidates.tsv`
7. **Compound** — killed niches: extract the *pattern* that killed them into `killed.md` so next session skips similar duds

Stop when: N iterations hit, OR 3+ QUALIFIED found, OR user interrupt.

### TSV schema (`candidates.tsv`)

```
iteration	slug	segment	community	incumbent	price_anchor	p1	p2	p3	p4	p5	p6	paid	access	feas	schlep	lockin	verdict	kill_reason	url_evidence
```

One row per niche hunted. `url_evidence` = pipe-separated top-3 source URLs.

## Output Artifacts

All under `~/.claude/niches/{YYMMDD}-{HHMM}-{hunt-slug}/`:

### Required

- `shortlist.md` — top 3-5 QUALIFIED niches, one page each (template below)
- `secondary.md` — QUALIFIED-DOWNGRADED niches (5/5 hard gates but P6 soft-fail)
- `candidates.tsv` — every niche hunted, with scores
- `killed.md` — KILLED niches with pattern-level lessons
- `go-to-market.md` — generated for the #1 QUALIFIED pick: 3-day MVP scope + 24-hour sale test plan + pricing anchor

### Optional

- `raw-evidence.md` — verbatim quotes, URL-tagged (audit trail)

### Directory setup

```bash
STAMP=$(date +%y%m%d-%H%M)
SLUG={hunt-slug}
mkdir -p ~/.claude/niches/${STAMP}-${SLUG}
```

## One-Pager Template (per QUALIFIED niche in `shortlist.md`)

```markdown
## {Niche name}

**Pain (one-sentence, quantified):** "I hate that I have to {X} every {Y} — it costs me ${Z}/month or {N} hours/week."
*Source: [verbatim-quote URL]*

**Who feels it (tight ICP):**
- Role: {e.g., Shopify store operator}
- Industry: {e.g., DTC apparel}
- Size: {e.g., $100k-1M GMV}
- Geography: {e.g., US + CA}

---

### P1 PROVEN PAYMENT — ≥3 existing paid solutions
- {Incumbent A — SaaS}: {price} — [link]
- {Incumbent B — Fiverr/Upwork gig}: {price per job, order count} — [link]
- {Incumbent C — consultant/agency or Excel template}: {price} — [link]

### P2 DOLLAR PAIN — quantified
- "${Z}/month lost" or "{N} hours/week wasted" — anchored to: [source]

### P3 REACHABLE AUDIENCE — ≥3 venues with 100+ buyers
- {Community 1 URL} — ~{N} members — buyer-density evidence: [link]
- {Community 2 URL} — ~{N} members — [link]
- {Community 3 URL} — ~{N} members — [link]

### P4 SCHLEP MOAT — what's the dirty work?
{Specific dirty work: e.g., "scraping and normalizing 40 weird supplier APIs that each break monthly", or "manually verifying every listing against a trademark database", or "maintaining a domain ontology of 2,000 weird SKUs"}
*Why an LLM-in-a-weekend clone fails:* {reason}

### P5 WORKFLOW LOCK-IN — what accumulates?
{Specific lock-in: e.g., "user's 12-month reconciliation history", "deep Shopify webhook integration", "team-shared templates", "daily morning ritual"}
*Migration cost after 3 months of use:* {concrete description}

### P6 24-HOUR SALE TEST
- Channel: {specific post/DM/cold-email channel}
- Offer: {what the stranger gets}
- Price: ${X}
- Path-to-$1 in 60 days? {Yes / No — if No, this niche goes to secondary.md}

---

**Competing bad solutions (with links):**
- {Name}: why it's bad — [1-star reviews link]
- {Name}: why it's bad — [link]

**Why indie-fit:**
- Buildable in {N} days with {stack}
- No enterprise sales (self-serve ≤${X} ACV)
- No network effects needed for day-1 value
- No regulated workflow

**Kill condition (what disproves this?):**
- e.g., "If >60% of 1-star reviews cite pricing not function, buyers are price-sensitive not pain-sensitive."
- e.g., "If target subreddit mods ban all tool promotion, acquisition collapses."

**First 10 customers plan (no ads):**
1. {Specific post in {specific community} on day 1}
2. {DM N writers of the source complaint quotes}
3. {Cold email N Upwork job posters with an offer}
4. {...}
```

## Go-to-Market (for #1 pick only, in `go-to-market.md`)

```markdown
## {Niche} — 3-Day MVP + 24-Hour Sale Test

### 3-day MVP scope (actually 3 days)
- Day 1: {core loop — ingest + transform, the schlep part}
- Day 2: {UI shell + auth + Stripe + the one lock-in hook}
- Day 3: {polish + deploy + landing page}
Cut ruthlessly. No dashboards. No teams. No extra integrations.

### Pricing anchor
- ${X}/mo or ${X}/job — matches current Fiverr / incumbent spend
- Free tier: none (paying customers are the point)
- First 10: ${X} lifetime deal or 50% off year one (for testimonials)

### 24-Hour Sale Test (Principle 6)
**Goal:** First $1 from a stranger within 60 days.

Week 1 (build + pre-sell):
- Day 1-3: ship MVP
- Day 4: post in {specific community} with free-tier + paid upgrade
- Day 5-7: DM {N} people who wrote the source pain quotes

Week 2-4:
- Cold email {N} Upwork job posters who posted this task in last 30 days
- Guest post / AMA in {community}
- Comment (not spam) on {specific Reddit threads} with a free-tool version

Week 5-8:
- SEO page for "{incumbent} alternative"
- Weekly retro: did anyone pay? If no in 60 days → kill and return to shortlist #2

### Kill date
No paying customer by day 60 → archive this niche to `killed.md`, move to shortlist #2.
```

## Quality Gate (before delivery)

Run this checklist. Any fail → do not deliver; fix and re-hunt.

- [ ] Every P1 claim names ≥3 existing paid solutions with URLs
- [ ] Every P2 claim has a $ or hour anchor cited, not invented
- [ ] Every P3 claim names ≥3 specific venues with URL + buyer-count estimate (auto-hunted + any `[USER-SUPPLIED]` tagged for audit)
- [ ] Every P4 claim describes dirty work an LLM can't weekend-clone, with a reason
- [ ] Every P5 claim names a specific lock-in mechanism (data / integration / habit / artifact)
- [ ] P6 sketch exists — specific channel + offer + price + 60-day plan
- [ ] **At least 2 of the 5 P-signals are anchored in a TIER-1 source** (GitHub Issues / App Store / G2 / Trustpilot / Stack Overflow bountied / Upwork budgets). Tier-3-only evidence → niche is KILLED.
- [ ] No QUALIFIED niche sources only from r/SaaS / r/Entrepreneur / Twitter / LinkedIn / ProductHunt / IH posts (founder echo chambers — see Tier 3)
- [ ] Reddit evidence comes from **vertical pro subs** (r/PropertyManagement, r/Bookkeeping, r/Esthetics, r/Veterinary, etc.) — not meta founder subs
- [ ] No 4/5 niches sneaking through as "promising"
- [ ] Anti-pattern checklist run — no "wish there was", no LLM-wrapper, no use-once utility, no VC-scale bets
- [ ] 3-day MVP scope is actually 3 days (no "and also integrations with...")
- [ ] Price anchor is a real number from a real competitor/Fiverr gig
- [ ] `killed.md` captures patterns, not just rejections (so next session compounds)
- [ ] `secondary.md` holds 5/5 hard + P6-fail niches (downgraded, not discarded)

## Voice

- Direct. No filler. No "as an AI..." No "it's worth noting..."
- Decision-oriented: every section ends in a verdict or a next step.
- Evidence-first: quotes with URLs beat summaries.
- Small numbers beat big numbers. "50 people on r/X paying $30/mo" beats "$2B TAM."
- Kill more than you keep. A good session is often 1 QUALIFIED + 1 DOWNGRADED + 6 KILLED.
