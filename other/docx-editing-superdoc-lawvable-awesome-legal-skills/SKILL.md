---
name: docx-editing-superdoc
description: Programmatically edit Word documents (.docx) with live preview and track changes via SuperDoc VS Code extension. Use when editing DOCX files, making tracked changes, redlining, marking up contracts, or when the user wants to modify Word documents with insertions/deletions visible. Triggers on docx, Word, track changes, redline, markup.
---

# DOCX Live Editor

Edit Word documents with live preview and track changes in VS Code via SuperDoc extension.

## Prerequisites

1. SuperDoc VS Code extension installed. Check with:
    ```bash
    $(command -v code || echo /Applications/Visual\ Studio\ Code.app/Contents/Resources/app/bin/code) --profile "Lawvable" --list-extensions | grep -i superdoc
    ```
2. Document must be open in VS Code before editing. Open with:
    ```bash
    $(command -v code || echo /Applications/Visual\ Studio\ Code.app/Contents/Resources/app/bin/code) path/to/doc.docx
    ```

## File Structure

Commands go to `.superdoc/{docname}.json` (same basename as the DOCX):

```
project/
├── contract.docx
└── .superdoc/
    └── contract.json   ← commands for contract.docx
```

## How It Works

1. Write command to `.superdoc/{docname}.json`
2. Extension executes and overwrites file with response
3. Changes appear live (green insertions, red deletions)

**State:** `"command"` field = pending | `"success"` field = response ready

## Commands

### `getText` - Read Document Content

```bash
# Get both text and HTML (default)
echo '{"id":"1","command":"getText","args":{}}' > .superdoc/contract.json

# Get only plain text (fewer tokens)
echo '{"id":"2","command":"getText","args":{"format":"text"}}' > .superdoc/contract.json

# Get only HTML (preserves structure)
echo '{"id":"3","command":"getText","args":{"format":"html"}}' > .superdoc/contract.json
```

**Formats:** `text` (plain text with paragraph breaks), `html` (full HTML), `both` (default)

### `getNodes` - Get Document Structure

Get all nodes of a specific type with their positions. Useful for understanding document structure before making edits.

```bash
# Get all tables
echo '{"id":"2","command":"getNodes","args":{"type":"table"}}' > .superdoc/contract.json

# Get all headings
echo '{"id":"3","command":"getNodes","args":{"type":"heading"}}' > .superdoc/contract.json
```

**Valid types:** `paragraph`, `heading`, `table`, `tableRow`, `tableCell`, `bulletList`, `orderedList`, `listItem`, `image`, `blockquote`

**Returns:**
```json
{
  "nodes": [
    {"index": 0, "type": "heading", "from": 1, "to": 25, "text": "1. Introduction", "level": 1},
    {"index": 1, "type": "heading", "from": 100, "to": 130, "text": "2. Definitions", "level": 1}
  ],
  "count": 2
}
```

### `replaceText` - Find and Replace

**Use when:** Changing existing text to something different. The found text is DELETED and replaced.

```bash
# Change a value: "2024" → "2025"
echo '{"id":"2","command":"replaceText","args":{"search":"2024","replacement":"2025"}}' > .superdoc/contract.json

# Change a placeholder: "[ORG_NAME]" → "Lawvable"
echo '{"id":"3","command":"replaceText","args":{"search":"[ORG_NAME]","replacement":"Lawvable"}}' > .superdoc/contract.json

# Change a word: "shall" → "must"
echo '{"id":"4","command":"replaceText","args":{"search":"shall","replacement":"must","occurrence":1}}' > .superdoc/contract.json

# Add formatting to existing text (text is replaced with formatted version)
echo '{"id":"5","command":"replaceText","args":{"search":"Important Notice","replacement":"<strong>Important Notice</strong>"}}' > .superdoc/contract.json
```

### `insertContent` - Insert NEW Content

**Use when:** Adding new text/elements while keeping the anchor text intact. The anchor text STAYS, new content is added before/after.

```bash
# Add a word after existing text: "agrees to pay" + " promptly"
echo '{"id":"5","command":"insertContent","args":{"content":" promptly","position":{"after":"agrees to pay"}}}' > .superdoc/contract.json

# Add a new section after a heading
echo '{"id":"6","command":"insertContent","args":{"content":"<h2>New Section</h2><p>Content here.</p>","position":{"after":"Introduction"}}}' > .superdoc/contract.json

# Add a disclaimer before signatures
echo '{"id":"7","command":"insertContent","args":{"content":"<p>By signing below, parties confirm agreement.</p>","position":{"before":"Signatures"}}}' > .superdoc/contract.json

# Add a clause after a section
echo '{"id":"8","command":"insertContent","args":{"content":"<p>Additional clause text.</p>","position":{"after":"Section 2."},"author":{"name":"Jane Smith"}}}' > .superdoc/contract.json
```

### When to Use Which

