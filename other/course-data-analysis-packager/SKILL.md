---
name: course-data-analysis-packager
description: Experimental skill for creating, organizing, or reviewing a reproducible course or class-project data analysis package from datasets, assignment requirements, rubrics, research questions, scripts, notebooks, CSV/Excel files, charts, reports, and slide outlines. Use for student/course deliverables that need a clean folder structure, data dictionary, analysis scripts, visual outputs, report template, PPT outline, README, execution commands, and quality checks.
---

# Course Data Analysis Packager

Use this skill to turn a course topic and dataset into a complete, reproducible analysis deliverable. The expected result is a folder that another student, teacher, or teammate can understand, run, and present.

Status: experimental. For the first real use on a new course assignment type, produce a package plan first and ask for confirmation before creating many files, moving data, or rewriting an existing project.

## Core Workflow

1. Clarify the assignment:
   - course, topic, deadline, required format, rubric, data source, group role, expected depth, and whether AI assistance is allowed.
   - if rules are missing, preserve uncertainty rather than inventing requirements.

2. Inspect data and sources:
   - identify raw files, schemas, missing values, duplicate rows, text fields, categorical fields, numerical fields, and privacy-sensitive columns.
   - for spreadsheets, use structured readers instead of ad hoc text parsing.

3. Define the research question:
   - make it narrow enough to answer with available data.
   - include comparison dimensions such as group, city, platform, time, user segment, topic, or risk level when useful.

4. Create the package structure:
   - read `references/package-structure.md` before creating or reorganizing files.
   - keep raw data separate from processed data.

5. Build the analysis plan:
   - choose metrics, charts, tables, assumptions, and limitations.
   - read `references/analysis-workflow.md` when writing scripts or notebook steps.

6. Produce deliverables:
   - README, data dictionary, analysis scripts/notebooks, output tables, figures, report template, and PPT outline.
   - keep figures directly usable in slides.

7. Run QA:
   - read `references/deliverable-qa.md` before final delivery.
   - verify commands run, outputs exist, claims match data, and privacy-sensitive fields are not exposed unnecessarily.

## Output Modes

- `package-plan`: propose folder structure, research question, metrics, scripts, and deliverables.
- `build-package`: create or edit the actual folder package.
- `review-package`: inspect an existing package for missing files, weak claims, broken scripts, or presentation gaps.
- `ppt-outline`: turn analysis results into a slide-by-slide presentation outline.

## Default Folder Contract

```text
project_name/
  README.md
  data/
    raw/
    processed/
  docs/
    data_dictionary.md
    report_template.md
    ppt_slide_outline.md
  scripts/
  notebooks/
  output/
    tables/
    figures/
```

Use this as a default, but adapt to the existing project if it already has a coherent structure.

## Writing Rules

- Use Chinese by default for Chinese course deliverables.
- Keep method names, data fields, and package names in English when that improves precision.
- Do not overclaim causal conclusions from descriptive or observational data.
- State missing data and sampling limits plainly.
- For platform or social-media data, include ethics and compliance notes when scraping, cookies, personal data, or platform rules are involved.
- Prefer simple, defensible analysis over complicated models that cannot be explained in class.

## Final Response Contract

When delivering a completed package, report:

- folder path;
- key files created or updated;
- commands to reproduce;
- main charts/tables produced;
- remaining assumptions or limitations;
- what still needs manual verification.
