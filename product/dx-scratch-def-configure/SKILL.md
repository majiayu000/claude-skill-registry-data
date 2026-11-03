---
name: dx-scratch-def-configure
description: "Drafts a schema-valid Salesforce DX scratch-def from natural language. Preview first (confirmation card, do not write). A later edit — including a write that also changes the draft — is another preview. Write only on consent that this draft is unchanged: invoke this skill and apply via its helper — never hand-write JSON with Write. Writes config/<purpose>-scratch-def.json (default purpose project) under an existing SF DX project that already has config/ (never creates config/). Grounds features on the PUBLIC config-values catalog: put product names (like Revenue Cloud) in features as-is. Use to author/validate a scratch-def or layer features onto a shape or snapshot. Also use for trial, shape-only, snapshot-only, underspecified, missing config/ (ask for the SF DX project path), or batch multi-def asks: invoke this skill, STOP, write report.md on disk (chat is not a substitute; do not skip the skill). Does not create orgs or enable Dev Hub. Not for dx-org-manage, dx-org-devhub-configure, or SKU work."
allowed-tools: Read, Write, Bash(python3), Bash(python)
metadata:
  version: "1.0"
  domains: ["Developer Experience"]
  relatedSkills:
    - "dx-org-devhub-configure"
    - "dx-org-manage"
    - "dx-org-shape-manage"
    - "dx-org-snapshot-manage"
    - "platform-trial-org-create"
  cliTools:
    - tool: ["python3", "python"]
      semver: ">=3.8.0"
---

# Configure Scratch Org Definition File

This skill writes `config/<purpose>-scratch-def.json` (default
`config/project-scratch-def.json`) from a product ask. It does **not** create
the org. Never `mkdir config`.

Every turn writes `report.md` on disk. Chat is not a substitute. Then exactly
one of these happens:

| Mode | When | What the user gets |
|------|------|--------------------|
| **Stop** | Trial, shape-only, shape/snapshot + features with no id, missing project, unclear ask, batch, other-user path | The next step, named. No scratch-def file. |
| **Preview** | First generate (including just-write / skip-preview) or a revision, and the project already has `config/` | A draft + Write file?. Nothing is written yet. |
| **Write** | They accept this draft **unchanged** (this preview, as drafted). This turn may restate it; no prior chat required. | The file. Name dx-org-manage. |

## CRITICAL first gate (before any helper)

First matching row wins. Copy that recipe into `report.md`.

Never Skill() another skill. Never run `sf`. Name the next skill in `report.md` only.

STOP: write `report.md` on disk. Chat is not a substitute. Skip the helper
and skip scratch-def JSON.

Consent is accepting this draft, **unchanged** — not a closed list of yes-words.
Accepting this draft (this preview, as drafted) and asking to write is consent:
apply; reconstruct if they restate the same draft; do not ask Write file?.
A first generate is Preview even if they say write or skip preview.
A different edition, product, or setting is a change: preview.

| If the ask is… | Then |
|----------------|------|
| Shape or snapshot **lifecycle alone** (no features to layer), including "use my org shape only" | STOP. Name dx-org-shape-manage or dx-org-snapshot-manage. |
| Trial / trialforce / "trial org definition" | STOP. Name platform-trial-org-create. Do **not** skip this skill. |
| Underspecified ("I need a scratch def") — no edition and no products/clouds/features | STOP. Ask the two questions below. If `config/` is also missing, include the Missing-project question. Do not invent an edition. |
| Another user's laptop / no readable workspace path | STOP. Cannot read another user's machine. Ask for a readable workspace path. |
| Batch generation (multiple def files in one turn), e.g. "Generate 5 def files for different personas" | STOP. Batch generation is not supported yet — offer to make the first one. |
| WRITE-eligible (imperative generate with edition and/or products/features, or shape/snapshot **+ features**) but cwd has **no** `config/` | STOP. Ask the Missing-project question (folder that **already** contains `config/`). Do **not** create `config/`. |
| Shape/snapshot **+ features**, root resolved, user omitted `sourceOrg` or snapshot id/name | STOP. Write `report.md` on disk. Ask for the id. Name dx-org-shape-manage / dx-org-snapshot-manage to list. Resume this skill with the id. |
| User revises the draft — this turn names a **different** edition, products, settings, or other edits, including a write request that also changes the draft, and root resolved | This turn's wording is the full draft. Preview it. Do not require a prior file or earlier chat. **Do not** apply yet. |
| User consents that this preview is the draft they want written, **unchanged** (this preview, as drafted), and root resolved | Write it. Reconstruct if this turn restates the same draft. No prior chat required. See **Write**. |
| Shape/snapshot **+ features**, root resolved, user supplied the id, and this turn is not consent to write | Preview it. **Do not** apply yet. |
| Imperative generate that names edition and/or products/features (one def), including a first-turn write or skip-preview ask, root resolved, and this turn is not consent to write | Preview it. **Do not** apply yet. |

