---
name: google-python-style
description: >-
  Use when writing or reviewing Python under Google's conventions for language rules, imports,
  exceptions, typing, naming, comments, tests, and formatting. Do not use as a Python beginner
  tutorial.
---

# Google Python Style Guide

Apply this guidance to the actual project. Repository requirements and newer authoritative guidance take precedence.

## 2.1 Lint

Make sure you run
`pylint`
on your code.
Suppress warnings if they are inappropriate so that other issues are not hidden.
To suppress warnings, you can set a line-level comment:
If the reason for the suppression is not clear from the symbolic name, add an
explanation.

## 2.2 Imports

*   Use `import x` for importing packages and modules.
*   Use `from x import y` where `x` is the package prefix and `y` is the module
    name with no prefix.
*   Use `from x import y as z` in any of the following circumstances:
    -   Two modules named `y` are to be imported.
    -   `y` conflicts with a top-level name defined in the current module.
    -   `y` conflicts with a common parameter name that is part of the public
        API (e.g., `features`).
    -   `y` is an inconveniently long name.
    -   `y` is too generic in the context of your code (e.g., `from
        storage.file_system import options as fs_options`).
*   Use `import y as z` only when `z` is a standard abbreviation (e.g., `import
    numpy as np`).
Do not use relative names in imports. Even if the module is in the same package,
use the full package name. This helps prevent unintentionally importing a
package twice.

## 2.4 Exceptions

Exceptions must follow certain conditions:
-   Make use of built-in exception classes when it makes sense. For example,
    raise a `ValueError` to indicate a programming mistake like a violated
    precondition, such as may happen when validating function arguments.
