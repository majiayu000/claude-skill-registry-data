---
name: gemini-illustrations
description: Generate consistent medieval manuscript-style illustrations for the Scholastic Bible using Gemini Imagen. Use when creating images, illustrations, artwork, or visuals for Bible pages, parables, book headers, chapter art, or any visual content for the site.
---

# Gemini Illustrations for Scholastic Bible

Generate beautiful, consistent medieval illuminated manuscript-style artwork for the Scholastic Bible project using Google's Imagen model.

## When to Use This Skill

- Creating header images for book or chapter pages
- Illustrating parables, miracles, or biblical narratives
- Generating decorative elements (borders, initials, flourishes)
- Any visual content needed for the Bible site

## Quick Start

1. **Read the source content first** (REQUIRED):
   - For book images: Read the book's introduction from `site/src/data/bible.json`
   - For chapter images: Read the chapter's summary from `site/src/data/bible.json`
   - Use this context to inform what scene/imagery to depict
2. Read the style guide: `cat .claude/skills/gemini-illustrations/style-guide.md`
3. Craft a prompt that reflects the actual content/themes from step 1
4. Run the generation script with your prompt

## Reading Source Content

**IMPORTANT: Always read the actual Bible content before generating images.**

### For Book Headers

```bash
# Extract book introduction from bible.json
node -e "const b = require('./site/src/data/bible.json'); const book = b.books.find(x => x.id === 'BOOK_ID'); console.log('Introduction:', book.introduction);"
```

Or read the full bible.json and find the book's `introduction` field.

### For Chapter Images

```bash
# Extract chapter summary from bible.json
node -e "const b = require('./site/src/data/bible.json'); const book = b.books.find(x => x.id === 'BOOK_ID'); const ch = book.chapters.find(c => c.number === CHAPTER_NUM); console.log('Summary:', ch.summary);"
```

Or read the full bible.json and find the chapter's `summary` field.

### Why This Matters

The introductions and summaries contain:
- Key themes and events covered
- Important figures mentioned
- Theological context
- Specific imagery references (e.g., "the burning bush", "the flood")

This ensures generated images actually reflect the content rather than generic biblical imagery.

## Generation Script

Use `lib/generate-image.js` to generate images:

```bash
# Generate with custom prompt and output path
PROMPT="Your prompt here" OUTPUT="site/public/images/my-image.png" node lib/generate-image.js

# Use Gemini 3 for better faces and quality (recommended)
MODEL="gemini-3-pro-image-preview" PROMPT="..." OUTPUT="..." node lib/generate-image.js
```

Environment variables:
- `PROMPT` - The image generation prompt (required if not using default)
- `OUTPUT` - Output file path (default: `site/public/header.png`)
- `ASPECT` - Aspect ratio: "1:1", "3:4", "4:3", "9:16", "16:9" (default: "16:9")
- `MODEL` - Model to use (default: `gemini-3-pro-image-preview`)

### Required Model

**CRITICAL: Always use `gemini-3-pro-image-preview` for all image generation.**

```bash
MODEL="gemini-3-pro-image-preview" PROMPT="..." OUTPUT="..." node lib/generate-image.js
```

**DO NOT switch to alternative models** (imagen, gemini-flash, etc.) without explicit user permission. If quota is exhausted:
1. STOP generating images immediately
2. Report the quota error to the user
3. Wait for user instructions - do NOT automatically switch models

The style consistency of the project depends on using a single model throughout.

## Editing Existing Images

Use `lib/edit-image.js` to fix or modify existing images without regenerating from scratch. This is useful for:
- Fixing halos (cruciform → plain circular)
- Removing unwanted text/labels that appeared
- Minor adjustments while preserving the overall composition

```bash
# Edit an existing image
INPUT="site/public/images/books/image.png" PROMPT="Edit instruction here" node lib/edit-image.js

# Save to different file (for comparison)
INPUT="site/public/images/books/image.png" OUTPUT="site/public/images/books/image-edit.png" PROMPT="..." node lib/edit-image.js
```

Environment variables:
- `INPUT` - Path to existing image (required)
- `OUTPUT` - Output path (default: overwrites input)
- `PROMPT` - Edit instruction

### Effective Edit Prompts

Keep edit prompts simple and specific:
```
# Good - specific and focused
"Change the halo to be a simple plain gold circular disc. Keep everything else the same."

# Good - targeted fix
"Remove the text/lettering from the image. Keep everything else identical."

# Bad - too vague
"Make it better"
```

### When to Edit vs Regenerate

**Use editing when:**
- The overall composition is good but one element is wrong
- You want to preserve a specific scene/pose
- Minor fixes needed (halo style, remove text)

**Regenerate when:**
- Multiple major issues
- Wrong subject matter entirely
- Composition doesn't work

## Prompt Construction

Always include these elements in order:

1. **Subject**: What is being depicted (biblical scene, symbol, figure)
2. **Style anchor**: "Medieval illuminated manuscript style" or "Book of Kells style"
3. **Visual elements**: From the style guide (gold leaf, Celtic knotwork, aged parchment)
4. **Halo specification**: See critical halo rules below
5. **Color palette**: Burgundy, gold, cream, oak tones
6. **Composition note**: "wide banner format" or "square vignette" etc.
7. **Exclusions**: "no modern elements, no text, no labels, no words, no lettering"

