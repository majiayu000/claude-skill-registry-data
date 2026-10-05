---
name: ozor-landing-page-to-video
description: "Convert any landing page or website into an Ozor.ai video prompt. Use this skill whenever the user provides a URL, landing page content, or website copy and wants to turn it into a video. Trigger on phrases like 'make a video from my website', 'video from this landing page', 'turn my homepage into a video', 'video from this URL', 'product page to video', 'website to video', 'marketing video from my site', 'convert this page to video', or any request to transform web content into video format using Ozor."
---

# Ozor Landing Page-to-Video Converter

Transform any landing page, website, or URL into a structured, ready-to-paste Ozor.ai video prompt. This skill extracts the messaging, value props, and brand identity from web content and produces a video prompt that captures the page's essence in motion.

## Supported Input Types

- **URLs** — any publicly accessible web page
- **Landing page copy** — pasted text from a marketing page
- **Homepage content** — full homepage text and structure
- **Product pages** — feature-focused pages
- **Pricing pages** — plan comparison content
- **About pages** — company story and mission
- **App store listings** — iOS/Android app descriptions

## Workflow

### Phase 1 — Analyze the Page

Read or fetch the page content and extract:

1. **Page type** — what kind of page is this?
   - Hero-driven landing page (single product/feature focus)
   - Multi-section homepage (full product overview)
   - Product/feature page (deep dive on one capability)
   - Pricing page (plan comparison)
   - About/company page (story and mission)

2. **Core message** — the headline or hero text. This becomes the video hook.

3. **Value propositions** — extract the 3–5 key benefits or selling points. These become the middle scenes.

4. **Social proof** — look for:
   - Customer logos or counts ("Trusted by 10,000+ teams")
   - Testimonials or quotes
   - Metrics ("99.9% uptime", "2x faster")
   - Awards, press mentions, certifications

5. **CTA** — what does the page want visitors to do? ("Start free trial", "Book a demo", "Download now")

6. **Brand signals** — extract from the page:
   - Product/company name
   - Primary colors (from CSS, buttons, or visual inspection)
   - Tone of voice (professional, playful, technical, warm)
   - Logo presence

7. **Visual assets** — note any product screenshots, illustrations, or imagery that could be referenced.

### Phase 2 — Choose the Video Format

Based on the page type and likely distribution channel:

| Page Type | Primary Video | Secondary Video |
|-----------|--------------|-----------------|
| Landing page | 30–45s product launch, 8–12 scenes (16:9) | 15s social teaser, 5 scenes (9:16) |
| Homepage | 45–60s brand overview, 12–15 scenes (16:9) | 30s product highlight, 8–10 scenes (9:16) |
| Product page | 30–45s feature explainer, 8–12 scenes (16:9) | 15s feature teaser, 5 scenes (9:16) |
| Pricing page | 30s plan comparison, 8–10 scenes (16:9) | — |
| About page | 45–60s brand story, 12–15 scenes (16:9) | — |
| App listing | 15–30s app preview, 5–10 scenes (9:16) | 30s full demo, 8–10 scenes (16:9) |

Always produce the primary video. Mention the secondary as an option.

### Phase 3 — Structure the Video

Map page sections to video scenes:

**For hero-driven landing pages (most common, ~10–12 scenes):**

1. **Hook** — the hero headline, animated boldly. This is the page's main claim.
2. **Problem statement** — if the page states a pain point, show it. If not, imply it from the solution.
3. **Problem elaboration** — expand on the frustration or cost of the status quo. Use a stat or relatable scenario from the page.
4. **Solution intro** — introduce the product by name with a one-line description. Transition from the problem.
5. **Solution detail** — the product in action. Use the page's primary screenshot or describe the UI in motion.
6. **Benefit 1** — first key value prop, shown as bold text with a supporting visual or icon animation.
7. **Benefit 2** — second key value prop, same treatment.
8. **Benefit 3** — third key value prop, same treatment.
9. **Social proof — metrics** — customer count, usage stats, or performance numbers with counter animations.
10. **Social proof — logos/testimonials** — trusted-by logos scrolling, or a short testimonial quote with attribution.
11. **CTA text** — the page's call to action displayed as bold animated text.
12. **CTA with URL and logo** — "[Exact CTA]" with the page URL and product logo. Clean fade-out.

**For multi-section homepages (~12–15 scenes):**

1. **Hook** — hero headline, animated boldly on a branded background.
2. **Subheadline** — hero subtext or one-sentence product description with visual.
3. **Product overview** — high-level what-it-does scene with a screenshot or product visual.
4. **Feature 1 intro** — name and one-line benefit of the first key feature.
5. **Feature 1 visual** — screenshot, animation, or icon illustrating the feature in action.
6. **Feature 2 intro** — name and one-line benefit of the second key feature.
7. **Feature 2 visual** — supporting visual for the second feature.
8. **Feature 3 intro** — name and one-line benefit of the third key feature.
9. **Feature 3 visual** — supporting visual for the third feature.
10. **Integration / ecosystem** — partner logos, integrations, or platform reach (if on the page).
11. **Social proof — metrics** — customer count, usage stats, or performance numbers.
12. **Social proof — logos/testimonials** — trusted-by logos or a testimonial quote.
13. **Pricing or differentiator** — a quick mention of pricing advantage or key differentiator (if present).
14. **CTA text** — primary call to action as bold animated text.
15. **CTA with URL and logo** — CTA with page URL and product logo. Clean fade-out.

**For product/feature pages (~8–10 scenes):**

