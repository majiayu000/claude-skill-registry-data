---
type: Skill
name: design-content-calendar
description: Produces structured content calendars with platform-specific posting schedules, content pillars, and batch publishing plans. Use when the task asks to "plan content", "schedule posts", "create a content calendar", "editorial calendar", "posting schedule", or "content strategy". Covers content pillars, posting cadence, multi-site calendars, seasonal hooks, and content repurposing matrices.
license: Proprietary. See LICENSE.txt
metadata:
  type: Skill
---

# Content Calendar

Use this skill when planning content strategy, building editorial calendars, or scheduling posts across platforms.

## MCP Tool Discovery

The mcp-ai-wpoos plugin registers tools under **agent-specific prefixes** or
as bare names. Always check your tool list for the correct names:

```
Pattern: nv_oos_{AGENT_NAME}_agent_{TOOL_NAME}
Example: nv_oos_sophie_agent_generate_gemini_image_validated
         schedule_social_post  (bare — usually registered as-is)
```

| Calendar Task | Tool Name Pattern |
|---|---|
| Schedule posts | `schedule_social_post` |
| Create visuals | `nv_oos_*_agent_generate_gemini_image_validated` or bare |
| Resize images | `resize_image` |
| Research trends | `nv_oos_*_agent_web_search_validated` or bare |
| Find existing media | `nv_oos_*_agent_search_attachments` or `search_attachments` |
| Remote site calendar | `remote_wp_connection` — discover spoke sites for multi-site planning |

## WP-CLI Commands

Key `mcp-ai` WP-CLI commands for content planning. Run via `terminal`:

| Command | Use for |
|---|---|
| `wp mcp-ai cron` | Inspect scheduled content and cron events |
| `wp mcp-ai content` | Search and manage content across post types |
| `wp mcp-ai bulk` | Batch schedule posts for multi-platform calendars |

## When to use this skill

Trigger when ANY of the following is true:

- Planning a content strategy or editorial calendar.
- The task asks to "schedule posts", "plan content", or "create a posting schedule".
- Setting up content pillars or themes.
- Creating seasonal/holiday content plans.
- Integrating WordPress content with a publishing schedule.

## Content pillars framework

### The 4-pillar model

```
Pillar 1: Educate     → Tutorials, how-tos, industry insights, tips
Pillar 2: Inspire     → Case studies, transformations, behind-the-scenes
Pillar 3: Entertain   → Memes, trends, challenges, personality content
Pillar 4: Convert     → Offers, testimonials, product features, CTAs
```

### Mix ratios by goal

| Goal | Educate | Inspire | Entertain | Convert |
|---|---|---|---|---|
| **Brand awareness** | 30% | 30% | 30% | 10% |
| **Lead generation** | 40% | 20% | 10% | 30% |
| **Community building** | 20% | 30% | 40% | 10% |
| **Product launch** | 20% | 20% | 10% | 50% |

## Posting cadence

| Platform | Minimum | Optimal | Maximum |
|---|---|---|---|
| **Instagram** | 3×/week | 1×/day (feed) + 1–2 stories/day | 2×/day |
| **Twitter/X** | 1×/day | 3–5×/day | 10×/day |
| **LinkedIn** | 2×/week | 1×/day (weekdays) | 2×/day |
| **Facebook** | 3×/week | 1×/day | 2×/day |
| **TikTok** | 3×/week | 1–3×/day | 5×/day |
| **Pinterest** | 3×/week | 5–10×/day | 30×/day |
| **Blog/Website** | 1×/week | 2–4×/week | 1×/day |

## Content calendar template

