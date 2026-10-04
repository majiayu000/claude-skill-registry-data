---
name: blog-post
category: publishing
description: "Full-stack blog post production — turns a topic, idea, or brief into a complete publishing package across written, social, and multimedia surfaces. Generates broomva.tech .mdx posts (or Substack/other long-form), X posts and threads, LinkedIn posts, Instagram posts and reel scripts, plus multimedia asset plans (images, video, audio, GIFs). Outputs a structured content package to /broomva/posts/. Use when: (1) creating a new blog post or article, (2) turning an idea into multi-platform content, (3) producing a content package for a topic, (4) writing and distributing a post across channels, (5) generating social content from a long-form piece. Triggers on: 'blog post', 'new post', 'write a post about', 'content package', 'publish about', 'create post', 'blog-post'."
---

# Blog Post — Full-Stack Content Production

Turn a topic into a complete, strategy-aware publishing package: long-form post + social adaptations + multimedia assets.

## Compounding Skills

This skill **orchestrates** — it does not re-implement what already exists:

| Skill | Role in Pipeline |
|-------|-----------------|
| `/content-creation` | Storytelling frameworks, visual content strategy, social distribution patterns, AI asset generation (Imagen 4.0, Veo 3.1, TTS), Remotion video |
| `/deep-research` | Multi-source research when topic requires verified claims or data |
| `/agent-browser` | Screenshots, reference extraction, web research |
| `/pencil` | Design social cards, carousel slides, diagrams |
| `/arcan-glass` | BroomVA brand styling for visual assets |
| `/remotion-best-practices` | Video composition, spring animations, sequencing |
| `/google-veo` | Veo 3.1 cinematic prompting — camera vocabulary, shot composition, style direction |
| `/subtitle-generation` | Burn-in subtitles for reels (80% watch muted) |
| `/prompt-library` | Reusable prompts for content generation |
| `/competitor-intel` | Market context when writing about products or strategy |

**Rule**: Before generating content for any phase, check if a compounding skill handles it better. Delegate, don't duplicate.

## Modes

### Full Pipeline (default)
```
BRIEF → RESEARCH → ANGLE → OUTLINE → LONG-FORM → ADAPT → MEDIA → STRATEGY → PUBLISH
```
**9 phases, each produces a file or action in the output package.**

### X-First Mode
```
BRIEF → ANGLE → X CONTENT → MEDIA → PUBLISH
```
**Lightweight mode for standalone X content** — not derived from a blog post. Use when: building in public, reacting to news, sharing a demo, shipping a contrarian take, or posting a terminal screenshot with context. Produces `x-post.md` and/or `x-thread.md` with growth-optimized patterns. See [references/x-growth-strategy.md](references/x-growth-strategy.md).

**Triggers**: "x post about", "tweet about", "x thread about", "post on x", "ship to x", "build in public"

**X-First pipeline:**
1. **Brief** — Topic + intent (1 line is enough)
2. **Angle** — Apply the angle test (specificity, tension, evidence) even for short content
3. **Generate** — Use growth-optimized templates: visual proof, native media, engagement hooks, strategic tags
4. **Media** — Terminal screenshot, architecture diagram, demo GIF, or native video (60-90s)
5. **Publish** — Via `xurl post` or `xurl reply` (thread). Always attach media natively (never external links)

**X-First content types** (see [references/x-growth-strategy.md](references/x-growth-strategy.md)):
- Terminal screenshot + insight (3-5x/week)
- "How I built X" thread (1x/week)
- Demo video, 60-90s native (1x/week)
- Contrarian take (1-2x/week)
- Before/after comparison (1-2x/week)
- "Day N of building X" update (daily optional)
- Strategic reply to big accounts (3-5x/day)

## Phase 0: Content Brief Intake

Gather or construct a content brief. See [templates/brief.md](templates/brief.md) for the template.

**Required fields:**
- `topic` — What this post is about
- `intent` — Why this post exists (educate, persuade, announce, reflect, document)
- `audience` — Who reads this (developers, founders, general, specific community)

**Optional fields:**
- `platforms` — Target channels (default: all). Options: `broomva-tech`, `substack`, `x-post`, `x-thread`, `linkedin`, `instagram-post`, `instagram-reel`
- `tone` — Voice (default: confident-technical). Options: `conversational`, `academic`, `provocative`, `reflective`, `storytelling`
- `references` — URLs, papers, prior posts to build on
- `media` — Desired outputs: `png`, `mp4`, `gif`, `mp3` (default: all)
- `cta` — What should the reader do after? (follow, subscribe, try, share, discuss)
- `destination` — Primary long-form target (default: `broomva-tech`). Options: `substack`, `medium`, `dev-to`, `hashnode`
- `slug` — URL-friendly identifier (auto-generated from topic if omitted)

