---
name: figma-design-workflow
description: Generate Figma mockups from wrangler specifications with hierarchical file structure and approval tracking
---

# Figma Design Workflow

## Skill Usage Announcement

**MANDATORY**: When using this skill, announce it at the start with:

```
🔧 Using Skill: figma-design-workflow | [brief purpose based on context]
```

**Example:**
```
🔧 Using Skill: figma-design-workflow | [Provide context-specific example of what you're doing]
```

This creates an audit trail showing which skills were applied during the session.



Generate production-ready Figma mockups from wrangler specifications using a hierarchical design system architecture. Creates master design system file plus child feature files, tracks approval status in wrangler metadata, and establishes verification baselines for implementation.

## Overview

This skill bridges the gap between specification and implementation by generating visual mockups that capture UI requirements. It parses wrangler specifications to extract pages, components, and user flows, then creates Figma frames using design system tokens and components.

**Key Capabilities:**
- Read specifications from wrangler MCP issues
- Parse UI requirements (pages, components, flows, interactions)
- Generate Figma frames using design system as library
- Hierarchical structure: master design system + child feature files
- Iterative refinement based on user feedback
- Approval tracking in wrangler metadata
- Sets verification baseline for implementation

**Hierarchical File Structure:**
```
Project Design System (master file)
├── Design Tokens (colors, typography, spacing)
├── Base Components (buttons, inputs, cards)
└── Component Variants (states, sizes, themes)

Feature: Dashboard (child file)
├── Links to: Project Design System (library)
├── Dashboard Page Frame
├── Widget Components (using system components)
└── User Flow Annotations

Feature: User Profile (child file)
├── Links to: Project Design System (library)
├── Profile Page Frame
├── Settings Modal (using system components)
└── User Flow Annotations
```

## When to Use

**Auto-trigger scenarios:**
- Specification contains UI requirements (pages, screens, components)
- Implementation plan creation for frontend work
- User explicitly requests mockups or design review

**Manual invocation:**
- User asks to "create mockups" or "design screens"
- During specification review phase
- Before starting frontend implementation
- When refining UX flows

**When NOT to use:**
- Backend/API specifications with no UI
- Pure data model specifications
- Specifications with approved mockups already (check metadata first)

## Prerequisites

### Required

1. **Design system must exist** - Run design-system-setup if missing:
   ```typescript
   // Check for design system
   const designSystem = await mcp__plugin_wrangler_wrangler_mcp__issues_search({
     query: "design system",
     filters: { labels: ["design-system"] }
   });

   if (designSystem.issues.length === 0) {
     // Invoke design-system-setup skill
     // This skill CANNOT proceed without design system
   }
   ```

2. **Figma MCP server configured** in `.claude-plugin/plugin.json`

3. **Figma personal access token** set in environment

4. **Wrangler specification** exists and contains UI requirements

### Optional

- Existing mockups to iterate on
- User flows or wireframes for reference
- Brand guidelines for visual refinement

## Workflow

### Phase 1: Specification Analysis

**1.1 Fetch Specification**

Read the wrangler specification:

```typescript
// User provides spec ID or search for it
const spec = await mcp__plugin_wrangler_wrangler_mcp__issues_get({
  id: specificationId
});

// Validate it's a specification
if (spec.type !== "specification") {
  throw new Error("Issue must be type 'specification'");
}

// Check if mockups already exist and are approved
const metadata = spec.wranglerContext;
if (metadata?.figmaFileUrl && metadata?.approvalStatus === "approved") {
  // Ask user if they want to iterate or skip
  const shouldIterate = await AskUserQuestion({
    questions: [{
      question: "This specification has approved mockups. What would you like to do?",
      header: "Existing Mockups",
      multiSelect: false,
      options: [
        {
          label: "Iterate on existing",
          description: "Refine the current mockups based on new feedback or requirements"
        },
        {
          label: "Skip mockup creation",
          description: "Use the existing approved mockups as-is"
        },
        {
          label: "Start fresh",
          description: "Create new mockups from scratch (previous ones will be archived)"
        }
      ]
    }]
  });
}
```

