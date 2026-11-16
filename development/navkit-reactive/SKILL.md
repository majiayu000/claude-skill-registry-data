---
name: navkit-reactive
description: navkit's reactive layer (navkit/reactive.py) -- `reactive()`, `computed()`, `effect()`, `bind()`/`unbind()`/`is_bound()`/`peek()`, Binding, declared-type checks (ReactiveTypeError), dispose_effects. Use when declaring reactive attributes, writing bindings or effects, or debugging a value that does not update or a write that raises.
---

# The reactive layer

Observable attributes and the bindings between them; the mechanism navml markup compiles to.

- `reactive()` declares a source, `computed()` a derived value, and `obj.attr = bind(expression)` attaches an
  expression to *one instance*. `bind()` only wraps the expression in a `Binding`; the descriptor recognises one on
  assignment and installs it instead of storing a value, so the target is named by a real attribute reference.
- The three calls that name an attribute without assigning -- `unbind(obj, Widget.width)`, `is_bound()`, `peek()` --
  take the class attribute itself (the declaration object).
- Dependencies are discovered by running the expression and noting what it read, so a conditional subscribes only to
  the branch it took. Propagation is push-pull: a write eagerly marks dependents stale, values recompute lazily on read
  and are memoised -- glitch-free (a diamond recomputes once), mirroring the frame loop one layer up.
- `effect()` is the only eager node, for reactions that must happen whether or not anybody reads a value. Effects run
  after a batch is dispatched and before the paint, never during it.

## Things to know before touching it

- **A write is checked against the annotation**: `width: int = reactive(0)` refuses a `str` with `ReactiveTypeError`
  (also a `TypeError`). Only writes -- a binding's or computed's value is not checked. `Any`, no annotation, or a name
  only under `TYPE_CHECKING` is unchecked (that is the opt-out; no flag). The erasure is shallow: `frozenset[str]`
  checks the `frozenset`.
- **Assigning a value over a live binding raises**, deliberately; `unbind()` takes it back. Assigning another `bind()`
  replaces the old one. This is why `Widget.layout()` checks `is_bound()`.
- **A yielding binding is the exception**: `bind(expr, yielding=True)` is a default that a plain assignment replaces
  (the cell unlinks first). Markup's translated captions are bound that way (`i18n` skill); don't use it to dodge a
  real conflict.
- **A `bind()` on a non-reactive attribute is silently stored** (no descriptor to notice). A `computed` target raises
  and an unknown `Widget()` keyword raises, so what is left is a typo on a plain attribute; the repr
  `<unassigned binding ...>` gives it away.
- **A computed may not write.** The write path refuses if any frame on the tracking stack is a computed. Use an effect.
- **A collection has to be replaced to count as changed.** `entries.append(x); self.entries = entries` propagates
  nothing (the equality guard sees the same object). Build a new list; `frozenset` classes and `inline_style` are
  replaced the same way.
- An object carrying reactive attributes needs a `__dict__`, so slotted value types (`Style`, `DirEntry`) cannot host
  them.
- **`remove()` disposes a subtree's effects** (`dispose_effects`), so a widget that can be removed and put back declares
  its effects in `mounted()`, not `__init__`.
- **A declaration in a class body shadows the reactive descriptor** if written as a plain attribute: set e.g.
  `Console.can_focus` in `__init__`, never in the class body.
- **A console screen is not reactive and cannot be**: `Console.revision` is one counter standing in for it; anything
  mutating the screen behind the widget's back must bump it.
- Tests that drive a model directly must call `settle()` (tests/conftest.py) between acting and asserting.

## Read when

| Reference | Read when |
|---|---|
| `reference/declared-types.md` | why writes are type-checked and computed values are not; declarations as an extension point |
