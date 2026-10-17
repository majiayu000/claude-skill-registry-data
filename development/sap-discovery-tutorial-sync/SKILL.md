---
name: sap-discovery-tutorial-sync
description: Use when a team maintains a tutorial in SAP Discovery Center format (e.g. SAP-samples/btp-developer-guide-cap/documentation/tutorials) and wants to copy or update the sap-tutorials platform version of it (e.g. sap-tutorials/btp-dev-guidance/tutorials) — converts the Discovery Center markdown into our v2-parser format (frontmatter, OPTION blocks, slug-named images, optional rules.vr), validates it against the real build, and opens a PR. Triggers on "sync/import/update the Discovery Center version of <slug>", "copy the btp-developer-guide-cap tutorial over", "pull the SAP-samples version of <tutorial> into our repo".
---

# Sync a Discovery Center tutorial into the sap-tutorials platform format

This skill converts one tutorial from SAP Discovery Center source format into the
sap-tutorials v2-parser format, validates it, and opens a PR. It handles both
**new imports** (first time the tutorial is added to our platform) and **updates**
(syncing upstream changes while preserving our enrichments).

**Supported source:** default `SAP-samples/btp-developer-guide-cap` at
`documentation/tutorials/<slug>/<slug>.md`. The source repo and path are skill
parameters — other teams' repos work too.

**Target:** `sap-tutorials/btp-dev-guidance` at `tutorials/<slug>.md`.

---

## Global Constraints

These invariants apply at every step and override any shortcut:

- **Never direct-merge, never push to main.** Every change goes through a PR.
- **`git fetch origin` before branching** from the target repo.
- **Branch from fresh `origin/main`**, not a stale local copy.
- `TUTORIAL_SLUG=<slug>` is the env-var for single-tutorial fetch (no `--slug` flag exists).
- `validate-tutorials` is **fail-open** (exit 0 even on quarantine) — always inspect
  `.tutorial-cache/quarantine/errors.json` and the presence of
  `hugo/content/tutorials/<slug>.md`, never the exit code.
- **OPTION marker syntax:** `[OPTION BEGIN [LABEL]]` … `[OPTION END]`
- **OS picker auto-wires** only when the body contains ≥2 distinct canonical OS
  labels: `Windows`, `macOS`, `Linux`, `BAS`. Preserve source labels exactly —
  do not invent OS labels that the source did not use.
- `rules.vr` content goes to the `<repo>-Contribution` private companion repo
  (consistent with the quiz-file location convention and the `tutorial-qa-to-prod` skill).
- All `npm run fetch-tutorials` / `validate-tutorials` commands wrap in
  `scripts/quiet-run.sh` per the repo's token-efficiency rule.
- Author frontmatter keys you write: `parser`, `primary_tag`, `tags`, `time`,
  `author_name`, `author_profile`; optional: `video`, `auto_validation`.

---

## Phase A — Draft locally (always run first)

### Step 1: Resolve the source

Set parameters (user may override):
```
SOURCE_REPO=SAP-samples/btp-developer-guide-cap
SOURCE_PATH=documentation/tutorials
SLUG=<slug>
TARGET_REPO=sap-tutorials/btp-dev-guidance
TARGET_PATH=tutorials
```

Fetch the source markdown:
```bash
SOURCE_URL="https://raw.githubusercontent.com/${SOURCE_REPO}/main/${SOURCE_PATH}/${SLUG}/${SLUG}.md"
curl -fsSL "$SOURCE_URL" -o /tmp/discovery-sync-${SLUG}-source.md
```

Record the source commit SHA for PR attribution:
```bash
SOURCE_SHA=$(gh api "repos/${SOURCE_REPO}/commits?path=${SOURCE_PATH}/${SLUG}/${SLUG}.md&per_page=1" \
  --jq '.[0].sha')
echo "Source SHA: $SOURCE_SHA"
```

### Step 2: Detect mode — new import or update

Check whether the tutorial already exists in the target repo. If you have a local
checkout of `sap-tutorials/btp-dev-guidance`, check the file on disk. Otherwise:

```bash
gh api "repos/${TARGET_REPO}/contents/${TARGET_PATH}/${SLUG}.md" \
  --jq '.sha' 2>/dev/null && echo "UPDATE" || echo "NEW"
```

- **NEW**: no merge step; straight conversion.
- **UPDATE**: 3-way merge required (Step 7).

### Step 3: Run the converter

Run `convert-body.mjs` against the fetched source and parse the JSON output.
`convert-body.mjs` is a **first-party repo script** — use plain `node` (no `-I` flag;
`-I` is not recognised on Node 26 on Windows and is not needed for first-party scripts):

```bash
node <tutorials-ims-checkout>/.claude/skills/sap-discovery-tutorial-sync/scripts/convert-body.mjs \
  /tmp/discovery-sync-${SLUG}-source.md "${SLUG}" \
  > /tmp/discovery-sync-${SLUG}-result.json
```

