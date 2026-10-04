---
name: profile
description: "Fires on nearly every session. Provides: AE identity (name, title, company, product), territory context (type, size, region, quota), ICP definition, qualification gates (Hell Yes / Hell No signals), operating rhythm (daily, weekly cadence). Output contract: all outputs are personalized to this specific AE's role, territory, and selling motion."
user-invocable: false
---

# Profile — AE Identity Skill

> **Tier 3 — This entire file is regenerated during deep personalization Phase 1-2 based on the AE's identity, company, and territory context.**

## Purpose

Contains the AE's complete professional identity: who they are, what they sell, their territory, their qualification gates, and their operating rhythm. This skill fires on nearly every session because it provides the foundational context for all other operations.

## When Referenced

- **Nearly every interaction** (all intents) — provides AE identity context, territory parameters, and operating rhythm as foundational context for all outputs
- **Deep personalization sessions** (customize-system intent) — fully regenerates this file from user inputs during calibration
- **Morning briefings and evening wrap-ups** (start-my-day, end-my-day intents) — uses operating rhythm for daily planning and review
- **Adding new accounts** (add-account intent) — uses qualification gates (Hell Yes / Hell No) to assess fit

## Core Framework

### AE Identity

**Name:** {{AE_NAME}}
**Title:** {{AE_TITLE}}
**Company:** {{COMPANY}} ({{COMPANY_URL}})
**Manager:** {{MANAGER_NAME}}
**Team:** {{TEAM_NAME}}
**Region:** {{REGION}}

### What We Sell

**Primary Product:** {{PRIMARY_PRODUCT}}
**Additional Products:** {{SECONDARY_PRODUCTS}}
**Description:** {{PRODUCT_DESCRIPTION}}

### Territory Context

**Territory Type:** {{TERRITORY_TYPE}}
**Territory Size:** {{TERRITORY_SIZE}} accounts
**Quota:** {{QUOTA_AMOUNT}}
**Fiscal Year Start:** {{FISCAL_YEAR_START}}
**Average Deal Size:** {{AVERAGE_DEAL_SIZE}}
**Average Sales Cycle:** {{SALES_CYCLE_LENGTH}}
**CRM:** {{CRM_SYSTEM}}

### Ideal Customer Profile (ICP)

**Target Industry:** {{ICP_INDUSTRY}}
**Target Size:** {{ICP_SIZE}}
**Target Use Case:** {{ICP_USE_CASE}}

### Qualification Gates

#### Hell Yes Signals
*After deep personalization, these are customized to your specific market and selling motion.*

Default signals (before deep personalization):
- Decision maker identified and engaged
- Clear, quantified pain with budget allocated
- Timeline pressure exists (contract renewal, mandate, or initiative deadline)
- Champion identified who is actively advocating
- ICP fit confirmed (right industry, right size, right use case)
- Competitive landscape known and favorable

#### Hell No Signals
*After deep personalization, these are customized to your specific disqualification patterns.*

Default signals (before deep personalization):
- No identifiable pain or vague "exploring options" with no urgency
- Budget not allocated and no path to allocation
- Decision timeline is "someday" with no triggering event
- Primary contact has no authority and no access to authority
- Wrong industry, wrong size, or wrong use case for what we sell
- Prospect wants free consulting disguised as evaluation

### Operating Rhythm

**Daily:**
1. Morning: morning briefing — tasks + deals needing attention
2. Before meetings: meeting prep — intel brief
3. After calls: call processing — 6-Output Framework processing
4. End of day: evening wrap — review and preview

**Weekly:**
1. Monday: weekly summary — territory pipeline summary
2. Friday: forecast update — CRM forecast

**As needed:**
- deal strategy, competitive analysis, business case for deal strategy
- pipeline review, whitespace analysis for territory management
- account research, outreach, contextual email for account engagement

### Cognitive Profile
*After deep personalization, this section captures how the AE thinks, processes information, and makes decisions.*

Default (before deep personalization):
- **Communication style:** {{COMMUNICATION_STYLE}}
- **Decision-making approach:** Data-informed but relationship-driven
- **Preferred feedback style:** Direct, specific, actionable
- **Time management preference:** Structured with flexibility for reactive needs

## Personalization Notes

- **This entire file is Tier 3** — fully regenerated during deep personalization Phase 1 (Identity) and Phase 2 (Company Intel)
- All {{TEMPLATE_VARIABLES}} are populated during deep personalization
- Qualification gates (Hell Yes/Hell No) are customized based on user's ICP and market
- Cognitive profile is built from deep personalization interview responses
- Operating rhythm is universal structure but specific commands may be adjusted based on user preferences

### First-Use Calibration Storage (Presentation)

On the first run of the presentation capability, the user is asked how they prefer presentations (data-heavy, narrative, or visual). The preference is stored here:

- **Deck style preference:** [Populated on first presentation run — data-heavy / narrative / visual]
- **Slide density notes:** [Any additional preferences about content density, chart usage, or layout]

This preference informs template selection and slide content density for all future presentation requests.
