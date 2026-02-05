---
name: localizing-wpf-applications
description: Localizes WPF applications using resource files, x:Uid, and BAML localization. Use when building multi-language applications or supporting right-to-left layouts.
---

# WPF Localization Patterns

Implementing multi-language support in WPF applications.

## 1. Localization Overview

```
Localization Approaches
├── Resource Files (.resx)
│   ├── Simple string lookup
│   └── Strongly-typed access
├── BAML Localization
│   ├── x:Uid attributes
│   └── LocBaml tool
└── Runtime Features
    ├── FlowDirection (RTL support)
    ├── Culture-aware formatting
    └── Dynamic language switching
```

---

## 2. Resource File Approach

### 2.1 Creating Resource Files

```
Project Structure:
├── Properties/
│   └── Resources.resx          (default/fallback)
├── Resources/
│   ├── Strings.resx            (default English)
│   ├── Strings.ko-KR.resx      (Korean)
│   ├── Strings.ja-JP.resx      (Japanese)
│   └── Strings.de-DE.resx      (German)
```

### 2.2 Resource File Content

**Strings.resx (English - default):**
```xml
<data name="AppTitle" xml:space="preserve">
    <value>My Application</value>
</data>
<data name="WelcomeMessage" xml:space="preserve">
    <value>Welcome, {0}!</value>
</data>
<data name="SaveButton" xml:space="preserve">
    <value>Save</value>
</data>
<data name="CancelButton" xml:space="preserve">
    <value>Cancel</value>
</data>
```

**Strings.ko-KR.resx (Korean):**
```xml
<data name="AppTitle" xml:space="preserve">
    <value>내 애플리케이션</value>
</data>
<data name="WelcomeMessage" xml:space="preserve">
    <value>환영합니다, {0}님!</value>
</data>
<data name="SaveButton" xml:space="preserve">
    <value>저장</value>
</data>
<data name="CancelButton" xml:space="preserve">
    <value>취소</value>
</data>
```

### 2.3 Using Resources in XAML

```xml
<Window xmlns:p="clr-namespace:MyApp.Resources">
    <Window.Title>
        <Binding Source="{x:Static p:Strings.AppTitle}"/>
    </Window.Title>

    <StackPanel>
        <TextBlock Text="{x:Static p:Strings.WelcomeMessage}"/>
        <Button Content="{x:Static p:Strings.SaveButton}"/>
        <Button Content="{x:Static p:Strings.CancelButton}"/>
    </StackPanel>
</Window>
```

### 2.4 Using Resources in Code

```csharp
using MyApp.Resources;

// Direct access
var title = Strings.AppTitle;

// Formatted string
var welcome = string.Format(Strings.WelcomeMessage, userName);

// Access by key (for dynamic keys)
var value = Strings.ResourceManager.GetString("SaveButton");
```

---

## 3. Setting Culture

### 3.1 At Application Startup

```csharp
namespace MyApp;

using System.Globalization;
using System.Threading;
using System.Windows;

public partial class App : Application
{
    protected override void OnStartup(StartupEventArgs e)
    {
        base.OnStartup(e);

        // Set culture from user settings or system
        var cultureName = GetSavedCulture() ?? CultureInfo.CurrentCulture.Name;
        SetCulture(cultureName);
    }

    public static void SetCulture(string cultureName)
    {
        var culture = new CultureInfo(cultureName);

        // Set for current thread
        Thread.CurrentThread.CurrentCulture = culture;
        Thread.CurrentThread.CurrentUICulture = culture;

        // Set for new threads (.NET 4.6+)
        CultureInfo.DefaultThreadCurrentCulture = culture;
        CultureInfo.DefaultThreadCurrentUICulture = culture;
    }

    private string? GetSavedCulture()
    {
        return Properties.Settings.Default.Culture;
    }
}
```

### 3.2 Dynamic Language Switching

```csharp
namespace MyApp.Services;

using System.Globalization;
using System.Threading;
using System.Windows;

public sealed class LocalizationService
{
    public event EventHandler? CultureChanged;

    public CultureInfo CurrentCulture => Thread.CurrentThread.CurrentUICulture;

    public void ChangeCulture(string cultureName)
    {
        var culture = new CultureInfo(cultureName);

        Thread.CurrentThread.CurrentCulture = culture;
        Thread.CurrentThread.CurrentUICulture = culture;
        CultureInfo.DefaultThreadCurrentCulture = culture;
        CultureInfo.DefaultThreadCurrentUICulture = culture;

        // Save preference
        Properties.Settings.Default.Culture = cultureName;
        Properties.Settings.Default.Save();

        // Notify subscribers
        CultureChanged?.Invoke(this, EventArgs.Empty);

        // Restart required for full XAML update
        RestartApplication();
    }

    private void RestartApplication()
    {
        var result = MessageBox.Show(
            "Application needs to restart to apply language change. Restart now?",
            "Language Changed",
            MessageBoxButton.YesNo);

        if (result == MessageBoxResult.Yes)
        {
            System.Diagnostics.Process.Start(Application.ResourceAssembly.Location);
            Application.Current.Shutdown();
        }
    }
}
```

---

## 4. BAML Localization (x:Uid)

### 4.1 Adding x:Uid Attributes

```xml
<Window x:Uid="MainWindow">
    <Grid x:Uid="MainGrid">
        <TextBlock x:Uid="TitleText" Text="Welcome"/>
        <Button x:Uid="SaveButton" Content="Save"/>
        <Button x:Uid="CancelButton" Content="Cancel"/>
    </Grid>
</Window>
```

### 4.2 Project Configuration

