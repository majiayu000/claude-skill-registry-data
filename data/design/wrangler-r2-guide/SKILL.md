---
name: Wrangler R2 Guide
description: Manage Cloudflare R2 object storage for file hosting using Wrangler CLI. Use when uploading files to R2, managing buckets, configuring public access, or when user mentions "R2", "Wrangler", "upload to cloud", or "image hosting".
---

# Wrangler R2 Guide

Manage Cloudflare R2 object storage using the Wrangler CLI. R2 provides S3-compatible storage with zero egress fees.

## Prerequisites

```bash
# Install Wrangler CLI
npm install -g wrangler

# Authenticate
wrangler login

# Verify authentication
wrangler whoami
```

## Bucket Operations

### List Buckets
```bash
wrangler r2 bucket list
```

### Create Bucket
```bash
wrangler r2 bucket create bucket-name
```

### Get Bucket Info
```bash
wrangler r2 bucket info bucket-name
```

### Delete Bucket
```bash
wrangler r2 bucket delete bucket-name
```

## Object Operations

**IMPORTANT:** By default, Wrangler uses local development storage. Use `--remote` flag for cloud operations.

### Upload File
```bash
# Upload to remote (production)
wrangler r2 object put bucket-name/path/to/file.png --file=local/file.png --remote

# Upload with content type
wrangler r2 object put bucket-name/image.jpg --file=image.jpg --content-type=image/jpeg --remote
```

### Bulk Upload
```bash
# Upload all PNG files
for file in *.png; do
  wrangler r2 object put "bucket-name/images/$file" --file="$file" --remote
done
```

### Download File
```bash
wrangler r2 object get bucket-name/path/to/file.png --file=downloaded.png --remote
```

### Delete File
```bash
wrangler r2 object delete bucket-name/path/to/file.png --remote
```

## Public Access Configuration

### Enable Public URL (r2.dev subdomain)
```bash
wrangler r2 bucket dev-url enable bucket-name -y
```

### Check Public URL Status
```bash
wrangler r2 bucket dev-url get bucket-name
```

Example output:
```
Public access is enabled at 'https://pub-abc123.r2.dev'
```

### Disable Public URL
```bash
wrangler r2 bucket dev-url disable bucket-name
```

### Test Public Access
```bash
# Test with curl
curl -I "https://pub-abc123.r2.dev/path/to/file.png"

# Should return HTTP 200 OK with Content-Type header
```

## Custom Domain Setup

### List Custom Domains
```bash
wrangler r2 bucket domain list bucket-name
```

### Add Custom Domain
1. Add CNAME in DNS:
   ```
   assets.example.com CNAME bucket-name.r2.cloudflarestorage.com
   ```
2. Connect domain via Cloudflare Dashboard (not available via CLI in this Wrangler version)

## CORS Configuration

### List CORS Rules
```bash
wrangler r2 bucket cors list bucket-name
```

### Set CORS Rules
Create `cors.json`:
```json
{
  "CORSRules": [
    {
      "AllowedOrigins": ["*"],
      "AllowedMethods": ["GET"],
      "AllowedHeaders": ["*"],
      "MaxAgeSeconds": 3600
    }
  ]
}
```

Apply CORS:
```bash
wrangler r2 bucket cors set bucket-name cors.json
```

### Delete CORS Rules
```bash
wrangler r2 bucket cors delete bucket-name
```

## Common Workflows

### Upload Images for AI Reference
```bash
cd image-directory

# Upload all images to image-refs/ path
for file in IMG_*.png; do
  echo "Uploading $file..."
  wrangler r2 object put "bucket-name/image-refs/$file" --file="$file" --remote
done

# Verify uploads
curl -I "https://pub-abc123.r2.dev/image-refs/IMG_0821.png"
```

### Replace/Update Files
```bash
# Simply re-upload to overwrite
wrangler r2 object put "bucket-name/path/file.png" --file=new-file.png --remote
```

## Troubleshooting

### "Resource location: local" Warning
**Symptom:** Upload succeeds but files not in cloud bucket

**Solution:** Add `--remote` flag to all commands:
```bash
wrangler r2 object put bucket-name/file.png --file=file.png --remote
```

### Authentication Errors
```bash
# Re-authenticate
wrangler logout
wrangler login
```

### Public URLs Return 404
**Check:**
1. Dev URL is enabled: `wrangler r2 bucket dev-url get bucket-name`
2. File path matches exactly (case-sensitive)
3. File was uploaded with `--remote` flag

### CORS Issues in Browser
**Symptom:** Browser blocks requests even though URLs work in curl

**Solution:** Configure CORS rules (see CORS Configuration section)

## Cost Considerations

**R2 Pricing (2024):**
- Storage: $0.015/GB/month
- Class A operations (write/list): $4.50/million
- Class B operations (read): $0.36/million
- Egress: FREE (major advantage)

**Example Cost (100 images, 150MB):**
- Storage: ~$0.002/month
- Operations: ~$0.01/month
- **Total: ~$0.02/month**

## Security Best Practices

1. **Separate buckets** for public vs. private assets
2. **Use dev-url for quick testing**, custom domains for production
3. **Configure CORS** only when browser access is needed
4. **Regular backups** of critical assets
5. **Monitor usage** in Cloudflare Dashboard

## Key Differences from Documentation

**This version (4.24.3) syntax:**
```bash
# Object operations
wrangler r2 object put bucket-name/path --file=file --remote
wrangler r2 object get bucket-name/path --file=output --remote
wrangler r2 object delete bucket-name/path --remote

# Bucket info
wrangler r2 bucket info bucket-name

# Dev URL
wrangler r2 bucket dev-url get bucket-name
wrangler r2 bucket dev-url enable bucket-name -y

# CORS
wrangler r2 bucket cors list bucket-name
```

**Newer versions may use different syntax** - check `wrangler r2 --help` for your version.

## Mystica Project Setup

**Bucket:** `mystica-assets`
**Public URL:** `https://pub-1f07f440a8204e199f8ad01009c67cf5.r2.dev/`
**Images Path:** `image-refs/`

**Upload images:**
```bash
cd /Users/silasrhyneer/Code/new-mystica/docs/image-refs

for file in IMG_*.png; do
  wrangler r2 object put "mystica-assets/image-refs/$file" --file="$file" --remote
done
```

**Use in scripts:**
```bash
npx tsx scripts/generate-image.ts \
  --type "Weapon" \
  --materials "fire,steel" \
  --provider gemini \
  -r "https://pub-1f07f440a8204e199f8ad01009c67cf5.r2.dev/image-refs/IMG_0821.png,https://pub-1f07f440a8204e199f8ad01009c67cf5.r2.dev/image-refs/IMG_2791.png"
```

## Related Documentation

- **Full R2 Guide:** `docs/external/r2-image-hosting.md`
- **AI Image Generation:** `.claude/skills/generate-item-image.md`
- **Cloudflare R2 Docs:** https://developers.cloudflare.com/r2/
- **Wrangler CLI Reference:** https://developers.cloudflare.com/workers/wrangler/
