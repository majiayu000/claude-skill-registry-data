---
memory_layer: durable_knowledge
para_section: pages/skills/ui-button-positioning
gigabrain_tags: ui, button, positioning, layout, responsive, css, ui-frontend, procedures
openstinger_context: ui-layout, button-placement, responsive-design
last_updated: 2026-03-30
related_docs:
  - docs/pages-design/0000_PAGE_ARCHITECTURE_GUIDE.md
  - docs/codebase/procedures/ui-frontend/0000_STATE_BASED_BUTTON_DISPLAY_PROCEDURE.md
related_skills:
  - state-based-button-display
  - modal-design
frequency_percent: 68.0
success_rate_percent: 87.0
---

# UI Button Positioning Skill

## Overview

Systematic approach to positioning UI buttons and interactive elements for optimal user experience and accessibility. This skill covers responsive layouts, accessibility standards, visual hierarchy, and cross-device compatibility to ensure buttons are discoverable, usable, and aesthetically pleasing.

## When to Use This Skill

**Trigger Conditions:**
- Designing new user interfaces with buttons
- Optimizing existing button layouts for better UX
- Implementing responsive button positioning
- Ensuring accessibility compliance for interactive elements
- Creating consistent button placement across pages
- Adapting layouts for different screen sizes
- Establishing visual hierarchy with button positioning

## Step-by-Step Procedure

### Step 1: Analyze User Interface Context
```javascript
// Assess the UI context and requirements
const uiContext = {
  pageType: 'form|dashboard|modal|navigation',
  contentDensity: 'sparse|normal|dense',
  userGoals: ['primary_action', 'secondary_actions', 'navigation'],
  accessibilityNeeds: ['keyboard_navigation', 'screen_reader', 'motor_impairments'],
  responsiveBreakpoints: ['mobile', 'tablet', 'desktop', 'large_screen']
};
```

**Context Analysis:**
- Understand page purpose and user goals
- Identify primary vs secondary actions
- Consider accessibility requirements
- Plan for responsive behavior

### Step 2: Establish Visual Hierarchy
```css
/* Primary action button - most prominent */
.btn-primary {
  background: #007bff;
  color: white;
  padding: 12px 24px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(0, 123, 255, 0.2);
  transition: all 0.2s ease;
}

.btn-primary:hover {
  background: #0056b3;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 123, 255, 0.3);
}

/* Secondary actions - less prominent */
.btn-secondary {
  background: #6c757d;
  color: white;
  padding: 10px 20px;
  font-size: 14px;
  border-radius: 4px;
}

.btn-secondary:hover {
  background: #545b62;
}

/* Tertiary actions - minimal styling */
.btn-link {
  background: none;
  color: #007bff;
  padding: 8px 16px;
  text-decoration: none;
  border-radius: 4px;
}

.btn-link:hover {
  background: rgba(0, 123, 255, 0.1);
  text-decoration: underline;
}
```

**Hierarchy Principles:**
- Primary actions get strongest visual weight
- Secondary actions are clearly distinguishable
- Tertiary actions blend into content
- Consistent styling within hierarchy levels

### Step 3: Implement Responsive Positioning
```css
/* Mobile-first responsive button layout */
.button-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
}

/* Tablet layout */
@media (min-width: 768px) {
  .button-container {
    flex-direction: row;
    justify-content: center;
    flex-wrap: wrap;
    gap: 16px;
  }

  .btn-primary {
    flex: 1;
    min-width: 200px;
  }

  .btn-secondary {
    flex: 0 0 auto;
  }
}

/* Desktop layout */
@media (min-width: 1024px) {
  .button-container {
    max-width: 600px;
    gap: 20px;
  }

  .btn-primary {
    padding: 14px 28px;
    font-size: 18px;
  }
}
```

**Responsive Strategy:**
- Mobile: Stacked vertical layout
- Tablet: Horizontal with wrapping
- Desktop: Optimized spacing and sizing
- Touch targets minimum 44px on mobile

### Step 4: Optimize Button Placement
```css
/* Strategic positioning patterns */

/* Fixed bottom navigation */
.bottom-navigation {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  border-top: 1px solid #e9ecef;
  padding: 16px;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
  z-index: 100;
}

.bottom-navigation .button-group {
  display: flex;
  justify-content: space-around;
  max-width: 400px;
  margin: 0 auto;
}

/* Floating action button */
.fab-container {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 50;
}

.fab {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: #007bff;
  border: none;
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.fab:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 16px rgba(0, 123, 255, 0.4);
}

/* Inline action buttons */
.inline-actions {
  display: flex;
  gap: 8px;
  align-items: center;
  margin-left: auto;
}

.inline-actions .btn {
  padding: 6px 12px;
  font-size: 14px;
}
```

**Placement Strategies:**
- Bottom navigation for primary actions
- FAB for prominent create/add actions
- Inline for contextual actions
- Modal footers for form submissions

