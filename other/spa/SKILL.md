---
name: spa
description: Single Page Application architecture with client-side routing
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: web-development
---
## What I do
- Build SPAs with client-side routing
- Manage application state
- Handle browser history API
- Implement lazy loading
- Optimize initial load

## When to use me
When building interactive web apps with smooth navigation.

## React Router
```javascript
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/about">About</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </BrowserRouter>
  );
}
```
