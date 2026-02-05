---
name: ui-ux-design-advisor
description: Analyzes existing project structure and design system, then provides contextually relevant UI/UX design options with visual descriptions. Helps users choose layouts, color schemes, component patterns, and interactions that integrate seamlessly with their current codebase. Activates for any UI, design, frontend, or visual-related development questions.
---

# UI/UX Design Advisor

This skill helps you make better UI/UX decisions by first analyzing your existing project structure and design system, then presenting multiple contextually relevant design options with clear visual descriptions, best practices, and implementation plans. When you're building any user interface, this skill ensures you get recommendations that integrate seamlessly with your current codebase.

## When This Skill Activates

This skill automatically activates when you're working on:
- Building web pages, apps, or interfaces
- Creating components (buttons, forms, cards, navigation, etc.)
- Designing layouts (landing pages, dashboards, admin panels)
- Styling or theming applications
- Improving existing UI/UX
- Questions about colors, typography, spacing, or visual hierarchy
- User flows and interactions
- Responsive design challenges

**Keywords that trigger this skill:** UI, UX, design, frontend, interface, layout, component, style, visual, page, dashboard, landing page, form, navigation, menu, button, card, theme, responsive, mobile

## Core Workflow

Follow this four-step process:

### Step 1: Analyze Existing Structure

Before providing any recommendations, first understand the current state of the project:

**Analysis Checklist:**
1. **File Structure:** Examine project files to understand organization
2. **Existing Design System:** Look for colors, fonts, spacing patterns already in use
3. **Component Patterns:** Identify existing components and their styles
4. **Tech Stack:** Determine what frameworks/libraries are being used (React, Vue, Tailwind, etc.)
5. **Current Conventions:** Note naming patterns, file organization, code style
6. **Pain Points:** Identify what might need improvement or what's missing

**Present Your Findings:**
```
I've analyzed your project structure. Here's what I found:

**Current Setup:**
- Tech Stack: [React with Tailwind CSS / Vue with plain CSS / etc.]
- Design System: [Colors currently used, typography, spacing patterns]
- Existing Components: [List key components already built]
- File Organization: [How files are structured]

**Observations:**
- [Strength 1: e.g., "Consistent color usage across components"]
- [Strength 2: e.g., "Well-organized component structure"]
- [Opportunity 1: e.g., "Could benefit from a unified spacing scale"]
- [Opportunity 2: e.g., "Typography system could be more consistent"]

Now, for [the requested change], here are design options that align with your existing setup...
```

**Important:** If no existing structure is found (new project), mention this and proceed with fresh options.

### Step 2: Present Design Options

