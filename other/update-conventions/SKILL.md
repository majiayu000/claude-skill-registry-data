---
name: update-conventions
description: Use this skill when the user wants to change `docs/CONVENTIONS.md` or `docs/CHARTER.md`. Triggers on "let's change the convention for...", "update the rules", "amend the charter", "change our principles". Conventions and charter changes go through RFC review, not direct PR.
---

# Skill: update-conventions

Edits to `docs/CONVENTIONS.md` and `docs/CHARTER.md` are not normal PRs —
they change how everyone works in the repo. They go through RFC review.

## Procedure

1. **Push back if the user starts editing directly.** Conventions changes are
   high-leverage; they should be deliberated.

2. Open an RFC instead. Use the `new-rfc` skill, with the RFC scoped to
   "change conventions section X to Y". The RFC's *Proposal* section should
   contain the specific edited text — the diff, essentially.

3. After the RFC is accepted, the actual edit to `CONVENTIONS.md` is a small
   PR that cites the RFC in the commit footer:

   ```
   docs(conventions): adopt RFC-NNNN — <one-line summary>

   Implements RFC-NNNN: <link>
   ```

4. Update the RFC's *Follow-on artifacts* section to point at the merged commit.

## Exception

Trivial edits — typo fixes, broken-link fixes, formatting — don't need an RFC.
A normal PR is fine. If you're not sure, err toward RFC: the cost of an extra
RFC is small; the cost of an unannounced rule change is large.
