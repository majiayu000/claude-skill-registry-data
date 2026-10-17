---
name: materialdesigninxaml-wpf-toolkit
description: Google's Material Design theme and control library for WPF applications in C# and VB.Net
triggers:
  - how do I add Material Design to my WPF app
  - setup Material Design themes in XAML
  - use Material Design controls in WPF
  - configure Material Design color palette
  - create Material Design dialogs in WPF
  - implement Material Design cards and buttons
  - style WPF app with Material Design
  - add Material Design icons to XAML
---

# MaterialDesignInXamlToolkit

> Skill by [ara.so](https://ara.so) — Design Skills collection.

Comprehensive Material Design theme and control library for Windows desktop WPF applications. Provides Material Design styles for all major WPF controls, additional custom controls (cards, dialogs, chips, etc.), easy palette configuration, full Material Design Icons pack, and transition effects.

## Installation

Install via NuGet Package Manager or Package Manager Console:

```powershell
Install-Package MaterialDesignThemes
```

Or via .NET CLI:

```bash
dotnet add package MaterialDesignThemes
```

## Initial Setup

### App.xaml Configuration

Configure the base theme in your `App.xaml`:

```xml
<Application 
    x:Class="YourApp.App"
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
    xmlns:materialDesign="http://materialdesigninxaml.net/winfx/xaml/themes"
    StartupUri="MainWindow.xaml">
    <Application.Resources>
        <ResourceDictionary>
            <ResourceDictionary.MergedDictionaries>
                <!-- Material Design 2 (Classic) -->
                <materialDesign:BundledTheme 
                    BaseTheme="Light" 
                    PrimaryColor="DeepPurple" 
                    SecondaryColor="Lime" />
                <ResourceDictionary Source="pack://application:,,,/MaterialDesignThemes.Wpf;component/Themes/MaterialDesign2.Defaults.xaml" />
                
                <!-- OR Material Design 3 (Modern) -->
                <!-- <materialDesign:BundledTheme 
                    BaseTheme="Light" 
                    PrimaryColor="DeepPurple" 
                    SecondaryColor="Lime" />
                <ResourceDictionary Source="pack://application:,,,/MaterialDesignThemes.Wpf;component/Themes/MaterialDesign3.Defaults.xaml" /> -->
            </ResourceDictionary.MergedDictionaries>
        </ResourceDictionary>
    </Application.Resources>
</Application>
```

### Window Setup

Apply Material Design style to your main window:

```xml
<Window x:Class="YourApp.MainWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:materialDesign="http://materialdesigninxaml.net/winfx/xaml/themes"
        Style="{StaticResource MaterialDesignWindow}"
        Height="450" Width="800">
    <!-- Your content here -->
</Window>
```

## Theme Configuration

### Available Color Palettes

Primary and Secondary colors can be set to:
- Red, Pink, Purple, DeepPurple, Indigo, Blue, LightBlue, Cyan, Teal, Green, LightGreen, Lime, Yellow, Amber, Orange, DeepOrange, Brown, Grey, BlueGrey

### Dark Theme

```xml
<materialDesign:BundledTheme 
    BaseTheme="Dark" 
    PrimaryColor="Indigo" 
    SecondaryColor="Cyan" />
```

### Runtime Theme Switching

In C#:

```csharp
using MaterialDesignThemes.Wpf;
using MaterialDesignColors;

// Switch to dark theme
var paletteHelper = new PaletteHelper();
ITheme theme = paletteHelper.GetTheme();
theme.SetBaseTheme(Theme.Dark);
paletteHelper.SetTheme(theme);

// Change primary color
theme.SetPrimaryColor(Colors.Blue);
paletteHelper.SetTheme(theme);

// Change secondary color
theme.SetSecondaryColor(Colors.Lime);
paletteHelper.SetTheme(theme);
```

## Common Controls

### Buttons

```xml
<!-- Contained Button (default) -->
<Button Style="{StaticResource MaterialDesignRaisedButton}"
        Content="Raised Button" />

<!-- Outlined Button -->
<Button Style="{StaticResource MaterialDesignOutlinedButton}"
        Content="Outlined Button" />

<!-- Text Button -->
<Button Style="{StaticResource MaterialDesignFlatButton}"
        Content="Flat Button" />

<!-- Icon Button -->
<Button Style="{StaticResource MaterialDesignIconButton}"
        ToolTip="Delete">
    <materialDesign:PackIcon Kind="Delete" />
</Button>

<!-- Floating Action Button (FAB) -->
<Button Style="{StaticResource MaterialDesignFloatingActionButton}"
        ToolTip="Add">
    <materialDesign:PackIcon Kind="Plus" />
</Button>

<!-- Mini FAB -->
<Button Style="{StaticResource MaterialDesignFloatingActionMiniButton}">
    <materialDesign:PackIcon Kind="Pencil" />
</Button>
```

### Cards

```xml
<materialDesign:Card Padding="16" Margin="8">
    <StackPanel>
        <TextBlock Style="{StaticResource MaterialDesignHeadline6TextBlock}"
                   Text="Card Title" />
        <TextBlock Style="{StaticResource MaterialDesignBody2TextBlock}"
                   TextWrapping="Wrap"
                   Text="Card content goes here. Cards contain content and actions about a single subject." />
        <StackPanel Orientation="Horizontal" HorizontalAlignment="Right" Margin="0,16,0,0">
            <Button Style="{StaticResource MaterialDesignFlatButton}"
                    Content="ACTION 1" />
            <Button Style="{StaticResource MaterialDesignFlatButton}"
                    Content="ACTION 2" />
        </StackPanel>
    </StackPanel>
</materialDesign:Card>
```

### Text Fields

```xml
<!-- Filled TextField -->
<TextBox materialDesign:HintAssist.Hint="Email"
         Style="{StaticResource MaterialDesignFilledTextBox}" />

<!-- Outlined TextField -->
<TextBox materialDesign:HintAssist.Hint="Name"
         Style="{StaticResource MaterialDesignOutlinedTextBox}" />

<!-- With Helper Text -->
<TextBox materialDesign:HintAssist.Hint="Username"
         materialDesign:HintAssist.HelperText="Choose a unique username"
         Style="{StaticResource MaterialDesignFilledTextBox}" />

<!-- With Character Counter -->
<TextBox materialDesign:HintAssist.Hint="Description"
         materialDesign:TextFieldAssist.CharacterCounterVisibility="Visible"
         MaxLength="100"
         Style="{StaticResource MaterialDesignOutlinedTextBox}" />

<!-- Password Field -->
<PasswordBox materialDesign:HintAssist.Hint="Password"
             Style="{StaticResource MaterialDesignFilledPasswordBox}" />
```

### Icons

Using Material Design Icons pack:

```xml
<!-- Simple Icon -->
<materialDesign:PackIcon Kind="Home" />

<!-- Sized Icon -->
<materialDesign:PackIcon Kind="Account" Width="24" Height="24" />

<!-- Colored Icon -->
<materialDesign:PackIcon Kind="Heart" Foreground="Red" Width="32" Height="32" />

<!-- In Button -->
<Button>
    <StackPanel Orientation="Horizontal">
        <materialDesign:PackIcon Kind="Delete" Margin="0,0,8,0" />
        <TextBlock Text="Delete" />
    </StackPanel>
</Button>
```

Browse all icons at: https://materialdesignicons.com/

### Chips

```xml
<!-- Basic Chip -->
<materialDesign:Chip Content="Basic Chip" />

<!-- Deletable Chip -->
<materialDesign:Chip Content="Deletable"
                     IsDeletable="True"
                     DeleteClick="Chip_DeleteClick" />

<!-- Chip with Icon -->
<materialDesign:Chip>
    <StackPanel Orientation="Horizontal">
        <materialDesign:PackIcon Kind="Account" />
        <TextBlock Text="User Chip" Margin="8,0,0,0" />
    </StackPanel>
</materialDesign:Chip>

<!-- Chip Group -->
<materialDesign:ChipGroup>
    <materialDesign:Chip Content="Choice 1" />
    <materialDesign:Chip Content="Choice 2" />
    <materialDesign:Chip Content="Choice 3" />
</materialDesign:ChipGroup>
```

### Dialogs

In XAML:

```xml
<Grid>
    <Grid.RowDefinitions>
        <RowDefinition Height="Auto" />
        <RowDefinition Height="*" />
    </Grid.RowDefinations>
    
    <!-- Dialog Host Container -->
    <materialDesign:DialogHost Identifier="RootDialog" Grid.RowSpan="2">
        <!-- Your main content -->
        <Grid>
            <Button Content="Open Dialog" Click="OpenDialog_Click" />
        </Grid>
    </materialDesign:DialogHost>
</Grid>
```

In C#:

```csharp
using MaterialDesignThemes.Wpf;

// Simple message dialog
private async void OpenDialog_Click(object sender, RoutedEventArgs e)
{
    await DialogHost.Show(new TextBlock 
    { 
        Text = "This is a dialog",
        Margin = new Thickness(16)
    }, "RootDialog");
}

// Custom dialog content
private async void OpenCustomDialog_Click(object sender, RoutedEventArgs e)
{
    var view = new SampleDialogView(); // Your UserControl
    var result = await DialogHost.Show(view, "RootDialog");
    
    if (result is bool boolResult && boolResult)
    {
        // User clicked OK/Accept
    }
}

// Close dialog from within dialog content
private void CloseDialog_Click(object sender, RoutedEventArgs e)
{
    DialogHost.Close("RootDialog", true); // Pass result
}
```

Full dialog with custom content:

```xml
<!-- SampleDialog.xaml -->
<StackPanel Margin="16">
    <TextBlock Style="{StaticResource MaterialDesignHeadline6TextBlock}"
               Text="Confirm Action" />
    <TextBlock Margin="0,16"
               Text="Are you sure you want to proceed?" />
    <StackPanel Orientation="Horizontal" HorizontalAlignment="Right">
        <Button Style="{StaticResource MaterialDesignFlatButton}"
                Content="CANCEL"
                Command="{x:Static materialDesign:DialogHost.CloseDialogCommand}">
            <Button.CommandParameter>
                <system:Boolean>False</system:Boolean>
            </Button.CommandParameter>
        </Button>
        <Button Style="{StaticResource MaterialDesignFlatButton}"
                Content="OK"
                Command="{x:Static materialDesign:DialogHost.CloseDialogCommand}">
            <Button.CommandParameter>
                <system:Boolean>True</system:Boolean>
            </Button.CommandParameter>
        </Button>
    </StackPanel>
</StackPanel>
```

### Snackbar

In XAML:

```xml
<materialDesign:Snackbar x:Name="MainSnackbar"
                         MessageQueue="{materialDesign:MessageQueue}" />
```

In C#:

```csharp
using MaterialDesignThemes.Wpf;

public partial class MainWindow : Window
{
    private SnackbarMessageQueue _messageQueue;
    
    public MainWindow()
    {
        InitializeComponent();
        _messageQueue = new SnackbarMessageQueue(TimeSpan.FromSeconds(3));
        MainSnackbar.MessageQueue = _messageQueue;
    }
    
    private void ShowSnackbar_Click(object sender, RoutedEventArgs e)
    {
        _messageQueue.Enqueue("Item added to cart");
    }
    
    private void ShowSnackbarWithAction_Click(object sender, RoutedEventArgs e)
    {
        _messageQueue.Enqueue(
            "Item deleted",
            "UNDO",
            () => { /* Undo action */ },
            null,
            false,
            true);
    }
}
```

### Progress Indicators

```xml
<!-- Circular Progress (Indeterminate) -->
<ProgressBar Style="{StaticResource MaterialDesignCircularProgressBar}"
             IsIndeterminate="True" />

<!-- Circular Progress (Determinate) -->
<ProgressBar Style="{StaticResource MaterialDesignCircularProgressBar}"
             Value="65"
             Maximum="100" />

<!-- Linear Progress (Indeterminate) -->
<ProgressBar Style="{StaticResource MaterialDesignLinearProgressBar}"
             IsIndeterminate="True" />

<!-- Linear Progress (Determinate) -->
<ProgressBar Style="{StaticResource MaterialDesignLinearProgressBar}"
             Value="45"
             Maximum="100" />
```

### DatePicker and TimePicker

```xml
<!-- DatePicker -->
<DatePicker materialDesign:HintAssist.Hint="Select Date"
            Style="{StaticResource MaterialDesignFilledDatePicker}" />

<!-- TimePicker -->
<materialDesign:TimePicker materialDesign:HintAssist.Hint="Select Time"
                           Style="{StaticResource MaterialDesignFilledTimePicker}" />

<!-- Clock -->
<materialDesign:Clock />
```

### ComboBox

```xml
<!-- Filled ComboBox -->
<ComboBox materialDesign:HintAssist.Hint="Select Option"
          Style="{StaticResource MaterialDesignFilledComboBox}">
    <ComboBoxItem Content="Option 1" />
    <ComboBoxItem Content="Option 2" />
    <ComboBoxItem Content="Option 3" />
</ComboBox>

<!-- Outlined ComboBox -->
<ComboBox materialDesign:HintAssist.Hint="Country"
          Style="{StaticResource MaterialDesignOutlinedComboBox}"
          ItemsSource="{Binding Countries}"
          DisplayMemberPath="Name" />
```

### CheckBox and RadioButton

```xml
<!-- CheckBox -->
<CheckBox Content="Accept terms and conditions" />

<!-- RadioButton -->
<StackPanel>
    <RadioButton Content="Option A" GroupName="Options" />
    <RadioButton Content="Option B" GroupName="Options" />
    <RadioButton Content="Option C" GroupName="Options" />
</StackPanel>

<!-- Switch/Toggle -->
<ToggleButton Style="{StaticResource MaterialDesignSwitchToggleButton}"
              ToolTip="Enable notifications" />
```

### ListBox and ListView

```xml
<!-- Material Design ListBox -->
<ListBox>
    <ListBoxItem>
        <StackPanel Orientation="Horizontal">
            <materialDesign:PackIcon Kind="Account" VerticalAlignment="Center" />
            <TextBlock Text="User Profile" Margin="16,0,0,0" />
        </StackPanel>
    </ListBoxItem>
    <ListBoxItem>
        <StackPanel Orientation="Horizontal">
            <materialDesign:PackIcon Kind="Settings" VerticalAlignment="Center" />
            <TextBlock Text="Settings" Margin="16,0,0,0" />
        </StackPanel>
    </ListBoxItem>
</ListBox>
```

### DataGrid

```xml
<DataGrid ItemsSource="{Binding Users}"
          CanUserAddRows="False"
          AutoGenerateColumns="False"
          materialDesign:DataGridAssist.CellPadding="13 8 8 8"
          materialDesign:DataGridAssist.ColumnHeaderPadding="8">
    <DataGrid.Columns>
        <DataGridTextColumn Header="Name" Binding="{Binding Name}" />
        <DataGridTextColumn Header="Email" Binding="{Binding Email}" />
        <DataGridCheckBoxColumn Header="Active" Binding="{Binding IsActive}" />
    </DataGrid.Columns>
</DataGrid>
```

## Advanced Features

### Color Zones

```xml
<!-- Primary Color Zone -->
<materialDesign:ColorZone Mode="PrimaryLight" Padding="16">
    <TextBlock Text="Primary Light" />
</materialDesign:ColorZone>

<!-- Secondary Color Zone -->
<materialDesign:ColorZone Mode="SecondaryMid" Padding="16">
    <TextBlock Text="Secondary Mid" />
</materialDesign:ColorZone>

<!-- Dark Color Zone -->
<materialDesign:ColorZone Mode="Dark" Padding="16">
    <TextBlock Text="Dark Zone" />
</materialDesign:ColorZone>
```

Modes: `Standard`, `Inverted`, `PrimaryLight`, `PrimaryMid`, `PrimaryDark`, `Accent`, `Light`, `Dark`, `SecondaryLight`, `SecondaryMid`, `SecondaryDark`

### DrawerHost (Navigation Drawer)

```xml
<materialDesign:DrawerHost IsLeftDrawerOpen="{Binding IsDrawerOpen}">
    <!-- Left Drawer Content -->
    <materialDesign:DrawerHost.LeftDrawerContent>
        <StackPanel Margin="16">
            <TextBlock Text="Navigation" 
                       Style="{StaticResource MaterialDesignHeadline6TextBlock}" />
            <ListBox>
                <ListBoxItem Content="Home" />
                <ListBoxItem Content="Profile" />
                <ListBoxItem Content="Settings" />
            </ListBox>
        </StackPanel>
    </materialDesign:DrawerHost.LeftDrawerContent>
    
    <!-- Main Content -->
    <Grid>
        <Button Content="Open Drawer"
                Command="{x:Static materialDesign:DrawerHost.OpenDrawerCommand}"
                CommandParameter="{x:Static Dock.Left}" />
    </Grid>
</materialDesign:DrawerHost>
```

### Elevation (Shadows)

```xml
<!-- Apply shadow depth -->
<Border Background="White"
        materialDesign:ElevationAssist.Elevation="Dp4"
        Padding="16">
    <TextBlock Text="Card with Dp4 elevation" />
</Border>
```

Elevation values: `Dp0`, `Dp1`, `Dp2`, `Dp3`, `Dp4`, `Dp5`, `Dp6`, `Dp8`, `Dp9`, `Dp12`, `Dp16`, `Dp24`

### Transitions

```xml
<materialDesign:Transitioner SelectedIndex="{Binding SelectedIndex}">
    <materialDesign:TransitionerSlide>
        <Grid>
            <TextBlock Text="First Slide" />
        </Grid>
    </materialDesign:TransitionerSlide>
    <materialDesign:TransitionerSlide>
        <Grid>
            <TextBlock Text="Second Slide" />
        </Grid>
    </materialDesign:TransitionerSlide>
</materialDesign:Transitioner>
```

Navigate programmatically:

```csharp
// Move to next slide
materialDesignTransitioner.MoveNextCommand.Execute(null);

// Move to previous slide
materialDesignTransitioner.MovePreviousCommand.Execute(null);

// Move to specific index
SelectedIndex = 1;
```

## MVVM Pattern Integration

### ViewModel Example

```csharp
using System.Windows.Input;
using MaterialDesignThemes.Wpf;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

public partial class MainViewModel : ObservableObject
{
    [ObservableProperty]
    private string _userName;
    
    [ObservableProperty]
    private bool _isDarkTheme;
    
    private readonly PaletteHelper _paletteHelper;
    private readonly SnackbarMessageQueue _messageQueue;
    
    public MainViewModel()
    {
        _paletteHelper = new PaletteHelper();
        _messageQueue = new SnackbarMessageQueue();
    }
    
    public SnackbarMessageQueue MessageQueue => _messageQueue;
    
    [RelayCommand]
    private void ToggleTheme()
    {
        ITheme theme = _paletteHelper.GetTheme();
        theme.SetBaseTheme(IsDarkTheme ? Theme.Dark : Theme.Light);
        _paletteHelper.SetTheme(theme);
        
        _messageQueue.Enqueue($"Theme changed to {(IsDarkTheme ? "Dark" : "Light")}");
    }
    
    [RelayCommand]
    private async Task ShowDialog()
    {
        var view = new ConfirmDialogView();
        var result = await DialogHost.Show(view, "RootDialog");
        
        if (result is bool boolResult && boolResult)
        {
            _messageQueue.Enqueue("Action confirmed");
        }
    }
}
```

### View Binding

```xml
<Window x:Class="YourApp.MainWindow"
        xmlns:materialDesign="http://materialdesigninxaml.net/winfx/xaml/themes">
    <Grid>
        <StackPanel>
            <TextBox Text="{Binding UserName, UpdateSourceTrigger=PropertyChanged}"
                     materialDesign:HintAssist.Hint="Username"
                     Style="{StaticResource MaterialDesignOutlinedTextBox}" />
            
            <ToggleButton IsChecked="{Binding IsDarkTheme}"
                          Command="{Binding ToggleThemeCommand}"
                          Style="{StaticResource MaterialDesignSwitchToggleButton}"
                          Content="Dark Theme" />
            
            <Button Content="Show Dialog"
                    Command="{Binding ShowDialogCommand}"
                    Style="{StaticResource MaterialDesignRaisedButton}" />
            
            <materialDesign:Snackbar MessageQueue="{Binding MessageQueue}" />
        </StackPanel>
    </Grid>
</Window>
```

## Common Patterns

### Theme Switcher Component

```xml
<!-- ThemeSwitch.xaml -->
<UserControl x:Class="YourApp.Controls.ThemeSwitch"
             xmlns:materialDesign="http://materialdesigninxaml.net/winfx/xaml/themes">
    <StackPanel Orientation="Horizontal">
        <materialDesign:PackIcon Kind="WeatherNight" VerticalAlignment="Center" />
        <ToggleButton x:Name="ThemeToggle"
                      Style="{StaticResource MaterialDesignSwitchToggleButton}"
                      Margin="8,0"
                      Checked="ThemeToggle_Checked"
                      Unchecked="ThemeToggle_Unchecked" />
        <materialDesign:PackIcon Kind="WeatherSunny" VerticalAlignment="Center" />
    </StackPanel>
</UserControl>
```

```csharp
// ThemeSwitch.xaml.cs
using MaterialDesignThemes.Wpf;

public partial class ThemeSwitch : UserControl
{
    private readonly PaletteHelper _paletteHelper = new PaletteHelper();
    
    public ThemeSwitch()
    {
        InitializeComponent();
        
        // Set initial state based on current theme
        ITheme theme = _paletteHelper.GetTheme();
        ThemeToggle.IsChecked = theme.GetBaseTheme() == BaseTheme.Dark;
    }
    
    private void ThemeToggle_Checked(object sender, RoutedEventArgs e)
    {
        ITheme theme = _paletteHelper.GetTheme();
        theme.SetBaseTheme(Theme.Dark);
        _paletteHelper.SetTheme(theme);
    }
    
    private void ThemeToggle_Unchecked(object sender, RoutedEventArgs e)
    {
        ITheme theme = _paletteHelper.GetTheme();
        theme.SetBaseTheme(Theme.Light);
        _paletteHelper.SetTheme(theme);
    }
}
```

### Confirm Delete Dialog

```xml
<!-- ConfirmDeleteDialog.xaml -->
<StackPanel Margin="16">
    <StackPanel Orientation="Horizontal" Margin="0,0,0,16">
        <materialDesign:PackIcon Kind="AlertCircle" 
                                 Foreground="{DynamicResource MaterialDesignValidationErrorBrush}"
                                 Width="24" Height="24"
                                 VerticalAlignment="Center" />
        <TextBlock Text="Confirm Delete"
                   Style="{StaticResource MaterialDesignHeadline6TextBlock}"
                   Margin="8,0,0,0" />
    </StackPanel>
    
    <TextBlock TextWrapping="Wrap"
               Text="Are you sure you want to delete this item? This action cannot be undone." />
    
    <StackPanel Orientation="Horizontal" HorizontalAlignment="Right" Margin="0,16,0,0">
        <Button Style="{StaticResource MaterialDesignFlatButton}"
                Content="CANCEL"
                Command="{x:Static materialDesign:DialogHost.CloseDialogCommand}">
            <Button.CommandParameter>
                <system:Boolean>False</system:Boolean>
            </Button.CommandParameter>
        </Button>
        <Button Style="{StaticResource MaterialDesignFlatButton}"
                Content="DELETE"
                Foreground="{DynamicResource MaterialDesignValidationErrorBrush}"
                Command="{x:Static materialDesign:DialogHost.CloseDialogCommand}">
            <Button.CommandParameter>
                <system:Boolean>True</system:Boolean>
            </Button.CommandParameter>
        </Button>
    </StackPanel>
</StackPanel>
```

### Loading Overlay

```xml
<Grid>
    <!-- Main Content -->
    <ContentControl Content="{Binding MainContent}" />
    
    <!-- Loading Overlay -->
    <Grid Visibility="{Binding IsLoading, Converter={StaticResource BooleanToVisibilityConverter}}"
          Background="#80000000">
        <StackPanel HorizontalAlignment="Center" VerticalAlignment="Center">
            <ProgressBar Style="{StaticResource MaterialDesignCircularProgressBar}"
                         IsIndeterminate="True"
                         Width="48" Height="48" />
            <TextBlock Text="Loading..."
                       Foreground="White"
                       Margin="0,16,0,0"
                       HorizontalAlignment="Center" />
        </StackPanel>
    </Grid>
</Grid>
```

## Troubleshooting

### Icons Not Showing

Ensure you've installed the package and added the resource dictionary:

```xml
<Application.Resources>
    <ResourceDictionary>
        <ResourceDictionary.MergedDictionaries>
            <materialDesign:BundledTheme BaseTheme="Light" PrimaryColor="Blue" SecondaryColor="Lime" />
            <ResourceDictionary Source="pack://application:,,,/MaterialDesignThemes.Wpf;component/Themes/MaterialDesign2.Defaults.xaml" />
        </ResourceDictionary.MergedDictionaries>
    </ResourceDictionary>
</Application.Resources>
```

### Theme Not Applying

1. Verify the `Style="{StaticResource MaterialDesignWindow}"` is set on your Window
2. Check that BundledTheme is correctly referenced in App.xaml
3. Ensure no conflicting styles are overriding Material Design styles

### Performance Issues

For better rendering performance:

```xml
<!-- In Window or UserControl -->
<Window TextOptions.TextFormattingMode="Ideal"
        TextOptions.TextRenderingMode="Auto"
        RenderOptions.BitmapScalingMode="HighQuality">
```

Or in code:

```csharp
RenderOptions.SetBitmapScalingMode(this, BitmapScalingMode.HighQuality);
TextOptions.SetTextFormattingMode(this, TextFormattingMode.Ideal);
TextOptions.SetTextRenderingMode(this, TextRenderingMode.Auto);
```

### Dialog Not Showing

Ensure DialogHost has an Identifier and you're using the correct identifier when showing:

```xml
<materialDesign:DialogHost Identifier="MainDialog">
```

```csharp
await DialogHost.Show(content, "MainDialog");
```

### Custom Colors Not Working

Use PaletteHelper to modify colors at runtime:

```csharp
var paletteHelper = new PaletteHelper();
ITheme theme = paletteHelper.GetTheme();

// Modify specific colors
var primaryColor = Color.FromRgb(33, 150, 243);
theme.SetPrimaryColor(primaryColor);

var secondaryColor = Color.FromRgb(255, 193, 7);
theme.SetSecondaryColor(secondaryColor);

paletteHelper.SetTheme(theme);
```

## Additional Resources

- **GitHub**: https://github.com/MaterialDesignInXAML/MaterialDesignInXamlToolkit
- **Wiki**: https://github.com/MaterialDesignInXAML/MaterialDesignInXamlToolkit/wiki
- **Demo Apps**: Included in source repository (MaterialDesignDemo, MaterialDesign3Demo)
- **Icon Pack**: https://materialdesignicons.com/
- **Discord**: Community support and discussion
- **Material Design Guidelines**: https://material.io/design/
