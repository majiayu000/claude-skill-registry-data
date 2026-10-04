---
name: youtube-auto
description: "Automate YouTube content creation, SEO optimization, thumbnail generation, and channel management."
triggers:
  - "youtube automation"
  - "YouTube SEO"
  - "自动上传 YouTube"
  - "generate thumbnail"
---

# YouTube Auto

Automated YouTube channel management and content optimization.

## Features

- 📤 **Auto Upload** — Schedule and publish videos
- 🖼️ **Thumbnail Gen** — AI-powered thumbnail creation
- 🔍 **SEO Optimize** — Title, description, tags
- 📊 **Analytics** — View performance metrics
- 💬 **Comment Mgmt** — Auto-reply to comments

## Usage

### Upload Video

```bash
hermes youtube upload video.mp4 \
  --title "How to build an AI Agent" \
  --description "In this video..." \
  --tags "AI,Python,Tutorial" \
  --schedule "2026-06-01 14:00"
```

### Generate Thumbnail

```bash
hermes youtube thumbnail video.mp4 \
  --style "clickbait" \
  --text "AI AGENT" \
  --output thumbnail.png
```

### SEO Optimization

```bash
hermes youtube seo --title "Your Title" --analyze
```

## Configuration

```yaml
# youtube-config.yml
channel:
  api_key: ${YOUTUBE_API_KEY}
  channel_id: UCxxxxx

upload:
  default_category: Education
  default_privacy: public
  
seo:
  min_title_length: 30
  max_tags: 15
```

## Pitfalls

1. **Copyright** — Don't use copyrighted music/media
2. **Thumbnail Policy** — Avoid clickbait/misleading images
3. **Upload Limits** — 100 videos per day limit