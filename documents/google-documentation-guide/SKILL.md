---
name: google-documentation-guide
description: >-
  Use when planning, writing, or reviewing developer documentation, Markdown, READMEs, and
  documentation maintenance using Google's documentation philosophy and practices. Do not use
  for prose that is not technical documentation.
---

# Google Documentation Guide

Apply this guidance to the actual project. Repository requirements and newer authoritative guidance take precedence.

## Philosophy

### Radical simplicity

*   **Scalability and interoperability** are more important than a menagerie of
    unessential features. Scale comes from simplicity, speed, and ease.
    Interoperability comes from unadorned, digestible content.
*   **Fewer distractions** make for better writing and more productive reading.
*   **New features should never interfere with the simplest use case** and
    should remain invisible to users who don't need them.
*   **Markdown is designed for the average engineer** -- the busy,
    just-want-to-go-back-to-coding engineer. Large and complex documentation is
    possible but not the primary focus.
*   **Minimizing context switching makes people happier.** Engineers should be
    able to interact with documentation using the same tools they use to read
    and write code.

### Readable source text

* **Plain text not only suffices, it is superior**. Markdown itself is not
  essential to this formula, but it is the best and most widely supported
  solution right now. HTML is generally not encouraged.
* **Content and presentation should not mingle**. It should always be possible
  to ditch the renderer and read the essential information at source. Users
  should never have to touch the presentation layer if they don't want to.
* **Portability and future-proofing leave room for the unimagined integrations
  to come**, and are best achieved by keeping the source as human-readable as
  possible.
* **Static content is better than dynamic**, because content should not depend
  on the features of any one server. However, **fresh is better than stale**. We
  strive to balance these needs.


## Documentation Best Practices

### Minimum Viable Documentation

A small set of fresh and accurate docs is better than a large assembly of
"documentation" in various states of disrepair.
Write short and useful documents. Cut out everything unnecessary, including
out-of-date, incorrect, or redundant information. Also make a habit of
continually massaging and improving every doc to suit your changing needs.
**Docs work best when they are alive but frequently trimmed, like a bonsai
tree**.

### Update Docs with Code

**Change your documentation in the same CL as the code change**. This keeps your
docs fresh, and is also a good place to explain to your reviewer what you're
doing.
A good reviewer can at least insist that docstrings, header files, README.md
files, and any other docs get updated alongside the CL.

### Delete Dead Documentation

Dead docs are bad. They misinform, they slow down, they incite despair in
engineers and laziness in team leads. They set a precedent for leaving behind
messes in a code base. If your home is clean, most guests will be clean without
being asked.
Just like any big cleaning project, **it's easy to be overwhelmed**. If your
docs are in bad shape:
*   Take it slow, doc health is a gradual accumulation.
*   First delete what you're certain is wrong, ignore what's unclear.
*   Get your whole team involved. Devote time to quickly scan every doc and make
    a simple decision: Keep or delete?
*   Default to delete or leave behind if migrating. Stragglers can always be
    recovered.
*   Iterate.

### Documentation is the Story of Your Code

Writing excellent code doesn't end when your code compiles or even if your test
coverage reaches 100%. It's easy to write something a computer understands, it's
much harder to write something both a human and a computer understand. Your
mission as a Code Health-conscious engineer is to **write for humans first,
computers second.** Documentation is an important part of this skill.
1.  **Meaningful names**: Good naming allows the code to convey information that
    would otherwise be relegated to comments or documentation. This includes
    nameable entities at all levels, from local variables to classes, files, and
    directories.
2.  **Inline comments**: The primary purpose of inline comments is to provide
    information that the code itself cannot contain, such as why the code is
    there.
3.  **Method and class comments**:
    *   **Method API documentation**: The header / Javadoc / docstring comments
        that say what methods do and how to use them. This documentation is
        **the contract of how your code must behave**. The intended audience is
        future programmers who will use and modify your code.
