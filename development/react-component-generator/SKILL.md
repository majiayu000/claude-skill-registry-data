---
name: react-component-generator
description: Generate React component files with TypeScript, hooks, props interfaces, and styling patterns following best practices. Triggers on "create React component", "generate component for", "React TypeScript component", "scaffold React component".
---

# React Component Generator

Generate production-ready React components with TypeScript, proper typing, hooks patterns, and various styling approaches.

## Output Requirements

**File Output:** `.tsx` files, optionally with `.css`/`.module.css`/`.styles.ts`
**Format:** TypeScript React (TSX)
**Standards:** React 18+, TypeScript 5+

## When Invoked

Immediately generate a complete, typed React component. Include props interface, sensible defaults, and appropriate hooks.

## Component Patterns

### Functional Component (Standard)
```tsx
// Button.tsx
import { type ButtonHTMLAttributes, forwardRef } from 'react';
import styles from './Button.module.css';

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  /** Button visual variant */
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  /** Button size */
  size?: 'sm' | 'md' | 'lg';
  /** Show loading state */
  isLoading?: boolean;
  /** Full width button */
  fullWidth?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      variant = 'primary',
      size = 'md',
      isLoading = false,
      fullWidth = false,
      disabled,
      className,
      children,
      ...props
    },
    ref
  ) => {
    const classNames = [
      styles.button,
      styles[variant],
      styles[size],
      fullWidth && styles.fullWidth,
      isLoading && styles.loading,
      className,
    ]
      .filter(Boolean)
      .join(' ');

    return (
      <button
        ref={ref}
        className={classNames}
        disabled={disabled || isLoading}
        {...props}
      >
        {isLoading ? (
          <>
            <span className={styles.spinner} aria-hidden="true" />
            <span className={styles.srOnly}>Loading...</span>
          </>
        ) : (
          children
        )}
      </button>
    );
  }
);

Button.displayName = 'Button';
```

### Component with State and Effects
```tsx
// SearchInput.tsx
import {
  useState,
  useEffect,
  useCallback,
  type ChangeEvent,
  type KeyboardEvent,
} from 'react';
import { useDebouncedValue } from '@/hooks/useDebouncedValue';
import styles from './SearchInput.module.css';

export interface SearchInputProps {
  /** Placeholder text */
  placeholder?: string;
  /** Initial search value */
  defaultValue?: string;
  /** Debounce delay in milliseconds */
  debounceMs?: number;
  /** Called when search value changes (debounced) */
  onSearch: (query: string) => void;
  /** Called on Enter key press */
  onSubmit?: (query: string) => void;
  /** Show loading indicator */
  isLoading?: boolean;
  /** Disable input */
  disabled?: boolean;
}

export function SearchInput({
  placeholder = 'Search...',
  defaultValue = '',
  debounceMs = 300,
  onSearch,
  onSubmit,
  isLoading = false,
  disabled = false,
}: SearchInputProps) {
  const [value, setValue] = useState(defaultValue);
  const debouncedValue = useDebouncedValue(value, debounceMs);

  // Call onSearch when debounced value changes
  useEffect(() => {
    onSearch(debouncedValue);
  }, [debouncedValue, onSearch]);

  const handleChange = useCallback((e: ChangeEvent<HTMLInputElement>) => {
    setValue(e.target.value);
  }, []);

  const handleKeyDown = useCallback(
    (e: KeyboardEvent<HTMLInputElement>) => {
      if (e.key === 'Enter' && onSubmit) {
        onSubmit(value);
      }
    },
    [value, onSubmit]
  );

  const handleClear = useCallback(() => {
    setValue('');
  }, []);

  return (
    <div className={styles.container}>
      <input
        type="search"
        className={styles.input}
        placeholder={placeholder}
        value={value}
        onChange={handleChange}
        onKeyDown={handleKeyDown}
        disabled={disabled}
        aria-label="Search"
      />

      {isLoading && (
        <span className={styles.spinner} aria-hidden="true" />
      )}

      {value && !isLoading && (
        <button
          type="button"
          className={styles.clearButton}
          onClick={handleClear}
          aria-label="Clear search"
        >
          ×
        </button>
      )}
    </div>
  );
}
```

