---
name: social-content
description: Social media content creation and scheduling
author: "@namanwtf"
version: 3.0.0
requires: brand-context, copywriting
category: social
---

# 📱 Social Content Agent

**Purpose:** Create platform-optimized social media content for Instagram, LinkedIn, Twitter/X, TikTok.

---

## Platform Optimization

### Instagram
- **Carousel posts:** 5-10 slides for education
- **Reels:** 15-30 seconds, trending audio
- **Stories:** Polls, quizzes, behind-scenes
- **Best times:** Test 11 AM - 1 PM, 7 PM - 9 PM in your timezone

### LinkedIn
- **Long-form:** 1,300 characters for thought leadership
- **Polls:** High engagement
- **Best times:** 9 AM - 11 AM weekdays (local timezone)

### Twitter/X
- **Threads:** 8-12 tweets for stories
- **Single tweets:** Under 280 characters
- **Best times:** 9 AM - 11 AM, 6 PM - 8 PM (local timezone)

### TikTok
- **Length:** 15-60 seconds
- **Hook:** First 1-3 seconds critical
- **Trends:** Participate in trending sounds/challenges
- **Best times:** 7 PM - 11 PM (local timezone)

---

## Content Calendar

```yaml
Monday: Product feature highlight
Tuesday: Customer testimonial
Wednesday: Industry insight/education
Thursday: Behind the scenes
Friday: User-generated content
Saturday: Community content/fun
Sunday: Personal/founder story
```

---

## Commands

```bash
@social-content create --platform instagram --type reel
@social-content schedule --week-ahead
@social-content batch-create --count 30
@social-content analyze --engagement
```

---

## Content Types

### Educational
- How-to guides
- Industry insights
- Tips and tricks
- Myth-busting

### Engagement
- Polls and questions
- "This or that" posts
- Fill-in-the-blank
- AMA (Ask Me Anything)

### Promotional
- Product launches
- Limited-time offers
- Customer testimonials
- Case studies

### Behind-the-Scenes
- Team introductions
- Office/facility tours
- Making-of content
- Day-in-the-life

---

## Usage Examples

### Create Instagram Reel
```
User: @social-content create --platform instagram --type reel --topic "product-demo"

Agent: 🎬 REEL CREATED

Hook (0-3 sec): "Stop scrolling if you hate [problem]"

Script:
0-3s: Hook + problem agitation
3-8s: Solution introduction
8-20s: Product demonstration
20-25s: Social proof
25-30s: CTA

Caption:
Tired of [problem]? 😤

We built [solution] to fix that.

✅ Benefit 1
✅ Benefit 2
✅ Benefit 3

Link in bio to try it free →

#hashtag1 #hashtag2 #hashtag3
```

### Create LinkedIn Post
```
User: @social-content create --platform linkedin --type thought-leadership

Agent: 💼 LINKEDIN POST CREATED

[Opening hook - contrarian take or personal story]

[3-5 paragraphs expanding on the idea]
• Point 1 with insight
• Point 2 with data
• Point 3 with actionable advice

[Closing with question to drive engagement]

What's your experience with this?

#IndustryTag #ThoughtLeadership #Business
```

---

## Best Practices

- Post consistently (minimum 3-5x per week per platform)
- Engage with comments within first hour
- Use platform-native features (Reels, Stories, Polls)
- A/B test posting times for your audience
- Track engagement rate, not just follower count

---

## Related Skills

- **copywriting**: Caption and copy creation
- **analytics-dashboard**: Performance tracking
- **competitive-intel**: Competitor social monitoring

---

*Part of the Brand Marketing Team framework.*
*Author: @namanwtf | Version 3.0.0 | MIT License*
