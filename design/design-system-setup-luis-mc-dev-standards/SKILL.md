---
name: design-system-setup
description: Create and keep a project's design system under docs/design-system to DOCSPEC section 15 - README with the order of work, a next-version draft (ux-rules with rule IDs, components, tokens, content words, CHANGES, an offline review-visuals gallery), numbered read-only versions promoted only with a recorded owner approval, and guard-test templates per stack. Use when the user wants to set up, start, version, approve or promote a design system, add UX rules or tokens, build the review gallery, or add the design-system guard tests.
model: sonnet
effort: medium
---

# Design system - setup and keep

Runs `scripts/design_system.py` from the `luismc-docs` plugin (DOCSPEC section 15). Every command is a dry run until `--apply`.

```bash
S="${CLAUDE_PLUGIN_ROOT}/scripts/design_system.py"
python3 "$S" init --apply                  # docs/design-system/: README, approvals.json, next-version/ (never overwrites)
python3 "$S" styles                        # read-only: style files and CSS custom properties the project already has
python3 "$S" guards --apply                # guard tests into scripts/design/ (--stack typescript-vitest, --dest DIR)
python3 "$S" visuals                       # rebuild next-version/review-visuals/index.html: offline gallery with drawn swatches, contrast and every component (the session-start and stop hooks now do this when it is stale; running it by hand still works)
python3 "$S" check                         # DS1-DS5 findings (DS4 also flags a gallery from an older script); docs_check.py runs the same
python3 "$S" status                        # versions, the enforced one, approvals
python3 "$S" promote --approved-by owner --approved-on 2026-11-02 --evidence "chat, 2026-11-02"   # dry run; add --apply
python3 "$S" approve-implementation v1 --approved-on 2026-11-20 --evidence "chat" --apply
```

## Style reading (after init): show, ask, then fill

`init` writes a project-neutral starter (every item is a starter item to keep, change or delete before v1 is approved). Then read the project's own styles:

1. Run `design_system.py styles`. It lists design-token files, theme and Tailwind configuration, and CSS custom properties. It changes nothing.
2. Show the owner the files and values found. Ask once: "Use these values in the starter tokens?"
3. Only on yes: replace the matching token values in `next-version/tokens.md` (colours, fonts, spacing, radius). Keep the token names. Check WCAG 2.2 AA contrast of the new pairs. Add a `CHANGES.md` entry and rebuild the gallery.
4. On no, or when nothing is found: keep the starter values.

## Rules to follow

- Every design change, even a typo, goes into `next-version/`; write a `CHANGES.md` entry (`- C<n>: ...`) and rebuild the gallery.
- Never edit a numbered folder (`v1`, `v2` ...): it is read-only after approval and its digest is in `approvals.json`.
- Only the owner approves. Never run `promote` or `approve-implementation` on your own judgment: you need the owner's approval date and where it was given (the chat, a comment) and you pass them as `--approved-on` and `--evidence`. Show the gallery to the owner first. It draws colour swatches with WCAG contrast, type, spacing and radius samples, and every component, light and dark side by side. Read its "Token gaps", "Contrast failures" and "Not drawn" lists before you show it. Rebuild `next-version` only; a numbered version is never rebuilt.
- Apps follow the highest numbered version. UI work for a new version waits for the owner's approval of the version, an audit of the apps, and the owner's approval of the implementation.
- Rules carry IDs (`UX-<n>`); feature specs and code cite the ID and never copy the rule. Words users see live in `content.md` (DOCSPEC R11.3).
- Templates hold structure and a starter set of generic, project-neutral rules. Keep, change or delete each one; never import another project's rules.

## Guard tests

`guards` copies `design-system.ts` (finds the enforced version, computes the digest) and three tests: layout, freeze (digest and branch diff against `DESIGN_BASE`, default `origin/main`) and follow (retired words, rule table and citations, raw colours). Edit `CONFIG` at the top of `design-system-follow.test.ts` (source roots, extensions, token files). Make the test runner include `scripts/design/*.test.ts`. Other stacks: port the same three checks; the digest algorithm is in R15.5.

## Existing design system elsewhere

Move it to `docs/design-system/` with `git mv`, rewrite links and guard paths in one task (R15.8), add the earlier approvals to `approvals.json` by hand, then run `check`.
