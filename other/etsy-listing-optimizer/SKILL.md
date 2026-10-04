---
name: etsy-listing-optimizer
description: Audit, rewrite, prioritize, and monitor Etsy or marketplace listings using public-safe product data. Use when the user asks to optimize an Etsy listing, improve product titles, tags, descriptions, keyword fit, marketplace SEO, listing batches, shop audits, eRank-style keyword review, competitor notes, or listing refresh workflows without exposing shop exports, private metrics, customer data, credentials, raw CSVs, or live shop configuration.
---

# Etsy Listing Optimizer

## Overview

Use this skill to improve marketplace listings through a review-first workflow: audit the current listing, choose keywords, rewrite title/tags/description, prioritize batches, and define a monitoring cadence. Use fake sample data in public examples and keep private shop data out of shared outputs.

## Workflow

1. Clarify the product type, buyer intent, marketplace, and whether the user wants a single-listing rewrite, keyword review, shop audit, or batch plan.
2. Read `references/listing-constraints.md` before writing titles, tags, descriptions, image notes, or attributes.
3. Read `references/keyword-workflow.md` before choosing or rejecting keywords.
4. Read `references/batch-and-monitoring.md` before prioritizing many listings or recommending a refresh cadence.
5. Produce a concise optimization result with before/after fields, rationale, rejected keywords, review notes, and next steps.
6. Require human review before anything is pasted into a live listing, shop dashboard, ad system, or scheduling tool.

## Default Output

For a single listing, return:

1. Listing audit summary.
2. Buyer intent and positioning.
3. Optimized title.
4. Up to 13 tags.
5. Description rewrite.
6. Image, category, and attribute notes.
7. Keywords used and keywords rejected.
8. Human review checklist before publishing.

For a shop or batch, return:

1. Priority logic.
2. Batch list using fake or user-approved identifiers.
3. Recommended workflow for each listing.
4. Data freshness warnings.
5. Monitoring cadence.

## Safety Rules

- Do not publish or echo private shop exports, raw CSV rows, customer data, order data, revenue, ad data, credentials, API tokens, internal paths, or live shop configuration.
- Do not claim guaranteed ranking, sales, or platform outcomes.
- Do not recommend keyword stuffing, misleading tags, unrelated trends, trademark misuse, or competitor copying.
- Do not paste changes into a live marketplace. The user must review and apply.
- If using competitor or keyword-tool data, summarize patterns and rationale instead of exposing private exports.

## Style Rules

- Match the actual product, material, format, and use case.
- Prefer clear buyer language over awkward keyword piles.
- Keep descriptions natural and scannable.
- Use all allowed tags only when they are relevant.
- Explain tradeoffs when a strong keyword is rejected for mismatch, trademark risk, weak intent, or poor fit.
