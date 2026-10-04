---
name: sync
description: Audits whether changes finished on working and update pages actually made it into the canonical page, applies whatever did not, then archives the working copies. This is the skill that executes the apply-after-release step — audit with zero writes, then apply, then archive, each behind its own preview and go gate. Frame names are identical on both sides so comparing names settles nothing; the call is made on three signals together — text diff, frame height, and component master. Triggers - "/fig:sync", "find what never made it into canonical", "bring the canonical page current", "정본 반영 안 된 것 찾아줘", "운영 페이지 최신화", "교체 안 된 화면 찾아줘".
allowed-tools: AskUserQuestion, Bash, Read, Write, mcp__plugin_figma_figma__use_figma, mcp__plugin_figma_figma__get_metadata, mcp__plugin_figma_figma__get_screenshot, mcp__claude_ai_Notion__notion-fetch, mcp__plugin_figma_figma__whoami
---

# fig:sync — bring canonical current (audit → apply → archive)

Checks every finished screen against the canonical page to see whether it actually landed there, applies what did not, then moves the working copies into the archive. This is the post-release procedure, executed instead of remembered.

The canonical page is supposed to be "what is running right now", but shipping and updating canonical happen at different moments. Left alone, the gap widens and engineering and QA start making decisions against an old screen. **That lag is the accident this skill prevents.**

**Prerequisites**: always load `figma:figma-use` before calling `use_figma`. Step 1 (audit) is **zero writes** — `use_figma` is used as a read-only script that only `return`s a report.

**Seat check before the first write** — call `whoami` once. Where every plan it lists carries `seat: View`, stop before step 3's first `use_figma` write and say so: the reading half of this skill runs on a View seat, the writing half needs an Edit seat on the file's plan, and no retry changes that. Where the seats are mixed, go ahead — and if the first write comes back as a permission error, report the seat table and stop rather than retrying.

## When to invoke

- "find what never made it into canonical", "bring the canonical page current", "check everything that wasn't replaced"
- Right after a release or a batch of shipped work, to bring canonical in line
- When working pages have piled up long enough that nobody knows what was applied
- As a periodic sweep — roughly monthly, to keep the lag from opening

## When NOT to invoke

- Marking changes between two designs (AS-IS/TO-BE) and writing up the task doc → `/fig:diff`
- Naming and section tidying, stubbing placeholders → `/fig:prep`
- Checking for violations only → `/fig:lint`
- Flow arrows → `/fig:arrows`
- Applying to frontend code → `/fig:code`
- Just understanding the file structure → `/fig:read`

## Where the rules come from — the config file (same source as fig:prep and fig:lint)

The rules are set by **`figma-conventions.yaml`**, read through `resolve-config.py --js <fileKey>`.

Sections read: `pages` (the three axes, excluded sections) · `sync` (comparison-pair patterns, diff length limit, version pages) · `naming`.

**There are two ways to apply a change, and a structure comparison decides which.** Moving the frame is the default, but when the layer composition is identical and only values differ, edit the values instead — node ids have to survive or the deep links in specs and tickets break. Step 3 executes that decision, and the report says which was used and why.

If the team keeps a written guide, point `guide_source` at it. It is not fetched on every run.

## Inputs

- `figma_url` (required): the target file URL. A specific page can be given, but the audit is file-wide by default
- `scope` (optional): to narrow the audit to a domain or a period

## Procedure

### Step 1 — settle the axes (never guess; record them per file)

Conventions differ per file. Some group by version, some by period, some split progress with divider pages (empty pages named `## title ##`).

1. **If `files.<fileKey>.pages` already has the three axes, use them.** Skip to step 2 of the procedure
2. Otherwise read **the page list and its order** from `figma.root.children`. The file-level response from `get_metadata` returns an incomplete page list, so it is not used
3. Infer the three axes, remembering there are two ways to match — **by name** (`match: name`) and **by the band beneath a divider** (`match: divider`)

   | Axis | What it is | Signals |
   |---|---|---|
   | canonical | The page everything is compared against | A production prefix, strictly tidied structure |
   | archive | Applied work, already tidied away | A version or period prefix, date or version section hierarchy |
   | queue | Shipped by engineering, not yet in canonical | A divider group label (done, deployed), individual working pages |

4. **Always sweep the groups split by dividers.** The pages in a band whose label means "done" are the un-applied candidates. Comparing only the archive pages found by name prefix misses real un-applied work — measured. This is exactly why the queue is usually not findable by name
5. **Confirm the inference once** — list N canonical, M archive, K queue pages and ask whether that is right
6. **Record the confirmed convention in `files.<fileKey>`** (the label and the three axes). The next run starts at point 1. If the page list stops matching the convention, confirm again

### Step 2 — audit (zero writes, three-signal judgement)

Check each piece of work in the archive and queue against canonical.

**Frame names settle nothing.** The working copy and canonical keep the same frame names — it is the same screen — so a name comparison always says "match". You have to look at the content.

**Signal 1 — text diff (the main one)**

If the work contains a comparison pair (name patterns from `sync.pair_patterns`), take the text set of each side and difference them. That is the change keyword set for that piece. With no pair (a new screen, a single proposal), take the whole section's text as candidates.

