---
name: Taro Documentation
description: This skill should be used when the user mentions "Taro" in any technical context, asks about "Taro API", "Taro components", "Taro configuration", "Taro development", "Taro project", "mini program with Taro", "WeChat mini program", uses Taro methods (like "Taro.request", "Taro.navigateTo"), or discusses multi-platform development with Taro framework. Provides comprehensive Taro framework documentation including APIs, components, configuration, and development guides.
version: 0.1.0
---

# Taro Documentation Skill

## Overview

Taro is a comprehensive multi-platform development framework that enables building applications for multiple platforms from a single codebase. Platforms include WeChat Mini Programs, Alipay Mini Programs, Baidu Smart Programs, ByteDance Mini Apps, QQ Mini Programs, H5 (web), React Native, and Harmony OS.

**Key characteristics:**
- React-like syntax and component model
- Write once, run on multiple platforms
- Extensive API coverage for platform-specific features
- Rich component library
- Strong TypeScript support
- Active ecosystem with plugins and UI libraries

## When to Use This Skill

Use this skill when users are:
- Developing Taro applications or mini programs
- Asking questions about Taro APIs, components, or configuration
- Troubleshooting Taro-related issues
- Seeking guidance on Taro best practices
- Converting or migrating projects to Taro
- Integrating Taro with other frameworks or libraries

## Core Concepts

### Framework Architecture

Taro follows a React-like architecture:
- **Component-based**: UI built with reusable components
- **JSX syntax**: Write UI declaratively using JSX/TSX
- **Virtual DOM**: Efficient rendering and updates
- **Lifecycle methods**: Component lifecycle hooks
- **State management**: Local state and global state solutions

### Multi-Platform Compilation

Taro compiles to different platform targets:
- **Compilation time**: Code transforms to platform-specific syntax
- **Runtime adapters**: Platform API differences handled by runtime
- **Conditional compilation**: Platform-specific code when needed
- **Unified APIs**: Single API surface across platforms

### Project Structure

Standard Taro project organization:
```
taro-project/
├── src/
│   ├── app.config.ts      # Global app configuration
│   ├── app.ts             # App entry point
│   ├── pages/             # Page components
│   │   ├── index/
│   │   │   ├── index.tsx
│   │   │   └── index.config.ts
│   ├── components/        # Reusable components
│   └── assets/            # Static resources
├── config/
│   ├── index.js           # Build configuration
│   ├── dev.js             # Development config
│   └── prod.js            # Production config
└── package.json
```

## Using Taro Documentation

### Available Resources

This skill provides access to comprehensive Taro documentation organized into small topic files (all <100 KB). Choose the file prefix that matches the question:

1. **API References** (files prefixed with `apis-`)
   - Network & routing: `apis-network*.md`, `apis-routing.md`
   - Storage & UI feedback: `apis-storage*.md`, `apis-ui-feedback*.md`, `apis-ui-navigation.md`
   - Device, sensors, connectivity: `apis-device-system.md`, `apis-device-sensors.md`, `apis-device-connectivity*.md`
   - Media (image/video/audio): `apis-media-image.md`, `apis-media-video*.md`, `apis-media-audio*.md`
   - Location & canvas: `apis-location*.md`, `apis-canvas*.md`
   - Cloud & payment: `apis-cloud*.md`, `apis-payment.md`
   - Miscellaneous APIs: `apis-other*.md`
   - (Files with `-partN` suffix continue the same topic.)

2. **Component References** (files prefixed with `components-`)
   - Containers and layout: `components-containers*.md`
   - Basic content: `components-basic.md`, `components-other.md`
   - Forms & inputs: `components-form*.md`
   - Navigation: `components-navigation.md`
   - Media & graphics: `components-media*.md`, `components-map-canvas.md`, `components-gesture.md`, `components-skyline.md`
   - Open capabilities: `components-open-capability.md`

3. **Configuration References**
   - `config-app.md` – Global app configuration (app.config.ts)
   - `config-page.md` – Page-level configuration
   - `config-build.md` – Build/compiler settings and optimization

4. **Guide References** (files prefixed with `guides-`)
   - Getting started & fundamentals: `guides-quickstart*.md`, `guides-basics*.md`
   - Architecture & routing: `guides-routing.md`, `guides-testing.md`
   - State & UI libraries: `guides-state.md`, `guides-ui-libraries.md`
   - Platform specifics: `guides-platform-weapp.md`, `guides-platform-h5.md`, `guides-platform-rn.md`, `guides-platform-harmony*.md`
   - Optimization & troubleshooting: `guides-optimization*.md`, `guides-troubleshooting.md`, `guides-community.md`
   - Plugin development & advanced topics: `guides-plugin-dev*.md`


### How to Reference Documentation

When users ask Taro-related questions:

1. **Identify the topic**: Determine which documentation area is relevant (API, component, configuration, or guide)

2. **Load appropriate reference**: Use the Read tool to access the specific topic file:
  ```
  Read references/apis-network.md           # Network/API calls (see apis-network-part*.md for continuation)
  Read references/components-form.md        # Form components and inputs  
  Read references/config-app.md             # Global app configuration
  Read references/guides-platform-weapp.md  # WeChat Mini Program guides
  ```

3. **Search within files**: Use Grep with wildcards to scan the relevant file family:
  ```
  Grep pattern:"Taro\.request" path:"references/apis-network*.md"
  Grep pattern:"Button component" path:"references/components-form*.md"
  ```

4. **Provide contextual answers**: Combine documentation with understanding of user's context to give relevant, actionable guidance

## Common Development Scenarios

### API Usage

