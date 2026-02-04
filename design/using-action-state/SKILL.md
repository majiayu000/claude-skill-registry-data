---
name: using-action-state
description: Teaches useActionState hook for managing form state with Server Actions in React 19. Use when implementing forms, handling form submissions, tracking pending states, or working with Server Functions.
allowed-tools: Read, Write, Edit, Glob, Grep
version: 1.0.0
---

# useActionState Patterns for Forms

<role>
Teaches React 19's `useActionState` hook for form state management with Server Actions.
</role>

<when-to-activate>
When: mentioning `useActionState`, form state/handling, Server Actions/Functions; tracking pending/submission status; implementing progressive enhancement; server-side form validation.
</when-to-activate>

<overview>
`useActionState` manages form state based on action results: tracks pending state (automatic `isPending`), manages form state (returns action results), integrates Server Actions (`'use server'`), enables progressive enhancement (optional no-JS permalink). Replaces manual form submission state management.
</overview>

<workflow>
## Standard Form with useActionState

**Server Action:**

```javascript
'use server';

export async function submitForm(previousState, formData) {
  const email = formData.get('email');

  if (!email || !email.includes('@')) {
    return { error: 'Invalid email address' };
  }

  await saveToDatabase({ email });
  return { success: true };
}
```

````

**Component:**

```javascript
'use client';

import { useActionState } from 'react';
import { submitForm } from './actions';

function ContactForm() {
  const [state, formAction, isPending] = useActionState(submitForm, null);

  return (
    <form action={formAction}>
      <input name="email" type="email" required />

      <button type="submit" disabled={isPending}>
        {isPending ? 'Submitting...' : 'Submit'}
      </button>

      {state?.error && <p className="error">{state.error}</p>}
      {state?.success && <p className="success">Submitted!</p>}
    </form>
  );
}
```

</workflow>

<conditional-workflows>
## Decision Points

**Progressive Enhancement:** Add permalink as third argument: `useActionState(submitForm, null, '/api/submit')`. Form submits to URL before JS loads; server handles both cases.

**Validation:** Server Action receives previousState, returns error object for failures, success object when valid; component renders errors from state.

**Multi-Step Forms:** Track step in state; Server Action advances step or returns errors; component renders current step.
</conditional-workflows>

<progressive-disclosure>
## References

- **Server Actions**: `../../forms/skills/server-actions/SKILL.md`
- **Form Validation**: `../../forms/skills/form-validation/SKILL.md`
- **Progressive Enhancement**: `../../../research/react-19-comprehensive.md` (lines 715-722)

**Cross-Plugin References:**

- If customizing validation error messages, use the customizing-errors skill for error formatting with safeParse and field error flattening

Load as needed for specific patterns.
</progressive-disclosure>

<examples>
## Example 1: Validation with

Zod

```javascript
'use server';

import { z } from 'zod';

const schema = z.object({
  email: z.string().email(),
  message: z.string().min(10).max(1000),
});

export async function contactAction(previousState, formData) {
  const data = {
    email: formData.get('email'),
    message: formData.get('message'),
  };

  const result = schema.safeParse(data);

  if (!result.success) {
    return { errors: result.error.flatten().fieldErrors };
  }

  try {
    await db.contacts.create({ data: result.data });
    return { success: true };
  } catch (error) {
    return { error: 'Failed to submit contact form' };
  }
}
```

```javascript
'use client';

import { useActionState } from 'react';
import { contactAction } from './actions';

export default function ContactForm() {
  const [state, formAction, isPending] = useActionState(contactAction, null);

  if (state?.success) {
    return <p>Thank you for contacting us!</p>;
  }

  return (
    <form action={formAction}>
      <div>
        <label htmlFor="email">Email</label>
        <input id="email" name="email" type="email" required />
        {state?.errors?.email && <span className="error">{state.errors.email}</span>}
      </div>

      <div>
        <label htmlFor="message">Message</label>
        <textarea id="message" name="message" required />
        {state?.errors?.message && <span className="error">{state.errors.message}</span>}
      </div>

      <button type="submit" disabled={isPending}>
        {isPending ? 'Sending...' : 'Send Message'}
      </button>

      {state?.error && <p className="error">{state.error}</p>}
    </form>
  );
}
```

## Example 2: Multi-Step Form

```javascript
'use server';

export async function multiStepAction(previousState, formData) {
  const step = previousState?.step || 1;

  if (step === 1) {
    const name = formData.get('name');
    if (!name || name.length < 2) {
      return { step: 1, error: 'Name is required' };
    }
    return { step: 2, data: { name } };
  }

  if (step === 2) {
    const email = formData.get('email');
    if (!email?.includes('@')) {
      return { step: 2, error: 'Valid email required', data: previousState.data };
    }

    await db.users.create({
      data: { ...previousState.data, email },
    });

    return { step: 3, success: true };
  }
}
```

```javascript
'use client';

import { useActionState } from 'react';
import { multiStepAction } from './actions';

export default function MultiStepForm() {
  const [state, formAction, isPending] = useActionState(multiStepAction, { step: 1 });

  if (state.success) {
    return <p>Registration complete!</p>;
  }

  return (
    <form action={formAction}>
      {state.step === 1 && (
        <>
          <h2>Step 1: Name</h2>
          <input name="name" type="text" required />
          {state.error && <p className="error">{state.error}</p>}
        </>
      )}

      {state.step === 2 && (
        <>
          <h2>Step 2: Email</h2>
          <p>Name: {state.data.name}</p>
          <input name="email" type="email" required />
          {state.error && <p className="error">{state.error}</p>}
        </>
      )}

      <button type="submit" disabled={isPending}>
        {isPending ? 'Processing...' : state.step === 2 ? 'Complete' : 'Next'}
      </button>
    </form>
  );
}
```

</examples>

<constraints>
**MUST**: First parameter

is `previousState`, second is `formData`; return serializable values (no functions, symbols); access form values via `formData.get('fieldName')`; mark functions with `'use server'` directive.

**SHOULD**: Validate inputs server-side; return structured error objects for field errors; disable submit button on `isPending`; show loading indicators; use validation libraries (zod, yup).

**NEVER**: Trust client-side validation alone; return sensitive data in errors; mutate `previousState` directly; skip error handling for async operations; omit authentication/authorization checks.
</constraints>

<validation>
**After Implementation**: Test form submission (valid data → success, invalid → errors, check `isPending`); verify Server Action (receives `previousState` and `formData`, returns serializable objects, handles errors); check security (server validates all inputs, authentication/authorization implemented, no sensitive data exposed); test progressive enhancement (disable JS, form submits to permalink, server handles both cases).
</validation>

---

## Common Patterns

**Optimistic Updates**: Combine with `useOptimistic` for immediate UI feedback:

```javascript
const [state, formAction] = useActionState(addTodo, null);
const [optimisticTodos, addOptimisticTodo] = useOptimistic(todos, (state, newTodo) => [
  ...state,
  newTodo,
]);
```

See `../optimistic-updates/SKILL.md`.

**Reset Form on Success**:

```javascript
const formRef = useRef();

const [state, formAction] = useActionState(async (prev, formData) => {
  const result = await submitForm(prev, formData);
  if (result.success) {
    formRef.current?.reset();
  }
  return result;
}, null);

return (
  <form ref={formRef} action={formAction}>
    ...
  </form>
);
```

For comprehensive documentation: `research/react-19-comprehensive.md` lines 135-180.
````