**If the user provides only a topic**, infer reasonable defaults and confirm before proceeding.

## Phase 1: Research & Enrichment

**When to research**: If the brief includes references, data claims, or the topic requires external validation.

**How to research:**
1. Use `/deep-research` for topics needing 5+ verified sources
2. Use `/agent-browser` to extract content from reference URLs
3. Use web search for current data, trends, or competitor context
4. Use `/competitor-intel` if topic involves market positioning

**Output**: `research.md` — key findings, sources, data points, quotes. Keep it factual and citable.

**When to skip**: Personal reflections, opinion pieces, internal documentation — research is optional, not mandatory.

## Phase 2: Angle & Narrative Selection

The angle is what makes content *intentional* rather than generic. It answers: "Of all the things I could say about this topic, what specific lens am I using and why?"

**Angle selection criteria:**
1. **Audience gap** — What does this audience need that isn't being said?
2. **Unique evidence** — What data or experience do I have that others don't?
3. **Contrarian potential** — Is there a widely-held belief I can challenge with evidence?
4. **Timeliness** — Is there a current event or trend that makes this relevant now?
5. **Story potential** — Is there a transformation narrative (before → after)?

**Framework selection** (from `/content-creation` storytelling references):

| Content Type | Best Framework | When to Use |
|-------------|---------------|-------------|
| Case study / results | **PSI** (Problem-Solution-Impact) | Showing quantified outcomes |
| Industry take / opinion | **ABT** (And-But-Therefore) | Challenging conventional wisdom |
| Technical deep dive | **1-3-1** (One idea, three evidence, one takeaway) | Teaching a concept |
| Product / launch story | **Pixar Spine** | Transformation narrative |
| Data-driven insight | **Data Arc** (Context-Tension-Resolution) | Leading with surprising numbers |
| Decision documentation | **So-What** (What-Why-Action) | Internal or reflective posts |

**Output**: Update `outline.md` with the chosen angle, framework, and rationale.

## Phase 3: Outline Generation

Build a structured outline from the angle. This is the *architectural blueprint* — all downstream content derives from it.

**Outline structure:**
```
# Title Options (3 candidates, pick best)

## Hook (1-2 sentences — the "why should I care" opener)

## Sections
1. [Section name] — [1-line purpose]
   - Key point A
   - Key point B
   - Evidence/data to include
   - Media placement: [image/video/gif opportunity]

2. [Section name] — [1-line purpose]
   ...

## Closing
- Memorable takeaway (one line)
- CTA alignment with brief

## Media Inventory
- Hero image concept
- Supporting images (one per ~300 words)
- Video opportunity (if applicable)
- GIF opportunity (if applicable)
- Audio narration (y/n)
```

**Output**: `outline.md`

## Phase 4: Long-Form Content Generation

Write the primary long-form post. Target platform determines format.

### broomva.tech (default)

Use the [templates/broomva-tech-post.mdx](templates/broomva-tech-post.mdx) template.

**Frontmatter schema:**
```yaml
---
title: "Post Title"
summary: "One-sentence summary for cards and SEO"
date: YYYY-MM-DD
published: true
tags:
  - tag1
  - tag2
audio: /audio/writing/{slug}.mp3  # if audio generated
---
```

**Content conventions:**
- Use standard Markdown (GFM) — the engine renders via remark + remark-gfm
- Embed video: `<video src="/images/writing/{slug}/video.mp4" autoplay muted loop playsinline style="width:100%;border-radius:8px;margin-bottom:1.5rem"></video>`
- Images: `![Alt text](/images/writing/{slug}/image-name-opt.png)`
- Figures: `<figure><img src="..." alt="..." /><figcaption>Caption</figcaption></figure>`
- Tables: Standard GFM tables (styled by Tailwind prose)
- No custom MDX components needed — raw HTML works

### Substack / Alternative Platforms

Use [templates/substack-post.md](templates/substack-post.md). Standard Markdown, no frontmatter beyond title/subtitle. Adjust image paths to be relative or hosted URLs.

