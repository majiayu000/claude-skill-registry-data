---
name: agent-media
description: AI UGC video production from the terminal using the `agent-media` CLI.
homepage: https://github.com/gitroomhq/agent-media
metadata: {"clawdbot":{"emoji":"🌎","requires":{"bins":[],"env":[]}}}
---

npm release: https://www.npmjs.com/package/agent-media-cli
agent-media cli github: https://github.com/gitroomhq/agent-media
official website: https://agent-media.ai

# agent-media — AI UGC Video Production & Media Generation

Produce complete UGC videos and SaaS review videos from the terminal using the `agent-media` CLI.

---

## MANDATORY RULES — READ BEFORE EVERY COMMAND

**You MUST follow ALL of these rules. Violating any rule produces a broken, unwatchable video.**

### Rule 1: ALWAYS use `--actor` — PICK A RANDOM ONE
Every UGC video MUST include `--actor <slug>`. Without an actor, there is no talking head and no lip sync — the video will just be a static image with voiceover.

**If the user hasn't specified an actor:**
1. Run `agent-media actor list` to get the full list of available actors
2. Pick a **random** actor from the list — do NOT always use the same one (e.g., don't always default to `sofia` or `naomi`)
3. Tell the user which actor you picked and suggest they can browse with `agent-media actor list` or pick a specific one with `--actor <slug>`

**NEVER hardcode a default actor.** Every video should feel different — variety in actors is key to quality UGC content.

### Rule 2: ALWAYS count words — 2.5 words per second
Natural speech is 2.5 words/second. Scripts MUST match the target duration **exactly** — too many words sounds robotic, too few words creates awkward pauses and silence:
- **5s video** → 10–12 words (not fewer!)
- **10s video** → 22–25 words (not fewer!)
- **15s video** → 33–37 words (not fewer!)

**CRITICAL**: Count the words before submitting. If the script is too short, ADD more content. If too long, CUT words. A 15-word script on a 10s video = 5 seconds of dead silence. A 50-word script on a 10s video = rushed robotic speech. Both are broken.

### Rule 3: SaaS reviews MUST have screenshots
For any SaaS/product review video, you MUST provide 1-3 product screenshots via `--broll --broll-images`. Without screenshots, the video has no product context — viewers see only a talking head with no evidence of the product.

`--broll-images` accepts both **HTTP/HTTPS URLs** and **local file paths** (local files are auto-uploaded). Images are **semantically matched** to the most relevant broll scene based on filename — so use descriptive filenames! Examples:
- `--broll-images ./dashboard.png,./calendar-view.png` (local files — descriptive names!)
- `--broll-images https://example.com/pricing-page.png,https://example.com/editor.png` (URLs)
- Mix of both works too

If the user provides a product URL but no screenshots, visit the site yourself and extract image URLs from the page.

### Rule 4: SaaS reviews MUST have the product name
Ask the user: "What SaaS product should I review?" Do NOT proceed without it. The product name must appear in the script so it shows up in subtitles.

### Rule 5: Always use `--sync`
Always append `--sync` to wait for the result and get the output URL.

### Rule 6: Name screenshot files descriptively
Broll images are **semantically matched** to scenes by filename. Use descriptive names so the AI assigns the right image to the right scene:
- **GOOD**: `dashboard.png`, `calendar-view.png`, `post-editor.png`
- **BAD**: `screenshot1.png`, `IMG_0042.png`, `image.png`

When saving screenshots for `--broll-images`, rename them to describe what they show.

---

## Prerequisites

The `agent-media` CLI must be installed and authenticated:

```bash
npm install -g agent-media-cli
agent-media login
```

Verify with `agent-media whoami`. If not logged in, run `agent-media login` and follow the OTP flow.

## UGC Pipeline (Flagship Feature)

The UGC pipeline turns a script into a complete video with AI talking heads, B-roll, voiceover, and animated subtitles — one command.

### Flow

Script → Scene splitting → TTS voiceover → AI talking heads + B-roll → Crossfade assembly → Animated subtitles → Background music → End screen CTA

### Basic UGC

```bash
# ALWAYS include --actor for talking heads + lip sync
agent-media ugc "Ever wonder why some videos go viral? Here's the secret..." --actor sofia --sync

# From file
agent-media ugc ./script.txt --actor naomi --sync

# AI-generated script from a product description
agent-media ugc -g "A fitness tracker that monitors sleep quality" --actor marcus --sync
```

### UGC with B-roll

```bash
# With B-roll cutaway scenes mixed in
agent-media ugc "Your script here..." --actor marcus --broll --sync

# With product screenshots as B-roll (REQUIRED for SaaS reviews)
agent-media ugc "Your script here..." --actor sofia --broll --broll-images https://example.com/screenshot1.png,https://example.com/screenshot2.png --sync
```

### UGC Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--actor <slug>` | Library actor for talking heads | `--actor sofia` |
| `--persona <slug>` | Custom persona (cloned voice + face) | `--persona brand-voice` |
| `--face-url <url>` | Direct face photo URL or local file | `--face-url ./photo.png` |
| `--voice <name>` | TTS voice | `--voice nova` |
| `--tone <name>` | Voice tone: energetic, calm, confident, dramatic | `--tone energetic` |
| `--style <name>` | Subtitle style (17 options — pick random!) | `--style tiktok` |
| `-d, --duration <s>` | Target duration: 5, 10, or 15 seconds | `--duration 10` |
| `--aspect <ratio>` | Aspect ratio: 9:16, 16:9, 1:1 | `--aspect 16:9` |
| `--music <genre>` | Background music: chill, energetic, corporate, dramatic, upbeat | `--music chill` |
| `--cta <text>` | End screen call-to-action text | `--cta "Follow for more"` |
| `--broll` | Enable B-roll cutaway scenes | `--broll` |
| `--broll-images <urls>` | Comma-separated screenshot/image URLs for B-roll | `--broll-images url1,url2` |
| `--template <slug>` | Script template (see below) | `--template saas-review` |
| `-g, --generate-script <prompt>` | AI-generate script from description | `-g "yoga mat product"` |
| `--product-url <url>` | Product URL for script generation context | `--product-url https://...` |
| `-s, --sync` | Wait for completion and print output URL | `--sync` |

### PIP Mode (Picture-in-Picture)

PIP mode creates a full-frame talking head with rotating B-roll image overlays in the lower portion. The actor speaks to camera while relevant visuals slide in and out below. Subtitles appear just above the overlay.

```bash
# Basic PIP video — actor speaks to camera with auto-generated B-roll overlays
agent-media ugc "Stop scrolling. If you struggle to grow on social media, consistency beats perfection every time." \
  --actor adaeze --pip --duration 15 --style hormozi --sync

# PIP with specific style
agent-media ugc "Three things I wish I knew before starting my business..." \
  --actor sofia --pip --duration 10 --style tiktok --sync
```

**PIP Options:**

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--pip-position <pos>` | `bottom-center`, `bottom-left`, `bottom-right` | `bottom-center` | B-roll overlay position |
| `--pip-size <size>` | `small`, `medium`, `large` | `medium` | B-roll overlay size (40%, 55%, 70% of width) |
| `--pip-animation <anim>` | `slide-up`, `slide-left`, `slide-right`, `fade`, `scale` | `slide-up` | Overlay entrance/exit animation |
| `--pip-style <style>` | `none`, `rounded`, `shadow` | `none` | Overlay frame style |

```bash
# PIP with bottom-right overlay, large size, slide-left animation
agent-media ugc "Your script here..." \
  --actor adaeze --pip --pip-position bottom-right --pip-size large --pip-animation slide-left --sync

# PIP with rounded overlay and scale animation
agent-media ugc "Your script here..." \
  --actor sofia --pip --pip-style rounded --pip-animation scale --duration 10 --sync
```

**PIP Rules:**
- `--actor` is **required** (PIP needs a talking head)
- Max duration is **15 seconds** (longer videos are split into ≤10s clips with seamless continuity)
- B-roll overlays are **auto-generated** from the script — no `--broll-images` needed
- Script word count rules apply: 2.5 words/sec (15s = ~37 words max)
- Do NOT combine `--pip` with `--broll` — they are separate modes

### Script Templates

| Template | Structure | Best For |
|----------|-----------|----------|
| `monologue` | Hook → Body → CTA | Direct-to-camera talking |
| `testimonial` | Problem → Solution → Result → CTA | Customer stories |
| `product-review` | Intro → Experience → Verdict → CTA | Product reviews |
| `problem-solution` | Hook → Pain → Solution → CTA | Before/after pain points |
| `saas-review` | Hook → Walkthrough → Opinion → CTA | SaaS/app reviews |
| `before-after` | Hook → Before → After → CTA | Transformations |
| `listicle` | Hook → Tip 1 → Tip 2 → Tip 3 + CTA | Tips and lists |
| `product-demo` | Intro → Demo → Recap → CTA | Product walkthroughs |

### Rule 7: ALWAYS use `--style` — PICK A RANDOM ONE
Every UGC video MUST include `--style <name>`. Without a style, you get the same hormozi subtitle every time — boring and repetitive.

**If the user hasn't specified a style:**
1. Pick a **random** style from the list below — do NOT always default to `hormozi`
2. Tell the user which style you picked

**NEVER hardcode a default style.** Variety in styles makes each video feel unique.

### Subtitle Styles (17 styles)

**Popular**
| Style | Look | Best For |
|-------|------|----------|
| `hormozi` | Bold white, yellow karaoke highlight | Business/marketing content |
| `tiktok` | Bold white, orange-red karaoke | TikTok-style UGC |
| `minimal` | Light, fade in/out | Professional, subtle |
| `clean` | White text on dark box | Clean readability |

**Bold & Energetic**
| Style | Look | Best For |
|-------|------|----------|
| `bold` | Cyan neon outline, karaoke | High energy |
| `impact` | Huge text, 2 words, max punch | Short punchy clips |
| `fire` | Red-orange karaoke, dark red outline | Hype / excitement |
| `pop` | Yellow text, 2 words at a time | Attention-grabbing |
| `spotlight` | Gold highlight, deep shadow | Premium / luxury |

**Aesthetic & Soft**
| Style | Look | Best For |
|-------|------|----------|
| `aesthetic` | Subtle, lowercase, airy | Lifestyle / beauty |
| `pastel` | Soft pink tones | Feminine / soft content |
| `glow` | Purple-pink glow outline | Night / party vibes |

**Colorful**
| Style | Look | Best For |
|-------|------|----------|
| `neon` | Green neon text | Tech / gaming |
| `electric` | Cyan text + magenta highlight | Bold creative |
| `gradient` | Blue-to-coral karaoke | Modern / trendy |
| `karaoke` | Green word-by-word | Karaoke-style |
| `boxed` | White bold on solid black box | Maximum contrast |

## SaaS Review Videos

Generate a complete SaaS review video. **ALL FOUR are required — do NOT skip any:**
1. **Product name** in the script (so it appears in subtitles)
2. **`--actor`** (for talking head + lip sync)
3. **`--broll --broll-images`** with 1-3 product screenshot URLs
4. **Script word count** matching duration (2.5 words/sec)

### Step-by-Step Flow (FOLLOW THIS EXACTLY)

1. **Get product name** — ask user if not provided. STOP if missing.
2. **Get 1-3 screenshot URLs** — ask user, or if they give a URL, visit the site and extract `<img>` URLs showing the product dashboard/UI. STOP if no screenshots.
3. **Pick an actor** — ask user or pick a RANDOM one from `agent-media actor list`. Never always use the same one.
4. **Write the script** — MUST be 22-25 words for 10s or 33-37 words for 15s. Too few words = awkward pauses. Too many = robotic. Mention the product name 2-3 times. Count the words before submitting.
5. **Run the command** with ALL required flags:

```bash
# CORRECT — descriptive filenames so images match the right scenes
agent-media ugc "Postiz is the best social media tool I've used. Postiz schedules across twenty-five platforms with AI. Try Postiz today." \
  --actor naomi --duration 10 --style hormozi --broll \
  --broll-images ./postiz-dashboard.png,./postiz-calendar.png --sync

# CORRECT — URLs with descriptive paths work too
agent-media ugc "Postiz is the best social media tool I've used. Postiz schedules across twenty-five platforms with AI. Try Postiz today." \
  --actor naomi --duration 10 --style hormozi --broll \
  --broll-images "https://postiz.com/dashboard-screenshot.png,https://postiz.com/scheduling-view.png" --sync

# WRONG — no actor, no screenshots, script too long
agent-media ugc "Here's how to schedule a post in Postiz step by step..." --sync
```

### Review Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--actor <slug>` | AI actor (**required**) | `--actor naomi` |
| `--broll` | Enable B-roll scenes (**required** for reviews) | `--broll` |
| `--broll-images <paths>` | Screenshot URLs or local files (**required**, 1-3) | `--broll-images ./img1.png,./img2.png` |
| `--duration <s>` | 5, 10, or 15 seconds | `--duration 10` |
| `--style <name>` | Subtitle style | `--style hormozi` |
| `--cta <text>` | End screen text | `--cta "Try it free"` |
| `-s, --sync` | Wait for result (**always use**) | `--sync` |

## Persona Management

Save voice + face combos for consistent UGC across videos:

```bash
# Create a persona from voice sample + face photo
agent-media persona create --name "brand-voice" --voice ./sample.mp3 --face ./photo.png

# List personas
agent-media persona list

# Use in UGC
agent-media ugc "Your script..." --persona brand-voice --sync

# Delete
agent-media persona delete <persona-id>
```

## Add Subtitles to Any Video

```bash
agent-media subtitle <video-path-or-job-id> --style hormozi --sync
agent-media subtitle ./my-video.mp4 --style bold --sync
```

## Pricing & Credit Deduction

### Plans

| Plan | Price | Monthly Credits | ~10s Videos | ~5s Videos |
|------|-------|-----------------|-------------|------------|
| Creator | $39/mo | 3,900 | ~13 | ~26 |
| Pro | $69/mo | 6,900 | ~23 | ~46 |
| Pro Plus | $129/mo | 12,900 | ~43 | ~86 |

Pay-as-you-go credit pack: 3,900 credits for $39 (one-time purchase, never expires).

### How credits are deducted

**Rate: 30 credits per second of video.** 1 credit = $0.01.

| Duration | Credits deducted | Dollar value |
|----------|-----------------|--------------|
| 5s video | 150 credits | $1.50 |
| 10s video | 300 credits | $3.00 |
| 15s video | 450 credits | $4.50 |
| + AI script generation | +5 credits | +$0.05 |
| Subtitles only | 50 credits | $0.50 |

**Deduction order:** Monthly credits are used first (they expire at period end), then purchased credits (never expire).

**Refunds:** If the video generation fails, credits are automatically refunded. Canceled jobs are also refunded.

Run `agent-media credits` to check balance before generating.

## Job Management

```bash
agent-media status <job-id>     # Check job status
agent-media list                # List recent jobs
agent-media download <job-id>   # Download output media
agent-media cancel <job-id>     # Cancel and refund credits
agent-media retry <job-id>      # Retry a failed job
```

## Account

```bash
agent-media whoami              # Current user info
agent-media credits             # Credit balance
agent-media subscribe           # Manage subscription
agent-media login / logout      # Authentication
```

## REST API (v2)

agent-media also has a REST API for programmatic access. Interactive docs at https://agent-media.ai/docs/api-reference

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/generate/ugc_video | Generate a UGC video |
| POST | /v1/generate/product_review | Generate a product review video |
| POST | /v1/generate/subtitle | Add subtitles to a video |
| GET | /v1/actors | List available AI actors |
| GET | /v1/videos/{jobId} | Check job status |

### Auth

```
Authorization: Bearer ma_YOUR_API_KEY
```

### SDKs (coming soon)

TypeScript and Python SDKs are in development. For now, use the REST API directly via curl or any HTTP client.

### curl Example

```bash
# Generate a video
curl -X POST https://api-v2-production-2f24.up.railway.app/v1/generate/ugc_video \
  -H "Authorization: Bearer <EXAMPLE_CREDENTIAL>" \
  -H "Content-Type: application/json" \
  -d '{
    "script": "Your 50+ character script here...",
    "actor_slug": "sofia",
    "tone": "energetic"
  }'

# Check status
curl https://api-v2-production-2f24.up.railway.app/v1/videos/{job_id} \
  -H "Authorization: Bearer <EXAMPLE_CREDENTIAL>"
```

### MCP Server (Claude Code / Cursor) — coming soon

```json
{
  "mcpServers": {
    "agent-media": {
      "command": "npx",
      "args": ["@agent-media/mcp-server"],
      "env": { "AGENT_MEDIA_API_KEY": "ma_xxx" }
    }
  }
}
```

### OpenAPI Spec

Download at https://agent-media.ai/openapi.json — import into Postman, Insomnia, or any OpenAPI tool.

## Checklist Before Every UGC Command

Before running ANY `agent-media ugc` command, verify:
- [ ] `--actor` is included (no actor = no talking head = broken video). Pick a RANDOM actor if user didn't specify one!
- [ ] `--style` is included. Pick a RANDOM style if user didn't specify one — never always use hormozi!
- [ ] Script word count matches duration EXACTLY (5s=10-12, 10s=22-25, 15s=33-37 words — too few = pauses, too many = robotic)
- [ ] `--sync` is appended
- [ ] For SaaS reviews: `--broll --broll-images` with 1-3 screenshot URLs
- [ ] For SaaS reviews: product name appears 2-3 times in script
- [ ] Credits are sufficient (`agent-media credits`)
