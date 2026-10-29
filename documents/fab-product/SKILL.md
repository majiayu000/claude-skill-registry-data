---
name: fab-product
description: Preparing an UEFN project to be sold on Fab (a Fab product, not a map). Read it when the project is registered as a Fab product, when the owner talks about Fab, a listing, the UEFN Source archive, screenshots for the listing or the product's documentation.
last_reviewed: 2026-10-23
sources: [official-docs]
---

# Fab product (UEFN Source)

A Fab product is a small UEFN project whose components the customer adds to their own project. The kit installs NOTHING in it (no `Claude/`, `.claude/`, `CLAUDE.md`, no Python): Epic does not allow `.py` files in an UEFN Source archive. Everything here works from your profile, with `~/.claude/hooks/fab_pack.py`.

## Epic's rules for the archive (Fab documentation, "Upload UEFN source to Fab")
- The archive is the complete project folder zipped: exactly one project, with project file, plugin file and all content; not encrypted.
- No Python scripts; no `Saved` or `Intermediate` folders.
- Every asset path 140 characters or fewer, including the top-level folder name. Count it as `<ProjectName>/Content/...`.
- English letters, digits and underscore only in folder and file names; clear names, not generic ones such as `Assets` or `NewFolder`; no unused folders.
- Declare third-party software and assets in the listing.

## The helper (run it, do not recount by hand)
- `python ~/.claude/hooks/fab_pack.py check <project>`: what blocks the upload (exit 1), warnings (empty folders, third-party content such as VerseUIKit, another project's names in the assets), notes (information only, such as `.lore` files that `zip` already leaves out).
- `python ~/.claude/hooks/fab_pack.py docs <project> [--apply]`: dry run first, then writes, INSIDE Content in the folder that holds the product's assets (`Content/<Product>/`), `Documentation/` (README.md, SETTINGS.md) and `FabListing/` (listing.md, third_party.md, screenshots.md). It never overwrites; `Documentation/SETTINGS.md` is regenerated from the code (the `@editable` settings with defaults and each file's Summary) until the owner edits it.
- `python ~/.claude/hooks/fab_pack.py zip <project>`: writes `<ProjectName>.zip` next to the project: the WHOLE project (Fab wants it all), without `.py`, `Saved`, `Intermediate` and kit files; it refuses when names or paths still break the rules.

## How to work
1. Run `check`. COUNTING RULE: the three lists are never added together. Say "N blocks, M warnings" from the first two lists only, and mention the notes on a separate line as information ("nothing to do"). A note is never a warning: `.lore`, `.loreignore`, `.urcignore` and `*.code-workspace` in the project root are a note (`zip` leaves them out), so they never make the package "not ready". The Checklist page of the console counts the same way (one item per kind of problem, so several messages of one kind show as one warning with "+N more"): quote its numbers when you give a verdict, and say the number of messages only as detail. Report the blocks in plain words; never rename or move assets without the owner's yes (a rename must keep references working: use the editor's move/rename, not the file system).
2. Run `docs` (dry run), tell the owner what would be created, then `--apply`.
2b. TAGS: choose the listing tags ONLY among the ones the portal suggests: `python ~/.claude/hooks/fab_checklist.py tags` prints them by category (the Checklist page shows your tags in red when one is not in that list). Pick the ones that really describe the product, write them in `## Tags` of `listing.md`, and replace any tag that is not in the list. Never use generic tags (Fortnite, UEFN, widget, material...).
3. The listing Description is customer text for the portal: never write in it a file name of the package (third_party.md, README.md...), nor sentences about the kit or the check. Third-party content is declared in the portal's own field. Fill the TODO fields from what the code and level really contain (`fab_pack.py listing-fill <project>` fills the Technical details of the listing by itself; you write the texts); do not invent features. PRICE, SUBCATEGORY AND LICENCES ARE THE OWNER'S, decided at publication: never write them, never ask for them, never leave a field for them in any file of the package, and do not list them among the things still to do.
4. Third-party content: `FabListing/third_party.md` is filled ONLY with what the owner declares. You write no row, no note and no remark of your own in it (not even "this is an Epic mount"). If you notice something that may be third-party (for example VerseUIKit, or an imported image), tell the owner in the reply and stop there.
5. Verse code the customer receives keeps the header rule: Summary, real date, version; changes are not listed in the file.
6. Materials: when the owner confirms a material works, save its recipe (`skills_lib.py recipe-add materials <file.json> "<product name>"`, run from `~/.claude/kit-template/Claude/hooks/`); that is what the materials skill learns from. Say it in the reply, with the recipe name.
7. Mechanics: before building a stand-alone device, a mechanic or a map template, look for a recipe (`skills_lib.py recipes mechanics <keyword>`) and follow it. When the owner confirms one works, run `fab_lab.py draft-recipe <project> "<name>"` (from `~/.claude/hooks/`), fill every TODO (devices, settings, wiring, Verse files, assets, how to verify) and save it with `skills_lib.py recipe-add mechanics <file.json> "<product name>"`. It counts as confirmed at once; say the recipe name in the reply.
7. Lessons: your UEFN MCP calls are recorded outside the project (`fab_lab.py`, folder `~/.claude/fab-lab/<Product>/`). When a material or mechanic is finished, run `python fab_lab.py card <project>`, fill the TODO parts of the draft (goal, final recipe, traps, third-party assets) and ask the owner whether to promote it into a skill or recipe. Never write lesson files in the project.
8. Before saying "ready": `check` has no blocks, no TODO is left in `FabListing/listing.md`, and tell the owner it is ready. NEVER run `zip` on your own: only when the owner asks for it, and not while the listing or the documents still have TODO. There is no "test the zip in a clean project" step.

