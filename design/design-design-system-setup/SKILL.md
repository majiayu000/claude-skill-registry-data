---
name: design-system-setup
description: Initialize design systems for projects via Q&A and templates, with auto-detection when missing
---

# Design System Setup

## Skill Usage Announcement

**MANDATORY**: When using this skill, announce it at the start with:

```
🔧 Using Skill: design-system-setup | [brief purpose based on context]
```

**Example:**
```
🔧 Using Skill: design-system-setup | [Provide context-specific example of what you're doing]
```

This creates an audit trail showing which skills were applied during the session.



Initialize design systems for projects through guided workflows. Auto-detects missing design systems during specification review and offers two paths: interactive Q&A customization or rapid template-based setup with AI refinement.

## Overview

This skill helps establish a design system foundation for projects that lack one. It integrates with Figma MCP to create design files, exports tokens to code (CSS variables, Tailwind config, or design tokens JSON), and stores metadata in wrangler issues for future reference.

**Key Capabilities:**
- Auto-detection when design system is missing during spec review
- Choice-driven workflow: guided Q&A or template selection
- 3 pre-built templates (minimal, modern, vibrant)
- Figma file creation via MCP
- Token export in multiple formats
- Metadata tracking in wrangler issues

## When to Use

**Auto-detection scenarios** (skill triggers automatically):
- Reviewing specifications that reference UI components without design system
- Implementation planning for frontend work lacking design tokens
- Code review findings showing inconsistent styling patterns
- Issue creation for UI work without design foundation

**Manual invocation** (user explicitly requests):
- `/wrangler:setup-design-system` slash command
- User asks to "create a design system" or "set up design tokens"
- Starting new project with frontend requirements

**When NOT to use:**
- Design system already exists (check wrangler metadata first)
- Pure backend/API projects with no UI
- Projects explicitly avoiding design systems (documented decision)

## Prerequisites

### Required

1. **Figma MCP server configured** in `.claude-plugin/plugin.json`:
   ```json
   {
     "mcpServers": {
       "figma": {
         "command": "npx",
         "args": ["-y", "@modelcontextprotocol/server-figma"]
       }
     }
   }
   ```

2. **Figma personal access token** in environment:
   - Set `FIGMA_PERSONAL_ACCESS_TOKEN` environment variable
   - Or configure in MCP server settings

3. **Wrangler MCP server** (auto-configured in wrangler projects)

### Optional

- Frontend framework preference (React, Vue, HTML/CSS)
- Existing brand guidelines or color palette
- Typography requirements or font licenses

## Workflow

### Phase 1: Detection & Choice

**1.1 Detect Missing Design System**

Check for existing design system metadata:

```typescript
// Use wrangler MCP to search for design system metadata
const existingDesignSystem = await mcp__plugin_wrangler_wrangler_mcp__issues_search({
  query: "design system",
  filters: {
    labels: ["design-system"],
    status: ["open", "in_progress", "closed"]
  },
  fields: ["title", "description", "labels"],
  limit: 1
});

if (existingDesignSystem.issues.length > 0) {
  // Design system exists, extract Figma URL from metadata
  const figmaUrl = existingDesignSystem.issues[0].wranglerContext?.figmaFileUrl;
  // Skip setup, notify user
  return;
}
```

**1.2 Present Workflow Choice**

Use AskUserQuestion to present two paths:

```typescript
const workflowChoice = await AskUserQuestion({
  questions: [{
    question: "No design system found. How would you like to proceed?",
    header: "Setup Method",
    multiSelect: false,
    options: [
      {
        label: "Template + AI Refinement",
        description: "Start with a pre-built template, then customize with frontend-design skill for project-specific polish"
      },
      {
        label: "Guided Q&A Setup",
        description: "Answer questions about color mood, typography, and spacing to build a custom design system from scratch"
      }
    ]
  }]
});
```

### Phase 2A: Template + AI Workflow

**2A.1 Template Selection**

Present template options with visual previews:

```typescript
const templateChoice = await AskUserQuestion({
  questions: [{
    question: "Which design template best fits your project aesthetic?",
    header: "Template",
    multiSelect: false,
    options: [
      {
        label: "Minimal",
        description: "Clean, focused design. Single accent color, 6-step grayscale, 5 font sizes. Best for MVPs, internal tools, prototypes."
      },
      {
        label: "Modern",
        description: "Comprehensive professional system. 9-shade color scales, full component library (20+ components), enterprise-ready."
      },
      {
        label: "Vibrant",
        description: "Bold, playful design. Multi-color palette (5 families), expressive typography, generous spacing. Best for consumer apps, creative brands."
      }
    ]
  }]
});
```

**Visual Preview Reference:**

Each template includes a `preview.svg` file showing color palette, typography samples, and key components. Reference these when presenting options:

- **Minimal**: `skills/design-workflow/design-system-setup/templates/minimal/preview.svg`
- **Modern**: `skills/design-workflow/design-system-setup/templates/modern/preview.svg`
- **Vibrant**: `skills/design-workflow/design-system-setup/templates/vibrant/preview.svg`

**2A.2 Load Template Files**

Read the selected template:

```typescript
const templateName = templateChoice.answers.template.toLowerCase();
const basePath = `/Users/juliushecht/medb/code/wrangler/skills/design-workflow/design-system-setup/templates/${templateName}`;

// Load template files
const tokens = await Read({ file_path: `${basePath}/tokens.json` });
const components = await Read({ file_path: `${basePath}/components.json` });
const figmaTemplate = await Read({ file_path: `${basePath}/figma-template.json` });
```

**2A.3 Create Figma File**

Use Figma MCP to create design file:

```typescript
// Create new Figma file with template
const figmaFile = await figma_create_file({
  name: `${projectName} Design System`,
  template: JSON.parse(figmaTemplate)
});

// Store Figma file URL
const figmaUrl = `https://www.figma.com/file/${figmaFile.key}`;
```

**2A.4 Export Tokens**

Ask user for export format preference:

```typescript
const exportFormat = await AskUserQuestion({
  questions: [{
    question: "How should design tokens be exported to code?",
    header: "Token Format",
    multiSelect: false,
    options: [
      {
        label: "CSS Variables",
        description: "Export as CSS custom properties (:root { --color-primary: #3B82F6; })"
      },
      {
        label: "Tailwind Config",
        description: "Export as tailwind.config.js theme extension (colors, spacing, typography)"
      },
      {
        label: "Design Tokens JSON",
        description: "Export as W3C Design Tokens format for multi-platform usage"
      }
    ]
  }]
});
```

Generate token export file based on selection:

**CSS Variables:**
```css
:root {
  /* Colors */
  --color-primary: #3B82F6;
  --color-neutral-50: #FAFAFA;
  --color-neutral-100: #F5F5F5;
  /* ... */

  /* Typography */
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-mono: "SF Mono", Consolas, Monaco, monospace;
  --font-size-xs: 0.75rem;
  --font-size-sm: 0.875rem;
  /* ... */

  /* Spacing */
  --spacing-1: 0.25rem;
  --spacing-2: 0.5rem;
  --spacing-4: 1rem;
  /* ... */
}
```

**Tailwind Config:**
```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: '#3B82F6',
        neutral: {
          50: '#FAFAFA',
          100: '#F5F5F5',
          // ...
        }
      },
      fontFamily: {
        sans: ['-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        mono: ['SF Mono', 'Consolas', 'Monaco', 'monospace']
      },
      fontSize: {
        xs: '0.75rem',
        sm: '0.875rem',
        // ...
      },
      spacing: {
        1: '0.25rem',
        2: '0.5rem',
        4: '1rem',
        // ...
      }
    }
  }
}
```

**Design Tokens JSON (W3C format):**
```json
{
  "color": {
    "primary": {
      "value": "#3B82F6",
      "type": "color"
    },
    "neutral": {
      "50": { "value": "#FAFAFA", "type": "color" },
      "100": { "value": "#F5F5F5", "type": "color" }
    }
  },
  "typography": {
    "fontFamily": {
      "sans": {
        "value": "-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif",
        "type": "fontFamily"
      }
    },
    "fontSize": {
      "xs": { "value": "0.75rem", "type": "fontSize" },
      "sm": { "value": "0.875rem", "type": "fontSize" }
    }
  }
}
```

**2A.5 Invoke Frontend-Design Skill**

Now use the frontend-design skill to refine the template for project-specific needs:

```
The design system template has been created. Now we'll refine it for your specific project context.

