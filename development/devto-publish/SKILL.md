---
name: devto-publish
description: Publish articles to Dev.to. Use this skill when the article is ready and user wants to publish.
---

# Dev.to Publisher

This skill publishes articles to Dev.to using their official API.

## When to Use

Use this skill when:
- Article content is finalized
- Featured image has been generated
- Ready to publish the completed article

## Prerequisites

The `DEVTO_API_KEY` environment variable must be set with your Dev.to API key.

To get your API key:
1. Go to https://dev.to/settings/extensions
2. Scroll to "DEV Community API Keys"
3. Enter a description and click "Generate API Key"
4. Copy the key

## How to Use

```bash
/home/user/.claude/skills/devto-publish/scripts/devto-publish.sh <article_file> [--title "Title"] [--tags "tag1,tag2,tag3"] [--published true|false] [--image url]
```

### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| article_file | Yes | - | Path to markdown file |
| --title | No | From file | Article title (overrides H1 in file) |
| --tags | No | - | Comma-separated tags (max 4) |
| --published | No | false | Set to `true` to publish immediately |
| --image | No | - | Cover image URL |

### Standard Usage for Content Farm Workflow

```bash
/home/user/.claude/skills/devto-publish/scripts/devto-publish.sh \
  /home/user/workspace/output/article.md \
  --tags "ai,technology,automation" \
  --published true
```

### With Cover Image

Use the fal.ai image URL from the image-gen skill response:

```bash
/home/user/.claude/skills/devto-publish/scripts/devto-publish.sh \
  /home/user/workspace/output/article.md \
  --tags "ai,tech,automation" \
  --image "https://storage.googleapis.com/fal-flux/..." \
  --published true
```

## Output Preparation

Before publishing, ensure these files exist in `/home/user/workspace/output/`:

### article.md
The complete article in Markdown format.

### featured.png
The generated featured image (copied from `/tmp/images/`).

### metadata.json
SEO metadata in this format:

```json
{
  "title": "Your SEO-optimized title",
  "description": "Meta description (150-160 characters)",
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "sources": [
    "https://source1.com/article",
    "https://source2.com/article"
  ],
  "word_count": 1200,
  "generated_at": "2024-01-15T10:30:00Z"
}
```

## Response

Returns the Dev.to article URL on success.

Response saved to `/tmp/devto/publish_response.json`:
```json
{
  "id": 123456,
  "title": "Article Title",
  "url": "https://dev.to/username/article-slug",
  "published": true
}
```

**Always report the `url` back to the user after successful publishing.**

## Guidelines

1. Always use `--published true` to publish publicly (content farm workflow default)
2. Dev.to supports up to 4 tags per post
3. Tags should be lowercase, no spaces
4. Cover images must be URLs (use the fal.ai URL from image-gen response)
5. Markdown is fully supported including code blocks with syntax highlighting
6. Choose tags that match the article topic (e.g., "ai", "technology", "programming", "automation")