- A string only in the new version → it **must be present** in canonical to count as applied
- A string only in the current version → it **must be absent** from canonical to count as applied (this is what catches rewording and removals)

**Signal 2 — frame height**

Changes that add or remove elements change the height. If the new version's height matches canonical and differs from the current version, that is evidence of applied; the reverse is evidence of not applied. Never decisive alone — it supports signal 1.

**Signal 3 — component master**

Component-level changes (a state added, hierarchy tidied) do not show up in frame text. Get the master id from a canonical frame's instance via `getMainComponentAsync()` and compare it with the working copy's instance. **Referencing the same master means it is already merged** — if the master lives on the canonical page, editing the working copy *is* updating canonical.

**The result has exactly three buckets**

| Bucket | Basis |
|---|---|
| Applied | At least one signal clearly supports it, with no signal against |
| Not applied | A new-version keyword is missing from canonical, or a current-version keyword is still there |
| Needs checking | All three signals are silent — a purely visual change where the pair's text is identical and heights match |

**Never decide the needs-checking cases.** Collect them, report them, and ask whether to run a screenshot comparison — it costs per item, so it does not run automatically. Cases where the pair's "current" side was overwritten after the work and now matches the new version land here too; note that those cannot be used as comparison material at all.

### Step 3 — apply (structure comparison decides the method)

Only the not-applied cases. For each one, **compare the structure first.**

List the text nodes of the canonical frame and the new-version frame in document order as `parent name|characters` and compare.

- **Order, count, and parent names all match** → only the values differ. **Edit the values.** Node ids survive, so external deep links hold. Count the intended edits in advance and put a guard in the script that aborts when the count differs from expected
- **Anything differs** → the structure changed. **Move the frame** as the convention prescribes, and note in the report that external links pointing at the old canonical frame id will break (see the deep link audit)

Value edits are text edits, so **read the target node's current fonts with `getStyledTextSegments(['fontName'])` and load them** before writing. Never assume a default font.

**Preview → go.** State the target frames, what will change and how many, the method (value edit or move), and the reasoning. With several pieces, split them and pass a gate per piece.

Right after applying, run the same comparison again and confirm the result matches the new version.

### Step 4 — archive

Move working pages whose changes are now in canonical into the archive.

1. **Confirm which archive page and which period (version) section they belong to.** Page id ranges hint at when the work happened, but the actual ship date is not in the file — ask rather than guess
2. **Read padding, spacing, and background style from an existing work section** in the archive and apply the same to the new one. Do not invent a style
3. Move the frames into the new section and place them at the conventional position
4. Delete the emptied working page **after confirming it has zero children**. Page deletion cannot be undone, so ask for it as **an independent gate**, never folded into another confirmation
5. If the archive pages have piled up, only name the candidates for moving into long-term storage — this skill does not rename or move archives itself

**When stretching a section, compute all four edges from real coordinates.** Sections on a page are not vertically ordered, so picking "the section below" by eye is wrong. There are cases that overlap vertically but not horizontally, so all four edges have to be checked.

### Step 5 — verify

- Call `/fig:lint` and confirm frame membership, bounds, and section overlap pass. Mandatory when clone or move was involved
- Confirm the moved frames have the same text node count as before the move
- Reference material kept in canonical but excluded from audits (size variants and the like) goes in a section matching `pages.exclude_sections`. Left in a normal section it reports as a missing state variant or a flow orphan

### Step 6 — the signals Figma shows engineering

Where `handoff.dev_status` is on, and only after Step 5 passed:

1. **Mark completed** — on each canonical section the applied changes landed in, `section.devStatus = { type: "COMPLETED" }`. This is what turns the "ready for dev" a prep left there into "shipped" where engineering looks
2. **Name the version** — `sync.named_version` with `{date}` and `{n}` (screens applied) filled in, then in a **separate** `use_figma` call after every write above has finished:

   ```js
   await figma.saveVersionHistoryAsync("{title}", "{one line: what was applied, from where}");
   ```

   Separate on purpose: changes made earlier in the same script are not guaranteed to be in the version. `null` saves none — and `null` is the default

Both go in the preview with everything else; nothing here is a second gate.

*(Checked on a live file with an Edit seat, 2026-08-31: `use_figma` rejects both of these — `"devStatus" is not a supported API` and `"saveVersionHistoryAsync" is not a supported API`. It is the tool's allowlist, not the seat and not the file, and Figma's REST API has no endpoint that sets a dev status either. Both settings ship off; the apply in Steps 1 to 5 is unaffected and its seat check above still holds.)*

## Reporting

```
audited N  →  applied X · not applied Y · needs checking Z

[not applied — handled]
· name (owner)
  before: what canonical looked like
  applied: what changed and how / method (value edit or move) and why

[needs checking]
· name — which signals were silent, whether a screenshot comparison is needed

[archived]
· working page → archive location, whether deleted

[handoff]
· sections marked completed: N · version saved: {title}   (or: off — handoff.dev_status, sync.named_version)
```

If nothing was un-applied, report just that, briefly.

## Implementation snippets

