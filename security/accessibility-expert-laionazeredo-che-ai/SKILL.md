---
name: "accessibility-expert"
description: "Master guide for web accessibility following WCAG 2.2 guidelines. Covers audit processes, ARIA patterns, semantic HTML, and inclusive design."
---

# Accessibility Expert Guide

This skill ensures that all web interfaces are inclusive and accessible to users with diverse needs.

## ♿ WCAG 2.2 Standards
- **Perceivable**: Provide text alternatives for non-text content. Create content that can be presented in different ways without losing information.
- **Operable**: Make all functionality available from a keyboard. Give users enough time to read and use content.
- **Understandable**: Make text content readable and understandable. Help users avoid and correct mistakes.
- **Robust**: Maximize compatibility with current and future user agents, including assistive technologies.

## 🛠 ARIA & Semantic HTML
- **Semantic HTML**: Use native elements (`<button>`, `<nav>`, `<main>`) before resorting to ARIA roles.
- **ARIA Roles**: Use `role`, `aria-label`, `aria-labelledby`, and `aria-describedby` to provide additional context.
- **Live Regions**: Use `aria-live` for dynamic content updates that need to be announced by screen readers.

## 🎨 Inclusive Design
- **Contrast**: Maintain a minimum contrast ratio of 4.5:1 for normal text and 3:1 for large text (WCAG AA).
- **Focus Indicators**: Never hide the default focus ring unless providing a clear, custom alternative.
- **Forms**: Always provide clear, visible labels for form inputs. Use `aria-invalid` and `aria-errormessage` for validation.

## 🔗 References
- [WCAG 2.2 Guidelines](https://www.w3.org/WAI/standards-guidelines/wcag/)
- [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
