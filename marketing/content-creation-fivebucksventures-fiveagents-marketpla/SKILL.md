---
name: content-creation
description: Write persona-targeted marketing copy — landing pages, emails, ad copy, blog posts, social media copy for any active brand
allowed-tools: Read, Grep, Glob, Bash, WebSearch, WebFetch
area: Marketing
use_for: "Write persona-targeted marketing copy — landing pages, emails, ad copy, blog posts, social media copy"
deps:
  mcp: []
  gateway: ["fivebucks (opt — fb.ai template manifest shapes `_copy.json`; **scope: social_posts**)"]
  files: ["brand.md", "audience.md", "product.md", "competitors.md", "design-system/ (opt — local; or fb.ai brand kit via fivebucks_get_brand_kit; brand.md fallback)"]
  env: []
---

## Maintenance

| Agent | Version | Last Changed |
|---|---|---|
| Link | v2.20.0 | July 12, 2026 |

**Description:** Write persona-targeted marketing copy — landing pages, emails, ad copy, blog posts, social media copy for any active brand

### Change Log

**v2.20.0** — July 12, 2026
- **Declared the fb.ai dependency and its required scope.** fb.ai API keys are now scoped; this skill's `deps.gateway` now names `fivebucks` and the scope it needs (`social_posts`), so `brand-setup` can tell users which capability boxes to tick. No behaviour change — see `agents/link.md` for the scope/error/quota contract.

**v2.18.0** — July 01, 2026
- **Argil video-ad-script guidance removed (gateway v1.7.4).** Argil (AI avatar video) was retired from the gateway with no replacement, so the "Video Ad Scripts (for Argil)" subsection, its output-table row, and the "When to use" bullet are gone. **Capability gap flagged:** avatar-video ad scripts are no longer supported — reinstating them would require a new AI-avatar vendor + integration. (Also cleared the dangling `brands/{brand}/avatars.md` reference, a file no longer created since brand-setup v2.11.1.)

**v2.10.0** — June 09, 2026
- **Video structure script support added (Step 2b).** When writing YouTube video scripts, content-creation now reads the Video Structure table from the social calendar (populated by `social-calendar` Step 2a Part 1b, sourced from `trend-radar` Step 2c competitor analysis). Each structural section — credibility hook, pattern interruptor, framework, build-with-escalation, reflection beat, close/CTA — becomes a script segment with technique-specific writing guidance. The competitor's proven structure is preserved while the brand's own credibility anchor and content replaces the competitor's. Falls back to generic storytelling frameworks when no video structure is available.

**v2.9.0** — May 28, 2026
- **Hook craft added.** Step 1 + Step 3 now read `hook-library.md` and pick a named **hook archetype** for the opening line / headline / carousel cover. The chosen archetype aligns with the social-calendar entry's Content Angle, and `content-performance-analyst` reports which archetypes win per brand — so hook selection is data-informed over time.

**v2.8.0** — May 20, 2026
- Brand color/font resolution is now a **3-tier lookup**: fb.ai brand kit (`fivebucks_get_brand_kit`) → local `brands/{brand}/design-system/` → `brand.md`, per the Brand kit field map in `agents/link.md`. Trimmed the duplicated design-system reading boilerplate (now centralized in link.md tier 2).

# Content Creation Skill

## Before Executing

Read `agents/link.md` before starting. It defines the active brand, personality, quality checklist, and available tools. Determine the active brand from `$DEFAULT_BRAND` env var — if not set, ask the user.

## Role

You are a B2B copywriter and content strategist for the active brand. Your job is to write persona-targeted, brand-consistent marketing content across all formats—landing pages, emails, ads, blog posts, and social copy. Every piece must be grounded in verified product features and persona-specific pain points. No invented claims, no vague buzzwords.

---

## When to use

Use this skill when the task involves:
- Writing landing page copy
- Drafting email sequences or single emails
- Creating ad copy (Google, LinkedIn, Meta)
- Writing long-form YouTube video scripts (follows the Video Structure table from `social-calendar` Step 2a Part 1b — see Step 2b below)
- Writing blog posts or SEO articles
- Creating social media copy (LinkedIn, Twitter/X)
- Writing product descriptions or feature callouts
- Creating comparison pages ({brand} vs. competitor)

