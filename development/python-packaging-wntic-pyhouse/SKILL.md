---
name: python-packaging
description: Use when the question is the mechanics around a module rather than what it is called — `__init__.py`, `__all__`, a re-export, one file or two modules, relative versus absolute imports, a circular import, or whether this needs a class at all. Owns when a class earns its place and the one-class-per-module cap with the test for when a closed set of declarations may share a module, the four-part re-export contract, building nothing at import time, and the `py.typed` marker a library distribution ships. Naming a module is `naming`. - Adding a public module to a package; a wildcard import; import order; a module-level settings object, engine or client.
---

# Python Packaging

How a module is packaged, and how another module reaches it. These rules are
**architecture-neutral** — they hold in a layered app, a standalone service, and a shared library alike,
because they are about Python's import system rather than about layers.

What they do *not* decide is which package a module belongs in. That is the architecture's job:
`hex-architecture` (in the `pyhouse-hex` plugin) for a layered app, `flat-layered` (in
`pyhouse-flat`) for a package-by-technology service, or the project's own layout where neither applies.

## When to use vs. neighbours

- Choosing a name for anything — a package, module, class, function or variable → `naming`, first.
  "Name this module" lands there, not here; this skill only checks the filename against the class
  once the name exists.
- Creating a module or an `__init__.py`, or changing a package's public surface → this skill.
- Any question of relative vs absolute, or how to spell an import → this skill.
- A circular import, or an import pushed into a function body to break one → this skill; the cycle is
  a structural problem and rule 11 says so.
- Which package a module belongs in → `hex-architecture` (in the `pyhouse-hex` plugin) or
  `flat-layered` (in `pyhouse-flat`).
- Annotation forms, comments → `python-style`; logging → `python-logging`.
- The exception catalog's contents and where its file sits → `exception-catalog`; that it may hold many
  classes is this skill's set test, of which it is the first worked example.
- Whether the boundary between two modules or packages should exist at all → `coupling`, first; this skill owns the mechanics once it is drawn.

## Naming — owned by `naming`

**The choice of the name itself lives in the `naming` skill** — the derivation procedure, the tests a
name must pass, the kind-by-kind rules, and the vague-noun families (`CheckResult`, `…Data`,
`…Manager`, `process_…`). Load it before writing an identifier; load it *first* when the code was
ported or generated, because that is where names arrive by inertia.

Two consequences of naming land here, in the packaging mechanics:

- A module filename must describe its contents and **match its single class in snake_case**
  (`qux_client.py` → `QuxClient`), or name the set when a closed set of declarations shares it
  (`foo_schemas.py`). `utils.py` holding `class FooHelper` is wrong twice — the file
  names a category rather than a responsibility, and so does the class.
- Renaming, and which names are never renamed in place, are `naming`'s **Renaming**.

## Modules

- **A module that defines a class defines exactly one**, and the module name matches it in snake_case
  (`qux_client.py` → `QuxClient`, `entity_registry.py` → `EntityRegistry`, `qux_settings.py` →
  `QuxSettings`). The rule caps classes per module; it does not require one. A module of related
  functions is a first-class shape — see below. The one way past the cap is a closed set of
  declarations, named for the set — see **When several classes may share a module**.
- **`__all__` goes after the imports and before the class definition**, never at the top of the file.
- A module filename must describe its contents, by the rules in `naming`.

```python
import httpx2

__all__ = ["QuxClient"]


class QuxClient:
    def __init__(self, http: httpx2.AsyncClient) -> None:
        self._http = http
```

### When a module needs a class at all

**A class that declares a type earns its place by being one.** A `Protocol`, an enum, an exception
class, a frozen record — its job is to give a shape or a contract a name the type checker can see, and
it needs no state and often no methods at all. Nothing in the rest of this section applies to it, and a
`Protocol` with no `__init__` and nothing but `...` bodies is exactly right.

Everything below is about **a class that holds behaviour**, where the question is real. A module is
already a namespace, so such a class earns its place when it **holds state its methods share and
callers should not manage** — a connection, a base address, a compiled ruleset, injected collaborators.
That is the whole test, and it is about state, not about size or subject matter.

With no such state the module is the unit and its functions are its interface. A transformation — parse
this payload, normalise this record, select these rows — is that shape, and wrapping it in a class
produces an object callers construct only to discard.

The tells that a behaviour class is the wrong shape: there is no `__init__`, or it takes nothing;
every method could be a `@staticmethod`; no method reads an attribute the constructor set. Read them
only after deciding the class is not declaring a type — they describe a `Protocol` perfectly, and a
`Protocol` is not the thing they are about. The tells that the shape is right: two or more methods read the same constructor-set attributes; the object is injected
somewhere; it has a lifecycle to open and close.

