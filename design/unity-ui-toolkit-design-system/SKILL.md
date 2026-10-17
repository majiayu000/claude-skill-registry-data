---
name: unity-ui-toolkit-design-system
description: Drop-in design system for Unity 6 UI Toolkit with tokens, components, icons, mobile responsiveness, and runtime helpers
triggers:
  - "use Unity UI Toolkit design system"
  - "add design system to Unity UI"
  - "create styled UI components in Unity"
  - "implement mobile responsive Unity UI"
  - "use Unity UIDocument design tokens"
  - "add themed buttons and inputs to Unity"
  - "create Unity UI with component library"
  - "style Unity UI Toolkit interface"
---

# Unity UI Toolkit Design System

> Skill by [ara.so](https://ara.so) — Design Skills collection.

A drop-in design system for Unity 6 UI Toolkit (UIDocument + UXML + USS) providing tokens, 24+ components, 63 icons, mobile responsiveness, and runtime helpers. Battle-tested in production cross-platform games.

## What It Provides

- **Token-based theming**: Dark theme by default with `var(--color-*)` cascade, light theme override available
- **24 ready components**: Buttons, inputs, tabs, toggles, modals, toasts, badges, navigation, progress indicators, etc.
- **63 SVG icons**: Auto-tinting via `-unity-background-image-tint-color` for state changes
- **Mobile responsiveness**: Single `.mobile` class flips all spacing and touch targets
- **Runtime helper**: Auto-attaches to UIDocuments, handles toggle knobs, spinner rotation, skeleton shimmer
- **Themed scrollbars**: 8px slim scrollbar that auto-themes with palette

## Installation

### Requirements

- Unity 6 (6000.x or newer)
- `com.unity.ui` (UI Toolkit) — built-in module
- `com.unity.modules.vectorgraphics` — built-in module

### Option A: Direct Copy

```powershell
# From your Unity project root
git clone https://github.com/sinanata/unity-ui-document-design-system ../design-system-src
cp -r ../design-system-src/Assets/DesignSystem Assets/DesignSystem
```

### Option B: Git Submodule (Recommended)

```bash
cd your-unity-project
git submodule add https://github.com/sinanata/unity-ui-document-design-system Vendor/unity-ui-document-design-system
```

Create OS-level link:

```powershell
# Windows (no admin required)
cmd /c mklink /J Assets\DesignSystem Vendor\unity-ui-document-design-system\Assets\DesignSystem
```

```bash
# macOS/Linux
ln -s ../Vendor/unity-ui-document-design-system/Assets/DesignSystem Assets/DesignSystem
```

Add to `.gitignore`:

```gitignore
# Per-clone link to vendored design system
Assets/DesignSystem
Assets/DesignSystem.meta
```

## Basic Usage

### Attach Stylesheet to UXML

```xml
<ui:UXML xmlns:ui="UnityEngine.UIElements">
  <Style src="project://database/Assets/DesignSystem/Resources/UI/Styles/DesignSystem/DesignSystem.uss" />
  
  <ui:VisualElement class="ds-root">
    <!-- Your UI here -->
  </ui:VisualElement>
</ui:UXML>
```

The `ds-root` class is required as the container for all design system components.

### Runtime Auto-Attachment

The `DesignSystemRuntime.cs` automatically attaches to every UIDocument in the scene. No manual setup needed.

## Component Patterns

### Buttons

Five variants with automatic hover/press/disabled states:

```xml
<!-- Primary CTA -->
<ui:Button text="Get Started" class="ds-btn ds-btn--primary" />

<!-- Secondary outline -->
<ui:Button text="Cancel" class="ds-btn ds-btn--secondary" />

<!-- Tertiary text-only -->
<ui:Button text="Learn More" class="ds-btn ds-btn--tertiary" />

<!-- Warning -->
<ui:Button text="Delete" class="ds-btn ds-btn--warning" />

<!-- Danger -->
<ui:Button text="Remove" class="ds-btn ds-btn--danger" />

<!-- Full width -->
<ui:Button text="Continue" class="ds-btn ds-btn--primary ds-btn--block" />

<!-- Small size -->
<ui:Button text="Small" class="ds-btn ds-btn--primary ds-btn--sm" />

<!-- Large size -->
<ui:Button text="Large" class="ds-btn ds-btn--primary ds-btn--lg" />

<!-- With icon -->
<ui:Button class="ds-btn ds-btn--primary">
  <ui:VisualElement class="ds-icon ds-icon--sm ds-icon--plus" />
  <ui:Label text="Add Item" />
</ui:Button>
```

Disable programmatically:

```csharp
button.SetEnabled(false); // USS handles :disabled state styling
```

### Inputs

Text fields with search, textarea variants:

```xml
<!-- Basic input -->
<ui:TextField class="ds-input" />

<!-- Search with icon -->
<ui:VisualElement class="ds-search">
  <ui:VisualElement class="ds-icon ds-icon--sm ds-icon--search ds-search__icon" />
  <ui:TextField class="ds-search__field" />
</ui:VisualElement>

<!-- Textarea -->
<ui:TextField multiline="true" class="ds-input ds-input--textarea" />

<!-- Password -->
<ui:TextField password="true" class="ds-input" />
```

Set placeholders from C#:

```csharp
var searchField = root.Q<TextField>(className: "ds-search__field");
searchField.textEdition.placeholder = "Search animals...";

var emailField = root.Q<TextField>("email-field");
emailField.textEdition.placeholder = "name@example.com";
```

### Tabs

Segmented control with active state:

```xml
<ui:VisualElement class="ds-tabs">
  <ui:Button text="All" class="ds-tab is-active" name="tab-all" />
  <ui:Button text="Active" class="ds-tab" name="tab-active" />
  <ui:Button text="Archived" class="ds-tab" name="tab-archived" />
</ui:VisualElement>
```

Handle tab switching:

```csharp
var tabs = root.Query<Button>(className: "ds-tab").ToList();
foreach (var tab in tabs)
{
    tab.clicked += () => {
        // Remove active from all
        tabs.ForEach(t => t.RemoveFromClassList("is-active"));
        // Add to clicked
        tab.AddToClassList("is-active");
        
        // Handle content switching
        string tabName = tab.name;
        ShowContentFor(tabName);
    };
}
```

### Icons

63 built-in SVG icons with auto-tinting:

```xml
<!-- Basic icon -->
<ui:VisualElement class="ds-icon ds-icon--paw" />

<!-- Small size -->
<ui:VisualElement class="ds-icon ds-icon--sm ds-icon--user" />

<!-- Large size -->
<ui:VisualElement class="ds-icon ds-icon--lg ds-icon--store" />

<!-- Common icons -->
<ui:VisualElement class="ds-icon ds-icon--heart" />
<ui:VisualElement class="ds-icon ds-icon--cart" />
<ui:VisualElement class="ds-icon ds-icon--settings" />
<ui:VisualElement class="ds-icon ds-icon--chevron-right" />
<ui:VisualElement class="ds-icon ds-icon--arrow-left" />
<ui:VisualElement class="ds-icon ds-icon--check" />
<ui:VisualElement class="ds-icon ds-icon--close" />
<ui:VisualElement class="ds-icon ds-icon--plus" />
<ui:VisualElement class="ds-icon ds-icon--minus" />
```

Icons automatically tint based on parent state (hover, active, disabled) via `-unity-background-image-tint-color`.

### Toggles & Checkboxes

iOS-style toggle and square checkbox:

```xml
<!-- Toggle switch (runtime adds sliding knob) -->
<ui:Toggle class="ds-toggle" />

<!-- Checkbox -->
<ui:Toggle class="ds-check" />

<!-- With label -->
<ui:VisualElement class="ds-row">
  <ui:Toggle class="ds-check" name="remember-me" />
  <ui:Label text="Remember me" class="ds-body-1" />
</ui:VisualElement>
```

Handle changes:

```csharp
var toggle = root.Q<Toggle>("remember-me");
toggle.RegisterValueChangedCallback(evt => {
    bool isChecked = evt.newValue;
    PlayerPrefs.SetInt("RememberMe", isChecked ? 1 : 0);
});
```

### Modals & Dialogs

Overlay components with header/body/actions slots:

```xml
<!-- Modal -->
<ui:VisualElement class="ds-modal" name="settings-modal">
  <ui:VisualElement class="ds-modal__content">
    <ui:VisualElement class="ds-modal__header">
      <ui:Label text="Settings" class="ds-h3" />
      <ui:Button class="ds-btn ds-btn--tertiary ds-btn--sm" name="close-modal">
        <ui:VisualElement class="ds-icon ds-icon--sm ds-icon--close" />
      </ui:Button>
    </ui:VisualElement>
    
    <ui:VisualElement class="ds-modal__body">
      <!-- Modal content -->
    </ui:VisualElement>
    
    <ui:VisualElement class="ds-modal__actions">
      <ui:Button text="Cancel" class="ds-btn ds-btn--secondary" />
      <ui:Button text="Save" class="ds-btn ds-btn--primary" />
    </ui:VisualElement>
  </ui:VisualElement>
</ui:VisualElement>

<!-- Confirm dialog -->
<ui:VisualElement class="ds-dialog" name="confirm-delete">
  <ui:VisualElement class="ds-dialog__content">
    <ui:Label text="Delete item?" class="ds-h4" />
    <ui:Label text="This action cannot be undone." class="ds-body-2" />
    <ui:VisualElement class="ds-dialog__actions">
      <ui:Button text="Cancel" class="ds-btn ds-btn--secondary" />
      <ui:Button text="Delete" class="ds-btn ds-btn--danger" />
    </ui:VisualElement>
  </ui:VisualElement>
</ui:VisualElement>
```

Show/hide with display toggle:

```csharp
var modal = root.Q("settings-modal");
modal.style.display = DisplayStyle.Flex; // Show
modal.style.display = DisplayStyle.None; // Hide

// Close button handler
var closeBtn = root.Q<Button>("close-modal");
closeBtn.clicked += () => modal.style.display = DisplayStyle.None;
```

### Toasts

Non-blocking notifications:

```xml
<ui:VisualElement class="ds-toast ds-toast--success">
  <ui:VisualElement class="ds-icon ds-icon--sm ds-icon--check" />
  <ui:Label text="Changes saved" class="ds-body-2" />
</ui:VisualElement>

<ui:VisualElement class="ds-toast ds-toast--error">
  <ui:VisualElement class="ds-icon ds-icon--sm ds-icon--close" />
  <ui:Label text="Connection failed" class="ds-body-2" />
</ui:VisualElement>

<ui:VisualElement class="ds-toast ds-toast--warning">
  <ui:VisualElement class="ds-icon ds-icon--sm ds-icon--alert" />
  <ui:Label text="Low storage" class="ds-body-2" />
</ui:VisualElement>
```

Create and auto-dismiss:

```csharp
public void ShowToast(VisualElement root, string message, string type = "success")
{
    var toast = new VisualElement();
    toast.AddToClassList("ds-toast");
    toast.AddToClassList($"ds-toast--{type}");
    
    var icon = new VisualElement();
    icon.AddToClassList("ds-icon");
    icon.AddToClassList("ds-icon--sm");
    icon.AddToClassList($"ds-icon--{(type == "success" ? "check" : "close")}");
    
    var label = new Label(message);
    label.AddToClassList("ds-body-2");
    
    toast.Add(icon);
    toast.Add(label);
    root.Add(toast);
    
    // Auto-dismiss after 3 seconds
    root.schedule.Execute(() => {
        root.Remove(toast);
    }).ExecuteLater(3000);
}

// Usage
ShowToast(root, "Item added to cart", "success");
```

### Progress & Loading

Progress bars, spinners, skeleton loaders:

```xml
<!-- Progress bar -->
<ui:VisualElement class="ds-progress">
  <ui:VisualElement class="ds-progress__bar" style="width: 60%;" />
</ui:VisualElement>

<!-- Spinner (runtime handles rotation) -->
<ui:VisualElement class="ds-spinner" />

<!-- Skeleton loader (runtime handles shimmer) -->
<ui:VisualElement class="ds-skeleton ds-skeleton--text" />
<ui:VisualElement class="ds-skeleton ds-skeleton--avatar" />
<ui:VisualElement class="ds-skeleton ds-skeleton--card" />
```

Update progress dynamically:

```csharp
var progressBar = root.Q(className: "ds-progress__bar");
float progress = 0.75f; // 75%
progressBar.style.width = Length.Percent(progress * 100);
```

### Badges & Labels

Status indicators and counters:

```xml
<!-- Badges -->
<ui:Label text="New" class="ds-badge ds-badge--primary" />
<ui:Label text="Sale" class="ds-badge ds-badge--warning" />
<ui:Label text="Sold Out" class="ds-badge ds-badge--danger" />

<!-- Notification dot -->
<ui:VisualElement style="position: relative;">
  <ui:VisualElement class="ds-icon ds-icon--bell" />
  <ui:VisualElement class="ds-notification-dot" />
</ui:VisualElement>

<!-- Notification badge with count -->
<ui:VisualElement style="position: relative;">
  <ui:VisualElement class="ds-icon ds-icon--cart" />
  <ui:Label text="3" class="ds-notification-badge" />
</ui:VisualElement>
```

### Sliders

Single and range sliders:

```xml
<!-- Single slider -->
<ui:Slider low-value="0" high-value="100" class="ds-slider" name="volume-slider" />

<!-- Range slider -->
<ui:VisualElement class="ds-range">
  <ui:Slider low-value="0" high-value="100" value="20" class="ds-range__slider" name="range-min" />
  <ui:Slider low-value="0" high-value="100" value="80" class="ds-range__slider" name="range-max" />
</ui:VisualElement>
```

Handle value changes:

```csharp
var volumeSlider = root.Q<Slider>("volume-slider");
volumeSlider.RegisterValueChangedCallback(evt => {
    float volume = evt.newValue / 100f;
    AudioListener.volume = volume;
});

var minSlider = root.Q<Slider>("range-min");
var maxSlider = root.Q<Slider>("range-max");
minSlider.RegisterValueChangedCallback(evt => {
    if (evt.newValue > maxSlider.value) {
        minSlider.value = maxSlider.value;
    }
});
```

## Mobile Responsiveness

Add `.mobile` class to switch to touch-friendly sizes:

```csharp
using UnityEngine;
using UnityEngine.UIElements;

public class MobileUIController : MonoBehaviour
{
    private UIDocument uiDocument;
    private VisualElement root;
    
    void Start()
    {
        uiDocument = GetComponent<UIDocument>();
        root = uiDocument.rootVisualElement;
        
        UpdateMobileClass();
    }
    
    void UpdateMobileClass()
    {
        // Simple width-based detection
        if (Screen.width < 768)
        {
            root.AddToClassList("mobile");
        }
        else
        {
            root.RemoveFromClassList("mobile");
        }
    }
    
    void Update()
    {
        // Handle orientation changes
        if (Screen.width != previousWidth)
        {
            UpdateMobileClass();
            previousWidth = Screen.width;
        }
    }
    
    private int previousWidth;
}
```

Platform-specific detection:

```csharp
void Start()
{
    root = GetComponent<UIDocument>().rootVisualElement;
    
#if UNITY_ANDROID || UNITY_IOS
    root.AddToClassList("mobile");
#else
    if (Screen.width < 768)
    {
        root.AddToClassList("mobile");
    }
#endif
}
```

Mobile class changes:
- Buttons: 36px → 48px height
- Inputs: 40px → 48px height, 13px → 15px font
- Tabs: 40px → 48px height
- Slider thumbs: 18px → 24px
- Touch targets minimum 48×48px

## Theming

### Light Theme

Add `.theme-light` to root for light palette:

```xml
<ui:VisualElement class="ds-root theme-light">
  <!-- Components auto-theme via var(--color-*) cascade -->
</ui:VisualElement>
```

Or toggle programmatically:

```csharp
var root = uiDocument.rootVisualElement;
bool isLightTheme = PlayerPrefs.GetInt("LightTheme", 0) == 1;

if (isLightTheme)
{
    root.AddToClassList("theme-light");
}

// Theme toggle button
var themeToggle = root.Q<Button>("theme-toggle");
themeToggle.clicked += () => {
    root.ToggleInClassList("theme-light");
    isLightTheme = root.ClassListContains("theme-light");
    PlayerPrefs.SetInt("LightTheme", isLightTheme ? 1 : 0);
};
```

### Custom Color Tokens

Override tokens in your own USS:

```css
.ds-root {
    --color-primary: #FF6B6B;
    --color-primary-hover: #FF5252;
    --color-background: #1A1A2E;
    --color-surface: #16213E;
}
```

## Complete Example: Login Screen

```xml
<ui:UXML xmlns:ui="UnityEngine.UIElements">
  <Style src="project://database/Assets/DesignSystem/Resources/UI/Styles/DesignSystem/DesignSystem.uss" />
  
  <ui:VisualElement class="ds-root" style="padding: 24px; min-height: 100%; justify-content: center;">
    <ui:VisualElement style="max-width: 400px; width: 100%; align-self: center;">
      
      <!-- Header -->
      <ui:VisualElement style="align-items: center; margin-bottom: 32px;">
        <ui:VisualElement class="ds-icon ds-icon--lg ds-icon--user" style="margin-bottom: 16px;" />
        <ui:Label text="Sign In" class="ds-h2" />
        <ui:Label text="Welcome back!" class="ds-body-2" style="color: var(--color-text-secondary);" />
      </ui:VisualElement>
      
      <!-- Email input -->
      <ui:VisualElement style="margin-bottom: 16px;">
        <ui:Label text="Email" class="ds-label" style="margin-bottom: 8px;" />
        <ui:VisualElement class="ds-search">
          <ui:VisualElement class="ds-icon ds-icon--sm ds-icon--email ds-search__icon" />
          <ui:TextField class="ds-search__field" name="email-field" />
        </ui:VisualElement>
      </ui:VisualElement>
      
      <!-- Password input -->
      <ui:VisualElement style="margin-bottom: 16px;">
        <ui:Label text="Password" class="ds-label" style="margin-bottom: 8px;" />
        <ui:TextField password="true" class="ds-input" name="password-field" />
      </ui:VisualElement>
      
      <!-- Remember me -->
      <ui:VisualElement class="ds-row" style="justify-content: space-between; margin-bottom: 24px;">
        <ui:VisualElement class="ds-row">
          <ui:Toggle class="ds-check" name="remember-toggle" />
          <ui:Label text="Remember me" class="ds-body-2" />
        </ui:VisualElement>
        <ui:Button text="Forgot password?" class="ds-btn ds-btn--tertiary ds-btn--sm" name="forgot-btn" />
      </ui:VisualElement>
      
      <!-- Sign in button -->
      <ui:Button text="Sign In" class="ds-btn ds-btn--primary ds-btn--block" name="signin-btn" />
      
      <!-- Divider -->
      <ui:VisualElement style="height: 1px; background-color: var(--color-border); margin: 24px 0;" />
      
      <!-- Sign up link -->
      <ui:VisualElement class="ds-row" style="justify-content: center;">
        <ui:Label text="Don't have an account?" class="ds-body-2" style="margin-right: 4px;" />
        <ui:Button text="Sign up" class="ds-btn ds-btn--tertiary ds-btn--sm" name="signup-btn" />
      </ui:VisualElement>
      
    </ui:VisualElement>
  </ui:VisualElement>
</ui:UXML>
```

Controller script:

```csharp
using UnityEngine;
using UnityEngine.UIElements;

public class LoginController : MonoBehaviour
{
    private UIDocument uiDocument;
    private VisualElement root;
    private TextField emailField;
    private TextField passwordField;
    private Toggle rememberToggle;
    private Button signinBtn;
    
    void Start()
    {
        uiDocument = GetComponent<UIDocument>();
        root = uiDocument.rootVisualElement;
        
        // Get references
        emailField = root.Q<TextField>("email-field");
        passwordField = root.Q<TextField>("password-field");
        rememberToggle = root.Q<Toggle>("remember-toggle");
        signinBtn = root.Q<Button>("signin-btn");
        
        // Set placeholders
        emailField.textEdition.placeholder = "name@example.com";
        passwordField.textEdition.placeholder = "Enter your password";
        
        // Load saved email if remember me was checked
        if (PlayerPrefs.GetInt("RememberMe", 0) == 1)
        {
            emailField.value = PlayerPrefs.GetString("SavedEmail", "");
            rememberToggle.value = true;
        }
        
        // Button handlers
        signinBtn.clicked += OnSignIn;
        
        var forgotBtn = root.Q<Button>("forgot-btn");
        forgotBtn.clicked += OnForgotPassword;
        
        var signupBtn = root.Q<Button>("signup-btn");
        signupBtn.clicked += OnSignUp;
    }
    
    void OnSignIn()
    {
        string email = emailField.value;
        string password = passwordField.value;
        
        // Validation
        if (string.IsNullOrEmpty(email) || string.IsNullOrEmpty(password))
        {
            ShowToast("Please fill in all fields", "error");
            return;
        }
        
        // Save remember me preference
        if (rememberToggle.value)
        {
            PlayerPrefs.SetString("SavedEmail", email);
            PlayerPrefs.SetInt("RememberMe", 1);
        }
        else
        {
            PlayerPrefs.DeleteKey("SavedEmail");
            PlayerPrefs.SetInt("RememberMe", 0);
        }
        
        // Disable button while authenticating
        signinBtn.SetEnabled(false);
        signinBtn.text = "Signing in...";
        
        // Authenticate (your logic here)
        StartCoroutine(AuthenticateUser(email, password));
    }
    
    System.Collections.IEnumerator AuthenticateUser(string email, string password)
    {
        // Simulate network request
        yield return new WaitForSeconds(1.5f);
        
        // Success
        ShowToast("Signed in successfully", "success");
        
        // Re-enable button
        signinBtn.SetEnabled(true);
        signinBtn.text = "Sign In";
        
        // Navigate to main screen
        // SceneManager.LoadScene("MainMenu");
    }
    
    void OnForgotPassword()
    {
        ShowToast("Password reset link sent", "success");
    }
    
    void OnSignUp()
    {
        // Navigate to signup screen
    }
    
    void ShowToast(string message, string type)
    {
        var toast = new VisualElement();
        toast.AddToClassList("ds-toast");
        toast.AddToClassList($"ds-toast--{type}");
        
        var icon = new VisualElement();
        icon.AddToClassList("ds-icon");
        icon.AddToClassList("ds-icon--sm");
        icon.AddToClassList(type == "success" ? "ds-icon--check" : "ds-icon--close");
        
        var label = new Label(message);
        label.AddToClassList("ds-body-2");
        
        toast.Add(icon);
        toast.Add(label);
        root.Add(toast);
        
        root.schedule.Execute(() => root.Remove(toast)).ExecuteLater(3000);
    }
}
```

## Typography Classes

```xml
<ui:Label text="Main Heading" class="ds-h1" />
<ui:Label text="Section Heading" class="ds-h2" />
<ui:Label text="Subsection" class="ds-h3" />
<ui:Label text="Card Title" class="ds-h4" />

<ui:Label text="Body text large" class="ds-body-1" />
<ui:Label text="Body text standard" class="ds-body-2" />
<ui:Label text="Caption text" class="ds-caption" />

<ui:Label text="Input Label" class="ds-label" />
<ui:Label text="Overline Text" class="ds-overline" />
```

## Common Patterns

### List with Cards

```xml
<ui:ScrollView class="ds-scrollview">
  <ui:VisualElement class="ds-card" style="margin-bottom: 16px;">
    <ui:VisualElement class="ds-row" style="justify-content: space-between;">
      <ui:Label text="Item Name" class="ds-h4" />
      <ui:Label text="$29.99" class="ds-body-1" style="color: var(--color-primary);" />
    </ui:VisualElement>
    <ui:Label text="Description of the item" class="ds-body-2 ds-text-secondary" />
    <ui:Button text="Add to Cart" class="ds-btn ds-btn--primary ds-btn--sm" />
  </ui:VisualElement>
  <!-- More cards... -->
</ui:ScrollView>
```

### Navigation Bar

```xml
<!-- Bottom navigation (mobile) -->
<ui:VisualElement class="ds-bottom-nav">
  <ui:Button class="ds-bottom-nav__item is-active">
    <ui:VisualElement class="ds-icon ds-icon--home" />
    <ui:Label text="Home" />
  </ui:Button>
  <ui:Button class="ds-bottom-nav__item">
    <ui:VisualElement class="ds-icon ds-icon--search" />
    <ui:Label text="Search" />
  </ui:Button>
  <ui:Button class="ds-bottom-nav__item">
    <ui:VisualElement class="ds-icon ds-icon--user" />
    <ui:Label text="Profile" />
  </ui:Button>
</ui:VisualElement>

<!-- Side navigation (desktop) -->
<ui:VisualElement class="ds-side-nav">
  <ui:Button class="ds-side-nav__item is-active">
    <ui:VisualElement class="ds-icon ds-icon--home" />
    <ui:Label text="Home" />
  </ui:Button>
  <ui:Button class="ds-side-nav__item">
    <ui:VisualElement class="ds-icon ds-icon--settings" />
    <ui:Label text="Settings" />
  </ui:Button>
</ui:VisualElement>
```

### Empty State

```xml
<ui:VisualElement class="ds-empty-state">
  <ui:VisualElement class="ds-icon ds-icon--lg ds-icon--box" />
  <ui:Label text="No items yet" class="ds-h3" />
  <ui:Label text="Start adding items to your collection" class="ds-body-2 ds-text-secondary" />
  <ui:Button text="Add Item" class="ds-btn ds-btn--primary" />
</ui:VisualElement>
```

## Troubleshooting

### Icons Not Showing

**Problem**: Icons appear as empty boxes.

**Solution**: Ensure SVG files are imported as Texture (svgType: 3). Check `.meta` files:

```yaml
TextureImporter:
  svgType: 3
```

Re-import if needed: Right-click icon folder → Reimport.

### Toggles Missing Knob

**Problem**: Toggle appears as empty box.

**Solution**: The `DesignSystemRuntime.cs` script must be active. It auto-attaches to UIDocuments. Verify in Hierarchy that your UIDocument GameObject has the script attached.

### Mobile Class Not Applying

**Problem**: UI doesn't change when adding `.mobile` class.

**Solution**: Ensure `Mobile.uss` is imported after `DesignSystem.uss`. Check import order in UXML or add mobile class after document loads:

```csharp
void Start()
{
    yield return null; // Wait one frame for USS to load
    if (IsMobile())
    {
        root.AddToClassList("mobile");
    }
}
```

### Scrollbar Not Themed

**Problem**: Scrollbar uses default Unity style.

**Solution**: The scrollbar must be inside `.ds-root`. Check hierarchy:

```xml
<ui:VisualElement class="ds-root">
  <ui:ScrollView> <!-- This will get themed scrollbar -->
    <!--
