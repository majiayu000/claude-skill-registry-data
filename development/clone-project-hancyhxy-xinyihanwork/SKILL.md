---
name: clone-project
description: This skill should be used when users want to create a new gallery project for the personal portfolio website. Trigger phrases include "create gallery project", "clone project", "add portfolio project", "new case study", "create new project", or when users want to add a project to the gallery section of the portfolio.
---

# Clone Project

## Overview

This skill automates the creation of new gallery projects for the portfolio website. It handles project scaffolding, template selection, metadata management, and content syncing using a standardized workflow.

## When to Use This Skill

Use this skill when:
- User wants to create a new gallery/portfolio project
- User mentions adding a case study or project to the website
- User says "create project", "clone project", "add portfolio project"
- User needs to set up a new project page with proper structure

## Workflow

### Step 1: Gather Project Information

Collect the following information from the user using AskUserQuestion tool:

**Required Parameters:**
1. **Template Type**: Ask which layout to use
   - `two-column` - For case studies and product/design narratives with sticky left titles and right content (like Alibaba case study)
   - `stacked` - For art/visual projects with vertical flow of text and images (like art project layout)

2. **Project Slug**: URL-friendly identifier (will be auto-slugified)
   - Use kebab-case format (e.g., "my-design-project")
   - Avoid spaces and special characters

3. **Project Title**: Full display name (e.g., "Re-Architecting Alibaba Help Center for Global Consistency")

4. **Date**: Project date in flexible formats
   - Accepts: `YYYY-MM-DD`, `YYYY.MM`, `YYYY-MM`, or `YYYY`
   - Will be stored as ISO `YYYY-MM-DD` in gallery.json
   - Will be displayed as `YYYY.MM` on the page

5. **Tags**: Comma-separated tags (e.g., "UX Design, NLP, BART Transformer")

6. **Company**: Company or organization name (use "-" if not applicable)

7. **Classification**: Project category (must be one of):
   - `UX/Product` - UX and product design work
   - `Experiential` - Experience design and installations
   - `Content` - Content strategy and social media
   - `Visual` - Visual design and branding

8. **Description** (optional): Brief meta description for SEO

### Step 2: Execute Project Creation

Run the scaffolding script from the project root directory:

```bash
node scripts/new-gallery.js \
  --type <two-column|stacked> \
  --slug <project-slug> \
  --title "<Project Title>" \
  --date "<YYYY-MM-DD | YYYY.MM | YYYY-MM | YYYY>" \
  --tag "<Tag1, Tag2, Tag3>" \
  --company "<Company Name>" \
  --classification "<UX/Product|Experiential|Content|Visual>" \
  --description "<Optional description>" \
  --update-json true \
  --sync true
```

**What this does:**
- Creates `gallery/<slug>/` directory
- Copies and customizes template files from `assets/templates/<type>/`
- Generates `index.html` with metadata
- Creates `text.md` with template content
- Creates `public/` directory for images
- Updates `content/gallery.json` with project entry (sorted by date, newest first)
- Auto-syncs content from `text.md` into `index.html`

**Script locations in this skill:**
- `scripts/new-gallery.js` - Main scaffolding script
- `scripts/sync-gallery.js` - Content sync utility (used by new-gallery.js)

### Step 3: Guide Next Steps

After successful creation, inform the user of the following next steps:

1. **Add Images:**
   - Place `cover.png` in `gallery/<slug>/public/` (required for hero image)
   - Add body images (e.g., `body-1.png`, `body-2.png`) as needed
   - Recommend PNG/JPG format, optimized for web

2. **Edit Content:**
   - Update `gallery/<slug>/text.md` with actual project content
   - Follow the Markdown format in `/.claude/references/GALLERY_GUIDE.md`
   - Use `##` or `###` for section headers
   - Use `####` for subsection headers
   - Reference images as `./public/image-name.png`

3. **Re-sync Content (if needed):**
   - If `text.md` is updated after creation, run:
     ```bash
     node scripts/sync-gallery.js --slug <slug>
     ```
   - This updates the HTML between SYNC markers in `index.html`

