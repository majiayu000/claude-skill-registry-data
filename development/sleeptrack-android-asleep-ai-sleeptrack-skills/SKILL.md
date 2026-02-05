---
name: sleeptrack-android
description: This skill helps Android developers integrate the Asleep SDK for sleep tracking functionality. Use this skill when developers ask about Android implementation, MVVM architecture patterns, permission handling, Jetpack Compose UI, Kotlin coroutines integration, or Android-specific sleep tracking features. This skill provides working code examples from the official sample app.
---

# Sleeptrack Android

## Overview

This skill provides comprehensive guidance for integrating the Asleep sleep tracking SDK into Android applications. It covers Android-specific implementation details including MVVM architecture, permission handling, state management, UI patterns, and lifecycle management.

Use this skill when developers need to:
- Set up Asleep SDK in Android projects
- Implement sleep tracking with proper Android architecture
- Handle Android-specific permissions (microphone, notifications, battery optimization)
- Manage tracking lifecycle with state machines
- Build UI with ViewBinding or Jetpack Compose
- Handle errors and edge cases in Android environment
- Implement foreground services for background tracking

**Prerequisites**: Review the `sleeptrack-foundation` skill first for core concepts including session lifecycle, error codes, and API fundamentals.

## Quick Start

### 1. Add Dependencies

Add to your app-level `build.gradle`:

```gradle
dependencies {
    // Core dependencies
    implementation 'androidx.core:core-ktx:1.12.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'androidx.lifecycle:lifecycle-service:2.7.0'

    // Required for Asleep SDK
    implementation 'com.squareup.okhttp3:okhttp:4.11.0'
    implementation 'com.google.code.gson:gson:2.10'
    implementation 'ai.asleep:asleepsdk:3.1.4'

    // Optional: Hilt for DI
    implementation "com.google.dagger:hilt-android:2.48"
    kapt "com.google.dagger:hilt-compiler:2.48"
}
```

**Minimum Requirements**:
- minSdk: 24 (Android 7.0)
- targetSdk: 34
- Java: 17
- Kotlin: 1.9.24+

See `references/gradle_setup.md` for complete Gradle configuration.

### 2. Configure Permissions

Add to `AndroidManifest.xml`:

```xml
<manifest>
    <!-- Essential permissions -->
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.RECORD_AUDIO" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE_MICROPHONE" />

    <!-- Battery optimization -->
    <uses-permission android:name="android.permission.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS" />

    <!-- Notifications (Android 13+) -->
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
</manifest>
```

### 3. Initialize SDK

```kotlin
Asleep.initAsleepConfig(
    context = applicationContext,
    apiKey = "your_api_key_here",
    userId = "unique_user_id",
    baseUrl = "https://api.asleep.ai",
    callbackUrl = null, // Optional webhook URL
    service = "YourAppName",
    asleepConfigListener = object : Asleep.AsleepConfigListener {
        override fun onSuccess(userId: String?, asleepConfig: AsleepConfig?) {
            // SDK initialized successfully
        }

        override fun onFail(errorCode: Int, detail: String) {
            Log.e("Asleep", "Init failed: $errorCode - $detail")
        }
    }
)
```

### 4. Start Sleep Tracking

```kotlin
Asleep.beginSleepTracking(
    asleepConfig = asleepConfig,
    asleepTrackingListener = object : Asleep.AsleepTrackingListener {
        override fun onStart(sessionId: String) {
            // Tracking started successfully
        }

        override fun onPerform(sequence: Int) {
            // Called every ~30 seconds (1 sequence)
        }

        override fun onFinish(sessionId: String?) {
            // Tracking completed
        }

        override fun onFail(errorCode: Int, detail: String) {
            // Handle tracking errors
        }
    },
    notificationTitle = "Sleep Tracking Active",
    notificationText = "Tap to return to app",
    notificationIcon = R.drawable.ic_notification,
    notificationClass = MainActivity::class.java
)
```

### 5. Stop Tracking

```kotlin
Asleep.endSleepTracking()
```

