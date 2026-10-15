---
name: repo-radar-stinger
description: Scan GitHub for repos trending in the last 24 hours (vibe coding, AI coding, AI memory, vulnerabilities) via Exa/Firecrawl MCP, vet ONE, and output post options in the user's voice with receipts.
license: AGPL-3.0-or-later
compatibility: Claude Cowork (Routines), Cowork desktop, Cursor, Codex
metadata:
  hive-tier: standalone
  voice-skill: user-set (name your voice skill in references/editorial-preferences.md)
  ledger: /areas/content-post-ledger.md in user memory
  paired-skill: viral-news-stinger (independent sibling, shared ledger)
  version: "1.0"
---

# Repo Radar Stinger

## Purpose

Runs on a cadence (Claude Routines) or on demand. Scans GitHub for repositories trending RIGHT NOW in the user's configured beats (defaults: vibe coding and AI-assisted development, AI coding tools, AI memory systems, newly disclosed vulnerabilities, and anything else on the board a builder audience would share). Vets the single best one, then produces three copy-paste-ready post options in the user's voice (or a neutral voice when none is configured) with the repo link and citations underneath. If nothing on the board is worth posting, it produces nothing.

## When to use

- A scheduled Routine run whose prompt invokes this skill by name
- "What's trending on GitHub", "find me a repo to post about", "run the repo radar"
- Any request for a viral-ready post about a trending repository in the user's voice

## When not to use

- General news with no repository at the center: that is viral-news-stinger's beat
- Rewriting existing content in the user's voice with no mining: use the user's voice skill directly
- Reviewing or auditing a repo's code quality: that is a different job entirely

## Hard gates (all of them, every run)

1. **Preferences, then ledger.** Read `references/editorial-preferences.md` (voice skill, beats, editorial policy) first, then the shared topic ledger, before any scan. A repo already covered, by owner/repo, link, or substance, is dead on arrival. See `references/ledger-protocol.md`.
2. **24 hours.** The rule binds the SPIKE, not the repo's age. An old repo surging today is fair game; last week's darling is stale. Acceptable spike evidence is defined in `references/repo-vetting.md` (today's trending board, stars-today, a release or disclosure inside 24 hours).
3. **One repo.** Pick ONE candidate from the scan, then vet only that one. Never deep-vet multiple repos; that burns tokens for nothing. If the chosen repo fails vetting, the run ends with a no-post report. It does not fall back to vetting a second repo.
4. **Receipts or nothing.** Vetting per `references/repo-vetting.md` must pass: real code, honest one-sentence description, exact captured numbers, and for security topics a mandatory second source. Never fabricate stars, capabilities, or severity. For vulnerability repos, post the disclosure as news; never write exploit usage instructions or frame the post as a how-to.
5. **No forced output.** If the board holds nothing worth posting, say exactly that in three sentences and stop.
6. **Editorial policy** from `references/editorial-preferences.md`: politically neutral by default (no partisan advocacy, contested issues presented fairly), sharp but never fabricated. Preferences change which candidates are picked; they never relax the vetting rules.

## Procedure

1. Read `references/editorial-preferences.md` and hold the voice skill name, beats, and editorial policy. Load the memory tools if they are deferred (in Cowork, ToolSearch for `memory_list`, `memory_read`, `memory_write`, `memory_str_replace`). Read the ledger per `references/ledger-protocol.md` and hold the exclusion list.
2. Confirm the Exa and/or Firecrawl MCP tools are available (load via ToolSearch if deferred: `web_fetch_exa`, `web_search_exa`, `firecrawl_search`, `firecrawl_research_search_github`). These are the required mining tools. If neither server is connected, report that and stop; only fall back to a built-in fetch/search tool if one exists, and say so in the output.
3. Scan, capped at three or four calls total:
   - Fetch https://github.com/trending (daily board) with `web_fetch_exa` or Firecrawl. Capture repo names, descriptions, languages, stars, and stars-today.
   - Optionally one topic-led pass: `firecrawl_search` with `categories: ["github"]` or `firecrawl_research_search_github` on the priority beats (agent skills, AI memory, CVE proof-of-concepts).
   - Optionally one momentum cross-check: OSS Insight trending API (`period=past_24_hours`) or trendshift.io, per `references/research/distilled-repo-radar.md`.
4. Filter candidates through the gates: current spike, not in the ledger, in a configured beat (defaults and order in `references/editorial-preferences.md`), and hookable. Skip star-farmed templates and README-only vaporware, unless the star-farming itself is the story.
5. Choose ONE repo. State the choice and the one-sentence description of what it actually does.
6. Vet it per `references/repo-vetting.md`: fetch the repo page, read the README, capture exact numbers, cross-check independent coverage, run the security-topic rules when they apply.
7. Apply the voice. If a voice skill is configured and available, load it and follow its full workflow: pick one register (choose per its guide), read its guide for each length, calibrate against its corpus, and run its anti-AI gate on every option; its hard rules override the length and punctuation rules here, never the accuracy, fact-check or vetting gates. If none is configured (or it is unavailable), write in a neutral, clear voice, do not invent a persona, and say so in the output header.
8. Write the deliverable exactly per `references/output-template.md`: micro (9 words or less), medium (10-60 words), long form (200+ words), the repository link, 2-4 hashtags actually moving in the niche, and the numbered receipts (repo page capture counts as receipt one).
9. Deliver the output as the run's final message. In an unattended Routine run, also send it through the user-facing message tool if one is available, so it reaches the user verbatim.
10. Append one ledger line (`repo | owner/repo | link`) per `references/ledger-protocol.md`. A no-post run appends nothing.

## References map

- `references/ledger-protocol.md`: load at step 1 and step 10; the shared memory file location, format, and read/write rules
- `references/editorial-preferences.md`: load at step 1; the user-editable voice skill name, beats, editorial policy, length bands and ledger path
- `references/repo-vetting.md`: load at steps 4-6; spike evidence, default beat order, the vetting checklist, security-topic rules
- `references/output-template.md`: load at step 8; the exact deliverable shape and the no-post shape
- `references/research/distilled-repo-radar.md`: load when a discovery endpoint or tool capability needs checking; cited distillation of this skill's research archive
- `references/research/raw/`: source-repository archive for tracing a distilled claim; omitted from the installed plugin

## Related skills

- The user's voice skill (separate account skill, named in `references/editorial-preferences.md`): the voice. When none is configured, drafts are neutral and labeled as such.
- viral-news-stinger (sibling skill in this pack): the news counterpart. Runs independently on its own cadence and shares the ledger so the two never double-cover a story.

## Critical Directive

- You must read all files and context contained within your skill.
- In the event your core knowledge does not provide sufficient guidance you must make every attempt to search the internet, related knowledge base documentation files, and other available resources to supplement your knowledge prior to proceeding with your task.
- Additional related skills: the user's voice skill is a separate account skill; viral-news-stinger is bundled in this pack.

Ship Gate removed: research-only skill, produces social post drafts and a memory ledger line, never committable code.
