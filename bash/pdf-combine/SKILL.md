---
name: pdf-combine
description: >-
  Combine multiple PDF files into a single PDF. Use when: (1) User wants to merge PDF files, (2)
  User mentions 'combine PDFs', 'merge PDFs', or 'join PDFs', (3) User has multiple PDFs that need
  to be consolidated. Respects file order: when given a directory, files are sorted alphabetically;
  when given specific file paths, the order provided is preserved.
---

# Combine PDF Files

Combine multiple PDF files into a single PDF document.

## Usage

The user can specify:
- A directory containing PDF files (files will be sorted alphabetically by filename)
- Multiple specific PDF file paths (order is preserved as given)
- Output file path for the combined PDF

## Script Details

- **Script location**: `$HOME/.claude/skills/pdf-combine/scripts/combine_pdfs.py`
- **Dependency**: PyMuPDF (fitz) - `pip install PyMuPDF`

## Instructions

1. Determine the source PDF files:
  - If user provides a directory, all PDFs in that directory will be combined in alphabetical order
  - If user provides specific file paths, use them in the exact order provided

2. Determine the output file path:
  - If user specifies an output path, use it
  - If not specified, ask the user for the output file name/path

3. Run the combine script:
   ```bash
   python3 $HOME/.claude/skills/pdf-combine/scripts/combine_pdfs.py <input1.pdf> <input2.pdf> ... -o <output.pdf>
   ```

   Or for a directory:
   ```bash
   python3 $HOME/.claude/skills/pdf-combine/scripts/combine_pdfs.py <directory> -o <output.pdf>
   ```

4. Report the results to the user (number of files combined, total pages, output location)

## Examples

### Combine specific files in order

```bash
python3 $HOME/.claude/skills/pdf-combine/scripts/combine_pdfs.py \
  chapter1.pdf chapter2.pdf chapter3.pdf \
  -o book.pdf
```

### Combine all PDFs in a directory (alphabetical order)

```bash
python3 $HOME/.claude/skills/pdf-combine/scripts/combine_pdfs.py \
  ./documents/ \
  -o combined.pdf
```

## Order Rules

- **Directory input**: Files are sorted alphabetically by filename (case-insensitive)
- **Explicit file list**: Files are combined in the exact order provided by the user
- If user wants a specific order for files in a directory, they should provide the files explicitly

## Error Handling

- If a file doesn't exist, the script will report an error
- If no PDF files are found in a directory, the script will report an error
- Non-PDF files are skipped with a warning
