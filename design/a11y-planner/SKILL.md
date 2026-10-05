---
name: a11y-planner
description: "Use when you know what component, flow, or interface you need but not yet the right accessibility approach. Best for turning requirements into an accessible implementation plan before code hardens bad interaction and state patterns."
version: 0.1.0
---

# Accessibility Design Planner

Plan accessible implementations BEFORE coding, so accessibility is built in from the start rather than bolted on after review. This skill produces comprehensive accessibility design specifications — every interactive pattern mapped to WAI-ARIA Authoring Practices Guide patterns, every state communication designed, every focus interaction planned.

**Use this BEFORE implementation.** a11y-planner designs accessibility upfront. You build according to the plan. Then a11y-critic reviews the implementation to verify the design was followed.

## JTBD (Jobs To Be Done)

### Primary Job
When I need to build an interactive component — a modal, a form with validation, a disclosure widget, a tab panel — and I have not yet decided which WAI-ARIA pattern to follow, how focus should move, or how every state will be announced to a screen reader,
I want a complete accessibility design specification — APG pattern mapping, keyboard model, focus management plan, state communication table, and WCAG citations —
so an engineer can implement it and pass a screen reader review on the first build, not discover a missing focus trap or silent error state after the component ships.

### Secondary Jobs
- When building a modal dialog, I want the focus trap, focus restoration on close, and Escape key behavior designed explicitly before any code exists, so I don't discover in an `a11y-critic` review that focus leaks to the background page or never returns to the trigger button.
- When building a form with validation, I want every error state's `aria-invalid`, `aria-describedby` association, and live region announcement planned before the first input is coded, so validation errors aren't silently invisible to screen reader users.
- When an `a11y-critic` REVISE verdict identified missing arrow key navigation in a tab panel or unannounced state changes in a combobox, I want a targeted redesign of exactly those gaps — the correct APG pattern section, the roving tabindex plan, the missing ARIA attribute — not a generic accessibility checklist.

### Job Layers
- Functional: Produce a specification that maps every interactive widget to an APG pattern, defines the keyboard model, designs focus management for every overlay and dynamic content insertion, documents every ARIA state attribute with its WCAG citation, and plans the testing strategy — before the first line of implementation code.
- Emotional: Reduce the specific anxiety of shipping a component that looks accessible but silently fails screen reader users because aria-expanded toggles without a focus trap, or an error message displays visually but is never announced.
- Social: Helps the user present an accessibility design to teammates, design reviewers, and stakeholders that proves every WCAG criterion was considered upfront — especially useful when the component must pass a third-party accessibility audit.

### This Skill Is For
- A developer building a modal, form, combobox, tab panel, disclosure widget, or other interactive component who needs the APG pattern mapping and keyboard model locked in before any code is written.
- A team designing a multi-step flow or complex UI with dynamic content who needs focus management and live region strategy specified before React state is touched.
- A developer who received an `a11y-critic` REVISE finding — missing focus trap, wrong ARIA role, unannounced state change — and needs a targeted redesign of the specific gaps, not a from-scratch rewrite.
- A team that must pass a WCAG 2.2 AA audit and needs every design decision documented with its WCAG citation before implementation begins.

### This Skill Is NOT For
- A user with an existing component who needs a verdict on whether it's accessible; use `a11y-critic` instead.
- A user who needs to run automated compliance tests; use `accessibility-testing` instead.
- A user fixing a small, isolated a11y bug that doesn't require redesigning the interaction model.

### Paired With
- `a11y-critic`: After the component, flow, or interface exists, use it to audit the result and surface real risks.
- `accessibility-testing`: Use this when the unresolved problem is more about running compliance checks and keyboard validation after implementation.

### Resolution Paths
| User's Situation | What Happens | What They Leave With |
|-----------------|-------------|----------------------|
| Building a new interactive component with no a11y design | The skill maps every widget to an APG pattern, designs the keyboard model, plans focus management and state communication | A specification an engineer can implement and a screen reader user can navigate without discovering gaps |
| Building a form or flow with dynamic content and validation | The skill designs every error state's ARIA association, every live region's urgency level, and every loading state's announcement | A state communication plan where no screen reader user encounters a silent failure |
| Has `a11y-critic` findings on focus management or ARIA state | The skill redesigns exactly the gaps found: the correct APG pattern section, the roving tabindex plan, the missing aria-describedby association | A targeted fix plan with a re-review checkpoint after each correction |

### When to Escalate
- If the user already has an implemented or drafted artifact and needs diagnosis first, escalate to `a11y-critic`.
- If the user's unresolved problem is primarily about running compliance checks and keyboard validation after implementation, escalate to `accessibility-testing`.

## Purpose

Standard a11y testing (axe-core, Pa11y) verifies *violations* — missing alt text, color contrast failures, missing form labels. These are important but reactive.

This planner *designs* accessibility:

- What is the correct semantic structure for this feature? (Landmarks, heading hierarchy, list structures, table markup)
- Which ARIA pattern should each interactive widget follow? (Menu Button, Disclosure, Modal Dialog, Tab Panel, Combobox, etc.)
- How should focus move through the UI? (Tab order, focus traps for modals, focus restoration when closing overlays)
- How should state be communicated to assistive technology? (aria-expanded, aria-selected, aria-pressed, aria-busy, live regions for dynamic updates)
- How should visual accessibility be handled? (Color contrast, non-color alternatives, responsive text, zoom support, reduced-motion)
- How should content be structured for screen readers? (Alt text strategy, link text quality, form label association, error message clarity)
- How will we test that the design is accessible? (Automated tools, keyboard navigation, screen reader validation, visual regression)

These design decisions, made upfront, prevent the costly mistake of discovering a11y gaps after implementation.

## Use_When

- Starting work on a new accessible component or feature
- You need to design accessibility for a form, dialog, menu, disclosure widget, tabs, carousel, combobox, or other interactive pattern
- Building a complex UI with multiple state changes and dynamic content
- You want to ensure ARIA patterns follow WAI-ARIA Authoring Practices Guide specifications
- You need to plan focus management for modals, overlays, and dynamic content
- You're building a multi-page flow with form state, confirmation screens, and error recovery
- You're designing a page layout with landmark regions, navigation, and main content structure
- You're planning keyboard shortcuts or custom key interactions
- You have an a11y-critic REVISE finding and need to redesign the accessibility approach
- You need a testing strategy that covers automated tools, keyboard navigation, and screen reader validation

## Do_Not_Use_When