**Invoking frontend-design skill for project-specific customization...**

Context for frontend-design:
- Template selected: ${templateName}
- Token foundation established
- Figma file created: ${figmaUrl}

Please create a sample component (e.g., landing page hero, dashboard card, or key UI element) that demonstrates the design system applied to this project's specific needs. Use the established tokens but add project-specific character and polish.
```

Invoke the `frontend-design` skill, passing project context and template as starting point.

**2A.6 Store Metadata**

Create wrangler issue tracking design system:

```typescript
await mcp__plugin_wrangler_wrangler_mcp__issues_create({
  title: "Design System - ${templateName} Template",
  type: "issue",
  status: "closed",
  priority: "high",
  labels: ["design-system", "figma", templateName],
  description: `
# Design System Setup

**Template**: ${templateName}
**Figma File**: ${figmaUrl}
**Token Export Format**: ${exportFormat}

## Template Details

${templateReadme}

## Usage

Design tokens are available in:
- Figma file (link above)
- Code export: \`${tokenFilePath}\`

## Components Included

${componentsList}

## Next Steps

- [ ] Customize colors for brand
- [ ] Add project-specific components
- [ ] Document component usage patterns
  `,
  wranglerContext: {
    figmaFileUrl: figmaUrl,
    templateName: templateName,
    tokenFormat: exportFormat,
    createdAt: new Date().toISOString()
  }
});
```

### Phase 2B: Guided Q&A Workflow

**2B.1 Color Mood Selection**

```typescript
const colorMood = await AskUserQuestion({
  questions: [{
    question: "What color mood fits your project?",
    header: "Color Mood",
    multiSelect: false,
    options: [
      {
        label: "Cool & Professional",
        description: "Blues, teals, grays. Trustworthy, corporate, technical."
      },
      {
        label: "Warm & Energetic",
        description: "Oranges, reds, yellows. Bold, exciting, action-oriented."
      },
      {
        label: "Calm & Natural",
        description: "Greens, earth tones. Organic, sustainable, wellness."
      },
      {
        label: "Creative & Vibrant",
        description: "Purples, pinks, multi-color. Playful, expressive, artistic."
      }
    ]
  }]
});
```

**2B.2 Typography Preferences**

```typescript
const typography = await AskUserQuestion({
  questions: [{
    question: "What typography style suits your project?",
    header: "Typography",
    multiSelect: false,
    options: [
      {
        label: "Modern Sans-Serif",
        description: "Clean, contemporary. Inter, Work Sans, DM Sans. Versatile for most applications."
      },
      {
        label: "Classic Serif",
        description: "Traditional, elegant. Merriweather, Lora, Crimson. Editorial, luxury brands."
      },
      {
        label: "Display & Expressive",
        description: "Bold, attention-grabbing. Poppins, Righteous, Fredoka. Creative, consumer-facing."
      },
      {
        label: "Monospace/Technical",
        description: "Code-like, precise. JetBrains Mono, Fira Code. Developer tools, technical products."
      }
    ]
  }]
});
```

**2B.3 Spacing & Density**

```typescript
const spacing = await AskUserQuestion({
  questions: [{
    question: "How spacious should the interface feel?",
    header: "Spacing",
    multiSelect: false,
    options: [
      {
        label: "Compact",
        description: "4px base unit, tight spacing. Data-dense applications, dashboards."
      },
      {
        label: "Balanced",
        description: "8px base unit, moderate spacing. General applications, most use cases."
      },
      {
        label: "Generous",
        description: "12px base unit, open spacing. Marketing sites, consumer apps."
      }
    ]
  }]
});
```

**2B.4 Border Radius Style**

```typescript
const borderRadius = await AskUserQuestion({
  questions: [{
    question: "What border radius style fits your brand?",
    header: "Corners",
    multiSelect: false,
    options: [
      {
        label: "Sharp (0-2px)",
        description: "Angular, modern, technical. Minimal radius."
      },
      {
        label: "Subtle (4-8px)",
        description: "Balanced, professional. Moderate rounding."
      },
      {
        label: "Rounded (12-16px)",
        description: "Friendly, approachable. Generous rounding."
      },
      {
        label: "Pill (24px+)",
        description: "Playful, consumer-focused. Full rounds on buttons."
      }
    ]
  }]
});
```

**2B.5 Generate Design System**

Use Q&A responses to generate custom tokens:

```typescript
// Map color mood to primary color
const primaryColors = {
  "Cool & Professional": { primary: "#3B82F6", scale: "blue" },
  "Warm & Energetic": { primary: "#F97316", scale: "orange" },
  "Calm & Natural": { primary: "#10B981", scale: "green" },
  "Creative & Vibrant": { primary: "#8B5CF6", scale: "purple" }
};

