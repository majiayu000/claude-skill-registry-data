---
name: regen-investor-deck
description: >
  Build or update a ReGen Civics venture-lane pitch deck (.pptx). Wraps the
  pptx skill with ReGen voice, the v1.2 lane rules, slide architecture, and
  the canonical company narrative: ReGen Civics sells outcomes, gives its
  tools away, and connects land projects into a network. Pulls numbers only
  from the admin metrics table. Triggers on: "investor deck", "pitch deck",
  "pptx for investors", "update the deck", "accelerator deck", "pitch
  presentation", "investor presentation", "deck for the raise", or any
  request to build, update, or convert content into a pitch presentation.
---

# ReGen Civics Investor Deck

## What this skill does

Produce or update a pitch deck that holds together when Rye walks into a
room with accelerator reviewers, pre-seed investors, or angels. The deck
pitches ReGen Civics, the company: open tools, AI-assisted services, the
network of land projects, and revenue that comes from outcomes. It has to be
legible to venture investors without losing the soul of the project.

It never pitches the cooperative, a fund, or land projects as something to
put money into. That is the rule this skill exists to hold (see "The lane
rules" below).

Always invoke the `pptx` skill before starting; this skill builds on top
of it for the slide construction and asset wiring. Never use python-pptx
directly without reading `~/.claude/skills/pptx/SKILL.md` first. For the
plan's main venture deck (11 slides, `docs/private/FUNDING_ENGINE_PLAN.md`
section 6), fold the 14 slides below the way that section lays out.

## The canonical 14-slide deck

This is the default architecture. Cut slides for shorter formats; rarely
add slides without strong reason.

| #  | Slide                         | Single goal                                                 |
| -- | ----------------------------- | ----------------------------------------------------------- |
| 1  | Cover                         | Brand presence, name, tagline, one image                   |
| 2  | The opening                   | One specific, current observation that sets the table       |
| 3  | The problem we're addressing  | Land projects die of structure, not soil                    |
| 4  | The frame                     | Open tools, paid outcomes: what we give away, what we earn  |
| 5  | What ReGen Civics is          | Plain-language summary: tools, services, network            |
| 6  | The business model            | Outcome-based revenue lines, labelled where counsel is open |
| 7  | The game                      | Quests, seasons, citizenship tiers, why this finds a project its people |
| 8  | The infrastructure            | Coordination infrastructure and incentive design            |
| 9  | Traction                      | Numbers from the metrics table, each with a timeframe       |
| 10 | The pipeline                  | Land projects in flight + the incubator cohort              |
| 11 | Team                          | Rye, contributors, advisors, key collaborations            |
| 12 | The ask                       | What you want from this program or investor, and what it buys |
| 13 | Use of funds                  | Where the company's raise goes                              |
| 14 | Close + contact               | One sentence, calendar link, email                          |

For a 10-slide variant, fold:
- 4 + 5 → "What it is"
- 6 + 7 + 8 → "How it works"
- 12 + 13 → "The ask + use of funds"

For a 5-slide "elevator deck," keep: cover, what it is, traction,
the ask, contact.

Appendix slides (optional): the company and cooperative diagram, the nine
forms of capital with a stacked bar from a real project, a diligence sample,
the architecture. The cooperative appears only there, and only in COOP's
words.

## The lane rules (v1.2, binding)

`docs/private/FUNDING_ENGINE_PLAN.md` section 1.5 splits the pitch into
lanes and says never mix them. This skill is the venture lane.

- **Venture lane:** pitch ReGen Civics (the company): tools, services,
  network, outcome-based revenue, network effects, structures built not to
  collapse.
- **The cooperative:** describe it only with the fields of `COOP` in
  `shared/fund.ts`, verbatim: `COOP.statement` for what it is and where it
  stands, `COOP.designPrinciples` introduced by `COOP.designPrinciplesNote`,
  and `COOP.notAnOffer` once on any slide that mentions it. It is in design,
  it is not a legal entity, and it accepts no money. Never use the present
  tense about its members, land, votes or terms. It is not part of the ask.
- **Grants and foundations:** a narrative, not a deck. Use the answer bank.
- **Nine forms of capital,** never eight: financial, material, living,
  intellectual, experiential, social, cultural, spiritual, health
  (`shared/capitals.ts`).
- **Crowdpooling,** when it appears, uses the binding wording: "Crowdpooling
  coordinates and accounts for what people bring to land projects: time,
  things, skills, land and money. Money goes through outside partners each
  project holds, never through ReGen Civics."

