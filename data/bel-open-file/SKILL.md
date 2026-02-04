---
name: bel-open-file
description: This skill should be used when the user wants to open or preview a file that already exists on disk using the operating system's default application. Triggers on requests like "open this file", "show me the PDF", "preview the image", "view the document", or "display the spreadsheet". Works with all file types including PDFs, images, documents, emails, and spreadsheets.
---

# Open File with OS Default Application

Open any file on disk using the operating system's default application for viewing.

## When to Use This Skill

Use this skill when the user wants to:
- Open a file that already exists on disk
- Preview a document, image, PDF, or spreadsheet
- View a file with the default application
- Display a file that has already been saved

**Trigger phrases:**
- "Open the file contract.pdf"
- "Show me the document in _RESULTS_FROM_AGENT/report.docx"
- "Preview the image logo.png"
- "View this spreadsheet"
- "Display the PDF I downloaded earlier"
- "Open the email attachment"

**Do NOT use this skill if:**
- The file needs to be downloaded from the database first (use `bel-download-file-from-crm-db` instead)
- The user wants to view a file from the database (use `bel-show-crm-file` instead)
- The file doesn't exist on disk yet

## How to Use This Skill

### Quick Start

Simply execute the script with the file path:

```bash
python scripts/open_file.py <file_path>
```

**Examples:**
```bash
# Open a PDF
python scripts/open_file.py _RESULTS_FROM_AGENT/contract.pdf

# Open an image
python scripts/open_file.py _DATA_FROM_USER/logo.png

# Open a spreadsheet
python scripts/open_file.py _RESULTS_FROM_AGENT/report.xlsx

# Open an email file
python scripts/open_file.py _DOWNLOADS_FROM_AGENT/message.eml

# Quiet mode (suppress output)
python scripts/open_file.py document.pdf --quiet
```

### Supported File Types

The script works with **any file type** that has a registered default application on the operating system:

**Documents:**
- PDF: `.pdf`
- Word: `.docx`, `.doc`
- Text: `.txt`, `.md`, `.log`
- Rich Text: `.rtf`

**Spreadsheets:**
- Excel: `.xlsx`, `.xls`, `.csv`
- Numbers: `.numbers`

**Images:**
- Common formats: `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.svg`
- Professional formats: `.tif`, `.tiff`, `.webp`

**Emails:**
- Email messages: `.eml`, `.msg`
- Outlook: `.pst`

**Archives:**
- Compressed files: `.zip`, `.tar`, `.gz`, `.7z`

**Presentations:**
- PowerPoint: `.pptx`, `.ppt`
- Keynote: `.key`

**And many more!** If the OS has a default application registered, this skill will open it.

## Cross-Platform Support

The script automatically detects the operating system and uses the appropriate command:

**macOS:**
- Command: `open <file>`
- Opens files with the default macOS application

**Linux:**
- Command: `xdg-open <file>`
- Opens files with the default Linux desktop application

**Windows:**
- Command: `os.startfile(<file>)`
- Opens files with the default Windows application

## Technical Details

### How It Works

1. Validates that the file exists on disk
2. Resolves to absolute path for reliability
3. Detects the operating system
4. Executes the appropriate OS command to open the file
5. Returns success/error status

### Error Handling

Common errors:
- **File not found:** The specified file path doesn't exist
- **Permission denied:** Insufficient permissions to access the file
- **No default application:** No application registered for that file type
- **Command not found:** `xdg-open` not available on Linux (rare)

## Integration with Other Skills

This skill integrates with:
- **`bel-download-file-from-crm-db`**: First download, then open
- **`bel-show-crm-file`**: Orchestration skill that uses both download and open
- Any skill that produces output files that need to be viewed

## Example Workflows

### Workflow 1: Open a specific file
```
User: "Open the contract.pdf file"

1. Verify file exists at specified path
2. Run: python scripts/open_file.py contract.pdf
3. File opens in default PDF viewer
```

### Workflow 2: Preview downloaded results
```
User: "Show me the report I generated"

1. Identify the file path (e.g., _RESULTS_FROM_AGENT/report.xlsx)
2. Run: python scripts/open_file.py _RESULTS_FROM_AGENT/report.xlsx
3. File opens in default spreadsheet application
```

### Workflow 3: View user-provided data
```
User: "Display the image I uploaded"

1. Find the image in _DATA_FROM_USER/
2. Run: python scripts/open_file.py _DATA_FROM_USER/logo.png
3. Image opens in default image viewer
```

## Notes on Email Files

**Email files (.eml, .msg) work well with this skill:**
- `.eml` files: Standard email format, opens in default mail client (Mail.app on macOS, Outlook on Windows, Thunderbird on Linux)
- `.msg` files: Outlook format, opens in Outlook or compatible email client

The operating system handles the rendering and display automatically.
