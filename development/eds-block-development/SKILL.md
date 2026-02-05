---
name: eds-block-development
description: Guide for developing EDS blocks using vanilla JavaScript, Content Driven Development, and block decoration patterns. Covers block structure, decorate function, content extraction, DOM manipulation, and EDS best practices for Adobe Edge Delivery Services.
---

# EDS Block Development Guide

## Purpose

Guide developers through creating and modifying Adobe Edge Delivery Services (EDS) blocks following vanilla JavaScript patterns, Content Driven Development principles, and EDS best practices.

## When to Use This Skill

Automatically activates when:
- Creating new blocks in `/blocks/`
- Modifying existing block JavaScript (`.js` files)
- Implementing block decoration patterns
- Working with EDS content structures
- Using keywords: "block", "decorate", "EDS block"

---

## Quick Start: Block Structure

### File Organization

Every EDS block follows this structure:

```
blocks/your-block/
├── your-block.js       # Decoration logic (REQUIRED)
├── your-block.css      # Block-specific styles (REQUIRED)
├── README.md           # Usage documentation (REQUIRED)
├── EXAMPLE.md          # Google Docs example (REQUIRED)
└── test.html           # Development test file (RECOMMENDED)
```

**Critical naming convention:** File names must match the block name exactly (kebab-case).

---

## The Decorate Function Pattern

All EDS blocks export a default `decorate` function that receives the block element:

```javascript
export default function decorate(block) {
  // 1. Configuration (at the top)
  const config = {
    animationDuration: 300,
    maxItems: 10,
    errorMessage: 'Failed to load content'
  };

  // 2. Extract content from EDS structure
  const rows = Array.from(block.children);
  const content = rows.map(row => {
    const cells = Array.from(row.children);
    return cells.map(cell => cell.textContent.trim());
  });

  // 3. Create new DOM structure
  const container = document.createElement('div');
  container.className = 'your-block-wrapper';

  // 4. Build your component
  content.forEach(([title, description]) => {
    const item = document.createElement('div');
    item.className = 'your-block-item';
    item.innerHTML = `
      <h3>${title}</h3>
      <p>${description}</p>
    `;
    container.appendChild(item);
  });

  // 5. Setup event handlers
  container.querySelectorAll('.your-block-item').forEach(item => {
    item.addEventListener('click', () => {
      console.log('Item clicked');
    });
  });

  // 6. Replace block content
  block.textContent = '';
  block.appendChild(container);
}
```

---

## Content Extraction Patterns

### Basic Two-Column Pattern

```javascript
export default function decorate(block) {
  const rows = Array.from(block.children);

  const items = rows.map(row => {
    const [titleCell, descriptionCell] = row.children;
    return {
      title: titleCell?.textContent?.trim() || '',
      description: descriptionCell?.textContent?.trim() || ''
    };
  });

  // Use the items...
}
```

### Picture Extraction Pattern

```javascript
function extractPicture(cell) {
  const picture = cell.querySelector('picture');
  if (!picture) return null;

  return {
    img: picture.querySelector('img'),
    sources: Array.from(picture.querySelectorAll('source'))
  };
}

export default function decorate(block) {
  const rows = Array.from(block.children);

  rows.forEach(row => {
    const [imageCell, contentCell] = row.children;
    const picture = extractPicture(imageCell);

    if (picture) {
      // Use the picture element
    }
  });
}
```

### Link Extraction Pattern

```javascript
function extractLink(cell) {
  const link = cell.querySelector('a');
  return link ? {
    href: link.href,
    text: link.textContent.trim(),
    target: link.target
  } : null;
}
```

---

## DOM Manipulation Best Practices

### 1. Clear the Block First

```javascript
export default function decorate(block) {
  // Extract data first
  const data = extractContent(block);

  // Clear the block
  block.textContent = '';

  // Add new content
  const container = createNewStructure(data);
  block.appendChild(container);
}
```

### 2. Use Document Fragments for Multiple Elements

```javascript
function createItems(data) {
  const fragment = document.createDocumentFragment();

  data.forEach(item => {
    const element = document.createElement('div');
    element.textContent = item;
    fragment.appendChild(element);
  });

  return fragment;
}

export default function decorate(block) {
  const data = extractContent(block);
  block.textContent = '';
  block.appendChild(createItems(data));
}
```

### 3. Minimize DOM Manipulation

