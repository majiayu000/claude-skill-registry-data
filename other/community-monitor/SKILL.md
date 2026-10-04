---
name: community-monitor
description: Track Slack communities, Discord servers, Facebook groups, and forums for buying signals and engagement opportunities
tags: [community, monitoring, buying-signals, slack, discord, facebook-groups, lead-generation]
---

# Community Monitor

Tracks Slack communities, Discord servers, Facebook groups, and industry forums for buying signals, pain points, and engagement opportunities. Identifies prospects who are actively asking for recommendations, expressing frustrations matching your services, or seeking help in your domain. Scores signal relevance and outputs a prioritized action report with recommended engagement strategies.

## Prerequisites

- `agency.config.json` at repo root with `services`, `icp`, and optionally `outreach` sections
- WebSearch tool available
- Optional: `person-researcher` skill for enriching identified prospects
- Optional: `crm-writer` skill for logging signals to CRM
- Optional: `social-listener` skill for broader social monitoring (this skill focuses on closed communities)

## Capabilities Used

1. `signal-scanner` -- for intent signal detection patterns and keyword matching logic
2. `person-researcher` -- for enriching prospects discovered in community signals
3. `crm-writer` -- for logging high-value signals and prospects to the CRM pipeline

## Phase 0: Intake

1. Read `agency.config.json` from the project root.
2. Extract:
   - `agency.name`, `agency.domain` -- for identifying self-mentions
   - `services[].name`, `services[].keywords` -- service-related signal keywords
   - `icp.segments[].titles`, `icp.segments[].industries` -- prospect qualification criteria
   - `icp.intent_keywords` -- buying intent language patterns
   - `icp.negative_keywords` -- filter out competitors and service providers
   - `icp.primary_keywords`, `icp.secondary_keywords` -- topic relevance
3. Accept parameters:
   - `communities` -- list of specific communities to monitor. Format:
     ```json
     [
       {
         "name": "Shopify Entrepreneurs",
         "platform": "facebook_group",
         "url": "https://facebook.com/groups/shopifyentrepreneurs"
       },
       {
         "name": "eCommerce Fuel",
         "platform": "slack",
         "url": "https://ecommercefuel.com/community"
       },
       {
         "name": "Shopify Devs",
         "platform": "discord",
         "url": "https://discord.gg/shopifydevs"
       }
     ]
     ```
   - `keywords` -- additional tracking keywords beyond config (default: use config keywords)
   - `signal_types` -- filter: `buying | pain_point | recommendation_request | how_to | comparison` (default: all)
   - `time_window` -- how far back to search (default: "past 7 days")
   - `max_signals` -- max signals to return (default: 30)

## Phase 1: Community Discovery

If `communities` parameter is empty or user wants to expand, discover relevant communities:

### Facebook Group discovery:
- `site:facebook.com/groups "{service_keyword}" "{industry}"`
- `"facebook group" "{niche}" "{icp_industry}" members`
- `"join" "facebook group" "{service_keyword}"`

### Slack community discovery:
- `"slack community" "{service_keyword}" OR "{industry}" "join"`
- `site:slack.com "{niche}" community`
- `"{industry}" "slack workspace" "invite"`

### Discord server discovery:
- `site:discord.gg "{service_keyword}" OR "{industry}"`
- `"discord server" "{niche}" "{industry}" "join"`
- `site:discord.com/invite "{service_keyword}"`

### Forum discovery:
- `site:community.shopify.com "{service_keyword}"`
- `"{industry}" forum "{service_keyword}" active`
- `site:indiehackers.com "{service_keyword}"`

### For each discovered community, capture:
```json
{
  "name": "Community name",
  "platform": "facebook_group | slack | discord | forum",
  "url": "URL or invite link",
  "member_estimate": "Approximate member count if visible",
  "activity_level": "HIGH | MEDIUM | LOW",
  "relevance": "HIGH | MEDIUM | LOW",
  "join_status": "open | requires_approval | invite_only"
}
```

Compile a target list of 10-20 communities ranked by relevance and activity.

## Phase 2: Signal Keyword Generation

Build comprehensive keyword sets for signal detection:

### Buying signal keywords:
Combine `icp.intent_keywords` with:
- "looking for agency" / "need help with" / "anyone recommend"
- "hiring" / "want to hire" / "need a developer"
- "budget for" / "how much does" / "pricing for"
- "considering" / "evaluating" / "switching from"
- "RFP" / "project brief" / "scope of work"

