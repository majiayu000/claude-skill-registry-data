---
name: component-design-systems
description: "A design system has three token layers, and conflating them is what makes systems"
---

# Component Design Systems (Verbose)

## Core Patterns

### Token Layers

A design system has three token layers, and conflating them is what makes systems
impossible to retheme.

```css
/* 1. Primitive — raw values, no meaning. Never referenced by components. */
:root {
  --red-600: #b42318;
  --gray-100: #f2f4f7;
  --size-3: 0.75rem;
}

/* 2. Semantic — meaning, no context. This is what components consume. */
:root {
  --color-bg-danger: var(--red-600);
  --color-bg-subtle: var(--gray-100);
  --space-inline-sm: var(--size-3);
}

/* 3. Component — only when a component genuinely deviates. */
:root {
  --button-height-sm: 2rem;
}
```

Dark mode then costs one block, because only layer 2 rebinds:

```css
[data-theme="dark"] {
  --color-bg-subtle: var(--gray-800);
}
```

The non-obvious part: **tokens are the durable contract, component APIs are not.**
Over five years you will migrate class components to hooks, CSS-in-JS to CSS
modules, and possibly frameworks entirely. `--color-bg-danger` survives every one
of those, and it is simultaneously the interface to design tools, iOS, Android,
and email templates. So govern token names strictly — renaming one is a breaking
change with a deprecation window — and let component internals churn freely.

### Compound Components

Prop-driven components fail at a predictable point: when a consumer needs a layout
you did not anticipate.

```tsx
const SelectCtx = createContext<Ctx | null>(null);

function useSelectCtx() {
  const ctx = useContext(SelectCtx);
  if (!ctx) throw new Error("Select.* must be rendered inside <Select>");
  return ctx;
}

export function Select({ value, onChange, children }: SelectProps) {
  const [open, setOpen] = useState(false);
  const ctx = useMemo(() => ({ value, onChange, open, setOpen }), [value, onChange, open]);
  return <SelectCtx.Provider value={ctx}>{children}</SelectCtx.Provider>;
}

Select.Trigger = function Trigger({ children }: { children: ReactNode }) {
  const { open, setOpen } = useSelectCtx();
  return <button aria-expanded={open} onClick={() => setOpen(!open)}>{children}</button>;
};

Select.Option = function Option({ value, children }: OptionProps) {
  const { onChange, setOpen } = useSelectCtx();
  return (
    <li role="option" onClick={() => { onChange(value); setOpen(false); }}>
      {children}
    </li>
  );
};
```

Throwing from `useSelectCtx` turns a silent misuse into an immediate, obvious error.

| | Prop-driven | Compound |
|---|---|---|
| Novel layout | Needs a new `renderX` prop | Consumer just rearranges |
| API surface | Grows with every request | Stable |
| Discoverability | High — autocomplete lists props | Lower; needs docs |
| Best for | Closed sets (Button, Badge) | Slotted UI (Select, Dialog, Card) |

Use props for leaf components with a small fixed shape. Reach for composition the
moment a component has *slots*.

### Polymorphic and Forwarding Components

```tsx
type ButtonProps<C extends ElementType> = {
  as?: C;
  variant?: "primary" | "ghost" | "danger";
} & Omit<ComponentPropsWithoutRef<C>, "as">;

export const Button = forwardRef(function Button<C extends ElementType = "button">(
  { as, variant = "primary", className, ...rest }: ButtonProps<C>,
  ref: ComponentPropsWithRef<C>["ref"]
) {
  const Tag = as ?? "button";
  return <Tag ref={ref} className={cx(styles.base, styles[variant], className)} {...rest} />;
});
```

The `as` prop lets a link look like a button without duplicating styles — and
without shipping a `<button onClick={navigate}>` that breaks middle-click,
ctrl-click, and screen-reader link navigation.

### Variants as Data

```ts
export const badge = cva("inline-flex items-center rounded-full font-medium", {
  variants: {
    tone: {
      neutral: "bg-[--color-bg-subtle] text-[--color-fg-default]",
      danger:  "bg-[--color-bg-danger-subtle] text-[--color-fg-danger]",
    },
    size: { sm: "h-5 px-2 text-xs", md: "h-6 px-2.5 text-sm" },
  },
  compoundVariants: [{ tone: "danger", size: "sm", class: "font-semibold" }],
  defaultVariants: { tone: "neutral", size: "md" },
});
```

Because the variant map is a plain object, you can enumerate it in a story and
snapshot every combination. That catches the "danger + small looks broken" case
that no unit test would think to assert.

### Accessibility as a Library Guarantee

The system's value proposition is that accessibility is solved *once*. Concretely:

- Focus is visible via `:focus-visible`; never removed with a bare `outline: none`.
- Interactive targets meet WCAG 2.2 target size (24×24 CSS px minimum).
- Icon-only controls require an `aria-label` — make it a required prop in TypeScript.
- Text/background token pairs are contrast-checked in CI, so a token change cannot
  silently drop below 4.5:1.

For anything with a focus-management contract — dialogs, menus, comboboxes,
tooltips — wrap a headless primitive rather than hand-rolling. Roving tabindex,
typeahead, scroll locking, and returning focus to the trigger are each easy to get
90% right and very visible when wrong.

## Common Anti-Patterns

❌ **Components reading primitive tokens directly** — `background: var(--red-600)`
means dark mode requires touching every component.
✅ Components read semantic tokens; only semantic tokens read primitives.

❌ **Boolean props multiplying** — `isCompact`, `isInline`, `hasIcon`,
`isDestructive` create 16 combinations, most untested and several nonsensical.
✅ One enum per axis, with invalid combinations unrepresentable.

❌ **Not forwarding `ref` and `className`** — the component cannot be a popover
trigger, cannot be measured, cannot be nudged 4px by a consumer.
✅ `forwardRef` plus a `{...rest}` spread and merged `className` everywhere.

❌ **Hard-coding external spacing** — `margin-bottom: 16px` on a Card makes it
wrong in every layout that isn't the one you designed against.
✅ Components own internal padding; the parent owns spacing between children (`gap`).

❌ **A "Button" that renders `<div onClick>`** — no keyboard activation, no role,
no focusability.
✅ Real semantic elements, with `as` for the link/button swap.

❌ **Docs written after adoption** — the undocumented loading state gets
reimplemented in four product teams, differently.
✅ A story per state, shipped in the same PR as the component.

❌ **Accepting a one-off variant to unblock a team** — `variant="specialDashboard"`
is permanent and nobody will ever dare delete it.
✅ Give them an escape hatch (`className`, composition); promote to a variant only
after the pattern appears in three places.

## Component Design System Checklist

- [ ] Primitive / semantic / component token layers separated
- [ ] Components reference only semantic tokens
- [ ] Dark theme achieved by rebinding semantic tokens alone
- [ ] Token renames go through a deprecation window
- [ ] Every component forwards `ref` and merges `className`
- [ ] Rest props spread onto the underlying element
- [ ] Variants expressed as a data map, not JSX ternaries
- [ ] Every variant × size combination rendered in a story
- [ ] Composition used wherever consumers need layout control
- [ ] Context hooks throw when used outside their provider
- [ ] Interactive components built on a headless primitive or audited for keyboard nav
- [ ] `:focus-visible` styling present; no bare `outline: none`
- [ ] Icon-only controls require an accessible name at the type level
- [ ] Token contrast pairs verified in CI
- [ ] Components carry no external margin
- [ ] Each component documents its states plus one anti-example