```javascript
// ❌ BAD - Multiple reflows
data.forEach(item => {
  const element = document.createElement('div');
  element.textContent = item;
  block.appendChild(element); // Triggers reflow each time
});

// ✅ GOOD - Single reflow
const fragment = document.createDocumentFragment();
data.forEach(item => {
  const element = document.createElement('div');
  element.textContent = item;
  fragment.appendChild(element);
});
block.appendChild(fragment); // Single reflow
```

---

## Error Handling

### Basic Error Handling

```javascript
export default function decorate(block) {
  try {
    const config = { /* ... */ };
    const content = extractContent(block);

    if (!content || content.length === 0) {
      throw new Error('No content found');
    }

    const container = createStructure(content);
    block.textContent = '';
    block.appendChild(container);

  } catch (error) {
    console.error('Block decoration failed:', error);
    block.innerHTML = '<p class="error-message">Unable to load content</p>';
  }
}
```

### Async Operations

```javascript
export default async function decorate(block) {
  try {
    // Show loading state
    block.innerHTML = '<p class="loading">Loading...</p>';

    // Fetch data
    const response = await fetch('/api/data');
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const data = await response.json();

    // Clear and render
    block.textContent = '';
    block.appendChild(createStructure(data));

  } catch (error) {
    console.error('Failed to load data:', error);
    block.innerHTML = '<p class="error-message">Failed to load content</p>';
  }
}
```

---

## CSS Best Practices

### Block-Specific Naming

```css
/* Namespace all classes with block name */
.your-block-wrapper {
  /* Container styles */
}

.your-block-item {
  /* Item styles */
}

.your-block-title {
  /* Title styles */
}

/* Use BEM naming for variants */
.your-block-item--featured {
  /* Featured variant */
}

.your-block-item__icon {
  /* Item element */
}
```

### Mobile-First Responsive Design

```css
/* Base styles (mobile) */
.your-block-item {
  padding: 1rem;
  margin-bottom: 1rem;
}

/* Tablet */
@media (min-width: 600px) {
  .your-block-item {
    padding: 1.5rem;
  }
}

/* Desktop */
@media (min-width: 900px) {
  .your-block-item {
    padding: 2rem;
  }
}
```

### Use CSS Variables

```css
.your-block {
  background-color: var(--background-color);
  color: var(--text-color);
  font-family: var(--body-font-family);
  padding: var(--spacing-m);
}
```

---

## Accessibility

### Semantic HTML

```javascript
export default function decorate(block) {
  const container = document.createElement('nav'); // Use semantic elements
  container.setAttribute('aria-label', 'Block navigation');

  const list = document.createElement('ul');

  items.forEach(item => {
    const li = document.createElement('li');
    const button = document.createElement('button');
    button.textContent = item.text;
    button.setAttribute('aria-label', `Open ${item.text}`);

    li.appendChild(button);
    list.appendChild(li);
  });

  container.appendChild(list);
  block.textContent = '';
  block.appendChild(container);
}
```

### Keyboard Navigation

```javascript
export default function decorate(block) {
  const items = block.querySelectorAll('.your-block-item');

  items.forEach((item, index) => {
    // Make items focusable
    item.setAttribute('tabindex', '0');

    // Handle keyboard events
    item.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        item.click();
      }

      if (e.key === 'ArrowDown' && items[index + 1]) {
        items[index + 1].focus();
      }

      if (e.key === 'ArrowUp' && items[index - 1]) {
        items[index - 1].focus();
      }
    });
  });
}
```

---

## Performance Optimization

### 1. Lazy Loading Images

```javascript
export default function decorate(block) {
  const images = block.querySelectorAll('img');

  images.forEach(img => {
    img.setAttribute('loading', 'lazy');
  });
}
```

### 2. Debouncing Event Handlers

```javascript
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, args), wait);
  };
}

export default function decorate(block) {
  const handleResize = debounce(() => {
    // Resize logic
  }, 250);

  window.addEventListener('resize', handleResize);
}
```

### 3. Use requestIdleCallback for Non-Critical Work

```javascript
export default function decorate(block) {
  // Critical rendering
  const container = createStructure(data);
  block.appendChild(container);

  // Non-critical work
  if ('requestIdleCallback' in window) {
    requestIdleCallback(() => {
      // Analytics, non-critical enhancements, etc.
      trackBlockView(block);
    });
  } else {
    setTimeout(() => {
      trackBlockView(block);
    }, 1);
  }
}
```

