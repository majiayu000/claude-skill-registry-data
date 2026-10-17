---
name: figma-flutter-mcp-design-to-code
description: Extract Figma design tokens, components, and screens to generate Flutter code using Model Context Protocol (MCP)
triggers:
  - "help me convert this Figma design to Flutter code"
  - "extract design tokens from Figma for Flutter"
  - "generate Flutter widgets from Figma components"
  - "build a Flutter screen from this Figma design"
  - "export Figma assets for my Flutter app"
  - "set up Flutter theme from Figma design system"
  - "analyze this Figma component structure"
  - "get color palette from Figma for Flutter"
---

# Figma Flutter MCP Design to Code

> Skill by [ara.so](https://ara.so) — Design Skills collection.

An MCP (Model Context Protocol) server that bridges Figma designs and Flutter development. It extracts design tokens, components, screens, and assets from Figma, providing structured data that helps AI agents generate production-ready Flutter code following platform conventions.

## What It Does

- **Design Token Extraction**: Colors, typography, spacing from Figma frames
- **Component Analysis**: Structure, layout, styling of Figma components and widgets
- **Screen Generation**: Full screen layouts with scaffolding, navigation, and sections
- **Asset Export**: PNG, JPEG, JPG, and SVG assets with automatic pubspec.yaml updates
- **Flutter-Native Output**: Guidance for Material Design widgets, layouts, and patterns

This is NOT a code generator — it provides rich context that helps AI agents write better Flutter code.

## Installation

### Prerequisites

1. **Figma Access Token**: Create at [Figma Settings > Personal Access Tokens](https://help.figma.com/hc/en-us/articles/8085703771159-Manage-personal-access-tokens)
2. **Node.js 18+** and npm
3. **Cursor AI** or compatible MCP client

### Setup in Cursor

1. Press `CMD + Shift + P` (Windows: `Ctrl + Shift + P`)
2. Type "Open MCP Settings"
3. Click "Add new MCP"
4. Add configuration:

**MacOS/Linux:**
```json
{
  "mcpServers": {
    "Figma Flutter MCP": {
      "command": "npx",
      "args": [
        "-y",
        "figma-flutter-mcp",
        "--figma-api-key=YOUR_FIGMA_API_KEY",
        "--stdio"
      ]
    }
  }
}
```

**Windows:**
```json
{
  "mcpServers": {
    "Figma Flutter MCP": {
      "command": "cmd",
      "args": [
        "/c",
        "npx",
        "-y",
        "figma-flutter-mcp",
        "--figma-api-key=YOUR_FIGMA_API_KEY",
        "--stdio"
      ]
    }
  }
}
```

Replace `YOUR_FIGMA_API_KEY` with your actual token.

### Local Development Setup

```bash
# Clone repository
git clone https://github.com/mhmzdev/figma-flutter-mcp.git
cd figma-flutter-mcp

# Install dependencies
npm install

# Create .env file
echo "FIGMA_API_KEY=your_figma_api_key_here" > .env

# Start HTTP server for testing
npm run dev
```

**Local MCP Configuration:**
```json
{
  "mcpServers": {
    "local-figma-flutter": {
      "url": "http://localhost:3333/mcp"
    }
  }
}
```

## Getting Figma Links

Valid Figma links contain both FILE_ID and NODE_ID:

**Desktop App:**
- Select frame/component
- Press `CMD + L` (Mac) or `Ctrl + L` (Windows)

**Web:**
- Select frame/component
- Copy URL from browser

Example valid URL:
```
https://www.figma.com/file/ABC123/ProjectName?node-id=1%3A2
```

## Core Workflows

### 1. Theme and Typography Setup

Create two Figma frames showing your design system:

**Theme Colors Frame:**
```
Prompt: "Setup Flutter theme from <figma_link> including all color definitions as ColorScheme"
```

The MCP extracts:
- Primary, secondary, tertiary colors
- Surface, background colors
- Error, warning, success states
- Neutral gray scales

**Typography Frame:**
```
Prompt: "Extract typography system from <figma_link> and create TextTheme for Flutter"
```

Returns:
- Font families, weights, sizes
- Line heights, letter spacing
- Text style mappings (displayLarge, bodyMedium, etc.)

**Example Flutter Output:**
```dart
// lib/theme/app_theme.dart
import 'package:flutter/material.dart';

class AppTheme {
  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.light(
        primary: Color(0xFF6750A4),
        secondary: Color(0xFF625B71),
        tertiary: Color(0xFF7D5260),
        surface: Color(0xFFFFFBFE),
        background: Color(0xFFFFFBFE),
      ),
      textTheme: TextTheme(
        displayLarge: TextStyle(
          fontFamily: 'Inter',
          fontSize: 57,
          fontWeight: FontWeight.w400,
          letterSpacing: -0.25,
        ),
        bodyMedium: TextStyle(
          fontFamily: 'Inter',
          fontSize: 14,
          fontWeight: FontWeight.w400,
          letterSpacing: 0.25,
        ),
      ),
    );
  }
}
```

### 2. Widget Generation from Components

**Figma Component (Recommended):**
```
Prompt: "Create Flutter widget from figma COMPONENT link: <figma_link>, use named constructors for variants"
```

MCP analyzes:
- Component variants (enabled/disabled, states)
- Auto-layout properties (padding, spacing, alignment)
- Text content and styling
- Nested structure

**Example Flutter Output:**
```dart
// lib/widgets/custom_button.dart
import 'package:flutter/material.dart';

class CustomButton extends StatelessWidget {
  final String label;
  final VoidCallback? onPressed;
  final bool isEnabled;

  const CustomButton({
    Key? key,
    required this.label,
    this.onPressed,
    this.isEnabled = true,
  }) : super(key: key);

  const CustomButton.disabled({
    Key? key,
    required String label,
  }) : this(
    key: key,
    label: label,
    isEnabled: false,
  );

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: isEnabled ? onPressed : null,
      style: ElevatedButton.styleFrom(
        minimumSize: Size(327, 56),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
        ),
        padding: EdgeInsets.symmetric(horizontal: 24, vertical: 16),
      ),
      child: Text(
        label,
        style: Theme.of(context).textTheme.labelLarge,
      ),
    );
  }
}
```

**Figma Frame (Alternative):**
```
Prompt: "Convert this frame to a Flutter widget from <figma_link>, it should be reusable"
```

### 3. Full Screen Generation

```
Prompt: "Design this screen from figma link <figma_link>, ensure code is modular with separate widget files"
```

MCP identifies:
- Screen dimensions and orientation
- Scaffold structure (AppBar, Body, BottomNavigationBar)
- Navigation patterns
- Content sections
- Image and SVG assets

**Automatic Asset Handling:**
- Exports image assets to `assets/images/`
- Updates `pubspec.yaml` asset declarations
- Generates asset path constants

**Example Flutter Screen:**
```dart
// lib/screens/intro_screen.dart
import 'package:flutter/material.dart';
import 'package:my_app/widgets/custom_button.dart';
import 'package:my_app/theme/app_theme.dart';

class IntroScreen extends StatelessWidget {
  const IntroScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Image.asset(
                'assets/images/intro_illustration.png',
                height: 300,
              ),
              SizedBox(height: 48),
              Text(
                'Welcome to App',
                style: Theme.of(context).textTheme.displaySmall,
                textAlign: TextAlign.center,
              ),
              SizedBox(height: 16),
              Text(
                'Get started with our amazing features',
                style: Theme.of(context).textTheme.bodyLarge,
                textAlign: TextAlign.center,
              ),
              SizedBox(height: 48),
              CustomButton(
                label: 'Get Started',
                onPressed: () {
                  // Navigation logic
                },
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

### 4. Asset Export

**Image Assets (PNG, JPEG, JPG):**
```
Prompt: "Export this image asset from figma link: <figma_link>"
```

Automatically:
- Downloads to `assets/images/`
- Adds to `pubspec.yaml`
- Suggests usage pattern

**SVG Assets:**
```
Prompt: "Export this as SVG asset from Figma link: <figma_link>"
```

**SVG Best Practices:**
- Group icon elements in Figma
- Create dedicated frames for individual SVGs
- Avoid scattered vector nodes

**SVG Usage:**
```dart
// Add flutter_svg to pubspec.yaml
import 'package:flutter_svg/flutter_svg.dart';

SvgPicture.asset(
  'assets/icons/home_icon.svg',
  width: 24,
  height: 24,
  color: Theme.of(context).colorScheme.primary,
)
```

## Configuration

### Cursor Rules (`.cursor/rules/fluttering.mdc`)

Enhance AI output with project-specific rules:

```markdown
# Flutter Code Generation Rules

## Architecture
- Use feature-based folder structure
- Separate widgets into lib/widgets/
- Keep screens in lib/screens/
- Create lib/theme/ for theming

## Code Style
- Always use const constructors where possible
- Prefer named parameters for widgets
- Use Theme.of(context) over hardcoded values
- Follow Flutter/Effective Dart conventions

## Assets
- Image assets in assets/images/
- SVG assets in assets/icons/
- Always declare in pubspec.yaml

## State Management
- Use StatefulWidget for local state
- Mention if using Provider/Riverpod/Bloc

## Naming
- Widgets: PascalCase (CustomButton)
- Files: snake_case (custom_button.dart)
- Variables: camelCase (isEnabled)
```

### Environment Variables

```bash
# .env
FIGMA_API_KEY=figd_your_api_key_here
```

For production or CI/CD:
```bash
export FIGMA_API_KEY=figd_your_api_key_here
npx figma-flutter-mcp --figma-api-key=$FIGMA_API_KEY --stdio
```

## Common Patterns

### Pattern 1: Design System First

1. Create Figma frames for colors and typography
2. Generate theme files first
3. Build components using theme
4. Compose screens from components

### Pattern 2: Component Library

```
Prompt: "Analyze all components in this Figma page <figma_link> and create a Flutter widget library with consistent styling"
```

### Pattern 3: Responsive Layouts

```
Prompt: "Generate responsive Flutter layout from <figma_link> supporting mobile, tablet, and desktop breakpoints"
```

MCP provides:
- Frame dimensions
- Auto-layout constraints
- Responsive hints

Implement with:
```dart
LayoutBuilder(
  builder: (context, constraints) {
    if (constraints.maxWidth > 900) {
      return DesktopLayout();
    } else if (constraints.maxWidth > 600) {
      return TabletLayout();
    }
    return MobileLayout();
  },
)
```

### Pattern 4: Navigation Flows

```
Prompt: "Extract navigation structure from Figma prototype <figma_link> and implement Flutter navigation"
```

Example output structure:
```dart
// lib/routes/app_routes.dart
class AppRoutes {
  static const String intro = '/intro';
  static const String home = '/home';
  static const String profile = '/profile';

  static Route<dynamic> generateRoute(RouteSettings settings) {
    switch (settings.name) {
      case intro:
        return MaterialPageRoute(builder: (_) => IntroScreen());
      case home:
        return MaterialPageRoute(builder: (_) => HomeScreen());
      default:
        return MaterialPageRoute(builder: (_) => NotFoundScreen());
    }
  }
}
```

## Troubleshooting

### Issue: "MCP not responding" or "Tool call failed"

**Solution:**
```bash
# Update to latest version
npx clear-npx-cache
# Or force reinstall
npm uninstall -g figma-flutter-mcp
npx -y figma-flutter-mcp@latest --figma-api-key=$FIGMA_API_KEY --stdio
```

### Issue: Rate Limit (HTTP 429)

**Solution:**
- Wait 5-10 minutes before retrying
- Reduce concurrent requests
- Extract smaller portions of design

**Check rate limit status:**
```typescript
// Server includes retry with exponential backoff
// Wait time increases: 1s → 2s → 4s → 8s
```

### Issue: SVG export includes unwanted nodes

**Solution:**
1. In Figma, group SVG elements: `CMD + G` (Mac) or `Ctrl + G` (Windows)
2. Place in dedicated frame
3. Name frame clearly (e.g., "icon_home")
4. Export individual frame

### Issue: Colors not matching Figma

**Solution:**
- Ensure Figma uses RGB color space
- Check for opacity/blend modes
- Use color picker to verify hex values
- MCP extracts fills in order (first fill is primary)

### Issue: Assets not appearing in Flutter

**Solution:**
```yaml
# pubspec.yaml - verify indentation
flutter:
  assets:
    - assets/images/
    - assets/icons/
```

Then:
```bash
flutter pub get
flutter clean
flutter run
```

### Issue: Text styles incorrect

**Solution:**
- Use Figma Text Styles (not local overrides)
- Check font is available in Flutter project
- Add custom fonts to pubspec.yaml:

```yaml
flutter:
  fonts:
    - family: Inter
      fonts:
        - asset: fonts/Inter-Regular.ttf
        - asset: fonts/Inter-Bold.ttf
          weight: 700
```

## Advanced Usage

### Batch Processing Multiple Components

```
Prompt: "Process all button variants from Figma file <file_link>, create Flutter widget with factory constructors for each variant"
```

### Custom Widget Properties

```
Prompt: "Convert <figma_link> to Flutter, add properties for: onTap callback, custom icon, theme override"
```

### Animation Extraction

```
Prompt: "Analyze transition animations from Figma prototype <figma_link>, suggest Flutter animation implementation"
```

MCP provides timing and easing data for:
```dart
AnimatedContainer(
  duration: Duration(milliseconds: 300),
  curve: Curves.easeInOut,
  // ... properties
)
```

## Best Practices

1. **Organize Figma files**: Use clear naming, components, and auto-layout
2. **Start with design system**: Colors and typography first
3. **Use Figma components**: Better structure than grouped frames
4. **Test incrementally**: Generate one widget at a time
5. **Review and refine**: MCP provides guidance, not final code
6. **Follow Flutter conventions**: Use Material Design or Cupertino patterns
7. **Keep assets organized**: Separate images, icons, and other resources

## Resources

- [Full Documentation](https://github.com/mhmzdev/figma-flutter-mcp)
- [Video Tutorial (English)](https://youtu.be/lJlfOfpl2sI)
- [Figma API Reference](https://www.figma.com/developers/api)
- [Flutter Widget Catalog](https://docs.flutter.dev/ui/widgets)

---

**Remember**: This MCP provides context and guidance. The AI agent generates actual Flutter code based on this context and your project rules.