// Map typography to font families
const fontFamilies = {
  "Modern Sans-Serif": {
    display: "Inter",
    body: "Inter",
    googleFonts: "Inter:wght@400;500;600;700"
  },
  "Classic Serif": {
    display: "Merriweather",
    body: "Lora",
    googleFonts: "Merriweather:wght@700;900&family=Lora:wght@400;500;600"
  },
  "Display & Expressive": {
    display: "Poppins",
    body: "Work Sans",
    googleFonts: "Poppins:wght@600;700;800&family=Work+Sans:wght@400;500;600"
  },
  "Monospace/Technical": {
    display: "JetBrains Mono",
    body: "JetBrains Mono",
    googleFonts: "JetBrains+Mono:wght@400;500;600;700"
  }
};

// Map spacing to base unit
const spacingScales = {
  "Compact": 4,
  "Balanced": 8,
  "Generous": 12
};

// Map border radius to values
const borderRadiusValues = {
  "Sharp (0-2px)": { sm: "0px", md: "2px", lg: "2px", full: "2px" },
  "Subtle (4-8px)": { sm: "4px", md: "6px", lg: "8px", full: "9999px" },
  "Rounded (12-16px)": { sm: "8px", md: "12px", lg: "16px", full: "9999px" },
  "Pill (24px+)": { sm: "12px", md: "16px", lg: "24px", full: "9999px" }
};

// Generate complete token set
const customTokens = generateTokens(
  primaryColors[colorMood],
  fontFamilies[typography],
  spacingScales[spacing],
  borderRadiusValues[borderRadius]
);
```

**2B.6 Create Figma File & Export**

Follow same steps as Phase 2A.3-2A.6:
- Create Figma file with custom tokens
- Export tokens in chosen format
- Store metadata in wrangler issue

### Phase 3: Verification

**3.1 Validate Token Export**

Ensure token file is valid and accessible:

```typescript
// Read exported token file
const tokenFile = await Read({ file_path: tokenFilePath });

// Validate structure based on format
if (exportFormat === "CSS Variables") {
  // Check for :root selector and variable definitions
  if (!tokenFile.includes(":root") || !tokenFile.includes("--color-")) {
    throw new Error("Invalid CSS Variables export");
  }
} else if (exportFormat === "Tailwind Config") {
  // Check for valid JavaScript module
  if (!tokenFile.includes("module.exports") || !tokenFile.includes("theme")) {
    throw new Error("Invalid Tailwind Config export");
  }
} else if (exportFormat === "Design Tokens JSON") {
  // Parse and validate JSON structure
  try {
    JSON.parse(tokenFile);
  } catch (e) {
    throw new Error("Invalid Design Tokens JSON export");
  }
}
```

**3.2 Verify Figma File Access**

Test Figma file URL:

```typescript
// Use Figma MCP to fetch file metadata
const fileMetadata = await figma_get_file({
  file_key: figmaFileKey
});

