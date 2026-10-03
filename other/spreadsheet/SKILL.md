---
name: nuxt-ui-tools-spreadsheet
description: Use this skill when importing Excel, CSV, or pasted rows with nuxt-ui-tools as a package consumer. Covers defineSpreadsheetSchema (typed context, chained text/number/date/boolean/select columns, columns depending on the columns above (options, defaults, rules per row), groups and dynamic groups built from the context, exact matching, option sources shared with forms, unknown-value policies, rules and levels, validate, row identity with duplicates and stored records, output), useSpreadsheetImport (headless models, onSubmit with batches and rejections), the UiSpreadsheetImport* parts, useSpreadsheetSteps with custom steps, and the ready-made UiSpreadsheetImport wizard.
---

# nuxt-ui-tools Spreadsheet Import

Three layers, each usable without the next:

1. **Schema** (`defineSpreadsheetSchema`): the data contract. Columns, how headers and values
   match, rules, row identity, output. No UI.
2. **Runtime** (`useSpreadsheetImport`): headless state and commands, one reactive model per
   concern: `file`, `context`, `layout`, `columns`, `values`, `rows`, `review`, `submit`,
   `readiness`. Tests, scripts, and fully custom screens stop here.
3. **UI**: `UiSpreadsheetImport*` parts placed wherever you want (one page, a drawer, a wizard),
   optional steps (`useSpreadsheetSteps`), and one ready composition (`UiSpreadsheetImport`).

Matching is exact: a header or a value matches a declared name, ignoring case, accents, line
breaks, repeated spaces, and a trailing `*`. Anything else goes to the column's policy or to the
user. The engine never guesses.

Files are read with SheetJS (`xlsx`), an optional peer that must be 0.20.2 or later. npm only
serves 0.18.5, which has known vulnerabilities, so install it from the SheetJS CDN:
`bun add https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`.

## Schema

Declare the context type first when columns depend on data the page provides. Every callback
receives it as `ctx`. Columns are a chain: each method adds a column, and the callbacks of a column
(`options`, `default`, `rules`, `parse`) receive `row`, typed with the columns declared above it.
Write `columns` before the callbacks that read whole rows (`rows`, `validate`, `output`): they are
typed from it.

```ts
interface AssessmentsContext {
  center: TestCenter
  products: readonly Product[] // each with its own `scale` and `skills`
}

const productOf = (ctx: AssessmentsContext, id: string) =>
  ctx.products.find((product) => product.id === id)

export const assessmentsImport = defineSpreadsheetSchema<AssessmentsContext>()({
  key: 'assessments',
  file: { accept: ['.xlsx', '.csv'], maxRows: 5000 },
  columns: (c) =>
    c
      .select('testCenterId', {
        label: 'Test center',
        headers: 'Test center ID',
        options: ({ ctx }) => [ctx.center.vtestId],
        default: ({ ctx }) => ctx.center.vtestId,
        unknown: 'error',
      })
      .text('secureCode', { label: 'Secure code', required: true })
      .text('examName', { label: 'Exam name', required: true })
      .select('productId', {
        label: 'Product',
        from: 'examName',
        options: ({ ctx }) =>
          ctx.products.map((product) => ({
            label: product.name,
            value: product.id,
            aliases: product.examNames,
          })),
        required: true,
      })
      .date('completedAt', {
        label: 'Completed at',
        formats: ['MMMM d, yyyy h:mm a'],
        rules: (v) => [v.notFuture()],
      })
      .number('score', {
        // `row.productId` is typed: the product column is declared above.
        rules: (v, { row, ctx }) => [v.max(productOf(ctx, row.productId)?.maxScore ?? 100)],
      })
      .group('levels', { label: 'CEFR levels' }, (g) =>
        g
          .select('general', {
            label: 'General',
            headers: 'General level',
            // Each product has its own scale: the options follow the row's product.
            options: ({ row, ctx }) => productOf(ctx, row.productId)?.scale ?? CEFR,
          })
          .select('listening', { label: 'Listening', headers: 'Listening level', options: CEFR }),
      )
      .dynamic('affiliations', {
        label: 'Affiliations',
        items: ({ ctx }) => ctx.center.affiliationGroups,
        column: (group, c) =>
          c.select(group.slug, {
            label: group.name,
            headers: `${group.name}: PRÉREQUIS CECR`,
            options: {
              source: toOptions(group.items),
              create: { handler: ({ label }) => api.affiliations.create(label) },
            },
            multiple: true,
            unknown: 'create',
          }),
      }),
  rows: {
    key: (row) => row.secureCode,
    duplicates: 'error',
    existing: {
      lookup: ({ keys, ctx }) => assessmentsByCodeQuery({ centerId: ctx.center.id, codes: keys }),
      action: ({ row, existing }) =>
        row.levels.general === existing.levels.general ? 'skip' : 'update',
    },
  },
  validate: ({ row, issue }) => [
    !row.levels.general &&
      row.status === 'Done' &&
      issue('levels.general', 'Required when the test is done'),
  ],
  output: ({ row, mode, existing, ctx }) => ({
    ...row,
    centerId: ctx.center.id,
    assessmentId: existing?.id,
  }),
})
```

