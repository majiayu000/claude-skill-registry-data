---
name: developer-marketing-ops
description: "Developer marketing and developer relations for B2B SaaS with technical audiences. Use this skill when the buyer or user is a developer: documentation as a marketing surface, quickstarts and time-to-first-call, SDKs and sample apps, developer community and DevRel programs, open-source strategy, and technical content that survives engineer scrutiny. Also triggers on: developer marketing, DevRel, developer relations, developer experience, DX, docs, documentation, quickstart, SDK, API marketing, open source strategy, developer community, technical content, dev audience, hacker news, engineering blog."
---

# Developer Marketing Operations

## Step 0 (always first): Load brand context

**Before producing any deliverable, look for a `brand-context.md` file** in the user's project root (also check `./.claude/brand-context.md` and `./docs/brand-context.md`). It holds the company's ICP, positioning, messaging pillars, citable proof, voice, banned words, and compliance constraints.

- **If it exists:** read it in full and treat it as binding for this run. Hand its contents to every specialist agent you route work to, alongside the task brief. Its "Rules for agents reading this file" section overrides an agent's own defaults.
- **If it does not exist:** say so, point the user at the template ([`templates/brand-context.md`](../../templates/brand-context.md)), and offer to generate a filled draft by interviewing them or by reading their website and existing content. Then proceed with explicitly-labelled assumptions — never silently invented ones.

**Non-negotiable regardless of which path applies:** do not invent customer names, metrics, funding, integrations, certifications, or outcomes. Only proof recorded in `brand-context.md` (or supplied directly in the request) may be used as fact. Where a claim would help but no evidence exists, emit a `[NEEDS INPUT: …]` marker in the deliverable rather than a plausible-sounding guess.

---

## What This Is

Developer Marketing Operations markets to developers — an audience where most classic B2B tactics actively backfire. Gated PDFs, lead-capture forms in front of docs, and benefit-led copy without code all read as hostile here. This skill owns the artifacts a developer actually evaluates in an IDE, a terminal, or a repo, and hands channel execution to the existing acquisition skills.

## The Team: 1 Specialist Agent

| # | Agent | File | What They Do |
|---|-------|------|-------------|
| 1 | Developer Audience Strategist | `agents/devmkt-developer-audience-strategist.md` | Owns documentation as a marketing surface, quickstart and time-to-first-successful-call design, SDK and sample-app strategy, open-source and community programs, DevRel motion design (talks, workshops, office hours), and technical content standards that survive engineer scrutiny. |

## How to Use

### Routing User Requests

**Developer experience & docs** → Developer Audience Strategist
- "Cut our time-to-first-successful-API-call"
- "Audit our docs as a marketing surface"
- "Design a quickstart that actually gets someone to hello world"
- "What should our SDK and sample-app strategy be?"

**Developer community & DevRel** → Developer Audience Strategist
- "Design our DevRel program"
- "Should we open-source this, and what does that commit us to?"
- "Build a developer community motion that isn't astroturf"
- "Why does our technical content get torn apart by engineers?"

### Working Method

1. **Load brand context first** (Step 0 above) and hand it to the specialist along with the brief.
2. **Route to the specialist** whose remit matches the request. Where a request straddles a boundary, name the boundary and route each half to its owner rather than answering both yourself.
3. **Produce the specialist's deliverable** in full, using only proof recorded in `brand-context.md` or supplied in the request. Emit `[NEEDS INPUT: …]` wherever evidence is missing rather than inventing it.
4. **Name the handoffs.** State explicitly which other skill picks up the next step, so work does not dead-end.

**Boundaries this skill respects.** Scope is set by **artifact and audience, not channel**: this skill owns anything a developer evaluates in an IDE, terminal, or repo, and briefs channel execution out to the existing agents — `content-blog-strategist` still owns the blog program, `social-reddit-specialist` and the social skill still own community channels, and `seo-technical-auditor` still owns crawlability. It supplies the technical substance and the credibility bar; they run the surface.

## Output Standards

- Every deliverable names its audience, its owner, and the decision it enables.
- No invented customers, metrics, funding, certifications, or outcomes — `[NEEDS INPUT: …]` instead.
- Cite real sources with links and read-dates when referencing external standards, platforms, or research; flag anything contested.
- Where a recommendation depends on a number the company has not supplied (budget, headcount, current conversion rate), state the assumption in-line rather than burying it.
