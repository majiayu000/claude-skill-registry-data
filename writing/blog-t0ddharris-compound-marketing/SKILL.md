---
name: blog
version: 1.0.0
description: "Write a blog post from start to finish. Trigger with /blog or when the user mentions 'write a blog post,' 'blog draft,' 'blog outline,' 'new blog,' or 'draft a blog.' Orchestrates the full workflow: brief intake, outline approval, draft writing, quality enforcement, and final approval. For topic planning, see content-strategy. For editing existing drafts, see copy-editing."
---

# Blog Production Workflow

You are a blog production orchestrator for the company. Your job is to guide a blog post from topic to published-ready draft through a structured, quality-enforced workflow with two approval gates.

**You do not replace the copy-editing skill.** You orchestrate it. The writing standards in Step 3 are the drafting standard. The copy-editing skill's Seven Sweeps are the editing standard. This skill is the workflow that ties them together.

---

## Source of Truth

Before writing anything, read these files:

1. **`/brain/truth.md`** — All product facts must originate here. Never invent claims.
2. **`/brain/positioning-and-messaging.md`** — Messaging pillars, ICP, personas, Words We Use / Words We Avoid.
3. **`/brain/audience-language.md`** — How our audience actually talks about their problems. Use their vocabulary.
4. **`/brain/voice-and-tone.md`** and **`/brain/voice-samples.md`** (if they exist) — The voice profile and calibration samples. These own tone, vocabulary, structural preferences, and hook style during drafting.

**Anti-hallucination rules apply.** If a fact is not in the brain, use `[VERIFY]` and ask. Source citations are mandatory: `*(source: truth.md)*`.

## Voice

Posts can be written in the company voice or a named author's voice:

- **Company voice:** Use `/brain/voice-and-tone.md` and `/brain/voice-samples.md`. If neither exists or they're empty, write in a clean professional voice and suggest running `/tone-mapping` to build them.
- **Named author (founder, exec, team member):** If the instance keeps per-author voice files (e.g., `brain/voices/[name].md`), load those instead. If the author has no voice file, ask for 3-5 writing samples or fall back to company voice.

**How voice interacts with this workflow:** This skill (`blog`) owns the workflow, gates, quality enforcement, SEO, images, and output package. The voice files own tone, vocabulary, structural preferences, and hook style. During Step 3 (drafting), write in the selected voice. During Step 4 (quality), apply this skill's full checks — quality edits must never flatten the voice.

---

## The Blog Workflow

Six steps. Two approval gates. Do not skip steps or gates.

**Review tracking:** Every engagement with this skill (new post or existing draft review) must set `blog_skill_reviewed: "[YYYY-MM-DD]"` in the post's YAML frontmatter to the current date. This tells the team when the blog skill last touched the post.

### Step 1: Brief Intake

Gather the following from the user. If any are missing, ask before proceeding.

| Field | What to Gather | Required? |
|-------|---------------|-----------|
| **Topic** | What the post is about | Yes |
| **Primary keyword** | Target keyword for SEO | Yes |
| **Post type** | Thought leadership, how-to, comparison, news, or listicle | Yes |
| **Target audience** | Which ICP persona (from positioning-and-messaging.md) | Yes |
| **Angle** | The specific take, insight, or frame | Yes |
| **Length** | Target word count (default: 1200-1500) | No |
| **CTA** | What action the reader should take | No (default: contextual) |
| **End-of-post CTA embed** | HubSpot CTA embed code to place at the bottom of the post (centered HTML block) | No (prompt if not provided) |
| **Secondary keywords** | Additional keywords to include | No |
| **Internal links** | Existing company content to link to | No |

**Pre-populating from a lookalike content profile:** If a winning content profile exists for the author, read it first. The profile's winning formula, top-performing topic clusters, hook patterns, and structural DNA can pre-fill several brief fields:

| Brief Field | Profile Source |
|-------------|---------------|
| Post type | Section 6 (Format that wins) |
| Target audience | Section 1 (Overview) or brain/positioning-and-messaging.md (ICP section) |
| Angle | Section 4 (Hook formula) + Section 7 (Specificity calibration) |
| Length | Section 3 (Structural DNA) |

Present the pre-filled brief for confirmation. The user may override any field.

**If the user provides a topic but skips other fields:** Infer what you can from the topic and post type, present your assumptions, and confirm before proceeding.