| Task | Command | Example |
|------|---------|---------|
| Change a value | `replaceText` | "2024" → "2025" |
| Fill a placeholder | `replaceText` | "[NAME]" → "John" |
| Fix a typo | `replaceText` | "teh" → "the" |
| Change a word | `replaceText` | "shall" → "must" |
| Add a word after text | `insertContent` | add " promptly" after "agrees to pay" |
| Add a new paragraph | `insertContent` | add clause after "Section 3" |
| Add a new section | `insertContent` | add heading after "Introduction" |
| Add disclaimer | `insertContent` | add text before "Signatures" |
| Add review comment | `addComment` | comment on "confidential information" |

### `insertTable` - Create a Table

```bash
# Insert 3x4 table after specific text
echo '{"id":"8","command":"insertTable","args":{"rows":3,"cols":4,"position":{"after":"Introduction"}}}' > .superdoc/contract.json

# Insert 2x2 table (default) before specific text
echo '{"id":"9","command":"insertTable","args":{"position":{"before":"Signatures"}}}' > .superdoc/contract.json

# Pre-populated table with headers and data (dimensions inferred)
echo '{"id":"10","command":"insertTable","args":{"data":[["Name","Role"],["Alice","Engineer"]],"position":{"after":"Team:"}}}' > .superdoc/contract.json

# Cells support HTML formatting
echo '{"id":"11","command":"insertTable","args":{"data":[["<strong>Header</strong>"],["Value"]]}}' > .superdoc/contract.json

# With custom author for track changes
echo '{"id":"12","command":"insertTable","args":{"rows":2,"cols":3,"author":{"name":"John"}}}' > .superdoc/contract.json
```

**Parameters:**
- `rows`, `cols` - Dimensions (default: 2, or inferred from `data`)
- `data` - 2D array of cell contents (row-major). Supports plain text or HTML. Empty strings for blank cells.
- `position` - `{"after": "text"}` or `{"before": "text"}` for anchor-based positioning
- `author` - Optional author for track changes attribution

### `addComment` - Add Comment to Text

```bash
# Add a comment on specific text
echo '{"id":"1","command":"addComment","args":{"search":"confidential information","comment":"This clause needs legal review"}}' > .superdoc/contract.json

# Comment on nth occurrence
echo '{"id":"2","command":"addComment","args":{"search":"Party","comment":"Verify party name","occurrence":2}}' > .superdoc/contract.json
```

**Parameters:**
- `search` (required) - Text to find and attach comment to
- `comment` (required) - The comment text
- `occurrence` - Which match (1-indexed), defaults to first
- `author` - Optional `{name, email}` for attribution

### `undo` / `redo` - History Navigation

```bash
# Undo the last action
echo '{"id":"16","command":"undo","args":{}}' > .superdoc/contract.json

# Redo the last undone action
echo '{"id":"17","command":"redo","args":{}}' > .superdoc/contract.json
```

**Returns:** `{"success": true}` if action was undone/redone, `{"success": false}` if nothing to undo/redo.

### `formatText` - Apply Text Formatting

Apply font properties and text styling. **Not tracked** (applied directly for performance).

```bash
# Multiple formats on entire document
echo '{"id":"8","command":"formatText","args":{"fontFamily":"Arial","fontSize":"12pt","color":"#333333","scope":"document"}}' > .superdoc/contract.json

# Bold + highlight on specific range (use getNodes to find positions)
echo '{"id":"9","command":"formatText","args":{"bold":true,"highlight":"#FFEB3B","scope":{"from":100,"to":200}}}' > .superdoc/contract.json

# Remove formatting (false removes, omit leaves unchanged)
echo '{"id":"10","command":"formatText","args":{"bold":false,"highlight":false,"scope":{"from":100,"to":200}}}' > .superdoc/contract.json

# Add hyperlink to text range
echo '{"id":"11","command":"formatText","args":{"link":"https://example.com","scope":{"from":100,"to":120}}}' > .superdoc/contract.json

# Remove hyperlink
echo '{"id":"12","command":"formatText","args":{"link":false,"scope":{"from":100,"to":120}}}' > .superdoc/contract.json
```

**Parameters:**
- `fontFamily` - Font name (e.g., "Arial", "Times New Roman")
- `fontSize` - Size with unit (e.g., "12pt", "14px")
- `color` - Text color as CSS (e.g., "#ff0000", "red")
- `highlight` - Background color, or `false` to remove
- `bold`, `italic`, `underline`, `strikethrough` - `true` to apply, `false` to remove, omit to leave unchanged
- `link` - URL string to create hyperlink, or `false` to remove
- `scope` - `"document"` for entire doc, or `{"from": N, "to": M}` for range

**To format a specific paragraph:** Use `getNodes` with type `paragraph` to get positions, then apply formatting to that range.

## HTML Formatting

| Format | HTML |
|--------|------|
| Headings | `<h1>`, `<h2>`, `<h3>` |
| Paragraph | `<p>Text</p>` |
| Bold/Italic/Underline | `<strong>`, `<em>`, `<u>` |
| Color | `<span style="color: red">text</span>` |
| Lists | `<ul><li>...</li></ul>`, `<ol><li>...</li></ol>` |
| Link | `<a href="url">text</a>` |

**Adding a link to existing text:**

