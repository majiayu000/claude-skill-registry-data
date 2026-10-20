---
name: product-deepsearch
description: Use this skill to conduct high-fidelity, verified deep web research by
  coordinating multiple specialized subagents, leveraging Chromium browser sessions
  for visual verification of sources, and synthesizing a validated report with citations.
category: analysis
risk: safe
source: local
tags: '[research, multi-agent, browser, validation]'
date_added: '2026-07-07'
user-invocable: true
---
# Skill: Product Deep Research (product-deepsearch)

This skill should be used when the user requests detailed, verified, and up-to-date information on a complex topic, market trend, tool comparison, or technical solution where standard single-step web searching is insufficient or likely to return superficial, outdated, or biased results.

## 1. Core Architecture & Workflow

To achieve maximum accuracy and bypass the limitations of linear web searches, you MUST follow this 5-phase research workflow:

### Phase 1: Query Deconstruction & Planning
1. Deconstruct the user's research request into 3–5 distinct research angles or sub-questions:
   - **Angle A (Core Facts):** What is the established state?
   - **Angle B (Recent Changes):** What has changed recently (specifically checking 2025–2026 data)?
   - **Angle C (Contradictions/Biases):** What are the competing views, limitations, or potential marketing hype?
   - **Angle D (Verification):** What primary sources (documentation, official press releases, GitHub repos) can confirm these claims?

### Phase 2: Subagent Delegation
1. Do not perform all searches in a single linear thread. Define and invoke specialized subagents using `define_subagent` and `invoke_subagent`:
   - `research-primary`: Tasked with gathering the bulk of the raw facts and citations.
   - `fact-checker`: Tasked with verifying specific numbers, release dates, and finding opposing viewpoints or alternative solutions.
2. Monitor subagent outputs and coordinate their findings.

### Phase 3: Visual & Structural Verification (Chromium / Browser Subagent)
1. For critical or high-ambiguity sources (e.g., complex pricing pages, documentation tables, dynamic web apps):
   - Invoke `browser_subagent` to navigate directly to the target URL.
   - Take screenshots of the page content to bypass paywalls, cookie banners, or complex layouts that confuse standard text scrapers.
   - Verbally or visually verify that the content is rendering correctly and matches the extracted text.

### Phase 4: Synthesis & Cross-Verification
1. Gather all subagent reports and construct a verification matrix.
2. **Date Audit:** Filter out outdated sources. If a source is older than 12 months, search specifically for updates to verify if the information is still valid in 2026.
3. **Consensus Check:** A critical claim (e.g., feature support, pricing, performance metrics) must be verified by at least **two independent sources** before being accepted as fact. If sources conflict, highlight the discrepancy.

### Phase 5: Raporlama (Reporting)
1. Write the final report **in Turkish** (unless the user explicitly requests otherwise).
2. The report structure must follow:
   - **Özet (Executive Summary):** A high-level overview of the findings (max 200 words).
   - **Bulgular (Key Findings):** Structured sections matching the deconstructed research angles.
   - **Doğrulama ve Kaynaklar (Sources & Verification):** A markdown table containing:
     - Verified Claim
     - Source Website / Organization
     - Direct URL
     - Verification Date & Status (e.g., "Verified via Screenshot", "Confirmed by 2+ sources")
   - **Açık Noktalar / Belirsizlikler (Uncertainties/Gaps):** Any questions that remain unanswered or where sources were contradictory.

## 2. Hard Rules & Constraints

- **No Hallucinations/Assumptions:** If a detail cannot be found after searching at least 3 distinct search queries, declare it as "Bulunamadı" (Not Found) rather than guessing.
- **Visual Grounding:** Always use the `browser_subagent` to take screenshots of the primary source's UI/Documentation when verifying pricing models, system architectures, or product features.
- **Link Integrity:** All URL links included in the report must be active and point directly to the specific page containing the information, not generic homepages.
- **Anti-Hype Filter:** Actively strip marketing jargon (e.g., "revolutionary", "seamless", "next-gen") and replace it with objective capability metrics.