A schema without context skips the type argument: `defineSpreadsheetSchema({ ... })`.

### Column builders

| Method     | Value                                    | Own options                                              |
| ---------- | ---------------------------------------- | -------------------------------------------------------- |
| `.text`    | `string`                                 | —                                                        |
| `.number`  | `number`                                 | `decimal: '.' \| ','` (thousands separators are ignored) |
| `.date`    | ISO `string`, with the time if present   | `formats`, like `dd/MM/yyyy` or `MMMM d, yyyy h:mm a`    |
| `.boolean` | `boolean`                                | `true` / `false`: texts read as each (yes, oui, x, 1…)   |
| `.select`  | the option values, literal when possible | `options`, `from`, `unknown`                             |
| `.group`   | a nested object: `(g) => g.text(…)…`     | `label`, `description`, `when`                           |
| `.dynamic` | a record, one column per context item    | `items: ({ ctx }) => list`, `column: (item, c) => c.…`   |

Options every column takes: `label`, `headers` (strings, regexes, or `({ header, ctx }) => boolean`;
the label and the key always match too), `required`, `default` (a value or `({ ctx, row }) =>
value`, used when the column is missing or the cell is empty), `when` (`({ ctx }) => boolean`,
leaves the column out), `description`, `example`, `parse` (`({ cell, ctx, row }) => value`, its
return type becomes the value type), `rules`, `multiple` (`true` or `{ separator }`), `editable`.

Value types follow the options: optional and without a default → `T | null`; `required` or
`default` → `T`; `multiple` → `T[]`; `when` → the key is optional in the row. Declaring a key twice
is a type error, and so is reading a column declared below.

### Columns depending on columns above

`row` in a column's callbacks holds the columns declared above, parsed. Use it when the accepted
values, the default, or the rules of a column depend on another one:

```ts
c.select('product', { options: products, required: true })
  .select('category', { options: ({ row, ctx }) => categoriesOf(ctx, row.product) })
  .select('level', { options: ({ row, ctx }) => scaleOf(ctx, row.product) })
  .number('score', { rules: (v, { row, ctx }) => [v.max(maxScoreOf(ctx, row.product))] })
  .text('note', { default: ({ row }) => `Imported for ${row.product}` })
```

