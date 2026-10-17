---
name: skogai-routing
description: "SkogAI routing use when authoring, reading, scaffolding, validating, listing, or explaining SKOGAI.md/CLAUDE.md router files, xml-blocks, route XML tags, or @-link routing."
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/scripts/validate_router.py *), Bash(${CLAUDE_SKILL_DIR}/scripts/list_routers.py *), Bash(${CLAUDE_SKILL_DIR}/scripts/list_xml_tags.py *)
---

<output>

- list_routers.py: !`${CLAUDE_SKILL_DIR}/scripts/list_routers.py`
- list_xml_tags.py: !`${CLAUDE_SKILL_DIR}/scripts/list_xml_tags.py`

</output>

For how these `!`command``lines actually execute (permission gating via`allowed-tools`, why `${CLAUDE_SKILL_DIR}`matters, plugin cache gotchas, and
how subagents that preload this skill can answer with zero tool calls without
fabricating), see`references/dynamic-output-blocks.md`.

# SkogAI Routing

A router document is YAML frontmatter plus one XML root block. In v1, `type:
router` pairs with `<routes>`. `CLAUDE.md` and `SKOGAI.md` use the same document
shape at different levels of the routing chain.

Load `references/router-file-convention.md` when the task needs the exact v1
schema, examples, loading model, or boundary between implemented router behavior
and future document types. Load `references/claude-md-routing-rules.md` when
deciding whether a route should be an `@`-link or a plain path. Load
`references/at-linking.md` only for Claude Code `@`-link mechanics.

## Reading Frontmatter

Use `${CLAUDE_SKILL_DIR}/scripts/parse-frontmatter.sh <file> [field]` to extract
the YAML frontmatter block (or a single field from it) from a routing file —
adapted from plugin-dev's `plugin-settings` frontmatter parser.

## Validating A Routing File

Use `${CLAUDE_SKILL_DIR}/scripts/validate_router.py <file...>` to check one or more files against
`schemas/router.schema.json`: frontmatter parses as YAML, `type` equals
`router`, only the v1 frontmatter fields are present, and the body contains
exactly one attribute-free `<routes>` XML block whose nonblank lines are list
entries. Explicit targets are fail-closed: missing/malformed frontmatter,
another document type, extra fields, or an invalid body all exit nonzero. It's
a single `uv run --script` executable (schema path resolved relative to its own
location via `Path(__file__)`) — there's no separate shell wrapper, since a
wrapper would only exist to loop over args and resolve paths, both of which
Python already does natively.

Self-check, run live every time this skill loads (proof the validator and the
bundled example still agree, not just a description of the command):

- Bundled example: !`${CLAUDE_SKILL_DIR}/scripts/validate_router.py ${CLAUDE_SKILL_DIR}/examples/SKOGAI.md.example`

When the user asks to validate SKOGAI.md/CLAUDE.md routing files:

1. Resolve targets from the user's request: a given file path, or if a
   directory (or nothing) is given, use `list_routers.py` under that directory
   (default: cwd) to discover router candidates. Complete when every intended
   target path is explicit.
2. Pass only those discovered candidates, or the user's explicit target paths,
   to the validator. Discovery skips non-router and unparseable Markdown;
   explicit validation fails either case.
3. Run `${CLAUDE_SKILL_DIR}/scripts/validate_router.py <file...>`.
4. Report PASS/FAIL per file. For any FAIL, quote the specific schema
   error so the user knows exactly what to fix (e.g. missing `<routes>`
   section, `type` not `router`, missing frontmatter). Complete when every
   target has a PASS/FAIL line and every FAIL includes the validator reason.
   Don't auto-fix failures — report them and let the user or a follow-up edit
   fix the file.

## Finding all router files in a project

