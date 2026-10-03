---
name: nuxt-ui-tools-i18n
description: Use this skill when wiring nuxt-ui-tools translations in an app. Covers UiToolsProvider, locale objects, lazy schema text, and how package-owned UI copy differs from schema-owned text.
---

# nuxt-ui-tools I18n

Use this skill for package-consumer tasks involving:

- `UiToolsProvider`
- custom `ui-tools` locale objects
- Nuxt UI locale syncing
- schema-friendly translation keys with `() => t('...')`
- translating table and form package surfaces

## Read This Skill With

- `skills/consumer/package/SKILL.md`
- `skills/consumer/table/SKILL.md`
- `skills/consumer/form/SKILL.md`

## Root Setup

Package-owned `ui-tools` copy should come from the `ui-tools` locale layer, not from repeating those strings in every schema.

Typical app shell:

```vue
<script setup lang="ts">
import * as locales from '@nuxt/ui/locale'
import * as uiToolsLocales from '#ui-tools/i18n/locales'

const { locale } = useI18n()
</script>

<template>
  <UApp :locale="locales[locale]">
    <UiToolsProvider :locale="uiToolsLocales[locale]">
      <NuxtPage />
    </UiToolsProvider>
  </UApp>
</template>
```

If `uiToolsLocales[locale]` is `undefined`, `ui-tools` falls back to English.

Use a custom locale object when you want to override only part of the package copy:

```ts
const locale = defineUiToolsLocale({
  code: 'fr',
  name: 'Français',
  messages: {
    table: {
      footer: {
        rowsPerPage: 'Lignes par page',
      },
    },
  },
})
```

## What Belongs In The Provider Locale

Use the provider locale for package-owned UI such as:

- table footer labels
- filter operator labels
- column panel labels
- form action labels and validation messages
- empty states, built-in buttons, and built-in prompts

That copy belongs to the package and should be translated once through the locale object.

## What Belongs In Your Schema

Use lazy translation values for schema-owned text such as:

- column labels
- filter labels
- filter placeholders
- preset labels and descriptions
- row action labels
- form field labels, descriptions, and placeholders
- option labels you provide from app data

Preferred pattern:

```ts
const { t } = useI18n()

const schema = defineTableSchema({
  filters: {
    search: {
      fields: ['fullName'],
      placeholder: () => t('employees.search.placeholder'),
    },
    ui: (filter) => [
      filter.text('fullName', {
        label: () => t('employees.filters.name'),
        editor: {
          placeholder: () => t('employees.filters.searchName'),
        },
      }),
    ],
  },
  table: {
    columns: (column) => [
      column.field('fullName', {
        label: () => t('employees.columns.fullName'),
      }),
    ],
  },
})
```

## Important Rule

Do not rebuild the whole schema in `computed(() => defineTableSchema(...))` just to make translations reactive.

Instead:

1. keep the schema shape stable
2. pass lazy text values like `() => t('...')`
3. let `ui-tools` resolve them at render time

## Form Example

```ts
const { t } = useI18n()

const schema = defineFormSchema({
  fields: [
    {
      key: 'firstName',
      type: 'text',
      label: () => t('users.fields.firstName.label'),
      placeholder: () => t('users.fields.firstName.placeholder'),
    },
  ],
})
```
