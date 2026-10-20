---
name: doc-truth
description: Checks that what a repository's documents say actually exists - cited paths, links and anchors, parity between README.md and README.pt-BR.md, and versions and the plugin list against the manifests. Read-only, no network, exit code 0/1/2. Use when the user asks to check, audit or validate the documentation, for example "os docs estão certos?", "tem link quebrado?", "o README cita arquivo que não existe?", "o README em português está igual ao em inglês?", "doc-truth", "check the docs", "verify documentation paths and links", "do the READMEs match". Triggers - /doc-truth or /housekeeping:doc-truth.
---

# doc-truth (do the documents tell the truth?)

Reads every `.md` file tracked by git and checks what it claims against the repository: the cited path exists, the link and the anchor lead somewhere, `README.md` and `README.pt-BR.md` have the same structure, the version written next to a plugin's name is the one in the manifest. It is **read-only**: it never changes the repository, never runs a command that a document cites, and does not use the network. It needs `python3` (stdlib) and `git`.

It does not check external links (`https://...`) and does not check whether a description is correct, only whether what it points to exists.

Reply to the user in the user's language. The tool prints its output in Portuguese without accents (for example `limpo: nenhum achado`, "clean: no findings"): when you present the findings, explain them in the user's language and keep the category names, paths and fingerprints exactly as printed.

## When to use

Use it when the user asks to check the documentation: after editing READMEs or `docs/`, before a release, or when in doubt ("does the README still cite that file?"). Never offer it on your own: it is a tool for explicit requests only.

## Flow

### 0. Locate the script

The script ships with this skill: `${CLAUDE_SKILL_DIR}/scripts/doc_truth.py`. Use it directly, always with `python3 -I`.

```bash
test -f "${CLAUDE_SKILL_DIR}/scripts/doc_truth.py" && echo OK || echo FALTA
```

`OK` means the script exists. `FALTA` means "missing".

If `${CLAUDE_SKILL_DIR}` shows up unexpanded, use the path shown as "Base directory for this skill" when the skill was loaded, written out in full in every command.

In the commands below, `<repositório>` is the repository path ("repository") and `<arquivo>` is a file ("file").

### 1. Run

```bash
python3 -I "${CLAUDE_SKILL_DIR}/scripts/doc_truth.py" <repositório>
```

Options: `--json` (the output has a `schema` field) and `--config <arquivo>`. If `.doc-truth.json` exists in the repository root, it is read automatically. Exit codes: `0` clean, `1` with findings, `2` error (not a git repository, invalid config).

### 2. Present

Present the findings grouped by category, in the order the output prints them, and say how many documents were checked. The output starts with `doc-truth <version>: <N> documentos conferidos em <path>` ("N documents checked in <path>"). It then prints `limpo: nenhum achado` ("clean: no findings") or `<N> achados` ("N findings"). The categories are:

- `path`: a path cited between backticks or in a code block does not exist **in the git tree**. What exists only on your disk does not count, so that the result is the same in CI. Propose fixing the text. If the file is created at run time (`decisions.json`), propose adding the name to `ignore_paths`.
- `link` and `anchor`: the link points to something that does not exist, or there is no heading for the anchor (GitHub slug rules).
- `parity`: `<name>.md` and `<name>.pt-BR.md` have different sequences of heading levels, or a `README.md` has no `README.pt-BR.md` (the finding reads `falta README.pt-BR.md`, "README.pt-BR.md is missing").
- `version`: an `X.Y.Z` version on the same line as a plugin's name does not match `plugin.json`.
- `plugins`: the catalog has a plugin that the root README does not link.

If the output says `aceitos pela lista allow` ("accepted by the allow list"), tell the user how many findings `.doc-truth.json` has already accepted (the line reads `(<N> aceitos pela lista allow)`).

### 3. Fix only on request

The skill reports. Fixing a document's text is an ordinary edit, which you make only when the user asks, showing what changes. **Never edit `.doc-truth.json`** (neither `allow` nor `exclude`) without the user's OK: accepting a finding is the user's decision. To accept a finding, the user puts the finding's `fingerprint` in `allow`; it does not depend on the line number.

## Configuration (`.doc-truth.json`)

```json
{
  "exclude": ["docs/plans/**", "**/CHANGELOG.md"],
  "ignore_paths": [".ar-board/", "decisions.json"],
  "allow": []
}
```

- `exclude`: documents that are not checked (historical, generated). They still count as link targets.
- `ignore_paths`: paths that deliberately do not exist in the tree (created at run time). A pattern with no `/` (a trailing `/` does not count) matches that name in any folder; a trailing `/` means the folder and everything under it. A pattern with a `/` in the middle, or with a leading `/`, starts at the repository root. `/SKILL.md` therefore matches only the bare text `SKILL.md` as written in a document and the root file `SKILL.md`, never a full path such as plugins/x/SKILL.md. `**` crosses folders and `*` does not.
- `allow`: fingerprints of accepted findings.
- An unknown key is an error (exit code 2).

## Rules

- Read-only, no network. Never run a command that a document cites.
- Tree diagrams (lines with `├──`) are not checked: they are drawings.
- Never run it on a repository you do not trust: git reads that repository's local configuration. If `git` is not on the PATH, tell the user so instead of trying another way.
