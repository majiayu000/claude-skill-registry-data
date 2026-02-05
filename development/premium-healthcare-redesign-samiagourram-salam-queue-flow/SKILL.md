---
name: premium-healthcare-redesign
description: Redesign React components and pages for healthcare SaaS with premium Apple/Uber-like aesthetics while preserving ALL existing logic, hooks, state management, API calls, and event handlers. Use this skill when the user requests to redesign, make premium, improve the look of, or beautify existing React code. Also use when the user provides design inspiration screenshots to adapt. The skill treats all functionality as sacred and focuses purely on visual transformation - layout, styling, typography, colors, spacing, and modern component structures can change freely, but hooks order, state management, backend communication, and all interactions must remain 100% intact.
---

# Premium Healthcare Redesign

## Overview

Transform existing React healthcare SaaS pages into premium, modern interfaces with Apple/Uber-inspired aesthetics while guaranteeing zero breakage of existing logic. This skill enables complete visual redesigns where typography, colors, layouts, and component structures can be reimagined freely, but all hooks, state, API calls, and event handlers remain untouched.

## Redesign Workflow

Follow this workflow for every redesign request:

### Step 1: Pre-Redesign Analysis

Before making any changes, thoroughly analyze the existing code:

1. **Read the entire component** to understand its structure and purpose
2. **Identify and document all protected logic**:
   - All hooks (useState, useEffect, useCallback, useMemo, custom hooks) - note their order
   - State variables and setters
   - API calls (endpoints, parameters, payloads, error handling)
   - Event handlers (onClick, onChange, onSubmit, etc.)
   - Props received and passed to children
   - Conditional rendering logic
   - Form validation patterns
   - Refs and side effects
3. **Create a mental map** of what can change (visuals) vs. what cannot (logic)
4. **Read references/logic-preservation-checklist.md** to reinforce critical rules

### Step 2: Design Thinking & Uniqueness

Before diving into code, commit to a DISTINCTIVE aesthetic direction that elevates the healthcare SaaS beyond generic interfaces:

1. **Understand the context**:
   - Is this for patients or practitioners?
   - What's the emotional tone? (Calming, efficient, empowering, professional)
   - What makes this interface memorable?

2. **Choose a BOLD aesthetic direction**:
   - **NOT**: Generic healthcare blue-and-white, predictable Material Design
   - **YES**: Refined luxury (soft neutrals, sophisticated typography), Modern brutalism (bold type, dramatic contrast), Organic warmth (natural colors, flowing layouts), Editorial elegance (magazine-inspired, generous white space), Tech-forward (subtle gradients, glass morphism, modern sans-serif)
   - Commit fully to the chosen direction - half-measures create forgettable designs

3. **Make distinctive typography choices**:
   - **Avoid**: Inter, Roboto, Arial, generic system fonts
   - **Use**: Distinctive pairings that match your aesthetic direction
     - For luxury: "Instrument Serif" + "Söhne"
     - For modern tech: "Sora" + "DM Sans"
     - For editorial: "Fraunces" + "Synonym"
     - For clean minimal: "Satoshi" + "Inter" (use sparingly)
   - Vary between designs - never converge on the same font across multiple pages

4. **Craft memorable visual details**:
   - **Color**: Go beyond blue - consider deep teals, soft lavenders, warm grays, sage greens
   - **Backgrounds**: Not just white - try gradient meshes, subtle textures, color-shifted panels
   - **Micro-interactions**: Smooth transitions (200-300ms), hover states that surprise, loading states that delight
   - **Spatial composition**: Asymmetric layouts, overlapping elements, unexpected white space

5. **Differentiation principle**: Ask "What's the ONE thing users will remember about this interface?" Then design around that.

**CRITICAL**: Each redesign should feel uniquely crafted for its specific context. No two patient dashboards should look identical. No two practitioner schedules should use the same visual language. Avoid falling into a "house style" - interpret each interface fresh.

### Step 3: Design Planning

With inspiration screenshots or general premium aesthetic goals:

1. **Read references/premium-design-patterns.md** for foundational design principles
2. **Plan the visual transformation**:
   - New layout structure (while keeping same component hierarchy)
   - Distinctive color scheme that fits the chosen aesthetic direction
   - Typography system with characterful font choices
   - Generous or intentional spacing patterns
   - Modern component styling (cards, buttons, inputs) with unique touches
   - Polished interactions (transitions, hover states, micro-animations)
3. **Consider shadcn/ui components** as a base, but customize extensively to match your aesthetic
4. **Ensure accessibility** is maintained (WCAG AA contrast, focus states, ARIA labels)

### Step 4: Redesign Execution

Execute the redesign with extreme care for logic preservation AND commitment to distinctive aesthetics:

1. **Start with a copy** of the original component
2. **Keep all hooks in exact same order** at the top of the component
3. **Replace styling with creative intention**:
   - Apply your distinctive typography system with custom font imports
   - Implement your chosen color palette with CSS variables for consistency
   - Add wrapper divs for creative layouts without disrupting logic flow
   - Create unique component styling that reflects your aesthetic direction
   - Layer in micro-interactions and transitions (CSS or Framer Motion)
   - Add atmospheric details: gradients, subtle shadows, texture overlays
4. **Preserve all functional code** (CRITICAL):
   - Keep all useState, useEffect, and custom hooks identical
   - Keep all API calls with same parameters and payloads
   - Keep all event handlers connected correctly
   - Keep all conditional rendering logic unchanged
5. **Test mentally as you go**:
   - After each change, verify handlers are still connected
   - Ensure state flows unchanged
   - Check that API calls remain intact

**Balance**: Your creative choices on typography, colors, and layout should be BOLD. Your treatment of existing logic should be CONSERVATIVE. These are not in conflict - one enables the other.

### Step 5: Verification

After redesign, verify nothing broke:

1. **Visual inspection**:
   - All interactive elements visible and distinctively styled
   - Layout responsive and cohesive with chosen aesthetic
   - Typography hierarchy clear and characterful
   - Colors sophisticated and accessible
   - Micro-interactions smooth and delightful
2. **Logic verification**:
   - Same number of hooks in same order
   - All event handlers still connected
   - API calls unchanged
   - State management intact
   - Conditional logic preserved
3. **Use references/logic-preservation-checklist.md** for comprehensive verification

### Step 6: Final Polish & Atmosphere

Add distinctive finishing touches that complete the experience:

1. **Micro-interactions & motion**:
   - Smooth transitions on all interactive elements (use transition-all duration-200)
   - Creative hover states that match your aesthetic (not just opacity changes)
   - Loading states with personality (skeleton loaders, animated spinners)
   - Page load animations with staggered reveals (animation-delay)
2. **Atmospheric details**:
   - Background treatments: gradients, subtle patterns, color-shifted panels
   - Depth through layered shadows and transparency
   - Decorative elements that reinforce the aesthetic (custom cursors, borders, dividers)
   - Context-specific textures or effects
3. **Refinement**:
   - Perfect spacing consistency throughout
   - Typography scale harmony (use rem units, clear hierarchy)
   - Color usage that follows your palette strictly
   - Accessibility polish (focus rings, hover states, ARIA labels)

**Remember**: The goal is not just "premium" - it's MEMORABLE. Every redesign should have a clear point of view that makes it stand out from generic healthcare interfaces.

## Handling Design Inspiration Screenshots

When the user provides inspiration screenshots:

1. **Analyze the inspiration** for:
   - Color palette and mood
   - Spacing and layout patterns
   - Typography hierarchy
   - Component styling (buttons, cards, inputs)
   - Interaction patterns
2. **Adapt, don't copy**:
   - Extract design principles rather than exact implementations
   - Adjust for healthcare context (trust, professionalism, clarity)
   - Ensure patterns work for both patient and practitioner interfaces
3. **Create a design system** if requested:
   - Extract reusable color variables
   - Define typography scales
   - Document button and component styles
   - Can be applied consistently across multiple pages

## Common Redesign Patterns

### Dashboard Transformation

**Before**: Cramped, basic layout
**After**: Spacious card-based layout with generous white space

