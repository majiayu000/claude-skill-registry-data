---
name: navigator-keybindings
description: User key bindings -- navigator/lib/config/keybindings.py (TABLES, Section, Entry, ini names, render/read/load/seed/apply/write), keybindings.ini beside navigator.ini, navkit's run-time overrides (override_keys, restore_keys, default_keys, own_keys, check_table in navkit/commands.py), Options > Configuration > Key bindings (KeyBindingsSetup, Shell.key_bindings, KeyBindingsDialog with BindingList, KeyCaptureDialog with KeyCatcher). Use when adding a key table, renaming a command a table binds, or changing how keys are rebound.
---

# Key bindings and keybindings.ini

The user can rebind every key that sits in a key table. Keys handled in an `on_key` (list, viewer and panel cursor
movement, typing) are not covered: move one into a table to make it rebindable.

**This is a departure.** DOS Navigator 1.51 had no key editor. It was added by request, and the departure is recorded in
`KeyBindingsSetup`'s docstring and in the module docstring.

## navkit: run-time overrides (`navkit/commands.py`)

- **`override_keys(cls, table, base)`** sets `cls`'s keys to `key_table(base) | table` in place of what the classes
  from `base` (exclusive) to `cls` bind. It replaces, so a key can be taken away as well as added, and both halves of a
  component (the markup half and the hand-written half) count as one table.
  - A subclass with no override of its own still adds its keys on top.
  - A base's override shows through. This is how `CopyDialog` sees a rebound `Dialog`.
- **The other functions:**
  - `restore_keys(cls)` drops one override; `restore_keys()` drops them all.
  - `default_keys(cls, base)` is what the code binds.
  - `own_keys(cls, base)` is what is bound now.
  - `check_table(owner, table)` is `check_keys`' validation with the table passed in, so it works for a table that is
    not a class attribute.
- **`override_keys_later("module:Class", make)`** is for a class not imported yet: `make(cls)` runs the first time
  `key_table()`/`own_keys()`/`restore_keys(cls)` is called once that module is in `sys.modules` (`_settle`).
  `restore_keys()` drops pending ones too.
- **No cache.** `key_table()` is read at every key press, menu caption and key-bar paint, so an override is live at
  once.
- **At the start `load()` imports no window's class for its keys** (`_unread`; importing every one of them was 41 ms
  of a 0.3 s start). For a section whose class is not imported yet:
  - **Left alone** when every line it has is the shipped default line or a retired default (`_lines_as_shipped`).
    A line left out is the default (`Section.complete`), so a file seeded before commands were added still counts.
  - **Read when the class is imported** (`override_keys_later`) when every line names a shipped command and its keys
    parse. A clash found then keeps the defaults and goes to `errors.log`, because the screen is Navigator's by then.
  - **Read at the start, importing the class,** otherwise, so its warning is printed before the screen is taken.
  - `tests/test_keybindings.py::test_a_window_not_opened_yet_is_not_imported_for_its_keys` checks this in a fresh
    interpreter: the test module itself imports every class.
- `tests/conftest.py`'s autouse `_default_keys` calls `restore_keys()` around every test.

## The model (`navigator/lib/config/keybindings.py`)

**Sections.** `TABLES` lists `(name, title, "module:Class")` in the dialog's order.
- `global` has None for its class. The caller passes the application class (`Navigator`), because importing
  `navigator.__main__` by name would make a second class.
- `Section.base` is the first class in the MRO whose name differs from the section's class. That skips the
  generated half: `Manager` sits over `Window`, and `CopyDialog` over `Dialog`.

**Adding a key table means adding a row to `TABLES`.** `test_every_section_names_each_command_once` then checks it.

**Entries.** `entries(table)` makes one `Entry` per distinct command, compared by equality. Commands are frozen
dataclasses, so all the keys that ask for one command are gathered under it:
- `store_quick_dir_1 = alt+shift+1, alt+!`
- the WordStar pair, `block_start = ctrl+k b, ctrl+k ctrl+b` (in `keybindings_wordstar.ini`; by default it has no key)

