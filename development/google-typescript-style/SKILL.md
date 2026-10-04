---
name: google-typescript-style
description: >-
  Use when writing or reviewing TypeScript under Google's source, type-system, naming, module,
  documentation, and conformance conventions. Do not use for plain JavaScript; use
  google-javascript-style instead.
---

# Google TypeScript Style Guide

Apply this guidance to the actual project. Repository requirements and newer authoritative guidance take precedence.

## Import paths

TypeScript code *must* use paths to import other TypeScript code. Paths *may* be
relative, i.e. starting with `.` or `..`,
or rooted at the base directory, e.g.
`root/path/to/file`.
Code *should* use relative imports (`./foo`) rather than absolute imports
`path/to/foo` when referring to files within the same (logical) project as this
allows to move the project around without introducing changes in these imports.
Consider limiting the number of parent steps (`../../../`) as those can make
module and path structures hard to understand.

## Namespace versus named imports

Both namespace and named imports can be used.
Prefer named imports for symbols used frequently in a file or for symbols that
have clear names, for example Jasmine's `describe` and `it`. Named imports can
be aliased to clearer names as needed with `as`.

## Exports

Use named exports in all code:
Do not use default exports. This ensures that all imports follow a uniform
pattern.

## Mutable exports

Regardless of technical support, mutable exports can create hard to understand
and debug code, in particular with re-exports across multiple modules. One way
to paraphrase this style point is that `export let` is not allowed.
If one needs to support externally accessible and mutable bindings, they
*should* instead use explicit getter functions.
For the common pattern of conditionally exporting either of two values, first do
the conditional check, then the export. Make sure that all exports are final
after the module's body has executed.

## Import type

You may use `import type {...}` when you use the imported symbol only as a type.
Use regular imports for values:
```
import type {Foo} from './foo';
import {Bar} from './foo';

import {type Foo, Bar} from './foo';
```

## Export type

Use `export type` when re-exporting a type, e.g.:
```
export type {AnInterface} from './foo';
```

## Use modules not namespaces

TypeScript supports two methods to organize code: *namespaces* and *modules*,
but namespaces are disallowed. That
is, your code *must* refer to code in other files using imports and exports of
the form `import {foo} from 'bar';`
Your code *must not* use the `namespace Foo { ... }` construct. `namespace`s
*may* only be used when required to interface with external, third party code.
To semantically namespace your code, use separate files.
Code *must not* use `require` (as in `import x = require('...');`) for imports.
Use ES6 module syntax.

## Use const and let

Always use `const` or `let` to declare variables. Use `const` by default, unless
a variable needs to be reassigned. Never use `var`.
Variables *must not* be used before their declaration.

## Use readonly

Mark properties that are never reassigned outside of the constructor with the
`readonly` modifier (these need not be deeply immutable).

## Properties used outside of class lexical scope

Properties used from outside the lexical scope of their containing class, such
as an Angular component's properties used from a template, *must not* use
`private` visibility, as they are used outside of the lexical scope of their
containing class.
TypeScript code *must not* use `obj['foo']` to bypass the visibility of a
property.

## Getters and setters

Getters and setters, also known as accessors, for class members *may* be used.
The getter method *must* be a
[pure function](https://en.wikipedia.org/wiki/Pure_function) (i.e., result is
consistent and has no side effects: getters *must not* change observable state).
They are also useful as a means of restricting the visibility of internal or
verbose implementation details (shown below).
If an accessor is used to hide a class property, the hidden property *may* be
prefixed or suffixed with any whole word, like `internal` or `wrapped`. When
using these private properties, access the value through the accessor whenever
possible. At least one accessor for a property *must* be non-trivial: do not
define "pass-through" accessors only for the purpose of hiding a property.
Instead, make the property public (or consider making it `readonly` rather than
just defining a getter with no setter).
Getters and setters *must not* be defined using `Object.defineProperty`, since
this interferes with property renaming.

## Visibility

Restricting visibility of properties, methods, and entire types helps with
keeping code decoupled.
- Limit symbol visibility as much as possible.
- Consider converting private methods to non-exported functions within the
  same file but outside of any class, and moving private properties into a
  separate, non-exported class.
- TypeScript symbols are public by default. Never use the `public` modifier
  except when declaring non-readonly public parameter properties (in
  constructors).

## Prefer function declarations for named functions

Prefer function declarations over arrow functions or function expressions when
defining named functions.
Arrow functions *may* be used, for example, when an explicit type annotation is
required.

