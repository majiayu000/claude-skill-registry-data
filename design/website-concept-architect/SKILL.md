---
name: website-concept-architect
version: 1.0.0
description: Walk the user through designing a website concept before any code — purpose, audience, content inventory, tone, visual archetype, structure — and output 2-3 distinct concept directions plus an ASCII homepage wireframe. Use when planning a new personal site, portfolio, or marketing page upstream of implementation. Hands off to ui-ux-architect / frontend-design.
---

# Website Concept Architect

Pre-code concept design for personal sites, portfolios, and landing pages. This skill produces *direction*, not markup. The deliverable is a small set of distinct concept docs the user picks from; the chosen one feeds [ui-ux-architect](../ui-ux-architect/SKILL.md) for implementation.

## When to use

User is starting a new website and wants to decide *what it is* before writing code. Not for redesigns of working sites unless the brief is "rethink from scratch". Not for component-level UI decisions — those belong to ui-ux-architect.

## 1. Operating principle — walk, don't dump

Run the six stages **interactively, one at a time**. After each stage, present the menu, pause, wait for the user's pick, then advance. Never collapse multiple stages into a single question. Never skip stages even if the user volunteers info — surface what they said as a pre-selected default and confirm.

The point of the walk is to force decisions the user would otherwise defer. Skipping a stage means a vague concept doc later.

## 2. The six stages

| # | Stage | Purpose | Output |
|---|-------|---------|--------|
| 1 | Purpose | What is the site *for*? | 1-2 picks from archetype list |
| 2 | Audience | Who reads it? | 1-2 picks, drives tone & density |
| 3 | Content inventory | What lives on it? | Checked menu of sections |
| 4 | Tone & personality | How does it feel? | 2-3 adjectives from curated list |
| 5 | Visual direction | What does it look like? | 1 archetype (ranked suggestions, full list shown) |
| 6 | Synthesis | Concept docs | 2-3 distinct concept directions + ASCII wireframe |

## 3. Stage 1 — Purpose

Present these archetypes. User picks 1-2 (combinable, e.g. *portfolio + writing hub*):

- **Portfolio / showcase** — work artifacts are the point; projects are the spine of the IA.
- **Writing hub** — essays / blog / notes are the spine; everything else is navigation.
- **Professional calling card** — single-page or near-single-page; recruiters / clients land, learn, contact.
- **Digital garden** — evergreen interlinked notes; structure is the network, not chronology.
- **Project launcher** — a specific product or project is the hero; "about me" is a footnote.
- **Experimental playground** — site is itself a creative artifact; convention is the enemy.

If user picks **2 incompatible archetypes** (e.g. *experimental playground* + *professional calling card*), flag it and ask which wins on the homepage — the loser becomes a subsection.

## 4. Stage 2 — Audience

Picks shape **how much explanation things need** and **what voice fits**.

- **Recruiters / clients** — fast skim, credentials-first, low jargon, contact obvious.
- **Fellow devs / peers** — assumes shared vocab, tolerates density, code samples land.
- **Friends / community** — informal, personality-forward, in-jokes OK.
- **Future-you / archive** — built for searching your own past, density over polish.
- **The open web** — generic visitor, must self-explain, SEO matters.

Multi-audience is normal. If they pick 3+, ask which one the homepage is optimized for — the rest get accommodated on subpages.

## 5. Stage 3 — Content inventory

Present this menu. User checks what they want; offer to add custom items.

