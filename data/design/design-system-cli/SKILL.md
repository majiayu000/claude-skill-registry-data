---
name: design-system-cli
description: Complete Design System Reverse Engineering (DSRE) + Functional Cloning CLI - Extract visual design (tokens, assets) AND functional behavior (workflows, state machines, business rules) from any web application
license: MIT
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# Design System CLI Skill

Complete reverse engineering toolkit for cloning BOTH the visual design AND functional behavior of web applications.

## Overview

The design-system-cli provides two complementary capabilities:

### Part A: Visual Cloning (Phases 1-8)
1. **Design Tokens**: Colors, typography, spacing, border-radius, shadows, breakpoints
2. **Visual Assets**: Images, videos, SVG icons, background images with metadata
3. **Asset Prompts**: LLM-ready prompts for recreating extracted visual assets
4. **Component Generation**: React components from HTML structure
5. **Hard Fork & Rebrand**: Transform sites into legally clean templates

### Part B: Functional Cloning (Phases 9-12)
1. **Interaction Recording**: Capture user sessions with clicks, typing, network calls
2. **Flow Extraction**: Identify screens and user journeys
3. **Entity Inference**: Extract data models from API payloads
4. **Business Rules**: State machines, validation rules, permissions
5. **App Generation**: Generate working Next.js applications from behavioral data

**Result**: Clone BOTH the look AND behavior of any web application

## Core Capabilities

### Part A: Visual Cloning (Phases 1-8)

#### 1. Design Token Extraction

**Command**: `ds pipeline --url <url> --framework <framework>`

**Frameworks Supported**:
- `react-tailwind` - Tailwind CSS config for React
- `vue-tailwind` - Tailwind CSS config for Vue
- `react-mui` - Material-UI theme for React
- `angular-material` - Angular Material theme
- `css-variables` - Plain CSS custom properties

**Output Files**:
- `raw-tokens.json` - Raw extracted tokens
- `normalized-tokens.json` - Normalized design system
- `<framework>.config.js` - Framework-specific config

**Example**:
```bash
ds pipeline --url https://labs.google/aifuturesfund/ --framework react-tailwind
```

#### 2. Visual Asset Extraction

**Command**: `ds pipeline --url <url> --assets-out <path>`

**Extracts**:
- Images (`<img>` tags) with dimensions, alt text, aspect ratio
- Videos (`<video>` tags) with dimensions, controls, autoplay state
- SVG icons and illustrations
- Background images from computed styles
- Dominant colors from each asset

**Asset Metadata**:
- `id`: Unique identifier (img-1, video-1, svg-1, bg-1)
- `type`: image | video | icon | illustration | animation
- `role`: hero | thumbnail | avatar | background | decoration | content
- `src`: Asset URL
- `alt`: Alternative text (images only)
- `aspectRatio`: Width:height ratio (16:9, 1:1, etc.)
- `dominantColors`: Array of prominent colors
- `dimensions`: {width, height} in pixels

**Output**:
```json
{
  "page": "https://example.com",
  "capturedAt": "2025-11-19T13:18:46.363Z",
  "assets": [
    {
      "id": "img-1",
      "type": "image",
      "role": "hero",
      "src": "https://example.com/hero.webp",
      "alt": "Hero image description",
      "aspectRatio": "16:9",
      "dominantColors": ["#1a73e8", "#ffffff"],
      "dimensions": {"width": 1920, "height": 1080}
    }
  ]
}
```

#### 3. Asset Prompt Generation

**Command**: `ds assets-prompts --assets <assets.json> --out <asset-prompts.json>`

**Generates LLM-ready prompts** for image recreation via fal-ai models:

**Output Format**:
```json
{
  "page": "https://example.com",
  "items": [
    {
      "id": "img-1",
      "type": "image",
      "target_model": "fal-ai/image",
      "prompt": "TODO: describe hero for https://example.com",
      "negative_prompt": "text, watermark, logos, UI chrome",
      "guidance": {
        "aspect_ratio": "16:9",
        "color_palette": ["#1a73e8", "#ffffff"],
        "style_notes": "role: hero",
        "role": "hero"
      }
    }
  ]
}
```

