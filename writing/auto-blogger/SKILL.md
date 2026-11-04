---
name: auto-blogger
description: Autonomous blog post creation agent. Given a topic, it generates subtopics, outlines, full articles, and featured images.
tools_required: [wp_create_post, wp_update_post, wp_generate_image, seo_analyze, wp_taxonomy]
always_on: false
group: content
order: 5
suggests: [seo-optimizer, content-creator]
---

# Auto-Blogger

The Auto-Blogger is an autonomous agent designed to scale content production. It takes a high-level topic and handles the entire production lifecycle from ideation to publishing.

## Key Capabilities

1.  **Topic Expansion**: Breaks down broad topics into specific article ideas.
2.  **Autonomous Writing**: Creates comprehensive, structured blog posts.
3.  **Visuals**: Automatically generates and attaches relevant featured images.
4.  **SEO Loop**: Optimizes content before finalization.

## Usage Workflows

### 1. Single Post Generation
**Trigger**: "Write a blog post about [Topic]"

**Steps**:
1.  **Outline**: fast-track outline generation (Introduction, Key Points, Conclusion).
2.  **Draft**: Write the content using HTML formatting (h2, h3, lists).
3.  **Image**: Call `wp_generate_image` with a prompt based on the title.
4.  **Publish**: Create post using `wp_create_post` with status='publish' (or 'draft' if requested).

### 2. Bulk Series Generation
**Trigger**: "Create a 5-part series on [Topic]"

**Steps**:
1.  **Ideation**: Generate 5 distinct sub-topic titles.
2.  **Approval**: Present titles to user (if interactive) or proceed (if autonomous).
3.  **Loop**: For each title:
    *   Generate Content.
    *   Generate Image.
    *   Post to WordPress.
    *   Interlink previous post if applicable.

## Instruction Prompts

### Writing Style
*   **Tone**: Professional yet engaging.
*   **Structure**: Use short paragraphs, bullet points, and clear headings.
*   **Formatting**: ALWAYS returns content in valid HTML (no markdown in the `content` field of the tool).

### Image Generation
*   **Prompt Strategy**: "High quality, photorealistic, professional photography, [Topic specific details], soft lighting, 4k"
*   **Tool**: `wp_generate_image`
*   **Integration**: Use the returned `attachment_id` as `featured_image_id` in `wp_create_post` (or update via `wp_update_post`).

## Example Workflow (Internal)

```javascript
// Pseudo-code for agent logic
const title = "The Future of AI in WordPress";
const prompt = "Futuristic glowing AI brain connecting to WordPress logo, digital art, kyberpunk style";

// 1. Generate Image
const imgResult = wp_generate_image({ prompt: prompt });
const imgId = imgResult.attachment_id;

// 2. Write Post
const content = "<h2>Introduction</h2><p>AI is changing...</p>...";
wp_create_post({
  title: title,
  content: content,
  status: 'draft',
  featured_image_id: imgId
});
```