**1.2 Parse UI Requirements**

Extract structured UI requirements from specification text:

```typescript
// Parse specification description for UI elements
const uiRequirements = parseUIRequirements(spec.description);

interface UIRequirements {
  pages: Array<{
    name: string;
    description: string;
    sections: string[];
    interactions: string[];
  }>;

  components: Array<{
    name: string;
    type: string; // button, input, card, modal, etc.
    variants: string[];
    states: string[];
  }>;

  userFlows: Array<{
    name: string;
    steps: string[];
    entryPoint: string;
    exitPoint: string;
  }>;

  interactions: Array<{
    trigger: string;
    action: string;
    feedback: string;
  }>;

  dataDisplayed: Array<{
    type: string; // table, chart, list, etc.
    fields: string[];
    operations: string[]; // sort, filter, search, etc.
  }>;
}
```

**Parsing Strategies:**

**Identify Pages/Screens:**
```typescript
// Look for section headers, explicit mentions
// Patterns: "Dashboard page", "User Profile screen", "Settings view"
const pagePatterns = [
  /###?\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:Page|Screen|View)/gi,
  /\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+page\b/gi,
  /The\s+([a-z]+(?:\s+[a-z]+)*)\s+screen/gi
];

// Extract page structure
pages.forEach(page => {
  // Look for sections: "The dashboard includes..."
  const sections = extractSections(pageDescription);

  // Look for interactions: "Users can click...", "On hover..."
  const interactions = extractInteractions(pageDescription);
});
```

**Identify Components:**
```typescript
// Component mentions: buttons, inputs, cards, modals, etc.
const componentPatterns = [
  /\b(primary|secondary|tertiary)?\s*(button|input|card|modal|dropdown|checkbox|radio|toggle)\b/gi,
  /\b([A-Z][a-z]+)\s+component\b/gi
];

// Extract variants
// "Primary button in blue, secondary button in gray"
// "Large cards, small cards, compact cards"
const variantPatterns = [
  /(small|medium|large|compact|expanded)/gi,
  /(primary|secondary|tertiary|success|warning|error)/gi
];

// Extract states
// "Disabled state", "loading state", "hover effect"
const statePatterns = [
  /(disabled|enabled|loading|active|inactive|hover|focus|pressed)/gi
];
```

**Identify User Flows:**
```typescript
// Multi-step processes
// "User logs in → views dashboard → clicks widget → sees details"
// "1. User selects item 2. Confirms action 3. Sees success message"
const flowPatterns = [
  /(?:User|They)\s+([^→]+)(?:→([^→]+))+/gi,
  /\d+\.\s+([^\n]+)/gi
];

// Entry/exit points
// "Starts from login page", "Ends at confirmation screen"
const entryExitPatterns = [
  /(?:start|begin)s?\s+(?:from|at)\s+([^\n.,]+)/gi,
  /(?:end|finish)s?\s+(?:at|with)\s+([^\n.,]+)/gi
];
```

**Identify Data Display:**
```typescript
// Tables, charts, lists
// "Table showing user data with columns: name, email, status"
// "Bar chart of revenue by month"
const dataPatterns = [
  /(table|chart|graph|list)\s+(?:showing|displaying|of)\s+([^\n.]+)/gi,
  /columns?:\s*([^\n.]+)/gi,
  /(pie|bar|line|scatter)\s+chart/gi
];

// Operations
// "Sortable by date", "Filterable by status", "Searchable by name"
const operationPatterns = [
  /(sortable|sort|sorted)\s+by\s+([^\n.,]+)/gi,
  /(filterable|filter|filtered)\s+by\s+([^\n.,]+)/gi,
  /(searchable|search)\s+(?:by|for)\s+([^\n.,]+)/gi
];
```

**1.3 Validate Requirements**

Ensure sufficient UI detail exists:

```typescript
// Check if we have enough to create mockups
const validationResult = validateUIRequirements(uiRequirements);

if (validationResult.insufficientDetail) {
  // Ask user for clarification
  const clarifications = await AskUserQuestion({
    questions: [{
      question: `The specification lacks detail in these areas: ${validationResult.missingAreas.join(", ")}. How would you like to proceed?`,
      header: "Missing Details",
      multiSelect: false,
      options: [
        {
          label: "Infer from context",
          description: "Make reasonable assumptions based on similar patterns and standard practices"
        },
        {
          label: "Ask for specifics",
          description: "Pause and request detailed UI requirements from stakeholder"
        },
        {
          label: "Create basic wireframes",
          description: "Generate minimal mockups as a starting point for refinement"
        }
      ]
    }]
  });
}

interface ValidationResult {
  insufficientDetail: boolean;
  missingAreas: string[];
  warnings: string[];
  recommendations: string[];
}
```

### Phase 2: Figma File Setup

**2.1 Verify Design System**

```typescript
// Find design system issue
const designSystem = await mcp__plugin_wrangler_wrangler_mcp__issues_search({
  query: "design system",
  filters: { labels: ["design-system"] }
});

if (designSystem.issues.length === 0) {
  throw new Error("Design system not found. Run design-system-setup skill first.");
}

// Extract design system Figma file
const designSystemMetadata = designSystem.issues[0].wranglerContext;
const designSystemFileUrl = designSystemMetadata.figmaFileUrl;
const designSystemFileKey = extractFileKey(designSystemFileUrl);

// Verify access to design system file
const dsFile = await figma_get_file({
  file_key: designSystemFileKey
});

if (dsFile.error) {
  throw new Error("Cannot access design system file. Check Figma permissions.");
}
```

**2.2 Create Feature File**

```typescript
// Create new Figma file for this feature
const featureName = spec.title.replace(/^SPEC:\s*/i, "");

const featureFile = await figma_create_file({
  name: `Feature: ${featureName}`,
  teamId: dsFile.teamId // Same team as design system
});

const featureFileKey = featureFile.key;
const featureFileUrl = `https://www.figma.com/file/${featureFileKey}`;

// Link design system as library
await figma_enable_library({
  file_key: featureFileKey,
  library_file_key: designSystemFileKey
});
```

**2.3 Set Up File Structure**

```typescript
// Create pages in feature file
const pages = [
  { name: "Cover", description: "Overview and metadata" },
  { name: "Screens", description: "Page mockups" },
  { name: "Components", description: "Feature-specific components" },
  { name: "Flows", description: "User flow diagrams" },
  { name: "Annotations", description: "Design decisions and notes" }
];

for (const page of pages) {
  await figma_create_page({
    file_key: featureFileKey,
    name: page.name
  });
}
```

### Phase 3: Frame Generation

**3.1 Generate Page Frames**

For each page in UI requirements:

```typescript
for (const page of uiRequirements.pages) {
  // Create frame for page
  const frame = await figma_create_frame({
    file_key: featureFileKey,
    page_name: "Screens",
    name: page.name,
    width: 1440,  // Desktop default
    height: 1024,
    backgroundColor: designTokens.colors.neutral[50]
  });

  // Add sections to frame
  let yOffset = 0;
  for (const section of page.sections) {
    const sectionContent = await generateSection(section, designSystemFileKey);

    await figma_add_to_frame({
      file_key: featureFileKey,
      frame_id: frame.id,
      content: sectionContent,
      x: 0,
      y: yOffset
    });

    yOffset += sectionContent.height + 40; // 40px spacing
  }

  // Add interaction annotations
  for (const interaction of page.interactions) {
    await figma_add_annotation({
      file_key: featureFileKey,
      frame_id: frame.id,
      text: interaction,
      type: "interaction"
    });
  }
}
```

**Section Generation Strategy:**

```typescript
async function generateSection(
  sectionDescription: string,
  designSystemFileKey: string
): Promise<FigmaContent> {
  // Parse section type
  const sectionType = inferSectionType(sectionDescription);

  switch (sectionType) {
    case "header":
      return generateHeader(sectionDescription, designSystemFileKey);

    case "navigation":
      return generateNavigation(sectionDescription, designSystemFileKey);

    case "hero":
      return generateHero(sectionDescription, designSystemFileKey);

    case "content-grid":
      return generateContentGrid(sectionDescription, designSystemFileKey);

    case "data-table":
      return generateDataTable(sectionDescription, designSystemFileKey);

    case "form":
      return generateForm(sectionDescription, designSystemFileKey);

    case "footer":
      return generateFooter(sectionDescription, designSystemFileKey);

    default:
      return generateGenericContent(sectionDescription, designSystemFileKey);
  }
}

