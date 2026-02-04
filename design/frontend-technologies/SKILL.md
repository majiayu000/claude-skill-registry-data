---
name: frontend-technologies
description: Master modern web development with HTML, CSS, JavaScript, React, Vue, Angular, Next.js, TypeScript, and responsive design. Use when building web applications, optimizing UI performance, or learning frontend frameworks.
sasmp_version: "1.3.0"
bonded_agent: 01-typescript-fundamentals
bond_type: PRIMARY_BOND
---

# Frontend Technologies Skill

## Quick Start - React with TypeScript

```typescript
import React, { useState, useEffect } from 'react';

interface Props {
  title: string;
}

export function Example({ title }: Props) {
  const [count, setCount] = useState(0);

  useEffect(() => {
    document.title = `${title}: ${count}`;
  }, [count, title]);

  return (
    <div>
      <h1>{title}</h1>
      <p>Count: {count}</p>
      <button onClick={() => setCount(c => c + 1)}>
        Increment
      </button>
    </div>
  );
}
```

## Core Technologies

### Foundation
- HTML5 semantic markup
- CSS3 (Flexbox, Grid, animations)
- JavaScript ES2020+
- TypeScript for type safety

### Frameworks
- **React** 18+ with hooks
- **Vue.js** 3+ composition API
- **Angular** 16+ with RxJS
- **Svelte** for compiler-based approach

### Meta-Frameworks
- **Next.js** - React with SSR, SSG, API routes
- **Nuxt** - Vue with full-stack capabilities
- **SvelteKit** - Svelte framework
- **Remix** - Focus on web fundamentals

### State Management
- React Context API
- Redux Toolkit
- Zustand, Jotai, Recoil
- Vue Composition API / Pinia
- MobX, Akita

### Styling
- Tailwind CSS
- CSS Modules & BEM
- Styled Components / Emotion
- SASS/SCSS

### Build Tools
- Vite (fast development)
- Webpack (powerful bundling)
- Turbopack (next-gen)
- esbuild (transpilation)

### Testing
- Jest unit testing
- React Testing Library
- Cypress / Playwright E2E
- Vitest for Vite projects

## Best Practices

1. **Semantic HTML** - Use correct elements for accessibility
2. **Responsive Design** - Mobile-first approach
3. **Performance** - Optimize Core Web Vitals
4. **Accessibility** - WCAG 2.1 AA compliance
5. **Type Safety** - Use TypeScript
6. **Code Quality** - ESLint + Prettier
7. **Testing** - Aim for 80%+ coverage
8. **Documentation** - Storybook for components

## Resources

- [MDN Web Docs](https://developer.mozilla.org/)
- [React Documentation](https://react.dev/)
- [Web.dev Learning](https://web.dev/learn/)