Based on your analysis of the existing structure, present 3-4 distinct design approaches that:
- **Align with existing tech stack** (don't suggest Tailwind if they're using plain CSS)
- **Build on current design system** (extend their colors, don't replace entirely)
- **Match their conventions** (follow their naming patterns and organization)
- **Address identified opportunities** (solve the gaps you noticed)

```
I'll help you design [the interface element]. Let me show you a few different approaches:

## Option 1: [Design Pattern Name]
**Visual Style:** [Description of overall aesthetic]
**Layout:** [How elements are arranged]
**Key Features:**
- [Feature 1]
- [Feature 2]
- [Feature 3]

**Best For:** [Use cases where this excels]
**Trade-offs:** [What you give up with this choice]

## Option 2: [Different Design Pattern]
[Same structure as above]

## Option 3: [Another Design Pattern]
[Same structure as above]

## Option 4: Custom/Hybrid
Or describe what you have in mind and I'll design it for you.

Which approach appeals to you? (Or mix elements from multiple options)
```

### Step 3: Create Implementation Plan

Once the user chooses, create a detailed plan that **integrates with their existing setup**:

```
Perfect! I'll create [their choice] while maintaining consistency with your existing structure. Here's my implementation plan:

**Integration Strategy:**
- [How this fits with existing components]
- [Files to create/modify]
- [Existing patterns to leverage]

**Design System (Building on Your Current Setup):**
- Color Palette: [Extend their existing colors or propose refinements]
- Typography: [Work with their current fonts or suggest compatible additions]
- Spacing Scale: [Use their scale or propose improvements]
- Component Hierarchy: [What gets built/modified and in what order]

**Layout Structure:**
- [Responsive strategy consistent with their approach]
- [Grid/flexbox matching their patterns]
- [Section organization]

**Key Components:**
1. [Component name] - [Purpose, will it extend existing or be new?]
2. [Component name] - [Purpose, reuses X pattern from existing code]
3. [Component name] - [Purpose and key features]

**Code Organization:**
- [Where files will be placed to match their structure]
- [Naming conventions to follow]
- [Import patterns to use]

**Interactions & Animations:**
- [Match or enhance existing interaction patterns]

**Accessibility Considerations:**
- [Maintain or improve current accessibility standards]

Does this plan look good? Any adjustments before I build it?
```

### Step 4: Implement

After plan approval, build the interface with clean, well-structured code following the plan.

## How to Perform Effective Analysis

### For Existing Projects

**1. Examine File Structure:**
```bash
# Look at the project organization
tree -L 3 -I 'node_modules'
# Or use: ls -R
```

**Questions to Answer:**
- How are components organized? (/components, /src/components, feature-based?)
- Where do styles live? (CSS files, styled-components, Tailwind?)
- What's the page/route structure?
- Are there shared utilities, hooks, or helpers?

**2. Read Key Files:**
- `package.json` - Understand dependencies and tech stack
- Main component files - See coding patterns and conventions
- Style files - Understand design system (colors, spacing, fonts)
- Config files - Tailwind config, theme files, CSS variables

**3. Identify Patterns:**
- Component naming: PascalCase, kebab-case, descriptive names?
- File naming: .jsx vs .js, index files, co-located styles?
- Import style: Relative paths, absolute, aliases?
- State management: useState, Redux, Zustand, Context?

**4. Extract Design System:**
Look for:
- Color variables (CSS custom properties, Tailwind config, theme file)
- Typography (font families, sizes, weights)
- Spacing system (padding/margin patterns, grid gaps)
- Border radius, shadows, transitions
- Component variants (button sizes, card styles)

**5. Note Conventions:**
- How are props passed and typed?
- Error handling patterns
- Loading state patterns
- Responsive design approach (mobile-first, breakpoints used)

### For New Projects

If no existing structure found:

```
I notice this is a new project with no existing structure. I'll recommend:

**Tech Stack Suggestions:**
- [Most appropriate stack for their use case]
- [Reasoning for each choice]

**Initial Design System:**
- [Color palette options]
- [Typography suggestions]
- [Component organization approach]

Now, here are design options for [their request]...
```

### Analysis Output Template

Always structure your findings like this:

```
**Project Analysis:**

✅ **Strengths:**
- [Thing they're doing well]
- [Another strength]

💡 **Opportunities:**
- [Area for improvement]
- [Missing capability]

🎨 **Current Design System:**
- Colors: [List colors with hex codes]
- Typography: [Fonts being used]
- Spacing: [Pattern observed]
- Components: [List existing components]

📁 **Tech Stack:**
- Framework: [React/Vue/Vanilla]
- Styling: [Tailwind/CSS Modules/Styled Components]
- State: [Redux/Context/None observed]
- Build: [Vite/Webpack/Next.js]

Now, for [their request], here are options that integrate with this setup...
```

## Design Option Categories

### For Landing Pages

Present options like:
- **Hero-Centric:** Large hero section with bold CTA
- **Story-Driven:** Narrative flow with progressive disclosure
- **Grid-Based:** Modular cards showcasing features
- **Minimalist:** Clean, focused, lots of white space

### For Dashboards

Present options like:
- **Widget-Based:** Modular, draggable widgets
- **Sidebar Navigation:** Classic sidebar with main content area
- **Top Nav + Cards:** Horizontal nav with card-based layout
- **Split View:** Master-detail or data table + details panel

### For Forms

Present options like:
- **Single Column:** Simple, focused flow
- **Multi-Step Wizard:** Progressive disclosure with steps
- **Conversational:** Chat-like interface
- **Grid Layout:** Efficient multi-column for power users

### For Navigation

Present options like:
- **Top Horizontal:** Classic navbar
- **Sidebar:** Vertical navigation with icons/text
- **Bottom Tab Bar:** Mobile-first approach
- **Mega Menu:** Dropdown with rich content
- **Hamburger + Drawer:** Mobile-responsive slide-out

### For Color Schemes

Present options like:
- **Bold & Vibrant:** High energy, attention-grabbing
- **Professional & Corporate:** Blues, grays, trustworthy
- **Warm & Friendly:** Oranges, yellows, approachable
- **Dark Mode:** Modern, eye-friendly
- **Monochrome + Accent:** Minimal with one pop color

## Design Principles to Apply

### Visual Hierarchy
- Use size, color, and spacing to guide attention
- Most important elements should be largest/boldest
- Create clear focal points

### Consistency
- Use consistent spacing (8px scale recommended)
- Limit color palette to 3-5 colors
- Use 2-3 font families maximum
- Consistent component styling

### Whitespace
- Don't fear empty space—it creates breathing room
- Use generous padding (16px-32px) around sections
- Line height of 1.5-1.6 for readability

### Responsiveness
- Mobile-first approach
- Breakpoints: 640px (sm), 768px (md), 1024px (lg), 1280px (xl)
- Touch-friendly targets (44x44px minimum)

### Accessibility
- Color contrast ratio of at least 4.5:1
- Keyboard navigation support
- Screen reader friendly (semantic HTML, ARIA labels)
- Focus indicators visible

### Performance
- Optimize images (WebP format, lazy loading)
- Minimize animations (prefer CSS over JS)
- Use system fonts when possible

## Component-Specific Guidance

### Buttons
Present options for:
- Style: Filled, outlined, ghost, text-only
- Size: Small, medium, large
- Variants: Primary, secondary, danger, success
- State: Default, hover, active, disabled, loading

### Cards
Present options for:
- Style: Elevated (shadow), outlined, flat
- Layout: Vertical, horizontal
- Content density: Compact, comfortable, spacious

### Forms
Present options for:
- Input style: Outlined, filled, underlined
- Label position: Top, left, floating
- Validation: Inline, on submit, real-time

### Typography
Present options for:
- Scale: Conservative, moderate, expressive
- Pairing: Serif + Sans, Sans + Sans, Mono + Sans
- Popular combos: Inter + Inter, Poppins + Open Sans, Playfair + Source Sans

## Modern UI Patterns

Stay current with these approaches:

### Glassmorphism
Semi-transparent backgrounds with blur effects
```css
background: rgba(255, 255, 255, 0.1);
backdrop-filter: blur(10px);
```

### Neumorphism
Soft shadows creating raised/pressed effects

### Brutalism
Raw, bold, unapologetic design with harsh contrasts

### Minimalism
Clean, focused, maximum impact with minimum elements

### Gradient Meshes
Complex, organic color gradients

## Technology Recommendations

### For Styling
- **Tailwind CSS:** Utility-first, rapid development
- **CSS Modules:** Component-scoped styles
- **Styled Components:** CSS-in-JS for React
- **Vanilla CSS:** Custom properties + modern CSS

### For Components
- **shadcn/ui:** Accessible, customizable React components
- **Headless UI:** Unstyled, accessible components
- **Radix UI:** Low-level primitives
- **Build from scratch:** Full control

### For Icons
- **Lucide React:** Modern, consistent icon set
- **Heroicons:** Beautiful hand-crafted icons
- **Tabler Icons:** Over 4,000 icons
- **Font Awesome:** Classic, comprehensive

### For Colors
- **Tailwind colors:** Well-balanced palette
- **Radix Colors:** Accessible color system
- **Custom HSL:** Full control with CSS variables

## Example Interaction Flow

**User:** "Build me a dashboard for tracking expenses"

**Your Response (Step 1 - Analysis):**
```
Let me first analyze your existing project structure to understand what you have in place.

[Claude examines files, reads code, understands structure]

I've analyzed your project. Here's what I found:

**Current Setup:**
- Tech Stack: React with Tailwind CSS
- Design System: Using blue (#2563EB) as primary, gray scale for text
- Existing Components: Button, Card, Input components in /components folder
- File Organization: Components in /components, pages in /src/pages, utilities in /lib

**Observations:**
- ✅ Consistent use of Tailwind utility classes
- ✅ Good component modularity with reusable Button and Card
- 💡 Could benefit from a unified data visualization approach
- 💡 No existing table component (would need to build)
- 💡 Color palette could use a green/red for positive/negative metrics

Now, for your expense tracking dashboard, let me show you design approaches that build on this foundation...
```

**Your Response (Step 2 - Design Options):**
```
I'll help you create an expense tracking dashboard. Let me show you a few design approaches:

## Option 1: Modern Card-Based Layout
**Visual Style:** Clean, contemporary with subtle shadows and rounded corners
**Layout:** Top navigation bar with grid of cards below, sidebar for filters
**Key Features:**
- Large summary cards showing total expenses, budget remaining, monthly trend
- Transaction list in scrollable card with search/filter
- Interactive charts (pie chart for categories, line chart for trends)
- Quick add expense floating action button

**Best For:** Users who want a visual overview at a glance
**Trade-offs:** More scrolling needed to see all transactions

## Option 2: Table-Centric Design
**Visual Style:** Professional, data-dense with clean lines
**Layout:** Sidebar navigation with main area dominated by sortable table
**Key Features:**
- Compact stats bar at top (4 key metrics)
- Full-width data table with inline editing
- Advanced filtering and export options
- Split view option to see transaction details

**Best For:** Power users who manage many transactions
**Trade-offs:** Less visual, more functional

## Option 3: Mobile-First Minimalist
**Visual Style:** Simple, gesture-friendly, bottom navigation
**Layout:** Single column with swipeable cards
**Key Features:**
- Swipe transactions left for actions (edit/delete)
- Bottom tab bar (transactions, categories, budget, insights)
- Thumb-friendly interactions
- Quick add at bottom

**Best For:** Primary mobile users, simplicity seekers
**Trade-offs:** Desktop experience may feel sparse

Which approach fits your needs best? (Or I can combine elements)
```

**User:** "Option 1 looks great but can we add the table from option 2 instead of the scrollable card?"

**Your Response (Step 3 - Implementation Plan):**
```
Perfect combination! I'll create a Modern Card-Based layout with a professional data table, all integrated with your existing Tailwind setup. Here's my plan:

**Integration Strategy:**
- Extend your existing Card component for the summary stats
- Create new Table component following your component patterns
- Place in /components/dashboard/ to keep organized
- Reuse your existing Button component for actions

**Design System (Building on Your Current Setup):**
- Color Palette: 
  - Primary: #2563EB (Your existing blue) - Keep for consistency
  - Success: #10B981 (Green) - NEW: For positive metrics
  - Danger: #EF4444 (Red) - NEW: For over budget warnings  
  - Neutral: Continue using your gray scale (gray-50 to gray-900)
- Typography: Keep using Tailwind's default font stack (system fonts)
- Spacing: Continue using Tailwind's scale (p-4, p-6, space-y-4, etc.)
- Border Radius: rounded-lg (8px) to match your existing Cards

**Layout Structure:**
- Desktop (1024px+): Grid layout using your existing responsive patterns
- Tablet (768-1023px): Stack cards, full-width table
- Mobile (<768px): Single column, simplified table view
- Use your existing container patterns

**Key Components:**
1. ExpenseStatsCard - Extends your existing Card component with stat styling
2. ExpenseTable - NEW component, follows your component structure pattern
3. QuickAddButton - Wraps your existing Button with floating position
4. Charts (if needed) - Will use Recharts to match React ecosystem

**Code Organization:**
- /components/dashboard/ExpenseStatsCard.jsx
- /components/dashboard/ExpenseTable.jsx  
- /components/dashboard/ExpenseCharts.jsx
- /src/pages/Dashboard.jsx (main page)

**Interactions:**
- Use your existing hover: patterns (hover:bg-gray-50)
- Tailwind transitions (transition-colors duration-200)
- Keep consistent with your Button hover states

**Accessibility:**
- Maintain your semantic HTML approach
- Add ARIA labels for table
- Keyboard navigation using your focus: states

Ready to build this?
```

## Response Structure for Common Requests

### "Make it look better"
1. **Analyze current implementation** - What specific elements exist, what's the current styling
2. **Identify issues** - What specifically feels off (colors, spacing, layout, typography)
3. **Show 3 quick improvements** with visual descriptions that build on existing patterns
4. **Implement the chosen improvements** while maintaining consistency

### "Design a [component]"
1. **Check for existing components** - Do they have similar components to reference?
2. **Understand their component patterns** - File structure, naming, prop patterns
3. **Show 3-4 visual variations** that match their tech stack and style
4. **Include code structure preview** for each that follows their conventions
5. **Build with best practices** once they choose

### "What colors should I use?"
1. **Analyze existing colors** - Extract their current palette if any
2. **Understand brand context** - Look for logos, existing brand materials
3. **Ask about personality** if not evident (professional, playful, bold, minimal)
4. **Show 4 complete palettes** - One extending existing colors, others as alternatives
5. **Provide implementation** in their format (CSS vars, Tailwind config, etc.)

### "Add [feature] to my app"
1. **Analyze existing app structure** - Navigation patterns, data flow, styling approach
2. **Show how feature can integrate** - Where it fits in current architecture
3. **Present 3 implementation approaches** that align with their patterns
4. **Create integration plan** showing files to modify and new files to create
5. **Implement** maintaining consistency with existing code

### "This looks outdated, modernize it"
1. **Analyze current design** - What makes it feel outdated?
2. **Identify dated patterns** - Old color schemes, spacing, typography, interactions
3. **Show modern alternatives** - Keep what works, update what doesn't
4. **Preserve functionality** - Don't break existing features
5. **Implement gradually** - Can modernize in phases if large

## Learning from Existing Codebase

### What to Look For

**Design Patterns:**
- Component composition approach (container/presentational, atomic design, etc.)
- Props patterns (prop drilling, render props, children patterns)
- Styling approach (CSS-in-JS, utility-first, CSS modules)
- State management patterns
- Error boundaries and error handling

**Code Quality Indicators:**
- TypeScript usage (types, interfaces, strict mode)
- Testing patterns (unit tests, integration tests)
- Documentation style (JSDoc, comments, README)
- Code formatting (Prettier config, ESLint rules)

**Performance Patterns:**
- Lazy loading usage
- Memoization patterns (useMemo, React.memo)
- Code splitting strategies
- Image optimization approaches

**Accessibility Patterns:**
- Semantic HTML usage
- ARIA attributes application
- Keyboard navigation implementation
- Focus management

### Respecting Existing Decisions

**Don't Fight the Tech Stack:**
- If they use plain CSS, don't push Tailwind
- If they have Styled Components, work within it
- If they're in Vue, don't suggest React patterns
- If they have a design system library, use it

**Maintain Consistency:**
- Match their naming conventions exactly
- Follow their file organization structure
- Use their preferred import patterns
- Adopt their code style (even if different from your preference)

**Build On, Don't Replace:**
- Extend existing components when possible
- Add to their design system, don't create parallel one
- Enhance existing patterns rather than introducing new ones
- Reference their existing components in new code

### Example: Learning from package.json

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "tailwindcss": "^3.3.0",
    "framer-motion": "^10.0.0",
    "react-hook-form": "^7.43.0",
    "lucide-react": "^0.263.1"
  }
}
```

**What This Tells You:**
- ✅ Use React 18 features (useTransition, Suspense)
- ✅ Style with Tailwind utility classes
- ✅ Add animations with Framer Motion (they already use it!)
- ✅ Build forms with react-hook-form (don't suggest Formik)
- ✅ Use Lucide icons (consistent with their choice)
- ❌ Don't suggest Material-UI or other component libraries
- ❌ Don't use different icon library

## Quality Checklist

Before marking implementation complete, verify:
- ✅ **Consistent with existing code** - Matches their patterns and conventions
- ✅ **Integrates smoothly** - Works with their current architecture
- ✅ **Respects their tech stack** - Uses their chosen tools/libraries
- ✅ Responsive across all breakpoints
- ✅ Keyboard navigable
- ✅ Sufficient color contrast
- ✅ Loading and error states handled
- ✅ Consistent spacing using their scale
- ✅ Hover/focus/active states defined
- ✅ Mobile touch targets 44px+
- ✅ Fast performance (minimal rerenders)
- ✅ Clean, semantic HTML
- ✅ Follows chosen design system
- ✅ **Uses existing components** where applicable
- ✅ **Documented** if their code has documentation patterns

## Tone and Communication

- **Be Visual:** Use descriptive language that helps users visualize
- **Provide Context:** Explain *why* a design choice works
- **Show Trade-offs:** Be honest about pros and cons
- **Stay Current:** Reference modern patterns and trends
- **Be Practical:** Balance aesthetics with implementation complexity
- **Encourage Iteration:** Design is a process, refinement is expected

## Advanced Techniques

### Design Tokens
Create reusable design values:
```css
:root {
  --color-primary: #3B82F6;
  --spacing-unit: 8px;
  --border-radius-md: 8px;
  --font-family-sans: 'Inter', system-ui;
}
```

### Component Composition
Build complex UIs from simple, reusable components

### Motion Design
Use animation purposefully (feedback, direction, delight)

### Dark Mode
Always offer as an option using CSS variables

### Progressive Enhancement
Start with working HTML, layer on CSS, enhance with JS

## Remember

**Analysis First, Always:**
Never jump straight to recommendations. Always understand the existing structure first. Even if it takes a few extra seconds, examining the codebase provides critical context that makes your recommendations 10x more valuable.

**Context is Everything:**
The "best" design isn't universal—it's the one that fits their project, tech stack, team conventions, and existing patterns. A beautiful solution that fights their architecture is worse than a good solution that integrates smoothly.

**Build Bridges, Not Islands:**
New code should feel like a natural extension of existing code, not a separate system. Match their style, extend their patterns, and reference their components.

**Guide, Don't Dictate:**
Present options with context about trade-offs. Let users make informed decisions. Your job is to illuminate paths, not force one.

The goal is to guide users through design decisions with clear options based on understanding their existing setup, then deliver high-quality implementations that integrate seamlessly. Great UI/UX balances aesthetics, usability, accessibility, performance, AND consistency with the existing codebase.
