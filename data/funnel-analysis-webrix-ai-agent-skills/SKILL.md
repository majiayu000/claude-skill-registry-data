---
name: funnel-analysis
displayName: Funnel Analysis
tagline: Analyze conversion funnels to identify drop-off points and optimize user journeys.
description: |
  Analyzes user conversion funnels to identify where users drop off and
  why. Calculates conversion rates between steps, compares funnels across
  segments, and recommends optimizations. Supports funnels for onboarding,
  checkout, feature adoption, and custom user journeys.
department:
  - Product
  - Data & Analytics
  - Growth
use_cases:
  - Conversion Optimization
  - User Journey Analysis
  - Growth Analytics
tools_required:
  - Mixpanel MCP
  - Google Analytics MCP
agents_compatible:
  - Claude / Claude Code
  - Cursor
  - Windsurf
  - ChatGPT
  - Any MCP-compatible agent
author: Webrix
verified: true
updatedAt: 2026-05-08
version: 1.0.0
exampleInput: |
  Analyze the onboarding funnel for new users last month.
  Steps: signup -> verify email -> create project -> invite team -> first action.
exampleOutput: |
  Funnel Analysis — Onboarding (April 2026)

  CONVERSION FUNNEL
  Signup:          1,200 users (100%)
  Verify Email:    1,020 users (85%)  — 15% drop
  Create Project:  714 users (59%)    — 30% drop ⚠️
  Invite Team:     428 users (36%)    — 40% drop ⚠️
  First Action:    342 users (29%)    — 20% drop

  OVERALL CONVERSION: 29% (signup to first action)

  BIGGEST DROP-OFFS
  1. Invite Team step: 40% drop — Users skip team invite
     Recommendation: Make invite optional, show value prop
  2. Create Project: 30% drop — Friction in project setup
     Recommendation: Add project templates, reduce required fields

  SEGMENT COMPARISON
  Organic Users:     34% overall conversion
  Paid Users:        22% overall conversion
  Referral Users:    41% overall conversion
---

# Funnel Analysis

Analyze conversion funnels to identify drop-off points and optimize user journeys.

**Integrations:** Mixpanel, Google Analytics

## When to Use

- The user wants to understand where users drop off in a flow
- Conversion optimization is needed for onboarding or checkout
- The user mentions "funnel analysis", "drop-off", or "conversion rate"

## Steps

### Step 1: Define Funnel Steps

Identify the sequential steps in the user journey.

### Step 2: Calculate Conversion Rates

Compute step-by-step conversion rates and identify drop-offs.

### Step 3: Segment Analysis

Compare funnel performance across user segments.

### Step 4: Recommend Optimizations

Suggest improvements for the biggest drop-off points.

## Output

Deliver:
- Funnel visualization with conversion rates
- Drop-off analysis with root causes
- Optimization recommendations by priority
