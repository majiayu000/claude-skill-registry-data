---
name: Guide Development
description: Auto-scaffold Designer Guides learning paths by analyzing existing guides (Claude Code, Cursor) and generating new guides for other tools
---

# Guide Development Skill

This skill helps you generate **Designer Guide learning paths** for different AI tools and design platforms. The guide generator analyzes your existing complete guides (Claude Code ✅, Cursor ✅) and creates new guides for other tools following the same proven structure and patterns.

## What This Skill Does

The guide generator **automatically creates**:
- ✅ Complete guide metadata (title, description, tags)
- ✅ Module structure (Setup, Features, Workflows, Advanced)
- ✅ Sequential lessons with estimated durations
- ✅ Rich lesson sections (intro, steps, code, images, callouts)
- ✅ Placeholder content ready for tool-specific details
- ✅ TypeScript guide objects that integrate with the existing guides system

## Current Guide Status

### ✅ Fully Developed Guides (2/6)
1. **Claude Code Learning Path** - 18 lessons across 4 modules
   - Complete setup, features, workflows, and best practices
   - Ready for use: http://localhost:3000/guides/claude-code-learning-path

2. **Cursor Learning Path** - 12 lessons across 4 modules
   - Complete setup, key features, design-to-code workflows
   - Ready for use: http://localhost:3000/guides/cursor-learning-path

### 📋 Placeholder Guides (4/6) - Ready for Generation
1. **GitHub Copilot Guide** - Structure only, needs content
2. **Replit Guide** - Structure only, needs content
3. **V0 Guide** - Structure only, needs content
4. **GitHub Guide** - Structure only, needs content

## Intent Detection - When Claude Should Suggest This Skill

Claude should **automatically proactively suggest using the guide generator** when detecting these keywords:
- "create a guide" or "generate guide" → Suggest: `npm run generate-guide`
- "guide for [tool-name]" → Suggest generator for that specific tool
- "designer guide" or "learning path" → Suggest: `npm run generate-guide`
- "update guide" or "add lesson" → Suggest: `npm run generate-lesson`
- When user mentions working on tool documentation → Offer guide generation
- "how do I create a guide?" or "what guides exist?" → Show available guides

## Auto-Suggestion Logic

**When user mentions guide work, Claude should:**

1. **Check status**: `npm run list-guides` (in background)
2. **Identify complete vs. placeholder guides**: 2 complete, 4 need content
3. **Suggest appropriate action**:
   - For PLACEHOLDER guides: "Ready to generate? Run: `npm run generate-guide`"
   - For NEW tool: "Let me create a guide for [tool]. Run: `npm run generate-guide`"
   - For EXISTING guide: "Guide already exists. Enhance it by editing guides.ts directly"
4. **Explain what it generates**: "This creates all 4 modules with lesson structure automatically"
5. **Next steps**: Guide for content enhancement and image/GIF addition

## Using the AI Guide Generator

**The guide generator creates guide structure following existing guide patterns!**

```bash
# Generate a new guide interactively
npm run generate-guide

# List all guides and completion status
npm run list-guides

# Validate guide structure
npm run validate-guides
```

**What the generator does automatically:**
- ✅ Creates guide metadata (title, description, slug, tags)
- ✅ Generates 4 module structure (Setup, Features, Workflows, Advanced)
- ✅ Creates sequential lessons with descriptions
- ✅ Adds lesson sections (intro, steps, images, code, callouts)
- ✅ Generates placeholder content ready for enhancement
- ✅ Adds guide object to guides.ts with proper TypeScript syntax
- ✅ Validates against your guide schema

**After generation, you will need to:**
- Add images/GIFs to `public/images/guides/[slug]/`
- Enhance lesson content with tool-specific details
- Add tool-specific code examples
- Review and test at `http://localhost:3000/guides/[slug]`
- Update placeholder section content with real information

## Guide Structure Reference

### Guide Data Model

Each guide at `guides.ts` contains:

```typescript
{
  id: string              // Unique identifier
  slug: string            // URL slug (e.g., "cursor-learning-path")
  title: string           // Display title
  description: string     // Full description
  excerpt: string         // Short summary
  tool: string            // Tool name (e.g., "Cursor", "GitHub Copilot")
  useCase: string         // Always "Learning Path"
  skillLevel: string      // Beginner, Intermediate, or Advanced
  designDomain: string    // Always "UX Design"
  readTime: number        // Estimated minutes
  author: string          // Author name
  publishedDate: string   // ISO date string
  thumbnail: string       // Image URL
  tags: string[]          // Searchable tags
  lessons: Lesson[]       // Array of lessons
}
```

### Lesson Structure

```typescript
{
  id: string              // Unique identifier (e.g., "lesson-1")
  title: string           // Lesson title
  duration: number        // Minutes to complete
  order: number           // Sequential order
  module: string          // Module name (setup, features, workflows, advanced)
  sections: Section[]     // Lesson content sections
}
```

### Section Types

**1. Intro Section** - Brief introduction
```typescript
{ type: 'intro', content: string, icon: string }
```

**2. Text Section** - Paragraph content
```typescript
{ type: 'text', content: string }
```

