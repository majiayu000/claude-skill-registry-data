---
name: rails-frontend-guidelines
description: Rails frontend development guidelines using Hotwire (Turbo + Stimulus), Tailwind CSS, and ViewComponent. Modern patterns for server-rendered HTML with progressive enhancement, zero-build frontend architecture, and Rails conventions. Use when creating views, components, Stimulus controllers, partials, or working with frontend code.
---

# Rails Frontend Development Guidelines

## Purpose

Comprehensive guide for modern Rails frontend development using Hotwire (Turbo + Stimulus), Tailwind CSS, and server-side rendering. Emphasizes progressive enhancement, minimal JavaScript, and Rails conventions.

## When to Use This Skill

- Creating new views or partials
- Building Stimulus controllers
- Working with Turbo Frames or Turbo Streams
- Styling with Tailwind CSS
- Creating ViewComponents
- Adding frontend interactivity
- Organizing frontend code
- Performance optimization

---

## Quick Start

### New View Checklist

Creating a view? Follow this checklist:

- [ ] Use semantic HTML5 elements
- [ ] Turbo Frame for interactive sections
- [ ] Turbo Stream for real-time updates
- [ ] Tailwind utility classes for styling
- [ ] Minimal Stimulus controllers for interactivity
- [ ] Partials for reusable components
- [ ] Accessible markup (ARIA labels, semantic elements)
- [ ] Mobile-first responsive design
- [ ] Progressive enhancement (works without JS)

### New Stimulus Controller Checklist

Creating a Stimulus controller? Follow this:

- [ ] Name matches HTML (data-controller matches filename)
- [ ] Use targets for DOM elements
- [ ] Use values for configuration
- [ ] Use actions for events
- [ ] Keep controllers small and focused (single responsibility)
- [ ] Clean up in disconnect() if needed
- [ ] Use classes for CSS manipulation

---

## Topic Guides

### ⚡ Turbo (Hotwire)

**Turbo Drive:**
- Automatic page navigation without full reload
- Enabled by default in Rails 7+
- Use data-turbo="false" to disable on specific links/forms

**Turbo Frames:**
- Scoped page updates
- Lazy loading support
- Break out with data-turbo-frame="_top"

**Turbo Streams:**
- Real-time updates over WebSocket or HTTP
- 7 actions: append, prepend, replace, update, remove, before, after
- Format: respond_to with format.turbo_stream

**[📖 Complete Guide: resources/turbo-guide.md](resources/turbo-guide.md)**

---

### 🎮 Stimulus Controllers

**Stimulus = "Modest JavaScript Framework"**

- Sprinkles JavaScript on server-rendered HTML
- Three core concepts: Controllers, Actions, Targets
- Lifecycle: connect() → disconnect()
- Values for configuration (automatically typed)
- Classes for CSS manipulation

**[📖 Complete Guide: resources/stimulus-guide.md](resources/stimulus-guide.md)**

---

### 📚 Complete Examples

**Full working examples:**

- Modern view with Turbo Frames
- Complete Stimulus controller
- Form with real-time validation
- Turbo Stream updates
- Responsive layouts with Tailwind

**[📖 Complete Guide: resources/complete-examples.md](resources/complete-examples.md)**

---

## Navigation Guide

| Need to... | Read this resource |
|------------|-------------------|
| Use Turbo Frames/Streams   | [turbo-guide.md](resources/turbo-guide.md) |
| Create Stimulus controller | [stimulus-guide.md](resources/stimulus-guide.md) |
| See full examples          | [complete-examples.md](resources/complete-examples.md) |

---

## Core Principles

1. **Server-Side First**: Render HTML on server, enhance with JavaScript
2. **Progressive Enhancement**: Works without JavaScript, better with it
3. **Turbo for Navigation**: Use Turbo Drive/Frames instead of full page reloads
4. **Stimulus for Interactivity**: Minimal JavaScript, attached to HTML
5. **Tailwind for Styling**: Utility-first CSS in templates
6. **Semantic HTML**: Use proper HTML5 elements
7. **Partials for Reuse**: Extract common patterns to partials

---

## File Structure Quick Reference

```
app/
  views/
    layouts/application.html.erb
    shared/_nav.html.erb
    posts/
      index.html.erb
      show.html.erb
      _post.html.erb
      _form.html.erb
  javascript/
    controllers/
      application.js
      hello_controller.js
      form_controller.js
```

---

## Related Skills

- **rails-backend-guidelines**: Backend patterns for controllers and models
- **skill-developer**: For creating new skills

---

**Skill Status**: Adapted for Rails 7+, Hotwire (Turbo + Stimulus), and Tailwind CSS
