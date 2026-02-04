---
name: frontend-engineering
description: >-
  Domain specialist for frontend architecture, state management, accessibility, and performance.
  Scope: component architecture, state management (Pinia, Vuex, Redux), accessibility (WCAG), responsive design, lazy loading, asset optimization, XSS prevention, CSP, frontend performance.
  Excludes: backend code, infrastructure, API design, security beyond XSS, performance profiling beyond frontend.
  Triggers: "frontend", "React", "Vue", "Angular", "component", "state management", "accessibility", "WCAG", "responsive", "XSS", "CSP".
---

# FRONTEND_ENGINEERING

## DOMAIN EXPERTISE
- **Common Issues**: State synchronization issues, prop drilling, excessive re-renders, accessibility violations, performance bottlenecks, XSS vulnerabilities, missing semantic HTML, poor responsive design, missing lazy loading
- **Common Mistakes**: Using global state instead of state management, prop drilling deeply, not using semantic HTML, not implementing ARIA labels, not testing with screen readers, XSS vulnerabilities via v-html/dangerouslySetInnerHTML, missing alt text, not optimizing bundle size
- **Related Patterns**: Component composition, presentational/container pattern, higher-order components, render props, custom hooks/composables, context API, state management patterns (Redux, Vuex, Pinia), server-side rendering, client-side rendering
- **Problematic Patterns**: God component, prop drilling, excessive props, callback hell, component coupling, missing error boundaries, unoptimized images, missing code splitting
- **Security Concerns**: XSS attacks (reflected, stored, DOM-based), CSRF attacks, content security policy violations, sensitive data in localStorage/sessionStorage, insecure third-party scripts, dangerous HTML usage
- **Performance Issues**: Large bundle sizes, missing code splitting, missing lazy loading for images/routes, unoptimized images, missing compression, excessive re-renders, memory leaks, missing service worker
- **Accessibility Issues**: Missing semantic HTML, missing ARIA labels, keyboard navigation issues, color contrast issues, missing focus indicators, screen reader incompatibility, missing alt text
- **State Management**: Global state, local component state, state persistence, time travel debugging, state synchronization, middleware, actions, reducers, selectors

## MODE DETECTION
- **WRITE Mode**: Keywords: ["create", "generate", "write", "build", "implement", "add", "new", "create component", "build UI", "implement state"]
- **REVIEW Mode**: Keywords: ["review", "analyze", "audit", "check", "find issues", "accessibility audit", "performance review", "security review"]

## LOADING STRATEGY
### Write Mode (Progressive)
Load patterns based on frontend requirements:
- Component architecture -> Load `@architecture/COMPONENT-ARCHITECTURE.md`
- State management -> Load `@state/STATE-MANAGEMENT.md`
- Accessibility -> Load `@accessibility/WCAG.md`
- Security -> Load `@security/XSS-PROTECTION.md`
- Performance -> Load `@performance/LAZY-LOADING.md`, `@performance/ASSET-OPTIMIZATION.md`

### Review Mode (Exhaustive)
Load comprehensive checklists:
- IF component review requested -> Load all architecture and component patterns
- IF accessibility audit requested -> Load `@accessibility/WCAG.md`
- IF security review requested -> Load `@security/XSS-PROTECTION.md`
- IF performance review requested -> Load all performance patterns

## ROUTING LOGIC
### Progressive Loading (Write Mode)
- **IF** request mentions "component", "UI", "interface" -> READ FILE: `@architecture/COMPONENT-ARCHITECTURE.md`
- **IF** request mentions "state", "Redux", "Vuex", "Pinia", "context" -> READ FILE: `@state/STATE-MANAGEMENT.md`
- **IF** request mentions "accessibility", "WCAG", "a11y", "ARIA" -> READ FILE: `@accessibility/WCAG.md`
- **IF** request mentions "XSS", "security", "sanitize" -> READ FILE: `@security/XSS-PROTECTION.md`
- **IF** request mentions "performance", "lazy load", "optimize" -> READ FILE: `@performance/LAZY-LOADING.md`

### Comprehensive Loading (Review Mode)
- **IF** request mentions "review", "audit", "analyze" -> READ FILES: All architecture, accessibility, security, performance patterns