// Example: Data Table Generation
async function generateDataTable(
  description: string,
  designSystemFileKey: string
): Promise<FigmaContent> {
  // Extract columns from description
  const columns = extractColumns(description);

  // Create table structure
  const table = {
    type: "table",
    columns: columns.map(col => ({
      name: col,
      width: 150,
      alignment: "left"
    })),
    rows: 5, // Sample rows
    style: {
      headerBackground: designTokens.colors.neutral[100],
      rowHoverBackground: designTokens.colors.primary[50],
      borderColor: designTokens.colors.neutral[200]
    }
  };

  // Use design system components for cells
  const tableFrame = await figma_create_table({
    file_key: designSystemFileKey,
    table: table
  });

  return tableFrame;
}
```

**3.2 Generate Components**

For feature-specific components:

```typescript
for (const component of uiRequirements.components) {
  // Check if design system has base component
  const baseComponent = await findDesignSystemComponent(
    designSystemFileKey,
    component.type
  );

  if (baseComponent) {
    // Create variant by extending base
    const variant = await figma_create_variant({
      file_key: featureFileKey,
      page_name: "Components",
      base_component_id: baseComponent.id,
      name: component.name,
      overrides: generateOverrides(component.variants, component.states)
    });
  } else {
    // Create custom component from scratch
    const customComponent = await figma_create_component({
      file_key: featureFileKey,
      page_name: "Components",
      name: component.name,
      // ... component structure
    });
  }
}
```

**3.3 Generate User Flows**

Create flow diagrams on "Flows" page:

```typescript
for (const flow of uiRequirements.userFlows) {
  // Create flow diagram
  const flowDiagram = await figma_create_flow({
    file_key: featureFileKey,
    page_name: "Flows",
    name: flow.name,
    steps: flow.steps.map((step, index) => ({
      number: index + 1,
      description: step,
      screenshot: null // Optional: link to screen frame
    })),
    connections: generateFlowConnections(flow.steps)
  });

  // Add entry/exit annotations
  await figma_annotate_flow({
    file_key: featureFileKey,
    flow_id: flowDiagram.id,
    entryPoint: flow.entryPoint,
    exitPoint: flow.exitPoint
  });
}
```

**3.4 Add Cover Page**

Create overview page with metadata:

```typescript
await figma_create_cover_page({
  file_key: featureFileKey,
  page_name: "Cover",
  content: {
    title: featureName,
    specification: spec.title,
    specificationUrl: `wrangler://issues/${spec.id}`,
    designSystem: designSystemFileUrl,
    created: new Date().toISOString(),
    status: "draft",
    pages: uiRequirements.pages.map(p => p.name),
    components: uiRequirements.components.map(c => c.name),
    flows: uiRequirements.userFlows.map(f => f.name)
  }
});
```

### Phase 4: Review and Refinement

**4.1 Initial Review**

Present mockups to user:

```typescript
// Generate thumbnail previews
const thumbnails = await figma_export_thumbnails({
  file_key: featureFileKey,
  page_names: ["Screens"]
});

