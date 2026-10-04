---
name: pptx-edit
description: Inspect and make targeted edits to an existing PowerPoint PPTX with python-pptx, preserving its template and untouched content. Use pptxgenjs for new decks.
---

# Edit existing presentations

python-pptx 1.0.2 is preinstalled. Run Python scripts with `office-python`. Do not install packages. Materialize the source attachment, copy it into the workspace, and retain an original copy.

Open with `from pptx import Presentation; deck = Presentation(source_path)`. Inspect slide order, shape IDs, shape types, text runs, tables, charts, and relationships before making changes. Use existing shapes and runs to retain formatting. Assigning an entire text frame's text discards its run formatting; for a targeted text replacement edit the relevant runs. Do not recreate the whole presentation to make a small edit.

Save to a new workspace path. Verify requested edits landed and untouched media, themes, masters, embedded objects, and unsupported package parts survived. Render the original when needed to compare layout. python-pptx does not support editing every PowerPoint feature; report unsupported edits clearly rather than flattening or deleting content. Do not promise animation or interactive behavior based on static previews.

Generated artwork is a workspace asset: inspect the generate_image result and embed its path. Preserve image proportions and compare crops. Send only the requested deliverables.

Run validate_office_file, render_office_preview every slide, and record visual_reviews with the returned source_sha256. Check content, formatting, clipping, overlap, slide order, and the requested changes. Each edit invalidates the review. After three unsuccessful repair cycles explain the remaining blocker and keep the draft in the workspace. Use finish_response only when approved is true.
