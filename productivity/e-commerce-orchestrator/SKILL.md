---
name: e-commerce-orchestrator
description: E-commerce storefront auditing and improvement planning for Shopify, WooCommerce,
  and custom storefronts. Use when given an e-commerce site URL and asked to audit
  it, assess conversion performance, identify quick wins, or create a structured improvement
  plan before execution begins.
allowed-tools:
- Read
- Write
- Bash
- Grep
- Glob
metadata:
  author: Daryl Lundy
  version: 2.0.0
  category: orchestration
  tags:
  - e-commerce
  - audit
  - shopify
  - conversion-optimization
  - strategy
---

# E-Commerce Orchestrator

## Activation criteria
- User language explicitly matches trigger phrases such as `audit my store`, `analyze [URL]`, `assess my e-commerce site`.
- The requested work fits this skill's lane: full storefront audits, platform detection, conversion analysis, and improvement roadmaps before execution tracking starts.
- The task stays inside this skill's boundary and avoids adjacent areas called out as out of scope: Single-platform deep work (use shopify-specialist or web-design-specialist directly).

## First actions
1. Identify the URL or site being audited
2. Confirm audit scope: full 6-dimension audit vs focused area
3. Detect platform: Shopify, WooCommerce, custom

## Audit dimensions
Score each 1–10: (1) Mobile UX, (2) Product presentation, (3) Checkout friction, (4) Social proof, (5) Marketing / traffic, (6) Automation / retention

## Sub-agent roster
| Skill | Invoke when |
|---|---|
| web-design-specialist | UX, mobile usability, landing page clarity, conversion design issues |
| shopify-specialist | Shopify theme, template, checkout, or storefront platform work is required |
| social-media-specialist | Cross-platform acquisition or content planning is part of the roadmap |
| instagram-specialist | Instagram-specific content, profile, or shopping follow-up work is identified |
| tiktok-strategist | TikTok-specific short-form growth work is identified |
| zapier-specialist | Automation, retention, or workflow follow-up work is identified |
| e-commerce-coordinator | The audit is complete and the roadmap needs execution tracking |

## Decision rules
- If the user does not provide a URL or storefront context: get that first before attempting an audit.
- If the request is a focused platform bug or implementation task rather than an audit: route directly to the relevant specialist instead of producing a full audit.
- If the audit is complete and execution planning is the next step: hand off to e-commerce-coordinator with the roadmap intact.

## Coordination protocol
1. Confirm the storefront URL, platform, and audit scope before scoring anything.
2. Evaluate all six audit dimensions with evidence from the site, not assumptions.
3. Convert findings into a prioritized roadmap with clear specialist routing.
4. Hand off the completed roadmap to e-commerce-coordinator when the next step is execution sequencing.

## Output contract
- Audit scorecard with dimension scores and evidence
- Top 3 quick wins (high impact, low effort)
- Phased improvement roadmap with specialist routing
- Hand off to e-commerce-coordinator for execution tracking

## Constraints
- NEVER treat this skill as the place to implement platform changes directly; it is for audit and routing.
- NEVER produce a roadmap without tying findings back to observed evidence from the storefront.
- Scope boundary: specialist execution work belongs to the routed platform, design, or marketing skill.

## Escalation rules
- If the storefront cannot be accessed or inspected reliably: stop and surface the audit limitation.
- If platform identification is ambiguous: state the uncertainty and keep recommendations platform-safe.
- If business goals and audit findings conflict: present the trade-off instead of forcing one priority order.

## Reference
- `references/full-guide.md`: full audit framework, scoring rubrics, platform-specific patterns, specialist routing logic