### Pain point keywords:
- "struggling with" / "frustrated by" / "can't figure out"
- "broken" / "not working" / "lost revenue"
- "conversion dropped" / "traffic but no sales" / "high bounce rate"
- "need to fix" / "anyone else having issues with"
- Service-specific: "shopify slow" / "checkout broken" / "theme issue"

### Recommendation request keywords:
- "can anyone recommend" / "who do you use for"
- "best agency for" / "top shopify developers"
- "looking for recommendations" / "suggestions for"
- "has anyone used" / "thoughts on" / "reviews of"

### How-to keywords (lower intent but engagement opportunity):
- "how do I" / "how to" / "best way to"
- "tutorial for" / "guide to" / "help with"
- Scoped to service keywords to stay relevant

### Comparison keywords:
- "vs" / "versus" / "compared to" / "alternative to"
- "{competitor} vs" / "better than {competitor}"
- "switch from" / "migrate from" / "replace"

## Phase 3: Signal Search

Search for community discussions matching signal keywords:

### Search strategy per platform:

**Facebook Groups:**
- `site:facebook.com/groups "{community_name}" "{signal_keyword}"`
- `site:facebook.com/groups "{service_keyword}" "{intent_keyword}"`
- Note: Many FB group posts are not indexed. Supplement with general searches.

**Slack (indexed content):**
- `site:slack-archive.org OR site:linen.dev "{community_keyword}" "{signal_keyword}"`
- `"{slack_community_name}" "{service_keyword}" "{intent_keyword}"`
- Many Slack communities have public archives or linen.dev mirrors.

**Discord (indexed content):**
- `site:discord.com "{service_keyword}" "{signal_keyword}"`
- `"{discord_server_name}" "{service_keyword}" "{intent_keyword}"`
- Some Discord channels are indexed via bots or archive services.

**Forums:**
- `site:{forum_domain} "{signal_keyword}" "{service_keyword}"`
- `site:community.shopify.com "{intent_keyword}" "{service_keyword}"`
- `site:indiehackers.com "{service_keyword}" "{intent_keyword}"`

### For each signal found, extract:
```json
{
  "signal_id": "auto-generated",
  "community": "Community name",
  "platform": "facebook_group | slack | discord | forum",
  "url": "URL to the post/thread",
  "author": "Username or name",
  "author_title": "If visible (from profile snippet)",
  "posted_date": "Date if available",
  "signal_text": "Relevant excerpt (max 400 chars)",
  "signal_type": "buying | pain_point | recommendation_request | how_to | comparison",
  "keywords_matched": ["shopify", "need help", "agency"]
}
```

### Rate limiting:
- Max 3 concurrent searches
- 2-second pause between batches
- Total queries per scan: 30-50

## Phase 4: Signal Scoring

Score each signal on a 100-point scale:

### Intent strength (0-40 points):
- Explicit buying intent ("need to hire", "budget approved"): 35-40
- Strong intent ("looking for", "evaluating agencies"): 25-34
- Moderate intent ("frustrated with", "need help"): 15-24
- Low intent ("how do I", "best practices"): 5-14
- Informational only: 0-4

### ICP match (0-30 points):
- Author title matches ICP titles: +15
- Author company matches ICP industries: +10
- Community aligns with ICP segment: +5
- No ICP data extractable: +5 (benefit of the doubt)

### Recency (0-15 points):
- Posted within 24 hours: 15
- Posted within 3 days: 12
- Posted within 7 days: 8
- Posted within 14 days: 4
- Older than 14 days: 0

### Engagement opportunity (0-15 points):
- No expert has replied: +10
- Thread is active with multiple participants: +5
- Already answered comprehensively: -5
- Thread is locked or archived: -15

### Signal tiers:
- **HOT SIGNAL** (75-100): Immediate action required
- **WARM SIGNAL** (50-74): Engage within 48 hours
- **COOL SIGNAL** (25-49): Queue for weekly review
- **NOISE** (<25): Discard

## Phase 5: Engagement Strategy

For each HOT and WARM signal, generate an engagement recommendation:

### Engagement types:

**Direct helpful response:**
- Answer their question with genuine expertise
- No pitch, pure value
- Include a subtle authority signal (experience reference)
- "We've helped 3 D2C brands solve exactly this -- here's what works..."

**Resource sharing:**
- Share a relevant blog post, case study, or tool
- Must be genuinely helpful, not a disguised pitch
- "Here's a checklist we put together for this exact scenario..."

**DM follow-up:**
- After providing public value, DM with more specific help
- "I shared some tips in the thread. Happy to look at your specific situation if helpful."

