---
name: senternet-site-mobile-forms
description: Add proper mobile keyboard, autocomplete, and autocorrect attributes to all form inputs.
---

# Mobile Form Input Attributes

Audit every `<input>`, `<textarea>`, and `<select>` in the site and apply the correct mobile-focused HTML attributes so iOS and Android users get the right keyboard, autofill, and correction behavior.

## Why this matters

Without these attributes:
- Email fields show the default alpha keyboard instead of the `@`-optimized email keyboard
- Name fields don't suggest contacts from the device address book
- Email and URL fields get autocorrected into gibberish
- Message textareas don't capitalize the first word of a sentence
- Browsers can't offer one-tap autofill for common fields

## Attribute reference by field type

### Email
```tsx
<input
  type="email"
  inputMode="email"
  autoComplete="email"
  autoCapitalize="none"
  autoCorrect="off"
  spellCheck={false}
/>
```
- `inputMode="email"` shows the `@` keyboard on iOS/Android
- `autoCapitalize="none"` prevents iOS from capitalizing the first character
- `autoCorrect="off"` prevents "gmail.com" from becoming "Gmail.com"
- `spellCheck={false}` suppresses red underlines on email addresses

### Full name
```tsx
<input
  type="text"
  autoComplete="name"
  autoCapitalize="words"
  autoCorrect="off"
/>
```
- `autoComplete="name"` offers contact autofill
- `autoCapitalize="words"` capitalizes each word (correct for names)
- `autoCorrect="off"` prevents names being "corrected" to dictionary words

### First name / last name (separate fields)
```tsx
<input type="text" autoComplete="given-name"  autoCapitalize="words" autoCorrect="off" />
<input type="text" autoComplete="family-name" autoCapitalize="words" autoCorrect="off" />
```

### Phone
```tsx
<input
  type="tel"
  inputMode="tel"
  autoComplete="tel"
  autoCorrect="off"
  autoCapitalize="none"
/>
```

### URL
```tsx
<input
  type="url"
  inputMode="url"
  autoComplete="url"
  autoCorrect="off"
  autoCapitalize="none"
  spellCheck={false}
/>
```

### Number / quantity
```tsx
<input
  type="text"
  inputMode="numeric"
  autoCorrect="off"
  autoCapitalize="none"
/>
```
Prefer `inputMode="numeric"` over `type="number"` when you want the numeric keyboard without the browser's up/down spinner UI.

### Search
```tsx
<input
  type="search"
  inputMode="search"
  autoComplete="off"
  autoCorrect="off"
  autoCapitalize="none"
  spellCheck={false}
/>
```

### Free-text / message textarea
```tsx
<textarea
  autoCapitalize="sentences"
  autoCorrect="on"
  spellCheck={true}
/>
```
- `autoCapitalize="sentences"` capitalizes the first word after each period
- `autoCorrect="on"` enables spell-checking (appropriate for prose)

### Subject / single-line prose
```tsx
<input
  type="text"
  autoCapitalize="sentences"
  autoCorrect="on"
  spellCheck={true}
/>
```

### Password
```tsx
<input
  type="password"
  autoComplete="current-password"  // or "new-password" for signup
  autoCorrect="off"
  autoCapitalize="none"
  spellCheck={false}
/>
```

## autoComplete token reference

Use the correct token so browsers and password managers can fill fields accurately:

| Field | `autoComplete` value |
|---|---|
| Full name | `name` |
| First name | `given-name` |
| Last name | `family-name` |
| Email | `email` |
| Phone | `tel` |
| Street address | `street-address` |
| City | `address-level2` |
| State | `address-level1` |
| Zip / postal code | `postal-code` |
| Country | `country` |
| Credit card number | `cc-number` |
| Card expiry | `cc-exp` |
| CVV | `cc-csc` |
| Current password | `current-password` |
| New password | `new-password` |
| One-time code | `one-time-code` |
| Username | `username` |
| Organization | `organization` |
| Job title | `organization-title` |
| Website / URL | `url` |
| Field the browser should not fill | `off` |

## Honeypot fields

Honeypot inputs should be hidden from both users and autofill:

```tsx
<input
  type="text"
  name="website"
  className="hidden"
  tabIndex={-1}
  autoComplete="off"
/>
```

`autoComplete="off"` prevents the browser from filling the honeypot, which would trigger false positives.

## Checklist

Go through every form in the site and verify:

- [ ] `type="email"` inputs have `inputMode="email"`, `autoCapitalize="none"`, `autoCorrect="off"`, `spellCheck={false}`
- [ ] Name inputs have `autoComplete="name"` (or `given-name`/`family-name`), `autoCapitalize="words"`, `autoCorrect="off"`
- [ ] Phone inputs use `type="tel"` and `inputMode="tel"`
- [ ] URL inputs use `type="url"` and `inputMode="url"` with `autoCorrect="off"` and `spellCheck={false}`
- [ ] Numeric inputs use `inputMode="numeric"` (not `type="number"` unless spinners are acceptable)
- [ ] Free-text textareas have `autoCapitalize="sentences"`, `autoCorrect="on"`, `spellCheck={true}`
- [ ] Password inputs have correct `autoComplete` (`current-password` or `new-password`)
- [ ] Honeypot inputs have `autoComplete="off"` and `tabIndex={-1}`
- [ ] No prose input has `autoCorrect="off"` unless it's a technical field (email, URL, code)
- [ ] Search inputs have `autoCorrect="off"` and `spellCheck={false}`

## How to audit

Search for all inputs in the project:

```bash
grep -rn '<input\|<textarea\|<select' src/ --include="*.tsx" --include="*.jsx"
```

For each result, check the field's semantic type and apply the attributes from the reference above.

## Framework: Next.js track

The input attributes (`inputMode`, `autoComplete`, `autoCapitalize`, `autoCorrect`, `enterKeyHint`, type selection) are plain HTML and apply verbatim.

The only difference: a form with client-side state or an `onSubmit` handler must live in a `'use client'` component — keep it a leaf so the surrounding page stays a server component. A form that posts to a route handler (`app/api/<name>/route.ts`) or a server action needs no directive at all.

See `/senternet-site-framework` for the full convention map.
