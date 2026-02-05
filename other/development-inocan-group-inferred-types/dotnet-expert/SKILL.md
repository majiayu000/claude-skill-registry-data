---
name: dotnet-expert
description: .NET 8.0 development expertise for VoiceLite including WPF patterns, async/await best practices, IDisposable patterns, and NuGet package recommendations. Activates when working on C# code, WPF XAML, or .NET-specific issues.
---

# .NET Expert

Specialized .NET 8.0 development guidance for VoiceLite's WPF desktop application.

## When This Skill Activates

- Working on `.cs` or `.xaml` files
- Mentions: "NuGet", "WPF", "XAML", "IDisposable", "async/await", "Dispatcher"
- Compiler errors: `CS####` error codes
- Performance issues: Memory leaks, GC pressure, threading
- .NET-specific questions: "How do I..." in C# context

## VoiceLite-Specific .NET Patterns

### 1. Disposal Pattern (CRITICAL for Audio Resources)

**NAudio WaveInEvent MUST be disposed** to prevent memory leaks:

```csharp
// AudioRecorder.cs - Proper disposal pattern
public class AudioRecorder : IDisposable
{
    private WaveInEvent? _waveIn;
    private bool _disposed = false;

    public void Dispose()
    {
        if (_disposed) return;

        // Stop recording first
        _waveIn?.StopRecording();

        // Dispose NAudio resources
        _waveIn?.Dispose();
        _waveIn = null;

        _disposed = true;
        GC.SuppressFinalize(this);
    }

    ~AudioRecorder()
    {
        Dispose();
    }
}

// CRITICAL: Test coverage required
// See: VoiceLite.Tests/Services/DisposalTests.cs
```

### 2. Dispatcher Pattern (UI Thread Safety)

**NEVER update UI from background thread** - always use Dispatcher:

```csharp
// MainWindow.xaml.cs - Correct UI updates
private async void OnTranscriptionCompleted(object sender, TranscriptionEventArgs e)
{
    // This event may fire from background thread!

    // ✅ CORRECT: Use Dispatcher for UI updates
    Application.Current.Dispatcher.Invoke(() =>
    {
        StatusLabel.Content = "Transcription complete";
        TranscriptionText.Text = e.Text;
    });

    // ❌ WRONG: Direct UI access from background thread
    // StatusLabel.Content = "..."; // Will throw InvalidOperationException!
}

// Async version
await Application.Current.Dispatcher.InvokeAsync(() =>
{
    // UI updates here
});
```

### 3. Async Event Handlers

**Event handlers can be `async void`** (only place this is acceptable):

```csharp
// MainWindow.xaml.cs
private async void OnAudioFileReady(object sender, AudioFileReadyEventArgs e)
{
    // async void is OK for event handlers
    try
    {
        await _whisperService.TranscribeAsync(e.FilePath);
    }
    catch (Exception ex)
    {
        ErrorLogger.Log($"Transcription failed: {ex.Message}");
    }
}

// Why async void here?
// - Event handler signature requires void return
// - UI remains responsive during await
// - Exceptions caught locally (critical!)
```

### 4. Process Management

**Whisper.exe subprocess management**:

```csharp
// PersistentWhisperService.cs - Proper process handling
public async Task<string> TranscribeAsync(string audioPath)
{
    Process? process = null;
    try
    {
        process = new Process
        {
            StartInfo = new ProcessStartInfo
            {
                FileName = "whisper.exe",
                Arguments = $"-m {modelPath} -f {audioPath}",
                RedirectStandardOutput = true,
                UseShellExecute = false,
                CreateNoWindow = true
            }
        };

        process.Start();

        // Calculate timeout (3x audio length)
        var timeout = (int)(audioLength * 3000);

        if (!process.WaitForExit(timeout))
        {
            // Timeout - kill process
            process.Kill();
            throw new TimeoutException($"Whisper timeout after {timeout}ms");
        }

        return await process.StandardOutput.ReadToEndAsync();
    }
    finally
    {
        // ALWAYS dispose process
        process?.Dispose();
    }
}
```

## NuGet Package Recommendations

VoiceLite's tech stack and recommended versions:

| Package | Version | Use Case | Notes |
|---------|---------|----------|-------|
| **NAudio** | 2.2.1 | Audio recording | Use WaveInEvent for recording |
| **H.InputSimulator** | 1.2.1 | Text injection | Keyboard & clipboard simulation |
| **Hardcodet.NotifyIcon.Wpf** | 2.0.1 | System tray icon | WPF-compatible tray support |
| **System.Text.Json** | 9.0.9 | Settings serialization | Prefer over Newtonsoft.Json |
| **System.Management** | 8.0.0 | System info | Used for version checking |
| **Moq** | 4.20+ | Unit testing | Mock dependencies in tests |
| **FluentAssertions** | 6.12+ | Test assertions | Readable test assertions |
| **xUnit** | 2.6+ | Test framework | VoiceLite test framework |

**Avoid**:
- ❌ Newtonsoft.Json (use System.Text.Json for .NET 8.0)
- ❌ Old NAudio versions (ensure 2.2.1+ for stability)

## Common .NET 8.0 Issues & Solutions

### Issue: System.Text.Json Doesn't Serialize Property

**Symptom**: Property missing from JSON output

**Fix**: Ensure property is public with getter/setter:

```csharp
// ❌ WRONG: Private or missing setter
private string Model { get; set; }
public string Model { get; }

// ✅ CORRECT: Public with both getter and setter
public string Model { get; set; }

// Alternative: Use JsonPropertyName attribute
[JsonPropertyName("model")]
public string Model { get; init; } // init-only is OK
```

### Issue: WPF Dispatcher Throws on Test Thread

**Symptom**: `System.InvalidOperationException: The calling thread must be STA`

**Fix**: Mock Dispatcher in tests or use SynchronizationContext:

```csharp
// In tests: Mock Application.Current
var mockApp = new Mock<Application>();
// ... setup mock dispatcher

// Or: Use SynchronizationContext
SynchronizationContext.SetSynchronizationContext(
    new SynchronizationContext()
);
```

### Issue: Memory Leak with Event Handlers

**Symptom**: Objects not garbage collected, memory grows

**Fix**: Always unsubscribe in Dispose():

```csharp
public class AudioRecorder : IDisposable
{
    public AudioRecorder()
    {
        _waveIn.DataAvailable += OnDataAvailable;
    }

    public void Dispose()
    {
        // CRITICAL: Unsubscribe events
        _waveIn.DataAvailable -= OnDataAvailable;
        _waveIn?.Dispose();
    }
}
```

### Issue: Async Deadlock in WPF

**Symptom**: UI freezes on `await` call

**Fix**: Use `ConfigureAwait(false)` for non-UI code:

```csharp
// In service layer (non-UI)
public async Task<string> TranscribeAsync(string path)
{
    var result = await ProcessAudioAsync(path)
        .ConfigureAwait(false); // Don't capture UI context

    return result;
}

// In UI layer (keep UI context)
private async void OnButtonClick(object sender, RoutedEventArgs e)
{
    var result = await _service.TranscribeAsync(path);
    // No ConfigureAwait here - we NEED UI context for updates
    ResultLabel.Text = result;
}
```

## WPF-Specific Patterns

### XAML Data Binding

```xml
<!-- ModernStyles.xaml pattern -->
<Style x:Key="ModernButton" TargetType="Button">
    <Setter Property="Background" Value="#2D2D30"/>
    <Setter Property="Foreground" Value="White"/>
    <Setter Property="BorderBrush" Value="#3E3E42"/>
    <Setter Property="Padding" Value="10,5"/>
</Style>

<!-- Usage in MainWindow.xaml -->
<Button Style="{StaticResource ModernButton}"
        Click="OnRecordClick"
        Content="Record"/>
```

### Value Converters

```csharp
// Converters/RelativeTimeConverter.cs
public class RelativeTimeConverter : IValueConverter
{
    public object Convert(object value, Type targetType,
                         object parameter, CultureInfo culture)
    {
        if (value is DateTime dt)
        {
            var diff = DateTime.Now - dt;
            if (diff.TotalMinutes < 1) return "Just now";
            if (diff.TotalHours < 1) return $"{(int)diff.TotalMinutes} mins ago";
            if (diff.TotalDays < 1) return $"{(int)diff.TotalHours} hours ago";
            return $"{(int)diff.TotalDays} days ago";
        }
        return value;
    }

    public object ConvertBack(object value, Type targetType,
                             object parameter, CultureInfo culture)
    {
        throw new NotImplementedException();
    }
}
```

## .NET 8.0 Performance Tips

### 1. Use Span<T> for Buffer Operations

```csharp
// ✅ GOOD: Use Span<byte> for audio buffers
public void ProcessAudioBuffer(Span<byte> buffer)
{
    // No allocations, stack-based
    for (int i = 0; i < buffer.Length; i++)
    {
        buffer[i] = 0; // Process in-place
    }
}

// ❌ BAD: Array allocation every time
public void ProcessAudioBuffer(byte[] buffer)
{
    var temp = new byte[buffer.Length]; // Heap allocation!
}
```

### 2. String Interpolation for Performance

```csharp
// ✅ GOOD: String interpolation (compiled to string.Format)
var msg = $"Transcribed {count} files in {elapsed}ms";

// ❌ BAD: String concatenation (multiple allocations)
var msg = "Transcribed " + count + " files in " + elapsed + "ms";
```

### 3. Nullable Reference Types

```csharp
// Enable in .csproj
<Nullable>enable</Nullable>

// Use in code
public class AudioRecorder
{
    private WaveInEvent? _waveIn; // Nullable
    private string _model = ""; // Non-nullable, initialized

    public string Model => _model; // Non-nullable guarantee
}
```

## Testing Patterns

### Unit Test Example

```csharp
// VoiceLite.Tests/Services/WhisperServiceTests.cs
public class WhisperServiceTests
{
    [Fact]
    public async Task TranscribeAsync_ValidAudio_ReturnsText()
    {
        // Arrange
        var service = new PersistentWhisperService();
        var testAudio = "test_5s.wav";

        // Act
        var result = await service.TranscribeAsync(testAudio);

        // Assert
        result.Should().NotBeNullOrEmpty();
        result.Length.Should().BeGreaterThan(0);
    }

    [Fact]
    public void Dispose_Called_DisposesResources()
    {
        // Arrange
        var recorder = new AudioRecorder();

        // Act
        recorder.Dispose();

        // Assert
        // Verify no exceptions thrown
        // Check memory released (advanced)
    }
}
```

## Compiler Error Quick Reference

| Error Code | Meaning | Common Fix |
|------------|---------|------------|
| CS0103 | Name does not exist | Add `using` statement or fix typo |
| CS0161 | Not all code paths return | Add `return` statement |
| CS1061 | No definition for method | Check method name, add reference |
| CS8602 | Null reference warning | Add null check or `!` operator |
| CS8618 | Non-nullable field not initialized | Initialize in constructor or use `= null!` |

## Resources

- **Official Docs**: https://learn.microsoft.com/en-us/dotnet/
- **WPF Docs**: https://learn.microsoft.com/en-us/dotnet/desktop/wpf/
- **NAudio Docs**: https://github.com/naudio/NAudio
- **FluentAssertions**: https://fluentassertions.com/
