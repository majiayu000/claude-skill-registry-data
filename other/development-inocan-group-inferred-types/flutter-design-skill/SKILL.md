---
name: flutter-design-skill
description: This skill provides the Comic style UI design guideline and code to make the Flutter app look better. ALWAYS use this skill when the user asks to create, update, design, modify, or build any page, screen, widget, or UI component in a Flutter application.
---

# Flutter Design Overview

- This skill provides the Comic style UI design guideline and code.
- It ensures that the Flutter application will have Comic UI style.

# When to Use

- Use this skill when the user requests to design or improve the UI of a Flutter application.
- Use this skill when the user mention Comic style UI design.

# Design Guidelines

- Refer to the [comic-theme.md](./comic-theme.md) for detailed design guidelines and code examples.

# Comic Design Rules

- Follow these critical design rules when implementing the Comic style UI in Flutter.

- **Reusable Flutter Widgets**: Always re-use or create a re-usable widgets to not repeat code.

  - For example, create a `./lib/widgets/theme/ComicButton` widget instead of styling each button individually.
  - all of the `Comic` widgets must be saved in `./lib/widgets/theme/comic_<component_name>.dart`
  - It must create re-usable widgets for common UI elements like buttons, cards, text fields, etc.

- **Comic Design**: Always follow these Comic design principles:

  - **Border**:
    - Standard elements: `2.0` thickness
    - List-based widgets (ListTile, compact cards): `1.5` thickness for lighter visual weight
  - **No shadow**: Always no shadows
  - **No elevation**: Always zero elevation
  - **Outline**: Use outline color for borders
  - **Rounded corners**: The border radius must be `12` for large elements, `8` for other elements.
  - **Colors**: Use the Theme Primary Color for primary elements.
    - Use the Theme Secondary Color for secondary elements.
    - Use the Theme Surface Color for cards and containers.
    - Use the Theme Background Color for the surface color.
    - Use the Theme onSurface Color for text and icons on surface color.
  - **Fonts**: Use the Theme Text Styles for all text elements.
    - Use `bodyLarge` for regular text.
    - Use `titleMedium` for titles.
    - Use `labelLarge` for buttons.

- **Spacing**: Use multiples of 8 (8, 16, 24, 32, etc.)

## Theme Design Guidelines

**CRITICAL FLUTTER RULES:**

- **Use Theme ONLY**: Always use `Theme.of(context)` for colors, fonts, and styles. NEVER hardcode them.

❌ NEVER DO:

```dart
Text('Login')  // Hardcoded text
color: Colors.blue  // Hardcoded color
fontSize: 16  // Hardcoded size
border: Border.all()  // Borders not allowed
elevation: 4  // Must be 0
ElevatedButton(child: Text('Click', style: TextStyle(...)))  // Inline style overrides Theme
```

✅ ALWAYS DO:

```dart
Text(T.login)  // i18n translation
color: Theme.of(context).colorScheme.primary  // Theme color
style: Theme.of(context).textTheme.bodyLarge  // Theme text style
elevation: 0  // Flat design
ElevatedButton(child: Text(T.click))  // Let Theme handle styling
```

# ComicButton System

## Concept & Intent

The **ComicButton** system is a unified, reusable button component library that implements the Comic design language across the entire Flutter application. Instead of styling buttons individually with inline styles, all buttons use the `ComicButton` base widget or its variants.

**Key Benefits:**

- **Consistency**: All buttons share the same Comic design DNA (2px border, no shadow, rounded corners)
- **Flexibility**: Three design options (`rounded`, `padding`, `textSize`) allow creating any button style
- **Maintainability**: Change the button style in one place, update everywhere
- **Theme Integration**: Automatically uses Theme colors and text styles

## Core Design Principles

All ComicButton variants follow these Comic design rules:

- **Border**: 2.0px thickness with outline color
- **Elevation**: Always 0 (flat design, no shadows)
- **Corners**: Rounded with borderRadius 12 (normal) or fully rounded (full/pill)
- **Colors**: Theme-based (surface, primary, secondary)
- **Typography**: Theme text styles (bodyLarge, titleMedium, bodyMedium)
- **Spacing**: Padding in multiples of 8

## Design Options

Every `ComicXxxButton` variant supports three design option enums:

### ComicButtonRounded

Controls the corner shape of the button.
| Value | Description | Use Case |
|-------|-------------|----------|
| `full` | Pill/stadium shape (StadiumBorder) | CTA buttons, login buttons |
| `normal` | Rounded corners (borderRadius: 12) | Standard buttons |