**Standard sections:**
- About / bio
- Now page (what you're focused on right now)
- Projects index
- Individual project case studies
- Essays / blog / writing
- Notes / digital garden / wiki
- Reading list / bookshelf
- Uses page (tools, hardware, setup)
- Resume / CV (or link to PDF)
- Contact (email, social, form)
- Newsletter signup
- RSS / Atom feed
- Changelog (site or life updates)
- Photo gallery
- Talks / podcasts / appearances
- Guestbook / webring (retro-web aesthetic)

For each picked section, ask one follow-up: **does this exist yet?** Sections without content get marked `[deferred]` in the concept doc so the user doesn't ship empty pages.

## 6. Stage 4 — Tone & personality

Pick 2-3 adjectives. These anchor stage 5's visual suggestions and stage 6's copy voice.

Present as **opposing pairs** so picks force tradeoffs:

- minimal ↔ dense
- playful ↔ serious
- warm ↔ clinical
- raw ↔ polished
- intimate ↔ public
- experimental ↔ conventional
- fast / scannable ↔ contemplative / long-form
- confident ↔ self-deprecating

A user who picks *minimal + playful + warm* gets very different suggestions than *dense + serious + clinical*. Record the picks verbatim — they go into the concept doc as the brief.

## 7. Stage 5 — Visual direction

Eight archetypes. **Rank the top 3 by fit** based on stages 1-4, but show the full list so the user can override.

| Archetype | Feel | Fits when stages 1-4 say... | Reference sites |
|-----------|------|------------------------------|------------------|
| **Terminal / CLI** | monospace, sparse, command-line | dev audience, minimal, raw, archive | sive.rs, wiki.nikiv.dev, ratfactor.com |
| **Editorial / Swiss** | strong type, grid, generous whitespace | polished, serious, professional calling card | rauno.me, paco.me, linear.app |
| **Brutalist** | raw HTML, default styles, no chrome | experimental, raw, intimate, dev audience | brutalist-web.design, motherfuckingwebsite.com |
| **Zine / maximalist** | collage, mixed fonts, layered textures | playful, experimental, community audience | cassie.codes, lynnandtonic.com |
| **Minimalist portfolio** | single column, big images, lots of whitespace | portfolio, polished, recruiters/clients | many designer portfolios |
| **Notebook / garden** | wiki-like, dense interlinks, evergreen | digital garden, archive audience, dense | gwern.net, andymatuschak.org |
| **Magazine / story** | long-scroll narrative, art-directed, hero imagery | project launcher, contemplative, open web | pitchfork.com long-reads, the verge features |
| **Database / index** | filterable table, almost a UI | dense, archive, lots of artifacts | are.na profiles, derek sivers' /now directory |

Show the ranking with one-sentence rationale per pick, e.g. *"Terminal/CLI fits because you picked dev audience + minimal + raw."* User picks one; if they override the ranking, ask why and record it (the override often reveals a constraint not surfaced earlier).

## 8. Stage 6 — Synthesis

Produce **2-3 distinct concept directions**, not one. Even if the user is decided, alternatives expose what they're trading off.

### Concept doc shape

For each direction, write a markdown doc with these sections:

```markdown
# Concept: <name>

## One-line pitch
<the site in 15 words or fewer>

## Brief
- Purpose: <stage 1 picks>
- Audience: <stage 2 picks, primary first>
- Tone: <stage 3 adjectives>
- Visual archetype: <stage 5 pick>

## Information architecture
<tree of pages/sections, max 2 levels deep>

## Homepage strategy
<what the homepage does in 2-3 sentences — first impression, primary action, what the visitor leaves knowing>

## Sample copy voice
<2-3 sentences in the chosen voice — about section opener, or homepage tagline + subhead>

## What this concept sacrifices
<honest list of what's deprioritized vs. the other concepts — every concept trades something>

## Ascii homepage wireframe
<see §9>
```

The three directions should differ on **a real axis**, not be cosmetic variants:
- **Concept A** = the obvious read of the user's picks
- **Concept B** = optimizes harder for the primary audience (often more minimal)
- **Concept C** = a deliberate stretch — what if the experimental dial went one click further?

If two of the three end up nearly identical, drop one and explain why.

## 9. ASCII homepage wireframe

One per concept. Keep it **80 cols wide**, label regions in `[BRACKETS]`. Show hierarchy with box-drawing or simple dashes.

Example for a terminal/CLI portfolio:

```
+------------------------------------------------------------------------------+
| ~ ramon.dev                                              [now] [writing] [/] |
+------------------------------------------------------------------------------+
|                                                                              |
|  ramon alvarez                                                               |
|  go developer · tooling · personal CLIs                                      |
|                                                                              |
|  > currently building rsk, a skill management CLI for claude code            |
|                                                                              |
|  --- recent ----------------------------------------------------------       |
|  2026-05-18  shipped: ralvaskills v0.3                                       |
|  2026-05-02  essay:   why I bundle skills as one repo                        |
|  2026-04-21  project: rsk cli infrastructure                                 |
|                                                                              |
|  --- projects --------------------------------------------------------       |
|  ralvaskills        personal AI skills toolkit            [→]                |
|  rsk                cli for managing skills               [→]                |
|                                                                              |
+------------------------------------------------------------------------------+
| email · github · rss                                                         |
+------------------------------------------------------------------------------+
```

Wireframes are about **proportion and hierarchy**, not pixel layout. No colors, no fonts, no icons beyond ASCII. If a section needs explanation, add a one-line note *below* the wireframe, not inside it.

## 10. Anti-patterns

- **Skipping stages because "the user already said".** Surface their input as a default and confirm; don't assume. Half the value is forcing the user to look at what they didn't say.
- **One concept doc instead of 2-3.** Alternatives are how the user understands what they're choosing. Single-concept output is a failed run.
- **Visual archetype before tone is locked.** Stage order matters — visual is downstream of purpose/audience/tone, not parallel.
- **Filling in content for `[deferred]` sections.** If the user hasn't written the essays, don't invent topic lists — the concept doc commits to *structure*, not *content*.
- **Wireframes with implementation details.** No "use shadcn Card here" — that's ui-ux-architect's job. Wireframes show what goes where.
- **Generic suggestions.** "A clean modern portfolio" is not a concept. Every concept doc must commit to specific picks on every axis.

## 11. Hand-off

Once the user picks one of the 2-3 concepts, the concept doc is the brief for:
- [ui-ux-architect](../ui-ux-architect/SKILL.md) — for tokens, components, accessibility, the four required states.
- Built-in `frontend-design` skill — for the actual code if going production-grade.

The concept doc should be saved to the project repo (e.g. `docs/concept.md`) so it survives as the design rationale.

## 12. Cross-skill ties

- [ui-ux-architect](../ui-ux-architect/SKILL.md) — implementation-level standards; this skill feeds it the brief.
- [demo-presentation-architect](../../personal/demo-presentation-architect/SKILL.md) — similar interactive walk-through structure, different domain.
- [demo-script-architect](../../personal/demo-script-architect/SKILL.md) — narrative principles (audience-first, progressive reveal) apply to homepage copy too.
