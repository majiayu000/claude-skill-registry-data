---
name: common-pitfalls
description: Apply when debugging errors, reviewing code for issues, or encountering unexpected behavior. Contains known mistakes with ChurchTools API, Vue components, TypeScript, Safari cookies, and form handling.
---

# Common Pitfalls

## ChurchTools API

| Pitfall | Wrong | Correct |
|---------|-------|---------|
| Nested params | `{ params: { key: 'val' } }` | `{ key: 'val' }` |
| Delete method | `churchtoolsClient.delete()` | `churchtoolsClient.deleteApi()` |
| Tags response | `response.data` | `response` (direct array) |
| Tag domains | `'appointment'` | `'person' \| 'song' \| 'group'` |

## Vue Components

| Pitfall | Wrong | Correct |
|---------|-------|---------|
| Button type | `<button>` | `<button type="button">` |
| BaseCard import | Absolute path | Relative: `../common/BaseCard.vue` |
| Reactivity | Plain objects | `ref()` or `reactive()` |

## TypeScript

- Check `src/ct-types.d.ts` for ChurchTools types
- Always define interfaces for API responses
- Use strict typing for all data

## Build Issues

- Verify import paths after moving components
- Check for missing dependencies in package.json
- Ensure all required fields in API requests

## Safari-specific

- Blocks `Secure; SameSite=None` cookies on `http://localhost`
- Blocks third-party cookies from different domains
- Solution: Use Vite proxy + HTTPS

## Form Submission

Buttons without `type="button"` will submit forms and cause page reloads:
```vue
<!-- Wrong - triggers form submission -->
<button @click="handleClick">Click</button>

<!-- Correct -->
<button type="button" @click="handleClick">Click</button>
```

## API Error Handling

Always wrap API calls in try-catch with loading states:
```typescript
try {
  loading.value = true
  // API call
} catch (err) {
  error.value = 'User-friendly message'
  console.error('Debug info:', err)
} finally {
  loading.value = false
}
```
