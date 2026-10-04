---
name: book-manuscript-edit
description: Edit, rebuild, visually review, reverse-sync, and stage KDP upload for The Six Tongues Protocol and similar SCBE book projects. Use when asked to edit chapter prose, do a style pass, sync LibreOffice edits back to Markdown, rebuild the KDP DOCX, prepare a review packet, or keep the Markdown to DOCX to review to upload flow aligned.
---

# Book Manuscript Edit

Use this skill to keep book work moving through one clean lane:
- Markdown is the source of truth unless the user explicitly made changes in LibreOffice first.
- Build the review artifact from source.
- Review visually in LibreOffice.
- Sync back from DOCX only when the visual review introduced real edits.
- Treat KDP upload as the last step, after text and metadata are locked.

## Workflow

1. Lock the edit target.
- Identify the exact chapter, interlude, scene, or packaging task.
- Read the target files before changing anything.
- If the user asks for a style pass or prose changes, read `C:\Users\issda\.claude\projects\C--Users-issda\memory\feedback_writing_style.md` first.

2. Edit the real source first.
- Default source of truth: `C:\Users\issda\SCBE-AETHERMOORE\content\book\reader-edition\`.
- Read the matching file in `C:\Users\issda\SCBE-AETHERMOORE\content\book\source\` before mirroring edits there. Do not assume the text matches.
- Keep Markdown formatting stable:
  - `*italic*` for internal thoughts
  - `--` for em dashes
  - `* * *` for scene breaks
  - `# Title` for chapter headings

3. Rebuild the review manuscript.
- Run:

```powershell
cd C:\Users\issda\SCBE-AETHERMOORE
python content\book\build_kdp.py
```

- Expect output at `C:\Users\issda\SCBE-AETHERMOORE\content\book\the-six-tongues-protocol-kdp.docx`.
- Verify the build summary still reports roughly `150K+ words` and `43 sections`.

4. Open the review artifact in LibreOffice.
- Run:

```powershell
start "" "C:\Program Files\LibreOffice\program\soffice.exe" --writer "C:\Users\issda\SCBE-AETHERMOORE\content\book\the-six-tongues-protocol-kdp.docx"
```

- Use this lane for visual checks:
  - headings
  - page rhythm
  - ornaments
  - side art / cover placement
  - TOC and front matter
  - obvious formatting breaks

5. Reverse-sync only when DOCX edits happened.
- If the user edited prose in LibreOffice, run:

```powershell
cd C:\Users\issda\SCBE-AETHERMOORE
python content\book\sync_docx_to_md.py
```

- After sync, read the touched Markdown files and confirm the imported text is sane before rebuilding again.

6. Stage the KDP upload lane.
- Build the final `.docx`.
- Confirm title, author name, front matter, and cover asset path are correct.
- Gather metadata, categories, keywords, description, and pricing notes before opening KDP.
- Keep upload steps human-confirmed. Do not publish on assumption.

## Writing Rules

Apply these rules when editing prose for Issac's voice:
- Keep internal thoughts in italics.
- Prefer short sentences by default.
- Use longer sentences only when the thought genuinely needs more turns.
- Choose specific sensory language over generic description.
- Leave negative space where the reader can do work.
- Avoid pretension and system-jargon flattening.

## Output Contract

Return:
- which source files were edited
- whether `reader-edition` and `source` were both updated
- whether the KDP DOCX was rebuilt
- whether LibreOffice review was part of the run
- whether reverse-sync from DOCX was run
- whether the upload packet is only staged or actually ready

## Guardrails

- Read before editing. Never guess at manuscript text.
- Do not change chapter ordering. `INDEX.md` and `build_kdp.py` control that.
- Do not run publication/upload actions in the same breath as exploratory editing unless the user explicitly wants that.
- Run `sync_docx_to_md.py` before rebuilding only when LibreOffice introduced edits worth preserving.
- Treat Markdown as canonical for normal prose work.
- Keep build scripts unchanged unless the user explicitly asks for toolchain changes.
- Keep publication claims factual. If current KDP rules matter, verify them from official sources before giving upload guidance.

## References

- `references/project-paths.md`
  - Read for the exact repo paths, command snippets, and review loop.

- `references/kdp-upload-lane.md`
  - Read when staging metadata, final checks, and the manual KDP upload pass.