```jsx
// Keep all hooks, state, and API calls exactly as they were
// Only change visual structure and styling

<div className="min-h-screen bg-slate-50">
  <main className="max-w-7xl mx-auto px-6 py-8">
    <h1 className="text-4xl font-semibold text-slate-900 mb-8">Dashboard</h1>
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Each card with existing logic, new styling */}
      <div className="bg-white rounded-2xl shadow-sm border border-slate-100 p-6">
        {/* Original content with preserved handlers */}
      </div>
    </div>
  </main>
</div>
```

### Form Redesign

**Before**: Basic form with simple inputs
**After**: Clean, modern form with proper spacing and styling

```jsx
// Preserve all validation logic, onChange handlers, and onSubmit
// Update only visual presentation

<form onSubmit={handleSubmit} className="max-w-2xl mx-auto space-y-6">
  <div>
    <label className="block text-sm font-medium text-slate-700 mb-2">
      Patient Name
    </label>
    <input
      value={name}
      onChange={handleNameChange} // PRESERVED
      className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all"
    />
  </div>
  <button 
    type="submit"
    className="w-full px-6 py-3 bg-blue-600 text-white rounded-xl font-medium hover:bg-blue-700 transition-all shadow-sm hover:shadow-md"
  >
    Save Patient
  </button>
</form>
```

### Table Redesign

**Before**: Heavy borders, cramped spacing
**After**: Clean, spacious table with subtle styling

```jsx
// Keep all data mapping logic, sorting, and click handlers
// Update only visual styling

<div className="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
  <table className="w-full">
    <thead className="bg-slate-50 border-b border-slate-200">
      <tr>
        <th className="px-6 py-4 text-left text-sm font-semibold text-slate-900">
          Name
        </th>
        {/* More headers */}
      </tr>
    </thead>
    <tbody className="divide-y divide-slate-100">
      {patients.map(patient => ( // PRESERVED mapping logic
        <tr key={patient.id} className="hover:bg-slate-50 transition-colors">
          <td className="px-6 py-4 text-slate-700">{patient.name}</td>
          <td className="px-6 py-4">
            <button 
              onClick={() => handleEdit(patient.id)} // PRESERVED handler
              className="text-blue-600 hover:text-blue-700"
            >
              Edit
            </button>
          </td>
        </tr>
      ))}
    </tbody>
  </table>
</div>
```

## Key Principles (Critical)

1. **Logic is Sacred**: Hooks, state, API calls, and handlers are completely untouchable
2. **Visual Freedom**: Layout, colors, typography, spacing, and component structure can change freely
3. **Preserve Functionality**: Every button, input, and interaction must work exactly as before
4. **Distinctive Aesthetics**: Each redesign should be memorable and context-specific, not generic
5. **Accessibility**: Maintain contrast ratios, focus states, and semantic HTML
6. **shadcn/ui as Base**: Use shadcn/ui components when appropriate, but customize extensively

## Avoiding Generic Healthcare UI

**NEVER create**:
- Predictable blue-and-white medical interfaces
- Generic sans-serif typography (Inter, Roboto, Arial everywhere)
- Cookie-cutter Material Design patterns
- Identical layouts across different page types
- Timid, safe color choices without personality
- Flat, lifeless interactions with no motion or delight
- Dense, cramped layouts that feel utilitarian but uninspired

**ALWAYS strive for**:
- Distinctive font pairings that elevate the experience
- Sophisticated color palettes beyond healthcare blue (teals, lavenders, warm grays, sage)
- Unique layouts that fit the content (asymmetry, overlap, generous white space)
- Micro-interactions that surprise and delight
- Atmospheric backgrounds (gradients, textures, subtle patterns)
- Clear aesthetic point-of-view (luxury, editorial, modern tech, organic, brutalist)
- Context-specific design choices (patient dashboards ≠ practitioner schedules)

**Design variation mandate**: If you redesign 5 patient dashboards, they should use 5 different aesthetic approaches. Vary typography, color schemes, layout patterns, and visual treatments. Never converge on a "house style" - interpret each interface fresh based on its specific context and user needs.

## References

- **references/premium-design-patterns.md**: Detailed design principles, component patterns, and examples for Apple/Uber-like aesthetics
- **references/logic-preservation-checklist.md**: Comprehensive checklist and rules for ensuring zero logic breakage during redesign
