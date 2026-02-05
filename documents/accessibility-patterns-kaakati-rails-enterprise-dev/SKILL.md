---
name: "Accessibility Patterns"
description: "WCAG 2.2 Level AA compliance patterns for Rails applications including ARIA implementation, keyboard navigation, focus management, screen reader support, and color contrast requirements. Use this skill when implementing any user-facing UI to ensure accessibility compliance. Trigger keywords: accessibility, a11y, WCAG, ARIA, screen reader, keyboard navigation, focus, color contrast, disability, assistive technology"
---

# Accessibility Patterns

Comprehensive WCAG 2.2 Level AA compliance patterns for Rails applications with ViewComponents, Hotwire, and TailAdmin.

## When to Use This Skill

Use this skill when:
- Implementing any user-facing UI component
- Building interactive widgets (modals, dropdowns, tabs)
- Creating forms with validation feedback
- Adding dynamic content updates (Turbo Streams)
- Reviewing existing components for accessibility compliance
- Responding to accessibility audit findings

---

## 1. WCAG 2.2 Level AA Quick Reference

### 1.1 Perceivable

| Criterion | Requirement | Implementation |
|-----------|-------------|----------------|
| 1.1.1 Non-text Content | Alt text for images | `alt="descriptive text"` or `alt=""` for decorative |
| 1.3.1 Info and Relationships | Semantic HTML | Use proper heading hierarchy, lists, tables |
| 1.4.3 Contrast (Minimum) | 4.5:1 for text, 3:1 for large text | Verify TailAdmin colors meet ratios |
| 1.4.4 Resize Text | 200% zoom support | Use relative units (rem, em) |
| 1.4.11 Non-text Contrast | 3:1 for UI components | Focus rings, borders, icons |

### 1.2 Operable

| Criterion | Requirement | Implementation |
|-----------|-------------|----------------|
| 2.1.1 Keyboard | All functionality via keyboard | Tab, Enter, Space, Arrow keys |
| 2.1.2 No Keyboard Trap | Users can navigate away | Proper focus management |
| 2.4.3 Focus Order | Logical tab sequence | DOM order matches visual order |
| 2.4.7 Focus Visible | Clear focus indicator | Tailwind focus rings |
| 2.5.8 Target Size | Minimum 24x24px | Touch targets 44x44px recommended |

### 1.3 Understandable

| Criterion | Requirement | Implementation |
|-----------|-------------|----------------|
| 3.1.1 Language of Page | Declare page language | `<html lang="en">` |
| 3.2.1 On Focus | No unexpected changes | Avoid auto-submit on focus |
| 3.3.1 Error Identification | Identify errors clearly | aria-invalid, role="alert" |
| 3.3.2 Labels or Instructions | Label all inputs | `<label>` or aria-label |

### 1.4 Robust

| Criterion | Requirement | Implementation |
|-----------|-------------|----------------|
| 4.1.2 Name, Role, Value | Expose to assistive tech | ARIA roles, states, properties |
| 4.1.3 Status Messages | Announce without focus | aria-live regions |

---

## 2. ARIA Roles, States, and Properties

### 2.1 Landmark Roles

Use semantic HTML with implicit roles:

```erb
<%# Prefer semantic HTML over ARIA roles %>
<header>      <%# role="banner" implicit %>
<nav>         <%# role="navigation" implicit %>
<main>        <%# role="main" implicit %>
<aside>       <%# role="complementary" implicit %>
<footer>      <%# role="contentinfo" implicit %>

<%# Only use explicit roles when semantic HTML not possible %>
<div role="search">
  <%= form_with url: search_path, method: :get do |f| %>
    <%= f.search_field :q, "aria-label": "Search site" %>
  <% end %>
</div>
```

### 2.2 Widget Roles

Common interactive widget patterns:

```erb
<%# Button %>
<button type="button" aria-pressed="false">Toggle Feature</button>

<%# Link styled as button %>
<a href="#" role="button">Perform Action</a>

<%# Tab Panel %>
<div role="tablist" aria-label="Account Settings">
  <button role="tab" aria-selected="true" aria-controls="panel-1" id="tab-1">
    Profile
  </button>
  <button role="tab" aria-selected="false" aria-controls="panel-2" id="tab-2">
    Security
  </button>
</div>
<div role="tabpanel" id="panel-1" aria-labelledby="tab-1">
  Profile content...
</div>
<div role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden>
  Security content...
</div>

<%# Expandable section %>
<button aria-expanded="false" aria-controls="details-section">
  Show Details
</button>
<div id="details-section" hidden>
  Expanded content...
</div>

<%# Menu %>
<button aria-haspopup="menu" aria-expanded="false">
  Options
</button>
<ul role="menu" hidden>
  <li role="menuitem"><a href="#">Edit</a></li>
  <li role="menuitem"><a href="#">Delete</a></li>
</ul>

<%# Alert Dialog %>
<div role="alertdialog" aria-modal="true" aria-labelledby="dialog-title" aria-describedby="dialog-desc">
  <h2 id="dialog-title">Confirm Delete</h2>
  <p id="dialog-desc">Are you sure you want to delete this item?</p>
  <button>Cancel</button>
  <button>Delete</button>
</div>
```

