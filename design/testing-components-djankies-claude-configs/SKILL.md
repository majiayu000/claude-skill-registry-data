---
name: testing-components
description: Teaches React Testing Library patterns for React 19 components. Use when writing component tests, testing interactions, or testing with Server Actions.
allowed-tools: Read, Write, Edit
version: 1.0.0
---

# Testing React 19 Components

For Vitest test structure and mocking patterns (describe/test blocks, vi.fn(), assertions), see `vitest-4/skills/writing-vitest-tests/SKILL.md`.

## Basic Component Testing

```javascript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Button from './Button';

test('button renders and handles click', async () => {
  const handleClick = vi.fn();

  render(<Button onClick={handleClick}>Click me</Button>);

  const button = screen.getByRole('button', { name: /click me/i });
  expect(button).toBeInTheDocument();

  await userEvent.click(button);
  expect(handleClick).toHaveBeenCalledTimes(1);
});
```

## Testing Forms with useActionState

```javascript
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import ContactForm from './ContactForm';

vi.mock('./actions', () => ({
  submitContact: vi.fn(async (prev, formData) => {
    const email = formData.get('email');
    if (!email?.includes('@')) {
      return { error: 'Invalid email' };
    }
    return { success: true };
  }),
}));

test('form shows error for invalid email', async () => {
  render(<ContactForm />);

  await userEvent.type(screen.getByLabelText(/email/i), 'invalid');
  await userEvent.click(screen.getByRole('button', { name: /submit/i }));

  await waitFor(() => {
    expect(screen.getByText(/invalid email/i)).toBeInTheDocument();
  });
});

test('form succeeds with valid email', async () => {
  render(<ContactForm />);

  await userEvent.type(screen.getByLabelText(/email/i), 'test@example.com');
  await userEvent.click(screen.getByRole('button', { name: /submit/i }));

  await waitFor(() => {
    expect(screen.getByText(/success/i)).toBeInTheDocument();
  });
});
```

## Testing with Context

```javascript
import { render, screen } from '@testing-library/react';
import { UserProvider } from './UserContext';
import UserProfile from './UserProfile';

test('displays user name from context', () => {
  const user = { name: 'Alice', email: 'alice@example.com' };

  render(
    <UserProvider value={user}>
      <UserProfile />
    </UserProvider>
  );

  expect(screen.getByText('Alice')).toBeInTheDocument();
});
```

For comprehensive testing patterns, see: React Testing Library documentation.
