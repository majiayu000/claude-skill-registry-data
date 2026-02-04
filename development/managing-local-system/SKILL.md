---
name: managing-local-system
description: Manages local filesystem operations, runs shell commands, and performs calculations. Use when working with local files, directories, executing shell commands, or doing mathematical calculations.
---

# Local System Tools

Tools for local filesystem operations, shell commands, and calculations.

## File System Operations

### Write file

```python
result = await filesystem_write_file(
    content="Hello, World!",
    filename="example.txt",
    directory="/path/to/dir"
)
```

### Read file

```python
result = await filesystem_read_file(filename="example.txt", directory="/path/to/dir")
# Returns: {"success": True, "data": {"content": "Hello, World!", ...}}
```

### List files

```python
result = await filesystem_list_files(
    directory="/path/to/dir",
    pattern="*.txt",
    recursive=True
)
```

### File operations

```python
# Check existence
result = await filesystem_file_exists(filename="test.txt")

# Get info
result = await filesystem_get_file_info(filename="test.txt")

# Delete
result = await filesystem_delete_file(filename="test.txt")

# Append
result = await filesystem_append_to_file(content="More text", filename="test.txt")

# Copy
result = await filesystem_copy_file(
    source_filename="original.txt",
    destination_filename="copy.txt"
)
```

### Create directory

```python
result = await filesystem_create_directory(directory="/new/path", parents=True)
```

## Security

By default, file operations are restricted to the current working directory.

Set `HUMCP_ALLOW_ABSOLUTE_PATHS=true` to allow operations outside cwd.

## Shell Commands

### Run script

```python
result = await shell_run_shell_script(
    script="echo 'Hello'\nls -la",
    shell="/bin/bash",
    timeout=30
)
```

### Check command exists

```python
result = await shell_check_command_exists(command="git")
# Returns: {"success": True, "data": {"exists": True, "path": "/usr/bin/git"}}
```

### Get environment variable

```python
result = await shell_get_environment_variable(variable_name="HOME")
```

### Get system info

```python
result = await shell_get_system_info()
# Returns OS, platform, Python version, hostname, etc.
```

### Get current directory

```python
result = await shell_get_current_directory()
```

## Calculator

### Basic operations

```python
result = await calculator_add(a=5, b=3)       # 8
result = await calculator_subtract(a=10, b=4) # 6
result = await calculator_multiply(a=6, b=7)  # 42
result = await calculator_divide(a=20, b=4)   # 5.0
```

### Advanced operations

```python
result = await calculator_power(base=2, exponent=10)  # 1024
result = await calculator_sqrt(number=144)            # 12.0
result = await calculator_percentage(value=50, total=200)  # 25.0
```

## Response Format

All tools return:
```json
{
  "success": true,
  "data": { ... }
}
```

On error:
```json
{
  "success": false,
  "error": "Error description"
}
```
