---
name: ui-ux-principles
description: Canonical UX and UI principles for every interface. Read before planning, building, reviewing, or testing any user-facing screen, flow, modal, form, or component.
---

# Global Interface Principles

This skill is the source of truth for interface behavior and presentation. Read the current version before building or changing any UI. Other skills may add domain or aesthetic guidance, but they must reference these principles and cannot override them unless the user explicitly requests an exception.

## Design Principles

### Design for the product mode

- Operational interfaces are compact, quiet, and structured around the work surface.
- Marketing and commerce interfaces may be more expressive through authentic imagery, branded typography, and one restrained accent color.
- Density follows the task. Repeated operational work is compact; explanation and persuasion have room to breathe.
- Familiar controls remain visually quiet in every mode.

### Layout and spacing

- Align navigation, page headers, content, tables, and action rows to one shared content frame.
- Use a named 4px-based spacing scale. Do not introduce isolated spacing values.
- Use panes, dividers, spacing, and surface changes before adding containers.
- A container must represent a genuine interaction or content boundary.
- Avoid wrapper soup, decorative cards, accumulated padding, and unused empty canvas.
- Responsive layouts recompose around task order. They do not merely scale down a desktop canvas.

### Typography

- Use no more than one display family and one body family on a product surface.
- Reserve expressive type for brand or editorial hierarchy. Controls and dense operational text use a highly legible sans-serif.
- Reserve monospace for code, identifiers, timestamps, and data that benefits from fixed-width alignment.
- Keep hierarchy short and decisive: optional eyebrow, title, supporting copy, action.
- Every text level adds information. Never restate the same title or instruction nearby.

### Color and theme completeness

- Build from semantic tokens for surfaces, borders, text, muted text, accent, success, warning, danger, focus, type, spacing, and radius.
- Prefer a restrained palette: neutral surface hierarchy, one product accent, and semantic status colors.
- Color has one meaning within a product. Brand color never replaces error, warning, destructive, disabled, or focus meaning.
- Text, icons, borders, controls, and states must be visually aligned with the surface behind them. Never place a text or control color on a background where it looks accidental, muddy, or inherited from another theme.
- Black text on gray or dark surfaces, dark text on dark surfaces, pale text on white surfaces, and similarly mismatched foreground/background combinations are release-blocking defects unless the pairing is an intentional token with verified contrast.
- A light or dark theme is complete only when every visible component and every state uses the correct theme tokens. An unthemed native control, popup, menu, dialog, table, editor, tooltip, empty state, loading state, error state, or third-party component is a release-blocking defect.
- Theme review must cover default, hover, focus, active, selected, disabled, loading, empty, success, warning, error, destructive, and overlay states.
- One-off color, spacing, radius, shadow, and type values require an explicit documented reason.
- Meet WCAG AA contrast in every state. Passing automated contrast checks does not excuse a visually discordant or obviously mis-themed combination.

### Density and component patterns

- Dense interfaces remain legible, aligned, and keyboard operable.
- Use one visually dominant action per view or decision region. Secondary actions are quieter.
- Buttons use specific verbs that state the result.
- Components define default, hover, focus, active, selected, disabled, loading, success, and error states where relevant.
- Use modest radii, fine borders, and restrained shadows. Pills are reserved for tags, filters, and statuses.
- Use authentic product, garment, system, or content imagery rather than generic decoration.

### Motion

- Motion confirms causality, change, progress, or spatial continuity.
- Functional transitions are brief and use transform or opacity where practical.
- Avoid ambient loops, decorative parallax, layout-property animation, and motion that competes with the task.
- Pause or stop non-essential motion on hover or focus where relevant.
- Respect `prefers-reduced-motion` without replacing one long animation with another.

### Interaction feedback and states

- Feedback appears next to the control or object that caused it.
- Success is brief. Errors remain until fixed or dismissed and include a recovery action where one exists.
- Loading preserves the final layout. Empty states explain what belongs there and offer the primary action.
- Preserve entered data after validation, network, and server errors.
- Navigation and state changes are deterministic and do not create surprise movement or layout shift.

### Microcopy

