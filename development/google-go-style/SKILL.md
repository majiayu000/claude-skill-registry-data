---
name: google-go-style
description: >-
  Use when writing or reviewing Go code under Google's style decisions and best practices,
  including naming, APIs, errors, documentation, tests, and maintainability. Do not use as a
  replacement for the Go language specification.
---

# Google Go Style Guide

Apply this guidance to the actual project. Repository requirements and newer authoritative guidance take precedence.

## Go Style Guide

### Style principles

There are a few overarching principles that summarize how to think about writing
readable Go code. The following are attributes of readable code, in order of
importance:
1.  **Clarity**: The code's purpose and rationale is clear to the reader.
1.  **Simplicity**: The code accomplishes its goal in the simplest way
    possible.
1.  **Concision**: The code has a high signal-to-noise ratio.
1.  **Maintainability**: The code is written such that it can be easily
    maintained.
1.  **Consistency**: The code is consistent with the broader Google codebase.

### Simplicity

Your Go code should be simple for those using, reading, and maintaining it.
Go code should be written in the simplest way that accomplishes its goals, both
in terms of behavior and performance. Within the Google Go codebase, simple
code:
*   Is easy to read from top to bottom
*   Does not assume that you already know what it is doing
*   Does not assume that you can memorize all of the preceding code
*   Does not have unnecessary levels of abstraction
*   Does not have names that call attention to something mundane
*   Makes the propagation of values and decisions clear to the reader
*   Has comments that explain why, not what, the code is doing to avoid future
    deviation
*   Has documentation that stands on its own
*   Has useful errors and useful test failures
*   May often be mutually exclusive with "clever" code

### Least mechanism

Where there are several ways to express the same idea, prefer the one that uses
the most standard tools. Sophisticated machinery often exists, but should not be
employed without reason. It is easy to add complexity to code as needed, whereas
it is much harder to remove existing complexity after it has been found to be
unnecessary.
1.  Aim to use a core language construct (for example a channel, slice, map,
    loop, or struct) when sufficient for your use case.
2.  If there isn't one, look for a tool within the standard library (like an
    HTTP client or a template engine).
3.  Finally, consider whether there is a core library in the Google codebase
    that is sufficient before introducing a new dependency or creating your own.

### Maintainability

Code is edited many more times than it is written. Readable code not only makes
sense to a reader who is trying to understand how it works, but also to the
programmer who needs to change it. Clarity is key.
*   Is easy for a future programmer to modify correctly
*   Has APIs that are structured so that they can grow gracefully
*   Is clear about the assumptions that it makes and chooses abstractions that
    map to the structure of the problem, not to the structure of the code
*   Avoids unnecessary coupling and doesn't include features that are not used
*   Has a comprehensive test suite to ensure promised behaviors are maintained
    and important logic is correct, and the tests provide clear, actionable
    diagnostics in case of failure
Maintainable code minimizes its dependencies (both implicit and explicit).
Depending on fewer packages means fewer lines of code that can affect behavior.
Avoiding dependencies on internal or undocumented behavior makes code less
likely to impose a maintenance burden when those behaviors change in the future.

### Formatting

