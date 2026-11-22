---
name: ng-ag-grid-developer
description: 'Build or modify Angular components with AG Grid Enterprise. Use when a task mentions ag-grid.'
license: MIT
---

## Basic Rules

- Verify the version first: `npm ls ag-grid-angular ag-grid-enterprise` (both must match)
- Enterprise standard — use `AllEnterpriseModule`, never `AllCommunityModule` alone; cherry-pick modules in production to cut bundle size
- `LicenseManager.setLicenseKey()` **before** `ModuleRegistry.registerModules()`, both before any grid renders
- `AgGridAngular` is standalone — add it to the component's `imports`
- Type rows: `GridOptions<T>`, `ColDef<T>`; set `getRowId` for stable row identity

## References

Load the file for the task at hand. Paths are relative to this skill's directory.

| Topic                   | File                                   | Load when                                                                                                    |
| ----------------------- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Setup, license, modules | `references/setup.md`                  | First-time setup, registering or cherry-picking modules                                                      |
| AG Grid MCP server      | `references/setup.md` § `ag-mcp`       | Using `ag-mcp` (client config files: MCP reference of `ng-implementation`); looking up version-specific docs |
| Columns, generics       | `references/column-definitions.md`     | `ColDef`, `columnTypes`, value getters/formatters, typed events, `getRowId`                                  |
| Row models              | `references/row-models.md`             | Client-side vs SSRM, datasource, large datasets                                                              |
| API, events, filtering  | `references/api-events-filtering.md`   | Grid API access, `setGridOption`, events, column/quick/external/advanced filters                             |
| Renderers, editors      | `references/cell-rendering-editing.md` | Custom Angular cell renderers/editors, `editable`                                                            |
| Grouping, pivoting      | `references/grouping-pivoting.md`      | `rowGroup`, `aggFunc`, `pivotMode`, side bar                                                                 |
| Master/detail           | `references/master-detail.md`          | `masterDetail`, detail grids                                                                                 |
| Excel export            | `references/excel-export.md`           | `exportDataAsExcel`, styles, multiple sheets                                                                 |
| Theming, layout         | `references/theming.md`                | Themes, CSS variables, `domLayout`, row height                                                               |

## Gotchas

- **`LicenseManager` before `ModuleRegistry`**: otherwise enterprise features may not activate correctly
- **Modules before grid instantiation**: register globally (`main.ts` / `app.config.ts`); modules registered after creation are ignored
- **`autoHeight` performance**: never `domLayout='autoHeight'` for grids > 1 000 rows
- **Initial options**: options marked `[Initial]` (`rowModelType`, `treeData`, `masterDetail`) cannot change after creation — destroy and re-create
- **SSRM and client-side are mutually exclusive**: a grid uses one row model
- **Pivot requires aggregation**: every value column needs an `aggFunc`
- **Cherry-picked modules**: always include `ClientSideRowModelModule` (or `ServerSideRowModelModule`) explicitly