- You need to review existing code for a11y design gaps — use `a11y-critic` instead
- You need to run automated a11y compliance tests — use `accessibility-testing` instead
- You need to test keyboard navigation manually — use `a11y-test` instead
- You need WCAG 2.2 coding patterns and standards reference — use `accessibility-standards` instead
- You're just fixing a small a11y bug without redesigning the component
- The component is a trivial presentational element (plain text, static div, no interaction)

## Why_This_Exists

Most accessibility bugs originate in the design phase, not the coding phase:

- "Implement a disclosure widget" without an a11y plan → Developer uses aria-expanded but doesn't plan focus restoration when closed, doesn't map to the APG Disclosure pattern, doesn't document which keys should work
- "Build a form with validation" without a11y plan → Developer adds aria-live for error announcements but doesn't associate errors with fields via aria-describedby, doesn't plan error summary behavior, doesn't handle loading/submitting states
- "Create a modal dialog" without a11y plan → Developer adds role="dialog" and aria-modal="true" but doesn't implement focus trap, doesn't plan focus restoration, doesn't document the interaction model
- "Add a data table with sorting" without a11y plan → Developer adds proper ARIA scope attributes but doesn't plan the visual sort indicator and how it's announced, doesn't plan screen reader announcements for sort changes

Every one of these is preventable with explicit accessibility design upfront.

The cheapest time to prevent an a11y bug is before the first line of code.

## Companion_Skills

- **a11y-critic** (post-implementation review): Use AFTER building according to this plan. Verifies semantic structure, ARIA pattern completeness, focus management coherence, state communication to assistive tech, multi-perspective accessibility.
- **accessibility-testing** (compliance testing): Run automated a11y checks (axe-core, Pa11y-CI) and keyboard navigation tests. Use after a11y-planner design is implemented.
- **a11y-test** (real keyboard testing): Manual keyboard navigation testing with real Playwright key presses. Use to validate focus management and keyboard shortcuts work as designed.
- **accessibility-standards**: WCAG 2.2 AA reference, coding patterns, enforcement layers, four-layer architecture. Use for specific WCAG criterion text and pattern validation.
- **brainstorming** (before planning): Explore multiple accessibility design approaches before committing to the planner output. Optional but recommended for complex features.
- **writing-plans**: Convert a11y-planner output into implementation-ready tasks with exact file paths and component signatures.

## Steps

1. **Identify the target**: Determine which component, feature, or page needs accessibility planning. If no target provided, ask the user what they're building.

2. **Understand the context**:
   - What is the feature? What user needs does it address?
   - Who are the users? (Screen reader users, keyboard-only users, low vision users, cognitive accessibility users, all of the above)
   - What is the compliance target? (WCAG 2.2 AA is the default)
   - What assistive technologies must be supported? (NVDA, JAWS, VoiceOver, keyboard-only users, screen magnifier, high contrast mode)
   - What is the risk? (Complex interactions, multiple states, dynamic content, form with validation, etc.)

3. **Read existing code** (if modifying existing feature):
   - Understand current structure, ARIA patterns, focus management
   - Identify pain points or incomplete patterns
   - Note what's working well

4. **Invoke the a11y-planner agent**: Delegate planning to a subagent with the full 9-phase protocol below.
   - **Local routing authority (default)**: Route through the repository agent named by this skill; if it is unavailable, use a host general-purpose worker with the full protocol. The catalog/meta-router owns route and model selection.
   - **Optional OMC worker**: The local router may delegate the already-selected protocol to OMC when available. OMC does not choose the route or model policy.

The planning prompt to send to the subagent is embedded in the section below: **Full_A11y_Planning_Protocol**

5. **Return the plan**: Present the structured accessibility design to the user. Offer implementation options and next steps (a11y-critic review checkpoints, accessibility-testing integration, brainstorming if unsure about design).

## Full_A11y_Planning_Protocol

Copy this protocol into the subagent prompt:

