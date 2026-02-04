---
name: idea-plugin-dev
description: Develop IntelliJ IDEA plugins with two templates, standard plugins and AI-integrated plugins. Use when creating new IntelliJ IDEA plugins, setting up plugin projects, implementing actions, settings pages, or integrating with IntelliAI Engine. Supports both simple plugins without AI dependencies and advanced plugins with AI provider selection and prompt template management.
---

# IntelliJ IDEA Plugin Development

This Skill provides guidance for developing IntelliJ IDEA plugins using standardized templates. It covers two types of plugins: standard
plugins (without AI) and AI-integrated plugins (with IntelliAI Engine).

## When to Use This Skill

Use this Skill when:

- Creating a new IntelliJ IDEA plugin project
- Setting up plugin structure and configuration
- Implementing actions, settings pages, or UI components
- Integrating AI capabilities via IntelliAI Engine
- Following best practices for IntelliJ plugin development
- Working with plugin templates (`template-without-ai` or `template-with-ai`)

## Plugin Types

### 1. Standard Plugin (template-without-ai)

**Use for**: Plugins that don't require AI functionality.

**Features**:

- Simplified Action (right-click menu)
- Icon management class
- Notification utilities
- Internationalization support
- Basic project structure

**Key Components**:

- `ExampleAction` - Single action example
- `ExampleIcons` - Icon management
- `NotificationUtil` - Notification helper
- `ExampleBundle` - Internationalization

### 2. AI-Integrated Plugin (template-with-ai)

**Use for**: Plugins that need AI capabilities via IntelliAI Engine.

**Additional Features**:

- AI provider selection in settings
- Prompt template management
- Settings page with advanced options
- Integration with IntelliAI Engine

**Key Components**:

- All standard plugin components
- `SettingsState` - Persistent configuration
- `ExampleSettingsConfigurable` - Settings UI
- `ExampleSettingsPanel` - Settings panel with AI provider dropdown and prompt templates

## Project Structure

### Standard Plugin Structure

```
template-without-ai/
├── src/main/java/dev/dong4j/zeka/stack/idea/plugin/example/
│   ├── action/          # Actions
│   ├── icons/           # Icon management
│   └── util/            # Utilities (Bundle, Notification)
├── src/main/resources/
│   ├── icons/           # Icon resources (SVG)
│   ├── META-INF/
│   │   └── plugin.xml   # Plugin configuration
│   └── messages*.properties  # Internationalization
├── includes/            # Plugin description and changelog
├── docs/                # User manual
├── build.gradle.kts     # Build configuration
└── gradle.properties    # Plugin properties
```

### AI-Integrated Plugin Structure

```
template-with-ai/
├── src/main/java/dev/dong4j/zeka/stack/idea/plugin/example/
│   ├── action/          # Actions
│   ├── icons/           # Icon management
│   ├── settings/        # Settings (State, Configurable, Panel)
│   └── util/            # Utilities
├── ... (same as standard)
└── build.gradle.kts     # Includes AI Engine dependencies
```

## Development Steps

### Step 1: Choose Template Type

**For standard plugins**:

- Use `template-without-ai` as base
- No AI Engine dependencies needed
- Simpler configuration

**For AI-integrated plugins**:

- Use `template-with-ai` as base
- Requires IntelliAI Engine plugin
- Includes settings page and AI provider management

### Step 2: Configure Project

1. **Update `gradle.properties`**:
   ```properties
   pluginGroup=dev.dong4j.zeka.stack.idea.plugin.example
   pluginName=Your Plugin Name
   pluginVersion=1.0.0
   rootProjectName=your-plugin-name
   ```

2. **Update `plugin.xml`**:
    - Change plugin ID
    - Update plugin name
    - Register your actions and services

3. **Update package names**:
    - Replace `dev.dong4j.zeka.stack.idea.plugin.example` with your package
    - Update all Java files
    - Update `plugin.xml` references

### Step 3: Implement Actions

**Standard Action Pattern**:

```java
public class ExampleAction extends AnAction {
    public ExampleAction() {
        super(
            ExampleBundle.message("action.example.title"),
            ExampleBundle.message("action.example.description"),
            ExampleIcons.EXAMPLE_16
        );
    }

    @Override
    public void actionPerformed(@NotNull AnActionEvent e) {
        Project project = e.getProject();
        PsiFile psiFile = e.getData(CommonDataKeys.PSI_FILE);
        
        if (project == null || psiFile == null) {
            NotificationUtil.showError(project, ExampleBundle.message("error.no.file"));
            return;
        }
        
        // Your action logic here
        NotificationUtil.showInfo(project, "Action executed");
    }
}
```

**Register in `plugin.xml`**:

```xml
<action id="your.package.action.ExampleAction"
        class="your.package.action.ExampleAction">
    <add-to-group group-id="EditorPopupMenu" anchor="last"/>
</action>
```

### Step 4: Icon Management

**Create Icon Class**:

```java
public class ExampleIcons {
    @NotNull
    private static Icon load(@NotNull String iconPath) {
        return IconLoader.getIcon(iconPath, ExampleIcons.class);
    }

    public static final Icon EXAMPLE_16 = load("/icons/example_16.svg");
}
```

**Add Icon Resources**:

- Place SVG files in `src/main/resources/icons/`
- Use 16x16 for actions, 24x24 for notifications, 32x32 for dialogs

### Step 5: Internationalization

**Add Messages**:

`messages.properties` (English):

```properties
action.example.title=Example Action
action.example.description=Execute example action
error.no.file=No file found
```

`messages_zh_CN.properties` (Chinese):

```properties
action.example.title=示例操作
action.example.description=执行示例操作
error.no.file=未找到文件
```

**Use in Code**:

```java
String message = ExampleBundle.message("action.example.title");
```

### Step 6: Settings Page (AI-Integrated Only)

**Create SettingsState**:

```java
@State(
    name = "ExamplePluginSettings",
    storages = @Storage("example-settings.xml")
)
public class SettingsState implements PersistentStateComponent<SettingsState> {
    public AIProviderConfig providerConfig;
    public boolean showAdvancedSettings = false;
    public String systemPrompt = getDefaultSystemPrompt();
    public String exampleTemplate = getDefaultExampleTemplate();
    
    public static SettingsState getInstance() {
        return ApplicationManager.getApplication().getService(SettingsState.class);
    }
}
```

**Create Settings Panel**:

```java
public class ExampleSettingsPanel {
    private JComboBox<AIProviderConfig> providerComboBox;
    private JBTextArea systemPromptTextArea;
    
    // Create AI provider selection panel
    private JPanel createAIProviderSelectionPanel() {
        List<AIProviderConfig> providers = getAiProviderTypes();
        // Build UI with FormBuilder
    }
}
```

**Register in `plugin.xml`**:

```xml
<applicationService serviceImplementation="your.package.settings.SettingsState"/>
<applicationConfigurable
    parentId="tools"
    instance="your.package.settings.ExampleSettingsConfigurable"
    id="your.package.settings.ExampleSettingsConfigurable"
    displayName="Your Plugin"/>
```

### Step 7: Build Configuration

**Standard Plugin (`build.gradle.kts`)**:

```kotlin
dependencies {
    intellijPlatform {
        create(providers.gradleProperty("platformType"), 
               providers.gradleProperty("platformVersion"))
        bundledPlugin("com.intellij.java")
        // No AI Engine dependency
    }
}
```

**AI-Integrated Plugin (`build.gradle.kts`)**:

```kotlin
dependencies {
    intellijPlatform {
        // ... same as standard
        // plugin("dev.dong4j.zeka.stack.idea.plugin.common.ai")  // Uncomment for marketplace
    }
    compileOnly("dev.dong4j:intelli-ai-engine:1.1.0")
}

tasks {
    // Add buildAiCommonPlugin and copyAiCommonPlugin tasks
    // for local development
}
```

### Step 8: Testing

1. **Build plugin**:
   ```bash
   ./gradlew buildPlugin
   ```

2. **Run in sandbox**:
   ```bash
   ./gradlew runIde
   ```

3. **Verify**:
    - Action appears in right-click menu
    - Settings page loads (AI-integrated)
    - Notifications work
    - Internationalization works

## Best Practices

### Code Organization

1. **Package Structure**:
    - `action/` - User actions
    - `icons/` - Icon management
    - `settings/` - Settings (AI-integrated only)
    - `util/` - Utilities (Bundle, Notification)

