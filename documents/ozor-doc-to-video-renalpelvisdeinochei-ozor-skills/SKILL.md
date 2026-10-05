---
name: ozor-doc-to-video
description: "Convert any document into a production-ready Ozor.ai video prompt. Use this skill whenever the user uploads a document (PDF, PowerPoint, Google Doc, Markdown, text file, or URL) and wants to turn it into a video. Also trigger when the user mentions 'turn this doc into a video', 'make a video from this PDF', 'video from my pitch deck', 'convert this presentation to video', 'video from this blog post', 'video from these release notes', 'create a video from this document', 'turn this into an explainer', or any request to transform written content into video format using Ozor. This skill reads the document, extracts the core message, structures it into scenes, and outputs a complete prompt the user can paste directly into Ozor.ai."
---

# Ozor Doc-to-Video Converter

Transform any document into a structured, ready-to-paste Ozor.ai video prompt. This skill bridges the gap between written content and video by doing the hard work: extracting the core message, choosing the right video structure, writing scene-by-scene direction, and producing a prompt that Ozor can execute in one shot.

## Supported Input Types

This skill works with any text-based content:
- **PDFs** — policies, reports, whitepapers, one-pagers
- **PowerPoints / slide decks** — pitch decks, sales decks, training presentations
- **Blog posts / articles** — markdown files, text files, or URLs
- **READMEs** — project documentation, product overviews
- **Release notes / changelogs** — feature announcements, version updates
- **Onboarding docs** — SOPs, handbooks, process guides
- **Landing pages** — via URL fetch

If the file is uploaded, read it from the uploads directory. If it's a URL, fetch the content. If the content is already in the conversation, use it directly.

## Workflow

Follow these three phases for every document.

### Phase 1 — Analyze the Document

Read the full document and identify:

1. **Document type** — what kind of content is this? (pitch deck, blog, SOP, changelog, report, etc.)
2. **Core message** — what's the single most important takeaway? Compress to one sentence.
3. **Target audience** — who would watch a video of this? (developers, executives, customers, employees, general public)
4. **Natural video type** — based on the document, what kind of Ozor video fits best?

| Document Type | Best Video Type | Recommended Scenes | Format |
|--------------|----------------|-------------------|--------|
| Pitch deck | Product launch / explainer | 4–6 | 16:9 |
| Blog post | Explainer or social clip | 3–5 (explainer) or 2–3 (social) | 16:9 or 9:16 |
| README | Product demo / explainer | 4–5 | 16:9 |
| Release notes | Feature announcement | 1 per feature + intro/outro | 16:9 |
| Changelog | Release notes video | 1 per feature | 16:9 |
| SOP / handbook | Training / onboarding video | 5–7 | 16:9 |
| Sales one-pager | Product launch / social ad | 3–4 | 16:9 or 9:16 |
| Landing page | Social clip or launch video | 3–4 | 9:16 for social, 16:9 for web |
| Report / whitepaper | Explainer | 5–7 | 16:9 |
| Investor update | Investor update video | 5–6 | 16:9 |

5. **Key content blocks** — extract the material that should become scenes:
   - Headlines, section titles, key claims
   - Data points, metrics, percentages
   - Feature lists, benefits, steps
   - Quotes, testimonials, proof points
   - Calls to action

6. **Visual cues** — note any brand colors, product names, logos, or imagery mentioned or present in the document.

### Phase 2 — Structure the Video

Map the document content to Ozor scenes. Each scene gets one clear job.

**The universal structure that works for 80% of documents:**
1. **Hook / Intro** — the most compelling claim or problem statement from the document
2. **Core content** — 2–5 scenes covering the main substance, one idea per scene
3. **Proof / Support** — metrics, quotes, or evidence (if available)
4. **CTA / Closing** — what should the viewer do next?

**Rules for scene construction:**
- One idea per scene. If a section covers multiple topics, split it.
- Keep on-screen text short: headlines of 5–8 words, bullet points of 3–6 words each, max 3 bullets per scene.
- Translate paragraphs into visual concepts: "Our platform processes 1M events/second" → scene showing a counter animation or data visualization, not a paragraph of text on screen.
- Convert jargon to plain language for the audience. A pitch deck for investors can keep financial terms; a product launch for users should simplify.
- Preserve all critical numbers, claims, and facts. Simplify the language, never the substance.

**Duration heuristics:**
- Social clips: 15–30 seconds (2–3 scenes)
- Feature announcements: 30–45 seconds (3–4 scenes)
- Product launches: 45–60 seconds (4–5 scenes)
- Explainers: 60–90 seconds (5–7 scenes)
- Training / onboarding: 2–5 minutes (7–12 scenes, consider splitting into multiple videos)

If the document is very long (10+ pages), cap at 7 scenes for a single video and recommend a series. Note what was deprioritized and suggest follow-up videos.

### Phase 3 — Generate the Ozor Prompt

