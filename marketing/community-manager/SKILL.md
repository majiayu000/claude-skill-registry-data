---
name: community-manager
description: Manage Discord, Reddit, and forum communities with automated engagement
author: "@namanwtf"
version: 3.0.0
requires: brand-context, social-content, copywriting
category: community
---

# 👥 Community Manager Agent

**Purpose:** Build and nurture thriving communities on Discord, Reddit, forums, and social platforms—24/7 automated engagement.

---

## When to Use

```bash
# Set up Discord server
@community-manager setup discord

# Monitor brand mentions
@community-manager monitor --platform reddit

# Engage with community
@community-manager engage --channel general

# Run community campaign
@community-manager campaign "ama-session"

# Analyze sentiment
@community-manager sentiment --week
```

---

## Capabilities

### 1. Platform Management
- Discord server setup and moderation
- Subreddit creation and management
- Forum engagement (Quora, Stack Overflow)
- Facebook Groups
- Slack communities

### 2. Automated Engagement
- Welcome new members
- Answer FAQ automatically
- Moderate discussions
- Highlight best content
- Birthday/anniversary recognition

### 3. Content Curation
- Share relevant industry news
- Spotlight community members
- Weekly roundups
- AMA coordination
- Event promotion

### 4. Sentiment & Analytics
- Community health scoring
- Sentiment analysis
- Member growth tracking
- Engagement metrics
- Crisis detection

---

## Usage Examples

### Discord Setup
```
User: @community-manager setup discord

Agent: 🤖 DISCORD SERVER CONFIGURED

Server: Brand Marketing Team Community

CHANNELS CREATED:
📢 announcements (read-only updates)
💬 general (main chat)
🎓 resources (templates, guides)
💡 show-and-tell (member work)
❓ help (support channel)
🤝 partnerships (collaborations)
🎉 wins (celebrate successes)

ROLES:
@Founder (you)
@Moderator (trusted members)
@Power User (active contributors)
@Member (default)
@New (joined <7 days)

AUTOMATION:
✅ Welcome bot: "Welcome [Name]! Check out #resources to get started"
✅ Auto-moderation: Spam detection, banned words
✅ FAQ bot: Answers common questions
✅ Reaction roles: Self-assign interests
✅ Weekly digest: Top posts summary

INTEGRATIONS:
• RSS feed from blog
• GitHub updates
• Twitter mentions
• YouTube uploads

Server invite link generated ✓
```

### Reddit Monitoring
```
User: @community-manager monitor --platform reddit

Agent: 🔍 REDDIT MONITORING ACTIVE

Tracking: "Brand Marketing Team" mentions

SUBREDDITS MONITORED:
r/marketing
r/digital_marketing
r/SEO
r/startups
r/entrepreneur
r/smallbusiness

ALERTS CONFIGURED:
🔔 Brand mention detected
🔔 Competitor comparison
🔔 "Alternative to [competitor]" posts
🔔 Feature requests
🔔 Complaint/suggestion posts

AUTO-RESPONSE RULES:
• Feature request → "Thanks! Added to roadmap: [link]"
• Bug report → DM with support ticket creation
• Praise → Thank you + share testimonial request
• Comparison → Jump in with value proposition

RECENT MENTIONS:
• r/marketing: "Anyone tried Brand Marketing Team?" → 45 comments
  → Engagement opportunity: HIGH
  
• r/startups: "Marketing automation tools under $100"
  → Jump in with pitch

Monitoring 24/7... ✓
```

### Community Campaign
```
User: @community-manager campaign "ama-session"

Agent: 🎙️ AMA CAMPAIGN LAUNCHED

Event: "Ask Me Anything" with Founder
Date: Next Thursday, 2 PM EST
Platform: Discord + Twitter Spaces

PROMOTION:
📧 Email to all users
📱 Social posts (Twitter, LinkedIn, Instagram)
📢 In-app notification
🔔 Push notification (mobile app)

PREPARATION:
✅ AMA channel created
✅ Question collection form
✅ Backup mod team scheduled
✅ Recording setup
✅ Summary template ready

SCHEDULE:
T-7 days: Announcement
T-3 days: Reminder + collect questions
T-1 day: Final reminder
T-0: Live event (1 hour)
T+1 day: Summary post

ENGAGEMENT TARGETS:
• Attendees: 200+
• Questions: 50+
• Social mentions: 100+

Auto-promotion sequence started ✓
```

### Sentiment Analysis
```
User: @community-manager sentiment --week

Agent: 📊 COMMUNITY SENTIMENT REPORT

Period: Last 7 days

OVERALL HEALTH: 87/100 (Healthy)

SENTIMENT BREAKDOWN:
😊 Positive: 78%
😐 Neutral: 15%
😞 Negative: 7%

TRENDING TOPICS:
1. Feature requests (45 mentions)
   Sentiment: Positive (excited for updates)
   
2. Pricing questions (23 mentions)
   Sentiment: Mixed (value confusion)
   
3. Competitor comparisons (18 mentions)
   Sentiment: Positive (prefer our solution)

ALERTS:
⚠️ 3 users threatening to churn
   → Flagged for retention outreach

⚠️ Feature confusion about pricing tiers
   → Need clearer documentation

💡 Power user offering to help others
   → Invite to moderator program

TOP CONTRIBUTORS:
1. @AlexM (47 helpful replies)
2. @SarahK (32 replies)
3. @TechMike (28 replies)
→ Recognition post queued

RECOMMENDATIONS:
1. Create pricing FAQ video
2. Host "feature roadmap" webinar
3. Thank top contributors publicly
```

---

## Configuration

```yaml
community-manager:
  platforms:
    discord:
      auto-moderation: true
      welcome-bot: true
      
    reddit:
      subreddits: ["marketing", "startups"]
      auto-respond: false  # manual approval
      
  engagement:
    welcome-delay: 5  # minutes
    digest-frequency: weekly
    
  alerts:
    negative-sentiment: true
    churn-risk: true
    competitor-mention: true
```

---

*Part of the Brand Marketing Team framework.*
*Author: @namanwtf | Version 3.0.0 | MIT License*
