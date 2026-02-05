---
name: textcleaner-repl
description: Interact with TextCleaner's REPL interface to manage pipelines, set input text, and process data through the socket server
allowed-tools:
  - Bash
  - Read
---

# TextCleaner REPL Skill

This skill enables Claude to interact with the TextCleaner REPL interface for managing text processing pipelines via the socket server.

## Prerequisites

Before using this skill, ensure:
1. TextCleaner is built: `go build -o go-textcleaner`
2. Socket server is running in a separate terminal:
   ```bash
   ./go-textcleaner --headless --socket /tmp/textcleaner.sock
   ```

## How to Use

To use this skill, invoke the REPL with:

```bash
./go-textcleaner --repl --socket /tmp/textcleaner.sock
```

Then interact with it using natural language commands. The REPL accepts commands in the following categories:

### Node Management
- `create node <name> [type <node_type>] [operation <op_name>] [parent <parent_name_or_id>]` - Create a node with optional type and parent
- `create child <parent_id> <name> [operation]` - Create a child node (alternative syntax)
- `update node <node_id> <name> [operation]` - Update node properties
- `delete node <node_id>` - Delete a node
- `select node <node_id>` - Select a node

**Node Types:**
- `operation` (default) - Single text transformation
- `foreach` - Process each line separately with child operations
- `if` - Conditional branching based on pattern
- `group` - Group multiple operations

### Tree Operations
- `indent <node_id>` - Make node a child of previous sibling
- `unindent <node_id>` - Make node a sibling of its parent
- `move up <node_id>` - Move node up in tree
- `move down <node_id>` - Move node down in tree

### Query Commands
- `show node <node_id>` - Display a specific node
- `show pipeline` - Show pipeline as JSON
- `show tree` - Show pipeline as indented tree
- `list nodes` - List all root nodes in table format
- `get input` - Get current input text
- `get output` - Get processed output
- `get selected` - Get currently selected node ID

### Text Processing
- `set input <text>` - Set input text (single line)
- `set input` - Set input text (multiline mode)

### Pipeline Management
- `export` - Export pipeline as JSON
- `import <json>` - Import pipeline from JSON
- `import` - Import pipeline (multiline mode)

### Utility
- `help [command]` - Show help for all commands or specific command
- `info [types]` - Show available node types and operations
- `clear` - Clear the screen
- `quit` / `exit` - Exit the REPL

## Example Workflows

### Basic Pipeline
```bash
# In REPL session:
textcleaner> create node Uppercase operation Uppercase
✓ Created node: node_0

textcleaner> set input hello world
✓ Input text set

textcleaner> get output
HELLO WORLD

textcleaner> show tree
└─ Uppercase [Uppercase] (node_0)
```

### Creating Child Nodes by Parent Name
```bash
textcleaner> create node Sum operation Sum\ Numbers
✓ Created node: node_0

textcleaner> create node TrimLines operation Trim parent Sum
✓ Created node: node_0_child_0

textcleaner> show tree
└─ Sum [Sum Numbers] (node_0)
  └─ TrimLines [Trim] (node_0_child_0)
```

### Processing Lines with Foreach
```bash
# Create a foreach node that processes each line separately
textcleaner> create node SumPerLine type foreach
✓ Created node: node_0

textcleaner> create node SumNumbers operation Sum\ Numbers parent SumPerLine
✓ Created node: node_0_child_0

textcleaner> set input
1 2 3
4 5 6
7 8 9

textcleaner> get output
6
15
24

# Without foreach, it would sum all numbers: 45
# With foreach, each line is summed separately: 6, 15, 24

textcleaner> show tree
└─ SumPerLine (node_0)
  └─ SumNumbers [Sum Numbers] (node_0_child_0)
```

### Chaining Operations in Foreach
```bash
textcleaner> create node ProcessLines type foreach
✓ Created node: node_0

textcleaner> create node Trim operation Trim parent ProcessLines
✓ Created node: node_0_child_0

textcleaner> create node Uppercase operation Uppercase parent Trim
✓ Created node: node_0_child_0_child_0

textcleaner> set input
  hello world
  test data
  example text

textcleaner> get output
HELLO WORLD
TEST DATA
EXAMPLE TEXT

textcleaner> show tree
└─ ProcessLines (node_0)
  └─ Trim [Trim] (node_0_child_0)
    └─ Uppercase [Uppercase] (node_0_child_0_child_0)
```

## Output Formats

### Table Output (list nodes)
```
ID                 Name             Type         Operation
---                ----             ----         ---------
node_0             Uppercase        operation    Uppercase
```

### Tree Output (show tree)
```
├─ Uppercase [Uppercase] (node_0)
│  └─ Lowercase [Lowercase] (node_1)
```

### JSON Output (show pipeline, export)
```json
[
  {
    "id": "node_0",
    "name": "Uppercase",
    "operation": "Uppercase",
    "type": "operation"
  }
]
```

## Key Features

### Parent Node References
Create child nodes by referencing parent nodes by **name or ID**:
- By name: `create node Child operation Uppercase parent MyParent`
- By ID: `create node Child operation Uppercase parent node_0`

### Foreach for Line-by-Line Processing
Use `type foreach` to create nodes that process each line separately:
```bash
# This will sum each line individually
create node MyForeach type foreach
create node SumEachLine operation Sum\ Numbers parent MyForeach

# Input: 1 2 3
#        4 5 6
# Output: 6
#         15
```

### Chained Operations
Chain multiple operations within foreach or other node types:
```bash
# Operations are applied sequentially to each line
create node ForEach type foreach
create node Trim operation Trim parent ForEach
create node Upper operation Uppercase parent Trim
create node Suffix operation Add\ Suffix ! parent Upper
```

## Tips

1. **Use parent names** for cleaner pipelines: `create node Child operation Uppercase parent ParentName`
2. **Test with Sum Numbers** to verify foreach works per-line
3. **Use quoted arguments** for text with spaces: `set input "hello world with spaces"`
4. **Navigate history** with arrow keys
5. **Tab completion** available for command names
6. **Stack operations** to test pipelines quickly
7. **Keep REPL and GUI windows** side-by-side to see real-time changes

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "no socket server running" | Start headless server first: `./go-textcleaner --headless --socket /tmp/textcleaner.sock` |
| "node not found" | Use `show tree` or `list nodes` to verify node IDs or names |
| "command not recognized" | Type `help` to see all available commands |
| Parent node by name not found | Verify the exact node name with `show tree` - names are case-sensitive |
| Foreach not processing per-line | Use `Sum Numbers` operation to verify - each line should sum separately |
| Child node created as sibling instead | Check parent reference is by name or ID, not just operation name |

## Integration with Claude

When using this skill, Claude can:
- Execute REPL commands to manage pipelines
- Parse and interpret REPL responses
- Guide you through complex pipeline configurations
- Troubleshoot pipeline issues
- Document pipeline operations

Start by using a command like: "Use the textcleaner REPL to [describe what you want to do]"
