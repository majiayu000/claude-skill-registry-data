---
name: tracking-form-status
description: Teaches useFormStatus hook for tracking form submission state in React 19. Use when implementing submit buttons, form loading states, or pending indicators.
allowed-tools: Read, Write, Edit
version: 1.0.0
---

# Form Status Tracking with useFormStatus

`useFormStatus` provides status info about parent form submissions.

## Basic Usage

**MUST be called inside a form component:**

```javascript
import { useFormStatus } from 'react-dom';

function SubmitButton() {
  const { pending, data, method, action } = useFormStatus();

  return (
    <button type="submit" disabled={pending}>
      {pending ? 'Submitting...' : 'Submit'}
    </button>
  );
}

function MyForm() {
  async function handleSubmit(formData) {
    'use server';
    await saveData(formData);
  }

  return (
    <form action={handleSubmit}>
      <input name="email" />
      <SubmitButton />
    </form>
  );
}
```

## Return Values

- `pending` (boolean): Whether form is submitting
- `data` (FormData | null): Data being submitted
- `method` (string): HTTP method ('get' or 'post')
- `action` (function | null): Action function

## Critical Requirement

❌ **Wrong - called at form level:**

```javascript
function MyForm() {
  const { pending } = useFormStatus();
  return <form>...</form>;
}
```

✅ **Correct - called inside form:**

```javascript
function MyForm() {
  return (
    <form>
      <SubmitButton />
    </form>
  );
}

function SubmitButton() {
  const { pending } = useFormStatus();
  return <button disabled={pending}>Submit</button>;
}
```

For comprehensive useFormStatus documentation, see: `research/react-19-comprehensive.md` lines 312-355.