Parse `{body, flags, images}` from the JSON result:
- `body`: the converted markdown body (no frontmatter yet).
- `flags[]`: items needing human judgment (nested `<details>`, dropped H2 wrappers,
  fences missing language tags, unbalanced markup). **Every flag must appear in the
  final report and in the PR body.**
- `images[]`: relative filenames of every image referenced in the converted body.

### Step 4: Review OPTION label normalization

Inspect the OPTION blocks in `body`. The converter preserves source labels verbatim.
After conversion, apply Claude judgment:

- Labels `Node.js`, `Java` → generic technology OPTION tabs (no OS picker).
- Labels matching `Windows`/`Win`, `macOS`/`Mac`, `Linux`/`Ubuntu`, `BAS` → these
  activate the global OS picker **only if** ≥2 distinct canonical OS names are
  present. If only one OS label exists, treat as a generic tab.
- Combined labels like `Mac and Linux` → preserve verbatim; the parser treats them
  as a single non-OS tab. Flag this for the author to consider splitting.
- **Never invent OS labels** that did not appear in the source.

### Step 5: Fetch images

Create the draft image folder and download every file in `images[]`:

```bash
mkdir -p .sync-draft/${SLUG}/${SLUG}/
for img in <each file from images[]>; do
  IMG_URL="https://raw.githubusercontent.com/${SOURCE_REPO}/main/${SOURCE_PATH}/${SLUG}/${img}"
  curl -fsSL "$IMG_URL" -o ".sync-draft/${SLUG}/${SLUG}/${img}"
done
```

Verify every image file was saved successfully. If any image 404s, flag it — a
missing image is the most common build failure.

### Step 6: Collect frontmatter interactively

Prompt the author for each required field. On **update**, use the existing values
from the target repo as defaults (do not re-ask from scratch).

| Field | Rule |
|---|---|
| `parser: v2` | Always set to `v2`. Never ask. |
| `primary_tag` | **Hard gate.** Fetch live taxonomy: `GET ${CAP_BASE_URL:-http://localhost:4004}/build/tags` → `{tags:string[]}` (also cached at `hugo/data/tags.json`). Present valid options. Reject any value not in the taxonomy. See `references/taxonomy-check.md` for the full resolution procedure. |
| `tags` | Array. Element 0 must be a level tag (`tutorial>beginner`, `tutorial>intermediate`, or `tutorial>advanced`). Validate all other elements against the same taxonomy source. |
| `time` | Integer minutes. Suggest an estimate from step count and prose length; author confirms. |
| `author_name` / `author_profile` | Prompt. On update, carry forward from the existing file (do not re-ask). |
| `video` | If the source contains an intro YouTube/Vimeo/openSAP iframe or link, offer to lift it into `video:` frontmatter. Only hosts on the platform allowlist are valid. |
| `auto_validation` | Set `true` only after Step 8 confirms a quiz will be added. Do not ask directly. |

**Taxonomy-unavailable fallback:** if neither `hugo/data/tags.json` nor the CAP
service is reachable, warn the author, allow free-text input, and append
`# UNVERIFIED TAG` to each unverified value in the review report. Never silently trust
unverified taxonomy values.

### Step 7: rules.vr prompt

Ask the author two questions:

1. Should this tutorial have a quiz (`rules.vr`)?
2. If yes, which type?
   - `[AUTOAUTHOR_ALL]` — platform auto-generates questions from step text at build time.
   - Hand-authored `[VALIDATE_N]`…`[VALIDATE_END_N]` stubs.
   - Carry-forward existing `rules.vr` (update case only — show the current content).

Marker syntax reference:
- Validation block: `[VALIDATE_N]` … `[VALIDATE_END_N]`  (N = 1-based step number)
- Auto-author: `[AUTOAUTHOR_ALL]` at the top of the rules.vr file

Write `rules.vr` to the `-Contribution` repo working path
(`.sync-draft/${SLUG}-Contribution/tutorials/${SLUG}/rules.vr`), not the public
target repo. Set `auto_validation: true` in frontmatter only when a quiz exists.

### Step 8: 3-way merge (UPDATE path only)

Skip this step on a new import. On update:

**Inputs:**
- **base** = converted source body at the last-synced SHA. Look up `.sync-draft/${SLUG}/.sync-manifest.json` for `lastSyncedSHA`; if absent (first update after a manual import), treat as no-base → apply upstream changes heuristically.
- **theirs** = the `body` from Step 3 (current source converted).
- **ours** = current `tutorials/${SLUG}.md` from the target repo (body without frontmatter).

**Rules:**
- Take upstream prose and step changes from **theirs**.
- **Preserve** our `frontmatter`, `rules.vr` references, OPTION/OS enrichments,
  `<!-- description -->` text, and any platform-specific callouts we added.