### ComicButtonPadding

Controls the internal padding of the button.
| Value | Padding | Use Case |
|-------|---------|----------|
| `large` | 32×20 | Important action buttons (login, submit) |
| `medium` | 24×16 | Standard buttons (default) |
| `small` | 16×12 | Compact buttons, inline actions |

### ComicButtonTextSize

Controls the text size inside the button.
| Value | Text Style | Use Case |
|-------|------------|----------|
| `large` | titleMedium | Important action buttons |
| `medium` | bodyLarge | Standard buttons (default) |
| `small` | bodyMedium | Compact buttons |

## Button Variants

### ComicButton (Base)

The foundation widget with neutral colors (surface background, onSurface text).

```dart
// Standard button
ComicButton(
  onPressed: () => doSomething(),
  child: Text(Lo.of(context)!.action),
)

// Large login button (pill shape)
ComicButton(
  onPressed: () => login(),
  rounded: ComicButtonRounded.full,
  padding: ComicButtonPadding.large,
  textSize: ComicButtonTextSize.large,
  child: Text(Lo.of(context)!.login),
)
```

### ComicPrimaryButton

Primary action button using Theme primary color.

```dart
ComicPrimaryButton(
  onPressed: () => submit(),
  rounded: ComicButtonRounded.full,
  padding: ComicButtonPadding.large,
  textSize: ComicButtonTextSize.large,
  child: Text(Lo.of(context)!.submit),
)
```

### ComicSecondaryButton

Secondary action button using Theme secondary color.

```dart
ComicSecondaryButton(
  onPressed: () => cancel(),
  padding: ComicButtonPadding.small,
  textSize: ComicButtonTextSize.small,
  child: Text(Lo.of(context)!.cancel),
)
```

## Quick Reference

| Button Style | rounded  | padding  | textSize |
| ------------ | -------- | -------- | -------- |
| Large CTA    | `full`   | `large`  | `large`  |
| Standard     | `normal` | `medium` | `medium` |
| Compact      | `normal` | `small`  | `small`  |

## File Location

All ComicButton widgets are defined in:
`./lib/widgets/theme/comic_button.dart`

# ComicTextFormField

## Concept & Intent

The **ComicTextFormField** is a reusable text input component that implements the Comic design language. It provides a consistent way to create text input fields across the entire Flutter application with Comic-style borders, proper spacing, and theme integration.

**Key Benefits:**

- **Consistency**: All text fields share the same Comic design DNA (2px border, no shadow, rounded corners)
- **Flexibility**: Extensive customization options while maintaining Comic design principles
- **Maintainability**: Change the text field style in one place, update everywhere
- **Theme Integration**: Automatically uses Theme colors and text styles

## Design Principles

All ComicTextFormField instances follow these Comic design rules:

- **Border**: 1.0px thickness with outline color (customizable) - lighter weight for compact input fields
- **Elevation**: Always 0 (flat design, no shadows)
- **Corners**: Rounded with borderRadius 12 (customizable)
- **Colors**: Theme-based (surface background, outline border, primary focus, error)
- **Typography**: Theme text styles (bodyLarge for content, bodyMedium for label/hint)
- **Spacing**: Content padding in multiples of 8

## Key Features

- **Full TextFormField API**: Supports all standard TextFormField parameters
- **Customizable Borders**: Configure border color, focus color, error color, width, and radius
- **Theme Integration**: Uses Theme colors for all visual elements
- **Validation Support**: Built-in validator and error text display
- **Input Control**: Supports read-only, enabled/disabled, obscure text, keyboard type
- **Icons**: Prefix and suffix icon support
- **Multi-line**: Configurable min/max lines for single or multi-line input
- **Length Control**: Maximum length with counter

## Usage Examples

### Basic Text Field

```dart
ComicTextFormField(
  controller: _nameController,
  labelText: T.fullName,
  hintText: T.fullNameHint,
)
```

### Password Field

```dart
ComicTextFormField(
  controller: _passwordController,
  labelText: T.password,
  hintText: T.enterPassword,
  obscureText: true,
  prefixIcon: Icon(Icons.lock),
)
```

### With Validation

```dart
ComicTextFormField(
  controller: _emailController,
  labelText: T.email,
  hintText: T.enterEmail,
  keyboardType: TextInputType.emailAddress,
  validator: (value) {
    if (value == null || value.isEmpty) {
      return T.emailRequired;
    }
    return null;
  },
)
```

### Multi-line Text Area

