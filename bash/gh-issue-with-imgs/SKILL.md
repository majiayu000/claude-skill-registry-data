---
name: gh-issue-with-imgs
description: "Create GitHub issues with embedded images via CLI. Uploads images as GitHub release assets and embeds them in the issue body. Use when: (1) Creating an issue that needs screenshots, (2) Programmatically attaching images without browser UI, (3) User says 'issue with images', 'gh issue with imgs', or 'create issue with screenshots'."
user-invocable: true
argument-hint: <owner/repo> <title> --body <body> --img <path> [--img <path>...]
allowed-tools:
  - Bash
  - Read
  - Glob
---

# GitHub Issue with Images

Create GitHub issues with embedded images using release assets as image hosting.

GitHub CLI does not support attaching images to issues natively. This skill works around that by uploading images to a dedicated release, then embedding the asset URLs in the issue body markdown.

## Usage

Arguments: `<owner/repo> <title> --body <body> --img <path> [--img <path>...]`

Multiple `--img` flags supported. If no `--body`, use empty string.

## Process

### Step 1: Parse Arguments

Extract from the skill arguments:

- `owner/repo` (required) - the target repository
- Title (required) - the issue title
- `--body` (optional) - issue body text
- `--img` (one or more) - paths to image files

### Step 2: Upload Images and Get URLs

Upload all `--img` paths with the helper script — it ensures the non-draft
`_attachments` release exists (cleaning up any legacy draft release), uploads
each file under a unique name, and prints one public download URL per input
path, in order:

```bash
bash $HOME/.claude/skills/gh-issue-with-imgs/scripts/upload-to-release.sh <owner/repo> <path> [<path> ...]
```

Why a script rather than `gh release upload <file>#<name>`: the `#<name>` suffix
only sets the asset's *display label* — the asset `name` (and download URL) stays
the sanitized original basename, so same-named files collide. The script copies
each file to a unique, URL-safe temp name and uploads that, yielding a predictable
URL. Capture stdout; each line is the `browser_download_url` for the matching input.

### Step 3: Build Issue Body

Append image markdown to the body:

```markdown
<original body text>

![<filename>](<asset_url>)
```

For multiple images, add each on its own line.

### Step 4: Create the Issue

```bash
gh issue create \
  --repo <owner/repo> \
  --title "<title>" \
  --body "$(cat <<'EOF'
<constructed body with embedded images>
EOF
)"
```

Print the created issue URL.

## Notes

- The `_attachments` release is a real (non-draft) release so asset URLs are publicly accessible without authentication
- Never use `--draft` — draft release assets return 404 for unauthenticated requests (e.g., Claude API vision, curl), even though they appear to work in browsers where the user is logged in
- Asset URLs are permanent as long as the release exists
- Works for both public and private repos (private repo assets require authentication to view)
- Image size limit: same as GitHub release assets (2 GB per file)
- Supported formats: any image format (png, jpg, gif, svg, webp, etc.)
- The `scripts/upload-to-release.sh` helper is shared: the gh-fetch-issue skill reuses it to embed `/ss` screenshot placeholders into existing issues
