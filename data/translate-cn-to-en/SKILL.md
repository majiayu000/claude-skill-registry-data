---
name: translate-cn-to-en
description: Scan and replace Chinese content in project files with English, preserving code logic and original formatting.
---

## Task Objective

Translate and replace all Chinese characters (comments, strings, documentation, etc.) within specified files or project scope into English.

## Execution Principles

1.  **Accurate Translation**: Ensure the translated English accurately conveys the original Chinese meaning and fits the technical context.
2.  **Preserve Formatting**: Maintain original code indentation, line breaks, punctuation (unless Chinese punctuation needs conversion to English), and documentation structure.
3.  **Code Safety**:
    *   **STRICTLY PROHIBITED**: Modifying identifiers like variable names or function names, unless they are essentially Chinese (not recommended but possible).
    *   **STRICTLY PROHIBITED**: Breaking code logic.
    *   Pay attention to Chinese in strings. If it's text for display, it can be translated; if it's a Key or specific protocol content, verify carefully before modification. Usually, UI display text and comments are translated by default.
4.  **Comment Processing**: Translate all Chinese comments.
5.  **Documentation Processing**: Translate Chinese content in Markdown and other documentation.

## Examples

**Before:**
```javascript
// This is an example function
function example() {
  console.log("你好，世界"); // Print greeting
}
```

**After:**
```javascript
// This is an example function
function example() {
  console.log("Hello, World"); // Print greeting
}
```

## Automated Verification

It is recommended to use a script to scan files after translation to ensure no residual Chinese characters remain.

### Python Check Script Example

```python
import os
import re

def contains_chinese(text):
  return re.search(r'[\u4e00-\u9fa5]', text)

def scan_files(directory, extensions=['.md', '.ts', '.js', '.py', '.java']):
  print(f"Scanning directory: {directory} for extensions: {extensions}")
  for root, dirs, files in os.walk(directory):
    for file in files:
      if any(file.endswith(ext) for ext in extensions):
        path = os.path.join(root, file)
        try:
          with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            if contains_chinese(content):
              print(f"[FOUND] Chinese characters in: {path}")
              # Optional: Print specific lines
              lines = content.split('\n')
              for i, line in enumerate(lines):
                if contains_chinese(line):
                  print(f"  Line {i+1}: {line.strip()[:100]}...")
        except Exception as e:
          print(f"[ERROR] Reading {path}: {e}")

# Usage Example:
# scan_files('./src')
```

### Node.js Check Script Example

```javascript
const fs = require('fs');
const path = require('path');

function containsChinese(text) {
  return /[\u4e00-\u9fa5]/.test(text);
}

function scanFiles(dir, extensions = ['.md', '.ts', '.js', '.py', '.java']) {
  console.log(`Scanning directory: ${dir} for extensions: ${extensions}`);
  const files = fs.readdirSync(dir);

  files.forEach(file => {
    const filePath = path.join(dir, file);
    const stats = fs.statSync(filePath);

    if (stats.isDirectory()) {
      scanFiles(filePath, extensions);
    } else {
      if (extensions.some(ext => filePath.endsWith(ext))) {
        try {
          const content = fs.readFileSync(filePath, 'utf-8');
          if (containsChinese(content)) {
            console.log(`[FOUND] Chinese characters in: ${filePath}`);
            const lines = content.split('\n');
            lines.forEach((line, index) => {
              if (containsChinese(line)) {
                console.log(`  Line ${index + 1}: ${line.trim().substring(0, 100)}...`);
              }
            });
          }
        } catch (err) {
          console.error(`[ERROR] Reading ${filePath}: ${err}`);
        }
      }
    }
  });
}

// Usage Example:
// scanFiles('./src');
```

## Notes

*   For polysemous words, choose the most appropriate English word based on context.
*   Maintain consistency in technical terminology.
*   If uncertain, ask first or keep as is and mark it.