## Android Architecture Pattern (MVVM + Hilt)

The recommended architecture follows Android best practices with MVVM pattern, Hilt dependency injection, and proper state management.

### State Management

Define tracking states using sealed classes:

```kotlin
sealed class AsleepState {
    data object STATE_IDLE: AsleepState()
    data object STATE_INITIALIZING : AsleepState()
    data object STATE_INITIALIZED : AsleepState()
    data object STATE_TRACKING_STARTING : AsleepState()
    data object STATE_TRACKING_STARTED : AsleepState()
    data object STATE_TRACKING_STOPPING : AsleepState()
    data class STATE_ERROR(val errorCode: AsleepError) : AsleepState()
}

data class AsleepError(val code: Int, val message: String)
```

### Basic ViewModel Pattern

```kotlin
@HiltViewModel
class SleepTrackingViewModel @Inject constructor(
    @ApplicationContext private val app: Application
) : ViewModel() {

    private val _trackingState = MutableStateFlow<AsleepState>(AsleepState.STATE_IDLE)
    val trackingState: StateFlow<AsleepState> = _trackingState

    private var config: AsleepConfig? = null

    fun initializeSDK(userId: String) {
        Asleep.initAsleepConfig(
            context = app,
            apiKey = BuildConfig.ASLEEP_API_KEY,
            userId = userId,
            baseUrl = "https://api.asleep.ai",
            callbackUrl = null,
            service = "MyApp",
            asleepConfigListener = object : Asleep.AsleepConfigListener {
                override fun onSuccess(userId: String?, asleepConfig: AsleepConfig?) {
                    config = asleepConfig
                    _trackingState.value = AsleepState.STATE_INITIALIZED
                }
                override fun onFail(errorCode: Int, detail: String) {
                    _trackingState.value = AsleepState.STATE_ERROR(AsleepError(errorCode, detail))
                }
            }
        )
    }

    fun startTracking() {
        config?.let {
            Asleep.beginSleepTracking(
                asleepConfig = it,
                asleepTrackingListener = trackingListener,
                notificationTitle = "Sleep Tracking",
                notificationText = "Active",
                notificationIcon = R.drawable.ic_notification,
                notificationClass = MainActivity::class.java
            )
        }
    }

    fun stopTracking() {
        Asleep.endSleepTracking()
    }
}
```

**For complete production-ready ViewModel with real-time data, error handling, and lifecycle management**, see `references/complete_viewmodel_implementation.md`.

### Basic Activity Pattern

```kotlin
@AndroidEntryPoint
class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private val viewModel: SleepTrackingViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        // Setup button
        binding.btnTrack.setOnClickListener {
            when (viewModel.trackingState.value) {
                AsleepState.STATE_INITIALIZED -> viewModel.startTracking()
                AsleepState.STATE_TRACKING_STARTED -> viewModel.stopTracking()
                else -> {}
            }
        }

        // Observe state
        lifecycleScope.launch {
            viewModel.trackingState.collect { state ->
                updateUI(state)
            }
        }
    }
}
```

**For complete Activity implementation with permission handling**, see `references/complete_viewmodel_implementation.md`.

## Permission Handling

Android requires multiple runtime permissions for sleep tracking:

### Required Permissions

1. **RECORD_AUDIO**: Microphone access for sleep sound recording
2. **POST_NOTIFICATIONS**: Android 13+ notification permission
3. **Battery Optimization**: Prevent app from being killed during tracking

### Permission Request Flow

```kotlin
// Request permissions sequentially
when {
    !hasMicrophonePermission() -> requestMicrophone()
    !hasNotificationPermission() -> requestNotification()
    !isBatteryOptimizationIgnored() -> requestBatteryOptimization()
    else -> allPermissionsGranted()
}
```

### Best Practices

1. **Request in sequence**: Request one permission at a time for better UX
2. **Show rationale**: Explain why each permission is needed before requesting
3. **Handle denial**: Provide fallback or guide users to settings
4. **Check on resume**: Re-check permissions when app resumes

