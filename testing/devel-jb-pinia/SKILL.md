---
name: devel-jb-pinia
description: "--| | SSR | Server-side rendering, state hydration | [advanced-ssr](references/advanced-ssr."
domain: cybersecurity
---

--|
| SSR | Server-side rendering, state hydration | [advanced-ssr](references/advanced-ssr.md) |
| Nuxt | Nuxt integration, auto-imports, SSR best practices | [advanced-nuxt](references/advanced-nuxt.md) |
| HMR | Hot module replacement for development | [advanced-hmr](references/advanced-hmr.md) |

## Key Recommendations

- **Prefer Setup Stores** for complex logic, composables, and watchers
- **Use `storeToRefs()`** when destructuring state/getters to preserve reactivity
- **Actions can be destructured directly** - they're bound to the store
- **Call stores inside functions** not at module scope, especially for SSR
- **Add HMR support** to each store for better development experience
- **Use `@pinia/testing`** for component tests with mocked stores
