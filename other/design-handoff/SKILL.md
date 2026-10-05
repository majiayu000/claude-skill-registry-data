---
name: design-handoff
displayName: Design Handoff
tagline: Streamline design-to-development handoff with specs, assets, and component documentation.
description: |
  Facilitates the design-to-development handoff process. Extracts design
  specs from Figma, generates component documentation, exports assets,
  and creates implementation checklists. Ensures developers have all
  the information they need to build pixel-perfect implementations.
department:
  - Design
  - Engineering
  - Product
use_cases:
  - Design Handoff
  - Component Documentation
  - Development Workflow
tools_required:
  - Figma MCP
  - Slack MCP
agents_compatible:
  - Claude / Claude Code
  - Cursor
  - Windsurf
  - ChatGPT
  - Any MCP-compatible agent
author: Webrix
verified: true
updatedAt: 2026-05-08
version: 1.0.0
exampleInput: |
  Create a design handoff for the new pricing page redesign.
  Include component specs, spacing, and responsive breakpoints.
exampleOutput: |
  Design Handoff — Pricing Page Redesign

  COMPONENTS
  1. PricingCard
     Dimensions: 320x480px (desktop), 100% width (mobile)
     Border Radius: 16px
     Shadow: 0 4px 24px rgba(0,0,0,0.08)
     States: default, hover (+2px elevation), selected (green border)

  2. PricingToggle
     Type: pill toggle (Monthly/Annual)
     Annual discount badge: "-20%"

  3. FeatureList
     Row height: 48px
     Check icon: 20x20px, color: #10B981

  SPACING
  Card gap: 24px (desktop), 16px (mobile)
  Section padding: 80px top, 64px bottom
  Container max-width: 1200px

  BREAKPOINTS
  Desktop: >1024px (3 columns)
  Tablet: 768-1024px (2 columns)
  Mobile: <768px (1 column, stacked)

  ASSETS EXPORTED: 12 icons, 3 illustrations
---

# Design Handoff

Streamline design-to-development handoff with specs, assets, and component documentation.

**Integrations:** Figma, Slack

## When to Use

- A design is ready for development implementation
- Developers need component specs and design tokens
- The user mentions "design handoff", "dev handoff", or "implementation specs"

## Steps

### Step 1: Extract Specs

Pull component dimensions, colors, typography, and spacing from Figma.

### Step 2: Document Components

Create component documentation with states and variants.

### Step 3: Export Assets

Export icons, illustrations, and other assets for development.

### Step 4: Create Checklist

Generate an implementation checklist for the development team.

## Output

Deliver:
- Component specification document
- Exported design assets
- Implementation checklist
- Responsive breakpoint guide
