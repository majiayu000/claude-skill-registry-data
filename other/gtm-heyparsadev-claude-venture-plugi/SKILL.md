---
name: gtm
description: This skill should be used when the user asks for go-to-market strategy, positioning, launch planning, channel strategy, pricing strategy, or messaging — e.g. "build a GTM strategy", "how should we launch", "which channels should we use", "positioning for my product", "pricing strategy", "استراتژی ورود به بازار", "گوتومارکت", "پلن لانچ", "از چه کانالی مشتری بیاریم", "قیمت‌گذاری", "پوزیشنینگ". Produces a positioning canvas, messaging house, channel plan, pricing strategy, and launch plan in the venture workspace.
version: 1.0.0
---

# GTM Strategy — Positioning, Channels, Pricing, Launch

Turn "we built something good" into "the right people hear about it, get it, and buy it." Order matters: **positioning → messaging → channels → pricing → launch plan** — each builds on the previous; never start at channels.

## Shared conventions (venture suite)

- **Workspace:** locate `ventures/` in the current working directory (ask once and create if missing). All outputs go to `ventures/<slug>/<NN-module>/`.
- **Templates are read-only.** Files under a skill's `references/` live inside the installed plugin and are shared by every venture. Never write to them. "Fill template X" always means: copy it into `ventures/<slug>/<NN-module>/` under a dated name and fill the copy.
- **Read `VENTURE.md` first.** When done: update its Status table and append key findings to "Key facts & numbers" (format: `- [module, YYYY-MM-DD] finding (source, confidence)`).
- **Language:** converse in the user's language. Write formal deliverables (reports, canvases, battlecards) in the `report_language` set in VENTURE.md. Persian reports keep standard English business terms as-is (TAM, SAM, SOM, CAC, LTV, GTM, churn, retention...).
- **Research integrity:** cite every external claim (source + date). Mark every estimate with confidence (high/med/low). Never fabricate numbers — write "no data found" instead.
- **Chain:** end by updating VENTURE.md and suggesting the logical next module.

## Prerequisites check (do this first)

GTM quality is capped by its inputs. Check VENTURE.md status:
- **competitors not done** → warn: positioning against unknown alternatives is guessing. Offer a quick inline competitive scan (30 min) or full `/venture:competitors` first.
- **market-research not done** → warn: channel/segment choices will be assumption-based. Proceed only if user accepts; mark affected sections `assumption-based` explicitly.
- **PMF weak or unmeasured (for stage launched+)** → say the hard thing: scaling GTM on weak PMF burns money; recommend `/venture:pmf` first. User may still proceed — design a *validation-oriented* GTM (small bets, learning goals) not a scaling one.

Scope with the user: full GTM or one piece (just positioning / just launch plan / just channels)? Each section below stands alone.

## Workflow

### 1. Positioning (April Dunford's 5 steps)

Template: `references/positioning-canvas.md` → fill a copy at `05-gtm/positioning-YYYY-MM-DD.md`.

① Real competitive alternatives (what would customers do without you — often "spreadsheet + secretary") → ② unique attributes you have and they don't → ③ value those attributes enable (so what?) → ④ who cares most about that value (= sharpened ICP) → ⑤ market category to frame it in (existing category = instant comprehension; new category = expensive education — recommend one).

Use as raw material: competitor matrix, PMF fit-segment, customer quotes from discovery (the "very disappointed" users' words are positioning gold).

### 2. Messaging house

Template: `references/messaging-house.md` → fill a copy at `05-gtm/messaging-YYYY-MM-DD.md`.

One promise (roof), 3 pillars with proof points, objection handling. Write in the customers' language (≠ report language, if they differ). No feature-listing: every pillar = customer outcome.

### 3. Channel strategy (Bullseye)

Template: `references/channel-playbook.md` → fill a copy at `05-gtm/channels-YYYY-MM-DD.md`.

Brainstorm wide across the channel menu → score each: ICP presence, expected CAC vs price point, speed-to-signal, fit with founder skills → pick **1–2 core + 1 experimental** (not five). For each: first concrete experiment, budget cap, success metric, kill criterion. Match channel economics to price: a $10/mo product cannot afford founder-led sales; a $20k/yr product can't rely on viral loops.

### 4. Pricing strategy

- Anchor to **value and alternatives** (from positioning ①), not cost-plus.
- Structure: tiers (good/better/best), per-seat vs flat vs usage — recommend with reasoning for this business type.
- If user has customer access: include the 4 Van Westendorp questions (too cheap / cheap / expensive / too expensive) to run in discovery calls.
- Local-market reality: purchasing-power-adjust; note local norms (in Iran: annual upfront billing common, USD-pegged pricing risky — flag such factors for the relevant geography).
- Give a **starting price + rationale + the experiment to test it** (e.g. next 10 sales calls at +30%). State it's a hypothesis: pricing is iterated, not solved.

### 5. Launch plan

Template: `references/launch-checklist.md` → fill a copy at `05-gtm/launch-plan-YYYY-MM-DD.md`.

Pre-launch (audience building, beta list, assets) → launch week (sequenced, owner per item) → post-launch (the launch is a spike; the plan for week 2+ matters more). Calibrate size to reality: a B2B tool's "launch" may be 20 outbound emails — that's fine, say so.

### 6. Metrics & targets

Per channel: leads/signups, activation, CAC. Overall: pipeline or week-over-week growth target. Set **review date** (typically +30d) to revisit with `/venture:review`.

## Output & close

Save as `ventures/<slug>/05-gtm/gtm-strategy-YYYY-MM-DD.md` (or `positioning-YYYY-MM-DD.md` etc. for partial runs) in `report_language`. Update VENTURE.md (status, key facts: positioning one-liner, chosen channels, starting price; new assumptions → riskiest list with test plan). Suggest next: `/venture:model` (pricing feeds unit economics) or `/venture:review` after 30 days of GTM execution.

## Quality bar

- Positioning statement must make a specific person say "that's for me" — if it could fit any product, redo step ②.
- Every channel recommendation carries a cost-bounded experiment with a kill criterion. No "do content marketing" hand-waving.
- The deliverable must be executable by one founder with limited budget unless VENTURE.md says otherwise.
