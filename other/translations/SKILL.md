---
name: translations
description: "Translate a Mendix app's user-visible strings with MDL — DESCRIBE TRANSLATIONS to export one file per language, CREATE [OR MODIFY|REPLACE] TRANSLATIONS to write them back. Use when localising an app, filling in a language with an LLM, or auditing which strings are still untranslated. Covers why a translation can be stored and still never appear."
---

# Translations

Every user-visible string of a Mendix app — page titles, widget captions, button
labels, validation messages, enum captions, menu items — is a `Texts$Text` with
one translation per language. MDL treats them in bulk: one file per language.

## The loop

```bash
# 1. export: an untranslated string comes back with an EMPTY target
mxcli -p app.mpr -c "describe translations for de_DE" > de_DE.mdl

# 2. fill in the right-hand sides (by hand, or hand the file to an LLM)

# 3. write them back
mxcli exec de_DE.mdl -p app.mpr
```

That is the whole design: `DESCRIBE` emits the `CREATE` form, so the export
format and the import format are the same file, and the empty targets are the
prompt.

## Statements

```sql
describe translations [in <Module>] for <lang>;

create translations            [in <Module>] for <lang> ( 'src' as 'target', ... );
create or modify translations  [in <Module>] for <lang> ( 'src' as 'target', ... );
create or replace translations [in <Module>] for <lang> ( 'src' as 'target', ... );
```

Entries use `as`, not a colon: a translation maps a user-provided name to another
name.

| verb | meaning |
|------|---------|
| `create` | the "add a language" form — **refuses** if that language already has translations anywhere in scope |
| `create or modify` | merge; a source string the file does not name keeps whatever it has |
| `create or replace` | the file is authoritative — a translation whose source the file does **not** name is **removed**, and the run names what it deleted |

`IN <Module>` scopes both directions, and under `OR REPLACE` it **bounds the
deletion** — without it, a set of per-module files would wipe each other on every
run.

## The trap: a language that is not enabled

**A translation for a language the project has not enabled is stored, passes
`mx check`, and is discarded at build time.** Measured with
`mxbuild --target=deploy`: the string reaches nothing under `deployment/` — no
`translations_<code>.properties` is produced at all — while the model and Studio
Pro both keep it happily.

So translating 400 strings into German can produce exactly no German in the app.
`create translations` warns when the language is not enabled; enable it in
project settings first (see the **project-settings** skill), then re-run.

A stock app makes this easy to hit by accident: it enables **one** language while
its marketplace modules ship translations in **nine**, so "other languages
already have translations here" is true and misleading.

> `list languages` lists languages that have **translations**, not the enabled
> ones — a stock app reports 8 while 1 is enabled. `describe settings` has the
> enabled list.

## Drift: a source string that was edited

The dictionary is keyed on the **source string**, so `Save` is translated once
for all the places it occurs. The flip side: editing a source string after the
file was written stops it matching, which would leave the translation attached to
a string that no longer exists.

A key that matches nothing is **reported, not skipped** — and where the
translation identifies the moved source unambiguously, the run names the fix:

```
Warning: 1 source string(s) in the file matched nothing in the project.

  "Thingz" as "Grejer"
      No text has "Thingz" as its source. A text now reads "Things" and carries
      the sv_SE "Grejer" — the source was probably edited. Change the file to:
        "Things" as "Grejer"
```

## Notes

- **Scale.** A whole app is a few hundred distinct source strings (411 on a real
  project measured), so one file per language is comfortably practical.
- **A rewrite does not lose other languages.** Re-executing a page or microflow
  keeps the translations MDL cannot express; you do not have to re-import a
  language after editing a document.
- **The source language** is the project's default: the left-hand column is what
  `DESCRIBE` shows for that language, so change `DefaultLanguageCode` before
  exporting if you want a different source. It is also **the language a new
  caption is written in** — `Caption: 'Opslaan'` is stored under the default, so
  set it *before* authoring pages, not after. Changing it later does not move
  text that already exists, and nothing warns: `mx check` is 0 errors either way
  (mendixlabs/mxcli#970). Re-running the `create` statements fixes it. See
  [project-settings](../project-settings/SKILL.md).
- Translating **into** the source language is refused — it would overwrite the
  strings everything else is keyed on.

## Common tasks

```sql
mdl 1;
-- what is still untranslated, and how much
describe translations for de_DE;        -- ends with "N source string(s), M translated, K to go."

-- one module at a time
describe translations in Sales for de_DE;

-- make a file authoritative for one module only
create or replace translations in Sales for de_DE ( 'Order' as 'Bestellung' );

-- remove a language's translations entirely
create or replace translations for de_DE ( );
```
