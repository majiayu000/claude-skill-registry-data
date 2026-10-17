---
name: cc-design-html-prototyping
description: High-fidelity HTML design and prototype guidance for AI agents with structured design thinking and quality guardrails
triggers:
  - "design a landing page"
  - "create a slide deck"
  - "build an interactive prototype"
  - "make an interactive explainer"
  - "design with [brand name] style"
  - "create an animated design"
  - "export design as PDF/PPTX"
  - "review this design"
---

# cc-design HTML Prototyping

> Skill by [ara.so](https://ara.so) — Design Skills collection.

High-fidelity HTML design and prototyping system for Claude Code and Codex. Creates landing pages, slide decks, interactive prototypes, explainers, animations, and design systems with structured design thinking, quality guardrails, and automatic verification.

## Installation

### Claude Code

```bash
/plugin marketplace add ZeroZ-lab/cc-design
/plugin install cc-design@cc-design
/reload-plugins
```

Activate with `/cc-design:design` command or `/design` shorthand.

### Codex

```bash
/plugin marketplace add ZeroZ-lab/cc-design
/plugin install cc-design@cc-design
/reload-plugins
```

Reference with `$cc-design` in prompts.

### Optional Dependencies

```bash
# For screenshot verification and export
npx playwright install chromium

# For video/audio export
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows
choco install ffmpeg
```

## Core Workflow

The 8-stage workflow guarantees quality:

```
Understand → Route → Plan → Approve → Build → Verify → Deliver
```

**Key behavioral guarantees:**
- Never builds without approved plan
- Never delivers without screenshot verification
- Blocks AI slop patterns (banned gradients, emoji spam)
- Follow-ups skip full discovery

## Output Types

### Landing Pages

```
"Design a SaaS landing page with Stripe's aesthetic"
"Create a product page mixing Vercel minimalism with Linear purple accents"
```

### Slide Decks

```
"Create a 10-slide pitch deck for Q3 board meeting"
"Make a presentation deck with Pentagram style"
"Export deck as editable PPTX"
```

### Interactive Prototypes

```
"Build an interactive prototype of the checkout flow"
"Notion-style kanban board with iOS device frame"
"Create a prototype with macOS window chrome"
```

### Interactive Explainers

```
"Create a flow explainer showing our RAG pipeline"
"Make a comparison explainer for React vs Vue"
"Build a decision tree for tech stack selection"
```

### Animations

```
"Animate this logo reveal with Pentagram style"
"Create a motion study for the hero section"
```

## Design Philosophy

Invoke specific schools for direction:

```
"Use Pentagram style for this infographic"
"Apply Experimental Jetset minimalism"
"Mix Takram restraint with Locomotive motion"
```

**20 philosophy schools across 5 traditions:**
- Information Architects (Pentagram, Wolff Olins, etc.)
- Motion Poets (Locomotive, Active Theory, etc.)
- Minimalists (Experimental Jetset, Base Design, etc.)
- Experimental Vanguard (Studio Dumbar, etc.)
- Eastern Philosophy (Kenya Hara, Nendo, etc.)

Full reference: `references/design-styles.md`

## Brand Style Cloning

Load design systems from 68+ brands:

```
"Create pricing page with Stripe's aesthetic"
"Notion-style interface"
"Mix Vercel and Linear styles"
```

Supported brands include: Stripe, Vercel, Linear, Notion, Apple, Tesla, Spotify, Airbnb, etc.

Full catalog: `references/brand-library.md`

## Code Patterns

### Design Framework (8 Layers)

Every design follows this structure:

```javascript
// Layer 1: Goal (outcomes, constraints, target)
const goal = {
  outcome: "Convert visitors to trial signups",
  constraints: ["Mobile-first", "< 3s load"],
  target: "B2B SaaS founders"
};

// Layer 2: Facts (truth, not assumptions)
const facts = {
  brand: "Existing logo, no guidelines",
  content: "5 feature sections + pricing",
  technical: "Static HTML, no backend"
};

// Layer 3: Assumptions (testable hypotheses)
const assumptions = {
  users: "Prefer minimalist design",
  behavior: "Will scroll 3 viewports max",
  context: "Desktop research, mobile signup"
};

// Layers 4-8: Strategy, Structure, Skeleton, Surface, Validation
```

### Quality Guardrails

Built-in anti-slop rules:

```javascript
// BANNED patterns
const slopPatterns = {
  gradients: [
    "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    "linear-gradient(to right, #ff6b6b, #4ecdc4)"
  ],
  layouts: [
    "50/50 hero split with form",
    "Centered hero with 3-column features"
  ],
  text: [
    "Empower your", "Unlock the power",
    "Revolutionary", "Game-changing"
  ]
};

// REQUIRED quality checks
const qualityRules = {
  typography: "System font stack or single web font only",
  spacing: "8px scale (8, 16, 24, 32, 48, 64, 96)",
  verification: "Screenshot required before delivery",
  contrast: "WCAG AA minimum (4.5:1 text, 3:1 UI)"
};
```

### Typography System

```css
/* System font stack pattern */
:root {
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", 
               Roboto, sans-serif;
  --font-mono: "SF Mono", Monaco, Consolas, monospace;
}

/* Type scale (major third: 1.25) */
:root {
  --text-xs: 0.64rem;   /* 10px */
  --text-sm: 0.8rem;    /* 13px */
  --text-base: 1rem;    /* 16px */
  --text-lg: 1.25rem;   /* 20px */
  --text-xl: 1.563rem;  /* 25px */
  --text-2xl: 1.953rem; /* 31px */
  --text-3xl: 2.441rem; /* 39px */
}
```

### Spacing Scale

```css
:root {
  --space-1: 0.25rem;  /* 4px */
  --space-2: 0.5rem;   /* 8px */
  --space-3: 0.75rem;  /* 12px */
  --space-4: 1rem;     /* 16px */
  --space-6: 1.5rem;   /* 24px */
  --space-8: 2rem;     /* 32px */
  --space-12: 3rem;    /* 48px */
  --space-16: 4rem;    /* 64px */
  --space-24: 6rem;    /* 96px */
}
```

### Animation System

Stage+Sprite timeline engine:

```javascript
// Stage: timeline controller
const stage = {
  duration: 2000,
  sprites: ['logo', 'title', 'cta'],
  timeline: [
    { at: 0, sprite: 'logo', action: 'fadeIn' },
    { at: 500, sprite: 'title', action: 'slideUp' },
    { at: 1200, sprite: 'cta', action: 'scale' }
  ]
};

// Sprite: animated element
const sprite = {
  id: 'logo',
  el: document.querySelector('.logo'),
  keyframes: [
    { opacity: 0, transform: 'scale(0.8)' },
    { opacity: 1, transform: 'scale(1)' }
  ],
  timing: {
    duration: 600,
    easing: 'cubic-bezier(0.34, 1.56, 0.64, 1)' // easeOutBack
  }
};
```

### React Prototyping

Inline JSX with Babel transpilation:

```html
<!DOCTYPE html>
<html>
<head>
  <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
  <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
</head>
<body>
  <div id="root"></div>
  
  <script type="text/babel">
    const { useState } = React;
    
    function KanbanBoard() {
      const [tasks, setTasks] = useState([
        { id: 1, text: 'Design review', column: 'todo' },
        { id: 2, text: 'Build prototype', column: 'doing' }
      ]);
      
      const moveTask = (id, newColumn) => {
        setTasks(tasks.map(t => 
          t.id === id ? { ...t, column: newColumn } : t
        ));
      };
      
      return (
        <div className="board">
          {['todo', 'doing', 'done'].map(col => (
            <Column key={col} name={col} tasks={tasks.filter(t => t.column === col)} onMove={moveTask} />
          ))}
        </div>
      );
    }
    
    ReactDOM.render(<KanbanBoard />, document.getElementById('root'));
  </script>
</body>
</html>
```

### Device Frames

```javascript
// iOS frame
const iOSFrame = {
  width: 390,
  height: 844,
  chrome: {
    statusBar: 47,
    homeIndicator: 34,
    notch: true
  }
};

// macOS window frame
const macOSFrame = {
  width: 1280,
  height: 800,
  chrome: {
    titleBar: 40,
    trafficLights: { x: 12, y: 16 },
    shadow: true
  }
};
```

## Export Formats

### PDF Export

```javascript
// Multi-file PDF (one per page)
const pdfExport = {
  format: 'multi',
  files: ['page-1.pdf', 'page-2.pdf'],
  dimensions: { width: 1920, height: 1080 }
};

// Single-file PDF (all pages)
const pdfBundle = {
  format: 'single',
  file: 'deck.pdf',
  pages: 10
};
```

### PPTX Export

```javascript
// Image-based PPTX (fastest)
const pptxImage = {
  format: 'image',
  slides: 10,
  resolution: '1920x1080'
};

// Editable PPTX (structured text)
const pptxEditable = {
  format: 'editable',
  slides: 10,
  preserveFormatting: true
};
```

### Video Export

```javascript
// MP4 with dual-track audio
const videoExport = {
  format: 'mp4',
  duration: 30000, // ms
  tracks: {
    sfx: 'effects.mp3',
    bgm: 'background.mp3'
  },
  mixing: {
    sfxVolume: 1.0,
    bgmVolume: 0.3
  }
};
```

## Configuration

### Plugin Hooks

Lifecycle hooks fire automatically (opt-out with env vars):

```bash
# Disable individual hooks
export CCDESIGN_HOOK_SESSION_START=off
export CCDESIGN_HOOK_PRE_COMPACT=off
export CCDESIGN_HOOK_STOP=off
```

**SessionStart**: Auto update check + design context recovery  
**PreCompact**: Preserves design tokens to `.claude/design-context.json`  
**Stop**: Cleans stale `.playwright-mcp/console-*.log` files (>7 days)

Hook logs: `.claude/hook-log.txt`

### Design Context Recovery

Design tokens persist across sessions:

```json
{
  "colors": {
    "primary": "#0066FF",
    "surface": "#FFFFFF"
  },
  "fonts": {
    "sans": "Inter, sans-serif"
  },
  "cssVars": {
    "--space-base": "16px",
    "--radius": "8px"
  },
  "timestamp": "2026-05-16T12:00:00Z"
}
```

## Design Review

5-dimension scoring system:

```javascript
const reviewDimensions = {
  philosophy: {
    score: 8.5,
    criteria: "Coherent application of stated school",
    feedback: "Strong Pentagram geometric rigor"
  },
  hierarchy: {
    score: 9.0,
    criteria: "Visual priority matches content priority",
    feedback: "Clear focal points, effective contrast"
  },
  craft: {
    score: 7.5,
    criteria: "Typography, spacing, alignment precision",
    feedback: "Minor spacing inconsistency in footer"
  },
  functionality: {
    score: 8.0,
    criteria: "Interaction clarity, mobile responsiveness",
    feedback: "Smooth transitions, good touch targets"
  },
  originality: {
    score: 6.5,
    criteria: "Avoids clichés, brings fresh perspective",
    feedback: "Layout feels familiar, could push boundaries"
  }
};
```

## Common Patterns

### Progressive Brand Loading

```javascript
// Start minimal, load progressively
const brandLoad = {
  phase1: "Typography + color palette",
  phase2: "Spacing + component patterns",
  phase3: "Motion + interaction details",
  source: "https://getdesign.md/brands/{brand-name}.md"
};
```

### Section-by-Section Preview

```javascript
// Build incrementally with approval gates
const buildPattern = {
  sections: ['hero', 'features', 'pricing', 'footer'],
  flow: [
    { section: 'hero', status: 'preview', action: 'approve/revise' },
    { section: 'features', status: 'waiting', action: null },
    // ... continues after approval
  ]
};
```

### Verification Protocol

```javascript
// Three-phase self-check before delivery
const verification = {
  structural: [
    "All links functional",
    "Forms submit correctly",
    "No console errors"
  ],
  visual: [
    "Screenshot matches design intent",
    "Responsive breakpoints work",
    "Animations render smoothly"
  ],
  excellence: [
    "No banned slop patterns",
    "Typography system applied",
    "Spacing scale consistent"
  ]
};
```

## Troubleshooting

### Playwright Issues

```bash
# Reinstall browser
npx playwright install chromium

# Check browser path
npx playwright install --dry-run

# Permissions error
sudo npx playwright install chromium
```

### FFmpeg Not Found

```bash
# Verify installation
ffmpeg -version

# Check PATH
which ffmpeg  # macOS/Linux
where ffmpeg  # Windows

# Reinstall if missing
brew reinstall ffmpeg  # macOS
```

### Design Context Not Persisting

```bash
# Check hook status
cat .claude/hook-log.txt

# Verify context file
cat .claude/design-context.json

# Re-enable PreCompact hook
export CCDESIGN_HOOK_PRE_COMPACT=on
```

### Export Fails

```javascript
// Check dependencies
const deps = {
  pdf: "Playwright required",
  pptx: "Playwright + node-pptx",
  video: "Playwright + ffmpeg"
};

// Verify file permissions
// Output dir: .claude/exports/
// Must be writable
```

### Brand Style Not Loading

```javascript
// Progressive load may take 2-3 turns
// Check load manifest
const manifest = require('./load-manifest.json');
// Verify brand exists in references/brand-library.md

// Manual load if needed
"Load the Stripe design system from getdesign.md"
```

### Slow Performance

```javascript
// Reduce scope
const optimization = {
  sections: "Build 2-3 key sections first",
  animations: "Simplify timeline, reduce sprites",
  assets: "Use system fonts, limit external resources"
};
```

## Reference Files

Key documentation in `references/`:
- `workflow.md` - 8-stage design process
- `design-styles.md` - 20 philosophy schools
- `brand-library.md` - 68+ brand systems
- `animation-system.md` - Stage+Sprite engine
- `export-formats.md` - PDF/PPTX/MP4 specs
- `quality-rules.md` - Anti-slop guardrails

## Version

Current: v0.5.0

Check for updates: Automatic on session start (if `CCDESIGN_HOOK_SESSION_START` enabled)
