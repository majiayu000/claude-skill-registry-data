---
name: frontend-debugging
description: Systematic 10-phase debugging procedure for SvelteKit 2 + Svelte 5 frontend issues. Use when components fail to render, routing breaks, runes throw errors, or Encore client calls fail.
---

# Frontend Debugging Skill

**Purpose:** Systematic 10-phase debugging procedure for SvelteKit 2 + Svelte 5 frontend issues.

---

## When to Use

- Component rendering issues
- Routing problems
- Svelte 5 runes errors ($state, $derived, $effect)
- API client failures
- Build or type errors

---

## 10-Phase Debugging Process

### Phase 1: Health Check
```bash
task frontend:dev
# Check browser console
```

### Phase 2: Type Safety
```bash
task frontend:typecheck
task frontend:lint
```

### Phase 3: Encore Client Sync
```bash
task founder:workflows:regen-client
# Verify ~encore/clients imports
```

### Phase 4: Svelte 5 Runes
- Check proper rune usage **and declaration**
- `$state`, `$derived`, `$bindable`, `$props` that you mutate must use `let` (never `const`)
- `$bindable` requires `{value}` with `oninput` instead of `bind:value`
- `$effect` for side effects only (no async return)

### Phase 5: Routing
- Verify +page.svelte structure
- Check +layout.svelte hierarchy
- Review load functions

### Phase 6: API Calls
- Always use Encore generated client
- Never manual `fetch()` calls
- Full type safety guaranteed

### Phase 7: SSR/CSR Issues
- Check server vs browser context
- Verify `browser` checks when needed

### Phase 8: Component Isolation
- Test component in isolation
- Check props/slots/events

### Phase 9: Build Testing
```bash
task frontend:build
# Test production build
```

### Phase 10: Browser DevTools
- Use Svelte DevTools extension
- Check component state/props
- Review network requests

---

## Reference Library

- `references/svelte5-runes-debugging.md` – Deep dive on rune errors (const vs let, `$bindable`, diagnostics workflow)
- `references/common-issues.md` – Expanded checklist for routing, SSR hydration, Encore client sync, and fast-fail signals
- `frontend-development_skill` – Source of truth for runes, Skeleton UI patterns, and API integration standards
- `e2e-testing_skill` – Playwright regression workflow when UI issues require end-to-end verification

