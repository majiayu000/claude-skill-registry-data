---
name: nuxt-ui-tools-table
description: Use this skill when building or debugging table usage with nuxt-ui-tools as a package consumer. Covers defineTableSchema, useTable, DataList, granular composition, columns, filters, sorting, offset or cursor loading, layouts, actions, selection, context, and URL state with concrete examples.
---

# nuxt-ui-tools Table

Use this skill for package-consumer tasks involving:

- `defineTableSchema(...)`
- `tableSource(...)`
- `useTable(...)`
- `DataList`
- `DataListRoot` and granular rendering parts
- table columns
- table filters
- client or remote table setup
- table query-state integration
- cursor infinite loading and no-pagination mode

## Read This Skill With

- `skills/consumer/package/SKILL.md`
- `skills/consumer/table/references/overview.md`

Then use the focused references:

- `skills/consumer/table/references/getting-started.md`
- `skills/consumer/table/references/data-modes.md`
- `skills/consumer/table/references/url-state.md`
- `skills/consumer/table/references/schema-surface.md`
- `skills/consumer/table/references/layouts.md`
- `skills/consumer/table/references/pagination.md`
- `skills/consumer/table/references/sorting.md`
- `skills/consumer/table/references/filters.md`
- `skills/consumer/table/references/columns.md`
- `skills/consumer/table/references/selection.md`
- `skills/consumer/table/references/context.md`
- `skills/consumer/table/references/actions.md`
- `skills/consumer/table/references/slots.md`
- `skills/consumer/table/references/patterns.md`

## I18n-Friendly Schema Text

Schema-owned table text should be written as translation-friendly lazy values when it comes from app i18n.

Use this pattern for:

- filter labels
- filter placeholders
- preset labels and descriptions
- column labels
- action labels
- static option labels

Example:

```ts
const { t } = useI18n()

const schema = defineTableSchema({
  tableKey: 'employees',
  rowKey: 'id',
  filters: {
    search: {
      fields: ['fullName', 'email'],
      placeholder: () => t('employees.search.placeholder'),
    },
    ui: (filter) => [
      filter.text('fullName', {
        label: () => t('employees.filters.name'),
        editor: {
          placeholder: () => t('employees.filters.searchName'),
        },
      }),
      filter.date('hiredAt', {
        label: () => t('employees.filters.hiredAt'),
        editor: {
          scalar: {
            presets: [
              {
                label: () => t('shared.datePresets.today'),
                value: ({ now }) => now,
              },
            ],
          },
        },
      }),
    ],
  },
  rowActions: ({ row }) => [
    {
      key: 'copy-email',
      label: () => t('employees.actions.copyEmail'),
    },
  ],
  table: {
    columns: (column) => [
      column.field('fullName', {
        label: () => t('employees.columns.fullName'),
      }),
    ],
  },
})
```

Prefer translation keys through `t(...)` over writing bilingual helpers or rebuilding the whole schema in a `computed(...)`.

If a surface only renders package-owned UI text and does not come from your schema, use the package locale/provider layer instead of duplicating those strings in your app schema.