```xml
<!-- .csproj -->
<PropertyGroup>
    <UICulture>en-US</UICulture>
</PropertyGroup>
```

### 4.3 Using LocBaml Tool

```bash
# Extract resources to CSV
LocBaml /parse MyApp.exe /out:en-US.csv

# Create satellite assembly
LocBaml /generate MyApp.resources.dll /trans:ko-KR.csv /cul:ko-KR /out:.\ko-KR
```

---

## 5. FlowDirection (RTL Support)

### 5.1 Setting FlowDirection

```xml
<!-- Left-to-Right (default) -->
<Window FlowDirection="LeftToRight">

<!-- Right-to-Left (Arabic, Hebrew) -->
<Window FlowDirection="RightToLeft">

<!-- Inherit from parent -->
<StackPanel FlowDirection="{Binding ElementName=Window, Path=FlowDirection}">
```

### 5.2 Dynamic FlowDirection

```csharp
public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();

        // Set based on current culture
        var culture = Thread.CurrentThread.CurrentUICulture;
        FlowDirection = culture.TextInfo.IsRightToLeft
            ? FlowDirection.RightToLeft
            : FlowDirection.LeftToRight;
    }
}
```

### 5.3 Mirroring Exceptions

```xml
<!-- Prevent mirroring for specific elements -->
<Image Source="logo.png" FlowDirection="LeftToRight"/>

<!-- Numbers should not be mirrored -->
<TextBlock FlowDirection="LeftToRight" Text="{Binding PhoneNumber}"/>
```

---

## 6. Date, Number, Currency Formatting

### 6.1 Culture-Aware Formatting in XAML

```xml
<!-- Date formatting -->
<TextBlock Text="{Binding Date, StringFormat={}{0:d}}"/>
<!-- en-US: 1/21/2026, ko-KR: 2026-01-21 -->

<!-- Currency formatting -->
<TextBlock Text="{Binding Price, StringFormat={}{0:C}}"/>
<!-- en-US: $1,234.56, ko-KR: ₩1,234 -->

<!-- Number formatting -->
<TextBlock Text="{Binding Amount, StringFormat={}{0:N2}}"/>
<!-- en-US: 1,234.56, de-DE: 1.234,56 -->
```

### 6.2 Culture-Aware Formatting in Code

```csharp
// Uses current thread culture
var dateStr = DateTime.Now.ToString("d");
var currencyStr = price.ToString("C");

// Specific culture
var koKr = new CultureInfo("ko-KR");
var dateKr = DateTime.Now.ToString("d", koKr);  // 2026-01-21
var currencyKr = price.ToString("C", koKr);     // ₩1,234
```

---

## 7. Binding Converter with Localization

```csharp
namespace MyApp.Converters;

using System;
using System.Globalization;
using System.Windows.Data;
using MyApp.Resources;

public class LocalizedEnumConverter : IValueConverter
{
    public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
    {
        if (value is Enum enumValue)
        {
            // Get localized string from resources
            var key = $"{enumValue.GetType().Name}_{enumValue}";
            return Strings.ResourceManager.GetString(key, culture) ?? enumValue.ToString();
        }

        return value?.ToString() ?? string.Empty;
    }

    public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
    {
        throw new NotImplementedException();
    }
}
```

---

## 8. Localized Resources in XAML

### 8.1 String Resources

```csharp
// Create LocalizedStrings class for easy XAML binding
namespace MyApp.Resources;

public class LocalizedStrings
{
    private static readonly Strings _strings = new();

    public Strings Strings => _strings;
}
```

```xml
<Application.Resources>
    <local:LocalizedStrings x:Key="LocalizedStrings"/>
</Application.Resources>

<!-- Usage -->
<TextBlock Text="{Binding Source={StaticResource LocalizedStrings},
                         Path=Strings.WelcomeMessage}"/>
```

### 8.2 Localized Images

```
Resources/
├── Images/
│   ├── flag.png            (default)
│   ├── flag.ko-KR.png      (Korean)
│   └── flag.ja-JP.png      (Japanese)
```

```csharp
public static class LocalizedImageHelper
{
    public static string GetLocalizedImagePath(string basePath)
    {
        var culture = Thread.CurrentThread.CurrentUICulture.Name;
        var dir = Path.GetDirectoryName(basePath);
        var name = Path.GetFileNameWithoutExtension(basePath);
        var ext = Path.GetExtension(basePath);

        // Try culture-specific image
        var localizedPath = Path.Combine(dir!, $"{name}.{culture}{ext}");

        if (File.Exists(localizedPath))
            return localizedPath;

        return basePath;
    }
}
```

---

## 9. Language Selection UI

```xml
<ComboBox x:Name="LanguageSelector"
          SelectionChanged="LanguageSelector_SelectionChanged">
    <ComboBoxItem Tag="en-US" Content="English"/>
    <ComboBoxItem Tag="ko-KR" Content="한국어"/>
    <ComboBoxItem Tag="ja-JP" Content="日本語"/>
    <ComboBoxItem Tag="de-DE" Content="Deutsch"/>
</ComboBox>
```

```csharp
private void LanguageSelector_SelectionChanged(object sender, SelectionChangedEventArgs e)
{
    if (LanguageSelector.SelectedItem is ComboBoxItem item)
    {
        var cultureName = item.Tag?.ToString();

        if (!string.IsNullOrEmpty(cultureName))
        {
            _localizationService.ChangeCulture(cultureName);
        }
    }
}
```

---

## 10. References

- [WPF Globalization and Localization Overview - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/wpf-globalization-and-localization-overview)
- [Localizing XAML - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/how-to-localize-an-application)
- [CultureInfo Class - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/api/system.globalization.cultureinfo)
