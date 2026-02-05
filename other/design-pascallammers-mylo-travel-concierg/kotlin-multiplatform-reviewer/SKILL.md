---
name: kotlin-multiplatform-reviewer
description: |
  WHEN: Kotlin Multiplatform (KMP) project review, expect/actual patterns, shared module structure, iOS interop
  WHAT: Module structure analysis + expect/actual validation + platform separation + iOS/Android interop + dependency management
  WHEN NOT: Android UI → kotlin-android-reviewer, Server → kotlin-spring-reviewer
---

# Kotlin Multiplatform Reviewer Skill

## Purpose
Reviews Kotlin Multiplatform (KMP) project structure and patterns including shared code design, expect/actual mechanism, and iOS interop.

## When to Use
- KMP project code review
- "expect/actual", "shared module", "commonMain", "multiplatform" mentions
- iOS/Android code sharing design review
- Projects with `kotlin("multiplatform")` plugin

## Project Detection
- `kotlin("multiplatform")` plugin in `build.gradle.kts`
- `src/commonMain`, `src/androidMain`, `src/iosMain` directories
- `shared` or `common` module exists

## Workflow

### Step 1: Analyze Structure
```
**Kotlin**: 2.0.x
**Targets**: Android, iOS (arm64, simulatorArm64)
**Shared Module**: shared
**Source Sets**:
  - commonMain (shared code)
  - androidMain (Android specific)
  - iosMain (iOS specific)
```

### Step 2: Select Review Areas
**AskUserQuestion:**
```
"Which areas to review?"
Options:
- Full KMP pattern check (recommended)
- Module structure/dependencies
- expect/actual implementation
- Platform code separation
- iOS interop (Swift/ObjC)
multiSelect: true
```

## Detection Rules

### Module Structure
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Bloated shared module | Split by layer | MEDIUM |
| Circular dependencies | Unidirectional deps | HIGH |
| Platform code in commonMain | Move to androidMain/iosMain | HIGH |
| Missing test module | Add commonTest | MEDIUM |

**Recommended Structure:**
```
project/
├── shared/
│   └── src/
│       ├── commonMain/kotlin/    # Shared business logic
│       ├── commonTest/kotlin/    # Shared tests
│       ├── androidMain/kotlin/   # Android specific
│       ├── iosMain/kotlin/       # iOS specific
│       └── iosTest/kotlin/
├── androidApp/                    # Android app
└── iosApp/                       # iOS app (Xcode)
```

### expect/actual Patterns
| Check | Recommendation | Severity |
|-------|----------------|----------|
| actual without expect | expect declaration required | CRITICAL |
| Missing actual impl | Provide actual for all targets | CRITICAL |
| Excessive expect/actual | Consider interface + DI | MEDIUM |
| Direct platform API in actual | Add abstraction layer | MEDIUM |

```kotlin
// commonMain - expect declaration
expect class Platform() {
    val name: String
    fun getDeviceId(): String
}

// androidMain - actual implementation
actual class Platform actual constructor() {
    actual val name: String = "Android ${Build.VERSION.SDK_INT}"
    actual fun getDeviceId(): String = Settings.Secure.getString(
        context.contentResolver,
        Settings.Secure.ANDROID_ID
    )
}

// iosMain - actual implementation
actual class Platform actual constructor() {
    actual val name: String = UIDevice.currentDevice.systemName()
    actual fun getDeviceId(): String = UIDevice.currentDevice
        .identifierForVendor?.UUIDString ?: ""
}
```

**BAD: expect/actual overuse**
```kotlin
// BAD: expect/actual for simple values
expect val platformName: String
actual val platformName: String = "Android"

// GOOD: interface + DI
interface PlatformInfo {
    val name: String
}

// androidMain
class AndroidPlatformInfo : PlatformInfo {
    override val name = "Android"
}
```

### Platform Separation
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Platform import in commonMain | Move to platform source set | CRITICAL |
| Java class in commonMain | expect/actual or pure Kotlin | HIGH |
| UIKit/Android SDK in common | Separate to platform source set | CRITICAL |

