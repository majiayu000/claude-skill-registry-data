---
name: demo-app-critique
description: >
  Review a CommCare app as a demo (wording, module names, flow, teaching, images, icons) and write
  a numbered change list with questions. Use before making a demo version of an app. Needs the HQ
  app.
---

# Demo app critique

Reads an existing CommCare app the way a demo audience will meet it, judges it against
[`_demo-app-taste.md`](../_demo-app-taste.md), and writes a **numbered change list plus the
questions that block it**, so the reviewer can approve the list before anything is changed.
The rubric records Lily Olson's demo judgment from the 2026-10-26 Kangaroo Care session; read it
in full before the critique, every time. This skill does not paraphrase it.

This is the read-only half of a demo makeover. `demo-app-makeover` calls it at the start (to
build the plan) and at the end (to check the result). It can also be run alone on any app someone
is thinking of demoing.

## Inputs

| Parameter | Used for | Resolver |
|---|---|---|
| `hq_domain`, `hq_app_id` | the app to critique | explicit arg; else the Connect Demos project context doc's Apps |
| `server` | HQ cluster (`us` or `eu`) | explicit arg; demo spaces such as `connect-demo` are on `eu` |
| `audience` | who the worker is and where (drives § 1 of the rubric) | explicit arg; else the app's own content; else ask. Never invent it |
| `reviewer_notes` | the reviewer's raw notes, if any, verbatim | explicit arg; optional |
| `source_materials` | training decks or protocols the content should follow | explicit arg; optional |

No `run_state.yaml` is read or written. The app id is the whole contract.

## Products

- **Change list doc**, a rendered Google Doc in the Connect Demos project folder titled `<App> demo — planned changes and questions`, containing:
  - the app as found: home screen tiles, the module list in order, and screen counts per form;
  - the numbered changes, each tagged with the rubric section it serves (§1–§7) and marked **asked** (from the reviewer's notes) or **proposed** (found by this critique);
  - **teaching coverage**: a table mapping every certification-test question to the screen that teaches it and the check question that confirms it, rated strong, medium or weak (rubric §5);
  - **source conflicts**: every fact on which the app, its test, its images and the source materials disagree;
  - the questions, with the ones that block work listed first.
- A short reply summarizing the list, for the caller to send or post.

## Terminology

Everything this skill writes follows [`skills/_terminology.md`](../_terminology.md): **Connect**,
never "CommCare Connect", and US spelling.

## Process

1. **Read the rubric.** Read [`_demo-app-taste.md`](../_demo-app-taste.md) in full, including its
   § 8, since the reviewer's habits shape the questions you ask.
2. **Read the app live, in the order a worker meets it.**
   - `commcare_list_apps` for the domain: confirm the app and note its latest build and released build.
   - Fetch each form's source with `commcare_get_form_source(write_to_path=…)`, and read the module and form names and their order. Work from files on disk; never paste whole XForms into context.
   - Read any lookup tables the forms draw from (`commcare_get_lookup_table_rows`). A Learn test often draws its questions from a table, not the form.
   - List every image and icon each screen uses, and look at each one.
   - **On the EU cluster** the session-based `commcare_*` atoms can't sign in yet (ace#3299). Use a signed-in Playwright script that calls the same HQ endpoints, written in the scratchpad, never in the plugin cache.
3. **Judge each rubric section against what you read.**
   - For every finding, write: the screen or module, what it does now, the change, and the rubric section.
   - Cover all seven sections even when a section has no findings; say "none" so the reviewer knows it was checked.
   - **Rubric §5 needs the coverage table.** Map every test question to its teaching screen and check, and rate each: strong (taught and checked), medium (taught, not checked), weak (only implied).
   - **Rubric §6 needs your own eyes.** Open every image. Note skin tone, background, text inside the image, any detail the screen depends on, and whether the image agrees with its screen's text.
4. **Separate what the reviewer asked from what you propose.** Their notes are instructions:
   number them first, in their order, using their words. Your proposals come after them, each
   with a one-line reason.
5. **List source conflicts and blocking questions.**
   - A conflict is any fact the app, its test, its images and its source materials state differently. Name each value and where it appears.
   - A question blocks work only when the answer changes what gets built. Put those first.
   - For every other question, state the default you'll take if no one answers.
6. **Write the change list doc** with `canopy gdoc publish --agent ace --project "Connect Demos"`
   (or `skills/gdoc-writer`), and read it back to check it rendered.
7. **Return the reply:** the doc link plus a short summary of the changes and the blocking
   questions, in the reviewer's terms. Sending or posting it is the caller's decision, never this
   skill's.

## MCP Tools Used

- CommCare HQ (`ace-connect`): `commcare_list_apps`, `commcare_get_form_source`, `commcare_get_lookup_table_rows`, `commcare_download_ccz` (to check what a build actually packages)
- Google Drive (`ace-gdrive`): `drive_read_file` (source materials), `drive_list_folder`
- Publishing: `canopy gdoc publish` (CLI) via `skills/gdoc-writer`

## Mode Behavior

- **Auto:** writes the doc and returns the reply draft. It changes nothing in the app.
- **Review:** same. The caller decides whether to share the doc and send the reply.

## Related skills

- `demo-app-makeover`: builds the approved list and calls this skill again on the result.
- `app-review`: the build-quality review for apps ACE builds in `/ace:run`. This skill asks a
  different question: is the app right for a demo?

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-10-26 | Initial version, distilled from Lily Olson's Learn Kangaroo Care demo session (EU `connect-demo`, builds 31–99) | ACE, at Jonathan's request |
