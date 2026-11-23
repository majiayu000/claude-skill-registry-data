---
name: pypi-rstobj
description: "API reference for rstobj 2.0.1, a Python library that builds reStructuredText markup and directives from dataclasses and renders them to text: Header, BulletList, EnumList, URI, Reference, ListTable, Image, CodeBlockPython and other code blocks, TableOfContent, Include. Use when code generates .rst files or Sphinx pages from Python data with rstobj."
---

# rstobj 2.0.1

rstobj builds reStructuredText from Python objects: create a dataclass such as `ListTable(data=...)`, call `.render()`, and get the reST text. Typical use is generating Sphinx pages or `.rst` files from data, often inside a jinja2 template (`{{ table.render() }}`) or with `sphinx-jinja`.

## Import

```python
import rstobj.api as rstobj        # then rstobj.markup.Header, rstobj.directives.ListTable
from rstobj.api import markup, directives
```

## Rules that apply to every class

- All fields are **keyword-only**: `Header(title="Intro")`, never `Header("Intro")`.
- `obj.render(indent=None, first_line_indent=None) -> str`. `indent=n` indents every line by n tabs (4 spaces); `first_line_indent=m` sets the first line's indent separately. Blank lines stay empty.
- **Strings are raw reST, never escaped.** `"*x*"` renders as emphasis; a backtick in a link title breaks the link. Escape yourself if needed.
- A list item or table cell may be a string, a number, or another rstobj object (it is rendered and indented to fit). One item holds **one** thing; for "text with a nested list under it", put both in one string: `"Title\n\n" + rstobj.markup.BulletList(items=[...]).render().strip("\n")`.
- In a string, a single `\n` inside a paragraph is a space in reST; use `\n\n` for a new paragraph.
- Output framing differs by class: `Header*`, `BulletList`, `EnumList` start with `"\n"`; `Image`, `ListTable`, `TableOfContent`, `Include` end with `"\n"`. Join pieces with `"\n\n".join(...)` and strip if you need exact spacing.

## Public API

### `rstobj.markup`

- `Header(title: str, header_level: int = 1, ref_label: str | None = None, auto_label: bool = False, bar_length: int | None = None)`: section title with an underline (`=`, `-`, `~`, `+`, `*`, `#`, `^` for levels 1-7). `auto_label=True` adds a `.. _<slug>:` label from the title. The underline is at least the title's display width (CJK counts double). `ValueError` if `header_level` is not 1-7.
- `Header1` ... `Header7(title, ref_label=None, auto_label=False, bar_length=None)`: `Header` with a fixed level.
- `BulletList(items: list)`: `- item` lines.
- `EnumList(items: list, start_num: int = 1)`: `1. item` lines, numbered from `start_num`.
- `URI(title: str, link: str)`, alias `URL`: `` `title <link>`_ ``.
- `Reference(title: str, label: str)`, alias `Ref`: Sphinx `` :ref:`title <label>` ``.

### `rstobj.directives`

Directives also take `class_: str | None` and `name: str | None` (`:class:`, `:name:`).

- `ListTable(data: list[list], title: str = "", index: bool = False, header: bool = True, widths: list[int] | None = None, align: str | None = None)`: `.. list-table::`. `header` makes row 1 the header; `index` makes column 1 a stub column; `align` is `"left"`, `"center"`, or `"right"` (`ListTable.AlignOptions`).
- `Image(uri: str, height: int | None = None, width: int | None = None, scale: int | None = None, alt_text: str | None = None, align: str | None = None)`: `.. image::`. `height`/`width` in px, `scale` in %. `align`: `Image.AlignOptions` (`left`/`center`/`right` for a standalone image).
- `Code(text: str)`: plain code text, the content of a code block.
- `CodeBlock(code: Code)`: `.. code-block::` without a language. `CodeBlock.from_string(text) -> CodeBlock`.
- `CodeBlockPython`, `CodeBlockBash`, `CodeBlockSQL`, `CodeBlockJavaScript`, `CodeBlockHTML`, `CodeBlockCSS`, `CodeBlockC`, `CodeBlockCPP`, `CodeBlockRuby`, `CodeBlockR`, `CodeBlockPerl`, `CodeBlockScala`, `CodeBlockMake`, `CodeBlockLua`, `CodeBlockRst`, `CodeBlockMarkdown`: same fields and `from_string`, with that language.
- `CodeBlockBase`: base class of the above; `CodeBlockBase.LangOptions` lists the language names.
- `CodeBlockEmpty(code: Code)`: a `::` literal block; `from_string(text)`. It has no options, so `class_`/`name` are ignored.
- `TableOfContent(title: str | None = None, depth: int | None = None, local: bool = False, backlinks: str | None = None)`: `.. contents::`. `backlinks`: `"entry"`, `"top"`, `"none"` (`TableOfContent.BacklinksOptions`). `name` is ignored (`contents` has no `:name:`).
- `Include(path: str, start_line=None, end_line=None, start_after=None, end_before=None, literal: bool | None = None, code: str | None = None, number_lines=None, encoding=None, tab_width=None)`: `.. include::` with docutils' options (`:start-line:` ...).

## Example

```python
import rstobj.api as rstobj

header = rstobj.markup.Header(title="Users", header_level=2, auto_label=True)
table = rstobj.directives.ListTable(
    data=[["id", "name"], [1, "Alice"], [2, "Bob"]],
    title="Users",
)
rst = header.render().strip("\n") + "\n\n" + table.render()
```

## More detail

For every field, the rendered output of each class, and more examples, see `ref/public-api.md`.
