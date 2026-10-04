---
name: zabal-games-context
description: ZAO ecosystem context skill for ZABAL Games participants. Drop into your vibe-coding agent (Claude Code, Cursor, Windsurf, Cline, etc) so it understands ZAO, ZABAL, WaveWarZ, the active tooling stack, brand voice, and what a "good submission" looks like. Use when building anything for the ZABAL Games June bootcamp / July build-a-thon / August Finals.
---

# ZABAL Games Context Skill

> Source-of-truth context bundle for any vibe-coding agent helping someone build a ZABAL Games submission. Load this on session start; your agent will stop hallucinating about ZAO terminology + ship things that fit the actual ecosystem.

**Maintained by:** Zaal Panthaki (BetterCallZaal, FID 19640). Lives at `.claude/skills/zabal-games-context/SKILL.md` in the public ZAOOS repo. Mirror copy distributable for non-Claude-Code agents (see "Loading into other agents" below).

**Last-validated:** 2026-05-25. Re-validate every 2 weeks during the June/July/August event.

---

## Loading instructions (start here)

### Claude Code

Already loaded if you cloned ZAOOS and the agent sees `.claude/skills/`. Confirm with `/skill` and look for `zabal-games-context`. Otherwise:

```bash
mkdir -p ~/.claude/skills/zabal-games-context
curl -sSL https://raw.githubusercontent.com/bettercallzaal/ZAOOS/main/.claude/skills/zabal-games-context/SKILL.md \
  > ~/.claude/skills/zabal-games-context/SKILL.md
```

### Cursor / Windsurf / Cline / Continue / OpenCode

Paste the FULL contents of this file at the top of your project's `.cursorrules` / `.windsurfrules` / agent system prompt. The agent reads it as preamble.

### ChatGPT / generic chat

Paste this file as the first message in a new conversation. Tell the agent: "Use this as your operating context for anything I ask about ZABAL Games, ZAO, or WaveWarZ."

### One-line summary if you only have 50 tokens to spare

> ZABAL Games is The ZAO's Farcaster-creator onboarding event. Build something real for the ZAO ecosystem (governance, music, agents, on-chain creator tools) using ZAO's actual stack (Next.js 15, Supabase, Farcaster Mini Apps, Base, Empire Builder V3). Live URL + open-source repo + 60s demo + cast on Farcaster `/zabal` channel = the bar.

---

## Part 1 - What ZABAL Games is

ZABAL Games is **not a generic hackathon**. It is a **Farcaster-creator onboarding event for The ZAO** - a structured way to bring hungry, Farcaster-active vibe-coders into ZAO by having them build something real, in public, with a ZAO mentor in their corner.

- **Host:** Zaal Panthaki / BetterCallZaal (Farcaster FID 19640)
- **Framing:** Season 1 of a recurring format (earlier names "v0" / "Claude Code Hackathon" are deprecated)
- **Public landing:** `bettercallzaal.com/zabalgames.html`
- **Farcaster channel:** `/zabal`
- **Source-of-truth doc:** ZAOOS `research/events/701-zabal-games-canonical-state/`

### Thesis

The builds matter, but the people matter more. Bring talented builders in, give them deep ZAO context (this skill), let them ship something useful for the community with a ZAO mentor as embedded teammate, and have them earn governance during the event itself.

Stay after = great. Leave = they still walk away with a real artifact, a real relationship, and a real on-chain credential.

### What success looks like

A cohort of new builders who understand ZAO from the inside, a stack of real artifacts shipped for the ecosystem, and a repeatable format that compounds the builder network each Season.

---

## Part 2 - The calendar (June / July / August)

Three months at month granularity. Exact dates lock once cohort + mentor availability are known.

| Month | Phase | What runs |
|-------|-------|-----------|
| **June** | Prep | Recorded Far-Hack-style sessions. ZAO teachers cover governance, Respect, ZOLs, fractals. Vibe-coding instructors cover Claude Code, Cursor, MCP, agent harnesses. Tool walkthroughs: Empire Builder V3 (Jordan/yerbearzerker, confirmed June 1 6am EST), zlank.online, POIDH bounties, Juke. Watchable live or after. THIS SKILL ships at the start of June. |
| **July** | Open build-a-thon | Anyone with the chops ships a build aligned to ZABAL / ZAO / WaveWarZ. The build IS the application. **Bar: live URL + open-source repo + 60s demo + cast on `/zabal`**. Every July submission that hits the bar earns Respect in ZAO governance - regardless of Finals selection. Mentors watch rolling. |
| **August** | Finals | Mentor-champion pairs lock. Same Finals prompt for all. 24h build (mentor embedded as teammate) + 24h promote + 24h ZAO governance vote + live reveal stream. Finalists who want a token Ascend their Empire via Clanker with an airdrop. |