All Go source files must conform to the format outputted by the `gofmt` tool.
This format is enforced by a presubmit check in the Google codebase.
[Generated code](https://docs.bazel.build/versions/main/be/general.html#genrule) should generally also be formatted (e.g., by using
[`format.Source`](https://pkg.go.dev/go/format#Source)), as it is also browsable in Code Search.

### MixedCaps

Go source code uses `MixedCaps` or `mixedCaps` (camel case) rather than
underscores (snake case) when writing multi-word names.
This applies even when it breaks conventions in other languages. For example, a
constant is `MaxLength` (not `MAX_LENGTH`) if exported and `maxLength` (not
`max_length`) if unexported.

### Naming

Naming is more art than science. In Go, names tend to be somewhat shorter than
in many other languages, but the same [general guidelines](https://testing.googleblog.com/2017/10/code-health-identifiernamingpostforworl.html) apply. Names should:
*   Not feel repetitive when they are used
*   Take the context into consideration
*   Not repeat concepts that are already clear


## Go Style Decisions

### Package names

In Go, package names must be concise and use only lowercase letters and numbers
(e.g., [`k8s`](https://pkg.go.dev/k8s.io/client-go/kubernetes), [`oauth2`](https://pkg.go.dev/golang.org/x/oauth2)). Multi-word package names should remain unbroken and
in all lowercase (e.g., [`tabwriter`](https://pkg.go.dev/text/tabwriter) instead of `tabWriter`, `TabWriter`, or
`tab_writer`).

### Receiver names

[Receiver](https://golang.org/ref/spec#Method_declarations) variable names must be:
*   Short (usually one or two letters in length)
*   Abbreviations for the type itself
*   Applied consistently to every receiver for that type
*   Not an underscore; omit the name if it is unused

### Constant names

Constant names must use MixedCaps like all other names in Go. ([Exported](https://tour.golang.org/basics/3)
constants start with uppercase, while unexported constants start with
lowercase.) This applies even when it breaks conventions in other languages.
Constant names should not be a derivative of their values and should instead
explain what the value denotes.

### Initialisms

Words in names that are initialisms or acronyms (e.g., `URL` and `NATO`) should
have the same case. `URL` should appear as `URL` or `url` (as in `urlPony`, or
`URLPony`), never as `Url`. As a general rule, identifiers (e.g., `ID` and `DB`)
should also be capitalized similar to their usage in English prose.

### Getters

Function and method names should not use a `Get` or `get` prefix, unless the
underlying concept uses the word "get" (e.g. an HTTP GET). Prefer starting the
name with the noun directly, for example use `Counts` over `GetCounts`.
If the function involves performing a complex computation or executing a remote
call, a different word like `Compute` or `Fetch` can be used in place of `Get`,
to make it clear to a reader that the function call may take time and could
block or fail.

### Doc comments

All top-level exported names must have doc comments, as should unexported type
or function declarations with unobvious behavior or meaning. These comments
should be full sentences that begin with the name of the object being
described. An article ("a", "an", "the") can precede the name to make it read
more naturally.
Doc comments appear in [Godoc](https://pkg.go.dev/) and are surfaced by IDEs,
and therefore should be written for anyone using the package.

### Import grouping

Imports should be organized into the following groups, in order:
1.  Standard library packages
1.  Other (project and vendored) packages
1.  Protocol Buffer imports (e.g., `fpb "path/to/foo_go_proto"`)
1.  Import for [side-effects](https://go.dev/doc/effective_go#blank_import)
    (e.g., `_ "path/to/package"`)

### Import "blank" (`import _`)

Packages that are imported only for their side effects (using the syntax `import
_ "package"`) may only be imported in a main package, or in tests that require
them.
Avoid blank imports in library packages, even if the library indirectly depends
on them. Constraining side-effect imports to the main package helps control
dependencies, and makes it possible to write tests that rely on a different
import without conflict or wasted build costs.
**Tip:** If you create a library package that indirectly depends on a
side-effect import in production, document the intended usage.

### Import "dot" (`import .`)

Do **not** use this feature in the Google codebase; it makes it harder to tell
where the functionality is coming from.

### Returning errors

Use `error` to signal that a function can fail. By convention, `error` is the
last result parameter.
Returning a `nil` error is the idiomatic way to signal a successful operation
that could otherwise fail. If a function returns an error, callers must treat
all non-error return values as unspecified unless explicitly documented
otherwise. Commonly, the non-error return values are their zero values, but this
cannot be assumed.
Exported functions that return errors should return them using the `error` type.
Concrete error types are susceptible to subtle bugs: a concrete `nil` pointer
can get wrapped into an interface and thus become a non-nil value (see the
[Go FAQ entry on the topic](https://golang.org/doc/faq#nil_error)).

### Error strings

Error strings should not be capitalized (unless beginning with an exported name,
a proper noun or an acronym) and should not end with punctuation. This is
because error strings usually appear within other context before being printed
to the user.
On the other hand, the style for the full displayed message (logging, test
failure, API response, or other UI) depends, but should typically be
capitalized.

### Handle errors

Code that encounters an error should make a deliberate choice about how to
handle it. It is not usually appropriate to discard errors using `_` variables.
If a function returns an error, do one of the following:
*   Handle and address the error immediately.
*   Return the error to the caller.
*   In exceptional situations, call [`log.Fatal`](https://pkg.go.dev/github.com/golang/glog#Fatal) or (if absolutely necessary)
    `panic`.
In the rare circumstance where it is appropriate to ignore or discard an error
(for example a call to [`(*bytes.Buffer).Write`](https://pkg.go.dev/bytes#Buffer.Write) that is documented to never
fail), an accompanying comment should explain why this is safe.

### In-band errors

In C and similar languages, it is common for functions to return values like -1,
null, or the empty string to signal errors or missing results. This is known as
in-band error handling.
Go's support for multiple return values provides a better solution (see the
[Effective Go section on multiple returns](http://golang.org/doc/effective_go.html#multiple-returns)). Instead of requiring clients to
check for an in-band error value, a function should return an additional value
to indicate whether its other return values are valid. This return value may be
an error or a boolean when no explanation is needed, and should be the final
return value.
Some standard library functions, like those in package `strings`, return in-band
error values. This greatly simplifies string-manipulation code at the cost of
requiring more diligence from the programmer. In general, Go code in the Google
codebase should return additional values for errors.

### Indent error flow

Handle errors before proceeding with the rest of your code. This improves the
readability of the code by enabling the reader to find the normal path quickly.
This same logic applies to any block which tests a condition then ends in a
terminal condition (e.g., `return`, `panic`, `log.Fatal`).
Code that runs if the terminal condition is not met should appear after the `if`
block, and should not be indented in an `else` clause.

### Don't panic

Do not use `panic` for normal error handling. Instead, use `error` and multiple
return values. See the [Effective Go section on errors](http://golang.org/doc/effective_go.html#errors).

### Goroutine lifetimes

When you spawn goroutines, make it clear when or whether they exit.
Concurrent code should be written such that the goroutine lifetimes are obvious.
Typically this will mean keeping synchronization-related code constrained within
the scope of a function and factoring out the logic into
synchronous functions. If the concurrency is still not obvious, it is
important to document when and why the goroutines exit.
There are other variants of the above that use raw signal channels like `chan
struct{}`, synchronized variables, [condition variables](https://drive.google.com/file/d/1nPdvhB0PutEJzdCq5ms6UI58dp50fcAN/view), and
more. The important part is that the goroutine's end is evident for subsequent
maintainers.

### Interfaces

Avoid creating interfaces until a real need exists. Focus on
the required behavior rather than just abstract named patterns like "service" or
"repository" and the like.
Design interfaces to be small for easier implementation and composition
([GoTip #78: Minimal Viable Interfaces](https://google.github.io/styleguide/go/index.html#gotip)). Document interfaces appropriately
including their contract, edge cases, and expected errors. Keep interface types
unexported if they are only used internally within a package.
The consumer of the interface should define it (not the package implementing the
interface), ensuring it includes only the methods they actually use. The
producer package may export the interface if the interface is the product (a
common protocol) to prevent interface redefinition bloat.
There is an adage: Functions should take interfaces as arguments but return
concrete types ([GoTip #49: Accept Interfaces, Return Concrete Types](https://google.github.io/styleguide/go/index.html#gotip)).
Returning concrete types allows the caller to have access to every public method
and field of that specific implementation, not just the subset of methods
defined in a pre-chosen interface. The caller can still pass that concrete
result into any other function that expects an interface. Sometimes returning an
interface is acceptable for encapsulation (e.g., `error` interface), and certain
constructs like command, chaining, factory, and
[strategy](https://en.wikipedia.org/wiki/Strategy_pattern) patterns.

### Pass values

Do not pass pointers as function arguments just to save a few bytes. If a
function reads its argument `x` only as `*x` throughout, then the argument
shouldn't be a pointer. Common instances of this include passing a pointer to a
string (`*string`) or a pointer to an interface value (`*io.Reader`). In both
cases, the value itself is a fixed size and can be passed directly.
This advice does not apply to large structs, or even small structs that may
increase in size. In particular, protocol buffer messages should generally be
handled by pointer rather than by value. The pointer type satisfies the
`proto.Message` interface (accepted by `proto.Marshal`, `protocmp.Transform`,
etc.), and protocol buffer messages can be quite large and often grow larger
over time.

### Receiver type

**Correctness wins over speed or simplicity.** There are cases where you must
use a pointer value. In other cases, pick pointers for large types or as
future-proofing if you don't have a good sense of how the code will grow, and
use values for simple [plain old data](https://en.wikipedia.org/wiki/Passive_data_structure).
*   If the method needs to mutate the receiver, the receiver must be a pointer.
*   If the receiver is a struct containing fields that
    cannot safely be copied, use a pointer receiver. Common examples
    are [`sync.Mutex`](https://pkg.go.dev/sync#Mutex) and other synchronization types.
*   If the receiver is a map, function, or channel, use a value rather than a
    pointer.
*   If the receiver is a "small" array or struct that is naturally a value type
    with no mutable fields and no pointers, a value receiver is usually the
    right choice.
*   When in doubt, use a pointer receiver.
As a general guideline, prefer to make the methods for a type either all pointer
methods or all value methods.

### Synchronous functions

Synchronous functions return their results directly and finish any callbacks or
channel operations before returning. Prefer synchronous functions over
asynchronous functions.
Synchronous functions keep goroutines localized within a call. This helps to
reason about their lifetimes, and avoid leaks and data races. Synchronous
functions are also easier to test, since the caller can pass an input and check
the output without the need for polling or synchronization.
If necessary, the caller can add concurrency by calling the function in a
separate goroutine. However, it is quite difficult (sometimes impossible) to
remove unnecessary concurrency at the caller side.

### Flags

Flags must only be defined in `package main` or equivalent.
General-purpose packages should be configured using Go APIs, not by punching
through to the command-line interface; don't let importing a library export new
flags as a side effect. That is, prefer explicit function arguments or struct
field assignment or much less frequently and under the strictest of scrutiny
exported global variables. In the extremely rare case that it is necessary to
break this rule, the flag name must clearly indicate the package that it
configures.

### Contexts

When passed to a function or method, [`context.Context`](https://pkg.go.dev/context) is always the first
parameter.
Do not add a context member to a struct type. Instead, add a context parameter
to each method on the type that needs to pass it along. The one exception is for
methods whose signature must match an interface in the standard library or in a
third party library outside Google's control. Such cases are very rare, and
should be discussed with the Google Go style mailing list before implementation
and readability review.
Since contexts are immutable, it is fine to pass the same context to multiple
calls that share the same deadline, cancellation signal, credentials, parent
trace, and so on.

### Use package `testing`

The Go standard library provides the [`testing` package](https://pkg.go.dev/testing). This is the only
testing framework permitted for Go code in the Google codebase. In particular,
assertion libraries and third-party testing frameworks are not
allowed.

### Identify the function

In most tests, failure messages should include the name of the function that
failed, even though it seems obvious from the name of the test function.
Specifically, your failure message should be `YourFunc(%v) = %v, want %v`
instead of just `got %v, want %v`.

### Got before want

Test outputs should include the actual value that the function returned before
printing the value that was expected. A standard format for printing test
outputs is `YourFunc(%v) = %v, want %v`. Where you would write "actual" and
"expected", prefer using the words "got" and "want", respectively.

### Compare stable results

Avoid comparing results that may depend on output stability of a package that
you do not own. Instead, the test should compare on semantically relevant
information that is stable and resistant to changes in dependencies. For
functionality that returns a formatted string or serialized bytes, it is
generally not safe to assume that the output is stable.

### Table-driven tests

Use table-driven tests when many different test cases can be tested using
similar testing logic.

### Test helpers

A test helper is a function that performs a setup or cleanup task. All failures
that occur in test helpers are expected to be failures of the environment (not
from the code under test) — for example when a test database cannot be started
because there are no more free ports on this machine.
If you pass a `*testing.T`, call [`t.Helper`](https://pkg.go.dev/testing#T.Helper) to attribute failures in the test
helper to the line where the helper is called. This parameter should come after
a context parameter, if present, and before any remaining
parameters.


## Go Style Best Practices

### Util packages

Go packages have a name specified on the `package` declaration, separate from
the import path. The package name matters more for readability than the path.
Go package names should be
related to what the package provides. Naming a
package just `util`, `helper`, `common` or similar is usually a poor choice (it
can be used as *part* of the name though). Uninformative names make the code
harder to read, and if used too broadly they are liable to cause needless
import conflicts.
Instead, consider what the callsite will look like.

### Adding information to errors

When adding information to errors, avoid redundant information that the
underlying error already provides. The `os` package, for instance, already
includes path information in its errors.
Here, "launch codes unavailable" adds specific meaning to the `os.Open` error
that's relevant to the current function's context, without duplicating the
underlying file path information.
Don't add an annotation if its sole purpose is to indicate a failure without
adding new information. The presence of an error sufficiently conveys the
failure to the caller.
1.  **`%w` (wrap) for programmatic inspection and error chaining**
The `%w` verb is specifically designed for error wrapping. It creates a new
error that provides an `Unwrap()` method, allowing callers to
programmatically inspect the error chain using `errors.Is` and `errors.As`.
Examples to use `%w`:
    *   When you explicitly document and test the underlying errors you expose:
        If your package's API guarantees that certain underlying errors can be
        unwrapped and checked by callers (e.g., "this function might return
        `ErrInvalidConfig` wrapped within a more general error"), then `%w` is
        appropriate. This forms part of your package's contract.

### Global state

Libraries should not force their clients to use APIs that rely on
[global state](https://en.wikipedia.org/wiki/Global_variable). They are advised
not to expose APIs or export
[package level](https://go.dev/ref/spec#TopLevelDecl) variables that control
behavior for all clients as parts of their API. The rest of the section uses
"global" and "package level state" synonymously.
Instead, if your functionality maintains state, allow your clients to create and
use instance values.
There are different approaches to migrating existing code to support dependency
passing. The main one you will use is passing dependencies as parameters to
constructors, functions, methods, or struct fields on the call chain.
Global state has cascading effects on the
health of the Google codebase. Global state should
be approached with **extreme scrutiny**.
