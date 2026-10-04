---
name: Sonner
description: Opinionated toast notification component for React by Emil Kowalski — API, variants, patterns, clean code standards
---

Sonner is an opinionated toast component for React by Emil Kowalski. Use it for all notification/feedback UI. It is the gold standard for toast UX.

## Installation

```bash
npm install sonner
# or
pnpm i sonner
```

## Setup

Place `<Toaster />` once at the root layout (works in server components like `layout.tsx`):

```tsx
import { Toaster } from 'sonner';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Toaster />
      </body>
    </html>
  );
}
```

## Toast Types

```tsx
import { toast } from 'sonner';

// Basic
toast('Message');

// Variants
toast.success('Saved successfully');
toast.error('Something went wrong');
toast.loading('Saving...');
toast.warning('Low disk space');
toast.info('Update available');

// With description
toast.success('File uploaded', {
  description: 'profile-photo.jpg has been uploaded.',
});

// Action button
toast('Message', {
  action: {
    label: 'Undo',
    onClick: () => console.log('Undo'),
  },
});

// Cancel button
toast('Message', {
  cancel: {
    label: 'Cancel',
    onClick: () => console.log('Cancelled'),
  },
});

// Promise (auto handles loading → success/error)
toast.promise(saveData(), {
  loading: 'Saving...',
  success: (data) => `Saved ${data.name}`,
  error: 'Failed to save',
});

// Custom JSX (fully custom, uses Sonner styles)
toast(<div>Custom <b>content</b></div>);

// Headless (no Sonner styles)
toast.custom((id) => (
  <div>
    Custom toast
    <button onClick={() => toast.dismiss(id)}>Close</button>
  </div>
));
```

## All Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `description` | ReactNode | — | Subtitle text |
| `duration` | number | 4000 | Auto-close ms (Infinity = never) |
| `position` | string | `bottom-right` | See positions below |
| `closeButton` | boolean | false | Show X button |
| `dismissible` | boolean | true | Swipe/click to dismiss |
| `icon` | ReactNode | — | Custom icon |
| `action` | object | — | `{ label, onClick }` |
| `cancel` | object | — | `{ label, onClick }` |
| `id` | string\|number | auto | For update/dismiss |
| `onDismiss` | function | — | Called when dismissed |
| `onAutoClose` | function | — | Called on auto-close |
| `style` | object | — | Inline styles |
| `className` | string | — | CSS class |

## Positions

`top-left` `top-center` `top-right` `bottom-left` `bottom-center` `bottom-right`

## Toaster Props

```tsx
<Toaster
  position="top-right"
  expand={false}          // expand all toasts (default: stack)
  richColors={true}       // vibrant success/error colors
  closeButton={true}      // global close button
  theme="light"           // 'light' | 'dark' | 'system'
  visibleToasts={3}       // max visible at once
  toastOptions={{         // default options for all toasts
    duration: 5000,
    classNames: {
      toast: 'my-toast',
      title: 'my-title',
    },
  }}
/>
```

## Update a Toast

```tsx
const id = toast.loading('Loading...');
// later:
toast.success('Done!', { id });
```

## Dismiss Programmatically

```tsx
toast.dismiss(id);    // dismiss specific
toast.dismiss();      // dismiss all
```

## Clean Code Rules

- Always use `toast.promise()` for async operations — never manually sequence loading/success/error toasts
- Set `duration: Infinity` for errors that require user action
- Use `richColors` in production for clear visual feedback
- Never show more than 3 toasts at once — set `visibleToasts={3}`
- Toasts are transitions (interruptible), not keyframe animations — this is intentional and correct