```dart
ComicTextFormField(
  controller: _bioController,
  labelText: T.bio,
  hintText: T.enterBio,
  maxLines: 5,
  minLines: 3,
  maxLength: 500,
)
```

### Disabled Field

```dart
ComicTextFormField(
  controller: _nicknameController,
  labelText: T.nickname,
  hintText: T.nicknameHint,
  enabled: false, // or readOnly: true
)
```

## Customization Options

### Border Styling

```dart
ComicTextFormField(
  controller: _controller,
  labelText: T.label,
  // Custom border styling
  borderWidth: 1.0,        // Default: 1.0
  borderRadius: 12,        // Default: 12
  borderColor: Colors.grey,
  focusedBorderColor: Colors.blue,
  errorBorderColor: Colors.red,
)
```

### Content Padding

```dart
ComicTextFormField(
  controller: _controller,
  labelText: T.label,
  // Custom padding (default: symmetric horizontal: 16, vertical: 16)
  contentPadding: EdgeInsets.all(20),
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| controller | TextEditingController? | null | Text field controller |
| labelText | String? | null | Label text displayed above input |
| hintText | String? | null | Hint text shown when empty |
| errorText | String? | null | Error message to display |
| prefixIcon | Widget? | null | Icon at the start of the field |
| suffixIcon | Widget? | null | Icon at the end of the field |
| keyboardType | TextInputType? | null | Keyboard type for input |
| obscureText | bool | false | Hide text for passwords |
| onChanged | ValueChanged<String>? | null | Callback when text changes |
| onFieldSubmitted | ValueChanged<String>? | null | Callback on submit |
| validator | String? Function(String?)? | null | Validation function |
| readOnly | bool | false | Prevent editing |
| enabled | bool | true | Enable/disable field |
| maxLines | int? | 1 | Maximum lines |
| minLines | int? | null | Minimum lines |
| maxLength | int? | null | Maximum characters |
| autofocus | bool | false | Auto focus on load |
| borderColor | Color? | null | Border color (default: outline) |
| focusedBorderColor | Color? | null | Focus border (default: primary) |
| errorBorderColor | Color? | null | Error border (default: error) |
| borderWidth | double | 1.0 | Border thickness |
| borderRadius | double | 12 | Corner radius |
| contentPadding | EdgeInsetsGeometry? | null | Internal padding |

## Border States

ComicTextFormField automatically handles five border states:

1. **Enabled Border**: Default state (outline color, 1.0px)
2. **Focused Border**: When field has focus (primary color, 1.0px)
3. **Error Border**: When validation fails (error color, 1.0px)
4. **Focused Error Border**: Error state with focus (error color, 1.0px)
5. **Disabled Border**: When field is disabled (outline with 50% opacity, 1.0px)

## File Location

ComicTextFormField is defined in:
`./lib/widgets/theme/comic_text_form_field.dart`

# List-Based Widgets Design

For list-based content such as `ListTile` and `Compact Cards`:

## Design Principles

- **Border**: Use `1.0` thickness (thinner than standard 2.0) for lighter visual weight in compact lists
- **Border Radius**: `12` for rounded corners
- **Elevation**: `0` (no shadow)
- **Margin**: `EdgeInsets.zero` (parent controls spacing)
- **Colors**: Use Theme colors (surface, outline, onSurface)

### Key Features

```dart
Card(
  elevation: 0, // Comic Design: no shadow
  margin: EdgeInsets.zero, // No margin (parent controls spacing)
  color: Theme.of(context).colorScheme.surface,
  // Comic Design: thinner border with rounded corners for compact list
  shape: RoundedRectangleBorder(
    borderRadius: BorderRadius.circular(12),
    side: BorderSide(
      color: Theme.of(context).colorScheme.outline,
      width: 1.0, // Thinner border for list items
    ),
  ),
  child: InkWell(
    onTap: onTap,
    borderRadius: BorderRadius.circular(12), // Match card radius for ripple
    child: // ... content
  ),
)
```

# ComicModalBottomSheet

## Concept & Intent

The **ComicModalBottomSheet** is a reusable modal bottom sheet component that implements the Comic design language. It provides a consistent way to display modal content from the bottom of the screen with Comic-style rounded top corners, proper spacing, and an integrated drag handle.

## Design Principles

- **Border Radius**: `12.0` for top-left and top-right corners (creates Comic-style rounded top)
- **Border Width**: `2.0` thickness on top, left, and right sides (no border on bottom)
- **Elevation**: `0` (flat design, no shadows)
- **Colors**: Theme-based (surface background, outline border)
- **Spacing**: Consistent padding using multiples of 8
- **Drag Handle**: Custom drag handle integrated inside the container (32px × 4px)

## Usage

```dart
// Show Comic Modal Bottom Sheet with integrated drag handle
showModalBottomSheet(
  context: context,
  backgroundColor: Colors.transparent, // Comic Design: transparent for custom styling
  elevation: 0, // Comic Design: no shadow
  builder: (context) {
    return Container(
      decoration: BoxDecoration(
        color: Theme.of(context).colorScheme.surface,
        borderRadius: const BorderRadius.only(
          topLeft: Radius.circular(12.0), // Comic Design: rounded top corners
          topRight: Radius.circular(12.0),
        ),
        border: Border(
          top: BorderSide(
            color: Theme.of(context).colorScheme.outline,
            width: 2.0, // Comic Design: 2.0 border
          ),
          left: BorderSide(
            color: Theme.of(context).colorScheme.outline,
            width: 2.0,
          ),
          right: BorderSide(
            color: Theme.of(context).colorScheme.outline,
            width: 2.0,
          ),
          // No bottom border
        ),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Drag handle indicator
          // Comic Design: 8px spacing from top
          const SizedBox(height: 8),
          Container(
            width: 32,
            height: 4,
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.onSurfaceVariant.withValues(alpha: 0.4),
              borderRadius: BorderRadius.circular(2),
            ),
          ),
          const SizedBox(height: 8),
          // Your content here (wrapped in Flexible if scrollable)
          Flexible(
            child: ListView(
              shrinkWrap: true,
              children: [
                // Your list items
              ],
            ),
          ),
        ],
      ),
    );
  },
);
```

## Key Features

- **Rounded Top Corners**: 12.0 radius on top-left and top-right for Comic style
- **Selective Borders**: Border on top, left, and right only (no bottom border)
- **Theme Integration**: Uses Theme colors for surface and outline
- **No Shadow**: Elevation set to 0 for flat design
- **Transparent Background**: Parent backgroundColor set to transparent for custom styling
- **Integrated Drag Handle**: Custom drag handle (32×4px) with proper spacing inside the container
- **Flexible Layout**: Uses Column with MainAxisSize.min and Flexible for proper sizing

## Drag Handle Specifications

- **Size**: 32px wide × 4px tall
- **Color**: `onSurfaceVariant` with 40% opacity
- **Border Radius**: 2px for rounded corners
- **Spacing**: 8px top and bottom (multiples of 8)
- **Position**: Inside the container, above the content

## Best Practices

- Always use `backgroundColor: Colors.transparent` in `showModalBottomSheet`
- Apply `elevation: 0` to maintain flat design
- Use Theme colors for consistency
- Wrap the Container's child in a Column with `mainAxisSize: MainAxisSize.min`
- Add the drag handle as the first element in the Column
- Use `Flexible` wrapper for scrollable content (ListView, GridView, etc.)
- Use `shrinkWrap: true` for ListView to allow proper sizing
- Add appropriate spacing (multiples of 8) around content

# Comic AppBar Design

## Concept & Intent

The **Comic AppBar** implements the Comic design language for app bars and header sections. It provides consistent styling with a characteristic 1.0px bottom border using the outlineVariant color, creating a subtle visual separation between the header and content areas that matches the bottom navigation bar style.

## Design Principles

- **Border**: 1.0px bottom border with outlineVariant color (matches bottom navigation bar)
- **Typography**: Use Theme titleLarge text style for titles
- **Height**: Standard AppBar height (56px) or custom heights for special cases
- **Colors**: Theme-based (surface background, outlineVariant border, onSurface text)
- **No Elevation**: Always 0 (flat design, no shadows)

## Usage Patterns

### Pattern 1: Standard Scaffold AppBar

Use this pattern when you have a `Scaffold` widget with an `appBar` property.

```dart
Scaffold(
  appBar: AppBar(
    title: Text(T.editProfile, style: theme.textTheme.titleLarge),
    bottom: PreferredSize(
      preferredSize: const Size.fromHeight(1),
      child: Container(height: 1, color: scheme.outlineVariant),
    ),
  ),
  body: // Your content here
)
```

**Key Features:**
- Uses standard `AppBar` widget
- Title uses `titleLarge` text style from Theme
- Bottom border achieved using `PreferredSize` with 1.0px height Container
- Border color uses Theme `outlineVariant` color (matches bottom navigation bar)

### Pattern 2: Custom Header (Without Scaffold)

Use this pattern when you need an app bar-like header without a Scaffold (e.g., in special layouts, custom scrolling views, or nested navigation).

```dart
SafeArea(
  child: Container(
    height: 56, // Standard AppBar height
    padding: const EdgeInsets.only(right: 4, left: 12),
    decoration: BoxDecoration(
      border: Border(
        bottom: BorderSide(
          // Comic Design: 1.0px border with outlineVariant color (matches bottom nav)
          color: Theme.of(context).colorScheme.outlineVariant,
          width: 1.0,
        ),
      ),
    ),
    child: Row(
      children: [
        // Title
        Expanded(
          child: Text(
            T.pageTitle,
            style: Theme.of(context)
                .textTheme
                .titleLarge
                ?.copyWith(fontWeight: FontWeight.w600),
            overflow: TextOverflow.ellipsis,
          ),
        ),
        // Action buttons (optional)
        IconButton(
          icon: const FaIcon(FontAwesomeIcons.someIcon),
          onPressed: () {
            // Action handler
          },
        ),
      ],
    ),
  ),
)
```

**Key Features:**
- Uses `Container` with bottom border decoration
- Wrapped in `SafeArea` for proper top spacing
- Height set to 56px (standard AppBar height)
- Padding adjusts for left/right spacing
- Border applied only to bottom (1.0px with outlineVariant color, matches bottom navigation bar)
- Title uses `titleLarge` text style
- Supports action buttons via `IconButton` or other widgets

## Design Specifications

| Property | Value | Description |
|----------|-------|-------------|
| **Height** | 56px | Standard AppBar height |
| **Border Position** | Bottom only | Visual separation from content |
| **Border Width** | 1.0px | Subtle border matching bottom navigation bar |
| **Border Color** | `colorScheme.outlineVariant` | Theme outlineVariant color (matches bottom nav) |
| **Title Style** | `titleLarge` | Theme text style |
| **Elevation** | 0 | Flat design (no shadow) |
| **Padding** | Left: 12px, Right: 4px | Balanced spacing for text and icons |

## When to Use Each Pattern

### Use Pattern 1 (Scaffold AppBar) when:
- Building a standard screen with Scaffold
- Need standard AppBar features (back button, actions, etc.)
- Want Flutter's built-in AppBar behavior

### Use Pattern 2 (Custom Header) when:
- Working without a Scaffold widget
- Building custom scrolling layouts
- Creating nested navigation structures
- Need more control over header layout and behavior
- Implementing complex header interactions (e.g., dropdown menus, category pickers)

## Example: Header with Action Buttons

```dart
SafeArea(
  child: Container(
    height: 56,
    padding: const EdgeInsets.only(right: 4, left: 12),
    decoration: BoxDecoration(
      border: Border(
        bottom: BorderSide(
          color: Theme.of(context).colorScheme.outlineVariant,
          width: 1.0,
        ),
      ),
    ),
    child: Row(
      children: [
        Expanded(
          child: Text(
            T.categories,
            style: Theme.of(context)
                .textTheme
                .titleLarge
                ?.copyWith(fontWeight: FontWeight.w600),
            overflow: TextOverflow.ellipsis,
          ),
        ),
        IconButton(
          icon: const FaIcon(FontAwesomeIcons.penToSquare),
          onPressed: () {
            // Create new item
          },
        ),
        IconButton(
          icon: const FaIcon(FontAwesomeIcons.chevronDown),
          onPressed: () {
            // Show dropdown menu
          },
        ),
      ],
    ),
  ),
)
```

## Best Practices

- **Always** use Theme colors (outlineVariant for border, titleLarge for text)
- **Always** set border width to 1.0px for consistency with bottom navigation bar
- **Always** apply border only to the bottom (not top/left/right)
- **Always** use SafeArea when implementing custom headers
- **Never** add elevation or shadows
- Use `overflow: TextOverflow.ellipsis` for long titles
- Use multiples of 8 for padding and spacing
- Maintain 56px height for consistency with standard AppBar

# Comic Modal

## Concept & Intent

The **ComicModal** is a reusable modal bottom sheet component that implements the Comic design language. It provides a consistent way to display modal content from the bottom of the screen with Comic-style rounded top corners, proper spacing, and an integrated drag handle.

**Key Benefits:**

- **Consistency**: All modals share the same Comic design DNA (2px border, no shadow, rounded top corners)
- **Flexibility**: Extensive customization options while maintaining Comic design principles
- **Maintainability**: Change the modal style in one place, update everywhere
- **Theme Integration**: Automatically uses Theme colors and text styles
- **Easy to Use**: Helper function `showComicModal()` simplifies modal creation

## Design Principles

All ComicModal instances follow these Comic design rules:

- **Border**: 2.0px thickness on top, left, and right sides (no bottom border) with outline color
- **Elevation**: Always 0 (flat design, no shadows)
- **Corners**: Rounded top corners with borderRadius 12
- **Colors**: Theme-based (surface background, outline border)
- **Spacing**: Consistent padding using multiples of 8
- **Drag Handle**: Custom drag handle (32px × 4px) with proper spacing inside the container

## Usage Examples

### Basic Modal

```dart
// Simple modal with basic content
showComicModal(
  context: context,
  builder: (context) => ComicModal(
    child: Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Padding(
          padding: EdgeInsets.all(16),
          child: Text(
            'Modal Title',
            style: Theme.of(context).textTheme.titleLarge,
          ),
        ),
        Padding(
          padding: EdgeInsets.fromLTRB(16, 0, 16, 16),
          child: Text('Modal content goes here'),
        ),
      ],
    ),
  ),
);
```

### Modal with List Items

```dart
// Modal with selectable list items
final result = await showComicModal<String>(
  context: context,
  builder: (context) => ComicModal(
    child: Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Padding(
          padding: EdgeInsets.all(16),
          child: Text(
            'Select an option',
            style: Theme.of(context).textTheme.titleLarge,
          ),
        ),
        ListTile(
          title: Text('Option 1'),
          onTap: () => Navigator.pop(context, 'option1'),
        ),
        ListTile(
          title: Text('Option 2'),
          onTap: () => Navigator.pop(context, 'option2'),
        ),
        ListTile(
          title: Text('Option 3'),
          onTap: () => Navigator.pop(context, 'option3'),
        ),
      ],
    ),
  ),
);

