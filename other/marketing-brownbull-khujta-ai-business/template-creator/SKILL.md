---
name: template-creator
description: Create new ChatGPT Enterprise templates for the Kowalah marketing website following the established content collection schema. Use when the user requests to create a new template resource (policy, evaluation guide, deployment checklist, job description, or program framework) for the /resources/templates section.
---

# Template Creator

## Overview

Create comprehensive, SEO-optimized templates for the Kowalah marketing website templates collection. This skill guides the creation of templates that follow the established schema, include proper frontmatter, and optimize for Answer Engine Optimization (AEO) through structured FAQs.

## When to Use This Skill

Use this skill when the user requests to create:
- AI policy templates
- ChatGPT Enterprise evaluation guides
- Deployment checklists and implementation guides
- Chief AI Officer or AI-related job descriptions
- AI program frameworks or templates
- Any other downloadable template resource for the `/resources/templates` section

## Template Creation Workflow

### Step 1: Gather Template Requirements

Before creating the template, understand the following from the user:

1. **Template Purpose**: What problem does this template solve?
2. **Target Audience**: Who will use this template (CIOs, CHROs, CTOs, etc.)?
3. **Template Type**: Which category does it fall into?
   - `policy` - Governance documents and policies
   - `evaluation` - Comparison/evaluation guides
   - `deployment` - Implementation and deployment guides
   - `job-description` - Role descriptions
   - `program-template` - Program frameworks
4. **Content Structure**: What sections should the template include?
5. **Key Differentiators**: What makes this template valuable?

### Step 2: Review the Schema

Load the schema reference to understand the complete template structure:

```bash
Read: .claude/skills/template-creator/references/template-schema.md
```

This reference contains:
- Complete TypeScript schema definition
- Field descriptions and requirements
- Template type icon mappings
- File naming conventions
- Content structure guidelines

### Step 3: Start with the Template Example

Copy the template example as a starting point:

```bash
Read: .claude/skills/template-creator/assets/template-example.md
```

This asset file provides:
- Complete frontmatter structure with all required fields
- Placeholder values showing the expected format
- Example content structure
- Implementation notes section

### Step 4: Create the Template Frontmatter

Fill in the YAML frontmatter with specific values:

#### Required Fields
- `title`: Clear, descriptive template name
- `description`: SEO-optimized description (150-160 characters)
- `template_type`: Choose from: policy, evaluation, deployment, job-description, program-template
- `category`: Template category (e.g., "Governance & Risk", "Implementation & Deployment")

#### Hero Section
- `hero.title`: Template title (can match main title or be variant)
- `hero.subtitle`: Compelling value proposition
- `hero.image`: Path to hero image (format: `/images/resources/templates/[slug]-hero.png`)
- `hero.badge`: Optional badge (Most Popular, New, Updated, Essential)

#### Overview Section
- `overview.who_its_for`: Specific target audience and roles
- `overview.when_to_use`: Timing and situations for use
- `overview.key_benefit`: Primary value proposition
- `overview.sections_included`: Array of section names (5-10 items)

#### How to Use Steps
Keep the standard 4-step process:
1. Copy the template
2. Customize for organization
3. Review with stakeholders
4. Deploy and iterate

Adjust descriptions to match the specific template type.

#### FAQ Section
Create 5-10 questions optimized for Answer Engine Optimization:
- Answer common objections
- Explain key decisions and approaches
- Provide implementation context
- Address "how is this different from X" questions
- Include timing/frequency questions

#### External Resources (Optional)
Use this field when linking to comprehensive external resources:
- `external_resources.google_doc.url`: Link to Google Doc with full content
- `external_resources.google_doc.label`: Button text (default: "Open in Google Docs")

**When to use external_resources:**
- Multi-tab Google Docs or Sheets that are easier to maintain externally
- Comprehensive guides that receive frequent updates
- Resources where collaborative editing is beneficial (easier in Google Docs)
- Templates where the "source of truth" should remain in an external system

**When NOT to use:**
- Simple templates that can be fully reproduced in Markdown
- Static content that doesn't need frequent updates
- Templates where you want full version control in the repo

**Template approach with external resources:**
- The template page acts as an overview/landing page
- Describe what's included in the external resource
- Provide context through FAQs and implementation notes
- Link to the comprehensive external resource for full details

#### CTA Section
- `cta.title`: Call-to-action heading
- `cta.content`: How Kowalah can help beyond the template
- `cta.button_label`: Usually "Talk to an Expert"
- `cta.button_link`: Usually "/contact"

#### Optional Fields
- `meta_title`: If different from title
- `related_templates`: Array of related template slugs
- `draft`: Set to `true` to hide from production
- `featured`: Set to `true` for homepage featuring

### Step 5: Write the Template Content

After the frontmatter, create the markdown content:

#### Start with Usage Note
Always begin with:
```markdown
***NOTE**: To use this template, copy the content using the "Copy page" button above, then customize for your organization.*
```