Options reading `row` return a list; each row is checked against its own list, and the cell editor
offers it. A value matching none is asked once per list: a question carries `scope` (the fields
the options read, with their values in the question's rows: "For Product: English") and `choices`
(that list). Editing the product re-checks the row.

### Options

A `select` takes the option sources of form selects:

```ts
c.select('status', { options: ['Done', 'Absent'] }) // a list
c.select('productId', { options: ({ ctx }) => ctx.products.map(toOption) }) // from the context
c.select('level', { options: ({ row, ctx }) => scaleOf(ctx, row.productId) }) // from the row
c.select('countryId', { options: countriesQuery() }) // a TanStack query
c.select('candidateId', { options: candidates }) // a defineRemoteOptions loader
c.select('site', { options: { source: sites, create: { handler } }, unknown: 'create' })
```

Items are values or `{ value, label, aliases }`; `aliases` are the other exact names a value has in
files. A remote loader is matched exactly with its optional `resolveLabels` query (one request for
every distinct value of the file); without it, each value is searched. Its `load` feeds the picker.

`from: 'examName'` reads the cell of a column declared above: the file's exam name becomes a
product. A `from` that names no column above is a type error.

### Unknown values

| `unknown`       | A value that is not an option…                                                  |
| --------------- | ------------------------------------------------------------------------------- |
| `ask` (default) | becomes a question in Values, once per distinct value; it blocks until answered |
| `error`         | is a blocking issue on the row                                                  |
| `skip-rows`     | leaves its rows out (reason `value`); the user can answer otherwise             |
| `leave-empty`   | is dropped                                                                      |
| `create`        | is created with `options.create.handler` when the user imports                  |

Answers apply to every row using the value (in the question's scope when options depend on the
row). Choices are listed in declared order, never pre-filled.

### Rules and levels

`rules: (v) => [...]`, or `(v, { row, ctx }) => [...]` to read the columns above, with `required`, `validate`, `email`, `pattern`, `minLength`, `maxLength`,
`min`, `max`, `between`, `notFuture`. Each takes `{ message, level }`; `error` (default) blocks the
row, `warning` and `info` only inform. Rules run on non-empty values, on each item with `multiple`,
and are typed by the column: `v.min` on a text column is a type error. Cross-field rules go in
`validate`, which returns issues or falsy values.

### Row identity

`rows.key` is a function of the row (a tuple for several fields). `duplicates`: `error` (both rows
blocked, "Same key as row 34"), `keep-first`, or `keep-last`. `existing.lookup({ keys, ctx })`
returns the stored records (a query definition or a promise); `action` is `update` (default),
`skip`, `error`, or a function of `{ row, existing, ctx }`. Stored records in the row's shape let
review show the cells that change. Each row gets a `mode`: `create`, `update`, or `skip`.

### Sheet and header row

`file.sheet: 'auto'` (default) picks the sheet whose rows name the most columns; `file.headerRow:
'auto'` (default) picks the row, among the first 20, naming the most columns. Title rows above are
skipped. Fix them with a sheet name and a 1-based row for your own templates.

## Runtime

```ts
const importer = useSpreadsheetImport(assessmentsImport, {
  context: {
    center: () => center.value, // a value, a ref, or a getter
    products: productsQuery(), // or a TanStack query, loaded by the runtime
  },
  onSubmit: async ({ create, update, rows, ctx, reportProgress, signal }) => {
    const result = await api.assessments.import({ create, update })
    return {
      rejected: result.errors.map((error) => ({
        index: rows[error.position].index,
        message: error.message,
      })),
    }
  },
  submit: { batchSize: 250 },
})

importer.file.load(file) // or importer.file.paste(text)
await importer.ready()
importer.readiness // { missingColumns, openValues, invalidRows, importable, loading, canSubmit }
await importer.submit.run()
```

`context` is required when the schema declares one. Every model is reactive and reads the same in
templates and scripts (`importer.rows.invalid.length`):

| Model     | State                                                                                                       | Commands                                                                                              |
| --------- | ----------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `file`    | `name`, `loaded`, `reading`, `error`, `sheets`                                                              | `load(source, name?)`, `paste(text)`, `clear()`                                                       |
| `context` | `ctx`, `loading`, `ready`, `error`                                                                          | —                                                                                                     |
| `layout`  | `sheet`, `headerRow`, `detected`, `ambiguous`, `candidates`, `preview`                                      | `setSheet()`, `setHeaderRow()`, `redetect()`                                                          |
| `columns` | `fields` (status `matched` / `default` / `missing` / `unmatched`, `suggestion`), `missing`, `unusedHeaders` | `assign(field, header)`, `ignore(field)`, `reset(field)`                                              |
| `values`  | `questions` (with `scope` and `choices`), `open`, `recognized`, `loading`                                   | `answer(question, option value or action)`, `clear()`, `choices(field, row?)`, `search()`             |
| `rows`    | `all`, `valid`, `invalid`, `discarded`, `importable`, `byMode`, `keyFields`                                 | `cell()`, `edit()`, `revert()`, `discard()`, `restore()`, `distinct()`, `issues()`, `exportInvalid()` |
| `review`  | `tab`, `level`, `mode`, `issue`, `search`, `visible`, `selection`, `inspected`, `position`                  | setters, `select()`, `inspect()`, `next()`, `previous()`                                              |
| `submit`  | `status`, `progress`, `imported`, `rejected`, `error`                                                       | `run()`, `retryRejected()`, `reset()`                                                                 |

Field paths (`levels.general`, `affiliations.${string}`) and row data are typed from the schema.
Edits are text: they go through the same parsing, options, answers, and rules as the file.
Suggestions offer, for a missing required field, an unused column whose values fit it; they are
never applied without the user. Rows the server refuses come back with a `server` issue.

## UI

Parts read the importer from `UiSpreadsheetImportRoot`, or from their own `importer` prop. They
render no step headings: titles and KPIs belong to your page.

| Part                                       | Slots and props                                                                                                               |
| ------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------- |
| `UiSpreadsheetImportRoot`                  | `importer`, `steps`, `locale`. Renders nothing.                                                                               |
| `…Dropzone`                                | default slot `{ load, paste, reading, error, accept }`; accepts drops, browsing, and ⌘V.                                      |
| `…FileCard`, `…SourceSettings`             | file name and Replace; sheet and header row with a preview (`always`, `no-preview`).                                          |
| `…ExpectedColumns`, `…TemplateButton`      | columns the file should have (`#column`); the template built from the schema.                                                 |
| `…ColumnMapping`                           | `only="missing"`, `suggestions`, `group-by-status`; `#field`, default slot with `assign`.                                     |
| `…ValueMapping`                            | `only="open"`, `no-recognized`; `#question`.                                                                                  |
| `…Table`, `…TableToolbar`, `…RowInspector` | editable virtualized grid (`fields`, `height`, `editable`, `selectable`, `#cell`), tabs and filters, one row with its issues. |
| `…Stats`, `…Stat`, `…ExportButton`         | KPI tiles (`#extra` for yours), one tile, the invalid rows as xlsx.                                                           |
| `…SubmitButton`, `…Summary`, `…Progress`   | import with readiness; what will be imported (`#rows`); progress, rejections, retry.                                          |
| `…Stepper`, `…Step`, `…StepNav`            | wizard parts: `orientation="vertical"` and `compact`; a slot per step key; Back, Continue, Import, `cancel-to`.               |

A page without steps:

```vue
<UiSpreadsheetImportRoot :importer="importer">
  <UiSpreadsheetImportDropzone v-if="!importer.file.loaded" />
  <template v-else>
    <UiSpreadsheetImportColumnMapping only="missing" />
    <UiSpreadsheetImportValueMapping only="open" />
    <UiSpreadsheetImportTable />
    <UiSpreadsheetImportSubmitButton />
  </template>
</UiSpreadsheetImportRoot>
```

A wizard declares its steps. Built-in steps know their readiness and default parts; yours are the
same object:

```ts
const steps = useSpreadsheetSteps(importer, [
  { key: 'center', label: 'Center', ready: () => Boolean(centerId.value) },
  spreadsheetSteps.file(),
  spreadsheetSteps.columns({ show: 'when-needed' }),
  spreadsheetSteps.values({ label: 'Matches', show: 'when-needed' }),
  spreadsheetSteps.review(),
  spreadsheetSteps.submit(),
])
```

```vue
<UiSpreadsheetImportRoot :importer="importer" :steps="steps">
  <UiSpreadsheetImportStepper orientation="vertical" :compact="steps.current === 'review'" />
  <UiSpreadsheetImportStep>
    <template #center><CenterPicker v-model="centerId" /></template>
  </UiSpreadsheetImportStep>
  <UiSpreadsheetImportStepNav cancel-to="/assessments" />
</UiSpreadsheetImportRoot>
```

`when-needed` steps are skipped while they have nothing to do, and stay done once visited.

`<UiSpreadsheetImport :importer="importer" :steps="…" title="…" closable>` is the ready
composition: stepper, current step with headings, navigation. A slot named after a step key
replaces its content.

Copy lives under `spreadsheet.*` in the locale; override it with `extendUiToolsLocale` and pass it to
the root, like `{ spreadsheet: { nav: { import: 'Import {count} assessments' } } }`. The current
step marker uses `--nut-sheet-accent-fg` for its text on the primary color.
