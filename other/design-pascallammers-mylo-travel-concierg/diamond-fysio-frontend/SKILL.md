---
name: diamond-fysio-frontend
description: Review and write React/Next.js components for Diamond Fysio project. Use when reviewing components, adding features, or checking code quality. Enforces project patterns like Tailwind CSS, accessibility, Contentful integration, and i18n.
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Diamond Fysio Frontend Skill

This skill ensures consistency with the Diamond Fysio project's frontend patterns and best practices.

## Project Overview

- **Framework**: Next.js 16 with Pages Router (primary) + App Router (new routes)
- **React**: v19
- **TypeScript**: Mixed (TSX and JSX components)
- **Styling**: Tailwind CSS
- **CMS**: Contentful with GraphQL
- **Icons**: Heroicons, FontAwesome, React Icons
- **Forms**: React Hook Form
- **Animation**: Framer Motion
- **i18n**: Dutch (nl) and English (en) locales

## Code Review Checklist

When reviewing or writing components, verify:

### 1. Accessibility (Critical)

- **ARIA labels**: All interactive elements must have `aria-label` attributes
- **Keyboard navigation**: Use `tabIndex={0}` for focusable elements
- **Focus states**: Apply `focus:outline-none focus-visible:ring-2 focus-visible:ring-teal-500`
- **Semantic HTML**: Use proper heading hierarchy (h1, h2, h3)
- **Alt text**: All images must have meaningful `alt` attributes

**Example from Button.jsx**:

```jsx
<p className={btnType} role="button" aria-label={title} tabIndex={0}>
  {title}
</p>
```

### 2. Styling Patterns

- **Use Tailwind CSS** exclusively (no inline styles or CSS modules)
- **Gradient buttons**: Follow the pattern `bg-gradient-to-r from-teal-500 to-cyan-600`
- **Hover states**: `hover:from-teal-400 hover:to-cyan-500`
- **Responsive design**: Use `md:`, `lg:` prefixes for breakpoints
- **Consistent spacing**: Use Tailwind spacing scale (px-8, py-3, etc.)

**Common button classes**:

```jsx
const btnType =
  'w-full inline-flex items-center justify-center px-8 py-3 text-base font-medium rounded-md text-white bg-gradient-to-r from-teal-500 to-cyan-600 hover:from-teal-400 hover:to-cyan-500 md:py-4 md:text-lg md:px-10 shadow focus:outline-none focus-visible:ring-2 focus-visible:ring-teal-500';
```

### 3. Internationalization (i18n)

- **Support both nl and en locales**
- **Use router locale**: `const locale = router?.locale || 'nl'`
- **Provide fallback defaults** for all translated strings
- **Structure**: Create defaults object with nl/en keys

**Example pattern**:

```jsx
const router = useRouter();
const locale = router?.locale || 'nl';
const isEn = locale === 'en';

const defaults = {
  nl: { title: 'Nederlandse tekst', ... },
  en: { title: 'English text', ... }
};

const t = {
  title: i18n?.title || defaults[locale].title
};
```

### 4. Next.js Routing

- **Internal links**: Use `next/link` with `<Link href={path}>`
- **External links**: Use `<a href={url} rel="noopener noreferrer">`
- **Locale awareness**: Check `router.locale` for current language
- **Pages structure**: Components in `/components`, pages in `/pages`

### 5. React Patterns

- **Hooks**: Use modern hooks (useState, useRouter, etc.)
- **Props destructuring**: `({ title, type, internal_link }) => {}`
- **Default props**: Use ES6 defaults `extra_classes = ''`
- **No React import needed**: Next.js handles this automatically

### 6. Contentful Integration

- **GraphQL queries**: Store in `/lib/query/`
- **Content types**: Check `/components/contentTypes/` for type definitions
- **Rich text**: Use `@contentful/rich-text-react-renderer`
- **Image optimization**: Use Next.js `<Image>` component when possible

### 7. Form Handling

- **Use React Hook Form** for complex forms
- **Validation**: Implement client-side validation
- **Error states**: Show user-friendly error messages in both languages
- **Loading states**: Display loading indicators during submission
- **Success feedback**: Use CheckCircleIcon from Heroicons for success states

