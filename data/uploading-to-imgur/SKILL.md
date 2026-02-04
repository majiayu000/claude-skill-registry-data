---
name: uploading-to-imgur
description: Upload images to Imgur via API and get shareable links. Supports anonymous upload (Client ID) and authenticated upload (Access Token). Returns detailed JSON with image URLs, delete links, dimensions, and metadata. Use when the user needs to upload images to Imgur, share images publicly, or get image hosting URLs.
---

# Uploading to Imgur

Upload images to Imgur and get shareable links with detailed metadata. Supports both anonymous and authenticated uploads.

## Quick start

### Upload a single image

```bash
python scripts/upload.py image.png
```

Returns:
- Public image URL
- Delete link (for removing the image later)
- Image metadata (size, dimensions, type)

### Upload multiple images

```bash
python scripts/upload.py photo1.png photo2.jpg photo3.gif
```

All results are returned as JSON with detailed information for each upload.

## Configuration

### Initial setup

Set your Imgur Client ID as environment variable:

```bash
export IMGUR_CLIENT_ID="your_client_id_here"
```

### Get your Client ID

See [AUTHENTICATION.md](AUTHENTICATION.md) for step-by-step guide to:
1. Register an Imgur application
2. Get your Client ID
3. (Optional) Get Access Token for authenticated uploads

**Quick link:** https://api.imgur.com/oauth2/addclient

## Upload modes

### Anonymous upload (Client ID)

Default mode. Images are not associated with your account.

```bash
export IMGUR_CLIENT_ID="your_client_id"
python scripts/upload.py image.png
```

**Pros:**
- Simple setup
- Client ID never expires
- No account management needed

**Cons:**
- Cannot manage images in your account
- Can only delete via delete link

### Authenticated upload (Access Token)

Images are uploaded to your Imgur account.

```bash
export IMGUR_ACCESS_TOKEN="your_access_token"
python scripts/upload.py image.png
```

**Pros:**
- Images appear in your Imgur account
- Manage images through Imgur web interface
- Can edit title, description, etc.

**Cons:**
- Token expires after 28 days
- More complex OAuth setup

## Output format

The script returns JSON with complete information:

```json
{
  "total": 2,
  "successful": 2,
  "failed": 0,
  "uploads": [
    {
      "original_path": "photo.png",
      "filename": "photo.png",
      "success": true,
      "upload_type": "anonymous",
      "imgur_data": {
        "id": "abc123",
        "link": "https://i.imgur.com/abc123.png",
        "delete_link": "https://imgur.com/delete/xyz789",
        "width": 1920,
        "height": 1080,
        "size": 256789,
        "type": "image/png"
      }
    }
  ]
}
```

## Advanced usage

### Save results to file

```bash
python scripts/upload.py image.png --output result.json --pretty
```

### Specify authentication

```bash
# Use specific Client ID
python scripts/upload.py image.png --client-id "your_client_id"

# Use Access Token instead
python scripts/upload.py image.png --access-token "your_token"
```

### Supported formats

- PNG (`.png`)
- JPEG (`.jpg`, `.jpeg`)
- GIF (`.gif`)
- BMP (`.bmp`)
- WebP (`.webp`)
- TIFF (`.tiff`)

## Rate limits

Imgur API limits:
- **~1,250 uploads per day**
- **~12,500 API requests per day**

Sufficient for most personal use cases.

## More information

- **Examples**: See [EXAMPLES.md](EXAMPLES.md) for common usage patterns
- **Authentication**: See [AUTHENTICATION.md](AUTHENTICATION.md) for detailed setup guide

## Scripts reference

### upload.py

Main upload script.

**Usage:**
```bash
python scripts/upload.py [OPTIONS] IMAGE [IMAGE ...]
```

**Required:**
- `IMAGE`: One or more image file paths

**Options:**
- `--client-id ID`: Imgur Client ID (or use IMGUR_CLIENT_ID env)
- `--access-token TOKEN`: Access Token for authenticated upload
- `--output FILE`: Save JSON results to file
- `--pretty`: Pretty-print JSON output
- `--help`: Show help message

**Environment variables:**
- `IMGUR_CLIENT_ID`: Client ID for anonymous upload
- `IMGUR_ACCESS_TOKEN`: Access Token for authenticated upload

**Exit codes:**
- `0`: All uploads succeeded
- `1`: One or more uploads failed

**Examples:**

Basic upload:
```bash
export IMGUR_CLIENT_ID="your_client_id"
python scripts/upload.py photo.png
```

Multiple images with output:
```bash
python scripts/upload.py img1.png img2.jpg --output results.json --pretty
```

Authenticated upload:
```bash
export IMGUR_ACCESS_TOKEN="your_token"
python scripts/upload.py photo.png
```

## Error handling

The script handles common errors gracefully:

- **File not found**: Reports which files don't exist
- **Invalid format**: Checks file extensions before upload
- **Network errors**: Reports connection issues with retry suggestions
- **Authentication errors**: Clear messages about invalid credentials
- **Rate limit exceeded**: Informs when daily limit is reached

Each failed upload includes an `error` field in the JSON output with details.

## Tips

1. **Save delete links**: You'll need them to remove images later
2. **Use environment variables**: More secure than hardcoding credentials
3. **Pretty print for debugging**: Use `--pretty` to inspect results
4. **Batch uploads**: Upload multiple images in one command for efficiency
5. **Check rate limits**: Monitor your daily usage if uploading frequently