```
┌─────────────────────────────────────────────────────────┐
│ WEEK OF: Aug 10, 2026          THEME: Design Systems    │
├──────────┬──────────┬──────────┬──────────┬────────────┤
│   MON    │   TUE    │   WED    │   THU    │    FRI     │
├──────────┼──────────┼──────────┼──────────┼────────────┤
│ Twitter  │ LinkedIn │ Instagram│ Twitter  │ LinkedIn   │
│ "Design  │ Article: │ Carousel:│ Thread:  │ Case study │
│  systems │ "Why     │ "5 color │ "How we  │ post       │
│  myth"   │  tokens  │  palette │  built   │            │
│          │  matter" │  tips"   │  our DS" │            │
├──────────┼──────────┼──────────┼──────────┼────────────┤
│ Status:  │ Status:  │ Status:  │ Status:  │ Status:    │
│ 📝 Draft │ ✅ Ready │ 🎨 Need  │ ✍️ WIP  │ ⏳ Planned │
│          │          │ graphics │          │            │
└──────────┴──────────┴──────────┴──────────┴────────────┘
```

## Scheduling content via MCP

Use `schedule_social_post` to schedule planned content:

**Schedule a week's worth of posts at once:**

```
# Monday — Twitter
content: "Design systems myth: they slow you down. Reality: they speed you up. Here's why..."
platforms: ["twitter"]
scheduled_time: "2026-08-10T09:00:00Z"

# Tuesday — LinkedIn
content: "Why design tokens matter for brand consistency..."
platforms: ["linkedin"]
scheduled_time: "2026-08-11T08:00:00Z"

# Wednesday — Instagram
content: "5 color palette tips every designer should know 🎨"
platforms: ["instagram"]
media_urls: ["https://example.com/palette-guide.jpg"]
scheduled_time: "2026-08-12T12:00:00Z"
```

**Recurring content:**

```
content: "Weekly inspiration roundup: the best design work we saw this week"
platforms: ["twitter", "linkedin"]
recurrence: "weekly"
recurrence_end: "2026-12-31T00:00:00Z"
scheduled_time: "optimal"
```

**Batch-create visuals ahead of time:**

```
1. For each planned post, use the Gemini image tool in your tool list
   (agent-prefixed or bare) to create matching visuals
2. Use resize_image (MCP) to create platform-specific variants
3. Store attachment IDs in your calendar for easy reference
```

## Multi-Site Content Calendar

When managing content across multiple WordPress sites (Hub + spokes), plan
calendars per site and use `remote_wp_connection` to discover which sites are
available:

```
1. List sites: remote_wp_connection { action: "list_connections" }
2. For each spoke (e.g., Parfumerie, Myyco):
   - Plan site-specific content pillars based on its niche
   - Pull existing products/posts for repurposing:
     remote_wp_connection { connection_id: "conn_xxx", action: "get_posts" }
   - Schedule posts targeting that site's audience
3. Hub calendar: cross-brand campaigns, shared seasonal hooks
4. Track all calendars in a single WordPress admin view
```

### Annual hooks

```
January    → New year, goals, trends predictions
February   → Valentine's, love/relationships
March      → Spring, renewal, International Women's Day
April      → Earth Day, sustainability
May        → Mental health, graduations
June       → Pride, summer kickoff
July       → Mid-year reviews, summer content
August     → Back to school, preparation
September  → Fall, new season, Q4 planning
October    → Halloween, spooky/creative themes
November   → Thanksgiving, gratitude, Black Friday
December   → Holidays, year in review, New Year prep
```

### Industry-specific hooks (design)

```
Design awards season (Awwwards, D&AD, Cannes Lions)
Adobe MAX conference (October)
New device launches (Apple events — Sep/Oct/Mar)
Font release days
Pantone Color of the Year announcement (December)
```

## Content repurposing matrix

```
One blog post →  Twitter thread (key points)
                 Instagram carousel (visual summary)
                 LinkedIn article (expanded version)
                 Short video (talking head summary)
                 Email newsletter (full send)
                 Pinterest pins (quote graphics)
                 Podcast episode (audio version)
```

## WordPress content calendar setup