**CRITICAL HALO RULES:**
- **Saints, apostles, prophets, angels**: Plain circular gold halo only
- **Christ ONLY**: May have cruciform halo (halo with cross)
- **Why this matters**: The cruciform halo is reserved exclusively for Christ. Using it for saints is theologically incorrect.

**Prompting strategy for halos:**
- Keep it minimal - don't over-specify or use negative language
- GOOD: "prophet with golden halo" or just let medieval style imply it
- BAD: "NOT cruciform", "no cross in halo" (negative prompts backfire)
- If the result has wrong halo, use `edit-image.js` to fix it rather than complex prompting

**IMPORTANT: Always exclude text from images.** Imagen is unreliable at spelling and lettering. Even requests for labels, names, or decorative text often produce gibberish or misspelled words. Use purely visual storytelling instead.

## Example Prompts

### Book Header (Genesis)
```
Creation of the world with light separating from darkness, medieval illuminated manuscript style.
Features: ornate golden Celtic knotwork border, divine light rays in gold leaf, swirling cosmos.
Colors: deep midnight blue, brilliant gold, cream highlights.
Composition: wide banner format. No text, no labels, no words, no lettering.
```

### Parable Illustration (Prodigal Son)
```
The return of the prodigal son embraced by his father, medieval illuminated manuscript style.
Features: Byzantine-influenced figures, pastoral background, ornate border.
Colors: rich burgundy robes, gold leaf accents, earth tones.
Composition: square vignette with decorative corner flourishes.
```

### Apostle/Saint Portrait (for Epistles)
```
Saint Paul writing an epistle in prison, medieval illuminated manuscript style.
Features: Byzantine-influenced figure, writing implements, chains, divine light through window, Celtic knotwork border.
Colors: burgundy and gold robes, aged parchment, warm stone textures.
Composition: wide banner format.
```

### Chapter Decoration
```
Decorative illuminated border frame with empty center, medieval manuscript style.
Features: intricate Celtic interlace patterns, vine scrollwork, small symbolic animals in corners.
Colors: deep burgundy, forest green, burnished gold, aged parchment background.
Composition: square format, suitable as decorative element. No text, no letters, no writing.
```

## File Organization

Save generated images to:
- `site/public/images/books/` - Book header images (named `{book-id}.png`, e.g., `genesis.png`)
- `site/public/images/chapters/` - Chapter illustrations
- `site/public/images/parables/` - Parable and narrative scenes
- `site/public/images/decorative/` - Borders, initials, flourishes

## Integration with Site

**IMPORTANT: After generating an image, you MUST integrate it into the site.**

### Book Header Images

Book pages automatically display header images if they exist at `site/public/images/books/{book-id}.png`.

The `[book]/index.astro` template checks for the image and renders a hero section:
- Image displays as a full-width banner with gradient overlay
- Book title overlays the image
- Falls back gracefully if no image exists

**Naming convention**: Use the book's URL ID (e.g., `genesis.png`, `1-corinthians.png`, `acts.png`)

### Chapter Images

Chapter pages automatically display header images if they exist at `site/public/images/chapters/{book-id}-{chapter}.png`.

The `[book]/[chapter].astro` template checks for the image and renders a hero section:
- Image displays as a full-width banner with gradient overlay
- Chapter title overlays the image
- Falls back gracefully if no image exists

**Naming convention**: Use `{book-id}-{chapter-number}.png` (e.g., `philemon-1.png`, `genesis-3.png`, `psalms-23.png`)

### Manual Integration

If adding images to other pages, use this pattern:
```astro
<img src={`${import.meta.env.BASE_URL}images/books/genesis.png`} alt="Genesis" />
```

### Integration Checklist

After generating an image:
- [ ] Verify image saved to correct path
- [ ] Confirm filename matches expected pattern ({book-id}.png)
- [ ] Test page loads image correctly (run dev server)
- [ ] Check image displays properly with overlay text readable

## Style Consistency Checklist

Before generating, verify your prompt includes:
- [ ] Medieval/manuscript style anchor phrase
- [ ] At least 2-3 visual elements from style guide
- [ ] **Halo specification** (if depicting holy figures): "plain circular gold halo" for saints, "cruciform halo" ONLY for Christ
- [ ] Appropriate color palette
- [ ] **Text exclusion phrase** (e.g., "no text, no labels, no words, no lettering")
- [ ] Correct aspect ratio for intended use

**Halo Warning:** The cruciform halo is reserved for Christ alone. For saints/apostles, keep halo prompts minimal (e.g., "golden halo") and use `edit-image.js` to fix any incorrect results rather than over-specifying in prompts.

**Text Warning:** Never request text, labels, names, banners, scrolls with writing, or any lettering. Imagen produces unreliable spelling and gibberish. Convey meaning through imagery alone.

See `style-guide.md` for complete visual reference.
