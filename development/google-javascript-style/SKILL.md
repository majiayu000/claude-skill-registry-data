---
name: google-javascript-style
description: >-
  Use when maintaining existing JavaScript under Google's source formatting, naming, module,
  language-feature, JSDoc, and policy conventions. The upstream guide is no longer updated. For
  TypeScript, use google-typescript-style instead.
---

# Google JavaScript Style Guide

Apply this guidance to the actual project. Repository requirements and newer authoritative guidance take precedence.

## 2.1 File name

File names must be all lowercase and may include underscores (`_`) or dashes
(`-`), but no additional punctuation. Follow the convention that your project
uses. Filenames’ extension must be `.js`.

## 3 Source file structure

All new source files should either be a `goog.module`
file (a file containing a `goog.module` call) or an ECMAScript (ES) module (uses
`import` and `export` statements).
Files consist of the following, **in order**:
1. License or copyright information, if present
2. `@fileoverview` JSDoc, if present
3. `goog.module` statement, if a `goog.module` file
4. ES `import` statements, if an ES module
5. `goog.require` and `goog.requireType` statements
6. The file’s implementation
**Exactly one blank line** separates each section that is present, except the
file's implementation, which may be preceded by 1 or 2 blank lines.

## 3.4.1.1.1 File extensions in import paths

The `.js` file extension is not optional in import paths and must always be
included.

## 3.4.2.1 Named vs default exports

Use named exports in all code. You can apply the `export` keyword to a
declaration, or use the `export {name};` syntax.
Do not use default exports. Importing modules must give a name to these values,
which can lead to inconsistencies in naming across modules.

## 3.4.2.2 Mutability of exports

Exported variables must not be mutated outside of module initialization.
There are alternatives if mutation is needed, including exporting a constant
reference to an object that has mutable fields or exporting accessor functions for
mutable data.

## 3.4.3 Circular Dependencies in ES modules

Do not create cycles between ES modules, even though the ECMAScript
specification allows this. Note that it is possible to create cycles with both
the `import` and `export` statements.

## 3.6 `goog.require` and `goog.requireType` statements

Imports are done with `goog.require` and `goog.requireType` statements. The
names imported by a `goog.require` statement may be used both in code and in
type annotations, while those imported by a `goog.requireType` may be used in
type annotations only.
The `goog.require` and `goog.requireType` statements form a contiguous block
with no empty lines. This block follows the `goog.module` declaration separated
by a single empty line. The entire argument to
`goog.require` or `goog.requireType` is a namespace defined by a `goog.module`
in a separate file. `goog.require` and `goog.requireType` statements may not
appear anywhere else in the file.
Each `goog.require` or `goog.requireType` is assigned to a single constant
alias, or else destructured into several constant aliases. These aliases are the
only acceptable way to refer to dependencies in type annotations or code. Fully
qualified namespaces must not be used anywhere, except as an argument to
`goog.require` or `goog.requireType`.
A file should not contain both a `goog.require` and a `goog.requireType`
statement for the same namespace. If the imported name is used both in code and
in type annotations, it should be imported by a single `goog.require` statement.
If a module is imported only for its side effects, the call must be a
`goog.require` (not a `goog.requireType`) and assignment may be omitted. A
comment is required to explain why this is needed and suppress a compiler
warning.
The lines are sorted according to the following rules: All requires with a name
on the left hand side come first, sorted alphabetically by those names. Then
destructuring requires, again sorted by the names on the left hand side.
Finally, any require calls that are standalone (generally these are for modules
imported just for their side effects).

## 4.1.1 Braces are used for all control structures

Braces are required for all control structures (i.e. `if`, `else`, `for`, `do`,
`while`, as well as any others), even if the body contains only a single
statement. The first statement of a non-empty block must begin on its own line.
**Exception**: A simple if statement that can fit entirely on a single line with
no wrapping (and that doesn’t have an else) may be kept on a single line with no
braces when it improves readability. This is the only case in which a control
structure may omit braces and newlines.

## 4.2 Block indentation: +2 spaces

Each time a new block or block-like construct is opened, the indent increases by
two spaces. When the block ends, the indent returns to the previous indent
level. The indent level applies to both code and comments throughout the block.

## 4.3.2 Semicolons are required

Every statement must be terminated with a semicolon. Relying on automatic
semicolon insertion is forbidden.

## 4.4 Column limit: 80