### 2.3 Live Regions

Announce dynamic content changes:

```erb
<%# Polite announcement (after current speech) %>
<div aria-live="polite" aria-atomic="true" class="sr-only">
  <%= flash[:notice] %>
</div>

<%# Assertive announcement (interrupt) %>
<div role="alert" aria-live="assertive">
  <%= flash[:alert] %>
</div>

<%# Status updates %>
<div role="status" aria-live="polite">
  Showing <%= @items.count %> of <%= @total %> items
</div>

<%# Progress %>
<div role="progressbar"
     aria-valuenow="<%= @progress %>"
     aria-valuemin="0"
     aria-valuemax="100"
     aria-label="Upload progress">
  <%= @progress %>% complete
</div>
```

### 2.4 Relationship Properties

Connect related elements:

```erb
<%# Labeling %>
<input type="text" id="email" aria-labelledby="email-label email-hint">
<label id="email-label" for="email">Email</label>
<span id="email-hint">We'll never share your email</span>

<%# Describing %>
<input type="password" aria-describedby="password-requirements">
<div id="password-requirements">
  Password must be at least 8 characters
</div>

<%# Error messages %>
<input type="email"
       aria-invalid="true"
       aria-describedby="email-error"
       aria-errormessage="email-error">
<div id="email-error" role="alert">
  Please enter a valid email address
</div>

<%# Controlling %>
<button aria-controls="dropdown-menu" aria-expanded="false">
  Menu
</button>
<ul id="dropdown-menu" hidden>...</ul>

<%# Owns (for non-DOM parent-child) %>
<div role="listbox" aria-owns="option-1 option-2 option-3">
  <%# Options may be rendered elsewhere in DOM %>
</div>
```

---

## 3. Keyboard Navigation Patterns

### 3.1 Focus Order and Tab Sequence

```erb
<%# Natural tab order follows DOM order %>
<nav>
  <a href="/">Home</a>
  <a href="/about">About</a>
  <a href="/contact">Contact</a>
</nav>

<%# Remove from tab order (but keep accessible) %>
<button tabindex="-1">Skip This</button>

<%# Add to tab order (non-focusable elements) %>
<div tabindex="0" role="button">Custom Button</div>

<%# NEVER use positive tabindex %>
<%# BAD: <input tabindex="1"> %>
```

### 3.2 Keyboard Shortcuts

Standard keyboard patterns:

| Component | Keys | Action |
|-----------|------|--------|
| Button | Enter, Space | Activate |
| Link | Enter | Navigate |
| Checkbox | Space | Toggle |
| Radio | Arrow keys | Select option |
| Tabs | Arrow keys | Switch tab |
| Menu | Arrow keys, Enter | Navigate, select |
| Modal | Escape | Close |
| Dropdown | Escape | Close |

### 3.3 Roving Tabindex Pattern

For composite widgets (tabs, menus, toolbars):

```javascript
// stimulus_controller: roving_tabindex_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["item"]

  connect() {
    this.currentIndex = 0
    this.updateTabindex()
  }

  next(event) {
    event.preventDefault()
    this.currentIndex = (this.currentIndex + 1) % this.itemTargets.length
    this.focusCurrent()
  }

  previous(event) {
    event.preventDefault()
    this.currentIndex = (this.currentIndex - 1 + this.itemTargets.length) % this.itemTargets.length
    this.focusCurrent()
  }

  updateTabindex() {
    this.itemTargets.forEach((item, index) => {
      item.setAttribute("tabindex", index === this.currentIndex ? "0" : "-1")
    })
  }

  focusCurrent() {
    this.updateTabindex()
    this.itemTargets[this.currentIndex].focus()
  }
}
```

```erb
<%# Usage %>
<div role="tablist"
     data-controller="roving-tabindex"
     data-action="keydown.right->roving-tabindex#next keydown.left->roving-tabindex#previous">
  <button role="tab" data-roving-tabindex-target="item" tabindex="0">Tab 1</button>
  <button role="tab" data-roving-tabindex-target="item" tabindex="-1">Tab 2</button>
  <button role="tab" data-roving-tabindex-target="item" tabindex="-1">Tab 3</button>
</div>
```

