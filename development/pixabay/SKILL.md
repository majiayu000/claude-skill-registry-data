---
name: pixabay
description: Search and download royalty-free images and videos from Pixabay. This skill should be used when the user needs stock photos, illustrations, vectors, or videos for projects. Supports filtering by type, category, color, orientation, and more.
---

# Pixabay API

Search and retrieve royalty-free images and videos from Pixabay's library of over 4 million assets.

## Configuration

The API key is stored in `~/.config/pixabay/api_key`. To set up:

```bash
mkdir -p ~/.config/pixabay
echo "YOUR_API_KEY" > ~/.config/pixabay/api_key
```

Read the key with:
```bash
PIXABAY_KEY=$(cat ~/.config/pixabay/api_key)
```

## Quick Start

### Search Images

```bash
PIXABAY_KEY=$(cat ~/.config/pixabay/api_key)
curl -s "https://pixabay.com/api/?key=${PIXABAY_KEY}&q=yellow+flowers&image_type=photo" | jq
```

### Search Videos

```bash
PIXABAY_KEY=$(cat ~/.config/pixabay/api_key)
curl -s "https://pixabay.com/api/videos/?key=${PIXABAY_KEY}&q=nature" | jq
```

## Image Search Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `key` | str | **Required.** API key |
| `q` | str | URL-encoded search term (max 100 chars). Example: `yellow+flower` |
| `lang` | str | Language code: cs, da, de, en, es, fr, id, it, hu, nl, no, pl, pt, ro, sk, fi, sv, tr, vi, th, bg, ru, el, ja, ko, zh. Default: `en` |
| `id` | str | Retrieve specific image by ID |
| `image_type` | str | `all`, `photo`, `illustration`, `vector`. Default: `all` |
| `orientation` | str | `all`, `horizontal`, `vertical`. Default: `all` |
| `category` | str | backgrounds, fashion, nature, science, education, feelings, health, people, religion, places, animals, industry, computer, food, sports, transportation, travel, buildings, business, music |
| `min_width` | int | Minimum width. Default: 0 |
| `min_height` | int | Minimum height. Default: 0 |
| `colors` | str | Comma-separated: grayscale, transparent, red, orange, yellow, green, turquoise, blue, lilac, pink, white, gray, black, brown |
| `editors_choice` | bool | Editor's Choice only. Default: `false` |
| `safesearch` | bool | Safe content only. Default: `false` |
| `order` | str | `popular` or `latest`. Default: `popular` |
| `page` | int | Page number. Default: 1 |
| `per_page` | int | Results per page (3-200). Default: 20 |

## Video Search Parameters

Same as images, except:
- Endpoint: `https://pixabay.com/api/videos/`
- Use `video_type` instead of `image_type`: `all`, `film`, `animation`

## Response Structure

### Image Response

```json
{
  "total": 4692,
  "totalHits": 500,
  "hits": [
    {
      "id": 195893,
      "pageURL": "https://pixabay.com/en/blossom-bloom-flower-195893/",
      "type": "photo",
      "tags": "blossom, bloom, flower",
      "previewURL": "https://cdn.pixabay.com/.../flower-195893_150.jpg",
      "webformatURL": "https://pixabay.com/get/...640.jpg",
      "largeImageURL": "https://pixabay.com/get/..._1280.jpg",
      "imageWidth": 4000,
      "imageHeight": 2250,
      "views": 7671,
      "downloads": 6439,
      "likes": 5,
      "user": "Josch13",
      "userImageURL": "https://cdn.pixabay.com/user/.../250x250.jpg"
    }
  ]
}
```

### Video Response

```json
{
  "total": 42,
  "totalHits": 42,
  "hits": [
    {
      "id": 125,
      "pageURL": "https://pixabay.com/videos/id-125/",
      "type": "film",
      "tags": "flowers, yellow, blossom",
      "duration": 12,
      "videos": {
        "large": { "url": "..._large.mp4", "width": 1920, "height": 1080 },
        "medium": { "url": "..._medium.mp4", "width": 1280, "height": 720 },
        "small": { "url": "..._small.mp4", "width": 960, "height": 540 },
        "tiny": { "url": "..._tiny.mp4", "width": 640, "height": 360 }
      }
    }
  ]
}
```

## Image URL Sizes

Replace `_640` in `webformatURL` to get other sizes:
- `_180` - 180px height
- `_340` - 340px height
- `_960` - max 960x720px

## Rate Limits

- 100 requests per 60 seconds
- Results must be cached for 24 hours
- Check headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

## Usage Requirements

When displaying search results, credit Pixabay as the source. Hotlinking images is not allowed - download to local storage for use. Videos may be embedded directly.

## Common Workflows

### Download Best Image for a Query

```bash
PIXABAY_KEY=$(cat ~/.config/pixabay/api_key)
# Search and get the first result's large image URL
URL=$(curl -s "https://pixabay.com/api/?key=${PIXABAY_KEY}&q=mountain+sunset&image_type=photo&per_page=3" | jq -r '.hits[0].largeImageURL')
# Download it
curl -o mountain_sunset.jpg "$URL"
```

### Browse Categories

To explore available content, search with category filter:
```bash
curl -s "https://pixabay.com/api/?key=${PIXABAY_KEY}&category=nature&editors_choice=true&per_page=5" | jq '.hits[] | {id, tags, previewURL}'
```
