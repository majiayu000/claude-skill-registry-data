---
name: baoyu-design-integration
description: Run Claude Design locally as an Agent Skill to produce polished UI mockups, prototypes, decks & wireframes as self-contained HTML
triggers:
  - "create a design using baoyu-design"
  - "make a prototype with claude design locally"
  - "design a UI mockup as HTML"
  - "build an interactive prototype"
  - "create a slide deck design"
  - "wireframe a mobile app interface"
  - "generate a landing page design"
  - "design a dashboard UI"
---

# baoyu-design Integration

> Skill by [ara.so](https://ara.so) — Design Skills collection.

`baoyu-design` packages **Claude Design** — the design engine behind claude.ai/design — as a portable Agent Skill. It enables local agents to produce polished UI mockups, interactive prototypes, wireframes, landing pages, dashboards, mobile apps, and slide decks as self-contained HTML files.

## What It Does

- **Full design process**: Clarifying questions → design context gathering → HTML deliverables → preview & verification
- **24 built-in skills**: Hi-fi design, interactive prototypes, wireframes, slide decks, mobile prototypes, design systems, export formats (PDF, PPTX, Figma)
- **Visual iteration loop**: Point at elements in browser preview, describe changes, agent edits source
- **Self-contained output**: All designs saved as standalone HTML in `designs/<project>/`
- **Best with Claude Opus 4.8**: Optimized for strong models but works with other capable LLMs

## Installation

### Via npx skills CLI (Recommended)

```bash
# Install into current project (auto-detects agent)
npx skills add JimLiu/baoyu-design

# Install globally for all projects
npx skills add JimLiu/baoyu-design -g

# Target specific agent
npx skills add JimLiu/baoyu-design --agent claude-code
npx skills add JimLiu/baoyu-design --agent cursor
npx skills add JimLiu/baoyu-design --agent codex
```

Installs to:
- `.claude/skills/` for Claude Code
- `.agents/skills/` for Cursor/Codex
- Add `-g` for user-level install (`~/.claude/skills/` or `~/.agents/skills/`)

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/JimLiu/baoyu-design.git

# Copy skill directory to your agent's skills folder
# For Claude Code:
cp -r baoyu-design/skills/baoyu-design ~/.claude/skills/

# For Cursor/Codex:
cp -r baoyu-design/skills/baoyu-design ~/.agents/skills/

# For project-specific install:
cp -r baoyu-design/skills/baoyu-design ./.claude/skills/
```

### Alternative: Direct URL

Paste the repository URL into your agent chat:

```
Read https://github.com/JimLiu/baoyu-design and follow its skills/baoyu-design/SKILL.md to design a settings screen for a meditation app.
```

## Skill Structure

```
skills/baoyu-design/
├── SKILL.md              # Entry point — orchestrates the design flow
├── system-prompt.md      # Design methodology & craft standards
├── references/
│   ├── claude.md         # Tool map for Claude Code
│   ├── cursor.md         # Tool map for Cursor
│   └── codex.md          # Tool map for Codex Agent
├── built-in-skills/      # 24 specialized design prompts
│   ├── hi-fi-design.md
│   ├── interactive-prototype.md
│   ├── wireframe.md
│   ├── make-deck.md
│   ├── mobile-prototype.md
│   └── ...
└── starter-components/   # Reusable scaffolds
    ├── device-frames/
    ├── deck-stage/
    ├── canvas/
    └── animation-engine/
```

## Usage Patterns

### Basic Design Request

The skill auto-activates from natural language:

```
Design 3 hi-fi variations of a settings screen for a meditation app.
```

In Claude Code, explicitly trigger with:
```
/baoyu-design design a pricing page
```

In Codex, mention when skills are available:
```
$baoyu-design create a dashboard UI
```

### With Design Context (Recommended)

Provide screenshots, design files, or codebase references for better results:

```
Design a pricing page based on this screenshot [attach image]. 
Use the brand colors and typography from the image.
```

```
Recreate the composer UI from src/components/Composer.jsx, 
then make it interactive with working state management.
```

```
Make a 10-slide deck from this PRD.md for an engineering all-hands. 
Use our brand guidelines from brand-kit.pdf.
```

### Interactive Prototype

```
Prototype a working onboarding flow with:
- Real state management
- Smooth transitions between steps
- Form validation
- Progress indicator
```

### Mobile Design

```
Wireframe a few layout ideas for a mobile expense-tracker home screen.
Show iOS and Android variations with native UI patterns.
```

### Slide Deck

```
Create a pitch deck with 12 slides covering:
1. Problem statement
2. Our solution
3. Market opportunity
4. Product demo
5. Business model
6. Team
7. Roadmap
8. Ask

Use clean, modern aesthetic with data visualizations.
```

### Design System Creation

```
Build a design system component library for our SaaS dashboard including:
- Button variants (primary, secondary, ghost, danger)
- Form inputs (text, select, checkbox, radio)
- Card layouts
- Navigation patterns
- Color palette and typography scale
```

## Preview Server

Designs are previewed over HTTP. The agent typically starts this automatically:

```bash
# Manual preview server (Python 3)
python3 -m http.server 4311 --directory designs

# Then open in browser:
# http://localhost:4311/<project>/<file>.html
```

```bash
# Alternative with Node.js
npx http-server designs -p 4311
```

## Output Structure

All deliverables are saved as self-contained HTML:

```
designs/
└── <project-name>/
    ├── index.html           # Main deliverable
    ├── variant-1.html       # Design variations
    ├── variant-2.html
    ├── variant-3.html
    ├── prototype.html       # Interactive prototype
    ├── wireframe.html       # Wireframe version
    └── deck.html            # Slide deck
```

Each HTML file is **standalone** — no external dependencies, all CSS/JS inline.

## Built-in Skills Reference

### Core Design
- `hi-fi-design` — High-fidelity UI mockups
- `interactive-prototype` — Working prototypes with state
- `wireframe` — Low-fidelity wireframes
- `frontend-aesthetic-direction` — Visual design exploration

### Decks & Presentations
- `make-deck` — Slide presentations
- `speaker-notes` — Add presenter notes

### Mobile & Motion
- `mobile-prototype` — iOS/Android app designs
- `animated-video` — Motion graphics and animations
- `sound-effects` — Audio integration

### Design Systems
- `create-design-system` — Component libraries
- `design-components` — Individual components (`.dc.html`)
- `make-tweakable` — Add live editing panel

### Export & Handoff
- `standalone-html` — Self-contained export
- `export-pdf` — PDF generation
- `export-pptx-editable` — Editable PowerPoint
- `export-pptx-screenshots` — Screenshot-based PPTX
- `send-to-figma` — Figma integration
- `send-to-canva` — Canva integration
- `handoff-to-claude-code` — Developer handoff

### AI Integration
- `gemini-image-generation` — AI-generated images
- `call-claude-from-prototypes` — Embedded AI features
- `read-pdf` — PDF content parsing

## Common Workflows

### Workflow 1: Brand-Consistent Landing Page

```
1. "Design a landing page for our SaaS product"
   → Agent asks for brand context
   
2. Provide: screenshot of existing site, logo, brand-kit.pdf
   
3. Agent produces 3 variations in designs/landing-page/
   
4. Preview at http://localhost:4311/landing-page/variant-1.html
   
5. "Make the hero section taller and add a video background"
   → Agent edits variant-1.html
   
6. "Export this as standalone HTML for deployment"
   → Agent uses standalone-html skill
```

### Workflow 2: Mobile App Prototype

```
1. "Prototype an iOS habit-tracking app with working navigation"
   
2. Agent asks about:
   - Target iOS version
   - Color scheme
   - Key features
   
3. Respond with feature list and design references
   
4. Agent produces interactive prototype with:
   - iOS device frame
   - Tab navigation
   - Modal interactions
   - State persistence
   
5. Test in browser, request refinements by pointing at elements
```

### Workflow 3: Pitch Deck Creation

```
1. "Create a 15-slide investor pitch deck from this outline.md"
   
2. Agent reads outline, asks for:
   - Company logo
   - Brand colors
   - Data for charts
   
3. Provide assets and data
   
4. Agent generates deck.html with:
   - Slide navigation
   - Presenter mode
   - Speaker notes
   
5. "Export as editable PPTX"
   → Uses export-pptx-editable skill
```

## Iteration & Refinement

The key advantage of local execution is **visual iteration**:

```
# Point at elements in browser preview
"Make that button larger"
"Change the header background to gradient"
"Add more padding around the cards"
"Use a darker shade of blue"
"Align those icons vertically"

# Agent uses browser DevTools or element annotation to identify
# the exact element, then edits the HTML source
```

This creates a tight feedback loop — you don't describe element locations, you **point** at them.

## Configuration

### Model Selection

For best results, configure your agent to use **Claude Opus 4.8**:

**Claude Code:**
```bash
# Set in ~/.claude/config.json
{
  "model": "claude-opus-4.8"
}
```

**Cursor:**
```javascript
// Settings → Features → AI Model
// Select: Claude Opus 4.8
```

**Environment Variable:**
```bash
export ANTHROPIC_MODEL="claude-opus-4.8"
```

### Custom Component Library

Add your own starter components:

```bash
# Create custom components directory
mkdir -p skills/baoyu-design/starter-components/custom/

# Add your component
cat > skills/baoyu-design/starter-components/custom/my-nav.html << 'EOF'
<!-- Your custom navigation component -->
<nav class="custom-nav">
  <!-- ... -->
</nav>
EOF
```

Reference in prompts:
```
Use the custom navigation from starter-components/custom/my-nav.html
```

### Brand Context Files

Store brand assets for reuse:

```bash
mkdir -p designs/_brand/
cp logo.svg designs/_brand/
cp brand-colors.json designs/_brand/
cp typography.css designs/_brand/
```

Reference in prompts:
```
Use brand assets from designs/_brand/
```

## Code Examples

### Example 1: Interactive Dashboard (Generated Output)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Analytics Dashboard</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { 
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: #f5f5f7;
      padding: 2rem;
    }
    .dashboard { 
      display: grid; 
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 1.5rem;
      max-width: 1400px;
      margin: 0 auto;
    }
    .card {
      background: white;
      border-radius: 12px;
      padding: 1.5rem;
      box-shadow: 0 2px 8px rgba(0,0,0,0.08);
      transition: transform 0.2s, box-shadow 0.2s;
    }
    .card:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 16px rgba(0,0,0,0.12);
    }
    .metric { font-size: 2rem; font-weight: 600; color: #1d1d1f; }
    .label { color: #86868b; font-size: 0.875rem; margin-top: 0.5rem; }
    .chart { height: 200px; margin-top: 1rem; }
  </style>
</head>
<body>
  <div class="dashboard">
    <div class="card">
      <div class="metric">$47,329</div>
      <div class="label">Revenue (MTD)</div>
      <canvas class="chart" id="revenueChart"></canvas>
    </div>
    <div class="card">
      <div class="metric">1,234</div>
      <div class="label">Active Users</div>
      <canvas class="chart" id="usersChart"></canvas>
    </div>
    <div class="card">
      <div class="metric">94.2%</div>
      <div class="label">Uptime</div>
      <canvas class="chart" id="uptimeChart"></canvas>
    </div>
  </div>
  
  <script>
    // Simple chart rendering (production would use Chart.js or similar)
    function drawLineChart(canvasId, data) {
      const canvas = document.getElementById(canvasId);
      const ctx = canvas.getContext('2d');
      const width = canvas.width = canvas.offsetWidth * 2;
      const height = canvas.height = canvas.offsetHeight * 2;
      ctx.scale(2, 2);
      
      ctx.strokeStyle = '#007AFF';
      ctx.lineWidth = 2;
      ctx.beginPath();
      data.forEach((value, i) => {
        const x = (i / (data.length - 1)) * (width / 2);
        const y = (height / 2) - (value * height / 2);
        i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
      });
      ctx.stroke();
    }
    
    drawLineChart('revenueChart', [0.3, 0.5, 0.4, 0.7, 0.6, 0.8, 0.75]);
    drawLineChart('usersChart', [0.4, 0.45, 0.5, 0.48, 0.6, 0.65, 0.7]);
    drawLineChart('uptimeChart', [0.9, 0.92, 0.95, 0.94, 0.96, 0.95, 0.97]);
  </script>
</body>
</html>
```

### Example 2: Mobile Prototype with iOS Frame

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Meditation App — Prototype</title>
  <style>
    body { 
      display: flex; 
      justify-content: center; 
      align-items: center; 
      min-height: 100vh; 
      background: #1a1a1a;
      margin: 0;
    }
    .device-frame {
      width: 390px;
      height: 844px;
      background: #000;
      border-radius: 55px;
      padding: 12px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.5);
      position: relative;
    }
    .device-frame::before {
      content: '';
      position: absolute;
      top: 0;
      left: 50%;
      transform: translateX(-50%);
      width: 150px;
      height: 30px;
      background: #000;
      border-radius: 0 0 20px 20px;
      z-index: 10;
    }
    .screen {
      width: 100%;
      height: 100%;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      border-radius: 47px;
      overflow: hidden;
      position: relative;
    }
    .app-content {
      padding: 60px 24px 24px;
      color: white;
      height: 100%;
      overflow-y: auto;
    }
    .greeting { font-size: 2rem; font-weight: 300; margin-bottom: 2rem; }
    .session-card {
      background: rgba(255,255,255,0.15);
      backdrop-filter: blur(10px);
      border-radius: 20px;
      padding: 1.5rem;
      margin-bottom: 1rem;
      cursor: pointer;
      transition: transform 0.2s;
    }
    .session-card:active { transform: scale(0.98); }
    .tab-bar {
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: 80px;
      background: rgba(0,0,0,0.3);
      backdrop-filter: blur(20px);
      display: flex;
      justify-content: space-around;
      align-items: center;
      padding-bottom: 20px;
    }
    .tab-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 4px;
      color: rgba(255,255,255,0.6);
      font-size: 0.75rem;
      cursor: pointer;
    }
    .tab-item.active { color: white; }
  </style>