// Show to user
console.log(`
Mockups created for specification: ${spec.title}

Figma File: ${featureFileUrl}

Pages Created:
${uiRequirements.pages.map(p => `- ${p.name}`).join('\n')}

Components Created:
${uiRequirements.components.map(c => `- ${c.name}`).join('\n')}

User Flows:
${uiRequirements.userFlows.map(f => `- ${f.name}`).join('\n')}

Please review the mockups in Figma and provide feedback for refinement.
`);
```

**4.2 Gather Feedback**

```typescript
const feedback = await AskUserQuestion({
  questions: [{
    question: "What would you like to refine in the mockups?",
    header: "Refinement",
    multiSelect: true,
    options: [
      {
        label: "Layout adjustments",
        description: "Spacing, alignment, component positioning"
      },
      {
        label: "Component variants",
        description: "Add missing states, sizes, or styles"
      },
      {
        label: "Visual hierarchy",
        description: "Typography, colors, emphasis"
      },
      {
        label: "User flow clarity",
        description: "Improve flow diagrams or interaction notes"
      },
      {
        label: "Approve as-is",
        description: "Mockups are ready for implementation"
      }
    ]
  }]
});
```

**4.3 Iterate**

If refinements requested:

```typescript
if (!feedback.answers.refinement.includes("Approve as-is")) {
  // Invoke frontend-design skill for creative refinement
  console.log(`
Invoking frontend-design skill for visual refinement...

Context:
- Feature file: ${featureFileUrl}
- Design system: ${designSystemFileUrl}
- Refinement areas: ${feedback.answers.refinement.join(", ")}

Please refine the mockups with:
1. Creative polish beyond template defaults
2. Distinctive visual character
3. Production-ready details
  `);

  // After frontend-design makes changes, loop back to review
}
```

**4.4 Approval**

Once user approves:

```typescript
const approvalConfirmed = await AskUserQuestion({
  questions: [{
    question: "Confirm that these mockups are approved as the implementation baseline?",
    header: "Approval",
    multiSelect: false,
    options: [
      {
        label: "Approve",
        description: "Mockups are final and ready for implementation"
      },
      {
        label: "More refinements",
        description: "Continue iterating"
      }
    ]
  }]
});

if (approvalConfirmed.answers.approval === "Approve") {
  // Mark as approved (next phase)
}
```

### Phase 5: Metadata Tracking

**5.1 Update Specification**

Store Figma metadata in wrangler issue:

```typescript
await mcp__plugin_wrangler_wrangler_mcp__issues_update({
  id: spec.id,
  wranglerContext: {
    ...spec.wranglerContext,
    figmaFileUrl: featureFileUrl,
    figmaFileKey: featureFileKey,
    figmaFrameUrls: uiRequirements.pages.map(page => ({
      page: page.name,
      url: `${featureFileUrl}?node-id=${page.frameId}`
    })),
    approvalStatus: "approved",
    approvalDate: new Date().toISOString(),
    verificationBaseline: true
  }
});

// Add label
await mcp__plugin_wrangler_wrangler_mcp__issues_labels({
  operation: "add",
  issueId: spec.id,
  labels: ["mockups-approved", "figma"]
});
```

**5.2 Create Verification Checklist**

Append to specification description:

```typescript
const verificationChecklist = `

---

## Mockup Verification Baseline

**Figma File**: ${featureFileUrl}
**Approved**: ${new Date().toISOString()}

### Implementation Checklist

${uiRequirements.pages.map(page => `
#### ${page.name}

- [ ] Layout matches mockup
- [ ] Components use design system tokens
- [ ] Interactions match specified behavior
- [ ] Responsive breakpoints implemented
- [ ] Accessibility requirements met
`).join('\n')}

### Visual QA

- [ ] Colors match design tokens
- [ ] Typography matches design system
- [ ] Spacing follows design system scale
- [ ] Component states render correctly
- [ ] Hover/focus effects implemented
- [ ] Loading states implemented
- [ ] Error states implemented
`;

await mcp__plugin_wrangler_wrangler_mcp__issues_update({
  id: spec.id,
  description: spec.description + verificationChecklist
});
```

**5.3 Link to Implementation Issues**

If implementation issues exist, link them:

```typescript
// Find related implementation issues
const implIssues = await mcp__plugin_wrangler_wrangler_mcp__issues_search({
  query: spec.title,
  filters: {
    type: ["issue"],
    status: ["open", "in_progress"]
  }
});

// Update each with mockup reference
for (const issue of implIssues.issues) {
  await mcp__plugin_wrangler_wrangler_mcp__issues_update({
    id: issue.id,
    description: issue.description + `\n\n**Design Reference**: ${featureFileUrl}`
  });
}
```

## Integration Points

### Design System Setup Skill

```typescript
// Check for design system before starting
const designSystem = await findDesignSystem();

