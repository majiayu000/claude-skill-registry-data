---
name: obsidian-linter
description: "Formats and styles your notes. It can be used to format YAML tags, aliases, arrays, and metadata; footnotes; headings; spacing; math blocks; regular markdown contents like list, italics, and bold styles; and more with the use of custom rule options as well."
source: obsidian-linter
---

# Linter

## Plugin metadata

- **id:** `obsidian-linter`
- **source:** vault-native
- **plugin-type:** community
- **status:** enabled
- **class:** FULL
- **has-settings:** true

### Commands

- `obsidian-linter:lint-file` -- Linter: Lint the current file
- `obsidian-linter:lint-file-unless-ignored` -- Linter: Lint the current file unless ignored
- `obsidian-linter:lint-all-files` -- Linter: Lint all files in the vault
- `obsidian-linter:lint-all-files-in-folder` -- Linter: Lint all files in the current folder
- `obsidian-linter:paste-as-plain-text` -- Linter: Paste as Plain Text & without Modifications
- `obsidian-linter:ignore-folder` -- Linter: Ignore folder
- `obsidian-linter:ignore-file` -- Linter: Ignore file

# Linter

**Description:** Formats and styles your notes. It can be used to format YAML tags, aliases, arrays, and metadata; footnotes; headings; spacing; math blocks; regular markdown contents like list, italics, and bold styles; and more with the use of custom rule options as well.
**Status:** Enabled
**Plugin ID:** obsidian-linter

## Available Commands

Available command IDs (use execute_command for Obsidian-native commands):
- `obsidian-linter:lint-file` -- Linter: Lint the current file
- `obsidian-linter:lint-file-unless-ignored` -- Linter: Lint the current file unless ignored
- `obsidian-linter:lint-all-files` -- Linter: Lint all files in the vault
- `obsidian-linter:lint-all-files-in-folder` -- Linter: Lint all files in the current folder
- `obsidian-linter:paste-as-plain-text` -- Linter: Paste as Plain Text & without Modifications
- `obsidian-linter:ignore-folder` -- Linter: Ignore folder
- `obsidian-linter:ignore-file` -- Linter: Ignore file

## Configuration File

Settings path: `.obsidian/plugins/obsidian-linter/data.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/plugins/obsidian-linter/data.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/plugins/obsidian-linter/data.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify data.json directly.

## Current Configuration

These are the plugin's current settings (sensitive values redacted):

```
ruleConfigs:
  add-blank-line-after-yaml:
    enabled: false
  dedupe-yaml-array-values:
    enabled: false
    dedupe-alias-key: true
    dedupe-tag-key: true
    dedupe-array-keys: true
  escape-yaml-special-characters:
    enabled: false
    try-to-escape-single-line-arrays: false
  force-yaml-escape:
    enabled: false
  format-tags-in-yaml:
    enabled: false
  format-yaml-array:
    enabled: false
    alias-key: true
    tag-key: true
    default-array-style: single-line
    default-array-keys: true
  insert-yaml-attributes:
    enabled: false
    text-to-insert: aliases: 
