---
name: marketing-page-builder
description: Comprehensive workflow for creating new marketing pages on the Kowalah website. Use this skill when a user requests to create a new marketing page, solutions page, product page, or any complete webpage from conception to implementation. The skill guides through three phases with progressive disclosure - page design, content creation, and visual asset generation - with natural checkpoints for user review and approval between phases. This should be used whenever the task involves creating a complete new page rather than just editing existing content.
---

# Marketing Page Builder

## Overview

Create complete marketing pages for the Kowalah website through a guided three-phase workflow with progressive disclosure. Each phase builds on the previous one, with natural checkpoints for user review and approval before proceeding. This skill combines page design, content creation, and visual asset generation into a cohesive, manageable process.

**Use this skill when:**
- User requests to create a new marketing page (solutions, product, company, etc.)
- User wants to build a complete webpage from scratch
- User asks to "design and build" or "create" a new page
- User provides page requirements and wants end-to-end implementation

**Do not use this skill for:**
- Editing existing pages (use direct file editing instead)
- Creating single content blocks without full page context
- Quick content updates or minor revisions
- Documentation-only requests without implementation

## Workflow Structure

The skill operates through three sequential phases with progressive disclosure:

**Phase 1: Page Design** → User approval checkpoint → **Phase 2: Content Creation** → User approval checkpoint → **Phase 3: Visual Assets**

Each phase is self-contained with clear deliverables, allowing users to pause, review, and provide feedback before moving forward.

## Phase 1: Page Design & Architecture

### When to Start

Begin Phase 1 when user provides initial page request. Examples:
- "I want to create a Solutions page for Manufacturing"
- "Help me build a new product page for AI Accelerators"
- "Let's design a page for CFO personas"

### Phase 1 Process

1. **Ask Clarifying Questions**
   - Understand page objective and target audience
   - Identify key messages and value propositions
   - Determine content requirements and user journey
   - Establish SEO focus and competitive positioning
   - Reference: `references/page-design-guide.md` for complete question list

2. **Determine Content Architecture**
   - Apply decision framework: Static Page vs Collection vs Sanity CMS
   - Analyze whether page is unique or part of a content type
   - Consider schema requirements and dynamic routing needs
   - Reference: `references/page-design-guide.md` for decision criteria

3. **Discover Available Components**
   - Read `src/content.config.ts` to examine existing schemas
   - Identify reusable theme components from SyncMaster
   - Map requirements to available collection fields
   - Note any custom component needs

4. **Reference Context Files**
   - `/docs/product-overview.md` - Product details, ICP, personas
   - `/docs/context/positioning-canvas.md` - Brand positioning
   - `/docs/context/messaging-framework.md` - Messaging guidelines
   - `src/content.config.ts` - Existing schemas

5. **Generate Design Document**
   - Create comprehensive design document with 11 sections
   - Include page overview, architecture decision, key messages
   - Specify page structure, content requirements, SEO needs
   - Document user experience flow, CTAs, technical implementation
   - Save as: `tasks/page-design-[page-name].md`

### Phase 1 Deliverable

Complete page design document at `tasks/page-design-[page-name].md` containing:
- Page overview and objectives
- Content architecture decision with rationale
- Key messages aligned with Kowalah framework
- Detailed page structure and component mapping
- Content requirements by section
- SEO, UX, and technical specifications

### Checkpoint: User Approval for Phase 2

**Before proceeding to Phase 2, ask user:**

"I've created the page design document at `tasks/page-design-[page-name].md`. This outlines:
- [Brief summary of page purpose]
- [Architecture approach chosen]
- [Key sections and components]

Would you like to review the design document before I proceed to create the actual content file? I can make adjustments if needed, or we can move forward with content creation."

**Wait for user confirmation before proceeding to Phase 2.**

## Phase 2: Content Creation

### When to Start

Begin Phase 2 only after:
1. Phase 1 design document is complete
2. User has reviewed and approved (or waived review)
3. User confirms readiness to proceed

### Phase 2 Process

1. **Read and Parse Design Document**
   - Extract collection name, page name, and content strategy
   - Identify content architecture (static page vs collection)
   - Note key messages, target audience, and page objectives
   - Extract visual asset specifications and SEO requirements

2. **Architectural Decision and Schema Analysis**
   - For Static Pages: Use flexible frontmatter structure
   - For Collections: Read schema from `src/content.config.ts`
   - Identify required vs optional fields
   - Map design sections to schema field names
   - Reference: `references/content-creation-guide.md` for patterns

3. **Content Generation with Brand Alignment**
   - Reference `/docs/context/messaging-framework.md` for tone
   - Apply executive-level messaging for target audience
   - Focus on benefits over feature descriptions
   - Create action-oriented CTAs
   - Integrate SEO keywords naturally
   - Use semantic icon names from Heroicons (browse heroicons.com)