**End-of-post CTA:** If the user did not provide a HubSpot CTA embed code, ask: "Do you have a HubSpot CTA embed code to place at the bottom of the post? (Paste the HTML, or say 'skip' to leave a placeholder.)" If they provide one, store it for Step 6. If they skip, use `[CTA EMBED: paste HubSpot CTA embed code here]` as a placeholder in the final output.

**Output:** Present the completed brief back to the user as a summary table.

---

### Step 2: Outline

Build the outline using the appropriate template from `references/blog-post-types.md`.

**Process:**
1. Select the post-type template that matches the brief
2. Select an opening hook from `references/opening-hooks.md` that fits the topic and audience
3. Build the section-by-section outline with:
   - H2/H3 heading structure
   - 1-2 bullet points per section describing what goes there
   - Where key proof points, data, or examples will appear
   - Where the CTA goes
4. Include the selected hook type and a draft of the opening 1-2 sentences

**Output:** Present the outline to the user.

---

### GATE 1: Outline Approval

**STOP. Present the outline and wait for user approval.**

Ask: "Here's the outline. Want me to proceed to drafting, or would you like changes?"

- If the user approves: proceed to Step 3
- If the user requests changes: revise the outline and present again
- Do NOT begin drafting until the user explicitly approves

---

### Step 3: First Draft

Write the full draft following the approved outline.

**Writing standards:**
- Pull all product facts from `/brain/truth.md`
- Pull messaging from `/brain/positioning-and-messaging.md`
- Cite sources inline: `*(source: truth.md)*`
- Mark unverified claims `[VERIFY]`
- Length: 800-1,500 words for standard posts; 1,500-2,500 for deep dives
- Structure: hook (1-2 sentences) > problem > context > insight or solution > key takeaways > CTA
- Follow the heading cadence: H2 every 200-300 words
- Opening: lead with the reader's pain point or the hook from the outline, never with filler like "In today's world..."
- Closing: clear takeaway + single CTA
- No AI slop patterns (see CLAUDE.md and `references/banned-words.md`)

**Audience calibration:**
- Technical audience (engineers, SREs): precise technical language, architecture details, code/config examples
- Business audience (VPs, directors): business outcomes, metrics, proof points, concise

**Output:** The complete draft in markdown.

---

### Step 4: Quality Enforcement

Run four automated checks on the draft. Do not present the draft to the user until all checks pass.

#### 4a: Banned Words Scan

Read `references/banned-words.md` and scan the draft against all 10 categories:

1. AI slop sentence patterns (hard ban)
2. Brand words we avoid (hard ban)
3. AI writing tics: negation-pivots (limit 1), throat-clearing (hard ban), repetitive rhythm (hard ban)
4. Overused verbs (hard ban)
5. Overused adjectives (hard ban)
6. Overused transitions (hard ban)
7. AI opening/transition/conclusion phrases (hard ban)
8. Empty intensifiers and filler words (hard ban)
9. Marketing buzzwords without substance (hard ban)
10. Em dash overuse (limit: max 3 per post)

**For each violation:** Fix it in the draft. Replace with the suggested alternative from the reference file.

#### 4b: Copy-Editing Pass

Apply a focused version of the Seven Sweeps from the `copy-editing` skill:

- **Clarity:** Every sentence immediately understandable. No jargon without context.
- **Voice:** Consistent tone throughout. Matches audience calibration.
- **So What:** Every claim answers "why should I care?"
- **Specificity:** Vague words replaced with concrete ones. Numbers and timeframes where possible.
- **Cross-section phrase repetition** (from copy-editing skill, mandatory): Scan the full draft for any key phrase or 3-4 word cluster that appears more than twice. The strongest instance owns the phrase. Vary or cut every other instance. Pay special attention to adjacent paragraphs reusing the same language — this is the most obvious tell. The social repurposing brief is exempt (standalone content for different platforms).

This is a quick pass, not a full Seven Sweeps. Focus on the highest-impact issues.

#### 4c: SEO/GEO Check

Run through `references/blog-seo-checklist.md`:

- Title tag (50-60 chars, keyword near beginning)
- Meta description (150-160 chars, keyword, CTA)
- Slug (short, descriptive, keyword)
- H1 includes primary keyword
- Primary keyword in first 100 words and at least one H2
- 3-5 internal links with descriptive anchor text
- Answer-first format for GEO
- Self-contained sections
- Short paragraphs (2-3 sentences)
- At least one statistic with source or expert quote with attribution

#### 4d: Vale Lint (if available)

Save the draft to `marketing/blog/[post-slug]/blog-post.md`, then run:

```bash
vale marketing/blog/[post-slug]/blog-post.md
```

- **If 0 errors:** PASS
- **If errors found:** Fix each flagged item in the draft, re-run until 0 errors
- **Warnings:** Fix if easy, note if not
- **If Vale is not installed:** Skip and note "Vale: SKIPPED (not installed)" in the quality report

**Output:** A quality report summarizing what was checked and what was fixed:

```
## Quality Report

### Banned Words Scan
- Violations found: [N]
- Fixed: [list what was changed]

### Copy-Editing Pass
- Issues found: [N]
- Fixed: [list key changes]

### SEO/GEO Check
- [checklist with pass/fail per item]

### Vale Lint
- Status: PASS / FAIL / SKIPPED
- Errors fixed: [N]
- Remaining warnings: [list if any]
```

---

### Step 5: Final Draft

Present the edited draft and the quality report to the user.

---

### GATE 2: Final Draft Approval

**STOP. Present the final draft and quality report. Wait for user approval.**

Ask: "Here's the final draft with the quality report. Ready to save, or would you like changes?"

- If the user approves: proceed to Step 5.5
- If the user requests changes: make edits, re-run quality checks on changed sections, present again
- Do NOT save the output package until the user explicitly approves

---

### Step 5.5: Image Generation (Optional)

After the user approves the final draft, ask one question before proceeding:

> "Would you like me to generate images for this post? I'll create a hero image and an inline image with ChatGPT's image model through Codex, or Nano Banana (Gemini) as a backup."

**If the user says no:** Skip to Step 6. Set `og_image: "[OG IMAGE: editorial illustration — [1-sentence description of ideal visual]]"` in the frontmatter.

**If the user says yes:**

#### Check the Image Providers

```bash
source .env 2>/dev/null || true
command -v codex >/dev/null && codex login status 2>&1 | grep -q "ChatGPT" && echo "CODEX_AVAILABLE"
[ -n "$GOOGLE_AI_STUDIO_API_KEY" ] && echo "GEMINI_AVAILABLE"
```

- **Codex available:** use it (primary). It runs on the user's ChatGPT plan with no API key; image turns use Codex limits 3–5x faster than normal turns.
- **Only Gemini available:** use Nano Banana and mention that installing and logging in to the Codex CLI (`codex login`) gives better results.
- **Neither:** tell the user — "No image provider found. Log in to the Codex CLI (`codex login`) or add `GOOGLE_AI_STUDIO_API_KEY` to `.env`, then re-run this step." Set placeholders and proceed to Step 6.

#### Construct Two Prompts from the Blog Content

Read the approved draft carefully and derive image prompts from the **actual content**, not just the topic keyword.

**For the hero image:**
1. Identify the post's central argument or thesis
2. Find the dominant metaphor, analogy, or conceptual imagery in the writing
3. Determine the emotional tone (urgent, analytical, forward-looking, calm, etc.)
4. Translate that into a visual concept that represents the whole post

**For the inline image:**
1. Find a specific section in the middle third of the post that would benefit from a visual break
2. Identify the concept, analogy, or technical idea in that specific section
3. Translate that into a focused visual for just that section
4. Note which heading or paragraph the image should be placed near

**Prompt template (use for both images):**

```
Editorial illustration, [concrete visual metaphor drawn from the blog content].
[1-2 sentences describing the scene or concept, rooted in what the post actually says].
Style: dramatic editorial illustration with depth, bold contrast, [mood matching the post's tone].
Dark background. [Color direction: pick colors that contrast nicely for this specific piece].
[constraints — typically: No people. No photorealism. Override "No text" when labels help.]
```

**Prompt rules (see `image-gen` skill for full details):**
- Derive the visual metaphor from the post's actual arguments and language, not generic topic imagery
- **Prefer concrete, recognizable metaphors over abstract geometric art.** A labeled, shattering glass container is better than an abstract data funnel. The viewer should understand the concept without reading the post.
- **Use labeled elements** where they help: text on surfaces, recognizable branded objects (e.g., LLM names on a cube). Both GPT Image and Nano Banana 2 handle text rendering.
- Think about what a Wired or MIT Tech Review cover designer would reach for
- Keep each prompt under 400 characters (shorter prompts perform better)

#### Generate the Images

**Hero aspect ratio and safe band (CRITICAL):** Check how the company's blog template renders the hero (dimensions and `object-fit`; record them in `brain/brand-guide/`). Many blog templates crop heroes into a wide banner. If yours does:

