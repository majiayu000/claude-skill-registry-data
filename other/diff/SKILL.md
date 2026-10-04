---
name: diff
description: Compares AS-IS and TO-BE designs, marks the changed elements with native Figma Dev Mode annotations, and writes up the linked task doc with a Figma link, an AS-IS/TO-BE table, and a scope callout. The tracker comes from the task_tracker section of figma-conventions.yaml and can be notion, github, or none; with none it stops at the Figma annotations and emits the table as markdown. AS-IS may sit in another section of the same page or on a different page entirely, so the source is settled first. It never creates annotation categories — it reuses a shared one or uses none, and carries classification in a label tag. Only the representative screen is marked; state variants inherit. Triggers - "/fig:diff", "mark what changed", "annotate the design changes", "as-is to-be 비교", "변경점 표시해줘", "바뀐 요소 annotation 달아줘".
allowed-tools: AskUserQuestion, Bash, mcp__plugin_figma_figma__use_figma, mcp__plugin_figma_figma__get_metadata, mcp__plugin_figma_figma__get_screenshot, mcp__claude_ai_Notion__notion-fetch, mcp__claude_ai_Notion__notion-update-page, mcp__claude_ai_Notion__notion-search, mcp__plugin_github_github__issue_read, mcp__plugin_github_github__issue_write, mcp__plugin_github_github__add_issue_comment, mcp__plugin_figma_figma__whoami
---

# fig:diff — marking AS-IS / TO-BE changes and writing up the task doc

Compares AS-IS and TO-BE designs, **finds what changed and pins it with native Figma Dev Mode annotations**, and lays the same thing out as a comparison table in **the linked task doc**. Where that write-up goes is decided by the `task_tracker` setting.

**Principles**
- **The single source for a change is the label text.** The category colour is a secondary cue and can be lost.
- **Never create a category.** Reuse a shared one, or go without.
- **Mark the representative screen only.** State variants (Default/Selected, Detail/Toast, and so on) fold into one representative and are handled with an "inherits" line.
- Every write (Figma or the tracker) goes through the **preview → "go"** gate.
- **Never guess where AS-IS is** — if it is not on the same page, search for it or ask.

## When to invoke

- There is an AS-IS/TO-BE pair and the ask is "mark what changed" or "compare these and annotate them"
- The changes also need writing up in the task doc
- An explicit "/fig:diff"

## When NOT to invoke

- Just understanding the frame structure → `/fig:read`
- Tidying structure and naming, filling placeholders → `/fig:prep`
- Flow arrows → `/fig:arrows`
- Auditing rule violations only → `/fig:lint`
- Auditing, applying, or migrating changes into the canonical page → `/fig:sync`

## Inputs

