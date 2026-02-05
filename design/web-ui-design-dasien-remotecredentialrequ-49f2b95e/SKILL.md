---
name: "Web UI Design"
description: "Design responsive web interfaces using modern UX principles, accessibility standards, and mobile-first approaches"
category: "ui-design"
required_tools: ["Read", "Write", "WebSearch", "WebFetch"]
---

# Web UI Design

## Purpose
Design modern, responsive web interfaces using HTML/CSS/JavaScript frameworks, following current UX best practices and accessibility standards.

## When to Use
- Creating web application interfaces
- Designing responsive layouts
- Planning component hierarchies
- Organizing page navigation

## Key Capabilities
1. **Responsive Design** - Create layouts that work on all screen sizes
2. **Component Thinking** - Break UI into reusable components
3. **Accessibility** - Ensure WCAG compliance and screen reader support

## Approach
1. Design mobile-first, then scale up
2. Use grid/flexbox for responsive layouts
3. Break UI into reusable components
4. Follow accessibility guidelines (ARIA, semantic HTML)
5. Ensure color contrast and keyboard navigation
6. Provide loading states and error feedback

## Example
**Context**: User profile page
````html
<!-- Mobile-first responsive design -->
<div class="profile-container">
  <header class="profile-header">
    <img src="avatar.jpg" alt="User avatar" class="avatar">
    <h1>John Doe</h1>
  </header>
  
  <section class="profile-info">
    <div class="info-grid">
      <div class="info-item">
        <label>Email</label>
        <span>john@example.com</span>
      </div>
      <div class="info-item">
        <label>Role</label>
        <span>Developer</span>
      </div>
    </div>
  </section>
  
  <footer class="profile-actions">
    <button class="btn-primary">Edit Profile</button>
    <button class="btn-secondary">Change Password</button>
  </footer>
</div>

<style>
.profile-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 1rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

@media (max-width: 768px) {
  .info-grid { grid-template-columns: 1fr; }
}
</style>
````

## Best Practices
- ✅ Mobile-first responsive design
- ✅ Semantic HTML elements (header, nav, main, footer)
- ✅ Accessible forms with labels and ARIA attributes
- ✅ Loading states and error messages
- ❌ Avoid: Fixed pixel widths
- ❌ Avoid: Relying only on color for information