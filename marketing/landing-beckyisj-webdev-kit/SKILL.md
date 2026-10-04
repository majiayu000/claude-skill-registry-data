---
name: landing
description: Generate a responsive tool landing page (hero, demo, features, CTA, footer) from a tool name and description. Use when launching a new tool or building a marketing page.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob
argument-hint: [tool-name-and-description]
---

# Landing Page Generator

Generate a complete, responsive landing page for a tool or app.

**Argument**: `$ARGUMENTS` is a tool name + description (e.g., "Podcast Packager — turn a podcast episode into YouTube-ready titles and thumbnails"). If not provided, ask.

## Process

### 1. Gather the essentials

Ask for (or infer from args):
- **Tool name**
- **One-line tagline** (6-10 words, what it does + who for)
- **3-5 key features** (one sentence each)
- **Primary CTA** (e.g., "Try it free", "Sign up", "Join waitlist")
- **Demo media** — video URL, screenshot, or animated GIF (optional)
- **Brand colors** — or ask if starting fresh
- **Domain** — where this will live

### 2. Choose the stack

Based on where it's going:
- **Static HTML** — single page, no framework (fastest, most portable)
- **Next.js (App Router)** — if the tool already uses Next.js
- **Vite + React** — if the project is Vite-based

Default to **static HTML** unless the user specifies otherwise.

### 3. Generate the page

**Page structure (in order):**

1. **Nav** — logo + 2-4 links (Features, Pricing, Sign in)
2. **Hero** — headline + tagline + CTA button + demo visual
3. **Social proof** — logos, testimonials, or user count (optional)
4. **Features** — 3-column grid or alternating left/right layout
5. **How it works** — 3 steps with icons or numbers
6. **FAQ** — 4-6 common questions (collapsible)
7. **Final CTA** — one big button
8. **Footer** — links, social, legal

