---
name: intellij-plugin-builder
description: Guide for creating IntelliJ Platform plugins using Gradle and Kotlin/Java. Use when users want to create, configure, or develop plugins for IntelliJ IDEA or other JetBrains IDEs.
---

# IntelliJ Plugin Builder

## Overview

This skill provides templates, best practices, and reference documentation for building IntelliJ Platform plugins. It covers project setup, core components (Actions, Services, Listeners), and configuration using the IntelliJ Platform Gradle Plugin (2.x).

It includes the **full official IntelliJ SDK documentation** for offline reference.

## Workflow

### 1. Project Setup
Use the provided initialization script to scaffold a new project with the correct structure and configuration.

```bash
python3 .claude/skills/intellij-plugin-builder/scripts/init_project.py "MyPlugin" "com.example.myplugin"
```

This will create:
- A standard Gradle project structure (`src/main/kotlin`, `src/main/resources`).
- `build.gradle.kts` configured with the IntelliJ Platform Gradle Plugin (2.x).
- `plugin.xml` with your ID and name.
- `gradle.properties` and `.gitignore`.

### 2. Core Development
Refer to `references/plugin_structure.md` for details on:
- **Actions**: Creating menu items and toolbar buttons.
- **Services**: Managing state and logic.
- **Listeners**: Reacting to IDE events.
- **Extensions**: Integrating with the IDE (Tool Windows, Inspections, etc.).

### 3. Common Tasks & Tutorials
The skill includes the full IntelliJ SDK documentation. Here are quick links to common tasks:

- **Creating Actions**: `references/intellij-sdk-docs/topics/tutorials/actions_tutorial.md`
- **Tool Windows**: `references/intellij-sdk-docs/topics/basics/plugin_structure/plugin_tool_windows.md`
- **Inspections**: `references/intellij-sdk-docs/topics/tutorials/code_inspections.md`
- **Listeners**: `references/intellij-sdk-docs/topics/basics/plugin_structure/plugin_listeners.md`
- **Services**: `references/intellij-sdk-docs/topics/basics/plugin_structure/plugin_services.md`
- **Settings/Config**: `references/intellij-sdk-docs/topics/tutorials/settings_tutorial.md`

### 4. Building and Running
- Run `./gradlew runIde` to start a sandbox IDE instance with your plugin installed.
- Run `./gradlew buildPlugin` to package the plugin for distribution.
- Run `./gradlew test` to run unit tests (JUnit 5 configured).

## Resources

### scripts/
- `init_project.py`: Scaffolds a complete IntelliJ Plugin project structure.
- `add_action.py`: Interactive script to scaffold a new Action class (Kotlin) and generate the XML registration snippet.

### references/
- `plugin_structure.md`: Detailed guide on project structure, key components (Actions, Services, Listeners), and Gradle configuration.
- `intellij-sdk-docs/`: Full clone of the official IntelliJ SDK documentation.
  - `topics/basics/`: Core concepts and architecture.
  - `topics/reference_guide/`: API reference and specific features.
  - `topics/tutorials/`: Step-by-step guides.


### assets/
- `build.gradle.kts`: A complete Gradle build script template configured for IntelliJ Plugin development (v2.x) with JUnit 5.
- `plugin.xml`: A template for the plugin configuration file.
- `settings.gradle.kts`: Gradle settings template.
- `gradle.properties`: Standard properties for JVM and plugin versions.
- `.gitignore`: Standard git ignore file for IntelliJ/Gradle projects.