Render a unified diff of **ours** vs the merged result and present it for review.
**STOP here.** Do not write any file until the author approves the merge result.

After approval, write the merged body and update `.sync-manifest.json`:
```json
{ "slug": "<slug>", "lastSyncedSHA": "<SOURCE_SHA>", "syncedAt": "<ISO timestamp>" }
```

### Step 9: Write draft and validate

Assemble the full tutorial markdown with frontmatter:

```
---
parser: v2
primary_tag: <value>
tags:
  - <level tag>
  - <additional tags...>
time: <minutes>
author_name: <value>
author_profile: <value>
# optional:
# video: <url>
# auto_validation: true
---

# <title>

<!-- description -->
<one-line description — fill this in>

---

<converted body>
```

Write to `.sync-draft/${SLUG}/${SLUG}.md`.

Then run validation — see the **Validation** section below (Task 6 wires the full
details of both the built-in precheck and the real-parser path).

### Step 10: Print the Phase A report

The report must cover:

```
Files written:
  .sync-draft/<slug>/<slug>.md
  .sync-draft/<slug>/<slug>/<image files...>
  .sync-draft/<slug>-Contribution/tutorials/<slug>/rules.vr  (if quiz)

Validation verdict: PASS | FAIL | PARSER-UNVERIFIED
  (reason if fail; quarantine reason from errors.json if applicable)

Flags from converter (each must be resolved before PR):
  [list every entry from flags[]]

Unverified frontmatter fields:
  [list any UNVERIFIED TAG fields]

Review checklist:
  [ ] <!-- description --> line is filled in (do not leave the placeholder)
  [ ] Every converter flag addressed
  [ ] OPTION labels correct — no invented OS labels
  [ ] Image files all present on disk
  [ ] Taxonomy tags verified against /build/tags
  [ ] author_name / author_profile correct
  [ ] rules.vr decision confirmed
  [ ] 3-way merge diff approved (update path only)
```

---

## ── STOP: Human reviews the draft ──

```
╔══════════════════════════════════════════════════════════╗
║  Phase B runs ONLY after you explicitly confirm.        ║
║  Nothing has been pushed. The draft is local only.      ║
║                                                          ║
║  Review .sync-draft/<slug>/ and confirm:                 ║
║  • All checklist items above are resolved                ║
║  • Validation passed (or PARSER-UNVERIFIED is accepted)  ║
║  • Merge result approved (update path)                   ║
║                                                          ║
║  Type "confirm" or "yes, open the PR" to proceed.        ║
╚══════════════════════════════════════════════════════════╝
```

**Do not proceed to Phase B until the user explicitly says yes.** If they request
changes, return to the relevant Phase A step, update the draft, re-run validation,
and present the report again.

---

## Phase B — Open PR (only on explicit confirmation)

### Step 11: Branch from fresh origin/main of the target repo

In a local checkout of `sap-tutorials/btp-dev-guidance`:

```bash
git fetch origin
git checkout -b discovery-sync/${SLUG} origin/main
```

Never branch from a stale local `main`. Never reuse an existing branch that may
contain unrelated changes.

### Step 12: Copy draft into place

```bash
cp .sync-draft/${SLUG}/${SLUG}.md tutorials/${SLUG}.md
cp -r .sync-draft/${SLUG}/${SLUG}/ tutorials/${SLUG}/
# Update the sync manifest if present:
cp .sync-draft/${SLUG}/.sync-manifest.json tutorials/${SLUG}/.sync-manifest.json 2>/dev/null || true
```

Stage and commit:
```bash
git add tutorials/${SLUG}.md tutorials/${SLUG}/
git commit -m "feat(${SLUG}): sync from Discovery Center source

Source: https://github.com/${SOURCE_REPO}/tree/${SOURCE_SHA}
Generated by sap-discovery-tutorial-sync skill."
```

### Step 13: Open the PR

```bash
gh pr create \
  --title "feat(${SLUG}): sync from Discovery Center (${SOURCE_REPO})" \
  --body "$(cat <<'PREOF'
## Summary

Converts \`${SLUG}\` from SAP Discovery Center source into sap-tutorials v2-parser format.

**Source commit:** ${SOURCE_REPO}@${SOURCE_SHA}
**Mode:** NEW IMPORT | UPDATE (pick one)

## Inferred / unverified fields (please verify)

<!-- List every UNVERIFIED TAG and every converter flag[] entry here -->
- `primary_tag`:
- `tags`:
- Converter flags: (list from Phase A report)

## Review checklist

- [ ] `<!-- description -->` line is filled in
- [ ] OPTION labels correct
- [ ] Images all present
- [ ] Taxonomy tags verified
- [ ] rules.vr decision implemented (see companion PR if applicable)
- [ ] 3-way merge result reviewed (update path)

_Generated by the `sap-discovery-tutorial-sync` skill._
PREOF
)" \
  --base main \
  --head discovery-sync/${SLUG}
```

