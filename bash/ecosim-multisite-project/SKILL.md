---
name: ecosim-multisite-project
description: Sort EcoSIM run folders for a set of sites into one project directory with input/<SITE_ID>/ and run_dir/<SITE_ID>/ subdirectories and a project manifest. Use when asked to create EcoSIM run folders, runs, or cases for several sites at once ("create ecosim run folders for US-UMB, US-xGR, and US-Ha1", "set up a multi-site EcoSIM project"), or to add, refresh, or summarize sites in such a project.
---

# EcoSIM Multi-Site Project

## Use When

- The request names more than one site, or a project of sites.
- Sites already prepared one by one should be gathered into a single project.
- A project needs refreshing after a site's inputs or traits changed.

## Layout

```text
result/projects/<PROJECT>/
  input/<SITE_ID>/       the site's inputs (copy of result/<SITE_ID>/input/)
  run_dir/<SITE_ID>/     <SITE_ID>.namelist, input paths ../../input/<SITE_ID>/<file>
  project.json           manifest: per-site inputs, chronology, tracker, smoke, and trait status
  PROJECT.md             the manifest as a table
```

Each case stays self-contained: its own grid, climate, plant management, the
site-corrected PFT parameter copy, GHG, and microbial files. Backups
(`*.before_*`, `*.orig_*`, `*.prev_*`) are not copied.

## Workflow

1. Choose a project name (from the user, or a short descriptive one) and the
   site list.
2. Prepare every site with the single-site workflow
   (`ameriflux-namelist-generator` `references/runfolder_workflow.md`), each in
   `result/<SITE_ID>/` with its own progress tracker: data preparation, run
   folder, 2-year smoke run, and plant-trait correction. Sites are independent;
   report per-site problems instead of stopping the whole project.
3. Assemble the project:

   ```bash
   python .agents/skills/ecosim-multisite-project/scripts/assemble_project.py \
     --project <PROJECT> --sites US-UMB US-xGR [...]
   ```

   The script requires `result/<SITE_ID>/input/`, `run_dir/<SITE_ID>.namelist`,
   and a passed smoke run (`--allow-no-smoke` to override), copies the inputs,
   rewrites namelist paths to `../../input/<SITE_ID>/`, checks that every path
   resolves from `run_dir/<SITE_ID>/`, and writes `project.json` and
   `PROJECT.md`. It exits nonzero if any site was skipped or has path problems.
4. Report from `PROJECT.md`: one row per site with PFTs, chronology, climate
   years, stage status, smoke run, and trait findings, plus the sites left out
   and why.
5. To add sites or pick up changes, fix them in `result/<SITE_ID>/` and rerun
   the script with those sites; other sites in the manifest are kept. Model
   output already in a project run directory is kept unless `--replace-runs`.

## Full Runs

Only on request, run each case in its project run directory:

```bash
nohup python .agents/skills/ameriflux-namelist-generator/scripts/run_site_full.py \
  --site-id <SITE_ID> --run-dir result/projects/<PROJECT>/run_dir/<SITE_ID> > /dev/null 2>&1 &
```

The same rules apply as for single sites: one continued run on failure, then
report the error. Sites run independently; a failing site does not stop the
others. Each run writes `full_run_summary.json` in its run directory.

## Rules

- Do not edit inputs inside the project; change them in `result/<SITE_ID>/` and
  reassemble, so the single-site tracker, logs, and evidence stay the source of
  truth.
- Keep one PFT parameter copy per site; trait corrections are site-specific.
- A site missing data or failing its smoke run is reported, not silently dropped.