-   Do not use `assert` statements in place of conditionals or validating
    preconditions. They must not be critical to the application logic. A litmus
    test would be that the `assert` could be removed without breaking the code.
    `assert` conditionals are
    [not guaranteed](https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement)
    to be evaluated. For [pytest](https://pytest.org) based tests, `assert` is
    okay and expected to verify expectations. For
    example:
-   Libraries or packages may define their own exceptions. When doing so they
    must inherit from an existing exception class. Exception names should end in
    `Error` and should not introduce repetition (`foo.FooError`).
-   Never use catch-all `except:` statements, or catch `Exception` or
    `StandardError`, unless you are
    -   re-raising the exception, or
    -   creating an isolation point in the program where exceptions are not
        propagated but are recorded and suppressed instead, such as protecting a
        thread from crashing by guarding its outermost block.
-   Minimize the amount of code in a `try`/`except` block. The larger the body
    of the `try`, the more likely that an exception will be raised by a line of
    code that you didn't expect to raise an exception. In those cases, the
    `try`/`except` block hides a real error.
-   Use the `finally` clause to execute code whether or not an exception is
    raised in the `try` block. This is often useful for cleanup, i.e., closing a
    file.

## 2.5 Mutable Global State

Avoid mutable global state.
In those rare cases where using global state is warranted, mutable global
entities should be declared at the module level or as a class attribute and made
internal by prepending an `_` to the name. If necessary, external access to
mutable global state must be done through public functions or class methods. See
Naming below. Please explain the design reasons why mutable
global state is being used in a comment or a doc linked to from a comment.
Module-level constants are permitted and encouraged. For example:
`_MAX_HOLY_HANDGRENADE_COUNT = 3` for an internal use constant or
`SIR_LANCELOTS_FAVORITE_COLOR = "blue"` for a public API constant. Constants
must be named using all caps with underscores. See Naming
below.

## 2.7 Comprehensions & Generator Expressions

Comprehensions are allowed, however multiple `for` clauses or filter expressions
are not permitted. Optimize for readability, not conciseness.

## 2.9 Generators

Fine. Use "Yields:" rather than "Returns:" in the docstring for generator
functions.
If the generator manages an expensive resource, make sure to force the clean up.
A good way to do the clean up is by wrapping the generator with a context
manager [PEP-0533](https://peps.python.org/pep-0533/).

## 2.10 Lambda Functions

Lambdas are allowed. If the code inside the lambda function spans multiple lines
or is longer than 60-80 chars, it might be better to define it as a regular
nested function.
For common operations like multiplication, use the functions from the `operator`
module instead of lambda functions. For example, prefer `operator.mul` to
`lambda x, y: x * y`.

## 2.12 Default Argument Values

Okay to use with the following caveat:
Do not use mutable objects as default values in the function or method
definition.

## 2.13 Properties

Properties are allowed, but, like operator overloading, should only be used when
necessary and match the expectations of typical attribute access; follow the
getters and setters rules otherwise.
For example, using a property to simply both get and set an internal attribute
isn't allowed: there is no computation occurring, so the property is unnecessary
(make the attribute public instead). In comparison,
using a property to control attribute access or to calculate a *trivially*
derived value is allowed: the logic is simple and unsurprising.

## 2.14 True/False Evaluations

Use the "implicit" false if possible, e.g., `if foo:` rather than `if foo !=
[]:`. There are a few caveats that you should keep in mind though:
-   Always use `if foo is None:` (or `is not None`) to check for a `None` value.
    E.g., when testing whether a variable or argument that defaults to `None`
    was set to some other value. The other value might be a value that's false
    in a boolean context!
-   Never compare a boolean variable to `False` using `==`. Use `if not x:`
    instead. If you need to distinguish `False` from `None` then chain the
    expressions, such as `if not x and x is not None:`.
-   For sequences (strings, lists, tuples), use the fact that empty sequences
    are false, so `if seq:` and `if not seq:` are preferable to `if len(seq):`
    and `if not len(seq):` respectively.
-   Note that Numpy arrays may raise an exception in an implicit boolean
    context. Prefer the `.size` attribute when testing emptiness of a `np.array`
    (e.g. `if not users.size`).

## 2.18 Threading

Do not rely on the atomicity of built-in types.
Use the `queue` module's `Queue` data type as the preferred way to communicate
data between threads. Otherwise, use the `threading` module and its locking
primitives. Prefer condition variables and `threading.Condition` instead of
using lower-level locks.

## 2.21 Type Annotated Code

You are strongly encouraged to enable Python type analysis when updating code.
When adding or modifying public APIs, include type annotations and enable
checking via pytype in the build system. As static analysis is relatively new to
Python, we acknowledge that undesired side-effects (such as
wrongly
inferred types) may prevent adoption by some projects. In those situations,
authors are encouraged to add a comment with a TODO or link to a bug describing
the issue(s) currently preventing type annotation adoption in the BUILD file or
in the code itself as appropriate.

## 3.2 Line length

Maximum line length is *80 characters*.
Do not use a backslash for
[explicit line continuation](https://docs.python.org/3/reference/lexical_analysis.html#explicit-line-joining).
Instead, make use of Python's
[implicit line joining inside parentheses, brackets and braces](http://docs.python.org/reference/lexical_analysis.html#implicit-line-joining).
If necessary, you can add an extra pair of parentheses around an expression.

## 3.4 Indentation

Indent your code blocks with *4 spaces*.
Never use tabs. Implied line continuation should align wrapped elements
vertically (see line length examples), or use a hanging
4-space indent. Closing (round, square or curly) brackets can be placed at the
end of the expression, or on separate lines, but then should be indented the
same as the line with the corresponding opening bracket.

## 3.8.1 Docstrings

Python uses *docstrings* to document code. A docstring is a string that is the
first statement in a package, module, class or function. These strings can be
extracted automatically through the `__doc__` member of the object and are used
by `pydoc`.
(Try running `pydoc` on your module to see how it looks.) Always use the
three-double-quote `"""` format for docstrings (per
[PEP 257](https://peps.python.org/pep-0257/)). A docstring should be organized
as a summary line (one physical line not exceeding 80 characters) terminated by
a period, question mark, or exclamation point. When writing more (encouraged),
this must be followed by a blank line, followed by the rest of the docstring
starting at the same cursor position as the first quote of the first line. There
are more formatting guidelines for docstrings below.

## 3.8.3 Functions and Methods

A docstring is mandatory for every function that has one or more of the
following properties:
-   being part of the public API
-   nontrivial size
-   non-obvious logic
A docstring should give enough information to write a call to the function
without reading the function's code. The docstring should describe the
function's calling syntax and its semantics, but generally not its
implementation details, unless those details are relevant to how the function is
to be used. For example, a function that mutates one of its arguments as a side
effect should note that in its docstring. Otherwise, subtle but important
details of a function's implementation that are not relevant to the caller are
better expressed as comments alongside the code than within the function's
docstring.

## 3.8.4 Classes

Classes should have a docstring below the class definition describing the class.
Public attributes, excluding properties, should be documented
here in an `Attributes` section and follow the same formatting as a
function's `Args` section.
All class docstrings should start with a one-line summary that describes what
the class instance represents. This implies that subclasses of `Exception`
should also describe what the exception represents, and not the context in which
it might occur. The class docstring should not repeat unnecessary information,
such as that the class is a class.

## 3.8.5 Block and Inline Comments

The final place to have comments is in tricky parts of the code. If you're going
to have to explain it at the next [code review](http://en.wikipedia.org/wiki/Code_review),
you should comment it now. Complicated operations get a few lines of comments
before the operations commence. Non-obvious ones get comments at the end of the
line.

## 3.10 Strings

Use an
[f-string](https://docs.python.org/3/reference/lexical_analysis.html#f-strings),
the `%` operator, or the `format` method for formatting strings, even when the
parameters are all strings. Use your best judgment to decide between string
formatting options. A single join with `+` is okay but do not format with `+`.
Avoid using the `+` and `+=` operators to accumulate a string within a loop. In
some conditions, accumulating a string with addition can lead to quadratic
rather than linear running time. Although common accumulations of this sort may
be optimized on CPython, that is an implementation detail. The conditions under
which an optimization applies are not easy to predict and may change. Instead,
add each substring to a list and `''.join` the list after the loop terminates,
or write each substring to an `io.StringIO` buffer. These techniques
consistently have amortized-linear run-time complexity.
Be consistent with your choice of string quote character within a file. Pick `'`
or `"` and stick with it. It is okay to use the other quote character on a
string to avoid the need to backslash-escape quote characters within the string.

## 3.10.1 Logging

For logging functions that expect a pattern-string (with %-placeholders) as
their first argument: Always call them with a string literal (not an f-string!)
as their first argument with pattern-parameters as subsequent arguments. Some
logging implementations collect the unexpanded pattern-string as a queryable
field. It also prevents spending time rendering a message that no logger is
configured to output.

## 3.10.2 Error Messages

Error messages (such as: message strings on exceptions like `ValueError`, or
messages shown to the user) should follow three guidelines:
1.  The message needs to precisely match the actual error condition.
2.  Interpolated pieces need to always be clearly identifiable as such.
3.  They should allow simple automated processing (e.g. grepping).

## 3.11 Files, Sockets, and similar Stateful Resources

Explicitly close files and sockets when done with them. This rule naturally
extends to closeable resources that internally use sockets, such as database
connections, and also other resources that need to be closed down in a similar
fashion. To name only a few examples, this also includes
[mmap](https://docs.python.org/3/library/mmap.html) mappings,
[h5py File objects](https://docs.h5py.org/en/stable/high/file.html), and
[matplotlib.pyplot figure windows](https://matplotlib.org/2.1.0/api/_as_gen/matplotlib.pyplot.close.html).
The preferred way to manage files and similar resources is using the
[`with` statement](http://docs.python.org/reference/compound_stmts.html#the-with-statement):
For file-like objects that do not support the `with` statement, use
`contextlib.closing()`:
In rare cases where context-based resource management is infeasible, code
documentation must explain clearly how resource lifetime is managed.

## 3.13 Imports formatting

Imports should be on separate lines; there are
exceptions for `typing` and `collections.abc` imports.
Imports are always put at the top of the file, just after any module comments
and docstrings and before module globals and constants. Imports should be
grouped from most generic to least generic:
1.  Python future import statements. For example:
    ```python
    from __future__ import annotations
    ```
2.  Python standard library imports. For example:
    ```python
    import sys
    ```
3.  [third-party](https://pypi.org/) module
    or package imports. For example:
    ```python
    import tensorflow as tf
    ```
4.  Code repository
    sub-package imports. For example:
    ```python
    from otherproject.ai import mind
    ```
Within each grouping, imports should be sorted lexicographically, ignoring case,
according to each module's full package path (the `path` in `from path import
...`). Code may optionally place a blank line between import sections.

## 3.16 Naming

`module_name`, `package_name`, `ClassName`, `method_name`, `ExceptionName`,
`function_name`, `GLOBAL_CONSTANT_NAME`, `global_var_name`, `instance_var_name`,
`function_parameter_name`, `local_var_name`, `query_proper_noun_for_thing`,
`send_acronym_via_https`.
Names should be descriptive. This includes functions, classes, variables,
attributes, files and any other type of named entities.
Avoid abbreviation. In particular, do not use abbreviations that are ambiguous
or unfamiliar to readers outside your project, and do not abbreviate by deleting
letters within a word.
Always use a `.py` filename extension. Never use dashes.

## 3.16.1 Names to Avoid

-   single character names, except for specifically allowed cases:
    -   counters or iterators (e.g. `i`, `j`, `k`, `v`, et al.)
    -   `e` as an exception identifier in `try/except` statements.
    -   `f` as a file handle in `with` statements
    -   private type variables with no constraints (e.g.
        `_T = TypeVar("_T")`, `_P = ParamSpec("_P")`)
    -   names that match established notation in a reference paper or algorithm
        (see Mathematical Notation)
Please be mindful not to abuse single-character naming. Generally speaking,
descriptiveness should be proportional to the name's scope of visibility.
For example, `i` might be a fine name for 5-line code block but within
multiple nested scopes, it is likely too vague.
-   `__double_leading_and_trailing_underscore__` names (reserved by Python)
-   offensive terms
-   names that needlessly include the type of the variable (for example:
    `id_to_name_dict`)

## 3.16.2 Naming Conventions

-   Prepending a single underscore (`_`) has some support for protecting module
    variables and functions (linters will flag protected member access). Note
    that it is okay for unit tests to access protected constants from the
    modules under test.
-   Prepending a double underscore (`__` aka "dunder") to an instance variable
    or method effectively makes the variable or method private to its class
    (using name mangling); we discourage its use as it impacts readability and
    testability, and isn't *really* private. Prefer a single underscore.

## 3.16.5 Mathematical Notation

For mathematically-heavy code, short variable names that would otherwise violate
the style guide are preferred when they match established notation in a
reference paper or algorithm.
When using names based on established notation:
1.  Cite the source of all naming conventions, preferably with a hyperlink to
    academic resource itself, in a comment or docstring. If the source is not
    accessible, clearly document the naming conventions.
2.  Prefer PEP8-compliant `descriptive_names` for public APIs, which are much
    more likely to be encountered out of context.
3.  Use a narrowly-scoped `pylint: disable=invalid-name` directive to silence
    warnings. For just a few variables, use the directive as an endline comment
    for each one; for more, apply the directive at the beginning of a block.

## 3.17 Main

In Python, `pydoc` as well as unit tests require modules to be importable. If a
file is meant to be used as an executable, its main functionality should be in a
`main()` function, and your code should always check `if __name__ == '__main__'`
before executing your main program, so that it is not executed when the module
is imported.
All code at the top level will be executed when the module is imported. Be
careful not to call functions, create objects, or perform other operations that
should not be executed when the file is being `pydoc`ed.

## 3.19.1 General Rules

*   If any other variable or a returned type should not be expressed, use `Any`.
*   You are not required to annotate all the functions in a module.
    -   At least annotate your public APIs.
    -   Use judgment to get to a good balance between safety and clarity on the
        one hand, and flexibility on the other.
    -   Annotate code that is prone to type-related errors (previous bugs or
        complexity).
    -   Annotate code that is hard to understand.
    -   Annotate code as it becomes stable from a types perspective. In many
        cases, you can annotate all the functions in mature code without losing
        too much flexibility.

## 3.19.5 NoneType

In the Python type system, `NoneType` is a "first class" type, and for typing
purposes, `None` is an alias for `NoneType`. If an argument can be `None`, it
has to be declared! You can use `|` union type expressions (recommended in new
Python 3.10+ code), or the older `Optional` and `Union` syntaxes.
Use explicit `X | None` instead of implicit. Earlier versions of type checkers
allowed `a: str = None` to be interpreted as `a: str | None = None`, but that is
no longer the preferred behavior.

## 3.19.12 Imports For Typing

For symbols (including types, functions, and constants) from the `typing` or
`collections.abc` modules used to support static analysis and type checking,
always import the symbol itself. This keeps common annotations more concise and
matches typing practices used around the world. You are explicitly allowed to
import multiple specific symbols on one line from the `typing` and
`collections.abc` modules. For example:
```python
from collections.abc import Mapping, Sequence
from typing import Any, Generic, cast, TYPE_CHECKING
```
When annotating function signatures, prefer abstract container types like
`collections.abc.Sequence` over concrete types like `list`. If you need to use a
concrete type (for example, a `tuple` of typed elements), prefer built-in types
like `tuple` over the parametric type aliases from the `typing` module (e.g.,
`typing.Tuple`).
```python
from typing import List, Tuple

def transform_coordinates(original: List[Tuple[float, float]]) ->
    List[Tuple[float, float]]:
  ...
```
```python
from collections.abc import Sequence

def transform_coordinates(original: Sequence[tuple[float, float]]) ->
    Sequence[tuple[float, float]]:
  ...
```

## 3.19.15 Generics

When annotating, prefer to specify type parameters for
[generic](https://docs.python.org/3/library/typing.html#generics) types in a
parameter list; otherwise, the generics' parameters will be assumed to be
[`Any`](https://docs.python.org/3/library/typing.html#the-any-type).
