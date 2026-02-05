---
name: "specimin-ui-accessibility"
description: "Explicit accessibility enhancement and validation for generated UI code. Only invoke when user explicitly requests accessibility review, a11y enhancement, or WCAG compliance check."
allowed-tools:
  - run_terminal_cmd
  - write
  - read_file
---

**REQUIRES ui-generate to be completed first.**
This skill performs deep accessibility enhancement and validation. **Manual testing is MANDATORY.**

# UI Accessibility Enhancement Agent

## Role
Accessibility specialist ensuring WCAG 2.1 Level AA compliance through code enhancement and validation. **Critical**: Research shows 80%+ of AI-generated code has accessibility violations. This skill provides systematic fixes and mandatory manual testing checklist.

## ⚠️ Critical Understanding

**Why This Skill Exists**:
> "Accessibility is by definition non-typical usage, therefore applying an average does not work."
> — Research finding on AI-generated accessibility failures

**Research Evidence**:
- 80%+ of initial AI generations have semantic HTML violations
- ChatGPT produced ZERO ARIA implementation in accessibility tests
- Bard generated ARIA roles on wrong elements with broken references
- Even accessibility-trained models produce WCAG-failing code
- Automated tools catch only 60-70% of violations
- **Manual validation with assistive technologies is MANDATORY**

**This skill cannot fully automate accessibility**. It provides:
1. Systematic code enhancements
2. Automated audit (catches 60-70% of issues)
3. **Mandatory manual testing checklist**

## Process Flow

### Stage 1: Load Generated Code

1. Find current feature branch and generated files:
```bash
BRANCH=$(git branch --show-current)
FEATURE_DIR=".specimin/ui/$BRANCH"
```

2. Read generation-report.md to identify:
   - Files created/modified
   - Components generated
   - Known accessibility issues flagged

3. Read all generated code files for analysis

### Stage 2: Semantic HTML Audit

**Check every element for semantic correctness**:

#### Common Violations (Fix These)

**Navigation Elements**:
- ❌ `<div class="nav">`
- ✅ `<nav aria-label="Main navigation">`

**Buttons vs Links**:
- ❌ `<div onClick={...}>` (not focusable, not keyboard accessible)
- ❌ `<a onClick={...}>` (link semantics incorrect for actions)
- ✅ `<button onClick={...}>` (semantic, focusable, keyboard accessible)
- ✅ `<a href="/page">` (navigation only)

**Headings**:
- ❌ Skipping levels: h1 → h3 (violates heading hierarchy)
- ❌ Using `<div class="text-2xl font-bold">` instead of headings
- ✅ Proper hierarchy: h1 → h2 → h3 (logical nesting)
- ✅ One h1 per page (page title)

**Form Controls**:
- ❌ `<input>` without `<label>`
- ❌ Label not programmatically associated (visual only)
- ✅ `<label for="email">` with `<input id="email">`
- ✅ Or `<label><input></label>` (implicit association)

**Landmark Regions**:
- ❌ `<div class="main-content">`
- ✅ `<main>` (primary content landmark)
- ✅ `<aside>` (sidebar, complementary content)
- ✅ `<footer>` (footer landmark)

**Lists**:
- ❌ `<div><div>Item 1</div><div>Item 2</div></div>`
- ✅ `<ul><li>Item 1</li><li>Item 2</li></ul>`

**Dialogs/Modals**:
- ❌ `<div class="modal">`
- ✅ `<dialog>` (native HTML5 dialog element, preferred)
- ✅ Or `<div role="dialog" aria-modal="true">`

### Stage 3: ARIA Implementation

**Critical Principle**: Use ARIA **only when semantic HTML is insufficient**.

> "First rule of ARIA: Don't use ARIA if you can use a native HTML element or attribute."
> — W3C ARIA Authoring Practices

#### When ARIA Is Needed

**Dropdown Menus**:
```html
<!-- Button trigger -->
<button
  aria-haspopup="true"
  aria-expanded="false"
  aria-controls="menu-id"
  id="menu-button">
  Menu
</button>

<!-- Dropdown menu -->
<div
  role="menu"
  aria-labelledby="menu-button"
  id="menu-id"
  hidden>
  <button role="menuitem">Item 1</button>
  <button role="menuitem">Item 2</button>
</div>
```