```kotlin
override fun onResume() {
    super.onResume()
    if (!hasRequiredPermissions() && Asleep.isSleepTrackingAlive(applicationContext)) {
        handlePermissionLoss()
    }
}
```

**For complete PermissionManager implementation**, see `references/complete_viewmodel_implementation.md`.

## Error Handling

Distinguish between critical errors and warnings:

### Error Classification

```kotlin
fun isWarning(errorCode: Int): Boolean {
    return errorCode in setOf(
        AsleepErrorCode.ERR_AUDIO_SILENCED,
        AsleepErrorCode.ERR_UPLOAD_FAILED
    )
}

fun handleError(error: AsleepError) {
    if (isWarning(error.code)) {
        // Show warning, continue tracking
        Toast.makeText(context, getUserFriendlyMessage(error), Toast.LENGTH_SHORT).show()
    } else {
        // Critical error - stop tracking
        stopTracking()
        showErrorDialog(getUserFriendlyMessage(error))
    }
}
```

## UI Patterns

### ViewBinding Example

```kotlin
class TrackingFragment : Fragment() {
    private var _binding: FragmentTrackingBinding? = null
    private val binding get() = _binding!!
    private val viewModel: SleepTrackingViewModel by viewModels()

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        viewLifecycleOwner.lifecycleScope.launch {
            viewModel.trackingState.collect { state ->
                when (state) {
                    AsleepState.STATE_TRACKING_STARTED -> {
                        binding.btnTrack.text = "Stop Tracking"
                    }
                    AsleepState.STATE_INITIALIZED -> {
                        binding.btnTrack.text = "Start Tracking"
                    }
                    else -> {}
                }
            }
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
```

### Jetpack Compose Example

```kotlin
@Composable
fun SleepTrackingScreen(
    viewModel: SleepTrackingViewModel = hiltViewModel()
) {
    val trackingState by viewModel.trackingState.collectAsState()

    Column(
        modifier = Modifier.fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        when (trackingState) {
            AsleepState.STATE_TRACKING_STARTED -> {
                Button(onClick = { viewModel.stopTracking() }) {
                    Text("Stop Tracking")
                }
            }
            AsleepState.STATE_INITIALIZED -> {
                Button(onClick = { viewModel.startTracking() }) {
                    Text("Start Sleep Tracking")
                }
            }
            is AsleepState.STATE_ERROR -> {
                ErrorDisplay(error = (trackingState as AsleepState.STATE_ERROR).errorCode)
            }
            else -> {
                CircularProgressIndicator()
            }
        }
    }
}
```

**For complete UI implementations with Material3 components**, see `references/ui_implementation_guide.md`.

## Lifecycle Management

### Handle App Lifecycle Events

```kotlin
@AndroidEntryPoint
class MainActivity : AppCompatActivity() {

    override fun onStart() {
        super.onStart()
        // Reconnect to existing tracking session
        if (Asleep.isSleepTrackingAlive(applicationContext)) {
            viewModel.reconnectToTracking()
        }
    }

    override fun onStop() {
        super.onStop()
        // Tracking continues in background via foreground service
        // No action needed
    }

    override fun onDestroy() {
        super.onDestroy()
        // Do NOT call endSleepTracking() here
        // Service continues in background
    }
}
```

### Foreground Service

The Asleep SDK automatically manages a foreground service during tracking. The notification keeps the service alive:

```kotlin
Asleep.beginSleepTracking(
    asleepConfig = config,
    asleepTrackingListener = listener,
    notificationTitle = "Sleep Tracking Active",
    notificationText = "Tracking your sleep patterns",
    notificationIcon = R.drawable.ic_sleep,
    notificationClass = MainActivity::class.java  // Tapping notification opens this
)
```

The service will:
- Keep the app alive during sleep tracking
- Show persistent notification
- Maintain microphone access
- Continue even if user swipes away the app

## Real-Time Sleep Data

Access preliminary sleep data during tracking:

```kotlin
// In ViewModel
override fun onPerform(sequence: Int) {
    // Check after sequence 10, then every 10 sequences
    if (sequence > 10 && sequence % 10 == 0) {
        getCurrentSleepData()
    }
}

private fun getCurrentSleepData() {
    Asleep.getCurrentSleepData(
        asleepSleepDataListener = object : Asleep.AsleepSleepDataListener {
            override fun onSleepDataReceived(session: Session) {
                val currentSleepStage = session.sleepStages?.lastOrNull()
                val currentSnoringStage = session.snoringStages?.lastOrNull()

                Log.d("Sleep", "Current stage: $currentSleepStage")
            }

            override fun onFail(errorCode: Int, detail: String) {
                Log.e("Sleep", "Failed to get current data: $errorCode")
            }
        }
    )
}
```

**Note**: Real-time data is preliminary and may differ from final report after processing.

## Testing

### Unit Testing
```kotlin
class SleepTrackingViewModelTest {
    @get:Rule val mainDispatcherRule = MainDispatcherRule()

    @Test
    fun `startTracking should fail if not initialized`() = runTest {
        viewModel.startTracking()
        assertNotEquals(AsleepState.STATE_TRACKING_STARTED, viewModel.trackingState.value)
    }
}
```

### Integration Testing
```kotlin
@Test
fun trackingFlow_complete() {
    onView(withId(R.id.btn_start_stop)).perform(click())
    onView(withId(R.id.tracking_indicator)).check(matches(isDisplayed()))
}
```

**For complete testing guide with Compose UI tests and test utilities**, see `references/testing_guide.md`.

## Common Issues & Solutions

### Tracking stops unexpectedly
**Causes**: Battery optimization, notification dismissed, permission revoked, microphone conflict

**Solution**: Check battery optimization and permissions on resume:
```kotlin
override fun onResume() {
    super.onResume()
    if (!hasRequiredPermissions() && Asleep.isSleepTrackingAlive(applicationContext)) {
        handlePermissionLoss()
    }
}
```

### No real-time data available
**Cause**: Checking before sequence 10

**Solution**: Only call `getCurrentSleepData()` after sequence 10

### ERR_UPLOAD_FORBIDDEN error
**Cause**: Same user_id tracking on multiple devices

**Solution**: Use unique user IDs per device or check for active sessions before starting

## Resources

This skill includes detailed reference documentation:

- `references/complete_viewmodel_implementation.md`: Complete ViewModel, Activity, and PermissionManager implementations
- `references/ui_implementation_guide.md`: Complete ViewBinding and Jetpack Compose UI examples
- `references/testing_guide.md`: Comprehensive unit, integration, and UI testing guides
- `references/android_architecture_patterns.md`: Complete architecture examples from the official sample app
- `references/gradle_setup.md`: Comprehensive Gradle configuration including dependencies and ProGuard rules

### Official Documentation

- **Android Getting Started**: https://docs-en.asleep.ai/docs/android-get-started.md
- **AsleepConfig Reference**: https://docs-en.asleep.ai/docs/android-asleep-config.md
- **SleepTrackingManager**: https://docs-en.asleep.ai/docs/android-sleep-tracking-manager.md
- **Error Codes**: https://docs-en.asleep.ai/docs/android-error-codes.md

### Android Resources

- **Android Permissions**: https://developer.android.com/guide/topics/permissions/overview
- **Foreground Services**: https://developer.android.com/develop/background-work/services/foreground-services
- **StateFlow Guide**: https://developer.android.com/kotlin/flow/stateflow-and-sharedflow
- **Hilt Documentation**: https://developer.android.com/training/dependency-injection/hilt-android

## Next Steps

After implementing Android sleep tracking:

1. **Test thoroughly**: Test on different Android versions (especially 13+ for notifications)
2. **Handle edge cases**: Low battery, airplane mode, app updates during tracking
3. **Fetch reports**: Use REST API or backend integration to retrieve sleep reports
4. **Build UI**: Create compelling visualizations of sleep data
5. **Analytics**: Track user engagement and sleep patterns

For backend report fetching and webhook integration, use the `sleeptrack-be` skill.
