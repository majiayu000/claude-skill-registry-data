---
name: nuxt-ui-tools-display
description: Use this skill when showing read-only content with nuxt-ui-tools display blocks, inside a form (the `info` field with `display` and `props`) or on their own (`UiDisplay`). Covers the 19 kinds (heading, text, alert, facts, stat, breakdown, meter, chart, table, diff, record, person, list, timeline, date, media, code, empty, accordion) and their variants, props that follow form values or load through a promise or TanStack Query options with skeleton and error states, the form api in props callbacks, the label shell, lazy file links, presets, slot classes, and tones, including tones an app registers.
---

# nuxt-ui-tools Display

Display blocks draw read-only content: notices, label/value facts, totals, gauges, records,
people, lists, timelines, dates, media, code, empty states. Each block is one **kind** with a few
**variants**, configured by plain props.

Use them in two places:

- in a form, as an `info` field with `display` and `props`, where `props` can read the form values,
  load data, and act on the form;
- anywhere else, with the `UiDisplay` component (`NutDisplay` with the `Nut` prefix).

```ts
import { defineFormSchema } from '#ui-tools/form'

defineFormSchema({
  fields: [
    { key: 'seats', type: 'number', label: 'Candidates', default: 30 },
    {
      key: 'quote',
      type: 'info',
      display: 'breakdown',
      dependencies: ['seats'],
      props: ({ deps }) => ({
        lines: [
          { label: 'Licences', detail: `${deps.get<number>('seats')} × €96`, value: total(deps) },
        ],
        total: { label: 'Total', value: totalWithVat(deps) },
      }),
    },
  ],
})
```

```vue
<UiDisplay
  display="facts"
  :props="{
    layout: 'grid',
    items: [{ label: 'Status', chip: { label: 'Active', tone: 'success' } }],
  }"
/>
```

## References

- `skills/consumer/display/references/kinds.md` — every kind, its variants and props, with examples
- `skills/consumer/display/references/info-field.md` — the form `info` field: static, derived and
  loaded props, the form `api`, the label shell, presets, the legacy notice
- `skills/consumer/display/references/theming.md` — tones (built-in and registered), slot classes,
  presets, icons, CSS variables, translations

## Kinds at a glance

| Kind        | Variants                                                                       | For                                         |
| ----------- | ------------------------------------------------------------------------------ | ------------------------------------------- |
| `heading`   | `title` (`sm`, `md`, `lg`), `eyebrow`                                          | titling a group of fields                   |
| `text`      | `body`, `lead`, `muted`, `caption`, `quote`, `legal`, `prose`                  | copy, quotes, legal notes                   |
| `alert`     | `soft`, `outline`, `subtle`, `solid`, `callout`, `inline`, `banner`            | notices with items, lists, details, actions |
| `facts`     | `ledger`, `grid`, `inline`, `columns`, `tiles`                                 | label → value pairs                         |
| `stat`      | `hero`, `price`, `row`, `trend`                                                | one figure or a row of them                 |
| `breakdown` | `open`, `collapsible`, `compare`                                               | lines adding up to a total                  |
| `meter`     | `bar`, `segments`, `split`, `ring`, `scale`                                    | usage, shares, scores, levels               |
| `chart`     | `bars`, `line`, `donut`, `funnel`                                              | small charts in the dashboard palette       |
| `table`     | —                                                                              | a light read-only table                     |
| `diff`      | `inline`, `columns`                                                            | what a change will do                       |
| `record`    | `row`, `card`, `compact`, `stack`                                              | one entity or a stack of them               |
| `person`    | `user`, `group`, `contact`                                                     | people                                      |
| `list`      | `bullets`, `numbered`, `icons`, `checks`, `steps`, `columns`, `files`, `chips` | lists                                       |
| `timeline`  | `vertical`, `log`, `pipeline`, `schedule`                                      | history and plans                           |
| `date`      | `tile`, `range`, `countdown`                                                   | a moment, a span, a deadline                |
| `media`     | `image`, `gallery`, `video`, `document`, `link`                                | files and links                             |
| `code`      | `block`, `value`, `secret`                                                     | values people copy                          |
| `empty`     | `dashed`, `plain`                                                              | nothing yet, and how to fix it              |
| `accordion` | `separated`, `flush`                                                           | folded content, nested blocks               |

## Shared props

Every kind takes `loading` (draws its skeleton) and `ui` (slot classes). Most take some of:

- `tone`: `primary`, `secondary`, `success`, `info`, `warning`, `error`, `neutral`, or a tone the
  app registered (see theming)
- `surface`: `plain`, `muted`, `bordered`, `elevated`
- `size`: `sm`, `md`, `lg`
- `max`, `step`, `empty` on lists: fold after `max` items with a « Show more · N » button, reveal
  `step` more at a time, and say what is missing when there is nothing
- `actions`: `UButton` props with a lazy `label`
- `copy` on facts, people and code values

Text props accept a string, a lazy translation (`() => t('key')`), a VNode, or a render function.

## Gotchas

- `props` is required on an info display field; with a `preset`, the preset fills the props you
  leave out.
- A registered tone needs both the `display.tones` entry (its colors) and the
  `DisplayToneRegistry` augmentation (its name in types).
- Pass dates as `Date`, ISO strings or epoch milliseconds; blocks format them with the locale.
- File links can be functions returning a signed URL; they run only when the link is used.