Use `formatText` with `link` parameter and position scope:
```bash
# Get paragraph positions, then apply link to range
echo '{"id":"1","command":"getNodes","args":{"type":"paragraph"}}' > .superdoc/contract.json && sleep 0.5 && cat .superdoc/contract.json
echo '{"id":"2","command":"formatText","args":{"link":"https://example.com","scope":{"from":218,"to":230}}}' > .superdoc/contract.json && sleep 0.5 && cat .superdoc/contract.json
```

**Important:** Replacement strings are only parsed as HTML if they **start with `<tag>` and end with `</tag>`**. Including text before/after (e.g., `(<a>text</a>)`) treats the entire string as literal text.

**Creating lists with `insertContent`:**
```bash
# Bullet list
echo '{"id":"1","command":"insertContent","args":{"content":"<ul><li>First</li><li>Second</li></ul>","position":{"after":"Key points:"}}}' > .superdoc/contract.json

# Numbered list with nested items and formatting
echo '{"id":"2","command":"insertContent","args":{"content":"<ol><li><strong>Step one</strong><ul><li>Sub-item</li></ul></li><li>Step two</li></ol>","position":{"after":"Instructions:"}}}' > .superdoc/contract.json
```

## How Search Works

Search extracts **plain text only**, ignoring all formatting:
- ✅ Matches across bold/normal, track changes, paragraphs
- ✅ Whitespace flexible (extra spaces/tabs/line breaks OK)
- Returns **first** occurrence. Use `occurrence` parameter for nth match, or include more context to make pattern unique.

## Best Practices

**Use unique phrases (5+ words):**
- ❌ `"the"` or `"Agreement"` (too common)
- ✅ `"agrees to pay the sum of"` or `"Section 3.2 Confidentiality"`

**Don't worry about formatting in search** - matches across bold, track changes, etc.

**Use `occurrence` for ambiguous matches** (1-indexed):
```json
{"command":"replaceText","args":{"search":"the","replacement":"that","occurrence":3}}
```

**For insertions, find unique anchor text nearby.**

## Workflow

**ALWAYS chain echo + sleep + cat in a single bash command to send and read response together.**

### Step 0: Clarify Author (once per session)
Before making any edits, use `AskUserQuestion` to ask whether changes should be attributed to the user (ask their name) or the agent (default: "Claude"). If the user wants their name, pass `"author":{"name":"Their Name"}` in **every** `replaceText`, `insertContent`, `insertTable`, and `addComment` command.

### Step 1: Read First
Get document content to understand structure and find anchor text:
```bash
echo '{"id":"1","command":"getText","args":{"format":"text"}}' > .superdoc/contract.json && sleep 0.5 && cat .superdoc/contract.json
```

### Step 2: Make Edit + Read Response
Execute command and immediately read the response in one bash call (see "When to Use Which" table to pick the right command):
```bash
echo '{"id":"2","command":"replaceText","args":{"search":"2024","replacement":"2025"}}' > .superdoc/contract.json && sleep 0.5 && cat .superdoc/contract.json
```

### Step 3: Verify with getText (content changes only)
For `replaceText`, `insertContent`, `insertTable` - verify the change is visible:
```bash
echo '{"id":"3","command":"getText","args":{"format":"text"}}' > .superdoc/contract.json && sleep 0.5 && cat .superdoc/contract.json
```

**Skip verification for `formatText`** - formatting (font, color, highlight) is not visible in text output. The command response `{"success": true}` is sufficient.

### Multi-Edit Example
Each command is a single bash call (echo + sleep + cat chained):
```bash
# 1. Read document
echo '{"id":"1","command":"getText","args":{"format":"text"}}' > .superdoc/contract.json && sleep 0.5 && cat .superdoc/contract.json

# 2. First edit + response
echo '{"id":"2","command":"replaceText","args":{"search":"2024","replacement":"2025"}}' > .superdoc/contract.json && sleep 0.5 && cat .superdoc/contract.json

# 3. Verify first edit
echo '{"id":"3","command":"getText","args":{"format":"text"}}' > .superdoc/contract.json && sleep 0.5 && cat .superdoc/contract.json

# 4. Second edit + response
echo '{"id":"4","command":"insertContent","args":{"content":"<p>Reviewed.</p>","position":{"after":"Signatures"}}}' > .superdoc/contract.json && sleep 0.5 && cat .superdoc/contract.json

# 5. Final verification
echo '{"id":"5","command":"getText","args":{"format":"text"}}' > .superdoc/contract.json && sleep 0.5 && cat .superdoc/contract.json
```

## Track Changes & Comments

Content edits (`replaceText`, `insertContent`) appear as tracked changes (author: "Claude"):
- Insertions: green/underline
- Deletions: red/strikethrough

Comments (`addComment`) appear as comment balloons attached to text ranges.

**Note:** Formatting changes (`formatText`) are applied directly without tracking.

## Troubleshooting

- **Command not executing**: Ensure document is open in SuperDoc and `.superdoc/` folder exists in same directory.
- **"Text not found" error**: Use `getText` first to see actual content, then include more surrounding context in search string.
- **Changes not visible**: Verify the SuperDoc extension is active.
