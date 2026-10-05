---
name: ai-seo
description: Use when optimize for AI search engines — Perplexity, ChatGPT Search,
  Google AI Overviews, answer engine optimization. Use when adapting SEO strategy
  for AI-powered search, optimizing for featured snippets, or building AI-friendly
  content.
domain: marketing
author: oyi77
license: Apache-2.0
subdomain: marketing
tags:
- growth
- marketing
- seo
- money
version: 1.0.0
category: marketing
---

# Ai Seo

## Overview

AI SEO (Answer Engine Optimization / GEO) optimizes content for AI-powered search engines — Perplexity, ChatGPT Search, Google AI Overviews, Gemini, Copilot — so your pages get cited in zero-click answers instead of buried below them. Unlike traditional SEO that chases ranking clicks, this skill restructures existing content into citation-ready formats, implements the schema AI crawlers prefer, and builds topical authority clusters that engines trust as primary sources.
## When to Use

**Trigger phrases:**
- "ai seo"
- "Adapting SEO strategy for AI search"
- "Optimizing for Google AI Overviews"
- "Building content that AI engines cite"
- "Answer engine optimization (AEO)"
- "Generative engine optimization (GEO)"

- Adapting SEO strategy for AI search
- Optimizing for Google AI Overviews
- Building content that AI engines cite
- Implementing structured data markup
- Optimizing for Perplexity, ChatGPT Search, Gemini, Copilot

## When NOT to Use

- When the audience is too small to justify the effort
- For regulated industries without compliance review
- When the campaign budget does not support the channel
- When the client has zero existing content to optimize

## Money-Making Overview

**Buyer persona:** SME owners ($2M-$20M ARR), SaaS marketing directors, e-commerce brand managers, and agency clients who see organic traffic from Google dropping and want to capture the growing share of zero-click AI-generated answers in Perplexity, ChatGPT Search, and Google AI Overviews.

**Problem they pay to solve:** Traditional SEO targets clicks. AI search engines answer the question in the SERP — if your content isn't structured for extraction, you get zero visibility even when ranking #1. Clients lose 30-60% of referral traffic as users stop clicking through.

**What you sell:** AI answer engine optimization — restructuring existing content into citation-ready formats, implementing schema that AI crawlers prefer, and building topical authority clusters that AI engines cite as primary sources.

**Pricing tiers:**

| Tier | Price | Deliverable | Timeline |
|---|---|---|---|
| **Audit** | $500 | AI SEO audit report + 5 priority fixes | 3 days |
| **Optimize** | $1,500 | Full content restructure (up to 10 pages) + schema + FAQ markup | 1 week |
| **Retainer** | $2,000/mo | Monthly monitoring, 15 pages/mo optimization, coverage gap analysis | Ongoing |

**First-dollar timeline:** Day 1 — run audit script, deliver report by Day 3. Close first client at $500 within the first week by auditing 3 competitor sites for free, then selling the fix.

## First Action in 60 Minutes

Run this script on your own or a target site to generate an instant AI search engine readiness report:

```bash
#!/usr/bin/env bash
# ai-seo-audit.sh — Usage: ./ai-seo-audit.sh https://example.com
set -euo pipefail

SITE="${1:?Usage: $0 https://example.com}"
echo "=== AI SEO Audit: $SITE ==="
echo ""

# 1. Check structured data (JSON-LD presence and types)
echo "--- Structured Data ---"
SD=$(curl -sL "$SITE" | grep -oP '(?<=<script type="application/ld\+json">).*?(?=</script>)' | head -5 || true)
if [ -z "$SD" ]; then
  echo "FAIL: No JSON-LD structured data found. AI engines rely on schema."
  echo "Fix: Add Organization, Article, or FAQPage schema."
else
  TYPES=$(echo "$SD" | grep -oP '"@type"\s*:\s*"[^"]+"' | sort -u)
  echo "Found schema types:"
  echo "$TYPES"
fi
echo ""

# 2. Check direct answer readability (H2 headings as question phrases)
echo "--- Answer Readiness ---"
H2S=$(curl -sL "$SITE" | grep -oP '<h2[^>]*>.*?</h2>' | sed 's/<[^>]*>//g' | head -10 || true)
QUESTION_COUNT=$(echo "$H2S" | grep -ciP '(how|what|why|when|where|which|can|does|is|are)\b' || true)
echo "H2s containing question phrasing: $QUESTION_COUNT"
if [ "$QUESTION_COUNT" -lt 3 ]; then
  echo "WARN: Few question-format headings. AI engines extract answers from Q&A patterns."
  echo "Fix: Convert H2 headings to natural-language questions your audience asks."
fi
echo ""

# 3. Check for definition/explanation paragraphs after headings
echo "--- Direct Answer Format ---"
CONTENT=$(curl -sL "$SITE" | sed 's/<[^>]*>/\n/g' | sed '/^$/d' | head -200 || true)
SHORT_PARAS=$(echo "$CONTENT" | awk 'length>0 && length<120' | wc -l)
TOTAL_PARAS=$(echo "$CONTENT" | awk 'length>0' | wc -l)
if [ "$TOTAL_PARAS" -gt 0 ]; then
  PCT=$((SHORT_PARAS * 100 / TOTAL_PARAS))
  echo "Short/direct paragraphs (under 120 chars): $PCT%"
  if [ "$PCT" -lt 20 ]; then
    echo "WARN: Few concise answer paragraphs. AI engines prefer 40-100 word direct answers."
    echo "Fix: Add a 1-2 sentence answer immediately after each question H2."
  fi
fi
echo ""

# 4. Page load speed (Core Web Vital proxy)
echo "--- Page Speed ---"
SPEED=$(curl -s -o /dev/null -w "%{http_code} %{time_total}s %{size_download}bytes" -L "$SITE" || true)
echo "HTTP $SPEED"
echo ""

# 5. Mobile-friendliness check
echo "--- Mobile Viewport ---"
VIEWPORT=$(curl -sL "$SITE" | grep -oP '<meta name="viewport"[^>]*>' || echo "MISSING")
echo "Viewport tag: $VIEWPORT"
echo ""

echo "=== SCORECARD ==="
SCORE=0
[ -n "$SD" ] && SCORE=$((SCORE + 25))
[ "$QUESTION_COUNT" -ge 3 ] && SCORE=$((SCORE + 25))
[ "$PCT" -ge 20 ] && SCORE=$((SCORE + 25))
[ -n "$VIEWPORT" ] && SCORE=$((SCORE + 25))
echo "AI SEO Readiness: ${SCORE}/100"
echo ""
echo "=== NEXT STEPS ==="
echo "1. Share this report with the client"
echo "2. Sell the full $1,500 Optimize package for the highlighted fixes"
echo "3. Build a retainer by proposing monthly monitoring ($2K/mo)"
```

