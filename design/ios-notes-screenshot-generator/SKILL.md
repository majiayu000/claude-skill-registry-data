---
name: ios-notes-screenshot-generator
description: This skill generates realistic iOS notes app screenshots from arbitrary text input. It creates pixel-perfect iPhone notes app interfaces with proper iOS design patterns, typography, spacing, and visual elements. Use this skill when users need to create iOS-style notes app screenshots for presentations, mockups, or design references.
---

# iOS Notes App Screenshot Generator

This skill transforms arbitrary text input into realistic iOS notes app screenshots that match Apple's design language and visual standards.

## When to Use This Skill

Use this skill when:
- User wants to create iOS-style notes app screenshots
- User needs to display text in a realistic iPhone notes interface
- User wants mockups for presentations or design references
- User needs to show how text would look in iOS Notes app

## How This Skill Works

### Core Components
- **iPhone Screen Layout**: Uses proper iPhone 14/15 dimensions (390x844px) with safe areas
- **iOS Design System**: Implements Apple's 8pt grid system, San Francisco font, and system colors
- **Realistic UI Elements**: Status bar, navigation bar, text areas, and interactive elements
- **Typography**: Proper iOS font weights, sizes, and line spacing

### Key Design Patterns Implemented
1. **Navigation Bar**: Large title mode (34pt) with standard iOS styling
2. **Status Bar**: Realistic time, battery, signal indicators
3. **Text Areas**: Proper margins (16pt), line height (1.4-1.5), and San Francisco font
4. **Color Semes**: System colors with light/dark mode support
5. **Spacing**: 8pt grid system throughout

### Asset Usage
- Use `assets/ios-notes-template.html` as the base template
- Reference `references/ios-design-patterns.md` for detailed specifications
- Customize `scripts/screenshot-generator.js` for dynamic content insertion

## Usage Instructions

1. **Input Processing**: Extract the user's text content and identify key requirements
2. **Template Selection**: Choose appropriate notes app layout (list view vs detail view)
3. **Content Insertion**: Insert text into proper iOS-styled containers
4. **Styling Application**: Apply iOS design patterns, typography, and spacing
5. **Screenshot Generation**: Create final HTML/CSS output that renders as iOS screenshot

### Implementation Steps

1. **Create Base Template**: Start with `assets/ios-notes-template.html`
2. **Apply iOS Design System**: Use `references/ios-design-patterns.md` specifications
3. **Insert User Content**: Place text in appropriate iOS-styled containers
4. **Generate Screenshot**: Output HTML/CSS that creates realistic iOS notes interface
5. **Validate Fidelity**: Ensure visual accuracy matches iOS Notes app

## Output Specifications

The skill generates HTML/CSS that:
- Creates pixel-perfect iOS notes app interface
- Uses proper iPhone screen dimensions and safe areas
- Implements iOS design patterns and typography
- Displays user text in realistic iOS notes environment
- Includes status bar, navigation, and text editing UI elements

## Technical Requirements

- **Screen Size**: 390x844px (iPhone 14/15 standard)
- **Typography**: San Francisco font family with iOS font weights
- **Colors**: iOS system colors with proper contrast ratios
- **Spacing**: 8pt grid system alignment
- **Visual Elements**: Realistic shadows, blur effects, and transitions