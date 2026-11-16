---
name: navml-components
description: How a navml component is put together and built -- the markup half and hand-written half, `*_nml.py` / `.pyi` generated artefacts, component directories and groups, `navml/_merge.py`'s splice and finder, `navml.register`, lazy re-exports, `navml.component.Component`, and the parser/generator modules (parser.py, expression.py, sibling.py, resolve.py, checks.py, generator.py, stubs.py, build.py, coder.py). Use when adding or moving a component, or changing the toolchain.
---

# navml components and the toolchain

## Four files, two optional halves

`button.nml` is the markup; `button_nml.py` is what the generator emits from it (tracked and shipped); `button.py` is
the hand-written handlers; `button.pyi` the generated stub. Markup alone, Python alone, and both are three peer shapes,
and `from navml.widgets.dialog.button import Button` is the same line for all three.

- **A component that paints has two halves by construction.** Markup declares and places; Python paints (`Label` gained
  a `label.py` for this; `field.nml` is the markup-only example). Conversely `CheckBoxes`/`RadioButtons` lost their
  markup halves: a document holding nothing but a head says only what its `class` statement says.
- **The merge is one line**, `handwritten.__bases__ = (generated,)`; the generated class is always the base, so a
  hand-written `__init__` calls `super().__init__()` and finds every id live.
- **The hand-written half never names the generated class** -- `class Button(Widget)` is what a Python-only component
  says too. The loader refuses the pair if its base disagrees with the markup's (CPython would drop it silently).
  A class based only on `object` cannot be spliced (`deallocator differs from 'object'`).
- The generated class always names `navml.component.Component` (`class Label(_Component)`,
  `class FramedButton(Button, _Component)`), which holds the `layout()` override, `__navml_source__`, and the
  keyword-property constructor. **`Component { }` is a live `.nss` selector** matching every markup-built widget (type
  selectors match by class *name*); it reads *built from markup*, never *is a component* (`spacer.py` is a component and does not match).
- **The generated class constructs children inline in `__init__`**, not a `_build()` method (a derived component's would
  override it). **A derived component's own children land after its base's** -- `Dialog.focusable()` moves its buttons
  to the end for this.
- **`Component.built()` runs once the whole tree exists.**
  - Every generated `__init__` ends with `self._navml_built(__class__)`, which calls `built()` only from the
    generated class nearest the instance's own. A derived document's children are there too.
  - It runs before the hand-written half's `__init__` goes on past `super().__init__()`.
  - Declared properties a caller passed are already set.
  - Use it for work that needs every child but must not wait for mounting (`SettingsPage` seeds its controls there).

## A big hand-written half: mixins

- **A hand-written half too big for one file is split by feature into mixins**, each a `navkit.widget.Mixin` in its
  own module in the component directory: `class Manager(Encoding, Copying, ..., Views, Window)`
  (`navigator/widgets/manager/manager/`). The merge keeps the leading `Mixin` bases and splices the generated class
  in after them, `__bases__ = (*mixins, generated)`, so a mixin's method sits where a method of the class would.
  A leading base that is not a `Mixin` is refused, as is a second widget base.
- **A mixin holds methods only.** `Mixin.__init_subclass__` refuses a `keys` table, `checks`/`enables`, and any
  `reactive`/`computed`, which stay in the class itself, so state is read in one place. A sync `on_*` in a mixin is
  refused at import, as a widget's is. A constant only one mixin uses (`FileEditor`'s `DRAW_KEYS`) may live with it;
  a class-level default of instance state stays in the class. Zero-argument
  `super()` works: the next class after a mixin is the next mixin, then the generated half.
- **A mixin is typed against the component's stub** (its surface, for a Python-only class) with
  `if TYPE_CHECKING: from <package> import Manager as _Base`
  and `else: from navkit.widget import Mixin as _Base`. `class Copying(_Base)` then sees `self.left` and the other
  mixins' methods, with no cycle, because the stub flattens the mixins.