### Data Fetching Component
```tsx
// UserProfile.tsx
import { useQuery } from '@tanstack/react-query';
import { fetchUser } from '@/api/users';
import { Skeleton } from '@/components/Skeleton';
import { ErrorMessage } from '@/components/ErrorMessage';
import styles from './UserProfile.module.css';

export interface UserProfileProps {
  /** User ID to fetch */
  userId: string;
  /** Show compact version */
  compact?: boolean;
}

export function UserProfile({ userId, compact = false }: UserProfileProps) {
  const {
    data: user,
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  if (isLoading) {
    return <UserProfileSkeleton compact={compact} />;
  }

  if (isError) {
    return (
      <ErrorMessage
        message={error instanceof Error ? error.message : 'Failed to load user'}
        onRetry={refetch}
      />
    );
  }

  if (!user) {
    return <ErrorMessage message="User not found" />;
  }

  if (compact) {
    return (
      <div className={styles.compact}>
        <img
          src={user.avatarUrl}
          alt={user.name}
          className={styles.avatarSmall}
        />
        <span className={styles.name}>{user.name}</span>
      </div>
    );
  }

  return (
    <article className={styles.profile}>
      <header className={styles.header}>
        <img
          src={user.avatarUrl}
          alt={user.name}
          className={styles.avatar}
        />
        <div className={styles.info}>
          <h2 className={styles.name}>{user.name}</h2>
          <p className={styles.email}>{user.email}</p>
        </div>
      </header>

      {user.bio && (
        <p className={styles.bio}>{user.bio}</p>
      )}

      <footer className={styles.footer}>
        <span>Joined {new Date(user.createdAt).toLocaleDateString()}</span>
      </footer>
    </article>
  );
}

function UserProfileSkeleton({ compact }: { compact: boolean }) {
  if (compact) {
    return (
      <div className={styles.compact}>
        <Skeleton circle width={32} height={32} />
        <Skeleton width={100} height={16} />
      </div>
    );
  }

  return (
    <div className={styles.profile}>
      <div className={styles.header}>
        <Skeleton circle width={80} height={80} />
        <div className={styles.info}>
          <Skeleton width={150} height={24} />
          <Skeleton width={200} height={16} />
        </div>
      </div>
      <Skeleton width="100%" height={60} />
    </div>
  );
}
```

### Form Component
```tsx
// ContactForm.tsx
import { useForm, type SubmitHandler } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Button } from '@/components/Button';
import { Input } from '@/components/Input';
import { Textarea } from '@/components/Textarea';
import styles from './ContactForm.module.css';

const contactSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Please enter a valid email'),
  subject: z.string().min(5, 'Subject must be at least 5 characters'),
  message: z.string().min(20, 'Message must be at least 20 characters'),
});

type ContactFormData = z.infer<typeof contactSchema>;

export interface ContactFormProps {
  /** Called on successful submission */
  onSubmit: (data: ContactFormData) => Promise<void>;
  /** Called on cancel */
  onCancel?: () => void;
}

export function ContactForm({ onSubmit, onCancel }: ContactFormProps) {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting, isSubmitSuccessful },
  } = useForm<ContactFormData>({
    resolver: zodResolver(contactSchema),
    defaultValues: {
      name: '',
      email: '',
      subject: '',
      message: '',
    },
  });

  const handleFormSubmit: SubmitHandler<ContactFormData> = async (data) => {
    await onSubmit(data);
    reset();
  };

  if (isSubmitSuccessful) {
    return (
      <div className={styles.success}>
        <p>Thank you! Your message has been sent.</p>
        <Button onClick={() => reset()}>Send another message</Button>
      </div>
    );
  }

  return (
    <form
      className={styles.form}
      onSubmit={handleSubmit(handleFormSubmit)}
      noValidate
    >
      <div className={styles.field}>
        <Input
          label="Name"
          {...register('name')}
          error={errors.name?.message}
          required
        />
      </div>

      <div className={styles.field}>
        <Input
          label="Email"
          type="email"
          {...register('email')}
          error={errors.email?.message}
          required
        />
      </div>

      <div className={styles.field}>
        <Input
          label="Subject"
          {...register('subject')}
          error={errors.subject?.message}
          required
        />
      </div>

      <div className={styles.field}>
        <Textarea
          label="Message"
          rows={5}
          {...register('message')}
          error={errors.message?.message}
          required
        />
      </div>

      <div className={styles.actions}>
        {onCancel && (
          <Button type="button" variant="ghost" onClick={onCancel}>
            Cancel
          </Button>
        )}
        <Button type="submit" isLoading={isSubmitting}>
          Send Message
        </Button>
      </div>
    </form>
  );
}
```