- Copy is short, natural, specific, and verb-led.
- Say what will happen next: `Save customer`, `Book the call`, `Reload this page`.
- Avoid `OK`, `Yes`, `Submit`, filler, repeated helper text, and context-free errors.
- Reassure through clarity and recovery, not apology-heavy prose.

### Finished detail

- A visual change is not complete until the current final render has been inspected at full resolution.
- Check alignment, hierarchy, rhythm, truncation, overflow, collisions, focus, target size, asset quality, content order, state consistency, color pairing, and theme completeness.
- Verify representative desktop, mid-width, and mobile views after the last content or layout change.
- Do not use stale screenshots, source review, automated contrast results, or automated tests as substitutes for final visual inspection.

## UX Principles

### One screen, one job

- Each page or modal has one clear purpose.
- Never merge list, create, edit, and detail views into one hybrid screen.
- Do not use edit-in-place, forms embedded inside lists, or expanding rows that turn into forms unless the user explicitly specifies that interaction.

### Fixed CRUD flow

- The list page is the home of every entity and exposes search, filters, sorting, pagination, and relevant bulk actions.
- Add and Edit use the same form component.
- A form with five fields or fewer and no nested data uses a modal. A longer form uses a page or drawer. A complex record with tabs, nested items, or related lists uses a full page.
- Delete uses either a clear confirmation modal or soft delete with an Undo toast, chosen according to reversibility and consequence.

### Orientation, feedback, and predictability

- The user always knows where they are, what they can do, and what just happened. Navigation state, the primary action, and action feedback are explicit.
- The same action always produces the same result in the same place. Avoid surprise navigation, layout shift, and hidden side effects.
- Never stack modals. A modal never opens another modal. Never open a popup or modal on page load.
- Warn before discarding unsaved changes. Keep input on validation errors. Validate inline on blur and on submit.
- After save, return the user to the originating view with the changed record visible.
- Errors explain what went wrong and how to fix it, with a retry when relevant. Empty states explain what belongs there and offer the primary action.
- The URL preserves filters, sort, page, and the open record so the state is deep-linkable and survives refresh.
- Use the fewest steps possible. If a task takes three clicks and can safely take one, simplify it.

## UI Principles

Every element must earn its place. If removing it loses no function or necessary meaning, remove it.

### No duplication

- A labelled tab does not repeat that label as a heading in its content.
- A page title shown in the header or banner is not repeated in the body, the final breadcrumb item, a card title, or a section heading.
- A modal title states the action once. Its body does not restate the title, and its primary button uses the specific verb, such as `Save customer`.
- Never show the same information twice on one screen. Do not repeat counts, add summary cards that restate table data, or use a subtitle that restates the title.
- Use one primary action per view. Do not duplicate the same action in the header and footer.

### No bloat

- Do not add generic hero banners, gratuitous icons, gradient cards, stock illustrations, emoji, or welcome text unless explicitly required.
- Avoid wrapper soup. Use one level of containment unless the content structure genuinely requires another.
- Do not add placeholder or marketing copy such as `Manage your items with ease`. Labels are short and functional.
- Remove helper text, tooltips, and descriptions that merely repeat the label.
- Do not add dashboards, statistics widgets, or charts that were not requested.
- Whitespace comes from spacing tokens, not accumulated padding used to fill the screen.

### Consistency and accessibility

- Use design tokens for spacing, color, type, and radius. Do not introduce one-off values.
- Every page header shows the title and a single primary action in the top right.
- Buttons use specific verbs, never `OK`, `Submit`, or `Yes`. Cancel is on the left, the primary action is on the right, and destructive actions use destructive styling.
- Right-align numbers and currency in tables. Use one date format across the application.
- Success uses an automatically disappearing toast. Errors remain visible until fixed. Never use browser `alert()` or `confirm()`.
- Loading uses skeletons rather than full-page spinners.
- Every interface is keyboard navigable with visible focus states, WCAG AA contrast, and labelled fields.
- On mobile, tables become cards and drawers become full-screen sheets.

## Taste Memory

Older skill references to `Fix Memory` mean this process.