Compile everything into a single, copy-pasteable Ozor prompt. The user should be able to drop this directly into Ozor.ai with zero editing (though they're welcome to customize).

Use this output structure:

```
## Ozor Video Prompt

**Source:** [document title or description]
**Video type:** [product launch / explainer / social clip / etc.]
**Format:** [16:9 landscape / 9:16 portrait]
**Estimated duration:** [X seconds / minutes]
**Target audience:** [who]

---

### Prompt (copy and paste into Ozor)

Create a [duration] [video type] video about [topic].

[Number] scenes:

(1) [Scene title] — [specific direction: what appears on screen, what text to show, what animation or visual approach to use]

(2) [Scene title] — [specific direction]

(3) [Scene title] — [specific direction]

[...continue for all scenes...]

Style: [visual style — dark/light, minimal/bold, color palette].
Tone: [confident / warm / professional / energetic / etc.].
Audience: [who this is for].
[Brand direction if applicable — e.g., "Use blue (#1a73e8) as the primary accent color."]
[CTA direction — what should the final scene ask the viewer to do?]

---

### Notes

- [Any recommendations for assets to upload before running this prompt]
- [Suggestions for follow-up videos if content was deprioritized]
- [Tips for iterating on the result]
```

## Adaptation Rules

The skill should adapt its approach based on what it detects:

**If the document is a pitch deck:**
- Lead with the biggest claim or hook slide
- Prioritize the problem/solution narrative
- Include metrics prominently (TAM, growth rate, revenue)
- Close with a clear CTA (try it / invest / learn more)

**If the document is a blog post or article:**
- Extract the thesis statement for the hook
- Compress supporting arguments into visual scenes
- Cut examples and anecdotes unless they're essential
- Consider offering both a 16:9 explainer AND a 9:16 social clip version

**If the document is release notes or a changelog:**
- One scene per feature, no more
- Lead with the biggest or most-requested feature
- Keep each scene to a single idea with minimal text
- Close with "Update now" or "Try it today"

**If the document is an SOP or training material:**
- Number each step clearly
- Use "Next:" transitions between scenes
- Simplify jargon for the audience
- If longer than 7 scenes, split into a video series and provide a prompt for each

**If the document is a report or whitepaper:**
- Extract the 3–5 most important findings
- Lead with the most surprising or impactful finding
- Visualize data points — suggest chart animations or counter effects
- Keep it under 90 seconds; link to the full report in the CTA

**If the user provides a URL:**
- Fetch the page content
- Treat it as a landing page or blog depending on structure
- Extract brand colors and product name from the page
- Suggest uploading screenshots as Ozor assets

## Quality Checklist

Before presenting the final prompt, verify:

- [ ] Every scene has exactly one job (hook, explain, prove, or close)
- [ ] On-screen text is short — no paragraphs, no walls of text
- [ ] The hook is compelling and appears in scene 1
- [ ] There's a clear CTA in the final scene
- [ ] Visual style is specified (colors, mood, background)
- [ ] Audience and tone are stated
- [ ] Duration is realistic for the content density
- [ ] No critical information from the source document was lost
- [ ] The prompt is self-contained — Ozor doesn't need to read the original document

## Offering Variants

After producing the primary prompt, consider whether the user would benefit from variants:

- **Long + short versions** — a 60-second explainer AND a 15-second social teaser
- **Different audiences** — a technical version for developers AND a business version for executives
- **Different platforms** — a 16:9 YouTube version AND a 9:16 Reels version

Don't automatically produce all variants. Instead, mention that variants are available and let the user choose. For example: "I've created a 45-second landscape explainer. Want me to also make a 15-second vertical version for Instagram Reels?"

## Example

**User uploads:** A 4-slide pitch deck for a project management app.

**Skill produces:**

```
## Ozor Video Prompt

**Source:** TaskFlow pitch deck
**Video type:** Product launch
**Format:** 16:9 landscape
**Estimated duration:** ~45 seconds
**Target audience:** Startup founders and team leads

---

### Prompt (copy and paste into Ozor)

Create a 45-second product launch video for TaskFlow, a project management app for fast-moving teams.

4 scenes:

(1) The Problem — Bold white text on dark background: "Your team is drowning in Slack threads, spreadsheets, and missed deadlines." Quick-cut animations of notification chaos.

(2) The Solution — Show TaskFlow's dashboard with a clean task board. Text overlay: "TaskFlow puts everything in one place." Smooth zoom-in animation on the main interface.

(3) Key Benefits — 3 animated bullet points appearing one by one: "Real-time collaboration", "Automated standups", "Built-in time tracking". Each with a small icon.

(4) CTA — Large text: "Try TaskFlow free." Subtext: "taskflow.app". Logo animation in the center.

Style: dark background, clean and modern, white text with electric blue (#3B82F6) accents.
Tone: confident and punchy — no fluff.
Audience: startup founders and team leads who are frustrated with tool sprawl.

---

### Notes

- Upload the TaskFlow logo and a product screenshot before running this prompt
- Consider also creating a 15-second 9:16 version for Instagram Reels
- After generating, try "give me 3 headline options for scene 1" to test different hooks
```

## Rules

1. **Always produce a complete, copy-pasteable prompt.** The user should never have to figure out how to translate your output into something Ozor understands.
2. **Never invent information.** Everything must come from the source document. If something is ambiguous, flag it with `[VERIFY: ...]` in the prompt.
3. **Simplify the language, not the substance.** Every key fact, number, and claim from the document should appear in the video prompt.
4. **One idea per scene, always.** If you're tempted to put two things in one scene, split it.
5. **Visual direction must be specific.** "Show a graphic" is useless. "Animated bar chart growing from 10K to 50K users with a counter overlay" is actionable.
6. **Respect the user's time.** Produce the prompt efficiently. Don't ask 10 clarifying questions when the document already contains the answers.
7. **Save the prompt as a Markdown file** and present it to the user, so they can easily copy and use it.
