---
name: forge-scout
description: "Forge doctrine for researching and vetting external skills, plugins, MCP servers, and CLIs: find a skill for X, check if there's a plugin/MCP for Y — approve/hard-pass gate."
---

# Forge playbook — Scout (external-capability research + vetting)

**Do not duplicate existing tools — defer to:** `forge-mcp-clients` skill (the dormant/opt-in MCP doctrine
every APPROVE verdict here still has to clear before anything is ever wired live), `forge-bin/forge-scout.cjs`
(the tailored-term generator + persistent vetting ledger this file's doctrine is built on top of), and the
`watch` skill (the ONLY sanctioned way to actually view a candidate's demo/review video — never described
or summarized from a title/thumbnail alone).

## What Scout is for
Per-project research into whether an EXTERNAL capability (a published Claude skill, a Claude Code plugin,
an MCP server, or a standalone CLI) would genuinely help the *current* project — not a generic "are there
Claude skills" sweep. A slides project searches for slide/PowerPoint-shaped capabilities; an Astro site
searches for Astro/static-site-shaped capabilities. Scout never installs anything itself; it produces a
researched, evidenced verdict that the owner opts into afterward.

## Step 1 — generate TAILORED search terms, not generic ones
Call `forge-bin/forge-scout.cjs terms --domain <domain> [--keywords <k1,k2,...>]` first. This returns a
domain-specific term list seeded from the project's actual domain (see the tool's `SEED_TEMPLATES` for the
curated set: website, astro, slides/presentation, fullstack, n8n, scraping, rag, prediction, integration,
electron/desktop, ecommerce, dashboard, game, mobile, mlops, tooling, voice — plus a domain-tailored fallback
for anything not yet curated). Example of the difference this makes:
- A slides project: `"claude powerpoint skill"`, `"claude slide generator skill"`, `"I stopped using
  PowerPoint claude code skill"` — **not** a bare `"claude skill"` search.
- An Astro project: `"claude astro skill"`, `"bulk website generator claude"` — **not** a bare
  `"claude plugin"` search.
Never hand-write ad-hoc terms when the tool's tailored list already covers the domain; extend it with
`--keywords` for anything project-specific the curated seed doesn't know about (a client name, a niche
library, a specific integration).

## Step 2 — research: web-search + watch every candidate's video
For each tailored term: web-search it, then for EVERY candidate that has a demo/review/walkthrough video,
actually watch it via the `watch` skill before forming a verdict — never judge a video by its title or
thumbnail alone. The exact invocation, verbatim (Dutch, matching the owner's own phrasing for this skill):
"als je een video wilt bekijken, doe ./watch {link}" — substitute the real URL found during search. A
candidate with a video that was never watched cannot be APPROVED; log it as unverified and either watch it
or HARD-PASS it with that reason.

## Step 3 — evaluate and record a verdict
Every candidate found gets exactly one of two verdicts, recorded via
`forge-bin/forge-scout.cjs record --capability <name> --verdict <approve|hard-pass> --reason "<why>" [--source <url>]`:

- **APPROVE** — the capability is genuinely useful, safe, maintained, and does not overlap an existing
  Forge capability. APPROVE is still **not** a green light to install or activate anything — see "Hard
  rules" below.
- **HARD-PASS** — permanently reject and record so the SAME capability is never re-researched on a future
  Scout pass. Use HARD-PASS for anything that:
  - could break or slow the system (heavy runtime dep, background daemon, unclear resource cost),
  - is junk (no real users, vaporware, marketing-only page),
  - overlaps a capability Forge already has (check `FORGE_SKILL_REGISTRY.md` and
    `config/orchestration/mcp-registry.json` first — never HARD-PASS-worthy duplication of effort),
  - is unmaintained (no meaningful commits/updates in a long time, abandoned issues),
  - is a security risk (requests broad/unscoped credentials, unclear data handling, unvetted third-party
    network calls, obfuscated code).

Before researching ANY capability, call `forge-bin/forge-scout.cjs list` (or `isVetted`) to check whether
it was already vetted — a prior HARD-PASS always persists and must not be re-litigated; a prior APPROVE is
reported as already-vetted rather than re-run from scratch.

## Hard rules (non-negotiable)
- **Nothing is auto-installed, ever.** Scout's job ends at a recorded, evidenced verdict — no skill/plugin/
  MCP file is copied, no dependency is added, no config is edited as a result of an APPROVE.
- **APPROVE still requires explicit owner opt-in.** This ties directly into the `forge-mcp-clients` dormant/
  opt-in doctrine and `forge-mcp-clients`' registry (`config/orchestration/mcp-registry.json` +
  `mcp-grants.json`) for anything MCP-shaped: an APPROVE verdict here is the research half only; the owner
  still has to name the capability explicitly before it goes from "vetted" to "opted in."