**Tabs**:
```html
<div role="tablist" aria-label="Product details">
  <button role="tab" aria-selected="true" aria-controls="panel-1" id="tab-1">
    Description
  </button>
  <button role="tab" aria-selected="false" aria-controls="panel-2" id="tab-2">
    Reviews
  </button>
</div>

<div role="tabpanel" id="panel-1" aria-labelledby="tab-1">
  Description content
</div>
<div role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden>
  Reviews content
</div>
```

**Modal Dialogs**:
```html
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="dialog-title"
  aria-describedby="dialog-desc">
  <h2 id="dialog-title">Confirm Action</h2>
  <p id="dialog-desc">Are you sure you want to delete this item?</p>
  <button>Cancel</button>
  <button>Delete</button>
</div>
```

**Live Regions** (status messages, notifications):
```html
<div role="status" aria-live="polite" aria-atomic="true">
  Form submitted successfully
</div>

<div role="alert" aria-live="assertive">
  Error: Please fix the highlighted fields
</div>
```

**Hidden Content** (visually hidden but screen-reader accessible):
```html
<span class="sr-only">Opens in new window</span>
<!-- Tailwind sr-only class: position: absolute; width: 1px; ... -->
```

#### Common ARIA Mistakes to Fix

**Wrong Elements**:
- ❌ `<li role="dialog">` (dialog role on list item)
- ✅ Use correct element for role

