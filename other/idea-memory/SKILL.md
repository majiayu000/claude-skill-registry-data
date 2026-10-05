---
name: idea-memory
description: Scout research skill — Idea Memory
---

# Skill: Idea Memory & Anti-Repetition

Track everything. Never repeat yourself. Learn from patterns.

## Storage
Use Supabase table: scout_ideas (schema below)

## Before Every Research Cycle
1. Query scout_ideas for last 30 days
2. Extract: sectors covered in last 7 days, product types sent in last 10 days
3. HARD RULES:
   - No same sector within 5 days
   - No same product type within 10 days
   - No idea that's substantially similar to anything sent in the last 30 days
4. Pick research sectors that are DUE for rotation

## After Every Report
Insert a record:
- date: today
- status: 'sent' or 'killed'
- title: one-line idea summary
- sector: from the sector list below
- product_type: from the product type list below
- confidence_score: overall score (null if killed)
- demand_score: demand validation score
- revenue_confidence: high/medium/low
- distribution_difficulty: easy/medium/hard
- founder_fit: strong/moderate/weak
- kill_reason: why it died (null if sent)
- summary: 2-3 sentence description
- build_time_estimate: estimated build time
- pricing_model: revenue model
- primary_channel: main distribution channel

## Sector Tags
devtools, fintech, healthtech, edtech, proptech, creator-economy, smb-tools, enterprise, consumer, marketplace, ecommerce, vertical-saas, api-infrastructure, ai-ml-tools, legaltech, hrtech, climatetech, logistics, foodtech, sportstech, media-content, cybersecurity, insurtech, govtech, nonprofit-tools, construction-tech, automotive, travel-hospitality, agriculture, gaming

## Product Type Tags
dashboard, workflow-automation, marketplace, api-wrapper, content-tool, analytics-platform, communication-tool, booking-scheduling, crm, internal-tool, monitoring-alerting, ai-assistant, browser-extension, data-pipeline, calculator-planner, directory-listing, template-library, integration-middleware, billing-invoicing, feedback-survey, social-tool, comparison-tool

## Monthly Self-Assessment (1st of each month)
Send a Telegram summary:
- Total ideas sent vs killed this month
- Sectors covered (and any gaps)
- Average confidence score
- Top 3 ideas by confidence score
- Most common kill reasons (patterns to watch)
- Source quality: which research sources produced the best ideas
- Recommendation: any adjustments needed to the research strategy
