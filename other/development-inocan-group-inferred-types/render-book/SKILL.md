---
name: render-book
description: Render the book into HTML or PDF formats using Quarto. Use when the user wants to "render the book", "build the book", "generate the book", or create HTML/PDF output.
---

# Rendering Book

Render the "Data Science with Python" book into HTML or PDF formats using Quarto.

**Why?** Automates the Quarto commands required to build the book, ensuring consistent output for both web (HTML) and print (PDF) formats.

## Quick Start

1. **Check Dependencies**: Ensure Python venv and Quarto are installed.
2. **Activate venv**: `source .venv/bin/activate`
3. **Choose Format**: HTML (default) or PDF.
4. **Execute**: Run the appropriate command.
5. **Verify**: Check logs and output files.

## Prerequisites

- **Python Environment**: Must have Python 3.11+ installed.
- **Virtual Environment**: Create and activate venv:
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```
- **Quarto**: Must have Quarto installed:
    ```bash
    brew install --cask quarto
    ```

## Workflow Steps

### 1. Preview (Development)

Live preview with auto-reload on file changes.

```bash
source .venv/bin/activate
quarto preview
```

> [!TIP]
> The preview will open automatically in your browser at `http://localhost:4XXX`.

### 2. Render HTML

This is the default and most common format.

```bash
source .venv/bin/activate
quarto render
```

> [!TIP]
> The output will be generated in `docs/index.html`.

### 3. Render PDF

Use this for generating the print version.

> [!NOTE]
> PDF generation uses LaTeX (LuaLaTeX). TinyTeX will auto-install required packages.

> [!IMPORTANT]
> Always use `--no-clean` to preserve the `docs/data/` folder which contains static datasets.

```bash
source .venv/bin/activate
quarto render --to pdf --no-clean
```

### 4. Quality Check

After rendering, verify output:

```bash
ls -la docs/index.html
ls -la docs/*.pdf
```

## Verification

Verify the output exists and was recently modified (within last 5 minutes):

```bash
# Verify HTML
find docs/ -name "index.html" -mmin -5

# Verify PDF
find docs/ -name "*.pdf" -mmin -5
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `command not found: quarto` | Quarto not installed | Run `brew install --cask quarto` |
| `jupyter not found` | Missing Python packages | Run `pip install -r requirements.txt` |
| PDF callout error | Typst/callout compatibility | Use HTML output or switch to LaTeX |
| Slow build | Many chapters with plots | Wait; Quarto caches execution |

## Common Mistakes

1. **Running without venv active**: Always activate the virtual environment first.
   ```bash
   # Wrong - will fail
   quarto render

   # Correct
   source .venv/bin/activate && quarto render
   ```

2. **Editing `docs/` directly**: Never edit files in `docs/`. They get overwritten on each render. Edit the `.qmd` source files instead.

3. **Forgetting to save `.qmd` files**: Ensure all changes are saved before rendering.

## Sample Output

**Successful HTML build:**
```
Output created: docs/index.html
```

**Successful preview:**
```
Watching files for changes
Browse at http://localhost:4846/
```

## Quality Rules

- **Always activate venv**: Ensure Python dependencies are available.
- **Check output before committing**: Always verify that `docs/index.html` was updated.
- **Clean build for major changes**: If output looks wrong, delete freeze and rebuild:
  ```bash
  rm -rf _freeze docs/* && quarto render
  ```