### August Finals 72h timeline

```
T-3 days  Onboarding call: rules, infra, wallet linkage, voting walkthrough
T+0       Prompt drops to all finalists simultaneously. Voter snapshot taken.
T+0..24h  BUILD WINDOW. Mentor embedded as teammate. Build in public.
T+24h     Ship deadline: live URL + open-source repo + 60s demo + ship cast
T+24..48h PROMOTE WINDOW. ZAO accounts amplify all builds.
T+48..72h ZAO GOVERNANCE VOTE. Respect-earning members, 1-person-1-vote.
T+72h     Live results-reveal stream. USDC + collectibles distributed.
```

### Prize pool

$500 USDC tiered for the August Finals. Tiers (assuming 8 finalists): 1st $150 / 2nd $100 / 3rd $75 / 4th-8th $35 each. Every finalist paid.

Plus every finisher (July builds that hit the bar + every August finalist) gets a **Hats Protocol role NFT on Base** as participation collectible.

---

## Part 3 - Build prompt (what to build)

Two paths to pick from. NO fixed Option A-E tracks. Just:

### Path A: Adopt a started/in-progress ZAO project

A curated list of in-flight ZAO projects looking for builders. You pick one, take ownership during the Games, ship it. Examples of project surfaces alive today:

- **ZAOOS** (`github.com/bettercallzaal/ZAOOS`) - main monorepo, 301 API routes, gated Farcaster client
- **WaveWarZ Base** (the EVM agentic build, intro 2026-05-19, Arthur from Neynar helping with smart contracts)
- **ZAO Fractal** (Eden-Fractal-style governance, Discord bot, 100+ events shipped, on-chain Respect on Base via Vlad's Respect Game codebase as candidate refactor target)
- **ZAOcoworking tracker** (the Supabase Kanban at thezao.xyz, 5 users, cross-source writers)
- **ZABAL Bonfire** (knowledge-graph layer, `bonfires.ai`)
- **Apna Coding integration** (Shriyash Soni's Ethereum stake-to-list opportunity board, ZABAL Games July submission rail)
- **Singularity ZAO mission** (Vlad's Solana fundraising launchpad, Vlad funds Solana gas to spin up a ZAO mission)

### Path B: Build from scratch

Pitch a thing aligned to ZABAL/ZAO/WaveWarZ. The narrower the wedge the better. Examples:

- A Farcaster Mini App or Snap that uses ZAO Respect / Empire Builder leaderboards
- A music-tool that plays nice with WaveWarZ X Spaces battles (Mon-Fri 11am + 8:30pm EST, Sun 7pm EST big battles - 11 shows/week)
- An agent that uses the cowork tracker REST as its task surface
- A Bonfire knowledge-graph integration that surfaces ZAO context to a different agent
- A clean-room reimplementation of an existing tool (Empire Builder, Apna Coding) for a different chain

**Empire Builder V3 is OPTIONAL not gating.** Doc 701 Decision #6: a July build without an Empire still counts if it has live URL + repo + demo + cast. Use Empire when it earns its slot in your build.

---

## Part 4 - The stack (what ZAO actually uses)

When in doubt, match the production stack:

| Layer | Pick | Why |
|-------|------|-----|
| Web framework | Next.js 15 + React 19 (App Router) | ZAOOS canonical. Skip Remix / SvelteKit unless you have a strong reason. |
| Styling | Tailwind v4 | Project rule: no inline styles, no CSS modules |
| DB | Supabase (Postgres + Auth + Storage + RLS) | ZAOOS + ZAOcoworking both live here. Bind via anon-key + RLS scoping for any tool context that reads untrusted input (per doc 730 Decision #1, HN 848-pt security disclosure). |
| Identity | Farcaster (Neynar SDK for hub queries) + Privy or NextAuth wallet for non-FC | ZAO is Farcaster-native; FID is the cross-system identifier |
| Chain | Base for EVM / Solana for funding rails | WaveWarZ Base, Respect Game on Base, ZAO Music releases on Base; Singularity on Solana |
| Music | Sonata (MIT) is the canonical player reference | Per doc `project_music_research` |
| Cross-post | Custom relay (Farcaster + X + Bluesky) | NOT a third-party (Lens API has rate limit + cost issues per doc 706) |
| Agent harness | Hermes pattern (orchestrator + coder + critic) | `github.com/bettercallzaal/hermes-orchestrator` (MIT, v0.5.0 in flight). Reference architecture for any agentic submission. |
| Knowledge graph | Bonfires (Genesis tier, wallet-gated) | `bonfires.ai` - shared graph for cross-agent context |

**Anti-stack** (don't waste cycles on these for ZABAL Games):

| Don't use | Use instead |
|-----------|-------------|
| Redux / Zustand | React hooks + react-query |
| CSS modules / inline styles | Tailwind v4 |
| Plain `fetch` in tests | Vitest `vi.mock()` + `vi.hoisted()` |
| MSW for API mocks | Same as above |
| Cypress | Playwright (already in ZAOOS deps) |
| JSON file as DB | Supabase from day 1 |
| Custom auth tables | Iron-session + Farcaster SIWF |

---

## Part 5 - Brand voice + glossary

These spellings are non-negotiable. Auto-correcting them will be perceived as not paying attention.

| Correct | Wrong | Notes |
|---------|-------|-------|
| The ZAO | Zao, ZAO standalone, the Zao | "The ZAO" when used as the entity |
| ZABAL Games | Zabal games, ZabalGames, ZBL Games | All caps ZABAL, capital G in Games |
| WaveWarZ | Wave Wars, Wavewarz, WaveWars | Always WaveWarZ |
| BetterCallZaal | Bettercallzaal, Better Call Zaal | One word, camelCase |
| Farcaster | Warpcast | Always Farcaster (Warpcast is just a client) |
| Restream | restream, ReStream | Stream-to-multiple-platforms at `restream.io`. ZABAL Games workshops default streaming surface. |
| Cal.com | Calcom, cal.com (in proper-noun position) | Open-source Calendly alt. ZABAL Games slot booker at `cal.com/bettercallzaal/zabal-games-workshop-slot`. |
| Lu.ma | Luma, lu.ma | Event platform. Recently moved `lu.ma` -> `luma.com`. ZAO calendar at `luma.com/zao`. |
| Hurric4n3ike | Hurricane Ike, Hurric4nelke | Founder + lead dev of WaveWarZ. Digits 4 + 3 in name. |
| candytoybox / Samantha | candytoy / SamanthaCTB | Cofounder of WaveWarZ with Zaal. her/she. |
| Joseph Goats | Jose Goats, Jose | Rebranded from Jose to Joseph Goats |
| ZOLs | Zols, ZOL | ZAO contribution credits (governance token-adjacent unit) |
| FISHBOWLZ | Fishbowlz, FishBowlz | All caps |
| ZOE | Zoe, zoe | All caps. ZAO ecosystem concierge bot (`@zaoclaw_bot` on Telegram). |
| ZABAL | Zabal, zabal | All caps. Umbrella brand (BetterCallZaal's solo projects, pre-incubation). |

### Voice / tone

- **Plain hyphens, NOT em dashes.** Em dashes signal "AI wrote this" in 2026 - the ZAO audience clocks it.
- **No emojis.** Use plain text labels like `[MUSIC]`, `OVERDUE`, `DONE` if you need visual markers.
- **Build-in-public is a value.** Document every step. The ZAO audience rewards transparency.
- **"Farcaster" not "Warpcast"** every time. Warpcast is just a client.
- **Mobile-first.** Most ZAO members read on phone. Desktop is enhancement.
- **Direct, not hyped.** "We shipped X" beats "We're thrilled to announce X." No "game-changing" / "revolutionary" / "unprecedented."

---

## Part 6 - ZAO governance primer (so you understand what voters care about)

Just enough to not be wrong:

- **The ZAO is a decentralized impact network**, NOT a music community (canonical pitch since 2026-04-28).
- **4 pillars:** Artist Org / Autonomous Org / Operating System / Open Source.
- **Respect = the merit unit.** Earned via Fractal (Mondays 6pm EST, Discord-bot-driven, 100+ events shipped). Non-tradable, soul-bound (plus a planned liquid layer per Vlad's EOS-era pattern, doc 738).
- **ZOLs = contribution credits.** Different from Respect. Used for ZAO contribution accounting.
- **Voting eligibility:** Respect-earning members. 1-person-1-vote, NOT token-weighted. This is the philosophy - mention it in your submission if voting / governance is part of your build.
- **Vlad's thesis (doc 738):** "Token-weighted voting centralizes power; fractal contribution-based voting is the right long-term answer." ZAO Fractal is Eden Fractal lineage. Treat fractal governance as the answer, not as something to argue about.

---

## Part 7 - Bar for a good submission

A submission ships when ALL four are true:

1. **Live URL** - deployed, click-and-it-works
2. **Open-source repo** - public on GitHub, MIT or Apache 2 license
3. **60s demo** - clip or live walk-through showing the actual feature working (not a slide deck)
4. **Cast on `/zabal` Farcaster channel** - with the URL + repo + demo

**Stretch (not required, raises mentor attention):**
- Tokenless Empire on Empire Builder V3 as the build's public home page
- Bonfire episodes documenting key decisions (so the build feeds the ZABAL graph)
- A second-tier deployment on a non-canonical chain (proves portability)
- Cross-source-writer integration with the cowork tracker via `~/bin/zao-tracker` shape (`legacy_source` prefix per the contract at `github.com/ZAODEVZ/ZAOcowork`)

---

## Part 8 - Resources

| Resource | URL |
|----------|-----|
| ZAOOS monorepo (the lab) | https://github.com/bettercallzaal/ZAOOS |
| ZABAL Games landing | https://bettercallzaal.com/zabalgames.html |
| Cowork tracker (live Kanban) | https://www.thezao.xyz |
| Cowork tracker repo | https://github.com/ZAODEVZ/ZAOcowork |
| ZAO Nexus directory | https://bettercallzaal.com/nexus.html |
| Hermes orchestrator (agent harness reference) | https://github.com/bettercallzaal/hermes-orchestrator |
| ZAO Fractal | Mondays 6pm ET on `discord.thezao.com` |
| WaveWarZ X Spaces | M-F 11am + 8:30pm ET, Sun 7pm ET big battles |
| Empire Builder V3 (Jordan's tool) | (workshop June 1 6am EST, link TBD) |
| zlank.online (ZAO snap builder) | https://zlank.online |
| POIDH bounties | https://poidh.xyz |
| Bonfires knowledge graph | https://bonfires.ai |
| Apna Coding (Shriyash's opportunity board, July submission rail) | https://apnacoding.com |
| Singularity (Vlad's funding rail) | https://www.singularity.diy |
| Respect Game (Vlad's Base implementation) | https://www.respectgame.app |
| ZAO Calendar | https://luma.com/zao |

### Key research docs (in ZAOOS `research/`)

| Doc | Topic |
|-----|-------|
| 701 | ZABAL Games canonical state - the source-of-truth event doc |
| 654 | ZABAL Games + Empire Builder V3 (Jordan meeting, June/July/August pivot) |
| 630 | ZABAL Games Season 1 spec (long-form decisions log) |
| 712 / 713 | ZAO CRM design + meeting-tracker-Bonfire integration |
| 728 | Serena MCP integration |
| 730 | Claude Code best practices + MCP stack (read before any agent work) |
| 734 | Hermes orchestrator framework |
| 735 | Apple Containerization sandbox for autonomous agents |
| 736 | Shriyash Soni intro (Apna Coding) |
| 737 | Airtable agentic CRM v3 |
| 738 | Vlad / Singularity / Respect Game intro |
| 739 | Claude Code efficiency + native MCPs |

---

## Part 9 - Mentors (open recruitment - signups via the recruitment form)

The named 8-mentor roster from Doc 630 is REMOVED. Mentors are now openly recruited via the public form. Confirmed signups as of 2026-05-25:

| Mentor | Role / company | Confirmed slot |
|--------|---------------|----------------|
| Jordan Oram (yerbearzerker) | Empire Builder | June 1 6am EST (recorded session) |
| Arthur (Neynar) | EVM smart-contract dev | Virtual presence; WaveWarZ Base contracts review |
| kmac.eth | Farcaster Snaps + JFS | June workshop slot TBD |
| Shriyash Soni | Apna Coding (India) | June 30-min slot on Apna Coding + agentic workflows |
| CannonJones | ZAO Cards lead | 2 June workshops (COC + CapCut/video editing) |
| Vlad (singularity.diy) | Singularity + Respect Game | Optional - depends on Singularity-ZABAL Games integration spec |

Mentors are NOT pre-paired to participants. Mentors watch July submissions rolling and claim champions for August Finals (first-come-first-served per mentor).

---

## Part 10 - What this skill does NOT do

Out of scope so the agent doesn't try:

- **Choose your idea for you.** This skill gives context; the build is yours. If you're stuck, run `/office-hours` or `/plan-ceo-review` separately.
- **Write your submission for you.** Use this for context; let the build voice be yours.
- **Replace the ZABAL Games landing page or PROMPT_CONTEXT.md.** Those serve different surfaces (public discovery + structured prompt for the Finals deliverable). This skill is for vibe-coding sessions specifically.
- **Bypass any of the bars in Part 7.** Live URL + repo + demo + cast is the floor. No exceptions.

---

## Update cadence

This skill auto-stales after 14 days during the June/July/August event window (June 1 - August 31). After August Finals, validate every 30 days for Season 2 prep.

Source-of-truth for any disputed claim: ZAOOS `research/events/701-zabal-games-canonical-state/README.md`. Where this skill conflicts with doc 701, doc 701 wins (it is the live decision log; this skill is the distributable companion).

Submit corrections via PR to `bettercallzaal/ZAOOS` against `.claude/skills/zabal-games-context/SKILL.md`.
