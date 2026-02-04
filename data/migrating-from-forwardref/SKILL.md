---
name: migrating-from-forwardref
description: Teaches migration from forwardRef to ref-as-prop pattern in React 19. Use when seeing forwardRef usage, upgrading React components, or when refs are mentioned. forwardRef is deprecated in React 19.
allowed-tools: Read, Write, Edit, Glob, Grep
version: 1.0.0
---

# Migrating from forwardRef to Ref as Prop

<role>
This skill teaches you how to migrate from the deprecated `forwardRef` API to React 19's ref-as-prop pattern.
</role>

<when-to-activate>
This skill activates when:

- User mentions `forwardRef`, refs, or ref forwarding
- Seeing code that uses `React.forwardRef`
- Upgrading components to React 19
- Need to expose DOM refs from custom components
- TypeScript errors about ref props
</when-to-activate>

<overview>
React 19 deprecates `forwardRef` in favor of ref as a regular prop:

**Why the Change:**
1. **Simpler API** - Refs are just props, no special wrapper needed
2. **Better TypeScript** - Easier type inference and typing
3. **Consistency** - All props handled the same way
4. **Less Boilerplate** - Fewer imports and wrapper functions

**Migration Path:**
- `forwardRef` still works in React 19 (deprecated, not removed)
- New code should use ref as prop
- Gradual migration recommended for existing codebases

**Key Difference:**
```javascript
// OLD: forwardRef (deprecated)
const Button = forwardRef((props, ref) => ...);

// NEW: ref as prop (React 19)
function Button({ ref, ...props }) { ... }
```
</overview>

<workflow>
## Migration Process

**Step 1: Identify forwardRef Usage**

Search codebase for `forwardRef`:
```bash
# Use Grep tool
pattern: "forwardRef"
output_mode: "files_with_matches"
```

**Step 2: Understand Current Pattern**

Before (React 18):
```javascript
import { forwardRef } from 'react';

const MyButton = forwardRef((props, ref) => {
  return (
    <button ref={ref} className={props.className}>
      {props.children}
    </button>
  );
});
```

**Step 3: Convert to Ref as Prop**

After (React 19):
```javascript
function MyButton({ children, className, ref }) {
  return (
    <button ref={ref} className={className}>
      {children}
    </button>
  );
}
```

**Step 4: Update TypeScript Types (if applicable)**

Before:
```typescript
import { forwardRef } from 'react';

interface ButtonProps {
  variant: 'primary' | 'secondary';
  children: React.ReactNode;
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant, children }, ref) => {
    return (
      <button ref={ref} className={variant}>
        {children}
      </button>
    );
  }
);
```

After:
```typescript
import { Ref } from 'react';

interface ButtonProps {
  variant: 'primary' | 'secondary';
  children: React.ReactNode;
  ref?: Ref<HTMLButtonElement>;
}

function Button({ variant, children, ref }: ButtonProps) {
  return (
    <button ref={ref} className={variant}>
      {children}
    </button>
  );
}
```

**Step 5: Test Component**

Verify ref forwarding still works:
```javascript
function Parent() {
  const buttonRef = useRef(null);

  useEffect(() => {
    buttonRef.current?.focus();
  }, []);

  return <Button ref={buttonRef}>Click me</Button>;
}
```

</workflow>

<conditional-workflows>
## Complex Scenarios

**If component uses useImperativeHandle:**

Before:
```javascript
const FancyInput = forwardRef((props, ref) => {
  const inputRef = useRef();

  useImperativeHandle(ref, () => ({
    focus: () => inputRef.current.focus(),
    clear: () => { inputRef.current.value = ''; }
  }));

  return <input ref={inputRef} />;
});
```

After:
```javascript
function FancyInput({ ref }) {
  const inputRef = useRef();

  useImperativeHandle(ref, () => ({
    focus: () => inputRef.current.focus(),
    clear: () => { inputRef.current.value = ''; }
  }));

  return <input ref={inputRef} />;
}
```

**If component has multiple refs:**

```javascript
function ComplexComponent({ ref, innerRef, ...props }) {
  return (
    <div ref={ref}>
      <input ref={innerRef} {...props} />
    </div>
  );
}
```

**If using generic components:**

