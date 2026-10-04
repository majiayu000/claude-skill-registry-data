---
name: google-java-style
description: >-
  Use when writing or reviewing Java source under Google's formatting, naming, ordering,
  Javadoc, and programming-practice conventions. Do not use for Java API design questions
  outside the guide's scope.
---

# Google Java Style Guide

Apply this guidance to the actual project. Repository requirements and newer authoritative guidance take precedence.

## 1.2 Guide notes

Example code in this document is **non-normative**. That is, while the examples
are in Google Style, they may not illustrate the *only* stylish way to represent the
code. Optional formatting choices made in examples should not be enforced as rules.

## 2.1 File name

For a source file containing classes, the file name consists of the case-sensitive name of the
top-level class (of which there is exactly one), plus the
`.java` extension.

## 2.2 File encoding: UTF-8

Source files are encoded in **UTF-8**.

## 2.3.1 Whitespace characters

Aside from the line terminator sequence, the **ASCII horizontal space
character** (**0x20**) is the only whitespace character that appears
anywhere in a source file. This implies that:
1. All other whitespace characters are escaped in `char` and string literals and in
   text blocks.
2. Tab characters are **not** used for indentation.

## 3 Source file structure

An ordinary source file consists of these sections, **in order**:
1. License or copyright information, if present
2. Package declaration
3. Imports
4. Exactly one top-level class declaration
**Exactly one blank line** separates each section that is present.

## 3.2 Package declaration

Every source file must have a package declaration. [Compact source files](https://openjdk.org/jeps/512) are not used. (This rule obviously does not apply to
`module-info.java` files, which have a different syntax that does not include a
package declaration.)

## 3.3.1 No wildcard imports

**Wildcard ("on-demand") imports**, static or otherwise, **are not
used**.

## 3.3.1.1 No module imports