**Connection request:**
- For LinkedIn-connected communities, connect with the person
- Personalized note referencing their community post

### For each signal:
```json
{
  "recommended_action": "RESPOND | DM | CONNECT | MONITOR | SKIP",
  "engagement_type": "helpful_response | resource_share | dm_followup | connection",
  "response_outline": "2-3 sentence outline of what to say",
  "tone_guidance": "Helpful expert, not salesy. Lead with value.",
  "timing": "ASAP | Within 24h | Within 48h | Queue for review",
  "escalate_to_outreach": true,
  "outreach_context": "Reference to use in follow-up email or LinkedIn message"
}
```

## Phase 6: Output

Return structured signal report:

```json
{
  "monitoring_summary": {
    "communities_scanned": 12,
    "total_signals_found": 45,
    "after_scoring": 30,
    "breakdown": {
      "hot": 4,
      "warm": 11,
      "cool": 15
    },
    "signal_types": {
      "buying": 3,
      "pain_point": 12,
      "recommendation_request": 6,
      "how_to": 15,
      "comparison": 4
    },
    "top_communities": [
      { "name": "Shopify Entrepreneurs", "signals": 8, "avg_score": 62 }
    ]
  },
  "signals": [
    {
      "signal_id": "SIG-001",
      "community": "Shopify Entrepreneurs",
      "platform": "facebook_group",
      "url": "https://...",
      "author": "John Smith",
      "signal_type": "recommendation_request",
      "signal_text": "Looking for a Shopify agency that can help with CRO. We're doing $500K/mo but our conversion rate is terrible...",
      "score": 88,
      "tier": "HOT",
      "recommended_action": "RESPOND",
      "response_outline": "Share 2-3 specific CRO quick wins for Shopify stores at that revenue level. Reference similar client results without naming.",
      "timing": "ASAP"
    }
  ],
  "community_health": [
    {
      "name": "Shopify Entrepreneurs",
      "activity_level": "HIGH",
      "signal_density": "8 relevant signals in 7 days",
      "recommendation": "MONITOR_DAILY"
    }
  ],
  "weekly_actions": {
    "respond_now": 4,
    "dm_this_week": 6,
    "queue_for_content": 8,
    "communities_to_join": ["Community X", "Community Y"]
  }
}
```

Present formatted summary:

```
COMMUNITY MONITORING REPORT
Period: {time_window}
Communities scanned: {N}
Total signals: {N} ({hot} HOT, {warm} WARM)

HOT SIGNALS -- ACT NOW ({count}):
1. [{platform}] {community} -- {signal_type}
   "{signal_text_preview}"
   Author: {author} | Score: {N}/100
   Action: {recommended_action} -- {timing}
   Approach: {response_outline}

WARM SIGNALS -- ENGAGE THIS WEEK ({count}):
1. [{platform}] {community} -- {signal_type}
   "{signal_text_preview}"
   Action: {recommended_action}

TOP COMMUNITIES BY SIGNAL DENSITY:
1. {community} -- {signal_count} signals -- Recommend: {daily/weekly monitoring}

SIGNAL TYPE BREAKDOWN:
- Buying signals: {count}
- Pain points: {count}
- Recommendation requests: {count}
- How-to questions: {count}
- Comparisons: {count}

WEEKLY ACTIONS:
- Respond to {N} threads now
- DM {N} prospects this week
- Create content addressing {N} common questions
- Join {N} new communities
```

## Phase 7: CRM Logging

If `crm-writer` is available and user approves:
- Log HOT and WARM signals to CRM with columns: Date, Community, Platform, Signal Type, Author, Score, URL, Action, Status
- Set initial status: "SIGNAL_DETECTED"
- Include engagement context for sales follow-up

## Example Usage

Trigger phrases:
- "Monitor communities for buying signals"
- "Track Slack and Discord for leads"
- "Find people asking for Shopify help in Facebook groups"
- "Scan communities for pain points we can solve"
- "Run community monitor for this week"
- "What are people asking about in our niche communities?"

```
User: Monitor Facebook groups and Slack communities for Shopify CRO buying signals
Assistant: [reads config, discovers relevant communities, builds signal keywords, searches for buying intent and pain point discussions, scores and ranks signals, generates engagement strategies for HOT signals]
```

```
User: Scan these 3 communities for signals: [Community 1, Community 2, Community 3]
Assistant: [same flow with provided communities, skips discovery phase, deep-scans each community for all signal types]
```