Do NOT use this skill for:
- Developing strategy or positioning → use research-strategy
- Designing visual assets → use creative-designer
- Creating full campaign decks → use campaign-presenter
- Analyzing performance data → use data-analysis

---

## Inputs required

Before starting, confirm these inputs with the user:

| Input | Required | Notes |
|-------|----------|-------|
| Target persona | Yes | Reference brands/{brand}/audience.md for personas |
| Content format | Yes | Landing page, email, ad copy, blog post, social post, etc. |
| Primary goal / CTA | Yes | e.g., drive free trial signups, book a demo, read article |
| Key features to highlight | Yes | Reference brands/{brand}/product.md |
| Competitor angle | Optional | e.g., position vs. SEMrush, vs. ZoomInfo |
| Language | Optional | EN (default) or ID (Indonesian — see audience.md language notes) |
| Word count / length | Optional | If not specified, use format defaults below |

---

## Step-by-step workflow

### Step 1: Read relevant context files
Always read before writing:
- **brands/{brand}/brand.md** — Voice & tone, approved phrases, Do/Don't list
- **brands/{brand}/audience.md** — Target persona pain points, objections, buying triggers, language notes
- **brands/{brand}/product.md** — Features, pricing, differentiators to cite
- **brands/{brand}/competitors.md** — If a competitive angle is needed
- **skills/content-creation/hook-library.md** — proven hook archetypes + opening-line patterns for social copy (read when the format is a social post; informs Step 3)
- **Brand visual identity** — resolve in 3-tier order; informs voice / tonal alignment + any visual specs for copy paired with visuals:
  1. **fb.ai brand kit** *(top tier — only when `FIVEBUCKS_API_KEY` is set)* — call gateway tool `fivebucks_get_brand_kit`; if non-null, use its color tokens + typography — resolve fields via the Brand kit field map in `agents/link.md` (secondary→`tokens.colors.accent`, text→`tokens.colors.dark`, fonts from `tokens.fonts.heading`/`body`; the kit has no separate `secondary` or font weight scale). Returns null when no kit is uploaded — fall through to tier 2.
  2. **brands/{brand}/design-system/** *(local folder — when the fb.ai kit is null or `FIVEBUCKS_API_KEY` is unset; the free baseline)* — read when present.
  3. **brands/{brand}/brand.md** — Colors + Google Font + Voice & Tone. Universal fallback when neither of the above is available. Never block on a missing key or design-system. Same Visual consistency rule as `agents/link.md`.

When the brief is for a format that has a matching **fb.ai template** (Carousel → `meta-carousel`, Story/Reel → `meta-story`, LinkedIn single-image → `linkedin-post`, IG/FB single-image → `meta-post`), copy must be produced as a **structured JSON artifact** matching the template's manifest field keys — content-generator passes those keys to `fivebucks_create_post` as overrides at render time. Save the JSON next to the markdown copy file as `_copy.json`. (Template existence is detected via `fivebucks_list_templates`; if none, `_copy.json` is optional — see below.)

#### meta-carousel copy contract (IG/FB carousel)

When the brand has a `meta-carousel` template on fb.ai, output `_copy.json` with these keys (6 slides — Cover + 4 value slides + CTA). These are the template's manifest field keys:

```json
{
  "cover_eyebrow":  "≤ 30 chars, all caps category tag (e.g. 'AI FOR SME OWNERS')",
  "cover_title":    "≤ 60 chars, the carousel's main headline",
  "cover_sub":      "≤ 140 chars, supporting subline",

  "s2_kicker":      "01",
  "s2_title":       "≤ 50 chars, sign 1 headline",
  "s2_body":        "≤ 220 chars, sign 1 body paragraph",
  "s2_pullquote":   "(optional, ≤ 80 chars) — used by templates with pullquote variant",

  "s3_kicker":      "02",
  "s3_title":       "≤ 50 chars, sign 2 headline",
  "s3_body":        "≤ 220 chars, sign 2 body paragraph",
  "s3_stat_value":  "(optional, ≤ 12 chars, e.g. '~3 hrs')",
  "s3_stat_label":  "(optional, ≤ 60 chars)",

  "s4_kicker":      "03",
  "s4_title":       "≤ 50 chars",
  "s4_body":        "≤ 220 chars",

  "s5_kicker":      "04",
  "s5_title":       "≤ 50 chars",
  "s5_body":        "≤ 220 chars",
  "s5_before":      "(optional, ≤ 50 chars) — used by templates with before/after variant",
  "s5_after":       "(optional, ≤ 80 chars)",

  "cta_eyebrow":    "≤ 20 chars (e.g. 'READY?')",
  "cta_title":      "≤ 50 chars, CTA headline",
  "cta_sub":        "≤ 200 chars, CTA body / value reinforcement",
  "cta_button":     "≤ 30 chars (e.g. 'fiveagents.io →')"
}
```

#### meta-story copy contract (IG/FB Stories + Reels)

When the brand has a `meta-story` template on fb.ai, output `_copy.json` with these keys (6 slides — Hook → Problem → Solution → Proof → Offer → CTA):

```json
{
  "s1_eyebrow":         "≤ 30 chars, all caps (e.g. 'AI THAT WORKS WHILE YOU SLEEP')",
  "s1_headline_pre":    "first line of hook headline",
  "s1_headline_accent": "second line, accent-colored",
  "s1_sub":             "≤ 200 chars supporting line",
  "s1_live":            "≤ 18 chars badge (e.g. 'Running live')",
  "s1_big":             "≤ 12 chars big stat (e.g. '3 hrs')",
  "s1_big_unit":        "≤ 40 chars unit/qualifier (e.g. 'saved every single day.')",

  "s2_eyebrow":         "(e.g. 'THE PROBLEM')",
  "s2_headline":        "≤ 60 chars problem headline",
  "s2_pain1":           "≤ 100 chars pain bullet 1",
  "s2_pain2":           "≤ 100 chars pain bullet 2",
  "s2_pain3":           "≤ 100 chars pain bullet 3",

  "s3_eyebrow":         "(e.g. 'THE FIX')",
  "s3_headline_pre":    "first line of solution headline",
  "s3_headline_accent": "second line, accent-colored",
  "s3_sub":             "≤ 200 chars supporting line",

  "s4_eyebrow":         "(e.g. 'REAL RESULTS')",
  "s4_headline":        "≤ 60 chars proof headline",
  "s4_stat1_num":       "≤ 12 chars",  "s4_stat1_lbl": "≤ 50 chars",
  "s4_stat2_num":       "≤ 12 chars",  "s4_stat2_lbl": "≤ 50 chars",
  "s4_stat3_num":       "≤ 12 chars",  "s4_stat3_lbl": "≤ 50 chars",
  "s4_stat4_num":       "≤ 12 chars",  "s4_stat4_lbl": "≤ 50 chars",
  "s4_quote":           "≤ 200 chars testimonial quote",
  "s4_quote_author":    "≤ 60 chars author + role",

  "s5_eyebrow":         "(e.g. 'WHAT YOU GET')",
  "s5_headline":        "≤ 60 chars offer headline",
  "s5_b1":              "≤ 80 chars bullet 1",
  "s5_b2":              "≤ 80 chars bullet 2",
  "s5_b3":              "≤ 80 chars bullet 3",
  "s5_b4":              "≤ 80 chars bullet 4",
  "s5_pill":            "≤ 30 chars pill (e.g. 'Live in 1 week')",

  "s6_eyebrow":         "(e.g. 'READY?')",
  "s6_headline_pre":    "first line of CTA headline",
  "s6_headline_accent": "second line, accent-colored",
  "s6_sub":             "≤ 200 chars CTA supporting line",
  "s6_cta":             "≤ 30 chars button label (e.g. 'Book a Free Call')",
  "s6_url":             "destination URL (e.g. 'fiveagents.io')"
}
```

#### linkedin-post copy contract (LinkedIn single-image)

When the brand has a `linkedin-post` template on fb.ai, output `_copy.json` with these keys (1 slide; the `direction` A/B/C is set by social-calendar). Unused keys for the chosen direction are ignored:

```json
{
  "eyebrow":      "≤ 30 chars, all caps category tag",
  "headline":     "≤ 90 chars, the hook headline (direction A centerpiece)",
  "body":         "≤ 200 chars, 1–2 supporting sentences",
  "stat_value":   "≤ 12 chars big stat (direction B hero, e.g. '78%')",
  "stat_label":   "≤ 60 chars stat caption",
  "quote":        "≤ 200 chars pull quote (direction C)",
  "attribution":  "≤ 60 chars author + role",
  "cta_text":     "≤ 60 chars CTA line",
  "cta_button":   "≤ 30 chars button label"
}
```

#### meta-post copy contract (IG/FB single-image)

When the brand has a `meta-post` template on fb.ai, output `_copy.json` with these keys (1 slide; `direction` A/B/C set by social-calendar). b4/b5 are optional (direction C may use 3–5 bullets):

```json
{
  "eyebrow":      "≤ 30 chars, all caps category tag",
  "headline":     "≤ 80 chars, scroll-stopping headline (direction A)",
  "body":         "≤ 140 chars, 1 supporting sentence",
  "quote":        "≤ 200 chars quote (direction B)",
  "attribution":  "≤ 60 chars author + role",
  "b1":           "≤ 80 chars bullet 1 (direction C)",
  "b2":           "≤ 80 chars bullet 2",
  "b3":           "≤ 80 chars bullet 3",
  "b4":           "(optional) ≤ 80 chars bullet 4",
  "b5":           "(optional) ≤ 80 chars bullet 5",
  "cta_text":     "≤ 60 chars CTA line",
  "cta_button":   "≤ 30 chars button label"
}
```

**Save both files per post:**
- `outputs/{brand}/posts/[Platform]/[Slug]_[Date]_copy.md` — human-readable narrative draft (still required for review)
- `outputs/{brand}/posts/[Platform]/[Slug]_[Date]_copy.json` — structured copy that content-generator passes to `fivebucks_create_post` as overrides

If the brand has no matching fb.ai template (or `FIVEBUCKS_API_KEY` is unset), `_copy.json` is optional — content-generator falls through to its Gemini-only path and reads narrative copy from `_copy.md` instead.

**Direction is set by `social-calendar`, not by content-creation.** Your job is the copy contract; the calendar entry's `Direction` column drives template-variant routing at render time.

### Step 1b: Supplement with live research via Perplexity MCP
Use the **WebSearch tool** when writing SEO content or competitive copy:
- For blog posts / SEO articles: search current keyword trends (e.g., "AI search optimization best practices 2026") to ensure content is timely
- For comparison pages: verify competitor's current positioning, pricing, or feature set
- For social copy: check trending conversation angles relevant to the persona's role

Only use Perplexity when the static context files don't provide enough current intelligence. Note any Perplexity-sourced claims in a footer comment in the output file.

### Step 2: Choose a storytelling framework
Select from skills/content-creation/storytelling-frameworks.md:
- **AIDA** (Attention → Interest → Desire → Action) — Best for landing pages, ads
- **PAS** (Problem → Agitate → Solution) — Best for email, long-form copy
- **BAB** (Before → After → Bridge) — Best for social posts, short ads
- **Problem-Solution** — Best for blog posts, comparison pages

### Step 2b: Apply video structure (YouTube scripts only)

*Run this step only when the content format is a YouTube video script and the social calendar entry includes a Video Structure table (written by `social-calendar` Step 2a Part 1b). Skip for all other formats.*

1. **Read the Video Structure table** from the social calendar Notion page. It contains 6 structural sections, each with a timestamp target, the brand's adapted version, and the technique.
2. **Use the structure as the script skeleton.** Each section becomes a script segment:

| Script Segment | Source | Writing Notes |
|---|---|---|
| Opening (0:00–0:30) | Section 1: Credibility Hook | Write the hook using the brand's credential. Match the technique (if `corporate_pedigree`, open with the corporate journey; if `speed_result`, open with the build timeline). First 3 seconds must arrest attention. |
| Pattern Break (0:30–1:30) | Section 2: Pattern Interruptor | If `flash_forward`: write a segment showing the end result before explaining how. If `show_dont_tell`: write a live demo beat. The viewer should think "wait, how did they do that?" |
| Framework (1:30–3:00) | Section 3: Framework | Teach the mental model. Use simple language, enumerate clearly ("There are 3 ways..."). This is the educational core. |
| Main Body (3:00–end-2min) | Section 4: Build with Escalation | Follow the escalation steps from the structure. Each step gets its own script section with rising stakes/complexity. Include transition lines between steps ("Now here's where it gets interesting..."). |
| Reflection (near end) | Section 5: Reflection Beat | Write an honest, personal reflection. Use first person. This is the vulnerability moment — the script should feel unrehearsed here. |
| Close (final 30s) | Section 6: Close/CTA | Match the CTA mechanic from the structure. If `comment_to_dm`: write the exact comment keyword and what the viewer receives. |

3. **The storytelling framework from Step 2 is subordinate to the video structure.** When a video structure is present, it overrides the generic framework (AIDA/PAS/BAB). The video structure IS the framework.

**If no Video Structure table exists** in the social calendar entry: fall back to Step 2's storytelling framework selection as before.

### Step 3: Draft the headline / hook
Write 3 headline options before choosing one:
- **For social posts:** pick a **hook archetype** from `hook-library.md` that fits the angle (the social-calendar entry's Content Angle names the intended archetype — honor it). Use the archetype's opening-line pattern for the format (LinkedIn first line / carousel cover / IG-FB headline). Avoid the "openers to never use."
- Lead with the persona's primary pain point OR primary desired outcome
- Use concrete language (not vague superlatives)
- Use approved phrases from brands/{brand}/brand.md where they fit naturally
- Test against: "Does this speak to [persona] specifically?"

### Step 4: Write the body copy
Follow the chosen framework structure. For every claim:
- Back it with a specific feature from brands/{brand}/product.md
- Match it to a pain point from brands/{brand}/audience.md
- Use the voice from brands/{brand}/brand.md (practical, confident, clear, not hypey)

**Format defaults by content type:**
- Landing page: 300-600 words (hero + 3-4 sections + CTA)
- Email (single): 150-250 words
- Email sequence: 3 emails — awareness, consideration, decision
- Ad copy: 1 headline (max 30 chars) + 1-2 description lines (max 90 chars each)
- Blog post: 600-1,200 words with H2 subheadings
- Social post (LinkedIn): 100-200 words with line breaks
- Social post (Twitter/X): 1-3 tweets, max 280 chars each

### Step 5: Write the CTA
Every piece of content must end with a clear, specific CTA:
- Primary CTA options: read from `brands/{brand}/product.md` — use the trial offer, demo CTA, and plan names defined there
- Match urgency to the persona's buying stage and plan tier (from `brands/{brand}/audience.md`)
- Trial availability and terms are brand-specific — always check `brands/{brand}/product.md` before offering a trial CTA

### Step 6: Run quality checklist
Review against the checklist below before saving output.

---

## Output format

**Save location — local workspace:**
```
outputs/{brand}/posts/[Platform]/     ← social copy
outputs/{brand}/strategy/             ← blog, email, landing page, ad copy
```

**Folder by content type:**
| Content Type | Local Folder |
|---|---|
| LinkedIn post copy | `outputs/{brand}/posts/LinkedIn/` |
| Facebook post copy | `outputs/{brand}/posts/Facebook/` |
| Instagram post copy | `outputs/{brand}/posts/Instagram/` |
| Twitter/X post copy | `outputs/{brand}/posts/Twitter/` |
| Blog post | `outputs/{brand}/strategy/` |
| Email | `outputs/{brand}/strategy/` |
| Landing page | `outputs/{brand}/strategy/` |
| Ad copy | `outputs/{brand}/strategy/` |
| YouTube video script | `outputs/{brand}/strategy/` |

**Naming convention:**

For **social posts** (LinkedIn / Facebook / Instagram — the files content-generator picks up downstream), use the post's topic slug so the filename matches what content-generator expects:

```
[Slug]_[DDMonYYYY]_copy.md
[Slug]_[DDMonYYYY]_copy.json   (when a Carousel/Story template is installed — see Step 1 contracts)
```

For **non-social outputs** (blog post, email, landing page, ad copy, etc.), use the content-type prefix:

```
[ContentType]_[DDMonYYYY]_copy.md
```

Examples:
- Social: `AISearchSEOFoundations_10Mar2026_copy.md` (paired with `..._copy.json` for IG/FB Carousel/Story when template exists)
- `BlogPost_10Mar2026_copy.md`
- `Email_10Mar2026_copy.md`
- `LandingPage_10Mar2026_copy.md`
- `AdCopy_10Mar2026_copy.md`
- `YouTubeScript_10Mar2026_copy.md`

**Output metadata:**
```markdown
---
Date: YYYY-MM-DD
Skill Used: content-creation
Framework: AIDA | PAS | BAB | Problem-Solution | Video-Structure
Persona: [Persona name from audience.md]
Format: Landing page | Email | Ad copy | Blog post | Social post | YouTube video script
Campaign: [Campaign name]
Language: EN | ID
Status: Draft | Final
---
```

---

## Quality checklist

Before finalizing any content output:

**Accuracy:**
- [ ] All product features mentioned exist in brands/{brand}/product.md
- [ ] Pricing is accurate per brands/{brand}/product.md (if mentioned)
- [ ] No invented testimonials, case studies, or customer logos
- [ ] Competitive claims supported by brands/{brand}/competitors.md
- [ ] No guaranteed ranking promises or timeframes

**Brand consistency:**
- [ ] Voice follows brands/{brand}/brand.md (practical, confident, not hypey)
- [ ] Approved phrases used where appropriate
- [ ] Do/Don't list followed
- [ ] Brand colors and typography referenced correctly if visual specs included — derive in 3-tier order: fb.ai brand kit (`fivebucks_get_brand_kit`, checked first when `FIVEBUCKS_API_KEY` set) → local `brands/{brand}/design-system/` (when present) → `brand.md`; never from memory; never blocked on a missing key or design-system
- [ ] When the brand has a matching fb.ai template (`fivebucks_list_templates`): `_copy.json` produced with that type's manifest field keys (meta-carousel cover_*/s2-5_*/cta_*; meta-story s1_*–s6_*; linkedin-post eyebrow/headline/body/stat_*/quote/attribution/cta_*; meta-post eyebrow/headline/body/quote/attribution/b1-b5/cta_*); per-key character budgets respected
- [ ] Direction NOT set in `_copy.json` — that's social-calendar's responsibility (lives in the Notion calendar entry's Direction column)

**Messaging effectiveness:**
- [ ] Headline addresses persona's specific pain point or desired outcome
- [ ] Body copy follows the chosen framework structure
- [ ] At least one proof point (specific feature or data) per major claim
- [ ] Objections from brands/{brand}/audience.md addressed or anticipated
- [ ] CTA is clear, specific, and persona-appropriate
- [ ] Output saved with correct naming and metadata
- [ ] Agent run logged to dashboard

---

## Final Step — Log to Dashboard

See `docs/new_agent_onboarding/metrics-spec.md` for the full JSONB contract.

```
Use gateway MCP tool `fiveagents_log_run`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- skill: "content-creation"
- brand: "<active-brand>"
- status: "<success|failed>"
- summary: "<1 line, <200 chars>"
- started_at: "<ISO timestamp>"
- completed_at: "<ISO timestamp>"
- metrics: {
    "date": "YYYY-MM-DD",
    "format": "<linkedin-post|facebook-post|blog|email|ad_copy|landing_page|youtube-script>",
    "persona": "<slug>",
    "framework": "<problem-agitate-solve|aida|bab|problem-solution|video-structure>",
    "language": "en",
    "campaign": "<campaign name>",
    "content_status": "Final",
    "word_count": 0,
    "deliverable": "<filename>",
    "output_path": "outputs/{brand}/posts/..."
  }
```
