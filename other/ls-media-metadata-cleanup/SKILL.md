---
name: ls-media-metadata-cleanup
description: "Inspect, remove, preserve, or update hidden metadata in photos, audio, and video before sharing, including batches and copyright fields. Produces verified copies while preserving originals; does not assess visible or audible sensitive content."
metadata:
  version: "1.0"
---

# Review hidden media metadata before sharing

**Purpose:** Help a user choose which hidden fields to retain, remove, or update,
then produce checked copies with their existing metadata tools. This is a guided
procedure, not a bundled codec, metadata editor, or privacy certification.

## Inspect and agree the changes

Resolve selected local files and an output directory. Reject ambiguous input
selection, symlink aliases back to originals, duplicate output names, existing
output collisions, or an output path that would overwrite an input. For batches,
prepare an explicit input-to-output mapping and resolve collisions before writing.
Do not recursively process an entire library unless that scope is requested.

Inventory installed metadata inspection/editing tools and their actual version,
format support, supported fields, and ability to write separate copies. Consult
installed help and primary tool documentation before constructing exact argv;
do not assume every photo, audio, or video container has the same metadata model.
A missing tool or unsupported writable format is blocked, not permission to install
software or upload files. Use the dependency owner if installation is authorized.

Read available metadata without modifying files. Keep raw GPS, device identifiers,
author names, private paths, thumbnails, and comments in private evidence. Show
field categories and redacted findings by default. Do not expose the metadata the
user is trying to remove in chat, logs, public manifests, or command strings.

Agree a field policy: retain, remove, or update for each requested category, such
as location, device/serial identifiers, author, comments, dates, embedded previews,
container tags, and copyright. Explain fields the selected tool cannot inspect or
change and secondary streams or embedded objects it does not cover. Do not imply
that clearing one tag namespace clears all embedded copies. Preserve legitimate
third-party copyright and attribution; confirm the rights holder before adding
ownership fields. Do not replace third-party credit with a default company credit.

## Produce copies and verify

1. Record input hashes and the agreed mapping privately. Prepare exact commands
   from the verified tool interface, using argv arrays and literal file operands;
   handle names beginning with option characters safely. Never interpolate media
   filenames or tag values into shell command text.
2. Write separate output copies in a protected directory. Prefer atomic final
   placement and fail on collisions. Tools that only edit in place must operate
   on newly created copies, never the originals. Preserve the original payload
   and quality when possible; disclose any required re-encoding before doing it.
3. Reread each output with the chosen inspection tool and compare the requested
   fields with the policy. Verify removals, updated values, and retained copyright
   or attribution. Check output readability and expected media streams/dimensions
   or duration. Compare input hashes again to confirm originals are unchanged.
4. Report each file as verified, partial, unsupported, or failed, with requested
   changes, retained fields, uncovered areas, and next action. A batch is partial
   if any member failed. Do not label an unreadable or uninspectable output clean.
   Keep failed outputs clearly separate from verified deliverables; remove only
   task-owned temporary copies when cleanup is authorized.

Return verified output locations and a concise sanitized summary. Hidden-metadata
review does not detect information visible in a photo or audible in a recording,
watermarks, OCR-readable text, or identifying content. It also does not certify
that a tool found every possible metadata structure. Sharing/uploading the copies
is a separate action requiring applicable disclosure authority.

## Validation scenario

Use a synthetic, nonprivate supported-format fixture when qualifying a tool:
add a location field and legitimate test attribution, remove location while
retaining attribution, reread the result, and confirm original hashes are unchanged.
Also check duplicate output paths and one unsupported batch member. Record the
actual tool/version and verification limits; package registration alone does not
qualify every editor or media format.
