---
name: moai-design-tools
description: >
  Design tool integration specialist covering Figma MCP design-context fetching
  and design-to-code implementation. Use when fetching design context from Figma
  or implementing designs as React/Tailwind code.
license: Apache-2.0
compatibility: Designed for Claude Code
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, WebFetch, WebSearch, mcp__context7__resolve-library-id, mcp__context7__get-library-docs
user-invocable: false
metadata:
  version: "5.2.0"
  category: "domain"
  status: "active"
  updated: "2026-10-11"
  modularized: "false"
  tools: "Figma MCP"
  tags: "figma, design to code, design export, react from design, tailwind from design, design context, ui implementation"
  context7-libraries: "/figma/docs"
  related-skills: "moai-domain-uiux, moai-domain-frontend, moai-library-shadcn, moai-lang-typescript, moai-lang-react"

# MoAI Extension: Progressive Disclosure
progressive_disclosure:
  enabled: true
  level1_tokens: 100
  level2_tokens: 5500

# MoAI Extension: Triggers
triggers:
  keywords: ["figma", "design to code", "design export", "react from design", "tailwind from design", "design context", "ui implementation", "design fetching", "figma mcp", "component from design", "layout from design"]
  agents: ["expert-frontend", "team-designer"]
  phases: ["run"]
---

# Design Tools Integration Specialist

Design-to-code workflow guidance centered on Figma MCP (design context fetching, token extraction, and implementation).

## Default Design Style (shadcn/ui Nova)

When no specific design style is requested, use the **shadcn/ui Nova** preset with Notion-style neutral color scheme:

```
bunx --bun shadcn@latest create --preset "https://ui.shadcn.com/init?base=radix&style=nova&baseColor=neutral&theme=neutral&iconLibrary=hugeicons&font=noto-sans&menuAccent=bold&menuColor=default&radius=small&template=next&rtl=false" --template next
```

### Nova Style Configuration

| Property | Value | Description |
|----------|-------|-------------|
| Style | `nova` | Modern, clean design language |
| Base Color | `neutral` | Notion-style grayscale palette |
| Theme | `neutral` | Consistent neutral theming |
| Icon Library | `hugeicons` | Comprehensive icon set |
| Font | `noto-sans` | Clean, readable sans-serif |
| Radius | `small` | Subtle rounded corners |
| Menu Accent | `bold` | Strong menu highlighting |

### When to Use Default Style

Apply the Nova preset when:
- User requests "clean", "modern", or "minimalist" design without specifics
- No brand guidelines or design system specified
- Creating dashboards, admin panels, or productivity tools
- Building documentation or content-focused interfaces

## Quick Tool Selection

### Figma MCP - Design Context and Generation