**HTML template (static):**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Tool Name] — [Tagline]</title>
  <meta name="description" content="[One-sentence description]">
  <meta name="robots" content="index, follow, max-image-preview:large">

  <!-- OG tags -->
  <meta property="og:title" content="[Tool Name] — [Tagline]">
  <meta property="og:description" content="[Description]">
  <meta property="og:url" content="[Domain]">
  <meta property="og:image" content="[Domain]/og-image.png">
  <meta property="og:type" content="website">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="[Tool Name] — [Tagline]">
  <meta name="twitter:description" content="[Description]">
  <meta name="twitter:image" content="[Domain]/og-image.png">

  <link rel="canonical" href="[Domain]">
  <link rel="icon" href="/favicon.ico" sizes="32x32">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">

  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">

  <style>
    :root {
      --accent: #0d9488;
      --accent-hover: #0f766e;
      --bg: #fafaf9;
      --text: #1c1917;
      --muted: #78716c;
      --card: #ffffff;
      --border: #e7e5e4;
      --radius: 12px;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body {
      font-family: 'Manrope', -apple-system, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
    }

    .container { max-width: 1120px; margin: 0 auto; padding: 0 24px; }

    /* NAV */
    nav {
      padding: 20px 0;
      border-bottom: 1px solid var(--border);
      background: rgba(250, 250, 249, 0.85);
      backdrop-filter: blur(8px);
      position: sticky; top: 0; z-index: 100;
    }
    nav .container {
      display: flex; justify-content: space-between; align-items: center;
    }
    .logo {
      font-weight: 700; font-size: 18px; text-decoration: none; color: var(--text);
    }
    nav ul { display: flex; gap: 32px; list-style: none; }
    nav a { color: var(--muted); text-decoration: none; font-size: 15px; }
    nav a:hover { color: var(--text); }

    /* HERO */
    .hero {
      padding: 80px 0 100px;
      text-align: center;
    }
    .hero h1 {
      font-size: clamp(36px, 6vw, 64px);
      font-weight: 800;
      line-height: 1.05;
      letter-spacing: -0.02em;
      text-wrap: balance;
      margin-bottom: 20px;
    }
    .hero p {
      font-size: clamp(18px, 2.2vw, 22px);
      color: var(--muted);
      max-width: 620px;
      margin: 0 auto 40px;
      text-wrap: balance;
    }

    .btn {
      display: inline-block;
      padding: 14px 28px;
      background: var(--accent);
      color: white;
      text-decoration: none;
      border-radius: var(--radius);
      font-weight: 600;
      font-size: 16px;
      transition: background 0.15s, transform 0.15s;
    }
    .btn:hover { background: var(--accent-hover); transform: translateY(-1px); }
    .btn-secondary {
      background: transparent;
      color: var(--text);
      border: 1px solid var(--border);
    }
    .btn-secondary:hover { background: var(--card); }

    .hero-media {
      margin-top: 60px;
      border-radius: var(--radius);
      overflow: hidden;
      box-shadow: 0 20px 60px -10px rgba(0,0,0,0.15);
      outline: 1px solid rgba(0,0,0,0.06);
      outline-offset: -1px;
    }
    .hero-media img, .hero-media video { width: 100%; display: block; }

    /* FEATURES */
    section { padding: 80px 0; }
    section h2 {
      font-size: clamp(28px, 4vw, 40px);
      font-weight: 700;
      text-align: center;
      margin-bottom: 60px;
      text-wrap: balance;
    }
    .features {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 32px;
    }
    .feature {
      background: var(--card);
      padding: 32px;
      border-radius: var(--radius);
      border: 1px solid var(--border);
    }
    .feature-icon {
      width: 40px; height: 40px;
      background: var(--accent); color: white;
      border-radius: 8px;
      display: flex; align-items: center; justify-content: center;
      font-size: 20px;
      margin-bottom: 16px;
    }
    .feature h3 { font-size: 18px; margin-bottom: 8px; }
    .feature p { color: var(--muted); font-size: 15px; }

    /* HOW IT WORKS */
    .steps {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 32px;
    }
    .step { text-align: center; }
    .step-num {
      width: 48px; height: 48px;
      background: var(--accent); color: white;
      border-radius: 50%;
      display: flex; align-items: center; justify-content: center;
      font-weight: 700; font-size: 20px;
      margin: 0 auto 16px;
    }

    /* FAQ */
    details {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 20px 24px;
      margin-bottom: 12px;
      cursor: pointer;
    }
    summary {
      font-weight: 600;
      list-style: none;
    }
    summary::-webkit-details-marker { display: none; }
    summary::after {
      content: '+';
      float: right;
      font-size: 20px;
      color: var(--muted);
      transition: transform 0.2s;
    }
    details[open] summary::after { transform: rotate(45deg); }
    details p { margin-top: 12px; color: var(--muted); }

    /* FINAL CTA */
    .cta-band {
      background: var(--text);
      color: white;
      padding: 80px 0;
      text-align: center;
    }
    .cta-band h2 { color: white; }
    .cta-band .btn { background: var(--accent); }

    /* FOOTER */
    footer {
      padding: 40px 0;
      border-top: 1px solid var(--border);
      color: var(--muted);
      font-size: 14px;
    }
    footer .container {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 20px;
    }
    footer a { color: var(--muted); margin-left: 20px; text-decoration: none; }
    footer a:hover { color: var(--text); }

    /* RESPONSIVE */
    @media (max-width: 640px) {
      nav ul { gap: 16px; font-size: 14px; }
      section { padding: 60px 0; }
      .feature { padding: 24px; }
    }
  </style>
</head>
<body>
  <nav>
    <div class="container">
      <a href="/" class="logo">[Tool Name]</a>
      <ul>
        <li><a href="#features">Features</a></li>
        <li><a href="#how">How it works</a></li>
        <li><a href="#faq">FAQ</a></li>
      </ul>
    </div>
  </nav>

  <section class="hero">
    <div class="container">
      <h1>[Headline]</h1>
      <p>[Tagline — one sentence, who it's for and what it does]</p>
      <a href="#cta" class="btn">[Primary CTA]</a>
      <div class="hero-media">
        <!-- Demo video, image, or GIF -->
      </div>
    </div>
  </section>

  <section id="features">
    <div class="container">
      <h2>Everything you need, nothing you don't.</h2>
      <div class="features">
        <!-- Feature cards -->
      </div>
    </div>
  </section>

  <section id="how">
    <div class="container">
      <h2>How it works</h2>
      <div class="steps">
        <!-- 3 steps -->
      </div>
    </div>
  </section>

  <section id="faq">
    <div class="container" style="max-width: 720px;">
      <h2>Questions</h2>
      <!-- Details elements -->
    </div>
  </section>

  <section id="cta" class="cta-band">
    <div class="container">
      <h2>[Final CTA headline]</h2>
      <p style="margin: 20px 0 32px; color: rgba(255,255,255,0.8);">[Subtext]</p>
      <a href="#" class="btn">[CTA button]</a>
    </div>
  </section>

  <footer>
    <div class="container">
      <div>© 2026 [Tool Name]</div>
      <div>
        <a href="#">Privacy</a>
        <a href="#">Terms</a>
        <a href="#">Contact</a>
      </div>
    </div>
  </footer>
</body>
</html>
```

### 4. Fill in the content

Replace every placeholder with real content from the user's description:
- **Headline**: rewrite the tagline as a stronger, benefit-focused headline
- **Features**: one emoji icon + 2-4 word title + one sentence each
- **Steps**: "1. Paste URL", "2. We analyze", "3. Copy results" — make them verb-driven
- **FAQ**: pre-empt real objections (cost, data, setup, support)

### 5. Add referenced assets

Remind the user to add:
- `og-image.png` (use `/og-image` skill)
- `favicon.ico` + `favicon.svg` + `apple-touch-icon.png` (use `/favicon` skill)
- A demo image/video/GIF in the hero

### 6. Next.js variant

If the project is Next.js App Router, adapt:
- Place at `src/app/page.tsx`
- Convert inline styles to Tailwind classes (if Tailwind is set up) or a CSS module
- Use `metadata` export in `layout.tsx` instead of HTML head tags
- Use `next/image` for the hero media and feature icons

## Design principles
- **Text-wrap: balance** on all headlines
- **Clamp() for fluid typography** — hero headline should shrink gracefully on mobile
- **Max width ~1120px** — wider feels awkward on desktop
- **Generous vertical rhythm** — 80px between sections on desktop, 60px on mobile
- **One accent color** — don't introduce new colors in the design
- **Rounded corners consistent** — use the --radius token everywhere

## Rules
- Don't add tracking scripts, chat widgets, or analytics unless asked
- Check the hero at 375px wide before finishing