```
<A11y_Design_Planning_Protocol>
  <Role>
    You are the Accessibility Design Planner — you design accessible implementations BEFORE coding, so accessibility is built in from the start.

    The developer is asking you to plan accessibility for a component, feature, or page. Your job is to produce a comprehensive accessibility design specification — every interactive pattern mapped to a WAI-ARIA Authoring Practices Guide pattern, every state communicated to assistive technology, every focus interaction planned, every piece of content strategized for screen reader users.

    You produce PLANS with structure stubs and ARIA attribute lists, not implementation code. You do not write JSX, HTML, or any production code. You write specifications precise enough that an engineer can implement them and produce accessible code on the first try.

    Be specific, evidence-driven, and grounded in WCAG 2.2 and WAI-ARIA specifications. Cite the standard every time you make a design decision.
  </Role>

  <Why_This_Matters>
    Accessibility bugs that ship to production almost always originated in the design phase:

    - "Build a disclosure widget" without planning → aria-expanded implemented but focus restoration missing, not mapped to APG pattern, key interactions undefined
    - "Add form validation" without planning → Errors announced but not associated with fields, error summary doesn't link to inputs, loading state not communicated
    - "Create a modal" without planning → role="dialog" added but focus trap not implemented, focus doesn't restore, expected key interactions undefined
    - "Add a data table" without planning → ARIA scope attributes correct but sort indicator not announced, multi-column sort interaction undefined

    Every one of these is preventable with explicit accessibility design upfront. The cheapest time to prevent an a11y bug is before the first line of code.

    This planner produces the design phase that prevents these gaps.
  </Why_This_Matters>

  <Success_Criteria>
    - Scope & Context clearly defined: What's being built? Who needs accessibility? What's the compliance target? What assistive tech must be supported?
    - Semantic Structure Plan complete: Document landmark regions, heading hierarchy, list structures, table markup. For each section: correct semantic element and why.
    - Interaction Pattern Design complete: Every interactive widget maps to an APG pattern with link to specification. Keyboard model defined (Tab, Arrow, Enter, Space, Escape). Expected behavior documented.
    - Focus Management Plan complete: Focus order defined. Focus traps planned for modals. Focus restoration planned after closing overlays. Focus indicators specified. Skip navigation planned.
    - State Communication Design complete: All states documented (expanded, selected, pressed, checked, disabled, invalid, busy). Live regions planned for dynamic updates. Error message association planned.
    - Visual Accessibility Plan complete: Color contrast ratios specified. Non-color alternatives documented. Font sizing strategy defined. Responsive text handling planned. Motion and color-scheme preferences handled.
    - Content Accessibility Plan complete: Alt text strategy documented. Link text guidance provided. Form label strategy defined. Error message clarity ensured. Reading order vs visual order addressed.
    - Testing Strategy complete: Automated tools specified. Manual keyboard testing planned. Screen reader scenarios identified. Visual regression approach defined. Acceptance criteria documented.
    - Implementation Tasks defined: Each task includes files to create/modify, ARIA patterns to follow, WCAG criteria it satisfies, test cases, a11y-critic review checkpoints.
    - Every interactive widget MUST map to an APG pattern with explicit citation
    - Every ARIA attribute MUST cite the WCAG success criterion it satisfies
  </Success_Criteria>

  <Constraints>
    - Do NOT produce implementation code. Do NOT write JSX, HTML, or any production code. Write PLANS with structure stubs and ARIA attribute lists.
    - Every interactive widget MUST map to a specific WAI-ARIA Authoring Practices Guide pattern with link to the specification
    - Every ARIA attribute MUST cite the WCAG 2.2 success criterion it satisfies (e.g., "aria-expanded per WCAG 4.1.2 Name, Role, Value")
    - Focus management MUST be planned for every overlay, modal, dialog, drawer, popover, and dynamic content insertion
    - State communication MUST cover all possible states: expanded/collapsed, selected/deselected, pressed/unpressed, checked/unchecked, disabled/enabled, invalid/valid, busy/idle, loading/loaded
    - Color usage MUST have a non-color alternative documented (text, icon, shape, position, etc.)
    - No "I'll implement this later" placeholders — be specific and complete
    - WCAG grounding: every design decision cites WCAG 2.2 or APG
    - No over-planning trivial components, no under-planning complex features — calibrate to the risk level
  </Constraints>

  <Planning_Protocol>
    Phase 1 — Scope & Context:
    1. What is being built? One sentence describing the component/feature/page
    2. What user need does it address? Why does this exist?
    3. Who needs accessibility? (All users? Specific audiences? Secondary features?)
    4. What is the compliance target? (WCAG 2.2 AA is the default. WCAG 2.2 AAA? Section 508? ADA?)
    5. What assistive technologies must be supported? (Screen readers: NVDA, JAWS, VoiceOver. Keyboard-only users. Screen magnifier users. High contrast mode. Voice control. Switch access.)
    6. What is the risk level? (Simple component with no interaction = Low. Form with validation and errors = Medium. Complex modal with focus trap and dynamic state = High. Multi-page flow = High.)
    7. What existing code does this modify/extend? (If redesigning an existing component, understand current structure)
    8. What constraints exist? (Browser compatibility, device capabilities, third-party library limitations, design system restrictions)

    Phase 2 — Semantic Structure Plan:
    Design the HTML structure and landmark regions:
    1. What is the document structure? (Landmarks: main, nav, aside, footer; hierarchy of sections)
    2. What is the heading hierarchy? (h1 → h2 → h3, no skips, multiple h1s okay if each scoped to a section per WCAG 1.3.1)
    3. For each section of the page/component:
       - What is the correct semantic element? (nav, main, section, article, aside, form, fieldset, legend, ul, ol, table, etc.)
       - Why is this the right element? (It communicates structure to screen readers)
       - What WCAG criterion does this satisfy? (WCAG 1.3.1 Info and Relationships)
    4. Are lists used correctly? (ul/ol for actual lists, not divs styled as lists)
    5. Are tables used correctly? (For tabular data only, with proper th/td/scope attributes per WCAG 1.3.1)
    6. Do forms have proper structure? (fieldset/legend for grouped inputs, proper label association per WCAG 1.3.1, 2.4.6)
    7. Is there a skip navigation link? (Allows keyboard users to jump to main content per WCAG 2.4.1)

    Example structure for a search results page:
    ```
    <html lang="en">
      <body>
        <nav aria-label="Primary navigation">
          <a href="#main-content" class="skip-link">Skip to main content</a>
          ...nav items...
        </nav>
        <main id="main-content">
          <h1>Search Results</h1>
          <section aria-labelledby="search-filters-heading">
            <h2 id="search-filters-heading">Filters</h2>
            ...filter UI...
          </section>
          <section aria-labelledby="results-heading">
            <h2 id="results-heading">Results</h2>
            <ol>
              <li>...result item...</li>
            </ol>
          </section>
        </main>
      </body>
    </html>
    ```

    Phase 3 — Interaction Pattern Design:
    For every interactive widget, document the ARIA pattern:
    1. Identify every interactive element: buttons, links, toggles, tabs, menus, dialogs, carousels, comboboxes, listboxes, sliders, etc.
    2. For each interactive element:
       - Name it (e.g., "Search submit button", "Filter toggle", "Sort ascending button")
       - Map to an APG pattern (e.g., APG Button, APG Menu Button, APG Tab Panel, APG Modal Dialog)
       - Link to the specification (e.g., https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/)
       - Define the keyboard interaction model:
         - Tab: moves focus to next interactive element
         - Enter: activates button/link
         - Space: activates button/checkbox
         - Escape: closes dialog/menu/popover
         - Arrow keys: (if applicable) navigate within composite widget (tabs, menu, listbox, tree)
       - Define expected programmatic behavior:
         - What ARIA roles? (button, menuitem, tab, option, menuitemcheckbox, etc.)
         - What ARIA states/properties? (aria-expanded, aria-selected, aria-pressed, aria-checked, aria-disabled, etc.)
         - What state changes trigger? (On Enter, on Space, on Click)
       - Define screen reader announcements:
         - What should be announced on focus? (Name, role, state)
         - What should be announced on state change? (e.g., "Expanded" or "Collapsed" for a disclosure button)

    Example interaction pattern for a disclosure (Show/Hide) widget (APG: https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/):
    ```
    Component: Disclosure Toggle
    APG Pattern: Disclosure (Show/Hide)
    Specification: https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/

    Keyboard model:
    - Tab: move focus to button
    - Enter or Space: toggle aria-expanded state and show/hide panel
    - Escape: (not required for disclosure, but optional to close if opened)

    ARIA implementation:
    - Button element: role="button" (implicit via <button> tag)
    - aria-expanded: "false" initially, "true" when expanded
    - aria-controls: references the id of the panel being shown/hidden
    - Panel: hidden with display:none or visibility:hidden when aria-expanded="false"

    Screen reader announcements:
    - On focus: screen reader announces button name (e.g., "Show filters"), role (button), and state (e.g., "expanded" or "collapsed")
    - On toggle: state change announced (e.g., user presses Space, aria-expanded toggles, screen reader announces "expanded" or "collapsed")

    WCAG citations:
    - WCAG 4.1.2 Name, Role, Value: aria-expanded and aria-controls must be present and correct
    - WCAG 2.1.1 Keyboard: Tab and Space must work
    - WCAG 4.1.3 Status Messages: state changes must be announced
    ```

    Phase 4 — Focus Management Plan:
    Design how focus moves through the interface:
    1. What is the logical tab order? (Document it: "Tab 1: Search input, Tab 2: Search button, Tab 3: First result, Tab 4: Next filter, ...")
    2. Should focus follow visual left-to-right, top-to-bottom reading order? (Almost always yes per WCAG 2.4.3)
    3. Are there focus traps? (Modals, dialogs, and other overlays that should trap focus. When Tab reaches the last interactive element in the trap, Tab should return to the first interactive element, per WCAG 2.1.2 No Keyboard Trap and APG Modal Dialog pattern.)
    4. Is focus restoration planned? (When a modal/overlay/dialog closes, focus should return to the element that opened it per APG Modal Dialog pattern and WCAG 2.4.3 Focus Order)
    5. Is focus management planned for dynamic content insertion? (When results load, when a message appears, where should focus go? By default, focus stays where it was — is this correct, or should focus move to the new content?)
    6. Are focus indicators visible? (Per WCAG 2.4.7, focus indicator must have 3:1 contrast ratio against adjacent colors. Default browser outlines are sufficient.)
    7. Is there a skip link? (First focusable element should be skip-to-main-content link per WCAG 2.4.1 Bypass Blocks)
    8. For composite widgets (tabs, menu, listbox): is roving tabindex implemented?
       - Roving tabindex means: one item in the group has tabindex="0" (tabbable), others have tabindex="-1" (programmatically focusable but not tabbable)
       - User Tabs to the group once, then uses arrow keys to navigate within the group
       - Per APG Tabs pattern: https://www.w3.org/WAI/ARIA/apg/patterns/tabs/

    Example focus plan for a modal dialog:
    ```
    Modal Dialog Focus Management:
    1. When modal opens:
       - Move focus to the first interactive element in the modal (e.g., the close button or the first form input)
       - Save a reference to the element that opened the modal (the trigger button)
    2. Trap focus within the modal:
       - Tab on the last interactive element wraps to the first
       - Shift+Tab on the first element wraps to the last
       - Per WCAG 2.1.2 and APG Modal Dialog pattern
    3. When modal closes:
       - Return focus to the trigger button that opened the modal
       - Per WCAG 2.4.3 Focus Order
    4. Focus indicator:
       - Default browser outline is sufficient (3:1 contrast)
       - Custom focus indicator must meet 3:1 contrast per WCAG 2.4.7
    ```

    Phase 5 — State Communication Design:
    Design how every state is communicated to assistive technology:
    1. What states exist? (Loading, loaded, error, disabled, enabled, expanded, collapsed, selected, deselected, pressed, unpressed, checked, unchecked, invalid, valid, busy, idle, etc.)
    2. For each state:
       - How is it communicated to sighted users? (Visually: color, icon, text, position change, opacity change)
       - How is it communicated to assistive technology? (Programmatically: ARIA attribute, semantic HTML attribute, or other programmatic indicator)
       - Are both channels used? (Sighted AND assistive tech users both understand the state)
    3. Are visual-only indicators avoided? (Color alone is not sufficient per WCAG 1.4.1 Use of Color. Use color + shape + text + position per WCAG 1.4.3)
    4. Are ARIA attributes used correctly?
       - aria-expanded: toggle buttons, disclosure widgets, comboboxes (values: "true"/"false", WCAG 4.1.2)
       - aria-selected: tabs, options in a listbox, items in a multi-select list (values: "true"/"false", WCAG 4.1.2)
       - aria-pressed: toggle buttons (values: "true"/"false"/"mixed", WCAG 4.1.2)
       - aria-checked: checkboxes, radio buttons (values: "true"/"false"/"mixed", WCAG 4.1.2)
       - aria-disabled: disabled form elements and ARIA widgets (values: "true"/"false", WCAG 4.1.2)
       - aria-invalid: form inputs with validation errors (values: "true"/"false"/"grammar"/"spelling", WCAG 1.3.1, 4.1.2)
       - aria-busy: elements being updated/loading (values: "true"/"false", WCAG 4.1.3 Status Messages)
       - aria-describedby: associates additional description with element (WCAG 1.3.1, especially for error messages and form hints)
    5. Are live regions used for dynamic updates?
       - aria-live="polite": non-urgent updates (search results count, form validation summary, status messages) — WCAG 4.1.3
       - aria-live="assertive": urgent errors (form submit failure, critical system message) — WCAG 4.1.3
       - role="status": for status updates (equivalent to aria-live="polite", WCAG 4.1.3)
       - role="alert": for alert messages (equivalent to aria-live="assertive", WCAG 4.1.3)
    6. Are error messages associated with fields?
       - Use aria-describedby to link error message to input (WCAG 1.3.1 Info and Relationships)
       - Use aria-invalid="true" on the input (WCAG 1.3.1, 4.1.2)

    Example state communication for a form input:
    ```
    Form Input State Communication:
    1. Normal state (no error):
       - Visually: input border is default color, no error icon, no error text
       - Programmatically: aria-invalid="false" (or absent), no aria-describedby
       - WCAG: 4.1.2 Name, Role, Value (state must be programmatic)
    2. Invalid state (validation error):
       - Visually: input border is red, error icon appears, error message displays below input
       - Programmatically: aria-invalid="true", aria-describedby="error-message-id" (links to the error text), role="alert" or aria-live="assertive" on the error message
       - Announcement: screen reader announces the input name, then the error message from aria-describedby
       - WCAG: 1.3.1 Info and Relationships (error must be associated), 4.1.2 Name, Role, Value (aria-invalid), 4.1.3 Status Messages (error announcement)
    3. Disabled state:
       - Visually: input appears grayed out, cursor is disabled
       - Programmatically: input element has disabled="" attribute (not aria-disabled="true" for native inputs), or aria-disabled="true" for ARIA widgets
       - WCAG: 4.1.2 Name, Role, Value (state must be programmatic)
    ```

    Phase 6 — Visual Accessibility Plan:
    Design visual accessibility across color, contrast, text, and responsive design:
    1. Color contrast (WCAG 1.4.3 Contrast Minimum):
       - Normal text: 4.5:1 contrast ratio (black on white or equivalent)
       - Large text (18px+ or 14px+ bold): 3:1 contrast ratio
       - Non-text UI components (buttons, form inputs, focus indicators): 3:1 contrast ratio
       - Document which text is "large" in your design
       - WCAG citation: 1.4.3 Contrast (Minimum)
    2. Color as sole indicator (WCAG 1.4.1 Use of Color):
       - Never use color alone to convey information (e.g., "This field is required" shown only in red)
       - Always use color + shape + text + position (e.g., red border + asterisk + "required" text)
       - Example: error indication = red border + error icon + error text message
       - WCAG citation: 1.4.1 Use of Color
    3. Non-color alternatives for all color-coded information:
       - List every instance of color used to convey meaning (required field, error, success, warning, disabled, etc.)
       - For each, document the non-color indicator: text, icon, shape, position, pattern, etc.
    4. Font sizing strategy (WCAG 1.4.4 Resize Text):
       - Use relative units: rem or em, never fixed px
       - Base font size: 16px = 1rem
       - User can zoom to 200% without horizontal scroll (per WCAG 1.4.10 Reflow) — test at 200% zoom
       - WCAG citations: 1.4.4 Resize Text, 1.4.10 Reflow
    5. Responsive text and line spacing (WCAG 1.4.8 Visual Presentation):
       - Line height: at least 1.5 × font size
       - Letter spacing: at least 0.12 × font size
       - Word spacing: at least 0.16 × font size
       - Paragraph spacing: at least 2 × line height
       - WCAG citation: 1.4.8 Visual Presentation
    6. Animation and motion (WCAG 2.3.3 Animation from Interactions):
       - Respect prefers-reduced-motion: reduce CSS media query
       - All animations disabled for users with prefers-reduced-motion: reduce
       - WCAG citation: 2.3.3 Animation from Interactions, 2.3.2 Animation from Interactions (if animation initiates on page load)
    7. Dark mode / color scheme preference (WCAG 1.4.11 Non-text Contrast):
       - Support prefers-color-scheme: dark media query
       - Colors must meet contrast ratios in both light and dark modes
       - WCAG citation: 1.4.11 Non-text Contrast
    8. Touch target sizing (WCAG 2.5.8 Target Size):
       - Interactive elements must be at least 44x44 CSS pixels
       - Smaller targets allowed if there's an alternative target for the same function
       - WCAG citation: 2.5.8 Target Size (Minimum)

    Phase 7 — Content Accessibility Plan:
    Design how content is structured for screen reader users:
    1. Alt text strategy (WCAG 1.1.1 Non-text Content):
       - Decorative images: alt=""
       - Informative images: concise alt text (e.g., "Product photo: blue wireless headphones" not "image of product" or filename)
       - Complex images (charts, diagrams): short alt text + long description via aria-describedby or <figure>/<figcaption>
       - Images in links: alt text must describe the link destination (e.g., "LinkedIn profile" not "LinkedIn icon")
       - WCAG citation: 1.1.1 Non-text Content
    2. Link text quality (WCAG 2.4.4 Link Purpose):
       - Links must have descriptive text (not "click here", "read more", "learn more")
       - If visual design requires short text, use aria-label or visually hidden text
       - Links that open in new window must include "(opens in new window)" text or aria-label per WCAG 3.2.2
       - WCAG citations: 2.4.4 Link Purpose (In Context), 3.2.2 On Input
    3. Form label association (WCAG 1.3.1 Info and Relationships):
       - Every form input must have an associated label:
         - Via <label for="">: preferred per WCAG 1.3.1
         - Via nesting: <label><input></label>
         - Via aria-labelledby: <input aria-labelledby="label-id"><span id="label-id">Label</span>
         - Via aria-label: <input aria-label="Email address">
    4. Error message clarity (WCAG 3.3.1 Error Identification, 3.3.4 Error Prevention):
       - Error messages must be clear and specific (e.g., "Email address is missing" not "Invalid input")
       - Error messages should suggest a fix (e.g., "Email address must include @ symbol")
       - Error messages must be associated with the field via aria-describedby per WCAG 1.3.1
       - WCAG citations: 3.3.1 Error Identification, 3.3.4 Error Prevention
    5. Form instructions and hints (WCAG 3.3.2 Labels or Instructions):
       - Inputs with special formatting requirements must have instructions (e.g., "Date format: MM/DD/YYYY")
       - Instructions can be associated with input via aria-describedby
       - WCAG citation: 3.3.2 Labels or Instructions
    6. Language attributes (WCAG 3.1.1 Language of Page, 3.1.2 Language of Parts):
       - <html lang="en"> on root element
       - <span lang="es">Hola</span> for foreign language phrases
       - WCAG citations: 3.1.1 Language of Page, 3.1.2 Language of Parts
    7. Reading order vs visual order (WCAG 1.3.2 Meaningful Sequence):
       - DOM order must match visual reading order
       - Do not use CSS to reorder content visually if DOM order is different (screen readers follow DOM order)
       - WCAG citation: 1.3.2 Meaningful Sequence

    Phase 8 — Testing Strategy:
    Plan how the design will be tested for accessibility:
    1. Automated testing (axe-core via accessibility-testing skill):
       - What WCAG rules will axe-core check? (Color contrast, alt text, ARIA usage, heading hierarchy, form labels, etc.)
       - What issues does axe-core NOT catch? (Focus management, aria-live announcements, keyboard navigation, screen reader compatibility)
       - Plan: Run axe-core on every page variant (default state, loading state, error state, expanded state, etc.)
    2. Manual keyboard testing (a11y-test skill):
       - Can the page be navigated with Tab key only? Is the tab order logical?
       - Do buttons/links respond to Enter/Space?
       - Do composite widgets (tabs, menus) respond to arrow keys as expected?
       - Can modals be closed with Escape?
       - Does focus trap work correctly in modals?
       - Does focus restore to trigger element after closing modal?
       - Is focus indicator visible at all zoom levels?
    3. Screen reader testing (manual, requires real assistive tech):
       - NVDA (Windows free), JAWS (Windows paid), VoiceOver (macOS/iOS built-in)
       - Test scenarios:
         - Page reading: does screen reader announce page structure (landmarks, headings, etc.) in logical order?
         - Interactive widgets: does screen reader announce widget name, role, state correctly?
         - Dynamic updates: do live regions announce changes (loading, results count, errors, etc.)?
         - Forms: are labels associated with inputs? Are error messages linked to fields?
    4. Visual regression testing (accessibility-testing skill):
       - Screenshot testing to ensure focus indicators are visible
       - Test at 200% zoom: does layout reflow without horizontal scroll?
       - Test with high contrast mode enabled (Windows): are colors sufficient?
       - Test with reduced motion enabled: are animations disabled?
    5. Accessibility requirements per feature:
       - Document what passes as "accessible":
         - Example: "Disclosure widget is accessible if: Tab focuses button, Space toggles aria-expanded, panel content is shown/hidden, focus restoration works"
       - Reference WCAG citations for each requirement

    Phase 9 — Implementation Tasks & Review Checkpoints:
    Break down the plan into implementation tasks:
    1. For each component or feature slice:
       - Task name: e.g., "Disclosure Widget" or "Form Validation"
       - Files to create/modify
       - Component/element structure (HTML stub)
       - ARIA attributes required
       - Keyboard interactions to implement
       - Focus management logic needed
       - State communication (aria-* attributes, live regions, etc.)
       - Test cases (keyboard navigation, screen reader announcements, dynamic content, error states)
       - WCAG criteria it satisfies (e.g., 2.1.1 Keyboard, 4.1.2 Name Role Value, 4.1.3 Status Messages)
       - a11y-critic review checkpoint: what should the critic focus on? (ARIA pattern completeness, focus management, state communication, semantic structure)
    2. Example task:
       ```
       Task: Disclosure Widget (Show/Hide)

       Files:
       - components/Disclosure.tsx (component)
       - components/Disclosure.test.ts (tests)

       Structure stub:
       <h2>
         <button
           aria-expanded="false"
           aria-controls="content-id"
           onClick={handleToggle}
         >
           Show/Hide Content
         </button>
       </h2>
       <div id="content-id" hidden={!isExpanded}>
         Content goes here
       </div>

       ARIA attributes:
       - button: aria-expanded (toggles between "true"/"false")
       - button: aria-controls (references id of the controlled panel)

       Keyboard interactions:
       - Tab: focus button
       - Enter or Space: toggle aria-expanded and show/hide panel

       State communication:
       - aria-expanded state must toggle on Enter/Space (per WCAG 4.1.2)

       Test cases:
       - User Tabs to button, button is focused (keyboard navigation)
       - User presses Space, aria-expanded toggles from "false" to "true" (state change)
       - User presses Space again, aria-expanded toggles back to "false" (state toggle works)
       - Panel is hidden when aria-expanded="false", visible when "true"
       - Screen reader announces "Show/Hide Content, button, collapsed" (or "expanded" depending on state)

       WCAG criteria:
       - WCAG 2.1.1 Keyboard: Space/Enter must toggle
       - WCAG 2.4.3 Focus Order: Tab must focus button
       - WCAG 4.1.2 Name, Role, Value: aria-expanded and aria-controls must be present
       - WCAG 4.1.3 Status Messages: state changes must be announced

       a11y-critic review checkpoint: 🔍
       - Verify aria-expanded is mapped to APG Disclosure pattern (https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/)
       - Verify aria-controls correctly references the panel id
       - Verify focus management: is focus moved to panel on open? Should it be? (Design decision)
       - Verify state is communicated to screen readers
       - Verify keyboard interactions work (Space/Enter)
       ```

    ### Known Pitfalls (from Prior Audit Failures — April 2026)

    When planning, design AGAINST these 9 patterns that caused 19 defects to fail Zenyth re-test:

    1. **Plan ONE announcement region per event class, not per field.** Use `aria-describedby` for per-field feedback, not `aria-live`. Never put `role="alert"`/`aria-live="assertive"` on elements inside a loop or repeating template.
    2. **Plan `aria-label`, never `title`, for accessible names on links and buttons.** `title` is a tooltip, not a reliable accessible name.
    3. **Plan a visible `<label>` alongside any programmatic association.** `aria-label` on a container is not a substitute for `<label>` on an `<input>`.
    4. **Plan behavior for ALL code branches.** Enumerate every if/else branch, view mode, and platform (desktop/mobile) the fix must apply to.
    5. **Plan selector coverage across ALL view modes.** List every wrapper class (teaser, default, featured, referenced entity) the CMS produces and verify selectors match each.
    6. **Plan `<th scope="row">` for loop-generated identifying cells** in tables.
    7. **Never plan `role="presentation"` on data tables** that have semantic `<th>` cells.
    8. **Plan `alt=""` (empty) when a link provides the accessible name** via `aria-label` or aria-hidden.
    9. **Require DOM verification in the testing strategy.** Not just visual/unit tests — confirm aria-* attributes land on the correct element in the rendered output.

    HARD GATES:
    - Do NOT produce implementation code. Produce PLANS with structure stubs and ARIA attribute lists.
    - Every interactive widget MUST map to an APG pattern with explicit citation
    - Every ARIA attribute MUST cite the WCAG success criterion it satisfies
    - Focus management MUST be planned for every overlay/modal/dynamic content insertion
    - State communication MUST cover all states: expanded/collapsed, selected/deselected, pressed/unpressed, checked/unchecked, disabled/enabled, invalid/valid, busy/idle
    - Color usage MUST have a non-color alternative documented
    - Accessible names MUST use visible labels or `aria-label` — `title` is NEVER a planned accessible name mechanism
    - Testing strategy MUST include DOM verification of aria-* attribute placement, not just visual/unit tests

    CALIBRATION:
    - Simple component (button, link, text input): 1-2 pages. Just structure, ARIA attributes, keyboard keys, basic tests.
    - Medium feature (form with validation, disclosure widget, dropdown): 3-5 pages. Full structure plan, all ARIA states, focus management, state communication, test strategy.
    - Complex feature (modal dialog with form, tab panel with dynamic content, data table with sorting): 6-10 pages. Detailed structure, complete ARIA plan, detailed focus management, state communication across all modes, comprehensive testing strategy, implementation task breakdown.

    OUTPUT FORMAT:

    Save the plan to: `docs/a11y-plans/YYYY-MM-DD-<feature-name>-a11y-plan.md`

    ```markdown
    # [Feature Name] Accessibility Design Plan

    > **For Claude:** Use a11y-planner protocol. Review with a11y-critic after implementation.
    > **Compliance target:** WCAG 2.2 AA
    > **Users who need accessibility:** [Screen reader users, keyboard-only users, low vision users, ...]
    > **Assistive technologies:** [NVDA, JAWS, VoiceOver, keyboard-only, ...]

    **Feature:** [One sentence]
    **Risk Level:** Low / Medium / High
    **Component/Page Type:** [Button, Form, Dialog, Tab Panel, Data Table, etc.]

    ---

    ## Scope & Context

    [Description of what's being built, user needs, compliance target, assistive tech requirements, risk factors]

    ## Semantic Structure Plan

    [Landmark regions, heading hierarchy, list structures, form structure, document outline]

    ### Structure Diagram

    [HTML structure stub showing semantic elements]

    ## Interaction Pattern Design

    [For each interactive widget: APG pattern mapping, keyboard model, ARIA attributes, screen reader announcements]

    ### Interactive Elements Table

    | Widget | APG Pattern | Keyboard Model | ARIA Attributes | WCAG Citation |
    |--------|-------------|----------------|-----------------|---------------|
    | [Name] | [Link to pattern] | [Tab, Enter, Space, Escape, Arrows] | [aria-* list] | [2.1.1, 4.1.2, etc] |

    ## Focus Management Plan

    [Tab order, focus traps for modals, focus restoration, skip link, composite widget roving tabindex]

    ## State Communication Design

    [How each state (expanded, selected, disabled, invalid, loading, etc.) is communicated visually and programmatically]

    ### State Communication Table

    | State | Visual Indicator | Programmatic Indicator | ARIA Attribute | WCAG Citation |
    |-------|-----------------|----------------------|-----------------|---------------|
    | [State] | [Color/icon/text] | [Attribute] | [aria-*] | [1.3.1, 4.1.2, etc] |

    ## Visual Accessibility Plan

    [Color contrast, non-color alternatives, font sizing, responsive text, animation/motion handling, touch target sizing]

    ## Content Accessibility Plan

    [Alt text strategy, link text quality, form labels, error message clarity, language attributes, reading order]

    ## Testing Strategy

    [Automated testing, keyboard navigation testing, screen reader testing, visual regression testing, acceptance criteria]

    ### Test Cases

    - [Keyboard navigation: Tab through all elements, verify logical order]
    - [Keyboard activation: Focus button, press Enter/Space, verify action]
    - [Escape to close: Open modal, press Escape, verify it closes and focus restores]
    - [ARIA state: Verify aria-expanded toggles, aria-selected reflects selection, etc.]
    - [Screen reader: Verify landmarks announced, headings hierarchical, live regions announce updates]
    - [Contrast: Verify all text 4.5:1 (normal) or 3:1 (large)]
    - [200% zoom: Verify layout reflows without horizontal scroll]

    ## Implementation Tasks

    ### Task 1: [Component Name]
    🔍 **Review checkpoint after this task**

    **Files:**
    - [files to create/modify]

    **Structure Stub:**
    [HTML structure with semantic elements and ARIA attributes]

    **ARIA Attributes:**
    - [attribute]: [description and WCAG citation]

    **Keyboard Interactions:**
    - [key]: [behavior]

    **Tests:**
    - [test case 1]
    - [test case 2]

    **WCAG Criteria:**
    - [WCAG 2.1.1 Keyboard, etc.]

    [Continue for each task...]

    ## a11y-Critic Review Checkpoints

    | Checkpoint | After Task | Focus Areas |
    |-----------|-----------|------------|
    | 🔍 1 | Task N | Verify APG pattern is complete, aria-expanded/selected/pressed is correct, focus management works, state is announced |

    ---

    ### Contract Appendix (for spec-kitty-bridge WP translation)

    When output will be consumed by spec-kitty-bridge, append these standardized sections after the domain-specific output above:

    ### Architecture Overview
    [Brief summary of component count, ARIA patterns, and keyboard interaction design from the plan above]

    ### Implementation Tasks
    For each task already listed above, add:
    #### Task {N}: {Component Name}
    Estimated Effort: {low | medium | high}
    Depends on: {[list of task numbers] or "none"}
    #### Test Strategy for Task {N}
    [Extracted from Tests field above]
    #### Acceptance Criteria for Task {N}
    [Derived from WCAG criteria and APG pattern requirements]

    ### Failure Modes
    [Consolidated from accessibility design anti-patterns that this plan prevents]

    ## References

    - [WAI-ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/)
    - [WCAG 2.2 Specification](https://www.w3.org/WAI/WCAG22/quickref/)
    - [a11y-critic skill](https://github.com/zivtech/a11y-critic) — for post-implementation review
    - [accessibility-testing skill](https://github.com/zivtech/zivtech-claude-skills) — for automated testing
    ```

  </Planning_Protocol>

  <Failure_Modes_To_Avoid>
    - Vague plans: "Use aria-expanded for disclosure" without specifying the APG pattern, keyboard interactions, focus management, or test cases
    - Missing APG pattern mapping: Designing a custom interaction pattern when an established APG pattern exists (Disclosure, Menu Button, Tabs, Modal, etc.)
    - Missing WCAG grounding: Making design decisions without citing WCAG criteria (every decision should cite 2.1.1, 4.1.2, 1.3.1, etc.)
    - Incomplete state communication: Planning some states (expanded) but missing others (disabled, invalid, loading)
    - No focus management planning: Assuming focus "just works" without designing tab order, focus traps, and focus restoration
    - Color-only indicators: Using color alone to convey state/meaning without text/icon/shape alternative
    - No testing strategy: "We'll test after implementation" guarantees gaps
    - Scope creep: Over-planning trivial components. A button needs 1 line, not 5 pages.
    - Visual-only state communication: Error indicated only by red border, without aria-invalid and associated error message
    - Missing skip link: No way to jump past navigation to main content
  </Failure_Modes_To_Avoid>

  <Examples>
    <Good>
      User: "Plan the accessibility of a search form with results and filters"
      Planner output:
      Scope: Search form with live results and filterable sidebar. Users need keyboard navigation, screen reader compatibility, focus management on dynamic results.
      Semantic structure: nav > search form (fieldset, legend), main > (aside for filters, section for results). Heading hierarchy: h1 (page title), h2 (filters), h2 (results).
      Interaction patterns:
        - Search input: native HTML input element, associated with label, autocomplete suggestions (APG Combobox pattern if autocomplete)
        - Search button: native button element, responds to Enter (default form submission)
        - Filter toggles: per APG Disclosure pattern, aria-expanded toggles, aria-controls references filter content
        - Result items: native link elements with descriptive text
      Focus management: Tab enters search input, Tab moves to search button, Tab moves to filter toggles, Tab moves to result links. Skip link at top to jump to main content. When results load, focus doesn't automatically move (user may still be typing).
      State communication: Search loading indicated with aria-busy="true" and role="status" message. Filters expanded/collapsed via aria-expanded. Result count announced in aria-live="polite" region.
      Visual accessibility: Search button meets 44x44 touch target. Focus indicators have 3:1 contrast. Text resizable (rem units, not px). Color is not sole indicator (search icon + text).
      Content: Search input has associated label. Filter toggles have clear names. Result links have descriptive text (not just "Read more"). Filter instructions if needed.
      Testing: Keyboard navigation (Tab through all elements), arrow keys (if autocomplete), live region announcements (results count updates), state communication (aria-expanded toggles, aria-busy changes), screen reader (structure clear, links descriptive).
      Implementation: SearchForm component (input + button + label), FilterSidebar (disclosure widget), ResultsList (link items with aria-live region), tests for keyboard nav + state changes + announcements.
      Why good: Complete a11y design mapped to APG patterns, WCAG citations, focus management designed, state communication specified, testing strategy includes keyboard + screen reader + live regions.
    </Good>

    <Good>
      User: "Plan the accessibility of a modal dialog with a form"
      Planner output:
      Scope: Modal dialog for user signup form. Users need focus trap, focus restoration, form validation errors, keyboard-only access.
      Semantic structure: <div role="dialog" aria-modal="true" aria-labelledby="dialog-title">. Inside: h2#dialog-title for modal title, form with inputs and labels, submit button, close button (aria-label="Close").
      Interaction pattern: APG Modal Dialog pattern (https://www.w3.org/WAI/ARIA/apg/patterns/dialogmodal/). Keyboard model: Tab traps within modal (last element Tabs to first), Escape closes modal. Close button and submit button provide exit paths.
      Focus management: When modal opens, focus moves to first interactive element (e.g., first form input or close button). When modal closes, focus returns to trigger button. Tab cycles within modal, never escapes to background. Escape closes modal and restores focus.
      State communication: Form inputs have associated labels (label for=""). Error messages associated via aria-describedby. aria-invalid="true" on inputs with errors. Validation errors announced in aria-live="assertive" region.
      Visual accessibility: Close button 44x44 touch target. Focus indicator visible. Form errors: red border + error icon + error text (color not sole indicator).
      Content: Modal has clear title (aria-labelledby). Close button has aria-label="Close". Form inputs have labels. Error messages are specific and helpful.
      Testing: Focus trap test (Tab cycles within modal, never reaches background), Escape closes modal, focus restores, form validation errors announced, keyboard activation (Enter submits form), screen reader announces modal title and form structure.
      Implementation: Modal component (role="dialog", focus trap logic, Escape handler, focus restoration), Form component (inputs with labels, error handling), tests for focus trap + Escape close + focus restoration + aria-invalid.
      Why good: Follows APG Modal Dialog pattern completely, focus management designed in detail, state communication for form validation, all tests specified, WCAG citations (2.1.1, 2.1.2, 4.1.2, 4.1.3).
    </Good>

    <Bad>
      User: "Plan the accessibility of a search form"
      Planner output: "Task 1: Create search input. Task 2: Create search button. Task 3: Handle results. Task 4: Add filters."
      Why bad: No APG pattern mapping, no focus management planning, no state communication design, no testing strategy, no WCAG citations. Guarantees accessibility will be incomplete when implemented.
    </Bad>
  </Examples>

  <Final_Checklist>
    - Did I understand the feature scope, compliance target, and user needs?
    - Did I create a complete semantic structure plan with landmarks, heading hierarchy, form structure?
    - Did I map every interactive widget to a specific APG pattern with citation?
    - Did I design keyboard interactions for every interactive element (Tab, Enter, Space, Escape, Arrows)?
    - Did I plan focus management (tab order, focus traps for modals, focus restoration)?
    - Did I design state communication (visual + programmatic for every state)?
    - Did I cite WCAG success criteria for every design decision?
    - Did I specify all ARIA attributes required?
    - Did I plan visual accessibility (color contrast, non-color alternatives, responsive text, touch targets)?
    - Did I plan content accessibility (alt text, link text, form labels, error message clarity)?
    - Did I create a complete testing strategy (keyboard navigation, screen reader, live regions, visual regression)?
    - Did I break down implementation into clear tasks with a11y-critic review checkpoints?
    - Did I avoid scope creep (simple components get simple plans, complex features get detailed plans)?
    - Are there any "figure this out during implementation" placeholders? (Bad — be specific)
    - Is every design decision grounded in WCAG 2.2 or APG?
  </Final_Checklist>
</A11y_Design_Planning_Protocol>
```

## Tool_Usage

When invoking a11y-planner:
- Use Read to examine existing code if redesigning an existing feature
- Use Grep to verify accessibility patterns in the codebase
- Use Bash to check package.json and project structure
- Write the plan document to `docs/a11y-plans/` in the project

## Companion Skills

This skill is part of the Zivtech a11y tooling ecosystem:

| Skill | When | What |
|-------|------|------|
| a11y-planner | First | Design accessibility BEFORE implementation (this skill) |
| accessibility-standards | Reference | WCAG 2.2 AA coding patterns and standards |
| brainstorming | Optional | Explore multiple accessibility design approaches before committing |
| Implementation | During | Build according to the a11y-planner design |
| a11y-critic | After | Review the implementation for design soundness, pattern completeness, gap analysis |
| accessibility-testing | After | Run automated tests (axe-core, Pa11y-CI), keyboard navigation tests |
| a11y-test | After | Manual keyboard testing with real Playwright key presses |

Use a11y-planner upfront to design accessibility. Build according to the plan. Then use a11y-critic to verify the design was followed.

## Examples

<Good_Use>
User: "Plan the accessibility of a modal dialog for user feedback"
1. You ask: "Who needs accessibility? Screen reader users? Keyboard-only users? Low vision users? All?" User: "All users."
2. You invoke a11y-planner with the feature description and the 9-phase protocol.
3. Planner produces: Semantic structure (dialog role, aria-modal, aria-labelledby), Interaction pattern (APG Modal Dialog), Focus management (focus trap, focus restoration on Escape), State communication (form validation errors via aria-describedby), Visual accessibility (color contrast, touch targets), Content (modal title clear, close button labeled), Testing (focus trap test, Escape closes, focus restores, form validation announced).
4. Returns structured plan with implementation tasks and a11y-critic review checkpoints.
</Good_Use>

<Good_Use>
User: "We have an a11y-critic REVISE verdict on our tabs component. Can you re-plan the accessibility?"
1. You read the a11y-critic review findings (e.g., "tabs missing arrow key navigation", "aria-selected not synchronized", "focus doesn't move to panel on tab selection")
2. You invoke a11y-planner focused on the specific gaps
3. Planner produces revised design: Arrow key navigation per APG Tabs pattern, aria-selected state management, focus movement to active tab panel, roving tabindex implementation
4. Returns focused implementation tasks to fix the specific findings
</Good_Use>

<Bad_Use>
User: "Create a button."
Your response: "A button is trivial. Just use <button>. No need for a11y-planner."
Instead, if the button has complex interactions or is part of a complex feature, invoke a11y-planner. Otherwise, just build it.
</Bad_Use>

## Related Skills in Zivtech Tooling

- **a11y-critic**: Review accessibility design decisions post-implementation. Read-only reviewer, harsh verdicts, evidence-backed findings.
- **accessibility-testing**: Run automated tests (axe-core, Pa11y-CI), keyboard navigation tests, visual regression tests.
- **a11y-test**: Real keyboard testing with Playwright. Tests real key presses, not just ARIA attributes.
- **accessibility-standards**: WCAG 2.2 AA reference, coding patterns, four-layer enforcement architecture.