---

## Testing Your Block

### Create test.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Block Test</title>

    <!-- EDS Core Styles -->
    <link rel="stylesheet" href="/styles/styles.css">

    <script type="module">
        import { loadBlock } from '/scripts/aem.js';

        // Load and decorate the block
        const block = document.querySelector('.your-block');
        await loadBlock(block);
    </script>
</head>
<body>
    <div class="your-block block">
        <div>
            <div>Title 1</div>
            <div>Description 1</div>
        </div>
        <div>
            <div>Title 2</div>
            <div>Description 2</div>
        </div>
    </div>
</body>
</html>
```

### Test with Development Server

```bash
npm run debug
```

Access your test at: `http://localhost:3000/blocks/your-block/test.html`

---

## Common Patterns

### Configuration Object

```javascript
export default function decorate(block) {
  // Configuration at the top
  const config = {
    autoplay: block.dataset.autoplay === 'true',
    delay: parseInt(block.dataset.delay) || 3000,
    animation: block.dataset.animation || 'fade'
  };

  // Use config throughout
}
```

### Data Attributes for Options

```javascript
export default function decorate(block) {
  // Read options from data attributes
  const layout = block.dataset.layout || 'grid';
  const columns = parseInt(block.dataset.columns) || 3;

  // Apply classes based on options
  block.classList.add(`layout-${layout}`);
  block.style.setProperty('--columns', columns);
}
```

### Helper Functions

```javascript
// Helper functions outside decorate
function createCard(data) {
  const card = document.createElement('div');
  card.className = 'card';
  card.innerHTML = `
    <h3>${data.title}</h3>
    <p>${data.description}</p>
  `;
  return card;
}

export default function decorate(block) {
  const data = extractContent(block);

  const container = document.createElement('div');
  data.forEach(item => {
    container.appendChild(createCard(item));
  });

  block.textContent = '';
  block.appendChild(container);
}
```

---

## Common Mistakes to Avoid

### ❌ Don't Forget to Clear the Block

```javascript
// ❌ BAD - Original content remains
export default function decorate(block) {
  const container = document.createElement('div');
  block.appendChild(container); // Adds to existing content
}

// ✅ GOOD - Clear first
export default function decorate(block) {
  const data = extractContent(block);
  block.textContent = ''; // Clear first
  block.appendChild(container);
}
```

### ❌ Don't Use innerHTML for User Content

```javascript
// ❌ BAD - XSS vulnerability
export default function decorate(block) {
  const userInput = block.textContent;
  block.innerHTML = `<div>${userInput}</div>`; // Dangerous!
}

// ✅ GOOD - Use textContent or createElement
export default function decorate(block) {
  const userInput = block.textContent;
  const div = document.createElement('div');
  div.textContent = userInput; // Safe
  block.textContent = '';
  block.appendChild(div);
}
```

### ❌ Don't Forget Error Handling

```javascript
// ❌ BAD - No error handling
export default async function decorate(block) {
  const response = await fetch('/api/data');
  const data = await response.json();
  renderData(block, data);
}

// ✅ GOOD - Proper error handling
export default async function decorate(block) {
  try {
    const response = await fetch('/api/data');
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    renderData(block, data);
  } catch (error) {
    console.error('Failed to load:', error);
    block.innerHTML = '<p>Failed to load content</p>';
  }
}
```

---

## Related Documentation

- **[Block Architecture Standards](../../../docs/for-ai/implementation/block-architecture-standards.md)** - Comprehensive architecture guide
- **[Frontend Guidelines](../../../docs/for-ai/guidelines/frontend-guidelines.md)** - JavaScript and CSS standards
- **[EDS Native Testing](../../../docs/for-ai/testing/eds-native-testing-standards.md)** - Testing patterns
- **[Content Driven Development](../content-driven-development/SKILL.md)** - CDD workflow

---

## Next Steps

1. Read the Content Driven Development skill for workflow guidance
2. Create your block structure with proper file organization
3. Implement the decorate function following these patterns
4. Create a test.html file to test locally
5. Run tests and verify functionality
6. Document your block in README.md and EXAMPLE.md

**Remember:** EDS blocks are simple, performant, and follow vanilla JavaScript patterns. Avoid frameworks, keep dependencies minimal, and focus on clean, maintainable code.