**Output**: `broomva-tech-post.mdx` and/or `substack-post.md` (based on `destination` in brief)

## Phase 5: Cross-Platform Adaptation

**Critical rule**: Each platform gets *native* content, not a copy-paste resize. The core *message* is shared; the *expression* is platform-native.

### Adaptation Matrix

| Platform | Length | Format | Hook Style | Media | CTA Style |
|----------|--------|--------|-----------|-------|----------|
| X blog post | Freeform (no limit) | Long-form article | Narrative hook + hero image | Images, video, GIFs inline | Link + engagement |
| X post | 280 chars | Single tweet | Punchy stat or claim | 1 image | Implied (engagement) |
| X thread | 5-8 tweets | Numbered thread | Scale proof or contrarian | Image every 2-3 tweets | Link in final tweet |
| LinkedIn | 1300 chars | Paragraphs + bullets | First 210 chars = hook | 1 image or document carousel | Direct ask |
| Instagram post | 2200 chars caption | Caption + carousel (1080x1350) | Visual-first, caption supports | 1-10 carousel images | Save/share/link in bio |
| Instagram reel | 15-60s script | Video script + captions | 3-second hook | 9:16 vertical video | Follow/link in bio |

### Platform-Specific Content Generation

See [references/platform-adaptation.md](references/platform-adaptation.md) for detailed per-platform strategies.

**X Blog Post** — Full long-form article published directly on X (formerly "Twitter Articles"). Freeform length — can match or exceed the broomva.tech post. Supports inline images, videos, GIFs, and rich formatting. Unlike the broomva.tech post, the X blog post is written for *X's audience and algorithm* — more conversational, more opinionated, more multimedia-dense. Every section should be accompanied by a visual (image, diagram, GIF, or video clip). The hero image is critical — it's the thumbnail that determines clicks. Use Imagen 4.0 for hero + supporting images, Veo 3.1 clips for inline video, and ffmpeg GIFs for demos. See [references/x-blog-post.md](references/x-blog-post.md).

**X Post** — Extract the single most surprising or provocative insight. Always attach an image (terminal screenshot, diagram, before/after, or generated visual) — text-only posts get 60% less reach. No external links in post body (X suppresses them) — put links in a self-reply. Include an engagement hook: question, contrarian frame, or "reply with your experience." Tag 1-2 relevant accounts when genuinely building on their work. See [references/x-growth-strategy.md](references/x-growth-strategy.md).