### 8. Component Structure

- **File organization**:
  - Simple components: Single file in `/components/ComponentName.jsx`
  - Complex components: Directory `/components/ComponentName/` with sub-components
- **Export pattern**: Use `export default ComponentName`
- **Naming**: PascalCase for component files and names

### 9. Code Quality

- **ESLint compliance**: Follow the project's ESLint config
  - React hooks rules enforced
  - jsx-a11y warnings enabled
  - Promise handling patterns
- **No unused variables**: Clean up unused imports and variables
- **Consistent formatting**: Use Prettier (runs via Husky pre-commit)

### 10. Performance Considerations

- **Lazy loading**: Use dynamic imports for heavy components
- **Image optimization**: Leverage Next.js Image component
- **Memoization**: Use React.memo for expensive renders (when needed)
- **Avoid unnecessary re-renders**: Check useEffect dependencies

## Common Issues to Flag

1. **Missing accessibility attributes** (aria-label, alt text, tabIndex)
2. **Inline styles instead of Tailwind classes**
3. **Missing i18n translations** (only Dutch or only English)
4. **Incorrect link components** (using `<a>` for internal links)
5. **Missing focus states** on interactive elements
6. **Non-semantic HTML** (divs instead of buttons, missing headings)
7. **Hard-coded text** that should be translatable
8. **Missing error handling** in forms or API calls

## Project-Specific Patterns

### Gradient Colors

Primary gradient: `from-teal-500 to-cyan-600`
Hover gradient: `from-teal-400 to-cyan-500`
Focus ring: `focus-visible:ring-teal-500`

### Icons

- Heroicons: `@heroicons/react/solid` or `@heroicons/react/outline`
- FontAwesome: `@fortawesome/react-fontawesome`
- React Icons: `react-icons`

### Layout

- Use `<Layout>` wrapper from `/components/Layout/Layout.jsx`
- Headers: Different header types in `/components/Headers/`
- Footer: Consistent footer from `/components/Layout/Footer.jsx`

## Example Code Reviews

### Good Example ✅

```jsx
import Link from 'next/link';

const Button = ({ title, internal_link, external_link, extra_classes = '' }) => {
  const btnType =
    'inline-flex items-center px-8 py-3 rounded-md bg-gradient-to-r from-teal-500 to-cyan-600 hover:from-teal-400 hover:to-cyan-500 focus:outline-none focus-visible:ring-2 focus-visible:ring-teal-500';

  return internal_link ? (
    <Link href={internal_link}>
      <p className={btnType} role="button" aria-label={title} tabIndex={0}>
        {title}
      </p>
    </Link>
  ) : (
    <a href={external_link} className={btnType} aria-label={title} rel="noopener noreferrer">
      {title}
    </a>
  );
};

export default Button;
```

### Issues to Fix ❌

```jsx
// Missing: Next.js Link, accessibility, Tailwind classes
const Button = ({ title, link }) => {
  return (
    <a href={link} style={{ backgroundColor: 'teal' }}>
      {' '}
      {/* inline style! */}
      {title} {/* no aria-label! */}
    </a>
  );
};
```

## When Adding New Features

1. **Check existing components** for similar patterns first
2. **Maintain accessibility** from the start
3. **Support both languages** (nl/en)
4. **Use Tailwind utilities** instead of custom CSS
5. **Test keyboard navigation** and focus states
6. **Follow the gradient/color scheme** for consistency
7. **Add proper error handling** and loading states
8. **Document complex logic** with comments if needed

## Testing Considerations

- Verify accessibility with keyboard navigation
- Test both Dutch and English versions
- Check mobile responsiveness (Tailwind breakpoints)
- Validate form submissions
- Test with Contentful data (staging and production)

## Deployment & Testing URLs

- **Live URL**: https://fysiodiamondfactory.nl
- **Recent deployments**: Check fysiodiamondfactory.nl for the latest production version

When testing features, always verify on the live site to ensure proper deployment.

## Resources

- Tailwind config: `/tailwind.config.js`
- ESLint config: `/eslint.config.js`
- TypeScript config: `/tsconfig.json`
- Documentation: `/docs/` folder
