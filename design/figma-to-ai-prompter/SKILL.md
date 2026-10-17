---
name: figma-to-ai-prompter
description: Generate optimized prompts from Figma designs for AI prototyping tools like Lovable, Figma Make, Pencil.dev, Paper.design and Google Stitch
triggers:
  - "convert figma design to ai prompt"
  - "generate prompt from figma file"
  - "create lovable prompt from design"
  - "optimize figma to prototype workflow"
  - "extract figma design structure"
  - "transform figma into ai-ready prompt"
  - "prepare figma for ai prototyping"
  - "reduce prompt tokens for figma conversion"
---

# Figma to AI Prompter

> Skill by [ara.so](https://ara.so) — Design Skills collection.

Figma-to-AI Prompter converts Figma designs into structured, token-optimized prompts for AI prototyping tools. It bridges the design-to-code gap by extracting design structure and generating targeted prompts for Lovable, Figma Make, Pencil.dev, Paper.design, and Google Stitch — achieving up to 97% reduction in prompt size and 18% reduction in execution cost.

## What It Does

- **Extracts** Figma design structure (layouts, components, styles)
- **Transforms** design data into tool-specific prompts
- **Optimizes** token usage through MCP text context instead of frame attachments
- **Supports** multiple AI prototyping platforms with different models and output formats
- **Validates** generated prototypes against original designs

## Installation

```bash
# Clone the repository
git clone https://github.com/royvillasana/figma-to-ai-prompter.git
cd figma-to-ai-prompter

# Install dependencies (if applicable)
npm install
```

## Project Structure

```
figma-to-ai-prompter/
├── prompts/                    # Tool-specific prompt templates
│   ├── figma-to-lovable.md
│   ├── figma-to-figmamake.md
│   ├── figma-to-pencil.md
│   └── figma-to-paper.md
├── examples/                   # Sample inputs and outputs
│   ├── input-figma.json
│   └── output-prompt.md
├── scripts/                    # Transformation utilities
│   └── transform.js
└── README.md
```

## Supported AI Tools

| Tool | Model | Output | Token Model |
|------|-------|--------|-------------|
| **Lovable** | Claude | Full-stack React app | Credit per message |
| **Figma Make** | Claude | Interactive HTML prototype | Figma subscription |
| **Pencil.dev** | AI | Production React components | Credit per generation |
| **Paper.design** | Agent | HTML/CSS canvas + code export | Agent tool calls |
| **Google Stitch** | Gemini 2.5 | Responsive UI → Figma/HTML | Limited monthly generations |

## Core Workflow

### 1. Extract Figma Design Data

Export your Figma design structure as JSON or use the Figma API:

```javascript
// Using Figma API
const FIGMA_TOKEN = process.env.FIGMA_TOKEN;
const FILE_KEY = 'your-file-key';

async function fetchFigmaFile(fileKey) {
  const response = await fetch(
    `https://api.figma.com/v1/files/${fileKey}`,
    {
      headers: { 'X-Figma-Token': FIGMA_TOKEN }
    }
  );
  return await response.json();
}

const figmaData = await fetchFigmaFile(FILE_KEY);
```

### 2. Transform to Structured Context

Use MCP text context blocks instead of frame attachments for token efficiency:

```javascript
// scripts/transform.js
function extractDesignStructure(figmaNode) {
  return {
    type: figmaNode.type,
    name: figmaNode.name,
    layout: {
      width: figmaNode.absoluteBoundingBox?.width,
      height: figmaNode.absoluteBoundingBox?.height,
      x: figmaNode.absoluteBoundingBox?.x,
      y: figmaNode.absoluteBoundingBox?.y
    },
    styles: extractStyles(figmaNode),
    children: figmaNode.children?.map(extractDesignStructure) || []
  };
}

function extractStyles(node) {
  return {
    fills: node.fills,
    strokes: node.strokes,
    effects: node.effects,
    cornerRadius: node.cornerRadius,
    constraints: node.constraints
  };
}