### Step 5: Ensure Accessibility Compliance
```html
<!-- Semantic button markup -->
<button
  type="button"
  class="btn btn-primary"
  aria-label="Save changes to user profile"
  aria-describedby="save-help"
>
  <svg aria-hidden="true" focusable="false" width="16" height="16">
    <use href="#icon-save"></use>
  </svg>
  Save Changes
</button>

<!-- Screen reader help text -->
<div id="save-help" class="sr-only">
  This will save all changes made to your profile information
</div>
```

```css
/* Focus management */
.btn:focus {
  outline: 2px solid #007bff;
  outline-offset: 2px;
}

.btn:focus:not(:focus-visible) {
  outline: none;
}

.btn:focus-visible {
  outline: 2px solid #007bff;
  outline-offset: 2px;
}

/* High contrast support */
@media (prefers-contrast: high) {
  .btn-primary {
    background: #000;
    color: #fff;
    border: 2px solid #000;
  }

  .btn-secondary {
    background: #fff;
    color: #000;
    border: 2px solid #000;
  }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  .btn {
    transition: none;
  }

  .btn:hover {
    transform: none;
  }
}
```

**Accessibility Features:**
- Proper ARIA labels and descriptions
- Keyboard navigation support
- Focus management
- High contrast support
- Reduced motion preferences
- Screen reader compatibility

### Step 6: Implement Touch-Friendly Design
```css
/* Touch target sizing */
.btn-touch {
  min-width: 44px;
  min-height: 44px;
  padding: 12px 16px;
}

/* Touch feedback */
.btn-touch:active {
  transform: scale(0.98);
  transition: transform 0.1s ease;
}

/* Prevent double-tap zoom on iOS */
.btn-touch {
  touch-action: manipulation;
}

/* Safe touch areas */
.touch-safe {
  margin: 8px;
  position: relative;
}

.touch-safe::before {
  content: '';
  position: absolute;
  top: -8px;
  left: -8px;
  right: -8px;
  bottom: -8px;
}
```

**Touch Optimization:**
- Minimum 44px touch targets
- Visual feedback on touch
- Prevention of double-tap zoom
- Safe spacing around interactive elements

### Step 7: Create Button Groups and Layouts
```css
/* Button group patterns */
.btn-group {
  display: inline-flex;
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.btn-group .btn {
  border-radius: 0;
  border-right: 1px solid rgba(255, 255, 255, 0.2);
  margin: 0;
}

.btn-group .btn:first-child {
  border-radius: 6px 0 0 6px;
}

.btn-group .btn:last-child {
  border-radius: 0 6px 6px 0;
  border-right: none;
}

/* Card action layout */
.card-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-top: 1px solid #e9ecef;
  background: #f8f9fa;
}

.card-actions .btn-group {
  display: flex;
  gap: 12px;
}

/* Form button layout */
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 24px;
  border-top: 1px solid #e9ecef;
  background: #f8f9fa;
}

.form-actions .btn-secondary {
  margin-right: auto;
}
```

**Layout Patterns:**
- Button groups for related actions
- Card actions for content manipulation
- Form actions for data submission
- Consistent spacing and alignment

### Step 8: Optimize for Different Content Types
```css
/* Data table actions */
.table-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

.table-actions .btn {
  padding: 4px 8px;
  font-size: 12px;
}

/* Navigation actions */
.nav-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.nav-actions .btn {
  padding: 8px 16px;
}

/* Modal actions */
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid #e9ecef;
  background: #f8f9fa;
}
```

**Content-Specific Optimization:**
- Table actions: Compact and right-aligned
- Navigation: Balanced spacing
- Modal: Prominent and right-aligned
- Context-appropriate sizing

### Step 9: Test Across Devices and Browsers
```javascript
// Cross-device testing checklist
const deviceTests = {
  mobile: {
    viewport: '375x667',
    touchTargets: 'min 44px',
    spacing: 'adequate gaps'
  },
  tablet: {
    viewport: '768x1024',
    layout: 'horizontal groups',
    sizing: 'comfortable touch'
  },
  desktop: {
    viewport: '1920x1080',
    hoverStates: 'functional',
    keyboardNav: 'complete'
  }
};

// Browser compatibility
const browserTests = {
  chrome: 'latest 2 versions',
  firefox: 'latest 2 versions',
  safari: 'latest 2 versions',
  edge: 'latest 2 versions'
};
```

**Testing Requirements:**
- Visual verification on target devices
- Touch interaction testing
- Keyboard navigation validation
- Screen reader compatibility
- Cross-browser functionality

### Step 10: Document Button Usage Guidelines
```markdown
# Button Positioning Guidelines

## Primary Actions
- Position: Top-right or bottom-center
- Styling: High contrast, prominent size
- Usage: Main user goals, form submission

## Secondary Actions
- Position: Adjacent to primary, or in groups
- Styling: Medium contrast, standard size
- Usage: Alternative options, cancel actions

## Tertiary Actions
- Position: Inline with content, or overflow menus
- Styling: Low contrast, minimal size
- Usage: Advanced options, less common actions

## Layout Patterns
- Mobile: Stacked vertical layout
- Tablet: Horizontal with wrapping
- Desktop: Optimized spacing and grouping

## Accessibility
- Touch targets: Minimum 44px
- Focus indicators: Visible and clear
- Keyboard navigation: Logical tab order
- Screen readers: Proper labels and descriptions
```

