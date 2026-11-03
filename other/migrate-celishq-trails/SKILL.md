---
name: migrate
description: Rewrites the stored celis patterns of an old form that celis no longer reads, and the old one-line patterns into the five lines Name, When, Forces, Do and Because, and closes the older trails. Use when the person runs /celis:migrate, or asks to move their old rules to patterns.
---

You rewrite each pattern of an old form, and each live pattern in the old one-line form into the five
lines that the card shows. Write nothing to the store before the person says yes.

1. Ask the person what to migrate: this project, this project and the `me` patterns, or all projects.
2. Add the migrate as one ask, as the card says.
3. Run `celis migrate`. It lists each pattern in a form that celis no longer reads, so no index shows
   it. Show the list to the person, and after a yes, run `celis migrate --yes`, which writes each one
   again in the current form. Then `celis migrate` must print `Nothing to migrate.`
4. List the live patterns with `celis grep -E " pattern [0-9a-f]{8} live "`. Skip each whose text has a
   `Forces:` line. When a text does not say enough, read its trail with `celis tree <trail id8>`.
5. For each other pattern, draft its five lines from its text: the `Name` from the form its `Do` gives,
   the `When` from the part before the first `:`, the `Do` from what it says to do, the `Because` from its reason, and the `Forces` from what the
   reason pulls against. Keep the meaning, and add no point the old text does not make.
6. Show the person the whole list: each id8, the old text and the five lines. Ask:
   yes, no, or a change. With more than 50 patterns, show and write them in batches of 50.
7. After a yes, write each one with `celis pattern --replaces <id> [--scope <its scope>] [--path <glob>]...
   -- "<the five lines>"`. Keep its scope, a done trail's too, and each `path` that
   `celis tree <its trail> --json` or its grep line shows; `{project}` takes no `--scope`. Its examples
   stay. To write into another project, add `--project <its id>`.
8. Ask the person whether to remove what celis no longer uses from its home, the folder that
   `celis help` names: `models/`, `index/`, `recalled/`, `asked/`, `cache/verified` and `retrieval.log`. After a
   yes, remove each of them that is there, and nothing else.
9. Ask the person whether to close the older trails that are still open. An older celis held the asks
   of a session under one trail, the first ask with the trail's own title; `celis tree --all` shows
   them. After a yes, drop each open step of such a trail with the reason `an older trail`, then close
   it with `celis step done <id> --as-planned --by person -- "An older trail; its asks are closed."`.
   Its learn brief has nothing to keep.
10. Run step 4 again: no pattern must be left. Close the ask with the counts, and tell them to the
    person: patterns of an old form written again, patterns rewritten, patterns left as they were, the
    items removed from the home, and the older trails closed.
