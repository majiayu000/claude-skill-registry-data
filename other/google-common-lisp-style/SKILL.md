---
name: google-common-lisp-style
description: >-
  Use when writing or reviewing Common Lisp under Google's naming, formatting, documentation,
  macro, error-handling, and language-usage conventions. Do not use for other Lisp dialects
  without checking compatibility.
---

# Google Common Lisp Style Guide

Apply this guidance to the actual project. Repository requirements and newer authoritative guidance take precedence.

## Must, Should, May, or Not

Each guideline's level of importance is indicated
by use of the following keywords and phrases, adapted from
[RFC 2119](https://www.ietf.org/rfc/rfc2119.txt).
|  |  |
| --- | --- |
| MUST | This word, or the terms "REQUIRED" or "SHALL", means that the guideline is an absolute requirement. You must ask permission to violate a MUST. |
| MUST NOT | This phrase, or the phrase "SHALL NOT", means that the guideline is an absolute prohibition. You must ask permission to violate a MUST NOT. |
| SHOULD | This word, or the adjective "RECOMMENDED", means that there may exist valid reasons in particular circumstances to ignore the demands of the guideline, but the full implications must be understood and carefully weighed before choosing a different course. You must ask forgiveness for violating a SHOULD. |
| SHOULD NOT | This phrase, or the phrase "NOT RECOMMENDED", means that there may exist valid reasons in particular circumstances to ignore the prohibitions of this guideline, but the full implications should be understood and carefully weighed before choosing a different course. You must ask forgiveness for violating a SHOULD NOT. |
| MAY | This word, or the adjective "OPTIONAL", means that an item is truly optional. |

## Priorities

When making decisions about how to write a given piece of
code, aim for the following -ilities in this priority order:
- Usability by the customer
- Debuggability/Testability
- Readability/Comprehensibility
- Extensibility/Modifiability
- Efficiency (of the Lisp code at runtime)
Given two options where one is more complex than the other,
pick the simpler option and revisit the decision only if
profiling shows it to be a performance bottleneck.
However, avoid premature optimization.
Don't add complexity to speed up something that runs rarely,
since in the long run, it matters less whether such code is fast.

## Using Libraries

Often, the smallest hammer is to use an existing library.
Or one that doesn't exist yet.
In such cases, you are encouraged to use or develop such a library,
but you must take appropriate precautions.

## Spelling and Abbreviations

You must use correct spelling in your comments,
and most importantly in your identifiers.
You must use only common and domain-specific abbreviations, and
must be consistent with these abbreviations. You may abbreviate
lexical variables of limited scope in order to avoid overly-long
symbol names.

## Line length

You should format source code so that no line is longer than 100 characters.

## Indentation

Indent your code the way a properly configured GNU Emacs does.
Maintain a consistent indentation style throughout a project.
Indent carefully to make the code easier to understand.

## Vertical white space

Vertical white space: one blank line between top-level forms.
You should strive to keep top-level forms,
including comments but excluding the documentation string, of
appropriate length; preferably short. Forms extending beyond a
single page should be rare and their use should be justified.
This applies to each of the forms in an `eval-when`,
rather than to the `eval-when` itself.
Additionally, `defpackage` forms may be longer,
since they may include long lists of symbols.

## Horizontal white space

Horizontal white space: none around parentheses. No tabs.
You must not include extra horizontal whitespace
before or after parentheses or around symbols.
You must not place right parentheses by themselves on a line.
A set of consecutive trailing parentheses must appear on the same line.
You should use only one space between forms.
You should not use spaces to vertically align forms
in the middle of consecutive lines.
An exception is made when the code possesses
an important yet otherwise not visible symmetry
that you want to emphasize.
You must set your editor to
avoid inserting tab characters in the files you edit.
Tabs cause confusion when editors disagree
on how many spaces they represent.
In Emacs, do `(setq-default indent-tabs-mode nil)`.

## Document everything

You should use document strings on all visible functions
to explain how to use your code.
Supply a documentation string when defining
top-level functions, types, classes, variables and macros.
Generally, add a documentation string wherever the language allows.
For functions, the docstring should describe the function's contract:
what the function does,
what the arguments mean,
what values are returned,
what conditions the function can signal.
It should be expressed at the appropriate level of abstraction,
explaining the intended meaning rather than, say, just the syntax.
In documentation strings, capitalize the names of Lisp symbols,
such as function arguments.
For example, "The value of LENGTH should be an integer."

## Comment semicolons

You must use the appropriate number of semicolons to introduce comments.
You must comment anything complicated
so that the next developer can understand what's going on.
(Again, the "hit by a truck" principle.)
- File headers and important comments
  that apply to large sections of code in a source file
  should begin with four semicolons.
- You should use three semicolons
  to begin comments that apply to just
  one top-level form or small group of top-level forms.
- Inside a top-level form, you should use two semicolons
  to begin a comment if it appears between lines.
- You should use one semicolon if it is a parenthetical remark
  and occurs at the end of a line.
  You should use spaces to separate the comment
  from the code it refers to so the comment stands out.
  You should try to vertically align
  consecutive related end-of-line comments.
You should include a space between the semicolon and the text of the comment.

## Symbol guidelines

You should use lower case.
You should follow the rules for Spelling and Abbreviations
You should follow punctuation conventions.
Use lower case for all symbols.
Consistently using lower case makes searching for symbol names easier
and is more readable.
Place hyphens between all the words in a symbol.
If you can't easily say an identifier out loud,
it is probably badly named.
There are conventions in Common Lisp
for the use of punctuation in symbols.
You should not use punctuation in symbols outside these conventions.
Unless the scope of a variable is very small,
do not use overly short names like
`i` and `zq`.

## Denote intent, not content

Name your variables according to their intent,
not their content.
You should name a variable according
to the high-level concept that it represents,
not according to the low-level implementation details
of how the concept is represented.
Thus, you should avoid embedding
data structure or aggregate type names,
such as `list`, `array`, or
`hash-table` inside variable names,
unless you're writing a generic algorithm that applies to
arbitrary lists, arrays, hash-tables, etc.
In that case it's perfectly OK to name a variable
`list` or `array`.

## Global variables and constants

Name globals according to convention.
The names of global constants should start and end
with plus characters.
Global variable names should start and end with asterisks
(also known in this context as earmuffs).

## Predicate names

Names of predicate functions and variables end with a `"P"`.
You should name boolean-valued functions and variables with a
trailing `"P"` or `"-P"`,
to indicate they are predicates.
Generally, you should use
`"P"` when the rest of the function name is one word
and `"-P"` when it is more than one word.

## Omit library prefixes

You should not include a library or package name
as a prefix within the name of symbols.

## Packages

Use packages appropriately.
The internal symbols of a package
should never be referred to from other packages.
That is, you should never have to use
the double-colon `::` construct.
(e.g. `QUAKE::HIDDEN-FUNCTION`).
If you need to use double-colons to write real production code,
something is wrong and needs to be fixed.
As an exception,
unit tests may use the internals of the package being tested.
So when you refactor, watch out for
internals used by the package's unit tests.
The `::` construct is also useful for very temporary hacks,
and at the REPL.
But if the symbol really is part of
the externally-visible definition of the package,
export it.
If you add a new package, it should always be of the second type,
unless you have a special reason and get permission.
Usually a package is designed to be one or the other,
by virtue of the names of the functions.
For example, if you have an abstraction called `FIFO`,
and it were in a package of the first type
you'd have functions named things like
`FIFO-ADD-TO` and `FIFO-CLEAR-ALL`.
If you used a package of the second type,
you'd have names like `ADD-TO` and `CLEAR-ALL`,
because the callers would be saying
`FIFO:ADD-TO` and `FIFO:CLEAR-ALL`.
(`FIFO:FIFO-CLEAR-ALL` is redundant and ugly.)
Your package must not shadow (and thus effectively redefine)
symbols that are part of the Common Lisp language.
There are certain exceptions,
but they should be very well-justified and extremely rare:
- If you are explicitly replacing a Common Lisp symbol
  by a safer or more featureful version.
- If you are defining a package not meant to be "used",
  and have a good reason to export a symbol
  that clashes with Common Lisp,
  such as `log:error` and `log:warn`
  and so on.

## Mostly Functional Style

You should avoid side-effects when they are not necessary.
Avoid modifying local variables, try rebinding instead.
Avoid creating objects and the SETFing their slots.
It's better to set the slots during initialization.
Make classes as immutable as possible, that is, avoid giving slots
setter functions if at all possible.

## Recursion

You should favor iteration over recursion.
For compatibility with all compilers and optimization settings,
and to avoid stack overflow when debugging,
you should prefer iteration or the built in mapping functions
to relying on proper tail calls.
If you do rely on proper tail calls,
you must prominently document the fact,
and take appropriate measures to ensure an appropriate compiler is used
with appropriate optimization settings.
For fully portable code, you may have to use trampolines instead.

## Special variables

Use special variables sparingly.

## Assignment

Be consistent in assignment forms.

## Assertions and Conditions

You must make proper usage of assertions and conditions.
- `ASSERT` should be used ONLY to detect internal bugs.
  Code should `ASSERT` invariants whose failure indicates
  that the software is itself broken.
  Incorrect input should be handled properly at runtime,
  and must not cause an assertion violation.
  The audience for an `ASSERT` failure is a developer.
  Do not use the data-form and argument-form in `ASSERT`
  to specify a condition to signal.
  It's fine to use them to print out a message for debugging purposes
  (and since it's only for debugging, there's no issue of
  internationalization).
- `CHECK-TYPE`,
  `ETYPECASE` are also forms of assertion.
  When one of these fails, that's a detected bug.
  You should prefer to use `CHECK-TYPE`
  over (DECLARE (TYPE ...))
  for the inputs of functions.
- Your code should use assertions and type checks liberally.
  The sooner a bug is discovered, the better!
  Only code in the critical path for performance
  and internal helpers should eschew
  explicit assertions and type checks.
- Invalid input, such as files that are read
  but do not conform to the expected format,
  should not be treated as assertion violations.
  Always check to make sure that input is valid,
  and take appropriate action if it is not,
  such as signalling a real error.
- `ERROR` should be used
  to detect problems with user data, requests, permissions, etc.,
  or to report "unusual outcomes" to the caller.
- `ERROR` should always be called
  with an explicit condition type;
  it should never simply be called with a string.
  This enables internationalization.
- Functions that report unusual outcomes
  by signaling a condition should say so explicitly in their contracts
  (their textual descriptions, in documentation and docstrings etc.).
  When a function signals a condition
  that is not specified by its contract, that's a bug.
  The contract should specify the condition class(es) clearly.
  The function may then signal any condition
  that is a type-of any of those conditions.
  That is, signaling instances of subclasses
  of the documented condition classes is fine.
- Complex bug-checks may need to use `ERROR`
  instead of `ASSERT`.
- When writing a server, you must not call `WARN`.
  Instead, you should use the appropriate logging framework.
- Code must not call `SIGNAL`.
  Instead, use `ERROR` or `ASSERT`.
- Code should not use `THROW` and `CATCH`;
  instead use the `restart` facility.
- Code should not generically handle all conditions,
  e.g. type `T`, or use `IGNORE-ERRORS`.
  Instead, let unknown conditions propagate to
  the standard ultimate handler for processing.
- There are a few places where handling all conditions is appropriate,
  but they are rare.
  The problem is that handling all conditions can mask program bugs.
  If you *do* need to handle "all conditions",
  you MUST handle only `ERROR`, *not* `T`
  and not `SERIOUS-CONDITION`.
  (This is notably because CCL's process shutdown
  depends on being able to signal `process-reset`
  and have it handled by CCL's handler,
  so we must not interpose our own handler.)
- `(error (make-condition 'foo-error ...))`
  is equivalent to `(error 'foo-error ...)` —
  code must use the shorter form.
- Code should not signal conditions from inside the cleanup form of
  `UNWIND-PROTECT`
  (unless they are always handled inside the cleanup form),
  or otherwise do non-local exits from cleanup handlers
  outside of the handler e.g. `INVOKE-RESTART`.
- Do not clean up by resignaling.
  If you do that, and the condition is not handled,
  the stack trace will halt at the point of the resignal,
  hiding the rest.
  And the rest is the part we really care about!
  **Bad code:**
  ```
              ;; Bad
              (handler-case
                (catch 'ticket-at
                  (etd-process-blocks))
                (error (c)
                  (reset-parser-values)
                    (error c)))
  ```
  ```
              ;; Better
              (unwind-protect
                (catch 'ticket-at
                  (etd-process-blocks))
                (reset-parser-values))
  ```

## Type Checking

If you know the type of something, you should make it explicit
in order to enable compile-time and run-time sanity-checking.

## CLOS

Use CLOS appropriately.
When a generic function is intended to be called from other
modules (other parts of the code), there should be an
explicit `DEFGENERIC` form,
with a `:DOCUMENTATION` string
explaining the generic contract of the function
(as opposed to its behavior for some specific class).
It's generally good to do explicit `DEFGENERIC` forms,
but for module entry points it is mandatory.
When the argument list of a generic function includes
`&KEY`,
the `DEFGENERIC` should always explicitly list
all of the keyword arguments that are acceptable,
and explain what they mean.
(Common Lisp does not require this, but it is good form,
and it may avoid spurious warnings on SBCL.)
You should avoid `SLOT-VALUE` and `WITH-SLOTS`,
unless you absolutely intend to circumvent
any sort of method combination that might be in effect for the slot.
Rare exceptions include `INITIALIZE-INSTANCE`
and `PRINT-OBJECT` methods and
accessing normally hidden slots in the low-level implementation of
methods that provide user-visible abstractions.
Otherwise, you should use accessors,
`WITH-ACCESSORS`
You must not use generic functions where there is no notional protocol.
To put it more concretely,
if you have more than one generic function that specializes its Nth argument,
the specializing classes should all be descendants of a single class.
Generic functions must not be used for "overloading",
i.e. simply to use the same name for two entirely unrelated types.

## Macros

Use macros when appropriate, which is often.
Define macros when appropriate, which is seldom.
You must never use a macro where a function will do.
That is, if the semantics of what you are writing
conforms to the semantics of a function,
then you must write it as a function rather than a macro.
If a macro call contains a form,
and the macro expansion includes more than one copy of that form,
the form can be evaluated more than once,
and code it contains macro-expanded and compiled more than once.
If someone uses the macro and calls it
with a form that has side effects or that takes a long time to compute,
the behavior will be undesirable
(unless you're intentionally writing
a control structure such as a loop).
A convenient way to avoid this problem
is to evaluate the form only once,
and bind a (generated) variable to the result.
There is a very useful macro called `ALEXANDRIA:ONCE-ONLY`
that generates code to do this.
See also `ALEXANDRIA:WITH-GENSYMS`,
to make some temporary variables in the generated code.
Note that if you follow our `CALL-WITH` style,
you typically expand the code only once, as either
an argument to the auxiliary function, or
the body of a lambda passed as argument to it;
you therefore avoid the above complexity.

## EVAL-WHEN

When using `EVAL-WHEN`, you should almost always use all of
`(:compile-toplevel :load-toplevel :execute)`.

## EVAL

You must not use `EVAL` at runtime.

## INTERN and UNINTERN

You must not use `INTERN` or `UNINTERN` at runtime.

## NIL: empty-list, false and I Don't Know

Appropriately use or avoid using `NIL`.

## Do not abuse lists

You must select proper data representation.
You must not abuse the `LIST` data structure.

## Lists vs. structures vs. multiple values

You should use the appropriate representation for product types.

## Lists vs. Arrays

You should use arrays rather than lists where random access matters.

## Lists vs. Sets

You should only use lists as sets for very small lists.

## Defining Functions

You should make proper use of
`&OPTIONAL` and
`&KEY` arguments.
You should not use `&AUX` arguments.
