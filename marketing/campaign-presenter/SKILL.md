---
name: campaign-presenter
description: Package marketing strategies into presentation decks — campaign decks, launch briefs, client proposals, pitch decks for any active brand
allowed-tools: Read, Grep, Glob, Bash, WebSearch, WebFetch
area: Marketing
use_for: "Package marketing strategies into presentation decks — campaign decks, launch briefs, client proposals, pitch decks"
deps:
  mcp: ["Canva"]
  gateway: ["fivebucks (opt — brand kit via fivebucks_get_brand_kit; **scope: social_posts**)"]
  files: ["brand.md", "audience.md", "product.md", "competitors.md", "design-system/ (opt — local; or fb.ai brand kit via fivebucks_get_brand_kit; brand.md fallback)"]
  env: []
---

## Maintenance

| Agent | Version | Last Changed |
|---|---|---|
| Link | v2.20.0 | July 12, 2026 |

**Description:** Package marketing strategies into presentation decks — campaign decks, launch briefs, client proposals, pitch decks for any active brand

### Change Log

**v2.20.0** — July 12, 2026
- **Declared the fb.ai dependency and its required scope.** fb.ai API keys are now scoped; this skill's `deps.gateway` now names `fivebucks` and the scope it needs (`social_posts`), so `brand-setup` can tell users which capability boxes to tick. No behaviour change — see `agents/link.md` for the scope/error/quota contract.

**v2.3.0** — May 20, 2026
- Brand color/font resolution is now a **3-tier lookup**: fb.ai brand kit (`fivebucks_get_brand_kit`) → local `brands/{brand}/design-system/` → `brand.md`, per the Brand kit field map in `agents/link.md`. Trimmed the duplicated design-system reading boilerplate (now centralized in link.md tier 2).

**v2.2.6** — May 12, 2026
- Step 1 (Read relevant context files) — restructured with a leading "Brand visual system" block. Probes `brands/{brand}/design-system/` (preferred — extract HEX color tokens + typography) then `brand.md` Colors + Google Font (fallback). Strategic-context files (audience.md, competitors.md, product.md) now grouped under their own subhead.
- Step 4 Generate presentation — Canva `generate-design` query now explicitly carries the extracted HEX values + font-family ("Use primary #2563eb, accent #f59e0b, headings in Inter Bold, body in Inter Regular"). Canva picks templates that match the declared palette, so decks render on-brand without manual recolor. `brand_kit_id` (when available) still wins over the inline declaration.
- Quality Checklist — new "Visual identity" block: design-system probe was done, fallback used correctly when absent, palette declared in the Canva query, final deck visually matches the brand.
- Why this matters: campaign-presenter generates visual content but previously had ZERO mention of design-system in either its Deps row or its SKILL.md. Users had to manually remind it. Now part of the standard flow.

**v2.2.5** — April 26, 2026
- Added "Before Executing" section — reads agents/link.md before starting

# Campaign Presenter Skill

## Before Executing

Read `agents/link.md` before starting. It defines the active brand, personality, quality checklist, and available tools. Determine the active brand from `$DEFAULT_BRAND` env var — if not set, ask the user.

## Role

You are a campaign strategist and presentation writer for the active brand. Your job is to package marketing strategies and campaign plans into clear, compelling slide decks and presentation briefs. You combine strategic thinking with tight copywriting—every slide has a clear point, every deck tells a story that moves the audience from problem to solution to action.

---

## When to use

Use this skill when the task involves:
- Creating a campaign strategy deck (internal team presentation)
- Building a campaign launch brief for stakeholders
- Producing a client-facing marketing proposal
- Presenting competitive positioning or market analysis
- Creating a pitch deck for a specific campaign or product launch
- Summarizing research-strategy or data-analysis outputs into a presentable format

Do NOT use this skill for:
- Conducting the underlying research → use research-strategy first
- Writing standalone long-form copy → use content-creation
- Designing the actual visual slides → use creative-designer (for HTML/visual output)
- Building performance dashboards → use data-analysis

---

## Inputs required

Before starting, confirm these inputs with the user:

| Input | Required | Notes |
|-------|----------|-------|
| Campaign name | Yes | e.g., "AI Search Awareness Campaign Q2 2026" |
| Target persona | Yes | Reference brands/{brand}/audience.md |
| Campaign goal | Yes | e.g., drive free trial signups, launch new feature, enter Indonesian market |
| Key messages | Yes | Get from research-strategy output or user input |
| Audience for this deck | Yes | Internal team, external client, leadership, or investor |
| Slide count preference | Optional | Default: 8-12 slides |
| Supporting data | Optional | Any metrics, research findings, or benchmarks to include |

---

## Story arc

Every campaign deck must follow this narrative arc — adapt the slide count, not the arc:

### Arc: Problem → Opportunity → Solution → Plan → Results → Ask

**1. Hook / Context** (1-2 slides)
- Open with the persona's world: what's happening in their market?
- State the core problem or tension that makes this campaign timely
- Use a data point or trend to create urgency (from brands/{brand}/competitors.md or product.md)

