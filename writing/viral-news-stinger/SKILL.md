---
name: viral-news-stinger
description: Mine the last 24 hours of trending news via Exa/Firecrawl MCP, fact-check ONE topic, and output viral-ready post options in the user's voice with receipts. Use for scheduled news-post Routine runs.
license: AGPL-3.0-or-later
compatibility: Claude Cowork (Routines), Cowork desktop, Cursor, Codex
metadata:
  hive-tier: standalone
  voice-skill: user-set (name your voice skill in references/editorial-preferences.md)
  ledger: /areas/content-post-ledger.md in user memory
  paired-skill: repo-radar-stinger (independent sibling, shared ledger)
  version: "1.0"
---

# Viral News Stinger

## Purpose

Runs on a cadence (Claude Routines) or on demand. Sweeps the last 24 hours of trending news and X conversation, picks the single most post-worthy topic, fact-checks that one topic hard, then produces three copy-paste-ready post options in the user's voice (or a neutral voice when none is configured) with citations underneath. Sharp, salacious, engineered to travel, and accurate enough to survive its own receipts being opened. If nothing clears the bar, it produces nothing.

## When to use

- A scheduled Routine run whose prompt invokes this skill by name
- "Find me something to post today", "what's hot right now", "run the news stinger"
- Any request for a viral-ready post about current news in the user's voice

## When not to use

- GitHub repository content: that is repo-radar-stinger's beat
- Rewriting or replying to existing content in the user's voice with no news mining: use the user's voice skill directly
- Evergreen content with no time hook

## Hard gates (all of them, every run)

1. **Preferences, then ledger.** Read `references/editorial-preferences.md` (voice skill, beats, editorial policy) first, then the shared topic ledger, before any search. A topic already covered, by slug, link, or substance, is dead on arrival. See `references/ledger-protocol.md`.
2. **24 hours.** The development itself must have happened inside the last 24 hours. A new article about an old event does not reset the clock. Verify published timestamps; never assume a search filter did it.
3. **One topic.** Pick ONE candidate from the sweep, then fact-check only that one. Never deep-research multiple candidates in parallel; that burns tokens for nothing. If the chosen topic fails verification, the run ends with a no-post report. It does not fall back to researching a second topic.
4. **Receipts or nothing.** The fact-check standard in `references/source-tiers.md` must pass. Every claim in every post option traces to a citation printed below the post. Never fabricate quotes, numbers, or events. Provocative framing of true facts is the product; fabrication is never.
5. **No forced output.** If the sweep finds nothing worth posting, say exactly that in three sentences and stop. No filler research, no mediocre post.
6. **Editorial policy.** Apply the user's beats and editorial policy from `references/editorial-preferences.md`. The default policy is politically neutral: no partisan advocacy, claims fact-checked, contested issues presented fairly. Accuracy rules in `references/source-tiers.md` apply regardless of preferences.

## Procedure

1. Read `references/editorial-preferences.md` and hold the voice skill name, beats, and editorial policy. Load the memory tools if they are deferred (in Cowork, ToolSearch for `memory_list`, `memory_read`, `memory_write`, `memory_str_replace`). Read the ledger per `references/ledger-protocol.md` and hold the exclusion list.
2. Confirm the Exa and/or Firecrawl MCP tools are available (in Cowork they may need loading via ToolSearch: `web_search_exa`, `web_fetch_exa`, `firecrawl_search`). These are the required mining tools. If neither server is connected, report that and stop; only fall back to a built-in web search tool if one exists, and say so in the output.
3. Sweep, capped at three or four search calls total:
   - Firecrawl `firecrawl_search` with `sources: [{"type":"news"}]` and `tbs: "qdr:d"` across the configured beats (defaults in `references/editorial-preferences.md`).
   - Optionally fetch one public X trend mirror for the live What's-happening list (see `references/research/distilled-viral-news.md` for URLs). Trends are candidates only, never receipts.
   - Optionally one Exa `web_search_exa` pass; if `web_search_advanced_exa` is available, use `startPublishedDate` set to 24 hours ago with `category: news`.
4. Filter candidates through the gates: fresh, not in the ledger, inside the editorial policy, and hookable (a sharp first line writes itself). Rank by viral potential: controversy, specificity, and how early the wave is.
5. Choose ONE topic. State the choice and the one-sentence core claim.
6. Fact-check that claim per `references/source-tiers.md`: Tier A or two independent Tier B confirmations, timestamp verification, denial/correction check, exact numbers. Capture every receipt (source, headline, published time, URL).
7. Apply the voice. If a voice skill is configured and available, load it and follow its full workflow: pick one register, read its guide for each length, calibrate against its corpus, and run its anti-AI gate on every option; its hard rules override the length and punctuation rules here, never the accuracy, fact-check or vetting gates. If none is configured (or it is unavailable), write in a neutral, clear voice, do not invent a persona, and say so in the output header.
8. Write the deliverable exactly per `references/output-template.md`: micro (9 words or less), medium (10-60 words), long form (200+ words), the single most relevant link, 2-4 hashtags actually trending on the topic, and the numbered receipts.
9. Deliver the output as the run's final message. In an unattended Routine run, also send it through the user-facing message tool if one is available, so it reaches the user verbatim.
10. Append one ledger line for the covered topic per `references/ledger-protocol.md`. A no-post run appends nothing.

## References map

- `references/ledger-protocol.md`: load at step 1 and step 10; the memory file location, format, and read/write rules
- `references/editorial-preferences.md`: load at step 1; the user-editable voice skill name, beats, editorial policy, length bands and ledger path
- `references/source-tiers.md`: load at steps 4-6; source quality tiers and the fact-check standard
- `references/output-template.md`: load at step 8; the exact deliverable shape and the no-post shape
- `references/research/distilled-viral-news.md`: load when a tool capability or trend-mirror URL needs checking; cited distillation of this skill's research archive
- `references/research/raw/`: source-repository archive for tracing a distilled claim; omitted from the installed plugin

## Related skills

- The user's voice skill (separate account skill, named in `references/editorial-preferences.md`): the voice. When none is configured, drafts are neutral and labeled as such.
- repo-radar-stinger (sibling skill in this pack): the GitHub counterpart. Runs independently on its own cadence and shares the ledger so the two never double-cover a story.

## Critical Directive

- You must read all files and context contained within your skill.
- In the event your core knowledge does not provide sufficient guidance you must make every attempt to search the internet, related knowledge base documentation files, and other available resources to supplement your knowledge prior to proceeding with your task.
- Additional related skills: the user's voice skill is a separate account skill; repo-radar-stinger is bundled in this pack.

Ship Gate removed: research-only skill, produces social post drafts and a memory ledger line, never committable code.