if (!fileMetadata || fileMetadata.error) {
  throw new Error("Figma file not accessible");
}
```

**3.3 Confirm Wrangler Metadata**

Verify issue was created with correct metadata:

```typescript
const designSystemIssues = await mcp__plugin_wrangler_wrangler_mcp__issues_search({
  query: "Design System",
  filters: {
    labels: ["design-system"]
  },
  limit: 1
});

if (designSystemIssues.issues.length === 0) {
  throw new Error("Design system metadata not stored");
}

const metadata = designSystemIssues.issues[0].wranglerContext;
if (!metadata.figmaFileUrl) {
  throw new Error("Figma URL not stored in metadata");
}
```

## Integration Points

### Wrangler MCP Metadata Storage

Store design system metadata in wrangler issues for future reference:

**Issue Structure:**
```yaml
---
id: "000042"
title: "Design System - Modern Template"
type: "issue"
status: "closed"
priority: "high"
labels: ["design-system", "figma", "modern"]
wranglerContext:
  figmaFileUrl: "https://www.figma.com/file/abc123/Project-Design-System"
  templateName: "modern"
  tokenFormat: "CSS Variables"
  tokenFilePath: "./src/styles/tokens.css"
  createdAt: "2025-11-21T10:00:00.000Z"
  lastUpdated: "2025-11-21T10:00:00.000Z"
---
```

**Querying Design System:**
```typescript
// Find design system in any project
const designSystem = await mcp__plugin_wrangler_wrangler_mcp__issues_search({
  query: "design system",
  filters: {
    labels: ["design-system"]
  }
});

if (designSystem.issues.length > 0) {
  const figmaUrl = designSystem.issues[0].wranglerContext.figmaFileUrl;
  const tokenPath = designSystem.issues[0].wranglerContext.tokenFilePath;
  // Use in implementation
}
```

### Frontend-Design Skill Integration

When using Template + AI workflow, pass context to frontend-design skill:

**Context to provide:**
- Template name and philosophy
- Token file location
- Figma file URL
- Project-specific requirements

**Example invocation:**
```
I've set up a ${templateName} design system with tokens exported to ${tokenPath}.

Now, using the frontend-design skill, please create a [specific component/page] that:
1. Uses the established design tokens
2. Adds project-specific character beyond the template
3. Demonstrates the design system in context

Figma reference: ${figmaUrl}
Template philosophy: ${templatePhilosophy}
```

### Figma MCP Tools

Key Figma MCP tools used in this skill:

**figma_create_file:**
```typescript
// Create new Figma file
const result = await figma_create_file({
  name: "Project Design System",
  template: templateData // JSON structure defining pages, frames, components
});
// Returns: { key: "abc123", name: "...", ... }
```

**figma_get_file:**
```typescript
// Fetch existing file
const file = await figma_get_file({
  file_key: "abc123"
});
// Returns: { document: {...}, components: {...}, ... }
```

**figma_create_component:**
```typescript
// Create reusable component
const component = await figma_create_component({
  file_key: "abc123",
  node_id: "frame_id",
  name: "Button/Primary",
  description: "Primary action button"
});
```

**figma_export_file:**
```typescript
// Export design tokens
const tokens = await figma_export_file({
  file_key: "abc123",
  format: "design-tokens-json"
});
```

## Error Handling

### Figma API Failures

**Missing Access Token:**
```
ERROR: Figma personal access token not found.