**Workflow**:
1. Extract assets with `ds pipeline --assets-out assets.json`
2. Generate prompts with `ds assets-prompts --assets assets.json --out asset-prompts.json`
3. Review and enhance prompts with asset context
4. Use prompts with fal-ai image generation models
5. Replace original assets with AI-generated versions

#### 4. Figma Integration

**Command**: `ds figma --tokens <normalized-tokens.json> --out <figma-plugin/>`

**Generates** a ready-to-use Figma plugin with:
- Color styles from token palette
- Text styles from typography tokens
- Interactive UI for import confirmation
- Complete manifest.json configuration

**Plugin Usage**:
1. Generate plugin: `ds figma --tokens normalized-tokens.json`
2. Load plugin in Figma: Plugins → Development → Import from manifest
3. Run plugin to import design tokens as Figma styles

---

### Part B: Functional Cloning (Phases 9-12)

Clone the **behavior and workflows** of applications, not just the visual design.

#### 5. Interaction Recording (Phase 9)

**Command**: `ds trace --url <url> --out trace.json --duration <ms>`

**Captures**:
- User interactions (clicks, typing, navigation, scrolls)
- Network requests and responses with full payloads
- DOM snapshots at each screen transition
- Form submissions and API calls
- Session replay data

**Output**: `trace.json` with complete interaction history

**Example**:
```bash
ds trace --url https://gradual.com --out gradual-trace.json --duration 30000
```

**Use Cases**:
- Record user workflows for analysis
- Document complex application flows
- Capture API contracts and data models
- Build behavioral test suites

#### 6. Flow Extraction (Phase 10)

**Command**: `ds flows --trace <trace.json> --out-screens <screens.json> --out-flows <flows.json>`

**Extracts**:
- Distinct screens from DOM snapshots
- User journeys and navigation patterns
- Screen transition triggers
- Flow confidence scoring

**Outputs**:
- `screens.json` - Unique screens with metadata
- `flows.json` - User journeys with step-by-step actions

**Example**:
```bash
ds flows --trace gradual-trace.json --out-screens screens.json --out-flows flows.json
```

**Use Cases**:
- Map application navigation structure
- Document user journeys
- Identify key user paths
- Analyze flow complexity

#### 7. Entity Inference (Phase 11)

**Command**: `ds entities --trace <trace.json> --out entities.json`

**Infers**:
- Data models from network payloads
- Field types and schemas (string, number, boolean, date-time, array, object)
- Required vs optional fields
- CRUD operations per entity
- Field relationships and metadata

**Output**: `entities.json` with complete data model

**Example**:
```bash
ds entities --trace gradual-trace.json --out entities.json
```

**Use Cases**:
- Reverse engineer database schemas
- Document API contracts
- Generate TypeScript types
- Build data models for new systems

#### 8. Business Rules Extraction (Phase 12)

**Command**: `ds rules --trace <trace.json> --flows <flows.json> --entities <entities.json> --out rules.json`

**Extracts**:
- State machines from entity status fields
- State transitions from user flows
- Validation rules from field types and API errors
- Permission rules from CRUD operation patterns
- Business rules for workflows and immutability

**Output**: `rules.json` with complete rule system

**Example**:
```bash
ds rules \
  --trace gradual-trace.json \
  --flows flows.json \
  --entities entities.json \
  --out rules.json
```

**Rule Types**:
- **State Machines**: Lifecycle states and transitions (draft → active → archived)
- **Validation Rules**: Field constraints (required, email, max:500, min:3)
- **Permission Rules**: Authorization requirements (create, update, delete, approve)
- **Business Rules**: Workflow logic and field immutability

#### 9. Functional App Generation (Phase 12)

**Command**: `ds fx-codegen --screens <screens.json> --flows <flows.json> --entities <entities.json> --rules <rules.json> --out <dir>`

**Generates**:
- Complete Next.js 14 application with App Router
- Typed API clients for each entity
- List and detail pages for all entities
- TypeScript types from entity schemas
- React components with validation
- README with functionality spec

**Output**: Working Next.js application