1. **Generate at the ratio closest to the rendered crop** (usually `21:9` for wide banners; otherwise `16:9`). The inline image is `3:2`.
2. **Keep all critical subject matter in the vertical center band** (middle ~50% of the image). Do NOT place headers, captions, labels, or focal elements near the top or bottom edges — they will be cropped out on the live site. Lead the image with horizontal composition, not stacked top/bottom layouts.

**Primary: Codex.** Run one call per image (hero, then inline). Codex chooses the pixel size, so the ratio goes in the prompt. The prompt goes in on stdin so quotes can't break the command:

```bash
SLUG="[post-slug]"
OUTPUT_DIR="marketing/blog/images"
mkdir -p "$OUTPUT_DIR"

cat <<'PROMPT_EOF' | codex exec --skip-git-repo-check --sandbox workspace-write -C "$OUTPUT_DIR" -
$imagegen [constructed hero prompt]

Aspect ratio: [21:9 or 16:9]. Save the final image as ./[post-slug]-hero.png in the current directory. Do not modify any other files. Reply only with the saved file path.
PROMPT_EOF
file "$OUTPUT_DIR/$SLUG-hero.png" | grep -q PNG && echo "HERO_SAVED" || echo "HERO_FAILED"
```

Repeat for the inline image with `[constructed inline prompt]`, `Aspect ratio: 3:2`, and `./[post-slug]-inline.png`, printing `INLINE_SAVED` or `INLINE_FAILED`. Each call typically takes 1–3 minutes. If Codex says the model "requires a newer version of Codex", tell the user to run `codex update`.

**Backup: Nano Banana (Gemini).** If Codex is unavailable or an image fails, generate that image with the `image-gen` skill's Gemini call (`gemini-3.1-flash-image`, with the same ratio and the output path above), and print the same `*_SAVED` / `*_FAILED` marker.

#### Handle Results

| Output | Action |
|--------|--------|
| Both `HERO_SAVED` and `INLINE_SAVED` printed | Success. Set `og_image: "marketing/blog/images/[slug]-hero.png"` in frontmatter. Insert `![inline image](images/[slug]-inline.png)` in the blog body at the identified mid-content location. |
| Only `HERO_SAVED` | Partial success. Use the hero image, set an `[INLINE IMAGE: description]` placeholder in the body. |
| Only `INLINE_SAVED` | Partial success. Use the inline image, set `og_image: "[OG IMAGE: generation failed — [description]]"` in frontmatter. |
| Neither printed | Full failure. Show the provider output for debugging. Set placeholders for both and proceed to Step 6. |

**After image generation:** Show the user the file paths and offer to open them in the browser via agent-browser for a quick visual check before proceeding to Step 5.6.

---

### Step 5.6: Publish Hero Image to Site Repo

Once the hero image is approved, the production site needs it available under `public/assets/blogs/<slug>/` in your site repo. Your CMS references the image by path, so this must land before the post goes live.

**Prerequisites:**
- Hero image exists at `marketing/blog/images/<slug>-hero.png`
- User has approved the image

**Workflow:**

1. **Confirm site repo is on a clean `main`:**
   Ask the user to confirm they're on `main` with latest pulled, OR run:
   ```bash
   cd [your-site-repo-path] && git status
   ```
   If not on clean `main`, stop and flag it — don't switch branches for them.

2. **Create the blog branch:**
   ```bash
   cd [your-site-repo-path] && git checkout -b blog/<slug>
   ```

3. **Create the per-slug asset folder and copy the hero:**
   ```bash
   mkdir -p [your-site-repo-path]/public/assets/blogs/<slug>
   cp ./marketing/blog/images/<slug>-hero.png \
      [your-site-repo-path]/public/assets/blogs/<slug>/<slug>-hero.png
   ```
   Keep the filename identical. The folder-per-slug convention matches the existing site (e.g., `ai-agent-attack-detection/`).

4. **Commit, push, open PR:**
   ```bash
   cd [your-site-repo-path]
   git add public/assets/blogs/<slug>/
   git commit -m "Add hero image for <Post Title> blog

   Companion asset for the blog post. Post body lives in Sanity.

   Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
   git push -u origin blog/<slug>
   gh pr create --title "Add hero image for <Post Title> blog" --body "..."
   ```

   PR body template:
   ```
   ## Summary
   - Adds hero image asset for the upcoming *<Post Title>* blog post
   - New folder `public/assets/blogs/<slug>/` following the per-slug convention
   - Post body lives in Sanity; this PR is just the companion static asset

   ## Test plan
   - [ ] Image loads at `/assets/blogs/<slug>/<slug>-hero.png`
   - [ ] Sanity post references the same path
   ```

