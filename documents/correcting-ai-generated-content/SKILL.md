---
name: correcting-ai-generated-content
description: >
  Audits AI-generated documents, NotebookLM exports, and Google Drive research
  files for factual gaps, missing production constraints, outdated information,
  and unverified claims. Runs web search to fill each gap. Rebuilds a corrected
  version in the target brand voice with [SOURCED]/[GENERATED] tagging
  throughout. Activate when user says: "this has gaps", "audit this NLM doc",
  "there's missing info", "surface the gaps", "fact-check this", "rebuild with
  real sources", "correct this article", "AI content needs verification",
  "update with current info", "notebooklm export needs work", "the AI got this
  wrong", "what's missing here", "this is incomplete", "the doc is shallow",
  or uploads a Drive or NLM doc asking for a corrected or improved version.
  FAIL if rebuilt output ships without web search on top 3 gaps. FAIL if
  CLAIMS/GAPS footers omitted. FAIL if [SOURCED]/[GENERATED] tags missing.
version: "1.0.0"
---

# Correcting AI-Generated Content

Three-phase workflow: **Audit → Search → Rebuild.**

For voice rebuild targets (lb-essay, FlashFusion B2B) and detailed search
protocol, see `references/`.

---

## Phase 1 — Audit

Read the full document. Produce this structured audit before touching content:

```
CLAIMS INVENTORY
- [Claim] → [Verified / Needs verification / Likely outdated / Unsubstantiated]

TOP GAPS (prioritized, max 5)
1. [Gap] — why it matters
2. ...

STRUCTURAL ISSUES
- [Missing section / wrong framing / incomplete decision framework]

VOICE ISSUES
- [Drift patterns, register mismatches, banned phrases]

SEARCH QUEUE
1. [Query for gap 1]
2. [Query for gap 2]
3. [Query for gap 3]
```

Do not start Phase 3 until audit is complete. Skip confirmation only if
user explicitly says to proceed.

---

## Phase 2 — Search

Run web searches from the Search Queue. For each gap:
- Search with a specific, current query (include year if recency matters)
- Fetch the most authoritative source (official docs > primary research > aggregators)
- Tag results [SOURCED] with source name + date, or [GENERATED] with reasoning
- Do not proceed to Phase 3 until top 3 gaps have search results

See `references/search-protocol.md` for priority ordering and source rules.

---

## Phase 3 — Rebuild

Reconstruct in the target surface format with sourced claims replacing assertions.

Surface options: `lb-essay` · `ff-b2b` · `plain-markdown`

See `references/rebuild-targets.md` for voice rules, CSS tokens, and
structure per surface.

Every rebuild must include CLAIMS and GAPS footers with [SOURCED]/[GENERATED]
tagging on every factual claim.

---

## Gotchas

- **04_Knowledge NLM deposits are unsafe.** Kyle's Drive `04_Knowledge` folder
  contains confirmed fabricated product names, invented events, and unverified
  case studies. Never use as a source without independent verification.
- **NLM exports strip production constraints.** The audit almost always
  surfaces missing failure modes, cost tradeoffs, and "what this doesn't
  tell you" content.
- **Voice rebuilds require restructuring, not editing.** Announcement openers
  and summarizing closers in AI-generated content are structural. Edit in place
  and you get a hybrid that satisfies neither register. Rewrite from the opener.
- **Model-generated precision is a red flag.** "60-80% improvement,"
  "99% of developers" — always verify specific numbers before repeating.