### 3.4 Focus Trapping for Modals

```javascript
// stimulus_controller: focus_trap_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["container"]

  connect() {
    this.focusableElements = this.containerTarget.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    )
    this.firstFocusable = this.focusableElements[0]
    this.lastFocusable = this.focusableElements[this.focusableElements.length - 1]

    // Store previous focus
    this.previousFocus = document.activeElement

    // Focus first element
    this.firstFocusable?.focus()
  }

  disconnect() {
    // Restore focus
    this.previousFocus?.focus()
  }

  trapFocus(event) {
    if (event.key !== "Tab") return

    if (event.shiftKey) {
      if (document.activeElement === this.firstFocusable) {
        event.preventDefault()
        this.lastFocusable.focus()
      }
    } else {
      if (document.activeElement === this.lastFocusable) {
        event.preventDefault()
        this.firstFocusable.focus()
      }
    }
  }
}
```

---

## 4. Focus Management

### 4.1 Visible Focus Indicators

TailAdmin-compatible focus styles:

```erb
<%# Default focus ring %>
<button class="focus:ring-2 focus:ring-primary focus:ring-offset-2 focus:outline-none">
  Click Me
</button>

<%# High contrast focus for dark backgrounds %>
<button class="focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-boxdark">
  Dark Button
</button>

<%# Custom focus visible (keyboard only) %>
<a href="#" class="focus-visible:ring-2 focus-visible:ring-primary focus-visible:outline-none">
  Link
</a>

<%# Focus within for parent highlighting %>
<div class="focus-within:ring-2 focus-within:ring-primary">
  <input type="text" class="focus:outline-none">
</div>
```

### 4.2 Skip Navigation Links

```erb
<%# At the very top of the page %>
<a href="#main-content"
   class="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4
          focus:z-50 focus:bg-primary focus:text-white focus:px-4 focus:py-2
          focus:rounded">
  Skip to main content
</a>

<header>...</header>
<nav>...</nav>

<main id="main-content" tabindex="-1">
  <%# Main content %>
</main>
```

### 4.3 Focus After Dynamic Actions

```javascript
// After deleting an item, focus the next item or container
deleteItem(event) {
  const item = event.target.closest("[data-item]")
  const nextItem = item.nextElementSibling || item.previousElementSibling

  item.remove()

  if (nextItem) {
    nextItem.focus()
  } else {
    this.containerTarget.focus()
  }
}

// After closing modal, return focus to trigger
closeModal() {
  this.element.hidden = true
  this.triggerElement?.focus()
}

// After form submission success
formSubmitSuccess() {
  // Announce success
  this.announceTarget.textContent = "Form submitted successfully"

  // Focus confirmation or next action
  this.confirmationTarget.focus()
}
```

---

## 5. Screen Reader Considerations

### 5.1 Visually Hidden Content

```erb
<%# Screen reader only text %>
<span class="sr-only">Additional context for screen readers</span>

<%# Tailwind sr-only class %>
<%# .sr-only { position: absolute; width: 1px; height: 1px; ... } %>

<%# Icon with accessible label %>
<button aria-label="Close">
  <svg class="h-5 w-5" aria-hidden="true">...</svg>
</button>

<%# Or with visually hidden text %>
<button>
  <svg class="h-5 w-5" aria-hidden="true">...</svg>
  <span class="sr-only">Close</span>
</button>
```

### 5.2 Hiding Decorative Content

```erb
<%# Decorative images %>
<img src="decoration.svg" alt="" aria-hidden="true">

<%# Decorative icons %>
<svg aria-hidden="true" focusable="false">...</svg>

<%# Duplicate content %>
<a href="/profile">
  <img src="avatar.jpg" alt="">  <%# alt="" because link text provides context %>
  <span>View Profile</span>
</a>

<%# Presentational elements %>
<div role="presentation">...</div>
<hr aria-hidden="true">
```

### 5.3 Meaningful Announcements

```erb
<%# Page title changes %>
<title><%= [@page_title, "MyApp"].compact.join(" | ") %></title>

<%# Loading states %>
<div aria-busy="true" aria-describedby="loading-message">
  <span id="loading-message" class="sr-only">Loading content...</span>
  Loading...
</div>

<%# Form validation summary %>
<div role="alert" aria-live="assertive">
  <h2>Please fix the following errors:</h2>
  <ul>
    <% @errors.each do |error| %>
      <li><a href="#<%= error.field %>"><%= error.message %></a></li>
    <% end %>
  </ul>
</div>

<%# Dynamic count updates %>
<span aria-live="polite" aria-atomic="true">
  <%= pluralize(@cart.items.count, "item") %> in cart
</span>
```