- **A HARD-PASS is permanent and non-negotiable without a NEW explicit owner override.** `isVetted()` always
  surfaces an existing HARD-PASS ahead of any later APPROVE attempt for the same capability — this is
  enforced by the ledger itself (`forge-scout.cjs`), not left to memory or good intentions.
- **No candidate is judged from marketing copy alone.** A web-search hit with a demo video is watched (Step
  2) before a verdict is recorded; a hit with no way to verify real behavior is HARD-PASSed as "unverifiable"
  rather than optimistically approved.
- **Every verdict carries a real reason and, where available, a real source (URL/repo).** No blank or
  templated reason field — `forge-scout.cjs record()` requires a non-empty reason.

## Skills / commands / MCP
`forge-bin/forge-scout.cjs` (`terms`, `record`, `list`, `isVetted` — the persistent ledger is split
template/user (2026-09-26 external audit N4/): the SHIPPED, curated baseline at
`config/orchestration/FORGE_SCOUT_VETTING.json` plus the separate, never-shipped
`config/orchestration/FORGE_SCOUT_VETTING.user.json` that `record()` actually writes new verdicts to —
`list()`/`isVetted()` transparently merge both, so read either name as "the ledger"), `watch` skill (mandatory video verification), `forge-mcp-clients`
skill (what an APPROVE still has to clear before anything is wired live), `FORGE_SKILL_REGISTRY.md` +
`config/orchestration/mcp-registry.json` (check first — never HARD-PASS as "overlap" without actually
checking these).

## Events
A real Scout pass logs `scout_researched` (once per research session: domain, term count, candidates found)
and `capability_vetted` (once per recorded verdict: capability, verdict, reason) via the project's real
`log-event.cjs` — never claim a Scout session ran, or a verdict was recorded, without these events actually
being logged.

## Fan-out & flow
**1-2 dedicated subagents own this role** — no larger team spawns for a Scout pass:
- **Search Boss** — owns Step 1 (tailored terms) and Step 2 (web-search + `./watch` verification); it is
  already the project's "Research / current information... no hallucination" role, so Scout is a natural
  extension of its existing responsibility, not a new agent.
- **Skill Boss** — owns Step 3 (recording the APPROVE/HARD-PASS verdict); it already "maintains the global
  skill registry" and "reports missing skills + safe fallback", so the vetting ledger is a natural extension
  of that existing responsibility, not a new agent.
No fan-out beyond these two; Scout never spawns a larger swarm for a research pass.

## Ship-readiness (unique)
Every term list actually came from `forge-scout.cjs terms` (not hand-invented); every video candidate was
actually watched via `./watch` before a verdict, or was HARD-PASSed as unverifiable; every verdict is
recorded in the real ledger with a non-empty reason; a prior HARD-PASS was checked and honored (never
re-approved); nothing was installed, activated, or opted in as a side effect of this skill running; the
report states plainly which capabilities were APPROVED (pending owner opt-in) and which were HARD-PASSED
(with why), never blurring "researched" with "installed."