function generatePromptContext(structure) {
  return `
Design Structure:
- Component: ${structure.name}
- Type: ${structure.type}
- Layout: ${structure.layout.width}x${structure.layout.height}
- Styles: ${JSON.stringify(structure.styles, null, 2)}
${structure.children.length > 0 ? `- Children: ${structure.children.length} elements` : ''}
  `.trim();
}

// Example usage
const designStructure = extractDesignStructure(figmaData.document);
const promptContext = generatePromptContext(designStructure);
console.log(promptContext);
```

### 3. Generate Tool-Specific Prompts

#### For Lovable (Claude → Full-stack React)

```markdown
# Lovable Prompt Template

## Design Context
{DESIGN_STRUCTURE}

## Requirements
- Create a full-stack React application
- Use Tailwind CSS for styling
- Match the exact layout and spacing from the design
- Implement responsive behavior for mobile/tablet/desktop
- Include all interactive states (hover, active, disabled)

## Component Hierarchy
{COMPONENT_TREE}

## Style Specifications
{COLOR_PALETTE}
{TYPOGRAPHY}
{SPACING_SYSTEM}

## Interactions
{INTERACTIVE_ELEMENTS}

Please generate a complete React application with:
1. Component structure matching the design hierarchy
2. Tailwind classes for all styling
3. Proper state management for interactions
4. Responsive breakpoints
```

#### For Figma Make (Claude → HTML Prototype)

```markdown
# Figma Make Prompt Template

## Design Analysis
{DESIGN_STRUCTURE}

## Output Requirements
- Generate interactive HTML/CSS prototype
- Use vanilla JavaScript for interactions
- Match pixel-perfect layout from Figma
- Include all design tokens (colors, spacing, typography)
- Implement hover and click states

## Layout Structure
{FRAME_HIERARCHY}

## Style Guide
{DESIGN_TOKENS}

## Validation
Once generated, compare against published Figma Make link:
{FIGMA_MAKE_URL}

Identify discrepancies in:
- Spacing and alignment
- Color values
- Typography
- Interactive behavior
```

#### For Pencil.dev (AI → Production React)

```markdown
# Pencil.dev Prompt Template

## Component Requirements
{COMPONENT_SPECS}

## Design System Integration
- Use existing design tokens: {TOKEN_PATH}
- Follow component patterns: {PATTERN_LIBRARY}
- Ensure accessibility (WCAG 2.1 AA)

## Technical Constraints
- React 18+
- TypeScript
- Styled-components or CSS modules
- Props interface for customization

## Design Context
{DESIGN_STRUCTURE}

Generate production-ready React component with:
1. Full TypeScript types
2. Prop documentation
3. Storybook stories
4. Unit tests
```

### 4. Token Optimization Strategy

**Avoid frame attachments** (adds 300-500 hidden tokens):

```javascript
// ❌ Token-heavy approach
const prompt = `Generate this design: [Frame attachment]`;
// Hidden cost: ~500 tokens + interpretation overhead

// ✅ Optimized approach using MCP text context
const prompt = `
Generate design with:
- Container: 1200px max-width, centered
- Header: 64px height, #1A1A1A background
- Grid: 3 columns, 24px gap
- Cards: white bg, 8px radius, 16px padding
`;
// Cost: ~45 tokens, precise instructions
```

**Structured extraction example:**

```javascript
function optimizePromptGeneration(figmaNode) {
  // Extract only essential information
  const essential = {
    layout: `${figmaNode.absoluteBoundingBox.width}x${figmaNode.absoluteBoundingBox.height}`,
    background: figmaNode.fills?.[0]?.color,
    padding: figmaNode.paddingLeft || 0,
    gap: figmaNode.itemSpacing || 0,
    cornerRadius: figmaNode.cornerRadius || 0
  };
  
  // Generate minimal, structured prompt
  return Object.entries(essential)
    .filter(([_, value]) => value !== undefined && value !== 0)
    .map(([key, value]) => `${key}: ${JSON.stringify(value)}`)
    .join('\n');
}

