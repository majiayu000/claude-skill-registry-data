---
name: macos-shortcuts
description: Manage and interact with macOS Shortcuts. Use this skill when the user wants to list available shortcuts, view a shortcut in the Shortcuts app, or run a shortcut. Supports running shortcuts with or without input parameters.
---

# macOS Shortcuts Skill

This skill provides integration with macOS Shortcuts, allowing you to list, view, and run shortcuts directly from the command line.

## Available Commands

### 1. List Available Shortcuts

Use the `shortcuts list` command to display all available shortcuts on the system.

**Command:**
```bash
shortcuts list
```

**When to use:**
- User asks to see all shortcuts
- User wants to know what shortcuts are available
- User needs to find a specific shortcut name

**Example output:**
```
My Morning Routine
Send Weekly Report
Process Screenshots
Convert to PDF
```

### 2. View Shortcut in Shortcuts App

Use the `shortcuts view` command to open a specific shortcut in the Shortcuts app for editing or inspection.

**Command:**
```bash
shortcuts view "<shortcut-name>"
```

**When to use:**
- User wants to see how a shortcut is configured
- User wants to edit a shortcut
- User wants to inspect a shortcut's actions

**Important:**
- The shortcut name must match exactly (case-sensitive)
- Use quotes around the shortcut name if it contains spaces

**Example:**
```bash
shortcuts view "My Morning Routine"
```

### 3. Run a Shortcut

Use the `shortcuts run` command to execute a shortcut. You can optionally provide input to the shortcut.

**Command (without input):**
```bash
shortcuts run "<shortcut-name>"
```

**Command (with input):**
```bash
shortcuts run "<shortcut-name>" --input-path <file-path>
```

Or with text input:
```bash
echo "some text" | shortcuts run "<shortcut-name>"
```

**When to use:**
- User wants to execute a shortcut
- User needs to run a shortcut with specific input
- User wants to automate a task using an existing shortcut

**Important:**
- The shortcut name must match exactly (case-sensitive)
- Use quotes around the shortcut name if it contains spaces
- Some shortcuts may require input, while others don't
- The output depends on what the shortcut returns

**Examples:**
```bash
# Run a simple shortcut
shortcuts run "Convert to PDF"

# Run a shortcut with file input
shortcuts run "Process Image" --input-path /path/to/image.jpg

# Run a shortcut with text input
echo "Hello World" | shortcuts run "Translate to Spanish"
```

## Error Handling

If a shortcut name doesn't exist, you'll see an error like:
```
The shortcut "Name" could not be found.
```

In this case:
1. First run `shortcuts list` to see available shortcuts
2. Verify the exact name (including capitalization)
3. Use quotes if the name contains spaces

## Tips

- Shortcut names are case-sensitive
- Always use quotes around shortcut names that contain spaces
- Use `shortcuts list` first if you're unsure of the exact name
- Some shortcuts may take time to execute, so be patient
- Shortcuts can return various types of output (text, files, etc.)

## Common Use Cases

1. **Listing shortcuts before running:** First list all shortcuts to find the exact name, then run it
2. **Batch processing:** Run shortcuts in loops or scripts for automation
3. **Integration with other tools:** Use shortcuts as part of larger workflows
4. **Quick automation:** Access powerful macOS automation without leaving the terminal
