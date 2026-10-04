---
name: google-objective-c-style
description: >-
  Use when writing or reviewing Objective-C and Objective-C++ under Google's naming, formatting,
  Cocoa-pattern, memory-management, and documentation conventions. Do not use as a Swift style
  guide.
---

# Google Objective-C Style Guide

Apply this guidance to the actual project. Repository requirements and newer authoritative guidance take precedence.

## Be consistent with Apple SDKs

Consistency with the way Apple SDKs use Objective-C has value for the same
reasons as consistency within our code base. If an Objective-C feature solves a
problem that's an argument for using it. However, sometimes language features
and idioms are flawed, or were just designed with assumptions that are not
universal. In those cases it is appropriate to constrain or ban language
features or idioms.

## Inclusive Language

In all code, including naming and comments, use inclusive language and avoid
terms that other programmers might find disrespectful or offensive (such as
"master" and "slave", "blacklist" and "whitelist", or "redline"), even if the
terms also have an ostensibly neutral meaning. Similarly, use gender-neutral
language unless you're referring to a specific person (and using their
pronouns). For example, use "they"/"them"/"their" for people of unspecified
gender (even when singular), and "it"/"its" for non-people.

## File Names

File names should reflect the name of the class implementation that they
contain—including case.
File extensions should be as follows:
Extension | Type
--------- | ---------------------------------
.h        | C/C++/Objective-C header file
.m        | Objective-C implementation file
.mm       | Objective-C++ implementation file
.cc       | Pure C++ implementation file
.c        | C implementation file
File names for categories should include the name of the class being extended,
like GTMNSString+Utils.h or NSTextView+GTMAutocomplete.h

## Prefixes

Prefixes are commonly required in Objective-C to avoid naming collisions in a
global namespace. Classes, protocols, global functions, and global constants
should generally be named with a prefix that begins with a capital letter
followed by one or more capital letters or numbers.
WARNING: Apple reserves two-letter prefixes—see
[Conventions in Programming with Objective-C](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/Conventions/Conventions.html)—so
prefixes with a minimum of three characters are considered best practice.

## Category Naming

Category names should start with an appropriate prefix identifying
the category as part of a project or open for general use.
Category source file names should begin with the class being extended followed
by a plus sign and the name of the category, e.g., `NSString+GTMParsing.h`.
Methods in a category should be prefixed with a lowercase version of the prefix
used for the category name followed by an underscore (e.g.,
`gtm_myCategoryMethodOnAString:`) in order to prevent collisions in
Objective-C's global namespace.
If a class is not shared with other projects, categories extending it may omit
name prefixes and method name prefixes.

## Objective-C Method Names

Method and parameter names typically start as lowercase and then use mixed case.
Proper capitalization should be respected, including at the beginning of names.
The method name should read like a sentence if possible, meaning you should
choose parameter names that flow with the method name. Objective-C method names
tend to be very long, but this has the benefit that a block of code can almost
read like prose, thus rendering many implementation comments unnecessary.
Use prepositions and conjunctions like "with", "from", and "to" in the second
and later parameter names only where necessary to clarify the meaning or
behavior of the method.
If the method returns an attribute of the receiver, name the method after the
attribute.
An accessor method should be named the same as the object it's getting, but it
should not be prefixed with the word `get`. For example:
```objectivec
// GOOD:

- (id)delegate;     // GOOD.
```
Accessors that return the value of boolean adjectives have method names
beginning with `is`, but property names for those methods omit the `is`.
Dot notation is used only with property names, not with method names.
These guidelines are for Objective-C methods only. C++ method names continue to
follow the rules set in the C++ style guide.

## Function Names

Function names should start with a capital letter and have a capital letter for
each new word (a.k.a. "[camel case](https://en.wikipedia.org/wiki/Camel_case)"
or "Pascal case").
Because Objective-C does not provide namespacing, non-static functions should
have a prefix that minimizes the chance of a name collision.

## Variable Names

