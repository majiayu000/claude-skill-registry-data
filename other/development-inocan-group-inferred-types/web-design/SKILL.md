---
name: web-design
description: Principles and code snippets for designing responsive, accessible websites. Use this skill when building or refining web interfaces.
license: MIT
metadata:
  category: design
---
# Web Design Handbook

## Overview

This skill provides guidelines and examples for creating modern, user-friendly websites.

### Core Principles

- **User-centric design**: Start with user needs; design navigation and layout accordingly.
- **Responsive design**: Ensure your site looks good on devices of all sizes.
- **Accessibility**: Follow WCAG guidelines; use semantic HTML; provide alternative text for images.
- **Performance**: Optimize images, minify CSS and JS, and use caching.

## HTML & CSS Basics

### HTML5 Skeleton

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Example Page</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header>
    <nav>
      <ul class="nav">
        <li><a href="/">Home</a></li>
        <li><a href="/about.html">About</a></li>
        <li><a href="/contact.html">Contact</a></li>
      </ul>
    </nav>
  </header>
  <main>
    <h1>Welcome</h1>
    <p>This is a sample page.</p>
  </main>
  <footer>
    <p>&copy; 2025 Your Company</p>
  </footer>
</body>
</html>
```

### Responsive CSS with Flexbox

```css
* {
  box-sizing: border-box;
}
.nav {
  display: flex;
  list-style-type: none;
  gap: 1rem;
}
.nav a {
  text-decoration: none;
  color: #333;
}
@media (max-width: 600px) {
  .nav {
    flex-direction: column;
  }
}
```

## CSS Frameworks

- **Bootstrap**: Provides a responsive grid system and ready-made UI components.
- **Tailwind CSS**: Utility-first framework for rapid customization.

Example using Tailwind:

```html
<script src="https://cdn.tailwindcss.com"></script>
<button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
  Click Me
</button>
```

## UI/UX Best Practices

- Keep navigation simple and consistent.
- Use whitespace to separate content.
- Maintain a clear visual hierarchy.
- Choose accessible color combinations (check contrast ratios).
- Use standard fonts for readability.

## Performance Optimization

- Use `srcset` for responsive images.
- Compress images (JPEG/PNG/WebP).
- Minify and bundle CSS/JS.
- Enable browser caching and HTTP/2.

## Additional Resources

- MDN Web Docs.
- W3C Web Accessibility Initiative (WAI).
- Google's Lighthouse performance tool.