It is often reasonable to say that any behavior documented here should
have a test verifying it. This documentation details what arguments the
method takes, what it returns, any "gotchas" or restrictions, and what
exceptions it can throw or errors it can return. It does not usually
explain why code behaves a particular way unless that's relevant to a
developer's understanding of how to use the method. "Why" explanations
are for inline comments. Think in practical terms when writing method
documentation: "This is a hammer. You use it to pound nails."
    *   **Class / Module API documentation**: The header / Javadoc / docstring
        comments for a class or a whole file. This documentation gives a brief
        overview of what the class / file does and often gives a few short
        examples of how you might use the class / file.
Examples are particularly relevant when there's several distinct ways to
use the class (some advanced, some simple). Always list the simplest use
case first.
4.  **README.md**: A good README.md orients the new user to the directory and
    points to more detailed explanation and user guides:
    *   What is this directory intended to hold?
    *   Which files should the developer look at first? Are some files an API?
    *   Who maintains this directory and where I can learn more?
5.  **docs**: The contents of a good docs directory explain how to:
    *   Get started using the relevant API, library, or tool.
    *   Run its tests.
    *   Debug its output.
    *   Release the binary.
6.  **Design docs, PRDs**: A good design doc or PRD discusses the proposed
    implementation at length for the purpose of collecting feedback on that
    design. However, once the code is implemented, design docs should serve as
    archives of these decisions, not as half-correct docs (they are often
    misused).