Never say, on any slide, in speaker notes or in a caption (Gate G5, and
`node scripts/check-fund-claims.mjs` checks this file for it):
<!-- fund-claims-allow: this line names the G5-banned phrases so agents can avoid them -->
returns of any kind, IRR, ROI, yield, token appreciation, "value grows", distributions or dividends, exchange listings, token prices, "index fund", portfolio, "invest in land projects through us", direct investment, accredited investors, minimums, carry, preferred return, management fees, LPs, Fund I or II.

## Voice rules for investor decks

These ride on top of the project Writing Rules. Investor-deck specific:

- **Numbers do most of the work.** Investors trust quantification. Every
  number comes from the admin `metrics` table with its source (Gate G4).
  Where we don't have one, say "directional, not audited."
- **Don't defend the regen frame.** Skeptical investors are reading;
  pretending they aren't is a tell. Better: "Here's why land projects built
  on these structures last, and how we earn when they do."
- **Honesty about stage.** Early revenue. First seasons. A cooperative still
  in design. Real numbers but small numbers. Frame it as "early access" not
  "we're huge."
- **Tokens stay out of mainstream decks.** Describe that layer as "incentive
  design" and "coordination infrastructure" (plan section 1.5). In a web3
  variant, show the Game's tokens ($ReGen, RGVoice); $RCivics and RCVoice
  appear only as `COOP.coopTokens` says.
- **No "regenerative renaissance" buzzword stack on slide 2.** Earn it
  by slide 5 or 6. Investors who don't speak movement-language will
  bounce off a buzzword wall.
- **Em-dashes banned. Project rule.**

## Slide-by-slide guidance

### Slide 1: Cover

- Logo (top-left or centered)
- Title: "ReGen Civics" + subtitle "[Pitch Name], [Date]"
  (use commas not em-dashes)
- One photo: real land, real people. Not stock. Not abstract.
- One line that names the date and the audience (e.g.
  "October 2026, prepared for [Program Name]")

### Slide 2: The opening

Pick one current, specific observation:

- "A 40-acre community farm needs $400K, but only $80K of it is cash."
  (the plan's founder-video example; confirm the project with Rye)
- "[Specific land project] needed [tools, hands, a well] to plant [X
  acres]. The crowdpool showed where each one would come from."
- "Most forming communities never get off the ground for lack of land,
  money and organizational skill." (Diana Leafe Christian's practitioner
  estimate; cite it as one)

If we don't have a specific number, name a specific named project as the
anchor instead of a generic "landscapes need capital" line.

### Slide 3: The problem

Three bullets max. Each one specific, each one sourced. Draw them from the
seven collapse patterns in plan section 1 (Thesis 1):

1. The capitalization gap before land
2. Unclear or illegitimate decision-making
3. No livelihood engine

This slide is for investors, not for movement insiders. Use their
language: "failure rate," "structure," "diligence," "under-served market."

### Slide 4: The frame

This is the slide that makes or loses skeptical investors.

Visual: two anchors with a bridge between them, labeled:

- **Left:** "ReGen Civics, the company". Open tools, AI-assisted
  services, outcome-based revenue, legible to venture capital.
- **Right:** "The network". Land projects running their own games,
  quests, seasons, bioregional governance.

Caption: "Legibility is the bridge. Two anchors hold up one bridge."

Use the language from `CONTEXT_THE_TWO_GAMES.md` where it fits. Where that
file describes the Fund side, the cooperative replaces it and is described
only with `COOP`.

### Slide 5: What ReGen Civics is

Plain language. One paragraph. One diagram showing tools, services and the
network, and how a land project moves through them. Start from the plan's
core sentence: "ReGen Civics helps regenerative land projects design
structures that don't collapse, then connects them into a network that
capital can trust."

### Slide 6: The business model

- **Free tools, paid outcomes.** Use the revenue lines in plan section 1
  (Thesis 2): structure design and onboarding services, custom game builds,
  and the outcome-based fees listed there.
- **Label every line counsel has not cleared** (plan section 1.4). Never
  present stakes in projects as the core revenue line.
- Never take a percentage of grants won.
- The cooperative is not a revenue line on this slide. If the deck must
  mention it, it goes in the appendix in `COOP`'s words with
  `COOP.notAnOffer`.

### Slide 7: The game

- The ReGen Civics Year: Design, Resource, Build, and Rest seasons
- 13 stewardship roles (the season character art is real, show 4-6 of them)
- Quests + citizenship tiers
- Why this matters: "Players become contributors. Contributors become
  stewards. The game is how a land project finds its people."

This slide is the hardest to get right because investors hear "game"
and reach for the eject. Frame it as the engagement layer for the network,
not a Steam game.

### Slide 8: The infrastructure

