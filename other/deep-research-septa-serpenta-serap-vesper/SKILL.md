---
name: deep-research
description: Use when deep-diving a product, tech, or company.
---

# Deep-Dive Research Briefs

Vesper's standard for research deliverables: every claim tagged, every figure sourced, no fabricated specs, and a verdict that actually says which path is worth the money.

## Trigger
- "Deep-dive research on X", "find EVERYTHING concrete about X", multi-part numbered research briefs, "is X worth it / best path to Y" purchase/verdict questions.

## Workflow
1. **Parse the brief into numbered asks** — keep the user's numbering; each ask maps to a section of the deliverable. Do not merge or drop asks.
2. **Source hierarchy**: official docs/product pages FIRST (extract fully), then reputable press, then community/forums, then GitHub/RE efforts. Collect URLs + prices as you go.
3. **Huge SPA pages** (e.g. lovense.com product pages, 190K+ chars):
   - `web_extract` truncates head+tail but SAVES the full text to a cache file (`~/.hermes/profiles/vesper/cache/web/<domain>-<hash>.md`). Note the path in the tool result.
   - Do NOT page through 200K chars — `search_files` the cache file with a regex of spec keywords (`battery|Weight|kg|FAQ|Memory|price|Height|...`) to find line offsets, then `read_file` those specific ranges.
4. **When a site blocks extraction** ("Website Not Supported", 403/503, browser timeout):
   - Mine search snippets: run multiple targeted queries — snippet titles+descriptions often carry the key facts (prices, specs, dates).
   - Wayback fallback: `curl "http://archive.org/wayback/available?url=<url>&timestamp=<YYYYMMDD>"` to locate a snapshot, then fetch it. Expect 503s — check availability first, wait, retry once.
   - Browser is the LAST resort; if `browser_navigate` times out, do NOT retry identical args (loop risk) — fall back to snippets.
   - Even Cloudflare-challenged pages sometimes produce a cache file: check the web_extract result footer for the `cache/web/...md` path and read_file/search_files it before giving up on the page.
5. **Flag every claim**: `[DOCUMENTED]` (official/reputable source) vs `[SPECULATIVE]` (inference, marketing-video claims, unverified). Explicitly name what is UNDISCLOSED (e.g. "model identity not disclosed").
6. **Pre-order/vaporware discipline**: separate announced specs from shipped reality — ship dates, refundable deposits, "estimated price" wording, T&C escape hatches. Say "no public evidence yet" rather than "no support exists" when the product hasn't shipped.
   - **Named-brand verification** (user says "check X — could be a real brand misremembered"): treat every user-named brand as UNVERIFIED until proven. Run ≥2–3 search variants before declaring non-existence: brand alone, brand + category word, brand + CEO/founder name, alternate spellings/capitalization. Check trademark registries (UK IPO journal / USPTO) — a class-28 "Syndoll" trademark hit proved the name is real but a *toy* brand, not a sex-doll company. Classify findings as ✅ SHIPPED / 🚧 ANNOUNCED / 🧪 CROWDFUNDED / 💀 STALE (promise lapsed, never shipped) / 🚫 NOT FOUND (no evidence at all — likely misremembered) / ⚠️ VAPORWARE (exists as name/marketing only). Reporting "X does not exist as described" is a valid, valuable finding — the user asked for it explicitly.
7. **Deliverable shape** (user preference — embed it):
   - Spec tables: dimensions, weight, materials, battery/operation, features, customization, price tiers.
   - Software stack section: what model/LLM, cloud vs local, memory, voice, languages.
   - Developer/API story: official API surface vs RE/community ecosystem; what the API covers vs the product.
   - Brand-ecosystem extras: confirm what's documented, flag what's assumed.
   - Honest verdict vs alternatives with a COSTED comparison (turnkey vs DIY: parts, prices, trade-offs, what you give up) and a bottom line.
   - For LANDSCAPE/multi-vendor briefs ("which of all these players does X"): per-vendor comparison table (vendor, status flag, price, the X-story, Y/N), dead-end brands called out, then the blunt bottom line — if the honest answer is "nobody ships it, X is closest, DIY is the only real path," SAY SO in the first paragraph, not buried in the verdict.
   - Sources list with URLs.
8. Save the full report to `/home/lumi/<topic>_research.md` and give a tight chat summary (findings per ask, verdict, files, issues/blockers encountered).

## Pitfalls
- NEVER fabricate specs or invent API endpoints. "Estimated" stays estimated; "TBD" stays TBD.
- Cross-check headline figures against the official spec page — e.g. media said Emily had "8-hour battery"; the official spec showed 8 h STANDBY / 3 h continuous use.
- Snippet facts can be wrong or marketing-flavored; treat them as leads, not proof.
- User-named brands are leads, not facts: in one brief, three named players (SynDoll Labs/Thalanor, BOLTT, "Sex Doll Genius") did not exist as described or were SEO spam. Verify before spending search budget; say "not found / misremembered" plainly.
- A vendor's dev API may cover only PART of their lineup — Lovense's developer API controls toys, NOT the Emily doll's brain. Check what an API actually controls before crediting the product with it.
- For hardware/companion-tech research, note privacy/cloud architecture explicitly — it decides the verdict for self-hosted use cases.
- If a key source is unreachable, say so in the Issues line of the summary instead of silently omitting.

## Support files
- `references/lovense-emily-ai-doll.md` — condensed findings from the Aug 2026 Emily deep-dive (official specs, pricing, AI-stack status, API/RE landscape, DIY comparison, key URLs). Reuse before re-researching.
- `references/ai-doll-llm-api-landscape.md` — Aug 2026 whole-market status: who ships doll/companion hardware with LLM/API support (Realbotix app-level BYO-LLM but no dev SDK; Lovense Emily cloud-locked; UBTech U1, Noetix, Starpery, Jiggly Joy all proprietary; OSSM + buttplug/ButtplugLLM/AgenticLover as the only true BYO-LLM path; dead-end brands SynDoll/Thalanor, BOLTT, "Tempest", "Repurposed"). Reuse before re-researching.
