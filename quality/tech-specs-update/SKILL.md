---
name: tech-specs-update
description: Update the related tech specs and requirements as part of planned work. Invoke only when explicitly called by user.
user-invocable: true
disable-model-invocation: false
---
# Update Tech Specs

Update the related tech specs and requirements as part of planned work, in the same change as the behavior they describe.
A change that leaves a canonical document describing the old behavior is not complete.

## Identify What the Change Touches

- Locate every requirement, technical specification, architecture document, and feature file that describes the behavior being changed.
- Search by identifier, anchor, and domain term, not only by filename, because a single behavior is usually described in more than one place.
- List what you found before editing, and say explicitly when a change touches no canonical document.

## Decide Before Editing

- Confirm that the change is authorized to alter the specification, not just the code.
  Specs lead and code follows: if the implementation now contradicts an approved spec, that is a code gap to surface, not a document to quietly rewrite.
- Stop and ask for direction when the change would weaken a requirement, alter an external contract, or resolve a contradiction between canonical documents.

## Apply the Update

- Follow the repository's own authoring standards for the document being edited.
- Preserve identifiers, anchors, and traceability links; update inbound and outbound references in the same change.
- Keep obligation strength intact: do not downgrade a requirement to an example or drop an edge case because the new implementation does not cover it.
- Update indexes and cross-references so the documents stay navigable.

## Validate

Run the repository's documentation lint, link check, identifier validation, and traceability checks over the changed files.
Report what ran, what failed, and any check that could not be performed.
