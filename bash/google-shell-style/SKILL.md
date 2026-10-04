---
name: google-shell-style
description: >-
  Use when writing or reviewing Bash and shell scripts under Google's conventions for scope,
  features, naming, comments, quoting, command substitution, and error handling. Do not use for
  non-Bourne-compatible shells without checking applicability.
---

# Google Shell Style Guide

Apply this guidance to the actual project. Repository requirements and newer authoritative guidance take precedence.

## Shell Style Guide

### Which Shell to Use

Bash is the only shell scripting language permitted for executables.
Executables must start with `#!/bin/bash` and minimal flags. Use `set` to set
shell options so that calling your script as `bash script_name` does not break
its functionality.
The only exception to the above is where you're forced to by whatever you're
coding for. For example some legacy operating systems or constrained execution
environments may require plain Bourne shell for certain scripts.

### When to use Shell

Shell should only be used for small utilities or simple wrapper
scripts.
Some guidelines:
*   If you're mostly calling other utilities and are doing relatively little
    data manipulation, shell is an acceptable choice for the task.
*   If performance matters, use something other than shell.
*   If you are writing a script that is more than 100 lines long, or that uses
    non-straightforward control flow logic, you should rewrite it in a more
    structured language *now*. Bear in mind that scripts grow. Rewrite your
    script early to avoid a more time-consuming rewrite at a later date.
*   When assessing the complexity of your code (e.g. to decide whether to switch
    languages) consider whether the code is easily maintainable by people other
    than its author.

### File Extensions

Executables should have a `.sh` extension or no extension.
-   If the executable will have a build rule that renames the source file
    then prefer to use a `.sh` extension.
    This enables you to use the recommended naming convention, with a source
    file like `foo.sh` and a build rule named `foo`.
-   If the executable will be added directly to the user's `PATH`, then prefer
    to use no extension. It is not necessary to know what language a program is
    written in when executing it and shell doesn't require an extension so we
    prefer not to use one for executables that will be directly invoked by
    users. At the same time, consider whether it is preferable to deploy the
    output of a build rule rather than deploying the source file directly.
-   If neither of the above apply, then either choice is acceptable.
Libraries must have a `.sh` extension and should not be executable.

### SUID/SGID

SUID and SGID are *forbidden* on shell scripts.
Use `sudo` to provide elevated access if you need it.

### STDOUT vs STDERR

All error messages should go to `STDERR`.
This makes it easier to separate normal status from actual issues.
A function to print out error messages along with other status
information is recommended.

### File Header

Start each file with a description of its contents.
Every file must have a top-level comment including a brief overview of
its contents. A
copyright notice
and author information are optional.

### Function Comments

Any function that is not both obvious and short must have a function header
comment. Any function in a library must have a function header comment
regardless of length or complexity.
It should be possible for someone else to learn how to use your
program or to use a function in your library by reading the comments
(and self-help, if provided) without reading the code.
All function header comments should describe the intended API behaviour using:
*   Description of the function.
*   Globals: List of global variables used and modified.
*   Arguments: Arguments taken.
*   Outputs: Output to STDOUT or STDERR.
*   Returns: Returned values other than the default exit status of the last
    command run.

### Implementation Comments

Comment tricky, non-obvious, interesting or important parts of your
code.
This follows general Google coding comment practice. Don't comment
everything. If there's a complex algorithm or you're doing something
out of the ordinary, put a short comment in.

### TODO Comments

Use TODO comments for code that is temporary, a short-term solution, or
good-enough but not perfect.
`TODO`s should include the string `TODO` in all caps, followed by the name,
e-mail address, or other identifier of the person with the best context about
the problem referenced by the `TODO`. The main purpose is to have a consistent
`TODO` that can be searched to find out how to get more details upon request. A
`TODO` is not a commitment that the person referenced will fix the problem. Thus
when you create a `TODO`, it is almost always your name that is given.

### Indentation

