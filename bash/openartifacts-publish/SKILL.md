---
name: openartifacts-publish
description: Publish, update, or withdraw an existing Markdown note as a public OpenArtifacts page. Use when the user asks to publish, share, update, delete, remove, or withdraw an OpenArtifacts page.
metadata:
  copilot-enabled-agents: opencode, claude, codex
  copilot-builtin-version: "2"
---

# Publish Markdown to OpenArtifacts

Copilot supplies everything this skill needs through the environment:
`$OPENARTIFACTS_WORKSPACE_ROOT` is the vault root, and `COPILOT_PLUS_LICENSE_KEY`
is the credential the bundled wrapper sends. Do not read Copilot settings or credential
files, print the key, install anything, or run Node, npm, npx, or the Obsidian CLI.

If `COPILOT_PLUS_LICENSE_KEY` is unset or empty, stop before generating anything and tell
the user: Publishing to OpenArtifacts needs a Copilot Plus license key. Add it in Copilot Settings and try again.

## 1. Prepare the page

Read one existing Markdown source note. Treat YAML frontmatter as metadata, never as page
content. Note its `openartifacts` property, or on older notes the `symposium` property:
an `https://…/d/<docId>` value means the note is already published and this task updates
that page; pass that `docId` to the wrapper. Compare document ids, not urls: an older
`symposium.site` link and an `openartifacts.site` link with the same id are the same page.
If either property holds any other value, or the two name different ids, stop and ask the
user before touching them.

Write complete UTF-8 HTML (at most `10485760` bytes) to a new file
under `$OPENARTIFACTS_WORKSPACE_ROOT/.openartifacts/handoffs/`, creating
the directory if needed. Preserve the note's content; render Obsidian-specific syntax such
as wikilinks, callouts, embeds, Mermaid, and Bases into static HTML or SVG. CSS, scripts,
and external resources are allowed and are published unchanged.

Themes are optional. For a named theme, check
`$OPENARTIFACTS_WORKSPACE_ROOT/.openartifacts/themes/<name>.md`, then
`themes/<name>.md` next to this skill. Check each path independently. If neither
exists, continue with readable defaults; a missing theme must never block publishing.
The bundled `research-memo` is an optional example.

## 2. Let the user review

Tell the user the absolute path of the HTML file and that opening it in a browser shows
the page as it will be uploaded; OpenArtifacts adds its own header and footer bylines when
it serves the page. Then end your turn.

Never publish in the same turn that generated the HTML. Publish only when a later
message from the user clearly asks to publish this page. Treat anything else as feedback
(revise the same file and repeat this step) or as a cancellation. When unsure whether a
message is an approval, ask once. Never simulate the user's approval.

## 3. Publish

Run the wrapper next to this SKILL.md with the HTML file, the note's title (its file
name without `.md`), and the existing `docId` when updating. On macOS or Linux:

```bash
sh "/absolute/path/to/this/skill/directory/openartifacts-publish.sh" publish "$OPENARTIFACTS_WORKSPACE_ROOT/.openartifacts/handoffs/unique.html" "Note title" [docId]
```

On Windows, use the `.cmd` wrapper (prefix with `&` in PowerShell):

```powershell
& "/absolute/path/to/this/skill/directory/openartifacts-publish.cmd" publish "$env:OPENARTIFACTS_WORKSPACE_ROOT/.openartifacts/handoffs/unique.html" "Note title" [docId]
```

Success prints the server's JSON, `{"docId", "url", "version"}`. Set the note's
`openartifacts` frontmatter property to that `url` (create the frontmatter block if
needed, keep every other property) and remove a `symposium` property whose link has the
same document id. Delete the HTML file from `.openartifacts/handoffs/`, then
report the URL. Publishing the same note again updates the same page.

On failure the wrapper prints the HTTP status and the server's message to stderr and
exits 1. Report that message verbatim. Do not retry on your own, invent a cause, strip
styling, or publish another way. For a 401, the license key was refused or the plan
cannot publish; point the user at Copilot Settings. For `not_found` on an update, stop;
do not create a replacement page unless the user explicitly asks.

## 4. Withdraw

For delete, remove, or withdraw requests, read the `docId` with the same rules as step 1:
`openartifacts` first, `symposium` on older notes, compared by document id, and stop to
ask on any other value or on two properties naming different ids. If there is none, say
nothing is published. Otherwise tell the user the link will stop working and that copies
people already saved cannot be recalled, then end your turn. On a clear yes, run the wrapper
with `unshare <docId>`, remove the `openartifacts` and `symposium` properties from the
note, and report that the page is gone. Never tell the user to delete the page at its
public URL.
