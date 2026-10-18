---
name: "Web: Review"
description: "Review an existing interface: collate its assets, publish an observation logger built for it, run passes that fix, write back, check and export, and end at sign-off"
when_to_use: "When an existing interface is to be reviewed for layout, state, copy or interaction problems and the findings fixed on a branch; also to resume a review whose export file already exists."
model: opus
effort: high
metadata:
  glyph: ᛟ
  family: web
  goblin-spinner: walking the pages|reading the log|closing the loop
disable-model-invocation: true
allowed-tools: ["Read", "Glob", "Grep", "Write", "Edit", "Bash", "AskUserQuestion", "Artifact", "ArtifactData"]
argument-hint: "[app path or URL] [task id] [resume]"
---

# Review an existing interface

Load `web-conventions` and `artefact-conventions` first. The review is a loop of passes over a shared observation store (principle 7); it ends when nothing is open, the principles check passes and the walkthrough has captured every page.

## Step 1: Start

Run the shared start from `web-conventions`. For a review the inventory must also yield: the routes (per `asset-conventions` detection), the UI library in use (for principle 9), the device list (principle 8) and how the app is served locally. Pick the task slug from the roadmap task id or the branch name; everything lands in `docs/artefacts/<slug>/`.

If `docs/artefacts/<slug>/observations.json` exists and carries an `artifact` URL, this is a **resume**: skip Step 2, read the live store and start Step 3 from what is still open.

- [ ] Routes, UI library, devices and serve command named in the inventory table

## Step 2: The logger

Build the task's logger from the library entry `skills/web-conventions/library/observation-logger.html`:

1. Copy it to `docs/artefacts/<slug>/log.html`.
2. Resolve every `ADAPT:` comment: title and eyebrow; the links to the app and its API; the `where` options, one per route and region from the inventory in reading order; the sources list; the palette, remapped to this project's artefact aesthetic per `artefact-conventions` Step 2 (or 2b for a first artefact).
3. `grep -c 'ADAPT:'` must print 0.
4. Load `artifact-capabilities`, then publish with the `Artifact` tool declaring `db` and `assets`.
5. Write `docs/artefacts/<slug>/observations.json` by hand as `{"exported": null, "artifact": "<url>", "entries": []}` so the next session can find the store.

Hand Jason the URL and the device list, and say what to walk: every route, on every device, every open state. Stop; the pass starts when he says the log has entries.

- [ ] No `ADAPT:` left in the published page
- [ ] Export file holds the artefact URL

## Step 3: A pass

1. **Read.** `ArtifactData` `list` on collection `observations` with `out_dir` set to a scratch directory, then `python3 ~/.claude/library/scripts/web/observations.py export <scratch>/observations --artifact <url> --out docs/artefacts/<slug>/observations.json`. A contract fault stops the pass until the entry is corrected in the page.
2. **Triage.** Group the open entries by `where`, blockers first. For each, say in one line what will change or why not. A layout change bigger than a tweak gets a wireframe first (principle 6, `web-conventions`): drawn in product tokens, callouts citing `#seq`, approved before any code.
3. **Fix** on the branch. Watch principle 4 while editing any repeating item and principle 9 whenever a class name is added.
4. **Write back.** One `ArtifactData` `batch` per pass: `update` each touched entry with `status`, `resolution` and `updatedAt`, pinned with the `version` read in step 1. `declined` carries the reason; no status but `open` goes without a resolution.
5. **Check.** `web-check` in `pass` mode over what changed. Findings are written to the store as entries with `source: check` and their principle number (`batch` `set`, new doc ids), so Jason sees them in the page.
6. **Export** again as in step 1 and stage the file with the pass's changes. A pass that has not exported is not finished.
7. **Report** `observations.py status` output, then ask one question: another pass, or sign-off?

- [ ] Export file newer than every write-back in the pass
- [ ] Every non-open entry has a resolution line

## Step 4: Sign-off

`observations.py status docs/artefacts/<slug>/observations.json` must print `blocks sign-off: nothing`. Then `web-check` in `signoff` mode over every route; a finding reopens Step 3 or is waived by Jason with a reason written to the entry. Then `web-walkthrough`. Offer shelving once, per `web-conventions`. The hook on `gh pr create` reads the same export file, so a PR opened early is refused with the open list.