Use `${CLAUDE_SKILL_DIR}/scripts/list_routers.py [root_dir] [-o output_file]` to recursively scan
a project for router documents: it walks every `*.md` file under `root_dir`
(default: cwd; skips `.git`/`node_modules`), parses frontmatter, and prints
the relative path of each file where `type: router`. This is a cheap
frontmatter-only scan (no schema validation) — its job is discovery ("what
router files exist here"), not correctness ("are they valid"); pipe the
result into `validate_router.py` for that. Files with missing, malformed, or
non-mapping frontmatter are ignored by discovery rather than aborting the scan.

When the user asks to list/find/inventory routing files across a project:

1. Resolve `root_dir` from the user's request, else the current working
   directory (or `${CLAUDE_PROJECT_DIR}` if the user means "this whole
   project" specifically, since that's the substitution that resolves to the
   project root regardless of current subdirectory — requires Claude Code
   v2.1.196+).
2. Run `${CLAUDE_SKILL_DIR}/scripts/list_routers.py <root_dir>`. If the user
   wants the list saved somewhere, pass `-o <path>`. If they want it saved but
   haven't named a path, default to a file under `/tmp` (e.g.
   `/tmp/routers-<root-dir-name>.txt`) rather than writing into the project —
   this default is provisional until a real project-relative save location
   (e.g. a `.claude/` or `.skogai/` convention) has actually been used and
   confirmed, so don't upgrade it to a project path on your own judgment.
3. Optionally follow up with
   `${CLAUDE_SKILL_DIR}/scripts/validate_router.py <files...>` on the
   discovered list if the user also wants validation, not just discovery.
   Complete when the router list has been returned or written to the requested
   output path.

## Printing the XML tags in every router file

Use `${CLAUDE_SKILL_DIR}/scripts/list_xml_tags.py [root_dir] [-o output_file]` — it does the same
router discovery as `list_routers.py` (frontmatter `type: router`, `.git`/
`node_modules` skipped) but prints, per file, the unique XML tag names found
in it: `<relative-path>: <tag1> <tag2> ...` (or `(no xml tags)`). This is the
automated form of "find the routers, then show me their tags" as a single
command instead of two manual steps — run this directly rather than chaining
`list_routers.py` output into something else by hand.

When the user asks what tags exist in the routing files (or wants an
overview of a project's `<routes>`-and-beyond structure):

1. Run `${CLAUDE_SKILL_DIR}/scripts/list_xml_tags.py <root_dir>` (root_dir:
   whatever the user pointed at, else cwd).
2. Report the per-file tag lines back to the user as-is. Same `/tmp` default
   as `list_routers.py` if they want the output saved but haven't named a
   path — don't invent a project-relative location. Complete when every printed
   router line is preserved in the report or saved output.

## Scaffolding a new routing file

When the user asks to add/set up a routing file in a repo:

1. Resolve the target directory from the user's request, else the current
   working directory. Confirm it looks like a repo root (has `.git` or the
   user already told you it is one). Complete when the target directory and
   repo-root evidence are known.
2. Check whether `SKOGAI.md` already exists there. If it does, stop and tell
   the user — do not overwrite silently.
3. Read `examples/SKOGAI.md.example` (relative to this skill's directory) as
   the template. Write a new `SKOGAI.md` in the target directory with:
   - `type: router` in frontmatter
   - `permalink` set from whatever the user specified, otherwise a
     reasonable slug derived from the repo/directory name (e.g.
     `<repo-name>/claude`)
   - an empty or minimal `<routes>` block — do not invent route entries the
     user hasn't asked for
4. Check the target's `CLAUDE.md`:
   - If it doesn't exist, ask the user before creating one — a missing
     CLAUDE.md may be intentional.
   - If it already has a `<routes>` block containing an `@SKOGAI.md` entry
     (in any form), leave it alone.
   - If it already has a `<routes>` block without that entry, add
     `- @SKOGAI.md` as a new line inside it.
   - If it has no `<routes>` block at all, ask the user before restructuring
     an existing CLAUDE.md into router form — don't silently convert it.
     `examples/CLAUDE.md.example` shows the target shape for a fresh file.
5. Run `scripts/validate_router.py` on each routing file created or edited.
   Report exactly what changed and whether validation passed; do not describe
   the scaffold as complete if validation fails. Complete when every created
   or edited routing file has a validation result.
