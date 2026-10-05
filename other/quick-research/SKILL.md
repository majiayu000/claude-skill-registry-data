---
name: quick-research
description: Automatically perform a fast, reliable web lookup when the user conversationally says "araştırır mısın", "bir bak", "bakabilir misin", "güncel mi", "fiyatı ne", "hangisi", "doğru mu", or asks for a small low-stakes comparison or factual check. Verify the exact identity and current date, open 2–5 suitable authoritative or primary sources as needed, distinguish official/independent evidence from ads, sponsors, affiliates, sellers, and copied content, and return a concise sourced answer. Route broad, consequential, disputed, due-diligence, literature-scan, or "derin/bütün kaynaklar/yüzeysel olma" requests to deep-research; route medical/financial/legal/safety questions to the relevant specialist plus evidence-integrity-guard.
---

# Quick Research

Answer the user's actual question quickly without sacrificing source integrity. This skill owns ordinary lookups; it is not a shortened substitute for a high-stakes or broad investigation.

## Workflow

1. **Define the lookup.** Resolve exact entity/product/version/location/date and the one or two facts or comparison criteria that matter. Ask only if ambiguity would change the answer.
2. **Check freshness.** Identify which claims may have changed and use live sources for them. Never fill a current fact from model memory.
3. **Choose sources by claim.** Prefer the official/primary owner for status, rule, specification, price, schedule, or announcement. Add a strong independent source when interpretation, performance, controversy, or bias matters.
4. **Open the evidence.** Inspect the actual page or record; do not rely on a search snippet, headline, generated summary, or result ranking.
5. **Check incentives and independence.** Label seller, issuer, sponsored, affiliate, advertorial, or community sources. Several pages copying one origin count as one source.
6. **Resolve conflict.** Compare date, scope, version, geography, units, definitions, and source authority. If still unresolved, show the disagreement rather than averaging or guessing.
7. **Verify the draft.** Check names, dates, numbers, units, links, and whether every citation supports the nearby claim. Use `$evidence-integrity-guard` when available for disputed, commercial, time-sensitive, or consequential facts.

## Depth boundary

Switch to `$deep-research` when the request needs broad coverage, several research questions, due diligence, an exhaustive scan, an evidence table, deliberate counterevidence, or a consequential recommendation. Use a domain skill for medicine, finance, law, security, or another specialist decision. A simple user phrasing controls answer length, not the required safety depth.

## Output

Lead with a direct answer or winner. Then give the 2–5 facts that drive it, the relevant date/location/version, a concise caveat or conflict if any, and citations beside the claims they support. Do not force a generic report template, pricing section, pros/cons list, or minimum source count when the question does not need it.

## Rules

- Never invent or infer a source, quotation, statistic, date, price, feature, or current status.
- Never present advertising, seller copy, an affiliate ranking, or an issuer claim as independent validation.
- Never say “all sources” or “the whole market” was checked when only a small lookup was performed.
- State exactly what could not be verified or accessed.
- Keep the result compact and actionable unless the user asks for detail.