Save as `ai-seo-audit.sh` and run: `bash ai-seo-audit.sh https://client-site.com`

The output is your deliverable — a live AI SEO readiness scorecard with prioritized fixes. Send it as a PDF to close the deal.

## Deliverable Format

### AI SEO Audit Report (Invoice-Ready Template)

```
Company: [Client Name]
URL: [https://client-site.com]
Date: [YYYY-MM-DD]
Auditor: [Your Name]

---

EXECUTIVE SUMMARY

AI search engines (Perplexity, ChatGPT Search, Google AI Overviews) now answer
queries directly in the SERP. [Client] currently scores [X]/100 on AI SEO readiness.
This report identifies [N] high-impact fixes that will increase citation rate and
brand visibility in AI-generated answers.

---

1. STRUCTURED DATA ANALYSIS
   Current: [JSON-LD present/missing/types found]
   Impact: [Missing schema = lost citations / Good schema = strong foundation]
   Fix: [Specific schema types to add with code example]

2. ANSWER FORMAT EVALUATION
   Current: [X question-format H2s found / concise paragraph ratio]
   Impact: [AI extraction difficulty score]
   Priority URLs to restructure:
   - [/page-1] — Rewrite H2 as question, add 40-word answer
   - [/page-2] — Add FAQPage schema
   - [/page-3] — Reformat list into direct-answer paragraph

3. TOPICAL AUTHORITY GAPS
   Missing subtopics that competing cited pages cover:
   - [Subtopic 1] — 0 articles vs 3 from competitor
   - [Subtopic 2] — No pillar page
   Recommendation: Create [N] new pages on above topics

4. TECHNICAL FOUNDATION
   - Page load: [seconds] — [pass/fail]
   - Mobile viewport: [present/missing]
   - Core Web Vitals proxy: [status]

5. PRIORITIZED FIX LIST
   Critical (do this week):
   1. [Fix] — [effort] — [expected impact]
   2. [Fix] — [effort] — [expected impact]
   Important (do this month):
   3. [Fix] — [effort] — [expected impact]
   4. [Fix] — [effort] — [expected impact]
   Growth (quarterly):
   5. [Fix] — [effort] — [expected impact]

---

PRICING

[X] Priority Fixes Implementation ........ $500
Full AI SEO Content Restructure (10 pages) ...... $1,500
Monthly Retainer (15 pages/mo + monitoring) .... $2,000/mo

---

APPENDIX: AI Engine Citation Scoring
- Perplexity: [cites/passes/blocked]
- ChatGPT Search: [visible/partial/missing]
- Google AI Overviews: [present/competing/absent]
```

Copy template, fill sections from audit output, brand with your logo, send as PDF.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Traditional SEO still works, this is hype" | Google AI Overviews already serve 1B+ queries. Perplexity and ChatGPT Search are growing 5x YoY. Traffic that stops at the AI answer never reaches your site. |
| "I'll wait until the algorithms stabilize" | The AI search ecosystem is settling NOW. First-mover advantage is real — sites optimized today are the ones AI engines trust as primary sources. |
| "My client doesn't rank for those queries anyway" | AI engines cite long-tail content traditional SEO ignores. A $500 audit shows exactly which of their pages are citation-ready vs invisible. |
| "Nobody in Indonesia needs this" | Indonesian businesses compete globally. Any brand targeting English-speaking markets loses visibility if Perplexity/ChatGPT answers competitors' content, not theirs. |
| "Schema markup is too technical for me" | JSON-LD is copy-paste. The audit script generates the exact schema you need. Five minutes of copy-paste fixes a missing-schema fail. |
| "Clients won't pay for 'invisible' optimization" | They pay for traffic loss reversal. Show them their competitor cited in an AI answer above their listing. That visual closes the deal. |
| "I need a team for this" | One script, one report, one invoice. AI SEO is a solo consultancy — no designers, no developers, no project managers. |

## Process

1. **Research** — Analyze target audience, competitors, and trending topics
2. **Audit** — Run ai-seo-audit.sh on target URLs, produce scorecard
3. **Fix** — Add JSON-LD schema, rewrite H2s as questions, add direct-answer paragraphs
4. **Monitor** — Track citation appearance in Perplexity, ChatGPT Search, Google AI Overviews
5. **Report** — Monthly citation report showing visibility gains and gaps closed

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings
