---
name: paprika-recipes
description: >-
  Use when working with a Paprika Recipe Manager 3 library on macOS — looking
  up, searching, listing or exporting saved recipes, or turning any text source
  into a real recipe: a web page the clipper failed on, prose, a PDF, a note, a
  photo of a cookbook page. Triggers: Paprika, recipe library, add a recipe,
  import recipe, paprikarecipe, recipe collection, cookbook.
license: MIT
metadata:
  author: eins78
  repo: https://github.com/eins78/agent-skills
  version: "1.1.1"
---

# Paprika Recipe Manager 3 (macOS)

Read the local library directly from its database. Create recipes through the
app's own import format. Both paths are verified against a live install of
Paprika 3.8.4; see `references/recipe-format.md` for the evidence.

**The app has no AppleScript dictionary and no URL scheme.** Its only scripted
surfaces are the SQLite database (read) and the file import (write). That is
enough — there is no need for the Paprika cloud API or an account password.

## Prerequisites

- Paprika Recipe Manager 3 installed (Mac App Store build, sandboxed)
- `sqlite3`, `zip`, `unzip` — all present on macOS
- Node 18+ for the helper scripts (zero npm dependencies)
- For `--confirm`: Automation permission for the controlling terminal. macOS
  asks once; **the user approves it**. Until then `osascript` fails with
  `-1743` and the import must be confirmed by hand.

## Reading the library

Safe while Paprika is open. Every query goes through `sqlite3 -readonly`;
nothing here writes to the live database.

```bash
node ${CLAUDE_SKILL_DIR}/scripts/paprika-db.mjs count            # totals + sync revisions
node ${CLAUDE_SKILL_DIR}/scripts/paprika-db.mjs list             # all active recipes
node ${CLAUDE_SKILL_DIR}/scripts/paprika-db.mjs list --search miso
node ${CLAUDE_SKILL_DIR}/scripts/paprika-db.mjs get "Miso Soup"  # one recipe, full JSON
node ${CLAUDE_SKILL_DIR}/scripts/paprika-db.mjs categories       # categories + counts
node ${CLAUDE_SKILL_DIR}/scripts/paprika-db.mjs photo "Miso Soup"
node ${CLAUDE_SKILL_DIR}/scripts/paprika-db.mjs snapshot /tmp/paprika.sqlite
```

`get` emits **the same JSON shape the import format uses**, so its output can
be edited and fed straight back to `paprika-recipe.mjs`.

Three details the script handles so callers don't have to: `ZCREATED` is a Core
Data timestamp (2001 epoch, not Unix), trashed recipes must be filtered on
`ZINTRASH`, and categories live behind a generated join table.

**Never `cp` the database and read the copy with `-readonly`** — a copy keeps
`journal_mode=wal` and SQLite then refuses to open it (`unable to open database
file (14)`) because it cannot create the `-shm` sidecar. Use `snapshot`, which
uses `VACUUM INTO`.

### Don't write to the database directly

`ZSTATUS`, `ZISSYNCED` and `ZSYNCHASH` are bookkeeping the app maintains for
cloud sync. A hand-written row risks corrupting the library and confusing sync
across devices. Import is the supported write path, and it is not slower.

## Creating a recipe from any text source

This is the main capability. The agent does the understanding; the script does
the mechanical part.

**1 — Read the source.** A web page, a note, a PDF (`pdftotext file.pdf -`, or
the `pandoc` skill), a photo of a cookbook page, a pasted message, a chat
transcript. Anything you can read — and, via *Video sources* below, anything
you can only hear.

> **When the user names a source, find *that* source.** If a search comes back
> empty, that is evidence about the search, not about the user's memory. Never
> substitute a similar-looking document you found elsewhere — a plausible
> substitute produces a recipe that is wrong in ways nobody can see afterwards,
> because it is internally consistent and correctly attributed to the wrong
> thing.
>
> The specific trap: **a container's text is not its contents.** Attachments,
> embeds and linked files usually live outside the body you just searched, and
> they are often unidentifiable by name — Apple Notes titles *every* scanned PDF
> literally `PDF` with a null filename, so four different recipes look like four
> identical rows. Enumerate the attachments and extract each one's text. A
> title-based scan finds nothing while looking thorough.

**2 — Structure it as JSON.** The only required field is `name`.

