---
name: stock-images
description: Search and download stock photos from Pexels, Unsplash, and Pixabay for projects, landing pages, UI mockups, and content. Use when users explicitly ask to find stock photos, need a hero/profile/content image, or want to download a selected stock image.
---

## Security Rules

- NEVER display API keys in your output
- NEVER echo full curl commands that contain API keys
- **Pixabay limitation**: Pixabay requires the API key as a URL query parameter, which is visible in process lists (`ps aux`). Be aware of this inherent API limitation. Never display the full Pixabay curl command in output.
- Only download from allowed domains:
  - `images.pexels.com`
  - `images.unsplash.com`, `plus.unsplash.com`
  - `pixabay.com`, `cdn.pixabay.com`
- All URLs MUST use HTTPS
- After downloading, check file size — alert if > 10MB
- For Unsplash downloads, use the `links.download` URL (not `urls.raw`) to comply with Unsplash API TOS (triggers download count)

## Non-Activation

Do NOT activate this skill when:
- Discussing image components (`<img>`, `next/image`, etc.)
- AI image generation is requested (that is a different skill)
- Referencing existing images already in the project

## Setup Detection

Before searching, check if API keys are configured:

```bash
test -f ~/.config/stock-images/keys.json && stat -f "%Lp" ~/.config/stock-images/keys.json 2>/dev/null || stat -c "%a" ~/.config/stock-images/keys.json 2>/dev/null
```

- If the file does not exist: guide the user interactively through setup:
  1. Ask which providers they want to use (Pexels, Unsplash, Pixabay — all free)
  2. Provide the relevant signup links:
     - Pexels: https://www.pexels.com/api/
     - Unsplash: https://unsplash.com/developers
     - Pixabay: https://pixabay.com/api/docs/
  3. Once the user provides their keys, create the config file via Bash with `chmod 600`
  4. NEVER display the keys back after saving
- If permissions are not `600`: warn the user and offer to fix with `chmod 600 ~/.config/stock-images/keys.json`.
- If the file exists with correct permissions: use the keys silently. Do NOT display the file contents, the keys, or commands containing key values.

Determine configured providers without printing secret values:

```bash
python3 - <<'PY'
import json
from pathlib import Path

config = Path.home() / ".config" / "stock-images" / "keys.json"
data = json.loads(config.read_text())
providers = [
    name for name in ("pexels", "unsplash", "pixabay")
    if data.get(name) and not str(data[name]).startswith("YOUR_")
]
print("\n".join(providers))
PY
```

Parse the JSON to determine which providers are configured (have non-empty, non-placeholder values). At least one provider is required.

## Search Implementation

Extract from the user's request:
- **query**: what to search for (required)
- **count**: how many images (default: 5, max: 20)
- **orientation**: landscape, portrait, or square — infer from context (e.g., "hero banner" → landscape, "profile photo" → portrait)
- **provider**: specific provider or "all" (default: all configured)

Keep the parsed search results and metadata available for follow-up requests in the same conversation. If the user later says "download image #3", map that number back to the exact provider, image URL, download URL, author, author profile, and attribution data from the presented results.

Run curl commands for each configured provider. When multiple providers are configured, run them in parallel (separate Bash tool calls).

### Pexels

```bash
curl -sS -G --max-time 15 --fail "https://api.pexels.com/v1/search" \
  --data-urlencode "query=SEARCH_QUERY" \
  -d "per_page=COUNT" \
  -d "orientation=ORIENTATION" \
  -H "Authorization: PEXELS_KEY"
```

Response fields:
- `photos[].src.original` — full image URL
- `photos[].src.medium` — thumbnail
- `photos[].photographer` — author name
- `photos[].photographer_url` — author profile
- `photos[].width`, `photos[].height` — dimensions

### Unsplash

```bash
curl -sS -G --max-time 15 --fail "https://api.unsplash.com/search/photos" \
  --data-urlencode "query=SEARCH_QUERY" \
  -d "per_page=COUNT" \
  -d "orientation=ORIENTATION" \
  -H "Authorization: Client-ID UNSPLASH_KEY"
```

Response fields:
- `results[].urls.raw` — full image URL
- `results[].urls.small` — thumbnail
- `results[].user.name` — author name
- `results[].user.links.html` — author profile
- `results[].links.download` — download URL (use this for downloads, not urls.raw)
- `results[].width`, `results[].height` — dimensions

### Pixabay

```bash
curl -sS -G --max-time 15 --fail "https://pixabay.com/api/" \
  -d "key=PIXABAY_KEY" \
  --data-urlencode "q=SEARCH_QUERY" \
  -d "per_page=COUNT" \
  -d "orientation=ORIENTATION" \
  -d "image_type=photo"
```

Pixabay-specific: map "landscape" → "horizontal", "portrait" → "vertical". Minimum per_page is 3.

Response fields:
- `hits[].largeImageURL` — full image URL
- `hits[].previewURL` — thumbnail
- `hits[].user` — author name
- `hits[].user_id` — for building profile URL: `https://pixabay.com/users/USER-USER_ID/`
- `hits[].imageWidth`, `hits[].imageHeight` — dimensions
- `hits[].tags` — description

### Error Handling

- **curl exits non-zero / timeout**: skip that provider, continue with others, inform user
- **HTTP 401**: API key invalid or revoked — inform user, suggest re-running setup
- **HTTP 429**: rate limit — inform user, suggest waiting or trying another provider
- **Empty / malformed JSON**: skip provider, continue with others
- **Malformed keys.json**: inform user config is corrupted, offer to recreate

### Presenting Results

Present results in the user's language. Format:

```
## Results for "query" (N images)

### Provider Name
1. "Image Title/Description" — by [Author Name](author_profile_url)
   URL: https://...
   Resolution: WxH
```

After presenting, ask if the user wants to download any of them.

## Download Implementation

When the user selects an image to download:

1. **Validate the URL**: must start with `https://` and match an allowed domain
2. **Unsplash special case**: use the `links.download` URL from search results instead of `urls.raw` to comply with Unsplash API TOS (this triggers their download counter)
3. **Determine destination**: default `./images/` in current project directory. Ask for confirmation if the directory doesn't exist before creating it.
4. **Generate filename**: `<query-slug>-<provider>.<ext>` (e.g., `mountain-landscape-pexels.jpg`). Default extension is `.jpg` unless the URL clearly indicates otherwise (`.png`, `.webp`).
5. **Download**:

```bash
curl -sL --max-time 30 --fail -o "./images/FILENAME" "IMAGE_URL"
```

6. **Verify**: check file size and confirm to user

```bash
ls -lh "./images/FILENAME"
```

7. **Attribution reminder**: after download, remind the user:
   > Attribution required: `Photo by [Author](author_url) on [Provider]`

Alert if file size > 10MB — the user may want a smaller resolution.

Attribution and license requirements vary by provider and project use. Always preserve and present author attribution metadata so the user can comply with the relevant provider terms.

## Behavior Guidelines

- Infer orientation from context: "hero", "banner", "header" → landscape; "avatar", "profile" → portrait; "thumbnail", "icon" → square
- When the user is working on a UI component and mentions needing an image, proactively offer to search stock images
- Always present author attribution — Unsplash and Pixabay TOS require it
- Respond in the user's language
- If no results found, suggest alternative search terms
- If only one provider is configured, skip the provider selection and use it directly