if (!designSystem) {
  console.log("No design system found. Invoking design-system-setup skill...");
  // Invoke design-system-setup
  // Wait for completion
  // Then continue with this skill
}
```

### Frontend-Design Skill

```typescript
// Use for creative refinement
// Pass context: feature file, design system, refinement areas
// Frontend-design adds polish, distinctive character, production details
```

### Wrangler MCP

**Specification Storage:**
```yaml
---
id: "000042"
title: "SPEC: Dashboard Feature"
type: "specification"
status: "in_progress"
labels: ["frontend", "mockups-approved", "figma"]
wranglerContext:
  figmaFileUrl: "https://www.figma.com/file/xyz789/Feature-Dashboard"
  figmaFileKey: "xyz789"
  figmaFrameUrls:
    - page: "Dashboard Overview"
      url: "https://www.figma.com/file/xyz789/...?node-id=123"
    - page: "Widget Details"
      url: "https://www.figma.com/file/xyz789/...?node-id=456"
  approvalStatus: "approved"
  approvalDate: "2025-11-21T15:30:00.000Z"
  verificationBaseline: true
---
```

**Querying Mockups:**
```typescript
// Find all specs with approved mockups
const specsWithMockups = await mcp__plugin_wrangler_wrangler_mcp__issues_search({
  query: "",
  filters: {
    type: ["specification"],
    labels: ["mockups-approved"]
  }
});
```

### Figma MCP Tools

Key tools used:

**figma_create_file** - Create feature file
**figma_get_file** - Fetch design system
**figma_enable_library** - Link design system as library
**figma_create_page** - Set up file pages
**figma_create_frame** - Generate page mockups
**figma_create_component** - Create feature components
**figma_create_variant** - Extend design system components
**figma_create_flow** - Generate user flow diagrams
**figma_add_annotation** - Add design notes
**figma_export_thumbnails** - Generate previews

## Error Handling

### Missing Design System

```
ERROR: Design system not found.

This skill requires an existing design system to reference components and tokens.

Run design-system-setup skill first:
1. Invoke design-system-setup skill
2. Choose template or Q&A workflow
3. Complete setup
4. Re-run this skill

Or create design system manually:
1. Create Figma file with design tokens
2. Export tokens to code
3. Create wrangler issue with label "design-system"
4. Add figmaFileUrl to wranglerContext
```

### Insufficient UI Detail

```
ERROR: Specification lacks sufficient UI detail for mockup generation.

Missing areas:
- Page layouts not described
- Component requirements unclear
- User flows not specified

Options:
1. Refine specification with more UI detail
2. Create basic wireframes as starting point
3. Schedule design discussion with stakeholder
```

### Figma API Failures

```
ERROR: Failed to create Figma file.

Possible causes:
- Figma API rate limiting
- Invalid access token
- Network connectivity issues

Workaround:
1. Create Figma file manually: https://www.figma.com
2. Link design system as library
3. Update specification metadata with file URL
4. Continue with manual mockup creation
```

### Library Link Failures

```
ERROR: Cannot link design system as library.

This usually means:
- Design system file not published as library
- Insufficient permissions on design system file
- Design system file in different Figma organization

Fix:
1. Open design system file: ${designSystemFileUrl}
2. Click "Publish" in Figma
3. Ensure "Publish as library" is enabled
4. Re-run this skill
```

## Examples

### Example 1: Dashboard Specification

**Input specification:**
```markdown
# Dashboard Feature

## Overview
Users need a dashboard to monitor key metrics and access common actions.

## Pages

### Dashboard Home
- Header with user profile and notifications
- Metric cards showing: active users, revenue, conversions
- Recent activity table with columns: timestamp, user, action, status
- Quick action buttons: Create Report, Export Data

### Metric Details
- Drill-down view when clicking a metric card
- Line chart showing trend over time
- Filters: date range, segment
- Export button

## Components
- Metric Card: displays number, trend (up/down), change percentage
- Data Table: sortable, filterable, paginated
- Action Button: primary (blue), secondary (gray)