if (result != null) {
  print('Selected: $result');
}
```

### Scrollable Modal with Long Content

```dart
// Modal with scrollable content
showComicModal(
  context: context,
  isScrollControlled: true,
  builder: (context) => ComicModal(
    maxHeightFactor: 0.9, // Use 90% of screen height
    child: ListView.builder(
      shrinkWrap: true,
      itemCount: 50,
      itemBuilder: (context, index) {
        return ListTile(
          title: Text('Item $index'),
          onTap: () => Navigator.pop(context),
        );
      },
    ),
  ),
);
```

### Modal with Custom Padding

```dart
// Modal with custom content padding
showComicModal(
  context: context,
  builder: (context) => ComicModal(
    contentPadding: EdgeInsets.all(24),
    child: Column(
      mainAxisSize: MainAxisSize.min,
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Terms & Conditions',
          style: Theme.of(context).textTheme.titleLarge,
        ),
        SizedBox(height: 16),
        Text('Your terms and conditions content here...'),
        SizedBox(height: 16),
        Row(
          mainAxisAlignment: MainAxisAlignment.end,
          children: [
            ComicButton(
              onPressed: () => Navigator.pop(context, false),
              child: Text('Decline'),
            ),
            SizedBox(width: 8),
            ComicPrimaryButton(
              onPressed: () => Navigator.pop(context, true),
              child: Text('Accept'),
            ),
          ],
        ),
      ],
    ),
  ),
);
```

### Modal without Drag Handle

```dart
// Modal without drag handle (cleaner look for simple content)
showComicModal(
  context: context,
  builder: (context) => ComicModal(
    showDragHandle: false,
    contentPadding: EdgeInsets.all(16),
    child: Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Text('Simple notification'),
        SizedBox(height: 8),
        ComicButton(
          onPressed: () => Navigator.pop(context),
          child: Text('OK'),
        ),
      ],
    ),
  ),
);
```

## ComicModal Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| child | Widget | required | The content widget to display in the modal |
| showDragHandle | bool | true | Whether to show the drag handle indicator at the top |
| backgroundColor | Color? | null | Background color (default: Theme surface color) |
| borderColor | Color? | null | Border color (default: Theme outline color) |
| borderWidth | double | 2.0 | Border thickness (Comic standard) |
| borderRadius | double | 12 | Corner radius for top corners |
| contentPadding | EdgeInsetsGeometry? | null | Custom padding around content (optional) |
| maxHeightFactor | double? | null | Maximum height as fraction of screen (0.0 to 1.0) |

## showComicModal() Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| context | BuildContext | required | BuildContext for showing the modal |
| builder | Function | required | Builder function that returns the modal content |
| isScrollControlled | bool | false | Whether modal should expand to fill available space |
| isDismissible | bool | true | Whether modal can be dismissed by tapping outside |
| enableDrag | bool | true | Whether modal can be dragged down to dismiss |
| useSafeArea | bool | true | Whether to wrap content in SafeArea |

## Design Specifications

| Property | Value | Description |
|----------|-------|-------------|
| **Border Position** | Top, Left, Right | No border on bottom (seamless with screen edge) |
| **Border Width** | 2.0px | Comic standard thickness |
| **Border Radius** | 12px | Rounded top corners only |
| **Border Color** | `colorScheme.outline` | Theme outline color |
| **Background** | `colorScheme.surface` | Theme surface color |
| **Elevation** | 0 | Flat design (no shadow) |
| **Drag Handle Width** | 32px | Standard width for handle |
| **Drag Handle Height** | 4px | Standard height for handle |
| **Drag Handle Spacing** | 8px top & bottom | Multiples of 8 spacing |
| **Drag Handle Color** | `onSurfaceVariant` (40% opacity) | Subtle indicator |

## When to Use ComicModal

### Use ComicModal when:
- Displaying action sheets or option menus
- Showing forms that slide up from bottom
- Presenting filters or settings panels
- Displaying contextual content that doesn't need full screen
- Creating slide-up confirmation dialogs
- Showing lists of selectable items
- Implementing bottom sheets for mobile-first design

### Use ComicDialog instead when:
- Need center-screen alert/confirmation
- Content is critical and requires immediate attention
- Blocking user interaction is necessary
- Content is brief and doesn't benefit from bottom positioning

## Best Practices

- **Always** use `showComicModal()` helper function instead of `showModalBottomSheet()` directly
- **Always** wrap modal content in `ComicModal` widget for consistent styling
- **Set** `isScrollControlled: true` when content might be taller than half screen
- **Use** `maxHeightFactor` to limit modal height for very long content
- **Set** `shrinkWrap: true` for ListView/GridView inside modal
- **Wrap** content in Column with `mainAxisSize: MainAxisSize.min` for auto-sizing
- **Use** `contentPadding` for consistent spacing or control padding in your content
- **Pass** result via `Navigator.pop(context, value)` to return data to caller
- **Use** Theme colors and text styles for all content
- **Test** with SafeArea enabled (default) to ensure proper spacing on all devices
- **Consider** disabling drag handle (`showDragHandle: false`) for simple, non-scrollable content

## Comparison: Before vs After

### ❌ Before (Manual Styling)

```dart
// Old style: Manual border/styling in every modal
showModalBottomSheet(
  context: context,
  builder: (context) {
    return Container(
      decoration: BoxDecoration(
        color: Theme.of(context).colorScheme.surface,
        borderRadius: BorderRadius.only(
          topLeft: Radius.circular(12),
          topRight: Radius.circular(12),
        ),
        border: Border(
          top: BorderSide(color: Theme.of(context).colorScheme.outline, width: 2),
          left: BorderSide(color: Theme.of(context).colorScheme.outline, width: 2),
          right: BorderSide(color: Theme.of(context).colorScheme.outline, width: 2),
        ),
      ),
      child: // ... complex setup
    );
  },
);
```

### ✅ After (Comic Style)

```dart
// Comic style: Clean, consistent, reusable
showComicModal(
  context: context,
  builder: (context) => ComicModal(
    child: // ... your content
  ),
);
```

## File Location

ComicModal widget and helper function are defined in:
`./lib/widgets/theme/comic_modal.dart`

Import:
```dart
import 'package:philgo/widgets/theme/comic_modal.dart';
```

# Comic SnackBar

## Concept & Intent

The **Comic SnackBar** system provides helper functions to display notification messages that follow Comic design principles. Instead of using the standard `ScaffoldMessenger.of(context).showSnackBar()` with inline styling, use the pre-built Comic SnackBar functions for consistent, theme-based notifications.

## Design Principles

All Comic SnackBars follow these design rules:

- **Border**: 2.0px thickness with semantic colors (green, red, blue, orange)
- **Elevation**: Always 0 (flat design, no shadows)
- **Corners**: Rounded with borderRadius 12
- **Colors**: Semantic colors with lower contrast for softer appearance:
  - Success: Medium green border (#66BB6A) on very light green background (#F1F8F4)
  - Error: Medium red border (#EF5350) on very light red background (#FFF5F5)
  - Info: Medium blue border (#42A5F5) on very light blue background (#F3F8FC)
  - Warning: Medium orange border (#FFA726) on very light orange background (#FFF8F0)
- **Typography**: Theme bodyMedium text style with medium-tone colored text for comfortable readability
- **Spacing**: Padding and margins in multiples of 8
- **Behavior**: Floating style with proper margins

## Available Functions

### showComicSuccessSnackBar

Displays a success message with green color scheme.

```dart
showComicSuccessSnackBar(context, T.profileUpdateSuccess);
```

**Use Cases:**
- Form submission success
- Profile update success
- Data saved successfully
- Action completed successfully

**Visual Style:**
- Background: Very light green (#F1F8F4)
- Text: Medium dark green (#2E7D32)
- Border: Medium green (#66BB6A, 2.0px)

### showComicErrorSnackBar

Displays an error message with red color scheme.

```dart
showComicErrorSnackBar(context, T.nicknameRequired);
```

**Use Cases:**
- Validation errors
- Failed operations
- Required field warnings
- API errors

**Visual Style:**
- Background: Very light red (#FFF5F5)
- Text: Medium dark red (#C62828)
- Border: Medium red (#EF5350, 2.0px)

### showComicInfoSnackBar

Displays an informational message with blue color scheme.

```dart
showComicInfoSnackBar(context, T.pleaseWait);
```

**Use Cases:**
- Informational messages
- Status updates
- General notifications
- Neutral messages

**Visual Style:**
- Background: Very light blue (#F3F8FC)
- Text: Medium dark blue (#1565C0)
- Border: Medium blue (#42A5F5, 2.0px)

### showComicWarningSnackBar

Displays a warning message with orange color scheme.

```dart
showComicWarningSnackBar(context, T.pleaseCheckInput);
```

**Use Cases:**
- Warning messages
- Cautionary notices
- Input validation warnings
- Non-critical issues

**Visual Style:**
- Background: Very light orange (#FFF8F0)
- Text: Medium dark orange (#EF6C00)
- Border: Medium orange (#FFA726, 2.0px)

## Usage Examples

### Basic Success Message

```dart
// After successful form submission
final user = await philgoApiUserUpdate(data);
if (mounted) {
  AppState.of(context).setUser(user);
  showComicSuccessSnackBar(context, T.profileUpdateSuccess);
}
```

### Validation Error

```dart
// Form validation
if (_nicknameController.text.trim().isEmpty) {
  showComicErrorSnackBar(context, T.nicknameRequired);
  return;
}
```

### Error Handling

```dart
try {
  await philgoApiFileDelete(photoUrl);
  showComicSuccessSnackBar(context, T.photoDeleted);
} catch (e) {
  showComicErrorSnackBar(context, 'Failed to delete: $e');
}
```

### Info Message

```dart
// Processing indicator
showComicInfoSnackBar(context, T.processingRequest);
await performLongOperation();
```

## Design Specifications

| Property | Value | Description |
|----------|-------|-------------|
| **Border Width** | 2.0px | Comic standard thickness |
| **Border Radius** | 12px | Rounded corners |
| **Elevation** | 0 | Flat design (no shadow) |
| **Behavior** | Floating | SnackBar floats above content |
| **Margin** | 16px all sides | Space from screen edges |
| **Padding** | Horizontal: 16px, Vertical: 12px | Content spacing |
| **Text Style** | bodyMedium | Theme text style |

## Comparison: Before vs After

### ❌ Before (Non-Comic Style)

```dart
// Old style: Inline styling, no border, inconsistent
ScaffoldMessenger.of(context).showSnackBar(
  SnackBar(
    content: Text(T.nicknameRequired),
    backgroundColor: Theme.of(context).colorScheme.error,
  ),
);
```

### ✅ After (Comic Style)

```dart
// Comic style: Consistent design, proper border, theme-based
showComicErrorSnackBar(context, T.nicknameRequired);
```

## Best Practices

- **Always** use Comic SnackBar functions instead of creating SnackBars manually
- **Choose** the appropriate function based on message type:
  - Success: `showComicSuccessSnackBar`
  - Error/Validation: `showComicErrorSnackBar`
  - Info/Neutral: `showComicInfoSnackBar`
  - Warning/Caution: `showComicWarningSnackBar`
- **Pass** localized text (T.xxx or Lo.xxx) instead of hardcoded strings
- **Check** `mounted` before showing SnackBar in async operations
- **Never** create SnackBars with inline styling or hardcoded colors

## File Location

Comic SnackBar helper functions are defined in:
`./lib/widgets/theme/comic_snackbar.dart`

Import:
```dart
import 'package:philgo/widgets/theme/comic_snackbar.dart';
```


# Scripts

- This skill does not provide scripts.
