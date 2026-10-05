---
type: Skill
name: design-social-content
description: Create platform-optimized social media content — captions, hashtags, headlines, calls-to-action. Covers tone-of-voice, character limits, hook writing, A/B testing variants, and content repurposing across platforms. Use when writing captions, generating hashtags, crafting hooks, creating A/B test variants, adapting content per platform, or setting up an editorial voice.
license: Proprietary. See LICENSE.txt
metadata:
  type: Skill
---

# Social Content Creation

Use this skill when crafting social media captions, headlines, hashtags, or content strategies for any platform.

## MCP Tool Discovery

The mcp-ai-wpoos plugin registers tools under **agent-specific prefixes** or
as bare names. Always check your tool list for the correct names:

```
Pattern: nv_oos_{AGENT_NAME}_agent_{TOOL_NAME}
Example: nv_oos_sophie_agent_web_search_validated
         web_search_validated  (bare — may not be registered)
```

| Content Task | Tool Name Pattern |
|---|---|
| Image analysis (context for captions) | `analyze_image` |
| Extract text from images | `extract_image_text` |
| Generate alt text | `generate_image_alt_text_validated` |
| Generate captions | `generate_image_caption_validated` |
| Research trending topics | `nv_oos_*_agent_web_search_validated` or bare `web_search_validated` |
| Publish final content | `schedule_social_post` |

For AI-assisted caption generation (prompt-based copywriting), the **media
worker** (`/api/social/generate-content`) or direct AI model calls serve as
fallbacks.

## WP-CLI Commands

Key `mcp-ai` WP-CLI commands for social content workflows. Run via `terminal`:

| Command | Use for |
|---|---|
| `wp mcp-ai cron` | Check scheduled social posts |
| `wp mcp-ai bulk` | Batch generate captions and hashtags |
| `wp mcp-ai content` | Pull existing posts for repurposing |

## When to use this skill

Trigger when ANY of the following is true:

- Writing or reviewing social media post copy.
- The task mentions "caption", "hashtags", "social copy", or "post text".
- Content needs to be adapted for multiple platforms.
- Setting up a content strategy or editorial voice.
- A/B testing post variants.

## Content workflow (MCP-first)

```
1. Research trends → web search tool in your tool list
2. Generate image  → Gemini tool in your tool list (agent-prefixed or bare)
3. Analyze image   → analyze_image (MCP) — understand visual context
4. Write caption   → Creative process + AI assistance
5. Optimize image  → resize_image (MCP) — per-platform dimensions
6. Publish         → schedule_social_post (MCP)
```

Use `analyze_image` to get a detailed description of generated images, which
helps craft captions that reference specific visual elements. Use the web
search tool in your tool list to research trending topics and hashtags before
writing.

## Platform content formulas

### Twitter/X

```
Hook (curiosity/controversy) + Value (insight/tip) + CTA (question/retweet)
= "Most designers overlook this one font pairing trick. It instantly
   makes layouts feel premium. Here's how: 🧵👇"
```

Best hooks: questions, bold statements, numbers, "how to", "stop doing X".

### Instagram

```
Headline (bold statement) + Body (story/context) + Value (takeaway) + CTA
+ Hashtags (5-15)

"✨ The rebrand that doubled their revenue.
Swipe to see the before/after →"
```

Best formats: carousels (educational), reels (entertaining), stories (behind-the-scenes).

### LinkedIn

```
Hook (industry observation) + Context (why it matters) + Insight (your take)
+ CTA (discussion)

"After 50+ brand redesigns, I've noticed one pattern: companies that
succeed don't just change their logo — they change their story."
```

Best formats: text-only, document carousels, case studies, polls.

### Facebook

```
Question/Hook + Story (personal or customer) + Value + CTA (comment/share)

"Remember when logos had to work in black & white faxes? 📠
Design has come a long way. Here's what responsive logos look like in 2026..."
```

## Hashtag strategy

### Research & selection

- **Brand hashtag**: unique to you (`#DesignBy[Studio]`).
- **Industry hashtags**: broad reach (`#BrandDesign`, `#GraphicDesign`, `#UI`).
- **Niche hashtags**: targeted community (`#LogoReveal`, `#DesignProcess`).
- **Trending hashtags**: timely (`#DesignTrends2026`).

### Volume by platform

| Platform | Optimal count | Placement |
|---|---|---|
| Instagram | 5–15 | First comment or end of caption |
| LinkedIn | 3–5 | End of post |
| Twitter/X | 1–2 | End of tweet |
| Facebook | 0–2 | End (low effectiveness) |
| TikTok | 3–5 | Caption |