**A helper that does not need `self` is a module function, not a private method.** Putting it at module
level beside the class is the better shape, not a compromise: it cannot reach instance state, so a
reader knows it is stateless without reading it, and a test can call it without constructing anything.
This is why a module may hold one class and several private functions and still obey the rule above.
**The private functions come after the class**, so the module reads from its interface down to its
details: constants first, then the class, then the helpers it calls.

**Module-level constants are correct; module-level mutable state is not.** A compiled pattern, a
timeout, a lookup table belongs at module level, where it is built once and is easy to find — hoisting
it into the class as a class attribute buys nothing. A mutable module-level binding is a singleton
nobody declared, shared by every caller in the process and every test in the run; it belongs to an
object with an owner, or it does not exist. Anything that must be *built* rather than declared is
rule 8's, mutable or not.

### When several classes may share a module

The cap exists because a class with behaviour is a unit: a reader looks for it by name, a test
constructs it on its own, and it changes for its own reasons, so a second one in the same file hides
behind the first one's filename. Declarations that belong together have none of those properties —
splitting them buys no decoupling and costs a reader the one view of the whole set. **Several classes
may share a module only when all three of these hold:**

1. **Every class is a declaration** — an exception, a record or wire model, an enum, a `TypedDict`.
   None holds state, is injected, or has a lifecycle to open and close.
2. **They form one closed set that changes as a unit** — one error catalog; one resource's request and
   response models; one external API's payloads. A change to the set is one edit in one file; a class
   that would change for reasons of its own is not in the set.
3. **The module is named for the set, not for one member** — `exceptions.py`, `foo_schemas.py`,
   `foo_payloads.py`, or `foos.py` inside a `schemas/` package that already says the rest — so its
   name still predicts its contents.

**A class with behaviour always has its own module**, whatever it would sit beside. The two worked
examples of the test:

- **The exception catalog** — the root error and every subclass in one file, so the catalog stays
  auditable in one read (`exception-catalog` owns its contents and its place).
- **A per-resource wire-schema module** — the request and response models describing one resource's
  contract from different angles.

Two further allowances, and no others:

- **A private declaration that never leaves its module** — an underscore-named record, enum or
  `TypedDict` used only by the module that declares it — may sit beside that module's class. It is part
  of that class's implementation, not a second unit; the day another module imports it, it moves to a
  module of its own and loses the underscore.
- **A module whose name and contents a framework dictates** — Django's `models.py` and `admin.py`,
  Alembic's `env.py` — follows the framework's convention. The framework finds what it loads by that
  name, and a split it does not expect fights it at every file.

What the test still refuses: two entities in one module each change for their own reasons (condition
2); two adapters, or a client beside the parser it feeds, put behaviour in a shared file (condition 1); a
set module named after one of its members hides the rest (condition 3).

Modules holding multiple **functions** — a route module, a module of pure filters — do not engage this
rule at all. It is about classes.

### Nothing is built at import time

**Importing a module binds names.** It does not reach the network or the filesystem, read an environment
variable, or build anything that needs either — a settings object, a client, an engine, a session
factory, a connection pool. Those are built **inside a function the caller runs** — the entry function
calling the class, or a factory function where building takes more than the call. Declaring is not
building: a class, a constant, a type alias, or a schema object that only describes a shape may sit
at module level, because none of them needs anything to exist.

```python
# no — runs on import, so importing this module is what fails
settings = QuxSettings()


# yes — the caller decides when, and the failure names the missing value
def main() -> None:
    settings = QuxSettings()
    ...
```

Reading the installed distribution's own metadata is a filesystem read like any other, so it gets no
exemption: a `__version__` computed at module level is a build, and the version a program reports is
read behind a function the caller calls (`python-versioning` owns the number and where it is declared).

Where a factory function is written, cache it only once a second caller genuinely exists — a framework
resolving it per request, say; needing one usually means something below the composition root is
building what it should be handed.

The reason is the import graph, which is why it lives here. A module-level construction runs for every
importer, including ones that never touch the object: a test collector importing a sibling symbol, a
documentation build, a CLI that only wanted one constant. Each of those now needs the full environment
of the thing it did not ask for, and the traceback names the import rather than the missing value. It
also puts a side effect somewhere nothing can order it, since import order is decided by whoever imports
first.

Carve-out 2 below is a concession to modules that genuinely cannot avoid this — an application object a
server loads by path — not a licence for the rest.

## The `__init__.py` re-export contract

This contract is what makes the collapsed import form below legal. It has four parts, and skipping any
one of them breaks either the runtime or the type checker.

- **Always `from .module import *`**, never `from .module import ClassName`.
- **Always `__all__ = module.__all__`** (or `+`-joined across modules), never `__all__ = ["ClassName"]`.
- **Precede the wildcards with one `from . import <module>, …` line** naming every re-exported submodule,
  alphabetically.