## Rules learned from two rejected products (apply them from the first minute)

These come from a real case (assets copied by hand between the owner's projects). Fab validates the whole project offline, and the editor's own validation may look only at the assets you touched, so "no errors here" proves nothing.

1. **Scan at the start, not at the end.** First thing in a Fab project run `fab_assets.py <project>` (or `fab_pack.py check`). It lists imports of assets of another project, internal names of another project and Windows user names saved in the import paths. Report it in plain words before building anything.
2. **Never copy assets by hand from another project into a Fab product** without telling the owner: they bring the old internal name and sometimes a real import (`/OtherProject/.../Asset`) that does not exist here. Rebuild or re-save them inside this project and scan again.
3. **Do not use `update_metadata_tags`** on assets of a Fab product.
4. **Use the exact parameter names** from the tool table (`mcp_map.py --find`); do not guess them.
5. **Never call `list_properties` on textures**: the output is huge and useless. Read only the property you need.
6. **Never edit `.uasset` bytes yourself.** The kit does the one safe change by itself, before every `check` and `zip`: Windows user names and the names of your other projects inside source paths become `x` of the same length (same file size, a backup in the lab folder outside the project). Anything else is fixed in the editor.
7. A file is locked while the editor is open: that is normal, not a reason to close the editor by yourself. When the owner agrees (ask once), `fab_clean_cycle.py <project> --apply` closes UEFN politely, cleans, reopens the project and re-checks.
8. When the owner records the UEFN validation (Checklist page) with Skip Fix-up, do not offer "Run Validation Fix-up": it resets illegal references to default and can break the product.
9. **`Content/Collections` and `Content/Developers/<user name>` (with its own `Collections`) belong to the project, even when empty.** The editor creates and keeps them; they are decided and whitelisted by the owner. Never report them as empty or unused folders, never count them as a warning, and never propose deleting or moving them. The kit's `check` and Checklist already ignore them: if you see them, say nothing.
10. **SETTINGS.md exists only when the product has Verse code** (it documents the `@editable` settings). A product with no Verse file has no SETTINGS.md: do not create it, do not ask for it and do not count it as missing.
11. **`Documentation/AUTHOR.md` is always created by `docs`** (Verse or not): it holds the owner's saved signature block. Do not write or change it yourself; if it says there is no signature saved, tell the owner to save one.

## Verse files of a Fab product (this style only here, never in maps)
Every `.verse` file the customer receives is written as a small manual. Header, in this order, all `#` lines between dashed rules:
1. `# <Name>.verse`, then `# Title  -  vN  (last modified: YYYY-MM-DD)` with the real date; raise N at every substantial change (the change history is not kept in the file).
2. `WHAT IT DOES`, `WHY IT IS USEFUL`, `QUICK SETUP` (numbered, one line per setting of the Details panel, ending with the DebugLoggingEnabled hint), `GOOD TO KNOW` (limits and surprises).
3. `Author:` and then the owner's signature block (ASCII art and links). Never write it from memory: it is saved once with `python ~/.claude/hooks/fab_pack.py signature save <a finished verse file>` and printed with `header <Name>` (layout plus signature). If none is saved, ask the owner for a finished file; do not invent links.
Body: numbered section comments (`# --- 1. TAG DEFINITIONS ---`), a comment above every class, every `@editable` and every function saying what it is for in the customer's words, and short comments on the non-obvious lines. `check` warns when a header misses a part or the saved signature.

Listing screenshots and thumbnails are NOT made by the agent: no viewport captures, no camera moves, no `grid`, no Content Browser thumbnails (too small, and the owner makes them himself). Do not offer to make them and do not list them among the things still to do.