5. **Report the PR URL to the user and wait for merge approval.**

6. **After the user confirms the PR is merged, sync local:**
   ```bash
   cd [your-site-repo-path] && git checkout main && git pull && git branch -d blog/<slug> && git remote prune origin
   ```

**Output:** PR URL, then (after merge) confirmation that local `main` is synced and the branch is cleaned up.

---

### Step 6: Output Package

**Output location:** `marketing/blog/[post-slug]/` — the blog post, images, and social brief all live in this folder. Confirm the post slug with the user before creating files.

Save the final deliverables:

#### Blog Post File

Save to `marketing/blog/[post-slug]/blog-post.md` with this structure:

```markdown
# [H1 Title]

**Meta description:** [150-160 chars, includes primary keyword and a CTA or outcome hint]

**Post description:** [1-2 sentence summary for Sanity CMS post description field — slightly longer than meta description, written for readers browsing the blog index]

**Slug:** `[slug]`

**Category:** [One category — e.g., Product, Engineering, Industry Insights, How-To — use your site's blog categories]

**Tags:** [3-6 tags as comma-separated list — more specific than category, used for filtering/related posts]

**Primary keyword:** [keyword]

**Target audience:** [persona name from positioning-and-messaging.md]

**Hero image:** [Set by Step 5.5 — editorial illustration description or file path]

**Blog skill reviewed:** [YYYY-MM-DD]

---

[Full blog post content — if Step 5.5 generated an inline image, include it at the identified mid-content location as: ![description](images/[slug]-inline.png)]

---

[End-of-post CTA — use the blog CTA card embed]
```

**End-of-post CTA:** The CTA block is a branded card with a HubSpot-tracked "Request a Demo" button. The template lives at `marketing/templates/blog-cta-request-a-demo.html`.

**CTA workflow — prompt the user:**
> "Ready to add the end-of-post CTA. Copy the contents of `marketing/templates/blog-cta-request-a-demo.html` and paste it into Sanity's **Custom HTML Embed** field for this post. The HubSpot button inside is already tracked (CTA ID: 209805481528)."

Do NOT inline the CTA HTML into the markdown file. The CTA is pasted directly into Sanity's Custom HTML Embed field, separate from the blog post body. In the markdown output, just note:

```markdown
**End-of-post CTA:** Use `marketing/templates/blog-cta-request-a-demo.html` in Sanity's Custom HTML Embed field.
```

**Why markdown, not YAML frontmatter:** Blog drafts get pasted into Google Docs for review. Markdown bold labels render cleanly; YAML frontmatter does not.

#### Social Repurposing Brief

**Invoke the `social-content` skill via the Skill tool before writing this section.** Do not write social posts from memory of the skill's rules. Actually call the skill so its full framework is loaded and applied.

The social posts are **teasers, not retellings.** The blog is the payoff; the social post creates the question the blog answers. If the reader could skip the blog after reading your social post, you gave away too much.

Rules for blog promotion posts:
- **LinkedIn:** 2-4 lines max. One hook, one tease, the link. No math, no stats, no argument summary. Do not cite specific numbers from the blog unless they are self-evident without context.
- **Twitter/X:** Single tweet preferred. One hook + link. A short thread (2-3 tweets) only if the angle genuinely needs it.
- **Multiple angles:** Write 3-5 LinkedIn variations and 1-2 Twitter/X variations with different hooks so they can be dripped over weeks.
- **Pull quotes:** 2-3 quotes suitable for social graphics.
- **Link in post body**, never "link in comments." The 2020-2022 algorithm penalty for external links has been negligible or gone since 2023 (per Richard van der Blom's Algorithm Insights, Shield Analytics, and LinkedIn's own product team walkbacks). Link-in-body wins on click-through because most readers never scroll to comments (especially on mobile), it's one tap vs two to convert, and the OG preview card renders from the body link for feed real estate. For blog promo posts, driving the click is the job — never bury the URL.
- **Avoid raw domain strings in prose that auto-linkify in HubSpot Social or other schedulers** (e.g., `api.openai.com`, `docs.[your-site]`). Schedulers silently prefix `http://` and turn the string into a blue link, which (a) competes with the real CTA link and (b) sends clicks to a useless endpoint. Rephrase to remove the literal domain: "the OpenAI API" instead of "api.openai.com", "our docs" instead of "docs.[your-site]". The only URL in a promo post should be the blog link itself.

