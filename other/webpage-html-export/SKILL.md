---
name: webpage-html-export
description: "Export html from single files, canvas pages, or whole vaults. Direct access to the exported HTML files allows you to publish your digital garden anywhere. Focuses on flexibility, features, and style parity."
source: webpage-html-export
---

# Webpage HTML Export

## Plugin metadata

- **id:** `webpage-html-export`
- **source:** vault-native
- **plugin-type:** community
- **status:** enabled
- **class:** PARTIAL
- **has-settings:** true

# Webpage HTML Export

**Description:** Export html from single files, canvas pages, or whole vaults. Direct access to the exported HTML files allows you to publish your digital garden anywhere. Focuses on flexibility, features, and style parity.
**Status:** Enabled
**Plugin ID:** webpage-html-export

## Plugin API

This plugin exposes a JavaScript API. Use call_plugin_api to call these methods:
- `hasOwnProperty` -- call via call_plugin_api("webpage-html-export", "hasOwnProperty", [args])
- `isPrototypeOf` -- call via call_plugin_api("webpage-html-export", "isPrototypeOf", [args])
- `propertyIsEnumerable` -- call via call_plugin_api("webpage-html-export", "propertyIsEnumerable", [args])
- `toString` -- call via call_plugin_api("webpage-html-export", "toString", [args])
- `valueOf` -- call via call_plugin_api("webpage-html-export", "valueOf", [args])
- `toLocaleString` -- call via call_plugin_api("webpage-html-export", "toLocaleString", [args])

Note: Dynamically discovered methods require user approval for each call unless marked as safe in settings.

## Configuration File

Settings path: `.obsidian/plugins/webpage-html-export/data.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/plugins/webpage-html-export/data.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/plugins/webpage-html-export/data.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify data.json directly.

## Current Configuration

These are the plugin's current settings (sensitive values redacted):

```
settingsVersion: 0.0.0
exportOptions:
  createDocumentContainer: true
  keepModHeaderFooter: false
  addPageIcon: true
  unifyTitleFormat: true
  createPusherElement: true
  makeHeadersTrees: true
  postProcess: true
  displayProgress: true
  inlineHTML: false
  useFallbackRenderer: false
  addBodyClasses: true
  addMathjaxStyles: true
  addHeadTag: true
  backlinkOptions:
    featureId: backlinks
    enabled: true
    unavailable: false
    alwaysEnabled: false
    hideSettingsButton: false
    featurePlacement:
      selector: .footer
      type: start
    displayTitle: Backlinks
  tagOptions:
    featureId: tags
    enabled: true
    unavailable: false
    alwaysEnabled: false
    hideSettingsButton: false
    featurePlacement:
      selector: .header .data-bar
      type: end
    showInlineTags: true
    showFrontmatterTags: true
  aliasOptions:
    featureId: aliases
    enabled: true
    unavailable: false
    alwaysEnabled: false
    hideSettingsButton: false
    featurePlacement:
      selector: .header .data-bar
      type: start
    displayTitle: Aliases
  propertiesOptions:
    featureId: properties
    enabled: true
    unavailable: false
    alwaysEnabled: false
    hideSettingsButton: false
    featurePlacement:
      selector: .header
      type: start
    displayTitle: Properties
  fileNavigationOptions:
    featureId: file-navigation
    enabled: true
    unavailable: false
    alwaysEnabled: false
    hideSettingsButton: false
    featurePlacement:
      selector: #left-sidebar-content
      type: end
    showCustomIcons: false
    showDefaultFolderIcons: false
    showDefaultFileIcons: false
    defaultFolderIcon: lucide//folder
    defaultFileIcon: lucide//file
    defaultMediaIcon: lucide//file-image
    exposeStartingPath: true
    includePath: site-lib/html/file-tree.html
  searchOptions:
    featureId: search
    enabled: true
    unavailable: false
    alwaysEnabled: false
    hideSettingsButton: false
    featurePlacement:
      selector: #left-sidebar .topbar-content
      type: start
    displayTitle: Search...
  outlineOptions:
    featureId: outline
    enabled: true
    unavailable: false
    alwaysEnabled: false
    hideSettingsButton: false
    featurePlacement:
      selector: #right-sidebar-content
      type: end
    displayTitle: Outline
    startCollapsed: false
    minCollapseDepth: 0
  themeToggleOptions:
    featureId: theme-toggle
    enabled: true
    unavailable: false
    alwaysEnabled: false
    hideSettingsButton: false
    featurePlacement:
      selector: #right-sidebar .topbar-content
      type: start
  graphViewOptions:
    featureId: graph-view
    enabled: true
    unavailable: false
    alwaysEnabled: false
    hideSettingsButton: false
    featurePlacement:
      selector: #right-sidebar-content
      type: start
    displayTitle: Graph View
    showOrphanNodes: true
    showAttachments: false
    allowGlobalGraph: true
    allowExpand: true
    attractionForce: 1
    linkLength: 15
    repulsionForce: 80
    centralForce: 2
    edgePruning: 100
    minNodeRadius: 3
    maxNodeRadius: 7
  sidebarOptions:
    featureId: sidebar
    enabled: true
    unavailable: false
    alwaysEnabled: false
    hideSettingsButton: false
    allowResizing: true
    allowCollapsing: true
    rightDefaultWidth: 20em
    leftDefaultWidth: 20em
  customHeadOptions:
    featureId: custom-head
    enabled: true
    unavailable: false
    alwaysEnabled: false
    hideSettingsButton: false
    featurePlacement:
      selector: head
      type: end
    includePath: site-lib/html/custom-head.html
  documentOptions:
    featureId: obsidian-document
    enabled: true
    unavailable: false
    alwaysEnabled: true
    hideSettingsButton: false
    allowFoldingLists: true
    allowFoldingHeadings: true
    documentWidth: 40em
  rssOptions:
    featureId: rss
    enabled: true
    unavailable: false
    alwaysEnabled: false
    hideSettingsButton: false
  linkPreviewOptions:
    featureId: link-preview
    enabled: true
    unavailable: false
    alwaysEnabled: false
    hideSettingsButton: true
  relativeHeaderLinks: false
  includeJS: true
  includeCSS: true
  inlineMedia: false
  inlineCSS: false
  inlineJS: false
  inlineFonts: false
  inlineOther: false
  combineAsSingleFile: false
  offlineResources: false
  slugifyPaths: true
  flattenExportPaths: false
  fixLinks: true
  siteName: FORGE-OS
  iconEmojiStyle: Native
  autoDisposeWebpages: true
logLevel: warning
titleProperty: title
rssDateProperty: date
onlyExportModified: true
deleteOldFiles: true
exportPreset: online
openAfterExport: true
filePickerBlacklist: [(^|\/)node_modules\/, (^|\/)dist\/, (^|\/)dist-ssr\/, (^|\/)\.vscode\/]
filePickerWhitelist: [\.\w+$]
```

For full settings, read: `.obsidian/plugins/webpage-html-export/data.json`

## Documentation

For detailed plugin documentation (commands, options, dependencies):
read_file(".vault-operator/data/skills/webpage-html-export.readme.md")

## Usage

When the user asks for functionality related to Webpage HTML Export:
1. Read the plugin documentation (.readme.md) to understand capabilities and dependencies
2. Read the config file (.obsidian/plugins/webpage-html-export/data.json). If it does not exist, that is normal -- create it with the required settings
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