#### Content Structure
Organize content using clear markdown hierarchy:
- `# Heading 1` for main title
- `## Heading 2` for major sections
- `### Heading 3` for subsections
- Use lists, tables, and emphasis appropriately

#### Implementation Notes
End with an Implementation Notes section providing:
- Customization guidance
- Contextual factors to consider
- Industry-specific adaptation tips

### Step 6: Save the Template File

Save the template to the correct location:

**Location**: `src/content/templates/[template-slug].md`

**Naming Convention**: Use kebab-case
- ✅ `ai-policy-template.md`
- ✅ `chatgpt-evaluation-guide.md`
- ✅ `caio-job-description.md`
- ❌ `AI_Policy_Template.md`
- ❌ `ChatGPT Evaluation Guide.md`

The filename (without `.md`) becomes the URL slug: `/resources/templates/[filename]`

### Step 7: Generate Hero Image Midjourney Prompt

After saving the template, generate a Midjourney prompt for the hero image:

**Image Requirements:**
- **Dimensions**: 800×450px (16:9 landscape) for hero sections
- **Format**: Professional, conceptual business/technology scene
- **Brand Integration**: Kowalah colors (#fa26a0, #ae10e3) as subtle accents
- **Style**: Clean, modern, executive-appropriate

**Glassmorphism Optimization** (IMPORTANT):
The template detail pages use a glassmorphism card overlay on the left side of the hero image. Optimize images for this design:

✅ **Ideal Composition:**
- **Subject positioning**: Place people/focal points on the **right third** of the frame
- **Left side atmospheric**: Keep left two-thirds as soft, blurred environment for card overlay
- **Environmental emphasis**: Prioritize setting and atmosphere over close-up subjects
- **Wide environmental shots**: Office scenes, boardrooms, strategic settings with depth
- **Soft bokeh backgrounds**: Create visual texture without competing focal points

❌ **Avoid:**
- Close-up portraits with faces centered
- Important details in the center or left third (will be covered by card)
- Images where the main subject is the primary focal point
- Busy or detailed left-side content that distracts from card readability

**Purpose**: Hero images provide color, atmosphere, and brand consistency - the glassmorphism card is the visual hero, not the background image.

**Visual Theme by Template Type:**

- **`policy`** - Executive governance scenes: boardroom discussions, compliance frameworks, leadership strategy sessions
- **`evaluation`** - Analysis and decision-making: comparison matrices, strategic evaluation, vendor assessment contexts
- **`deployment`** - Implementation and transformation: rollout planning, team enablement, change management scenes
- **`job-description`** - Leadership and talent: executive interview contexts, strategic hiring, organizational capability building
- **`program-template`** - Framework and structure: program planning, organizational design, strategic frameworks

**Prompt Generation Template:**

```
[Subject/scene description based on template type], [composition details], shot on Fujifilm X-T4 35mm f/1.4, shallow depth of field bokeh, [lighting], natural skin tones, slight film grain, [attire/context], [expressions/mood], [subtle brand color integration], 800×450px landscape, [compositional notes], documentary style, authentic moment, no text, pure photography
```

**Reference Files:**
- Read `/docs/context/visual-style-guide.md` for complete Midjourney prompt guidelines
- Use "Preventing Text Overlays in Midjourney" section to avoid unwanted text generation
- Follow "Template Addition for Text Prevention" format

**Example Midjourney Prompts:**

**AI Policy Template** (policy type):
```
Executive leadership team in modern boardroom reviewing AI governance framework, medium shot with subjects on right third, shot on Fujifilm X-T4 35mm f/1.4, shallow depth of field, warm natural window lighting, natural skin tones, slight film grain, professional business attire, confident collaborative expressions, digital screens with subtle purple glow showing policy frameworks, left side soft bokeh for text overlay, 800×450px landscape composition, atmospheric depth, documentary style, authentic strategy session, no text, pure photography
```

**Chief AI Officer Job Description** (job-description type):
```
Modern executive office environment with senior leader visible on right edge of frame, wide environmental shot, shot on Fujifilm X-T4 35mm f/1.4, shallow depth of field, warm natural window lighting from left, natural skin tones, slight film grain, executive in sharp business attire partially visible on right third, confident posture, left two-thirds showcases atmospheric office interior with organizational charts and strategic planning boards softly blurred, subtle pink and purple accent lighting (#fa26a0, #ae10e3) on office walls and technology, 800×450px landscape composition, depth and bokeh throughout left side, professional strategic workspace aesthetic, documentary style, environmental atmosphere emphasized over subject, no text, pure photography
```

**ChatGPT Evaluation Guide** (evaluation type):
```
Business team analyzing AI platform comparison, wide shot with subjects on left, shot on Fujifilm X-T4 35mm f/1.4, shallow depth of field bokeh, natural office lighting, natural skin tones, slight film grain, professional casual attire, focused analytical expressions, laptops and tablets showing evaluation matrices with purple screen glow, right side soft focus for overlay space, 800×450px landscape composition, strategic decision context, documentary style, no text, pure photography
```

**Output Format:**

After generating the prompt, present it to the user:

```
## Hero Image Midjourney Prompt Generated

**Image Path**: `/images/resources/templates/[template-slug]-hero.png`
**Dimensions**: 800×450px (16:9 landscape)
**Template Type**: [type] → [visual theme]

**Midjourney Prompt**:
```
[Complete generated prompt]
```

**Next Steps**:
1. Copy the prompt above into Midjourney
2. Generate the image and select the best variation
3. Download and optimize the image
4. Save to `/public/images/resources/templates/[template-slug]-hero.png`
5. Verify the image path in the template frontmatter matches
```

### Step 8: Verify the Template

After creating the template, verify:

1. **Schema Compliance**: All required frontmatter fields present
2. **Template Type**: Correct `template_type` value (determines icon)
3. **FAQ Quality**: 5-10 substantive questions with detailed answers
4. **Content Structure**: Proper markdown hierarchy and formatting
5. **File Location**: Saved in `src/content/templates/`
6. **File Naming**: Uses kebab-case naming
7. **Hero Image Prompt**: Midjourney prompt generated and ready for image creation

### Step 9: Test the Template

Navigate to the template in the development server to verify:

```
http://localhost:4321/resources/templates/[template-slug]
```

Check:
- Hero section displays with glassmorphism background image effect
- Hero image loads from `/images/templates/[template-slug]-hero.png`
- Overview section shows correct icon (based on template_type)
- "Sections Included" list displays with green checkmarks
- Copy page dropdown works with all export options
- FAQ section renders properly
- Related templates link correctly (if specified)

## Template Type Icon Reference

The `template_type` field determines the icon displayed in the overview section:

- `"policy"` → 📄 DocumentTextIcon (governance documents)
- `"evaluation"` → 📊 TableCellsIcon (comparison guides)
- `"deployment"` → 🚀 RocketLaunchIcon (implementation guides)
- `"job-description"` → 💼 BriefcaseIcon (role descriptions)
- `"program-template"` → 📁 FolderIcon (program frameworks)

## Answer Engine Optimization (AEO) Best Practices

Templates should be optimized for LLMs to parse and cite:

### FAQ Quality
- Write 5-10 substantive questions
- Provide detailed, informative answers (2-4 sentences minimum)
- Address common objections and concerns
- Explain key decisions and trade-offs
- Include timing, frequency, and process questions

### Content Structure
- Use clear heading hierarchy
- Include tables for comparisons
- Use lists for step-by-step instructions
- Add bold emphasis for key concepts
- Keep paragraphs focused and scannable

### SEO Elements
- `meta_title`: Includes target keywords and "| Kowalah"
- `description`: 150-160 characters with primary keywords
- `hero.title`: Clear, keyword-rich title
- `overview` fields: Include target audience and use case keywords

### Automatic JSON-LD Structured Data

**Every template automatically generates three types of structured data for maximum LLM discoverability:**

1. **TechArticle Schema**
   - Categorizes the template as technical content
   - Includes author, publisher, category, and audience information
   - Generated from: `title`, `description`, `category`, `overview.who_its_for`

2. **HowTo Schema**
   - Provides step-by-step implementation guidance
   - Maps all "How to Use" steps with position and descriptions
   - Includes external tools (Google Docs link if available)
   - Generated from: `how_to_use.steps`, `external_resources.google_doc`

3. **FAQPage Schema**
   - Provides Q&A pairs for answer engines
   - Generated from: `faq.questions` array

**What this means:**
- LLMs can understand template type, audience, and use cases
- Answer engines can cite specific steps or FAQs
- Google and other search engines get rich structured context
- Templates appear in AI-powered search results with enhanced snippets

**No additional work required** - just ensure your frontmatter follows the schema and the structured data generates automatically from the template detail page.

## Common Template Categories

Use these categories for consistency:

- **Governance & Risk**: Policies, compliance frameworks, risk assessments
- **Implementation & Deployment**: Rollout guides, deployment checklists
- **Talent & Hiring**: Job descriptions, interview guides, onboarding plans
- **Strategy & Planning**: Strategic frameworks, planning templates
- **Change Management**: Adoption plans, communication templates

## Resources

### references/template-schema.md
Complete schema definition with:
- TypeScript interface
- All field descriptions
- Template type mappings
- File naming conventions
- Content structure guidelines

### assets/template-example.md
Template boilerplate with:
- Complete frontmatter structure
- All required and optional fields
- Example content sections
- Implementation notes template

---

## Example Usage

**User Request:** "Create a ChatGPT Enterprise Evaluation Guide template"

**Workflow:**
1. Gather requirements about what the evaluation guide should cover
2. Read `references/template-schema.md` to understand schema
3. Read `assets/template-example.md` for structure
4. Create frontmatter with:
   - `template_type: "evaluation"` (→ TableCellsIcon)
   - `category: "Implementation & Deployment"`
   - Comprehensive FAQ about evaluation criteria
5. Write content covering evaluation framework, comparison matrices, decision criteria
6. Save as `src/content/templates/chatgpt-evaluation-guide.md`
7. Verify template displays correctly with table icon in overview
