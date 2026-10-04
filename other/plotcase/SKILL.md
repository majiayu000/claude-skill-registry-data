---
name: plotcase
description: Search local PlotCase bundled examples and launch the local PlotCase desktop app on Windows. Use this skill whenever the user explicitly asks to find PlotCase examples, search PlotCase images or plots, browse built-in PlotCase charts, open PlotCase, or start the locally installed PlotCase program. Prefer `academic-write-all-skill` as the first academic intake when the request is broad or mixed; use this skill as the dedicated downstream PlotCase example-search and GUI-launch path after AWAS has already fixed the plotting route.
---

# PlotCase Local Search + Launcher

Use this skill when the user wants either of these outcomes:

1. Search local PlotCase bundled examples by chart type, scenario, or visual style.
2. Launch the locally installed PlotCase desktop application.

## Search first, launch second

Because PlotCase does not expose a documented external CLI or API, the most reliable workflow is:

1. Search the local bundled examples first.
2. Return the most relevant example titles and paths.
3. Launch PlotCase only when the user wants to inspect or reproduce a result in the GUI.

## Search PlotCase examples

Use this command when the user asks to find matching PlotCase examples, chart images, or built-in templates:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "<USER_HOME>/.config/opencode/skills/plotcase/scripts/search_examples.ps1" -Query "森林图 临床"
```

If you want to consume the results programmatically or avoid terminal encoding issues, use JSON output:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "<USER_HOME>/.config/opencode/skills/plotcase/scripts/search_examples.ps1" -Query "森林图 临床" -OutputFormat Json
```

You can also filter by category or file extension:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "<USER_HOME>/.config/opencode/skills/plotcase/scripts/search_examples.ps1" -Query "论文风" -Category "森林图" -Ext ".xlsx" -OutputFormat Json
```

Good query patterns:

- 热图 / 火山图 / 森林图 / 小提琴图 / 网络图 / 游泳图
- 生存分析 / 临床 / 组学 / 差异分析 / 蛋白互作
- 适合论文 / 带显著性标记 / 多因素 / 进阶
- 论文风 / 医学风 / 临床图 / 组学图 / 发表图

The curated local example index is documented in:

- `references/examples-index.md`
- `assets/examples/examples.json`

## Rebuild the local example index

Use this command to regenerate the example index from the local PlotCase installation after upgrading PlotCase or changing the install path:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "<USER_HOME>/.config/opencode/skills/plotcase/scripts/generate_examples_index.ps1"
```

## Verify PlotCase before launch

Use this command to confirm the local executable path is still valid:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "<USER_HOME>/.config/opencode/skills/plotcase/scripts/verify_plotcase.ps1"
```

## Launch PlotCase

Use this command when the user explicitly wants to open the GUI:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "<USER_HOME>/.config/opencode/skills/plotcase/scripts/launch_plotcase.ps1"
```

## Expected behavior

- Search returns the best matching local PlotCase examples and their data paths.
- Verification confirms whether the configured `PlotCase.exe` path still exists.
- Launch starts PlotCase in a separate desktop process and returns quickly.

## If something fails

Check the following:

1. The PlotCase install directory still exists in Downloads.
2. The example paths in `assets/examples/examples.json` still match the local install, or rebuild the index with `generate_examples_index.ps1`.
3. Windows still allows PowerShell to launch the app.

If the PlotCase install path changes, update `scripts/verify_plotcase.ps1`, `scripts/launch_plotcase.ps1`, and regenerate `assets/examples/examples.json`.
