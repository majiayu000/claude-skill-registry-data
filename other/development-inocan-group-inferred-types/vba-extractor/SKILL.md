---
name: vba-extractor
description: Extract VBA/macro code from Microsoft Office files (.xlsm, .xlsb, .docm, .pptm). This skill should be used when users want to read, view, or extract VBA macros from Excel workbooks or other Office documents containing embedded VBA projects.
---

# VBA Extractor

Extract and display VBA macro code from Microsoft Office files.

## Overview

This skill enables extraction of VBA (Visual Basic for Applications) code from Office files with embedded macros. VBA code is stored in a compressed binary format inside Office files and requires specialized tools to extract.

## Supported File Types

- `.xlsm` - Excel Macro-Enabled Workbook
- `.xlsb` - Excel Binary Workbook
- `.docm` - Word Macro-Enabled Document
- `.pptm` - PowerPoint Macro-Enabled Presentation
- `.xls` - Legacy Excel files (97-2003)
- `.doc` - Legacy Word files (97-2003)

## Workflow

### Step 1: Verify Python and oletools

The extraction requires Python with the `oletools` package:

```bash
python --version
pip install oletools
```

If `oletools` is not installed, install it first.

### Step 2: Extract VBA Code

Run `olevba` with the `-c` flag to extract only the code (no analysis):

```bash
python -m oletools.olevba "<path-to-file>" -c > vba_code.txt
```

The `-c` flag outputs only the VBA source code without the security analysis.

### Step 3: Read the Output

Read the generated `vba_code.txt` file to view the extracted VBA code.

## Common Issues

### Windows Encoding Errors

On Windows, the console may fail with Unicode encoding errors. To avoid this, always redirect output to a file:

```bash
python -m oletools.olevba "file.xlsm" -c > output.txt 2>nul
```

### No VBA Project Found

If no VBA is found, the file may not contain macros or may be a different format (e.g., `.xlsx` instead of `.xlsm`).

## Alternative Approaches (Not Recommended)

JavaScript libraries like `cfb`, `xlsx`, and `ole-doc` can read the VBA project structure but cannot reliably decompress the VBA source code. The Microsoft VBA compression algorithm is proprietary and these libraries lack proper decompression support.

**What works:** Python's `oletools` library
**What doesn't work reliably:** JavaScript-based extraction

## Output Format

The extracted output includes:
- Module names (e.g., `CropBoxes.bas`, `Sheet1.cls`)
- Full VBA source code for each module
- Separation markers between modules

Example output structure:
```
VBA MACRO ModuleName.bas
in file: xl/vbaProject.bin - OLE stream: 'VBA/ModuleName'
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Sub MySub()
    ' VBA code here
End Sub
```
