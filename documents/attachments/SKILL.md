---
name: attachments
description: Discover, select, download, and inspect GitHub ticket attachments. Use when an issue or pull request contains screenshots, mockups, documents, or uploaded files needed as task context.
user-invocable: false
---

**Conversation-owning agent only**: selection requires user interaction in Step 2.
Never delegate this procedure to a worker/subagent that cannot surface questions to
the active conversation.

## Attachment Handling

After fetching the ticket, check for attachments that may provide additional context (mockups, design specs, API docs, screenshots, etc.).

### Step 1: Discover Attachments

If the calling skill already provides a discovered attachment list (e.g. from the `context-gatherer` digest), use it and skip the scan below — continue at Step 2.

Scan `body` and each `comments[].body` for URLs matching these domain patterns, embedded with either `![alt](url)` (image embed) or `[text](url)` (link) markdown syntax:
- `https://user-images.githubusercontent.com/...`
- `https://github.com/<owner>/<repo>/assets/...`
- `https://github.com/user-attachments/files/...`
- `https://github.com/user-attachments/assets/...`

**Note**: `user-attachments/assets/` URLs are often extensionless. If embedded with `![...]()` syntax, classify as **image**; if embedded with `[...]()` syntax, classify as **document** (file download).

Extract the display name (alt text or link text, fallback to filename from URL) and URL. Size is unknown until download.

**Note**: this display name is for presentation only (Step 2 prompt). It is issue-author-controlled and is never used as the on-disk download filename — Step 3 derives that separately and validates it.

If **no attachments found** → skip the rest of this procedure and return to the calling skill.

### Step 2: Present to User

Classify each attachment by extension:
- **image**: png, jpg, jpeg, gif, svg, webp
- **document**: md, txt, json, yaml, yml, csv, xml, html, log, pdf
- **binary**: everything else

Use the client's available user-input mechanism and allow multiple selections:

> "Found N attachment(s) on this ticket. Which would you like to download for context?"

Options (one per attachment if ≤ 4, grouped by type if > 4):
- `"<name> (<type>, <size>)"` per attachment when ≤ 4
- `"All images (N)"`, `"All documents (N)"`, `"All other files (N)"` when > 4

If user selects none → skip the rest of this procedure and return to the calling skill.

### Step 3: Download Selected Attachments

Store downloads under a freshly created, atomically-unique private directory —
never a shared, predictable path, which would let a symlink be pre-planted at a
guessable resolved download filename before the run starts. Create it as its
own standalone Bash call — never a shell-variable assignment that captures
the command's own output (an assignment wrapper never matches a granted
`Bash(mktemp -d:*)` prefix, and `shell-rules` forbids command substitution
where the agent can run the command and read the result):

```bash
mktemp -d "${TMPDIR:-/tmp}/cenci-attachments-XXXXXX"
```

`mktemp -d` both creates the directory and guarantees its name is unique and
unpredictable, so concurrent runs never collide and nothing can pre-plant a
symlink at it — no `<scope>` subdirectory is needed for uniqueness.

**Verify before downloading**, as its own standalone Bash call:

```bash
test -d "<attach-dir>"
```

Confirm the command succeeded and the printed directory is a non-empty,
existing directory before any download proceeds. If `mktemp -d` fails (disk
full, unwritable `TMPDIR`, etc.), abort the entire attachment step rather than
continuing with an unverified directory.

**Carry the printed path forward as the literal text `<attach-dir>`** for
every reference in the rest of this step; do not hold it in a shell
variable. Bash-tool shell state does not persist between calls, so a
shell-variable reference to a directory captured earlier would expand to
empty in a later, separate Bash call, and every path built from it would
silently collapse to an absolute root-relative path — precisely the hazard
the verification above guards against. This mirrors `refine/SKILL.md`'s
per-run `<token>` rule: carry the literal value forward as text, never
re-derive it or rely on shell state across calls.

Prefer a connected GitHub attachment-download tool when one is available, especially
for private `user-attachments` URLs. Otherwise use `curl`. Before downloading, resolve
a safe on-disk filename for each attachment — never the Step 1 display/alt text, which
is issue-author-controlled and presentation-only, not a trusted filesystem input:

1. **Derive a basename from the URL.** Strip any `?query` and `#fragment`, then take
   the last `/`-separated path segment of what remains. Do not percent-decode this
   segment — decoding could re-introduce `/` or `..` sequences that the raw segment
   didn't contain.
2. **Validate the basename.** It must match `^[A-Za-z0-9._-]+$`, must not be exactly
   `.` or `..`, and must not contain `..` anywhere — the same rule used for scope keys
   in the `shell-rules` skill (do not weaken this to a bare character-class check).
   Then cap its length: if the validated basename exceeds 200 characters, truncate
   the stem (everything before the last `.`) so `stem+ext ≤ 200`, preserving the
   extension unchanged — a conservative cap that leaves headroom below common
   `NAME_MAX` (255) filesystem limits for the `-<k>` collision suffixes applied later.