## Arrow function bodies

Use arrow functions with concise bodies (i.e. expressions) or block bodies as
appropriate.
Only use a concise body if the return value of the function is actually used.
The block body makes sure the return type is `void` then and prevents potential
side effects.
Tip: The `void` operator can be used to ensure an arrow function with an
expression body returns `undefined` when the result is unused.

## Prefer passing arrow functions as callbacks

Callbacks can be invoked with unexpected arguments that can pass a type check
but still result in logical errors.
Avoid passing a named callback to a higher-order function, unless you are sure
of the stability of both functions' call signatures. Beware, in particular, of
less-commonly-used optional parameters.
Instead, prefer passing an arrow-function that explicitly forwards parameters to
the named callback.

## Prefer rest and spread when appropriate

Use a *rest* parameter instead of accessing `arguments`. Never name a local
variable or parameter `arguments`, which confusingly shadows the built-in name.
Use function spread syntax instead of `Function.prototype.apply`.

## Control flow statements and blocks

Control flow statements (`if`, `else`, `for`, `do`, `while`, etc) always use
braced blocks for the containing code, even if the body contains only a single
statement. The first statement of a non-empty block must begin on its own line.
**Exception:** `if` statements fitting on one line *may* elide the block.

## Iterating containers

Prefer `for (... of someArr)` to iterate over arrays. `Array.prototype.forEach` and vanilla `for`
loops are also allowed:
```
for (const x of someArr) {
  // x is a value of someArr.
}

for (let i = 0; i < someArr.length; i++) {
  // Explicitly count if the index is needed, otherwise use the for/of form.
  const x = someArr[i];
  // ...
}
for (const [i, x] of someArr.entries()) {
  // Alternative version of the above.
}
```
`Object.prototype.hasOwnProperty` should be used in `for`-`in` loops to exclude
unwanted prototype properties. Prefer `for`-`of` with `Object.keys`,
`Object.values`, or `Object.entries` over `for`-`in` when possible.

## Only throw errors

JavaScript (and thus TypeScript) allow throwing or rejecting a Promise with
arbitrary values. However if the thrown or rejected value is not an `Error`, it
does not populate stack trace information, making debugging hard. This treatment
extends to `Promise` rejection values as `Promise.reject(obj)` is equivalent to
`throw obj;` in async functions.
Instead, only throw (subclasses of) `Error`:
```
// Throw only Errors
throw new Error('oh noes!');
// ... or subtypes of Error.
class MyError extends Error {}
throw new MyError('my oh noes!');
// For promises
new Promise((resolve) => resolve()); // No reject is OK.
new Promise((resolve, reject) => void reject(new Error('oh noes!')));
Promise.reject(new Error('oh noes!'));
```

## Catching and rethrowing

When catching errors, code *should* assume that all thrown errors are instances
of `Error`.
Exception handlers *must not* defensively handle non-`Error` types unless the
called API is conclusively known to throw non-`Error`s in violation of the above
rule. In that case, a comment should be included to specifically identify where
the non-`Error`s originate.

## Empty catch blocks

It is very rarely correct to do nothing in response to a caught exception. When
it truly is appropriate to take no action whatsoever in a catch block, the
reason this is justified is explained in a comment.

## Switch statements

All `switch` statements *must* contain a `default` statement group, even if it
contains no code. The `default` statement group must be last.
```
switch (x) {
  case Y:
    doSomethingElse();
    break;
  default:
    // nothing to do.
}
```
Within a switch block, each statement group either terminates abruptly with a
`break`, a `return` statement, or by throwing an exception. Non-empty statement
groups (`case ...`) *must not* fall through (enforced by the compiler):
```
switch (x) {
  case X:
    doSomething();
    // fall through - not allowed!
  case Y:
    // ...
}
```

## Equality checks