**Broken References**:
- ❌ `aria-labelledby="nonexistent-id"` (ID doesn't exist)
- ✅ Ensure all ARIA references point to valid IDs

**Incomplete Patterns**:
- ❌ `aria-expanded` attribute that never updates
- ✅ Ensure state attributes change with UI state

**Redundant ARIA**:
- ❌ `<button role="button">` (redundant)
- ✅ `<button>` (native semantics sufficient)

### Stage 4: Keyboard Navigation Enhancement

**Every interactive element must be keyboard accessible.**

#### Focus Management

**Tab Order**:
- All interactive elements receive focus in logical order
- Skip to main content link (first focusable element)
- Tab through navigation → main content → footer
- No focus traps (except intentional like modals)

**Visible Focus Indicators**:
```html
<!-- Tailwind focus styles -->
<button class="... focus:outline-none focus:ring-2 focus:ring-blue-500">
  Click me
</button>

<!-- Custom focus (if needed) -->
<a class="... focus:underline focus:ring-2">
  Link
</a>
```

#### Keyboard Event Handlers

**Modals**:
```javascript
// Escape key closes modal
onKeyDown={(e) => {
  if (e.key === 'Escape') closeModal();
}}

// Focus trap inside modal (Tab cycles within)
// Return focus to trigger when closed
```

**Dropdowns**:
```javascript
// Enter/Space opens dropdown
// Arrow keys navigate items
// Escape closes
// Tab closes and moves focus
```

**Custom Components** (not native):
```javascript
// Enter and Space both activate
onKeyDown={(e) => {
  if (e.key === 'Enter' || e.key === ' ') {
    e.preventDefault();
    handleActivate();
  }
}}
```

#### Framework-Specific Patterns

**React**:
```typescript
import { useRef, useEffect } from 'react';

// Focus management
const modalRef = useRef<HTMLDialogElement>(null);

useEffect(() => {
  if (isOpen) {
    modalRef.current?.focus();
    // Trap focus logic
  }
}, [isOpen]);
```

**Phoenix LiveView**:
```elixir
# Focus on mount
def mount(_params, _session, socket) do
  {:ok, socket, temporary_assigns: [focus: "modal-id"]}
end

# HEEx template
<div id={@focus} phx-hook="FocusOnMount">
```

**Vue**:
```vue
<script setup>
import { ref, onMounted } from 'vue';

const modalRef = ref(null);

onMounted(() => {
  if (isOpen.value) {
    modalRef.value?.focus();
  }
});
</script>
```

### Stage 5: Additional Accessibility Requirements

#### Images and Media

**Alt Text**:
- ❌ `<img src="photo.jpg">` (no alt)
- ❌ `<img src="logo.jpg" alt="logo">` (redundant)
- ✅ `<img src="logo.jpg" alt="Company Name">` (descriptive)
- ✅ `<img src="decorative.jpg" alt="">` (decorative image, empty alt)

**Videos**:
- Captions/subtitles for audio content
- Transcripts available
- Playback controls keyboard accessible

#### Color and Contrast

**Color Not Sole Indicator**:
- ❌ Red text only to indicate errors
- ✅ Red text + icon + explicit "Error:" label

**Contrast Ratios** (WCAG AA):
- Normal text: 4.5:1 minimum
- Large text (18pt+ or 14pt bold+): 3:1 minimum
- UI components and graphics: 3:1 minimum

**Check**:
- Tailwind default colors generally pass (gray-700+ on white)
- Custom colors need manual verification
- Use browser DevTools Accessibility checker

#### Forms

**Labels**:
- Every input has associated label
- Label text describes purpose clearly
- Group related inputs with `<fieldset>` and `<legend>`

**Validation**:
- Error messages programmatically associated with inputs
- `aria-invalid="true"` on invalid fields
- `aria-describedby` pointing to error message ID

**Required Fields**:
```html
<label for="email">
  Email <span aria-label="required">*</span>
</label>
<input
  type="email"
  id="email"
  required
  aria-required="true"
  aria-describedby="email-error">
<span id="email-error" role="alert">
  <!-- Error message inserted here -->
</span>
```

#### Responsive and Zoom

**Text Resize**:
- Content readable at 200% zoom without horizontal scroll
- No fixed pixel font sizes (use rem)
- Avoid `user-scalable=no` in viewport meta

**Touch Targets**:
- Minimum 44x44 pixels (mobile)
- Adequate spacing between interactive elements
- Tailwind: `p-2` typically sufficient, `min-h-[44px]` if needed

### Stage 6: Automated Accessibility Audit

**Run conceptual equivalent of axe-core checks**:

#### Checklist

**Critical (Must Fix)**:
- [ ] All images have alt attributes
- [ ] Form inputs have labels
- [ ] Buttons have accessible names
- [ ] Links have discernible text
- [ ] Page has `<html lang="...">` attribute
- [ ] Page has meaningful `<title>`
- [ ] Heading hierarchy valid (no skipping)
- [ ] Color contrast sufficient (4.5:1 text, 3:1 UI)
- [ ] No keyboard traps
- [ ] ARIA references valid (IDs exist)

**Serious (Should Fix)**:
- [ ] Landmarks present (main, nav, footer)
- [ ] Skip links available
- [ ] Focus indicators visible
- [ ] ARIA attributes correct for roles
- [ ] Lists use semantic markup (ul/ol)
- [ ] Tables have proper headers (if used)

**Moderate (Consider)**:
- [ ] Explicit language changes marked (`lang` attribute)
- [ ] Abbreviations explained (first use)
- [ ] Link text descriptive (not "click here")

### Stage 7: Generate Accessibility Report

Create accessibility-report.md documenting:

**Audit Results**:
- Violations found and fixed
- Automated check results (pass/fail)
- WCAG 2.1 Level AA compliance status

**Enhancements Made**:
- Semantic HTML improvements
- ARIA additions
- Keyboard navigation enhancements
- Focus management implementations

**Manual Testing Checklist** (MANDATORY):
- [ ] Keyboard-only navigation test
- [ ] Screen reader testing (NVDA/JAWS/VoiceOver)
- [ ] Zoom to 200% test
- [ ] Color contrast verification
- [ ] Touch target size verification (mobile)

**Known Limitations**:
- Automated tools catch 60-70% of issues
- Context-dependent problems require human judgment
- Screen reader quirks across devices
- Business logic validation

### Stage 8: Present Manual Testing Checklist

**Critical**: Show user this mandatory checklist:

```
## 🔴 MANDATORY Manual Accessibility Testing

AI-generated code requires human validation. Complete ALL checks below:

### Keyboard Navigation Test (30 minutes)
- [ ] Unplug mouse (force keyboard-only)
- [ ] Tab through entire interface
- [ ] Verify logical tab order
- [ ] Test all interactive elements (Enter/Space to activate)
- [ ] Escape closes modals/dropdowns
- [ ] No focus traps (except intentional)
- [ ] Focus indicators clearly visible

### Screen Reader Test (1 hour)
**Windows** (NVDA - free):
- [ ] Download NVDA (https://www.nvaccess.org/)
- [ ] Navigate page with screen reader on
- [ ] Verify all content announced
- [ ] Check heading navigation (H key)
- [ ] Check landmark navigation (D key)
- [ ] Verify form labels read correctly
- [ ] Test interactive widgets (modals, dropdowns, tabs)

**Mac/iOS** (VoiceOver - built-in):
- [ ] Enable VoiceOver (Cmd+F5)
- [ ] Navigate with VO keys (Control+Option+arrows)
- [ ] Verify rotor navigation (landmarks, headings)
- [ ] Test on Safari (primary VO browser)

**Basics to verify**:
- Page title announced on load
- Headings provide page structure
- Buttons/links clearly identified
- Form fields have labels
- Error messages read aloud
- Status updates announced (live regions)

### Visual Test (15 minutes)
- [ ] Zoom browser to 200% (Cmd/Ctrl + +)
- [ ] No horizontal scroll appears
- [ ] All content remains readable
- [ ] No text overlap
- [ ] Interactive elements still usable

### Color Contrast Test (15 minutes)
- [ ] Use browser DevTools Accessibility tab
- [ ] Check all text meets 4.5:1 ratio (normal text)
- [ ] Check 3:1 ratio for large text and UI components
- [ ] Verify error states use more than color alone

### Mobile/Touch Test (30 minutes)
- [ ] Test on actual device (not just emulator)
- [ ] All touch targets minimum 44x44 pixels
- [ ] Adequate spacing between interactive elements
- [ ] Pinch zoom works (not disabled)
- [ ] Landscape and portrait orientations work

### Total Time: ~2.5-3 hours
This cannot be skipped. Accessibility cannot be automated away.
```

### Stage 9: Finalize

**ONLY after user acknowledges manual testing requirement**:

1. Write accessibility-report.md to feature directory
2. Commit accessibility enhancements:
```bash
bash ${CLAUDE_PLUGIN_ROOT}/.claude-plugin/skills/specimin-ui-accessibility/scripts/save-accessibility.sh "$BRANCH"
```

3. Confirm to user:
   "✓ Accessibility enhancements applied and committed.

   ⚠️  **NEXT STEP REQUIRED**: Complete manual accessibility testing checklist.
   See .specimin/ui/[branch]/accessibility-report.md for full checklist.

   After testing complete, run `specimin:wrap` to create PR."

## Output: Accessibility Report Format

```markdown
# Accessibility Report - [Feature Name]

## Executive Summary
- **WCAG Level**: AA (Target)
- **Automated Compliance**: [X]% of checks passed
- **Manual Testing**: ⚠️ REQUIRED (see checklist below)
- **Critical Issues**: [N] found and fixed
- **Status**: ✅ Ready for Manual Testing | ⚠️ Issues Remain | ❌ Blocked

## Violations Found and Fixed

### Critical (Blocking)

#### 1. Non-Semantic Button Elements
**Found**: `<div onClick={handleClick}>Submit</div>`
**Issue**: Not keyboard accessible, no semantic meaning
**WCAG**: 4.1.2 Name, Role, Value (Level A)
**Fixed**: Changed to `<button onClick={handleClick}>Submit</button>`

#### 2. Missing Form Labels
**Found**: `<input type="email" placeholder="Email">`
**Issue**: Screen readers cannot identify field purpose
**WCAG**: 3.3.2 Labels or Instructions (Level A)
**Fixed**: Added `<label for="email">Email</label>` with association

#### 3. Skipped Heading Level
**Found**: h1 → h3 (skipped h2)
**Issue**: Breaks document structure for screen readers
**WCAG**: 2.4.6 Headings and Labels (Level AA)
**Fixed**: Changed to h2, adjusted visual styling

### Serious (Should Fix)

#### 4. Missing Landmark Regions
**Found**: `<div class="main-content">`
**Issue**: Screen reader users cannot navigate by landmarks
**WCAG**: 4.1.2 Name, Role, Value (Level A)
**Fixed**: Changed to `<main>` element

#### 5. Incomplete ARIA Pattern
**Found**: Dropdown with `aria-expanded` never updating
**Issue**: Screen reader announces incorrect state
**WCAG**: 4.1.2 Name, Role, Value (Level A)
**Fixed**: Added state management to toggle `aria-expanded` on open/close

### Moderate (Enhancements)

#### 6. Generic Link Text
**Found**: `<a href="/docs">Click here</a>`
**Issue**: Not descriptive out of context
**WCAG**: 2.4.4 Link Purpose (Level A)
**Fixed**: Changed to `<a href="/docs">View documentation</a>`

## Enhancements Applied

### Semantic HTML Improvements
- Replaced 8 div elements with semantic alternatives (nav, main, button)
- Established proper heading hierarchy (h1 → h2 → h3)
- Used list elements (ul/li) for navigation and feature lists

### ARIA Additions
- Modal dialog: Added `role="dialog"`, `aria-modal="true"`, `aria-labelledby`
- Dropdown menu: Added `aria-haspopup`, `aria-expanded`, `aria-controls`
- Live region: Added `role="status"` for form submission feedback
- Hidden content: Added `aria-hidden="true"` to decorative elements

### Keyboard Navigation
- Focus indicators: Added `focus:ring-2 focus:ring-blue-500` to all interactive elements
- Modal keyboard handling: Escape closes, focus trap implemented, focus restoration on close
- Dropdown keyboard handling: Enter/Space opens, Arrow keys navigate, Escape closes

### Focus Management
**Modal open sequence**:
1. Trap focus inside modal
2. Focus first interactive element
3. Tab cycles within modal
4. Escape restores focus to trigger button

**Implementation**:
- React: useEffect + useRef pattern
- Phoenix LiveView: phx-hook="FocusManagement"
- Vue: onMounted + ref pattern

## Automated Audit Results

### axe-core Equivalent Checks

✅ **Passed (35/40)**:
- All images have alt attributes
- Form inputs have associated labels
- Color contrast meets WCAG AA (4.5:1)
- HTML lang attribute present
- Page title meaningful
- No duplicate IDs
- ARIA references valid
- Buttons have accessible names
- [... full list]

❌ **Failed (0/40)**: None remaining

⚠️ **Manual Review Needed (5/40)**:
- Alt text quality (requires context judgment)
- Heading structure appropriateness (requires content understanding)
- Link text descriptiveness (requires context)
- Form error message clarity (requires UX review)
- Color not sole indicator (requires visual review)

## Known Limitations

### Automated Testing Boundaries
- **Coverage**: Automated tools catch 60-70% of accessibility issues
- **Context**: Cannot judge appropriateness of alt text, heading levels
- **Screen Reader Quirks**: Differences between NVDA, JAWS, VoiceOver
- **User Experience**: Cannot test actual navigation flows

### Framework-Specific Considerations
**Phoenix LiveView**:
- Client-side JavaScript hooks used for focus management
- Server-side validation messages need `phx-feedback-for` for proper timing
- Live navigation requires `aria-live` regions for route changes

**React**:
- Focus management requires refs and useEffect
- Router transitions need announcement to screen readers
- State updates need `aria-live` for status messages

### Business Logic Gaps
- Form validation error messages (content not generated)
- Loading states and spinners (design not provided)
- Error recovery flows (business logic needed)

## 🔴 MANDATORY Manual Testing Checklist

**Estimated Time: 2.5-3 hours**

AI-generated code CANNOT be shipped without human accessibility testing.

### 1. Keyboard Navigation Test (30 min)

**Setup**: Unplug mouse, use keyboard only

- [ ] **Tab Order**: Logical progression through interface
- [ ] **Skip Link**: "Skip to main content" link works (if present)
- [ ] **Navigation**: Tab through all nav items, Enter/Space activates
- [ ] **Forms**: Tab through fields, Space checks checkboxes, Enter submits
- [ ] **Buttons**: Enter or Space activates all buttons
- [ ] **Modals**: Escape closes, focus trapped inside when open
- [ ] **Dropdowns**: Enter/Space opens, Escape closes, Arrow keys navigate (if applicable)
- [ ] **Focus Indicators**: Always visible, never hidden by CSS
- [ ] **No Traps**: Can Tab to and from every interactive element

**Tools**: None required (keyboard only)

### 2. Screen Reader Test (1 hour)

**Windows - NVDA (Free)**:
Download: https://www.nvaccess.org/download/

- [ ] **Install NVDA**: Follow wizard, restart optional
- [ ] **Launch NVDA**: Desktop shortcut or Ctrl+Alt+N
- [ ] **Open Page**: Use Chrome or Firefox (best NVDA support)
- [ ] **Listen to Page Load**: Page title announced
- [ ] **Navigate by Headings**: Press H to jump between headings
- [ ] **Navigate by Landmarks**: Press D to jump between regions (main, nav, etc.)
- [ ] **Navigate by Elements**: Press B (buttons), K (links), F (forms)
- [ ] **Test Form**: Arrow through fields, hear labels, submit, hear confirmation
- [ ] **Test Interactive Widgets**: Modals, dropdowns, tabs (verify announcements)
- [ ] **Verify Images**: Images announce alt text, decorative images skipped

**Mac/iOS - VoiceOver (Built-in)**:
- [ ] **Enable VO**: Cmd+F5 (Mac) or Settings > Accessibility > VoiceOver (iOS)
- [ ] **Open Page**: Use Safari (best VO support)
- [ ] **Navigate**: Control+Option+Arrow keys (Mac), swipe (iOS)
- [ ] **Rotor Navigation**: Control+Option+U for landmarks/headings menu
- [ ] **Test Interactive Elements**: Buttons, links, forms
- [ ] **Verify Announcements**: All content understandable via audio only

**What to Listen For**:
- Clear, descriptive announcements (not "button button" or "link graphic")
- Form labels read before input fields
- Error messages announced immediately
- Status updates announced (form submission, loading)
- Modal open/close announced
- All text content accessible (nothing skipped)

### 3. Visual/Zoom Test (15 min)

- [ ] **Zoom 200%**: Cmd/Ctrl and press + until 200%
- [ ] **No Horizontal Scroll**: Content reflows, doesn't require side-scrolling
- [ ] **Text Readable**: All text remains legible, no overlap
- [ ] **Interactive Elements**: Buttons, links still clickable
- [ ] **Layout Intact**: No broken layouts, content still usable

**Tools**: Browser zoom (Cmd/Ctrl + +)

### 4. Color Contrast Test (15 min)

- [ ] **Open DevTools**: F12 or Right-click > Inspect
- [ ] **Accessibility Tab**: Chrome DevTools > Accessibility pane
- [ ] **Check Elements**: Inspect text elements, view contrast ratio
- [ ] **Verify Ratios**: Normal text ≥4.5:1, large text ≥3:1, UI components ≥3:1
- [ ] **Color Not Sole Indicator**: Errors use icon + text, not just red color

**Tools**: Chrome DevTools Accessibility panel

### 5. Mobile/Touch Test (30 min)

- [ ] **Real Device**: Test on actual phone/tablet (emulator insufficient for touch)
- [ ] **Touch Targets**: All buttons/links easily tappable (44x44px minimum)
- [ ] **Spacing**: Adequate space between interactive elements (no mis-taps)
- [ ] **Pinch Zoom**: Works (viewport doesn't disable)
- [ ] **Orientation**: Portrait and landscape both work
- [ ] **Screen Reader**: Test VoiceOver on iOS or TalkBack on Android
- [ ] **Gestures**: Swipe navigation works with screen reader

**Tools**: Physical mobile device

## Testing Resources

### Screen Readers
- **NVDA (Windows, Free)**: https://www.nvaccess.org/
- **JAWS (Windows, Paid)**: https://www.freedomscientific.com/products/software/jaws/
- **VoiceOver (Mac/iOS, Built-in)**: Cmd+F5 or Settings > Accessibility
- **TalkBack (Android, Built-in)**: Settings > Accessibility > TalkBack

### Browser Tools
- **Chrome DevTools**: Accessibility panel, Lighthouse audit
- **Firefox DevTools**: Accessibility inspector
- **axe DevTools**: Browser extension (free version available)
- **WAVE**: Browser extension for visual accessibility review

### Color Contrast Checkers
- **WebAIM Contrast Checker**: https://webaim.org/resources/contrastchecker/
- **Colour Contrast Analyser**: Desktop app (free)

### Learning Resources
- **WebAIM**: https://webaim.org/ (comprehensive guides)
- **W3C ARIA Authoring Practices**: https://www.w3.org/WAI/ARIA/apg/
- **A11y Project**: https://www.a11yproject.com/ (checklist and resources)

## Sign-Off

**Accessibility testing completed by**: ___________________
**Date**: ___________________
**Screen reader used**: ___________________
**Devices tested**: ___________________

**Issues found during manual testing**:
- [ ] None - all tests passed
- [ ] Issues found (list below):

___________________________________________________________________
___________________________________________________________________

**Ready for production**: [ ] Yes [ ] No

## Next Steps

1. **Complete manual testing** using checklist above (~3 hours)
2. **Document any issues** found during testing
3. **Fix critical issues** before production deployment
4. **Re-test** after fixes applied
5. **Run `specimin:wrap`** to create PR when ready
6. **Include accessibility testing notes** in PR description

---

## Appendix: WCAG 2.1 Level AA Compliance

### Principles Covered

**Perceivable**:
- ✅ 1.1.1 Non-text Content (Alt text for images)
- ✅ 1.3.1 Info and Relationships (Semantic HTML, ARIA)
- ✅ 1.4.3 Contrast (Minimum) (4.5:1 for text)
- ✅ 1.4.10 Reflow (No horizontal scroll at 200% zoom)
- ✅ 1.4.11 Non-text Contrast (3:1 for UI components)

**Operable**:
- ✅ 2.1.1 Keyboard (All functionality via keyboard)
- ✅ 2.1.2 No Keyboard Trap (Can Tab out of all elements)
- ✅ 2.4.1 Bypass Blocks (Skip links, landmarks)
- ✅ 2.4.3 Focus Order (Logical tab order)
- ✅ 2.4.6 Headings and Labels (Descriptive, hierarchical)
- ✅ 2.4.7 Focus Visible (Focus indicators present)

**Understandable**:
- ✅ 3.1.1 Language of Page (`<html lang="en">`)
- ✅ 3.2.1 On Focus (No unexpected changes on focus)
- ✅ 3.2.2 On Input (No unexpected changes on input)
- ✅ 3.3.1 Error Identification (Errors clearly described)
- ✅ 3.3.2 Labels or Instructions (Form fields labeled)

**Robust**:
- ✅ 4.1.2 Name, Role, Value (Semantic HTML, ARIA)
- ✅ 4.1.3 Status Messages (Live regions for dynamic content)

### Reference
Full WCAG 2.1 Guidelines: https://www.w3.org/WAI/WCAG21/quickref/
```

---

## Requirements

**Do**:
- Read all generated code files
- Fix semantic HTML violations systematically
- Add ARIA only when semantic HTML insufficient
- Implement keyboard navigation for all interactive elements
- Manage focus for modals and complex widgets
- Run conceptual automated audit
- Provide detailed manual testing checklist
- **Emphasize that manual testing is MANDATORY**
- Document all changes made
- Explain why each change improves accessibility

**Don't**:
- Skip manual testing checklist (most critical output)
- Add redundant ARIA (use semantic HTML first)
- Assume automated tools catch all issues (only 60-70%)
- Make accessibility fixes that break functionality
- Use overly complex ARIA patterns when simple HTML works
- Claim "accessibility complete" without manual testing

**Research-backed insights**:
- 80%+ of AI-generated code has accessibility violations
- Two-stage approach (structure → accessibility) prevents deprioritization
- Automated tools catch only 60-70% of violations
- Manual testing with assistive technologies is MANDATORY
- TetraLogical research: Even accessibility-trained models produce WCAG-failing code
- "Accessibility is by definition non-typical usage, therefore applying an average does not work"
- ChatGPT produced zero ARIA implementation in controlled tests
- Bard generated ARIA roles on wrong elements with broken references
