---
name: file-type-defaults
description: Set default applications for file types on macOS using utiluti. Use when setting file type associations, changing default apps for extensions, or managing macOS file handlers.
---

# File Type Defaults

Set default applications for file types on macOS using the `utiluti` command-line tool.

## Prerequisites

Ensure `utiluti` is installed:

```bash
brew install utiluti
```

## Instructions

### Recommended Approach: File-based Method

The most reliable method is to use `utiluti file set` with a sample file. This works even for extensions with dynamic UTIs.

#### Step 1: Get application bundle ID

```bash
osascript -e 'id of app "Application Name"'
```

#### Step 2: Set default using an existing file

```bash
# Use an existing file of that type (preferred)
utiluti file set /path/to/existing/file.<extension> <bundle-id>

# OR create a sample file if needed
touch /tmp/sample.<extension>
utiluti file set /tmp/sample.<extension> <bundle-id>
```

Example:

```bash
osascript -e 'id of app "Cursor"'
# Returns: com.todesktop.230313mzl4w4u92

# Using an existing .conf file
utiluti file set ~/.dotfiles/tmux/tmux.conf com.todesktop.230313mzl4w4u92

# Or using a temporary sample file
touch /tmp/sample.conf
utiluti file set /tmp/sample.conf com.todesktop.230313mzl4w4u92
```

### Alternative: UTI-based Method (for well-known types)

This method works for file types with standard, non-dynamic UTIs.

#### Step 1: Get UTI for file extension

```bash
utiluti get-uti <extension>
```

Example:

```bash
utiluti get-uti txt
# Returns: public.plain-text

utiluti get-uti md
# Returns: net.daringfireball.markdown

utiluti get-uti pdf
# Returns: com.adobe.pdf
```

#### Step 2: Set default application

```bash
utiluti type set <uti> <bundle-id>
```

Example:

```bash
utiluti type set public.plain-text com.barebones.bbedit
```

**Note:** Some file extensions (like `.conf`) have dynamic UTIs (e.g., `dyn.ah62d4rv4ge80g55sq2`) that cannot be set using `utiluti type set`. Use the file-based method instead.

### Finding application bundle IDs

Use `osascript` to find an application's bundle ID:

```bash
osascript -e 'id of app "Application Name"'
```

Examples:

```bash
osascript -e 'id of app "Visual Studio Code"'
# Returns: com.microsoft.VSCode

osascript -e 'id of app "BBEdit"'
# Returns: com.barebones.bbedit

osascript -e 'id of app "Preview"'
# Returns: com.apple.Preview
```

## Common Use Cases

### Configuration files (.conf) to Cursor

```bash
# Using an existing .conf file (recommended)
utiluti file set ~/.dotfiles/tmux/tmux.conf com.todesktop.230313mzl4w4u92

# Or using a temporary file
touch /tmp/sample.conf
utiluti file set /tmp/sample.conf com.todesktop.230313mzl4w4u92
```

### Text files to BBEdit (UTI method)

```bash
utiluti get-uti txt
utiluti type set public.plain-text com.barebones.bbedit
```

### Markdown files to Visual Studio Code (UTI method)

```bash
utiluti get-uti md
utiluti type set net.daringfireball.markdown com.microsoft.VSCode
```

### JSON files to Cursor (UTI method)

```bash
utiluti get-uti json
utiluti type set public.json com.todesktop.230313mzl4w4u92
```

### Python files to Cursor (file method for reliability)

```bash
touch /tmp/sample.py
utiluti file set /tmp/sample.py com.todesktop.230313mzl4w4u92
```

## Verification

After setting a default, verify by:

1. Right-clicking a file of that type in Finder
2. Checking "Open With" → default should show your selected app
3. Or use command-line verification:
   ```bash
   # For UTI-based settings
   utiluti type get <uti>

   # For file-based settings
   utiluti file app /path/to/sample.file
   ```

## Reference

- utiluti GitHub: https://github.com/scriptingosx/utiluti
- List of common UTIs: https://developer.apple.com/library/archive/documentation/Miscellaneous/Reference/UTIRef/Articles/System-DeclaredUniformTypeIdentifiers.html

## Notes

- Changes take effect immediately for new file operations
- **Prefer using existing files over temporary files** - this ensures the exact file type is matched
- Some file types may require logging out and back in for changes to fully propagate
- System applications (like TextEdit) might override custom settings for certain types
- **When in doubt, use the file-based method** - it works universally for all file extensions, including those with dynamic UTIs
- The file-based method (`utiluti file set`) sets the association system-wide for that extension
- If you still get "No application knows how to open" errors after setting the association:
  - Try right-clicking the file in Finder → "Get Info" → Change "Open with:" → Click "Change All..."
  - Or try opening via right-click → "Open With" → select the app
  - The Launch Services database may need time to update
