---
name: ai-banner-design
description: Research and create a channel-ready commercial banner for a specific placement such as a website or SaaS hero, YouTube channel banner, paid display ad, social cover, email header, marketplace campaign, or event promotion. Use when current dimensions, safe areas, crop behavior, file requirements, industry conventions, references, exact copy, and a distinctive banner composition must be resolved before image generation; do not use for posters, thumbnails, responsive web implementation, multipage campaigns, or generic images without a banner placement.
---

# AI Banner Design

Research the placement before designing. Deliver one banner whose dimensions, safe area, hierarchy, references, and visual direction fit its actual commercial use.

## Catalog

- Display name: AI Banner Design
- Categories: Commercial Production, Layout & Design
- Status: Ready
- Route label: Research plus GPT Image 2 banner production
- Tone: lime
- Short description: Research and design channel-ready commercial banners.
- Similar skills: make-thumbnail, poster-design, product-detail-page
## What this skill does

- Resolves the banner's placement, crop behavior, and safe area through live official research when available or a labeled built-in preset when browsing is unavailable.
- Searches a focused set of current industry references when the harness supports it; search failure does not block the Banner workflow.
- Converts the business message into one banner hierarchy and one distinctive visual direction.
- Uses GPT Image 2 Medium for every final banner; Midjourney may only create an optional text-free artistic-direction reference upstream.

## How to use

State where the banner will appear, what it should communicate, and any exact copy or brand assets. The Agent checks current requirements when browsing is available and otherwise uses a matching dated preset.

#### Create a software website hero

```text
Create a website hero banner for our AI workflow product using the headline “Work moves itself”.
```

#### Create a YouTube channel banner

```text
Create a YouTube banner for a practical AI-tools channel called “Applied AI Lab”.
```

#### Create a paid display banner

```text
Create a Google display banner for our accounting software trial campaign.
```

## Workflow

### 1. Resolve the placement

Compile:

```yaml
channel: website | YouTube | Google Ads | social | email | marketplace | print | other
placement: hero | channel cover | display slot | profile cover | header | campaign banner
market_and_device: supplied or researched
objective: awareness | launch | conversion | announcement | navigation
exact_copy: headline | support line | CTA | brand name
assets: product | person | logo | brand | style
deliverables: one master unless variants are explicitly requested
```

When the user supplies a product, person, logo, existing banner, or other original asset, keep the actual file as a model input and assign it an explicit role. Do not replace an available original with a prose reconstruction. A style reference guides treatment; it does not authorize copying or replace the subject source.

If placement cannot be inferred, ask where the banner will appear before generation; placement changes ratio, safe area, crop, text policy, and output format. Do not accept “banner” as a sufficient specification.

### 2. Research current requirements

Read [references/research-and-placement.md](references/research-and-placement.md). Do not assume the harness has browsing or search tools.

When browsing is available, make one reasonable attempt to open current official platform documentation for the named placement. Record access date, market, dimensions, ratio, file size/format, safe area, device crop behavior, and content restrictions. A missing browser/search tool, blocked request, login wall, timeout, unreadable official page, or failed search means live verification is unavailable. Do not loop across search providers or invent current values; immediately use the closest exact built-in preset below.

| Placement preset | Fallback canvas and ratio | Safe-area and content rule | Preset status |
| --- | --- | --- | --- |
| YouTube channel banner | 2560×1440, 16:9, PNG/JPEG, maximum 6 MB | Keep every logo, face, product, title, and CTA inside a centered 1235×338 conservative zone; only expendable background reaches the outer crop area | Dated official snapshot, 2026-08-18 |
| Generic website/SaaS hero | 1920×1080 working master, 16:9 | Keep all essential content inside the central 60%; extend nonessential background laterally for shallow desktop or 21:9 crops | Project working preset, 2026-08-20; not a platform rule |
| Google responsive display — landscape (explicit legacy placement) | 1200×628, 1.91:1, maximum 5120 KB | Use one clean focal image; no overlaid headline, logo, fake button, border, or collage because platform text/logo assets are separate | Dated official snapshot, 2026-08-20 |
| Google responsive display — square (explicit legacy placement) | 1200×1200, 1:1, maximum 5120 KB | Same clean-image rule; treat this as a separate deliverable, never a panel in one sheet | Dated official snapshot, 2026-08-20 |
| Google responsive display — vertical (explicit legacy placement) | 900×1600, 9:16, maximum 5120 KB | Same clean-image rule; keep the product or service visually dominant | Dated official snapshot, 2026-08-20 |
| Common Google static display slots | 300×250, 336×280, 728×90, 970×90, 468×60, 300×600, or 160×600 | Use the one explicitly requested slot and verify legibility at native size; if no slot is named, ask whether the ad is responsive or static | Dated official snapshot, 2026-08-18 |
| Generic social/profile cover | 1920×1080 working master, 16:9 | Keep essential content inside the central 60%; treat the edges as expendable crop area | Project working preset, 2026-08-20; not upload-ready for a named platform without verification |
| Generic email header | 1200×400 export, 3:1, intended for 600×200 display at 2× density | Keep essential content inside the central 90%; prefer live HTML for critical copy when the template supports it | Project working preset, 2026-08-20; confirm the real template when available |