```typescript
interface GenericProps<T> {
  value: T;
  ref?: Ref<HTMLDivElement>;
}

function GenericComponent<T>({ value, ref }: GenericProps<T>) {
  return <div ref={ref}>{String(value)}</div>;
}
```

</conditional-workflows>

<progressive-disclosure>
## Reference Files

For detailed information:

- **Ref Cleanup Functions**: See `../../../research/react-19-comprehensive.md` (lines 1013-1033)
- **useImperativeHandle**: See `../../../research/react-19-comprehensive.md` (lines 614-623)
- **TypeScript Migration**: See `../../../research/react-19-comprehensive.md` (lines 890-916)
- **Complete Migration Guide**: See `../../../research/react-19-comprehensive.md` (lines 978-1011)

Load references when specific patterns are needed.
</progressive-disclosure>

<examples>
## Example 1: Simple Button Migration

**Before (React 18 with forwardRef):**

```javascript
import { forwardRef } from 'react';

const Button = forwardRef((props, ref) => (
  <button ref={ref} {...props}>
    {props.children}
  </button>
));

Button.displayName = 'Button';

export default Button;
```

**After (React 19 with ref prop):**

```javascript
function Button({ children, ref, ...props }) {
  return (
    <button ref={ref} {...props}>
      {children}
    </button>
  );
}

export default Button;
```

**Changes Made:**
1. ✅ Removed `forwardRef` import
2. ✅ Removed `forwardRef` wrapper
3. ✅ Added `ref` to props destructuring
4. ✅ Removed unnecessary `displayName`
5. ✅ Simplified function signature

## Example 2: TypeScript Component with Multiple Props

**Before:**

```typescript
import { forwardRef, HTMLAttributes } from 'react';

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  title: string;
  description?: string;
  variant?: 'default' | 'outlined';
}

const Card = forwardRef<HTMLDivElement, CardProps>(
  ({ title, description, variant = 'default', ...props }, ref) => {
    return (
      <div ref={ref} className={`card card-${variant}`} {...props}>
        <h3>{title}</h3>
        {description && <p>{description}</p>}
      </div>
    );
  }
);

Card.displayName = 'Card';

export default Card;
```

**After:**

```typescript
import { Ref, HTMLAttributes } from 'react';

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  title: string;
  description?: string;
  variant?: 'default' | 'outlined';
  ref?: Ref<HTMLDivElement>;
}

function Card({
  title,
  description,
  variant = 'default',
  ref,
  ...props
}: CardProps) {
  return (
    <div ref={ref} className={`card card-${variant}`} {...props}>
      <h3>{title}</h3>
      {description && <p>{description}</p>}
    </div>
  );
}

export default Card;
```

**Changes Made:**
1. ✅ Changed import from `forwardRef` to `Ref` type
2. ✅ Added `ref?: Ref<HTMLDivElement>` to interface
3. ✅ Removed `forwardRef` wrapper
4. ✅ Added `ref` to props destructuring
5. ✅ Removed `displayName`

## Example 3: Input with useImperativeHandle

**Before:**

```javascript
import { forwardRef, useRef, useImperativeHandle } from 'react';

const SearchInput = forwardRef((props, ref) => {
  const inputRef = useRef();

  useImperativeHandle(ref, () => ({
    focus() {
      inputRef.current?.focus();
    },
    clear() {
      inputRef.current.value = '';
    },
    getValue() {
      return inputRef.current?.value || '';
    }
  }));

  return (
    <input
      ref={inputRef}
      type="text"
      placeholder="Search..."
      {...props}
    />
  );
});

export default SearchInput;
```

**After:**

```javascript
import { useRef, useImperativeHandle } from 'react';

function SearchInput({ ref, ...props }) {
  const inputRef = useRef();

  useImperativeHandle(ref, () => ({
    focus() {
      inputRef.current?.focus();
    },
    clear() {
      inputRef.current.value = '';
    },
    getValue() {
      return inputRef.current?.value || '';
    }
  }));

  return (
    <input
      ref={inputRef}
      type="text"
      placeholder="Search..."
      {...props}
    />
  );
}

export default SearchInput;
```

**Usage (unchanged):**

```javascript
function SearchBar() {
  const searchRef = useRef();

  const handleClear = () => {
    searchRef.current?.clear();
  };

  return (
    <>
      <SearchInput ref={searchRef} />
      <button onClick={handleClear}>Clear</button>
    </>
  );
}
```