Official Figma MCP integration via Remote MCP server (https://mcp.figma.com/mcp). Install with: `claude plugin install figma@claude-plugins-official`

Best For: Fetching design context from Figma files, extracting design tokens, generating new designs with Code-to-Canvas (generate_figma_design), accessing FigJam boards, and linking components to code with Code Connect.

Key Strengths: 16 official tools including read (get_design_context, get_variable_defs, get_screenshot, get_metadata), write (use_figma, generate_figma_design, create_new_file), Code Connect (get_code_connect_map, add_code_connect_map, get_code_connect_suggestions, send_code_connect_mappings), FigJam (get_figjam, generate_diagram), design system (search_design_system, create_design_system_rules), and utility (whoami). Write-to-canvas is currently free during beta.

Workflow: Install plugin → get_design_context → get_variable_defs → get_screenshot → Implement design → Verify against screenshot.

Context7 Library: /figma/docs

## Quick Decision Guide

Choose Figma MCP when:
- Need to extract design context from existing Figma files
- Working with designers who use Figma
- Required to fetch design tokens and component specifications
- Need screenshots or visual references from Figma
- Documenting existing design systems

## Common Design-to-Code Patterns

### Universal Patterns

These patterns apply to every design-to-code workflow.

**Design Token Management:**

Figma MCP extracts tokens from existing files; implement them as CSS variables or Tailwind config.

**Component Architecture:**

Figma MCP reads component structure from Figma; preserve that hierarchy in the implemented components.

**Responsive Design:**

Figma MCP extracts responsive variants; implement them with Tailwind responsive classes.

**Style Consistency:**

Figma MCP validates against the design system; apply consistent Tailwind classes derived from design tokens.

### Workflow Best Practices

Applicable to all tools:

**Design System Integration:**
- Define design tokens before starting design work
- Use consistent naming conventions across tools
- Maintain single source of truth for design values
- Document token usage and component patterns

**Version Control:**
- Commit Figma metadata snapshots for reference
- Track design iterations with git
- Document design decisions in code comments

**Collaboration:**
- Use Figma comments for design feedback
- Create pull requests for design changes
- Maintain design documentation alongside code

**Quality Assurance:**
- Validate design tokens against style guide
- Test responsive breakpoints
- Verify accessibility compliance
- Review generated code for optimization

## Tool-Specific Implementation

For detailed tool-specific implementation guidance, see the reference files:

### Figma MCP Implementation

File: reference/figma.md

Covers Figma MCP connection setup, file metadata fetching, component tree extraction, design token retrieval, screenshot capture, and style guide generation.

Key sections: MCP configuration, authentication setup, file access patterns, metadata queries, component hierarchy parsing, token extraction formats, screenshot API usage, design system documentation.

## Navigation Guide

When working with design-to-code features:

1. Start with Quick Tool Selection (above) if choosing a tool
2. Apply Default Nova Style when no style specified
3. Review Common Design-to-Code Patterns for universal concepts
4. Open tool-specific reference file for implementation details
5. Use Context7 tools to access latest tool documentation

## Context7 Documentation Access

Access up-to-date tool documentation using Context7 MCP:

**Figma:**
- Use resolve-library-id with "figma" to get library ID
- Use get-library-docs with topic "mcp", "api", "design-tokens", "metadata"

## Works Well With

- moai-domain-uiux: Design systems and component architecture
- moai-domain-frontend: React implementation patterns
- moai-library-shadcn: shadcn/ui component integration (Nova preset)
- moai-lang-typescript: TypeScript for generated components
- moai-lang-react: React best practices
- moai-foundation-core: SPEC-driven development workflows

---

Status: Active
Version: 5.2.0 (Pencil MCP removed — vendor dependency dropped)
Last Updated: 2026-10-11
Tools: Figma MCP (16 tools, Official Remote Server)
Default Style: shadcn/ui Nova (neutral, noto-sans, small radius)

<!-- moai:evolvable-start id="rationalizations" -->
## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I can implement the design from the screenshot, I do not need Figma context" | Screenshots lose component structure, spacing tokens, and interaction states. Figma MCP provides structured design data. |
| "I will export to code and clean it up" | Generated code is a starting point, not a deliverable. Export without review produces non-semantic, non-accessible markup. |
| "Design tokens are too rigid, I need custom values" | Custom values bypass the design system. Extend tokens through the system, not around it. |
| "I will sync with the designer after implementation" | Post-implementation sync means rework. Sync before implementation means alignment. |

<!-- moai:evolvable-end -->

<!-- moai:evolvable-start id="red-flags" -->
## Red Flags

- Implementation uses hardcoded values instead of design tokens from Figma or the design spec
- Exported code committed without semantic HTML cleanup
- Interaction states (hover, focus, active, disabled) missing from implementation
- Design source updated but implementation not synced
- Design tool export contains absolute positioning that breaks responsive layout

<!-- moai:evolvable-end -->

<!-- moai:evolvable-start id="verification" -->
## Verification

- [ ] Design tokens from Figma or the design spec used for colors, spacing, and typography
- [ ] All interaction states implemented (hover, focus, active, disabled)
- [ ] Exported code cleaned up with semantic HTML and accessibility attributes
- [ ] Implementation matches design file at all breakpoints (compare visually)
- [ ] No hardcoded pixel values where design tokens are available

<!-- moai:evolvable-end -->