---

## 6. Color and Contrast

### 6.1 WCAG Contrast Requirements

| Content Type | Minimum Ratio | Example |
|--------------|---------------|---------|
| Normal text (<18px) | 4.5:1 | Body text |
| Large text (>18px or 14px bold) | 3:1 | Headings |
| UI components | 3:1 | Buttons, inputs, icons |
| Graphical objects | 3:1 | Charts, diagrams |

### 6.2 TailAdmin Color Contrast Analysis

**Passing Combinations (WCAG AA):**

```erb
<%# Text on light backgrounds %>
<p class="text-black bg-white">           <%# 21:1 - Excellent %>
<p class="text-bodydark bg-white">        <%# ~7:1 - Pass %>
<p class="text-primary bg-white">         <%# ~4.7:1 - Pass %>

<%# Text on dark backgrounds %>
<p class="text-white bg-boxdark">         <%# ~12:1 - Excellent %>
<p class="text-bodydark1 bg-boxdark">     <%# ~5:1 - Pass %>

<%# Error states %>
<p class="text-danger bg-white">          <%# ~4.5:1 - Pass %>

<%# Verify custom colors %>
<%# Use: https://webaim.org/resources/contrastchecker/ %>
```

### 6.3 Don't Rely on Color Alone

```erb
<%# BAD: Color only indicates status %>
<span class="text-success">Approved</span>
<span class="text-danger">Rejected</span>

<%# GOOD: Icon + text + color %>
<span class="text-success flex items-center gap-2">
  <svg aria-hidden="true"><%# checkmark icon %></svg>
  Approved
</span>
<span class="text-danger flex items-center gap-2">
  <svg aria-hidden="true"><%# X icon %></svg>
  Rejected
</span>

<%# GOOD: Badges with pattern %>
<span class="bg-success/10 text-success border border-success px-2 py-1 rounded">
  Approved
</span>
```

---

## 7. Testing Approaches

### 7.1 Automated Testing with axe-core

```ruby
# spec/support/accessibility_helpers.rb
require "axe-rspec"

RSpec.configure do |config|
  config.include AxeRspec
end

# Usage in system specs
RSpec.describe "Dashboard", type: :system do
  it "is accessible" do
    visit dashboard_path
    expect(page).to be_axe_clean
  end

  it "is accessible with specific rules" do
    visit dashboard_path
    expect(page).to be_axe_clean.according_to(:wcag2aa)
  end

  it "is accessible excluding known issues" do
    visit dashboard_path
    expect(page).to be_axe_clean.excluding("color-contrast")
  end
end
```

### 7.2 Manual Testing Checklist

**Keyboard Testing:**
- [ ] Tab through entire page - logical order?
- [ ] Can access all interactive elements?
- [ ] Focus visible at all times?
- [ ] Can escape modals with Escape key?
- [ ] Arrow keys work in menus/tabs?

**Screen Reader Testing:**
- [ ] Page title announced on load
- [ ] Headings create logical outline
- [ ] Images have appropriate alt text
- [ ] Form labels announced with inputs
- [ ] Error messages announced
- [ ] Dynamic updates announced (live regions)

**Visual Testing:**
- [ ] 200% zoom - content still usable?
- [ ] High contrast mode - content visible?
- [ ] Forced colors mode - UI intact?

### 7.3 Tools

| Tool | Purpose |
|------|---------|
| axe DevTools (browser) | Automated accessibility testing |
| WAVE | Visual accessibility evaluation |
| Lighthouse | Performance + accessibility audit |
| NVDA/VoiceOver | Screen reader testing |
| Colour Contrast Analyser | Manual contrast checking |

---

## 8. Rails/ViewComponent Patterns

### 8.1 Accessible ViewComponent Base

```ruby
# app/components/accessible_component.rb
class AccessibleComponent < ViewComponent::Base
  # Common accessibility helpers

  def unique_id(prefix = "component")
    @unique_id ||= "#{prefix}-#{SecureRandom.hex(4)}"
  end

  def describedby_id
    "#{unique_id}-description"
  end

  def labelledby_id
    "#{unique_id}-label"
  end

  def error_id
    "#{unique_id}-error"
  end

  def aria_attributes(options = {})
    attrs = {}
    attrs["aria-label"] = options[:label] if options[:label]
    attrs["aria-labelledby"] = options[:labelledby] if options[:labelledby]
    attrs["aria-describedby"] = options[:describedby] if options[:describedby]
    attrs["aria-expanded"] = options[:expanded] if options.key?(:expanded)
    attrs["aria-controls"] = options[:controls] if options[:controls]
    attrs["aria-current"] = options[:current] if options[:current]
    attrs["aria-invalid"] = options[:invalid] if options[:invalid]
    attrs
  end
end
```