## Example 4: Component Library Pattern

**Before:**

```typescript
import { forwardRef, ComponentPropsWithoutRef, ElementRef } from 'react';

type ButtonElement = ElementRef<'button'>;
type ButtonProps = ComponentPropsWithoutRef<'button'> & {
  variant?: 'primary' | 'secondary';
};

const Button = forwardRef<ButtonElement, ButtonProps>(
  ({ variant = 'primary', className, ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={`btn btn-${variant} ${className || ''}`}
        {...props}
      />
    );
  }
);

Button.displayName = 'Button';
```

**After:**

```typescript
import { Ref, ComponentPropsWithoutRef, ElementRef } from 'react';

type ButtonElement = ElementRef<'button'>;
type ButtonProps = ComponentPropsWithoutRef<'button'> & {
  variant?: 'primary' | 'secondary';
  ref?: Ref<ButtonElement>;
};

function Button({
  variant = 'primary',
  className,
  ref,
  ...props
}: ButtonProps) {
  return (
    <button
      ref={ref}
      className={`btn btn-${variant} ${className || ''}`}
      {...props}
    />
  );
}
```

</examples>

<constraints>
## MUST

- Add `ref` to props interface when using TypeScript
- Use `Ref<HTMLElement>` type from React for TypeScript
- Test that ref forwarding works after migration
- Maintain component behavior exactly (only syntax changes)

## SHOULD

- Migrate components gradually (forwardRef still works)
- Update tests to verify ref behavior
- Use consistent prop ordering (ref near other element props)
- Document breaking changes if part of public API

## NEVER

- Remove `forwardRef` if still on React 18
- Change component behavior during migration
- Break existing ref usage in parent components
- Skip TypeScript type updates for ref prop

</constraints>

<validation>
## After Migration

1. **Verify Ref Forwarding**:
   ```javascript
   const ref = useRef(null);
   <MyComponent ref={ref} />
   // ref.current should be the DOM element
   ```

2. **Check TypeScript Compilation**:
   ```bash
   npx tsc --noEmit
   ```
   No errors about ref props

3. **Test Component Behavior**:
   - Component renders correctly
   - Ref accesses correct DOM element
   - useImperativeHandle methods work (if used)
   - No console warnings about deprecated APIs

4. **Verify Backward Compatibility**:
   - Existing usage still works
   - No breaking changes to component API
   - Tests pass

</validation>

---

## Migration Checklist

When migrating a component from forwardRef:

- [ ] Remove `forwardRef` import
- [ ] Remove `forwardRef` wrapper function
- [ ] Add `ref` to props destructuring
- [ ] Add `ref` type to TypeScript interface (if applicable)
- [ ] Remove `displayName` if only used for forwardRef
- [ ] Test ref forwarding works
- [ ] Update component tests
- [ ] Check TypeScript compilation
- [ ] Verify no breaking changes to API

## Common Migration Patterns

### Pattern 1: Simple Ref Forwarding
```javascript
// Before
const Comp = forwardRef((props, ref) => <div ref={ref} />);

// After
function Comp({ ref }) { return <div ref={ref} />; }
```

### Pattern 2: With useImperativeHandle
```javascript
// Before
const Comp = forwardRef((props, ref) => {
  useImperativeHandle(ref, () => ({ method() {} }));
  return <div />;
});

// After
function Comp({ ref }) {
  useImperativeHandle(ref, () => ({ method() {} }));
  return <div />;
}
```

### Pattern 3: TypeScript with Generics
```typescript
// Before
const Comp = forwardRef<HTMLDivElement, Props>((props, ref) => ...);

// After
function Comp({ ref, ...props }: Props & { ref?: Ref<HTMLDivElement> }) { ... }
```

For comprehensive forwardRef migration documentation, see: `research/react-19-comprehensive.md` lines 978-1033.

## Ref Cleanup Functions (New in React 19)

React 19 supports cleanup functions in ref callbacks:

```javascript
<div
  ref={(node) => {
    console.log('Connected:', node);

    return () => {
      console.log('Disconnected:', node);
    };
  }}
/>
```

**When Cleanup Runs:**
- Component unmounts
- Ref changes to different element

This works with both ref-as-prop and the old forwardRef pattern.
