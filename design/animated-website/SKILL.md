---
name: animated-website
description: Turn any video into a luxury scroll-animated website with parallax effects
---

# Animated Website from Video

Turn any MP4 video into a stunning, scroll-driven animated website with parallax effects, glass morphism cards, and cinema-quality polish. One command, one HTML file, zero dependencies.

## Requirements

- **FFmpeg** installed and available in PATH
- **Python 3** (for local preview server)
- An **MP4 video file** provided by the user

## Workflow

### Step 1: Analyze the Video

Run `ffprobe` on the provided MP4 to extract:
- Total duration (seconds)
- Frame rate (fps)
- Resolution (width x height)
- Total frame count

Report these stats to the user before proceeding.

### Step 2: Extract Frames

Extract frames from the video at 2 fps (or adjust based on duration to stay under 120 frames total).

```bash
# Desktop frames (1920x1080 WebP, quality 80)
ffmpeg -i INPUT.mp4 -vf "fps=2,scale=1920:1080" -c:v libwebp -quality 80 frames/desktop_%04d.webp

# Mobile frames (960x540 WebP, quality 70)
ffmpeg -i INPUT.mp4 -vf "fps=2,scale=960:540" -c:v libwebp -quality 70 frames/mobile_%04d.webp
```

Store frames in a temporary `frames/` directory next to the output file.

### Step 3: Generate Section Content

Analyze the video context (filename, user description, or any provided brief) and generate content for **6 scroll sections**:

| Section | Purpose | Content Needed |
|---------|---------|---------------|
| **Hero** | Full-screen opening | Headline, subheadline, CTA button text |
| **Features** | Key capabilities | 3-4 feature cards with icon, title, description |
| **Stats** | Social proof / numbers | 3-4 animated stat counters with labels |
| **How It Works** | Process breakdown | 3-5 numbered steps with short descriptions |
| **Gallery** | Visual showcase | Parallax image grid with captions |
| **CTA** | Final conversion | Headline, body text, button text, button URL |

Present the draft content to the user for approval before building.

### Step 4: Build the HTML File

Generate a single self-contained HTML file with all assets base64-encoded inline:

**Scroll Animation Engine:**
- Canvas element draws frames synced to scroll position
- `requestAnimationFrame` loop for smooth playback
- Frame preloading with progress indicator
- Responsive breakpoint swaps desktop/mobile frame sets

**Visual Effects:**
- Ambient floating particles (subtle, slow-moving, low opacity)
- Film grain overlay (CSS noise animation)
- Glass morphism cards (`backdrop-filter: blur(16px)`, semi-transparent bg)
- Letter-split text animations (each character staggers in on scroll)
- Parallax gallery (layers move at different scroll speeds)
- Navigation dots fixed on the right edge (highlight active section)

**Design Tokens:**
- Background: `#0a0a0b`
- Text primary: `#ffffff`
- Text secondary: `rgba(255,255,255,0.6)`
- Accent: user-chosen or default `#D97757`
- Card bg: `rgba(255,255,255,0.05)`
- Card border: `rgba(255,255,255,0.1)`
- Font: Inter (loaded from Google Fonts) or system sans-serif fallback
- Border radius: `16px` on cards, `999px` on buttons

**Structure:**
```
- Progress bar (top, fixed)
- Navigation dots (right, fixed)
- Section 1: Hero (full viewport, canvas background)
- Section 2: Features (glass cards grid)
- Section 3: Stats (animated counters)
- Section 4: How It Works (numbered steps)
- Section 5: Gallery (parallax grid)
- Section 6: CTA (centered, large)
- Footer (minimal)
```

Save the output as `animated-site-[topic].html` in the current working directory.

### Step 5: Launch Preview

Start a local Python server and open in the default browser:

```bash
python3 -m http.server 8888 &
open http://localhost:8888/animated-site-[topic].html
```

## Customization Options

After the initial build, offer these tweaks:

| Option | What it changes |
|--------|----------------|
| **Scroll speed** | Frames per scroll pixel (default: 0.5) |
| **Accent color** | Primary highlight color (default: #D97757) |
| **Section text** | Any headline, description, or CTA copy |
| **Logo** | Add a logo image to the hero and nav |
| **Font** | Swap Inter for another Google Font |
| **Frame density** | More or fewer frames extracted (affects file size) |
| **Sections** | Add, remove, or reorder the 6 sections |

## Rules

- ALL assets must be inlined (base64 data URIs). The final HTML must work offline with zero external fetches (except optional Google Font).
- Keep total file size under 50MB. If frames push it over, reduce frame count or quality.
- Every section must be at least 100vh tall so scroll animations have room to breathe.
- Test that navigation dots correctly highlight the active section.
- Mobile responsive: stack cards vertically, use mobile frame set below 768px.
- If FFmpeg is not installed, tell the user how to install it and stop.
- Never hallucinate video content. If you cannot determine what the video is about, ask the user to describe it.