**Keyless commands.** A class's `keyless_commands` (a tuple of bindings, navigator-layer only -- navkit never reads it)
lists commands it handles but binds no default key to. `keyless(cls, base)` gathers them along the MRO up to the
section's base, and `entries(table, keyless)` appends each one the table does not bind, with `defaults=()`. Variant
names are worked out over bound and keyless commands together, so `place_marker_3` and `unindent_block` keep their
names when no key has them. `FileEditor` lists every command of `WORDSTAR` this way.

**Names.** A name is the class name in snake case.
- When a table binds a class more than one way, each variant gets suffixes from the fields that differ between them:
  - a True bool adds the field's name;
  - a number or word adds the value, with `-` written `minus_`;
  - False or None adds nothing;
  - fields that are equal in every variant (`by_key=True`) add nothing.
- Examples: `move_left_extend`, `quick_change_3`, `scroll_names_minus_1`.
- **Names are the file's keys.** Renaming a command class, or giving one a new variant, renames its line, and the old
  line becomes an "unknown command" warning.

**Titles.** A title is the name, humanised. A command's `title` is not used, because that is a short key-bar caption
("Dupe").

## The file

- **Location and creation.** It lives at `config_dir()/keybindings.ini`, beside `navigator.ini`. `main()` calls
  `load_keybindings()` after `seed_associations()`. That function:
  1. calls `seed(Navigator)`, which writes every default with `open("x")` and so never overwrites;
  2. calls `load(Navigator)`;
  3. prints warnings as `nav: ...` before the screen is taken.
- **Format.** There is one `[section]` per table, with its title as a comment.
  - A line is `name = key, key`, in canonical spelling. A chord's keys are separated by a blank.
  - An empty value means the command has no key.
  - A line that differs from its default ends with `# default: ...`.
  - A key starting with `#` or `;` is joined with a bare `,` (`format_keys`), because ` #` would start an inline
    comment.