Indent 2 spaces. No tabs.
Use blank lines between blocks to improve readability. Indentation is
two spaces. Whatever you do, don't use tabs. For existing files, stay
faithful to the existing indentation.
**Exception:** The only exception for using tabs is for the body of `<<-`
tab-indented
[here-document](https://www.gnu.org/software/bash/manual/html_node/Redirections.html#Here-Documents).

### Line Length and Long Strings

Maximum line length is 80 characters.
If you have to write literal strings that are longer than 80 characters, this
should be done with a
[here document](https://www.gnu.org/software/bash/manual/html_node/Redirections.html#Here-Documents)
or an embedded newline if possible.
Words that are longer than 80 chars and can't sensibly be split are ok, but
where possible these items should be on a line of their own, or factored into a
variable. Examples include file paths and URLs, particularly where
string-matching them (such as `grep`) is valuable for maintenance.

### Pipelines

Pipelines should be split one per line if they don't all fit on one line.
If a pipeline all fits on one line, it should be on one line.
If not, it should be split at one pipe segment per line with the pipe on the
newline and a 2 space indent for the next section of the pipe. `\ ` should be
consistently used to indicate line continuation. This applies to a chain of
commands combined using `|` as well as to logical compounds using `||` and `&&`.

### Control Flow

Put `; then` and `; do` on the same line as the `if`, `for`, or `while`.
Control flow statements in shell are a bit different, but we follow the same
principles as with braces when declaring functions. That is: `; then` and `; do`
should be on the same line as the `if`/`for`/`while`/`until`/`select`. `else`
should be on its own line and closing statements (`fi` and `done`) should be on
their own line vertically aligned with the opening statement.

### Case statement

*   Indent alternatives by 2 spaces.
*   A one-line alternative needs a space after the close parenthesis of the
    pattern and before the `;;`.
*   Long or multi-command alternatives should be split over multiple lines with
    the pattern, actions, and `;;` on separate lines.
The matching expressions are indented one level from the `case` and `esac`.
Multiline actions are indented another level. In general, there is no need to
quote match expressions. Pattern expressions should not be preceded by an open
parenthesis. Avoid the `;&` and `;;&` notations.
Simple commands may be put on the same line as the pattern <i>and</i>
`;;` as long as the expression remains readable. This is
often appropriate for single-letter option processing. When the
actions don't fit on a single line, put the pattern on a line on its
own, then the actions, then `;;` also on a line of its own.
When on the same line as the actions, use a space after the close
parenthesis of the pattern and another before the `;;`.

### Variable expansion

In order of precedence: Stay consistent with what you find; quote your
variables; prefer `"${var}"` over `"$var"`.
These are strongly recommended guidelines but not mandatory
regulation. Nonetheless, the fact that it's a recommendation and
not mandatory doesn't mean it should be taken lightly or downplayed.
They are listed in order of precedence.
*   Stay consistent with what you find for existing code.
*   Quote variables, see Quoting section below.
*   Don't brace-delimit single character shell specials / positional parameters,
    unless strictly necessary or avoiding deep confusion.
Prefer brace-delimiting all other variables.

### Quoting

*   Always quote strings containing variables, command substitutions, spaces or
    shell meta characters, unless careful unquoted expansion is required or it's
    a shell-internal integer (see next point).
*   Use arrays for safe quoting of lists of elements, especially command-line
    flags. See Arrays below.
*   Optionally quote shell-internal, readonly
    [special variables](https://www.gnu.org/software/bash/manual/html_node/Special-Parameters.html)
    that are defined to be integers: `$?`, `$#`, `$$`, `$!`. Prefer quoting of
    "named" internal integer variables, e.g. PPID etc for consistency.
*   Prefer quoting strings that are "words" (as opposed to command options or
    path names).
*   Be aware of the quoting rules for pattern matches in `[[ … ]]`. See the
    Test, `[ … ]`, and `[[ … ]]` section below.
*   Use `"$@"` unless you have a specific reason to use `$*`, such as simply
    appending the arguments to a string in a message or log.

### ShellCheck

The [ShellCheck project](https://www.shellcheck.net/) identifies common bugs and
warnings for your shell scripts. It is recommended for all scripts, large or
small.

### Command Substitution

Use `$(command)` instead of backticks.
Nested backticks require escaping the inner ones with `\ `.
The `$(command)` format doesn't change when nested and is
easier to read.

### Test, `[ … ]`, and `[[ … ]]`

`[[ … ]]` is preferred over `[ … ]`, `test` and `/usr/bin/[`.
`[[ … ]]` reduces errors as no pathname expansion or word splitting takes place
between `[[` and `]]`. In addition, `[[ … ]]` allows for pattern and regular
expression matching, while `[ … ]` does not.

### Testing Strings

Use quotes rather than filler characters where possible.
Bash is smart enough to deal with an empty string in a test. So, given
that the code is much easier to read, use tests for empty/non-empty
strings or empty strings rather than filler characters.

### Wildcard Expansion of Filenames

Use an explicit path when doing wildcard expansion of filenames.
As filenames can begin with a `-`, it's a lot safer to
expand wildcards with `./*` instead of `*`.

### Eval

`eval` should be avoided.
Eval munges the input when used for assignment to variables and can
set variables without making it possible to check what those variables
were.

### Arrays

Bash arrays should be used to store lists of elements, to avoid quoting
complications. This particularly applies to argument lists. Arrays
should not be used to facilitate more complex data structures (see
When to use Shell above).
Arrays store an ordered collection of strings, and can be safely
expanded into individual elements for a command or loop.
Using a single string for multiple command arguments should be
avoided, as it inevitably leads to authors using `eval`
or trying to nest quotes inside the string, which does not give
reliable or readable results and leads to needless complexity.

### Arrays Decision

Arrays should be used to safely create and pass around lists. In
particular, when building a set of command arguments, use arrays to
avoid confusing quoting issues. Use quoted expansion –
`"${array[@]}"` – to access arrays. However, if more
advanced data manipulation is required, shell scripting should be
avoided altogether; see above.

### Pipes to While

Use process substitution or the `readarray` builtin (bash4+) in preference to
piping to `while`. Pipes create a subshell, so any variables modified within a
pipeline do not propagate to the parent shell.
The implicit subshell in a pipe to `while` can introduce subtle bugs that are
hard to track down.

### Arithmetic

Always use `(( … ))` or `$(( … ))` rather than
`let` or `$[ … ]` or `expr`.
Never use the `$[ … ]` syntax, the `expr`
command, or the `let` built-in.
`<` and `>` don't perform numerical
comparison inside `[[ … ]]` expressions (they perform
lexicographical comparisons instead; see Testing Strings).
For preference, don't use `[[ … ]]` *at all* for numeric comparisons, use
`(( … ))` instead.
It is recommended to avoid using `(( … ))` as a standalone
statement, and otherwise be wary of its expression evaluating to zero
- particularly with `set -e` enabled. For example,
`set -e; i=0; (( i++ ))` will cause the shell to exit.

### Aliases

Although commonly seen in `.bashrc` files, aliases should be avoided in scripts.
As the
[Bash manual](https://www.gnu.org/software/bash/manual/html_node/Aliases.html)
notes:
> For almost every purpose, shell functions are preferred over aliases.
Aliases are cumbersome to work with because they require carefully quoting and
escaping their contents, and mistakes can be hard to notice.

### Function Names

Lower-case, with underscores to separate words. Separate libraries with `::`.
Parentheses are required after the function name. The keyword `function` is
optional, but must be used consistently throughout a project.
If you're writing single functions, use lowercase and separate words with
underscore. If you're writing a package, separate package names with `::`.
However, functions intended for interactive use may choose to avoid colons as it
can confuse bash auto-completion.
Braces must be on the same line as the function name (as with other languages at
Google) and no space between the function name and the parenthesis.

### Variable Names

Same as for function names.
Variables names for loops should be similarly named for any variable
you're looping through.

### Constants, Environment Variables, and readonly Variables

Constants and anything exported to the environment should be capitalized,
separated with underscores, and declared at the top of the file.

### Source Filenames

Lowercase, with underscores to separate words if desired.
This is for consistency with other code styles in Google:
`maketemplate` or `make_template` but not
`make-template`.

### Use Local Variables

Declare function-specific variables with `local`.
Ensure that local variables are only seen inside a function and its children by
using `local` when declaring them. This avoids polluting the global namespace
and inadvertently setting variables that may have significance outside the
function.
Declaration and assignment must be separate statements when the
assignment value is provided by a command substitution; as the
`local` builtin does not propagate the exit code from the
command substitution.

### Function Location

Put all functions together in the file just below constants. Don't hide
executable code between functions. Doing so makes the code difficult to follow
and results in nasty surprises when debugging.
If you've got functions, put them all together near the top of the
file. Only includes, `set` statements and setting constants
may be done before declaring functions.

### main

A function called `main` is required for scripts long enough
to contain at least one other function.
In order to easily find the start of the program, put the main program in a
function called `main` as the bottom-most function. This provides consistency
with the rest of the code base as well as allowing you to define more variables
as `local` (which can't be done if the main code is not a function). The last
non-comment line in the file should be a call to `main`:
```shell
main "$@"
```
Obviously, for short scripts where it's just a linear flow,
`main` is overkill and so is not required.

### Checking Return Values

Always check return values and give informative return values.
For unpiped commands, use `$?` or check directly via an
`if` statement to keep it simple.

### Builtin Commands vs. External Commands

Given the choice between invoking a shell builtin and invoking a
separate process, choose the builtin.
We prefer the use of builtins such as the
[*Parameter Expansion*](https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html)
functionality provided by `bash` as it's more efficient, robust, and portable
(especially when compared to things like `sed`). See also the
[`=~` operator](https://www.gnu.org/software/bash/manual/html_node/Conditional-Constructs.html#index-_005b_005b).

### When in Doubt: Be Consistent

Using one style consistently through our codebase lets us focus on other (more
important) issues. Consistency also allows for automation. In many cases, rules
that are attributed to “Be Consistent” boil down to “Just pick one and stop
worrying about it”; the potential value of allowing flexibility on these points
is outweighed by the cost of having people argue over them.
However, there are limits to consistency. It is a good tie breaker when there is
no clear technical argument, nor a long-term direction. Consistency should not
generally be used as a justification to do things in an old style without
considering the benefits of the new style, or the tendency of the codebase to
converge on newer styles over time.