### 8.2 Accessible Form Input Component

```ruby
# app/components/form_input_component.rb
class FormInputComponent < AccessibleComponent
  def initialize(form:, attribute:, label:, hint: nil, required: false)
    @form = form
    @attribute = attribute
    @label = label
    @hint = hint
    @required = required
  end

  def has_error?
    @form.object.errors[@attribute].any?
  end

  def error_message
    @form.object.errors[@attribute].first
  end

  def input_attributes
    attrs = {
      "aria-describedby": [@hint ? describedby_id : nil, has_error? ? error_id : nil].compact.join(" ").presence,
      "aria-required": @required,
      "aria-invalid": has_error?
    }
    attrs["aria-errormessage"] = error_id if has_error?
    attrs.compact
  end
end
```

```erb
<%# app/components/form_input_component.html.erb %>
<div class="mb-4">
  <%= @form.label @attribute, @label, class: "block text-sm font-medium text-black dark:text-white" %>

  <% if @hint %>
    <p id="<%= describedby_id %>" class="text-sm text-bodydark mt-1">
      <%= @hint %>
    </p>
  <% end %>

  <%= @form.text_field @attribute,
      class: "mt-1 block w-full rounded border-stroke dark:border-strokedark
             bg-transparent px-4 py-2 text-black dark:text-white
             focus:border-primary focus:ring-primary
             #{has_error? ? 'border-danger' : ''}",
      **input_attributes %>

  <% if has_error? %>
    <p id="<%= error_id %>" class="mt-1 text-sm text-danger" role="alert">
      <%= error_message %>
    </p>
  <% end %>
</div>
```

### 8.3 Accessible Modal Component

```ruby
# app/components/modal_component.rb
class ModalComponent < AccessibleComponent
  renders_one :trigger
  renders_one :body

  def initialize(title:)
    @title = title
  end
end
```

```erb
<%# app/components/modal_component.html.erb %>
<div data-controller="modal">
  <%= trigger %>

  <div data-modal-target="dialog"
       role="dialog"
       aria-modal="true"
       aria-labelledby="<%= labelledby_id %>"
       class="fixed inset-0 z-50 hidden"
       data-action="keydown.escape->modal#close">

    <%# Backdrop %>
    <div class="fixed inset-0 bg-black/50"
         data-action="click->modal#close"
         aria-hidden="true"></div>

    <%# Dialog %>
    <div class="fixed inset-0 flex items-center justify-center p-4"
         data-controller="focus-trap"
         data-focus-trap-target="container"
         data-action="keydown->focus-trap#trapFocus">

      <div class="bg-white dark:bg-boxdark rounded-lg shadow-xl max-w-md w-full p-6">
        <h2 id="<%= labelledby_id %>" class="text-xl font-semibold text-black dark:text-white">
          <%= @title %>
        </h2>

        <button data-action="click->modal#close"
                class="absolute top-4 right-4"
                aria-label="Close dialog">
          <svg aria-hidden="true">...</svg>
        </button>

        <%= body %>
      </div>
    </div>
  </div>
</div>
```

---

## 9. Quick Reference Checklist

Before shipping any UI component, verify:

**Structure:**
- [ ] Semantic HTML used (headings, lists, tables, nav, main, etc.)
- [ ] Heading hierarchy is logical (h1 > h2 > h3)
- [ ] Language declared on html element

**Keyboard:**
- [ ] All interactive elements focusable
- [ ] Focus order is logical
- [ ] Focus indicator visible
- [ ] No keyboard traps

**Screen Readers:**
- [ ] Images have alt text (or alt="" if decorative)
- [ ] Form inputs have labels
- [ ] ARIA used correctly (or not at all)
- [ ] Dynamic content announced

**Visual:**
- [ ] Color contrast meets 4.5:1 (text) or 3:1 (UI)
- [ ] Information not conveyed by color alone
- [ ] Works at 200% zoom
- [ ] Focus indicators have 3:1 contrast

**Forms:**
- [ ] Labels associated with inputs
- [ ] Required fields indicated
- [ ] Errors identified and described
- [ ] Error messages linked to inputs

**Interactive:**
- [ ] Buttons are buttons, links are links
- [ ] State communicated (expanded, selected, pressed)
- [ ] Loading states announced