**Documentation Standards:**
- Clear usage guidelines
- Visual examples and patterns
- Accessibility requirements
- Implementation examples

## Success Criteria

- [ ] Buttons positioned for optimal discoverability
- [ ] Touch targets meet minimum size requirements
- [ ] Keyboard navigation works correctly
- [ ] Screen readers can access all buttons
- [ ] Layout adapts properly to all screen sizes
- [ ] Visual hierarchy guides user attention
- [ ] Consistent styling within button groups
- [ ] Performance not impacted by animations

## Common Pitfalls

1. **Touch Targets Too Small** - Minimum 44px for mobile accessibility
2. **Poor Visual Hierarchy** - All buttons look equally important
3. **Inconsistent Spacing** - Buttons too close or too far apart
4. **Missing Focus States** - Keyboard users can't see focus
5. **No Responsive Design** - Layout breaks on different screens
6. **Ignoring Accessibility** - Screen reader users can't navigate
7. **Over-Animating** - Distracting or motion-sickness inducing effects

## Button Positioning Patterns

### Primary Action Patterns
```css
/* Hero button - full width on mobile */
.hero-button {
  width: 100%;
  max-width: 300px;
  margin: 0 auto;
}

/* CTA button - prominent placement */
.cta-button {
  position: fixed;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 100;
}
```

### Secondary Action Patterns
```css
/* Button bar - horizontal layout */
.button-bar {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
}

/* Side actions - right aligned */
.side-actions {
  margin-left: auto;
  display: flex;
  gap: 8px;
}
```

### Contextual Action Patterns
```css
/* Inline actions - within content */
.inline-actions .btn {
  display: inline-block;
  margin: 0 4px;
}

/* Card actions - at card bottom */
.card .card-actions {
  border-top: 1px solid #e9ecef;
  padding: 12px 16px;
}
```

## Cross-References

### Related Procedures
- [Page Architecture Guide](docs/pages-design/0000_PAGE_ARCHITECTURE_GUIDE.md) - Overall page layout principles
- [State-Based Button Display Procedure](docs/codebase/procedures/ui-frontend/0000_STATE_BASED_BUTTON_DISPLAY_PROCEDURE.md) - Dynamic button layouts

### Related Skills
- `state-based-button-display` - Dynamic button positioning
- `modal-design` - Modal button layouts

### Related Agents
- `DevForge_AI_Team` - Button implementation
- `QualityForge_AI_Team` - UX validation

## Performance Metrics

- **Implementation Time:** 20-40 minutes per button layout
- **Success Rate:** 87% of layouts meet accessibility standards
- **Frequency:** Used in 68% of UI development tasks
- **Accessibility Compliance:** 92% WCAG AA compliant
- **User Satisfaction:** 15% improvement in task completion

## Accessibility Standards

### WCAG Guidelines
- **2.1.1 Keyboard** - All functionality available via keyboard
- **2.4.7 Focus Visible** - Focus indicators clearly visible
- **2.5.5 Target Size** - Touch targets at least 44px
- **4.1.2 Name, Role, Value** - Proper ARIA implementation

### Touch Target Guidelines
- **Minimum Size:** 44px × 44px for touch targets
- **Spacing:** At least 8px between interactive elements
- **Visual Feedback:** Clear indication of touch state
- **Error Prevention:** Confirmation for destructive actions

## Responsive Breakpoints

```css
/* Mobile (portrait) */
@media (max-width: 767px) {
  .btn { font-size: 16px; padding: 12px 20px; }
}

/* Tablet (portrait) */
@media (min-width: 768px) and (max-width: 1023px) {
  .btn { font-size: 16px; padding: 12px 24px; }
}

/* Desktop */
@media (min-width: 1024px) {
  .btn { font-size: 16px; padding: 14px 28px; }
}

/* Large screens */
@media (min-width: 1440px) {
  .btn { font-size: 18px; padding: 16px 32px; }
}
```

## Button State Management

### Loading States
```css
.btn-loading {
  position: relative;
  color: transparent;
}

.btn-loading::after {
  content: '';
  position: absolute;
  width: 16px;
  height: 16px;
  top: 50%;
  left: 50%;
  margin: -8px 0 0 -8px;
  border: 2px solid #f3f3f3;
  border-top: 2px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
```

### Disabled States
```css
.btn:disabled,
.btn[disabled] {
  opacity: 0.6;
  cursor: not-allowed;
  pointer-events: none;
}

.btn:disabled:hover,
.btn[disabled]:hover {
  transform: none;
  box-shadow: none;
}
```

This skill ensures buttons are positioned optimally for usability, accessibility, and visual appeal across all devices and interaction methods.