```json
{
  "name": "Rhabarberkompott",
  "ingredients": "200 g Rhabarber\n1 Vanilleschote\n2 EL Zucker",
  "directions": "Rhabarber rüsten und in 1 cm breite Stücke schneiden.\n\nVanilleschote längs halbieren, Mark herauskratzen.\n\nAlles ca. 5 Minuten köcheln lassen.",
  "notes": "war nicht süß genug",
  "servings": "2 servings",
  "source": "migusto.migros.ch",
  "source_url": "https://migusto.migros.ch/de/rezepte/rhabarberkompott",
  "categories": ["Dessert"]
}
```

Rules that actually bite:

- **`ingredients` and `directions` are newline-delimited plain text**, not
  arrays. One ingredient per line.
- **End a section header with a colon.** A line whose *last character* is `:`
  renders as a bold, highlighted subsection header — a real Paprika formatting
  feature. So write `For the dressing:`, never `For the dressing` or
  `For the dressing (makes 200 ml)`. This is an authoring rule, not a curiosity:
  a header without the trailing colon silently renders as an ordinary
  ingredient line, and nothing about the stored data reveals the difference.

  ```
  For the dressing:          ← bold header
  2 tbsp rice vinegar
                             ← blank line separates the blocks
  To serve:                  ← bold header
  Sliced tomatoes
  ```

  The colon must be **last**, not merely present: `Salt: about 2 g` stays a
  plain line. And it is a *rendering* rule — the colon is ordinary stored text,
  so never strip it when reading, editing or round-tripping.
- **`servings`, `prep_time`, `cook_time` are free text**, not numbers —
  `"2 servings"`, `"15 mins"`.
- **`categories` are plain names, and an unknown name creates a category.**
  This is a side effect with no undo path in this skill, and it **outlives the
  recipe**: a category is its own row in `ZRECIPECATEGORY`, so deleting the
  recipe that introduced it leaves the category behind, to be removed by hand
  in the app. Verified. Always run `paprika-db.mjs categories` first and reuse
  existing names; a typo or a near-duplicate ("Desserts" vs "Dessert")
  permanently pollutes the sidebar on every synced device.
- **Omit `uid`, `hash`, `photo_hash`.** The app assigns them.
- **`created` is ignored** — the app stamps its own import time.
- **Keep the source language.** Libraries are frequently mixed-language; don't
  translate a recipe on the way in.
- **Put substitutions and results in `notes`** — that is what the field is for
  in practice (*"Replace the butter with 60 g vegan block."*).
- **Don't invent what the source doesn't say.** If a source gives ingredients
  but no method, leave `directions` empty and record that in `notes`. A
  plausible-sounding invented step is indistinguishable from a real one once
  it's in the library.
- **Link to another recipe with `[recipe:Name]`** — see below. Whenever a
  source says *"serve with X"* or calls for a component the library already
  has, that is a link, not a plain string.

### When the recipe is only spoken — video sources

A reel, short or TikTok may carry no recipe text at all: not in the caption,
not on the page. The recipe is then in the narration, and you can still get it
— transcribe the audio (`yt-dlp` to fetch, any speech-to-text to read it).
The mechanics are ordinary; what is specific to recipes is what you do with
the result.

- **Read the caption first.** Many food accounts put the whole recipe there,
  which saves the entire exercise. When they don't, the caption still names
  the dish and the creator — that is your `source`.
- **On-screen text is usually auto-subtitles, not an ingredient card.** It
  looks like a recipe overlay in thumbnails and isn't: it is the narration,
  one phrase at a time. Check a handful of spread-out frames before deciding
  the video shows quantities in writing.
- **Cross-check every amount against what the video shows.** This is the step
  that makes a heard recipe trustworthy, and it is not optional. Cooking
  videos put a scale, a jug or a labelled pack on screen at the moment each
  amount goes in. Confirm the digits against the words. A mis-heard quantity
  is quiet and plausible — it yields a recipe that reads perfectly and cooks
  wrong, and nothing downstream will catch it.
- **Structure, never paste.** Write your own `directions`. A transcript is
  speech: filler, asides, the same step twice. Keep the technique and the
  reasons a cook needs; drop the talk.
- **Expect subtitles burned into the photo.** Every frame of a subtitled video
  carries text, so there is no clean frame to hunt for. Take the one that best
  shows the finished dish.
- **Say so in `notes`.** Record that the amounts came from narration, and what
  you checked them against, so a later reader knows the recipe was heard
  rather than read.

### Choosing an import format — native by default

**When this skill writes a file, write the native format.** `.paprikarecipe` for
one recipe, `.paprikarecipes` for several.

```bash
node ${CLAUDE_SKILL_DIR}/scripts/paprika-recipe.mjs build recipe.json --out ~/Downloads/r.paprikarecipe
node ${CLAUDE_SKILL_DIR}/scripts/paprika-recipe.mjs bundle a.json b.json --out ~/Downloads/two.paprikarecipes
```

It carries 24 fields to `.yml`'s 15, is the only format that can **update** an
existing recipe (via `uid`) or carry a **photo**, and is the only one that can be
**imported automatically** — `open` routes it by file type, then `--confirm`
clicks a button on a sheet that identifies itself.

A second format exists: vendor-documented plain-text **`.yml`**, produced by the
`yaml` subcommand. It is kept and documented, and it is the right choice in two
cases:

- **a human hand-authoring** a recipe in a text editor and importing it themselves
- **conversion scripts from other structured data** — when something already holds
  recipe-shaped data, emitting YAML (which is just JSON) is often easier than
  producing the gzipped native format

Both cases accept the same two costs: **no update or round-trip** (there is no
`uid`, so re-running a conversion duplicates rather than corrects) and a
**manual import** — `.yml` is not associated with the app, so it goes through
File → Import on macOS or Settings → Import on iOS.

```bash
node ${CLAUDE_SKILL_DIR}/scripts/paprika-recipe.mjs yaml recipe.json --out ~/Downloads/r.yml
```

📖 Full comparison, evidence and the failure modes:
[`references/import-formats.md`](references/import-formats.md).


### Linking to another recipe — `[recipe:Name]`

Paprika resolves a `[recipe:Exact Recipe Name]` token in a text field into a
tappable link to that recipe. It is **plain text in the stored field**, not a
separate column — which is why it survives the interchange format untouched.

```
1 tbsp [recipe:Spice Rub]              inline, after a quantity
Vegan Ricotta ([recipe:Cashew Ricotta]) in parentheses, beside a label
Serve with:
[recipe:Chili / Garlic Oil]           standalone on its own line
```

What is verified:

- **It resolves by name, not by uid.** The token carries a name; the name may
  contain spaces, slashes and punctuation. It must match the target's `name`
  **exactly** — so rename a linked recipe and the link goes stale.
- **It round-trips.** The token survives `get` → `build` → `import` and appears
  verbatim in Paprika's own `.paprikarecipes` export. Nothing escapes or
  rewrites it.
- **An unknown target is harmless to write.** Importing a recipe whose token
  names a recipe that does not exist succeeds normally — no error, no crash.
- **Rendering is confirmed for `ingredients`.** A token in that field displays
  as a tappable link — observed in the Paprika **iOS** app. The stored format is
  identical on both platforms, but rendering was not separately checked on macOS.

What is **not** verified: how a token renders in `directions` or `notes` (it is
*stored* there fine, and real libraries do use it in `notes`), and what an
unknown target looks like on screen — plain literal text or a dead link. If
that matters, put links in `ingredients`, which is the field that is proven.

#### Link both ways

A dish links **down** to its component in `ingredients`. Also link the component
**back up** to the dishes that use it, in its `notes`:

```
Used with:
[recipe:Roast Carrots with Spice Rub]
[recipe:Grilled Aubergine with Spice Rub]
```

Without it the relationship is one-way. Opening the component — which is exactly
what happens when someone is deciding whether to make a batch — gives no way to
reach the dishes it was made for. That is the moment the answer is most useful.

Keep it to the list. The dish already describes the dish; a paragraph here just
goes stale when a dish changes.

Two caveats specific to this direction:

- It lives in `notes`, where **rendering is unverified** (see above). Real
  libraries do use links there, but if you need a guaranteed-rendering link,
  `ingredients` is the proven field.
- Every back-link is another name to keep in sync. Links resolve by name, so
  renaming a dish silently breaks its component's back-link as well as any
  forward link. Prefer back-links on components that are genuinely reused;
  a one-off does not need one.

Because a link is just text, **check the target exists before emitting one**:

```bash
node ${CLAUDE_SKILL_DIR}/scripts/paprika-db.mjs list --search "Spice Rub" \
  | jq -r '.[].name'   # must print the name exactly as you'll write it
```

**3 — Build and import.**

```bash
node ${CLAUDE_SKILL_DIR}/scripts/paprika-recipe.mjs build recipe.json --out ~/Downloads/recipe.paprikarecipe
node ${CLAUDE_SKILL_DIR}/scripts/paprika-recipe.mjs import ~/Downloads/recipe.paprikarecipe --confirm
```

Attach a photo with `--photo image.jpg` (embedded as base64 in the file; must
be a JPEG). Import several at once by building a bundle:

```bash
node ${CLAUDE_SKILL_DIR}/scripts/paprika-recipe.mjs bundle a.json b.json --out ~/Downloads/batch.paprikarecipes
```

### Photos replace, they don't merge

The single most destructive behaviour in this format, verified by test:

- **An import overwrites the recipe's photo state.** A file with no embedded
  image sets the photo to null *and deletes the JPEG from disk*. There is no
  "leave the photo alone" — silence means delete.
- **`photo_data` without a `photo` filename terminates the app** mid-import.
  No recipe written, no error dialog — the app is simply gone. macOS writes a
  crash report (`~/Library/Logs/DiagnosticReports/`): `SIGABRT` from an
  uncaught exception on an `NSManagedObjectContext` queue. Check there before
  concluding an import "did nothing".
  The filename is where the decoded JPEG gets written; it is not optional.

`paprika-recipe.mjs build` handles both: it re-embeds the current photo
whenever the input carries a `photo_path` that exists on disk (`paprika-db.mjs
get` fills that in), and it always emits a filename alongside `photo_data`.

When a recipe names a photo that **isn't on disk**, `build` refuses outright
rather than writing a file whose import would delete it:

```
error: "Miso Soup" refers to photo AE175116-….jpg, but no local JPEG was found
```

That happens when the photo hasn't been downloaded from Paprika Cloud yet —
most likely soon after a fresh install, while the library is still syncing.
Open the recipe in the app so the photo downloads, then retry. Pass
`--no-photo` only when removing the photo is what you actually want.

`photo_hash` is computed by the app — an uppercase SHA-256 of the JPEG bytes.
Never supply it. Re-importing byte-identical image data is a no-op.

**4 — Verify, always.**

```bash
node ${CLAUDE_SKILL_DIR}/scripts/paprika-db.mjs list --search "Rhabarberkompott"
```

### The import is not headless

Paprika raises a modal sheet on its main window:

> **Import Recipes** — Are you sure you want to import the recipes contained in
> this file? *Format: Paprika (paprikarecipe)* — `Cancel` / `Import`

then a second sheet: **Import Complete** — *Successfully imported 1 recipes.* —
`OK`.

`--confirm` clicks through both via System Events, but only after checking the
sheet's own text; anything unexpected is left alone for a human. Without
`--confirm`, tell the user to click Import — don't report success until the
database confirms it.

#### When `--confirm` appears to hang

Observed once: the command produced no output and had not exited after about
five minutes, while Paprika sat with the `Import Recipes` sheet already open.
The cause was **not** reproduced — so treat the symptom, and don't assume it
was a denied Automation permission, which fails differently (error `-1743`,
and promptly).

- **Don't pipe the import through `tail` or `head`.** `tail` emits only at
  EOF, so killing a stuck pipeline shows you nothing whatsoever — including
  the `handed to …` and `confirmed: clicked Import` progress lines that tell
  you how far it actually got. Run it unpiped.
- **Check for an open sheet before re-running anything.** If a sheet is up,
  `open` already succeeded, and running the import again just stacks a second
  sheet behind the first:

  ```bash
  osascript -e 'tell application "System Events" to tell process "Paprika Recipe Manager 3" \
    to return value of static text of sheets of windows'
  ```

  If that prints the import text, click *that* sheet rather than re-importing:
  `click button "Import" of sheet 1 of window 1`, then `button "OK"` on the
  completion sheet. Verify against the database either way.
- **Before killing it, check every PID.** `pgrep -f paprika-recipe.mjs` also
  matches the shell you typed the command into, because the pattern appears in
  that shell's own command line. Run `ps -o pid,ppid,command` over the matches
  and kill only the `node …` process and its wrapper — never the bare `pgrep`
  output.

### Editing an existing recipe

Importing a file whose `uid` matches an existing recipe **updates that recipe in
place** — the app reports *"1 recipes updated"* and the row count doesn't change.

```bash
node ${CLAUDE_SKILL_DIR}/scripts/paprika-db.mjs get "Some Recipe" > edit.json
# edit the JSON, keeping its uid
node ${CLAUDE_SKILL_DIR}/scripts/paprika-recipe.mjs build edit.json --keep-ids --out ~/Downloads/edit.paprikarecipe
node ${CLAUDE_SKILL_DIR}/scripts/paprika-recipe.mjs import ~/Downloads/edit.paprikarecipe --confirm
```

`--keep-ids` is the only destructive flag here. Three caveats:

- Categories **merge** rather than replace — an import can add a category to a
  recipe but cannot remove one.
- The original `created` is preserved.
- The photo is **replaced**, not merged. Piping `get` output into `build` as
  shown above carries it over; a hand-written JSON with no `photo_path` deletes
  it. `build` refuses when it can see a photo it cannot embed, but it cannot
  detect a photo you never told it about. See "Photos replace, they don't merge".

## One source, several recipes

A source that gives a component plus dishes made from it — a sauce and two
salads that use it — can go in as one recipe or several. Both shapes appear in
real libraries:

| Shape | How | Use when |
|---|---|---|
| **Sectioned** | One recipe; `ingredients` carries labelled blocks (`For the Sauce:`, `To Serve:`) | The component only exists to serve this dish |
| **Extracted** | The component becomes its own recipe; each dish names it as an ingredient line (`2 tbsp Garlic Confit`) | The component is reusable across dishes |

The deciding question is **"would the user make this component for something
else?"** — if the source itself uses it in more than one dish, that's a yes.

**Extracting is cheap because of `[recipe:Name]`** (above): each dish links to
the component and the link is tappable, so the two aren't merely related by a
matching string. Write the ingredient line as `80 g [recipe:Garlic Confit]`,
not a bare name — and link the component back to its dishes in `notes`, so the
set is navigable from either end.

The one real cost that remains: the shopping list adds the component as a
**single line** rather than expanding it into its own ingredients, so shopping
for a dish you haven't already got the component for takes two steps.

**Ask rather than guess.** Check the library's existing habit first
(`paprika-db.mjs categories` — a large "Condiments"-style bucket is a strong
signal the user extracts components), then confirm before importing several
recipes from one source.

## Other import paths

**Web clipper — works almost always.** The share extension
(`Paprika Mac Share.appex`) takes a page from the browser share sheet and
parses the recipe out of it. This is the normal route for a URL, and it is
better than anything this skill does: it gets the photo, the source, and the
structure in one step. **If the user gives you a recipe URL, suggest the
clipper first.**

**Manual import — when the clipper can't parse the site.** Paprika says so
plainly: *"We couldn't process the recipe on this site. But don't worry, you
can still save the recipe using the clipboard tools below."* The fallback is
the app's own **Browser** tab plus its clipboard tools (`Smart Copy/Paste`,
`Detect Clipboard URLs`): open the page in Paprika's browser, select the
ingredients, paste into the ingredients field, repeat for directions.

**This skill is the third option** — and the only one that works for sources
that aren't a web page at all, or when the work should happen without a human
driving the UI field by field. For a page the clipper failed on, fetching the
page and structuring it here is usually faster than manual copy-paste.

## Sync — an import is not local

**A local import publishes to every device on the account. Verified** on a
separate device (Paprika iOS over cellular, away from the Mac) minutes after a
Mac-side import: title, star rating, categories, source, prep time, servings,
ingredients and directions as separate lines, and notes all survived.

Consequences worth taking seriously:

- **There is no local-only mode and no dry run.** An imported recipe lands with
  `ZISSYNCED=1` and is already on its way out. You cannot "test quietly."
- **A mistake is not confined to this machine.** A bad bulk import shows up on
  the user's phone within a minute. This is why the caution against
  bulk-writing is not bureaucratic — undoing it means deleting recipes on a
  device you don't control.
- Test with **one** obviously-named throwaway, then tell the user it exists.

**Don't act on recipe counts while a sync is landing.** A fresh install pulls
the library in over minutes (observed: 122 → 259 rows over ~15 minutes). Before
anything that depends on a total, check that `paprika-db.mjs count` returns the
same totals *and* the same `sync_revisions` twice, at least 60 s apart.