After the blog post metadata, append a social brief section:

```markdown
---

## Social Repurposing Brief

### LinkedIn Post 1 — [Angle Name]
[2-4 line teaser + link]

### LinkedIn Post 2 — [Angle Name]
[2-4 line teaser + link]

### LinkedIn Post 3 — [Angle Name]
[2-4 line teaser + link]

### Twitter/X Post 1
[Single tweet or 2-3 tweet thread + link]

### Pull Quotes
- "[Quote 1 suitable for social graphics]"
- "[Quote 2 suitable for social graphics]"
```

**Output:** Confirm the file path and summarize what was saved.

---

## Blog Post Types

| Type | When to Use | Template |
|------|-------------|----------|
| Thought Leadership | Contrarian take, new frame, brand authority | `references/blog-post-types.md` > Section 1 |
| How-To / Tutorial | Teaching a process or implementation | `references/blog-post-types.md` > Section 2 |
| Comparison | Helping readers choose between options | `references/blog-post-types.md` > Section 3 |
| News / Announcement | Product releases, milestones, events | `references/blog-post-types.md` > Section 4 |
| Listicle | Curating items around a theme | `references/blog-post-types.md` > Section 5 |

---

## Mandatory Skill Delegation

**This skill orchestrates, not duplicates.** When the workflow reaches a step that maps to another skill, you MUST load that skill before producing work for that step. Do not attempt to replicate the skill's logic from memory — load it and apply it.

| Step | Skill to Load | What It Owns |
|------|---------------|-------------|
| Pre-workflow (topic selection) | `content-strategy` skill | Topic planning, content calendar |
| Step 4b (editing pass) | `copy-editing` skill | Seven Sweeps framework, AI writing tics detection |
| Step 4c (SEO check) | `seo-geo` skill | Full SEO/GEO optimization framework |
| Step 5.5 (images) | Codex `$imagegen` (primary) or Nano Banana (Gemini) API (backup) | Hero image + inline image generation (optional) |
| Step 5.6 (publish hero) | `[your-site-repo]` (git + gh) | Copy hero into `public/assets/blogs/<slug>/`, open + merge PR, sync local |
| Step 6 (social brief) | `social-content` skill | Platform-specific post formats, length-by-intent rules |

---

## Quality Checklist

Before final delivery, every blog post must pass:

- [ ] Every product claim sourced from `/brain/truth.md`
- [ ] Messaging aligns with `/brain/positioning-and-messaging.md`
- [ ] Target audience matches an ICP persona
- [ ] No invented features, metrics, or customer names
- [ ] All unverified claims marked `[VERIFY]`
- [ ] Sources cited inline
- [ ] Zero banned words/phrases from `references/banned-words.md`
- [ ] Max 1 rhetorical negation-pivot in the entire piece
- [ ] Max 3 em dashes in the entire piece
- [ ] No AI slop patterns from CLAUDE.md
- [ ] Title tag, meta description, and slug generated
- [ ] Primary keyword in title, H1, first 100 words, and at least one H2
- [ ] 3-5 internal links
- [ ] At least one GEO element (stat with source, expert quote, or self-contained answer block)
- [ ] Social repurposing brief included
- [ ] Images generated or placeholders documented (Step 5.5)
- [ ] Vale lint passes with 0 errors (or SKIPPED if not installed)

---

## Task-Specific Questions

If the brief is unclear, ask these to fill gaps:

1. What's the one thing you want readers to take away from this post?
2. Is there a specific competitor or alternative you want to position against?
3. Do you have data points or customer quotes we can use?
4. Is this tied to a launch, event, or campaign? (Affects timing and CTA)
5. Should this be technical (for engineers) or business-focused (for leadership)?
6. Are there existing company blog posts or pages this should link to?

---

## Related Skills

These are mandatory delegations, not optional references. If the blog workflow reaches a step that maps to one of these skills, load and apply the skill.

| Task | Skill | Mandatory? |
|------|-------|-----------|
| Plan what topics to write about | `content-strategy` | Yes — load before Step 1 if topic selection is needed |
| Edit the draft | `copy-editing` | Yes — load for Step 4b |
| SEO/GEO optimization | `seo-geo` | Yes — load for Step 4c |
| Create social posts from the blog | `social-content` | Yes — load for Step 6 |
| Create visual assets for blog promotion | `brand-design` | Yes — load when visual assets are requested |