- **`navml/sibling.py` reads the mixins too**, without importing them. A base shaped as a mixin, imported from a
  module of the same source tree (relative, or absolute under the same top-level package), is parsed, and its methods are folded into the class's own,
  each carrying `origin` so messages name the right file, with its class-level names (a constant moved out with the
  methods using it). Its imports are merged in as well; a name two files bind differently is refused, and so is a
  mixin imported under a name the module already imports something else as (Shell's command `Terminal`: the mixin
  is `ConsoleMixin`, as `CommandLineMixin` is because `CommandLine` is a widget). So the handler-collision and `await` checks see a method wherever it moved, and **the
  `.pyi` lists every mixin's methods as the class's own, keeping only the markup base**. Editing a mixin's method or
  imports therefore makes `navml build --check` report the stub stale, as editing the `.py` does.
- **Module-level helpers the mixins share go to a sibling module** (`manager/manager/helpers.py`), never into the
  component's `.py`: a mixin importing that module at import time would be a cycle. The component's module may
  re-export them where others import them from it (`panel.panel` stays the public face of `human_size`,
  `fit_text`...), and a global a test patches on the module stays there with the code reading it (`Panel`'s listing,
  `SCAN_GRACE`, `_read_location`).
- **What a stub says of the hand-written class** (`.pyi` and surface alike): every `self.name = ...` a method of it
  or its mixins assigns, as `name: T` (`_Any` unannotated), less what a live base already declares (`Widget.width`);
  a property as `@property` (with its setter, under the setter's own parameter names), so a class or mixin defining
  it is an override pyright takes; `@staticmethod`/`@classmethod` kept; and the imports of an `if TYPE_CHECKING:`
  block (not a mixin's `_Base`). Checked with pyright (`./venv/bin/pyright FILES`, `[tool.pyright]` in `pyproject.toml`):
  no errors in the stubs or from overrides; what remains is the code's own typing.
- **A Python-only class has a surface stub instead** (`navml/surface.py`): `navml build` finds a class in a module
  with no `.nml` whose bases include mixins, and writes `<stem>_surface.pyi` beside it -- the class with its own bases
  only, every method and class-level name of it and its mixins (as `sibling.py` folds them), and what its module
  defines imported from it. A stub with no module of its own; its mixins say
  `if TYPE_CHECKING: from <module>_surface import <Class> as _Base`, since typed against the class itself they would
  be a cycle (the class derives from them). `--check` reports a stale one; `tests/test_nml_build.py` checks `navkit`
  too. A mixin is recognised by shape -- `class X(_Base)` or `(Mixin)` -- wherever in the same top-level package it
  is imported from (`navkit.app.focus`), so a real base from the tree (`ContextMenuHost`) is never folded in.
- **A Python-only class splits the same way** (`FileEditor`, `FileViewer`: nothing to merge), and so
  does navkit's `Application`, whose mixins live in `navkit/app/` and import what they share from
  `navkit.application` itself -- which therefore imports them just before its class, after everything they take
  (`navkit/app/__init__.py` imports `navkit.application` first, so either may be imported first). Keep a method
  that reads a module global a test patches (`REPEAT_DELAY`, `CLIPBOARD_ANSWER_TIMEOUT`) in the class's own module.
- **A moved method may name nothing defined after the class it left** -- a `NameError` only when it runs (Shell's
  `UserScreenPeek` moved into `console_keys.py` with its one caller). `tests/test_undefined_names.py` fails on it,
  for every module.
- **A mixin is not a type to a stylesheet.** `navkit.stylesheet.type_names` leaves out every class that is a mixin
  (`__navkit_mixin__` in its own namespace), so `Links { }` never matches the manager. Code that looks for "the first
  class in the MRO that is not this one" must skip mixins too (`keybindings.Section.base`).

## A component is a directory; components come in groups

- The files live in `navml/widgets/dialog/button/` beside an `__init__.py` re-exporting the class (and any event it
  declares). **Files repeat the directory's name** (`packaging/linux/build.sh` finds siblings by stripping `_nml.py`).
  **Every component gets a directory**, Python-only ones too. The flat shape stays legal (`tests/test_nml_build.py`'s
  `package` fixture is flat on purpose).
- Groups: layouts under `navml/widgets/layout/`, the *Dialogs* components under `navml/widgets/dialog/`, menus under
  `menu/`; `Window`, `Desktop`, `Timer`, `Spacer` at the top. Navigator groups the same way (`shell/`, `manager/`,
  `file_ops/`, `tree/`, `viewer/`, `editor/`). A group's `__init__.py` is a docstring and never re-exports;
  `_COMPONENTS` (navml) / `_WIDGETS` (navigator) map a name to its dotted path (`"dialog.button"`), so
  `from navml.widgets import Button` is unchanged.
- **The library registers, not the component**: `navml.register("navml.widgets")` once; `_registered()` walks up the
  dotted name. A component package registers itself in its `__init__.py` (not a `.pth`: the `.deb`/`.rpm` use
  `PYTHONPATH`).
- **A package `__init__.py` must not re-export eagerly** -- generating a component imports the ones it uses, so eager
  re-export would import everything. `navml/widgets/__init__.py` uses a PEP 562 `__getattr__` with a `TYPE_CHECKING`
  block.
- Silent failure modes fixed once: `build.order()` keys its graph on the directory name as well as the module's, and
  `build._forget()` evicts the component's package with its module.

## The finder

- **It keys on `button_nml.py`, never `button.nml`**, so both halves are ordinary `.py` files that reach a wheel. The
  markup ships anyway via one `"*" = ["*.nml", "*.pyi"]` entry in `[tool.setuptools.package-data]`.
- **A component is a module, never a package**; the finder refuses to claim a package (a stale flat `button_nml.py`
  beside a `button/` directory would otherwise splice onto an old base).
- **A component module must never be a test module, `conftest.py` or pytest plugin** -- pytest's assertion rewriter
  bypasses `sys.meta_path`, so the splice would not happen.

## The parser and the generator

- **The parser imports nothing the document names.** Every check a document can fail alone is `navml/parser.py`'s
  (structure, identifiers, reserved words, self-collisions); every check needing a live class is the generator's.
  `parse(text)` / `parse_file(path)` return a `Document`; `imports_of(path)` reads only the import block, which orders a
  cold build without executing anything. `navml/errors.py`'s `MarkupError` is the one exception both raise.
- **The generator is seven modules in a one-way chain**: `expression.py` compiles an expression or handler body by
  rewriting free names on the syntax tree; `sibling.py` reads the hand-written `.py` **without importing it**;
  `resolve.py` is the only module importing what a document names; `checks.py` refuses what a live class reveals;
  `generator.py` and `stubs.py` emit the two artefacts (`surface.py` a split Python-only class's stub); `build.py` orders
  a directory by import graph and writes.
  `navml/_alias.py` is run-time support beside `component.py`.
- **Anything emitting code goes through `navml/coder.py`'s `Coder`** (line buffer, logical indents, trailing comments),
  never string assembly or whole-module `ast.unparse` -- `ast` carries no comments and the source map *is* comments
  (`# button.nml:12`).
- The generated file never reads the sibling `.py` to decide what to emit, so there is no `--check` drift.
- **A model document takes a separate path**: `build.compile_document` asks `navml.model.is_model` (any `field` line)
  and hands it to `navml/model.py`. That module reuses `resolve._namespace`, `Sibling`, `Coder` and the merge, but not
  the widget resolver, checks or generator. Models live in their own library, `navml/models/`, registered like
  `navml.widgets`.
- navkit grew for navml: a public `Declaration`, `Binding.owned_by(owner)`,
  `stylesheet.check_declarations(text, *, line, filename)`.

## Read when

| Reference | Read when |
|---|---|
| `reference/overview.md` | where navml's inspiration comes from (QML, Kivy) |
| `reference/two-halves.md` | the two halves, directories, groups, deriving, the import machinery, shipping markup |
| `reference/shared-base.md` | `Component`, how a value gets in, no required ctor args, navigated properties, a component's sheet |
| `reference/parser.md` | the parser: comments, continuation, root id, node graph |
| `reference/generator.md` | what the generator emits, source mapping, converting `Manager`, what writing it settled |
| `reference/still-open.md` | open questions for the language/toolchain |
| `reference/appendix-transformer.md` | the expression transformer prototype |