**Example**:
```bash
ds fx-codegen \
  --screens screens.json \
  --flows flows.json \
  --entities entities.json \
  --rules rules.json \
  --out apps/gradual-clone
```

**Generated Structure**:
```
apps/gradual-clone/
├── app/
│   ├── layout.tsx          # App shell with navigation
│   ├── [entity]s/
│   │   ├── page.tsx       # List page
│   │   └── [id]/page.tsx  # Detail page
├── lib/
│   ├── types.ts           # TypeScript types from entities
│   └── api/
│       └── [entity]s.ts   # CRUD API clients
├── package.json           # Next.js 14 dependencies
└── README.md             # Functionality spec
```

## Complete Workflows

### Workflow 1: Complete Functional Clone (Phases 9-12)

**Goal**: Clone an entire SaaS application (like Gradual, Linear, or Notion)

```bash
# Step 1: Record user interactions (30 seconds)
ds trace --url https://gradual.com --out gradual-trace.json --duration 30000

# Step 2: Extract screens and user flows
ds flows --trace gradual-trace.json --out-screens gradual-screens.json --out-flows gradual-flows.json

# Step 3: Infer data models from API calls
ds entities --trace gradual-trace.json --out gradual-entities.json

# Step 4: Extract business rules and state machines
ds rules \
  --trace gradual-trace.json \
  --flows gradual-flows.json \
  --entities gradual-entities.json \
  --out gradual-rules.json

# Step 5: Generate working Next.js application
ds fx-codegen \
  --screens gradual-screens.json \
  --flows gradual-flows.json \
  --entities gradual-entities.json \
  --rules gradual-rules.json \
  --out apps/gradual-clone

# Step 6: Run the cloned application
cd apps/gradual-clone
npm install
npm run dev  # http://localhost:3000
```

**Result**: Complete working application with:
- All screens and navigation
- Full data models and TypeScript types
- State machines and lifecycle management
- Validation rules and permissions
- CRUD operations and API clients

### Workflow 2: Combined Visual + Functional Clone

**Goal**: Clone BOTH the look AND behavior of an application

```bash
# Part A: Visual Cloning
ds pipeline --url https://example.com --framework react-tailwind --assets-out assets.json
ds assets-prompts --assets assets.json --out asset-prompts.json

# Part B: Functional Cloning
ds trace --url https://example.com --out trace.json --duration 30000
ds flows --trace trace.json --out-screens screens.json --out-flows flows.json
ds entities --trace trace.json --out entities.json
ds rules --trace trace.json --flows flows.json --entities entities.json --out rules.json
ds fx-codegen --screens screens.json --flows flows.json --entities entities.json --rules rules.json --out apps/full-clone

# Part C: Merge Results
# Copy visual assets into functional app
cp -r design-system/* apps/full-clone/
# Use generated Tailwind config
cp tailwind.config.js apps/full-clone/

# Run complete clone
cd apps/full-clone
npm install
npm run dev
```

**Result**: Pixel-perfect visual clone with complete functional behavior

## Use Cases

### Visual Cloning Use Cases

#### Full Design System Extraction
```bash
# Extract everything from a website
ds pipeline --url https://example.com --framework react-tailwind --assets-out assets.json

# Generate asset recreation prompts
ds assets-prompts --assets assets.json --out asset-prompts.json

# Generate Figma plugin
ds figma --tokens normalized-tokens.json --out figma-plugin/
```

### Functional Cloning Use Cases

#### Clone SaaS Application Workflows
```bash
# Record and clone key user journeys
ds trace --url https://linear.app --out linear-trace.json
ds flows --trace linear-trace.json --out-screens screens.json --out-flows flows.json
ds fx-codegen --screens screens.json --flows flows.json --entities entities.json --rules rules.json --out apps/linear-clone
```

**Use Cases**:
- Recreate project management workflows (Linear, Asana, Jira)
- Clone CRM functionality (Salesforce, HubSpot)
- Reverse engineer SaaS features for competitive analysis
- Build similar apps with custom branding