// Result: ~45 tokens vs 500+ with frame attachment
```

## Configuration

### Environment Variables

```bash
# .env
FIGMA_TOKEN=your_figma_personal_access_token
FIGMA_FILE_KEY=your_file_key
TARGET_TOOL=lovable  # lovable | figmamake | pencil | paper | stitch
```

### Tool-Specific Settings

```javascript
// config.js
module.exports = {
  lovable: {
    framework: 'react',
    styling: 'tailwind',
    maxTokens: 4000
  },
  figmamake: {
    outputFormat: 'html',
    includeInteractions: true,
    validationURL: process.env.FIGMA_MAKE_URL
  },
  pencil: {
    typescript: true,
    testFramework: 'jest',
    designSystem: 'custom'
  }
};
```

## Common Patterns

### Pattern 1: Complete Figma-to-Prompt Pipeline

```javascript
const { fetchFigmaFile, extractDesignStructure, generatePromptContext } = require('./scripts/transform');

async function generateAIPrompt(fileKey, targetTool) {
  // 1. Fetch Figma data
  const figmaData = await fetchFigmaFile(fileKey);
  
  // 2. Extract structure
  const structure = extractDesignStructure(figmaData.document);
  
  // 3. Generate optimized context
  const context = generatePromptContext(structure);
  
  // 4. Load tool-specific template
  const template = require(`./prompts/figma-to-${targetTool}.md`);
  
  // 5. Merge context with template
  const finalPrompt = template.replace('{DESIGN_STRUCTURE}', context);
  
  return finalPrompt;
}

// Usage
const prompt = await generateAIPrompt('abc123', 'lovable');
console.log(prompt);
```

### Pattern 2: Iterative Validation Loop

```javascript
async function validateAndRefine(initialPrompt, figmaMakeURL) {
  let currentPrompt = initialPrompt;
  let iteration = 0;
  const maxIterations = 3;
  
  while (iteration < maxIterations) {
    console.log(`Iteration ${iteration + 1}: Generating prototype...`);
    
    // Send to AI tool (pseudo-code)
    const generatedCode = await sendToAITool(currentPrompt);
    
    // Validate against Figma Make
    const validationPrompt = `
Compare this generated code against the published Figma Make design:
${figmaMakeURL}

Generated code:
${generatedCode}

List specific discrepancies in:
1. Layout and spacing
2. Colors and typography
3. Component structure
4. Interactive behavior

Provide updated prompt instructions to fix discrepancies.
    `;
    
    const feedback = await sendToAITool(validationPrompt);
    
    if (feedback.includes('no discrepancies')) {
      console.log('✅ Validation passed');
      break;
    }
    
    // Refine prompt based on feedback
    currentPrompt = `${currentPrompt}\n\n## Corrections from validation:\n${feedback}`;
    iteration++;
  }
  
  return currentPrompt;
}
```

### Pattern 3: Component Extraction for Design Systems

```javascript
function extractReusableComponents(figmaNode) {
  const components = [];
  
  function traverse(node) {
    if (node.type === 'COMPONENT' || node.type === 'COMPONENT_SET') {
      components.push({
        name: node.name,
        id: node.id,
        description: node.description,
        props: extractComponentProps(node),
        variants: node.children?.map(child => child.name) || []
      });
    }
    
    node.children?.forEach(traverse);
  }
  
  traverse(figmaNode);
  return components;
}

function extractComponentProps(componentNode) {
  const props = {};
  
  // Extract from component properties
  if (componentNode.componentPropertyDefinitions) {
    Object.entries(componentNode.componentPropertyDefinitions).forEach(([key, def]) => {
      props[key] = {
        type: def.type,
        defaultValue: def.defaultValue,
        values: def.variantOptions || []
      };
    });
  }
  
  return props;
}

