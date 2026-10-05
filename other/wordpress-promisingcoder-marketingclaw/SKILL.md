---
name: wordpress
description: "Publishing and scheduling blog posts on self-hosted or WordPress.com sites via the WP REST API — drafts, media upload, categories/tags, and status=future scheduled publishing using Application Passwords."
homepage: https://developer.wordpress.org/rest-api/
metadata:
  {
    "marketingclaw":
      {
        "emoji": "📝",
        "requires":
          {
            "bins": ["curl", "jq"],
            "env": ["WORDPRESS_URL", "WORDPRESS_USER", "WORDPRESS_APP_PASSWORD"],
          },
        "primaryEnv": "WORDPRESS_APP_PASSWORD",
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "jq",
              "bins": ["jq"],
              "label": "Install jq (brew)",
            },
          ],
      },
  }
---

# WordPress Skill

Publish and manage blog content on a WordPress site via the built-in WP REST API
(`/wp-json/wp/v2/...`), authenticated with an Application Password — no OAuth app needed.

## Draft-first rule

**Every post is created with `"status": "draft"` first.** Show the draft (title + body + any
scheduled time) to the human and get explicit approval before flipping `status` to `publish` or
`future`. Never create a post directly as `publish`.

## Setup

1. In WordPress admin: Users → Profile (for the account you'll post as) → scroll to
   "Application Passwords" → enter a name (e.g. "MarketingClaw") → Add New Application Password.
2. Copy the generated password (shown once, spaces included).
3. Set environment variables:
   ```bash
   export WORDPRESS_URL="https://yourblog.example.com"
   export WORDPRESS_USER="your-wp-username"
   export WORDPRESS_APP_PASSWORD="xxxx xxxx xxxx xxxx xxxx xxxx"   # keep the spaces
   ```
4. Application Passwords require HTTPS on the site (or `WP_ENVIRONMENT_TYPE=local` for local dev).

All requests use HTTP Basic auth: `curl -u "$WORDPRESS_USER:$WORDPRESS_APP_PASSWORD"`.

## Create a draft post

```bash
curl -s -u "$WORDPRESS_USER:$WORDPRESS_APP_PASSWORD" \
  -X POST "${WORDPRESS_URL%/}/wp-json/wp/v2/posts" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "5 Things We Learned Shipping v2",
    "content": "<p>Full post body as HTML...</p>",
    "status": "draft",
    "categories": [3],
    "tags": [12, 18]
  }' | jq '{id, link, status}'
```

## Update a post / publish / schedule

```bash
# Publish now (only after approval)
curl -s -u "$WORDPRESS_USER:$WORDPRESS_APP_PASSWORD" \
  -X POST "${WORDPRESS_URL%/}/wp-json/wp/v2/posts/POST_ID" \
  -H "Content-Type: application/json" \
  -d '{"status": "publish"}' | jq '{id, link, status}'

# Schedule for later (only after approval) — status=future + a future "date" (site-local time)
curl -s -u "$WORDPRESS_USER:$WORDPRESS_APP_PASSWORD" \
  -X POST "${WORDPRESS_URL%/}/wp-json/wp/v2/posts/POST_ID" \
  -H "Content-Type: application/json" \
  -d '{"status": "future", "date": "2026-07-15T09:00:00"}' | jq '{id, link, status, date}'
```

`date` is site-local time without a timezone suffix; use `date_gmt` (with a `Z` suffix) instead
if you want to specify UTC explicitly.

## Media upload

```bash
curl -s -u "$WORDPRESS_USER:$WORDPRESS_APP_PASSWORD" \
  -X POST "${WORDPRESS_URL%/}/wp-json/wp/v2/media" \
  -H "Content-Disposition: attachment; filename=\"hero.jpg\"" \
  -H "Content-Type: image/jpeg" \
  --data-binary "@/path/to/hero.jpg" | jq '{id, source_url}'

# Set as the post's featured image
curl -s -u "$WORDPRESS_USER:$WORDPRESS_APP_PASSWORD" \
  -X POST "${WORDPRESS_URL%/}/wp-json/wp/v2/posts/POST_ID" \
  -H "Content-Type: application/json" \
  -d '{"featured_media": MEDIA_ID}' | jq '{id, featured_media}'
```

## Categories and tags

```bash
# List / find
curl -s -u "$WORDPRESS_USER:$WORDPRESS_APP_PASSWORD" "${WORDPRESS_URL%/}/wp-json/wp/v2/categories?per_page=100" | jq '.[] | {id, name}'
curl -s -u "$WORDPRESS_USER:$WORDPRESS_APP_PASSWORD" "${WORDPRESS_URL%/}/wp-json/wp/v2/tags?per_page=100" | jq '.[] | {id, name}'

# Create
curl -s -u "$WORDPRESS_USER:$WORDPRESS_APP_PASSWORD" -X POST "${WORDPRESS_URL%/}/wp-json/wp/v2/categories" \
  -H "Content-Type: application/json" -d '{"name": "Product"}' | jq '{id, name}'
curl -s -u "$WORDPRESS_USER:$WORDPRESS_APP_PASSWORD" -X POST "${WORDPRESS_URL%/}/wp-json/wp/v2/tags" \
  -H "Content-Type: application/json" -d '{"name": "launch"}' | jq '{id, name}'
```

## List / check posts

```bash
curl -s -u "$WORDPRESS_USER:$WORDPRESS_APP_PASSWORD" \
  "${WORDPRESS_URL%/}/wp-json/wp/v2/posts?status=draft,future,publish&per_page=20" | \
  jq '.[] | {id, title: .title.rendered, status, date, link}'
```

Note: filtering by non-`publish` statuses requires an authenticated request (Basic auth above) —
anonymous requests only ever see published posts.

## Notes

- `content` accepts raw HTML (Gutenberg block markup or plain HTML both render fine); avoid
  hand-writing block comments unless you need specific block behavior.
- Rate limits are host-dependent (WordPress core has none by default; managed hosts like
  WordPress.com or WP Engine may throttle) — back off on 429s.
- Application Passwords can be revoked per-app from the same Profile screen without touching the
  user's main login password.
- Never print `$WORDPRESS_APP_PASSWORD` in logs or chat.