#### Document Legacy Applications
```bash
# Record enterprise application behavior
ds trace --url https://sap-system.company.com --out sap-trace.json
ds flows --trace sap-trace.json --out-screens sap-screens.json --out-flows sap-flows.json
ds entities --trace sap-trace.json --out sap-entities.json
```

**Use Cases**:
- Document undocumented legacy systems
- Extract business rules from old applications
- Modernize legacy workflows
- Create training materials and documentation

#### Extract API Contracts
```bash
# Capture all API calls and payloads
ds trace --url https://api-driven-app.com --out api-trace.json
ds entities --trace api-trace.json --out api-entities.json
```

**Use Cases**:
- Reverse engineer API specifications
- Generate TypeScript types from live APIs
- Document third-party integrations
- Build API client libraries

#### Asset Recreation Workflow
```bash
# 1. Extract visual assets with metadata
ds pipeline --url https://example.com --assets-out assets.json

# 2. Generate LLM-ready prompts
ds assets-prompts --assets assets.json --out asset-prompts.json

# 3. Review asset-prompts.json and enhance TODO prompts with descriptions
# Example: Change "TODO: describe hero for https://example.com"
#       To: "Modern abstract geometric pattern in blue and white, minimalist design, hero banner"

# 4. Use enhanced prompts with fal-ai for image generation
# 5. Replace original assets with AI-generated versions in your codebase
```

### Token-Only Extraction
```bash
# Extract design tokens without assets
ds extract --url https://example.com --out raw-tokens.json
ds normalize --raw raw-tokens.json --out normalized-tokens.json
ds codegen --normalized normalized-tokens.json --framework react-tailwind
```

## Integration with SuperClaude

### Auto-Activation Keywords

**Visual Cloning**:
- design system, extract tokens, recreate page
- Tailwind config, MUI theme, component library
- design tokens, Figma, design analysis
- visual assets, asset recreation, image generation
- fal-ai, asset prompts, regenerate images

**Functional Cloning**:
- clone application, reverse engineer, extract workflows
- trace interactions, record behavior, user flows
- state machine, business rules, validation rules
- data models, API contracts, TypeScript types
- functional clone, behavior extraction, workflow analysis

### File Pattern Detection
- `tailwind.config.*`, `theme.*`, `tokens.*`
- `*.design.json`
- `assets.json`, `asset-prompts.json`
- `trace.json`, `flows.json`, `entities.json`, `rules.json`
- `screens.json`

### Typical Operations

**Visual Operations**:
- `extract` - Extract raw design tokens from website
- `normalize` - Normalize tokens to standard format
- `generate` - Generate framework-specific configs
- `analyze` - Analyze design system consistency
- `recreate` - Recreate page with extracted design system
- `regenerate_assets` - Regenerate visual assets with AI
- `create_prompts` - Create LLM-ready asset prompts

**Functional Operations**:
- `trace` - Record user interactions and network calls
- `extract_flows` - Extract screens and user journeys
- `infer_entities` - Infer data models from API calls
- `extract_rules` - Extract business rules and state machines
- `generate_app` - Generate functional Next.js application
- `clone_behavior` - Clone application workflows
- `document_system` - Document legacy application behavior

### Command Integration

**Visual Cloning**:
- `/build` + design-system-cli → Extract and generate configs
- `/analyze` + design-system-cli → Analyze design consistency
- `/improve` + design-system-cli → Enhance design system
- `/design` + design-system-cli → Design system workflows

**Functional Cloning**:
- `/analyze` + design-system-cli → Analyze application workflows
- `/document` + design-system-cli → Document application behavior
- `/build` + design-system-cli → Generate functional clone
- `/troubleshoot` + design-system-cli → Debug workflow extraction

## Asset Context Schema

Complete schema documentation: `docs/asset_context_schema.md`

**Core Types**:
- `Asset`: Individual visual asset with metadata
- `AssetContext`: Complete collection of assets from a page
- `AssetPromptEntry`: LLM-ready prompt for asset recreation
- `AssetPromptsFile`: Collection of prompts for all assets