// Generate component library prompt
const components = extractReusableComponents(figmaData.document);
const componentPrompt = `
Create a design system with these components:

${components.map(c => `
## ${c.name}
Props: ${JSON.stringify(c.props)}
Variants: ${c.variants.join(', ')}
`).join('\n')}
`;
```

## Troubleshooting

### Issue: High Token Usage

**Problem:** Prompts exceeding 1000+ tokens  
**Solution:** Use MCP text context instead of frame attachments

```javascript
// Instead of attaching frames, extract structured data
const minimalContext = {
  dimensions: `${width}x${height}`,
  colors: extractColorPalette(node),
  spacing: extractSpacingValues(node),
  typography: extractTextStyles(node)
};

// Generate compact prompt
const prompt = `Create layout: ${JSON.stringify(minimalContext)}`;
```

### Issue: Inconsistent AI Output

**Problem:** Generated code doesn't match design  
**Solution:** Add explicit constraints and validation

```javascript
const prompt = `
${basePrompt}

STRICT REQUIREMENTS:
- Header height must be exactly 64px
- Use #1A1A1A for background (not approximations)
- Grid gap must be 24px (verify in DevTools)
- Card padding: 16px all sides

Validation: Compare output against ${figmaMakeURL}
`;
```

### Issue: Missing Design Tokens

**Problem:** Colors/spacing not extracted correctly  
**Solution:** Deep traverse all style properties

```javascript
function extractAllStyles(node, styles = {}) {
  // Extract fills
  if (node.fills) {
    node.fills.forEach(fill => {
      if (fill.type === 'SOLID') {
        const hex = rgbToHex(fill.color);
        styles.colors = styles.colors || [];
        if (!styles.colors.includes(hex)) {
          styles.colors.push(hex);
        }
      }
    });
  }
  
  // Extract text styles
  if (node.style) {
    styles.typography = styles.typography || [];
    styles.typography.push({
      fontFamily: node.style.fontFamily,
      fontSize: node.style.fontSize,
      fontWeight: node.style.fontWeight,
      lineHeight: node.style.lineHeightPx
    });
  }
  
  // Recurse
  node.children?.forEach(child => extractAllStyles(child, styles));
  
  return styles;
}
```

### Issue: Tool-Specific Formatting

**Problem:** Different tools require different prompt formats  
**Solution:** Use template system with tool-specific processors

```javascript
const toolProcessors = {
  lovable: (context) => `
# React App Requirements
${context}

Generate with:
- Vite + React 18
- Tailwind CSS
- Component composition
  `,
  
  figmamake: (context) => `
# HTML Prototype
${context}

Output:
- Semantic HTML5
- Vanilla CSS (no preprocessors)
- Minimal JavaScript
  `,
  
  pencil: (context) => `
# Production Component
${context}

Include:
- TypeScript types
- Prop validation
- Accessibility
- Tests
  `
};

const finalPrompt = toolProcessors[targetTool](designContext);
```

## Performance Benchmarks

- **Prompt size reduction:** 91-97% (from 500-1500 tokens → ~45 tokens)
- **Execution cost:** -18% (from ~40,782 → ~33,508 tokens)
- **Validation flow:** ~90 tokens total (initial + corrections)

## Best Practices

1. **Always use structured text context** over frame attachments
2. **Include validation URLs** for iterative refinement
3. **Extract design tokens** separately for reusability
4. **Test prompts** with minimal examples before full designs
5. **Version control prompts** alongside design files
6. **Document tool-specific quirks** in template comments

## Resources

- [Figma API Documentation](https://www.figma.com/developers/api)
- [Lovable Documentation](https://lovable.dev/docs)
- [Figma Make Guide](https://help.figma.com/hc/en-us/articles/360055203533-Use-Make-prototype)
- Author: Roy Villasana (royvillasana@gmail.com)
