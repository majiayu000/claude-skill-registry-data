---
name: ui-generate-code
description: Generate frontend code (HTML, CSS, React, Vue, Svelte, Tailwind, vanilla, etc.) from an existing UI spec — and only from a spec. The hard rule is no silent invention of design decisions. Use this skill whenever the user says "now write the code", "implement this spec", "generate the React component", or otherwise asks for an implementation of a UI that has been specced. Always run after ui-component-spec and ui-system. Refuse to proceed if a spec doesn't exist; instead, ask the user to run ui-brief, ui-blueprint, or ui-component-spec first, or document spec-gap assumptions explicitly before any code is written.
status: stable
---

# UI Generate Code

Generates frontend code from an existing spec. The job of this skill is **not** to design — it is to translate. Every line of generated code traces back to a specific spec decision. Where the spec is silent, the skill asks or logs an explicit assumption — never invents.

## When to use this skill

Use this skill when:
- A spec (`ui-component-spec` minimum, ideally with `ui-system`) has been approved and validated (ideally via `ui-spec-linter`) and the user wants the implementation.
- The user says "implement", "code this up", "build the component", "generate the React/Vue/HTML/etc. for this".

Do **not** use this skill when:
- No spec exists. Refuse and direct the user to `ui-brief` + `ui-blueprint` + `ui-component-spec`.
- The user wants quick exploratory code to play with before specing. That's legitimate, but it is not what this skill does — this skill produces spec-traceable production code, not sketches.

## Core principle

**This skill translates, it does not design.** If the spec doesn't say what color a button is, this skill does NOT pick a color. It either asks the user, or it logs `⚠️ ASSUMED: Used color.action.primary because spec said "primary action button" without specifying token.` Every silent invention is a vision-gap waiting to happen.

## The hard rules

These are non-negotiable. Violating them defeats the purpose of the kit.

1. **No silent design decisions.** Every choice not explicitly in the spec must be either (a) a question to the user or (b) a flagged assumption in the assumptions log.
2. **No invented values.** No hex codes, no pixel paddings, no font sizes, no animation durations that aren't in `ui-system` or the component spec. If you need a value the system doesn't have, ask.
3. **Every code section must trace to a spec section.** Inline comments map code → spec sections. Reviewers should be able to verify "the disabled state is implemented per `component-spec §4`" by reading the comments.
4. **All states from the component spec must be implemented.** If the spec lists 8 states, the code handles 8 states. If you skip one, you've broken the contract.
5. **Accessibility is not optional.** ARIA roles, keyboard handlers, focus management — all from the spec, all in the code.
6. **No new components except those in the spec.** If implementing a "primary CTA button" requires a sub-component, ask the user before introducing one. Don't sneak in a `Spinner` component without permission.

## Pre-flight check (mandatory)

Before writing any code, confirm:

1. **A component spec exists and is validated.** Read it. If it hasn't been run through `ui-spec-linter` yet, recommend doing so to catch gaps early. If no spec exists, refuse and ask the user to run `ui-component-spec`.
2. **A system spec exists** (or the user has confirmed it's not needed). If components reference tokens that aren't defined, the code will hardcode values — which violates rule 2.
3. **Framework / language target is known.** "React", "Vue", "vanilla HTML+CSS", "React with Tailwind", "Svelte" — the user must specify. Do not pick a default.
4. **Styling approach is known.** Tailwind utility classes? CSS modules? Styled-components? Inline styles? Plain CSS file? The user must specify.
5. **Component API style is known.** For React: controlled vs. uncontrolled? Hooks-only or class allowed? Function signature preferences?

If any of these is missing, ask. **Do not start writing code until all five are answered.**

## Workflow

### Step 1 — Read the spec end-to-end

Read every section. Note every concrete decision and every gap. A "gap" is anything the spec doesn't say that the code will need to know.

### Step 2 — List the gaps

Before writing a line of code, output a list of gaps:

```markdown
## Gaps in the spec — need answers before writing code
1. The spec says "border on focus" but doesn't specify width. Should I use `border-2` (2px) or `border-4` (4px)?
2. Animation duration on hover not specified. Use `motion.fast` (100ms)?
3. Click handler signature — does the parent expect `(value: string) => void` or `(event: ChangeEvent) => void`?

## Assumptions I'd make if you'd rather I just proceed
- ⚠️ Default focus border to 2px, since system §6 has no thicker option.
- ⚠️ Use `motion.fast` for hover, longest transitions.
- ⚠️ Standard React onChange signature `(event) => void`.
```

The user picks: answer the questions, or accept the assumptions. Either way, the gaps are no longer silent.

### Step 3 — Write the code

Write idiomatic code in the chosen framework. Each significant block has a comment mapping it to the spec section it implements:

```jsx
// component-spec §3 — Anatomy: Label + InputContainer + HelperText
return (
  <div className="...">
    <label htmlFor={id} className="...">{label}</label>
    {/* component-spec §4 — InputContainer holds the field and the visibility toggle */}
    <div className="...">
      <input
        id={id}
        type={visible ? "text" : "password"}
        // component-spec §4 — Disabled state per spec
        disabled={disabled}
        // component-spec §7 — error linkage
        aria-describedby={error ? `${id}-error` : `${id}-helper`}
        aria-invalid={!!error}
        ...
      />
      ...
    </div>
    ...
  </div>
);
```

### Step 4 — Implement every state

Walk the state matrix from the component spec. For each state, ensure the code has a path. Use class-name patterns, conditional renders, or CSS pseudo-classes per the styling approach.

### Step 5 — Implement accessibility

From the spec's accessibility section, implement every requirement: semantic element, label association, ARIA attributes, keyboard handlers, focus management. If the spec says "Escape closes the popover and returns focus to the trigger", the code must include both behaviors.

### Step 6 — Output the package

The output of this skill is a multi-file package:

1. **The code** — the component file(s) themselves.
2. **`assumptions.md`** — every assumption made, flagged with ⚠️.
3. **`spec-trace.md`** — a table mapping spec sections to code lines/blocks.
4. **`questions.md`** (optional) — anything you want the user to confirm, even after writing.

If the environment supports files, save these alongside the code. If not, deliver them inline as fenced sections.

### Step 7 — Hand off to acceptance

Tell the user: "Run this through `ui-acceptance` to verify. If discrepancies, run `ui-redline`." Do not declare done unilaterally.

## Output template

Code block first, then the supporting documents. Always include all four sections below.

```markdown
# Generated implementation: <component name>

**Framework:** <React | Vue | Svelte | vanilla>
**Styling:** <Tailwind | CSS modules | etc.>
**Source spec:** component-<slug>
**System spec:** system-<slug>

## 1. Code

<file: ComponentName.jsx (or .vue, .svelte, .html, etc.)>
<file: ComponentName.module.css if applicable>
<file: ComponentName.test.jsx if requested>

## 2. Assumptions log

| # | Assumption | Spec section that was silent | Severity if wrong |
|---|---|---|---|
| 1 | ⚠️ Used `motion.fast` for hover transition | component §5 didn't specify duration | minor |
| 2 | ⚠️ Default React controlled-component pattern | component didn't specify | minor (changes API surface) |
| 3 | ⚠️ Wrapping div uses `display: flex` | component §2 anatomy is hierarchical, no layout specified | minor |

If any of these is wrong, ask and I'll regenerate.

## 3. Spec → code trace

| Spec section | Implemented at |
|---|---|
| component §2 Anatomy | lines 12–28 of ComponentName.jsx |
| component §3 Props | TypeScript interface lines 4–10 |
| component §4 State: Default | base classes lines 14–17 |
| component §4 State: Hover | `:hover` modifier line 14 |
| component §4 State: Focus-visible | `:focus-visible` modifier line 15 |
| component §4 State: Disabled | conditional `disabled-classes` line 18 |
| component §4 State: Loading | conditional render lines 22–24 |
| component §4 State: Error | conditional render lines 25–27 |
| component §5 Behavior: Escape clears | onKeyDown handler lines 38–42 |
| component §7 a11y: label association | `htmlFor`/`id` pair line 13, 16 |
| component §7 a11y: error association | `aria-describedby` line 19 |
| component §7 a11y: required | `aria-required` line 20 |

## 4. What's NOT implemented

- <Anything intentionally skipped — e.g. "Animation on first mount: spec didn't say.">
- <Anything blocked on a gap that wasn't resolved.>
```

## Concrete example — generating a primary CTA button (React + Tailwind)

**Pre-flight answered:**
- Framework: React + TypeScript
- Styling: Tailwind, with system tokens as Tailwind config extensions
- API style: controlled, hooks-only

**Spec gaps surfaced before writing:**
1. Spec says "transitions on hover" but no duration — assume `motion.fast` = 100ms.
2. Spec says "loading state replaces icon with spinner" but doesn't specify which spinner. Use a Tailwind-friendly inline SVG spinner.

**User says proceed with assumptions.**

```tsx
// component-spec §1 — Primary CTA button (destructive variant excluded)
// component-spec §3 — Props
interface PrimaryCtaButtonProps {
  children: React.ReactNode;
  onClick: () => void;
  disabled?: boolean;
  loading?: boolean;
  type?: 'button' | 'submit';
  ariaLabel?: string;
}

export function PrimaryCtaButton({
  children,
  onClick,
  disabled = false,
  loading = false,
  type = 'button',
  ariaLabel,
}: PrimaryCtaButtonProps) {
  return (
    <button
      type={type}
      onClick={onClick}
      // component-spec §4 — Disabled state per spec; native `disabled` blocks events
      disabled={disabled || loading}
      // component-spec §7 — a11y: aria-busy reflects loading
      aria-busy={loading}
      aria-label={ariaLabel}
      className={[
        // component-spec §4 — Default state
        'inline-flex items-center justify-center gap-2',
        'px-4 py-2 rounded-md',
        'bg-action-primary text-text-inverse',
        'text-body font-semibold',
        // component-spec §4 — Hover state (motion.fast = 100ms — ⚠️ ASSUMED)
        'transition-colors duration-100',
        'hover:bg-action-primary-hover',
        // component-spec §4 — Focus-visible state
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-focus-ring focus-visible:ring-offset-2',
        // component-spec §4 — Active state
        'active:bg-action-primary-active',
        // component-spec §4 — Disabled state
        'disabled:bg-text-disabled disabled:cursor-not-allowed',
      ].join(' ')}
    >
      {loading ? (
        // component-spec §4 — Loading state replaces label-area icon with spinner
        <Spinner />  // ⚠️ ASSUMED: inline Spinner sub-component, not in spec
      ) : null}
      <span className={loading ? 'opacity-50' : ''}>{children}</span>
    </button>
  );
}
```

(Spinner sub-component would also need approval — flagged in assumptions.)

## Rules that prevent hallucinated code

1. **No imports the user didn't approve.** If you need a date library or icon library, ask.
2. **No CSS values not in the system.** Every padding, color, font-size resolves to a system token reference.
3. **No "TODO" comments without a corresponding entry in `assumptions.md` or `questions.md`.**
4. **No code that does more than the spec says.** If the spec says "button with onClick", do not add `onDoubleClick`, `onContextMenu`, etc. unless asked.
5. **No silent dependency on framework defaults.** If React's strict mode, suspense, or other implicit behavior is load-bearing, comment it.
6. **No styling approach mixing.** If Tailwind was chosen, don't sneak in a `style={...}` prop or a CSS-in-JS block.

## Acceptance criteria for this skill's output

Code produced by this skill is acceptable only if every one of these is true:

- [ ] A component spec was read before writing.
- [ ] Pre-flight questions (framework, styling, API style) were answered.
- [ ] All gaps in the spec were either answered by the user or flagged in `assumptions.md`.
- [ ] Every state in the component spec's state matrix has a code path.
- [ ] Every accessibility requirement in the component spec is implemented.
- [ ] Every keyboard interaction in the component spec is wired.
- [ ] Every styling value resolves to a system token (or is flagged as a gap).
- [ ] `spec-trace.md` (or the inline trace table) maps every spec section to specific code lines.
- [ ] No imports / dependencies were introduced without user approval.
- [ ] No "TODO" appears without a matching question or assumption entry.

If any check fails, revise before delivering.
