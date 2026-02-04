---
title: "Base Skill"
---

# Base Skill

Every Expert automatically has access to `@perstack/base` — a built-in skill that provides file operations, runtime control, and other essential tools.

**No configuration needed. It's always available.**

## Design Philosophy

### Runtime-Coupled Skill

Base Skill is the **only** skill tightly coupled with `@perstack/runtime`. The name "base" reflects this fundamental role — Perstack cannot operate without it, and the runtime assumes Base Skill is always present.

This coupling enables MCP-native runtime control. Rather than implementing special control mechanisms outside MCP, runtime operations (task completion, todos) are exposed as standard MCP tools.

### Binary Data Handling

For binary files (images, PDFs), Base Skill returns only `path` and `mimeType`. The runtime then:
1. Reads the file from the returned path
2. Base64 encodes the content
3. Passes the encoded data to the LLM

This separation keeps Base Skill simple while letting the runtime handle LLM-specific formatting.

### No External Network Access

Base Skill **never** accesses external networks. This is intentional:
- Keeps the attack surface minimal
- Forces explicit network dependencies via separate skills
- Makes network access auditable

If your Expert needs network access, define a dedicated skill for it.

### Workspace Isolation

All file operations are restricted to the workspace directory (where `perstack run` was executed).

- Experts cannot read, write, or access files outside the workspace
- Path traversal attempts (e.g., `../`) are blocked
- The `.perstack` directory is hidden from directory listings

---

## Tool Reference