- **An `__init__.py` contains only imports and `__all__`.** No class definitions, no constants, no logic.

That third bullet is the one people delete as redundant. It is not. The wildcard binds the submodule at
runtime, but **the type checker does not model that side effect** — without the explicit
`from . import …`, the `__all__ = module.__all__` reference fails type-checking as an undefined name. The
explicit import is what makes the contract check.

A single module:

```python
from . import qux_client
from .qux_client import *

__all__ = qux_client.__all__
```

Several modules — name them all in the `from . import …` line, repeat the wildcard per module, and
concatenate:

```python
from . import qux_client, qux_settings
from .qux_client import *
from .qux_settings import *

__all__ = qux_client.__all__ + qux_settings.__all__
```

**A package re-exports its immediate children — direct modules *and* child subpackages** — except the
carve-outs below. A package with children and an empty `__init__.py` is wrong; re-export them so
`from <package> import X` resolves. The two empty `__init__.py` files that are right are an application's
distribution root (carve-out 1) and a package whose modules may not be wildcarded (carve-out 2).

Adding a module to a re-exporting package is **four edits**: declare `__all__` in the module, add it to
the `from . import …` line, add its `from .<module> import *`, and append `<module>.__all__` to the
package's own `__all__`. Miss one and the collapsed form breaks at the first call site.

### Carve-outs — where re-export stops

**1 — the distribution root carries what that root is, and nothing more.** The rule keys on whether
anything outside the distribution imports it, and there are two cases.

- **An application's root is not an API.** Nothing outside imports it, so the top-level
  `<package>/__init__.py` re-exports nothing and stays empty. Aggregating to it would make
  `import <package>` transitively pull every third-party dependency the project has on every use, and destroy any
  dependency-free import path the architecture was maintaining, in exchange for an import path nobody
  outside uses. Re-export stops below the root; it does not climb to it.
- **A distributable package's root *is* its public API.** A library or SDK is imported by code that
  should not have to learn its file layout, so the root re-exports the names it promises — and only
  those. That is an **enumerated** surface, not the aggregation the first case forbids: a name is
  re-exported because it is part of the published contract, never because it is a child, and a name
  whose import pulls a heavy or optional dependency stays off the root and is reached by its own module
  path, so the cost above lands on whoever asked for that name rather than on every importer.

One test covers both: **does an importer of the root need this name?** An application's root has no
importer, so the answer is always no; a library's root has one, and the answer is the contract it
published.

**2 — a module with import-time side effects is not wildcarded.** If importing the module *does*
something — builds an application object, opens a connection, registers a handler — its package
`__init__` must not pull it in. Re-export only the side-effect-free surface, or leave the `__init__`
empty. The same applies to a package of modules that each export a **colliding** name (several route
modules each exporting `router`): a wildcard would clash, so those are reached by explicit aliased
import at the one place that consumes them.

This carve-out is per module, not per directory. A sibling package whose class names are distinct
re-exports them normally.

**3 — wildcard only class-modules.** `from .x import *` is for a module that declares `__all__` — a class
module. A module whose public name is a bare object rather than a class (a `metadata` instance, a
configured singleton) is **not** wildcarded into its package `__init__`, because the wildcard would bind
a name shadowing the submodule itself. Reach it by explicit relative import: `from ..metadata import
metadata`.

## Imports

### Relative vs absolute

- **Inside a package, relative imports up to two dots** — `from .sibling import X`,
  `from ..parent import Y`.
- **Same package → one dot, never up-and-back-down.** A module importing a sibling in its **own** package
  uses `.sibling`. Routing through the parent back into the same package
  (`from ..package.sibling import X` while already inside `package/`) resolves but reads as a cross-package
  reach. No tool flags it — the import is valid Python — so it is on the author.
- **Three or more dots → absolute.** `from ...thing import Z` is banned; write
  `from myapp.subpackage.thing import Z`. Once it would be `...`, the absolute path is both shorter and
  clearer.
- **Across package boundaries → absolute**, regardless of dot count. **A layer is a package**, so in a
  layered architecture this is the same rule under a second wording — cross-layer imports absolute,
  within-layer imports relative. One rule, not two.

```python
# in src/myapp/foos/foo_reader.py
from myapp.bars import BarParser  # another package — absolute

from ..exceptions import FooError  # one level up — relative
from .foo_parser import FooParser  # same package — one dot

# NOT: from ..foos.foo_parser import FooParser  # up-and-back-down into the same package
```

### Collapse same-package imports

Importing several symbols from the same place is **one statement**:

```python
# yes
from myapp.foos import (
    FooKind,
    FooParser,
    FooRecord,
)

# no
from myapp.foos.foo_kind import FooKind
from myapp.foos.foo_parser import FooParser
```