</head>
<body>
  <div class="device-frame">
    <div class="screen">
      <div class="app-content">
        <div class="greeting">Good evening, Sarah</div>
        <div class="session-card">
          <div style="font-size: 1.25rem; font-weight: 500;">Sleep Meditation</div>
          <div style="opacity: 0.8; margin-top: 0.5rem;">15 min · Relaxation</div>
        </div>
        <div class="session-card">
          <div style="font-size: 1.25rem; font-weight: 500;">Anxiety Relief</div>
          <div style="opacity: 0.8; margin-top: 0.5rem;">10 min · Breathing</div>
        </div>
        <div class="session-card">
          <div style="font-size: 1.25rem; font-weight: 500;">Morning Focus</div>
          <div style="opacity: 0.8; margin-top: 0.5rem;">8 min · Energy</div>
        </div>
      </div>
      <div class="tab-bar">
        <div class="tab-item active">
          <svg width="24" height="24" fill="currentColor"><circle cx="12" cy="12" r="8"/></svg>
          <span>Home</span>
        </div>
        <div class="tab-item">
          <svg width="24" height="24" fill="currentColor"><path d="M12 2L2 7v10c0 5.5 3.8 10.7 10 12 6.2-1.3 10-6.5 10-12V7l-10-5z"/></svg>
          <span>Library</span>
        </div>
        <div class="tab-item">
          <svg width="24" height="24" fill="currentColor"><circle cx="12" cy="8" r="4"/><path d="M12 14c-4.4 0-8 1.8-8 4v2h16v-2c0-2.2-3.6-4-8-4z"/></svg>
          <span>Profile</span>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
