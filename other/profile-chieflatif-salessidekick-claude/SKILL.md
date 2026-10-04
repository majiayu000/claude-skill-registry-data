---
name: profile
description: AE professional identity and context used for personalized output across all commands
tier: 3 (regenerated)
auto-fire: Nearly every session — AE identity, territory context, qualification gates
user-invocable: false
---

# Profile — AE Identity Skill

> **Tier 3 — This entire file is regenerated during /setup Phase 1-2 based on the AE's identity, company, and territory context.**

## Purpose

Contains the AE's complete professional identity: who they are, what they sell, their territory, their qualification gates, and their operating rhythm. This skill fires on nearly every session because it provides the foundational context for all other operations.

## When Referenced

- **Nearly every command** — provides AE identity context
- **/setup** — fully regenerates this file from user inputs
- **/today, /end-of-day** — uses operating rhythm for daily briefings
- **/add-company** — uses qualification gates (Hell Yes / Hell No)

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
*After /setup, these are customized to your specific market and selling motion.*

Default signals (pre-/setup):
- Decision maker identified and engaged
- Clear, quantified pain with budget allocated
- Timeline pressure exists (contract renewal, mandate, or initiative deadline)
- Champion identified who is actively advocating
- ICP fit confirmed (right industry, right size, right use case)
- Competitive landscape known and favorable

#### Hell No Signals
*After /setup, these are customized to your specific disqualification patterns.*

Default signals (pre-/setup):
- No identifiable pain or vague "exploring options" with no urgency
- Budget not allocated and no path to allocation
- Decision timeline is "someday" with no triggering event
- Primary contact has no authority and no access to authority
- Wrong industry, wrong size, or wrong use case for what we sell
- Prospect wants free consulting disguised as evaluation

### Operating Rhythm

**Daily:**
1. Morning: `/today` — tasks + deals needing attention
2. Before meetings: `/prep [Company]` — intel brief
3. After calls: `/closeout` — 6-Output Framework processing
4. End of day: `/end-of-day` — review and preview

**Weekly:**
1. Monday: `/weekly` — territory pipeline summary
2. Friday: `/forecast-update` — CRM forecast

**As needed:**
- `/strategy`, `/battle`, `/pov` for deal strategy
- `/pipeline`, `/whitespace` for territory management
- `/research`, `/outreach`, `/email` for account engagement

### Cognitive Profile
*After /setup, this section captures how the AE thinks, processes information, and makes decisions.*

Default (pre-/setup):
- **Communication style:** {{COMMUNICATION_STYLE}}
- **Decision-making approach:** Data-informed but relationship-driven
- **Preferred feedback style:** Direct, specific, actionable
- **Time management preference:** Structured with flexibility for reactive needs

## Personalization Notes

- **This entire file is Tier 3** — fully regenerated during /setup Phase 1 (Identity) and Phase 2 (Company Intel)
- All {{TEMPLATE_VARIABLES}} are populated during /setup
- Qualification gates (Hell Yes/Hell No) are customized based on user's ICP and market
- Cognitive profile is built from /setup interview responses
- Operating rhythm is universal structure but specific commands may be adjusted based on user preferences

### First-Use Calibration Storage (/deck)

On the first run of `/deck`, the user is asked how they prefer presentations (data-heavy, narrative, or visual). The preference is stored here:

- **Deck style preference:** [Populated on first /deck run — data-heavy / narrative / visual]
- **Slide density notes:** [Any additional preferences about content density, chart usage, or layout]

This preference informs template selection and slide content density for all future /deck calls.