```php
// Register Content Calendar CPT
register_post_type( 'social_post', [
    'labels'      => [ 'name' => 'Social Posts', 'singular_name' => 'Social Post' ],
    'public'      => false,
    'show_ui'     => true,
    'supports'    => [ 'title', 'editor', 'thumbnail', 'custom-fields' ],
    'menu_icon'   => 'dashicons-calendar-alt',
] );

// Add platform + schedule meta boxes
add_action( 'add_meta_boxes', function () {
    add_meta_box( 'social_schedule', 'Schedule', 'render_schedule_box', 'social_post', 'side' );
    add_meta_box( 'social_platform', 'Platform', 'render_platform_box', 'social_post', 'side' );
} );

// Auto-publish via MCP on scheduled time
// The AI agent handles publishing via schedule_social_post when triggered
add_action( 'publish_social_post', 'trigger_social_publishing', 10, 2 );
```

## Critical rules

- **Plan in themes, not random posts** — weekly/monthly themes create narrative cohesion.
- **Batch create content** — one day of creation → one week/month of scheduled posts via `schedule_social_post`.
- **Leave buffer for timely content** — plan 80%, leave 20% for trending/newsjacking.
- **Track what works** — save analytics to post meta: impressions, engagement, clicks, conversions.
- **Evergreen > ephemeral** — 70% evergreen (works anytime), 30% timely (this week only).
- **Generate visuals in batch** — use the Gemini image tool in your tool list ahead of time for all planned posts.
- **Research trends before planning** — use the web search tool in your tool list to identify trending topics and hashtags.
- **Plan per-site for multi-site** — use `remote_wp_connection` to discover spoke sites and plan site-specific calendars.

## What This Skill Does NOT Cover

- **Writing individual post captions or copy** — use **`design-social-content`**.
- **Publishing or scheduling individual social posts** — use `schedule_social_post` via **`design-social-publishing`**.
- **Creating images or visuals for posts** — use **`design-image-generation`**.
- **Monthly campaign strategy and product selection** — use **`design-campaign-orchestration`**.
- **Analyzing past content performance** — use **`design-analytics-reporting`**.
- **SEO keyword research for content** — use **`design-seo-content`**.

## Common Mistakes

```
WRONG:
  ● Filling the calendar 100% with no buffer for trending content
  ● Same content type every day (all static, no reels, no stories)
  ● Planning posts without checking if visuals exist or can be created
  ● Forgetting to plan for multi-site — Hub post ≠ spoke post
  ● Scheduling posts at random times without audience-activity data
  ● No seasonal or annual hooks woven into the monthly plan

RIGHT:
  ✅ 80% planned, 20% buffer for trending/reactive content
  ✅ Mix of reels, static posts, stories, and carousels each week
  ✅ Batch-generate visuals during planning before scheduling
  ✅ Per-site calendars: Hub for cross-brand, spoke for niche audiences
  ✅ Schedule at peak engagement times (check platform analytics)
  ✅ Anchor each month to a seasonal hook or industry event
```

## Cross-references

- Run **`design-social-content`** to write the actual posts for the calendar.
- Run **`design-social-publishing`** to publish scheduled content — use `schedule_social_post` (MCP).
- Run **`design-image-generation`** to create visuals for planned posts — check your tool list for the Gemini image tool.
- Run **`design-media-workflow`** for end-to-end automation including cross-site pipelines.
- Run **`mcp-ai-wpoos-plugin`** for `remote_wp_connection` and multi-site Gateway architecture.
- Use **`paper_store_*`** tools with `connection_id` (e.g. `"conn_8srcad8zylhe"`) to persist calendars to specific spoke sites.

## References

- Content strategy frameworks: <https://contentmarketinginstitute.com/>
- Social media holidays calendar: <https://www.socialmediatoday.com/news/social-media-holidays-calendar/>
- WordPress editorial calendar plugins: PublishPress, Edit Flow