3. **Fall back if invalid, absent, or extensionless.** Generate `attachment-<n>`
   (where `<n>` is the attachment's 1-based index within the current run's selected
   set — stable and deterministic, not a global counter) when the basename fails
   validation, when the URL has no last path segment at all, or when the segment is
   valid but has no extension — no `.` in it (e.g. extensionless
   `user-attachments/assets/<uuid>` URLs). An extensionless basename cannot satisfy
   Case A below, which requires the extension to already be known before download;
   Content-Type sniffing in Case B supplies it instead. Never fall back to the raw
   invalid value and never to the Step 1 display/alt text.
4. **Resolve and download — the sequencing differs by which path produced the name,
   because a fallback name's extension can only be known after the response arrives:**

   - **Case A — valid URL basename** (step 2 validation passed). The filename,
     including its original extension, is already fully known before any download
     starts — no sniffing applies. Check it for a collision against files already
     written this run in `<attach-dir>`; if it
     collides, append `-<k>` before the extension, starting at `k=2` and incrementing
     until unique (e.g. `report.pdf` → `report-2.pdf`). For a multi-dot name, split on
     the *last* `.` only — the extension is everything after the final dot, so
     `archive.tar.gz` → `archive.tar-2.gz`. Then download straight to the resolved
     name:

     ```bash
     curl -fsSL "<url>" -o "<attach-dir>/<resolved-filename>"
     ```

   - **Case B — fallback (`attachment-<n>`)**. The extension is unknown until the
     response's Content-Type is inspected, so the collision check and final name
     cannot be resolved before downloading:
     1. Download to a provisional, extension-less path using the fallback name,
        capturing the response's Content-Type via curl's write-out format (or the
        connector tool's response, if used instead):

        ```bash
        curl -fsSL "<url>" -w '%{content_type}' -o "<attach-dir>/attachment-<n>.partial"
        ```

        If this download reports failure (non-zero curl exit, or the connector tool's
        equivalent failure signal), discard the `.partial` file and do not proceed to
        steps 2–4 — this is a download failure for this attachment: apply the "On any
        download failure → warn and continue with remaining files" rule below.
     2. Map the captured Content-Type to an extension: `image/png`→`.png`,
        `image/jpeg`→`.jpg`, `image/gif`→`.gif`, `image/webp`→`.webp`,
        `image/svg+xml`→`.svg`, `application/pdf`→`.pdf`, `text/plain`→`.txt`,
        `text/markdown`→`.md`, `application/json`→`.json`, `text/csv`→`.csv`,
        `text/html`→`.html`, `application/xml` or `text/xml`→`.xml`. An unknown or
        missing Content-Type means no extension is appended.
     3. Check the extension-bearing name (`attachment-<n><ext>`) for a collision
        against files already written this run in the same directory; if it
        collides, append `-<k>` before the extension, starting at `k=2` and
        incrementing until unique.
     4. Move the provisional file to the final resolved name with a portable `mv`
        (no bash-only construct):

        ```bash
        mv "<attach-dir>/attachment-<n>.partial" "<attach-dir>/<resolved-filename>"
        ```

        If this `mv` fails (disk full, permissions, etc.), treat it as a download
        failure for this attachment — apply the same "On any download failure → warn
        and continue with remaining files" rule; never leave the `.partial` file in
        place as a substitute and never read/inspect it directly under its
        provisional name.

If a private-repository download fails and no connector can download it, retry with
the authenticated GitHub CLI token without printing the token.

Post-download: check size with `stat`. If > 10 MB and user wasn't warned → report and skip that file.

On any download failure → warn and continue with remaining files.

### Step 4: Load Attachment Content

For each downloaded file, use the client's matching file or image inspection tool:
- **Images** (png, jpg, jpeg, gif, webp): use multimodal image inspection
- **SVG**: read as text unless visual rendering is specifically needed
- **Text files** (md, txt, json, yaml, yml, csv, xml, html, log): read as text
- **PDF**: use the client's PDF reader or extraction support
- **Binary/other**: Report file path, note content cannot be read as text

**After reading each image**, produce a brief structured summary (5–15 lines) covering applicable aspects:
- **Type**: mockup, wireframe, screenshot, diagram, flowchart, error state, etc.
- **Layout**: overall structure, regions, and spatial arrangement
- **UI elements**: buttons, inputs, tables, navigation, modals, etc. — include their labels
- **Text content**: headings, labels, error messages, data values visible in the image
- **Visual style**: colors, spacing, typography, and key design details
- **Annotations**: arrows, callouts, numbered markers, or highlighted areas

Keep all attachment context available for the rest of the calling skill's execution.