### Design niche hashtags

```
#BrandIdentity #LogoDesign #VisualIdentity #DesignInspiration
#TypographyDesign #ColorPalette #DesignSystem #UIUXDesign
#CreativeDirection #PackagingDesign #MotionDesign #WebDesign
#DesignProcess #BehindTheDesign #DesignThinking
```

## Content calendar structure

```
Week 1: Awareness    — Industry insight, trend report, hot take
Week 2: Education    — Tutorial, tip, case study, process breakdown
Week 3: Social proof — Client result, testimonial, before/after
Week 4: Conversion   — Offer, service highlight, portfolio piece
```

Mix: 40% educational, 30% social proof, 20% awareness, 10% promotional.

## Tone-of-voice templates

| Tone | Example | Best For |
|---|---|---|
| **Professional** | "Our analysis reveals three key trends shaping brand design in 2026." | LinkedIn, case studies |
| **Conversational** | "Honestly? Most logos try to do way too much. Here's what actually works 👇" | Twitter, Instagram |
| **Inspirational** | "Great design doesn't just look good. It makes people feel something." | Instagram, Pinterest |
| **Educational** | "Typography hierarchy in 3 steps: 1) Headline grabs attention 2) Subhead adds context 3) Body delivers value." | Carousels, LinkedIn |
| **Bold/Edgy** | "Your brand isn't boring because of your colors. It's boring because you're playing safe." | Twitter, TikTok |

## AI-assisted content generation (media worker fallback)

```javascript
const response = await fetch('http://localhost:3100/api/social/generate-content', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    topic: 'The rise of variable fonts in web design',
    tone: 'educational',
    platform: 'linkedin',
    include_hashtags: true,
  }),
});

const { prompt_template, suggested_hashtags, character_limit } = await response.json();
```

> **Tip:** When writing captions for AI-generated images, use `analyze_image` (MCP) first to understand the visual content, then craft text that references specific elements in the image.

## A/B testing framework

For each post, test ONE variable:

```
Variant A: Question hook     → "Want better brand recognition?"
Variant B: Statement hook    → "Brand recognition drops 23% without consistency."

Variant A: Image (product mockup)
Variant B: Video (behind-the-scenes)

Variant A: Long caption (story)
Variant B: Short caption (punchy)

Track: impressions, engagement rate, link clicks, saves/shares.
Winner after 48h: promote variant with higher engagement.
```

## Critical rules

- **Hook first** — the first 125 characters (Instagram), 50 characters (Twitter), or 3 lines (LinkedIn) determine if they "see more".
- **One CTA per post** — "comment below" OR "save for later" OR "click link in bio", not all three.
- **No hashtag stuffing** — 30 irrelevant hashtags look spammy and hurt reach on Instagram.
- **Accessibility** — use emojis sparingly (screen readers announce each one), camelCase hashtags (#BrandDesign not #branddesign), add alt text to all images via `generate_image_alt_text_validated` (MCP).
- **Time zones matter** — schedule for the audience's peak time, not your local time; use `schedule_social_post` with `scheduled_time: "optimal"` (MCP).

## Common mistakes

```
# WRONG — no hook, generic CTA
"Check out our new blog post about design trends. Link in bio.
#design #graphicdesign #art #creative #branding #logo #typography..."

# RIGHT — hook, value, single CTA, targeted hashtags
"3 design trends that are already dead in 2026 💀
(And what to use instead)
1. Gradients on everything → Try: intentional color blocking
2. ...
Save this for your next brand refresh 📌
#BrandDesign #DesignStrategy #VisualIdentity"
```

## Cross-references

- Run **`design-image-generation`** to create visuals that match the content — check your tool list for the Gemini image tool.
- Run **`design-social-publishing`** to publish the content — use `schedule_social_post` (MCP).
- Run **`design-content-calendar`** to plan the publishing schedule.
- Run **`design-brand-kit`** to ensure brand voice consistency.
- Run **`mcp-ai-wpoos-plugin`** for `remote_wp_connection` — publish content targeting specific spoke sites.

## References

- Character limits & media specs: <https://sproutsocial.com/insights/social-media-image-sizes/>
- Instagram hashtag research: <https://later.com/blog/instagram-hashtags/>
- LinkedIn algorithm insights: <https://www.linkedin.com/blog/member/product/how-the-linkedin-algorithm-works>