- Mainstream decks: "coordination infrastructure" and "incentive design",
  the federation feed, the agent-native connectors
- Web3 variants only: Hypha DAO on Base (chain ID 8453), forum decisions
  becoming on-chain proposals, the private and public ledger with its claim
  flow

Diagram: a land project's own game on the left, the network in the middle,
partner networks reading the federation feed on the right.

### Slide 9: Traction

- Only numbers from the admin `metrics` table, each with a timeframe
  (plan section 6: traction goes second, with timeframes)
- Only numbers Rye has cleared for decks. Public pages show none until he
  marks them public.
- The Season One record (2022) from `shared/regenYear.ts` may appear as is
- Never token amounts, circulating supply, or anything priced in tokens

If a metric is small, frame it as growth ("from X to Y in Z months"),
not as absolute. If a metric isn't measured yet, say so on the slide
("To be measured in Season 2").

### Slide 10: The pipeline

Showcase 3-5 specific land projects with name, bioregion, what they need
across the nine forms of capital, and state. Use real photos.

Don't list 30 projects. Show the 5 most compelling and say "and X more
in flight."

### Slide 11: Team

- Rye (founder, lead): role + 2-3 lines + photo
- Key collaborators: 4-8, single line each
- Advisors: 3-5, single line each
- Notable partnerships: SEEDS, Hypha, Regen Network, etc.

Real people. Real photos. Real roles.

### Slide 12: The ask

Specific. Not "we're raising." Say:

- What you want from this program or investor, in the instrument it offers
  (accelerator terms, or a SAFE in the operating company; plan section 12
  covers incorporation, and some programs accept "incorporation in
  progress")
- The milestones it buys, in the plan's shape: "$[X] to reach [N] paying
  villages and $[Y] ARR in 18 months"
- Timeline: tied to real dates (the season calendar, program deadlines)

Never ask anyone to put money into the cooperative or into land projects
through us. The cooperative accepts no money, and it is not part of any
raise.

### Slide 13: Use of funds

Pie chart or simple percentage breakdown of the company's raise:

- X% to product and the tools
- X% to services capacity (design, onboarding, custom games)
- X% to network and partner work
- X% to operations (legal, ops)

If those percentages aren't set yet, ask Rye for them; don't invent them.
No line sends the raise into land projects or into the cooperative.

### Slide 14: Close + contact

- One sentence that lands. Pattern: "[Specific outcome we're working
  toward] will not happen by accident. It happens because [audience
  for this deck] decided to participate."
- Calendar link (use Rye's actual scheduling URL)
- Email: rieki@regencivics.earth (verify before locking)
- Social: forum, Twitter, LinkedIn

## Asset assembly checklist

Before producing the deck:

- [ ] Pull numbers from the admin `metrics` table only, with sources (Gate
      G4). Use the `regen-database-sql` skill for the queries. Never copy a
      number from old site copy or an old deck.
- [ ] Run `node scripts/check-fund-claims.mjs` on any copy you draft into
      the repo, and read every slide against the lane rules above
- [ ] Pull recent player photos from `client/public/images/quests/` and
      `client/public/images/roles/` if showing the game in action
- [ ] Pull land project photos from project pages
- [ ] Use the brand palette: forest greens (`#1A3A2E`, `#2D5A3F`,
      `#4A8362`), warm gold (`#D4A574`), parchment (`#F5E6D3`)
- [ ] Use real fonts: heading "Cinzel" or "Cormorant Garamond" if
      available, body "Inter" or system stack. Match the site.
- [ ] Image attribution: if using a partner photo, name the project /
      bioregion in the slide footer

## Versioning convention

- Save to `decks/INVESTOR_DECK_v[N]_YYYY-MM-DD.pptx`
- Bump major version (`v2`, `v3`) on structural changes; bump minor
  (`v2.1`, `v2.2`) on copy edits or number updates
- Always also save a "current" symlink: `decks/INVESTOR_DECK_LATEST.pptx`

## Cross-references

- `pptx` skill: read first, always, before generating
- `shared/fund.ts` (`COOP`): the only words for the cooperative
- `docs/private/FUNDING_ENGINE_PLAN.md` sections 1, 6 and 12.1: the thesis,
  the lanes, the deck spec, the cooperative architecture
- `regen-fundraising-copy` for the narrative voice in each slide
- `CONTEXT_THE_TWO_GAMES.md` for slide 4 framing
- `docs/planning/CITIZENSHIP_TIERS_SPEC.md` for slide 7 game mechanics
- `SEASONS_HISTORY.md` and `shared/regenYear.ts` for the Season One record
- `nano-banana-pro` for any custom imagery if photos aren't available