Underspecified questions: (1) what are you building/demoing? (2) which products/clouds?

Missing-project question: What is the path to your Salesforce DX project (the directory that already contains a config folder)?

## Preview

Show the confirmation card (see `examples/confirm-card.md`, or
`artifacts/examples/confirm-card.md` when packaged). Put **schema-valid JSON**
in chat alongside `report.md` (never inside it): the helper `document`. Ask
Write file? in `report.md`. **Do not** apply yet. Do not name dx-org-manage
until they consent to write.

## Write

One `apply` only — no preview, no second card, no Write file?. Reconstruct
if this turn restates the same draft (no in-context copy). `--out config/<purpose>-scratch-def.json`
(default `config/project-scratch-def.json`). Report the path + a one-line
summary + the **final written JSON in chat**. Name dx-org-manage
(dx-org-devhub-configure if Dev Hub is off).

## Outcome report (always)

**Read** `examples/report-recipes.md` (or `artifacts/examples/report-recipes.md`
when packaged) and copy the matching recipe. First line: `# Scratch Def Report`.
Plain prose — never the backtick character. Spell next-skill names as plain
words (dx-org-shape-manage, platform-trial-org-create).

Omit cache date, shipped-snapshot, jsonschema, and dropped-token notes from
`report.md` unless the helper warned this turn.

## Steps

1. Run the CRITICAL first gate. If it is STOP, write `report.md` and stop here.

2. On WRITE-eligible asks, **resolve the SF DX project root before any helper**:
   cwd with `config/` is the root; otherwise the Missing-config STOP row.

3. Resolve the helper by absolute path:

   ```bash
   HELPER="<skill_dir>/scripts/lib_scratch_def.py"
   [ -f "$HELPER" ] || HELPER="<skill_dir>/artifacts/scripts/lib_scratch_def.py"
   ```

4. **One helper call per turn** from the SF DX project root. Keep the draft in
   **chat/tool context**. Pass the draft on stdin with a quoted heredoc
   (`<<'EOF'`). Invoke `python3` when that binary exists; otherwise `python`.
   - Preview (generate or a revision of the draft):
     ```bash
     python3 "$HELPER" preview <<'EOF'
     {"edition":"Developer","features":["API"]}
     EOF
     ```
   - After consent that this draft is what they want, unchanged:
     ```bash
     python3 "$HELPER" apply --out config/<purpose>-scratch-def.json <<'EOF'
     …same draft JSON…
     EOF
     ```
     (default `config/project-scratch-def.json`). `--out` writes the scratch-def.
   If the helper warns `jsonschema not installed`, ask the user to install
   (`python3 -m pip install jsonschema` or `python -m pip install jsonschema`).
   On success, retry this same helper call once. If they decline or install fails,
   keep this result — do **not** block preview/apply.
   Do **not** Read `references/features.json` or `settings-map.json` into chat.
   Do not Grep them to pick extra tokens.

5. Put the user's product, cloud, and feature words in the `features` array
   as-is (for example Revenue Cloud, not a guessed token list). Use lower
   camelCase settings keys. The helper maps each string to at most one PUBLIC
   token and enriches required settings. Do not add catalog tokens the user
   did not name.

6. Write `report.md` on disk. Put chat JSON and the card per Preview / Write.

Unknown token: drop it and warn in report.md.

## Before you finish

- [ ] `report.md` exists on disk and matches a recipe
- [ ] Preview / revision (including write + change): this turn's wording is the full draft; card + document JSON in chat; asked Write file?; **Do not** apply yet
- [ ] Consent unchanged (this preview, as drafted; no prior chat required): `apply`; file + final JSON in chat; no Write file?; name dx-org-manage
- [ ] WRITE turns: root resolved; one helper call; features array is the user's words
- [ ] report.md mentions cache date, jsonschema, or dropped tokens only when the helper warned this turn

## Notes

Catalog: each helper invocation loads maps into process memory from:

1. Today's `cache/public-config-values-YYYY-MM-DD.json` if usable.
2. Else GET live PUBLIC config-values markdown; on success write today's cache file.
3. Else newest usable prior dated file in `cache/`. report.md: that date
   (only when this fallback fired).
4. Else shipped snapshot JSON `references/features.json` + `settings-map.json`
   (`artifacts/references/` when packaged). Backup. report.md: shipped snapshot
   (only when this fallback fired).

Every helper call (`preview` and `apply`) may write today's cache file under
`cache/` before the user confirms the scratch-def. Add `cache/` to `.gitignore`.
Treat cache JSON as generated. Delete is safe: the next call refetches if
today's file is missing. Feature tokens come from this catalog.
