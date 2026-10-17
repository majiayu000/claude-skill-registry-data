---
name: awesome-design-html
description: 115 brand-themed HTML design references for Claude Code — talk naturally ("Linear-style page", "飞书风的页面") to apply real brand tokens.
triggers:
  - "make a [brand]-style page"
  - "create a [brand] design"
  - "show me the [brand] HTML reference"
  - "design like [brand]"
  - "use [brand] design tokens"
  - "build a page inspired by [brand]"
  - "apply [brand] brand guidelines"
  - "[brand]风的页面"
---

# awesome-design-html

> Skill by [ara.so](https://ara.so) — Design Skills collection.

A Claude Code skill providing **115 brand-themed HTML design references** (93 web + 22 iOS) that work by natural language mention. No slash commands. Just say "make a Linear-style product page" or "飞书风的页面" and Claude reads the matching reference HTML with real brand tokens (colors, fonts, radius, spacing).

## What it does

- **Self-describing HTML references**: Each file is a complete, single-file HTML page with all CSS, fonts, and design tokens inline
- **Auto-loaded by brand mention**: When you mention "Stripe", "Notion", "飞书", Claude automatically references the corresponding HTML
- **Real brand fidelity**: Actual hex values, type scales, button shapes, gradients from each brand's current design system
- **Two libraries**: 
  - **Web** (93 brands): Marketing pages, hero sections, pricing tables — Linear, Stripe, Cursor, Apple, Tesla, etc.
  - **iOS** (22 apps): Mobile app mockups — Spotify, Instagram, Duolingo, ChatGPT, etc.
- **China tech showcase** (22 brands): First comprehensive set for Chinese brands — 飞书, 抖音, 阿里云, 微信, etc.

## Installation

### Method 1: AI-native install (recommended)

In any Claude Code session, paste:

```
Please install this Claude Code skill for me: https://github.com/yzfly/awesome-design-html
```

Claude clones to `~/.claude/skills/awesome-design-html` automatically.

### Method 2: Manual git clone

```bash
git clone https://github.com/yzfly/awesome-design-html.git ~/.claude/skills/awesome-design-html
```

### Method 3: Download release

Download the `.zip` from [Releases](https://github.com/yzfly/awesome-design-html/releases) and extract to `~/.claude/skills/awesome-design-html`.

## How to use

After installation, the skill is **auto-loaded**. No commands needed. Just mention a brand naturally:

```
"Make a Linear-style product page for a task manager"
"Create a Stripe-style pricing table with gradient mesh background"
"Show me a Spotify Now Playing iPhone mockup"
"Build a Cursor-style dark IDE landing page"
"Design a Duolingo-style onboarding flow with chunky 3D buttons"
"飞书风的团队协作页面"
"抖音风格的短视频界面"
```

Claude will:
1. Identify the brand mention
2. Load the corresponding HTML reference from `assets/web/design.[brand].html` or `assets/ios/design.[brand]-ios.html`
3. Extract design tokens (colors, fonts, spacing, radius)
4. Apply them to generate your requested page

## File structure

```
awesome-design-html/
├── assets/
│   ├── web/                    # 93 marketing page references
│   │   ├── design.linear.html
│   │   ├── design.stripe.html
│   │   ├── design.cursor.html
│   │   ├── design.feishu.html  # 飞书
│   │   ├── design.douyin.html  # 抖音
│   │   └── ...
│   └── ios/                    # 22 iOS app mockups
│       ├── design.spotify-ios.html
│       ├── design.chatgpt-ios.html
│       ├── design.duolingo-ios.html
│       └── ...
├── .github/
│   └── assets/
│       └── thumbnails/         # Preview images
└── README.md
```

## Key brands available

### AI flagships (15)
Claude, ChatGPT, Cursor, OpenCode, Supabase, Mistral, Cohere, ElevenLabs, Lovable, MiniMax, Ollama, Runway, Together, VoltAgent, xAI

### Premium SaaS (18)
Linear, Stripe, Notion, Vercel, Figma, Airbnb, Airtable, Cal.com, Intercom, Miro, Slack, Superhuman, Webflow, Zapier, Clay, Asana, Dropbox, GitHub

### Luxury & Auto (8)
Apple, Tesla, Ferrari, BMW, BMW M, Bugatti, Lamborghini, Renault

### iOS apps (22)
Spotify, Instagram, Duolingo, Tinder, Snapchat, WhatsApp, Apple Music, Discord, DoorDash, Hinge, Netflix, Notion, Robinhood, Starbucks, Telegram, Threads, TikTok, Uber, X/Twitter, YouTube, ChatGPT, Bluesky

### China showcase (22)
飞书 (Feishu), 抖音 (Douyin), 阿里云 (Aliyun), 微信 (WeChat), 钉钉 (DingTalk), 腾讯文档 (Tencent Docs), 小红书 (Xiaohongshu), 美团 (Meituan), 拼多多 (Pinduoduo), 滴滴 (DiDi), 哔哩哔哩 (Bilibili), 知乎 (Zhihu), 百度 (Baidu), 网易云音乐 (NetEase Music), 饿了么 (Ele.me), 京东 (JD.com), 淘宝 (Taobao), 快手 (Kuaishou), 豆瓣 (Douban), 12306, 支付宝 (Alipay), 携程 (Ctrip)

## Real usage examples

### Example 1: Linear-style task manager

```
User: "Create a Linear-style product page for a team task manager called 'FlowTask'"

Claude response will include:
- Linear's precise purple (#5E6AD2)
- Inter font stack
- Subtle grid background
- Low-contrast secondary text (#6E7191)
- Rounded buttons (6px radius)
- Clean spacing (24px grid)
```

### Example 2: Stripe pricing table

```
User: "Make a Stripe-style pricing page with three tiers"

Claude applies:
- Stripe's gradient mesh background
- System font stack
- Rounded cards (12px)
- Accent blue (#635BFF)
- Hover states with subtle lift
```

### Example 3: Spotify iOS mockup

```
User: "Show me a Spotify Now Playing screen for the song 'Blinding Lights'"

Claude generates:
- Full-screen iPhone mockup
- Spotify green (#1DB954)
- Album art with blur backdrop
- Circular playback controls
- Bottom tab bar with exact icon spacing
```

### Example 4: Chinese brand (飞书/Feishu)

```
User: "飞书风格的团队协作页面"

Claude applies:
- 飞书 primary blue (#3370FF)
- Lark Sans font (PingFang SC fallback)
- Card-based layout
- Soft shadows (0 2px 8px rgba(0,0,0,0.08))
- Rounded corners (8px)
```

## Design tokens you get

Each HTML reference includes:

### Colors
```html
<style>
  :root {
    --primary: #5E6AD2;        /* Brand primary */
    --secondary: #6E7191;      /* Text secondary */
    --background: #FFFFFF;     /* Page background */
    --surface: #F7F8FA;        /* Card/surface */
    --accent: #FF6B6B;         /* Call-to-action */
    /* ... */
  }
</style>
```

### Typography
```html
<style>
  body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    font-size: 16px;
    line-height: 1.5;
  }
  h1 { font-size: 48px; font-weight: 700; letter-spacing: -0.02em; }
  h2 { font-size: 32px; font-weight: 600; }
  /* ... */
</style>
```

### Spacing & Layout
```html
<style>
  .container { max-width: 1280px; padding: 0 24px; }
  .section { padding: 80px 0; }
  .grid { display: grid; gap: 24px; }
  /* ... */
</style>
```

### Components
```html
<button class="primary">
  <!-- Exact button radius, padding, hover states -->
</button>
<div class="card">
  <!-- Shadow, border, radius per brand -->
</div>
```

## Common patterns

### Pattern 1: Mixing multiple brands

```
"Create a landing page with Linear's navigation, Stripe's hero gradient, and Notion's content cards"
```

Claude will blend design tokens intelligently.

### Pattern 2: Customizing on top of a reference

```
"Use the Cursor design but change the primary color to orange and add a FAQ section"
```

### Pattern 3: Responsive behavior

All references include mobile-responsive CSS:

```html
<style>
  @media (max-width: 768px) {
    .hero { padding: 40px 16px; }
    h1 { font-size: 32px; }
    .grid { grid-template-columns: 1fr; }
  }
</style>
```

### Pattern 4: Direct file access (no skill)

You can also just open any HTML file directly:

1. Visit [Live Gallery](https://code.jiangshu.ai/awesome-design-html/)
2. Click any brand thumbnail
3. Save HTML file (`Cmd+S` / `Ctrl+S`)
4. Customize locally

Each file is **100% self-contained** — no external CSS, no build step.

## Troubleshooting

### Skill not loading automatically

**Check installation path:**
```bash
ls ~/.claude/skills/awesome-design-html
```

Should show:
```
README.md
assets/
.github/
```

**Reinstall if missing:**
```bash
rm -rf ~/.claude/skills/awesome-design-html
git clone https://github.com/yzfly/awesome-design-html.git ~/.claude/skills/awesome-design-html
```

### Brand not recognized

**Make sure you're using exact brand names:**
- ✅ "Linear-style page"
- ✅ "design like Stripe"
- ✅ "飞书风的页面"
- ❌ "Liner-style" (typo)
- ❌ "Stripped design" (wrong name)

**Check available brands:**
```bash
ls ~/.claude/skills/awesome-design-html/assets/web/
ls ~/.claude/skills/awesome-design-html/assets/ios/
```

File names are `design.[brand].html` — use the `[brand]` part in your prompt.

### Missing fonts or styles

All fonts are loaded via CDN in each HTML file:

```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

If fonts don't load, check network connectivity or use system fallbacks already defined:

```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

### iOS mockup looks wrong

iOS mockups use exact iPhone dimensions:

```html
<div class="iphone-frame" style="width: 375px; height: 812px; border-radius: 40px;">
  <!-- content -->
</div>
```

If proportions seem off, ensure viewport is wide enough or check for CSS overrides.

## Philosophy: Why HTML over Markdown

From the README thesis:

> **HTML is alive.** A Markdown spec saying "rounded blue button" forces you to imagine. An HTML file *is* the result — LLM and human see the same pixels.

> **One file beats a thousand lines of prose.** A 300-line HTML demo conveys color values, type ramp, motion, interaction in 30 seconds.

> **AI reads HTML natively.** Modern coding agents parse HTML directly — no translation layer needed.

This skill embodies that philosophy. Each reference is **executable documentation**. Claude doesn't read *about* Stripe's gradient mesh — it reads the gradient mesh itself, as code.

## Updates

The repository is actively maintained. New brands added regularly.

**Check latest brands:**
```bash
cd ~/.claude/skills/awesome-design-html
git pull origin main
```

**Current version:** See [Releases](https://github.com/yzfly/awesome-design-html/releases)

## Resources

- **Live Gallery**: [https://code.jiangshu.ai/awesome-design-html/](https://code.jiangshu.ai/awesome-design-html/)
- **GitHub**: [https://github.com/yzfly/awesome-design-html](https://github.com/yzfly/awesome-design-html)
- **License**: MIT
- **中文文档**: [README.zh-CN.md](https://github.com/yzfly/awesome-design-html/blob/main/README.zh-CN.md)

## Example: Complete HTML structure

Every reference follows this pattern:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Brand Name - Design Reference</title>
  
  <!-- Fonts -->
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  
  <style>
    /* Reset */
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    /* Design tokens */
    :root {
      --primary: #5E6AD2;
      --secondary: #6E7191;
      --background: #FFFFFF;
      --surface: #F7F8FA;
      --radius: 6px;
      --shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* Base styles */
    body {
      font-family: 'Inter', -apple-system, sans-serif;
      background: var(--background);
      color: #1A1A2E;
      line-height: 1.5;
    }
    
    /* Components */
    .button {
      background: var(--primary);
      color: white;
      padding: 12px 24px;
      border-radius: var(--radius);
      border: none;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s;
    }
    
    .button:hover {
      opacity: 0.9;
      transform: translateY(-1px);
    }
    
    /* Responsive */
    @media (max-width: 768px) {
      .hero { padding: 40px 16px; }
    }
  </style>
</head>
<body>
  <!-- Page content with semantic HTML -->
  <header>
    <nav><!-- Navigation --></nav>
  </header>
  
  <main>
    <section class="hero">
      <h1>Hero Headline</h1>
      <p>Subheadline text</p>
      <button class="button">Call to Action</button>
    </section>
  </main>
  
  <footer>
    <!-- Footer content -->
  </footer>
</body>
</html>
```

Open any file in `assets/web/` or `assets/ios/` to see full implementations.
