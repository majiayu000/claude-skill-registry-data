---
name: meta-ads-extractor
description: Extract and save ad creative assets (images and videos) from Meta Ads Library. Use when downloading competitor ad creatives, building a swipe file, researching ad formats, or saving Meta/Facebook ad images and videos from specific advertisers.
---

# Meta Ads Library Asset Extraction

Extract actual ad creative images and videos from Meta's Ad Library via browser automation.

## Prerequisites

- Browser tool (openclaw browser or Playwright)
- `curl` for downloading assets

## Workflow

### 1. Get the correct Ad Library Page ID

The Ad Library uses a **delegate_page ID**, NOT the profile ID from meta tags. This is the #1 source of errors.

```
Navigate to: https://www.facebook.com/<page-username>/
Extract via JS: document.documentElement.innerHTML.match(/"delegate_page":\{[^}]*"id":"(\d+)"/)
Fallback (if no delegate_page): use fb://profile/<id> from al:android:url meta tag
```

The delegate_page ID is what `view_all_page_id` parameter expects.

### 2. Open the Ad Library with filters

Build URL with these parameters:
```
https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=ALL&is_targeted_country=false&media_type=image_and_meme&search_type=page&view_all_page_id={PAGE_ID}
```

Key filter values:
- `active_status`: `active` | `inactive` | `all`
- `media_type`: `image_and_meme` | `video` | `all` (omit for all)
- `country`: `ALL` | `US` | `DE` etc.

### 3. Extract media URLs from DOM

Run the extraction JS from `references/dom-selectors.md` via browser evaluate. Returns JSON with image and video URLs.

**Important: extraction ≠ downloading.** The JS extracts ALL URLs from the page (instant, no network cost). Then download only the specific assets requested. When the user asks for "top N ads," the page sort order matches DOM order — so `images[0]` / `videos[0]` = highest impressions.

**Image selectors:** `img` elements with `fbcdn.net` src containing `s600x600` (ad thumbnails).
**Video selectors:** `video` elements with `fbcdn.net` src (direct .mp4 URLs).
**Video posters:** `video[poster]` attributes (full-res thumbnail frames).

### 4. Extract CTA destination URLs

Each ad card has a "Learn More" (or similar) button linking to the advertiser's landing page. Extract these for landing page analysis:

```javascript
// Run via browser evaluate — extracts CTA hrefs from ad cards
(() => {
  const ctas = [...document.querySelectorAll('a')]
    .filter(a => a.textContent.trim().match(/^(Learn More|Shop Now|Sign Up|Download|Get Offer|Book Now|Apply Now|Contact Us|Subscribe|Watch More|See More)$/i))
    .map(a => ({ text: a.textContent.trim(), url: a.href }))
    .filter(c => c.url && !c.url.includes('facebook.com/ads/library'));
  return JSON.stringify(ctas);
})()
```

These URLs can be passed to the **landing-page-analysis** skill for offer/funnel analysis.

### 5. Download assets & capture dimensions

All fbcdn.net URLs work with direct `curl` — no authentication needed. Only download what was requested.

```bash
curl -sL -o "output.jpg" "https://scontent-xxx.xx.fbcdn.net/v/..."
curl -sL -o "output.mp4" "https://video-xxx.xx.fbcdn.net/v/..."
```

### 6. Extract aspect ratios

After downloading, determine the aspect ratio of each asset:

**For images (using `sips` on macOS or `identify` from ImageMagick):**
```bash
# macOS
sips -g pixelWidth -g pixelHeight image.jpg

# Calculate ratio
width=1080; height=1350
# 1080:1350 = 4:5 (vertical feed)
```

**For videos (using `ffprobe`):**
```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 video.mp4
# Output: 1080,1920 → 9:16 (Stories/Reels)
```

**Common Meta ad aspect ratios:**
| Ratio | Dimensions | Use Case |
|-------|------------|----------|
| 1:1 | 1080×1080 | Feed (universal) |
| 4:5 | 1080×1350 | Feed (recommended, more space) |
| 9:16 | 1080×1920 | Stories, Reels |
| 16:9 | 1920×1080 | Video, landscape |
| 1.91:1 | 1200×628 | Link ads |

**Save metadata to JSON:**
```json
{
  "filename": "brand-video-01.mp4",
  "type": "video",
  "width": 1080,
  "height": 1920,
  "aspect_ratio": "9:16",
  "duration_seconds": 31
}
```

Create `{advertiser-slug}-metadata.json` alongside the assets with dimensions for each file.

### 6. Scroll for more results

The Ad Library lazy-loads ads. To get more than the initial batch (~20), scroll down and wait, then re-extract. The JS deduplicates automatically.

## Naming Convention

```
{advertiser-slug}-{type}-{nn}.{ext}
```
Examples: `hbs-online-image-01.jpg`, `iman-gadzhi-video-03.mp4`

## Delivering Assets

Send downloaded files via `message` tool with `action=send` and `filePath`. Include advertiser name and asset type in caption.

For batches: summary message first, then files one by one. Group images together, then videos.

**Telegram limits:** 50MB images / 2GB video. Most ad creatives are well under this.

## Integration with Other Skills

After extraction, use:
- **ad-creative-analysis** — Analyze each creative (video via Gemini, images via vision)
- **landing-page-analysis** — Visit + analyze the CTA destination page

## Known Limitations

- **Image resolution capped at 600×600** — server-enforced. Sufficient for reference/analysis.
- **Videos are full quality** — no resolution restriction.
- **Rate limiting** — add 1-2s delay between downloads for large batches.
- **Dynamic loading** — must scroll to load all ads; initial load shows ~20 results.
- **URL expiry** — fbcdn.net URLs contain auth tokens that expire. Download promptly.

## Reference

See `references/dom-selectors.md` for detailed CSS selectors, URL patterns, and JS extraction code.
