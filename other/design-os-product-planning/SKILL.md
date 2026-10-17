---
name: design-os-product-planning
description: Use Design OS to guide product planning, data modeling, design systems, and UI design before implementation
triggers:
  - "help me plan my product with Design OS"
  - "set up Design OS for product design"
  - "create a design specification with Design OS"
  - "generate a handoff package for my product"
  - "model my application data and UI"
  - "use Design OS to design my application"
  - "export components from Design OS"
  - "walk through the Design OS process"
---

# Design OS Product Planning Skill

> Skill by [ara.so](https://ara.so) — Design Skills collection.

Design OS is a TypeScript-based product planning and design tool that bridges the gap between product ideas and implementation. It provides a structured, AI-guided process to define product vision, model data, design UI, and export production-ready specifications for coding agents.

## What Design OS Does

Design OS solves the "build first, understand later" problem with AI coding tools by establishing a clear design specification before implementation begins. It guides you through:

1. **Product Planning** - Vision definition, roadmap breakdown, data modeling
2. **Design System** - Color schemes, typography, application shell design
3. **Section Design** - Feature requirements, sample data, screen designs
4. **Export** - Complete handoff packages for implementation

## Installation

### Prerequisites

- Node.js 18+ or Bun runtime
- Git

### Clone and Install

```bash
# Clone the repository
git clone https://github.com/buildermethods/design-os.git
cd design-os

# Install dependencies (npm, yarn, pnpm, or bun)
npm install

# or with bun
bun install
```

### Environment Setup

Create a `.env` file in the project root:

```bash
# Required: Your AI provider API key
ANTHROPIC_API_KEY=your_key_here
# or
OPENAI_API_KEY=your_key_here

# Optional: Customize AI model
AI_MODEL=claude-3-5-sonnet-20241022
```

Reference environment variables in code:

```typescript
const apiKey = process.env.ANTHROPIC_API_KEY;
const model = process.env.AI_MODEL || 'claude-3-5-sonnet-20241022';
```

## Running Design OS

### Start the Application

```bash
# Development mode
npm run dev

# or with bun
bun run dev

# Production build
npm run build
npm start
```

The application will start and guide you through the design process interactively.

## Key Commands and Workflow

### CLI Commands

```bash
# Start a new design project
npm run dev

# Build the project
npm run build

# Run tests
npm test

# Type checking
npm run type-check
```

### The Design Process Flow

Design OS uses a conversational, step-by-step process:

#### 1. Product Planning

Define your product vision and data model:

```typescript
// Example: Defining a product entity
interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  category: string;
  createdAt: Date;
}

// Example: Planning a roadmap feature
const feature = {
  name: "User Dashboard",
  priority: "high",
  status: "planned",
  requirements: [
    "Display user profile information",
    "Show recent activity",
    "Enable quick actions"
  ]
};
```

#### 2. Design System Configuration

Set up your visual design language:

```typescript
// Example: Design system configuration
const designSystem = {
  colors: {
    primary: "#3B82F6",
    secondary: "#8B5CF6",
    accent: "#10B981",
    background: "#F9FAFB",
    text: "#111827"
  },
  typography: {
    fontFamily: "Inter, system-ui, sans-serif",
    scale: {
      h1: "2.5rem",
      h2: "2rem",
      h3: "1.5rem",
      body: "1rem",
      small: "0.875rem"
    }
  },
  spacing: {
    unit: 8, // Base spacing unit in px
    scale: [0, 8, 16, 24, 32, 48, 64]
  }
};
```

#### 3. Section Design

Design individual features and screens:

```typescript
// Example: Section specification
interface SectionSpec {
  name: string;
  description: string;
  requirements: string[];
  dataModel: Record<string, any>;
  screens: Screen[];
}

const dashboardSection: SectionSpec = {
  name: "User Dashboard",
  description: "Main user interface after login",
  requirements: [
    "Show user stats",
    "Display recent items",
    "Provide navigation to key features"
  ],
  dataModel: {
    user: {
      id: "string",
      name: "string",
      email: "string",
      stats: {
        totalItems: "number",
        recentActivity: "Activity[]"
      }
    }
  },
  screens: [
    {
      name: "DashboardHome",
      layout: "grid",
      components: ["Header", "StatsCards", "ActivityFeed"]
    }
  ]
};
```

#### 4. Export and Handoff

Generate implementation-ready specifications:

```typescript
// Example: Export configuration
const exportConfig = {
  format: "typescript-react", // or "vue", "svelte", etc.
  includeTests: true,
  includeStorybook: true,
  outputPath: "./handoff"
};

// Generated component example
interface HandoffComponent {
  path: string;
  code: string;
  tests?: string;
  story?: string;
  dependencies: string[];
}
```

## Data Modeling Patterns

### Entity Definition

```typescript
// Example: E-commerce data model
interface DataModel {
  entities: {
    User: {
      id: string;
      email: string;
      profile: UserProfile;
      orders: Order[];
    };
    Product: {
      id: string;
      name: string;
      price: number;
      inventory: number;
      category: Category;
    };
    Order: {
      id: string;
      userId: string;
      items: OrderItem[];
      status: "pending" | "completed" | "cancelled";
      total: number;
      createdAt: Date;
    };
  };
  relationships: {
    "User.orders": "Order[]";
    "Order.items": "OrderItem[]";
    "Product.category": "Category";
  };
}
```

### Sample Data Generation

```typescript
// Example: Generate sample data for design
const sampleData = {
  users: [
    {
      id: "usr_1",
      name: "Sarah Johnson",
      email: "sarah@example.com",
      role: "admin"
    },
    {
      id: "usr_2",
      name: "Mike Chen",
      email: "mike@example.com",
      role: "user"
    }
  ],
  products: [
    {
      id: "prd_1",
      name: "Premium Widget",
      price: 49.99,
      inventory: 120
    }
  ]
};
```

## Component Export Patterns

### React Component Export

```typescript
// Example: Exported component structure
export interface ExportedComponent {
  name: string;
  props: Record<string, string>;
  children?: string[];
}

// Generated component code
const exportedCode = `
import React from 'react';

interface DashboardProps {
  user: User;
  stats: UserStats;
}

export function Dashboard({ user, stats }: DashboardProps) {
  return (
    <div className="dashboard">
      <Header user={user} />
      <StatsGrid stats={stats} />
      <ActivityFeed userId={user.id} />
    </div>
  );
}
`;
```

### Design Token Export

```typescript
// Example: Export design tokens
const tokens = {
  colors: {
    primary: {
      50: "#EEF2FF",
      500: "#3B82F6",
      900: "#1E3A8A"
    }
  },
  spacing: {
    xs: "0.5rem",
    sm: "1rem",
    md: "1.5rem",
    lg: "2rem",
    xl: "3rem"
  }
};

// Export as CSS variables
const cssVariables = `
:root {
  --color-primary-50: #EEF2FF;
  --color-primary-500: #3B82F6;
  --spacing-xs: 0.5rem;
  --spacing-sm: 1rem;
}
`;
```

## Working with the AI Conversation

### Providing Context

```typescript
// Example: Structuring context for AI
const projectContext = {
  type: "SaaS application",
  target: "B2B productivity tool",
  users: "Teams of 5-50 people",
  keyFeatures: [
    "Project management",
    "Team collaboration",
    "Reporting and analytics"
  ],
  techStack: {
    frontend: "React + TypeScript",
    backend: "Node.js",
    database: "PostgreSQL"
  }
};
```

### Iterating on Designs

The AI guides you through refinements:

1. Initial concept generation
2. Review and feedback
3. Refinement based on requirements
4. Validation against constraints
5. Final approval and export

## Configuration Options

### Project Configuration

```typescript
// designos.config.ts
export default {
  project: {
    name: "My SaaS App",
    version: "1.0.0",
    outputDir: "./design-handoff"
  },
  ai: {
    provider: "anthropic", // or "openai"
    model: process.env.AI_MODEL,
    temperature: 0.7
  },
  export: {
    format: "typescript-react",
    includeTests: true,
    includeDocumentation: true,
    componentLibrary: "shadcn-ui" // optional
  },
  design: {
    responsive: true,
    darkMode: true,
    accessibility: "WCAG-AA"
  }
};
```

## Common Patterns

### Feature Planning Pattern

```typescript
// Define a feature with clear boundaries
interface Feature {
  id: string;
  name: string;
  description: string;
  userStories: string[];
  acceptance: string[];
  dataRequirements: DataEntity[];
  screens: ScreenDesign[];
}

const userAuthFeature: Feature = {
  id: "feat_auth",
  name: "User Authentication",
  description: "Secure user login and registration",
  userStories: [
    "As a user, I can create an account",
    "As a user, I can log in securely",
    "As a user, I can reset my password"
  ],
  acceptance: [
    "Email validation",
    "Password strength requirements",
    "Session management"
  ],
  dataRequirements: [
    {
      entity: "User",
      fields: ["email", "passwordHash", "createdAt"]
    }
  ],
  screens: [
    { name: "Login", type: "form" },
    { name: "Register", type: "form" },
    { name: "ForgotPassword", type: "form" }
  ]
};
```

### Screen Layout Pattern

```typescript
// Define screen layouts with components
interface ScreenLayout {
  name: string;
  layout: "single-column" | "sidebar" | "grid" | "dashboard";
  regions: Region[];
}

const dashboardLayout: ScreenLayout = {
  name: "Dashboard",
  layout: "dashboard",
  regions: [
    {
      id: "header",
      component: "AppHeader",
      position: "top",
      height: "fixed"
    },
    {
      id: "sidebar",
      component: "Navigation",
      position: "left",
      width: "240px"
    },
    {
      id: "main",
      component: "DashboardContent",
      position: "center",
      scroll: true
    }
  ]
};
```

### Data Flow Pattern

```typescript
// Map data flow through the application
interface DataFlow {
  source: string;
  transformations: Transformation[];
  destination: string;
}

const userDataFlow: DataFlow = {
  source: "API:/api/users/{id}",
  transformations: [
    {
      type: "normalize",
      schema: "UserSchema"
    },
    {
      type: "enrich",
      with: "userPreferences"
    }
  ],
  destination: "Component:UserProfile"
};
```

## Troubleshooting

### AI Response Issues

**Problem**: AI generates designs that don't match vision

**Solution**: Provide more specific context and constraints:

```typescript
const constraints = {
  must: [
    "Mobile-first responsive design",
    "Maximum 3 clicks to any feature",
    "Support keyboard navigation"
  ],
  mustNot: [
    "No more than 2 modals deep",
    "Avoid horizontal scrolling",
    "No auto-playing media"
  ],
  preferences: [
    "Minimize form fields",
    "Use progressive disclosure",
    "Provide inline help"
  ]
};
```

### Export Issues

**Problem**: Generated code doesn't match project structure

**Solution**: Configure export templates:

```typescript
// Custom export template
const exportTemplate = {
  componentPath: "./src/components/${category}/${name}.tsx",
  testPath: "./src/components/${category}/__tests__/${name}.test.tsx",
  stylePath: "./src/components/${category}/${name}.module.css",
  imports: {
    react: "import React from 'react';",
    types: "import type { ${name}Props } from './types';",
    styles: "import styles from './${name}.module.css';"
  }
};
```

### Data Model Inconsistencies

**Problem**: Relationships between entities unclear

**Solution**: Use explicit relationship mapping:

```typescript
// Define relationships explicitly
const relationshipMap = {
  User: {
    hasMany: ["Order", "Review"],
    belongsTo: ["Organization"],
    hasOne: ["Profile"]
  },
  Order: {
    belongsTo: ["User"],
    hasMany: ["OrderItem"]
  },
  OrderItem: {
    belongsTo: ["Order", "Product"]
  }
};
```

### Incomplete Specifications

**Problem**: Missing details in handoff package

**Solution**: Use completion checklist:

```typescript
const completionChecklist = {
  productPlanning: {
    vision: true,
    roadmap: true,
    dataModel: true,
    relationships: true
  },
  designSystem: {
    colors: true,
    typography: true,
    spacing: true,
    components: true
  },
  sections: {
    requirements: true,
    sampleData: true,
    screens: true,
    interactions: true
  },
  export: {
    components: true,
    tests: true,
    documentation: true,
    assets: true
  }
};
```

## Best Practices

### Start with Clear Vision

```typescript
// Document your vision clearly
const productVision = {
  problem: "Teams struggle to coordinate across tools",
  solution: "Unified workspace for project management",
  target: "Remote teams of 10-100 people",
  differentiator: "Real-time collaboration with AI assistance",
  success: "Teams reduce coordination time by 50%"
};
```

### Iterate in Phases

Work through each Design OS phase completely before moving forward. Don't skip steps.

### Use Real Data Examples

Provide realistic sample data to inform better designs:

```typescript
const realisticSample = {
  user: {
    name: "Alexandra Martinez",
    email: "alex.martinez@company.com",
    role: "Product Manager",
    team: "Product Team Alpha",
    lastActive: "2024-01-15T14:30:00Z"
  }
};
```

### Document Decisions

Capture why decisions were made:

```typescript
const designDecisions = {
  "dashboard-layout": {
    decision: "Used card-based grid layout",
    reason: "Better scanability for multiple data types",
    alternatives: ["List view", "Kanban board"],
    tradeoffs: "Requires more vertical scrolling"
  }
};
```

## Integration with Coding Agents

Design OS outputs are optimized for AI coding agents:

```typescript
// Handoff package structure for coding agents
interface HandoffPackage {
  specification: {
    overview: string;
    requirements: Requirement[];
    dataModel: DataModel;
    userFlows: UserFlow[];
  };
  design: {
    system: DesignSystem;
    screens: Screen[];
    components: ComponentSpec[];
    interactions: Interaction[];
  };
  implementation: {
    components: ComponentCode[];
    tests: TestCode[];
    types: TypeDefinitions[];
    documentation: string;
  };
  context: {
    decisions: DesignDecision[];
    constraints: Constraint[];
    dependencies: string[];
  };
}
```

When handing off to a coding agent, provide the complete package with clear instructions on implementation priorities.