**Asset Roles** (auto-detected):
- `hero`: Large prominent images in header/hero sections
- `thumbnail`: Small preview images in grids/lists
- `avatar`: Profile pictures and user avatars
- `background`: Background images and patterns
- `decoration`: Icons, illustrations, SVG graphics
- `content`: Main content images and media

## Architecture

**Monorepo Structure**:
```
packages/
# Visual Cloning (Phases 1-8)
├── core/                   # Shared TypeScript interfaces
├── extractor/              # Playwright-based token and asset extraction
├── normalizer/             # Token normalization and standardization
├── codegen/                # Framework config generation + asset prompt generation
├── figma-bridge/           # Figma plugin generation

# Functional Cloning (Phases 9-12)
├── functional-trace/       # User interaction and network recording
├── functional-flows/       # Screen and flow extraction
├── functional-entities/    # Data model inference from APIs
├── functional-rules/       # Business rules and state machine extraction
└── functional-codegen/     # Next.js application scaffold generation
```

**Complete Processing Pipeline**:
```
VISUAL CLONING:
Website → Playwright → Raw Extraction → Normalization → Code Generation
                    ↓
                Assets.json → Asset Prompts → fal-ai → Regenerated Assets

FUNCTIONAL CLONING:
Website → User Interaction → Trace Recording → Flow Extraction
                                             ↓
                                    Entity Inference → Rules Extraction
                                             ↓
                                    Next.js App Generation

COMBINED:
Visual Design System + Functional Application = Complete Clone
```

## Examples

### Example 1: Extract from Google AI Futures Fund
```bash
ds pipeline --url https://labs.google/aifuturesfund/ --framework react-tailwind --assets-out assets.json
```

**Output**:
- `tailwind.config.js` with extracted color palette, typography, spacing
- `assets.json` with 92 visual assets (images, videos, SVGs)

### Example 2: Generate Asset Recreation Prompts
```bash
ds assets-prompts --assets assets.json --out asset-prompts.json
```

**Output**:
- `asset-prompts.json` with 92 LLM-ready prompts for fal-ai

### Example 3: Full Workflow
```bash
# Extract design system and assets
ds pipeline --url https://carbondesi

gnsystem.com --framework react-tailwind --assets-out carbon-assets.json

# Generate asset prompts
ds assets-prompts --assets carbon-assets.json --out carbon-prompts.json

# Generate Figma plugin
ds figma --tokens normalized-tokens.json --out figma-plugin/

# Result:
# - tailwind.config.js (design tokens)
# - carbon-assets.json (92 assets with metadata)
# - carbon-prompts.json (LLM-ready recreation prompts)
# - figma-plugin/ (ready-to-use Figma plugin)
```

## Known Limitations

1. **Asset Extraction**:
   - SVG className handling (fixed with getClassName() helper)
   - Background images only from computed styles
   - No lazy-loaded image detection

2. **Prompt Generation**:
   - Generic TODO placeholders require manual enhancement
   - No automatic prompt quality assessment
   - Single target model (fal-ai/image)

3. **Token Extraction**:
   - JavaScript-rendered content requires headless browser
   - Dynamic CSS-in-JS may be missed
   - Some design tokens may be inferred incorrectly

## Testing

**E2E Test**:
```bash
# Full pipeline test with real website
node bin/ds pipeline --url https://labs.google/aifuturesfund/ --framework react-tailwind --assets-out test-assets.json

# Verify outputs
ls -lh tailwind.config.js test-assets.json

# Generate and verify prompts
node bin/ds assets-prompts --assets test-assets.json --out test-prompts.json
ls -lh test-prompts.json
```

## Documentation

- `README.md` - Project overview and getting started
- `docs/asset_context_schema.md` - Complete asset schema documentation
- `SKILL.md` - This file (SuperClaude integration guide)

## Contributing

When enhancing this skill:
1. Update SKILL.md with new capabilities
2. Add examples for new workflows
3. Update ORCHESTRATOR.md keywords if needed
4. Maintain backward compatibility with existing outputs

## Resources

- **GitHub**: (Repository URL)
- **Documentation**: `docs/`
- **Examples**: See Examples section above
- **fal-ai Models**: https://fal.ai/models (for asset recreation)
