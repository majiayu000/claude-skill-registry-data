---
name: notion-to-mdx
description: Automatically converts Notion markdown exports to Next.js MDX format with proper metadata and formatting. Use this skill when working with Notion markdown files that need to be converted to page.mdx files in this Next.js repository. Handles title extraction, interactive dropdown creation, and automatic image downloading from Notion.
---

# Notion to MDX Converter

## Overview

This skill automates the conversion of Notion markdown exports into Next.js MDX-compatible format for this repository. It handles metadata extraction, formatting transformations, interactive conversion of expandable sections, and automatic downloading of images from Notion.

## When to Use This Skill

Use this skill when:
- Converting Notion markdown exports to page.mdx files in this repository
- A file needs MDX frontmatter metadata added
- Notion-specific markdown syntax needs to be transformed to Next.js MDX format
- User mentions converting Notion content or asks to work with Notion markdown

## Conversion Workflow

### Step 1: Identify the Source File

When a user requests conversion of Notion markdown, identify the target file:
- User may provide a file path directly
- User may have a file open in their editor (check system reminders)
- User may paste Notion markdown content directly

### Step 2: Run the Conversion Script

Execute the conversion script with the appropriate file path:

```bash
python .claude/skills/notion-to-mdx/scripts/convert_notion_to_mdx.py <input_file> [output_file] [--page-id PAGE_ID]
```

**Parameters:**
- `<input_file>`: Path to the Notion markdown file (required)
- `[output_file]`: Optional output path (defaults to overwriting input file)
- `--page-id PAGE_ID`: Optional Notion page ID for downloading images

**Image Downloading:**
If `--page-id` is provided and `NOTION_API_KEY` is found in `.env.local`, the script will:
- Detect Notion image attachments (format: `![text](attachment:UUID:filename)`)
- Download images from Notion using the API
- Save images to `public/images/from-notion/` using the attachment ID as the filename
- Update markdown references to point to local files

**The script will:**
1. Download Notion images (if page ID provided)
2. Extract the title from the first top-level heading (`# Title`)
3. Add MDX frontmatter with the title metadata
4. Identify bullet list sections and interactively prompt about expandable dropdowns

### Step 3: Interactive Dropdown Conversion

The script will identify bullet list sections in the document and prompt the user:

```
--- Section 1 (lines 45-52) ---
- First bullet point
- Second bullet point
- Third bullet point

Convert this to expandable dropdown? (y/n):
```

If the user responds 'y', the script prompts for summary text:

```
Enter the summary text (what appears when collapsed):
```

The script then converts the bullet list to:

```html
<details>
  <summary>User's summary text</summary>

- First bullet point
- Second bullet point
- Third bullet point
</details>
```

### Step 4: Verify the Output

After conversion, review the generated MDX file to ensure:
- Title metadata is correct in the frontmatter
- Expandable dropdowns are correctly formatted
- Images are downloaded to `public/images/` and references are updated
- File structure matches Next.js MDX requirements

## Conversion Details

### Title Extraction

The script extracts the title from the first top-level heading in the markdown:

```markdown
# My Document Title

Content here...
```

Becomes:

```mdx
---
title: "My Document Title"
---

# My Document Title

Content here...
```

If no top-level heading is found, defaults to "Untitled".

### Expandable Dropdowns

Regular bullet lists in Notion exports appear as standard markdown bullets. The script identifies these sections and allows interactive conversion to HTML `<details>` elements:

**Before (Notion bullet list):**
```markdown
- Point one
- Point two
- Point three
```

**After (if converted to dropdown):**
```html
<details>
  <summary>Click to expand</summary>

- Point one
- Point two
- Point three
</details>
```

### Image Downloading

When a Notion page ID is provided via `--page-id`, the script automatically downloads images embedded in the Notion export.

**How it works:**
1. Script scans the markdown for Notion image attachments: `![alt](attachment:UUID:filename)`
2. Extracts the attachment IDs from the markdown
3. Fetches blocks from the Notion page using the API
4. Matches attachment IDs to find signed S3 URLs
5. Downloads images to `public/images/from-notion/`
6. Uses the attachment ID as the filename (keeping original extension)
7. Updates markdown references to point to local files

**Before (Notion attachment):**
```markdown
![image.png](attachment:6e9315e9-4f0f-4fec-82d9-28ef74260e5f:image.png)
```

**After (local reference):**
```markdown
![image.png](/public/images/from-notion/6e9315e9-4f0f-4fec-82d9-28ef74260e5f.png)
```

**Requirements:**
- Notion page must be shared with the integration (API key owner)
- `NOTION_API_KEY` must be present in `.env.local`
- Page ID can be extracted from Notion URL: `notion.site/Page-Title-{PAGE_ID}`

**Note:** The script automatically searches for `.env.local` starting from the input file's directory up to the repository root.

## Example Usage

**User request:** "Convert the Notion markdown in app/my-post/page.mdx and download the images"

**Actions:**
1. Extract page ID from Notion URL (e.g., `1f82e4fe580280a29479cba5d8ffa898`)
2. Run: `python .claude/skills/notion-to-mdx/scripts/convert_notion_to_mdx.py app/my-post/page.mdx --page-id 1f82e4fe580280a29479cba5d8ffa898`
3. Script automatically:
   - Finds `NOTION_API_KEY` in `.env.local`
   - Downloads images from Notion
   - Extracts title
   - Prompts user about bullet list sections for dropdown conversion
4. User responds to prompts interactively
5. File is updated with converted content and local image references

**Example without images:**
```bash
python .claude/skills/notion-to-mdx/scripts/convert_notion_to_mdx.py app/my-post/page.mdx
```

**Example with images:**
```bash
python .claude/skills/notion-to-mdx/scripts/convert_notion_to_mdx.py app/my-post/page.mdx --page-id 1f82e4fe580280a29479cba5d8ffa898
```

## Non-Interactive Mode

To skip the interactive dropdown prompts (useful when no dropdowns are needed), modify the script call in code:

```python
convert_notion_to_mdx(input_path, output_path, interactive=False)
```

This will perform title extraction only.

## Resources

### scripts/convert_notion_to_mdx.py

Python script that performs the markdown-to-MDX conversion. Handles:
- Notion image downloading via API
- Title extraction from top-level headings
- MDX frontmatter generation
- Interactive dropdown creation with user prompts
- Automatic `.env.local` discovery for API credentials

**Dependencies:** `requests` library for HTTP requests to Notion API

The script can be executed directly from the command line or imported as a Python module for programmatic use.