```

### Example 3: Invoking Specific Built-in Skills

When you need a specific output type, reference the built-in skill:

```
Create a wireframe using the wireframe skill for a checkout flow with:
- Cart review
- Shipping address
- Payment method
- Order confirmation

Keep it low-fidelity, grayscale, with placeholder content.
```

```
Use the make-deck skill to create a product roadmap presentation:
- Q1 2024: Core features
- Q2 2024: Mobile apps
- Q3 2024: Enterprise features
- Q4 2024: AI integration

Include speaker notes for each slide.
```

```
Apply the mobile-prototype skill to design an Android expense tracker with:
- Bottom navigation
- FAB for adding expenses
- Material Design 3 styling
- Working category filters
```

## Troubleshooting

### Skill Not Activating

**Problem:** Agent doesn't recognize design requests.

**Solutions:**
```bash
# Verify installation
ls -la ~/.claude/skills/baoyu-design/
ls -la ~/.agents/skills/baoyu-design/

# Reinstall
npx skills add JimLiu/baoyu-design -g --force

# Explicitly trigger (Claude Code)
/baoyu-design create a dashboard

# Explicitly trigger (Codex)
$baoyu-design design a landing page
```

### Preview Server Not Starting

**Problem:** `localhost:4311` not accessible.

**Solutions:**
```bash
# Check if port is in use
lsof -i :4311