- `figma_url` (required): the TO-BE (or comparison target) URL. A page, a section, or a frame — the kind is detected and branched on.
- `task_ref` (optional): the task to write up. Without it, the tracker is searched by screen or feature keyword and the candidates confirmed. Failing that, the tracker step is skipped (with the user's confirmation).
- `shared_category` (optional): the name of the shared annotation category to reuse. Omitted, `task_tracker.annotation_category` from the config.

The rules come from `figma-conventions.yaml` — `resolve-config.py --js <fileKey>` supplies `task_tracker` and `sync.pair_patterns`.

Always load the `figma:figma-use` skill before calling `use_figma`.

**Seat check before the first write** — call `whoami` once. Where every plan it lists carries `seat: View`, stop before any `use_figma` write and say so: the reading half of this skill runs on a View seat, the writing half needs an Edit seat on the file's plan, and no retry changes that. Where the seats are mixed, go ahead — and if the first write comes back as a permission error, report the seat table and stop rather than retrying.

## Category policy (never create one)

- **Never create an annotation category** (`addAnnotationCategoryAsync` is off limits). Creating one on every run pollutes the file's category list, and on a file sync those categories are lost or remapped onto presets (measured).
- Use `getAnnotationCategoriesAsync()` to look up the name in `task_tracker.annotation_category` → if it exists, use that `categoryId`; if not, omit `categoryId` entirely (no category).
- **Classification is carried in a leading `[tag]` on the label, not in the category colour.** The tag list is `task_tracker.scope_tags`. Colour can be lost, so the single source for classification is the label text.

## Procedure

### 1. Settle the AS-IS / TO-BE sources (no guessing)
Detect what kind of node came in (a page = a canvas holding several frames and sections / a section / a single frame).

Take the TO-BE first, then **look for AS-IS in this order**:
1. **Another section on the same page**: match section names against `sync.pair_patterns` (shared with fig:sync).
2. Not on the same page → **search other pages**: propose pages from `figma.root.children` whose names contain AS, current, live, or before, or **which hold frames with the same screen names**.
3. Still unclear → **ask** (AskUserQuestion): "where is AS-IS — ① another page in this file ② another file ③ live production, with no comparison copy". If there are candidates, offer one as the recommendation.
4. If AS-IS **does not exist at all** (a genuinely new screen), comparison is impossible → confirm whether to treat it as "new screen" instead of as changes.

> If several pages have to be read, `setCurrentPageAsync` is once per script — split the `use_figma` calls per page and run them in parallel (the figma-use rule).

### 1-2. Set up the comparison structure (when AS-IS lives elsewhere)

When AS-IS sits on **another page or another file — a production page, say — clone it into the working page so both can be compared on one screen.** If a reviewer or an engineer has to travel between two pages, the comparison does not happen at all.

- **Split the sections into two blocks, AS-IS and TO-BE.** Do not break them up by feature or domain — a comparison page has exactly one axis of classification, before versus after.
- Name the sections so they match the patterns from step 1 (for example `NN. AS-IS` / `NN. TO-BE`).
- **Keep frame names identical on both sides** — the name is the pairing key and the section is the discriminator. Prefixing a frame with something like `[AS-IS]` breaks pairing.
- **Stack the two sections vertically and line up each screen's x** — the same screen facing itself top and bottom is what makes comparison easy.
- New screens and state variants that exist only in TO-BE go in the TO-BE section alone (the AS-IS slot is left empty).
- AS-IS is a reference copy, so **it is not edited.** Clone from the canonical page and leave the original alone.
- One frame of the same name in each of the two sections is correct — duplicate names count as a violation **within a section only** (say so when calling `/fig:lint`).

### 2. Pair the frames
- Call `get_metadata` on the target scope. If the response is large enough to be saved to a file, extract just the `<section>` and `<frame>` tags with python or jq from Bash (see the snippet).
- **Pair AS-IS ↔ TO-BE frames by name** (same screen name to same screen name). If there are sub-sections, go one level deeper.
- **A size difference (width/height) is a change signal** — a larger TO-BE raises the odds of added content.

### 3. Diff each screen
- For each pair, take high-resolution **per-frame** `get_screenshot` calls **in parallel**, curl them down to local files, and compare by eye (a whole canvas at once is too low-resolution to read).
- List what changed: new columns, fields, or sections; changed values, units, or styles; added icons.
- **Fold state variants into one representative** (Default/Selected, Detail/Toast → pin the representative only, plus a line saying the variants inherit the same change). No duplicate marks across sibling variants.
- Differences in dummy data (a total that is simply a different number) are **not design changes → excluded**.

### 4. Compare against task scope → classify
- If there is a task, read its **In/Out scope and change summary** and classify each change against it. Tags follow the order in `task_tracker.scope_tags` — typically three ways: "this task" / "out of scope" / "planned separately"
- With no tags in the config, emit the change list unclassified, and ask the user when a scope call is actually needed
- Do not decide out-of-scope changes unilaterally — **leave a question asking whether they were meant to be in this task**.

### 5. Secure the anchor nodes (reading)
- With a **read-only** `use_figma` script, grab each changed element's node by text content via `findOne` (exact or partial match) and check its `absoluteBoundingBox`.
- Sublayers inside an instance can carry `node.annotations` too. But the `0:xxxx` internal ids from `get_metadata` **cannot be addressed directly** by `getNodeByIdAsync` → secure them by text matching.

### 6. Preview → go (Figma)
- Present the change table (element / AS-IS / TO-BE / classification), **the label text of every pin**, which frame each goes on, and which category will be used (the shared name, or none), then wait for "go".

### 7. Write to Figma (annotations)
- Load `figma-use`, then with `use_figma`: switch currentPage → look up the shared category → attach each anchor. **Category lookup and all pin attachment in one script** (so nothing is lost in between). See the snippet.
- **The leading `[classification]` tag is mandatory** — if the colour comes undone, the classification survives as text.
- **Verify by reading back**: re-query `node.annotations`. Pins are visible **in Dev Mode only**, so `get_screenshot` cannot confirm them.

### 8. Task doc: preview → go → write

Three things go in, whatever the tracker: ① the Figma link (with `node-id`) plus one line saying "marked with Dev Mode annotations, representative screen, state variants inherit" ② **the AS-IS/TO-BE comparison table** ③ **the scope callout** (all in scope → `✅`; anything out of scope → `⚠️` plus a TBD).

Only where and how they go in is decided by `task_tracker.type`.

| type | Target | Method |
|---|---|---|
| `notion` | the `ui_section_heading` section of the task page (usually behind an empty callout) | `update_content`, catching the heading and callout as `old_str` and **inserting after them**. Never replace the whole body |
| `github` | the task issue | If the body has that section, insert beneath it; if not, add it as a comment |
| `none` | — | Nothing is written. **Emit the comparison table and the callout as markdown in the response** and stop |
| any other | — | As `none`. The write belongs to `pm`'s adapter for that type, which this skill does not read — emit the markdown, and say which type was not handled |

- If no task was found, skip this step (with the user's confirmation).
- **Search for the target section.** If `ui_section_heading` is missing or named differently, confirm where it should go. If there is already content there, do not overwrite it — append after it.

### 9. Verify
- Unless the type is `none`, read back and confirm the table, the callout, and the link.
- **Watch for corrupted non-ASCII characters**: text typed directly can come back with a broken syllable. Check the code point of the broken character and substitute a `\u` escape — retyping it by hand corrupts it again.

### 10. Follow-up once scope is settled (where applicable)
- When an out-of-scope change is later confirmed as in or out: update **together** the Figma label `[tag]`, the comparison table's classification, the scope In list, and the scope callout (⚠️↔✅) — each behind its own preview → go.

## Label wording

- Form: `**[classification] what changed** — how and why (value, format, position).`
- Include concrete values so an engineer can tell from the deliverable alone: position (behind or beside what), value format (mm:ss, for instance), exceptions (how an incomplete state is shown).
- Pick the classification tag from `task_tracker.scope_tags` — never invent a new one.

## Snippets

**Extracting sections and frames** (from a saved metadata file):

    # f = path to the saved get_metadata result
    python3 -c "
    import json,re
    t=json.load(open('$f'))[0]['text']
    for m in re.finditer(r'<(section|frame)\s+id=\"([^\"]+)\"\s+name=\"([^\"]+)\"\s+x=\"(-?[0-9.]+)\"\s+y=\"(-?[0-9.]+)\"\s+width=\"([0-9.]+)\"\s+height=\"([0-9.]+)\"', t):
        tag,i,n,x,y,w,h=m.groups()
        if tag=='section' or float(w)>=1400: print(f'{tag} {i} w={float(w):.0f} h={float(h):.0f}  {n}')
    "

**Category lookup + all pins + read-back** (one script, policy applied):

    // targets = [{ id, md }] — md starts with "[classification]". SHARED='Changed'
    const page = await figma.getNodeByIdAsync(PAGE_ID);
    await figma.setCurrentPageAsync(page);
    const cats = await figma.annotations.getAnnotationCategoriesAsync();
    const shared = cats.find(c => c.label === SHARED);   // missing → undefined → no category
    const res = [];
    for (const t of targets) {
      const n = await figma.getNodeByIdAsync(t.id);
      if (!n) { res.push({ id: t.id, ok: false }); continue; }
      const ann = { labelMarkdown: t.md };
      if (shared) ann.categoryId = shared.id;            // assign only if it exists, never create
      n.annotations = [ann];
      res.push({ name: n.name, cat: shared ? shared.id : null, ok: true });
    }
    return res;   // read-back verification is a separate call re-querying node.annotations

## Pitfalls

- **Never create a category**: a new custom category disappears on a file sync, pins get remapped onto presets, and some pins are lost outright. → reuse a shared one or go without, and carry the tag in the label.
- **Pins are Dev Mode only**: invisible in an ordinary screenshot or in edit mode. Verify by reading `node.annotations` back.
- **Never guess where AS-IS is**: not on the same page → search other pages, or ask.
- **Do not build the comparison page around feature sections**: two axes (feature × before/after) make comparison impossible. AS-IS/TO-BE are the only axis (section 1-2).
- **Representative only**: no duplicate pins across sibling state variants. One representative plus an "inherits" line.
- **Pins only for this task's changes**: incidental and out-of-scope changes go in the task doc's table, not on the canvas as `[out of scope]` pins. Navigation, AS-IS links, code notes and policy never become pins — the arrows, the AS-IS section, the ticket and the spec already hold them.
- **The next round clears them**: frames cloned from a marked TO-BE carry its pins. Clear them before marking the new round, otherwise last round's `[this task]` labels read as this round's.
- **Large metadata**: when it lands in a file, parse with python or jq. `0:xxxx` internal ids cannot be addressed → match by text.
- **Corrupted non-ASCII**: a syllable can break when typed straight into an external document. Read back after inserting and substitute a `\u` escape for anything broken.

## Constraints

- **Preview → "go"** before each write, to Figma and to the task doc (split the Figma side when there are many steps). **Never create** an annotation category. Nothing but the target node changes — no parents, no siblings. Never declare it done before verifying.

## Definition of done

- Every changed TO-BE element (on the representative frame) carries a `[classification]`-tagged label annotation, confirmed by read-back.
- The task doc's designated section holds the Figma link, the comparison table, and the scope callout, confirmed by read-back with no corrupted characters. Where the type is `none` or no task exists, markdown output stands in and that fact is stated.
- Out-of-scope changes are left flagged, and once settled, Figma and the tracker are updated together.