```kotlin
// BAD: Android import in commonMain
// commonMain/kotlin/Repository.kt
import android.content.Context  // Compile error!

// GOOD: expect/actual separation
// commonMain
expect class DataStore {
    fun save(key: String, value: String)
    fun get(key: String): String?
}

// androidMain
actual class DataStore(private val context: Context) {
    private val prefs = context.getSharedPreferences("app", Context.MODE_PRIVATE)
    actual fun save(key: String, value: String) {
        prefs.edit().putString(key, value).apply()
    }
    actual fun get(key: String): String? = prefs.getString(key, null)
}

// iosMain
actual class DataStore {
    actual fun save(key: String, value: String) {
        NSUserDefaults.standardUserDefaults.setObject(value, key)
    }
    actual fun get(key: String): String? =
        NSUserDefaults.standardUserDefaults.stringForKey(key)
}
```

### iOS Interop
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Missing @ObjCName | Swift-friendly naming | LOW |
| Sealed class iOS exposure | Use enum or @ObjCName | MEDIUM |
| Direct Flow exposure to iOS | Provide wrapper function | HIGH |
| suspend function iOS call | Provide completion handler wrapper | HIGH |

```kotlin
// BAD: Direct suspend function exposure
class Repository {
    suspend fun fetchData(): Data  // Hard to call from iOS
}

// GOOD: iOS wrapper provided
class Repository {
    suspend fun fetchData(): Data

    // iOS completion handler wrapper
    fun fetchDataAsync(completion: (Data?, Error?) -> Unit) {
        MainScope().launch {
            try {
                val data = fetchData()
                completion(data, null)
            } catch (e: Exception) {
                completion(null, e)
            }
        }
    }
}
```

**Flow iOS Exposure:**
```kotlin
// BAD: Direct Flow exposure
val dataFlow: Flow<Data>

// GOOD: iOS wrapper
fun observeData(onEach: (Data) -> Unit): Closeable {
    val job = MainScope().launch {
        dataFlow.collect { onEach(it) }
    }
    return object : Closeable {
        override fun close() { job.cancel() }
    }
}
```

### Dependency Management
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Platform library in commonMain | Use multiplatform library | HIGH |
| Version mismatch | Use Version Catalog | MEDIUM |
| Unused dependencies | Remove unused | LOW |

**Multiplatform Library Recommendations:**
| Purpose | Library |
|---------|---------|
| HTTP | Ktor Client |
| Serialization | Kotlinx Serialization |
| Async | Kotlinx Coroutines |
| DI | Koin, Kodein |
| Date/Time | Kotlinx Datetime |
| Settings | Multiplatform Settings |
| Logging | Napier, Kermit |
| DB | SQLDelight |

## Response Template
```
## KMP Project Review Results

**Project**: [name]
**Kotlin**: 2.0.x
**Targets**: Android, iOS (arm64, simulatorArm64)

### Module Structure
| Status | Item | Issue |
|--------|------|-------|
| OK | Source set separation | commonMain/androidMain/iosMain correct |
| MEDIUM | Tests | Add commonTest recommended |

### expect/actual
| Status | File | Issue |
|--------|------|-------|
| OK | Platform.kt | expect/actual correctly implemented |
| HIGH | DataStore.kt | Missing iosMain actual implementation |

### iOS Interop
| Status | Item | Issue |
|--------|------|-------|
| HIGH | Repository.kt | suspend function needs iOS wrapper |
| MEDIUM | UiState.kt | Add @ObjCName to sealed class |

### Recommended Actions
1. [ ] Add DataStore iosMain actual implementation
2. [ ] Add completion handler wrapper to fetchData()
3. [ ] Add commonTest source set
```

## Best Practices
1. **Share Scope**: Business logic > Data layer > UI (optional)
2. **expect/actual**: Minimize usage, prefer interface + DI
3. **iOS Interop**: Use SKIE library or manual wrappers
4. **Testing**: Test shared logic in commonTest
5. **Dependencies**: Prefer multiplatform libraries

## Integration
- `kotlin-android-reviewer` skill: Android specific code
- `kotlin-spring-reviewer` skill: Server shared code
- `code-reviewer` skill: General code quality

## Notes
- Based on Kotlin 2.0+
- KMP 1.9.20+ recommended (Stable)
- Compose Multiplatform requires separate review