1. **Hook** — feature name + one-line benefit, bold animated text.
2. **Problem** — the pain point this feature solves.
3. **How It Works — Step 1** — first step of the workflow, with a UI screenshot or diagram.
4. **How It Works — Step 2** — second step, continuing the visual walkthrough.
5. **How It Works — Step 3** — third step, showing the flow in action.
6. **Result** — what the user achieves. Show the outcome with a before/after or final-state visual.
7. **Key differentiator** — what makes this feature unique vs. alternatives (speed, accuracy, ease).
8. **Social proof** — a relevant testimonial, metric, or case study tied to this feature.
9. **CTA text** — "Try [feature name]" or the page's specific call to action.
10. **CTA with URL and logo** — CTA with page URL and product logo. Clean fade-out.

### Phase 4 — Generate the Ozor Prompt

```
## Ozor Video Prompt

**Source:** [Page URL or title]
**Video type:** [Product launch / Brand overview / Feature explainer]
**Format:** [16:9 landscape / 9:16 portrait]
**Estimated duration:** [X seconds]
**Target audience:** [derived from page content]

---

### Prompt (copy and paste into Ozor)

Create a [duration] [video type] video for [Product Name], [one-line description from page].

[N] scenes:

(1) Hook — [Hero headline from the page, displayed as bold animated text on a [dark/light] background. Style matches the page's visual tone.]

(2) Problem statement — [Pain point or frustration the target audience faces, derived from page copy. Visual: text animation or relatable icon.]

(3) Problem elaboration — [Expand on the cost or consequence of the status quo. Use a stat or scenario from the page.]

(4) Solution intro — [Product name + one-line description. Transition from problem to solution. Visual: product logo reveal or name animation.]

(5) Solution detail — [The product in action. Describe the UI, dashboard, or key interaction. Visual: screenshot or screen recording style animation.]

(6) Benefit 1 — [First value prop from the page, as bold text with supporting icon or visual.]

(7) Benefit 2 — [Second value prop, same treatment.]

(8) Benefit 3 — [Third value prop, same treatment.]

(9) Social proof — metrics — [Customer count, usage stats, or performance numbers with counter animation.]

(10) Social proof — logos/testimonials — [Trusted-by logos scrolling, or testimonial quote with attribution.]

(11) CTA text — ["Exact CTA from page" displayed as bold animated text. Build urgency or excitement.]

(12) CTA with URL and logo — ["Exact CTA from page" with URL "[page URL]". [Product] logo. Clean fade-out.]

Style: [derived from page — minimal/bold/playful/corporate]. Background: [dark/light based on page design]. Primary color: [extracted from page, e.g., "#3B82F6"]. Typography: [clean/modern/serif based on page].
Tone: [derived from page copy — confident/friendly/technical/energetic].
Audience: [derived from page messaging].

---

### Notes

- Upload a product screenshot from the landing page before running this prompt
- [Brand color extracted: #XXXXXX — mention in Brand Kit]
- [Secondary video option: "Want a 15-second vertical version for Instagram Reels?"]
- [Any content from the page that was deprioritized]
```

## Adaptation Rules

**If the page is text-heavy (long-form landing page):**
- Extract only the headlines and key claims
- Ignore detailed paragraphs — video must be punchy
- Cap at 10–12 scenes regardless of page length
- Suggest a series if the page covers multiple distinct topics

**If the page is minimal (sparse startup landing page):**
- Use the limited copy as-is — don't pad
- Keep the video short (15–30 seconds)
- Focus on the hook and CTA
- Suggest the user add more context for a longer version

**If the page has strong social proof:**
- Dedicate a full scene to it
- Use customer logos in a scrolling animation
- Display metrics with counter animations
- Quote testimonials with attribution

**If the page is a SaaS product:**
- Show the product UI in at least one scene
- Describe dashboard/interface animations specifically
- Include pricing tier mention if relevant
- Focus on the primary use case, not all features

**If the page is an e-commerce product:**
- Lead with the product visual
- Include price point if it's a selling point
- Show social proof (reviews, ratings)
- CTA should be "Shop now" or "Order today"

## Brand Extraction Guide

When analyzing a page, extract brand elements:

- **Colors:** Look at buttons, headers, accents. Primary CTA button color is usually the brand's primary color.
- **Tone:** Read the copy style. Short punchy sentences = energetic/confident. Detailed explanations = professional/technical. Casual language = friendly/warm.
- **Visual style:** Dark backgrounds = modern/premium. White backgrounds = clean/minimal. Colorful = playful/creative.
- **Typography feel:** Large bold headlines = confident. Thin elegant type = premium. Rounded friendly type = approachable.

Include these observations in the prompt's style section so Ozor matches the brand's look and feel.

## Quality Checklist

Before presenting the final prompt, verify:

- [ ] The hero headline is used as the video hook (scene 1)
- [ ] Value propositions are accurately represented
- [ ] Social proof is included if the page has it
- [ ] The CTA matches the page's actual call to action
- [ ] Brand colors and style are specified
- [ ] The video tells a coherent story (not just a list of page sections)
- [ ] On-screen text is short and scannable
- [ ] Product URL is included in the CTA scene

## Rules

1. **The page's hero headline is always the video hook.** Don't rewrite it unless it's genuinely unclear.
2. **Extract, don't invent.** Every claim, metric, and benefit must come from the page. Use `[VERIFY: ...]` for anything unclear.
3. **Match the brand's visual tone.** A playful brand gets an energetic video. A corporate brand gets a polished one.
4. **Always include the URL in the CTA scene.** The whole point is driving traffic back to the page.
5. **Recommend uploading a product screenshot.** Landing pages usually have hero images that should be in Ozor's asset library.
6. **Offer a secondary format.** Most landing page videos benefit from both a 16:9 and 9:16 version.