### Modal/Dialog Component
```tsx
// Modal.tsx
import {
  useEffect,
  useCallback,
  useRef,
  type ReactNode,
  type KeyboardEvent,
} from 'react';
import { createPortal } from 'react-dom';
import { FocusTrap } from '@/components/FocusTrap';
import styles from './Modal.module.css';

export interface ModalProps {
  /** Whether modal is open */
  isOpen: boolean;
  /** Called when modal should close */
  onClose: () => void;
  /** Modal title */
  title: string;
  /** Modal content */
  children: ReactNode;
  /** Modal size */
  size?: 'sm' | 'md' | 'lg' | 'xl';
  /** Close on overlay click */
  closeOnOverlayClick?: boolean;
  /** Close on Escape key */
  closeOnEscape?: boolean;
  /** Show close button */
  showCloseButton?: boolean;
}

export function Modal({
  isOpen,
  onClose,
  title,
  children,
  size = 'md',
  closeOnOverlayClick = true,
  closeOnEscape = true,
  showCloseButton = true,
}: ModalProps) {
  const modalRef = useRef<HTMLDivElement>(null);

  // Handle Escape key
  useEffect(() => {
    if (!isOpen || !closeOnEscape) return;

    const handleKeyDown = (e: globalThis.KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, closeOnEscape, onClose]);

  // Lock body scroll when open
  useEffect(() => {
    if (isOpen) {
      const originalOverflow = document.body.style.overflow;
      document.body.style.overflow = 'hidden';
      return () => {
        document.body.style.overflow = originalOverflow;
      };
    }
  }, [isOpen]);

  const handleOverlayClick = useCallback(() => {
    if (closeOnOverlayClick) {
      onClose();
    }
  }, [closeOnOverlayClick, onClose]);

  const handleContentClick = useCallback((e: React.MouseEvent) => {
    e.stopPropagation();
  }, []);

  if (!isOpen) return null;

  return createPortal(
    <div
      className={styles.overlay}
      onClick={handleOverlayClick}
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
    >
      <FocusTrap>
        <div
          ref={modalRef}
          className={`${styles.modal} ${styles[size]}`}
          onClick={handleContentClick}
        >
          <header className={styles.header}>
            <h2 id="modal-title" className={styles.title}>
              {title}
            </h2>
            {showCloseButton && (
              <button
                type="button"
                className={styles.closeButton}
                onClick={onClose}
                aria-label="Close modal"
              >
                ×
              </button>
            )}
          </header>
          <div className={styles.content}>{children}</div>
        </div>
      </FocusTrap>
    </div>,
    document.body
  );
}

// Subcomponents for composition
Modal.Footer = function ModalFooter({
  children,
}: {
  children: ReactNode;
}) {
  return <footer className={styles.footer}>{children}</footer>;
};
```

## File Structure Patterns

### Single File Component
```
components/
  Button/
    Button.tsx
    Button.module.css
    Button.test.tsx
    index.ts
```

### index.ts (Barrel Export)
```typescript
// components/Button/index.ts
export { Button } from './Button';
export type { ButtonProps } from './Button';
```

## Props Patterns

### Extending HTML Elements
```typescript
interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary';
}

interface InputProps extends Omit<InputHTMLAttributes<HTMLInputElement>, 'size'> {
  size?: 'sm' | 'md' | 'lg';
}
```

### Polymorphic Components
```typescript
type AsProp<C extends ElementType> = {
  as?: C;
};

type PropsToOmit<C extends ElementType, P> = keyof (AsProp<C> & P);

type PolymorphicComponentProp<
  C extends ElementType,
  Props = {}
> = React.PropsWithChildren<Props & AsProp<C>> &
  Omit<React.ComponentPropsWithoutRef<C>, PropsToOmit<C, Props>>;
```

## Validation Checklist

Before outputting, verify:
- [ ] TypeScript types for all props
- [ ] Default values for optional props
- [ ] Proper event handler types
- [ ] forwardRef for components needing refs
- [ ] displayName set for forwardRef components
- [ ] Accessible (aria labels, roles)
- [ ] Keyboard navigation support
- [ ] Loading/error states handled

## Example Invocations

**Prompt:** "Create a React dropdown select component with TypeScript"
**Output:** Complete `Select.tsx` with props interface, options, keyboard nav, accessibility.

**Prompt:** "Generate a data table component with sorting and pagination"
**Output:** Complete `DataTable.tsx` with generic typing, sort handlers, pagination state.

**Prompt:** "React modal component with animations"
**Output:** Complete `Modal.tsx` with portal, focus trap, transitions, accessibility.
