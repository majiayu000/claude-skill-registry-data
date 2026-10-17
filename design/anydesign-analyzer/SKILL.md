---
name: anydesign-analyzer
description: Analyze images, websites, and Figma files to generate structured design.md with DTCG tokens, component inventory, and reconstruction notes
triggers:
  - analyze this design and create a design.md
  - extract design tokens from this website
  - generate a design system from this screenshot
  - pull the color palette and typography from this image
  - create a design brief from this Figma file
  - analyze this landing page and document the design system
  - extract CSS variables and create design tokens
  - generate WCAG contrast report for these colors
---

# anydesign-analyzer

> Skill by [ara.so](https://ara.so) — Design Skills collection.

**anydesign** is a Claude skill that analyzes visual sources (images, websites, Figma files) and produces structured `design.md` files with DTCG-compliant design tokens, component inventories, and reconstruction notes. The output is portable across all AI builders (v0, Lovable, Cursor, Bolt, Claude Code) and design tools.

## What it produces

Every analysis generates three artifacts:

1. **`design.md`** — 7-section structured document (TL;DR, visual identity, design system, components, layout, reconstruction notes, open questions)
2. **`design-tokens.json`** — W3C DTCG format tokens (`$value` / `$type`)
3. **`design-a11y.md`** *(optional)* — WCAG 2.1 contrast report

All inferences include confidence levels: ✅ high / ⚠️ medium / ❓ low

## Installation

### 1. Clone and install the skill

```bash
# Clone the repository
git clone https://github.com/uxKero/anydesign.git

# Copy to Claude skills directory (personal)
cp -r anydesign ~/.claude/skills/

# OR for project-specific installation
cp -r anydesign /path/to/project/.claude/skills/
```

### 2. Install Python dependencies

```bash
cd anydesign
pip install -r requirements.txt

# If using capture_site.py for screenshots
playwright install chromium
```

### 3. (Optional) Connect Figma MCP

For Figma file analysis, connect the Figma MCP in Claude settings (`Settings → Connectors`). The skill uses these tools when available:
- `get_metadata`
- `get_variable_defs`
- `get_design_context`
- `get_screenshot`

## Core workflows

### Analyze a website

```python
# The skill activates automatically when you provide a URL
# Example prompt:
"Analyze https://vercel.com and create a design.md with full token extraction"

# The skill will:
# 1. Fetch the page HTML
# 2. Extract all CSS custom properties from linked stylesheets
# 3. Capture screenshots (multi-viewport if needed)
# 4. Generate design.md + design-tokens.json
```

### Analyze an uploaded image

```python
# Upload a screenshot or design mockup
# Example prompt:
"Extract the design system from this landing page screenshot"

# The skill will:
# 1. Use vision to identify colors, typography, spacing
# 2. Extract dominant colors via extract_colors.py
# 3. Infer component structure and hierarchy
# 4. Mark each inference with confidence level
```

### Analyze a Figma file

```python
# Requires Figma MCP connection
# Example prompt:
"Analyze this Figma file and check token consistency"

# The skill will:
# 1. Pull variable definitions via get_variable_defs
# 2. Extract usage via get_design_context
# 3. Cross-reference explicit tokens vs actual usage
# 4. Flag inconsistencies in the design.md
```

## Standalone CLI scripts

All scripts in `scripts/` work independently of Claude:

### Extract CSS variables from any URL

```bash
# Basic extraction
python scripts/extract_css_vars.py https://vercel.com/ --pretty

# Save to file
python scripts/extract_css_vars.py https://example.com/ --output tokens.json

# The script:
# - Fetches all linked stylesheets
# - Extracts inline <style> blocks
# - Groups --* custom properties by category (color, spacing, typography, etc.)
```

### Capture multi-viewport screenshots

```bash
# Single viewport
python scripts/capture_site.py https://your-site.com --output screenshot.png

# Multiple viewports
python scripts/capture_site.py https://your-site.com \
  --viewports desktop,tablet,mobile \
  --output captures/

# Options:
# --scroll: Enable scroll-capture for lazy-loaded content
# --dismiss-cookies: Auto-dismiss cookie banners
```

### Extract dominant colors from image

```bash
# Extract 5 dominant colors
python scripts/extract_colors.py screenshot.png --count 5

# Output as hex codes
python scripts/extract_colors.py image.png --format hex

# Save to JSON
python scripts/extract_colors.py image.png --output colors.json
```

### Check WCAG contrast

```bash
# Check single pair
python scripts/check_contrast.py --pair "#111,#FFF"

# Check multiple pairs
python scripts/check_contrast.py \
  --pair "#111,#FFF" \
  --pair "#3B82F6,#FFF" \
  --pair "#EF4444,#FFF"

# From pairs file (one per line: foreground,background)
python scripts/check_contrast.py --pairs-file colors.txt

# Output markdown table
python scripts/check_contrast.py --pair "#111,#FFF" --output contrast-report.md
```

### Validate a design.md

```bash
# Lint against spec
python scripts/lint_design_md.py path/to/design.md

# Validates:
# - YAML frontmatter presence
# - {token.refs} resolve correctly
# - 1:1 component mapping
# - Section 6 (reconstruction notes) is non-empty
```

### Audit tokens against live site

```bash
# Check if declared tokens match current CSS
python scripts/verify_design.py path/to/design-tokens.json https://vercel.com/

# Reports drift between:
# - Declared token values in JSON
# - Live CSS custom properties on the site
```

### Export for Claude Design

```bash
# Generate bundle for claude.ai/design upload
python scripts/export_for_claude_design.py path/to/design.md --out my-brand/

# Produces:
# - brand-kit.pptx (primary asset)
# - brand-overview.docx (full design.md as Word)
# - tokens.css (CSS custom properties)
# - tailwind.config.ts (Tailwind v3 config)
# - README-claude-design.md (upload instructions)
```

## Environment setup

```bash
# No API keys required for core functionality
# The skill uses Claude's built-in capabilities

# For Figma analysis, configure MCP in Claude settings
# For Playwright screenshots, ensure chromium is installed:
playwright install chromium
```

## design.md structure

Every generated `design.md` follows this 7-section format:

```markdown
---
title: Design System — [Project Name]
source: [URL or file path]
analyzed_at: [ISO timestamp]
confidence_legend: "✅ high / ⚠️ medium / ❓ low"
---

## 1. TL;DR
Three-sentence summary for AI builders and designers

## 2. Visual Identity
Brand personality, color philosophy, typography strategy

## 3. Design System (Tokens)
Colors, typography, spacing, radii, shadows, borders
All with confidence markers and {token.refs}

## 4. Component Inventory
Buttons, inputs, cards, navigation — structured by category

## 5. Layout & Composition
Grid systems, breakpoints, content hierarchy

## 6. Reconstruction Notes
Step-by-step guidance for rebuilding this design

## 7. Open Questions
What requires clarification or additional references
```

## design-tokens.json format

Tokens follow [W3C DTCG specification](https://www.designtokens.org/):

```json
{
  "color": {
    "primary": {
      "$value": "#3b82f6",
      "$type": "color",
      "confidence": "high",
      "source": "CSS var(--color-primary)"
    },
    "background": {
      "$value": "#ffffff",
      "$type": "color",
      "confidence": "high"
    }
  },
  "spacing": {
    "unit": {
      "$value": "4px",
      "$type": "dimension",
      "confidence": "medium"
    },
    "scale": {
      "1": { "$value": "{spacing.unit}", "$type": "dimension" },
      "2": { "$value": "8px", "$type": "dimension" },
      "4": { "$value": "16px", "$type": "dimension" }
    }
  },
  "typography": {
    "font-family": {
      "sans": {
        "$value": "Inter, system-ui, sans-serif",
        "$type": "fontFamily",
        "confidence": "high"
      }
    },
    "font-size": {
      "base": { "$value": "16px", "$type": "dimension" },
      "lg": { "$value": "18px", "$type": "dimension" }
    }
  }
}
```

## Real-world examples

### Example 1: Analyze Vercel landing page

```python
# Prompt:
"Analyze https://vercel.com and extract the complete design system"

# Output (in examples/vercel-landing/):
# - design.md: Full analysis with 808 extracted CSS variables
# - design-tokens.json: Geist design system in DTCG format
# - design-a11y.md: WCAG contrast report
# - capture.png: Desktop screenshot
# - claude-design-bundle/: Ready for claude.ai/design upload
```

### Example 2: Generate v0 brief from screenshot

```python
# Upload screenshot, prompt:
"Create a design.md I can paste into v0 to build this landing page"

# The skill generates a reconstruction-focused design.md
# Paste into v0.dev → builds working app
# See live demo: https://v0-anydesignexample.vercel.app/
```

### Example 3: Extract tokens for Style Dictionary

```bash
# Analyze site
python scripts/extract_css_vars.py https://your-brand.com/ --output raw-tokens.json

# The design-tokens.json is already DTCG-compliant
# Import directly into Style Dictionary:
# config.json:
{
  "source": ["design-tokens.json"],
  "platforms": {
    "css": {
      "transformGroup": "css",
      "buildPath": "build/css/",
      "files": [{
        "destination": "variables.css",
        "format": "css/variables"
      }]
    }
  }
}
```

### Example 4: Audit brand consistency

```bash
# After 6 months, check if site still matches captured tokens
python scripts/verify_design.py design-tokens.json https://your-brand.com/

# Output shows:
# - Tokens that match (✓)
# - Tokens that drifted (⚠️ with delta)
# - Tokens no longer present (✗)
```

## Using output with AI builders

| Tool | How to consume |
|------|----------------|
| **v0** | Paste entire `design.md` as project brief |
| **Lovable** | Paste `design.md`, iterate visually |
| **Cursor/Windsurf** | Add `design.md` to context, ask for components |
| **Claude Code** | Provide both `design.md` + `design-tokens.json` |
| **Bolt** | Paste `design.md` as prompt |
| **Style Dictionary** | Import `design-tokens.json` directly |
| **Figma Variables** | Import `design-tokens.json` (DTCG format) |
| **Tokens Studio** | Import `design-tokens.json` |

## Common patterns

### Pattern 1: Full website capture and tokenization

```bash
# 1. Capture screenshots
python scripts/capture_site.py https://example.com \
  --viewports desktop,tablet,mobile \
  --scroll \
  --output captures/

# 2. Extract CSS tokens
python scripts/extract_css_vars.py https://example.com --output raw-tokens.json

# 3. Analyze in Claude
"Using these screenshots and raw-tokens.json, create a complete design.md"

# 4. Validate output
python scripts/lint_design_md.py design.md

# 5. Check contrast
python scripts/check_contrast.py --pairs-file design-tokens.json
```

### Pattern 2: Figma to code workflow

```python
# In Claude with Figma MCP connected:
"Analyze [Figma file URL], check for token consistency, and generate design.md"

# The skill will:
# 1. Pull variable definitions (explicit tokens)
# 2. Extract actual usage (get_design_context)
# 3. Flag discrepancies
# 4. Generate design.md with notes on inconsistencies

# Then feed to v0/Cursor:
"Build this using the attached design.md"
```

### Pattern 3: Brand asset bundle for Claude Design

```bash
# 1. Analyze reference
"Analyze our brand homepage and create design.md"

# 2. Export bundle
python scripts/export_for_claude_design.py design.md --out brand-bundle/

# 3. Upload to claude.ai/design:
# - brand-kit.pptx (main asset)
# - brand-overview.docx (brief)
# - tokens.css or tailwind.config.ts (code reference)

# 4. All future Claude Design projects use this brand by default
```

## Troubleshooting

### Issue: CSS extraction returns empty

**Cause**: Site uses inline styles or CSS-in-JS, not CSS custom properties.

**Solution**:
```bash
# Check if site uses custom properties
curl -s https://example.com | grep -o "var(--[^)]*)" | head -5

# If empty, the site doesn't use CSS vars
# Rely on vision-based extraction instead:
"Analyze this screenshot and infer the design system"
```

### Issue: Playwright screenshot fails

**Cause**: Chromium not installed or site blocks automation.

**Solution**:
```bash
# Reinstall chromium
playwright install chromium

# Try with different user agent
python scripts/capture_site.py https://example.com \
  --user-agent "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
```

### Issue: Token references don't resolve in design.md

**Cause**: Circular references or malformed `{token.ref}` syntax.

**Solution**:
```bash
# Validate the design.md
python scripts/lint_design_md.py design.md

# Check design-tokens.json for circular refs
# Fix manually or regenerate
```

### Issue: Figma MCP tools not available

**Cause**: MCP not connected or insufficient permissions.

**Solution**:
1. Open Claude settings → Connectors
2. Verify Figma MCP is enabled
3. Check Figma file permissions (must have view access)
4. Retry analysis

### Issue: Contrast report shows all failures

**Cause**: Background color not correctly identified.

**Solution**:
```bash
# Manually specify background
python scripts/check_contrast.py \
  --pair "#3B82F6,#FFFFFF" \
  --background "#FFFFFF"

# Or update design.md with correct background token
```

## Advanced usage

### Custom token extraction with filters

```python
# In Python, use extract_css_vars.py as a module
import sys
sys.path.append('scripts')
from extract_css_vars import extract_css_variables

url = "https://example.com"
tokens = extract_css_variables(url)

# Filter only color tokens
color_tokens = {
    k: v for k, v in tokens.items() 
    if k.startswith('--color-') or '#' in v
}

# Convert to DTCG
dtcg = {
    "color": {
        k.replace('--color-', ''): {
            "$value": v,
            "$type": "color"
        }
        for k, v in color_tokens.items()
    }
}
```

### Batch processing multiple sites

```bash
# Create a sites.txt with URLs (one per line)
# Then process in batch:

while read url; do
  domain=$(echo $url | sed 's|https://||' | sed 's|/.*||')
  mkdir -p "output/$domain"
  
  python scripts/extract_css_vars.py "$url" \
    --output "output/$domain/tokens.json"
  
  python scripts/capture_site.py "$url" \
    --output "output/$domain/screenshot.png"
done < sites.txt

# Analyze each in Claude:
"For each folder in output/, create a design.md using the tokens.json and screenshot.png"
```

### Integration with CI/CD

```yaml
# .github/workflows/design-audit.yml
name: Design Token Audit
on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          playwright install chromium
      
      - name: Audit tokens
        run: |
          python scripts/verify_design.py \
            design-tokens.json \
            https://production-site.com/ \
            --output audit-report.md
      
      - name: Create issue if drift detected
        if: failure()
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: 'Design token drift detected',
              body: require('fs').readFileSync('audit-report.md', 'utf8')
            })
```

## Project structure reference

```
anydesign/
├── scripts/
│   ├── extract_css_vars.py      # CSS custom property extraction
│   ├── capture_site.py          # Multi-viewport screenshots
│   ├── extract_colors.py        # Dominant color extraction
│   ├── check_contrast.py        # WCAG contrast checker
│   ├── lint_design_md.py        # design.md validator
│   ├── verify_design.py         # Token drift auditor
│   └── export_for_claude_design.py  # Claude Design bundle generator
├── examples/
│   ├── vercel-landing/          # Real production example
│   └── landing-example/         # Synthetic demo
├── requirements.txt
└── SKILL.md                     # This file
```

## Additional resources

- [W3C Design Tokens Community Group](https://www.designtokens.org/)
- [WCAG 2.1 Contrast Guidelines](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html)
- [Claude Agent Skills Documentation](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
- [Live v0 demo](https://v0-anydesignexample.vercel.app/) built from skill output
- [Example: Vercel landing analysis](https://github.com/uxKero/anydesign/tree/main/examples/vercel-landing)
