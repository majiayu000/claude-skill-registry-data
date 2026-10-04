---
name: poster-designer
description: Create professional posters and visual designs using AI image generation. Supports event posters, product showcases, announcements, and social media graphics. Integrates with Gemini image generation API to create visuals based on templates and user content. Use when the user wants to design posters, generate marketing visuals, create promotional materials, or produce image-based content for events, products, or announcements.
---

# Poster Designer Skill

Create professional posters and visual designs using AI image generation.

## Quick Start

Generate a poster:

```
poster create --type event --title "Summer Music Festival" --date "2026-07-15"
```

## Capabilities

- **Event Posters** — Concerts, conferences, meetups, parties
- **Product Showcases** — E-commerce listings, feature highlights
- **Announcements** — Launches, openings, special offers
- **Social Media** — Instagram, Facebook, Twitter graphics

## Usage Patterns

### Interactive Mode

Simply describe what you want:

> "Create a poster for my band's gig next Friday at the Blue Note"

The skill will ask clarifying questions and generate the poster.

### Template Mode

Use predefined templates:

- `event` — General event poster with date/time/location
- `concert` — Music-focused with band name and setlist
- `product` — Product showcase with features and pricing
- `announcement` — News/launch announcement
- `sale` — Promotional sale poster

### Custom Mode

Provide detailed specifications:

> "Create a minimalist poster, 1080x1920 (9:16), dark blue background, neon pink text, featuring a geometric guitar illustration"

## Configuration

Set your Gemini API key:

```bash
export GEMINI_API_KEY="your-api-key"
```

Or create `.env` in the skill directory by copying `.env.example`:

```bash
cp .env.example .env
# Edit .env and add your API key
```

**Security Note:** Never commit your `.env` file or share your API key. Keep it in environment variables or secure secret storage.

Get your API key from: https://makersuite.google.com/app/apikey

## Output Formats

- **PNG** — Default high-quality raster output
- **With Text Overlay** — Generated image with text composited
- **Raw + Composite** — Both the base image and final poster

## Design Principles

### Typography
- Keep text readable (minimum 24pt for important info)
- Use 2-3 fonts maximum
- Ensure high contrast between text and background

### Composition
- Follow the rule of thirds
- Leave breathing room (don't overcrowd)
- Use visual hierarchy (most important info largest)

### Color
- Use complementary or analogous color schemes
- Ensure accessibility (WCAG AA contrast minimum)
- Consider brand colors when provided

## API Integration

The skill uses Gemini image generation API with native multimodal capabilities:

- Model: `gemini-3.1-flash-image-preview` (configurable)
- Supports aspect ratios: 1:1, 4:3, 16:9, 9:16, 3:4
- Output sizes: 1K (~1024px), 2K (~2048px), 4K (~3840px)

See [references/api-docs.md](references/api-docs.md) for detailed API documentation.

## Templates

See [references/templates.md](references/templates.md) for available templates and customization options.

## Examples

### Event Poster

```
User: "Create a poster for a tech conference on May 15th"

Skill asks:
- Event name?
- Venue?
- Speaker lineup (optional)?
- Style preference (modern/minimal/bold)?

Then generates poster with:
- Compelling headline
- Date/time/venue prominently displayed
- Speaker photos or tech-themed visuals
- QR code placeholder for tickets
```

### Product Showcase

```
User: "Design a product poster for my new wireless headphones"

Skill asks:
- Product name?
- Key features?
- Price?
- Style/tone?

Then generates:
- Hero product image
- Feature callouts
- Price and CTA
- Brand-appropriate styling
```

## Error Handling

If image generation fails:
1. Retry with exponential backoff (up to 3 attempts)
2. Provide detailed error message
3. Offer to adjust prompt and retry

## Security & Safety

- All generated content follows Gemini safety guidelines
- User content is not stored persistently
- API keys are never logged or exposed
- `.env.example` is provided as a template - copy to `.env` and add your key
- Never commit `.env` files with real credentials
- Keep API keys in environment variables or secure secret storage
