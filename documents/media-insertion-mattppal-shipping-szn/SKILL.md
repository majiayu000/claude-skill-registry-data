---
name: media-insertion
description: >-
  Insert images and videos from Slack messages into changelog markdown. Use when
  you have media files downloaded from Slack that need to be included in
  documentation.
targets:
  - '*'
---
# Media Insertion for Changelogs

This skill teaches you how to properly insert media (images and videos) from Slack into changelog content.

## Overview

When Slack messages include media files, the `fetch_messages_from_channel` tool downloads them to:
```
./docs/updates/media/YYYY-MM-DD/filename
```

You must insert references to these files in the markdown content so they appear in the final changelog.

## Step 1: Identify Media from Slack Response

The Slack tool response includes `processed_files` for each message with media:

```
📝 Message 1:
   💬 Text: Check out this new feature!
   📎 Files (1):
      🖼️ Image: feature-screenshot_abc123.png
        Path: ./docs/updates/media/2025-11-06/feature-screenshot_abc123.png
```

## Step 2: Insert Media References in Markdown

When writing the changelog content, insert the image reference right after describing the feature:

```markdown
### New feature name

Description of the feature and what it does.

![Alt text describing the image](./media/2025-11-06/feature-screenshot_abc123.png)

More details about the feature...
```

**Important:**
- Use the **local path** format: `./media/YYYY-MM-DD/filename`
- Write descriptive alt text that explains what the image shows (be specific, not generic)
- Place images where they make sense contextually (after introducing the feature)
- **Only reference images that actually exist in the Slack response** - check the file paths shown
- For videos (.mp4, .mov, .webm), use the same markdown syntax

## Step 3: Verify Images Before Inserting

Before adding an image reference to your markdown:
1. Check the Slack tool response for the exact filename
2. Verify the path matches: `./docs/updates/media/YYYY-MM-DD/filename`
3. Use that exact filename in your markdown reference: `./media/YYYY-MM-DD/filename`

**DO NOT** insert image references for files that weren't downloaded or don't appear in the Slack response.

## Step 4: Template Formatter Converts to Final Format

The `template_formatter` agent will later:
1. Verify each image file exists at `./docs/updates/media/YYYY-MM-DD/filename`
2. Convert paths: `./media/YYYY-MM-DD/filename` → `/images/changelog/YYYY-MM-DD/filename`
3. Wrap in Frame tags: `<Frame><img src="/images/changelog/..." alt="..." /></Frame>`
4. Convert video references to: `<Frame><video src="/images/changelog/..." controls /></Frame>`

## Examples

### Example 1: Single Image with Feature

**Slack message:**
- Text: "New planning mode UI with task list"
- Image: `planning-mode_xyz789.png`

**Changelog content you write:**
```markdown
### Agent planning mode improvements

Agent now shows a clear task list in planning mode, making it easier to review and approve what will be built.

![Plan mode interface showing task list and Start building button](./media/2025-11-06/planning-mode_xyz789.png)

This improvement addresses feedback from users who wanted more visibility...
```

### Example 2: Multiple Images for One Feature

**Slack message:**
- Text: "Redesigned settings page"
- Images: `settings-before_abc123.png`, `settings-after_def456.png`

**Changelog content you write:**
```markdown
### Settings page redesign

We've redesigned the settings page with a cleaner layout and better organization.

![Previous settings page layout](./media/2025-11-06/settings-before_abc123.png)

The new design groups related settings together and uses clearer labels:

![New settings page with improved organization](./media/2025-11-06/settings-after_def456.png)
```

### Example 3: Video Demo

**Slack message:**
- Text: "Agent can now stream responses"
- Video: `streaming-demo_ghi789.mp4`

**Changelog content you write:**
```markdown
### Real-time Agent streaming

Agent responses now stream in real-time, showing you progress as it works.

![Agent streaming responses demo](./media/2025-11-06/streaming-demo_ghi789.mp4)

This makes the experience feel faster and more interactive.
```

## Best Practices

1. **Always include media when available** - If Slack downloaded a file, it's relevant to the update
2. **Write descriptive alt text** - Explain what the image shows, not just "screenshot"
3. **Place strategically** - Insert images after you introduce the concept they illustrate
4. **Use local paths** - Don't try to convert paths yourself, use `./media/YYYY-MM-DD/filename`
5. **One image per feature minimum** - Visual updates should have visual proof

## Common Mistakes to Avoid

❌ **Don't skip images:**
```markdown
### New dashboard
We redesigned the dashboard.
```

✅ **Do include them:**
```markdown
### New dashboard
We redesigned the dashboard with a modern layout.

![New dashboard showing metrics overview](./media/2025-11-06/dashboard_abc123.png)
```

❌ **Don't use placeholder text:**
```markdown
![Image](./media/2025-11-06/file.png)
```

✅ **Do write descriptive alt text:**
```markdown
![Analytics dashboard with user engagement metrics](./media/2025-11-06/analytics_abc123.png)
```

## Quick Checklist

Before finishing your changelog content:
- [ ] Check Slack response for `processed_files`
- [ ] Insert image reference for each file
- [ ] Write descriptive alt text for each image
- [ ] Use local path format (`./media/YYYY-MM-DD/filename`)
- [ ] Place images contextually near related text