**Comparison-pair text diff (one whole archive page)**

```js
const page = await figma.getNodeByIdAsync(PAGE_ID);
await figma.setCurrentPageAsync(page);
const texts = n => [...new Set(n.findAll(x => x.type === 'TEXT').map(t => t.characters.trim()).filter(s => s && s.length < CFG.sync.text_diff_max_len))];
const sub = (sec, re) => sec.children.filter(c => c.type === 'SECTION' && re.test(c.name));
const out = [];
for (const grp of page.children.filter(c => c.type === 'SECTION')) {
  for (const task of grp.children.filter(c => c.type === 'SECTION')) {
    const tb = sub(task, new RegExp(CFG.sync.pair_patterns.to_be, 'i')), ai = sub(task, new RegExp(CFG.sync.pair_patterns.as_is, 'i'));
    if (tb.length && ai.length) {
      const T = new Set(tb.flatMap(texts)), A = new Set(ai.flatMap(texts));
      out.push({ grp: grp.name, task: task.name, mode: 'diff',
        onlyToBe: [...T].filter(x => !A.has(x)), onlyAsIs: [...A].filter(x => !T.has(x)) });
    } else {
      out.push({ grp: grp.name, task: task.name, mode: 'flat', all: texts(task).slice(0, 70) });
    }
  }
}
return out;
```

**Finding the keywords in canonical frames**

```js
const KW = [/* the strings from the diff above */];
function tf(n, acc) {   // dig through the section hierarchy, collect screen frames only
  for (const c of n.children || []) {
    if (c.type === 'SECTION') tf(c, acc);
    else if (['FRAME','COMPONENT','INSTANCE'].includes(c.type) && !c.name.startsWith('[label]')) acc.push(c);
  }
  return acc;
}
const res = {};
for (const kw of KW) res[kw] = [];
for (const f of tf(figma.currentPage, [])) {
  const txt = f.findAll(x => x.type === 'TEXT').map(t => t.characters).join('');
  for (const kw of KW) if (txt.includes(kw)) res[kw].push(f.name);
}
return res;   // an empty array means that keyword is absent from canonical
```

**Structure comparison (can this be a value edit?)**

```js
// Run on each page separately and compare the results (one setCurrentPageAsync per script)
const f = await figma.getNodeByIdAsync(FRAME_ID);
return f.findAll(x => x.type === 'TEXT').map(t => `${t.parent.name}|${t.characters.replace(/\n/g,' ')}`);
// Same length, same order, same parent names on both sides → only values differ → value edit is safe
```

**Value edit (guard plus font loading)**

```js
const edits = [/* [textNode, newValue] pairs */];
if (edits.length !== EXPECTED) throw new Error(`aborted: expected ${EXPECTED}, got ${edits.length}`);
const fonts = new Set();
for (const [t] of edits) for (const s of t.getStyledTextSegments(['fontName'])) fonts.add(JSON.stringify(s.fontName));
for (const fs of fonts) await figma.loadFontAsync(JSON.parse(fs));
for (const [t, v] of edits) t.characters = v;
return { mutatedNodeIds: edits.map(([t]) => t.id) };
```

**Four-edge intersection check before stretching a section**

```js
const t = target.absoluteBoundingBox;
const T = { x: t.x, y: t.y, r: t.x + t.width, b: t.y + t.height };   // computed with the post-stretch values
return figma.currentPage.children.filter(c => c.type === 'SECTION' && c.id !== target.id)
  .map(s => { const b = s.absoluteBoundingBox;
    return { name: s.name, hit: b.x < T.r && b.x + b.width > T.x && b.y < T.b && b.y + b.height > T.y }; })
  .filter(s => s.hit);   // must be empty to be safe
```

## Traps

| Trap | What to do |
|---|---|
| Identical frame names make every name comparison say "match" | Judge on the three content signals. Names are only for pairing |
| Comparing archive pages and stopping there | The "done" band under a divider is where un-applied work actually hides — always include the `match: divider` axis |
| The pair's current side was overwritten after the work and now matches the new version | Classify it as un-comparable and inspect canonical's structure directly |
| Replacing a whole frame breaks external deep links | When the structure matches, edit values only. If a move is unavoidable, report which links will break |
| A stretched section invades its neighbour | Compute the four-edge intersection with post-stretch coordinates. Do not check vertically alone |
| Mistaking a section child's coordinates for absolute | A section child's x/y are relative to the parent section |
| Editing text without loading the font | Read the node's current fonts and load them. Never assume a default |
| Putting reference material in a canonical section | Put it in a lint-excluded section to prevent false positives |
| Deleting an empty working page as part of another confirmation | Page deletion is its own gate. Confirm zero children first |

## Constraints

- Steps 1 and 2 are **zero writes** — no node changes during the audit
- Every write in steps 3 and 4 goes through **preview → go**. With several pieces, pass a gate per piece
- **Page deletion is an independent gate** — never folded into another confirmation
- Any judgement the config does not cover (value edit versus move) has its reasoning written into the report each time
- Archive pages are never renamed or moved by this skill — only named as candidates
- Never "improve" canonical in a direction the new version does not have. Applying means matching the new version, and stopping there
