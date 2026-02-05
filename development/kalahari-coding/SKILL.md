---
name: kalahari-coding
description: Core coding patterns and conventions for Kalahari project. MUST be used by all code-related agents.
---

# Kalahari Coding Standards

## 1. Icons

### ALWAYS
```cpp
core::ArtProvider::getInstance().getIcon("cmd_id")
core::ArtProvider::getInstance().createAction("cmd_id", parent)  // for QAction with auto-refresh
```

### NEVER
```cpp
QIcon("path/to/icon.svg")  // hardcoded path
```

### Available icons
- Location: `resources/icons/`
- Registered in: `icon_registrar.cpp` (gui::registerAllIcons())

## 2. Icon Colors

### ALWAYS
```cpp
QColor primary = core::ArtProvider::getInstance().getPrimaryColor();
QColor secondary = core::ArtProvider::getInstance().getSecondaryColor();
core::ArtProvider::getInstance().setPrimaryColor(QColor("#hex"));
core::ArtProvider::getInstance().setSecondaryColor(QColor("#hex"));
```

### NEVER
```cpp
QColor(255, 0, 0)  // hardcoded color
Theme::instance().getColor()  // DOES NOT EXIST!
```

## 3. Configuration

### ALWAYS
```cpp
auto& settings = core::SettingsManager::getInstance();
std::string value = settings.getValue("key", "default");
settings.setValue("key", "value");
```

### NEVER
```cpp
// hardcoded configuration values
const int MAX_SIZE = 100;  // should be in settings
```

## 4. UI Strings

### ALWAYS
```cpp
tr("User visible text")
tr("Format: %1").arg(value)
```

### NEVER
```cpp
"Hardcoded string"  // not translatable
```

## 5. Themes

### ALWAYS
```cpp
const core::Theme& theme = core::ThemeManager::getInstance().getCurrentTheme();
// Access theme colors:
theme.colors.primary
theme.colors.secondary
theme.palette.toQPalette()
theme.log.info  // log panel colors
```

### Adding New Theme Colors

Use the automated script `scripts/add_theme_color.py` for adding colors to the theme system.

**Basic usage (5 files modified):**
```bash
python scripts/add_theme_color.py <color_name> <dark_value> <light_value> -d "description"
```

**With Settings UI integration (9 files modified):**
```bash
python scripts/add_theme_color.py <color_name> <dark_value> <light_value> -d "description" -l "Label" -s
```

**Parameters:**
- `color_name`: camelCase name (e.g., `infoPrimary`)
- `dark_value`: hex color for Dark theme (e.g., `#6B9BD2`)
- `light_value`: hex color for Light theme (e.g., `#3D6A99`)
- `-d/--description`: description for C++ comments
- `-l/--label`: display label in Settings UI
- `-s/--add-to-settings`: add to Settings dialog UI

**Files modified by script:**
- `resources/themes/Dark.json` - dark theme color value
- `resources/themes/Light.json` - light theme color value
- `include/kalahari/core/theme.h` - QColor member in Theme struct
- `src/core/theme.cpp` - fromJson/toJson serialization
- `src/core/theme_manager.cpp` - fallback, applyColorOverrides, setColorOverride
- (with `-s`): `settings_data.h`, `settings_dialog.h`, `settings_dialog.cpp`, `main_window.cpp`

**Example:**
```bash
python scripts/add_theme_color.py htmlHeading "#4A90D9" "#2E5C8A" -d "HTML heading color" -l "Heading" -s
```

**NEVER add theme colors manually** - always use the script to ensure consistency across all 5-9 files.

## 6. Logging

### ALWAYS
```cpp
core::Logger::getInstance().info("Message: {}", value);
core::Logger::getInstance().debug("Debug: {}", value);
core::Logger::getInstance().warn("Warning: {}", value);
core::Logger::getInstance().error("Error: {}", value);
```

### Levels
- trace, debug, info, warn, error, critical

## 7. Layouts (Qt6)

### Basic patterns
```cpp
QVBoxLayout* mainLayout = new QVBoxLayout(this);
QHBoxLayout* rowLayout = new QHBoxLayout();
QGroupBox* group = new QGroupBox(tr("Title"));
```

### Stretch factors
- 0 = fixed size
- 1+ = flexible, fills available space

### Clearing layouts (ALWAYS use utility)
```cpp
#include "kalahari/gui/utils/layout_utils.h"

// ALWAYS - properly handles nested layouts
kalahari::gui::utils::clearLayout(m_contentLayout);

// NEVER - leaks nested layouts
while (QLayoutItem* item = layout->takeAt(0)) {
    delete item->widget();
    delete item;
}
```

## 8. Build

### Windows
```bash
scripts/build_windows.bat Debug
```

### Linux
```bash
scripts/build_linux.sh
```

### NEVER
- cmake directly
- WSL for Windows builds

## 9. Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Files | snake_case | `character_card.cpp` |
| Classes | PascalCase | `CharacterCard` |
| Methods | camelCase | `getTitle()` |
| Members | m_prefix | `m_title` |
| Constants | UPPER_SNAKE_CASE | `MAX_CHAPTERS` |
| Namespaces | lowercase | `kalahari::core` |

## 10. Singletons Reference

| Class | Access Method | Namespace |
|-------|---------------|-----------|
| ArtProvider | `getInstance()` | `kalahari::core` |
| SettingsManager | `getInstance()` | `kalahari::core` |
| ThemeManager | `getInstance()` | `kalahari::core` |
| IconRegistry | `getInstance()` | `kalahari::core` |
| Logger | `getInstance()` | `kalahari::core` |
| CommandRegistry | `getInstance()` | `kalahari::gui` |

## 11. MCP Tools for Code Intelligence

Use for understanding and navigating Kalahari codebase:
```
```

**When to use:**
- Before modifying any file → understand structure
- Before creating new class → find similar patterns
- Before refactoring → find all usages

### Context7 (External Docs)
Use for Qt6 and other library documentation:
```
mcp__context7__resolve-library-id("Qt6")           # get library ID (once)
mcp__context7__get-library-docs("/qt/qtdoc", topic="QDockWidget")
```

**When to use:**
- Unsure about Qt6 API parameters
- Need to know available signals/slots
- Checking Qt6 best practices

### Tool Selection Guide
| Need | Tool |
|------|------|
| Qt6 API reference | Context7 |
| Qt6 signals/slots | Context7 |
| External library docs | Context7 |