[Module imports](https://docs.oracle.com/en/java/javase/25/language/module-import-declarations.html) **are not used**.

## 3.3.2 No line-wrapping

Imports are **not line-wrapped**. The column limit (Section 4.4,
Column limit: 100) does not apply to imports.

## 3.3.3 Ordering and spacing

Imports are ordered as follows:
1. All static imports in a single group.
2. All non-static imports in a single group.
If there are both static and non-static imports, a single blank line separates the two
groups. There are no other blank lines between imports.
Within each group the imported names appear in ASCII sort order. (**Note:**
this is not the same as the import *lines* being in ASCII sort order, since '.'
sorts before ';'.)

## 3.3.4 No static import for classes

Static import is not used for static nested classes. They are imported with
normal imports.

## 3.4.1 Exactly one top-level class declaration

Each top-level class resides in a source file of its own.

## 3.4.2 Ordering of class contents

The order you choose for the members and initializers of your class can have a great effect on
learnability. However, there's no single correct recipe for how to do it; different classes may
order their contents in different ways.
What is important is that each class uses ***some* logical order**, which its
maintainer could explain if asked. For example, new methods are not just habitually added to the end
of the class, as that would yield "chronological by date added" ordering, which is not a logical
ordering.

## 3.4.2.1 Overloads: never split

Methods of a class that share the same name appear in a single contiguous group with no other
members in between. The same applies to multiple constructors. This rule applies even when
modifiers such as `static` or
`private` differ between the methods or constructors.

## 4.1.1 Use of optional braces

Braces are used with
`if`,
`else`,
`for`,
`do` and
`while` statements, even when the
body is empty or contains only a single statement.
Other optional braces, such as those in a lambda expression, remain optional.

## 4.1.2 Nonempty blocks: K & R style

Braces follow the Kernighan and Ritchie style for *nonempty* blocks and block-like
constructs:
- No line break before the opening brace, except as detailed below.
- Line break after the opening brace.
- Line break before the closing brace.
- Line break after the closing brace, *only if* that brace terminates a statement or
  terminates the body of a method, constructor, or *named* class.
  For example, there is *no* line break after the brace if it is followed by
  `else` or a comma.

## 4.2 Block indentation: +2 spaces

Each time a new block or block-like construct is opened, the indent increases by two
spaces. When the block ends, the indent returns to the previous indent level. The indent level
applies to both code and comments throughout the block.

## 4.3 One statement per line

Each statement is followed by a line break.

## 4.4 Column limit: 100

Java code has a column limit of 100 characters. A "character" means any Unicode code point.
Except as noted below, any line that would exceed this limit must be line-wrapped, as explained in
Section 4.5, Line-wrapping.
1. Lines where obeying the column limit is not possible (for example, a long URL in Javadoc,
   or a long JSNI method reference).
2. `package` declarations and
   imports (see Sections 3.2 Package declarations and
   3.3 Imports).
3. Contents of text blocks.
4. Command lines in a comment that may be copied-and-pasted into a shell.
5. Very long identifiers, on the rare occasions they are called for, are allowed to exceed the
   column limit. In that case, the valid wrapping for the surrounding code is as produced by
   [google-java-format](https://github.com/google/google-java-format).

## 4.5.1 Where to break

The prime directive of line-wrapping is: prefer to break at a
**higher syntactic level**. Also:
1. When a line is broken at a *non-assignment* operator the break comes *before*
   the symbol. (Note that this is not the same practice used in Google style for other languages,
   such as C++ and JavaScript.)
   - This also applies to the following "operator-like" symbols:
     - the dot separator (`.`)
     - the two colons of a method reference
       (`::`)
     - an ampersand in a type bound
       (`<T extends Foo & Bar>`)
     - a pipe in a catch block
       (`catch (FooException | BarException e)`).
2. When a line is broken at an *assignment* operator the break typically comes
   *after* the symbol, but either way is acceptable.
   - This also applies to the colon in an enhanced
     `for` ("foreach") statement.
3. A method, constructor, or record-class name stays attached to the open parenthesis
   (`(`) that follows it.
4. A comma (`,`) stays attached to the token that
   precedes it.
5. A line is never broken adjacent to the arrow in a lambda or a switch rule, except that a
   break may come immediately after the arrow if the text following it consists of a single unbraced
   expression. Examples:
   ```
   MyLambda<String, Long, Object> lambda =
       (String label, Long value, Object obj) -> {
         ...
       };

   Predicate<String> predicate = str ->
       longExpressionInvolving(str);

   switch (x) {
     case ColorPoint(Color color, Point(int x, int y)) ->
         handleColorPoint(color, x, y);
     ...
   }
   ```
**Note:** The primary goal for line wrapping is to have clear
code, *not necessarily* code that fits in the smallest number of lines.

## 4.5.2 Indent continuation lines at least +4 spaces

When line-wrapping, each line after the first (each *continuation line*) is indented
at least +4 from the original line.

## 4.8.2.1 One variable per declaration

Every variable declaration (field or local) declares only one variable: declarations such as
`int a, b;` are not used.
**Exception:** Multiple variable declarations are acceptable in the header of a
`for` loop.

## 4.8.2.2 Declared when needed

Local variables are **not** habitually declared at the start of their containing
block or block-like construct. Instead, local variables are declared close to the point they are
first used (within reason), to minimize their scope. Local variable declarations typically have
initializers, or are initialized immediately after declaration.

## 4.8.3.2 No C-style array declarations

The square brackets form a part of the *type*, not the variable:
`String[] args`, not
`String args[]`.

## 4.8.4.2 Fall-through: commented

Within an old-style switch block, each statement group either terminates abruptly (with a
`break`,
`continue`,
`return` or thrown exception), or is marked with a comment
to indicate that execution will or *might* continue into the next statement group. Any
comment that communicates the idea of fall-through is sufficient (typically
`// fall through`). This special comment is not required in
the last statement group of the switch block. Example:
There is no fall-through in new-style switches.

## 4.8.4.3 Exhaustiveness and presence of the `default` label

The Java language requires switch expressions and many kinds of switch statements to be
*exhaustive*. That effectively means that every possible value that could be switched on will
be matched by one of the switch labels. A switch is exhaustive if it has a `default` label, but also for example if the value being switched
on is an enum and every value of the enum is matched by a switch label. Google Style requires
*every* switch to be exhaustive, even those where the language itself does not require it.
This may require adding a `default` label, even if it
contains no code.

## 4.8.4.4 Switch expressions

Switch expressions must be new-style switches:
```
  return switch (list.size()) {
    case 0 -> "";
    case 1 -> list.getFirst();
    default -> String.join(", ", list);
  };
```

## 4.8.5.1 Type-use annotations

Type-use annotations appear immediately before the annotated type. An annotation is a type-use
annotation if it is meta-annotated with
`@Target(ElementType.TYPE_USE)`. Example:
```
final @Nullable String name;

public @Nullable Person getPersonByName(String name);
```

## 4.8.5.2 Class, package, and module annotations

Annotations applying to a class, package, or module declaration appear immediately after the
documentation block, and each annotation is listed on a line of its own (that is, one annotation
per line). These line breaks do not constitute line-wrapping (Section
4.5, Line-wrapping), so the indentation level is not
increased. Examples:
```
/** This is a class. */
@Deprecated
@CheckReturnValue
public final class Frozzler { ... }
```

## 4.8.5.3 Method and constructor annotations

The rules for annotations on method and constructor declarations are the same as the
previous section. Example:
```
@Deprecated
@Override
public String getNameIfPresent() { ... }
```
**Exception:** If the method or constructor only has a
*single*, *parameterless* annotation, it *may* appear together with the first
line of the signature, for example:
```
@Override public int hashCode() { ... }
```

## 4.8.6.2 TODO comments

Use `TODO` comments for code that is temporary, a short-term solution, or good-enough
but not perfect.
A `TODO` comment begins with the word `TODO` in all caps, a following
colon, and a link to a resource that contains the context, ideally a bug reference. A bug
reference is preferable because bugs are tracked and have follow-up comments. Follow this piece of
context with an explanatory string introduced with a hyphen `-`.
Avoid adding TODOs that refer to an individual or team as the context:
If your `TODO` is of the form "At a future date do something" make sure that you
either include a very specific date ("Fix by November 2005") or a very specific event ("Remove
this code when all clients can handle XML responses.").

## 4.8.7 Modifiers

Class and member modifiers, when present, appear in the order
recommended by the Java Language Specification:
```
public protected private abstract default static final sealed non-sealed
  transient volatile synchronized native strictfp
```
Modifiers on `requires` module directives, when present, appear in the following
order:
```
transitive static
```

## 5.1 Rules common to all identifiers

Identifiers use only ASCII letters and digits, and, in a small number of cases noted below,
underscores. Thus each valid identifier name is matched by the regular expression
`\w+` .
In Google Style, special prefixes or suffixes are **not** used. For example, these
names are not Google Style: `name_`, `mName`,
`s_name` and `kName`.

## 5.2.1 Package and module names

Package and module names use only lowercase letters and digits (no underscores). Consecutive
words are simply concatenated together. For example, `com.example.deepspace`, not
`com.example.deepSpace` or
`com.example.deep_space`.

## 5.2.2 Class names

Class names are written in UpperCamelCase.
A *test* class has a name that ends with `Test`,
for example, `HashIntegrationTest`.
If it covers a single class, its name is the name of that class
plus `Test`, for example `HashImplTest`.

## 5.2.3 Method names

Method names are written in lowerCamelCase.
Underscores may appear in JUnit *test* method names to separate logical components of the
name, with *each* component written in lowerCamelCase, for
example `transferMoney_deductsFromSource`. There is no One
Correct Way to name test methods.

## 5.2.4 Constant names

Constant names use `UPPER_SNAKE_CASE`: all uppercase
letters, with each word separated from the next by a single underscore. But what *is* a
constant, exactly?
Constants are static final fields whose contents are deeply immutable and whose methods have no
detectable side effects. Examples include primitives, strings, immutable value classes, and anything
set to `null`. If any of the instance's observable state can change, it is not a
constant. Merely *intending* to never mutate the object is not enough. Examples:
```
// Constants
static final int NUMBER = 5;
static final ImmutableList<String> NAMES = ImmutableList.of("Ed", "Ann");
static final Map<String, Integer> AGES = ImmutableMap.of("Ed", 35, "Ann", 32);
static final Joiner COMMA_JOINER = Joiner.on(','); // because Joiner is immutable
static final SomeMutableType[] EMPTY_ARRAY = {};

// Not constants
static String nonFinal = "non-final";
final String nonStatic = "non-static";
static final Set<String> mutableCollection = new HashSet<String>();
static final ImmutableSet<SomeMutableType> mutableElements = ImmutableSet.of(mutable);
static final ImmutableMap<String, SomeMutableType> mutableValues =
    ImmutableMap.of("Ed", mutableInstance, "Ann", mutableInstance2);
static final Logger logger = Logger.getLogger(MyClass.getName());
static final String[] nonEmptyArray = {"these", "can", "change"};
```

## 5.2.5 Non-constant field names

Non-constant field names (static or otherwise) are written
in lowerCamelCase.

## 5.2.6 Parameter names

Parameter names are written in lowerCamelCase.
One-character parameter names in public methods should be avoided.

## 5.2.7 Local variable names

Local variable names are written in lowerCamelCase.
Even when final and immutable, local variables are not considered to be constants, and should not
be styled as constants.

## 5.2.8 Type variable names

Each type variable is named in one of two styles:
- A single capital letter, optionally followed by a single numeral (such as
  `E`, `T`,
  `X`, `T2`)
- A name in the form used for classes (see Section 5.2.2,
  Class names), followed by the capital letter
  `T` (examples:
  `RequestT`,
  `FooBarT`).

## 5.3 Camel case: defined

Sometimes there is more than one reasonable way to convert an English phrase into camel case,
such as when acronyms or unusual constructs like "IPv6" or "iOS" are present. To improve
predictability, Google Style specifies the following (nearly) deterministic scheme.
1. Convert the phrase to plain ASCII and remove any apostrophes. For example, "Müller's
   algorithm" might become "Muellers algorithm".
2. Divide this result into words, splitting on spaces and any remaining punctuation (typically
   hyphens).
   - *Recommended:* if any word already has a conventional camel-case appearance in common
     usage, split this into its constituent parts (e.g., "AdWords" becomes "ad words"). Note
     that a word such as "iOS" is not really in camel case *per se*; it defies *any*
     convention, so this recommendation does not apply.
3. Now lowercase *everything* (including acronyms), then uppercase only the first
   character of:
   - ... each word, to yield *upper camel case*, or
   - ... each word except the first, to yield *lower camel case*
4. Finally, join all the words into a single identifier. Note that the casing of the original
   words is almost entirely disregarded.

## 6.1 `@Override`: always used

A method is marked with the `@Override` annotation
whenever it is legal. This includes a class method overriding a superclass method, a class method
implementing an interface method, an interface method respecifying a superinterface method, and an
explicitly declared accessor method for a record component.
**Exception:**
`@Override` may be omitted when the parent method is
`@Deprecated`.

## 6.2 Caught exceptions: not ignored

It is very rarely correct to do nothing in response to a caught
exception. (Typical responses are to log it, or if it is considered "impossible", rethrow it as an
`AssertionError`.)
When it truly is appropriate to take no action whatsoever in a catch block, the reason this is
justified is explained in a comment.

## 6.3 Static members: qualified using class

When a reference to a static class member must be qualified, it is qualified with that class's
name, not with a reference or expression of that class's type.

## 6.4 Finalizers: not used

Do not override `Object.finalize`. Finalization support
is [*scheduled for removal*](https://openjdk.org/jeps/421).

## 7.2 The summary fragment

Each Javadoc block begins with a brief **summary fragment**. This
fragment is very important: it is the only part of the text that appears in certain contexts such as
class and method indexes.
This is a fragment—a noun phrase or verb phrase, not a complete sentence. It does
**not** begin with `A {@code Foo} is a...`, or
`This method returns...`, nor does it form a complete imperative sentence
like `Save the record.`. However, the fragment is capitalized and
punctuated as if it were a complete sentence.
**Tip:** A common mistake is to write simple Javadoc in the form
`/** @return the customer ID */`. This is
incorrect, and should be changed to
`/** Returns the customer ID. */` or
`/** {@return the customer ID} */`.

## 7.3 Where Javadoc is used

At the *minimum*, Javadoc is present for every *visible* class, member, or record
component, with a few exceptions noted below. A top-level class is visible if it is `public`; a member is visible if it is `public` or `protected` and its containing
class is visible; and a record component is visible if its containing record is visible.

## 7.3.1 Exception: self-explanatory members

Javadoc is optional for "simple, obvious" members and record components, such as a
`getFoo()` method, *if* there *really and
truly* is nothing else worthwhile to say but "the foo".
**Important:** it is not appropriate to cite this exception to justify
omitting relevant information that a typical reader might need to know. For example, for a record
component named `canonicalName`, don't omit its
documentation (with the rationale that it would say only
`@param canonicalName the canonical name`) if a typical reader may have
no idea what the term "canonical name" means!

## 7.3.2 Exception: overrides

Javadoc is not always present on a method that overrides a supertype method.