When users ask about Taro APIs:
- Reference the relevant `references/apis-*.md` file (for example, `apis-network*.md` for network calls or `apis-device-system.md` for device info)
- Provide code examples showing API usage
- Note platform compatibility if relevant
- Mention common gotchas or best practices

**Example**: For "How do I make a network request?", reference Taro.request API documentation and provide example with error handling.

### Component Usage

When users ask about Taro components:
- Reference the appropriate `references/components-*.md` file (for example, `components-form*.md` or `components-media*.md`)
- Show component props and event handlers
- Provide JSX usage examples
- Note styling approaches and platform differences

**Example**: For "How do I create a scrollable list?", reference ScrollView component documentation and demonstrate with sample code.

### Configuration

When users ask about project setup or configuration:
- Reference `references/config-app.md`, `config-page.md`, or `config-build.md` depending on scope
- Explain configuration options and their effects
- Show configuration file examples
- Address build and compilation settings

**Example**: For "How do I configure page routing?", reference app.config.ts page configuration and demonstrate route setup.

### Development Guides

When users need broader guidance or best practices:
- Reference the matching `references/guides-*.md` file (for example, `guides-platform-weapp.md` or `guides-state.md`)
- Provide step-by-step guidance for complex tasks
- Share best practices and common patterns
- Link related APIs and components

**Example**: For "How do I integrate Redux?", reference state management guide and show integration steps.

## Platform Considerations

### Platform-Specific Features

Taro supports multiple platforms with varying capabilities:
- Some APIs/components are platform-specific
- Check platform support tables in documentation
- Use conditional compilation when needed
- Test on target platforms

### Conditional Compilation

For platform-specific code:
```tsx
// Example of conditional compilation
if (process.env.TARO_ENV === 'weapp') {
  // WeChat Mini Program specific code
}

if (process.env.TARO_ENV === 'h5') {
  // H5 specific code
}
```

### API Compatibility

Check API support across platforms:
- Documentation includes platform support matrices
- Some APIs may have limited support on certain platforms
- Provide fallbacks or alternatives when needed

## Best Practices

### Code Organization

- **Separation of concerns**: Separate UI, logic, and data layers
- **Reusable components**: Create generic components for common UI patterns
- **Type safety**: Use TypeScript for better development experience
- **Configuration externalization**: Keep configuration separate from code

### Performance Optimization

- **List rendering**: Use virtual lists for long lists
- **Image optimization**: Compress images and use lazy loading
- **Code splitting**: Split code by routes or features
- **Avoid unnecessary renders**: Use React.memo, useMemo, useCallback appropriately

### Development Workflow

- **Start with templates**: Use official templates for project scaffolding
- **Follow conventions**: Adhere to Taro naming and structure conventions
- **Test on multiple platforms**: Regularly test on target platforms during development
- **Use developer tools**: Leverage Taro DevTools and platform-specific debugging tools

## Troubleshooting Approach

When users encounter issues:

1. **Identify the problem area**: API, component, configuration, or build issue
2. **Check documentation**: Reference relevant documentation section
3. **Verify platform compatibility**: Ensure feature is supported on target platform
4. **Review configuration**: Check if configuration is correct
5. **Consult guides**: Look for similar issues in troubleshooting guides
6. **Provide solutions**: Offer concrete fixes or workarounds

## Additional Resources

### Reference Files

For detailed documentation, consult these topic-specific files (all <100 KB unless noted):

- **API shards (`references/apis-*.md`)** – 40+ files covering network, routing, storage, device, media, location, canvas, cloud, payment, and miscellaneous APIs. Files with `-partN` suffix continue the same topic sequentially.
- **Component shards (`references/components-*.md`)** – Containers, basic content, form controls, gestures, skyline rendering, navigation, media, map/canvas, and open capability components.
- **Configuration files (`references/config-*.md`)** – `config-app.md`, `config-page.md`, and `config-build.md` for their respective scopes.
- **Guide shards (`references/guides-*.md`)** – Quickstart, fundamentals, routing, testing, state, UI libraries, platform-specific guides, optimization, troubleshooting, plugin development, and community resources.
- **`references/taro-docs.xml`** (3.9 MB, 92,568 lines) – Original Repomix bundle retained as a fallback reference when you need the complete archive.
- **`*.original` backups** – The previous monolithic files renamed with `.original` for historical reference; avoid loading them unless necessary.

### Search Patterns

When searching within reference files, use glob patterns to cover all shards in a family:

**For APIs:**
```
Grep pattern:"Taro\.[APIName]" path:"references/apis-*.md"
```

**For components:**
```
Grep pattern:"<ComponentName" path:"references/components-*.md"
```

**For configuration:**
```
Grep pattern:"config\.(option)" path:"references/config-*.md"
```

**For guides:**
```
Grep pattern:"specific topic" path:"references/guides-*.md"
```

## Working with This Skill

### Approach

1. **Listen for Taro mentions**: Activate when user mentions Taro-related topics
2. **Assess question type**: Determine if question is about API, component, config, or general guidance
3. **Load relevant documentation**: Read appropriate reference file or search within it
4. **Provide contextual answer**: Combine documentation with user's specific context
5. **Include code examples**: Show practical usage when relevant
6. **Note platform considerations**: Mention compatibility if relevant

### Response Format

Structure responses with:
- Direct answer to user's question
- Relevant code examples
- Links to specific documentation sections (file path and topic)
- Platform considerations if applicable
- Related resources or next steps

## Summary

This skill provides comprehensive Taro framework documentation to support development of multi-platform applications. Reference the organized documentation files based on user questions, and combine documentation knowledge with practical guidance to help users build effective Taro applications.

Focus on providing accurate, contextual, and actionable information that helps users solve their specific Taro development challenges.