Please set FIGMA_PERSONAL_ACCESS_TOKEN in your environment:
1. Visit https://www.figma.com/developers/api#authentication
2. Generate a personal access token
3. Add to environment: export FIGMA_PERSONAL_ACCESS_TOKEN="figd_..."
4. Restart Claude Code session
```

**File Creation Failure:**
```
ERROR: Failed to create Figma file.

Possible causes:
- Invalid template structure
- Network connectivity issues
- Figma API rate limiting
- Insufficient permissions

Retry in a few moments. If error persists, try manual file creation:
1. Create blank Figma file at https://www.figma.com
2. Import template manually from: ${templatePath}
3. Update wrangler metadata with file URL
```

**Export Failure:**
```
ERROR: Failed to export design tokens from Figma.

Workaround:
1. Open Figma file: ${figmaUrl}
2. Install Tokens Studio plugin
3. Export tokens manually
4. Save to: ${tokenFilePath}
```

### Missing Prerequisites

**Figma MCP Not Configured:**
```
ERROR: Figma MCP server not found.

Add to .claude-plugin/plugin.json:
{
  "mcpServers": {
    "figma": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-figma"]
    }
  }
}

Then restart Claude Code.
```

### Invalid User Input

**Template Selection Timeout:**
```
No template selected within timeout period.

Defaulting to "Minimal" template for rapid setup.
You can customize later via Figma file: ${figmaUrl}
```

**Export Format Not Supported:**
```
ERROR: Export format "${format}" not supported.

Supported formats:
- CSS Variables
- Tailwind Config
- Design Tokens JSON

Please choose one of the supported formats.
```

## Examples

### Example 1: Auto-Detection During Spec Review

**Scenario:** Agent reviewing specification for new dashboard feature

```
[Reviewing specification: Dashboard Feature]

DETECTED: Specification references "primary button", "card component", and "color palette" but no design system exists.

**Auto-triggering design-system-setup skill...**

No design system found for this project. Let's set one up before proceeding with implementation.

[Presents workflow choice to user]
```

### Example 2: Manual Template Setup

**User request:**
```
I need to set up a design system for my SaaS application. It's a professional tool for data analytics.
```

**Agent response:**
```
I'll help set up a design system for your SaaS analytics tool.

[Uses AskUserQuestion to present workflow choice]
[User selects "Template + AI Refinement"]
[Uses AskUserQuestion to present template options]
[User selects "Modern" - comprehensive professional system]

Loading Modern template...
✓ Created Figma file: https://www.figma.com/file/xyz789/Analytics-Design-System
✓ Exported tokens as CSS Variables to: ./src/styles/tokens.css
✓ Stored metadata in wrangler issue #042

Now invoking frontend-design skill to create a project-specific dashboard component...

[Invokes frontend-design skill with context]
```

### Example 3: Q&A Custom Setup

**User request:**
```
Create a design system for a wellness app targeting Gen Z users.
```

**Agent response:**
```
I'll guide you through creating a custom design system for your wellness app.

[Q&A Flow]

Q: What color mood fits your project?
A: Calm & Natural (Greens, earth tones)

Q: What typography style suits your project?
A: Display & Expressive (Poppins/Work Sans)

Q: How spacious should the interface feel?
A: Generous (12px base unit)

Q: What border radius style fits your brand?
A: Rounded (12-16px)

Generating custom design system...
✓ Created Figma file with custom tokens
✓ Exported as Tailwind Config to: ./tailwind.config.js
✓ Included Google Fonts: Poppins & Work Sans
✓ Stored metadata in wrangler issue #043

Design system ready! Preview in Figma: https://www.figma.com/file/...
```

### Example 4: Integration with Frontend-Design

**Workflow:** Template selection → Token export → Frontend-design refinement

```
[After selecting Vibrant template and exporting tokens]

Design system foundation established with Vibrant template:
- Multi-color palette (pink, orange, teal, purple, yellow)
- Expressive typography (Poppins display, Work Sans body)
- Generous spacing and playful border radius
- Tokens exported to: ./src/styles/tokens.css
- Figma file: https://www.figma.com/file/abc123/...

