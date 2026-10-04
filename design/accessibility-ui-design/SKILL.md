---
name: accessibility-ui-design
description: When designing and implementing web interfaces to ensure they are usable by everyone.
version: 2.0.0
category: ui-ux
tags: [ui-ux, a11y, inclusive-design, wcag]
skill_type: architecture
author: skiLLM
license: MIT
compatible_agents: [claude-code, cursor, copilot, codex]
estimated_context_tokens: 1900
dangerous: false
requires_review: true
security_level: safe
dependencies: [dom-security-hardening]
triggers: [a11y, accessibility, wcag, screen reader, keyboard navigation]
permissions:
  filesystem: { read: true, write: true }
  network: { outbound: false }
  shell: { execute: false }
input_requirements: [HTML markup, interactive components]
output_contract: [semantic html, keyboard navigable, screen reader compatible, wcag aa compliant]
failure_conditions: [missing alt attributes, focus trap broken, color-only distinction, non-semantic components]
last_updated: 2026-05-15
---

# Accessibility (a11y) UI Design

## Purpose
Accessible interfaces are NOT optional extras—they're legal requirements (ADA, WCAG). This skill ensures web interfaces work for everyone: keyboard users, screen reader users, color-blind users, and users with cognitive disabilities. Accessible design is better design for all users.

## When to use
- Writing HTML markup for UI components
- Designing complex interactive widgets (modals, dropdowns, tabs, date pickers)
- Auditing existing user interfaces for WCAG compliance
- Building custom form controls
- Creating data tables or other structured content

## When NOT to use
- Visual design (separate concern)
- Component styling (use CSS appropriately)
- Performance optimization (different concern)

## Inputs required
- HTML or JSX markup
- List of interactive behaviors
- Understanding of WCAG 2.1 AA standards
- Accessibility testing tools (axe, Lighthouse, NVDA)

## Workflow
1. **Use Semantic HTML First**: Use native elements (`<button>`, `<nav>`, `<dialog>`, `<form>`) instead of building from `<div>`
2. **Keyboard Navigation**: Ensure ALL interactive elements are reachable via Tab key and operable via Enter or Space
3. **Manage Focus**: Trap focus inside modals; return focus to trigger after close
4. **Add ARIA Only When Needed**: Apply `aria-*` attributes ONLY when native HTML is insufficient
5. **Test Color Contrast**: Verify foreground/background colors meet WCAG AA 4.5:1 ratio for text
6. **Provide Text Alternatives**: Add `alt` attributes to images; provide captions for videos
7. **Label Form Controls**: Explicitly associate `<label>` elements with form inputs
8. **Test with Assistive Tech**: Test with screen reader (NVDA, JAWS) and keyboard only

## Rules
- MUST use semantic HTML elements (button, nav, form, fieldset, legend, etc.)
- MUST make all interactive elements keyboard accessible (no mouse-only interactions)
- MUST NOT remove focus outlines without providing custom focus states
- MUST provide alt text for all images (including empty `alt=""` for decorative images)
- MUST label all form inputs with `<label>` elements
- MUST use ARIA only to supplement, never replace, semantic HTML
- MUST achieve at minimum WCAG AA color contrast (4.5:1 for body text)
- MUST NOT rely solely on color to communicate information
- MUST support screen readers (test with real screen readers, not just tools)

## Anti-patterns
- **Div Buttons**: Using `<div onClick={...}>` instead of `<button>`
- **Relying on Color Alone**: Communicating error states purely through red text (add icon or text indicator)
- **Missing Labels**: Form inputs without associated `<label>` elements
- **Removed Focus**: `outline: none;` without providing custom focus states
- **Placeholder as Label**: Using `placeholder` attribute instead of `<label>` element
- **Inaccessible Modals**: Modals without focus trap or escape key support
- **Overuse of ARIA**: Using `role="button"` on divs instead of `<button>`

## Failure conditions
- Images missing alt attributes
- Color contrast fails WCAG AA (< 4.5:1 for text)
- Interactive elements not keyboard accessible
- Focus trap not working in modals
- Screen reader cannot identify form inputs
- No way to skip repetitive content (navigation)

## Validation checklist
- [ ] All interactive elements use semantic HTML (button, link, form)
- [ ] All elements reachable and operable via keyboard (Tab, Enter, Space, Escape)
- [ ] Focus visible and visible focus state (no `outline: none`)
- [ ] All images have alt text (or `alt=""` if decorative)
- [ ] All form inputs have associated `<label>` elements
- [ ] Color contrast meets WCAG AA 4.5:1 (or 3:1 for large text)
- [ ] Focus trap works in modals (cannot tab outside)
- [ ] Escape key closes modals and returns focus
- [ ] Modals announced to screen readers
- [ ] No keyboard traps (can always escape)
- [ ] Tested with keyboard only (no mouse)
- [ ] Tested with screen reader (NVDA, JAWS, VoiceOver)
- [ ] Automated tools pass (axe, Lighthouse)

## Output format
- **HTML structure**: Semantic elements with proper nesting
- **Focus management**: Visible focus states, focus traps in modals
- **ARIA attributes**: Applied only when semantic HTML insufficient
- **Color usage**: Contrast-compliant, not sole communication method
- **Form structure**: Labels explicitly associated, error messages linked
- **Validation**: Automated tool results + manual screen reader testing

## Security considerations
- Alt text MUST NOT leak sensitive information unnecessarily
- ARIA attributes MUST NOT expose hidden security features
- Focus management MUST prevent keyboard traps
- ARIA live regions MUST NOT expose private user data

## Agent execution notes
- Agent MAY: Add semantic HTML, add ARIA when needed, add alt text, fix color contrast, add focus management
- Agent MUST NEVER: Remove focus indicators, use `role="button"` on divs, use `placeholder` for labels, trap keyboard
- Agent MUST ASK: Before adding complex ARIA, before removing focus indicators, before major interactive behavior changes
- Agent MUST VALIDATE: Keyboard navigation works, color contrast passes, screen reader can understand content

## Example

**❌ Anti-pattern (Non-semantic, no labels, color-only error, no focus):**
```jsx
// BAD: DIV button, no accessibility
<div onClick={() => submit()} style={{ outline: 'none', cursor: 'pointer' }}>
  Submit
</div>

// BAD: Input without label
<input type="email" placeholder="Email address" />

// BAD: Error shown only in red
<div style={{ color: 'red' }}>Password too short</div>

// BAD: Modal with focus trap
<div role="dialog">
  <input />
  {/* User can Tab outside modal */}
</div>
```

**✅ Correct pattern (Semantic, labeled, accessible errors, focus managed):**
```jsx
// GOOD: Semantic button
<button onClick={() => submit()} type="button">
  Submit
</button>

// GOOD: Label explicitly associated
<label htmlFor="email-input">Email address</label>
<input id="email-input" type="email" required />

// GOOD: Error shown with icon and text (not just color)
<div className="error" role="alert" aria-live="polite">
  <Icon name="error" />
  Password too short (minimum 8 characters)
</div>

// GOOD: Modal with focus trap and keyboard handling
const Modal = ({ isOpen, onClose, children }) => {
  const modalRef = useRef(null);
  
  useEffect(() => {
    if (!isOpen) return;
    
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') onClose();
    };
    
    // Focus first interactive element in modal
    const firstFocusable = modalRef.current?.querySelector('button, [href], input');
    firstFocusable?.focus();
    
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen]);
  
  return (
    <dialog
      ref={modalRef}
      open={isOpen}
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
    >
      <h1 id="modal-title">Modal Title</h1>
      {children}
      <button onClick={onClose}>Close</button>
    </dialog>
  );
};
```