Variable names typically start with a lowercase and use mixed case to delimit
words.
Instance variables have leading underscores. File scope or global variables have
a prefix `g`. For example: `myLocalVariable`, `_myInstanceVariable`,
`gMyGlobalVariable`.

## Constants

Constant symbols (const global and static variables and constants created
with #define) should use mixed case to delimit words.
Global and file scope constants should have an appropriate prefix.
Because Objective-C does not provide namespacing, constants with external
linkage should have a prefix that minimizes the chance of a name collision,
typically like `ClassNameConstantName` or `ClassNameEnumName`.
For interoperability with Swift code, enumerated values should have names that
extend the typedef name:
```objectivec
// GOOD:

/** An enumeration of supported display tinges. */
typedef NS_ENUM(int32_t, DisplayTinge) {
  DisplayTingeGreen = 1,
  DisplayTingeBlue = 2,
};
```
A lowercase k can be used as a standalone prefix for constants of static storage
duration declared within implementation files:
```objectivec
// GOOD:

static const int kFileCount = 12;
static NSString *const kUserKey = @"kUserKey";
```

## Method Declarations

The recommended order
for declarations in an `@interface` declaration are: properties, class methods,
initializers, and then finally instance methods. The class methods section
should begin with any convenience constructors.

## Local Variables

Declare variables in the narrowest practical scopes, and close to their use.
Initialize variables in their declarations.

## Static Variables

When file scope variable/constant declarations in an implementation file do not
need to be referenced outside that file, declare them static (or in an anonymous
namespace in Objective-C++). Do not declare file scope variables or constants
with static storage duration (or in anonymous namespaces in Objective-C++) in .h
files.

## Unsigned Integers

Avoid unsigned integers except when matching types used by system interfaces.
Subtle errors crop up when doing math or counting down to zero using unsigned
integers. Rely only on signed integers in math expressions except when matching
NSUInteger in system interfaces.
Unsigned integers may be used for flags and bitmasks, though often NS_OPTIONS or
NS_ENUM will be more appropriate.

## Types with Inconsistent Sizes

Be aware that types long, NSInteger, NSUInteger and CGFloat have sizes that
differ in 32- and 64-bit builds. Their use is appropriate when matching system
interfaces but should be avoided when dealing with APIs that
require exact sizing, e.g., proto APIs.
File and buffer sizes often exceed 32-bit limits, so they should be declared
using `int64_t`, not with `long`, `NSInteger`, or `NSUInteger`.

## Declaration Comments

Every non-trivial interface, public and private, should have an accompanying
comment describing its purpose and how it fits into the larger picture.
Comments should be used to document classes, properties, ivars, functions,
categories, protocol declarations, and enums.
Additionally, each method should have a comment explaining its function,
arguments, return value, thread or queue assumptions, and any side effects.
Documentation comments should be in the header for public methods, or
immediately preceding the method for non-trivial private methods.
Document the thread usage assumptions the class, properties, or methods make, if
any. If an instance of the class can be accessed by multiple threads, take extra
care to document the rules and invariants surrounding multithreaded use.
Any sentinel values for properties and ivars, such as `NULL` or `-1`, should be
documented in comments.
Declaration comments explain how a method or function is used. Comments
explaining how a method or function is implemented should be with the
implementation rather than with the declaration.

## Macros

Avoid macros, especially where `const` variables, enums, Xcode snippets, or C
functions may be used instead.
Where a macro is needed, use a unique name to avoid the risk of a symbol
collision in the compilation unit. If practical, keep the scope limited by
`#undefining` the macro after its use.
Macro names should use `SHOUTY_SNAKE_CASE`—all uppercase letters with
underscores between words. Function-like macros may use C function naming
practices. Do not define macros that appear to be C or Objective-C keywords.
Avoid macros that expand to unbalanced C or Objective-C constructs. Avoid macros
that introduce scope, or may obscure the capturing of values in blocks.

## Nonstandard Extensions

Nonstandard extensions to C/Objective-C may not be used unless otherwise
specified.

## Identify Designated Initializers

Clearly identify your designated initializer(s).
Prefer identifying designated initializers by annotating them with designated
initializer attributes, e.g., `NS_DESIGNATED_INITIALIZER`. Declare designated
initializers in comments when designated initializer attributes are not
available. Prefer a single designated initializer unless there is a compelling
reason or requirement for multiple designated initializers.
Support initializers inherited from superclasses by
overriding superclass designated initializers
to ensure that all inherited initializers are directed through subclass
designated initializers. When there is a compelling reason or requirement that
an inherited initializer should not be supported, the initializer may be
annotated with availability attributes (e.g., `NS_UNAVAILABLE`) to discourage
usage; however, note that availability attributes alone do not completely
protect against invalid initialization.

## Initialization

Don't initialize instance variables to `0` or `nil` in the `init` method; doing
so is redundant.

## Instance Variables In Headers Should Be @protected or @private

Instance variables should typically be declared in implementation files or
auto-synthesized by properties. When ivars are declared in a header file, they
should be marked `@protected` or `@private`.

## Do Not Use +new

Do not invoke the `NSObject` class method `new`, nor override it in a subclass.
`+new` is rarely used and contrasts greatly with initializer usage. Instead, use
`+alloc` and `-init` methods to instantiate retained objects.

## Keep the Public API Simple

Keep your class simple; avoid "kitchen-sink" APIs. If a method doesn't need to
be public, keep it out of the public interface.
Unlike C++, Objective-C doesn't differentiate between public and private
methods; any message may be sent to an object. As a result, avoid placing
methods in the public API unless they are actually expected to be used by a
consumer of the class. This helps reduce the likelihood they'll be called when
you're not expecting it. This includes methods that are being overridden from
the parent class.
Since internal methods are not really private, it's easy to accidentally
override a superclass's "private" method, thus making a very difficult bug to
squash. In general, private methods should have a fairly unique name that will
prevent subclasses from unintentionally overriding them.

## #import and #include

`#import` Objective-C and Objective-C++ headers, and `#include` C/C++ headers.
C/C++ headers include other C/C++ headers using `#include`. Using `#import`
on C/C++ headers prevents future inclusions using `#include` and could result in
unintended compilation behavior.

## Order of Includes

The standard order for header inclusion is the related header, operating system
headers, language library headers, and finally groups of headers for other
dependencies.
The related header precedes others to ensure it has no hidden dependencies.
For implementation files the related header is the header file.
For test files the related header is the header containing the tested interface.
Separate each non-empty group of includes with one blank line. Within each group
the includes should be ordered alphabetically.
Import headers using their path relative to the project's source directory.

## Avoid Messaging the Current Object Within Initializers and `-dealloc`

Code in initializers and `-dealloc` should avoid invoking instance methods when
possible.
Superclass initialization completes before subclass initialization. Until all
classes have had a chance to initialize their instance state any method
invocation on self may lead to a subclass operating on uninitialized instance
state.
A similar issue exists for `-dealloc`, where a method invocation may cause a
class to operate on state that has been deallocated.
One case where this is less obvious is property accessors. These can be
overridden just like any other selector. Whenever practical, directly assign to
and release ivars in initializers and `-dealloc`, rather than rely on accessors.
-   Methods can be overridden in subclasses, either deliberately, or
    accidentally due to naming collisions.
-   When editing a helper method, it may not be obvious that the code is being
    run from an initializer.
There are common cases where a class may need to use properties and methods
provided by a superclass during initialization. This commonly occurs for classes
derived from UIKit and AppKit base classes, among other base classes. Use your
judgement and knowledge of common practice when deciding whether to make an
exception to this rule.

## Mutables, Copies and Ownership

For [Foundation and other hierarchies containing both immutable and mutable
subclasses](https://developer.apple.com/library/archive/documentation/General/Conceptual/CocoaEncyclopedia/ObjectMutability/ObjectMutability.html)
a mutable subclass may be substituted for an immutable so long as the
immutable's contract is honored.
The most common example of this sort of substitution are ownership transfers,
particularly for return values. In these cases an additional copy is not
necessary and returning the mutable subclass is more efficient.
[Callers are expected to treat return values as their declared type](https://developer.apple.com/library/archive/documentation/General/Conceptual/CocoaEncyclopedia/ObjectMutability/ObjectMutability.html#//apple_ref/doc/uid/TP40010810-CH5-SW67),
and thus the return value will be treated as an immutable going forward.
This rule also applies to classes where only a mutable variant exists so long as
the ownership transfer is clear. Protos are a common example.

## Copy Potentially Mutable Objects

Code receiving and retaining collections or other types with
[mutable variants](https://developer.apple.com/library/archive/documentation/General/Conceptual/CocoaEncyclopedia/ObjectMutability/ObjectMutability.html)
should consider that the passed object may be mutable, and thus an immutable or
mutable copy should be retained instead of the original object. In particular,
initializers and setters
[should copy instead of retaining objects whose types have mutable variants](https://developer.apple.com/library/archive/documentation/General/Conceptual/CocoaEncyclopedia/ObjectMutability/ObjectMutability.html#//apple_ref/doc/uid/TP40010810-CH5-SW68).
Synthesized accessors should use the `copy` keyword to ensure the generated code
matches these expectations.
NOTE: [The `copy` property keyword only affects the synthesized setter and has
no effect on
getters](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ObjectiveC/Chapters/ocProperties.html#//apple_ref/doc/uid/TP30001163-CH17-SW27).
Since property keywords have no effect on direct ivar access custom accessors
must implement the same copy semantics.
All Objective-C protos are mutable and typically should be copied rather than
retained
except in clear cases of ownership transfer.
Asynchronous code should copy potentially mutable objects prior to dispatch.
Objects captured by blocks are retained but not copied.
NOTE: It is unnecessary to copy objects that do not have mutable variants, e.g.
`NSURL`, `NSNumber`, `NSDate`, `UIColor`, etc.

## Use Lightweight Generics to Document Contained Types

All projects compiling on Xcode 7 or newer versions should make use of the
Objective-C lightweight generics notation to type contained objects.
Every `NSArray`, `NSDictionary`, or `NSSet` reference should be declared using
lightweight generics for improved type safety and to explicitly document usage.
If the fully-annotated types become complex, consider using a typedef to
preserve readability.
Use the most descriptive common superclass or protocol available. In the most
generic case when nothing else is known, declare the collection to be explicitly
heterogeneous using id.

## Avoid Throwing Exceptions

Don't `@throw` Objective-C exceptions, but you should be prepared to catch them
from third-party or OS calls.
We do compile with `-fobjc-exceptions` (mainly so we get `@synchronized`), but
we don't `@throw`. Use of `@try`, `@catch`, and `@finally` are allowed when
required to properly use 3rd party code or libraries. If you do use them, please
document exactly which methods you expect to throw.

## `nil` Checks

Avoid `nil` pointer checks that exist only to prevent sending messages to `nil`.
Sending a message to `nil` [reliably
returns](http://www.sealiesoftware.com/blog/archive/2012/2/29/objc_explain_return_value_of_message_to_nil.html)
`nil` as a pointer, zero as an integer or floating-point value, structs
initialized to `0`, and `_Complex` values equal to `{0, 0}`.
Note that this applies to `nil` as a message target, not as a parameter value.
Individual methods may or may not safely handle `nil` parameter values.
Note too that this is distinct from checking C/C++ pointers and block pointers
against `NULL`, which the runtime does not handle and will cause your
application to crash. You still need to make sure you do not dereference a
`NULL` pointer.

## Nullability

Interfaces can be decorated with nullability annotations to describe how the
interface should be used and how it behaves. Use of nullability regions (e.g.,
`NS_ASSUME_NONNULL_BEGIN` and `NS_ASSUME_NONNULL_END`) and explicit nullability
annotations are both accepted. Prefer using the `_Nullable` and `_Nonnull`
keywords over the `__nullable` and `__nonnull` keywords. For Objective-C methods
and properties prefer using the context-sensitive, non-underscored keywords,
e.g., `nonnull` and `nullable`.
Do not assume that a pointer is not null based on a nonnull qualifier, because
the compiler only checks a subset of such cases, and does not guarantee that the
pointer is not null. Avoid intentionally violating nullability semantics
of function, method, and property declarations.

## BOOL Expressions and Conversions

Be careful when converting general integral values to `BOOL`. Avoid comparing
directly with `YES` or comparing multiple `BOOL` values with comparison
operators.
`BOOL` on some Apple platforms (notably Intel macOS, watchOS, and 32-bit iOS)
is defined as a signed `char`, so it may have values other than `YES` (`1`) and
`NO` (`0`). Do not cast or convert general integral values directly to `BOOL`.
When converting a general integral value to a `BOOL`, use conditional operators
to return a `YES` or `NO` value.
Using logical operators (`&&`, `||` and `!`) with `BOOL` is also valid and will
return values that can be safely converted to `BOOL` without the need for a
conditional operator.
Don't directly compare `BOOL` variables directly with `YES`. Not only is
it harder to read for those well-versed in C, but the first point above
demonstrates that return values may not always be what you expect.
Don't directly compare `BOOL` values using comparison operators. `BOOL`
values that are true may not be equal. Use logical operators in place
of bitwise comparisons of `BOOL` values.

## Delegate Pattern

Delegates, target objects, and block pointers should not be retained when doing
so would create a retain cycle.
To avoid causing a retain cycle, a delegate or target pointer should be released
as soon as it is clear there will no longer be a need to message the object.
If there is no clear time at which the delegate or target pointer is no longer
needed, the pointer should only be retained weakly.
Block pointers cannot be retained weakly. To avoid causing retain cycles in the
client code, block pointers should be used for callbacks only where they can be
explicitly released after they have been called or once they are no longer
needed. Otherwise, callbacks should be done via weak delegate or target
pointers.

## Style Matches the Language

Within an Objective-C++ source file, follow the style for the language of the
function or method you're implementing. In order to minimize clashes between the
differing naming styles when mixing Cocoa/Objective-C and C++, follow the style
of the method being implemented.
For code in an `@implementation` block, use the Objective-C naming rules. For
code in a method of a C++ class, use the C++ naming rules.
For code in an Objective-C++ file outside of a class implementation, be
consistent within the file.
Projects may opt to use an 80 column line length limit for consistency with
Google's C++ style guide.

## Method Declarations and Definitions

One space should be used between the `-` or `+` and the return type. In general,
there should be no spacing in the parameter list except between parameters.
If a method declaration does not fit on a single line, put each parameter on its
own line. All lines except the first should be indented at least four spaces.
Colons before parameters should be aligned on all lines. If the colon before the
parameter on the first line of a method declaration is positioned such that
colon alignment would cause indentation on a subsequent line to be less than
four spaces, then colon alignment is only required for all lines except the
first. If a parameter declared after the `:` in a method declaration or
definition would cause the line limit to be exceeded, wrap the content to the
next line indented by at least four spaces.

## Conditionals

Include a space after `if`, `while`, `for`, and `switch`, and around comparison
operators.
Braces may be omitted when a loop body or conditional statement fits on a single
line.
If an `if` clause has an `else` clause, both clauses should use braces.
Intentional fall-through to the next case should be documented with a comment
unless the case has no intervening code before the next case.

## Indicating style exceptions

Lines of code that are not expected to adhere to these style recommendations
require `// NOLINT` at the end of the line or `// NOLINTNEXTLINE` at the end of
the previous line. Sometimes it is required that parts of Objective-C code must
ignore these style recommendations (for example code may be machine generated or
code constructs are such that its not possible to style correctly).