Now using frontend-design skill to create a project-specific hero section that showcases the vibrant aesthetic in context...

[Invokes frontend-design skill]
[Frontend-design creates custom hero with animations, unexpected layouts, bold typography]
[Result: Vibrant template + project-specific polish = distinctive, production-ready design]
```

## Best Practices

### Template Selection Guidance

**Use Minimal when:**
- MVP/prototype projects
- Internal tools with minimal UI needs
- Projects prioritizing speed over brand expression
- Teams wanting flexibility to evolve system later

**Use Modern when:**
- Enterprise applications
- SaaS products with complex UIs
- Professional web applications
- Projects requiring comprehensive component library
- Teams with established brand guidelines

**Use Vibrant when:**
- Consumer mobile apps
- Creative portfolios and agencies
- Youth-oriented brands
- Marketing/landing pages
- Projects where personality and memorability are critical

### Token Export Recommendations

**CSS Variables:**
- Best for vanilla HTML/CSS projects
- Works with any framework (framework-agnostic)
- Easy to update at runtime (theming, dark mode)
- Browser support: IE11+ (with fallbacks)

**Tailwind Config:**
- Best for Tailwind CSS projects (obviously)
- Seamless integration with utility classes
- IntelliSense support in VS Code
- Type-safe with TypeScript

**Design Tokens JSON:**
- Best for multi-platform projects (web, mobile, desktop)
- Platform-agnostic token format
- Enables design-to-code pipelines
- Compatible with Style Dictionary, Theo

### Metadata Management

**Always include in wrangler metadata:**
- `figmaFileUrl`: Direct link to Figma file
- `templateName`: Which template was used (if any)
- `tokenFormat`: Export format chosen
- `tokenFilePath`: Relative path to token file
- `createdAt`: Timestamp of setup
- `lastUpdated`: Timestamp of last modification

**Use labels for searchability:**
- `design-system`: All design system issues
- `figma`: Issues with Figma integration
- Template name: `minimal`, `modern`, or `vibrant`
- `custom`: If Q&A workflow was used

### Integration Workflow

**Template + AI is recommended for:**
- Most projects (80% of use cases)
- Teams wanting rapid setup with customization
- Projects with clear aesthetic direction
- When you want proven foundation + project polish

**Q&A workflow is recommended for:**
- Projects with unique brand requirements
- When existing templates don't fit aesthetic
- Teams with specific design constraints
- Educational purposes (understanding token structure)

## Verification Checklist

After setup completion, verify:

- [ ] Figma file created and accessible
- [ ] Token file exists at specified path
- [ ] Token file contains valid structure for chosen format
- [ ] Wrangler issue created with correct labels
- [ ] Metadata includes `figmaFileUrl` and `tokenFilePath`
- [ ] If Template + AI: frontend-design skill was invoked
- [ ] If Q&A: All user preferences reflected in tokens
- [ ] Google Fonts link included (if web fonts used)
- [ ] Token file imported in project (CSS link, JS import, etc.)

## Future Enhancements

**Planned features:**
- Brand asset upload (logo, icons) to Figma file
- Component library generation from templates
- Dark mode token generation
- Accessibility contrast checking
- Token versioning and changelog
- Figma-to-code sync automation
- Template customization wizard (modify template before export)
- Design system documentation generation

## Related Skills

- **frontend-design**: Refine templates with project-specific polish
- **writing-specifications**: Create design system specifications
- **implement**: Implement components using design tokens
- **code-review**: Review component implementation against design system

## References

- **Templates**: `/skills/design-workflow/design-system-setup/templates/`
- **Figma MCP Documentation**: https://github.com/modelcontextprotocol/servers/tree/main/src/figma
- **W3C Design Tokens Spec**: https://design-tokens.github.io/community-group/format/
- **Tailwind Theming**: https://tailwindcss.com/docs/theme