7.  **Other external docs**: Some teams maintain documentation in other
    locations, separate from the code, such as Google Sites, Drive, or wiki.
    If you do maintain documentation in
    other locations, you should clearly point to those locations from your
    project directory (for example, by adding an obvious link to the location
    from your project's `README.md`).

### Duplication is Evil

Do not write your own guide to a common Google technology or process. Link to it
instead. If the guide doesn't exist or it's badly out of date, submit your
updates to the appropriate directory or create a package-level
README.md. **Take ownership and don't be shy**: Other teams will usually welcome
your contributions.


## Markdown style guide

### Better is better than best

The standards for an internal documentation review are different from the
standards for code reviews. Reviewers should ask for improvements, but in
general, the author should always be able to invoke the "Better/Best Rule."
Fast iteration is your friend. To get long-term improvement, **authors must stay
productive** when making short-term improvements. Set lower standards for each
CL, so that **more such CLs** can happen.
As a reviewer of a documentation CL:
1.  When reasonable, LGTM immediately and trust that comments will be fixed
    appropriately.
2.  Prefer to suggest an alternative rather than leaving a vague comment.
3.  For substantial changes, start your own follow-up CL instead. Especially try
    to avoid comments of the form "You should *also*...".
4.  On rare occasions, hold up submission if the CL actually makes the docs
    worse. It's okay to ask the author to revert.

### Character line limit

Markdown content follows the residual convention of an 80-character line limit.
Why? Because it's what most of us do for code.

### Exceptions

Exceptions to the 80-character rule include:
*   Links
*   Tables
*   Headings
*   Code blocks

### Trailing whitespace

Don't use trailing whitespace. Use a trailing backslash to break lines.
Use a trailing backslash, sparingly:
Best practice is to avoid the need for a `<br />` altogether. A pair of newlines
will create a paragraph tag; get used to that.

### Document layout

In general, documents benefit from some variation of the following layout:
```markdown
# Document Title

Short introduction.

[TOC]

## Topic

Content.

## See also

* https://link-to-more-info
```
1.  `# Document title`: The first heading should be a level-one heading, ideally
    the same or nearly the same as the filename. The first level-one heading is
    used as the page `<title>`.
1.  `Short introduction.` 1–3 sentences providing a high-level overview of the
    topic. Imagine yourself as a complete newbie who landed on your "Extending Foo" doc
    and doesn't know the most basic information you take for granted. "What is
    Foo? Why would I extend it?"
1.  `## Topic`: The rest of your headings should start from level 2.
1.  `## See also`: Put miscellaneous links at the bottom for the user who wants
    to know more or didn't find what they needed.

### Use unique, complete names for headings

Use unique and fully descriptive names for each heading, even for sub-sections.
Since link anchors are constructed from headings, this helps ensure that the
automatically-constructed anchor links are intuitive and clear.

### Add spacing to headings

Prefer spacing after `#` and newlines before and after:
```markdown
...text before.

## Heading 2

Text after...
```

### Use a single H1 heading

Use one H1 heading as the title of your document. Subsequent headings should be
H2 or deeper. See Document layout for more information.

### Use lazy numbering for long lists

Markdown is smart enough to let the resulting HTML render your numbered lists
correctly. For longer lists that may change, especially long nested lists, use
"lazy" numbering:
```markdown
1.  Foo.
1.  Bar.
    1.  Foofoo.
    1.  Barbar.
1.  Baz.
```
However, if the list is small and you don't anticipate changing it, prefer fully
numbered lists, because it's nicer to read in source:
```markdown
1.  Foo.
2.  Bar.
3.  Baz.
```

### Nested list spacing

When nesting lists, use a 4-space indent for both numbered and bulleted lists:
```markdown
1.  Use 2 spaces after the item number, so the text itself is indented 4 spaces.
    Use a 4-space indent for wrapped text.
2.  Use 2 spaces again for the next item.

*   Use 3 spaces after a bullet, so the text itself is indented 4 spaces.
    Use a 4-space indent for wrapped text.
    1.  Use 2 spaces with numbered lists, as before.
        Wrapped text in a nested list needs an 8-space indent.
    2.  Looks nice, doesn't it?
*   Back to the bulleted list, indented 3 spaces.
```

### Inline

&#96;Backticks&#96; designate `inline code` that will be rendered literally. Use
them for short code quotations, field names, and more:
```markdown
You'll want to run `really_cool_script.sh arg`.

Pay attention to the `foo_bar_whammy` field in that table.
```
Use inline code when referring to file types in a generic sense, rather than a
specific existing file:
```markdown
Be sure to update your `README.md`!
```

### Codeblocks

For code quotations longer than a single line, use a fenced code block:
<pre>
```python
def Foo(self, bar):
  self.bar = bar
```
</pre>

### Declare the language

It is best practice to explicitly declare the language, so that neither the
syntax highlighter nor the next editor must guess.

### Use fenced code blocks instead of indented code blocks

Four-space indenting is also interpreted as a code block. However, we strongly
recommend fencing for all code blocks.
Indented code blocks can sometimes look cleaner in the source, but they have
several drawbacks:
*   You cannot specify the language. Some Markdown features are tied to language
    specifiers.
*   The beginning and end of the code block are ambiguous.
*   Indented code blocks are harder to search for in Code Search.

### Escape newlines

Because most command-line snippets are intended to be copied and pasted directly
into a terminal, it's best practice to escape any newlines. Use a single
backslash at the end of the line:
<pre>
```shell
$ bazel run :target -- --flag --foo=longlonglonglonglongvalue \
  --bar=anotherlonglonglonglonglonglonglonglonglonglongvalue
```
</pre>

### Links

Long links make source Markdown difficult to read and break the 80 character
wrapping. **Wherever possible, shorten your links**.

### Use explicit paths for links within Markdown

Use the explicit path for Markdown links. For example:
```markdown
[...](/path/to/other/markdown/page.md)
```
You don't need to use the entire qualified URL:
```markdown
[...](https://bad-full-url.example.com/path/to/other/markdown/page.md)
```

### Avoid relative paths unless within the same directory

Relative paths are fairly safe within the same directory. For example:
```markdown
[...](other-page-in-same-dir.md)
[...](/path/to/another/dir/other-page.md)
```
Avoid relative links if you need to specify other directories with `../`:
```markdown
[...](../../bad/path/to/another/dir/other-page.md)
```

### Use informative Markdown link titles

Markdown link syntax allows you to set a link title. Use it wisely. Users often
do not read documents; they scan them.
Links catch the eye. But titling your links "here," "link," or simply
duplicating the target URL tells the hasty reader precisely nothing and is a
waste of space:
```markdown
DO NOT DO THIS.

See the Markdown guide for more info: [link](markdown.md), or check out the
style guide [here](style.md).

Check out a typical test result:
[https://example.com/foo/bar](https://example.com/foo/bar).
```
Instead, write the sentence naturally, then go back and wrap the most
appropriate phrase with the link:
```markdown
See the [Markdown guide](markdown.md) for more info, or check out the
[style guide](style.md).

Check out a
[typical test result](https://example.com/foo/bar).
```

### Use reference links for long links

Use reference links where the length of the link would detract from the
readability of the surrounding text if it were inlined. Reference links make it
harder to see the destination of a link in source text, and add additional
syntax.
Use reference links more often in tables. It is particularly important to keep
table content short, since Markdown does not provide a facility to break text in
cell tables across multiple lines, and smaller tables are more readable.

### Use reference links to reduce duplication

Consider using reference links when referencing the same link destination
multiple times in a document, to reduce duplication.

### Define reference links after their first use

We recommend putting reference link definitions just before the next heading, at
the end of the section in which they're first used. If your editor has its own
opinion about where they should go, don't fight it; the tools always win.
We define a "section" as all text between two headings. Think of reference links
like footnotes, and the current section like the current page.
This arrangement makes it easy to find the link destination in source view,
while keeping the flow of text free from clutter. In long documents with lots of
reference links, it also prevents "footnote overload" at the bottom of the file,
which makes it difficult to pick out the relevant link destination.
There is one exception to this rule: reference link definitions that are used in
multiple sections should go at the end of the document. This avoids dangling
links when a section is updated or moved.

### Images

Use images sparingly, and prefer simple screenshots. This guide is designed
around the idea that plain text gets users down to the business of communication
faster with less reader distraction and author procrastination. However, it's
sometimes very helpful to show what you mean.

### Tables

Use tables when they make sense: for the presentation of tabular data that needs
to be scanned quickly.
Avoid using tables when your data could easily be presented in a list. Lists are
much easier to write and read in Markdown.
*   **Poor distribution**: Several columns don't differ across rows, and some
    cells are empty. This is usually a sign that your data may not benefit from
    tabular display.
*   **Unbalanced dimensions**: There are a small number of rows relative to
    columns. When this ratio is unbalanced in either direction, a table becomes
    little more than an inflexible format for text.
*   **Rambling prose** in some cells. Tables should tell a succinct story at a
    glance.

### Strongly prefer Markdown to HTML

Please prefer standard Markdown syntax wherever possible and avoid HTML hacks.
If you can't seem to accomplish what you want, reconsider whether you really
need it. Except for big tables, Markdown meets almost all needs
already.
Every bit of HTML hacking reduces the readability and portability of our
Markdown corpus. This in turn limits the usefulness of integrations with other
tools, which may either present the source as plain text or render it. See
Philosophy.


## READMEs

### Overview

A README is a short summary of the contents of a directory. The contents of the
file are displayed in GitHub and Gitiles when you view the contents of the
containing directory. README files provide critical information for people
browsing your code, especially first-time users.

### Where to put your README

Unlike all other Markdown files, `README.md` files should not be located inside
your product or library's documentation directory. `README.md` files should be
located in the top-level directory for your product or library's actual
codebase.
All top-level directories for a code package should have an up-to-date
`README.md` file. This is especially important for package directories that
provide interfaces for other teams.

### What to put in your README

At a minimum, your `README.md` file should contain a link to your user- and/or
team-facing documentation.
Every package-level `README.md` should include or point to the following
information:
1.  What is in this package or library and what's it used for.
1.  Points of contact.
1.  Status of whether this package or library is deprecated, or not for general
    release, etc.
1.  How to use the package or library. Examples include sample code, copyable
    `bazel run` or `bazel test` commands, etc.
1.  Links to relevant documentation.