For the YouTube fallback, keep the smaller 1235×338 zone as an absolute centered zone on the 2560×1440 master; do not scale it up. The dated official evidence described that zone at the minimum canvas, and the offline preset intentionally sacrifices usable width to reduce cross-device crop risk.

User-supplied exact dimensions override every preset. A matched dated official snapshot may be used to continue the job, but label it as not live-verified. A project working preset is a design master, not a claim of current platform compliance. If no preset matches, ask for exact dimensions when upload-readiness matters; otherwise use the generic 1920×1080 concept master and label it `concept only`.

Google's official help currently notes a 2026 migration from Display Ads toward Demand Gen. Use the responsive-display presets only when the user explicitly names that legacy placement; when “Google banner” is ambiguous, resolve responsive display, static display, or Demand Gen before selecting dimensions.

Record the provenance in the acceptance record:

```yaml
spec_source: live_official | built_in_official_snapshot | built_in_project_preset | user_supplied
spec_snapshot_date: YYYY-MM-DD | null
live_verification_status: verified | browser_unavailable | search_failed | official_page_unreadable | not_attempted
limitations: current-platform compliance not claimed when a preset was used
```

When the user gives a generic software/SaaS website banner with no ratio, treat it as a responsive website hero only if the context supports that inference. Use a 16:9 master with all essential content inside the central 60% and enough lateral continuation for 21:9 or shallow desktop crops; otherwise ask for the placement.

Separate:

- `hard requirement`: current official rule;
- `dated official snapshot`: a built-in fallback used without claiming live verification;
- `observed pattern`: recurring design behavior in references;
- `recommendation`: the selected design decision.

### 3. Research visual references

Search 6–10 current references from the same industry, audience, placement, and approximate price/brand tier. Prefer official brand campaigns, product pages, channel pages, or reputable design archives. Annotate only what to learn: hierarchy, crop, subject scale, copy density, palette logic, typography behavior, visual device, and differentiation opportunity.

If browsing is unavailable or reference search fails, do not fabricate sources or block the task. Use supplied references when present; otherwise derive one direction from the brand, audience, objective, category conventions, and the anti-generic constraints below. Record `reference_research: unavailable` and proceed. Midjourney remains optional only for the text-free artistic-direction reference described below.

Do not copy a competitor's composition, wording, logo, trade dress, mascot, or signature imagery. Synthesize recurring patterns and choose one deliberate way to differ. Skip broad reference search only when the user supplies an approved direction or reference set.

When the researched references do not establish a strong enough artistic direction, Midjourney may generate a text-free direction reference. Treat that output as internal style guidance only: do not size it as the requested banner, add banner copy, present it as a candidate final, or deliver it to the user as the banner. Select only the useful visual treatment, then pass that image to GPT Image 2 as an `artistic-direction reference`; it never replaces the user's product, person, logo, or brand assets.

### 4. Build the banner brief

Resolve one design direction:

```yaml
message: what viewers understand in one second
hierarchy: brand | headline | support | CTA
focal_subject: product | person | interface | type | concept
visual_device: one imageable idea tied to the subject
composition: focal zone | copy zone | scan path | safe area | crop continuation
brand_system: palette | typography behavior | materials | logo rule
reference_synthesis: common pattern | differentiation | prohibited copying
delivery_spec: exact pixels | ratio | format | file limit
```

For a software banner, show a meaningful product behavior, interface moment, workflow metaphor, or recognizable domain artifact. Reject generic purple gradients, floating glass cards, random 3D shapes, empty dashboards, and abstract blobs unless the brief specifically justifies them.

### 5. Select the model

