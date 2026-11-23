---
name: charles-design-tips
description: "20 practical design tips as one procedure for building or reviewing a screen: alignment, weight and line height, baselines, blue-tinted grays, text on color, one hue per color, dark-mode colors, layered shadows, padding, heading and stacked-text spacing, Delete away from Save, labels above fields, right-aligned table numbers, sentence case, button labels, empty states and landing-page CTAs. Each tip has its numbers, its reason and a check, and a review mode returns a findings table. Use when building, styling or reviewing any screen, form, table, dialog, empty state or landing page, or when a UI looks off or amateur. Triggers on: button text size, button height, line height, font weight, centered text, baseline, gray, grey, shadows, text on color, hue, dark mode colors, padding, spacing, stacked text, delete button, placeholder, form labels, table numbers, sentence case, title case, Submit button, empty state, CTA, landing page, make my UI look designed, review my screen."
---

# Design tips

From Charles Liu's "20 Practical Design Tips" reel. Twelve of the tips come from Dan Liu's threads "10 practical tips for improving your text layout" and "10 practical tips for choosing colors", and eight from Emil Kowalski's design rules (aiforui.dev).

Twenty small decisions separate a screen that looks designed from one that looks assembled: how text aligns, how heavy it is and how tall its lines are, which grays, colors and shadows sit around it, how much room each box gives its words, and what the words say. Each one is easy to miss, so walk all twenty on every screen you build or review. They're defaults: when you break one on purpose, say which one and why. Motion and interaction states aren't covered here.

## Run it

