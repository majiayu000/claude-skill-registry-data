---
name: block-scaffolding-from-design
description: Use when an approved kivo-creator match plan must be emitted - writing the page as block markup, scaffolding the blocks that were missing in the project's conventions (run the project's generator first, then review and copy the prepared files), turning unmatched design values into token proposals and importing media. For deciding which block a section uses use section-matching; for checking the rendered result use visual-fidelity.
license: MIT
compatibility: Node 20+. Project commands go through the runner from the kivo-wise session context. emit.mjs writes only under .creator/<run>/.
---

# Block scaffolding from design

Emit an approved plan. Existing blocks are filled; missing blocks are generated with the project's own generator and then completed with files prepared from the spec.

Runner placeholders (`{{runner.wp}}`, `{{runner.acorn}}`, `{{runner.cache}}`) come from the kivo-wise session context. Never run `wp`, `composer`, `php` or `npm` on the host.

## When to use

- The person approved `match-plan.md`.
- "Generate the missing blocks", "build the page from the plan".
- Not for changing the plan (`section-matching`) or judging the result (`visual-fidelity`).

## Inputs required

1. `.creator/<run>/match-plan.json` that passes `match.mjs --check`.
2. The project root and its runner (session context).
3. The kivo-creator plugin root (two levels above this skill's folder).

## Procedure

1. Emit: `node <kivo-creator>/scripts/emit.mjs --run=.creator/<run> --project=.`. It writes `page.html` (block markup), `scaffold/<project paths>` and `emitted.json` (`files`, `commands`, `media`, `gaps`, `proposals`, `notes`, `blockType`, and the section `selector` verify uses). New blocks follow the project's existing block type, not the profile: ACF Composer classes when the project's blocks are ACF, `block.json` when they are native (`blockType`: `type`, `source` = `override` | `count` | `asked`, `counts`). Existing blocks keep their own markup, so one page can mix both. If emit refuses with `New blocks need a block type`, go back to `/creator`: the person chooses once and the answer is recorded with `block-type.mjs --set=` or passed as `--blocks=`. Nothing in the project changes yet. When the project's existing blocks do not print `data-block`, add `--selector=<css>` for the wrapper they do print.
2. Token proposals first. Show `emitted.proposals` (value, role, suggested token). Add a token to the `@theme` block only when the person agrees, then run step 1 again so the views use the new utility. Never put a literal value or an arbitrary class (`text-[13px]`) in markup to avoid this step.
3. For each new block, in order:
   1. run the project's generator with the runner, exactly as listed in `emitted.commands` (for example `{{runner.acorn}} acf:block Stats --no-interaction`);
   2. show the difference between the generated files and `scaffold/<path>` as a diff;
   3. check what the prepared view assumes. ACF textarea fields follow the kivo-wise escaping rule `@textarea(...)` when emit finds `Blade::directive('textarea', …)` in the project's own code; otherwise the view uses `{!! nl2br(e(...)) !!}` and `emitted.notes` says so. Keep that fallback (it is not the forbidden `nl2br(esc_html())`), or, if the directive comes from a Composer package emit cannot see, switch back to `@textarea(...)`. Any other directive the view uses must exist in the project; if one does not, ask before changing the escaping;
   4. copy the reviewed files over the generated ones;
   5. native blocks (`blockType.type` is `native`, on any profile): `emitted.commands` is empty. If `{{runner.acorn}} list` shows a `make:block` generator, run it first and compare; otherwise copy `block.json`, the view and the CSS notes, then follow `emitted.notes` for the registration and the editor script, matching how the existing blocks do it.
4. Rebuild caches: `{{runner.acorn}} acf:cache` (or `{{runner.cache}}`) so ACF Composer picks up the new fields.
5. Media: for each `emitted.media` entry, import the file (`{{runner.wp}} media import <src> --porcelain`) and put the attachment id in place of `null` for that field in `page.html`. Ask before importing remote files you do not recognise.
6. Run the project's own checks on the new files (code style, static analysis, tests), as the project defines them.
7. Report: blocks filled, blocks created (with paths), gaps with their reasons, tokens added or still proposed, media imported. Then hand over to `visual-fidelity`.

## Verification

- `git status` shows only the new block files, the `@theme` lines the person approved and nothing else.
- The project's checks pass on the new files.
- `page.html` has no `null` image ids left, or the report lists each one.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `the match plan is not approved yet` | Open, low-confidence or invalid decisions | Go back to `section-matching` |
| `New blocks need a block type` | Mixed project or no blocks yet, and no `creator.blocks` / `--blocks` | Ask the person once (recommend `blockType.recommended` when there are no blocks); record it with `block-type.mjs --set=` or pass `--blocks=` |
| Generator command not found | The project has no ACF Composer generator or uses its own stubs | Run `{{runner.acorn}} list`; use the project's generator; if there is none, ask before creating files by hand |
| New fields missing in the editor | ACF Composer manifest not rebuilt | `{{runner.acorn}} acf:cache` (or `{{runner.cache}}`) |
| A view uses a directive the project lacks | The directive is registered somewhere emit does not scan (a Composer package) or not at all | For `@textarea`, the fallback `{!! nl2br(e(...)) !!}` is safe; for anything else ask, do not swap in a different escaping on your own |
| A proposal keeps coming back | The token was added under another name or namespace | Use the suggested namespace (`--color-*`, `--text-*`) so the mapper finds it |

## Escalation

Ask before adding any `@theme` token, before importing media from an unknown host, and whenever a generated block would duplicate an existing one with a different style.