**X Thread** — Re-tell the story in tweet-sized beats. Each tweet stands alone while building momentum. Spend 50% of effort on tweet 1 — it determines everything. Image every 2-3 tweets (increases completion by 45%). Self-reply the full chain fast (don't trickle). End with CTA: question for replies, Discord invite, or link in final self-reply. Tag the most relevant account in tweet 1 if crediting their work. See [references/x-growth-strategy.md](references/x-growth-strategy.md).

**LinkedIn** — Professional framing. Lead with insight or contrarian take in first 210 chars (before "See More" fold). Use bullet lists for key takeaways. 3-5 hashtags max.

**Instagram Post** — Design a carousel: cover slide with hook, 1 insight per slide (flashcard style, not paragraphs), stat slide, CTA slide. Caption tells the story; slides show the highlights.

**Instagram Reel** — Write a script with: 3-second visual hook, problem statement (5s), key insight (10-15s), evidence or demo (10-15s), CTA (5s). Vertical 9:16 format. See [references/reel-production.md](references/reel-production.md) for Veo 3.1 prompting and subtitle burn-in.

**Output**: `x-blog-post.md`, `x-post.md`, `x-thread.md`, `linkedin-post.md`, `instagram-post.md`, `instagram-reel.md`

## Phase 6: Multimedia Production

Plan and produce media assets. See [references/multimedia-production.md](references/multimedia-production.md).

### Asset Types

| Asset | Tool | When |
|-------|------|------|
| Hero image / social card | Nano Banana (`gemini-3.1-flash-image`) | Always — every post needs a hero |
| Supporting images | Nano Banana or `/agent-browser` screenshots | 1 per ~300 words |
| Animated GIF | ffmpeg from video or ImageMagick from frames | UI demos, flow previews |
| Audio narration | kokoro-tts / Edge TTS / ElevenLabs | If `mp3` in media targets |
| Video composition | Remotion + AI clips (Veo 3.1) | If `mp4` in media targets |
| Instagram carousel PNGs | `/pencil` MCP | If Instagram in platforms |

### Media Prompt Generation

For each planned asset, generate a specific AI prompt in `media/image-prompts.md`:
- Describe the visual concept tied to the content it accompanies
- Include style direction (dark theme, technical, minimal, etc.)
- Specify dimensions and aspect ratio per platform

### Audio Script

If audio is targeted, extract the post body text and write a narration-ready script in `media/audio-script.md`. Strip markdown formatting, add natural pauses, and note pronunciation guides for technical terms.

### Video Script

If video is targeted, write a Remotion-compatible composition outline in `media/video-script.md`:
- Scene breakdown (title, stats, screenshots, workflow, closing)
- Duration per scene
- Transition style
- Asset references (which images/clips to use)

**Output**: `media/` directory with prompt files and any generated assets

## Phase 7: Strategy & Distribution Planning

Generate strategy documents for the content package.

**Output files in `strategy/`:**
- `audience.md` — Target audience profile, what they care about, where they are
- `platform-strategy.md` — Per-platform approach, posting time, format rationale
- `distribution-plan.md` — Publishing sequence (which platform first, timing gaps, cross-linking)
- `cta.md` — Call-to-action strategy aligned across all channels

### Distribution Sequencing

Recommended order (adjust per strategy):
1. **Blog post** first (canonical URL)
2. **X thread** within 1 hour (drives initial engagement)
3. **LinkedIn** same day (professional audience, different peak hours)
4. **Instagram carousel** next day (visual audience, different consumption pattern)
5. **Instagram reel** 2-3 days later (extends content lifecycle)
6. **X post** (standalone) as engagement trigger mid-week

## Phase 8: Publishing & Distribution

Execute the distribution plan by publishing content to each platform. Uses CLI tools and REST APIs — no third-party services.

### Platform Connectors

| Platform | Tool | Auth | Capabilities |
|----------|------|------|-------------|
| **X/Twitter** | `xurl` CLI | OAuth2 (configured via `xurl auth oauth2`) | Post, thread, reply, media upload, like, repost |
| **LinkedIn** | `curl` + REST API | OAuth2 bearer token | Text posts, image posts, document carousels |
| **Instagram** | `curl` + Meta Graph API | Business account + access token | Photo posts, carousel posts, reel uploads |
| **broomva.tech** | `cp` + `git` + `gh` | Git credentials | Copy .mdx + assets, create PR |

### X Publishing (via xurl)

**Prerequisite check**: `xurl whoami` — if 401, prompt user to run `xurl auth oauth2`.

**Single post**:
```bash
# Text only
xurl post "$(cat x-post.md | head -1)"

# With image
xurl post "$(cat x-post.md | head -1)" --media media/thumbnails/x-card.png
```

**Thread** (parse x-thread.md, post sequentially):
```bash
# Extract tweet 1 (the hook), post it, capture the tweet ID
FIRST_ID=$(xurl post "Tweet 1 text" --media media/png/hero.png 2>&1 | jq -r '.data.id')

# Reply chain for remaining tweets
xurl reply $FIRST_ID "Tweet 2 text"
# ... continue for each tweet
```

**Thread parsing logic**: Read `x-thread.md`, split on `### N/N` headers, extract text between headers, identify `📸 Image:` lines for media attachment. See [references/publishing-automation.md](references/publishing-automation.md).

### LinkedIn Publishing (via curl)

**Prerequisite**: OAuth2 access token stored in `~/.config/blog-post/linkedin-token`.

```bash
LINKEDIN_TOKEN=$(cat ~/.config/blog-post/linkedin-token)
LINKEDIN_URN=$(cat ~/.config/blog-post/linkedin-urn)

# Uses Posts API v2 (ugcPosts was deprecated in 2024)
curl -s -X POST "https://api.linkedin.com/v2/posts" \
  -H "Authorization: Bearer $LINKEDIN_TOKEN" \
  -H "Content-Type: application/json" \
  -H "LinkedIn-Version: 202401" \
  -H "X-Restli-Protocol-Version: 2.0.0" \
  -d "{
    \"author\": \"urn:li:person:$LINKEDIN_URN\",
    \"commentary\": \"$(cat linkedin-post.md | sed '1,2d' | head -40)\",
    \"visibility\": \"PUBLIC\",
    \"distribution\": { \"feedDistribution\": \"MAIN_FEED\" },
    \"lifecycleState\": \"PUBLISHED\"
  }"
```

### Instagram Publishing (via Meta Graph API)

**Prerequisite**: Business/Creator account, access token in `~/.config/blog-post/instagram-token`.

```bash
IG_TOKEN=$(cat ~/.config/blog-post/instagram-token)
IG_USER_ID=$(cat ~/.config/blog-post/instagram-user-id)

# Step 1: Create media container (image must be publicly hosted)
CONTAINER_ID=$(curl -s -X POST \
  "https://graph.instagram.com/v19.0/$IG_USER_ID/media" \
  -d "image_url=https://broomva.tech/images/writing/{slug}/hero.png" \
  -d "caption=$(cat instagram-post.md | sed -n '/^## Caption/,$ p' | tail -n+2)" \
  -d "access_token=$IG_TOKEN" | jq -r '.id')

# Step 2: Publish
curl -s -X POST \
  "https://graph.instagram.com/v19.0/$IG_USER_ID/media_publish" \
  -d "creation_id=$CONTAINER_ID" \
  -d "access_token=$IG_TOKEN"
```

### broomva.tech Publishing

```bash
SLUG="{slug}"
# Copy post and assets
cp broomva-tech-post.mdx ~/broomva/broomva.tech/apps/chat/content/writing/$SLUG.mdx
mkdir -p ~/broomva/broomva.tech/apps/chat/public/images/writing/$SLUG/
cp media/png/* ~/broomva/broomva.tech/apps/chat/public/images/writing/$SLUG/
# Copy audio if exists
[ -f media/mp3/narration.mp3 ] && \
  cp media/mp3/narration.mp3 ~/broomva/broomva.tech/apps/chat/public/audio/writing/$SLUG.mp3
# Create PR
cd ~/broomva/broomva.tech
git checkout -b content/$SLUG
git add apps/chat/content/writing/$SLUG.mdx apps/chat/public/images/writing/$SLUG/
git commit -m "content: add $SLUG"
git push -u origin content/$SLUG
gh pr create --title "content: $SLUG" --body "New blog post"
```

### Publishing Workflow

When the user says "publish" or "distribute" after a content package is ready:

1. **Check available connectors** — Run `xurl whoami`, check for LinkedIn/IG tokens
2. **Report what can be published** — List platforms with ✅ (ready) or ❌ (needs setup)
3. **Confirm with user** — Show what will be posted to each platform, ask for go-ahead
4. **Execute in sequence** — Follow the distribution plan order
5. **Report results** — Show post URLs/IDs for each platform, note any failures
6. **Update README.md** — Mark published platforms with URLs

### Credential Storage

Store platform tokens in `~/.config/blog-post/` (gitignored, never committed):
```
~/.config/blog-post/
├── linkedin-token       # LinkedIn OAuth2 access token
├── linkedin-urn         # LinkedIn member URN
├── instagram-token      # Meta/Instagram access token
└── instagram-user-id    # Instagram Business account ID
```

X credentials are managed by `xurl` internally (stored in its own keychain).

### Graceful Degradation

- **No xurl auth?** → Generate post text but skip publishing; show `xurl auth oauth2` instructions
- **No LinkedIn token?** → Generate post but skip; show OAuth setup steps
- **No Instagram token?** → Generate post but skip; show Meta app setup steps
- **Always confirm before posting** — Never auto-publish without explicit user approval

## Output Structure

Each invocation creates a package at `/broomva/posts/{YYYY-MM-DD}-{slug}/`:

```
{YYYY-MM-DD}-{slug}/
├── README.md                    # Package manifest (what's inside, status, links)
├── brief.md                     # Content brief (input)
├── research.md                  # Research notes (if applicable)
├── outline.md                   # Content outline with angle + framework
├── broomva-tech-post.mdx        # Primary long-form (broomva.tech)
├── substack-post.md             # Alternative long-form (if requested)
├── x-blog-post.md               # X long-form article (multimedia-rich)
├── x-post.md                    # X single post
├── x-thread.md                  # X thread (5-8 tweets)
├── linkedin-post.md             # LinkedIn post
├── instagram-post.md            # Instagram caption + carousel spec
├── instagram-reel.md            # Reel script/concept
├── media/
│   ├── image-prompts.md         # AI image generation prompts
│   ├── audio-script.md          # TTS narration script
│   ├── video-script.md          # Video composition script
│   ├── gif-concept.md           # GIF animation concept
│   ├── hero.png                 # Hero/social card (generated)
│   ├── thumbnails/              # Per-platform thumbnails
│   ├── png/                     # Static images
│   ├── gif/                     # Animated GIFs
│   ├── mp3/                     # Audio narration
│   └── mp4/                     # Video files
└── strategy/
    ├── audience.md              # Target audience profile
    ├── platform-strategy.md     # Per-platform approach
    ├── distribution-plan.md     # Publishing schedule + sequence
    └── cta.md                   # Call-to-action strategy
```

## Agent Behavior

### On Invocation

1. **Parse intent** — Extract topic, audience, intent from user message
2. **Check brief completeness** — If only topic provided, propose defaults and confirm
3. **Create output directory** — `mkdir -p /broomva/posts/{date}-{slug}/media/{thumbnails,png,gif,mp3,mp4} /broomva/posts/{date}-{slug}/strategy`
4. **Execute phases 0-7 sequentially** — Each phase produces its output file
5. **Generate media assets** — Use available tools (Nano Banana, ffmpeg, kokoro-tts). If tools unavailable, leave prompt files for manual generation
6. **Copy to broomva.tech** — If destination is broomva-tech, also copy `.mdx` to `broomva.tech/apps/chat/content/writing/{slug}.mdx` and images to `broomva.tech/apps/chat/public/images/writing/{slug}/`
7. **Publish (Phase 8)** — If user says "publish" or "distribute", execute the distribution plan via `xurl` (X), `curl` (LinkedIn/Instagram), and `git` (broomva.tech). Always confirm before posting.
8. **Report** — Summarize what was created, what was published (with URLs), what needs manual action

### Graceful Degradation

- **No GEMINI_API_KEY?** → Generate image prompts but skip generation; note in README
- **No ffmpeg/Remotion?** → Write video/GIF scripts but skip rendering; note in README
- **No TTS engine?** → Write audio script but skip narration; note in README
- **Never fail silently** — Always explain what was skipped and why

### Quality Gates

Before completing, validate:
- [ ] Every platform adaptation has a unique hook (not copy-pasted)
- [ ] Long-form post has at least 3 media placement points
- [ ] X thread has 5-8 tweets with images planned every 2-3 tweets
- [ ] Instagram carousel has cover + 8-12 content slides specified
- [ ] LinkedIn hook is ≤ 210 characters
- [ ] CTA is consistent across channels but adapted per platform
- [ ] All file paths in README match actual files created
- [ ] No placeholder text remains in any output file

See [references/quality-checklist.md](references/quality-checklist.md) for the full validation checklist.

### Reel Production Quality Gates

When producing Instagram Reels (via Veo 3.1 + ffmpeg):
- [ ] Hook grabs attention in first 3 seconds (visual movement, NOT just text)
- [ ] Subtitles burned in (80% watch muted)
- [ ] No static shot longer than 5 seconds
- [ ] Audio present (narration, ambient, or music — never silence)
- [ ] CTA in final 3 seconds
- [ ] 9:16 vertical, `-movflags +faststart`
- [ ] Duration 15-45 seconds

See [references/reel-production.md](references/reel-production.md) for Veo 3.1 prompting (5-part formula, camera vocabulary), subtitle generation, and the full production pipeline.

## Self-Evolution

This skill improves with every use. See [references/self-evolution.md](references/self-evolution.md) for the full protocol.

**After every publish**: Track which hooks, formats, and timings performed best. Promote winners to templates. Annotate losers.

**Feedback loop**: `PUBLISH → MEASURE (48h) → EXTRACT PATTERNS → UPDATE SKILL → NEXT PUBLISH`

**X growth tracking**: Track followers/week, impressions/post, thread completion rate, engagement rate, and reply engagement from watchlist accounts. See [references/x-growth-strategy.md](references/x-growth-strategy.md) for full metrics.

**Content pillars**: Build Logs, Agent Architecture, Meta-Content, Open Source, Contrarian Takes. Each pillar has an optimal platform mix and X-first format.

**Compounding**: New skills are integrated when they handle a task the pipeline currently does manually, have 100+ community installs, and don't bloat SKILL.md beyond 600 lines.

## Quick Start

```
User: /blog-post "Building an Agent OS in Rust" — targeting developers,
      intent is to educate and attract contributors, provocative tone

Agent: [Creates brief → researches if needed → selects ABT angle →
       outlines → writes long-form → adapts for X/LinkedIn/IG →
       generates media + reels via Veo 3.1 → publishes via xurl/curl/git]
```
