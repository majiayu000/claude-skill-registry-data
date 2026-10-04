---
name: ui-atom
description: Atomic-design guidance for UI Atoms — the smallest single-purpose building blocks (buttons, inputs, icons, labels). Use when authoring or reviewing components under ui/atoms, components/atoms, or when deciding whether a component belongs at the atom level.
when_to_use: Creating or reviewing Atom-level components; deciding whether a component is an atom vs. molecule; enforcing single-responsibility and design-token consumption in primitives.
paths:
  - "**/ui/atoms/**/*.{jsx,tsx,vue,js,ts}"
  - "**/components/atoms/**/*"
  - "**/atoms/**/*"
---

# Atom

## What is an Atom?

Atoms are the fundamental building blocks of UI—single-purpose components that do one thing well (button, input, icon, label). They're the LEGO bricks of your interface, highly reusable and composable into complex UIs.

## Key Principles

1. **Single Responsibility**: Each atom does ONE thing. A Button clicks, an Input captures text, an Icon displays a symbol. Never combine purposes.

2. **Framework Agnostic Props**: Accept simple, primitive props (strings, numbers, booleans, callbacks). Avoid framework-specific patterns in the interface.

3. **Design Token Integration**: Use design tokens (colors, spacing, typography) from theme—atoms enforce visual consistency across the entire application.

## Best Practices

✅ **DO**:
- Keep atoms under 50 lines of code
- Accept `className` or `style` for customization
- Include accessibility attributes (aria-label, role)
- Make atoms stateless when possible—receive data via props
- Export with default and named exports for flexibility

❌ **DON'T**:
- Fetch data inside atoms
- Include business logic
- Hardcode colors/spacing—use theme tokens
- Create atoms that render other atoms (that's a molecule)
- Manage complex internal state

## Code Patterns

### Recommended

```jsx
// Button.jsx - Single purpose atom
const Button = ({ 
  label, 
  onClick, 
  variant = 'primary',
  disabled = false,
  ariaLabel 
}) => (
  <button
    className={`btn btn--${variant}`}
    onClick={onClick}
    disabled={disabled}
    aria-label={ariaLabel || label}
  >
    {label}
  </button>
);
```

### Avoid

```jsx
// ❌ WRONG - Atom doing too much
const Button = ({ onClick }) => {
  const [loading, setLoading] = useState(false);
  const handleClick = async () => {
    setLoading(true);
    await fetch('/api/action'); // Don't fetch in atoms!
    setLoading(false);
  };
  return <button onClick={handleClick}>Submit</button>;
};

// ✅ CORRECT - Parent handles logic, atom stays pure
const Button = ({ label, onClick, loading }) => (
  <button onClick={onClick} disabled={loading}>
    {loading ? 'Loading...' : label}
  </button>
);
```

## Related Terminologies

- **Molecule** (UI) - Composed of multiple atoms working together
- **Component** (UI) - Generic term; atoms are a type of component
- **Props** (UI) - How atoms receive data
- **Theme** (UI) - Provides design tokens atoms consume

## Quality Gates

- [ ] Single responsibility maintained
- [ ] Props are simple primitives or callbacks
- [ ] No data fetching or business logic
- [ ] Accessibility attributes included
- [ ] Uses design tokens from theme

**Source**: `/docs/ui/atom.md`