- Maintain `taste-log.md` alongside this document.
- Whenever the user rejects, corrects, or reworks a UI decision, append one line containing the date, what was done, what the user wanted instead, and why.
- Ask the user for the reason when it is not clear. Do not invent intent.
- When the same correction appears two or three times, propose promoting it to a rule in Design Principles. Do not promote one-offs.
- Before starting any UI task, read Design Principles, Definition of Done - UI, and the last 20 entries of `taste-log.md`.
- If a log entry contradicts an existing principle, flag the conflict and ask the user which one wins.
- Keep corrections from the active thread in working context until they have been recorded.
- When the user asks to `audit the UI/UX` of a project, apply this skill together with Impeccable, Apple design standards, accessibility review, source inspection, and current rendered desktop/mobile evidence.
- Record a changelog entry whenever a standing principle changes.

## Definition of Done - UI

Older skill references to the `Pre-ship Check` mean this section.

A UI task is not complete until every relevant item passes:

- [ ] The current Design Principles and last 20 taste-log entries were reviewed before implementation.
- [ ] The screen has one job, one title, and one visually dominant primary action.
- [ ] Removing any element would remove a function or necessary meaning.
- [ ] Titles, actions, information, and helper copy are not duplicated.
- [ ] Layout uses the product's shared frame, spacing scale, typography, colors, radii, and components.
- [ ] There are no unexplained one-off visual values.
- [ ] Every visible component and state is styled for the active light or dark theme, including native and third-party controls, overlays, menus, dialogs, tables, editors, tooltips, loading, empty, and error states.
- [ ] Foreground/background combinations are visually coherent and meet WCAG AA. No accidental black-on-gray, dark-on-dark, pale-on-white, or inherited cross-theme styling remains.
- [ ] Default, hover, focus, active, selected, disabled, loading, empty, validation error, system error, and success states were checked where relevant.
- [ ] Forms preserve input, show inline errors, protect unsaved changes, and return focus correctly.
- [ ] Success feedback disappears automatically. Errors persist and include retry or recovery where relevant.
- [ ] No browser `alert()` or `confirm()` is used.
- [ ] Keyboard navigation, visible focus, labels, modal focus trapping, focus return, WCAG AA contrast, and reduced motion were verified.
- [ ] Desktop, mid-width, and mobile layouts were rendered after the final change and inspected at full resolution.
- [ ] Mobile reflows according to task order, uses practical touch targets, and has no accidental horizontal overflow.
- [ ] The inspection checked clipping, collisions, layout shift, truncation, broken assets, excessive containment, stale content, visual misalignment, token leakage, and incomplete theme coverage.
- [ ] Screenshots or other visual evidence identify the route, viewport, timestamp, and current build or commit.
- [ ] Every applicable FRAC acceptance criterion passes.

Recommended review widths are 1440x900, a representative width from 980px to 1120px, and 390x844.

## Changelog

| Date | What went wrong | Rule added or changed |
|------|-----------------|-----------------------|
| 2026-10-14 | Interaction behavior and visual presentation were combined in one rule set. | Split the source of truth into separate UX Principles and UI Principles. |
| 2026-10-14 | Titles, labels, information, and actions could be repeated across one screen. | Added No duplication rules and the removal test. |
| 2026-10-14 | Decorative filler, wrapper soup, and unsolicited widgets made interfaces look generated rather than intentional. | Added No bloat rules requiring every element to earn its place. |
| 2026-10-14 | CRUD views could collapse into hybrid list, detail, and form screens. | Added One screen, one job and a fixed CRUD flow. |
| 2026-10-14 | UI corrections were fixed locally but did not reliably change future behavior. | Added Fix Memory, the Pre-ship Check, and a required changelog entry for principle changes. |
| 2026-10-14 | Product-specific visual taste was implicit across exemplar projects rather than available as standing guidance. | Added Design Principles and replaced the narrow pre-ship questions with Definition of Done - UI. |
| 2026-10-14 | Foreground/background mismatches and partially styled dark-mode components could pass broad token or contrast checks while remaining visibly broken. | Added color-pairing, semantic-token, full-state theme coverage, and release-blocking theme-completeness rules. |