JavaScript code has a column limit of 80 characters. Except as noted below, any
line that would exceed this limit must be line-wrapped.
1. `goog.module`, `goog.require` and `goog.requireType` statements.
2. ES module `import` and `export from` statements.
3. Lines where obeying the column limit is not possible or would hinder
   discoverability. Examples include:
   - A long URL which should be clickable in source.
   - A shell command intended to be copied-and-pasted.
   - A long string literal which may need to be copied or searched for wholly
     (e.g., a long file path).

## 4.5.1 Where to break

The prime directive of line-wrapping is: prefer to break at a **higher syntactic
level**.
1. When a line is broken at an operator the break comes after the symbol. (Note
   that this is not the same practice used in Google style for Java.)
   1. This does not apply to the "dot" (`.`), which is not actually an
      operator.
2. A method or constructor name stays attached to the open parenthesis (`(`)
   that follows it.
3. A comma (`,`) stays attached to the token that precedes it.
4. A line break is never added between a return and the return value as this
   would change the meaning of the code.
5. JSDoc annotations with type names break after "{". This is necessary as
   annotations with optional types (@const, @private, @param, etc) do not scan
   the next line.
> Note: The primary goal for line wrapping is to have clear code, not
> necessarily code that fits in the smallest number of lines.

## 4.5.2 Indent continuation lines at least +4 spaces

When line-wrapping, each line after the first (each *continuation line*) is
indented at least +4 from the original line, unless it falls under the rules of
block indentation.
When there are multiple continuation lines, indentation may be varied beyond +4
as appropriate. In general, continuation lines at a deeper syntactic level are
indented by larger multiples of 4, and two lines use the same indentation level
if and only if they begin with syntactically parallel elements.

## 5.1.1 Use `const` and `let`

Declare all local variables with either `const` or `let`. Use `const` by
default, unless a variable needs to be reassigned. The `var` keyword
must not be used.

## 5.1.2 One variable per declaration

Every local variable declaration declares only one variable: declarations such
as `let a = 1, b = 2;` are not used.

## 5.1.3 Declared when needed, initialized as soon as possible

Local variables are **not** habitually declared at the start of their containing
block or block-like construct. Instead, local variables are declared close to
the point they are first used (within reason), to minimize their scope, and
initialized as soon as possible.

## 5.2.1 Use trailing commas

Include a trailing comma whenever there is a line break between the final
element and the closing bracket.

## 5.3.3 Do not mix quoted and unquoted keys

Object literals may represent either *structs* (with unquoted keys and/or
symbols) or *dicts* (with quoted and/or computed keys). Do not mix these key
types in a single object literal.
This also extends to passing the property name to functions, like
`hasOwnProperty`. In particular, doing so will break in compiled code because
the compiler cannot rename/obfuscate the string literal.

## 5.4.2 Fields

Define all of a concrete object’s fields (i.e. all properties other than
methods) in the constructor. Annotate fields that are never reassigned with
`@const` (these need not be deeply immutable). Annotate non-public fields with
the proper visibility annotation (`@private`, `@protected`, `@package`).
`@private` fields' names may optionally end with an underscore. Fields must not
be defined within a nested scope in the constructor nor on a concrete class's
`prototype`.

## 5.4.6 Do not manipulate `prototype`s directly

The `class` keyword allows clearer and more readable class definitions than
defining `prototype` properties. Ordinary implementation code has no business
manipulating these objects, though they are still useful for defining classes.
Mixins and modifying the
prototypes of builtin objects are explicitly forbidden.

## 5.4.11 Do not create static container classes

Do not use container classes with only static methods or properties for the sake
of namespacing.

## 5.4.12 Do not define nested namespaces

Do not define a nested type (e.g. class, typedef, enum, interface) on another
module-local name.

## 5.5.3 Arrow functions

Arrow functions provide a concise function syntax and simplify scoping `this`
for nested functions. Prefer arrow functions over the `function` keyword for
nested functions.
Prefer arrow functions over other `this` scoping approaches such as
`f.bind(this)`, `goog.bind(f, this)`, and `const self = this`. Arrow functions
are particularly useful for calling into callbacks as they permit explicitly
specifying which parameters to pass to the callback whereas binding will blindly
pass along all parameters.
The right-hand side of the arrow contains the body of the function. By default
the body is a block statement (zero or more statements surrounded by curly
braces). The body may also be an implicitly returned single expression if
either: the program logic requires returning a value, or the `void` operator
precedes a single function or method call (using `void` ensures `undefined` is
returned, prevents leaking values, and communicates intent). The single
expression form is preferred if it improves readability (e.g., for short or
simple expressions).

