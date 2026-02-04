---
name: Drafty
description: Create, manage, and publish blog posts on Drafty.com using the Drafty API
---

# Drafty Blog Management Skill

This skill helps you create, edit, and manage blog posts on Drafty.com directly from Claude Code.

## What is Drafty?

Drafty is a modern blogging platform focused on clean writing and publishing. Your blog lives at `drafty.com/@username`.

## Authentication

To use this skill, you need a Drafty Pro account with an API key. Get yours at:
1. Go to https://www.drafty.com/dash
2. Settings → Advanced → Developer Tools
3. Copy your API key (starts with `drafty_`)

Store it in your environment:
```bash
export DRAFTY_API_KEY="drafty_xxxxx"
```

## Core Workflows

### Creating a New Post

When a user asks to create a blog post:

1. **Draft the content** in Markdown format
2. **Generate a title** (concise, SEO-friendly)
3. **Call the API** to publish:

```bash
curl -X POST https://www.drafty.com/api/integrations/posts \
  -H "Content-Type: application/json" \
  -H "X-Drafty-API-Key: $DRAFTY_API_KEY" \
  -d '{
    "title": "Understanding AI Agents",
    "content": "# Understanding AI Agents\n\nAI agents are...",
    "visibility": "public",
    "tags": ["ai", "agents"]
  }'
```

4. **Return the post URL** to the user

### Listing Existing Posts

To see recent posts:

```bash
curl https://www.drafty.com/api/integrations/posts?limit=10 \
  -H "X-Drafty-API-Key: $DRAFTY_API_KEY"
```

Returns JSON with post metadata and URLs.

### Updating a Post

To update an existing post:

```bash
curl -X PATCH https://www.drafty.com/api/integrations/posts/{postId} \
  -H "Content-Type: application/json" \
  -H "X-Drafty-API-Key: $DRAFTY_API_KEY" \
  -d '{
    "title": "Updated Title",
    "content": "# Updated Content\n\n...",
    "visibility": "public"
  }'
```

## Best Practices

### Content Guidelines

- **Markdown format**: Use standard Markdown with GFM extensions
- **Title optimization**: Keep titles under 60 characters for SEO
- **Post structure**: Start with H1 (`#`), use logical heading hierarchy
- **Code blocks**: Use triple backticks with language tags
- **Images**: Reference external URLs or use Unsplash integration

### Visibility Options

- `public`: Visible on your blog and in search
- `unlisted`: Accessible via direct link only
- `private`: Only visible to you when logged in

### Tags

- Use lowercase, hyphenated tags: `"ai-agents"`, `"web-development"`
- Maximum 5 tags per post for best organization
- Tags create automatic filtering on your blog

## Common Tasks

### "Write a blog post about X"

1. Research the topic (if needed)
2. Draft Markdown content with proper structure
3. Generate an SEO-friendly title
4. Choose appropriate tags
5. Create the post via API
6. Return the published URL

### "List my recent posts"

1. Call GET endpoint with reasonable limit (10-20)
2. Format results in readable table
3. Include post URLs for easy access

### "Update my latest post"

1. List posts to get the most recent
2. Extract the post ID
3. Make requested changes to title/content
4. Update via PATCH endpoint
5. Confirm update with URL

## Error Handling

### Authentication Errors (401)
- Verify API key is set: `echo $DRAFTY_API_KEY`
- Check key starts with `drafty_`
- Ensure key is valid (not expired/regenerated)

### Rate Limits (429)
- Free users: 10 posts/hour
- Pro users: Higher limits
- Wait and retry after cooldown

### Validation Errors (400)
- Ensure title and content are not empty
- Check visibility is one of: public, unlisted, private
- Verify JSON structure is correct

## API Reference

**Base URL**: `https://www.drafty.com/api/integrations`

### POST /posts
Create a new blog post

**Request Body:**
```json
{
  "title": "string (required)",
  "content": "string (required, Markdown)",
  "visibility": "public|unlisted|private (default: public)",
  "tags": ["string"] (optional)
}
```

**Response:**
```json
{
  "success": true,
  "postId": "abc123",
  "url": "https://drafty.com/@username/post-slug"
}
```

### GET /posts?limit=N
List user's posts (max limit: 50)

**Response:**
```json
{
  "posts": [
    {
      "id": "abc123",
      "title": "Post Title",
      "slug": "post-slug",
      "visibility": "public",
      "url": "https://drafty.com/@username/post-slug",
      "publishedAt": "2025-01-16T12:00:00Z"
    }
  ]
}
```

### PATCH /posts/{postId}
Update an existing post

**Request Body** (all fields optional):
```json
{
  "title": "string",
  "content": "string (Markdown)",
  "visibility": "public|unlisted|private",
  "tags": ["string"]
}
```

**Response:**
```json
{
  "success": true,
  "url": "https://drafty.com/@username/post-slug"
}
```

## Examples

See `examples.md` for complete workflow examples.

## Advanced Features

### OAuth Integration
For web apps, use OAuth instead of API keys. See `/docs/CUSTOM_GPT_GUIDE.md` for details.

### MCP Server
For Claude Desktop integration, see `/docs/MCP_SERVER_GUIDE.md` for building an MCP server.

## Getting Help

- **API Issues**: Check https://www.drafty.com/docs/api
- **Skill Issues**: Review error messages and validate API key
- **Feature Requests**: support@drafty.com