## User Flow
1. User lands on Dashboard Home
2. Sees metric cards at top
3. Reviews recent activity in table
4. Clicks metric card to drill down
5. Views detailed chart
6. Applies filters to refine data
7. Exports report
```

**Generated mockups:**

```
File: Feature: Dashboard Feature
Pages:
- Cover (metadata)
- Screens
  - Dashboard Home frame (1440x1024)
    - Header (using design system Header component)
    - 3 Metric Cards (custom variants of Card component)
    - Activity Table (using design system Table component)
    - Action Buttons (using design system Button component)
  - Metric Details frame (1440x1024)
    - Header with back button
    - Line Chart (custom component)
    - Filter Panel (using design system Input components)
    - Export Button (design system Button)
- Components
  - Metric Card (with up/down variants)
- Flows
  - Dashboard Navigation flow (7 steps with connections)
- Annotations
  - Interaction notes on each clickable element
```

### Example 2: User Profile Specification

**Input specification:**
```markdown
# User Profile Feature

## Pages

### Profile View
- Avatar (large, circular)
- User info: name, email, role, joined date
- Bio text area
- Edit Profile button
- Activity timeline

### Edit Profile Modal
- Modal overlay (centered, 600px wide)
- Avatar upload with preview
- Form fields: name, email, bio
- Save and Cancel buttons

## Components
- Avatar: sizes (small 32px, medium 48px, large 96px)
- Timeline Item: icon, timestamp, description