# Use different port
python3 -m http.server 8080 --directory designs
# Then update references to http://localhost:8080/

# Ensure designs/ directory exists
mkdir -p designs
```

### Output Quality Issues

**Problem:** Generated designs are low-quality or inconsistent.

**Solutions:**
1. **Use Claude Opus 4.8** — The skill is optimized for strong models
2. **Provide design context** — Screenshots, brand kits, or references dramatically improve output
3. **Be specific** — "Modern SaaS dashboard with dark mode, Tailwind aesthetic" vs "make a dashboard"
4. **Iterate visually** — Use browser preview to point at specific elements

### Missing Starter Components

**Problem:** Agent can't find device frames or templates.

**Solutions:**
```bash
# Verify starter components
ls skills/baoyu-design/starter-components/

# Re-download if missing
cd skills/baoyu-design
git pull origin main

# Or reinstall completely
npx skills add JimLiu/baoyu-design -g --force
```

### Multi-file Prototypes Not Loading

**Problem:** Prototype with external assets won't load.

**Solution:** All assets must be inline or served over HTTP:

```bash
# Don't open directly in browser (file:// protocol)
# ❌ file:///path/to/designs/project/index.html

# Do use preview server (http:// protocol)
# ✅ http://localhost:4311/project/index.html
python3 -m http.server 4311 --directory designs
```

### Agent Not Using Design Context

**Problem:** You provided screenshots/files but agent ignores them.

**Solutions:**
```
# Explicitly reference context in prompt
"Design a settings page using the colors and typography from screenshot.png"