1. **Match the stack.** Find how the project styles things (Tailwind, CSS variables, CSS Modules, a component library's theme) and make every fix there. When the project has tokens of a kind (colors, line heights, shadows, spacing), every fix of that kind changes or adds a token; use one-off values only for kinds it has no tokens for. Why: a token fix lands on every screen at once, and a one-off value is the next screen's bug.
2. **Take stock** before changing anything: every text style (size, weight, line height, alignment), every gray and brand color, every box with text in it (buttons, fields, toasts, chips), every big text with a short line under it, every heading, every row that holds a destructive action, and every form, table, empty state and landing page. Each tip below opens with what it applies to; this list decides which tips run.
3. **Walk the six areas in order:** type, spacing and layout, color, components and forms, copy, states and pages. Type goes first because the spacing tips measure from it: a button's height from its label, a stack's gap from a font size. Check every item from step 2 against every tip that applies to it.
4. **Measure, never eyeball.** Read rendered values in px (DevTools, or the code and its theme) and colors in hex and OKLCH. In a code-only review, take anything the code doesn't set from the browser's default styles, and say so in the finding. Why: "half the height" and "slightly blue" are exactly what the eye gets wrong at a glance.
5. **Verify** with the checks at the end.

**Reviewing instead of building?** Change nothing. Open the report with the stock list from step 2, grouped the way step 2 names things. Then write one table row per finding; when one value breaks two tips, one row names both:

| Severity | Tip | Where | Before | After |
| --- | --- | --- | --- | --- |
| broken | 5 Keep Delete far from Save | `EditProject.tsx:48` | Delete sits between Cancel and Save | Delete first in the footer with `margin-right: auto`, alone at the far left |
| polish | 2, 13 Button padding | `button.css:12` | `padding: 24px 22px`, label fills 30% | `padding: 10px 20px`, label fills 51% |

Severity is **broken** (someone can hit the wrong action, lose track of what they're typing, or get stuck), **friction** (slower to read, scan or decide than it needs to be) or **polish** (looks off, slows no one). Defaults: broken for 5, 11 and 19, for 9 and 16 when text falls under 4.5:1, and for 14 when the button pays, sends or deletes; friction for 1, 3, 15, 17, 20 and the other 14s; polish for 2, 4, 6, 7, 8, 10, 12, 13, 18 and the other 9s and 16s. Where is the file and line, or the screen and element; for a browser default, the line of the element that gets it. Before and After are the current and the fixed value in the project's own syntax. Sort by severity, then by tip number. Problems no tip covers go in a list after the table.

## Type

### 1. Don't center long paragraphs. Left-align them

Left-align any text that runs past two lines. Center only headings and text of two lines or fewer, and never center a heading over left-aligned text: a heading takes the alignment of the text it introduces. When unsure, left-align.

**Why:** a centered paragraph starts every line somewhere new, so the eye hunts for each start. A left edge is one straight line to come back to, and a centered heading over it puts two alignments in one block.

**Check:** every block of three or more lines is `text-align: left` (`start` in right-to-left languages), and every heading matches the text under it.

### 3. Keep body text regular

Body text (paragraphs, descriptions, helper text, table cells) is weight 400. Semibold and bold (600–700) are for titles and headings, for labels that name things (field labels, table headers), and for at most one value per block, the one that matters most, like a price or a total. Never bold a whole paragraph.

**Why:** if everything's bold, nothing stands out. Weight only works as contrast, and regular body text is what lets the title read first.

**Check:** no body, description, helper-text or cell style is above 400, and no block bolds more than one value.

### 6. Headlines need a tighter line height than body text

Headings and display text (anything set larger than the body to be read at a glance, like a big stat) take a line height of 1.1–1.3. Body text and small labels take 1.4–1.5, and text inside buttons and fields takes 1.4 (tip 2). Among headings, the bigger the text, the tighter: the largest gets 1.1 and each smaller level steps toward 1.3. A heading never inherits the body's line height.

**Why:** line height is a multiple of the font size, so the space between lines grows with the text. A 50px headline at the body's 1.5 sets its lines 75px apart, 25px more than the type is tall, and its two lines read as two headlines; at 1.1 they're 55px apart and read as one. Small body text needs the extra air for the eye to find the next line.

**Check:** line-height ÷ font-size for every style: headings and display text 1.1–1.3, and never looser than a smaller heading; body text and labels 1.4–1.5; control text 1.4.

### 10. Align mixed text sizes on the baseline, not the center

When text of different sizes shares a line (a price and "/ month", a title and its date, a number and its unit), align it on the baseline: `align-items: baseline` (or `last baseline`) in flex and grid, never `center`. Everything else in a row centers: text beside an icon, avatar or toggle centers on it, boxes side by side (a field and its icon, buttons of different sizes) center on each other, and text inside a shape (a button, a badge) centers in the shape.

**Why:** people read along the line the letters sit on. Centered on each other, two sizes sit on different lines and the small one looks like it slipped, like a "/ month" floating at the middle of a big $24.

**Check:** every row with two or more sizes of bare text uses baseline alignment, and a rule drawn under the larger text's letters touches the bottom of the smaller text's.

## Spacing and layout

### 2. Make your button text about half the button's height

A button's label or a text field's text, set at a line height of 1.4, fills half the control's height: height = 2 × 1.4 × font size. A 15px label has a 21px line and sits in a 42px button, 10–11px of padding top and bottom. So `padding: 24px 22px` (a 69px button, the label filling 30% of it) becomes `10px 20px` (41px, 51%). Side padding comes from tip 13. On touch screens, when this makes a control shorter than 44px, keep its size and extend its hit area to 44px with a pseudo-element.

**Why:** a fat button spends most of its height on padding and looks clumsy, and a tight one crowds its label. Half grows with the type, so every size looks balanced.

**Check:** font size × 1.4 ÷ the control's rendered height (border included) is between 0.4 and 0.6 for every button and field.

### 13. Use more padding on the sides than on the top

Buttons, fields, toasts, badges, chips, tabs and menu items get twice as much padding at each side as at the top and bottom: `padding: 12px` becomes `12px 24px`. Cards, panels, banners and table cells never have less at the sides than at the top. On a button with a leading icon, the icon side gets 2–3px less, so it looks even.

**Why:** most letters don't fill their line, and line height adds air above and below them, so equal padding already looks taller than it is and the sides look pinched. Twice as much at the sides looks even.

**Check:** every button, field, toast, badge, chip, tab and menu item has side padding 2× its top and bottom (2–3px less on a leading icon's side), and no other box has less at the sides than at the top.

### 15. Give headings more space above them than below

Every heading that introduces content under it (a page, section, card or dialog heading; not a table header) sits much closer to that content than to whatever comes before it: 48px above and 8px below by default (`margin: 24px 0` becomes `48px 0 8px`), and never less than twice as much above as below. Zero the top margin of the element after the heading (`h2 + p { margin-top: 0 }`), or the larger of the two margins wins and the 8px never shows. A heading at the top of its container takes the container's padding as its space above.

**Why:** distance reads as relationship before any word does. A heading halfway between two paragraphs belongs to neither, so readers can't tell which one it names.

**Check:** for every such heading, the rendered space above (after margins collapse) is at least 2× the rendered space below.

### 18. When you stack text, space it by the smaller text's height

When a big text sits over a short line that belongs to it (a number and its label, a card title and its one-line subtitle), the gap between them is the smaller text's font size: a 17px label sits 17px under its 38px number (`.label { margin-top: 17px }`). When the two are close in size (the larger less than 1.25× the smaller, like 16px over 14px), lay them out as lines of one block instead: both at the larger text's line height, with no gap. A heading over body text follows tip 15 instead.

**Why:** with no gap, the small text reads jammed against the big one, and a gap measured in its own size scales with what it labels. Two texts of nearly one size read as one block, so they space like its lines.

**Check:** the gap inside each stacked pair equals the smaller font size, or is zero with both at the larger line height when they're close in size.

### 5. Keep Delete far away from the Save button

A destructive action (Delete, Remove, Discard, Revoke, Leave) never sits beside the button that saves or confirms. In a footer it goes to the opposite end: put Delete first in the markup and give it `margin-right: auto` (`margin-inline-end: auto`), so Cancel and Save sit together at the other end. Never move it with `order`, which breaks the tab order, and never style it as the primary button. The exception is a confirmation whose confirm is the destructive action ("Delete project?"): there Cancel and Delete sit together, and Cancel takes the default focus.

**Why:** things side by side read as equals, and a hand aiming for Save sometimes lands on its neighbor. When the neighbor is Delete, that miss destroys work.

**Check:** in every footer, toolbar and row with a save or confirm button, the destructive action sits at the opposite end, with whitespace between them.

## Color

### 4. Pure gray can look dull, so tint it slightly blue

Never ship pure gray (red, green and blue equal) for backgrounds, borders, text or icons, from the lightest surface to the darkest text: pure black text becomes a near-black tinted the same way, and only pure white stays as it is. Shift each gray slightly toward blue: Dan Liu's example takes #d1d1d1 to #d1d3d5 (red stays, green +2, blue +4). Make the shift in the gray tokens, so the whole scale moves at once. Grays already tinted on purpose toward a warm brand stay as they are, and one interface never mixes warm and cool grays.

**Why:** next to colored UI, pure gray looks flat and a little yellowed. A hint of blue reads cleaner.

**Check:** no gray has red, green and blue equal, and in a cool palette every gray's highest channel is blue and its lowest is red.

### 9. On colored backgrounds, tint your text instead of using black

On a colored background, never use black or gray text. If white text reaches 4.5:1 on the color, use white. If it doesn't, use a dark shade from the background's own color scale: amber-800 (#92400e) on amber-100 (#fef3c7) is 6.4:1. Icons in the same block take the text's color.

**Why:** black on a color looks dirty, mixing with the background into a muddy tone. A shade of the same color reads as part of the surface and keeps the contrast.

**Check:** every text and icon on a colored fill is white or a darker shade from the fill's own scale, at 4.5:1 or more for text and 3:1 for icons.

### 12. Keep the same hue across every shade of a color

Shades of one color (a 50–950 scale, a color and its hover and pressed states, a chart that draws its series in shades of one color) share one hue; only lightness and saturation change. A chart whose blues are hsl(222 76% 42%), hsl(196 80% 56%) and hsl(252 86% 78%) has drifted to cyan and violet: give all three hue 222. A chart whose series must be told apart by color uses distinct hues on purpose; that's several colors, not shades of one, and this tip doesn't apply.

It's not a hard rule: there are exceptions if you know what you're doing. A hue change across shades is a deliberate exception, not drift, only when all three hold:

1. It moves one way across the whole scale as the shades darken. Tailwind's yellow goes from hue 102 at yellow-50 to 86 at yellow-500 and 58 at yellow-900 (OKLCH), so its dark end reads as gold-brown instead of olive.
2. Every shade still reads as the same color: no shade of a blue scale reads as cyan or violet.
3. A comment beside the tokens says why.

The drifted chart above fails the first two: from dark to light its hues go 222, 196, 252.

**Why:** a change of hue reads as a change of color, so a drifted shade looks like a different category or a mistake. One hue makes the scale read as one color at different strengths.

**Check:** read each scale's hues in the color space its tokens use (`hsl()` or `oklch()`). They're equal, or they meet all three conditions.

### 16. In dark mode, tone down your brand colors

In the dark theme, lower the chroma of every brand and accent color, and of chart colors drawn from them, by 20–30%, and keep the hue: oklch(0.53 0.25 264) becomes oklch(0.53 0.18 264), 28% less. Do it in the dark theme's tokens, so buttons, selected rows, links and badges calm down together. Change the lightness only where text needs it to reach 4.5:1: text on the brand fill, and brand-colored text on the dark surface.

**Why:** a color tuned for a white page carries its full saturation onto a dark one, where it glows and vibrates. With less chroma it sits on the surface instead of buzzing on top of it.

**Check:** every brand and accent token's dark-theme chroma is 70–80% of its light-theme chroma, at the same hue.

### 7. One big shadow can look fake, so layer a few small ones instead

Never give a surface one big drop shadow like `0 22px 44px 4px rgb(0 0 0 / 0.5)`. Every shadow in the interface (on cards, popovers, menus, dialogs, toasts) is a stack of three small ones: a 1px ring for the edge, a tight shadow for contact and a wider, softer one for lift. Start from this recipe:

```css
box-shadow:
  0 0 0 1px rgb(0 0 0 / 0.06),
  0 2px 4px rgb(0 0 0 / 0.06),
  0 12px 28px -6px rgb(0 0 0 / 0.16);
```

Every layer is black at low opacity (or the project's own dark ink, if it tints its shadows), never an opaque gray and never a light or saturated color, in light mode and in dark.

**Why:** a real object casts a crisp shadow where it nearly touches the page and a soft one around it. One big blur has neither, so it reads as a sticker with a muddy halo. The ring gives a white surface an edge on a white page.

**Check:** every `box-shadow` in use has three layers, and no layer has a blur over 28px or an opacity over 0.16.

## Components and forms

### 11. Placeholders disappear when you type, so put labels above your fields

Every input, select and textarea has a visible label above it, tied to it with `<label for>` or by wrapping it; checkboxes, radios and switches take theirs beside them, tied the same way. A placeholder is never the label: leave it empty, or use it for an example of the value (name@company.com). The one exception is a lone search box with a visible magnifier icon, which the icon and a "Search…" placeholder name; it still carries an `aria-label`.

**Why:** a placeholder vanishes the moment typing starts, right when people look back to check what the field was for. Once an email is typed into an unlabeled form, nothing says what the box is.

**Check:** every field except a lone search box has a visible `<label>` (above it, or beside a checkbox, radio or switch) whose `for` matches its `id`, or that wraps it.

### 17. In tables, right-align your numbers so the digits line up

Right-align every table column of quantities people compare (amounts, counts, percentages, durations) and its header, with `font-variant-numeric: tabular-nums` and the same number of decimals down the column. Text columns stay left-aligned, and so do numbers that are names rather than quantities, like order IDs and phone numbers.

**Why:** right alignment puts ones under ones and decimals under decimals, so the biggest amount shows at a glance. Left-aligned amounts zigzag, and people have to read every digit to compare them.

**Check:** every quantity column's cells and header are right-aligned, with tabular figures and equal decimals.

## Copy

### 8. Write your labels in sentence case, not title case

Every UI string (buttons, labels, headings, menus, tabs, table headers, toasts) is in sentence case: capitalize the first word, proper nouns and acronyms, nothing else. "Save changes", "Billing and plans", "Connect to GitHub", "API keys"; never "Save Changes" or "Comments On My Docs".

**Why:** title case puts a capital on every word, so labels read heavier and slower, and the capitals that carry meaning, on names and acronyms, stop standing out.

**Check:** search the UI strings. After the first word, every capital belongs to a proper noun or an acronym.

### 14. Don't label your buttons Submit. Say what they actually do

Label every button, and every link styled as one, with its outcome, verb first, plus the amount when money moves: "Pay $48.00", "Save changes", "Create account", "Send invite", "Delete 3 files". Never a bare "Submit", "OK", "Continue", "Yes" or "Confirm"; "Continue to payment" is fine, because it says where it goes.

**Why:** people decide from the button alone. An outcome tells them what happens before they press, and the amount on a payment button answers the last question they have.

**Check:** every button label starts with a verb, every payment button shows its amount, and none is one of the five bare words.

## States and pages

### 19. Add a CTA to every empty state

Every empty state has three parts: what's empty, in plain words ("No projects yet"), one line on why or what goes here ("Projects keep your docs, tasks and files in one place."), and one button that is the next step. Never a bare "No items found." Pick the button by why it's empty:

```
Why is it empty?
├── Nothing made yet                    → it makes the first one ("New project")
├── A search or filter found nothing    → it clears it ("Clear filters"), and the text names the search
├── Everything is done (all caught up)  → it opens what comes next ("View archive")
└── No access, or it failed to load     → it fixes that ("Request access", "Try again")
```

If one message serves several causes (a new account and an empty filter both show "No items found."), split it into one state per cause.

**Why:** an empty screen is a dead end unless it says what to do, and for a new user it's often the first screen they see, so it's where they learn the first action.

**Check:** load every list, table, search, inbox and dashboard with nothing in it. Each shows all three parts, and the button works.

### 20. On landing pages, make your CTA way bigger than what feels normal

Only in the hero and CTA sections of landing and marketing pages; product screens size every button by tips 2 and 13. Size the main CTA the way that feels normal, then multiply its font size by 1.7 (20px becomes 34px), with its padding and radius in em so it keeps tips 2 and 13's proportions as it grows (`padding: 0.5em 1em; border-radius: 0.5em` at a line height of 1.4). The secondary button beside it stays at the starting size, and the two center on each other. The CTA is the hero's only filled button, in the accent or the ink color. If its label wraps at 375px wide, shorten the label before you shrink the text.

**Why:** what feels big enough while you build reads timid on a live page, where people decide in a second. A CTA clearly bigger than everything near it is where the eye lands, and a secondary left small makes the difference obvious.

**Check:** the CTA's font size is at least 1.7× the secondary's, its padding is in em, it's the hero's only filled button, and its label fits on one line at 375px.

## Verify

Run every check you can. In a code-only review, compute what the code allows (sizes, ratios, OKLCH, contrast) without creating files, and after the findings list the checks you couldn't run and what each would catch.

- [ ] **Render** the screen at its real size and at 375px wide, in every theme it has.
- [ ] **Read the computed styles** of every text style (size, weight, line height, alignment) and every button, field and one-line box (height, padding), and hold them against tips 1, 2, 3, 6, 10 and 13.
- [ ] **Measure the colors** in hex and OKLCH: every gray (4), every text on a colored fill with its contrast (9), every scale's hues (12), every brand token in both themes (16) and every shadow (7).
- [ ] **Measure the spacing** around every heading (15) and inside every stack (18).
- [ ] **Type into every field.** Its label is still there (11).
- [ ] **Empty the data.** Every list, table, search and inbox shows its three parts and its button (19).
- [ ] **Search the strings** for Title Case and for a bare Submit, OK, Continue, Yes or Confirm (8, 14).
- [ ] **Look at the footers, the tables and the hero** at real size: Delete stands apart (5), the digits line up (17), and the CTA is the biggest thing in the hero (20).

## Deliver

- **Building:** the change, made in the project's tokens and components. Then one line per tip you applied (the tip, where, before → after), and one per tip you broke on purpose, with the reason.
- **Reviewing:** the stock list, the findings table, the problems no tip covers, and the checks you couldn't run.
