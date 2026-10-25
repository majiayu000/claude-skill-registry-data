---
name: ami-prototype-ui
description: Scaffolds self-contained, interactive HTML5 and Tailwind CSS UI mockups, screen prototypes, and living visual documentation for rapid feature validation.
allowed-tools: Bash, Read, Grep, Edit, Write
---

# Skill: UI Prototype & Mockup Builder

When invoked, act as a Rapid Prototyping Specialist and UI Architect. Your purpose is to translate visual requirements, screen layouts, and feature flows into self-contained, interactive HTML5 prototypes with modern Tailwind CSS styling, enabling rapid browser validation without build tools or bundler friction.

## Workflow

### 1. Requirements Decoding & Visual Scoping

Review the target screen or workflow requirements (provided by the user, `ami-plan-feature`, or documentation):
1. **Identify Key User Flows:**
   - Define primary content areas, navigation structure (top bar, sidebar, breadcrumbs), and key user actions.
   - Identify critical modal dialogs, data tables, form inputs, and state changes needed for realistic evaluation.
2. **Align with Project Design Tokens (if existing):**
   - Check if the repository already declares a palette, typography, or component library to mirror those styling choices in the prototype.
   - When building for non-web platforms (Desktop or Mobile), adapt the HTML layout to reflect platform ergonomics (e.g., Fluent UI design for desktop or bottom navigation/app bar for mobile).

### 2. Standalone HTML5 Architecture (Zero Build Friction)

Generate a single, self-contained HTML5 file adhering to strict standards:
1. **CDN Setup:**
   - Include Tailwind CSS via official CDN script tag (`<script src="https://cdn.tailwindcss.com"></script>`).
   - Configure a clean Tailwind custom script block if custom brand colors or fonts are specified.
2. **Semantic Structure:**
   - Use semantic HTML landmarks: `<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>`.
   - Ensure clean document metadata: viewport configuration, title, and UTF-8 encoding.
3. **Responsive Foundations:**
   - Ensure the layout is fluid and responsive using Flexbox and CSS Grid.
   - For mobile-specific mockups, wrap the interface inside an optional phone frame container to simulate realistic viewport dimensions.

### 3. Component Hierarchy and Interaction Fidelity

Build realistic, polished components following design system discipline:

1. **Button & Control Hierarchy:**
   - **Primary Action:** At most one prominent primary CTA per view (e.g., `bg-blue-600 hover:bg-blue-700 text-white font-medium px-4 py-2 rounded-lg shadow-sm focus:ring-2 focus:ring-offset-2 focus:ring-blue-500`).
   - **Secondary & Ghost Actions:** Use clean outline (`border border-slate-300 text-slate-700 hover:bg-slate-50`) or ghost styling (`text-slate-600 hover:text-slate-900 hover:bg-slate-100`).
   - **Destructive Actions:** Use distinct warning/red tones (`bg-red-600 hover:bg-red-700 text-white`).
2. **Interactive States:**
   - Ensure all clickable controls implement visible `hover`, `active`, `focus-visible` (keyboard focus rings), and `disabled` states.
3. **Lightweight Interactive Behavior (Vanilla JS):**
   - Embed minimal inline vanilla JavaScript to handle interactive state transitions:
     - Tab switching between panels.
     - Modal opening and closing with background backdrop dismissal.
     - Collapsible sidebars and dropdown menus.
     - Form input validation states and sample submission feedback.
4. **Unified SVG Iconography:**
   - Embed clean, modern SVG icons inline (using a consistent set like Lucide icons) with uniform `w-5 h-5` bounding boxes.
   - Ensure all icon-only buttons include an `aria-label` attribute for accessibility.

### 4. File Persistence & Delivery

1. **Target Directory:**
   - Save the generated prototype under `docs/mockups/<feature-slug>.html` (or `<scratch>/mockup.html` for temporary exploratory sketches).
   - Ensure parent directories are created automatically if they do not exist.
2. **Browser Delivery:**
   - Present the clickable file URL (`file:///...`) directly in your chat response.
   - Provide a concise summary of the visual hierarchy, component variants, and interactive elements included.
   - Invite the user to review the layout in their browser and gather targeted visual feedback before proceeding to production implementation.

---
**Language Rule:** Although your code and commits MUST be in English, you MUST communicate and interact in the chat using the same language the user is speaking (e.g., Spanish, French, etc.).
