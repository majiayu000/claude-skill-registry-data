---
name: writing
description: Create distinctive, production-grade blog posts. Use this skill when the user asks to build a new blog poast
---

I need you to create a custom SEO content writer skill using the skill-creator skill. This skill should write blog posts in my specific brand voice with a structured, approval-driven workflow.

### SKILL SPECIFICATIONS

**Skill Name:** [YOUR_SKILL_NAME]
Example: "acme-seo-writer" or "jane-content-creator"

**Brand/Writer Name:** [YOUR_NAME_OR_BRAND]
Example: "Jane Smith" or "Acme Marketing"

**Primary Website URL:** [YOUR_WEBSITE_URL]
Example: "https://www.acmemarketing.com"

**Default Word Count:** [DEFAULT_WORD_COUNT]
Example: 1500 or 2000

**Target Audience Description:** [WHO_WRITES_FOR]
Example: "B2B SaaS companies" or "small business owners in healthcare" or "e-commerce store owners"

**Primary Content Topics:** [MAIN_TOPICS]
Example: "digital marketing, social media strategy, content marketing" or "financial planning, investment strategies, retirement planning"

**SEO Vocabulary/Keywords to Emphasize:** [KEY_TERMS]
Example: "conversion optimization, funnel strategy, lead generation" or "fiduciary duty, asset allocation, portfolio diversification"

---

### WORKFLOW REQUIREMENTS

The skill MUST follow this multi-step approval workflow:

**Step 1: Gather Requirements**
- Collect primary keyword, topic/angle, target audience, word count
- Ask for negative keywords (words to avoid)
- Collect any optional information (specific CTAs, related topics, personal experiences)

**Step 2: Research & Analysis Phase**
The skill should conduct:
- 3-7 web searches for topic research, search intent, statistics, trends, expert perspectives
- Load and analyze the sitemap CSV to identify 3-5 relevant internal links
- Review the experiences/wins document to suggest 1-2 relevant stories (only if genuinely relevant)
- Compile all sources with specific placement recommendations

**Step 3: Present Outline & Recommendations [APPROVAL REQUIRED]**
Present to user:
- Search intent analysis
- Complete blog outline (H2s and H3s)
- Source integration plan (5-10 sources with URLs and placement)
- Internal linking plan (3-5 links with reasoning)
- Experience/win suggestions (or state if none are relevant)
- Explicitly ask for approval before proceeding

**Step 4: Write Full Blog Post**
Only after approval, write the complete blog post following:
- The approved outline structure
- Integration of all approved sources as contextual hyperlinks
- Natural placement of internal links
- Incorporation of approved experiences/wins
- Adherence to tone of voice guidelines

---

### REQUIRED FILES I'M PROVIDING

**1. Tone of Voice Document:** [ATTACHED]
- This document defines my writing style, voice, and language guidelines
- Save this as: `references/tone-of-voice.txt` or `.md`

**2. Website Sitemap CSV:** [ATTACHED]
- Contains columns: Link, Title, MetaDescription (or similar)
- This will be used for internal linking research
- Save this as: `references/sitemap.csv`

**3. Experiences/Wins Document:** [ATTACHED]
- Contains [CLIENT_WINS / CASE_STUDIES / PERSONAL_EXPERIENCES / SUCCESS_STORIES]
- Real examples and stories to weave into content as social proof
- Save this as: `references/[YOUR_EXPERIENCES_FILENAME].md`
Example filename: "client-wins.md" or "case-studies.md" or "success-stories.md"

---

### WRITING STYLE REQUIREMENTS

Based on my tone of voice document, the skill should write content that is:

**Tone Characteristics:** [DESCRIBE_YOUR_TONE]
Examples:
- "Confident and authoritative, but approachable and conversational"
- "Friendly and educational with a touch of humor"
- "Professional and data-driven, yet accessible to beginners"
- "Bold and opinionated, challenging industry norms"

**Language Preferences:**
✅ DO USE: [PHRASES_TO_USE]
Example: "second-person 'you', contractions, short punchy sentences, analogies"

🚫 AVOID: [PHRASES_TO_AVOID]
Example: "overly technical jargon, clickbait, formal corporate speak, empty buzzwords"

---

### SEO INTEGRATION REQUIREMENTS

**Primary Keyword Placement:**
- Title, first paragraph, 2-3 H2 headings
- Target keyword density: [1-2%] (or specify your preference)

**FAQ-Style Headings:**
- Throughout the blog, convert some H2s or H3s into question format (FAQs people would likely ask about the topic)
- Answer these questions concisely and completely in the section immediately below
- Make each FAQ section self-contained - it should make sense even if extracted from the blog post
- Use this approach frequently but not for the entire blog (aim for 2-4 FAQ-style sections per post)
- Example: Instead of "Local SEO Best Practices" use "What Are the Most Effective Local SEO Strategies?"
- The answer should be direct, actionable, and 2-4 paragraphs maximum

