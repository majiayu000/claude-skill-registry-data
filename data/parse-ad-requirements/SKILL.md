---
name: parse-ad-requirements
description: Extract structured advertising campaign parameters from natural language input provided by advertisers. This skill should be used when analyzing advertising requirements, campaign briefs, or ad requests that need to be converted into structured data. Supports both creating new campaigns and updating existing campaigns with additional information. Identifies missing information and provides helpful guidance for completing campaign requirements.
---

# Parse Advertising Requirements

## Overview

Extract structured advertising campaign parameters from natural language input provided by advertisers. Supports creating new campaigns and updating existing campaigns with additional information. Identify missing information and provide helpful guidance for completing campaign requirements.

## When to Use This Skill

Use this skill when:
- Analyzing advertising requirements or campaign briefs
- Converting natural language ad requests into structured data
- Creating a new advertising campaign from natural language input
- Updating an existing campaign with additional information
- Identifying missing or incomplete campaign information
- Validating that all necessary advertising parameters are provided
- Processing advertiser input for campaign setup

## Workflow

When given a natural language campaign description, follow this step-by-step workflow:

### Step 1: Extract Campaign Parameters

Analyze the input text and extract the following 12 fields:

1. **product_or_service**: The product, service, or brand being advertised
   - Examples: "fitness app", "organic coffee brand", "SaaS platform"

2. **product_or_service_url**: Website or landing page URL for the product/service
   - Examples: "https://myfitnessapp.com", "www.coffeebrand.com"

3. **campaign_name**: A descriptive name for this campaign
   - Examples: "Summer Fitness Launch", "Q4 Brand Awareness"

4. **target_audience**: Demographics, interests, or characteristics of the target audience
   - Examples: "women aged 25-35", "tech-savvy millennials", "small business owners"

5. **geography**: Geographic targeting for the campaign
   - Examples: "Southeast Asia", "United States", "Global", "New York City"

6. **ad_format**: Type of ad creative needed
   - Examples: "video ad", "carousel ad", "static image", "story ad"

7. **budget**: Campaign budget amount and currency
   - Examples: "$5,000", "€10,000", "5000 USD"

8. **platform**: Advertising platform(s) to use
   - Examples: "TikTok", "Facebook", "Instagram", "Google Ads", "LinkedIn"

9. **kpi**: Key performance indicators or success metrics
   - Examples: "CTR", "app installs", "conversions", "brand awareness", "engagement rate"

10. **time_period**: Campaign duration or timeline
    - Examples: "2 weeks", "Q1 2024", "ongoing", "launch in March"

11. **creative_direction**: Style, tone, or creative requirements
    - Examples: "energetic and motivating", "professional and trustworthy", "fun and playful"

12. **other_details**: Any additional requirements or context
    - Examples: "must include testimonials", "competitor: BrandX", "seasonal theme"

### Step 2: Identify Missing Fields

For each field:
- If the information is explicitly stated or can be reasonably inferred, populate the field
- If the information is not present or unclear, mark it as missing

### Step 3: Return Structured Output

Return a JSON object with this structure:

```json
{
  "success": true/false,
  "parameters": {
    "product_or_service": "value or null",
    "product_or_service_url": "value or null",
    "campaign_name": "value or null",
    "target_audience": "value or null",
    "geography": "value or null",
    "ad_format": "value or null",
    "budget": "value or null",
    "platform": "value or null",
    "kpi": "value or null",
    "time_period": "value or null",
    "creative_direction": "value or null",
    "other_details": "value or null"
  },
  "missingFields": ["field1", "field2"],
  "suggestions": {
    "field1": "Consider specifying...",
    "field2": "You might want to include..."
  }
}
```

- Set `success` to `true` only if ALL fields are populated (no missing fields)
- Set `success` to `false` if any fields are missing
- List all missing field names in the `missingFields` array
- Optionally provide helpful suggestions for missing fields

## Campaign Updates

When updating an existing campaign (indicated by context mentioning a campaign ID):
- Extract only the NEW information provided in the input
- Set fields to their extracted values if new information is provided
- Set fields to `null` if no new information is provided for that field
- The system will automatically merge new values with existing campaign data
- Only newly provided fields will overwrite existing values; null fields preserve existing data

## Extraction Rules

