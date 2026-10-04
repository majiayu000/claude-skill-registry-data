---
name: html
description: HTML markup language for structuring web pages
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: web-development
---
## What I do
- Create semantic HTML documents
- Use proper document structure
- Build accessible forms
- Implement responsive images
- Use semantic elements (header, nav, main, article, section, footer)
- Add metadata and SEO tags
- Handle multimedia elements

## When to use me
When creating or structuring web pages.

## Document Structure
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page Title</title>
  <meta name="description" content="Description">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header>
    <nav>
      <a href="/">Home</a>
      <a href="/about">About</a>
    </nav>
  </header>
  
  <main>
    <article>
      <h1>Title</h1>
      <p>Content</p>
    </article>
    
    <aside>
      <h2>Related</h2>
    </aside>
  </main>
  
  <footer>&copy; 2024</footer>
</body>
</html>
```

## Semantic Elements
```html
<header>Site header</header>
<nav>Navigation</nav>
<main>Main content</main>
<article>Self-contained content</article>
<section>Thematic grouping</section>
<aside>Sidebar content</aside>
<footer>Footer content</footer>

<figure>
  <img src="image.jpg" alt="Description">
  <figcaption>Caption</figcaption>
</figure>
```

## Forms
```html
<form action="/submit" method="POST">
  <label for="email">Email:</label>
  <input type="email" id="email" name="email" required>
  
  <label for="password">Password:</label>
  <input type="password" id="password" name="password" minlength="8">
  
  <select name="country">
    <option value="">Select</option>
    <option value="us">USA</option>
  </select>
  
  <button type="submit">Submit</button>
</form>
```

## Accessibility
```html
<!-- ARIA -->
<button aria-label="Close menu" aria-expanded="false">
  <span class="visually-hidden">Close</span>
</button>

<!-- Focus management -->
<a href="#main" class="visually-hidden">Skip to content</a>

<!-- Alt text -->
<img src="chart.png" alt="Sales chart showing 50% growth">
```