4. **Quality Validation Before Output**
   - Verify all required schema fields included
   - Check character limits and formatting constraints
   - Ensure no invented statistics or testimonials
   - Validate brand messaging alignment
   - Confirm mobile-friendly structure
   - Reference: `references/content-creation-guide.md` for checklists

5. **Generate Complete Content File**
   - Create clean YAML frontmatter (NO comments)
   - Use semantic icon names from Heroicons
   - Include all content sections from design
   - Use organized image directory paths with leading slashes
   - Deliver implementation-ready markdown file

6. **Create Image Creation Document**
   - Extract all image references from content
   - Categorize by creation method (AI-generated, screenshots, templates)
   - Provide detailed specifications with standardized dimensions
   - Prioritize by importance (hero images first)
   - Create actionable checklist
   - Save as: `tasks/image-creation-[page-name].md`

### Phase 2 Deliverables

1. **Astro Content File** at `src/content/[collection]/[filename].md`
   - Properly formatted markdown with complete YAML frontmatter
   - All schema fields populated and validated
   - Brand-aligned copy with executive tone
   - SEO-optimized meta tags and content structure

2. **Image Creation Document** at `tasks/image-creation-[page-name].md`
   - Prioritized image list (Priority 1, 2, 3)
   - Detailed specifications with standardized dimensions
   - AI generation prompts or Canva mockup instructions
   - Brand guidelines and quality standards
   - Implementation checklist

### Checkpoint: User Approval for Phase 3

**Before proceeding to Phase 3, ask user:**

"I've created two files:

1. **Content File:** `src/content/[collection]/[filename].md`
   - [Brief summary of content sections]
   - [Note any placeholders or data needed]

2. **Image Creation Document:** `tasks/image-creation-[page-name].md`
   - [Number of images needed]
   - [Types: AI-generated, mockups, etc.]

You can test the page with `npm run dev` (images will show as placeholders).

Would you like to review the content before I proceed to Phase 3 where I'll help generate the visual assets? Or would you prefer to handle image creation independently?"

**Wait for user confirmation before proceeding to Phase 3.**

## Phase 3: Visual Asset Generation

### When to Start

Begin Phase 3 only after:
1. Phase 2 content file and image document are complete
2. User has reviewed and approved (or waived review)
3. User confirms they want assistance with visual assets (not handling independently)

### Phase 3 Process

1. **Review Image Creation Document**
   - Open `tasks/image-creation-[page-name].md`
   - Identify Priority 1 images (hero sections, critical visuals)
   - Note standardized dimensions for each image
   - Understand creation methods needed

2. **Generate Platform Mockups (Canva)**
   - For each platform mockup in the image document:
     - Provide detailed Canva creation specifications
     - Suggest realistic interface content and messaging
     - Include platform feature context (Digital CAIO, Projects, etc.)
     - Specify brand integration (Kowalah gradient, colors, typography)
     - Reference: `references/image-creation-guide.md` for template

3. **Generate AI Image Prompts (Conceptual Scenes)**
   - For each conceptual/executive scene:
     - Create comprehensive AI generation prompts
     - Include exact dimensions from standardized set
     - Apply executive visual style guide specifications
     - Ensure brand color integration
     - Reference `/docs/context/executive-visual-style-guide.md`

4. **Provide Implementation Guidance**
   - Organize specifications by priority (1, 2, 3)
   - Include directory structure and file naming
   - Provide quality validation criteria
   - Offer next steps for testing and optimization

### Phase 3 Deliverable

Comprehensive visual asset specifications with:
- Detailed Canva mockup creation instructions
- AI generation prompts with exact dimensions
- Brand guidelines and quality standards
- Implementation checklist organized by priority
- Directory structure and file path guidance

### Final Checkpoint: Implementation Complete

**After Phase 3, provide user with:**

"All three phases are now complete:

✅ **Phase 1:** Page design document (`tasks/page-design-[page-name].md`)
✅ **Phase 2:** Content file (`src/content/[collection]/[filename].md`)
✅ **Phase 3:** Visual asset specifications (`tasks/image-creation-[page-name].md`)

**Next Steps:**
1. Work through image creation document to generate visual assets
2. Test page with `npm run dev` and navigate to the URL
3. Optimize completed images for web performance (WebP format)
4. Commit changes when content and images are complete

**Testing:**
```bash
npm run dev
# Navigate to: [URL]
```

Would you like help with any adjustments, or are you ready to implement the images?"

## Progressive Disclosure Principles

### Only Reveal What's Needed

**Do not front-load all questions.** Ask clarifying questions relevant to the current phase only:
- Phase 1: Ask about page objectives, audience, architecture
- Phase 2: Ask about content specifics, data sources, testimonials
- Phase 3: Ask about image preferences, creation methods, priorities

### Natural Checkpoints

**Always pause for user approval** between phases. Users should have the opportunity to:
- Review deliverables before proceeding
- Make adjustments or provide additional context
- Choose to skip phases (e.g., handle images independently)
- Understand what's coming next

### Avoid Overwhelming Users

