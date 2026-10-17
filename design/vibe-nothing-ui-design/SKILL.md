---
name: vibe-nothing-ui-design
description: Zero-dependency Nothing-inspired UI design system with monochrome styling, dot-matrix typography, and signal-red accents for web interfaces
triggers:
  - add nothing ui components
  - style with nothing design system
  - create monochrome interface
  - use dot matrix typography
  - implement nothing inspired ui
  - add vibe nothing components
  - style with signal red accent
  - create zero dependency ui
---

# Vibe-Nothing-UI-Design Skill

> Skill by [ara.so](https://ara.so) — Design Skills collection.

## Overview

Vibe-Nothing-UI-Design is a zero-dependency UI component library inspired by Nothing's visual language. It provides ready-to-use HTML/CSS components with:

- **Monochrome surfaces** (black, grey, white hierarchy)
- **Round-dot typography** (Doto font) and iconography
- **Single signal-red accent** (#D71921) for critical states only
- **Dark/light themes** via single attribute
- **No build step** — pure HTML, CSS custom properties, vanilla JS

Perfect for creating distinctive, minimal interfaces without framework dependencies.

## Installation

### Direct Integration

1. **Copy files** into your project:
```
your-project/
├── css/
│   └── nothing-ui.css
├── js/
│   └── nothing-ui.js
└── fonts/
    └── open/
        ├── doto/
        ├── geist/
        ├── geist-mono/
        └── newsreader/
```

2. **Link in HTML**:
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="css/nothing-ui.css">
</head>
<body data-theme="dark">
  <!-- Your components here -->
  
  <script src="js/nothing-ui.js"></script>
</body>
</html>
```

### Theme Control

Set theme on any ancestor element:

```html
<!-- Dark theme (default) -->
<body data-theme="dark">

<!-- Light theme -->
<body data-theme="light">

<!-- Per-section theming -->
<main data-theme="light">
  <aside data-theme="dark">...</aside>
</main>
```

Toggle programmatically:

```javascript
// Toggle theme
document.body.dataset.theme = 
  document.body.dataset.theme === 'dark' ? 'light' : 'dark';
```

## Core Components

### Buttons

```html
<!-- Primary button (white on black) -->
<button class="btn btn-primary">Run Agent</button>

<!-- Secondary button (outlined) -->
<button class="btn btn-secondary">Cancel</button>

<!-- Danger button (signal red - use sparingly) -->
<button class="btn btn-danger">Delete</button>

<!-- Disabled state -->
<button class="btn btn-primary" disabled>Processing...</button>

<!-- Small variant -->
<button class="btn btn-primary btn-sm">Compact</button>
```

### Form Inputs

```html
<!-- Text input -->
<div class="form-group">
  <label for="name" class="form-label">Project Name</label>
  <input type="text" id="name" class="form-input" placeholder="my-project">
</div>

<!-- Text area -->
<div class="form-group">
  <label for="desc" class="form-label">Description</label>
  <textarea id="desc" class="form-input" rows="4"></textarea>
</div>

<!-- Select dropdown -->
<div class="form-group">
  <label for="model" class="form-label">Model</label>
  <select id="model" class="form-select">
    <option>GPT-4</option>
    <option>Claude 3</option>
    <option>Gemini Pro</option>
  </select>
</div>

<!-- Checkbox -->
<label class="checkbox">
  <input type="checkbox">
  <span>Enable monitoring</span>
</label>

<!-- Radio buttons -->
<div class="radio-group">
  <label class="radio">
    <input type="radio" name="env" value="dev">
    <span>Development</span>
  </label>
  <label class="radio">
    <input type="radio" name="env" value="prod">
    <span>Production</span>
  </label>
</div>
```

### Cards

```html
<!-- Basic card -->
<div class="card">
  <div class="card-header">
    <h3>Deployment Status</h3>
  </div>
  <div class="card-body">
    <p>Your application is running on 3 instances.</p>
  </div>
  <div class="card-footer">
    <button class="btn btn-secondary btn-sm">View Logs</button>
  </div>
</div>

<!-- Card with signal -->
<div class="card">
  <div class="card-header">
    <h3>Build Pipeline</h3>
    <span class="badge badge-danger">Blocked</span>
  </div>
  <div class="card-body">
    <p>Requires manual approval to proceed.</p>
  </div>
</div>
```

### Badges & Status Pills

```html
<!-- Status badges -->
<span class="badge badge-success">Active</span>
<span class="badge badge-warning">Pending</span>
<span class="badge badge-danger">Failed</span>
<span class="badge badge-neutral">Idle</span>

<!-- In context -->
<div class="table-cell">
  <span class="badge badge-warning">Deploying</span>
</div>
```

### Tables

```html
<table class="table">
  <thead>
    <tr>
      <th>Agent</th>
      <th>Status</th>
      <th>Last Run</th>
      <th>Actions</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>content-generator</td>
      <td><span class="badge badge-success">Active</span></td>
      <td><code>2m ago</code></td>
      <td>
        <button class="btn btn-sm btn-secondary">Logs</button>
      </td>
    </tr>
    <tr>
      <td>image-processor</td>
      <td><span class="badge badge-danger">Blocked</span></td>
      <td><code>14m ago</code></td>
      <td>
        <button class="btn btn-sm btn-danger">Review</button>
      </td>
    </tr>
  </tbody>
</table>
```

### Alerts

```html
<!-- Info alert (neutral) -->
<div class="alert alert-info">
  <strong>Note:</strong> Deployment will begin in 5 minutes.
</div>

<!-- Success alert -->
<div class="alert alert-success">
  <strong>Deployed:</strong> Version 2.1.0 is now live.
</div>

<!-- Warning alert (signal red) -->
<div class="alert alert-warning">
  <strong>Action Required:</strong> API key expires in 3 days.
</div>

<!-- Error alert (signal red) -->
<div class="alert alert-error">
  <strong>Build Failed:</strong> Check logs for details.
</div>
```

### Navigation

```html
<!-- Sidebar navigation -->
<nav class="nav-sidebar">
  <a href="#" class="nav-item active">Dashboard</a>
  <a href="#" class="nav-item">Agents</a>
  <a href="#" class="nav-item">Deployments</a>
  <a href="#" class="nav-item">Settings</a>
</nav>

<!-- Breadcrumb -->
<nav class="breadcrumb">
  <a href="#">Projects</a>
  <span class="breadcrumb-separator">/</span>
  <a href="#">my-agent</a>
  <span class="breadcrumb-separator">/</span>
  <span>Runs</span>
</nav>

<!-- Tabs -->
<div class="tabs">
  <button class="tab active">Overview</button>
  <button class="tab">Logs</button>
  <button class="tab">Metrics</button>
</div>
```

### Modal Dialog

```html
<div class="modal" id="confirm-dialog">
  <div class="modal-overlay"></div>
  <div class="modal-content">
    <div class="modal-header">
      <h2>Confirm Deletion</h2>
      <button class="modal-close" aria-label="Close">&times;</button>
    </div>
    <div class="modal-body">
      <p>This action cannot be undone. Delete agent "content-gen"?</p>
    </div>
    <div class="modal-footer">
      <button class="btn btn-secondary">Cancel</button>
      <button class="btn btn-danger">Delete</button>
    </div>
  </div>
</div>

<script>
// Show modal
document.getElementById('confirm-dialog').classList.add('active');

// Hide modal
document.getElementById('confirm-dialog').classList.remove('active');
</script>
```

### Code Blocks

```html
<!-- Inline code -->
<p>Run <code>npm start</code> to begin.</p>

<!-- Code block -->
<pre class="code-block"><code>{
  "model": "gpt-4",
  "temperature": 0.7,
  "max_tokens": 2000
}</code></pre>
```

## Typography System

### Heading Hierarchy

```html
<h1 class="heading-1">Main Title</h1>
<h2 class="heading-2">Section Title</h2>
<h3 class="heading-3">Subsection</h3>
<h4 class="heading-4">Component Title</h4>
```

### Font Families

```html
<!-- Display (Doto - round dots) -->
<h1 style="font-family: var(--font-display)">Dashboard</h1>

<!-- UI text (Geist) -->
<p style="font-family: var(--font-ui)">Interface copy</p>

<!-- Monospace (Geist Mono) -->
<code style="font-family: var(--font-mono)">API_KEY=xyz</code>

<!-- Editorial (Newsreader Italic) - sparingly -->
<p style="font-family: var(--font-editorial); font-style: italic;">
  A more personal, conversational tone.
</p>
```

## CSS Custom Properties

### Colors

```css
/* Access theme colors */
.custom-element {
  background: var(--color-bg);
  color: var(--color-text);
  border: 1px solid var(--color-border);
}

/* Signal red (use only for critical states) */
.critical {
  color: var(--color-accent);
}

/* Available variables:
   --color-bg          Background
   --color-bg-elevated Surface
   --color-text        Primary text
   --color-text-muted  Secondary text
   --color-border      Dividers
   --color-accent      Signal red (#D71921)
*/
```

### Spacing

```css
.custom-spacing {
  padding: var(--spacing-4);      /* 16px */
  margin-bottom: var(--spacing-6); /* 24px */
  gap: var(--spacing-2);          /* 8px */
}

/* Scale: 
   --spacing-1: 4px
   --spacing-2: 8px
   --spacing-3: 12px
   --spacing-4: 16px
   --spacing-5: 20px
   --spacing-6: 24px
   --spacing-8: 32px
*/
```

### Border Radius

```css
.custom-card {
  border-radius: var(--radius-md); /* 8px */
}

/* Scale:
   --radius-sm: 4px
   --radius-md: 8px
   --radius-lg: 12px
   --radius-full: 9999px (pills)
*/
```

## Common Patterns

### Dashboard Layout

```html
<body data-theme="dark">
  <div class="app-layout">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <h1 class="heading-3">My App</h1>
      </div>
      <nav class="nav-sidebar">
        <a href="#" class="nav-item active">Dashboard</a>
        <a href="#" class="nav-item">Agents</a>
        <a href="#" class="nav-item">Settings</a>
      </nav>
    </aside>
    
    <!-- Main content -->
    <main class="main-content">
      <header class="page-header">
        <nav class="breadcrumb">
          <a href="#">Home</a>
          <span class="breadcrumb-separator">/</span>
          <span>Dashboard</span>
        </nav>
        <div class="search-bar">
          <input type="search" class="form-input" placeholder="Search...">
        </div>
      </header>
      
      <div class="content-area">
        <!-- Your content -->
      </div>
    </main>
  </div>
</body>
```

### Data Table with Status

```html
<div class="card">
  <div class="card-header">
    <h3>Active Deployments</h3>
    <button class="btn btn-primary btn-sm">New Deploy</button>
  </div>
  <div class="card-body">
    <table class="table">
      <thead>
        <tr>
          <th>Service</th>
          <th>Status</th>
          <th>Version</th>
          <th>Updated</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>api-gateway</td>
          <td><span class="badge badge-success">Running</span></td>
          <td><code>v2.1.0</code></td>
          <td>2 hours ago</td>
        </tr>
        <tr>
          <td>worker-queue</td>
          <td><span class="badge badge-warning">Deploying</span></td>
          <td><code>v1.8.3</code></td>
          <td>5 minutes ago</td>
        </tr>
        <tr>
          <td>analytics</td>
          <td><span class="badge badge-danger">Failed</span></td>
          <td><code>v3.0.0</code></td>
          <td>12 minutes ago</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
```

### Form with Validation States

```html
<form class="form">
  <!-- Valid input -->
  <div class="form-group">
    <label for="api-key" class="form-label">API Key</label>
    <input 
      type="text" 
      id="api-key" 
      class="form-input" 
      value="sk-..."
      readonly
    >
    <span class="form-help">Key is valid</span>
  </div>
  
  <!-- Error state -->
  <div class="form-group">
    <label for="endpoint" class="form-label">Endpoint URL</label>
    <input 
      type="url" 
      id="endpoint" 
      class="form-input is-invalid" 
      value="invalid-url"
    >
    <span class="form-error">Must be a valid URL</span>
  </div>
  
  <!-- Submit -->
  <div class="form-actions">
    <button type="submit" class="btn btn-primary">Save Settings</button>
    <button type="button" class="btn btn-secondary">Cancel</button>
  </div>
</form>
```

### Loading States

```html
<!-- Button loading -->
<button class="btn btn-primary" disabled>
  <span class="spinner"></span>
  Deploying...
</button>

<!-- Skeleton loader -->
<div class="card">
  <div class="skeleton skeleton-text"></div>
  <div class="skeleton skeleton-text" style="width: 70%;"></div>
  <div class="skeleton skeleton-rect" style="height: 200px;"></div>
</div>
```

## Design Principles

### Signal Red Usage

**DO use signal red for:**
- Critical errors (`badge-danger`, `alert-error`)
- Destructive actions (`btn-danger`)
- Live/blocked/needs-input states
- Items requiring immediate attention

**DON'T use signal red for:**
- Primary CTAs (use black/white inversion)
- Decorative elements
- Multiple items on screen (reserve for true signals)

```html
<!-- ✅ Correct: Signal for critical action -->
<button class="btn btn-danger">Delete All Data</button>
<span class="badge badge-danger">Requires Approval</span>

<!-- ❌ Incorrect: Primary action should invert -->
<button class="btn btn-danger">Save Changes</button>
```

### Depth & Hierarchy

Use borders, whitespace, and elevation — never shadows:

```css
/* Elevated surface */
.elevated-card {
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  padding: var(--spacing-6);
}

/* Frosted glass effect (built-in) */
.glass-panel {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}
```

## Troubleshooting

### Fonts Not Loading

Ensure the `fonts/open/` directory is correctly positioned relative to CSS:

```
project/
├── css/
│   └── nothing-ui.css    ← references ../fonts/open/
└── fonts/
    └── open/
        ├── doto/
        ├── geist/
        └── ...
```

If fonts are in a different location, update CSS:

```css
@font-face {
  font-family: 'Doto';
  src: url('/path/to/fonts/open/doto/Doto-Regular.woff2') format('woff2');
}
```

### Theme Not Switching

Ensure `data-theme` is on an ancestor of all components:

```html
<!-- ✅ Correct -->
<body data-theme="dark">
  <div class="card">...</div>
</body>

<!-- ❌ Won't work if card is outside -->
<div data-theme="dark"></div>
<div class="card">...</div>
```

### Accent Color Overused

If everything looks red, you're overusing the signal color. Review:

```html
<!-- ✅ Correct: One signal per view -->
<div class="dashboard">
  <div class="card">
    <span class="badge badge-success">Active</span>
  </div>
  <div class="card">
    <span class="badge badge-danger">Needs Review</span> ← Only signal
  </div>
</div>

<!-- ❌ Too many signals -->
<div class="dashboard">
  <button class="btn btn-danger">Save</button>
  <div class="alert alert-error">...</div>
  <span class="badge badge-danger">Failed</span>
</div>
```

### Custom Components Not Matching Style

Extend using CSS custom properties:

```css
.my-custom-widget {
  font-family: var(--font-ui);
  background: var(--color-bg-elevated);
  color: var(--color-text);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--spacing-4);
}
```

## Integration Examples

### With Static Site Generator

```html
<!-- In your template/layout file -->
<!DOCTYPE html>
<html lang="en">
<head>
  <link rel="stylesheet" href="/assets/css/nothing-ui.css">
</head>
<body data-theme="dark">
  {% block content %}{% endblock %}
  <script src="/assets/js/nothing-ui.js"></script>
</body>
</html>
```

### With Vanilla JS App

```javascript
// app.js
class App {
  constructor() {
    this.theme = localStorage.getItem('theme') || 'dark';
    this.applyTheme();
  }
  
  applyTheme() {
    document.body.dataset.theme = this.theme;
  }
  
  toggleTheme() {
    this.theme = this.theme === 'dark' ? 'light' : 'dark';
    localStorage.setItem('theme', this.theme);
    this.applyTheme();
  }
}

const app = new App();
```

### Dynamic Content

```javascript
// Generate table rows dynamically
function renderAgents(agents) {
  const tbody = document.querySelector('#agents-table tbody');
  tbody.innerHTML = agents.map(agent => `
    <tr>
      <td>${agent.name}</td>
      <td><span class="badge badge-${agent.statusClass}">${agent.status}</span></td>
      <td><code>${agent.lastRun}</code></td>
      <td>
        <button class="btn btn-sm btn-secondary" 
                onclick="viewLogs('${agent.id}')">
          Logs
        </button>
      </td>
    </tr>
  `).join('');
}
```

## Additional Resources

- **Live Demo**: https://wangbh030722.github.io/vibe-nothing-ui-design/
- **Component Reference**: https://wangbh030722.github.io/vibe-nothing-ui-design/index.html
- **SPEC.md**: Generation contract and token reference
- **DESIGN.md**: Design rationale and principles
