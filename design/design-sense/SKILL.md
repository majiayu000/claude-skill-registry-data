---
name: design-sense
description: Compose interfaces that hold together — skeleton before aesthetics, one alignment per row, sizing by declaration. Use when building or reviewing any UI component, fixing "it looks off but I cannot say why", or adding an element to an existing layout.
---

# Design sense

Most UI that "looks off" is not ugly. It is **structurally inconsistent** — two
alignments in one row, two things that should match sized by different
mechanisms, a number column that shifts with its digit count. The viewer cannot
name it and reports a feeling. This skill is how to not create that feeling.

Every rule below came from a real defect. None is a preference.

---

## 1. The order of operations

Build in this order. Doing them out of order is how a layout ends up needing to
be rebuilt rather than adjusted.

1. **Skeleton.** Boxes, widths, alignment. No colour, no type, no borders. If
   it is wrong here, no amount of styling saves it — and styling makes the
   wrongness harder to see, because now there is something to look at.
2. **Rhythm.** One spacing scale. Every gap is a step on it.
3. **Hierarchy.** Size and weight decide what is read first. Still no colour.
4. **Theme.** Colour, borders, shadow — applied last, on top of a layout that
   already works in greyscale.

**The test:** turn the colour off. If you cannot tell what matters, the problem
is in step 3, and reaching for a brighter accent will not fix it.

---

## 2. Composition rules

### One alignment per row

A row that aligns its children to the bottom, containing a label aligned to the
centre, containing a note on its own baseline, is three alignments in one line.
Nobody can name it; everybody sees it.

Pick one — `items-center` for controls, `items-baseline` for text of different
sizes — and let every child inherit it. A child that needs to differ says so
explicitly (`self-center`), and that exception should be rare enough to notice.

**Failure seen:** a bid bar with the row at `items-end`, the label at
`items-center`, and the caption on neither.

### A child in a top-aligned row must declare itself

Add an element to a row aligned at the top and it will sit flush against the
top edge and clip. Nothing is wrong with the element; it never said where it
goes. `self-center` is not decoration — it is the element stating its place.

### Size siblings by the same mechanism

Two controls that should be the same height must be sized the same way. One
sized by padding and one by a minimum height can only ever *coincide* — and
they stop coinciding the moment either one's padding changes.

Declare it: both `h-12`. Matching by accident is not matching.

### Containers assign meaning

Anything inside a bordered, tinted, single-hover-target panel is read as part
of that panel's purpose. Put a view count inside a box holding a price and a
Buy button and people read it as something they are being charged for.

**Before adding an element, ask what its container already claims.** If the
answer is wrong, the element belongs outside the container, not restyled
within it.

### Width follows content, not availability

Two short fields stretched to full width because the row was there, while the
thing that belonged beside them sat alone underneath. A field's width should
suggest the length of what goes in it: a name is short, a description is long,
and a full-width name field silently promises otherwise.

### Labels vary; inputs must not

Labels wrap. A two-line label above an input pushes that input a line below its
neighbour, and the row breaks. Make each field a flex column with the input
pinned to the bottom (`h-full flex-col` + `mt-auto`), so every input in a row
sits on one line whatever its label does.

Do not solve it by shortening the label — the next long label reintroduces it.

### Numbers in a column are right-aligned and fixed-width

`0` and `1,240` starting at different left edges makes a column look broken
even when every figure is correct. Right-align, fix the width, use tabular
figures. This is the cheapest credibility in an interface that shows numbers.

---

## 3. Spacing

**One scale, no exceptions.** 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64. A gap that
is not on it is a gap somebody guessed.

**Space belongs to relationships, not elements.** Related things sit closer
than unrelated things — that proximity is the only grouping signal that works
without a border. If you are reaching for a divider, first check whether the
spacing already says it.

**Padding is symmetric unless asymmetry means something.** `pl-3 pr-2` is
almost always a mistake somebody stopped noticing.

**A sticky element changes the spacing of what it sits over.** A page ending in
generous bottom padding, under a sticky bar, under a footer, produces a dead
band nobody designed. When something sticks, the space beneath it is its
responsibility, not the page's.

---

## 4. Responsive

### Design the narrow case first

