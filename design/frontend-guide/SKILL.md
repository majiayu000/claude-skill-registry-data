---
name: frontend-guide
description: Comprehensive frontend development guide covering HTML, CSS, JavaScript, TypeScript, React, Vue, Angular, and modern web technologies. Use when working on frontend development, web applications, or UI/UX implementation.
sasmp_version: "1.3.0"
bonded_agent: 01-frontend-specialist
bond_type: PRIMARY_BOND
eqhm_enabled: true
---

# Frontend Development Guide

Master modern frontend development with comprehensive learning resources and best practices.

## Quick Start

Start your frontend journey based on your experience level:

### Beginners
1. Learn HTML fundamentals - semantic markup, forms, accessibility
2. Master CSS - layout (Flexbox, Grid), responsive design, animations
3. JavaScript basics - variables, functions, DOM manipulation, async/await
4. Git and version control
5. Deploy first project to GitHub Pages

```html
<!-- Semantic HTML5 Example -->
<header>
  <nav>Navigation</nav>
</header>
<main>
  <article>
    <h1>Article Title</h1>
    <p>Content here</p>
  </article>
</main>
<footer>Footer content</footer>
```

### Intermediate
1. Modern JavaScript (ES6+) - classes, modules, promises
2. Learn a framework (React, Vue, or Angular)
3. State management (Context API, Redux, Vuex)
4. API integration with REST and GraphQL
5. Testing (Jest, Vitest, Cypress)
6. Build tools (Webpack, Vite)

```javascript
// React Hooks Example
import { useState, useEffect } from 'react';

function TodoList() {
  const [todos, setTodos] = useState([]);

  useEffect(() => {
    // Fetch todos on component mount
    fetchTodos();
  }, []);

  return (
    <ul>
      {todos.map(todo => <li key={todo.id}>{todo.title}</li>)}
    </ul>
  );
}
```

### Advanced
1. Next.js/Vue Nuxt for SSR and static generation
2. TypeScript for type-safe code
3. Advanced state management patterns
4. Performance optimization (code splitting, lazy loading)
5. Web performance APIs
6. Progressive Web Apps (PWA)
7. Design systems and component libraries

## Technology Stack Overview

### Core Technologies
- **HTML5**: Semantic markup, forms, APIs
- **CSS3**: Flexbox, Grid, animations, transitions
- **JavaScript/TypeScript**: ES6+, async patterns

### Popular Frameworks
- **React**: Component-based, JSX, hooks, ecosystem
- **Vue**: Progressive framework, simple API, great docs
- **Angular**: Enterprise framework, full-featured, opinionated

### State Management
- **React**: Context API, Redux, Zustand, Jotai
- **Vue**: Vuex, Pinia (recommended)
- **Angular**: RxJS, NgRx

### Build Tools & Package Managers
- **npm**: Default package manager
- **Yarn/pnpm**: Alternative package managers
- **Webpack**: Module bundler
- **Vite**: Modern, fast build tool
- **Turbopack**: High-performance bundler

### Testing Tools
- **Jest**: JavaScript testing framework
- **Vitest**: Vite-native unit testing
- **Cypress**: E2E testing
- **Playwright**: Cross-browser testing
- **Testing Library**: Component testing

## Learning Resources

### Official Documentation
- [MDN Web Docs](https://developer.mozilla.org/) - Authoritative reference
- [React Documentation](https://react.dev/) - React official docs
- [Vue Documentation](https://vuejs.org/) - Vue official docs
- [Web.dev by Google](https://web.dev/) - Modern web platform features

### Interactive Learning
- **Codecademy**: Interactive courses
- **FreeCodeCamp**: Free comprehensive tutorials
- **Frontend Masters**: Advanced frontend courses
- **Egghead**: Focused micro-courses

### Practice Projects
1. **Todo App** - CRUD operations, state management
2. **Weather App** - API integration, real-world data
3. **E-commerce Product Page** - Complex UI, interactions
4. **Blog Platform** - Full app with routing and data
5. **Dashboard** - Data visualization, real-time updates

## Performance Optimization

### Key Metrics
- Lighthouse Score (SEO, Performance, Accessibility)
- Core Web Vitals (LCP, FID, CLS)
- Time to Interactive (TTI)

### Optimization Techniques
- Code splitting and lazy loading
- Image optimization (WebP, responsive images)
- Minification and tree-shaking
- Service workers and caching strategies
- CSS-in-JS optimization
- Component memoization

## Accessibility (A11y)

### WCAG Guidelines
- Semantic HTML
- ARIA labels and roles
- Keyboard navigation
- Color contrast ratios
- Screen reader compatibility

## Deployment

### Static Hosting
- Vercel - Best for Next.js and frameworks
- Netlify - Simple deployment
- GitHub Pages - Free static hosting

### Full-Stack Hosting
- AWS Amplify
- Firebase Hosting
- DigitalOcean

## Next Steps

1. Choose a framework that resonates with you
2. Build 3-5 substantial projects
3. Contribute to open-source frontend projects
4. Learn testing and best practices
5. Explore advanced topics (performance, architecture)

**Roadmap.sh Reference**: https://roadmap.sh/frontend

---

**Status**: ✅ Production Ready | **SASMP**: v1.3.0 | **Bonded Agent**: 01-frontend-specialist
