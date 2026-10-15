---
name: stable-width-button
description: Prevent width jitter when content changes dynamically, by reserving the width of every content the element can hold. Use when building buttons or tabs whose label switches between known values, when a numeric readout (slider value, counter, timer, percentage) shifts its neighbours as it changes, or when layout shift occurs on state-driven content change.
---

# Stable-Width Button

A CSS technique for keeping a button's inline size stable when its visible content changes between a known set of values (e.g. "Save" / "Saving..." / "Saved").

## Problem

When a button's text changes on interaction, its intrinsic width changes too. This causes the button — and everything around it — to shift, producing layout jitter.

Common workarounds and their downsides:

| Approach                                      | Downside                                           |
| --------------------------------------------- | -------------------------------------------------- |
| Fixed `width`                                 | Breaks when translations or content vary in length |
| `min-width` guess                             | Under- or over-sized; fragile                      |
| CSS `text-indent` / invisible pseudo-elements | Hard to maintain; content isn't in the DOM         |

## Pattern

Render **all possible contents** inside the button. Only the active content is visible; the rest occupy zero height but retain their natural width, forcing the button to adopt the widest variant's inline size.

```tsx
export const Button: FC<
  ButtonHTMLAttributes<HTMLButtonElement> & {
    allPossibleContents?: ReactNode[];
  }
> = ({ children, allPossibleContents, ...props }) => {
  return (
    <button {...props}>
      {children}
      {allPossibleContents && allPossibleContents.length > 0 && (
        <div className="invisible flex h-0 flex-col overflow-clip leading-0">
          {allPossibleContents.map((content, index) => <div key={index}>{content}</div>)}
        </div>
      )}
    </button>
  );
};
```

## How It Works

| Class           | Purpose                                                                     |
| --------------- | --------------------------------------------------------------------------- |
| `h-0`           | Container contributes zero height — button height is unaffected             |
| `flex-col`      | Stacks all variants vertically so each gets its own line to determine width |
| `invisible`     | Hides content visually but preserves layout contribution                    |
| `overflow-clip` | Prevents hidden content from being scrollable or focusable                  |
| `leading-0`     | Eliminates line-height so the zero-height container doesn't leak space      |

The hidden container participates in the button's inline-size calculation. The button's width resolves to `max(active content width, widest hidden variant width)`, keeping it stable across state changes.

## Why `invisible` Instead of `hidden` or `display: none`

`display: none` and the `hidden` attribute remove the element from layout entirely — no width contribution. `visibility: hidden` (`invisible` in Tailwind) keeps the element in flow and preserves its box dimensions while making it non-interactive and invisible. This is exactly what we need: width participation without visual presence.

## Usage

Pass all possible label values via `allPossibleContents`:

```tsx
<Button allPossibleContents={[t("saving"), t("saved")]}>
  {isLoading ? t("saving") : t("saved")}
</Button>;
```

The current content naturally appears via `children`; the `allPossibleContents` array only needs to include **all variants** (including the current one is harmless — it just adds a redundant width contributor).

## When to Use

- Buttons that toggle between known states ("Edit" / "Editing" / "Done")
- Tab triggers where switching labels causes container reflow
- Any inline element with a finite set of content variants that should not cause width change

## When NOT to Use

- Content is user-generated or unbounded (use `min-width` or fixed width instead)
- The button already has `width: 100%` / fills its container (width is externally determined)
- Only one possible content value (no jitter risk)

## Generalization

This pattern is not limited to buttons. It applies to any element where:

1. The content switches between a known finite set of values.
2. The element's inline size is intrinsic (not externally constrained).
3. Width stability matters for the surrounding layout.

Tabs, badges, status indicators, and inline labels are all candidates.

## Slot Reservation: Content With Too Many Values To Enumerate

`allPossibleContents` stops working when the value set is large but structured — a slider readout (`0`–`140`), a counter, `mm:ss`, a percentage. Enumerating 141 variants to reserve three digits is absurd, and `10 × 10` for two digits is already silly.

Decompose the content into **independent positions** instead, and reserve each position separately: `[label] + [0-9] + [0-9]`. Ten alternatives per digit slot cover every number those slots can spell — two digits cost 10 hidden nodes, not 100.

| Axis                         | Behaviour                     |
| ---------------------------- | ----------------------------- |
| Alternatives within a slot   | `max` — a zero-height column  |
| Slots within the reservation | `sum` — a flex row of columns |

```tsx
const DIGITS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"];

/** Each `slots` entry is a column of alternatives contributing its widest; the row sums the slots. */
const ReservedWidth = ({ slots }: { slots: string[][]; }) => (
  <span aria-hidden className="invisible flex h-0 flex-row overflow-clip leading-0">
    {slots.map((alternatives, index) => (
      <span className="flex flex-col" key={`${index}-${alternatives[0]}`}>
        {alternatives.map((alternative) => <span key={alternative}>{alternative}</span>)}
      </span>
    ))}
  </span>
);

/** `gap 0` … `gap 140` — the track never moves, and the label column never resizes. */
const Knob = ({ label, value, max, onChange }: KnobProps) => (
  <label className="col-span-2 grid grid-cols-subgrid items-center">
    <span className="text-right">
      {label} {value}
      <ReservedWidth
        slots={[
          [`${label}\u00a0`],
          ...Array.from({ length: String(max).length }, () => DIGITS),
        ]}
      />
    </span>
    <input
      type="range"
      min={0}
      max={max}
      value={value}
      onChange={(event) => onChange(Number(event.target.value))}
    />
  </label>
);
```

Two details are load-bearing:

- **The reservation must be a block-level sibling of the visible content, not an inline one.** On its own line it makes the container resolve to `max(visible, reserved)`; drop it into the same line box — or make the cell itself a flex row — and the two widths _sum_, padding the cell by its own reserved width forever.
- **Trailing spaces need `\u00a0`.** A plain trailing space collapses at the end of a line box and reserves nothing, so a slot written as `` `${label} ` `` silently loses the gap between the word and the number.

Because each row now reserves its own worst case, a shared grid column (`grid-cols-subgrid`) stays put too: the column's max comes from fixed row widths rather than from whichever row currently happens to hold the longest value.

### Verify It, Don't Eyeball It

A few pixels of jitter are easy to miss and easy to reintroduce. Measure the neighbour that would move, at both ends of the value range:

```js
const trackLeft = () =>
  Math.round(document.querySelector("input[type=range]").getBoundingClientRect().left);
// Set the value to min, mid, and max: trackLeft() must not change, and the row's
// height must match what it was before the reservation was added.
```
