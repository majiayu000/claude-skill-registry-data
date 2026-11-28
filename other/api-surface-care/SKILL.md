---
name: api-surface-care
description: Treat any change to a shared interface as a contract change with consumers you cannot see. Use before renaming, removing, retyping, reordering, or changing the default of anything other code depends on — exported functions and types, HTTP routes and JSON fields, CLI flags and output formats, config keys, env vars, event or message schemas, DB columns, error codes, exit codes, and anything persisted or cached. Not for private helpers with only in-repo callers.
---

# api-surface-care

Private code has one consumer: the repo. Public surface has consumers you can't grep. Weak handling looks like a rename with every in-repo caller updated and a report saying "no breaking changes". Strong handling classifies the change before editing, keeps the old shape working or gives it a loud exit, and says which in the report.

Before changing one:

1. **Know which surface you're on.** Exported from the package, reachable over HTTP, parsed from a config file or env var, printed to stdout that scripts parse, stored in a DB, emitted onto a queue, returned as an error or exit code → contract. Renaming an internal helper is free; renaming a JSON field is a breaking change for every client.
2. **Classify before editing, and write it down.** Each surface change is one of: *additive* (new optional input, new output field), *narrowing* (accepts less or emits differently), or *breaking* (removes, renames, retypes, reorders, changes a default). Put the classification in the plan and the report. If you cannot classify it, you don't understand the change yet.
3. **Enumerate callers and paste the count.** Grep every in-repo caller, including tests, fixtures, docs, examples, and scripts — they encode what consumers expect. External consumers don't show up in grep: for libraries, published CLIs, and APIs, assume unseen callers exist and treat the change as public.
4. **Prefer additive evolution:** new optional parameter with a default, new field, new endpoint version. Widening what you accept and narrowing what you emit is safe; the reverse breaks people.
5. **Breaking changes need a path, not just a diff:** deprecate with a warning first where the ecosystem supports it, or version the surface (v2 endpoint, config `version:` key). Document the migration in the same change, and add the changelog entry the repo's convention expects.
6. **Watch the semantic breaks that look additive:** changing a default value, tightening validation on previously-accepted input, reordering enum values something serializes by index, changing error types or codes callers match on, making an optional field required, changing ordering or timing guarantees.
7. **Serialization is forever.** Anything persisted (DB rows, cached blobs, queued messages, files on disk) written in the old shape will be read by the new code — handle both shapes or migrate the data. Read one real old-shape record before assuming what it looks like.
8. **Exercise the old shape once.** After the change, call the surface the way an existing consumer would (old argument order, old field name, old config key). It must either still work or fail with a message that names the replacement. "Compiles" is not evidence; a test you updated alongside the change is not evidence either.

When the deliverable is a review of someone else's change, the same steps apply to their diff: classify each surface change, count their callers including the ones their sweep skipped, and list by name every consumer or claim you could not verify from the material rather than assuming it is fine. Then name the one check to run before merging (call the old shape, run the consumer's test, read the deploy config) as its own line.

Exit check: "could code I cannot see be depending on the exact behavior I just changed?" If yes, the change needs a compatibility story, and the report must name the classification, the caller count, and what happens to the old shape.