2. **Naming Conventions**:
    - Actions: `*Action.java`
    - Settings: `*SettingsState.java`, `*SettingsConfigurable.java`, `*SettingsPanel.java`
    - Icons: `*Icons.java`
    - Bundles: `*Bundle.java`

### UI Components

1. **Use IntelliJ UI Components**:
    - `JBLabel`, `JBTextField`, `JBCheckBox` (not JLabel, JTextField)
    - `FormBuilder` for layouts
    - `ToolbarDecorator` for tables
    - `JBTable` for data tables

2. **Settings Page**:
    - Use `FormBuilder` for consistent layout
    - Add emojis to labels for better UX (🤖, ⚙️, 📝, etc.)
    - Support collapsible advanced settings
    - Use `JBTabbedPane` for multiple prompt templates

### Internationalization

1. **Always use Bundle**:
    - Never hardcode strings
    - Use `ExampleBundle.message(key, params...)`
    - Provide both English and Chinese

2. **Key Naming**:
    - `action.*` - Action labels
    - `settings.*` - Settings labels
    - `error.*` - Error messages
    - `success.*` - Success messages

### Configuration

1. **Persistent State**:
    - Use `@State` annotation
    - Implement `PersistentStateComponent`
    - Initialize collections to avoid null

2. **Settings UI**:
    - Implement `Configurable` or `SearchableConfigurable`
    - Check `isModified()` before save
    - Reset UI in `reset()` method

## Common Patterns

### Notification Pattern

```java
// Success
NotificationUtil.showInfo(project, ExampleBundle.message("success.action.executed"));

// Error
NotificationUtil.showError(project, ExampleBundle.message("error.no.file"));

// Warning
NotificationUtil.showWarning(project, ExampleBundle.message("warning.message"));
```

### Action Update Pattern

```java
@Override
public void update(@NotNull AnActionEvent e) {
    Project project = e.getProject();
    PsiFile file = e.getData(CommonDataKeys.PSI_FILE);
    e.getPresentation().setEnabled(project != null && file != null);
}
```

### Settings Validation Pattern

```java
@Override
public void apply() throws ConfigurationException {
    if (!validateSettings()) {
        throw new ConfigurationException("Invalid settings");
    }
    settingsPanel.apply(settings);
}
```

## Differences: Standard vs AI-Integrated

| Feature               | Standard Plugin | AI-Integrated Plugin                      |
|-----------------------|-----------------|-------------------------------------------|
| AI Engine Dependency  | ❌ No            | ✅ Yes (compileOnly)                       |
| Settings Page         | ❌ No            | ✅ Yes                                     |
| AI Provider Selection | ❌ No            | ✅ Yes                                     |
| Prompt Templates      | ❌ No            | ✅ Yes                                     |
| Build Tasks           | Basic           | + buildAiCommonPlugin, copyAiCommonPlugin |
| plugin.xml            | Actions only    | + SettingsState, SettingsConfigurable     |

## Troubleshooting

### Plugin doesn't load

- Check `plugin.xml` syntax
- Verify package names match
- Check for missing dependencies

### Settings not persisting

- Verify `@State` annotation
- Check `getState()` and `loadState()` methods
- Ensure fields are `public`

### AI provider not available

- Check IntelliAI Engine plugin is installed
- Verify provider is configured and tested
- Check `AIProviderSettings.getInstance().getVerifiedProviders()`

### Icons not showing

- Verify icon path starts with `/icons/`
- Check SVG file exists in resources
- Ensure `IconLoader.getIcon()` path is correct

## References

- Template projects: `template-without-ai/` and `template-with-ai/`
- IntelliJ Platform SDK: https://plugins.jetbrains.com/docs/intellij/
- IntelliAI Engine: See `intelli-ai-engine/` project
- Example implementations: `intelli-ai-changelog/`, `intelli-ai-javadoc/`

## Examples

### Creating a Standard Plugin

1. Copy `template-without-ai` to your project
2. Update `gradle.properties` with your plugin info
3. Rename package from `example` to your package
4. Implement your action in `action/` package
5. Add icons and internationalization
6. Build and test

### Creating an AI-Integrated Plugin

1. Copy `template-with-ai` to your project
2. Follow standard plugin steps
3. Configure AI provider in settings
4. Implement prompt templates
5. Use `AIService.getInstance()` to call AI
6. Build and test (ensure IntelliAI Engine is available)