Not because mobile matters more, but because the narrow case forces the
priority question — what is this row FOR — and the answer improves the wide
case too.

### Dropping is a decision, and it is about width, not importance

On a 375px row, an avatar and a held-time clock cost ~163px, and the name
truncates to "Meridia…" to pay for it. The name is the row. Both get dropped.

State the trade in a comment where the drop happens: what was removed, what it
bought, why the remaining thing won. Otherwise somebody restores it in six
months and the name truncates again.

### Fold economy

Count what sits above the primary content on a phone. Six facts and two
progress bars above a leaderboard means the thing people came for starts below
the fold.

Rule: **one headline, one primary action, at most two supporting facts.**
Everything else folds behind a tap, or moves below the content.

### A breakpoint above the common laptop is effectively "off"

`hidden 2xl:block` (1536px) means most laptops never render it. Something built
and invisible is worse than something missing — it reads as built.

**Verify at the width people actually use**, not the width you have.

---

## 5. Mobile hard rules

- **Inputs at 16px** or iOS zooms on focus and never zooms back. Enforce it
  unlayered, and see §6.
- **Standalone tap targets ≥ 44px.** Links inside a sentence are exempt —
  boxing prose links breaks the paragraph.
- **Nothing scrolls horizontally.** Wide content (tables, tickers, code)
  scrolls inside its own container, never the page.
- **Sticky bottom bars pad with `env(safe-area-inset-bottom)`**, and the
  viewport must be set to `cover` or that inset is always zero.

---

## 6. The traps

**Layered `!important` beats unlayered `!important`.** In Tailwind v4, an
`!important` inside `@layer utilities` wins against an unlayered one. So a
theme override written as unlayered `!important` silently loses.

Use plain unlayered rules: unlayered beats layered regardless of specificity,
and needs no `!important` at all.

**Framework state loses to background re-renders.** A scroll-driven UI flag in
component state is reset by any router refresh or polling revalidation. Put the
flag on the document root and key the CSS off it — outside the framework,
nothing the framework does can undo it.

**Grepping rendered HTML for a label misses it.** React inserts comment nodes
between a literal and an interpolated value, so `held 3d` is `held <!-- -->3d`.
Match on a class or an attribute instead.

**Same number, different meaning by context.** "0 views" on a leaderboard row
reads as a verdict on the person; on their own profile it reads as the honest
state of a new page. Decide per context whether zero is information or an
accusation.

---

## 7. Review checklist

Run before calling a component done:

- [ ] Does it hold up in greyscale?
- [ ] One alignment per row, exceptions declared?
- [ ] Do siblings that match, match **by declaration**?
- [ ] Is every gap on the scale?
- [ ] Do numbers line up down their column?
- [ ] Does each element's container claim what the element means?
- [ ] Does it survive the longest realistic label, name and number?
- [ ] Checked at 375px, 768px, 1280px — and 1440px, not just your own screen?
- [ ] Does any tap target fall under 44px?
- [ ] Any horizontal scroll at 375px?

**And the one that catches most of it:** open the real page at the real width.
Verifying that the code renders is not verifying that a person can see it.

---

## Known limits

- **It is composition, not visual design.** Nothing here chooses a palette, a
  typeface, or a brand voice. A layout can pass every rule above and still look
  generic — structural consistency is the floor, not taste.
- **It cannot see the render.** Every rule is checkable by reading code except
  the one that matters most (open the real page at the real width). The
  checklist can be walked honestly and still miss what a screenshot would show
  in a second.
- **No accessibility coverage beyond tap targets.** Contrast ratios, focus
  order, screen-reader semantics, motion sensitivity and keyboard traps are out
  of scope — use the accessibility review path for those.
- **The numbers are conventions, not measurements.** 44px targets and the
  375/768/1280/1440 widths are defaults that held up in practice, not
  thresholds derived from this project's own analytics. A product whose real
  traffic sits elsewhere should use its real widths.
- **It assumes a spacing scale exists.** On a codebase with no scale, "every gap
  is a step on it" is advice about work that hasn't been done yet.
- **Silent on animation, and on data-dense surfaces** — tables, dashboards and
  charts have their own alignment economics that these rules only partly reach.
