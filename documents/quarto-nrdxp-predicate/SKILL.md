---
name: quarto
description: |
  Formatting, structure, and execution rules for Quarto markdown documents.
  Trigger when:
  - Writing, editing, or rendering Quarto documents, reports, presentations, or websites.
  - Files matching the pattern **/*.qmd are in the workspace or referenced.
  - Tasks involve: quarto render, quarto preview, knitr, jupyter.
  - Prompt contains keywords: quarto, qmd, yaml header, code chunk, callout, cross-reference.
---

# Quarto (.qmd) Authoring Rules

Quarto is a superset of Pandoc Markdown. It prioritizes semantic structure over visual formatting.

> **Golden Rule:** Never use raw HTML tags (`<div>`, `<img>`, `<br>`) unless absolutely necessary. Use Pandoc Fenced Divs and Spans.

> **Official Documentation:** [quarto.org/docs](https://quarto.org/docs/) is the authoritative reference. Consult it for edge cases, advanced features, or when this skill lacks specifics.

---

## 1. Block Structure (Fenced Divs)

Quarto uses **Fenced Divs** (`:::`) to define layout, callouts, and structural blocks. More colons (`:::::`) enable nesting.

### Callouts (Alerts)

Convert standard Markdown blockquotes (`>`) into semantic callouts.

| Type          | Syntax                     | Use Case                     |
| :------------ | :------------------------- | :--------------------------- |
| **Note**      | `::: {.callout-note}`      | Non-critical info            |
| **Tip**       | `::: {.callout-tip}`       | Best practices/optimizations |
| **Important** | `::: {.callout-important}` | Key constraints              |
| **Warning**   | `::: {.callout-warning}`   | Failure modes                |
| **Caution**   | `::: {.callout-caution}`   | Data loss risks              |

**Features:**

- **Title:** Use a `##` heading inside, or the `title="..."` attribute.
- **Collapse:** Add `collapse="true"` for expandable callouts (collapsed by default).
- **Appearance:** `appearance="simple"` or `appearance="minimal"` for alternate styles.
- **Icons:** `icon=false` to suppress the default icon.

```markdown
::: {.callout-caution collapse="true" appearance="simple"}

## Warning Title

Collapsible content.
:::
```

### Multi-Column Layouts

Do not use HTML tables or CSS grids for layout. Use Quarto layout divs.

```markdown
:::: {.columns}

::: {.column width="40%"}
Left content (e.g., text)
:::

::: {.column width="60%"}
Right content (e.g., image or code)
:::

::::
```

### Tabsets

Group content into switchable tabs using the `.panel-tabset` class.

```markdown
::: {.panel-tabset}

## Python

Python code here...

## R

R code here...

:::
```

### Layout Classes

Control content width using column classes:

| Class            | Width                            |
| ---------------- | -------------------------------- |
| `.column-body`   | Default text column              |
| `.column-page`   | Extends into page margins        |
| `.column-screen` | Full viewport width              |
| `.column-margin` | Right margin (for notes, asides) |

```markdown
::: {.column-margin}
This appears in the margin.
:::

::: {.column-page}
![Wide figure](wide.png)
:::
```

---

## 2. Cross-Referencing (Strict)

Quarto requires specific ID prefixes for automatic numbering. **Do not manually number sections, figures, or tables.**

### The Prefix Rule

You **MUST** use these prefixes in curly braces `{#...}` to enable referencing:

| Element          | Prefix | Example ID      | Reference Syntax |
| ---------------- | ------ | --------------- | ---------------- |
| **Figures**      | `fig-` | `{#fig-arch}`   | `@fig-arch`      |
| **Tables**       | `tbl-` | `{#tbl-stats}`  | `@tbl-stats`     |
| **Sections**     | `sec-` | `{#sec-deploy}` | `@sec-deploy`    |
| **Equations**    | `eq-`  | `{#eq-perf}`    | `@eq-perf`       |
| **Listings**     | `lst-` | `{#lst-main}`   | `@lst-main`      |
| **Theorems**     | `thm-` | `{#thm-main}`   | `@thm-main`      |
| **Lemmas**       | `lem-` | `{#lem-helper}` | `@lem-helper`    |
| **Corollaries**  | `cor-` | `{#cor-result}` | `@cor-result`    |
| **Propositions** | `prp-` | `{#prp-claim}`  | `@prp-claim`     |
| **Conjectures**  | `cnj-` | `{#cnj-open}`   | `@cnj-open`      |
| **Definitions**  | `def-` | `{#def-term}`   | `@def-term`      |
| **Examples**     | `exm-` | `{#exm-basic}`  | `@exm-basic`     |
| **Exercises**    | `exr-` | `{#exr-prob1}`  | `@exr-prob1`     |
| **Solutions**    | `sol-` | `{#sol-ans}`    | `@sol-ans`       |
| **Algorithms**   | `alg-` | `{#alg-sort}`   | `@alg-sort`      |

> **LaTeX Warning:** Avoid underscores (`_`) in IDs. They cause issues when rendering to PDF.

**Reserved Prefixes (full list):** `fig`, `tbl`, `lst`, `tip`, `nte`, `wrn`, `imp`, `cau`, `thm`, `lem`, `cor`, `prp`, `cnj`, `def`, `exm`, `exr`, `sol`, `rem`, `alg`, `eq`, `sec`

**Wrong:** `See [Figure 1](#figure-1)`
**Right:** `See @fig-arch`

### Figure Syntax

Images require an ID and a caption (the alt text) to be treated as a Figure.

```markdown
![System Architecture Diagram](images/arch.png){#fig-arch}
```

**Subfigures** use a parent div with `layout-ncol`:

```markdown
::: {#fig-panels layout-ncol=2}

![First](a.png){#fig-first}

![Second](b.png){#fig-second}

Panel caption here.
:::
```

### Table Syntax

Tables must have a caption definition (`: ...`) and an ID to be referenceable.

```markdown
| Component | Status |
| :-------- | :----- |
| API       | Stable |

: System Status {#tbl-status}
```

**Column Widths:** Use `tbl-colwidths` to control proportions:

```markdown
: Caption {#tbl-id tbl-colwidths="[60,40]"}
```

### Grid Tables

For complex cells (lists, code blocks, multiple paragraphs), use grid tables:

```markdown
+---------------+---------------+
| Fruit | Advantages |
+===============+===============+
| Bananas | - Portable |
| | - Bright |
+---------------+---------------+
| Oranges | - Vitamin C |
| | - Tasty |
+---------------+---------------+

: Grid table with lists {#tbl-grid}
```

---

## 3. Code Blocks & Execution

Distinguish between **Display Code** and **Executable Code**.

### Display Only (Standard Markdown)

Use standard triple backticks for static snippets.

````markdown
```rust
fn main() { ... }
```
````

### Executable Code (Computation)

Use curly braces `{python}` to indicate the engine should execute the block. Use hash-pipes `#|` for options.

````markdown
```{python}
#| label: fig-plot
#| fig-cap: "Performance metrics"
#| echo: false

import matplotlib.pyplot as plt
plt.plot([1,2,3])
```
````

### Execution Options

Options can be set globally (in YAML `execute:` block) or per-cell (with `#|`).

| Option      | Values                    | Effect                                      |
| ----------- | ------------------------- | ------------------------------------------- |
| `eval`      | `true`, `false`           | Whether to run the code                     |
| `echo`      | `true`, `false`, `fenced` | Show source code in output                  |
| `output`    | `true`, `false`, `asis`   | Show/suppress output; `asis` = raw markdown |
| `warning`   | `true`, `false`           | Show/hide warnings                          |
| `error`     | `true`, `false`           | Allow errors (`true` continues on error)    |
| `include`   | `true`, `false`           | Include cell in output at all               |
| `code-fold` | `true`, `false`, `show`   | Collapsible source code                     |

---

## 4. Diagrams (Mermaid)

Do not use images for diagrams if they can be defined as code. Quarto renders Mermaid natively.

````markdown
```{mermaid}
%%| label: fig-flow
%%| fig-cap: "Authentication Flow"

sequenceDiagram
    User->>API: Request
    API-->>User: Response
```
````

---

## 5. Metadata & Configuration (YAML)

### Document Header

Every `.qmd` file should start with YAML frontmatter.

```yaml
---
title: "Technical Specification"
author: "Engineering Team"
date: last-modified
format:
  html:
    toc: true
    number-sections: true
    code-fold: true
    theme: cosmo
  pdf:
    toc: true
    number-sections: true
---
```

### Global Execution Options

```yaml
execute:
  echo: true # Show code by default
  warning: false # Hide warnings
  freeze: auto # Only re-execute changed documents
```

### Project Configuration (`_quarto.yml`)

For multi-document projects (books, websites):

```yaml
project:
  type: book # or: website, manuscript, default

book:
  title: "My Book"
  chapters:
    - index.qmd
    - intro.qmd
    - part: "Main Content"
      chapters:
        - chapter1.qmd
        - chapter2.qmd
```

---

## 6. Shortcodes (Special Features)

Use Quarto shortcodes `{{< ... >}}` for special elements.

| Shortcode                           | Purpose                                |
| ----------------------------------- | -------------------------------------- |
| `{{< pagebreak >}}`                 | Force a page break (PDF/Docx)          |
| `{{< include _file.qmd >}}`         | Embed another file (partial)           |
| `{{< embed notebook.ipynb#cell >}}` | Embed output from another notebook/qmd |
| `{{< video src >}}`                 | Embed video players                    |
| `{{< var version >}}`               | Insert variable from `_variables.yml`  |
| `{{< meta title >}}`                | Insert value from document metadata    |
| `{{< env VAR_NAME >}}`              | Insert environment variable            |

**Include/Embed Rules:**

- Shortcodes must appear on their own line, surrounded by blank lines.
- Use absolute paths from project root for reliability.

---

## 7. Citations & Bibliography

Quarto uses Pandoc citation syntax with a bibliography file.

**YAML Setup:**

```yaml
---
bibliography: references.bib
csl: apa.csl # Optional: citation style
---
```

**Citation Syntax:**

| Syntax                | Renders As               |
| --------------------- | ------------------------ |
| `[@smith2023]`        | (Smith 2023)             |
| `@smith2023`          | Smith (2023) inline      |
| `[@smith2023, p. 42]` | (Smith 2023, p. 42)      |
| `[-@smith2023]`       | (2023) — suppress author |
| `[@a; @b]`            | Multiple citations       |

---

## 8. Raw Format Blocks

Embed format-specific content (ignored in other formats):

````markdown
```{=latex}
\begin{center}
LaTeX-only content
\end{center}
```
````

````markdown
```{=html}
<details><summary>HTML-only</summary>Content</details>
```
````

**Inline:** Use `` `\LaTeX`{=latex} `` for inline raw content.

---

## 9. Inline Spans

Apply attributes to inline text using `[text]{.class #id key="value"}`.

```markdown
This is [important text]{.highlight} with inline styling.
```

---

## Anti-Patterns

| Anti-Pattern           | Description                 | Remedy                                           |
| ---------------------- | --------------------------- | ------------------------------------------------ |
| **Raw HTML**           | `<div class="alert">`       | Use `::: {.callout-note}`                        |
| **Hardcoded Numbers**  | "As seen in Figure 3"       | Use "As seen in @fig-xyz"                        |
| **Manual TOC**         | Writing out a list of links | Use `toc: true` in YAML                          |
| **Remote Images**      | Hotlinking images           | Download to `/images` or use repo-relative paths |
| **Empty Lines**        | Using `<br>` for spacing    | Use CSS classes or margin attributes             |
| **Underscores in IDs** | `{#my_figure_1}`            | Use hyphens: `{#my-figure-1}`                    |

---

## Migration Checklist (Markdown → Quarto)

1. **Header:** Add YAML frontmatter with `title`, `format`, and `toc`.
2. **Alerts:** Regex replace `> **Note:**` with `::: {.callout-note}` blocks.
3. **Images:** Add `{#fig-name}` to all image links that need captions.
4. **Links:** Convert local section links `[Link](#heading)` to `@sec-heading`.
5. **Diagrams:** Convert static diagram images to `mermaid` blocks where possible.
6. **IDs:** Replace underscores with hyphens in all identifiers.
7. **Tabsets:** Convert manual tab implementations to `::: {.panel-tabset}`.
8. **Citations:** Convert manual citations to `[@key]` with a `.bib` file.
9. **Project:** For multi-file docs, create `_quarto.yml` to define structure.

---

## Output Formats

Quarto supports multiple output formats via the `format:` key:

| Format       | Value      | Notes                            |
| ------------ | ---------- | -------------------------------- |
| HTML         | `html`     | Default, interactive             |
| PDF          | `pdf`      | Requires LaTeX                   |
| Word         | `docx`     | MS Word                          |
| Presentation | `revealjs` | Slides via Reveal.js             |
| Book         | `book`     | Multi-chapter (in `_quarto.yml`) |
| Typst        | `typst`    | Modern PDF alternative           |

```yaml
format:
  html: default
  pdf:
    documentclass: article
  revealjs:
    theme: dark
```