- GPT Image 2 Medium through `gpt-image` v1.0 owns every final banner, including an intentionally text-free final. Any headline, CTA, brand name, Chinese, multilingual content, or other readable copy makes this route mandatory.
- When originals exist, upload them and pass their returned URLs through the selected route's documented image-input fields. State which source controls subject, logo, brand, composition, or style, and preserve only the properties supported by that role.
- Use GPT Image 2 in reference-aware mode when an existing banner or brand composition must change without losing approved assets.
- Midjourney is allowed only in Step 3 to create an optional text-free artistic-direction reference when research and supplied references are insufficient. Its output is not a banner, is never a deliverable, and must be supplied back to GPT Image 2 as style guidance for final production.
- Never use Midjourney, Z-Image, Nano, Seedream, `ai-banner`, or another specialist endpoint as the final Banner route or as a fallback after a GPT Image 2 text failure.
- Default to one GPT Image 2 Medium result, `batchCount: 1`, and a supported ratio that can be deterministically resized or cropped to the researched delivery dimensions. Low is only a named layout draft.

### 6. Compile a concise Prompt

Start from the cleaned WeShop Banner default only for a SaaS/product-release website hero. Start from the cleaned YouTube default only for a YouTube channel banner. Replace their sample brand, copy, palette, and theme with verified user inputs.

Keep research and requirements internal. Submit concise natural prose:

```text
Design one [placement and ratio] banner for [brand/product/audience]. Render “[exact copy]” with [hierarchy] inside [safe area]. Make [message] visible through [one visual device], using [focal subject and composition]. Preserve [assets]. Use [specific direction distilled from research] while remaining original. Continue nonessential background detail into crop zones. No [placement-specific failures or invented copy].
```

Do not send URLs, competitor names, research notes, field labels, or long banned lists to the image model.

If Midjourney supplied an artistic-direction reference, bind it only to visual treatment in the GPT Image 2 Prompt. Do not inherit its text, subject identity, composition, or accidental brand-like elements.

### 7. Generate, finish, and accept

Execute the final banner through `gpt-image` v1.0 / GPT Image 2 Medium and poll to terminal state. Resize, crop, or apply deterministic typography after generation when required for exact platform dimensions or text fidelity.

Keep the original input file unchanged. When the run uses supplied imagery, preserve those files as separate original/source assets. Never present a generated surrogate as the user's original.

Accept only when:

1. Dimensions, ratio, file format/size, safe area, and crop behavior satisfy either the live researched placement or one exact built-in preset; preset use is labeled with its snapshot date and is never presented as live verification.
2. Brand, headline, support copy, CTA, and focal subject follow one clear scan path and remain legible at delivery size.
3. Required product, person, interface, logo, and brand assets meet their preservation level.
4. The visual direction fits the industry's context without copying a reference or collapsing into a generic template.
5. Device or placement crops remove only expendable background detail, never essential copy, logos, faces, products, or CTAs.
6. No invented claim, price, date, logo, button behavior, filler text, watermark, or unsupported platform statement appears.

### 8. Retry one failed property

Retry once on GPT Image 2 with a non-identical Prompt naming only the failed property. Tighten the safe area for crop failures, remove optional copy for text failures, strengthen one asset lock for reference drift, or replace the visual device when the result is generic. Midjourney is not a production fallback. Do not solve exact-pixel or font-level failures by repeating the same generative request; finish deterministically when permitted. Record sources, access date, model, parameters, Prompt revision, execution ID, error, retryability, refund state, and failed acceptance item.

When this Skill selects GPT Image 2, use `quality: "medium"` and `imageSize: "2K"` by default; change either only when the user explicitly requests another tier.

Every GPT Image 2 call in this Skill defaults to Medium at 2K; use another tier only when the user explicitly requests it.

## User-facing output

- Media type: One researched-or-preset banner image plus a compact specification and acceptance record
- Default quantity: 1 master banner; additional placements are separate deliverables
- Content per image: One commercial objective, one focal hierarchy, and placement-safe exact copy
- Default layout: Researched placement dimensions; inferred SaaS website hero uses a responsive 16:9 master
- Video output: No
- Specification source: Live official research when available; otherwise a labeled built-in official snapshot, project working preset, or user-supplied dimensions
- Model policy: GPT Image 2 Medium produces every final banner; Midjourney may only produce an optional text-free artistic-direction reference that is then supplied to GPT Image 2
- Downstream use: Website heroes, YouTube channels, paid display, social covers, email headers, marketplace campaigns, launches, and announcements