**Present information in digestible chunks:**
- Summarize deliverables concisely at checkpoints
- Highlight what was created and where to find it
- Preview what the next phase will do
- Ask clear yes/no questions for approval

### Allow Flexibility

**Users can:**
- Pause at any checkpoint and resume later
- Skip Phase 3 if handling images independently
- Request modifications to any phase before proceeding
- Ask questions or request clarification at any point

## Quality Standards Across All Phases

### Brand Alignment
- Target audience: CEOs at mid-sized enterprises (1,000-10,000 employees)
- Value proposition: Digital CAIO vs. expensive human hire
- Tone: Professional, strategic, authoritative (executive-appropriate)
- Key benefits: Immediate availability, 24/7 access, collective intelligence

### Technical Standards
- All image paths start with forward slash (`/images/...`)
- Use semantic icon names from Heroicons (heroicons.com)
- No YAML comments in frontmatter (breaks Astro parsing)
- Standardized image dimensions: 800×800, 800×200, 800×450, 400×600
- Kebab-case file naming conventions

### Content Quality
- No invented statistics, testimonials, or company information
- Use placeholders like `[X%]`, `[Customer Name]` when data unavailable
- Benefit focus over technical feature descriptions
- Action-oriented CTAs that drive conversion
- Mobile-friendly content structure
- SEO optimization naturally integrated

## Resources

### references/
This skill includes three comprehensive reference guides:

- **`page-design-guide.md`** - Phase 1 reference for design document creation
  - Content architecture decision framework
  - Clarifying questions to ask
  - Design document structure
  - Available Astro collections and components

- **`content-creation-guide.md`** - Phase 2 reference for content file creation
  - Content architecture patterns
  - Quality validation frameworks
  - Icon system integration
  - Image directory organization
  - YAML frontmatter best practices

- **`image-creation-guide.md`** - Phase 3 reference for visual asset generation
  - Image type classification
  - Canva mockup specification templates
  - Digital CAIO chat interface examples
  - Quality standards and success criteria

These references should be consulted during their respective phases for detailed guidance, validation checklists, and technical specifications.

## Common Usage Patterns

### New Solutions Page
```
User: "I want to create a Solutions page for Manufacturing"

Phase 1: Ask about manufacturing challenges, target personas (COO, VP Operations),
         key value propositions, competitive landscape
         → Generate design document

Checkpoint: "Design document ready. Review before content creation?"

Phase 2: Create solutions collection content with manufacturing focus
         → Generate content file and image document

Checkpoint: "Content ready. Test with npm run dev. Generate images?"

Phase 3: Create specifications for manufacturing environment visuals,
         Digital CAIO interface mockups
```

### New Product Feature Page
```
User: "Let's build a page for our AI Accelerators product"

Phase 1: Ask about accelerator types, use cases, target audience,
         differentiation from competitors
         → Generate design document

Checkpoint: "Design document ready. Proceed with content?"

Phase 2: Create product collection content with accelerator capabilities
         → Generate content file and image document

Checkpoint: "Content ready. Want help with visual assets?"

Phase 3: Create specifications for accelerator showcase mockups,
         implementation process diagrams
```

### New Persona/Role Page
```
User: "Create a page targeting CFOs"

Phase 1: Ask about CFO pain points, financial concerns, ROI focus,
         governance requirements
         → Generate design document

Checkpoint: "Design document ready. Review or proceed?"

Phase 2: Create content emphasizing financial benefits, risk mitigation
         → Generate content file and image document

Checkpoint: "Content ready. Generate image specifications?"

Phase 3: Create specifications for executive strategy sessions,
         financial dashboard mockups, ROI visualization
```

## Troubleshooting

### User Wants to Skip a Phase
- **Phase 1 Skip:** Ask for existing design document or requirements doc
- **Phase 2 Skip:** Confirm they have content file already created
- **Phase 3 Skip:** Confirm they'll handle images independently, provide document anyway

### User Wants to Modify Previous Phase
- Return to the requested phase
- Make modifications to the deliverable
- Re-present the checkpoint before proceeding forward

### User Unsure About Proceeding
- Offer to explain what the next phase will do
- Suggest reviewing current deliverables first
- Provide estimated time/complexity of next phase
- Offer alternative approaches if needed

### Schema or Collection Doesn't Exist
- Phase 1: Note that new collection schema will be needed
- Phase 2: Create content with proposed schema structure
- Flag for user that `src/content.config.ts` needs updating before testing

## Success Criteria

A successful page creation workflow should result in:

✅ **Complete Design Documentation** - Comprehensive design document with architecture decision
✅ **Implementation-Ready Content** - Properly formatted content file that passes schema validation
✅ **Visual Asset Roadmap** - Detailed specifications for all required images
✅ **Brand Alignment** - All content aligns with Kowalah positioning and messaging
✅ **Technical Correctness** - Proper paths, naming conventions, schema compliance
✅ **User Confidence** - User understands what was created and how to implement
✅ **Progressive Disclosure** - User never felt overwhelmed, always knew next steps