## 5.5.5.2 Rest parameters

Use a *rest* parameter instead of accessing `arguments`. Rest parameters are
typed with a `...` prefix in their JSDoc. The rest parameter must be the last
parameter in the list. There is no space between the `...` and the parameter
name. Do not name the rest parameter `var_args`. Never name a local variable or
parameter `arguments`, which confusingly shadows the built-in name.

## 5.6.1 Use single quotes

Ordinary string literals are delimited with single quotes (`'`), rather than
double quotes (`"`).
Ordinary string literals may not span multiple lines.

## 5.6.3 No line continuations

Do not use *line continuations* (that is, ending a line inside a string literal
with a backslash) in either ordinary or template string literals. Even though
ES5 allows this, it can lead to tricky errors if any trailing whitespace comes
after the slash, and is less obvious to readers.

## 5.8.1 For loops

With ES6, the language now has three different kinds of `for` loops. All may be
used, though `for`-`of` loops should be preferred when possible.
`for`-`in` loops may only be used on dict-style objects, and should not be used to iterate over an
array. `Object.prototype.hasOwnProperty` should be used in `for`-`in` loops to
exclude unwanted prototype properties. Prefer `for`-`of` and `Object.keys` over
`for`-`in` when possible.

## 5.8.2 Exceptions

Exceptions are an important part of the language and should be used whenever
exceptional cases occur. Always throw `Error`s or subclasses of `Error`: never
throw string literals or other objects. Always use `new` when constructing an
`Error`.
This treatment extends to `Promise` rejection values as `Promise.reject(obj)` is
equivalent to `throw obj;` in async functions.

## 5.8.2.1 Empty catch blocks

It is very rarely correct to do nothing in response to a caught exception. When
it truly is appropriate to take no action whatsoever in a catch block, the
reason this is justified is explained in a comment.

## 5.8.3.1 Fall-through: commented

Within a switch block, each statement group either terminates abruptly (with a
`break`, `return` or `throw`n exception), or is marked with a comment to
indicate that execution will or might continue into the next statement group.
Any comment that communicates the idea of fall-through is sufficient (typically
`// fall through`). This special comment is not required in the last statement
group of the switch block.

## 5.8.3.2 The `default` case is present

Each switch statement includes a `default` statement group, even if it contains
no code. The `default` statement group must be last.

## 5.10 Equality Checks

Use identity operators (`===`/`!==`) except in the cases documented below.

## 5.10.1 Exceptions Where Coercion is Desirable

Catching both `null` and `undefined` values:
```
if (someObjectOrPrimitive == null) {
  // Checking for null catches both null and undefined for objects and
  // primitives, but does not catch other falsy values like 0 or the empty
  // string.
}
```

## 5.11.2 Dynamic code evaluation

Do not use `eval` or the `Function(...string)` constructor (except for code
loaders). These features are potentially dangerous and simply do not work in CSP
environments.

## 5.11.4 Non-standard features

Do not use non-standard features. This includes old features that have been
removed (e.g., `WeakMap.clear`), new features that are not yet standardized
(e.g., the current TC39 working draft, proposals at any stage, or proposed but
not-yet-complete web standards), or proprietary features that are only
implemented in some browsers. Use only features defined in the current ECMA-262
or WHATWG standards. (Note that projects writing against specific APIs, such as
Chrome extensions or Node.js, can obviously use those APIs). Non-standard
language “extensions” (such as those provided by some external transpilers) are
forbidden.

## 5.11.5 Wrapper objects for primitive types

Never use `new` on the primitive object wrappers (`Boolean`, `Number`, `String`,
`Symbol`), nor include them in type annotations.
The wrappers may be called as functions for coercing (which is preferred over
using `+` or concatenating the empty string) or creating symbols.

## 5.11.6 Modifying builtin objects

Never modify builtin types, either by adding methods to their constructors or to
their prototypes. Avoid depending on libraries that do this. Note that the
JSCompiler’s runtime library will provide standards-compliant polyfills where
possible; nothing else may modify builtin objects.
Do not add symbols to the global object unless absolutely necessary (e.g.
required by a third-party API).

## 6.1 Rules common to all identifiers

