---
name: admin-lists-screen
kind: pattern
rule: lists
description: Pattern of rule lists. Load when assembling or editing an admin list screen — the ready-made order of blocks, the <prefix>-table markup, row click, row menu with an actions column and a row predicate, sortable header, toolbar slots, failure toast.
---
<!-- rt-kit v0.34.0 · patterns/admin-lists-screen.md · 82c8594c752d · правится надстройкой, не здесь -->

# Assembling a list screen

Pattern of the rule `lists`. What must be true — the law
`docs/constitution/lists.md`.

## When to use

- A new screen with a list of records is created.
- An existing one is edited: columns, row menu, toolbar, sorting.

## Order of blocks

The layout comes from the shared block `<prefix>-page` of the application layer, not from the
screen's styles. The screen answers for the order:

```html
<ng-container rtBlock="<prefix>-page">
    <header rtElem="header">
        <!-- div rtElem="header-main" with h1 rtElem="title" + p rtElem="hint" -->
        <<prefix>-toolbar>
        <!-- <prefix>ToolbarLeft / <prefix>ToolbarRight -->
        <div rtElem="scroll">
            <!-- overflow-x: auto -->
            <<prefix>-table rtElem="table">
            <!-- min-width: max-content -->
            <<prefix>-pagination>
        </div>
    </header>
</ng-container>
```

Both scrolling rules are needed together: with the container alone the columns shrink instead of
shifting. The toolbar and the pagination carry no classes of their own — the gap is set by
`<prefix>-page` itself.

## The table

```html
<<prefix>-table #rowsTable="<prefix>Table" rtElem="table" clickable [ariaLabel]="'recordsTableAria' | transloco"
[emptyMessage]="'recordsEmpty' | transloco" [tableId]="tableId" [dataSource]="rows()" [columnsConfig]="columnsConfig()"
[rowHasActions]="hasRowActions" [loading]="loading()">
```

- `tableId` — the key under which the column choice is stored; it also goes to the settings aside.
- `[columnsConfig]`, not a bare list of keys: the captions for the settings panel and for the
  cards on a narrow screen are taken from it.

## Row click

```html
<tr
    *cdkRowDef="let row; columns: rowsTable.displayedColumns()"
    cdk-row
    qa-dataid="records-row"
    <prefix>TableRow
    (activated)="openAside(row)"></tr>
```

Rows are declared on `rowsTable.displayedColumns()`: the column with the menu the table adds
itself.

## Row menu

```html
<<prefix>-table … [showRowActions]="true" [rowHasActions]="hasRowActions" [loading]="loading()">
    <ng-template <prefix>TableRowActions let-row [<prefix>TableRowActionsRowType]="rows()"></ng-template>
```

```typescript
protected readonly hasRowActions: I<Prefix>Table.RowActionsPredicate<IRecord.Row> = recordRowHasActions;
```

There are two inputs, and they do not replace each other. `showRowActions` creates the actions
column itself — by default it is omitted, and without it the table draws only the declared
columns: neither the actions template nor the predicate adds the column. `rowHasActions` decides
whether to show the button on a particular row, and creates no column at all. That is how the
roles screen came out with four columns and unreachable actions: the build, the lint and the
units on the row rules were green, and it was found by the end-to-end run.

The actions cell is hidden until the pointer is on the row — the end-to-end test hovers the row
before pressing.

Action availability lies in a row field (`canConfirm`, `canReject`), not in a call of a component
method. An action the record cannot take is removed from the menu entirely. An irreversible one
carries `danger`, `confirmTitle` and `confirmMessage` with the consequence — not "Are you sure?",
but what exactly will happen.

## Sortable header

```html
<th *cdkHeaderCellDef cdk-header-cell <prefix>SortHeader="createdAt">{{ 'recordsCreatedAt' | transloco }}</th>
```

The column is marked `sortable: true` in `columnsConfig`. The header cycles the sort and hands
the chosen one out by the `(sortChange)` event; the query itself is done by the screen. The
caption stays inside the button — the accessible name is taken from it.

The list arrives already sorted, so the screen passes the table the current sort —
`[sort]="sortModel()"` — and the arrow stands on the right column at once, before the first
press. Without it the list looks unsorted while it is sorted.

## Toolbar

The toolbar is split in two by slots: `<prefix>ToolbarLeft` — what changes the query,
`<prefix>ToolbarRight` — actions on the list. The screen sets up no layout of its own inside the
toolbar.

The left slot — filters and search. The right — `<prefix>-icon-button variant="primary"` icons
with a pair `tooltip` + `ariaLabel` of the same text: refresh (`sync`), column settings
(`sliders-v`), create (`plus`). If the list failed to load, the retry is the same refresh button.

## Loading refusal

```typescript
this.#notifications.error(this.#transloco.translate(this.#store.errorKey() ?? 'recordsLoadFailed'));
```

The key is read right after the request, not by subscribing to the store signal: the store is
shared by the list and the edit panel, and a subscription would show one refusal twice. No
`<p role="alert">` lines above the table.

## Check

```bash
npx nx build admin
```

The production build is mandatory: without `[<prefix>TableRowActionsRowType]` the type of
`let-row` is inferred as `unknown`, and only that build fails — units and the dev server pass.

