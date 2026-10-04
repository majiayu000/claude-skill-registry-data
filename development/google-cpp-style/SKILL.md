---
name: google-cpp-style
description: >-
  Use when writing or reviewing C++ under Google's C++ style conventions, including headers,
  naming, classes, functions, ownership, exceptions, and formatting. Do not use as a general C++
  language tutorial.
---

# Google C++ Style Guide

Apply this guidance to the actual project. Repository requirements and newer authoritative guidance take precedence.

## C++ Version

Currently, code should target C++20, i.e., should not use C++23
features. The C++ version targeted by this guide will advance
(aggressively) over time.

## Self-contained Headers

Header files should be self-contained (compile on their own) and
end in `.h`. Non-header files that are meant for inclusion
should end in `.inc` and be used sparingly.
All header files should be self-contained. Users and refactoring
tools should not have to adhere to special conditions to include the
header. Specifically, a header should
have header guards and include all
other headers it needs.

## The #define Guard

All header files should have `#define` guards to
prevent multiple inclusion. The format of the symbol name
should be
`<PROJECT>_<PATH>_<FILE>_H_`.

## Include What You Use

If a source or header file refers to a symbol defined elsewhere,
the file should directly include a header file which properly intends
to provide a declaration or definition of that symbol. It should not
include header files for any other reason.
Do not rely on transitive inclusions. This allows people to remove
no-longer-needed `#include` statements from their headers without
breaking clients. This also applies to related headers
- `foo.cc` should include `bar.h` if it uses a
symbol from it even if `foo.h`
includes `bar.h`.

## Forward Declarations

Avoid using forward declarations where possible.
Instead, include the headers you need.
Do not use forward declarations of entities that your project
does not own.

## Names and Order of Includes

Include headers in the following order: Related header, C system headers,
C++ standard library headers,
other libraries' headers, your project's
headers.
Separate each non-empty group with one blank line.
Within each section the includes should be ordered
alphabetically. Note that older code might not conform to
this rule and should be fixed when convenient.

## Namespaces

With few exceptions, place code in a namespace. Namespaces
should have unique names based on the project name, and possibly
its path. Do not use *using-directives* (e.g.,
`using namespace foo`). Do not use
inline namespaces. For unnamed namespaces, see
Internal Linkage.

## Internal Linkage

When definitions in a `.cc` file do not need to be
referenced outside that file, give them internal linkage by placing
them in an unnamed namespace or declaring them `static`.
Do not use either of these constructs in `.h` files.

## Local Variables

Place a function's variables in the narrowest scope
possible, and initialize variables in the declaration.

## Static and Global Variables

