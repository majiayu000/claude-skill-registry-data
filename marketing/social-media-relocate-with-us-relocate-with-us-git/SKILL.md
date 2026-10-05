---
name: social-media
description: Create and plan social media content for LinkedIn, Twitter/X, and Telegram for the VisaJobs.xyz job board. Use when the user asks for posts, content plans, social media schedules, LinkedIn posts, tweets, Telegram messages, or weekly content.
---

# Social Media Content for VisaJobs.xyz

## Brand Context

- **Site**: visajobs.xyz
- **LinkedIn**: https://www.linkedin.com/company/visasponsoredjobs/
- **Telegram**: https://t.me/visa_sponsored_jobs
- **Audience**: International software engineers looking to relocate to Europe with visa sponsorship
- **Tone**: Helpful, direct, data-driven, personal. Not corporate.

## File Output

Save post files to the project root. They are gitignored:
- `linkedin-posts-week-MMMDD.md`
- `twitter-posts-week-MMMDD.md`

## LinkedIn Post Format

Optimized for the LinkedIn algorithm:

- **Hook**: Strong first 2 lines (visible before "see more")
- **Whitespace**: Short paragraphs, lots of line breaks
- **Engagement**: End with CTA (save, tag, comment)
- **Hashtags**: 3-5 per post at the end
- **Length**: 800-1300 characters sweet spot

### Post Angles (rotate through the week)

| Angle | Description | Best Day |
|-------|-------------|----------|
| **Big Drop** | New batch announcement with country breakdown + emoji flags | Mon/Tue |
| **Junior/Grad** | Target early-career roles, bust the "need experience" myth | Wed |
| **Unpopular Opinion** | Provocative take to drive comments | Thu |
| **Company Spotlight** | Deep-dive one company's relocation perks | Fri |
| **Data/Numbers** | Job market stats, country breakdowns, salary comparisons | Sat |
| **Monday Prep** | Actionable checklist for job seekers | Sun |
| **Country Deep Dive** | Focus on one country (Germany, Netherlands, etc.) | Mon |

### Core Hashtags

```
#VisaSponsorship #RelocationJobs #TechJobs #WorkAbroad #Hiring
#JuniorDev #NewGrad #TechCareers #SoftwareEngineering
#Germany #EUBlueCard #Berlin #Amsterdam #Barcelona
```

### CTA Templates

```
Save this post. Tag someone who's looking.
Which city surprised you? Drop it in the comments 👇
Browse all → visajobs.xyz
Apply → visajobs.xyz
Join our Telegram → t.me/visa_sponsored_jobs
```

## Twitter/X Post Format

- **Standalone tweets**: Punchy, under 280 chars, bookmark/RT-worthy
- **Threads**: Hook tweet with number + "↓", 4-6 follow-up tweets, one idea per tweet
- **Engagement tweets**: Polls, "reply with your stack", hot takes
- **Frequency**: 2-3 tweets per day

### Tweet Types

| Type | Purpose | Example Hook |
|------|---------|-------------|
| **Banger** | RT + bookmark | "Companies sponsoring visas to Europe: [list]" |
| **Thread** | Reach + depth | "🧵 5 underrated cities for tech relocation ↓" |
| **Hot take** | Comments | "Berlin is overrated for tech relocation" |
| **Poll** | Engagement | "What's stopping you from applying abroad?" |
| **Tip** | Value | "Your CV should be ONE page for European jobs" |
| **Numbers** | Authority | "330+ visa-sponsored jobs tracked this week" |

### Posting Schedule

| Time (CET) | Type | Goal |
|-------------|------|------|
| 8-9am | Hook tweet or thread | Morning scrollers |
| 1-2pm | Tip / engagement | Midday visibility |
| 6-7pm | Bookmark bait / list | Evening save-for-later |

## Telegram Format

- Short, scannable blocks
- Heavy emoji use
- Direct links to apply URLs
- Format for easy forwarding
- High information density: country, role, company, link

### Telegram Template

```
🚨 NEW JOBS ADDED

🇩🇪 Germany
• SoundCloud — Backend Engineer → [link]
• Miro — Graduate Software Engineer → [link]

🇳🇱 Netherlands
• Databricks — Software Engineer (New Grad) → [link]

All visa sponsored + relocation included.

👉 Full list: visajobs.xyz
```

## Content Creation Workflow

1. Read current `src/_data/jobs.json` to know what's new
2. Group new jobs by country and angle
3. Create posts for each platform
4. Save to gitignored files in project root
5. Include posting schedule and tips

## Key Data Points to Reference

- Total jobs on the board (check jobs.json length)
- Number of companies
- Country breakdown
- EU Blue Card: no lottery, processed in weeks, ~€45,300 threshold for tech in Germany
- Netherlands 30% ruling: tax benefit for expats
