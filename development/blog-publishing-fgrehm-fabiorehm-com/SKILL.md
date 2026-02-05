---
name: blog-publishing
description: |
  Pre-publish validation and checklist for blog posts. Runs automated checks, optional research, and final review before publishing.
  Trigger phrases: "publish", "ship it", "ready to publish", "go live", "pre-publish", "publish post"
allowed-tools: Read, Bash, Grep, WebSearch, WebFetch
---

# Publishing Workflow

## 0. Pre-Publishing Review

**Before running automated checks, confirm content readiness:**

Check the conversation history for evidence of prior reviews:
- Look for "blog-voice-review skill is running" or voice review results
- Look for "blog-proofreading skill is running" or proofreading results
- Check for link testing (curl commands), formatting checks, etc.

**If reviews were already done in this conversation:**
- Note that and proceed directly to automated checks
- Example: "I see you already did voice review and proofreading earlier, let's run the validation checks..."

**If no evidence of reviews, suggest running them:**

```
Before we publish, let's make sure the content is ready:

- Voice review: checks for authentic voice, personal experience, conversational tone
- Proofreading: tests links, checks formatting, reviews flow
- Fact checking: verifies claims against sources (if applicable)

Want to run voice review and proofreading now? Or skip to publishing validation?
```

**If user confirms they're done or wants to skip, proceed to automated checks.**

The typical publishing readiness pattern is: **write → voice → facts (if needed) → proofread → publish**

## 1. Automated Checks

Run validation script:
```bash
python3 .claude/skills/blog-publishing/scripts/validate-post.py <path-to-post>
```

The script checks:
- Scans for leftover `TODO(@` comments
- Validates required frontmatter fields (title, date, description)
- Checks directory structure matches slug
- Verifies date is reasonable for publish
- Confirms post is in `/content/en/drafts/` (warns if already in blog/)

## 2. Find Related Posts for Research & SEO

Optional but recommended. After automated checks pass, search for related content to ensure your post isn't written in a vacuum and discover potential resources to link.

**When to use:**
- After automated checks pass
- Pick 3-5 key topics, concepts, or tools from your post
- Want curated links for a Resources/Related Reading section
- Want to surface any gaps or angles you might expand on

**Process:**

1. **You identify key topics**
   - "Find posts about DevPod, containerization, and local development"
   - "Search for content on automated deployment patterns"
   - Give me 3-5 specific topics to research

2. **I search and evaluate** (WebSearch)
   - Look for recent posts, articles, tools (prefer 2024-2025)
   - Evaluate relevance to your specific angle
   - Note why each result matters relative to your post
   - Filter out generic tutorials that don't add value

3. **I present findings with context**
   - Link + publication date
   - Why it's relevant to *your* post specifically
   - How it complements or differs from your angle
   - Gaps it exposes that you might address

4. **You decide what to include**
   - Pick which links add value
   - Write the narrative context (I'm providing raw relevance, you provide framing)
   - Add to Resources section with your own commentary

5. **Optional: Flag opportunities**
   - "This gap suggests you could expand section X"
   - "No existing content covers your angle on Y"
   - "This contradicts a point in your post - worth addressing?"

**Response format:**

```
**Topic: [X]**

🔗 [Article Title] (Publication, Date)
- Why relevant: [1-2 sentences on how it connects to your post]
- Angle difference: [How it's different or complementary]

🔗 [Another article]
- Why relevant: ...

**Gaps I noticed:**
- [Potential area for expansion or note]
- [Something you might want to address]
```

**What this isn't:**
- Not a comprehensive literature review
- Not writing content for you
- Not telling you what *should* be in Resources
- Not exhaustive research - just enough to inform your decisions

**Integration:**
Runs after automated checks but before the final Publishing Checklist. Gives you research context while you're in final review mode.

## 3. Publishing Checklist

Walk through interactively:

**Content Review**
- [ ] All TODO comments removed?
- [ ] No placeholder content remaining?
- [ ] Spelling and grammar checked?

**Frontmatter & Structure**
- [ ] Date matches intended publish date?
- [ ] Description suitable for SEO/social?
- [ ] Tags are relevant and accurate?
- [ ] Directory structure matches slug?

**Final Quality Check**
- [ ] Conversational and authentic voice?
- [ ] Technical concepts explained accessibly?
- [ ] Honest about limitations?
- [ ] Links tested and working?
- [ ] Credits/attributions where appropriate? (optional - not every post needs this)
- [ ] Closing feels natural? (no required format - some posts just end)

## 4. Final Publishing Steps

If all checks pass:

1. **Update date** - Set `date` field in frontmatter to publish date
2. **Move post** - Move from `/content/en/drafts/slug/` to `/content/en/blog/YYYY/MM/DD/slug/`
   ```bash
   # Example
   mv content/en/drafts/my-post content/en/blog/2025/11/01/my-post
   ```
3. **Clean frontmatter** - Remove `draft: true` (optional - location determines status)
4. **Commit and push** - Post will be live on next build

## Script Location
See `.claude/skills/blog-publishing/scripts/validate-post.py` for implementation.
