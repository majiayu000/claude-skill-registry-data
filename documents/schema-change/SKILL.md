---
name: schema-change
description: Procedure for changing anything in pkg/schema — version bumps, fixture regeneration, compatibility diff, migrations, and MCP tool-definition sync. Use for ANY change to a wire shape, before touching pkg/schema.
---

# schema-change

Published schema versions are immutable (enforced by `scripts/schema-compat.sh`). This skill is the only sanctioned path for changing wire shapes.

## Decide: compatible or breaking?

- **Compatible** (new optional field, new schema type, doc changes): no version bump. Existing fixtures must not change.
- **Breaking** (field removed/renamed/retyped, semantics changed, required field added): new version. `foo.v1` stays; add `foo.v2`. **Requires Nick's sign-off — get it on the issue before writing code.**

## Procedure

1. Confirm the issue covers this change and (if breaking) has Nick's sign-off recorded on it.
2. Edit `pkg/schema`:
   - Breaking: add the new versioned type alongside the old one. Never edit or delete a published type.
   - Update the version registry / type dispatch if one exists.
3. Regenerate golden fixtures into `pkg/schema/testdata/`:
   - New fixtures for new versions. Existing fixture files must be byte-identical after regeneration — if one changed, you made a breaking edit to a published version; go back to step 2.
4. Run `./scripts/schema-compat.sh` and `go test ./pkg/schema/...` — both must pass.
5. **Sync consumers in the same PR:**
   - MCP tool input/output definitions in `internal/server` that reference the changed shapes.
   - Any REST/WS handler docs.
   - `docs/design/approval-object.md` if approval shapes changed.
6. If stored data is affected, ship a SQLite migration in the same PR (old rows must remain readable — the server may hold both versions live during transition).
7. PR: reference the issue, label `area/schema`, and add `approval-path` if approval shapes changed (Nick merges those).

## Never

- Mutate a published fixture to make the diff pass.
- Bump a version "while you're in there" without an issue and sign-off.
- Let MCP tool definitions drift from `pkg/schema` — same PR, always.