Objects with
[static storage duration](http://en.cppreference.com/w/cpp/language/storage_duration#Storage_duration) are forbidden unless they are
[trivially
destructible](http://en.cppreference.com/w/cpp/types/is_destructible). Informally this means that the destructor does not do
anything, even taking member and base destructors into account. More formally it
means that the type has no user-defined or virtual destructor and that all bases
and non-static members are trivially destructible.
Static function-local variables may use dynamic initialization.
Use of dynamic initialization for static class member variables or variables at
namespace scope is discouraged, but allowed in limited circumstances.

## thread_local Variables

`thread_local` variables that aren't declared inside a function
must be initialized with a true compile-time constant,
and this must be enforced by using the
[`constinit`](https://en.cppreference.com/w/cpp/language/constinit)
attribute. Prefer
`thread_local` over other ways of defining thread-local data.

## Doing Work in Constructors

Avoid virtual method calls in constructors, and avoid
initialization that can fail if you can't signal an error.
Constructors should never call virtual functions. If appropriate
for your code ,
terminating the program may be an appropriate error handling
response. Otherwise, consider a factory function
or `Init()` method as described in
[TotW #42](https://abseil.io/tips/42)
.
Avoid `Init()` methods on objects with
no other states that affect which public methods may be called
(semi-constructed objects of this form are particularly hard to work
with correctly).

## Implicit Conversions

Do not define implicit conversions. Use the `explicit`
keyword for conversion operators and single-argument
constructors.
Type conversion operators, and constructors that are
callable with a single argument, must be marked
`explicit` in the class definition. As an
exception, copy and move constructors should not be
`explicit`, since they do not perform type
conversion.
Constructors that cannot be called with a single argument
may omit `explicit`. Constructors that
take a single `std::initializer_list` parameter should
also omit `explicit`, in order to support copy-initialization
(e.g., `MyType m = {1, 2};`).

## Copyable and Movable Types

A class's public API must make clear whether the class is copyable,
move-only, or neither copyable nor movable. Support copying and/or
moving if these operations are clear and meaningful for your type.
Every class's public interface must make clear which copy and move
operations the class supports. This should usually take the form of explicitly
declaring and/or deleting the appropriate operations in the `public`
section of the declaration.
Specifically, a copyable class should explicitly declare the copy
operations, a move-only class should explicitly declare the move operations, and
a non-copyable/movable class should explicitly delete the copy operations. A
copyable class may also declare move operations in order to support efficient
moves. Explicitly declaring or deleting all four copy/move operations is
permitted, but not required. If you provide a copy or move assignment operator,
you must also provide the corresponding constructor.
A type should not be copyable/movable if the meaning of
copying/moving is unclear to a casual user, or if it incurs unexpected
costs. Move operations for copyable types are strictly a performance
optimization and are a potential source of bugs and complexity, so
avoid defining them unless they are significantly more efficient than
the corresponding copy operations. If your type provides copy operations, it is
recommended that you design your class so that the default implementation of
those operations is correct. Remember to review the correctness of any
defaulted operations as you would any other code.

## Structs vs. Classes

Use a `struct` only for passive objects that
carry data; everything else is a `class`.
`structs` should be used for passive objects that carry
data, and may have associated constants. All fields must be public. The
struct type itself must not have invariants that imply relationships between
different fields, since direct user access to those fields may
break those invariants, but users of a struct may have requirements and
guarantees on particular uses of it. Constructors, destructors, and helper
methods may be present; however, these methods must not require or enforce
any invariants.
If more functionality or invariants are required, or struct has wide visibility and expected to
evolve, then a `class` is more appropriate. If in doubt, make it a `class`.

## Inheritance

Composition is often more appropriate than inheritance.
When using inheritance, make it `public`.
Explicitly annotate overrides of virtual functions or virtual
destructors with exactly one of an `override` or (less
frequently) `final` specifier. Do not
use `virtual` when declaring an override.
Rationale: A function or destructor marked
`override` or `final` that is
not an override of a base class virtual function will
not compile, and this helps catch common errors. The
specifiers serve as documentation; if no specifier is
present, the reader has to check all ancestors of the
class in question to determine if the function or
destructor is virtual or not.

## Access Control

Make classes' data members `private`, unless they are
constants. This simplifies reasoning about invariants, at the cost
of some easy boilerplate in the form of accessors (usually `const`) if necessary.

## Inputs and Outputs

Prefer using return values over output parameters:
they improve readability, and often provide the same or better performance.
See
[TotW #176](https://abseil.io/tips/176).
Prefer to return by value or, failing that, return by reference.
Avoid returning a raw pointer unless it can be null.
Parameters are either inputs to the function, outputs from the
function, or both. Non-optional input parameters should usually be values
or `const` references, while non-optional output and
input/output parameters should usually be references (which cannot be null).
Generally, use `std::optional` to represent optional by-value
inputs, and use a `const` pointer when the non-optional form would
have used a reference. Use non-`const` pointers to represent
optional outputs and optional input/output parameters.
Avoid defining functions that require a reference parameter to outlive the call.
In some cases reference parameters can bind to temporaries, leading to lifetime
bugs. Instead, find a way to eliminate the lifetime requirement
(for example, by copying the parameter), or pass retained parameters by
pointer and document the lifetime and non-null requirements.
See [TotW 116](https://abseil.io/tips/116) for more.

## Write Short Functions

Prefer small and focused functions.

## Function Overloading

Use overloaded functions (including constructors) only if a
reader looking at a call site can get a good idea of what
is happening without having to first figure out exactly
which overload is being called.
You may overload a function when there are no semantic differences
between variants. These overloads may vary in types, qualifiers, or
argument count. However, a reader of such a call must not need to know
which member of the overload set is chosen, only that **something**
from the set is being called.

## Default Arguments

Default arguments are allowed on non-virtual functions
when the default is guaranteed to always have the same
value. Follow the same restrictions as for function overloading, and
prefer overloaded functions if the readability gained with
default arguments doesn't outweigh the downsides below.
Default arguments are banned on virtual functions, where
they don't work properly, and in cases where the specified
default might not evaluate to the same value depending on
when it was evaluated. (For example, don't write `void
f(int n = counter++);`.)

## Ownership and Smart Pointers

Prefer to have single, fixed owners for dynamically
allocated objects. Prefer to transfer ownership with smart
pointers.
Do not design your code to use shared ownership
without a very good reason. One such reason is to avoid
expensive copy operations, but you should only do this if
the performance benefits are significant, and the
underlying object is immutable (i.e.,
`std::shared_ptr<const Foo>`). If you
do use shared ownership, prefer to use
`std::shared_ptr`.

## Exceptions

We do not use C++ exceptions.
This prohibition also applies to exception handling related
features such as `std::exception_ptr` and
`std::nested_exception`.

## Run-Time Type Information (RTTI)

Avoid using run-time type information (RTTI).
RTTI has legitimate uses but is prone to abuse, so you
must be careful when using it. You may use it freely in
unit tests, but avoid it when possible in other code. In
particular, think twice before using RTTI in new code. If
you find yourself needing to write code that behaves
differently based on the class of an object, consider one
of the following alternatives to querying the type:
- Virtual methods are the preferred way of executing
  different code paths depending on a specific subclass
  type. This puts the work within the object itself.
- If the work belongs outside the object and instead
  in some processing code, consider a double-dispatch
  solution, such as the Visitor design pattern. This
  allows a facility outside the object itself to
  determine the type of class using the built-in type
  system.
Do not hand-implement an RTTI-like workaround. The
arguments against RTTI apply just as much to workarounds
like class hierarchies with type tags. Moreover,
workarounds disguise your true intent.

## Casting

Use C++-style casts
like `static_cast<float>(double_value)`, or brace
initialization for conversion of arithmetic types like
`int64_t y = int64_t{1} << 42`. Do not use
cast formats like `(int)x` unless the cast is to
`void`. You may use cast formats like `T(x)` only when
`T` is a class type.

## Use of const

In APIs, use `const` whenever it makes sense.
`constexpr` is a better choice for some uses of
`const`.
All of a class's `const` operations should be safe
to invoke concurrently with each other. If that's not feasible, the class must
be clearly documented as "thread-unsafe".

## Use of constexpr, constinit, and consteval

Use `constexpr` to define true
constants or to ensure constant initialization.
Use `constinit` to ensure constant
initialization for non-constant variables.

## Integer Types

Of the built-in C++ integer types, the only one used
is
`int`. If a program needs an integer type of a
different size, use an exact-width integer type from
`<stdint.h>`, such as
`int16_t`. If you have a
value that could ever be greater than or equal to 2^31,
use a 64-bit type such as `int64_t`.
Keep in mind that even if your value won't ever be too large
for an `int`, it may be used in intermediate
calculations which may require a larger type. When in doubt,
choose a larger type.
You should not use the unsigned integer types such as
`uint32_t`, unless there is a valid
reason such as representing a bit pattern rather than a
number, or you need defined overflow modulo 2^N. In
particular, do not use unsigned types to say a number
will never be negative. Instead, use
assertions for this.

## Preprocessor Macros

Avoid defining macros, especially in headers; prefer
inline functions, enums, and `const` variables.
Name macros with a project-specific prefix. Do not use
macros to define pieces of a C++ API.
Exporting macros from headers (i.e., defining them in a header
without `#undef`ing them before the end of the header)
is extremely strongly discouraged. If you do export a macro from a
header, it must have a globally unique name. To achieve this, it
must be named with a prefix consisting of your project's namespace
name (but upper case).

## 0 and nullptr/NULL

Use `nullptr` for pointers, and `'\0'` for chars (and
not the `0` literal).

## Type Deduction (including auto)

Use type deduction only if it makes the code clearer to readers who aren't
familiar with the project, or if it makes the code safer. Do not use it
merely to avoid the inconvenience of writing an explicit type.

## Concepts and Constraints

Use concepts sparingly.
In general, concepts and constraints should only be used in cases
where templates would have been used prior to C++20.
Avoid introducing new concepts in headers,
unless the headers are marked as internal to the library.
Do not define concepts that are not enforced by the compiler.
Prefer constraints over template metaprogramming, and
avoid the `template<Concept T>` syntax;
instead, use the `requires(Concept<T>)`
syntax.

## Nonstandard Extensions

Nonstandard extensions to C++ may not be used unless otherwise specified.
Do not use nonstandard extensions. You may use portability wrappers that
are implemented using nonstandard extensions, so long as those wrappers
are provided by a designated project-wide portability
header.

## Choosing Names

Give things names that make their purpose or intent understandable to a new
reader, even someone on a different team than the owners. Do not worry about
saving horizontal space as it is far more important to make your code
immediately understandable by a new reader.

## File Names

Filenames should be all lowercase and can include
underscores (`_`) or dashes (`-`).
Follow the convention that your
project uses. If there is no consistent
local pattern to follow, prefer "`_`".

## Type Names

Type names start with a capital letter and have a capital
letter for each new word, with no underscores:
`MyExcitingClass`, `MyExcitingEnum`.

## Variable Names

The names of variables (including function parameters) and data members are
`snake_case` (all lowercase, with underscores between words). Data members of classes
(but not structs) additionally have trailing underscores. For instance:
`a_local_variable`, `a_struct_data_member`,
`a_class_data_member_`.

## Constant Names

Variables declared `constexpr` or `const`, and whose value is fixed for
the duration of the program, are named with a leading "k" followed
by mixed case. Underscores can be used as separators in the rare cases
where capitalization cannot be used for separation. For example:
```
const int kDaysInAWeek = 7;
const int kAndroid8_0_0 = 24;  // Android 8.0.0
```

## Function Names

Ordinarily, functions follow [PascalCase](https://en.wiktionary.org/wiki/Pascal_case):
start with a capital letter and have a capital letter for each new word.
Accessors and mutators (get and set functions) may be named like variables,
in `snake_case`. These often correspond to actual member variables,
but this is not required. For example, `int count()` and
`void set_count(int count)`.

## Namespace Names

Namespace names are `snake_case` (all lowercase, with underscores
between words).
Top-level namespaces must be globally unique and recognizable, so each one
should be owned by a single project or team, with a name based on the name of
that project or team. Usually, all code in the namespace should be under one or
more directories with the same name as the namespace.

## Macro Names

Please see the description
of macros; in general macros should *not* be used.
However, if they are absolutely needed, then they should be
named with all capitals and underscores, and with a project-specific prefix.

## Function Declarations

Almost every function declaration should have comments immediately
preceding it that describe what the function does and how to use
it. These comments may be omitted only if the function is simple and
obvious (e.g., simple accessors for obvious properties of the class).
Private methods and functions declared in `.cc` files are not exempt.
Function comments should be written with an implied subject of
*This function* and should start with the verb phrase; for example,
"Opens the file", rather than "Open the file". In general, these comments do not
describe how the function performs its task. Instead, that should be
left to comments in the function definition.

## Line Length

Each line of text in your code should be at most 80
characters long.
A line may exceed 80 characters if it is

## Looping and branching statements

- The components of the statement should be separated by single spaces (not
  line breaks).
- Inside the condition or iteration specifier, put one space (or a line
  break) between each semicolon and the next token, except if the token is a
  closing parenthesis or another semicolon.
- Inside the condition or iteration specifier, do not put a space after the
  opening parenthesis or before the closing parenthesis.
- Put any controlled statements inside blocks (i.e., use curly braces).
- Inside the controlled blocks, put one line break immediately after the
  opening brace, and one line break immediately before the closing brace.
Empty loop bodies should use either an empty pair of braces or
`continue` with no braces, rather than a single semicolon.