# Attach files inline if supported
[Attach: brand-kit.pdf, logo.svg]
"Use these brand assets for a landing page design"

# Point to codebase patterns
"Match the component style from src/components/Button.tsx"
```

## Best Practices

1. **Start with context** — Provide screenshots, brand guidelines, or existing code before requesting designs
2. **Use Claude Opus 4.8** — Quality scales dramatically with model capability
3. **Iterate visually** — Point at browser preview elements instead of describing locations
4. **Export when final** — Use `standalone-html` or `export-pdf` skills for production-ready outputs
5. **Version control designs** — Commit `designs/` directory to track design iterations
6. **Organize by project** — Use descriptive folder names: `designs/landing-page/`, `designs/mobile-app/`
7. **Leverage built-in skills** — Reference specific skills (`make-deck`, `mobile-prototype`) for consistent output types

## Environment Variables

No API keys required — the skill runs within your agent's existing authentication context.

Optional configuration:

```bash
# Preferred model (if agent supports override)
export ANTHROPIC_MODEL="claude-opus-4.8"

# Custom preview port
export BAOYU_PREVIEW_PORT="4311"

# Custom designs output directory
export BAOYU_DESIGNS_DIR="./designs"
```

## Integration with Development Workflow

### Version Control

```bash
# Add designs to git
git add designs/
git commit -m "Add dashboard design variations"

# .gitignore (if you want to exclude)
echo "designs/" >> .gitignore
```

### Export for Production

```
# Generate production-ready HTML
"Export the final dashboard design as standalone HTML with minified CSS/JS"

# The agent will:
# 1. Inline all assets
# 2. Minify CSS and JavaScript
# 3. Remove comments and debug code
# 4. Output to designs/<project>/production.html
```

### Handoff to Developers

```
# Use handoff skill
"Use handoff-to-claude-code skill to prepare this prototype for development"

# Generates:
# - Annotated HTML with component boundaries
# - CSS variables for theming
# - JavaScript state structure
# - Implementation notes
```

## Resources

- **Repository**: https://github.com/JimLiu/baoyu-design
- **Documentation**: README.md in repository
- **Changelog**: CHANGELOG.md for version history
- **License**: MIT

---

**The skill auto-activates when you describe design tasks.** Just ask for what you need — the agent handles the rest.