## CONTEXT DETECTION
### Framework Detection
- **React**: package.json with "react", .jsx, .tsx files, React components, hooks, Redux
- **Vue.js**: package.json with "vue", .vue files, Vue components, Vuex, Pinia
- **Angular**: package.json with "@angular/*", .component.ts, .module.ts files, TypeScript
- **Svelte**: package.json with "svelte", .svelte files
- **Ember.js**: package.json with "ember-cli", Ember application structure
- **SolidJS**: package.json with "solid-js", .jsx files with solid-js

### Language Detection
- **JavaScript**: .js files, package.json, no TypeScript
- **TypeScript**: .ts, .tsx files, tsconfig.json, type definitions
- **JSX/TSX**: React JSX syntax, TSX files

### UI Library Detection
- **Material UI**: package.json with "@mui/material", "@mui/icons-material"
- **Bootstrap**: package.json with "bootstrap", "@types/bootstrap"
- **Tailwind CSS**: tailwind.config.js, postcss.config.js
- **Chakra UI**: package.json with "@chakra-ui/react"
- **Ant Design**: package.json with "antd"

## EXECUTION PROTOCOL

### Phase 1: Clarification
1. **Detect Mode**: WRITE vs REVIEW based on keywords
2. **Detect Context**: Framework (React/Vue/Angular), language (JavaScript/TypeScript), UI libraries
3. **Load Patterns**: Progressive (write) or Exhaustive (review)
4. **Detect Multi-Domain**: Check if additional skills needed (security, performance, API)

### Phase 2: Planning
1. Load relevant frontend pattern references
2. Implement component architecture according to framework conventions
3. Apply state management best practices
4. Ensure accessibility (semantic HTML, ARIA labels)
5. Prevent XSS vulnerabilities (sanitization, CSP)
6. Implement performance optimizations (lazy loading, code splitting)
7. Provide framework-specific examples

### Phase 3: Execution
1. Load all frontend checklist references
2. Systematically check each category:
   - Component architecture (prop drilling, component coupling)
   - State management (global state, state synchronization)
   - Accessibility (WCAG compliance, semantic HTML, ARIA)
   - Security (XSS vulnerabilities, CSP, content security)
   - Performance (bundle size, lazy loading, re-renders)
3. Provide prioritized issues with severity levels

### Phase 4: Validation
- Verify components follow framework conventions
- Check accessibility with screen reader (WCAG Level AA)
- Validate XSS prevention (sanitization, CSP)
- Ensure performance optimizations applied
- Check for cross-references (MUST be within skill only)

## OUTPUT FORMAT

### Write Mode Output
```markdown
## Frontend Implementation: [Component]

### Framework: [React/Vue/Angular/Svelte]

### Implementation
```jsx/react/vue/tsx
// Framework-specific component code
```

### State Management
- [State pattern used]
- [State management library]

### Accessibility
- [Semantic HTML]
- [ARIA labels]
- [Keyboard navigation]

### Security
- [XSS prevention measures]
- [Content Security Policy]

### Performance
- [Lazy loading strategy]
- [Code splitting]
- [Bundle optimization]

### Related Patterns
@architecture/[specific-pattern].md
```

### Review Mode Output
```markdown
## Frontend Review Report

### Critical Issues
1. **[Issue Name]**: [Component/file:line]
   - Severity: CRITICAL
   - Category: [Architecture/Accessibility/Security/Performance]
   - Description: [Issue details]
   - Impact: [Accessibility violation / XSS vulnerability / Performance degradation]
   - Fix: [Recommended action]
   - Reference: @architecture/[specific-pattern].md or @security/[specific-pattern].md

### High Priority Issues
[Same format]

### Medium Priority Issues
[Same format]

### Low Priority Issues
[Same format]

### Accessibility Assessment
- **WCAG Level**: [A / AA / AAA compliance]
- **Semantic HTML**: [Compliant / Issues found]
- **ARIA Labels**: [Complete / Missing labels]
- **Keyboard Navigation**: [Fully accessible / Issues found]
- **Color Contrast**: [Compliant / WCAG violations]

### Security Assessment
- **XSS Vulnerabilities**: [Locations and types]
- **CSP Issues**: [Missing or weak CSP]
- **Third-Party Scripts**: [Security concerns]

### Performance Assessment
- **Bundle Size**: [Current size, recommended size]
- **Code Splitting**: [Implemented / Missing]
- **Lazy Loading**: [Implemented / Missing]
- **Re-renders**: [Excessive / Optimal]

### Recommendations
1. [Architecture improvement]
2. [Accessibility improvement]
3. [Security improvement]
4. [Performance optimization]
```