4. **Preview:**
   - Open `gallery/<slug>/index.html` in browser to preview
   - Or use live server for real-time updates

### Step 4: Verify

Confirm that:
- Project directory exists at `gallery/<slug>/`
- `content/gallery.json` has been updated with new entry
- Project appears in the gallery (check homepage)

## Content Authoring Format

Projects use a standardized Markdown format in `text.md`:

```markdown
![cover](./public/cover.png)

# Project Title

### Project Brief
- Date: YYYY.MM
- Project Name: Project Title
- Tag: Tag 1, Tag 2
- Company: Company Name

### Section Title
Paragraph text here.

![Alt text](./public/image1.png)

#### Subsection Title
More detailed content.

### Another Section
- Bullet point A
- Bullet point B

![Another image](./public/image2.png)
```

**Key points:**
- The "Project Brief" section is ignored during sync (metadata comes from gallery.json)
- Headings: `##` or `###` for sections, `####` for subsections
- Images: Keep in `public/` directory, reference as `./public/<name>`
- The sync script converts Markdown to HTML and injects it between sync markers

### Embedding Video

Projects can include embedded video content from platforms like Vimeo or YouTube:

1. **In text.md:**
   - Add video link at any position in your content flow where you want the video to appear
   - Use standard Markdown link format: `[Watch the installation video](https://vimeo.com/417398448)`
   - The video will appear in the order you place it within your content sections

2. **In index.html:**
   - After running the sync script, manually add a responsive iframe embed at the corresponding position
   - Use the `.video-embed` wrapper class (included in templates) for responsive 16:9 aspect ratio
   - Example HTML structure:
     ```html
     <div class="video-embed">
       <iframe src="https://player.vimeo.com/video/417398448?fl=pl&fe=sh"
               title="Video description"
               allow="autoplay; fullscreen; picture-in-picture"
               allowfullscreen
               loading="lazy">
       </iframe>
     </div>
     ```

3. **Supported platforms:**
   - **Vimeo:** Convert link to `https://player.vimeo.com/video/VIDEO_ID`
   - **YouTube:** Convert link to `https://www.youtube.com/embed/VIDEO_ID`

4. **Reference example:**
   - See `gallery/my-friends-are-my-power-station/` for working implementation
   - Shows video link in `text.md` and corresponding iframe embed in `index.html`

**Note:** The sync script does not automatically convert video links to iframes. You must manually insert the iframe HTML after syncing content.

## Template Information

**Two-Column Template** (`assets/templates/two-column/`):
- Grid layout: sticky left title + scrolling right content
- Best for: Case studies, product narratives, design processes
- Responsive: Collapses to single column on mobile

**Stacked Template** (`assets/templates/stacked/`):
- Vertical flow: title above content
- Best for: Art projects, visual portfolios, galleries
- Simpler structure for image-heavy content

Both templates include:
- Hero image container (2:1 aspect ratio by default)
- Responsive design with mobile breakpoints
- SEO meta tags and Open Graph support
- Automatic fallback for missing cover images

## Troubleshooting

**Duplicate project error:**
- Check if project with same name or URL already exists in `content/gallery.json`
- Use a different slug or update the existing project

**Sync markers not found:**
- Ensure `index.html` contains `<!-- SYNC:CONTENT-START -->` and `<!-- SYNC:CONTENT-END -->` markers
- Templates should include these by default

**Images not showing:**
- Verify images are in `gallery/<slug>/public/` directory
- Check image paths in `text.md` use correct format: `./public/<name>.ext`
- Ensure `cover.png` exists for hero image

## Resources

### scripts/
- `new-gallery.js` - Main project scaffolding script (Node.js, no external dependencies)
- `sync-gallery.js` - Content sync utility that parses Markdown and injects into HTML

### assets/
- `templates/two-column/` - Two-column layout template files
- `templates/stacked/` - Stacked layout template files

### Global references
- `/.claude/references/GALLERY_GUIDE.md` - Complete documentation of the gallery workflow and standards
