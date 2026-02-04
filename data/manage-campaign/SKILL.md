---
name: manage-campaign
description: Retrieve and manage advertising campaign state throughout the campaign lifecycle. Use when checking campaign status, retrieving campaign data by ID, understanding campaign completion progress, or determining next steps in the campaign workflow. Triggers on requests to get campaign details, check campaign status, view campaign progress, or retrieve stored campaign data.
---

# Manage Campaign

## Overview

Retrieve and manage advertising campaign state. Campaigns progress through a defined workflow: parameters → research → ad copy → images → mixed media. This skill helps track progress and determine next steps.

## When to Use This Skill

Use this skill when:
- Retrieving campaign data by ID
- Checking campaign completion status
- Determining next workflow step
- Viewing stored campaign parameters, research, or assets
- Understanding what components are complete or pending

## Campaign Lifecycle

Campaigns follow this workflow:

```
1. parseAdRequirements → Creates campaign with parameters
2. conductAdResearch → Adds research report
3. generateAdCopy → Adds ad copy variations (A/B)
4. generateAdImages → Adds image variations (A/B)
5. generateMixedMedia → Creates final composite
```

Each step stores results in the campaign record.

## Campaign Data Structure

A campaign contains:

| Field | Description | Set By |
|-------|-------------|--------|
| id | UUID identifier | parseAdRequirements |
| parameters | Campaign parameters (product, audience, platform, etc.) | parseAdRequirements |
| research | Research report with insights and recommendations | conductAdResearch |
| ad_copy | Two ad copy variations (A/B) | generateAdCopy |
| images | Two image variations (A/B) | generateAdImages |
| mixed_media | Final composite creative | generateMixedMedia |
| selected_ad_copy_variation | User's chosen copy (A or B) | User selection |
| selected_image_variation | User's chosen image (A or B) | User selection |

## Completion Status

Check these flags to determine campaign progress:

- **hasParameters**: Campaign parameters are set
- **hasResearch**: Research report is complete
- **hasAdCopy**: Ad copy variations generated
- **hasImages**: Image variations generated
- **hasMixedMedia**: Final creative is ready
- **hasSelectedAdCopy**: User selected a copy variation
- **hasSelectedImage**: User selected an image variation
- **isComplete**: All components are present

## Workflow Guidance

### Determining Next Step

Based on completion status, recommend:

| Status | Next Action |
|--------|-------------|
| No parameters | Call parseAdRequirements |
| Parameters only | Call conductAdResearch |
| Has research | Call generateAdCopy |
| Has ad copy | Call generateAdImages |
| Has images | User selects variations, then generateMixedMedia |
| Complete | Campaign ready for deployment |

### Handling Missing Selections

Before generating mixed media:
1. Check if ad copy variation is selected
2. Check if image variation is selected
3. If not selected, prompt user to choose A or B

## Output Format

When reporting campaign status, return:

```json
{
  "campaign_id": "uuid",
  "campaign_name": "name or null",
  "status": "in_progress or complete",
  "completion": {
    "hasParameters": true,
    "hasResearch": true,
    "hasAdCopy": false,
    "hasImages": false,
    "hasMixedMedia": false,
    "hasSelectedAdCopy": false,
    "hasSelectedImage": false
  },
  "next_step": "generateAdCopy",
  "next_step_description": "Generate ad copy variations based on research insights",
  "created_at": "ISO timestamp",
  "updated_at": "ISO timestamp"
}
```

## Important Notes

- Campaign IDs are UUIDs - validate format before querying
- All campaign data is persisted in PostgreSQL
- Each workflow step updates the campaign record
- Missing components block downstream steps
- User selections are required before mixed media generation