## Interactions
- Click Edit Profile → modal opens
- Upload avatar → preview updates
- Save → modal closes, profile updates
- Cancel → modal closes, no changes
```

**Workflow:**

```
[Fetch specification #042]
✓ Specification found: "SPEC: User Profile Feature"

[Parse UI requirements]
✓ Found 2 pages: Profile View, Edit Profile Modal
✓ Found 2 components: Avatar, Timeline Item
✓ Found 4 interactions

[Verify design system]
✓ Design system found: "Project Design System"
✓ Figma file accessible

[Create feature file]
✓ Created: "Feature: User Profile Feature"
✓ Linked design system as library

[Generate frames]
✓ Profile View frame created
  - Used design system Avatar component (large variant)
  - Created custom Timeline Item component
✓ Edit Profile Modal frame created
  - Used design system Modal component
  - Used design system Form components

[Create components]
✓ Avatar: created 3 size variants
✓ Timeline Item: created component with icon slot

[User review]
Mockups ready for review: https://www.figma.com/file/abc123/...

[Gather feedback]
User requests: "Add hover state to timeline items"

[Invoke frontend-design for refinement]
Frontend-design skill adds:
- Subtle hover effect with background color transition
- Timeline item expansion on hover showing full details
- Micro-interaction animations

[Final approval]
User approves mockups.

[Update metadata]
✓ Updated specification #042
  - figmaFileUrl: https://www.figma.com/file/abc123/...
  - approvalStatus: approved
  - verificationBaseline: true
✓ Added labels: mockups-approved, figma
✓ Appended verification checklist to description

[Link to implementation issues]
✓ Found 3 related issues
✓ Added design reference to each

COMPLETE: Mockups approved and ready for implementation.
```

### Example 3: Iterative Refinement

**Scenario:** Existing mockups need updates based on new requirements

```
User: "Update the Dashboard mockups to include a dark mode toggle"

Agent:
[Fetch specification]
✓ Found spec #038 with existing mockups
✓ Current approvalStatus: approved
✓ Existing Figma file: https://www.figma.com/file/xyz789/...

[Ask user]
Q: This specification has approved mockups. What would you like to do?
A: Iterate on existing

[Parse new requirement]
✓ New requirement: dark mode toggle component

[Update Figma file]
✓ Opened existing file: Feature: Dashboard
✓ Added to Header:
  - Dark mode toggle (using design system Toggle component)
  - Position: top-right, next to notifications
✓ Created dark mode color variants for all frames

[Review]
Updated mockups: https://www.figma.com/file/xyz789/...

User: "Looks good, approve"

[Update metadata]
✓ Updated approvalDate to current timestamp
✓ Incremented version: v1.1
✓ Added changelog note: "Added dark mode toggle"

COMPLETE: Mockups updated and re-approved.
```

## Best Practices

### Specification Parsing

**Do:**
- Look for explicit UI mentions (pages, screens, components)
- Infer structure from section headers and organization
- Extract data fields for tables and forms
- Identify user flows from sequential descriptions
- Use design system components where possible

**Don't:**
- Create mockups without sufficient UI detail
- Guess at complex layouts without clarification
- Ignore existing mockups (check metadata first)
- Create components that duplicate design system

### Frame Organization

**Naming conventions:**
- Pages: "{Feature Name} - {Page Name}" (e.g., "Dashboard - Home")
- Components: "{Feature}/{Component}/{Variant}" (e.g., "Dashboard/MetricCard/Positive")
- Flows: "{Feature} - {Flow Name}" (e.g., "Dashboard - Metric Drill-Down")

**Layer structure:**
- Use Auto Layout for responsive frames
- Group related elements logically
- Name layers descriptively (not "Frame 123")
- Add constraints for responsive behavior

### Design System Usage

**Always:**
- Link design system as library first
- Use design system components as base
- Apply design tokens for colors, typography, spacing
- Create variants, not duplicates

**Never:**
- Copy-paste components from design system
- Hardcode colors or spacing values
- Create custom components for things that exist in design system
- Break away from design system without justification

### Approval Tracking

**Metadata must include:**
- `figmaFileUrl`: Direct link to file
- `figmaFrameUrls`: Links to specific frames
- `approvalStatus`: "draft", "review", "approved"
- `approvalDate`: ISO timestamp
- `verificationBaseline`: true/false

**Labels:**
- `figma`: All mockup issues
- `mockups-approved`: Approved baselines
- `needs-review`: Awaiting user review
- `iteration-{N}`: Version tracking

### Iteration Workflow

**Version tracking:**
- v1.0: Initial mockups
- v1.1, v1.2, etc.: Minor refinements
- v2.0: Major redesign

**Changelog in description:**
```markdown
## Mockup Changelog

### v1.2 (2025-11-21)
- Added dark mode toggle to header
- Refined metric card hover states

### v1.1 (2025-11-20)
- Updated table column widths
- Added loading state for charts

### v1.0 (2025-11-19)
- Initial mockups created
```

## Verification Checklist

After mockup creation, verify:

- [ ] Design system exists and is accessible
- [ ] Feature file created in Figma
- [ ] Design system linked as library
- [ ] All pages from spec have frames
- [ ] All components from spec created
- [ ] User flows diagrammed on Flows page
- [ ] Cover page includes metadata
- [ ] Annotations added for interactions
- [ ] Thumbnails exported for preview
- [ ] User reviewed mockups
- [ ] Feedback incorporated (if any)
- [ ] User approved mockups
- [ ] Specification metadata updated
- [ ] Labels added: mockups-approved, figma
- [ ] Verification checklist appended to spec
- [ ] Related implementation issues linked

## Future Enhancements

**Planned features:**
- Auto-detect responsive breakpoints from spec
- Generate mobile/tablet variants automatically
- AI-powered layout suggestions
- Component usage analytics (which design system components used most)
- Screenshot-to-mockup (refine existing screenshots)
- Mockup-to-code generation hints
- Design token drift detection (mockup uses colors not in design system)
- Accessibility annotations (contrast ratios, ARIA labels)

## Related Skills

- **design-system-setup**: Create design system foundation (prerequisite)
- **frontend-design**: Creative refinement and polish
- **writing-specifications**: Create detailed UI specifications
- **implement**: Implement mockups in code
- **code-review**: Verify implementation matches mockup baseline

## References

- **Design System Setup**: `/skills/design-workflow/design-system-setup/SKILL.md`
- **Figma MCP Documentation**: https://github.com/modelcontextprotocol/servers/tree/main/src/figma
- **Wrangler MCP Usage**: `/docs/MCP-USAGE.md`