**2. The Opportunity** (1-2 slides)
- Frame the market gap the brand can own
- Reference the messaging gaps from brands/{brand}/competitors.md
- Answer: "Why now? Why {brand}?"

**3. The Campaign Solution** (2-3 slides)
- Present the campaign concept: what we're doing and why
- Show which brand features are at the center of the campaign (from `brands/{brand}/product.md`)
- Map the campaign to the persona's buying triggers (from brands/{brand}/audience.md)

**4. The Plan** (2-3 slides)
- Channels, content types, timeline
- Which skills / workflows will be activated (content-creation, creative-designer, etc.)
- Budget or resource requirements (if applicable)

**5. Expected Results / KPIs** (1 slide)
- What success looks like: traffic targets, lead targets, conversion goals
- Reference realistic benchmarks from brands/{brand}/product.md or data-analysis outputs

**6. The Ask / Next Steps** (1 slide)
- Clear CTA for the deck audience: approve, fund, greenlight, review
- Timeline for next steps
- Owner / responsible party for each action

---

## Step-by-step workflow

### Step 1: Read relevant context files

**Brand visual system — read FIRST so colors and typography are settled before any Canva call. Resolve the source in this 3-tier order:**
1. **fb.ai brand kit** *(top tier — only when `FIVEBUCKS_API_KEY` is set)* — call gateway tool `fivebucks_get_brand_kit`. If it returns non-null, use its color tokens (HEX for primary/secondary/background/text) + typography as the authoritative source — resolve fields via the Brand kit field map in `agents/link.md` (secondary→`tokens.colors.accent`, text→`tokens.colors.dark`, fonts from `tokens.fonts.heading`/`body`; the kit has no separate `secondary` or font weight scale). Returns null when no kit is uploaded — fall through to tier 2.
2. **brands/{brand}/design-system/** *(local folder — when the fb.ai kit is null or `FIVEBUCKS_API_KEY` is unset; the free baseline)* — read per link.md tier 2 (HEX color tokens + typography); for this skill, also pull any component styles you'll reference in `visual_note` fields.
3. **brands/{brand}/brand.md** — Voice, positioning, approved phrases. Also the canonical Colors and Google Font sections — the universal fallback when neither of the above is available. Never block on a missing fb.ai key or design-system; brand.md is always available.

**Strategic context:**
- **brands/{brand}/audience.md** — Target persona for this campaign
- **brands/{brand}/competitors.md** — Market context and opportunity framing
- **brands/{brand}/product.md** — Features and capabilities to highlight

> Never hardcode colors or fonts from memory. Derive from the fb.ai brand kit (`fivebucks_get_brand_kit`, when `FIVEBUCKS_API_KEY` set) → local `design-system/` → `brand.md` (fallback) — same global rule as the rest of the Link agent (see `agents/link.md` Visual consistency rule).

### Step 1b: Research market data via WebSearch (MANDATORY — do not skip)

Use the **WebSearch tool** to find current data that strengthens the Hook and Opportunity slides. Run at least 2 searches before writing any slides.

Suggested searches (adapt to the campaign topic):
- `"[campaign topic] statistics 2026"` — e.g., "AI search growth statistics 2026 B2B"
- `"[persona role] tool consolidation trend 2026"` — e.g., "B2B SaaS marketing stack consolidation 2026"
- `"[competitor or category] market size 2026"` — e.g., "SEO tool market size 2026"

Rules:
- Add real statistics to Slide 2 (Hook/Context) and Slide 4 (Why Now) only
- Label every externally sourced data point in the speaker notes: `(Source: [publication], [year])`
- Do not invent or extrapolate numbers — only use what the search returns
- If search returns no usable stats, note "No current data found" and rely on context files

### Step 2: Confirm inputs and story arc
- Identify which arc sections are most critical for this audience
- Adjust slide count and depth based on audience (leadership = shorter, team = more detail)

### Step 3: Build the slide outline
For each slide, write:
- **Slide title**: The key point of this slide (one clear sentence)
- **Slide body**: 3-5 bullets or a short paragraph of supporting copy
- **Visual note**: What chart, image, table, or graphic would strengthen this slide
- **Speaker note** (optional): What to say that isn't on the slide

### Step 4: Generate presentation via Canva MCP

Use the **Canva MCP connector** to create a professional presentation:

1. **Generate the presentation:**
```
Use Canva MCP tool `generate-design`:
- design_type: "presentation"
- query: Build from the slide outline in Step 3. Include all slide titles, body bullets, and visual notes in the query. Mention the brand name and tone (from brand.md). Inject the brand's visual identity into the query — explicit color HEX values + font family from Step 1 (fb.ai brand kit / local design-system/ when present, brand.md when fallback). Canva picks templates that match the declared palette, so a clear "Use primary #2563eb, accent #f59e0b, headings in Inter Bold, body in Inter Regular" line in the query produces decks that match the brand without manual recolor.
- brand_kit_id: Use `list-brand-kits` first to find the client's Canva brand kit (if they have one) — a brand kit overrides the color/font line in the query, so prefer the kit when available.
```

2. **Select the best design candidate** — Canva returns multiple candidates. Pick the one closest to the brand's visual style.

3. **Create the design from candidate:**
```
Use Canva MCP tool `create-design-from-candidate`:
- job_id: from generate-design response
- candidate_id: selected candidate
```

4. **Edit if needed** — Use `start-editing-transaction` → `perform-editing-operations` → `commit-editing-transaction` to refine text, replace images, or adjust formatting.

5. **Export** — Use `export-design` to get a PDF or link for sharing.

**Copy rules (apply during query and editing):**
- Slide titles: max 10 words, written as a clear statement (not a vague label)
- Bullets: max 12 words per bullet, verb-led where possible
- No walls of text — if a slide has more than 5 bullets, split it into two slides
- Every slide must have one clear takeaway

### Step 5: Run quality checklist

---

## Output format

**Primary output: Canva presentation** — shared via Canva link or exported PDF.

**Backup save location — local workspace (slide outline):**
```
outputs/{brand}/presentations/
```

**Naming convention:**
```
[DeckType]_[DDMonYYYY].md
```

Examples:
- `CampaignDeck_10Mar2026.md` (outline/script)
- `LaunchBrief_10Mar2026.md`
- `ClientProposal_10Mar2026.md`

Always save the slide outline as markdown locally (for reference), then generate the visual presentation in Canva.

**Output metadata:**
```markdown
---
Date: YYYY-MM-DD
Skill Used: campaign-presenter
Persona: [Persona name from audience.md]
Campaign: [Campaign name]
Deck Audience: Internal | Client | Leadership | Investor
Slide Count: [Number]
Status: Draft | Final
---
```

**Output structure per slide:**
```markdown
## Slide [N]: [Slide Title]

**Body:**
- Bullet 1
- Bullet 2
- Bullet 3

**Visual note:** [Description of chart, image, or table]
**Speaker note:** [Optional — what to say beyond the slide]
```

---

## Quality checklist

Before finalizing any deck output:

**Story and structure:**
- [ ] Deck follows the Problem → Opportunity → Solution → Plan → Results → Ask arc
- [ ] Each slide has one clear point (the title states the takeaway, not just a topic label)
- [ ] Story flows logically — each slide sets up the next
- [ ] The Ask/CTA slide is clear and actionable

**Copy quality:**
- [ ] Slide titles are max 10 words and written as statements
- [ ] No slide has more than 5 bullets (split if needed)
- [ ] Brand voice follows brands/{brand}/brand.md (confident, practical, not hypey)
- [ ] Approved phrases used where appropriate

**Research:**
- [ ] Step 1b WebSearch completed — at least 2 searches run before writing slides
- [ ] Real statistics added to Hook/Context and Why Now slides
- [ ] All external data points sourced in speaker notes

**Accuracy:**
- [ ] All product features mentioned exist in brands/{brand}/product.md
- [ ] Pricing mentioned is accurate per brands/{brand}/product.md
- [ ] No invented metrics, testimonials, or case studies
- [ ] Competitive claims supported by brands/{brand}/competitors.md
- [ ] No guaranteed promises or timeframes (unless documented in product.md)

**Visual identity:**
- [ ] Brand visual source resolved in 3-tier order at Step 1: fb.ai brand kit (`fivebucks_get_brand_kit`, checked first when `FIVEBUCKS_API_KEY` set) → local `brands/{brand}/design-system/` (when present) → `brand.md`; colors and fonts extracted before the Canva call
- [ ] When the fb.ai kit was null/unavailable and `design-system/` was absent, `brand.md` Colors + Google Font sections were used as fallback — never hardcoded from memory; never blocked on a missing key or design-system
- [ ] The Canva `generate-design` query named the brand's primary/accent colors (HEX) and font family explicitly, OR a Canva brand kit was attached via `brand_kit_id`
- [ ] Final deck visually matches the brand's fb.ai brand kit / design-system / brand.md palette (no off-brand template colors carried over from Canva defaults)

**Output:**
- [ ] Saved to outputs/{brand}/presentations/ with correct naming and metadata
- [ ] Slide count matches the agreed scope
- [ ] Agent run logged to dashboard

---

## Final Step — Log to Dashboard

See `docs/new_agent_onboarding/metrics-spec.md` for the full JSONB contract.

```
Use gateway MCP tool `fiveagents_log_run`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- skill: "campaign-presenter"
- brand: "<active-brand>"
- status: "<success|failed>"
- summary: "<1 line, <200 chars>"
- started_at: "<ISO timestamp>"
- completed_at: "<ISO timestamp>"
- metrics: {
    "date": "YYYY-MM-DD",
    "deck_type": "<weekly-review|campaign|launch|proposal|pitch>",
    "campaign": "<campaign name>",
    "deck_audience": "<leadership|team|client>",
    "slide_count": 0,
    "content_status": "Final",
    "slides": [{ "number": 1, "title": "Executive Summary", "type": "overview" }],
    "deliverable": "<filename>",
    "output_path": "outputs/{brand}/presentations/"
  }
```