### Step 14: rules.vr companion PR (if quiz)

In a local checkout of the `<repo>-Contribution` companion repo:

```bash
git fetch origin
git checkout -b discovery-sync/${SLUG} origin/main
cp .sync-draft/${SLUG}-Contribution/tutorials/${SLUG}/rules.vr tutorials/${SLUG}/rules.vr
git add tutorials/${SLUG}/rules.vr
git commit -m "feat(${SLUG}): add rules.vr from Discovery Center sync"
gh pr create \
  --title "feat(${SLUG}): rules.vr from Discovery Center sync" \
  --body "Companion rules.vr for sap-tutorials/btp-dev-guidance PR <link main PR URL here>.
Generated by the \`sap-discovery-tutorial-sync\` skill." \
  --base main \
  --head discovery-sync/${SLUG}
```

Cross-link both PRs: edit the main repo PR to add the companion PR URL, and the
companion PR to add the main repo PR URL.

### Step 15: Final report

Return to the user:
```
PR opened: <main PR URL>
Companion PR (rules.vr): <companion PR URL> (or "none — no quiz")

Source: ${SOURCE_REPO}@${SOURCE_SHA}
Draft preserved at: .sync-draft/${SLUG}/

Next: after PR review, the content publish workflow will pick up the merged file.
Never direct-merge. Never push to main.
```

---

## Validation

### Overview (for Phase A Step 9)

Two-stage validation in order. Always run Stage 1 first; Stage 2 requires a local
`tutorials-ims` checkout.

---

### Stage 1 — Built-in precheck (always, no checkout needed)

`convert-body.mjs` is a **self-contained skill script** (`.claude/skills/sap-discovery-tutorial-sync/scripts/`
in the `tutorials-ims` checkout). Run it with plain `node` — no `-I` flag (the `-I`
isolation flag is not recognised on Node 26 on Windows and is not needed for
first-party scripts operating on already-fetched local files):

```bash
node <tutorials-ims-checkout>/.claude/skills/sap-discovery-tutorial-sync/scripts/convert-body.mjs \
  --precheck .sync-draft/${SLUG}/${SLUG}.md \
  "${SLUG}" \
  .sync-draft/${SLUG}/${SLUG}/
```

- The third argument is the **images directory** — `readdirSync` scans it for
  filenames to check against every `![alt](path)` reference in the markdown.
- Output: a JSON array of problem strings on stdout. **Empty array (`[]`) = clean.**
- Checks performed: balanced `[OPTION BEGIN]`/`[OPTION END]` pairs; every
  referenced image exists on disk; exactly one `# ` H1; slug is lowercase;
  `parser: v2` present in frontmatter.

**If the result array is non-empty → STOP.** Report every problem string to the
author. Do not proceed to Stage 2 or Phase B until all problems are resolved and
`--precheck` returns `[]`.

---

### Stage 2 — Real parser (requires `tutorials-ims` checkout)

Place the draft file and its images into the fetch layout the fetcher expects, then
run the full pipeline against the local checkout (both commands wrapped in
`scripts/quiet-run.sh` per the repo token-efficiency rule):

```bash
# Copy draft into the source layout the fetcher reads from:
mkdir -p scripts/fetch-sources/${SLUG}/
cp .sync-draft/${SLUG}/${SLUG}.md scripts/fetch-sources/${SLUG}/${SLUG}.md
cp -r .sync-draft/${SLUG}/${SLUG}/ scripts/fetch-sources/${SLUG}/${SLUG}/

# Run the fetcher (single-tutorial mode) then the validator:
TUTORIAL_SLUG=${SLUG} CAP_BASE_URL=${CAP_BASE_URL:-http://localhost:4004} \
  scripts/quiet-run.sh npm run fetch-tutorials
scripts/quiet-run.sh npm run validate-tutorials
```

**`validate-tutorials` is fail-open** — it exits 0 even when tutorials are
quarantined. Never trust the exit code. After both commands complete, inspect:

1. **`hugo/content/tutorials/${SLUG}.md`** — must exist. Quarantined files are
   moved OUT of this directory; absence means the tutorial was rejected.
2. **`.tutorial-cache/quarantine/errors.json`** — if this file exists, check
   whether it contains an entry for `${SLUG}`. If it does, the tutorial failed
   validation; report the `reason` field to the author.

If either check fails → **STOP.** Report the quarantine reason and do not proceed
to Phase B.

---

### Stage 3 — No checkout available

When no `tutorials-ims` checkout is accessible, run Stage 1 (built-in precheck)
only. Mark the draft **"parser-unverified"** in the Phase A report and in the PR
body. **Never claim the tutorial builds** without evidence from Stage 2.
