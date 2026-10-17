---
name: design-dna-extractor
description: Extract and apply visual design identity as machine-readable Design DNA JSON (tokens, style, effects) from reference UIs
triggers:
  - extract design DNA from this screenshot
  - analyze the visual design system of this website
  - generate UI matching this design DNA
  - create design tokens from these references
  - turn this design into structured JSON
  - apply this design DNA to my content
  - analyze design style and effects from images
  - structure this UI's design system
---

# design-dna-extractor

> Skill by [ara.so](https://ara.so) — Design Skills collection.

An agent skill for extracting, structuring, and applying visual design identity as machine-readable "Design DNA" across three dimensions: **design tokens**, **qualitative style**, and **visual effects**.

## What It Does

**design-dna** turns reference UIs (screenshots, images, URLs) into a complete, quantified JSON specification covering:

| Dimension | Coverage |
|-----------|----------|
| **Design System** | Colors, typography, spacing, layout, shapes, elevation, motion, components |
| **Design Style** | Mood, visual language, composition, imagery, interaction feel, brand voice |
| **Visual Effects** | Canvas, WebGL, 3D, particles, shaders, scroll effects, cursor interactions, SVG animation |

The skill drives a **three-phase workflow**:

1. **Structure** — Surface the full schema and field meanings
2. **Analyze** — From references, produce complete DNA JSON (every field filled)
3. **Generate** — Given DNA JSON + content, implement the design

## Installation

### Quick Install (Recommended)

```bash
npx skills add zanwei/design-dna
```

### Install to Specific Agent

```bash
# Cursor only
npx skills add zanwei/design-dna -a cursor -g -y

# Claude Code only
npx skills add zanwei/design-dna -a claude-code -g -y
```

### Install from Local Clone

```bash
git clone https://github.com/zanwei/design-dna.git
npx skills add ./design-dna -y
```

### List Available Skills

```bash
npx skills add zanwei/design-dna --list
```

## Three-Phase Workflow

### Phase 1: Structure

**When to use:** Before analyzing references, to understand the complete schema.

**User request:**
> "Show me the Design DNA schema structure"

**Agent action:**
- Read `references/schema.md`
- Surface all available fields across design-system, design-style, and visual-effects
- Explain what each field captures

**Output:** Full field inventory with descriptions, helping you understand what will be extracted.

---

### Phase 2: Analyze

**When to use:** You have reference designs (screenshots, images, URLs) to extract DNA from.

**User request:**
> "Analyze the design DNA from this screenshot"
> "Extract design tokens from https://example.com"

**Agent action:**
- Inspect all visual properties across the three dimensions
- Fill **every field** in the DNA JSON (no empty fields)
- Note conflicts or variants across multiple references
- Output complete, quantified Design DNA JSON

**Example output structure:**

```json
{
  "design-system": {
    "color": {
      "palette": {
        "primary": ["#1a1a1a", "#333333"],
        "secondary": ["#0066cc", "#0052a3"],
        "accent": ["#ff6b35"],
        "neutral": ["#f5f5f5", "#e0e0e0", "#cccccc"],
        "semantic": {
          "success": "#10b981",
          "warning": "#f59e0b",
          "error": "#ef4444",
          "info": "#3b82f6"
        }
      },
      "roles": {
        "background": "#ffffff",
        "surface": "#f5f5f5",
        "text-primary": "#1a1a1a",
        "text-secondary": "#666666",
        "border": "#e0e0e0"
      }
    },
    "typography": {
      "font-families": {
        "primary": "Inter, system-ui, sans-serif",
        "secondary": "Georgia, serif",
        "monospace": "JetBrains Mono, monospace"
      },
      "scale": {
        "xs": "0.75rem",
        "sm": "0.875rem",
        "base": "1rem",
        "lg": "1.125rem",
        "xl": "1.25rem",
        "2xl": "1.5rem",
        "3xl": "1.875rem",
        "4xl": "2.25rem"
      },
      "weights": [400, 500, 600, 700],
      "line-heights": {
        "tight": 1.25,
        "normal": 1.5,
        "relaxed": 1.75
      },
      "letter-spacing": {
        "tight": "-0.025em",
        "normal": "0",
        "wide": "0.025em"
      }
    },
    "spacing": {
      "scale": [0, 4, 8, 12, 16, 24, 32, 48, 64, 96, 128],
      "unit": "px",
      "layout-grid": 8
    },
    "layout": {
      "grid": {
        "columns": 12,
        "gutter": 24,
        "margin": 16
      },
      "containers": {
        "sm": 640,
        "md": 768,
        "lg": 1024,
        "xl": 1280,
        "2xl": 1536
      },
      "breakpoints": {
        "mobile": 640,
        "tablet": 768,
        "desktop": 1024,
        "wide": 1280
      }
    },
    "shape": {
      "border-radius": {
        "none": 0,
        "sm": 4,
        "md": 8,
        "lg": 12,
        "xl": 16,
        "full": 9999
      },
      "border-width": [1, 2, 4],
      "border-style": "solid"
    },
    "elevation": {
      "shadows": {
        "sm": "0 1px 2px 0 rgba(0,0,0,0.05)",
        "md": "0 4px 6px -1px rgba(0,0,0,0.1)",
        "lg": "0 10px 15px -3px rgba(0,0,0,0.1)",
        "xl": "0 20px 25px -5px rgba(0,0,0,0.1)"
      },
      "z-index": {
        "dropdown": 1000,
        "modal": 2000,
        "tooltip": 3000
      }
    },
    "motion": {
      "durations": {
        "fast": 150,
        "normal": 250,
        "slow": 350
      },
      "easings": {
        "default": "cubic-bezier(0.4, 0, 0.2, 1)",
        "in": "cubic-bezier(0.4, 0, 1, 1)",
        "out": "cubic-bezier(0, 0, 0.2, 1)"
      }
    }
  },
  "design-style": {
    "mood": {
      "primary-adjectives": ["minimal", "clean", "modern"],
      "energy-level": "calm",
      "formality": "professional",
      "playfulness": "subtle"
    },
    "visual-language": {
      "aesthetic": "modernist",
      "ornamentation": "minimal",
      "symmetry": "asymmetric-balanced",
      "density": "spacious"
    },
    "composition": {
      "hierarchy-method": "scale-and-weight",
      "layout-pattern": "grid-based",
      "whitespace-philosophy": "generous",
      "alignment-preference": "left-aligned"
    },
    "imagery": {
      "photography-style": "clean-product-shots",
      "illustration-style": "none",
      "iconography": "outline-icons",
      "image-treatment": "subtle-border"
    },
    "interaction-feel": {
      "responsiveness": "immediate",
      "feedback-style": "subtle-animation",
      "hover-behavior": "color-shift",
      "transition-character": "smooth"
    },
    "brand-voice": {
      "tone": "confident",
      "personality": "authoritative",
      "copywriting-style": "concise",
      "messaging-approach": "benefit-focused"
    }
  },
  "visual-effects": {
    "canvas-webgl": {
      "used": false,
      "techniques": []
    },
    "particles": {
      "used": false
    },
    "shaders": {
      "used": false
    },
    "scroll-effects": {
      "parallax": true,
      "reveal-animations": true,
      "progress-indicators": false
    },
    "cursor-effects": {
      "custom-cursor": false,
      "hover-effects": "scale-and-shadow"
    },
    "svg-animation": {
      "used": true,
      "techniques": ["line-drawing", "morph"]
    },
    "glassmorphism": {
      "used": false
    },
    "gradients": {
      "types": ["linear"],
      "complexity": "simple"
    }
  }
}
```

**Key principles:**
- **Complete coverage** — Every field is filled; no blanks or TODOs
- **Quantified values** — Specific numbers, hex codes, font names
- **Conflict documentation** — If multiple references disagree, note variants
- **Cross-reference schema** — Use `references/schema.md` to understand field semantics

---

### Phase 3: Generate

**When to use:** You have Design DNA JSON and want to implement matching UI with your own content.

**User request:**
> "Generate a landing page using this Design DNA and my product copy"
> "Apply this design DNA to create a dashboard"

**Agent action:**
- Read `references/generation-guide.md` for implementation principles
- Apply all DNA fields (design-system, design-style, visual-effects) to your content
- Default output: self-contained HTML/CSS/JS
- Follow semantic HTML, responsive patterns, accessibility

**Example prompt:**

```
Generate a product landing page using this Design DNA:

[paste DNA JSON]

Content:
- Hero headline: "Ship faster with AI-powered code reviews"
- Subheadline: "Catch bugs before deployment"
- CTA: "Start free trial"
- Features: Speed, Accuracy, Integration
```

**Agent generates:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Product Landing</title>
  <style>
    /* Design System: Color */
    :root {
      --primary-100: #1a1a1a;
      --primary-200: #333333;
      --secondary-100: #0066cc;
      --accent-100: #ff6b35;
      --neutral-100: #f5f5f5;
      --text-primary: #1a1a1a;
      --text-secondary: #666666;
      
      /* Typography */
      --font-primary: Inter, system-ui, sans-serif;
      --font-secondary: Georgia, serif;
      
      /* Spacing */
      --space-4: 16px;
      --space-6: 24px;
      --space-8: 32px;
      --space-12: 48px;
      
      /* Shape */
      --radius-md: 8px;
      --radius-lg: 12px;
      
      /* Motion */
      --duration-normal: 250ms;
      --easing-default: cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    
    body {
      font-family: var(--font-primary);
      color: var(--text-primary);
      background: #ffffff;
      line-height: 1.5;
    }
    
    /* Design Style: Spacious composition, generous whitespace */
    .container {
      max-width: 1280px;
      margin: 0 auto;
      padding: 0 var(--space-4);
    }
    
    .hero {
      min-height: 80vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
      padding: var(--space-12) 0;
    }
    
    /* Design Style: Scale-and-weight hierarchy */
    .hero h1 {
      font-size: 3.75rem; /* 3xl+ from DNA scale */
      font-weight: 700;
      line-height: 1.25; /* tight from DNA */
      margin-bottom: var(--space-6);
      letter-spacing: -0.025em; /* tight from DNA */
    }
    
    .hero p {
      font-size: 1.5rem; /* 2xl from DNA */
      color: var(--text-secondary);
      line-height: 1.75; /* relaxed from DNA */
      margin-bottom: var(--space-8);
      max-width: 600px;
    }
    
    /* Design System: Shape, Motion, Interaction */
    .cta {
      display: inline-block;
      padding: var(--space-4) var(--space-8);
      background: var(--secondary-100);
      color: white;
      text-decoration: none;
      border-radius: var(--radius-lg);
      font-weight: 600;
      transition: transform var(--duration-normal) var(--easing-default),
                  box-shadow var(--duration-normal) var(--easing-default);
    }
    
    /* Design Style: Hover behavior = color-shift + scale-and-shadow */
    .cta:hover {
      background: #0052a3; /* secondary-200 from DNA */
      transform: translateY(-2px);
      box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); /* elevation lg */
    }
    
    /* Visual Effects: Scroll reveal animations */
    .features {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: var(--space-8);
      padding: var(--space-12) 0;
      opacity: 0;
      transform: translateY(20px);
      animation: reveal 0.6s var(--easing-default) forwards;
      animation-delay: 0.2s;
    }
    
    @keyframes reveal {
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }
    
    .feature {
      padding: var(--space-6);
      background: var(--neutral-100);
      border-radius: var(--radius-md);
      border: 1px solid #e0e0e0; /* border role from DNA */
    }
    
    .feature h3 {
      font-size: 1.25rem; /* xl from DNA */
      font-weight: 600;
      margin-bottom: var(--space-4);
    }
    
    @media (max-width: 768px) {
      .hero h1 {
        font-size: 2.25rem; /* 4xl responsive */
      }
      .hero p {
        font-size: 1.125rem; /* lg responsive */
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <section class="hero">
      <h1>Ship faster with AI-powered code reviews</h1>
      <p>Catch bugs before deployment</p>
      <a href="#" class="cta">Start free trial</a>
    </section>
    
    <section class="features">
      <div class="feature">
        <h3>Speed</h3>
        <p>Instant feedback on every commit</p>
      </div>
      <div class="feature">
        <h3>Accuracy</h3>
        <p>AI-powered bug detection</p>
      </div>
      <div class="feature">
        <h3>Integration</h3>
        <p>Works with your existing tools</p>
      </div>
    </section>
  </div>
</body>
</html>
```

**Generation principles (from `references/generation-guide.md`):**

1. **Apply all three dimensions** — design-system (tokens), design-style (qualitative feel), visual-effects (interactions)
2. **Faithful reproduction** — Match the reference's visual richness and detail
3. **Semantic HTML** — Proper elements, accessibility, responsive
4. **Self-contained** — Default to single-file HTML unless specified otherwise
5. **Production-ready** — Clean code, no placeholders

---

## Common Patterns

### Pattern 1: Multi-Reference Analysis

When analyzing **multiple references** (e.g., 3 screenshots + 2 URLs):

1. **Identify dominant patterns** across all references
2. **Note variants** where references disagree (e.g., "Reference A uses 8px radius, B uses 12px — dominant: 12px")
3. **Fill every field** based on consensus or most representative example
4. **Document conflicts** in the JSON output

**Example conflict notation:**

```json
{
  "design-system": {
    "shape": {
      "border-radius": {
        "md": 12,
        "_note": "Variant: Reference A uses 8px, but 12px dominant across B, C, D"
      }
    }
  }
}
```

### Pattern 2: Iterative Refinement

If the first generation feels visually thin compared to references:

**Prompt:**
> "Against the reference [attach same URLs/screenshots], audit hierarchy, ornamentation, typographic rhythm, motion, materiality, and overall UI—then merge your conclusions back into the current implementation."

**Agent action:**
- Re-inspect references for **missed details** (micro-animations, subtle shadows, gradient overlays, etc.)
- Update DNA JSON or implementation to close the gap
- Produce visually richer output

### Pattern 3: DNA Reuse Across Projects

Save extracted DNA JSON to version control:

```bash
# Save DNA
echo '[DNA JSON]' > design-dna.json

# Commit
git add design-dna.json
git commit -m "Add Design DNA for brand identity"

# Reuse in new project
# Prompt: "Generate a dashboard using design-dna.json"
```

### Pattern 4: Component-Specific Generation

Extract DNA, then generate **specific components**:

**Prompt:**
> "Using this Design DNA, generate a navigation bar component"

**Agent generates:**
- Standalone nav component
- Applies DNA tokens (colors, spacing, typography, motion)
- Matches design-style (hierarchy, interaction feel)

---

## Configuration

### Environment Variables

If using AI vision APIs for image analysis (optional):

```bash
# .env
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
```

**Note:** The skill works without API keys if the agent has built-in vision (e.g., Claude Code, Cursor with Claude 3.5 Sonnet).

### Schema Customization

To extend the DNA schema:

1. Edit `references/schema.md` — add new fields or dimensions
2. Update `references/generation-guide.md` — document how to apply new fields
3. Test with **Analyze → Generate** cycle

---

## Troubleshooting

### Issue: Empty or Incomplete DNA JSON

**Symptom:** Agent outputs DNA with missing fields or "TBD" values.

**Fix:**
- Explicitly request: **"Fill every field in the Design DNA schema—no empty values."**
- Reference `references/schema.md` to surface all required fields
- Provide higher-quality references (screenshots vs. blurry photos)

---

### Issue: Generated UI Doesn't Match Reference

**Symptom:** Output looks generic, missing the reference's visual richness.

**Fix:**
1. **Re-analyze** references with explicit instruction: **"Extract all visual details including micro-interactions, shadows, gradients, typographic rhythm, and spacing."**
2. **Iterative refinement:** Attach references again and request audit (see Pattern 2)
3. Verify `visual-effects` dimension is populated (not all "false")

---

### Issue: DNA JSON Conflicts Across References

**Symptom:** Multiple references have incompatible styles.

**Fix:**
- **Choose dominant reference** and note variants
- Or: **Extract separate DNA** for each reference, then manually merge
- Document conflicts in JSON `_note` fields

---

### Issue: Agent Generates React/Vue Instead of HTML

**Symptom:** Default output is a framework component, not self-contained HTML.

**Fix:**
- Explicitly request: **"Generate self-contained HTML/CSS/JS."**
- Or specify framework: **"Generate as a React component using this DNA."**

---

## Key Files Reference

| File | Purpose |
|------|---------|
| `references/schema.md` | Complete Design DNA field definitions |
| `references/generation-guide.md` | How to implement UI from DNA JSON |
| `SKILL.md` | This agent skill documentation |

---

## Example: Full Workflow

**Step 1 — Collect references:**
```
User: "I want to extract design DNA from https://linear.app and this screenshot [attachment]."
```

**Step 2 — Analyze:**
```
Agent:
- Inspects Linear.app and screenshot
- Extracts design-system (colors, typography, spacing, etc.)
- Captures design-style (minimal, modern, fast interactions)
- Notes visual-effects (subtle scroll reveals, smooth transitions)
- Outputs complete DNA JSON (300+ lines)
```

**Step 3 — Generate:**
```
User: "Using this DNA, generate a task dashboard with columns: To Do, In Progress, Done."

Agent:
- Applies DNA tokens (Linear's color palette, Inter font, 8px grid)
- Matches design-style (minimal, generous whitespace, scale-based hierarchy)
- Implements visual-effects (smooth drag-and-drop, hover feedback)
- Outputs self-contained HTML/CSS/JS dashboard
```

**Step 4 — Refine:**
```
User: "Compare against the Linear reference—add missing details."

Agent:
- Re-inspects Linear.app
- Adds subtle shadows, status color coding, keyboard shortcuts hint
- Updates implementation to match reference fidelity
```

---

## Tips for Best Results

1. **High-quality references** — Screenshots at native resolution, live URLs preferred over photos
2. **Multiple angles** — Provide 2–5 references to capture full design system
3. **Explicit instructions** — Request "complete DNA" or "fill every field" to avoid incomplete output
4. **Iterative refinement** — First pass gives structure; second pass adds richness
5. **Version control DNA** — Commit JSON to track design evolution over time

---

## Related Skills

- `design-system-tokens` — Focus on design tokens only (subset of design-dna)
- `ui-component-generator` — Generate isolated components from DNA
- `visual-regression-testing` — Compare generated output against references

---

## License

MIT — https://github.com/zanwei/design-dna/blob/main/LICENSE