Always use triple equals (`===`) and not equals (`!==`). The double equality
operators cause error prone type coercions that are hard to understand and
slower to implement for JavaScript Virtual Machines. See also the
[JavaScript equality table](https://dorey.github.io/JavaScript-Equality-Table/).
**Exception:** Comparisons to the literal `null` value *may* use the `==` and
`!=` operators to cover both `null` and `undefined` values.

## Type and non-nullability assertions

Type assertions (`x as SomeType`) and non-nullability assertions (`y!`) are
unsafe. Both only silence the TypeScript compiler, but do not insert any runtime
checks to match these assertions, so they can cause your program to crash at
runtime.
Because of this, you *should not* use type and non-nullability assertions
without an obvious or explicit reason for doing so.
When you want to assert a type or non-nullability the best answer is to
explicitly write a runtime check that performs that check.
Sometimes due to some local property of your code you can be sure that the
assertion form is safe. In those situations, you *should* add clarification to
explain why you are ok with the unsafe behavior:
If the reasoning behind a type or non-nullability assertion is obvious, the
comments *may* not be necessary. For example, generated proto code is always
nullable, but perhaps it is well-known in the context of the code that certain
fields are always provided by the backend. Use your judgement.

## Type assertions and object literals

Use type annotations (`: Foo`) instead of type assertions (`as Foo`) to specify
the type of an object literal. This allows detecting refactoring bugs when the
fields of an interface change over time.

## Dynamic code evaluation

Do not use `eval` or the `Function(...string)` constructor (except for code
loaders). These features are potentially dangerous and simply do not work in
environments using strict
[Content Security Policies](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP).

## Modifying builtin objects

Never modify builtin types, either by adding methods to their constructors or to
their prototypes. Avoid depending on libraries that do
this.
Do not add symbols to the global object unless absolutely necessary (e.g.
required by a third-party API).

## Descriptive names

Names *must* be descriptive and clear to a new reader. Do not use abbreviations
that are ambiguous or unfamiliar to readers outside your project, and do not
abbreviate by deleting letters within a word.
- **Exception:** Variables that are in scope for 10 lines or fewer, including
  arguments that are *not* part of an exported API, *may* use short (e.g.
  single letter) variable names.

## Camel case

Treat abbreviations like acronyms in names as whole words, i.e. use
`loadHttpUrl`, not ~~`loadHTTPURL`~~, unless required by a platform name (e.g.
`XMLHttpRequest`).

## `_` prefix/suffix

Identifiers must not use `_` as a prefix or suffix.
This also means that `_` *must not* be used as an identifier by itself (e.g. to
indicate a parameter is unused).

## Constants

**Immutable**: `CONSTANT_CASE` indicates that a value is *intended* to not be
changed, and *may* be used for values that can technically be modified (i.e.
values that are not deeply frozen) to indicate to users that they must not be
modified.
**Global**: Only symbols declared on the module level, static fields of module
level classes, and values of module level enums, *may* use `CONST_CASE`. If a
value can be instantiated more than once over the lifetime of the program (e.g.
a local variable declared within a function, or a static field on a class nested
in a function) then it *must* use `lowerCamelCase`.

## Type inference

Code *may* rely on type inference as implemented by the TypeScript compiler for
all type expressions (variables, fields, return types, etc).
```
const x = 15;  // Type inferred.
```
Leave out type annotations for trivially inferred types: variables or parameters
initialized to a `string`, `number`, `boolean`, `RegExp` literal or `new`
expression.
Explicitly specifying types may be required to prevent generic type parameters
from being inferred as `unknown`. For example, initializing generic types with
no values (e.g. empty arrays, objects, `Map`s, or `Set`s).
```
const x = new Set<string>();
```

## Nullable/undefined type aliases

Type aliases *must not* include `|null` or `|undefined` in a union type.
Nullable aliases typically indicate that null values are being passed around
through too many layers of an application, and this clouds the source of the
original issue that resulted in `null`. They also make it unclear when specific
values on a class or interface might be absent.
Instead, code *must* only add `|null` or `|undefined` when the alias is actually
used. Code *should* deal with null values close to where they arise, using the
above techniques.

## Prefer optional over `|undefined`

In addition, TypeScript supports a special construct for optional parameters and
fields, using `?`:
Optional parameters implicitly include `|undefined` in their type. However, they
are different in that they can be left out when constructing a value or calling
a method. For example, `{sugarCubes: 1}` is a valid `CoffeeOrder` because `milk`
is optional.
Use optional fields (on interfaces or classes) and parameters rather than a
`|undefined` type.
For classes preferably avoid this pattern altogether and initialize as many
fields as possible.

## Use structural types

TypeScript's type system is structural, not nominal. That is, a value matches a
type if it has at least all the properties the type requires and the properties'
types match, recursively.
When providing a structural-based implementation, explicitly include the type at
the declaration of the symbol (this allows more precise type checking and error
reporting).
Use interfaces to define structural types, not classes

## Prefer interfaces over type literal aliases

TypeScript supports
[type aliases](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#type-aliases)
for naming a type expression. This can be used to name primitives, unions,
tuples, and any other types.
However, when declaring types for objects, use interfaces instead of a type
alias for the object literal expression.

## Mapped and conditional types

TypeScript's
[mapped types](https://www.typescriptlang.org/docs/handbook/2/mapped-types.html)
and
[conditional types](https://www.typescriptlang.org/docs/handbook/2/conditional-types.html)
allow specifying new types based on other types. TypeScript's standard library
includes several type operators based on these (`Record`, `Partial`, `Readonly`
etc).
These type system features allow succinctly specifying types and constructing
powerful yet type safe abstractions. They come with a number of drawbacks
though:
The style recommendation is:
- Always use the simplest type construct that can possibly express your code.
- A little bit of repetition or verbosity is often much cheaper than the long
  term cost of complex type expressions.
- Mapped & conditional types may be used, subject to these considerations.

## `any` Type

TypeScript's `any` type is a super and subtype of all other types, and allows
dereferencing all properties. As such, `any` is dangerous - it can mask severe
programming errors, and its use undermines the value of having static types in
the first place.
**Consider *not* to use `any`.** In circumstances where you want to use `any`,
consider one of:
- Provide a more specific type
- Use `unknown`
- Suppress the lint warning and document why

## Using `unknown` over `any`

The `any` type allows assignment into any other type and dereferencing any
property off it. Often this behaviour is not necessary or desirable, and code
just needs to express that a type is unknown. Use the built-in type `unknown` in
that situation — it expresses the concept and is much safer as it does not allow
dereferencing arbitrary properties.
To safely use `unknown` values, narrow the type using a
[type guard](https://www.typescriptlang.org/docs/handbook/advanced-types.html#type-guards-and-differentiating-types)

## `{}` Type

The `{}` type, also known as an *empty interface* type, represents a interface
with no properties. An empty interface type has no specified properties and
therefore any non-nullish value is assignable to it.
Google3 code **should not** use `{}` for most use cases. `{}` represents any
non-nullish primitive or object type, which is rarely appropriate. Prefer one of
the following more-descriptive types:
- `unknown` can hold any value, including `null` or `undefined`, and is
  generally more appropriate for opaque values.
- `Record<string, T>` is better for dictionary-like objects, and provides
  better type safety by being explicit about the type `T` of contained values
  (which may itself be `unknown`).
- `object` excludes primitives as well, leaving only non-nullish functions and
  objects, but without any other assumptions about what properties may be
  available.

## Wrapper types

There are a few types related to JavaScript primitives that *should not* ever be
used:
- `String`, `Boolean`, and `Number` have slightly different meaning from the
  corresponding primitive types `string`, `boolean`, and `number`. Always use
  the lowercase version.
- `Object` has similarities to both `{}` and `object`, but is slightly looser.
  Use `{}` for a type that include everything except `null` and `undefined`,
  or lowercase `object` to further exclude the other primitive types (the
  three mentioned above, plus `symbol` and `bigint`).
Further, never invoke the wrapper types as constructors (with `new`).

## @ts-ignore

Do not use `@ts-ignore` nor the variants `@ts-expect-error` or `@ts-nocheck`.
You may use `@ts-expect-error` in unit tests, though you generally *should not*.
`@ts-expect-error` suppresses all errors. It's easy to accidentally over-match
and suppress more serious errors. Consider one of:
- When testing APIs that need to deal with unchecked values at runtime, add
  casts to the expected type or to `any` and add an explanatory comment. This
  limits error suppression to a single expression.
- Suppress the lint warning and document why, similar to
  suppressing `any` lint warnings.

## Conformance

These rules are commonly used to enforce critical restrictions (such as defining
globals, which could break the codebase) and security patterns (such as using
`eval` or assigning to `innerHTML`), or more loosely to improve code quality.
Google-style TypeScript must abide by any applicable global or framework-local
conformance rules.

## JSDoc versus comments

There are two types of comments, JSDoc (`/** ... */`) and non-JSDoc ordinary
comments (`// ...` or `/* ... */`).
- Use `/** JSDoc */` comments for documentation, i.e. comments a user of the
  code should read.
- Use `// line comments` for implementation comments, i.e. comments that only
  concern the implementation of the code itself.

## Document all top-level exports of modules

Use `/** JSDoc */` comments to communicate information to the users of your
code. Avoid merely restating the property or parameter name. You *should* also
document all properties and methods (exported/public or not) whose purpose is
not immediately obvious from their name, as judged by your reviewer.
**Exception:** Symbols that are only exported to be consumed by tooling, such as
@NgModule classes, do not require comments.
