---
name: system-naming
description: Name interface, code, design-system, and product concepts clearly and consistently. Use this skill when choosing, reviewing, auditing, or refactoring names for button labels, commands, menu items, fields, variables, classes, CSS custom properties, design tokens, Figma variables, Figma layers, UI components, icons, colour names, feature names, product names, navigation labels, UX terminology, or any "what should this be called?" question. Covers naming taxonomies, user-facing labels, semantic versus implementation names, controlled vocabulary, alias handling, and consistency checks. Does NOT choose visual values, token scale values, component architecture, layouts, animation, accessibility mechanics, or brand strategy; use the relevant domain skill for those decisions.
---

# Naming

Naming rules for product interfaces, design systems, and implementation code. This skill decides what a thing should be called and how that name fits the surrounding vocabulary.

Based on [NN/g UI copy](https://www.nngroup.com/articles/ui-copy/), [Shopify Polaris naming](https://polaris-react.shopify.com/content/naming), [Component Gallery](https://component.gallery/components/), [Good Practices naming](https://goodpractices.design/guidelines/naming), [Design Systems iconography](https://www.designsystems.com/iconography-guide/), [Intuit token taxonomy](https://medium.com/@NateBaldwin/creating-a-flexible-design-token-taxonomy-for-intuits-design-system-81c8ff55c59b), [Vodafone variables taxonomy](https://medium.com/vodafone-uk-design-experience/figma-variables-at-vodafone-uk-how-we-structured-taxonomy-for-a-complex-multi-brand-design-system-693b1b95675f), [Classnames](https://classnames.paulrobertlloyd.com), [Moccu naming convention](https://www.moccu.com/en/insights/digital-design/naming-convention-a-helpful-framework-for-structuring-design-systems/), [Color.pizza](https://parrot.color.pizza), [Onym](https://guide.onym.co), and [Naming Cheatsheet](https://github.com/kettanaito/naming-cheatsheet).

Use `references/taxonomy.md` when auditing many names, mapping Figma names to code names, or choosing terms across several domains at once.

Keep the boundary with surface-copy clear: this skill owns product action labels, command names, terminology systems, and cross-surface consistency. surface-copy owns explanatory or persuasive wording such as error message bodies, empty state body text, onboarding text, tooltip prose, loading copy, and marketing-style CTAs. For a full flow, establish names here first, then use surface-copy for surrounding copy and tone.

---

## Naming Workflow

1. **Identify the surface.** Decide whether the name is user-facing copy, a design-system name, a code identifier, a Figma layer or variable, or a product/feature name. A good user label and a good implementation identifier often have different constraints.
2. **Define the thing.** Write the plain-language definition before naming it. Identify the object, action, state, role, scope, and owner.
3. **Reuse the vocabulary.** Search existing code, components, tokens, Figma files, docs, and product copy. Prefer the established term unless it is clearly wrong.
4. **Choose the name shape.** Pick the pattern for that surface: verb-led command, noun component, role-based token, glyph-based icon, or descriptive feature name.
5. **Test the name.** Check that it is specific, pronounceable, scannable, stable, not overloaded, and not tied to an implementation detail unless the audience is implementation-only.
6. **Record aliases.** If people already use multiple terms, choose one preferred term and record aliases or deprecated terms in the project glossary.

The core rule: name by the job the name performs. User-facing names explain the outcome. System names preserve structure. Code names preserve intent.

---

## User-Facing Labels

Buttons, commands, menu items, links, and confirmation actions use short, direct labels.

- Start with a verb when the control performs an action: `Create invoice`, `Delete project`, `Export CSV`.
- Name the outcome, not the mechanism: `Save changes`, not `Submit`; `Send invite`, not `Trigger invite`.
- Include the object when ambiguity or risk is high: `Delete file`, not `Delete`.
- Use exact destructive labels in confirmations: `Delete 12 files`, not `OK`, `Yes`, or `Confirm`.
- Reserve `Cancel` for backing out without applying the action.
- Use sentence case unless the product's style guide says otherwise.
- Avoid branded, cute, or metaphorical labels for routine commands. They slow people down.
- If a command appears in several places, keep the same label everywhere unless the object changes.

For toggles, label the setting, not the click. Prefer `Email notifications` with visible on/off state over a button that flips between `Enable` and `Disable` unless the control is explicitly command-like.

---

## Component and Pattern Names

Use standard UI terms before inventing local ones. A component name should describe the pattern, not its visual treatment.

- Name components as nouns: `Dialog`, `Popover`, `Combobox`, `DataTable`, `CommandMenu`.
- Do not rename standard patterns for style: `GlassPanel` is a style, not a component role.
- Keep compound parts predictable: `{Parent}.{Part}` such as `Dialog.Trigger`, `Dialog.Content`, `Dialog.Title`.
- Distinguish common pairs:
  - `Tooltip`: short, non-interactive help on hover/focus.
  - `Popover`: floating interactive content.
  - `Dialog`: blocking decision or focused task.
  - `Sheet`: edge-attached panel, often mobile-friendly.
  - `Toast`: low-priority background feedback.
  - `Alert`: persistent inline or page-level notice.
  - `Select`: choose from known options.
  - `Combobox`: type to search or enter a value.
  - `Badge`: compact status or count.
  - `Tag` or `Chip`: removable or user-selected metadata.

If a component name needs an explanation every time, the name is probably wrong or the component is doing too much.

---

## Code Identifiers

Code names should expose intent without leaking accidental implementation details.

- Variables name the value they hold: `selectedAccount`, `invoiceTotal`, `visibleColumns`.
- Functions use verbs or verb phrases: `calculateTotal`, `formatCurrency`, `fetchInvoices`.
- Event handlers name the event or user action: `handleSubmit`, `handleRowSelect`, `onOpenChange`.
- Booleans use the local convention. In this suite, component props omit the `is` prefix: `open`, `disabled`, `loading`. In app code, `is`, `has`, `can`, and `should` are acceptable only when they state state, possession, capability, or policy.
- Avoid vague containers: `data`, `item`, `value`, `thing`, `payload`, unless the surrounding type makes the meaning obvious.
- Avoid negative booleans such as `isNotReady` or `disableRetry`. They create double negatives in conditions.
- Avoid names that describe current implementation when the concept is broader: `localStorageTheme` is worse than `themePreference` unless the storage mechanism is the point.

For CSS classes, choose one naming model per project. Semantic classes name the object or role (`search-field`, `billing-summary`). Utility classes name the property or behaviour because they are intentionally implementation-facing.

---

## Tokens and Variables

Token names are a taxonomy, not a pile of labels. They must sort, search, and survive visual redesign.

- Order names from broad to specific.
- Primitive tokens describe what the value is: `--blue-500`, `--space-4`, `--radius-md`.
- Semantic tokens describe the role: `--color-text-primary`, `--color-surface-raised`.
- Component tokens scope semantic values only when needed: `--button-padding-x`, `--card-edge`, `--card-shadow`.
- Include state or mode only when it changes the role: `--color-action-hover`, `--color-border-focus`.
- Do not put a component name in a semantic token. Use component tokens for component scope.
- Mirror Figma variable groupings and code names where possible. If they differ, document the mapping.
- Avoid ordinal names without meaning: `primary-2`, `surface-3`, `grey-alt`. If a number is a scale step, make that explicit and documented.

For detailed design-token architecture, use system-tokens. This skill owns whether the names communicate the right taxonomy.

---

## Icons and Colours

Icon names describe the glyph. Labels and aliases describe the use.

- Name icons by what they depict: `trash`, `lightbulb`, `chevron-left`, `paperclip`.
- Do not name an icon by one use case: use `lightbulb` with aliases such as `idea` or `tip`, not an icon named `idea` if the glyph is a bulb.
- Add search aliases for common meanings, products, and verbs.
- Accessible labels for icon-only controls name the action or destination: `Delete file`, `Open settings`, not `Trash icon`.

Colour names depend on audience:

- Primitive colour tokens use objective hue and scale names: `blue-500`, `neutral-900`.
- Semantic colour tokens use role names: `color-text-primary`, `color-status-error`.
- Human-facing palette names can be friendlier, but should not replace functional token names.
- Avoid cute colour names in implementation unless the brand system explicitly requires them.

Use surface-colour for palette construction, contrast, OKLCH, and theme mapping.

---

## Features and Products

Most features should have descriptive names. Branded names are expensive because people must learn and remember them.

- Use descriptive feature names for capabilities inside a product: `Saved views`, `Bulk edit`, `Scheduled exports`.
- Use branded product names only for standalone offerings, marketable packages, or concepts that need legal or commercial separation.
- Check pronunciation, spelling, localisation, domain fit, and collisions before recommending a product name.
- Avoid naming a feature after its internal team, architecture, or launch campaign.
- If the name needs a subtitle to be understood, the descriptive name is usually the better primary name.

When reviewing product names, separate language quality from strategy. A name can be elegant and still be bad if it fails search, pronunciation, legal, or category fit.

---

## Glossary Discipline

Create or update a terminology table when a project has repeated naming drift.

Use these columns:

| Preferred term | Definition | Use for | Avoid | Aliases | Owner |
|---|---|---|---|---|---|
| `Popover` | Floating interactive content anchored to a trigger | Component, docs | Tooltip, flyout | Floating panel | system-components |

The glossary is the source of truth. When you rename, propose a migration path for code, Figma, docs, analytics events, and user-facing copy.

---

## Anti-Patterns

1. **Synonym drift.** `Project`, `workspace`, and `team` used for the same concept.
2. **Mechanism names for user actions.** `Submit`, `Execute`, `Trigger`, or `Run workflow` when the user expects the outcome.
3. **Cute names for routine controls.** Novelty increases comprehension cost.
4. **Visual names for structural concepts.** `BlueButton`, `GlassCard`, `BigModal`.
5. **Implementation leakage.** `redisUser`, `graphqlError`, or `localStorageTheme` when the concept is broader.
6. **Ordinal names without taxonomy.** `primary-2`, `surface-alt`, `new-card`.
7. **Icon names by meaning only.** `idea` for a lightbulb glyph with no alias system.
8. **Branded feature sprawl.** Every minor capability gets a proper noun.
9. **Negative booleans.** Names that make conditions read as double negatives.
10. **Undocumented aliases.** Renaming in one surface while old names survive elsewhere.

---

## Checklist

### Fit
- Surface identified: user label, code, token, component, icon, Figma, feature, or product
- Definition written before choosing the name
- Existing vocabulary checked
- Preferred term and aliases documented when needed

### Clarity
- Name is specific and scannable
- Name avoids vague words unless type or context supplies meaning
- User-facing labels name outcomes
- Technical names preserve intent rather than mechanism
- No double negatives or overloaded terms

### Consistency
- Similar concepts share the same name shape
- Component and pattern names use standard UI terminology
- Tokens follow primitive, semantic, and component layering
- Figma and code names are aligned or mapped
- Rename impact considered across code, Figma, docs, analytics, and copy

---

## Learning from Usage

After completing a naming task, review whether the chosen names held up across user-facing copy, design artefacts, and implementation. Append durable findings to `learnings.md` in this skill's folder. Installed learnings are local runtime notes preserved across suite updates; consult `learnings.md` before starting any new naming task.