| Tool                                      | Category  | Description                             |
| ----------------------------------------- | --------- | --------------------------------------- |
| [`attemptCompletion`](#attemptcompletion) | Runtime   | Signal task completion                  |
| [`todo`](#todo)                           | Runtime   | Manage task list                        |
| [`clearTodo`](#cleartodo)                 | Runtime   | Clear task list                         |
| [`healthCheck`](#healthcheck)             | System    | Check MCP server health                 |
| [`exec`](#exec)                           | System    | Execute system commands                 |
| [`readTextFile`](#readtextfile)           | File      | Read text files                         |
| [`readImageFile`](#readimagefile)         | File      | Read image files (PNG, JPEG, GIF, WebP) |
| [`readPdfFile`](#readpdffile)             | File      | Read PDF files                          |
| [`writeTextFile`](#writetextfile)         | File      | Create or overwrite text files          |
| [`appendTextFile`](#appendtextfile)       | File      | Append to text files                    |
| [`editTextFile`](#edittextfile)           | File      | Search and replace in text files        |
| [`moveFile`](#movefile)                   | File      | Move or rename files                    |
| [`deleteFile`](#deletefile)               | File      | Delete files                            |
| [`getFileInfo`](#getfileinfo)             | File      | Get file/directory metadata             |
| [`listDirectory`](#listdirectory)         | Directory | List directory contents                 |
| [`createDirectory`](#createdirectory)     | Directory | Create directories                      |
| [`deleteDirectory`](#deletedirectory)     | Directory | Delete directories                      |

---

## System Execution

### healthCheck

Returns Perstack runtime health status and diagnostics.

**Parameters:** None

**Returns:**
```json
{
  "status": "ok",
  "workspace": "/path/to/workspace",
  "uptime": "42s",
  "memory": { "heapUsed": "25MB", "heapTotal": "50MB" },
  "pid": 12345
}
```

**Use cases:**
- Verify Perstack runtime is running and responsive
- Check workspace configuration
- Monitor runtime uptime and memory usage
- Debug connection issues

---

### exec

Executes system commands within the workspace.

**Parameters:**
| Name      | Type                     | Required | Description                                  |
| --------- | ------------------------ | -------- | -------------------------------------------- |
| `command` | `string`                 | Yes      | Command to execute (e.g., `ls`, `python`)    |
| `args`    | `string[]`               | Yes      | Arguments to pass to the command             |
| `env`     | `Record<string, string>` | Yes      | Environment variables                        |
| `cwd`     | `string`                 | Yes      | Working directory (must be within workspace) |
| `stdout`  | `boolean`                | Yes      | Whether to capture stdout                    |
| `stderr`  | `boolean`                | Yes      | Whether to capture stderr                    |
| `timeout` | `number`                 | No       | Timeout in milliseconds                      |

**Returns:**
```json
{ "output": "command output here" }
```

**Behavior:**
- Executes command using Node.js `execFile`
- Validates `cwd` is within the workspace
- Merges provided env with `process.env`
- Returns "Command executed successfully, but produced no output." if no output captured
- Returns timeout error if command exceeds timeout

**Constraints:**
- Working directory must be within workspace
- Do not execute long-running foreground commands (e.g., `tail -f`)
- Be cautious with resource-intensive commands

**Security Note:**
While `cwd` is validated, the executed command itself can still access files outside the workspace (e.g., `cat /etc/passwd`). For production deployments, use infrastructure-level isolation (containers, sandboxes) to enforce strict boundaries.

---

## Runtime Control

### attemptCompletion

Signals task completion with automatic todo validation.

**Parameters:** None

**Returns (remaining todos):**
```json
{
  "remainingTodos": [
    { "id": 0, "title": "Incomplete task 1", "completed": false },
    { "id": 2, "title": "Incomplete task 2", "completed": false }
  ]
}
```

**Returns (all todos complete or no todos):**
```json
{}
```

**Behavior:**
- Checks the current todo list for incomplete items
- If incomplete todos exist: returns them in `remainingTodos` and continues the agent loop
- If no incomplete todos (or no todos at all): triggers run result generation and ends the agent loop
- The Expert should complete remaining todos before calling again

**Run result:**

When todo validation passes, the LLM generates a run result — a summary of the work done. This ensures every completed run has a clear outcome, regardless of whether the Expert was delegated or run directly.

For delegated Experts, the run result is returned to the delegating Expert as the tool call result, maintaining context isolation.

**Best Practice:**
- Mark all todos as complete before calling `attemptCompletion`
- Use `clearTodo` if you want to reset and start fresh
- The tool prevents premature completion by surfacing forgotten tasks

---

### todo

Task list manager for tracking work items.

**Parameters:**
| Name             | Type     | Required | Description                   |
| ---------------- | -------- | -------- | ----------------------------- |
| `newTodos`       | string[] | No       | Task descriptions to add      |
| `completedTodos` | number[] | No       | Todo IDs to mark as completed |

**Returns:**
```json
{
  "todos": [
    { "id": 0, "title": "Task 1", "completed": false },
    { "id": 1, "title": "Task 2", "completed": true }
  ]
}
```

**Behavior:**
- Each todo gets a unique incremental ID when created
- Returns the full todo list after every operation
- State persists across calls within the session

**Observability:**
The runtime records all tool calls (including todo) into checkpoints, making task progress visible in execution history.

---

### clearTodo

Resets the todo list to empty state.

**Parameters:** None

**Returns:**
```json
{ "todos": [] }
```

---

## File Operations

### readTextFile

Reads text files with optional line range support.

**Parameters:**
| Name   | Type   | Required | Description            |
| ------ | ------ | -------- | ---------------------- |
| `path` | string | Yes      | File path              |
| `from` | number | No       | Start line (0-indexed) |
| `to`   | number | No       | End line (exclusive)   |

**Returns:**
```json
{ "path": "file.txt", "content": "file content", "from": 0, "to": 10 }
```

**Behavior:**
- Reads as UTF-8 encoded text
- Supports partial reading via line range
- Defaults to reading entire file if range not specified

**Constraints:**
- File must exist
- Binary files will cause errors or corrupted output

---

### readImageFile

Validates and returns image file metadata for runtime processing.

**Parameters:**
| Name   | Type   | Required | Description     |
| ------ | ------ | -------- | --------------- |
| `path` | string | Yes      | Image file path |

**Returns:**
```json
{ "path": "/workspace/image.png", "mimeType": "image/png", "size": 12345 }
```

**Runtime Integration:**
The runtime reads the file at `path`, base64 encodes it, and passes it to the LLM as an inline image.

**Supported formats:** PNG, JPEG, GIF, WebP

**Constraints:**
- Maximum file size: **15MB**
- File must exist and be a supported image format

---

### readPdfFile

Validates and returns PDF file metadata for runtime processing.

**Parameters:**
| Name   | Type   | Required | Description   |
| ------ | ------ | -------- | ------------- |
| `path` | string | Yes      | PDF file path |

**Returns:**
```json
{ "path": "/workspace/doc.pdf", "mimeType": "application/pdf", "size": 54321 }
```

**Runtime Integration:**
The runtime reads the file at `path`, base64 encodes it, and passes it to the LLM as an inline file.

**Constraints:**
- Maximum file size: **30MB**
- File must exist and be a valid PDF

---

### writeTextFile

Creates or overwrites text files.

**Parameters:**
| Name   | Type   | Required | Description                              |
| ------ | ------ | -------- | ---------------------------------------- |
| `path` | string | Yes      | Target file path                         |
| `text` | string | Yes      | Content to write (max 10,000 characters) |

**Returns:**
```json
{ "path": "/workspace/file.txt", "text": "written content" }
```

**Behavior:**
- Creates parent directories automatically
- Overwrites existing files
- Writes as UTF-8 encoded text
- Pass empty string to clear file contents

**Constraints:**
- Maximum 10,000 characters per call
- Use `appendTextFile` for larger files

---

### appendTextFile

Appends content to existing files.

**Parameters:**
| Name   | Type   | Required | Description                              |
| ------ | ------ | -------- | ---------------------------------------- |
| `path` | string | Yes      | Target file path                         |
| `text` | string | Yes      | Content to append (max 2,000 characters) |

**Returns:**
```json
{ "path": "/workspace/file.txt", "text": "appended content" }
```

**Behavior:**
- Appends to end of file without modifying existing content
- Does not add newline automatically

**Constraints:**
- File must exist
- Maximum 2,000 characters per call
- Call multiple times for larger content

---

### editTextFile

Performs search-and-replace in text files.

**Parameters:**
| Name      | Type   | Required | Description                             |
| --------- | ------ | -------- | --------------------------------------- |
| `path`    | string | Yes      | Target file path                        |
| `oldText` | string | Yes      | Text to find (max 2,000 characters)     |
| `newText` | string | Yes      | Replacement text (max 2,000 characters) |

**Returns:**
```json
{ "path": "/workspace/file.txt", "oldText": "old", "newText": "new" }
```

**Behavior:**
- Performs exact string replacement (first occurrence only)
- Normalizes line endings (CRLF → LF) before matching
- File must contain exact match of `oldText`

**Constraints:**
- File must exist
- `oldText` must exist in file
- Maximum 2,000 characters for both `oldText` and `newText`

---

### moveFile

Moves or renames files.

**Parameters:**
| Name          | Type   | Required | Description       |
| ------------- | ------ | -------- | ----------------- |
| `source`      | string | Yes      | Current file path |
| `destination` | string | Yes      | Target file path  |

**Returns:**
```json
{ "source": "/workspace/old.txt", "destination": "/workspace/new.txt" }
```

**Behavior:**
- Creates destination directory if needed
- Performs atomic move operation

**Constraints:**
- Source must exist
- Destination must not exist
- Source must be writable

---

### deleteFile

Removes files from the workspace.

**Parameters:**
| Name   | Type   | Required | Description         |
| ------ | ------ | -------- | ------------------- |
| `path` | string | Yes      | File path to delete |

**Returns:**
```json
{ "path": "/workspace/deleted.txt" }
```

**Constraints:**
- File must exist
- File must be writable
- Cannot delete directories (use directory-specific tools)

---

### getFileInfo

Retrieves detailed file or directory metadata.

**Parameters:**
| Name   | Type   | Required | Description            |
| ------ | ------ | -------- | ---------------------- |
| `path` | string | Yes      | File or directory path |

**Returns:**
```json
{
  "exists": true,
  "path": "file.txt",
  "absolutePath": "/workspace/file.txt",
  "name": "file.txt",
  "directory": "/workspace",
  "extension": ".txt",
  "type": "file",
  "mimeType": "text/plain",
  "size": 1234,
  "sizeFormatted": "1.21 KB",
  "created": "2024-01-01T00:00:00.000Z",
  "modified": "2024-01-02T00:00:00.000Z",
  "accessed": "2024-01-03T00:00:00.000Z",
  "permissions": {
    "readable": true,
    "writable": true,
    "executable": false
  }
}
```

**Behavior:**
- Works for both files and directories
- Returns `null` for extension and mimeType on directories
- Formats size in human-readable format (B, KB, MB, GB, TB)

---

## Directory Operations

### listDirectory

Lists directory contents with metadata.

**Parameters:**
| Name   | Type   | Required | Description    |
| ------ | ------ | -------- | -------------- |
| `path` | string | Yes      | Directory path |

**Returns:**
```json
{
  "path": "/workspace/src",
  "items": [
    { "name": "index.ts", "path": "index.ts", "type": "file", "size": 256, "modified": "2024-01-01T00:00:00.000Z" },
    { "name": "lib", "path": "lib", "type": "directory", "size": 4096, "modified": "2024-01-01T00:00:00.000Z" }
  ]
}
```

**Behavior:**
- Lists only immediate children (non-recursive)
- Sorts entries alphabetically
- Excludes `.perstack` directory from results

**Constraints:**
- Path must exist
- Path must be a directory

---

### createDirectory

Creates directories with recursive parent creation.

**Parameters:**
| Name   | Type   | Required | Description              |
| ------ | ------ | -------- | ------------------------ |
| `path` | string | Yes      | Directory path to create |

**Returns:**
```json
{ "path": "/workspace/new/nested/dir" }
```

**Behavior:**
- Creates all parent directories as needed
- Uses `mkdir` with `recursive: true`

**Constraints:**
- Directory must not already exist
- Parent directory must be writable

---

### deleteDirectory

Removes directories from the workspace.

**Parameters:**
| Name        | Type      | Required | Description                            |
| ----------- | --------- | -------- | -------------------------------------- |
| `path`      | `string`  | Yes      | Directory path to delete               |
| `recursive` | `boolean` | No       | Whether to delete contents recursively |

**Returns:**
```json
{ "path": "/workspace/old-dir" }
```

**Behavior:**
- Validates directory existence and permissions
- Removes directory (and contents if `recursive: true`)

**Constraints:**
- Directory must exist
- Directory must be writable
- Non-empty directories require `recursive: true`
- Cannot delete files (use `deleteFile` instead)

---

## Example: Agent Loop Flow

Here's how an Expert uses Base Skill tools in a typical agent loop:

```
┌─────────────────────────────────────────────────────────────────┐
│  User: "Organize files in this directory by type"              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  1. LIST DIRECTORY                                              │
│  ─────────────────────────────────────────────────────────────  │
│  tool: listDirectory                                            │
│  input: { path: "." }                                           │
│  output: { items: [                                             │
│    { name: "photo.jpg", type: "file" },                         │
│    { name: "report.pdf", type: "file" },                        │
│    { name: "notes.txt", type: "file" }                          │
│  ]}                                                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  2. TODO                                                        │
│  ─────────────────────────────────────────────────────────────  │
│  tool: todo                                                     │
│  input: { newTodos: [                                           │
│    "Create images/ directory",                                  │
│    "Create documents/ directory",                               │
│    "Move files to appropriate directories"                      │
│  ]}                                                             │
│  output: { todos: [{ id: 0, title: "...", completed: false }] } │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  3. CREATE DIRECTORIES                                          │
│  ─────────────────────────────────────────────────────────────  │
│  tool: createDirectory                                          │
│  input: { path: "images" }                                      │
│  output: { path: "/workspace/images" }                          │
│                                                                 │
│  tool: createDirectory                                          │
│  input: { path: "documents" }                                   │
│  output: { path: "/workspace/documents" }                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  4. MOVE FILES                                                  │
│  ─────────────────────────────────────────────────────────────  │
│  tool: moveFile                                                 │
│  input: { source: "photo.jpg", destination: "images/photo.jpg" }│
│  output: { source: "...", destination: "..." }                  │
│                                                                 │
│  tool: moveFile                                                 │
│  input: { source: "report.pdf", destination: "documents/..." }  │
│  ...                                                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  5. MARK TODOS COMPLETE                                         │
│  ─────────────────────────────────────────────────────────────  │
│  tool: todo                                                     │
│  input: { completedTodos: [0, 1, 2] }                           │
│  output: { todos: [{ id: 0, completed: true }, ...] }           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  6. COMPLETE                                                    │
│  ─────────────────────────────────────────────────────────────  │
│  tool: attemptCompletion                                        │
│  input: {}                                                      │
│  output: {} (no remaining todos)                                │
│  → Agent loop ends                                              │
└─────────────────────────────────────────────────────────────────┘
```

The Expert definition for this workflow:

```toml
[experts."file-organizer"]
description = "Organizes files in the workspace by type"
instruction = """
You organize files in the current directory.
1. List all files using listDirectory
2. Create subdirectories by file type (images/, documents/, etc.)
3. Move files to appropriate directories using moveFile
"""
```

All tools come from Base Skill — no skill definitions needed.