## Common misses

- An own `@if (rows().length === 0)` — the screen was assembled bypassing the table.
- An own column list instead of `displayedColumns()` — the column with the menu disappears.
- Action availability computed by a component method — recomputed on every check.
- `[rowHasActions]` not set — the "…" button hangs on a row without actions.
- The title nested in the toolbar instead of its own `<header>`.
- `qa-dataid` not set on the table, the row, the cells and the toolbar elements.

## The slots of the shared page and the host token

A section of this tree. Between the screen and the kit stands the shared page view
`admin-list-page`: it declares the toolbar, the heading, the place for the table, the refusal with
a retry and the page switcher — not the screen. What is left for the section is to put its own
into the page slots and to name itself the host.

The whole screen is three things in the decorator and three in the template:

```typescript
@Component({
    selector: 'admin-proposals-list',
    imports: [AdminListPageComponent, AdminListToolbarLeftDirective, AdminTreeFilterComponent /* … */],
    providers: [provideAdminListHost((): typeof AdminProposalsListComponent => AdminProposalsListComponent)],
    host: { class: BEM_BLOCK },
})
export class AdminProposalsListComponent extends AdminListScreenBase<IProposal.Short.State, IProposal.Short.Api> {
    protected readonly title: string = adminLabel('sectionProposals');
    protected readonly hint: string = adminLabel('hintProposals');
    protected readonly qaPrefix: string = 'proposals';
    /* the store, the columns, the order fields and the table sign — as they were */
}
```

The class is passed to the provider by a call, not by value: providers are parsed together with
the decorator, when the class name is not bound yet, and one passed by value would fall with a
reference to something undeclared.

```html
<admin-list-page [hint]="hint" [qaPrefix]="qaPrefix" [title]="title">
    <ng-template adminListToolbarLeft>
        <admin-tree-filter [choices]="choices()" [tree]="query().tree" (treeChange)="changeTree($event)" />
    </ng-template>

    <rt-table #rowsTable="rtTable" clickable [attr.qa-dataid]="qaTable()" [dataSource]="rows()"><!-- … --></rt-table>
</admin-list-page>
```

There are three slots: `adminListToolbarLeft` — what changes the selection; `adminListToolbarRight`
— the section buttons; `adminListAboveTable` — what concerns the whole list at once. An unoccupied
slot does not appear on the screen at all and takes no height: a measurement on three sections
gives a gap between the toolbar and the table of exactly one page column step.

**The table is declared as a kit element, not as an attribute on one's own markup.** The kit has
one selector for two forms, and both build: `<table rt-table>` gives table semantics by the tag
itself, but the skeletons, the reading overlay and the narrow-screen cards it draws as nodes that
are never children of `<table>` — on that form they are not visible at all. The element form gets
its semantics by a role the kit sets itself: `role="table"` on the host, the row and cell roles
from CDK.

**The section anchors are assembled from its prefix, not written as a string at each element.**
The section names the prefix once by the field `qaPrefix`, from it the shared base gives
`qaTable()` and `qaRow()`, and the cells are assembled in place —
`[attr.qa-dataid]="qaPrefix + '-cell-tree'"`. Strings written out one by one drift from the prefix
silently: a spec that opened a neighbouring section finds its own anchor by them and passes green.

**An empty list shows an emptiness view, not a phrase in place of the rows.** The view is given by
the kit and only once the read is over: an icon, a heading and a second line about where the
records come from. In two lines, not one through a colon: the kit draws them as different nodes
and in different type.

```typescript
/* in the shared base the second line is one for the cargo sections, and the filter changes it */
protected readonly emptyDescription: Signal<string> = computed(() =>
    adminLabel(this.query().tree === '' ? 'listEmptyFrom' : 'listEmptyByFilterFrom'),
);

/* a section it does not suit overrides it with its own */
protected override readonly emptyDescription: Signal<string> = computed(() => adminLabel('listEmptyInvitesFrom'));
```

The view heading is the input `[emptyMessage]`, the second line is `[emptyDescription]`, the icon
is `[emptyIcon]`. The skeletons of an ongoing read and the refusal toast stay as they were: three
states — empty, reading, refused — are distinguishable on the screen, and one is not substituted
for another.

The page knows the prefix by the same word: from it the page assembles `<prefix>-hint`,
`<prefix>-columns`, `<prefix>-refresh`, `<prefix>-fault` and `<prefix>-retry`. The end-to-end suite
takes them by the helper `pageQa`, not by a string in place.

### Frequent misses of this layer

- Refresh or the column settings put by a section into the right slot — they are drawn by the
  page, and second buttons like them will stand next to the first.
- An input or an event added to the page for the sake of a new action — the action is asked of the
  host, and it is declared once in the host model.
- A host answer written in the screen itself — everything is answered by the shared list screen
  base; the screen only points at itself by a provider.
- An anchor `list-*` on the shared page — it is the same on every section, and a spec that opened
  the wrong section finds that very one.
- The phrase «no records» written in the template under `@if` by the list length — a screen
  assembled that way shows it during an ongoing read and after a refusal too: emptiness is told
  from them by the kit, not by an array length.