**3. Steps Section** - Numbered steps with instructions
```typescript
{
  type: 'steps',
  steps: [
    { number: 1, title: string, content: string[], icon: string },
    { number: 2, title: string, content: string[], icon: string }
  ]
}
```

**4. Image Section** - Images and screenshots
```typescript
{ type: 'image', alt: string, label: string }
```

**5. Code Section** - Code examples
```typescript
{ type: 'code', language: string, title: string, code: string }
```

**6. Callout Section** - Tips, warnings, or information
```typescript
{
  type: 'callout',
  calloutType: 'tip' | 'warning' | 'info',
  title: string,
  content: string,
  icon: string
}
```

## Template Patterns from Existing Guides

### Module Structure (Proven Pattern)
1. **Setup** (3 lessons) - Installation, configuration, first project
2. **Features** (3 lessons) - Core features, AI capabilities, customization
3. **Workflows** (3 lessons) - Practical workflows, collaboration, integration
4. **Advanced** (3 lessons) - Advanced techniques, best practices, troubleshooting

### Lesson Duration Pattern
- Each lesson: **2-3 minutes** to complete
- Setup module lessons: 2 minutes (simpler)
- Advanced module lessons: 3 minutes (more complex)

### Section Pattern (Proven Sequence)
1. **Intro** - What you'll learn and why it matters
2. **Text** - Background information and concepts
3. **Steps** - Numbered instructions to follow
4. **Image** - Visual demonstration (screenshot/GIF placeholder)
5. **Callout** - Pro tip or important note
6. **Code** (optional) - Code example if applicable

## Guide Development Workflow

### Step 1: Generate Guide Structure
```bash
npm run generate-guide
# Follow interactive prompts:
# - Tool name (e.g., "GitHub Copilot")
# - URL slug (e.g., "github-copilot-learning-path")
# - Skill level (Beginner/Intermediate/Advanced)
# - Number of lessons (default: 12)
# - Number of modules (default: 4)
```

### Step 2: Review Generated Guide
- Open `src/data/guides.ts`
- Verify guide metadata and lesson structure
- Check module organization

### Step 3: Add Images & GIFs
- Create folder: `public/images/guides/[slug]/`
- Add images/GIFs for each lesson that needs visuals
- Images should be 800-1200px wide
- Optimize using: `npm run optimize-images`

### Step 4: Enhance Content
- Edit lesson titles for tool-specific details
- Update section content with real information
- Replace placeholder "callout tips" with tool-specific advice
- Add actual code examples where needed
- Customize step titles and instructions

### Step 5: Test & Review
```bash
npm run dev                    # Start dev server
# Navigate to: http://localhost:3000/guides/[slug]
# Review all lessons and sections
# Check mobile responsiveness
# Test all interactive elements
```

### Step 6: Validation
- Guides are automatically validated when served
- Check console for any guide structure errors
- All lessons should render without warnings

## Commands Reference

```bash
# Generate a new guide (interactive mode)
npm run generate-guide

# Add a lesson to an existing guide
npm run generate-lesson

# List all guides and their status
npm run list-guides

# Validate guide structure
npm run validate-guides

# Start development server to preview guides
npm run dev

# Optimize guide images
npm run optimize-images
```

## Important Rules

⚠️ **One Tool at a Time**: Complete one guide fully before starting another.

✅ **Complete Structure First**: Let the generator create the full structure, then enhance content step by step.

🎯 **Quality Content**: Focus on making guide content clear and practical for designers.

📱 **Test Thoroughly**: Always preview in browser and test on mobile.

🖼️ **Always Add Images**: Every lesson should have at least one image/GIF placeholder.

## Success Criteria

A guide is complete when:

✅ Guide metadata (title, description, tags) is accurate
✅ All lessons render correctly
✅ Module structure is logical (Setup → Features → Workflows → Advanced)
✅ Each lesson has 4+ sections (intro, text, steps, image, callout)
✅ All image placeholders have descriptive alt text
✅ Images/GIFs are optimized and added
✅ Code examples (if applicable) are valid
✅ Guide displays correctly at http://localhost:3000/guides/[slug]
✅ Mobile responsive design verified
✅ All sections match guide schema

## Next Steps After Guide Completion

1. Commit changes with guide name in message
2. Update progress in `npm run progress-report`
3. Move to next placeholder guide
4. Track progress toward 6/6 complete guides

## Agent Coordination & Workflow

This skill works with other AI agents:

### Related Skills & Agents
- **pattern-dev** - Develops patterns (guides complement patterns)
- **test-gen** - Generates component tests if guides have interactive demos
- **design** - Analyzes design consistency in guide UI

### Coordinated Workflow
```bash
# Complete AIUX workflow
npm run generate-pattern              # Generate pattern
npm run generate-guide                # Generate guide lesson about pattern
npm run design-analyze                # Analyze design consistency
npm run progress-report               # Track overall progress
```

---

**Project Goal**: Complete 6 Designer Guide learning paths covering all major AI tools and design platforms. Currently: 2/6 complete (Claude Code, Cursor), 4/6 placeholders ready for generation.

**Related Project**: 24 AI design patterns (15/24 complete, 9 in progress)
