---
name: stitch::code-to-design
description: >-
  Convert frontend code (Vite, React, etc.) to a Stitch Design by chaining
  static HTML extraction, design system extraction, and file upload. **ALWAYS** use this skill when the user's intent is to move existing web apps or React components into Stitch (e.g., requests to "save", "migrate", or "upload"). You must use this skill even for simple "save" operations, as it is the only way to ensure the design system is extracted and assets are properly linked.
allowed-tools:
  - "stitch*:*"
  - "Bash"
  - "Read"
  - "Write"
  - "web_fetch"
---

# Code to Design

Transform your existing frontend code into a Stitch Design so you can iterate and improve it using Stitch.

This skill orchestrates three other skills in sequence:
1. `extract-static-html`: Extract a single self-contained HTML file from your build output.
2. `extract-design-md`: Analyze the source code to create a design system (DESIGN.md).
3. `upload-to-stitch`: Upload that HTML file and the design system to your Stitch project.

## Workflow

Follow these steps to convert your existing code.

### Prerequisites

- A built web application directory containing `index.html` and assets.
- Target Stitch `projectId` (use `list_projects` if unknown).

### Steps

#### 1. Extract Self-Contained HTML

Delegate to the `extract-static-html` skill to generate a standalone HTML file.
Read [skills/extract-static-html/SKILL.md](../extract-static-html/SKILL.md) for detailed instructions and script usage.

Expected output: A single file like `/path/to/extracted/standalone.html`.

#### 2. Verify HTML (Optional — User-Driven)

After extraction, inform the user of the output file path so they can manually
verify in a browser if desired. **Do not block on verification** — proceed
directly to Step 3.

If the user reports issues after reviewing, fix them before continuing.

#### 3. Extract Design System (File)

Delegate to the `extract-design-md` skill to analyze the project's source files
(components, stylesheets, theme configs) and produce a design system. Read
[skills/extract-design-md/SKILL.md](../extract-design-md/SKILL.md) for the
full analysis workflow.

Write `.stitch/DESIGN.md` following the `extract-design-md` skill's output
structure.

#### 4. Upload DESIGN.md and Create Design System in Stitch

Delegate to the `manage-design-system` skill to upload the `DESIGN.md` and
create the design system in Stitch. Read
[skills/manage-design-system/SKILL.md](../manage-design-system/SKILL.md) for
the full workflow (upload script usage, `create_design_system_from_design_md`
call, and required schemas).

#### 5. Upload HTML to Stitch

Use the same `upload-to-stitch` skill's script to upload the extracted HTML file.
Read [skills/upload-to-stitch/SKILL.md](../upload-to-stitch/SKILL.md) for detailed instructions and script usage.

You will need:
- The path to the standalone HTML file generated in Step 1.
- Your Stitch API Key (same key used in Step 4).
- The target `projectId`.