tags: 
  move-tags-to-yaml:
    enabled: false
    how-to-handle-existing-tags: Nothing
  remove-yaml-keys:
    enabled: false
  sort-yaml-array-values:
    enabled: false
    sort-alias-key: true
    sort-tag-key: true
    sort-array-keys: true
    sort-order: Ascending Alphabetical
  yaml-key-sort:
    enabled: false
    priority-keys-at-start-of-yaml: true
    yaml-sort-order-for-other-keys: None
  yaml-timestamp:
    enabled: false
    date-created: true
    date-created-key: date created
    date-created-source-of-truth: file system
    date-modified: true
    date-modified-key: date modified
    date-modified-source-of-truth: file system
    format: dddd, MMMM Do YYYY, h:mm:ss a
    convert-to-utc: false
    update-on-file-contents-updated: never
  yaml-title:
    enabled: false
    title-key: title
    mode: first-h1-or-filename-if-h1-missing
  yaml-title-alias:
    enabled: false
    preserve-existing-alias-section-style: true
    keep-alias-that-matches-the-filename: false
    use-yaml-key-to-keep-track-of-old-filename-or-heading: true
    alias-helper-key: linter-yaml-title-alias
  capitalize-headings:
    enabled: false
    style: Title Case
    ignore-case-words: true
    ignore-words: macOS, iOS, iPhone, iPad, JavaScript, TypeScript, AppleScript, I
    lowercase-words: [string, 2277 chars]
    starting-word-ignore-characters: '"(‘“-
    ending-word-ignore-characters: .?!,:;'")”’0123456789-
  file-name-heading:
    enabled: false
  header-increment:
    enabled: false
    start-at-h2: false
  headings-start-line:
    enabled: false
  remove-trailing-punctuation-in-heading:
    enabled: false
    punctuation-to-remove: .,;:!。，；：！
  footnote-after-punctuation:
    enabled: false
  move-footnotes-to-the-bottom:
    enabled: false
    include-blank-line-between-footnotes: false
  re-index-footnotes:
    enabled: false
  auto-correct-common-misspellings:
    enabled: false
    skip-words-with-multiple-capitals: false
  blockquote-style:
    enabled: false
    style: space
  convert-bullet-list-markers:
    enabled: false
  default-language-for-code-fences:
    enabled: false
  emphasis-style:
    enabled: false
    style: consistent
  no-bare-urls:
    enabled: false
    no-bare-uris: false
  ordered-list-style:
    enabled: false
    number-style: ascending
    list-end-style: .
  proper-ellipsis:
    enabled: false
  quote-style:
    enabled: false
    single-quote-enabled: true
    single-quote-style: ''
    double-quote-enabled: true
    double-quote-style: ""
  remove-consecutive-list-markers:
    enabled: false
  remove-empty-list-markers:
    enabled: false
  remove-hyphenated-line-breaks:
    enabled: false
  remove-multiple-spaces:
    enabled: false
  strong-style:
    enabled: false
    style: consistent
  two-spaces-between-lines-with-content:
    enabled: false
    line-break-indicator:   
  unordered-list-style:
    enabled: false
    list-style: consistent
  compact-yaml:
    enabled: false
    inner-new-lines: false
  consecutive-blank-lines:
    enabled: false
  convert-spaces-to-tabs:
    enabled: false
    tabsize: 4
  empty-line-around-blockquotes:
    enabled: false
  empty-line-around-code-fences:
    enabled: false
  empty-line-around-horizontal-rules:
    enabled: false
  empty-line-around-math-blocks:
    enabled: false
  empty-line-around-tables:
    enabled: false
  heading-blank-lines:
    enabled: false
    bottom: true
    empty-line-after-yaml: true
  line-break-at-document-end:
    enabled: false
  move-math-block-indicators-to-their-own-line:
    enabled: false
  paragraph-blank-lines:
    enabled: false
  remove-empty-lines-between-list-markers-and-checklists:
    enabled: false
  remove-link-spacing:
    enabled: false
  remove-space-around-characters:
    enabled: false
    include-fullwidth-forms: true
    include-cjk-symbols-and-punctuation: true
    include-dashes: true
  remove-space-before-or-after-characters:
    enabled: false
    characters-to-remove-space-before: ,!?;:).’”]
    characters-to-remove-space-after: ¿¡‘“([
  space-after-list-markers:
    enabled: false
  space-between-chinese-japanese-or-korean-and-english-or-numbers:
    enabled: false
    english-symbols-punctuation-before: -+;:'"°%$)]
    english-symbols-punctuation-after: -+'"([¥$
  trailing-spaces:
    enabled: false
    two-space-line-break: false
  add-blockquote-indentation-on-paste:
    enabled: false
  prevent-double-checklist-indicator-on-paste:
    enabled: false
  prevent-double-list-item-indicator-on-paste:
    enabled: false
  proper-ellipsis-on-paste:
    enabled: false
  remove-hyphens-on-paste:
    enabled: false
  remove-leading-or-trailing-whitespace-on-paste:
    enabled: false
  remove-leftover-footnotes-from-quote-on-paste:
    enabled: false
  remove-multiple-blank-lines-on-paste:
    enabled: false
lintOnSave: false
recordLintOnSaveLogs: false
displayChanged: true
suppressMessageWhenNoChange: false
suppressLintAllFilesConfirmationModal: false
suppressLintAllFilesInFolderConfirmationModal: false
lintOnFileChange: false
displayLintOnFileChangeNotice: false
linterLocale: system-default
logLevel: ERROR
commonStyles:
  aliasArrayStyle: single-line
  tagArrayStyle: single-line
  minimumNumberOfDollarSignsToBeAMathBlock: 2
  escapeCharacter: "
  removeUnnecessaryEscapeCharsForMultiLineArrays: false
```

For full settings, read: `.obsidian/plugins/obsidian-linter/data.json`

## Documentation

For detailed plugin documentation (commands, options, dependencies):
read_file(".vault-operator/data/skills/obsidian-linter.readme.md")

## Usage

When the user asks for functionality related to Linter:
1. Read the plugin documentation (.readme.md) to understand capabilities and dependencies
2. Read the config file (.obsidian/plugins/obsidian-linter/data.json). If it does not exist, that is normal -- create it with the required settings
3. Configure the plugin by writing data.json with the values needed for the task
4. Execute the task using the appropriate tool:
   - For Obsidian-native commands (including file export): use execute_command
   - For CLI-based conversion needing Pandoc/LaTeX: use execute_recipe
   - For data queries: use call_plugin_api
5. If a command opens a UI dialog, tell the user what to click.

CRITICAL RULES:
- Prefer native Obsidian commands over external tools when both can accomplish the task.
- NEVER create fake output files. If the user asks for a PDF/DOCX/image export, use execute_recipe -- do NOT write content to a .pdf file yourself.
- If a dependency is missing (e.g. Pandoc), tell the user what to install.
IMPORTANT: After reading this file, ALWAYS take action or respond. Never end silently.
