---
name: vue-frontend
category: frontend
difficulty: intermediate
wcag_level: AA
version: 1.0.0
last_updated: 2025-10-17
related_skills:
- typescript
- testing
- accessibility
- security
description: Composition API vs Options API
---


# Vue.js Frontend Development Skill

## Level 1: Quick Reference (~700-900 tokens)

### Core Concepts

**Composition API vs Options API**

```typescript
// Composition API (recommended for new projects)
import { ref, computed } from 'vue';

const count = ref(0);
const doubled = computed(() => count.value * 2);

// Options API (traditional)
export default {
  data() { return { count: 0 }; },
  computed: { doubled() { return this.count * 2; } }
};
```

**Reactivity Fundamentals**

```typescript
// ref - for primitives and single values
const count = ref(0);
count.value++; // access with .value

// reactive - for objects
const state = reactive({ count: 0, name: 'Vue' });
state.count++; // direct access

// computed - derived state
const doubled = computed(() => count.value * 2);

// watch - side effects
watch(count, (newVal, oldVal) => {
  console.log(`Count changed from ${oldVal} to ${newVal}`);
});
```

**Component Communication**

```typescript
// Props (parent → child)
defineProps<{ message: string }>();

// Emits (child → parent)
const emit = defineEmits<{ submit: [data: FormData] }>();
emit('submit', formData);

// Provide/Inject (ancestor → descendant)
// Parent
provide('theme', ref('dark'));
// Child
const theme = inject<Ref<string>>('theme');
```

### Essential Checklist

**Setup & Configuration**

- [ ] Vue 3 with Vite or Vue CLI
- [ ] TypeScript integration
- [ ] ESLint + Prettier configured
- [ ] Vue Router installed
- [ ] Pinia for state management
- [ ] Vitest + Vue Test Utils for testing

**Component Development**

- [ ] Use Composition API with `<script setup>`
- [ ] Define props with TypeScript types
- [ ] Emit typed events
- [ ] Implement proper lifecycle hooks
- [ ] Use composables for reusable logic

**Routing & Navigation**

- [ ] Define routes with lazy loading
- [ ] Implement route guards (auth, permissions)
- [ ] Handle 404 and error pages
- [ ] Use typed router with generics

**State Management**

- [ ] Define Pinia stores with TypeScript
- [ ] Use composition stores for complex logic
- [ ] Implement persistence for user preferences
- [ ] Handle async actions properly

**Performance**

- [ ] Use `v-once` for static content
- [ ] Implement virtual scrolling for large lists
- [ ] Lazy load routes and components
- [ ] Use `v-memo` for expensive renders
- [ ] Configure proper build optimization

**Accessibility (WCAG 2.1 AA)**

- [ ] Semantic HTML elements
- [ ] ARIA labels and roles
- [ ] Keyboard navigation support
- [ ] Focus management
- [ ] Screen reader testing

**Security**

- [ ] Sanitize user input (DOMPurify)
- [ ] Configure CSP headers
- [ ] Avoid `v-html` with untrusted content
- [ ] Implement proper authentication
- [ ] Secure API communication

---

## Level 2:
>
> **📚 Full Examples**: See [REFERENCE.md](./REFERENCE.md) for complete code samples, detailed configurations, and production-ready implementations.

 Implementation Guide (~4000-5000 tokens)

### 1. Vue 3 Composition API

#### Setup Function & Script Setup

The Composition API provides better TypeScript support and code organization:


*See [REFERENCE.md](./REFERENCE.md#example-0) for complete implementation.*


#### Reactive Primitives

**ref vs reactive**:

- `ref`: Primitives, single values, needs `.value` in script
- `reactive`: Objects, arrays, no `.value` needed


*See [REFERENCE.md](./REFERENCE.md#example-1) for complete implementation.*


#### Computed Properties


*See [REFERENCE.md](./REFERENCE.md#example-2) for complete implementation.*


#### Watchers


*See [REFERENCE.md](./REFERENCE.md#example-3) for complete implementation.*


### 2. Component Architecture

#### Props & Emits


*See [REFERENCE.md](./REFERENCE.md#example-4) for complete implementation.*


#### Slots


*See [REFERENCE.md](./REFERENCE.md#example-5) for complete implementation.*


#### Provide/Inject


*See [REFERENCE.md](./REFERENCE.md#example-6) for complete implementation.*


### 3. Vue Router

#### Route Configuration


*See [REFERENCE.md](./REFERENCE.md#example-7) for complete implementation.*


#### Navigation Guards


*See [REFERENCE.md](./REFERENCE.md#example-8) for complete implementation.*


#### Typed Routes


*See [REFERENCE.md](./REFERENCE.md#example-9) for complete implementation.*


### 4. State Management with Pinia

#### Store Definition


*See [REFERENCE.md](./REFERENCE.md#example-10) for complete implementation.*


#### Store Composition


*See [REFERENCE.md](./REFERENCE.md#example-11) for complete implementation.*


#### Store Persistence


*See [REFERENCE.md](./REFERENCE.md#example-12) for complete implementation.*


### 5. Performance Optimization

#### Virtual Scrolling


*See [REFERENCE.md](./REFERENCE.md#example-13) for complete implementation.*


#### Lazy Loading


*See [REFERENCE.md](./REFERENCE.md#example-14) for complete implementation.*


#### Memoization


*See [REFERENCE.md](./REFERENCE.md#example-15) for complete implementation.*


#### Build Optimization


*See [REFERENCE.md](./REFERENCE.md#example-16) for complete implementation.*


### 6. Testing with Vitest

#### Component Testing


*See [REFERENCE.md](./REFERENCE.md#example-17) for complete implementation.*


#### Store Testing


*See [REFERENCE.md](./REFERENCE.md#example-18) for complete implementation.*


#### Composable Testing


*See [REFERENCE.md](./REFERENCE.md#example-19) for complete implementation.*


### 7. Accessibility (WCAG 2.1 AA)

#### Semantic HTML


*See [REFERENCE.md](./REFERENCE.md#example-20) for complete implementation.*


#### ARIA Attributes


*See [REFERENCE.md](./REFERENCE.md#example-21) for complete implementation.*


#### Keyboard Navigation


*See [REFERENCE.md](./REFERENCE.md#example-22) for complete implementation.*


#### Focus Management


*See [REFERENCE.md](./REFERENCE.md#example-23) for complete implementation.*


### 8. Security Best Practices

#### XSS Prevention


*See [REFERENCE.md](./REFERENCE.md#example-24) for complete implementation.*


#### Content Security Policy


*See [REFERENCE.md](./REFERENCE.md#example-25) for complete implementation.*


#### Secure API Communication


*See [REFERENCE.md](./REFERENCE.md#example-26) for complete implementation.*


#### Input Validation


*See [REFERENCE.md](./REFERENCE.md#example-27) for complete implementation.*


---

## Level 3: Deep Dive Resources

### Official Documentation

- [Vue 3 Documentation](https://vuejs.org/guide/introduction.html) - Official Vue 3 guide
- [Vue Router Documentation](https://router.vuejs.org/) - Official routing library
- [Pinia Documentation](https://pinia.vuejs.org/) - Official state management
- [Vitest Documentation](https://vitest.dev/) - Testing framework
- [Vue Test Utils](https://test-utils.vuejs.org/) - Component testing utilities

### Advanced Topics

- [Vue 3 Composition API RFC](https://github.com/vuejs/rfcs/blob/master/active-rfcs/0013-composition-api.md) - Design rationale
- [VueUse](https://vueuse.org/) - Collection of composition utilities
- [Vue Macros](https://vue-macros.sxzz.moe/) - Experimental features
- [Nuxt 3](https://nuxt.com/) - Full-stack Vue framework
- [Vite](https://vitejs.dev/) - Next-generation build tool

### Performance & Optimization

- [Vue Performance Guide](https://vuejs.org/guide/best-practices/performance.html) - Official performance tips
- [Virtual Scrolling](https://github.com/tangbc/vue-virtual-scroll-list) - Large list optimization
- [Vue DevTools](https://devtools.vuejs.org/) - Performance profiling

### Accessibility

- [Vue A11y](https://vue-a11y.com/) - Vue accessibility resources
- [ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/) - W3C patterns
- [axe DevTools](https://www.deque.com/axe/devtools/) - Accessibility testing

### Security

- [OWASP Vue Security Cheatsheet](https://cheatsheetseries.owasp.org/cheatsheets/Vue_Security_Cheat_Sheet.html)
- [DOMPurify](https://github.com/cure53/DOMPurify) - XSS sanitization
- [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP) - MDN guide

### Bundled Resources

- See `templates/composition-component.vue` - Complete component template
- See `templates/pinia-store.ts` - Pinia store template
- See `templates/component.test.ts` - Vitest test template
- See `config/vitest.config.ts` - Vitest configuration
- See `resources/accessibility-checklist.md` - WCAG 2.1 AA checklist
- See `resources/performance-checklist.md` - Performance optimization guide

## Examples

### Basic Usage

```python
// TODO: Add basic example for vue
// This example demonstrates core functionality
```

### Advanced Usage

```python
// TODO: Add advanced example for vue
// This example shows production-ready patterns
```

### Integration Example

```python
// TODO: Add integration example showing how vue
// works with other systems and services
```

See `examples/vue/` for complete working examples.

## Integration Points

This skill integrates with:

### Upstream Dependencies

- **Tools**: Common development tools and frameworks
- **Prerequisites**: Basic understanding of general concepts

### Downstream Consumers

- **Applications**: Production systems requiring vue functionality
- **CI/CD Pipelines**: Automated testing and deployment workflows
- **Monitoring Systems**: Observability and logging platforms

### Related Skills

- See other skills in this category

### Common Integration Patterns

1. **Development Workflow**: How this skill fits into daily development
2. **Production Deployment**: Integration with production systems
3. **Monitoring & Alerting**: Observability integration points

## Common Pitfalls

### Pitfall 1: Insufficient Testing

**Problem:** Not testing edge cases and error conditions leads to production bugs

**Solution:** Implement comprehensive test coverage including:

- Happy path scenarios
- Error handling and edge cases
- Integration points with external systems

**Prevention:** Enforce minimum code coverage (80%+) in CI/CD pipeline

### Pitfall 2: Hardcoded Configuration

**Problem:** Hardcoding values makes applications inflexible and environment-dependent

**Solution:** Use environment variables and configuration management:

- Separate config from code
- Use environment-specific configuration files
- Never commit secrets to version control

**Prevention:** Use tools like dotenv, config validators, and secret scanners

### Pitfall 3: Ignoring Security Best Practices

**Problem:** Security vulnerabilities from not following established security patterns

**Solution:** Follow security guidelines:

- Input validation and sanitization
- Proper authentication and authorization
- Encrypted data transmission (TLS/SSL)
- Regular security audits and updates

**Prevention:** Use security linters, SAST tools, and regular dependency updates

**Best Practices:**

- Follow established patterns and conventions for vue
- Keep dependencies up to date and scan for vulnerabilities
- Write comprehensive documentation and inline comments
- Use linting and formatting tools consistently
- Implement proper error handling and logging
- Regular code reviews and pair programming
- Monitor production metrics and set up alerts

---

**Note**: This skill focuses on Vue 3 Composition API, modern tooling (Vite, Vitest), and production-ready patterns. For options API or Vue 2, refer to the official migration guides.