Identifiers use only ASCII letters and digits, and, in a small number of cases
noted below, underscores and very rarely (when required by frameworks like
Angular) dollar signs.
Give as descriptive a name as possible, within reason. Do not worry about saving
horizontal space as it is far more important to make your code immediately
understandable by a new reader. Do not use abbreviations that are ambiguous or
unfamiliar to readers outside your project, and do not abbreviate by deleting
letters within a word.
**Exception**: Variables that are in scope for 10 lines or fewer, including
arguments that are *not* part of an exported API, *may* use short (e.g. single
letter) variable names.

## 6.2.2 Class names

Class, interface, record, and typedef names are written in `UpperCamelCase`.
Unexported classes are simply locals: they are not marked `@private`.

## 6.2.3 Method names

Method names are written in `lowerCamelCase`. Names for `@private` methods may
optionally end with a trailing underscore.

## 6.2.5 Constant names

Constant names use `CONSTANT_CASE`: all uppercase letters, with words separated
by underscores. There is no reason for a constant to be named with a trailing
underscore, since private static properties can be replaced by (implicitly
private) module locals.

## 6.2.8 Local variable names

Local variable names are written in `lowerCamelCase`, except for module-local
(top-level) constants, as described above. Constants in function scopes are
still named in `lowerCamelCase`. Note that `lowerCamelCase` is used
even if the variable holds a constructor.

## 7.8 Method and function comments

In methods and named functions, parameter and return types must be documented,
even in the case of same-signature `@override`s. The `this` type should be
documented when necessary. Return type may be omitted if the function has no
non-empty `return` statements.
Method, parameter, and return descriptions (but not types) may be omitted if
they are obvious from the rest of the method’s JSDoc or from its signature.

## 7.10.1 Nullability

The type system defines modifiers `!` and `?` for non-null and nullable,
respectively. These modifiers must precede the type.
1. Type annotations for primitives (`string`, `number`, `boolean`, `symbol`,
   `undefined`, `null`) and literals (`{function(...): ...}` and `{{foo:
   string...}}`) are always non-nullable by default. Use the `?` modifier to
   make it nullable, but omit the redundant `!`.
2. Reference types (generally, anything in `UpperCamelCase`, including
   `some.namespace.ReferenceType`) refer to a class, enum, record, or typedef
   defined elsewhere. Since these types may or may not be nullable, it is
   impossible to tell from the name alone whether it is nullable or not. Always
   use explicit `?` and `!` modifiers for these types to prevent ambiguity at
   use sites.

## 7.11 Visibility annotations

Visibility annotations (`@private`, `@package`, `@protected`) may be specified
in a `@fileoverview` block, or on any exported symbol or property. Do not
specify visibility for local variables, whether within a function or at the top
level of a module. `@private` names may optionally end with an underscore.

## 8.2.2 How to handle a warning

Before doing anything, make sure you understand exactly what the warning is
telling you. If you're not positive why a warning is appearing, ask for help
.
Once you understand the warning, attempt the following solutions in order:
1. **First, fix it or work around it.** Make a strong attempt to actually
   address the warning, or find another way to accomplish the task that avoids
   the situation entirely.
2. **Otherwise, determine if it's a false alarm.** If you are convinced that
   the warning is invalid and that the code is actually safe and correct, add a
   comment to convince the reader of this fact and apply the `@suppress`
   annotation.
3. **Otherwise, leave a TODO comment.** This is a **last resort**.
   If you do this, **do
   not suppress the warning.** The warning should be visible until it can be
   taken care of properly.

## 8.2.3 Suppress a warning at the narrowest reasonable scope

Warnings are suppressed at the narrowest reasonable scope, usually that of a
single local variable or very small method. Often a variable or method is
extracted for that reason alone.
Even a large number of suppressions in a class is still better than blinding the
entire class to this type of warning.

## 8.4.1 Reformatting existing code

1. It is not required to change all existing code to meet current style
   guidelines. Reformatting existing code is a trade-off between code churn and
   consistency. Style rules evolve over time and these kinds of tweaks to
   maintain compliance would create unnecessary churn. However, if significant
   changes are being made to a file it is expected that the file will be in
   Google Style.
2. Be careful not to allow opportunistic style fixes to muddle the focus of a
   CL. If you find yourself making a lot of style changes that aren’t critical
   to the central focus of a CL, promote those changes to a separate CL.

## 8.4.2 Newly added code: use Google Style

Brand new files use Google Style, regardless of the style choices of other files
in the same package.
If this reformatting is not done, then new code should be as consistent as
possible with existing code in the same file, but must not violate the style
guide.