- One symbol per line inside the parens, alphabetically sorted, trailing comma on the last entry. A
  one-symbol import stays on a single line.
- Import from the **package**, not from an individual module — which is exactly what the re-export
  contract underwrites. Bypassing `__init__.py` forces every reader to know the file layout.

**"Package" means the one that DIRECTLY contains the defining module — never a grandparent.** Reach a
symbol through **one** `from .module import *` hop. Do not reach it through a grandparent that would
re-export it across a second hop: the intermediate package's `__all__` is a **computed** concatenation
(`a.__all__ + b.__all__`) that the type checker cannot evaluate through a `from .subpackage import *`, so the
name resolves at runtime while the checker reports "module has no attribute".

Concretely: a class defined in `myapp/foos/bars/bar_parser.py` comes from its `bars` package —
`from myapp.foos.bars import BarParser` (one hop) — **not** from
`myapp.foos` (two hops, the middle `__all__` computed). A class sitting *directly*
under a package is one hop from it, so importing it from there is correct.

### Import order inside a module

PEP 8 grouping, one blank line between groups:

1. `__future__` — **banned in this style** (`python-style`); this slot stays empty.
2. Standard library.
3. Third-party.
4. First-party absolute.
5. First-party relative.

The formatter and import sorter handle this automatically. Do not fight them, but know the groupings so
hand-written imports land in the right block.

## Rules

1. Use `naming` for identifier choice and renaming; check module filenames against their class names.
2. **One class per module, unless the classes are one closed set of declarations.** Several classes
   share a module only when every one is a declaration with no state, injection or lifecycle, they
   change as one unit, and the module is named for the set; a class with behaviour always has its own
   module. The only other allowances are a private declaration that never leaves its module — the day
   another module imports it, it moves to its own module and loses the underscore — and a module whose
   name and contents a framework dictates. The rule caps classes and does not require one, so a
   function-only module does not engage it. Whether the module wants a class at all is **When a module
   needs a class at all**: state its methods share, or no class — and a helper that never touches
   `self` is a module-level function, not a private method.
3. Put module exports between imports and definitions, using the placement shown in **Modules**; in a
   module holding a class, the definitions run constants, then the class, then its private helpers.
4. Check each re-exporting `__init__.py` against all four parts of the re-export contract.
5. When adding a public module, complete all four package edits listed under that contract.
6. **A package re-exports its immediate children**, except at each carve-out's documented scope: the
   distribution root by what that root is — an application's stays empty, a library's enumerates the
   names it publishes and no others, leaving a name that pulls a heavy or optional dependency to its
   own module path — side effects or colliding exports, and bare-object modules.
7. Select relative or absolute reach using **Relative vs absolute**, without routing a sibling import
   through its parent. Three or more dots, and any layer boundary — which is a package boundary — take
   the absolute form.
8. **Build nothing at import time.** Importing a module binds names; anything that reaches the network
   or filesystem, reads the environment, or needs either is built inside a function the caller runs — so
   importing a module never demands the environment of an object the importer did not ask for.
9. Import from the package that directly contains the defining module, never from the inner module
   and never through a grandparent — one re-export hop — and collapse its symbols into the documented
   sorted form. A module directly under an application's root, which carve-out 1 keeps the root from
   re-exporting, is imported by its own module path (`from myapp.exceptions import …`).
10. Keep imports in the five documented groups; apply `python-style` to the empty future-import slot.
11. **Spell an import as what it uses, and never to work around a cycle.** No `from x import *` outside
    an `__init__.py` — it pollutes the namespace and breaks linting; no module alias
    (`import myapp.foos as fs`) — `from … import` shows what is used; and no import moved into a
    function body or a `TYPE_CHECKING` block to break a cycle — the cycle is a structural problem, and
    the structure is what gets fixed.
12. **No mutable module-level state.** A dict used as a cache, an accumulating list, a registry filled
    at run time is a singleton nobody declared, shared by every caller and every test; give it an owner
    or drop it. Module-level constants are correct.
13. **A library distribution declares itself typed** — an empty `py.typed` marker in its import
    package, beside the root `__init__.py`, shipped in the wheel. Without it a type checker refuses to
    analyse the installed library, and once that refusal is silenced every name imported from it is
    untyped, so no importer's call into it is checked. An application's distribution, which nothing
    imports, carries none.

## Hard stops

- Any identifier is being chosen, or carried over from ported or generated code → stop, use `naming`;
  this skill checks the filename against the class once the name exists.
- Asked which package a module belongs in → stop, use `hex-architecture` (in `pyhouse-hex`) or
  `flat-layered` (in `pyhouse-flat`), or the project's own layout where neither applies.
- Asked whether the boundary between two modules or packages should exist at all → stop, use
  `coupling`; this skill owns the mechanics once it is drawn.
