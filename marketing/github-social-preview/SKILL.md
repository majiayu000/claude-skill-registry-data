---
name: github-social-preview
description: Generates a professional GitHub repository social preview image sized 1280x640 pixels as a JPG under 1 MB. Always trigger immediately when the user's message starts with "gsp". Also trigger on "generate github social preview", "create repo preview image", or any request to generate a social preview or OG image for a GitHub repository.
version: 1.2.0
---

# GitHub Social Preview Skill

## Intent

Generate branded GitHub social preview images using repo metadata, visual rules, and the included preview generator.

## Do Not Use When

- Do not use for unrelated image generation, manual graphic design requests, or previews without enough repo identity context.
- Required context is missing and cannot be reasonably inferred.
- A more specific skill in this repo is a better match.

## Constraints

- Do not fabricate missing facts, measurements, dates, sources, or user context.
- Keep output aligned with Mick's direct, practical communication style unless the skill says otherwise.
- Preserve safety, legal, medical, financial, and operational boundaries stated in this file.
- Prefer concise, usable output over broad explanation.

## Validation Checklist

- [ ] The output matches the skill's intended task and platform.
- [ ] Required inputs, assumptions, and uncertainty are explicit.
- [ ] Safety, scope, and source limits are respected.
- [ ] The response follows the requested format or the skill's default output format.
- [ ] The result is practical enough to use without another cleanup pass.

Generate a clean, professional 1280x640 social preview image for any GitHub repository and export it as a JPG under 1 MB.

## Primary Triggers

Use this skill when the user starts with `gsp`, or asks to create a social preview or Open Graph image for a GitHub repository.

```text
gsp <repo_url>
generate github social preview <repo_url>
create repo preview image <repo_url>
make social preview for <repo_url>
og image for <repo_url>
```

## Expected Inputs

- A GitHub repository URL (required)
- Optionally: a custom tagline, theme preset, accent color, layout hint, logo, screenshot, or background art

## Expected Outputs

- File: `github-social-preview.jpg`
- Size: exactly 1280x640 pixels
- Format: JPEG
- File size: under 1 MB (auto-recompressed if needed)

## Workflow

### Step 1 — Fetch repository metadata

Using the GitHub URL, retrieve:

1. Repository name (from URL path)
2. Repository description (from GitHub page or API)
3. README content (for fallback description and keyword extraction)
4. Topics / tags (from GitHub topics)
5. Primary programming language
6. Owner or organization name

Use the `WebFetch` tool to read the GitHub repository page. Parse the HTML or JSON response for description, topics, and language. If a raw README is needed, fetch `https://raw.githubusercontent.com/<owner>/<repo>/main/README.md` (try `master` if `main` returns 404).

### Step 2 — Derive display content

Build the four visual elements from the metadata gathered:

| Element | Source | Fallback |
| --- | --- | --- |
| Title | Repository name, formatted (replace hyphens/underscores with spaces, title case) | Raw repo name |
| Subtitle | Repository description | First sentence of README |
| Tags | Topics list (up to 5 tags) | Top keywords extracted from README or repo name tokens |
| Language badge | Primary language | Omit if unknown |

If no description, README, or topics exist, generate a minimal clean design with the title only.

### Step 3 — Generate the image

Run `scripts/generate_preview.py` with the derived content as arguments. The script:

1. Creates a 1280x640 canvas with the configured background gradient
2. Applies a theme preset or accent override when requested
3. Optionally places a repo logo, screenshot, or background art when the assets are available
4. Renders the GitHub-style Octicon logo mark in the top-left corner
5. Fits or truncates long title, subtitle, and tag text cleanly
6. Renders the title as the dominant H1 text
7. Renders the subtitle as a smaller H2 line below the title
8. Renders tag pills at the bottom
9. Renders the language badge bottom-right if known
10. Exports as JPEG at quality 92

### Step 4 — Enforce size constraint

After generation, check the output file size.

- If under 1 MB: done
- If 1 MB or larger: re-run export at progressively lower JPEG quality (85, 75, 65, 55) until the file is under 1 MB
- If still over 1 MB at quality 55: scale the canvas to 90% and retry from quality 92

### Step 5 — Confirm output

Report back:

- Full path to `github-social-preview.jpg`
- Final file size
- JPEG quality used
- Any fallbacks applied (missing description, missing topics, etc.)
- Preview checklist results for contrast, crop safety, and file size

### Step 6 — Local preview checklist

Before finalizing the output, verify:

- title contrast is strong enough against the background
- subtitle contrast is still readable
- key content stays inside a safe crop zone
- final file size is under 1 MB

If one of these fails, adjust theme, accent, text length, or asset placement and regenerate.

## Design Specification

See `templates/design_config.json` for the full color, font, and layout specification.

Summary:

- Background: dark gradient (#0d1117 to #161b22), GitHub dark theme
- Title: white, bold, 72pt equivalent
- Subtitle: muted gray (#8b949e), 36pt equivalent
- Tag pills: rounded rectangles, #21262d fill, #30363d border, #58a6ff text
- Language badge: colored dot + label, bottom-right
- GitHub mark: top-left, low-opacity white watermark
- No decorative clutter, no gradients on text, no drop shadows

Theme presets now include:

- `github-dark`
- `docs-blue`
- `builder-green`
- `launch-warm`

## Accent Color Selection

When the user does not specify a theme or accent, derive the accent from the repo's primary language so previews are recognizable at a glance:

| Language | Accent |
| --- | --- |
| PowerShell | #012456 deep blue |
| Python | #3776ab blue |
| JavaScript / TypeScript | #f1e05a yellow / #3178c6 blue |
| C# / .NET | #512bd4 purple |
| Go | #00add8 cyan |
| Rust | #dea584 amber |
| Shell | #89e051 green |

A user-provided accent or theme always wins over the language mapping. When the user mentions a brand color or pastes a hex value, use it directly and check title contrast against it.

## Layout Variants

Pick the layout emphasis from what the repo is:

- `library or toolkit` (default): title dominant, subtitle, tag pills, language badge
- `docs repo`: subtitle gets more weight since the description is the value; fewer tags, no language badge
- `app or product`: screenshot placement preferred when one is available, title moves to the left column

Infer the variant from topics and README signals, and say which variant was used in the confirmation output.

## Batch Mode

When the user provides multiple repo URLs (`gsp url1 url2 ...` or a pasted list):

- process each repo through the full workflow, reusing one theme across the set unless told otherwise so the previews look like a family
- name outputs `github-social-preview-<repo>.jpg` instead of overwriting the default filename
- report one summary table at the end: repo, file, size, quality, fallbacks applied
- if one repo fails to fetch, continue the batch and report the failure rather than stopping

## Fallback Behavior

| Condition | Behavior |
| --- | --- |
| No repository description | Use first non-heading sentence from README |
| README missing or too short | Infer from repo name tokens and topics |
| No topics | Extract top 3-5 keywords from README headings or repo name |
| No language detected | Omit language badge entirely |
| No metadata at all | Render title-only design with GitHub mark |
| Image over 1 MB after quality 55 | Scale canvas to 90% and retry |
| Long repo or tag text | Fit to width first, then truncate with ellipsis only if needed |
| Logo or screenshot available | Add them only if they improve the layout without crowding the text |

## Limitations

- Requires Python 3 with Pillow installed (`pip install Pillow`)
- Font rendering depends on system fonts; the script falls back to Pillow's built-in font if no system font is found
- Does not authenticate with the GitHub API; rate limits on public pages may apply
- Topics are not always visible without authentication; the script falls back to README keywords if the topics section is empty
- JPEG compression removes alpha channel; transparency is not supported in the output format
- The generated image is saved to the current working directory as `github-social-preview.jpg`

## Script Reference

```text
scripts/generate_preview.py   — Main image generation and compression script
templates/design_config.json  — Color, font, and layout configuration
examples/example_usage.md     — Worked examples with sample outputs described
```

## Help And Examples

If the user is not sure how to use this skill, asks what it needs, or asks for examples:

- Explain in plain language what this skill can do.
- Tell the user the minimum input needed for a useful first pass.
- Show the example prompts below.
- Offer the fastest next prompt the user can send.

Minimum useful input:

- A GitHub repository URL. Theme or tagline is optional.

Example prompts:

- `gsp https://github.com/microsoft/winget-cli`
- `Use github-social-preview to create a social preview image for this repo with a builder-green theme.`
- `Show me an example prompt for generating an OG image from a GitHub repository URL.`