- **Reading** (`read`). Problems are warnings, never errors:
  - a missing line keeps its default, **less any key the file gives another command** (`Section.complete`): a
    default added after the file was written (`select_all` taking Ctrl+A over a WordStar file's word-left Ctrl+A)
    yields to the file instead of the clash throwing the section back to its defaults; a chord counts as its first
    key both ways;
  - **a line naming exactly a retired default is read as no line** (`RETIRED_DEFAULTS`, section and command to the
    keys they had by default before): the file is seeded whole, so without it a default once written could never
    change -- an old file's `start_search = ctrl+f` kept Ctrl+F from the Find bar, and the viewers' `shift+f4` view switches (now Shift+F3) kept *Edit...* out. **Changing a default key means an
    entry there** for the command that loses it; a line the user changed (other keys, or more) is untouched;
  - an unknown section or name is a warning;
  - a key that will not parse is a warning, and that line keeps its default;
  - a section that fails `Section.table` (one key on two commands, or a chord whose first key is also bound alone) is a
    warning, and the whole section keeps its defaults;
  - a file that is not ini at all is one warning, and every section uses its defaults.
- **Applying** (`apply` / `Section.apply`). A section equal to its defaults calls `restore_keys`; any other calls
  `override_keys`.
- **Writing** (`write`). The whole file is written through `settings.write_atomically`. It touches the disk only, so
  the caller binds first with `apply` on the loop, then writes on a thread. Comments written by hand are not kept.

## Sets of keys (presets)

- **Shipped:** `navigator/assets/keymaps/` (`presets_dir()`, package data `keymaps/*.ini`).
  `keybindings_default.ini` is the one *whole* file: every command at its default, generated by
  `tools/keymap_default.py` (`render(..., header=)`), so Load can go back as Reset does and a user sees everything
  that can be bound. **Adding, renaming or rebinding a command makes it stale**: rerun the tool;
  `test_the_default_set_is_every_default_and_up_to_date` runs `--check`. The others are hand-written:
  `keybindings_wordstar.ini` (DN's WordStar editor keys, the clipboard staying on Ctrl+X/C/V),
  `keybindings_dn151.ini` (that plus DN's Ctrl+X/C/V cursor keys) and `keybindings_emacs.ini`. Each is the file
  format holding **only lines that differ from the defaults**, so a command added later arrives bound.
  - `test_a_shipped_set_loads_clean_and_shadows_nothing` reads each with no warnings and checks the editor's and the
    edit window's tables cannot hide each other: a chord's first key in *any* table on the focus path wins over a key
    bound alone in another (`Application._chord_key` runs before the tables), so Emacs's `ctrl+x ctrl+s` needs the
    editor to drop Ctrl+X. The global table is looked at before the tree (`_run_key`), which is why the Emacs set
    moves the ASCII table off Ctrl+B.
  - A new shipped set needs adding to the test's `PRESETS`.
- **The user's:** `keymaps/` beside `navigator.ini` (`user_presets_dir()`), written by the dialog's *Save*.
- **Not vi/vim:** it needs a normal/insert mode, which key tables cannot express (a plain letter always types, and
  panel and viewer cursor movement is in `on_key`). A modal editing mode in `FileEditor` would come first.

## The dialog

- **Opening it.** `KeyBindingsSetup` is under Options > Configuration > *Key bindings...*. Its handler
  `Shell.key_bindings` does three things:
  1. runs `KeyBindingsDialog(sections)`;
  2. on OK, calls `keybindings.apply`;
  3. calls `asyncio.to_thread(keybindings.write, ...)`, showing an *Error* box on `OSError`. The keys stay bound for
     the session.
- **`KeyBindingsDialog`** (`navigator/widgets/setup/key_bindings_dialog/`).
  - **Lists.** *Category* on the left is a ListViewer of section titles. *Commands* is a `BindingList`: title, a `│`
    divider, then keys as `key_label` writes them. A `*` marks a command that is not at its default. The `detail` line
    under the lists shows the full keys and the default.
  - **Pending edits.** Edits live in `assignments` (`{section: {name: keys}}`). Nothing is bound until OK, and Cancel
    drops them.
  - **Buttons.**
    - *Rebind* (the default button) and *Add* open `KeyCaptureDialog`.
    - *Clear* sets `()`.
    - *Default* restores the command's defaults.
    - *Reset* restores every section, after asking.
    - *Save...* (`save_file`) writes every section as edited so far, through `keybindings.write` on a thread, to a file
      named in navml's `FileDialog` opened on `user_presets_dir()` (made first); no suffix gets `.ini`, an existing
      file is asked about. It binds nothing.
    - *Load...* (`load_file`) opens the box on `user_presets_dir()` when it holds any `*.ini`, else `presets_dir()`,
      reads the file with `keybindings.read` on a thread, and `assign()`s it **in place of every edit**: what the file
      does not name is at its default. Warnings are one *Key bindings* box (`WARNINGS_SHOWN`, then *and N more*); a file
      that cannot be read changes nothing. OK binds it, as any edit.
  - **`bind_key` checks.**
    - Another command in the same section has the key: it asks *"F5 is bound to Copy. Reassign it?"*, and Yes takes the
      key from that command.
    - In any section but `global`, a key the global table binds: it asks, because the application's table is looked at
      first.
    - Last, `_put` validates through `Section.table` and shows *Cannot bind that:* with the reason.
- **`KeyCaptureDialog`** is a small Dialog over a `KeyCatcher` (a `Control`). The catcher has the focus, so its `on_key`
  sees every key before the dialog's own table: Tab, Alt+letter and F10 are captured.
  - Enter accepts and Esc cancels, so those two can be bound only in the file.
  - Two keys make a chord, and a third key starts again.
  - A bare modifier never arrives: it is a `ModifiersEvent`.
  - It answers the canonical spec.

## Tests

- `tests/test_key_overrides.py` covers the navkit layer.
- `tests/test_keybindings.py` covers names, the file, the shipped sets and the dialog, driven with `Until` titles: *Key
  Bindings* for the dialog, *Press a key* for the capture box, *Key bindings* for its questions. Save/Load tests stand
  the file box in with `_file_box_answers` (a monkeypatched `FileDialog.execute`).
  - The refusal box opens in the same batch the capture box closes, so don't wait for *Key Bindings* in between.