1. **Be Conservative**: Only populate a field if the information is clearly stated or strongly implied
2. **Use Null for Missing**: If a field is not mentioned, set it to `null` rather than guessing
3. **Preserve Original Phrasing**: When extracting, use the advertiser's own words when possible
4. **Infer Carefully**: Some fields can be inferred (e.g., if they mention "TikTok video", ad_format is "video ad" and platform is "TikTok")
5. **Handle Ambiguity**: If information is ambiguous, mark the field as missing and suggest clarification

## Examples

### Example 1: Partially Complete Input

**Input**: "Create a TikTok video ad for my fitness app targeting Southeast Asian women aged 25-35 with a $5,000 budget. The goal is to drive app installs with an energetic and motivating tone."

**Output**:
```json
{
  "success": false,
  "parameters": {
    "product_or_service": "fitness app",
    "product_or_service_url": null,
    "campaign_name": null,
    "target_audience": "Southeast Asian women aged 25-35",
    "geography": "Southeast Asia",
    "ad_format": "video ad",
    "budget": "$5,000",
    "platform": "TikTok",
    "kpi": "app installs",
    "time_period": null,
    "creative_direction": "energetic and motivating",
    "other_details": null
  },
  "missingFields": ["product_or_service_url", "campaign_name", "time_period"],
  "suggestions": {
    "product_or_service_url": "Please provide the landing page or app store URL for your fitness app",
    "campaign_name": "Consider providing a campaign name for tracking purposes (e.g., 'Q1 2024 Southeast Asia Launch')",
    "time_period": "When should this campaign run? Specify duration or dates (e.g., '2 weeks', 'March 1-15')"
  }
}
```

### Example 2: Minimal Input

**Input**: "I need ads for my coffee brand"

**Output**:
```json
{
  "success": false,
  "parameters": {
    "product_or_service": "coffee brand",
    "product_or_service_url": null,
    "campaign_name": null,
    "target_audience": null,
    "geography": null,
    "ad_format": null,
    "budget": null,
    "platform": null,
    "kpi": null,
    "time_period": null,
    "creative_direction": null,
    "other_details": null
  },
  "missingFields": [
    "product_or_service_url",
    "campaign_name",
    "target_audience",
    "geography",
    "ad_format",
    "budget",
    "platform",
    "kpi",
    "time_period",
    "creative_direction"
  ],
  "suggestions": {
    "target_audience": "Who is your ideal customer? (e.g., coffee enthusiasts aged 25-45, young professionals)",
    "platform": "Where do you want to advertise? (e.g., Instagram, Facebook, Google, TikTok)",
    "budget": "What is your advertising budget? Please include currency",
    "geography": "Which geographic region should we target? (e.g., United States, Europe, specific cities)",
    "ad_format": "What type of ad creative? (e.g., video ad, static image, carousel)",
    "kpi": "What success metrics matter most? (e.g., brand awareness, website traffic, sales conversions)"
  }
}
```

### Example 3: Complete Input

**Input**: "Run an Instagram carousel ad campaign called 'Spring Coffee Collection' for our organic coffee brand at www.organicbrew.com. Target coffee enthusiasts aged 25-45 in the United States with a $10,000 budget. Campaign runs for 3 weeks starting March 1st. Focus on conversions (online purchases). Use a warm and inviting tone that emphasizes sustainability. Include customer testimonials in the creative."

**Output**:
```json
{
  "success": true,
  "parameters": {
    "product_or_service": "organic coffee brand",
    "product_or_service_url": "www.organicbrew.com",
    "campaign_name": "Spring Coffee Collection",
    "target_audience": "coffee enthusiasts aged 25-45",
    "geography": "United States",
    "ad_format": "carousel ad",
    "budget": "$10,000",
    "platform": "Instagram",
    "kpi": "conversions (online purchases)",
    "time_period": "3 weeks starting March 1st",
    "creative_direction": "warm and inviting tone that emphasizes sustainability",
    "other_details": "Include customer testimonials in the creative"
  },
  "missingFields": [],
  "suggestions": {}
}
```

## Important Notes

- Always return valid JSON
- Ensure all 12 parameter fields are present in the output
- The `success` field should reflect whether ALL required information is present
- Be helpful and specific in suggestions
- Maintain a professional, friendly tone when providing suggestions
- When updating campaigns, only extract NEW information from the input
- Null values in updates preserve existing campaign data (they don't delete it)
