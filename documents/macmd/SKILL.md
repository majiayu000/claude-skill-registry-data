---
name: macmd
description: Drive and configure MacMD, the native macOS Markdown editor, from the command line or UI automation. Use when opening or editing .md files in MacMD, changing its themes, fonts, layout, or preferences programmatically, exporting Markdown to HTML or PDF through it, or verifying MacMD behavior. Not for editing Markdown text itself or for other editors.
---

# MacMD

Native macOS Markdown editor (SwiftUI document app). Bundle id `com.sleetcrash.MacMD`, installed at `/Applications/MacMD.app`. Fully offline: no network entitlements, no telemetry. Source: https://github.com/sleetcrash/MacMD

## Capability map

- Editor: plain-text Markdown with live syntax highlighting (headings, emphasis, code, links, lists, task checkboxes, blockquotes, strikethrough, YAML/TOML front matter). Line-number gutter. Optional word-count tab.
- Preview: sandboxed offline WKWebView (bundled markdown-it + mermaid, strict CSP, zero network). Renders 12 mermaid diagram types. Front matter renders as a muted metadata block with theme-colored keys.
- Layout: three pane modes per window chrome control: editor only, split, preview only. Bidirectional scroll sync in split.
- Theming: light/dark/system mode, heading color schemes (Default, Unified, Standard), preset and custom palettes, custom editor background colors with a saved library, 8 font families, cursor styles.
- Export: self-contained HTML (File > Export to HTML, Cmd-Shift-E) and single-page full-bleed PDF (File > Export to PDF). Both render through the same sandboxed pipeline; remote image refs are stripped, local images inlined.
- Templates: File > New from Template creates prefilled SKILL.md, agent, CLAUDE.md, or AGENTS.md documents.

## Opening documents

```sh
open -a MacMD file.md            # open a file
open -a MacMD                    # launch (restores prior windows)
open -na MacMD file.md           # force a new instance (rarely needed)
```

Accepted extensions: `.md`, `.markdown`, `.mdown`, `.mkd`, plus any plain text. Files are UTF-8; a leading BOM is stripped on read and a single trailing newline is appended on save. Files over 64 MiB refuse to open; over 8 MiB they open with highlighting and live preview disabled.

## Configuring preferences from the CLI

Preferences live in `defaults` under `com.sleetcrash.MacMD`. QUIT THE APP FIRST (`osascript -e 'quit app "MacMD"'`); a running app overwrites external writes.

```sh
defaults write com.sleetcrash.MacMD appAppearance -string dark      # light | dark | system (the Mode; inert while a static theme is applied)
defaults write com.sleetcrash.MacMD selectedTheme -string std.cmyk  # see Theme ids below; delete the key for Default
defaults write com.sleetcrash.MacMD themeSchemaVersion -int 2       # REQUIRED when staging: without it a launch runs the legacy migration
defaults write com.sleetcrash.MacMD editorFontSize -float 14        # 9 to 32
defaults write com.sleetcrash.MacMD editorFontFamily -string menlo  # system-mono | menlo | monaco | courier-new | system | new-york | helvetica-neue | georgia
defaults write com.sleetcrash.MacMD cursorStyle -string bar         # bar | block | underline
defaults write com.sleetcrash.MacMD cursorBlink -bool true
defaults write com.sleetcrash.MacMD cursorColor -string "#FF8800"   # #RRGGBB; delete the key for the system accent
defaults write com.sleetcrash.MacMD paneMode -string split          # editor | split | preview
defaults write com.sleetcrash.MacMD showFormatting -bool true       # styled vs plain editor
defaults write com.sleetcrash.MacMD showLineNumbers -bool true
defaults write com.sleetcrash.MacMD showToolbar -bool true
defaults write com.sleetcrash.MacMD toolbarAutoHide -bool true      # slide-in toolbar; false = always visible
defaults write com.sleetcrash.MacMD showWordCount -bool false
defaults write com.sleetcrash.MacMD checkSpellingWhileTyping -bool true
defaults write com.sleetcrash.MacMD checkGrammarWithSpelling -bool false
```

Version note: `selectedTheme`, `customThemes`, and `themeSchemaVersion` are the theme-restructure keys (post-2.2). That build's one-shot migration DELETED the six legacy keys (`colorScheme`, `themeId`, `backgroundMode`, `customBackground`, `backgroundPreset`, `customPalettes`); writing them against it does nothing. Against a 2.2.x build, use the legacy keys instead: `colorScheme` (off | unified | standard) + `themeId`, `backgroundMode` (default | preset | custom) + `backgroundPreset` (bg.cream | bg.parchment | bg.gray) or `customBackground` (#RRGGBB), and custom palettes as JSON in `customPalettes`. 2.2 also removed `newWindowWidth`/`newWindowHeight`.

Theme ids: `default` (or key absent); tinted `tint.cream`, `tint.parchment`, `tint.gray`; Standard presets `std.rgb`, `std.cmyk`, `std.eva00`, `std.eva01`, `std.eva02`, `std.evaend`; Unified presets `uni.red`, `uni.orange`, `uni.yellow`, `uni.green`, `uni.teal`, `uni.blue`, `uni.purple`, `uni.periwinkle`; customs `custom.<UUID>`. Custom themes persist as JSON in the `customThemes` key (fields: id, name, scheme off|unified|standard, slots, background {light, dark}, isStatic; a static theme stores identical light/dark values and forces the window appearance from its background's luminance). Saved custom backgrounds remain a string array in `customBackgrounds`.

Read current state: `defaults read com.sleetcrash.MacMD`.

## What has NO programmatic interface

- No AppleScript dictionary, no URL scheme, no CLI flags. Menu actions (export, templates, print) need UI automation (accessibility clicks) or the user.
- Export cannot be invoked headlessly. To convert Markdown to HTML/PDF without a human, use a standalone converter instead; MacMD's exports are user-driven.

## Menu map for UI automation

- File: New (Cmd-N), New from Template (Skill, Agent, CLAUDE.md, AGENTS.md), Open, Save, Export to HTML (Cmd-Shift-E), Export to PDF, Print (Cmd-P).
- Edit: Find (Cmd-F), Find and Replace (Cmd-Option-F), Spelling and Grammar toggles.
- Format: Bold (Cmd-B), Italic (Cmd-I), Strikethrough (Shift-Cmd-X), Inline Code, Link (Cmd-K), Toggle Task Checkbox (Cmd-Shift-L).
- View: font size (Cmd-Plus / Cmd-Minus / Cmd-0 reset), Show Word Count, Show Formatting (Cmd-/), Show Line Numbers, Show Toolbar, Show Preview (Cmd-Shift-P), Layout (Editor Only / Split / Preview Only).
- MacMD > Settings (Cmd-,): Appearance tab is transactional (Apply previews, Save persists, closing reverts unsaved Apply); Editing tab takes effect immediately.
- Window chrome: a copy-text button (copies the whole Markdown source) and the three-segment layout control sit at the right end of the format toolbar in every document window (the toolbar auto-hides by default and slides in when the pointer reaches the top of the document).

## Verification tips

- The app logs nothing useful to the unified log; verify UI state with screenshots or the accessibility tree.
- After writing `defaults`, relaunch and confirm with `defaults read`.
- A document saved by MacMD always ends in exactly one trailing newline; byte-compare accordingly.
