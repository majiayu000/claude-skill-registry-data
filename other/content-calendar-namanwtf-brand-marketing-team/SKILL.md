---
name: content-calendar
description: Automated content planning, scheduling, and publishing across all platforms
author: "@namanwtf"
version: 3.0.0
requires: brand-context, social-content, copywriting
category: content
---

# 📅 Content Calendar Agent

**Purpose:** Never miss a post. Plan, schedule, and publish content across all platforms with AI-powered optimization.

---

## When to Use

```bash
# Create monthly content plan
@content-calendar plan --month april

# Schedule posts for the week
@content-calendar schedule --week

# Auto-publish approved content
@content-calendar publish --approved

# Reschedule based on performance
@content-calendar optimize

# View calendar
@content-calendar view
```

---

## Capabilities

### 1. Strategic Planning
- Monthly content themes based on goals
- Seasonal/event-based content suggestions
- Platform-specific content mix
- Content pillar balancing
- Evergreen content identification

### 2. Smart Scheduling
- Optimal posting times per platform
- Audience activity analysis
- Frequency optimization
- Cross-platform coordination
- Timezone-aware publishing

### 3. Content Generation
- Auto-generate captions from briefs
- Hashtag suggestions per platform
- Content repurposing (blog → social)
- Variation creation (A/B testing)
- UGC curation

### 4. Publishing Automation
- One-click multi-platform publish
- Approval workflows
- Auto-resize for platform specs
- Story/reel generation from posts
- Emergency pause/resume

---

## Usage Examples

### Monthly Planning
```
User: @content-calendar plan --month april --goal "product-launch"

Agent: 📅 APRIL CONTENT CALENDAR

Theme: Product X Launch

Week 1 (Apr 1-7): TEASER PHASE
Mon: Mystery countdown (Instagram Story)
Tue: "Something big is coming" (Twitter)
Wed: Behind-the-scenes factory tour (YouTube Short)
Thu: Spec leak hint (Reddit)
Fri: Teaser video drop (TikTok/Reels)
Sat: User poll: "What do you want most?" (All platforms)
Sun: Rest

Week 2 (Apr 8-14): LAUNCH WEEK
Mon: OFFICIAL LAUNCH DAY 🚀
    • Morning: Announcement (All platforms)
    • Afternoon: Influencer unboxing (Instagram)
    • Evening: Live Q&A (YouTube)
Tue: Feature deep-dive: Battery (Blog + Social)
Wed: Gaming performance showcase (TikTok/Shorts)
Thu: Camera comparison vs competitors (YouTube)
Fri: User testimonials (Instagram/Twitter)
Sat/Sun: Community engagement

Week 3-4: SUSTAIN
[Detailed schedule continues...]

Total Posts: 45
Platforms: Instagram, Twitter, TikTok, YouTube, LinkedIn
Estimated Engagement: +150% vs last month
```

### Weekly Scheduling
```
User: @content-calendar schedule --week

Agent: 📆 THIS WEEK'S SCHEDULE

MONDAY:
• 9:00 AM (Instagram): Motivational quote graphic
• 11:00 AM (LinkedIn): Industry insight article
• 3:00 PM (Twitter): Poll about phone features

TUESDAY:
• 10:00 AM (TikTok): Product demo video
• 2:00 PM (Instagram): User-generated content repost
• 6:00 PM (YouTube): Long-form review

[Full week schedule...]

All posts optimized for:
✅ Peak engagement times
✅ Platform best practices
✅ Hashtag research
✅ Caption variations

Ready to approve? [Approve All] [Review One by One]
```

### Performance Optimization
```
User: @content-calendar optimize

Agent: 📊 CALENDAR OPTIMIZATION

Insights from Last 30 Days:
• Best Instagram time: 11 AM (not 9 AM currently)
• Best TikTok time: 7 PM (correct)
• Tuesday posts underperforming
• Video content 3x better engagement

Changes Applied:
✅ Shifted Instagram posts to 11 AM
✅ Moved Tuesday content to Wednesday
✅ Increased video ratio from 30% to 60%
✅ Reduced text-only posts

Expected Impact:
• Engagement: +35%
• Reach: +28%
• Clicks: +42%
```

---

## Configuration

```yaml
content-calendar:
  platforms:
    instagram:
      frequency: 1  # posts per day
      best-times: ["11:00", "19:00"]
      content-mix: [0.4, 0.3, 0.3]  # images, videos, stories
    
    twitter:
      frequency: 3
      best-times: ["09:00", "13:00", "17:00"]
      
    linkedin:
      frequency: 1
      best-times: ["08:00", "12:00"]
      days: ["tue", "wed", "thu"]
      
  workflow:
    auto-publish: false  # require approval
    approval-reminder: 24  # hours before
    buffer-days: 3  # schedule ahead
```

---

*Part of the Brand Marketing Team framework.*
*Author: @namanwtf | Version 3.0.0 | MIT License*