**Source Integration:**
- All research sources must be embedded as contextual hyperlinks (not listed at the end)
- Use descriptive anchor text, never "click here" or naked URLs
- Paraphrase insights, never quote exact text

**Internal Linking:**
- Integrate 3-5 internal links from the sitemap CSV
- Links should flow naturally within the content
- Use descriptive anchor text that matches the destination page topic

**Experiences/Wins Integration:**
- Only suggest experiences that are directly relevant to the blog topic
- Format: "[Person/Client] saw [specific result] by implementing [strategy]..."
- Include specific metrics for credibility
- Integrate naturally within relevant sections (not as separate case study blocks)

---

### CONTENT STRUCTURE REQUIREMENTS

**Standard Blog Structure:**

**Introduction (150-200 words):**
- Hook with relatable pain point or industry shift
- Set up the problem/opportunity
- Promise the solution/framework

**Body (1200-1400 words):**
- 4-6 main H2 sections
- Each H2 followed by 2-4 H3 subheadings
- Direct, concise paragraphs (2-4 sentences max)
- Natural keyword integration throughout

**Conclusion (100-150 words):**
- Summarize 2-3 main takeaways
- Motivational call-to-action
- Invitation for engagement

---

### QUALITY STANDARDS

Before delivering the final blog, the skill must verify:

- [ ] User approved the outline before writing
- [ ] Primary keyword appears naturally (not stuffed)
- [ ] All approved sources embedded as hyperlinks
- [ ] All 3-5 planned internal links integrated
- [ ] Approved experiences/wins included (if any)
- [ ] No negative keywords used
- [ ] Tone matches brand voice guidelines
- [ ] Every heading followed by valuable content
- [ ] Proper structure maintained
- [ ] Word count meets requirement
- [ ] No copyright violations (all content paraphrased)

---

### ADDITIONAL CUSTOMIZATION (Optional)

**Special Instructions:** [ANY_SPECIAL_REQUIREMENTS]
Examples:
- "Always include a 'Quick Takeaways' section at the top"
- "End each post with a specific CTA to join our newsletter"
- "Include a data table in every post if statistics are available"
- "Always mention our [PRODUCT/SERVICE] naturally in the conclusion"

**Negative Keywords to Always Avoid:** [COMPETITORS_OR_BANNED_TERMS]
Example: "Competitor names: XYZ Corp, ABC Company" or "Avoid: 'guaranteed results', 'overnight success', 'secret hack'"

---

## INSTRUCTIONS FOR CLAUDE

Using the skill-creator skill:

1. **Initialize the skill structure** using the provided skill name
2. **Create the SKILL.md file** following the exact workflow structure outlined above
3. **Create the references folder** and add:
   - The tone of voice document I provided
   - The sitemap CSV I provided
   - The experiences/wins document I provided
4. **Write comprehensive instructions** in SKILL.md that:
   - Explain the 4-step workflow clearly
   - Reference when to load each reference file
   - Include examples of how to present the outline and recommendations
   - Provide quality checklists and best practices
5. **Package the completed skill** into a .zip file for distribution

Create a skill that transforms you into an expert SEO content writer that writes in my specific voice, follows my workflow, and uses my resources effectively.

HOW TO USE THIS TEMPLATE
Step 1: Fill in All Variables
Replace every [BRACKETED_ITEM] with your specific information.
Step 2: Gather Your Files
Prepare these three files:
Tone of Voice Document - Your writing style guide (txt or md format)
Sitemap CSV - Your website's pages (must include: Link, Title, Description columns)
Experiences Document - Your client wins, case studies, or success stories (md format)
Step 3: Send to Claude
In a conversation with Claude:
Paste your filled-out prompt
Upload all three files
Claude will use the skill-creator to build your custom SEO writer skill
Step 4: Receive Your Skill
Claude will deliver a packaged .zip file containing your personalized SEO content writer skill, ready to use!

EXAMPLE FILLED-OUT PROMPT
Here's what a completed prompt might look like:
I need you to create a custom SEO content writer skill using the skill-creator skill.

### SKILL SPECIFICATIONS

**Skill Name:** acme-seo-writer
**Brand/Writer Name:** Acme Marketing
**Primary Website URL:** https://www.acmemarketing.com
**Default Word Count:** 2000
**Target Audience Description:** B2B SaaS companies looking to improve their content marketing and SEO
**Primary Content Topics:** content marketing, SEO strategy, conversion optimization, marketing automation
**SEO Vocabulary/Keywords to Emphasize:** funnel strategy, lead generation, marketing qualified leads, conversion rate optimization, content clusters

[... rest of filled-out sections ...]

**Tone Characteristics:** Confident and data-driven, but approachable. We use real examples and case studies to back up every claim. We're opinionated about best practices but never condescending.

**Language Preferences:**
✅ DO USE: "you", contractions, rhetorical questions, data points with sources, real customer examples
🚫 AVOID: "synergy", "next-generation", "revolutionary", "game-changer", competitor names

**Negative Keywords to Always Avoid:** "HubSpot, Marketo, guaranteed ROI, overnight success"

