---
name: preloading-resources
description: Teaches resource preloading APIs in React 19 including prefetchDNS, preconnect, preload, and preinit. Use when optimizing initial load or navigation performance.
allowed-tools: Read, Write, Edit
version: 1.0.0
---

# Resource Preloading APIs

React 19 adds functions for optimizing resource loading.

## Available Functions

```javascript
import { prefetchDNS, preconnect, preload, preinit } from 'react-dom';
```

### prefetchDNS

Perform DNS resolution early:

```javascript
function App() {
  prefetchDNS('https://api.example.com');
  prefetchDNS('https://cdn.example.com');

  return <div>App content</div>;
}
```

### preconnect

Establish connection before needed:

```javascript
function App() {
  preconnect('https://api.example.com');

  return <div>App content</div>;
}
```

### preload

Preload resources without executing:

```javascript
function App() {
  preload('/font.woff2', { as: 'font', type: 'font/woff2', crossOrigin: 'anonymous' });
  preload('/hero-image.jpg', { as: 'image' });
  preload('/critical.css', { as: 'style' });

  return <div>App content</div>;
}
```

### preinit

Preload and execute resource:

```javascript
function App() {
  preinit('/critical.js', { as: 'script' });
  preinit('/critical.css', { as: 'style', precedence: 'high' });

  return <div>App content</div>;
}
```

## Use Cases

**On Route Hover:**
```javascript
function NavLink({ to, children }) {
  const handleMouseEnter = () => {
    preload(`/api/data${to}`, { as: 'fetch' });
    preinit(`/routes${to}.js`, { as: 'script' });
  };

  return (
    <Link to={to} onMouseEnter={handleMouseEnter}>
      {children}
    </Link>
  );
}
```

For comprehensive preloading documentation, see: `research/react-19-comprehensive.md` lines 811-834.
