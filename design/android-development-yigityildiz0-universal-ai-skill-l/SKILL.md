---
name: android-development
description: Android native development expertise with Kotlin, Jetpack Compose, Material Design 3, and modern Android architecture. Use when building Android.
---

# Android Development

Structured guidance for building modern Android applications with Kotlin, Jetpack Compose, Material Design 3, and current Android architecture patterns. Covers project structure, Compose UI development, theming, navigation, architecture, data layer, lifecycle management, and testing strategies specific to production Android applications.

## When to Use This Skill

Use this skill for:

- Setting up a new Android project with multi-module Gradle configuration and version catalogs
- Building UI screens with Jetpack Compose, state hoisting, and recomposition optimization
- Implementing Material Design 3 theming with dynamic color, custom color schemes, and dark theme support
- Setting up Compose Navigation with type-safe routes, nested graphs, and deep links
- Designing MVVM or MVI architecture with ViewModel, UiState, Repository pattern, and Hilt DI
- Implementing the data layer with Room, DataStore, Retrofit or Ktor, and Paging 3
- Handling Android lifecycle, coroutine scoping, side effects, and background work with WorkManager
- Writing unit tests, Compose UI tests, and integration tests for Android components

**Trigger phrases**: "android app", "kotlin android", "jetpack compose", "compose ui", "material design", "material you", "viewmodel", "android navigation", "room database", "hilt", "gradle version catalog", "android testing", "compose preview", "mvvm", "mvi", "datastore", "paging 3", "workmanager", "compose state", "recomposition"

## What This Skill Does

Provides Android development patterns including:

- **Project Structure**: Multi-module Gradle setup, version catalogs, build conventions, ProGuard/R8 configuration
- **Jetpack Compose**: Composable functions, state management, Modifier chains, previews, recomposition optimization
- **Material Design 3**: Dynamic color, custom themes, typography, shapes, dark theme, Material You adaptation
- **Navigation**: Compose Navigation with type-safe routes, nested graphs, bottom navigation, deep links
- **Architecture**: MVVM with ViewModel and UiState, Repository pattern, UseCases, Hilt dependency injection
- **Data Layer**: Room database, DataStore preferences, Retrofit/Ktor networking, offline-first caching, Paging 3
- **Lifecycle**: LaunchedEffect, DisposableEffect, lifecycle-aware Flow collection, WorkManager, foreground services
- **Testing**: JUnit 5 unit tests, Compose testing with ComposeTestRule, Robolectric, Hilt testing, UI automation

## Instructions

### Step 1: Project Structure and Gradle Configuration

A well-organized Android project uses multi-module architecture, version catalogs for dependency management, and convention plugins to keep build files DRY.

**Recommended Module Structure**:

```
my-app/
├── app/                          # Application module (wiring, DI, navigation)
│   ├── build.gradle.kts
│   └── src/main/
│       ├── AndroidManifest.xml
│       └── kotlin/com/example/myapp/
│           ├── MyApplication.kt
│           ├── MainActivity.kt
│           └── navigation/
│               └── AppNavGraph.kt
├── core/
│   ├── common/                   # Shared utilities, extension functions
│   ├── data/                     # Repository implementations, data sources
│   ├── database/                 # Room database, DAOs, entities
│   ├── datastore/                # DataStore preferences
│   ├── domain/                   # Use cases, domain models, repository interfaces
│   ├── model/                    # Shared data models
│   ├── network/                  # Retrofit/Ktor service definitions, DTOs
│   └── ui/                       # Shared Compose components, theme
├── feature/
│   ├── home/                     # Home screen feature module
│   ├── profile/                  # Profile feature module
│   └── settings/                 # Settings feature module
├── build-logic/                  # Convention plugins
│   └── convention/
│       └── src/main/kotlin/
│           ├── AndroidApplicationConventionPlugin.kt
│           ├── AndroidLibraryConventionPlugin.kt
│           └── AndroidComposeConventionPlugin.kt
├── gradle/
│   └── libs.versions.toml        # Version catalog
├── build.gradle.kts              # Root build file
├── settings.gradle.kts
└── gradle.properties
```

**Version Catalog** (`gradle/libs.versions.toml`):

```toml
[versions]
agp = "8.7.3"
kotlin = "2.1.0"
ksp = "2.1.0-1.0.29"
compose-bom = "2024.12.01"
compose-compiler = "1.5.15"
hilt = "2.53.1"
room = "2.6.1"
lifecycle = "2.8.7"
navigation = "2.8.5"
retrofit = "2.11.0"
okhttp = "4.12.0"
coroutines = "1.9.0"
paging = "3.3.5"
datastore = "1.1.1"
work = "2.10.0"
junit5 = "5.11.4"
truth = "1.4.4"
turbine = "1.2.0"
robolectric = "4.14.1"

[libraries]
# Compose BOM aligns all Compose library versions
compose-bom = { group = "androidx.compose", name = "compose-bom", version.ref = "compose-bom" }
compose-ui = { group = "androidx.compose.ui", name = "ui" }
compose-ui-graphics = { group = "androidx.compose.ui", name = "ui-graphics" }
compose-ui-tooling = { group = "androidx.compose.ui", name = "ui-tooling" }
compose-ui-tooling-preview = { group = "androidx.compose.ui", name = "ui-tooling-preview" }
compose-ui-test-manifest = { group = "androidx.compose.ui", name = "ui-test-manifest" }
compose-ui-test-junit4 = { group = "androidx.compose.ui", name = "ui-test-junit4" }
compose-material3 = { group = "androidx.compose.material3", name = "material3" }
compose-material-icons = { group = "androidx.compose.material", name = "material-icons-extended" }

# Architecture components
lifecycle-runtime-compose = { group = "androidx.lifecycle", name = "lifecycle-runtime-compose", version.ref = "lifecycle" }
lifecycle-viewmodel-compose = { group = "androidx.lifecycle", name = "lifecycle-viewmodel-compose", version.ref = "lifecycle" }
navigation-compose = { group = "androidx.navigation", name = "navigation-compose", version.ref = "navigation" }

# Hilt
hilt-android = { group = "com.google.dagger", name = "hilt-android", version.ref = "hilt" }
hilt-compiler = { group = "com.google.dagger", name = "hilt-android-compiler", version.ref = "hilt" }
hilt-navigation-compose = { group = "androidx.hilt", name = "hilt-navigation-compose", version = "1.2.0" }
hilt-testing = { group = "com.google.dagger", name = "hilt-android-testing", version.ref = "hilt" }

# Room
room-runtime = { group = "androidx.room", name = "room-runtime", version.ref = "room" }
room-compiler = { group = "androidx.room", name = "room-compiler", version.ref = "room" }
room-ktx = { group = "androidx.room", name = "room-ktx", version.ref = "room" }
room-paging = { group = "androidx.room", name = "room-paging", version.ref = "room" }
room-testing = { group = "androidx.room", name = "room-testing", version.ref = "room" }

# Networking
retrofit = { group = "com.squareup.retrofit2", name = "retrofit", version.ref = "retrofit" }
retrofit-converter-kotlinx = { group = "com.squareup.retrofit2", name = "converter-kotlinx-serialization", version.ref = "retrofit" }
okhttp-logging = { group = "com.squareup.okhttp3", name = "logging-interceptor", version.ref = "okhttp" }

# DataStore and Paging
datastore-preferences = { group = "androidx.datastore", name = "datastore-preferences", version.ref = "datastore" }
paging-runtime = { group = "androidx.paging", name = "paging-runtime", version.ref = "paging" }
paging-compose = { group = "androidx.paging", name = "paging-compose", version.ref = "paging" }

# WorkManager
work-runtime = { group = "androidx.work", name = "work-runtime-ktx", version.ref = "work" }
work-testing = { group = "androidx.work", name = "work-testing", version.ref = "work" }

# Testing
junit5-api = { group = "org.junit.jupiter", name = "junit-jupiter-api", version.ref = "junit5" }
junit5-engine = { group = "org.junit.jupiter", name = "junit-jupiter-engine", version.ref = "junit5" }
junit5-params = { group = "org.junit.jupiter", name = "junit-jupiter-params", version.ref = "junit5" }
truth = { group = "com.google.truth", name = "truth", version.ref = "truth" }
turbine = { group = "app.cash.turbine", name = "turbine", version.ref = "turbine" }
coroutines-test = { group = "org.jetbrains.kotlinx", name = "kotlinx-coroutines-test", version.ref = "coroutines" }
robolectric = { group = "org.robolectric", name = "robolectric", version.ref = "robolectric" }

[plugins]
android-application = { id = "com.android.application", version.ref = "agp" }
android-library = { id = "com.android.library", version.ref = "agp" }
kotlin-android = { id = "org.jetbrains.kotlin.android", version.ref = "kotlin" }
kotlin-compose = { id = "org.jetbrains.kotlin.plugin.compose", version.ref = "kotlin" }
kotlin-serialization = { id = "org.jetbrains.kotlin.plugin.serialization", version.ref = "kotlin" }
ksp = { id = "com.google.devtools.ksp", version.ref = "ksp" }
hilt = { id = "com.google.dagger.hilt.android", version.ref = "hilt" }
room = { id = "androidx.room", version.ref = "room" }
```

**Application Module** (`app/build.gradle.kts`):

```kotlin
plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.compose)
    alias(libs.plugins.kotlin.serialization)
    alias(libs.plugins.ksp)
    alias(libs.plugins.hilt)
}

android {
    namespace = "com.example.myapp"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.example.myapp"
        minSdk = 26
        targetSdk = 35
        versionCode = 1
        versionName = "1.0.0"

        testInstrumentationRunner = "com.example.myapp.testing.HiltTestRunner"
    }

    buildTypes {
        debug {
            isDebuggable = true
            applicationIdSuffix = ".debug"
            versionNameSuffix = "-debug"
        }
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro",
            )
            signingConfig = signingConfigs.getByName("release")
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
        freeCompilerArgs += listOf(
            "-opt-in=kotlinx.coroutines.ExperimentalCoroutinesApi",
            "-opt-in=androidx.compose.material3.ExperimentalMaterial3Api",
        )
    }

    buildFeatures {
        compose = true
        buildConfig = true
    }

    packaging {
        resources {
            excludes += "/META-INF/{AL2.0,LGPL2.1}"
        }
    }
}

dependencies {
    // Feature modules
    implementation(project(":feature:home"))
    implementation(project(":feature:profile"))
    implementation(project(":feature:settings"))

    // Core modules
    implementation(project(":core:common"))
    implementation(project(":core:data"))
    implementation(project(":core:domain"))
    implementation(project(":core:ui"))

    // Compose
    implementation(platform(libs.compose.bom))
    implementation(libs.compose.ui)
    implementation(libs.compose.ui.graphics)
    implementation(libs.compose.material3)
    implementation(libs.compose.ui.tooling.preview)
    debugImplementation(libs.compose.ui.tooling)
    debugImplementation(libs.compose.ui.test.manifest)

    // Architecture
    implementation(libs.lifecycle.runtime.compose)
    implementation(libs.lifecycle.viewmodel.compose)
    implementation(libs.navigation.compose)

    // Hilt
    implementation(libs.hilt.android)
    ksp(libs.hilt.compiler)
    implementation(libs.hilt.navigation.compose)

    // Testing
    testImplementation(libs.junit5.api)
    testRuntimeOnly(libs.junit5.engine)
    testImplementation(libs.truth)
    testImplementation(libs.coroutines.test)
    androidTestImplementation(platform(libs.compose.bom))
    androidTestImplementation(libs.compose.ui.test.junit4)
    androidTestImplementation(libs.hilt.testing)
    kspAndroidTest(libs.hilt.compiler)
}
```

**ProGuard/R8 Rules** (`app/proguard-rules.pro`):

```proguard
# Kotlin serialization
-keepattributes *Annotation*, InnerClasses
-dontnote kotlinx.serialization.AnnotationsKt
-keepclassmembers @kotlinx.serialization.Serializable class ** {
    *** Companion;
}
-keepclasseswithmembers class **$$serializer {
    *** INSTANCE;
}

# Retrofit
-keepattributes Signature, Exceptions
-keep,allowshrinking,allowoptimization interface * {
    @retrofit2.http.* <methods>;
}
-dontwarn javax.annotation.**
-dontwarn kotlin.Unit

# Room
-keep class * extends androidx.room.RoomDatabase
-keep @androidx.room.Entity class *
-dontwarn androidx.room.paging.**

# Hilt
-keep class dagger.hilt.** { *; }
-keep class javax.inject.** { *; }
-keep class * extends dagger.hilt.android.internal.managers.ViewComponentManager$FragmentContextWrapper { *; }
```

**Key Gradle Configuration Principles**:

- Use a version catalog (`libs.versions.toml`) as the single source of truth for all dependency versions across modules
- Apply the Compose BOM to align all Compose library versions automatically, avoiding version conflicts
- Enable R8 minification and resource shrinking in the release build type to reduce APK size
- Set `minSdk = 26` (Android 8.0) as a practical baseline that covers over 95% of active devices
- Use convention plugins in `build-logic/` to share common configuration across feature and core modules
- Always set an `applicationIdSuffix` on debug builds to allow side-by-side installation with release builds

### Step 2: Jetpack Compose Fundamentals

Jetpack Compose uses a declarative, function-based approach to UI. Understanding composable functions, state management, recomposition, and Modifier chains is essential for building performant Compose UIs.

**Composable Functions and State Hoisting**:

```kotlin
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

/**
 * Stateful wrapper that owns the search query state.
 * Use this pattern at the screen level, hoisting state up to the
 * nearest common ancestor that needs it.
 */
@Composable
fun SearchScreen(
    onNavigateToResult: (query: String) -> Unit,
    modifier: Modifier = Modifier,
) {
    // rememberSaveable survives configuration changes (rotation, process death)
    var query by rememberSaveable { mutableStateOf("") }
    var isSearching by rememberSaveable { mutableStateOf(false) }

    SearchContent(
        query = query,
        isSearching = isSearching,
        onQueryChange = { query = it },
        onSearch = {
            isSearching = true
            onNavigateToResult(query)
        },
        modifier = modifier,
    )
}

/**
 * Stateless composable that receives all state as parameters.
 * This pattern makes the component testable, previewable, and reusable.
 */
@Composable
fun SearchContent(
    query: String,
    isSearching: Boolean,
    onQueryChange: (String) -> Unit,
    onSearch: () -> Unit,
    modifier: Modifier = Modifier,
) {
    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
    ) {
        OutlinedTextField(
            value = query,
            onValueChange = onQueryChange,
            label = { Text("Search") },
            singleLine = true,
            modifier = Modifier.fillMaxWidth(),
        )

        Button(
            onClick = onSearch,
            enabled = query.isNotBlank() && !isSearching,
            modifier = Modifier.fillMaxWidth(),
        ) {
            if (isSearching) {
                CircularProgressIndicator(
                    modifier = Modifier.size(20.dp),
                    strokeWidth = 2.dp,
                )
                Spacer(modifier = Modifier.width(8.dp))
            }
            Text(if (isSearching) "Searching..." else "Search")
        }
    }
}
```

**Stable Types and Recomposition Optimization**:

```kotlin
import androidx.compose.runtime.Immutable
import androidx.compose.runtime.Stable

/**
 * Mark data classes as @Immutable when all properties are val and
 * use immutable types. This tells the Compose compiler the class
 * will never change after construction, enabling recomposition skipping.
 */
@Immutable
data class ArticleUiModel(
    val id: String,
    val title: String,
    val summary: String,
    val imageUrl: String?,
    val publishedAt: String,
    val isBookmarked: Boolean,
)

/**
 * Use @Stable for classes where the Compose compiler cannot infer stability
 * (e.g., classes with mutable internal state that is observed correctly).
 */
@Stable
class ArticleListState(
    val articles: List<ArticleUiModel>,
    val isLoading: Boolean,
    val errorMessage: String?,
) {
    companion object {
        val Empty = ArticleListState(
            articles = emptyList(),
            isLoading = false,
            errorMessage = null,
        )
    }
}

/**
 * Use derivedStateOf to avoid unnecessary recompositions when the derived
 * value has not actually changed, even if the source state has.
 */
@Composable
fun ArticleList(
    articles: List<ArticleUiModel>,
    modifier: Modifier = Modifier,
) {
    // Only recomposes when the count actually changes, not on every list update
    val bookmarkCount by remember(articles) {
        derivedStateOf { articles.count { it.isBookmarked } }
    }

    Column(modifier = modifier) {
        Text(
            text = "$bookmarkCount bookmarked",
            style = MaterialTheme.typography.labelMedium,
        )
        // Use key() to help Compose identify items across recompositions
        articles.forEach { article ->
            key(article.id) {
                ArticleCard(article = article)
            }
        }
    }
}
```

**Modifier Chain Best Practices**:

```kotlin
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.unit.dp

/**
 * Modifier order matters. Each modifier wraps the previous one.
 * Common pattern: size/padding -> shape/clip -> background -> content padding -> interaction.
 */
@Composable
fun ArticleCard(
    article: ArticleUiModel,
    onClick: () -> Unit = {},
    modifier: Modifier = Modifier,
) {
    Card(
        modifier = modifier
            // 1. External spacing (caller controls placement)
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 4.dp)
            // 2. Shadow before clip so it renders outside the shape
            .shadow(elevation = 2.dp, shape = RoundedCornerShape(12.dp))
            // 3. Clip to shape for rounded corners on ripple and content
            .clip(RoundedCornerShape(12.dp))
            // 4. Clickable after clip so the ripple respects the shape
            .clickable(onClick = onClick)
            // 5. Accessibility: provide a content description for screen readers
            .semantics {
                contentDescription = "Article: ${article.title}"
            },
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = article.title,
                style = MaterialTheme.typography.titleMedium,
            )
            Spacer(modifier = Modifier.height(4.dp))
            Text(
                text = article.summary,
                style = MaterialTheme.typography.bodyMedium,
                maxLines = 3,
            )
        }
    }
}
```

**Compose Previews**:

```kotlin
import androidx.compose.material3.Surface
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.tooling.preview.PreviewParameter
import androidx.compose.ui.tooling.preview.PreviewParameterProvider

class ArticlePreviewProvider : PreviewParameterProvider<ArticleUiModel> {
    override val values: Sequence<ArticleUiModel> = sequenceOf(
        ArticleUiModel(
            id = "1",
            title = "Jetpack Compose Best Practices",
            summary = "Learn how to build performant UIs with Compose...",
            imageUrl = null,
            publishedAt = "2024-12-01",
            isBookmarked = false,
        ),
        ArticleUiModel(
            id = "2",
            title = "A Very Long Title That Should Wrap to Multiple Lines in the Card Layout",
            summary = "Short summary.",
            imageUrl = "https://example.com/image.jpg",
            publishedAt = "2024-11-15",
            isBookmarked = true,
        ),
    )
}

@Preview(showBackground = true, name = "Light Mode")
@Preview(showBackground = true, name = "Dark Mode",
    uiMode = android.content.res.Configuration.UI_MODE_NIGHT_YES)
@Composable
private fun ArticleCardPreview(
    @PreviewParameter(ArticlePreviewProvider::class) article: ArticleUiModel,
) {
    MyAppTheme {
        Surface {
            ArticleCard(article = article, onClick = {})
        }
    }
}

@Preview(showBackground = true, widthDp = 360, heightDp = 640)
@Composable
private fun SearchScreenPreview() {
    MyAppTheme {
        SearchContent(
            query = "Kotlin",
            isSearching = false,
            onQueryChange = {},
            onSearch = {},
        )
    }
}
```

**Key Compose Principles**:

- Hoist state to the lowest common ancestor that needs it. Stateless composables are easier to test and preview
- Use `rememberSaveable` for state that must survive configuration changes; use `remember` for transient UI state only
- Mark data classes with `@Immutable` or `@Stable` to help the Compose compiler skip unnecessary recompositions
- Always accept a `modifier: Modifier = Modifier` parameter as the last optional parameter on public composables
- Use `derivedStateOf` when computing a value from other state objects to avoid redundant recompositions
- Modifier order matters: size and padding modifiers wrap outer to inner, and clickable should come after clip for correct ripple bounds

### Step 3: Material Design 3 Theming

Material Design 3 (Material You) introduces dynamic color, updated component styles, and a flexible theming system. A well-structured theme ensures consistent visual identity across the entire application.

**Color Scheme and Dynamic Color**:

```kotlin
import android.os.Build
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext

// Define custom colors using Material 3 tonal palette roles
private val LightColorScheme = lightColorScheme(
    primary = Color(0xFF1B6D3D),
    onPrimary = Color(0xFFFFFFFF),
    primaryContainer = Color(0xFFA5F5B8),
    onPrimaryContainer = Color(0xFF00210E),
    secondary = Color(0xFF4F6353),
    onSecondary = Color(0xFFFFFFFF),
    secondaryContainer = Color(0xFFD1E8D4),
    onSecondaryContainer = Color(0xFF0C1F13),
    tertiary = Color(0xFF3A656F),
    onTertiary = Color(0xFFFFFFFF),
    tertiaryContainer = Color(0xFFBEEAF6),
    onTertiaryContainer = Color(0xFF001F26),
    error = Color(0xFFBA1A1A),
    onError = Color(0xFFFFFFFF),
    errorContainer = Color(0xFFFFDAD6),
    onErrorContainer = Color(0xFF410002),
    background = Color(0xFFFBFDF8),
    onBackground = Color(0xFF191C19),
    surface = Color(0xFFFBFDF8),
    onSurface = Color(0xFF191C19),
    surfaceVariant = Color(0xFFDCE5DB),
    onSurfaceVariant = Color(0xFF414941),
    outline = Color(0xFF717971),
    outlineVariant = Color(0xFFC0C9BF),
)

private val DarkColorScheme = darkColorScheme(
    primary = Color(0xFF8AD89E),
    onPrimary = Color(0xFF00391B),
    primaryContainer = Color(0xFF00522B),
    onPrimaryContainer = Color(0xFFA5F5B8),
    secondary = Color(0xFFB6CCB8),
    onSecondary = Color(0xFF213527),
    secondaryContainer = Color(0xFF374B3C),
    onSecondaryContainer = Color(0xFFD1E8D4),
    tertiary = Color(0xFFA2CED9),
    onTertiary = Color(0xFF01363F),
    tertiaryContainer = Color(0xFF204D56),
    onTertiaryContainer = Color(0xFFBEEAF6),
    error = Color(0xFFFFB4AB),
    onError = Color(0xFF690005),
    errorContainer = Color(0xFF93000A),
    onErrorContainer = Color(0xFFFFDAD6),
    background = Color(0xFF191C19),
    onBackground = Color(0xFFE1E3DE),
    surface = Color(0xFF191C19),
    onSurface = Color(0xFFE1E3DE),
    surfaceVariant = Color(0xFF414941),
    onSurfaceVariant = Color(0xFFC0C9BF),
    outline = Color(0xFF8B938A),
    outlineVariant = Color(0xFF414941),
)

@Composable
fun MyAppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    dynamicColor: Boolean = true,
    content: @Composable () -> Unit,
) {
    val colorScheme = when {
        // Dynamic color is available on Android 12+ (API 31)
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            val context = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(context)
            else dynamicLightColorScheme(context)
        }
        darkTheme -> DarkColorScheme
        else -> LightColorScheme
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = AppTypography,
        shapes = AppShapes,
        content = content,
    )
}
```

**Typography**:

```kotlin
import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp

val InterFontFamily = FontFamily(
    Font(R.font.inter_regular, FontWeight.Normal),
    Font(R.font.inter_medium, FontWeight.Medium),
    Font(R.font.inter_semibold, FontWeight.SemiBold),
    Font(R.font.inter_bold, FontWeight.Bold),
)

val AppTypography = Typography(
    displayLarge = TextStyle(
        fontFamily = InterFontFamily,
        fontWeight = FontWeight.Normal,
        fontSize = 57.sp,
        lineHeight = 64.sp,
        letterSpacing = (-0.25).sp,
    ),
    headlineLarge = TextStyle(
        fontFamily = InterFontFamily,
        fontWeight = FontWeight.SemiBold,
        fontSize = 32.sp,
        lineHeight = 40.sp,
    ),
    headlineMedium = TextStyle(
        fontFamily = InterFontFamily,
        fontWeight = FontWeight.SemiBold,
        fontSize = 28.sp,
        lineHeight = 36.sp,
    ),
    titleLarge = TextStyle(
        fontFamily = InterFontFamily,
        fontWeight = FontWeight.Medium,
        fontSize = 22.sp,
        lineHeight = 28.sp,
    ),
    titleMedium = TextStyle(
        fontFamily = InterFontFamily,
        fontWeight = FontWeight.Medium,
        fontSize = 16.sp,
        lineHeight = 24.sp,
        letterSpacing = 0.15.sp,
    ),
    bodyLarge = TextStyle(
        fontFamily = InterFontFamily,
        fontWeight = FontWeight.Normal,
        fontSize = 16.sp,
        lineHeight = 24.sp,
        letterSpacing = 0.5.sp,
    ),
    bodyMedium = TextStyle(
        fontFamily = InterFontFamily,
        fontWeight = FontWeight.Normal,
        fontSize = 14.sp,
        lineHeight = 20.sp,
        letterSpacing = 0.25.sp,
    ),
    labelLarge = TextStyle(
        fontFamily = InterFontFamily,
        fontWeight = FontWeight.Medium,
        fontSize = 14.sp,
        lineHeight = 20.sp,
        letterSpacing = 0.1.sp,
    ),
    labelMedium = TextStyle(
        fontFamily = InterFontFamily,
        fontWeight = FontWeight.Medium,
        fontSize = 12.sp,
        lineHeight = 16.sp,
        letterSpacing = 0.5.sp,
    ),
)
```

**Shapes**:

```kotlin
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Shapes
import androidx.compose.ui.unit.dp

val AppShapes = Shapes(
    extraSmall = RoundedCornerShape(4.dp),
    small = RoundedCornerShape(8.dp),
    medium = RoundedCornerShape(12.dp),
    large = RoundedCornerShape(16.dp),
    extraLarge = RoundedCornerShape(28.dp),
)
```

**Using Theme Values in Composables**:

```kotlin
@Composable
fun StatusBadge(
    label: String,
    isActive: Boolean,
    modifier: Modifier = Modifier,
) {
    val containerColor = if (isActive) {
        MaterialTheme.colorScheme.primaryContainer
    } else {
        MaterialTheme.colorScheme.surfaceVariant
    }
    val contentColor = if (isActive) {
        MaterialTheme.colorScheme.onPrimaryContainer
    } else {
        MaterialTheme.colorScheme.onSurfaceVariant
    }

    Surface(
        modifier = modifier,
        shape = MaterialTheme.shapes.small,
        color = containerColor,
        contentColor = contentColor,
    ) {
        Text(
            text = label,
            modifier = Modifier.padding(horizontal = 12.dp, vertical = 4.dp),
            style = MaterialTheme.typography.labelMedium,
        )
    }
}
```

**Key Theming Principles**:

- Use `dynamicColorScheme` on Android 12+ devices to automatically extract colors from the user's wallpaper, falling back to your custom color scheme on older devices
- Always define both light and dark color schemes. Use `isSystemInDarkTheme()` to follow the system setting
- Reference `MaterialTheme.colorScheme`, `MaterialTheme.typography`, and `MaterialTheme.shapes` in composables instead of hardcoding values
- Use semantic color roles (`primary`, `secondary`, `error`, `surface`, `surfaceVariant`) rather than raw color values to maintain consistency
- Test your theme with both dynamic color enabled and disabled, and verify readability in both light and dark modes

### Step 4: Navigation

Compose Navigation provides a declarative, type-safe way to manage screen transitions, deep links, and nested navigation graphs.

**Type-Safe Route Definitions**:

```kotlin
import kotlinx.serialization.Serializable

/**
 * Define routes as @Serializable data classes or objects.
 * This approach provides compile-time safety for navigation arguments.
 */
sealed interface Route {
    @Serializable
    data object Home : Route

    @Serializable
    data object Profile : Route

    @Serializable
    data object Settings : Route

    @Serializable
    data class ArticleDetail(val articleId: String) : Route

    @Serializable
    data class UserProfile(val userId: String, val tab: String = "posts") : Route
}

/**
 * Top-level navigation destinations for bottom navigation.
 */
enum class TopLevelDestination(
    val route: Route,
    val selectedIcon: ImageVector,
    val unselectedIcon: ImageVector,
    val label: String,
) {
    HOME(
        route = Route.Home,
        selectedIcon = Icons.Filled.Home,
        unselectedIcon = Icons.Outlined.Home,
        label = "Home",
    ),
    PROFILE(
        route = Route.Profile,
        selectedIcon = Icons.Filled.Person,
        unselectedIcon = Icons.Outlined.Person,
        label = "Profile",
    ),
    SETTINGS(
        route = Route.Settings,
        selectedIcon = Icons.Filled.Settings,
        unselectedIcon = Icons.Outlined.Settings,
        label = "Settings",
    ),
}
```

**Navigation Host with Bottom Navigation**:

```kotlin
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.navigation.NavDestination.Companion.hasRoute
import androidx.navigation.NavDestination.Companion.hierarchy
import androidx.navigation.NavGraph.Companion.findStartDestination
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import androidx.navigation.toRoute

@Composable
fun MainScreen() {
    val navController = rememberNavController()
    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentDestination = navBackStackEntry?.destination

    // Determine whether to show bottom navigation
    val showBottomBar = TopLevelDestination.entries.any { dest ->
        currentDestination?.hasRoute(dest.route::class) == true
    }

    Scaffold(
        bottomBar = {
            if (showBottomBar) {
                NavigationBar {
                    TopLevelDestination.entries.forEach { destination ->
                        val selected = currentDestination?.hierarchy?.any {
                            it.hasRoute(destination.route::class)
                        } == true

                        NavigationBarItem(
                            selected = selected,
                            onClick = {
                                navController.navigate(destination.route) {
                                    // Pop up to the start destination to avoid
                                    // building up a large back stack
                                    popUpTo(navController.graph.findStartDestination().id) {
                                        saveState = true
                                    }
                                    launchSingleTop = true
                                    restoreState = true
                                }
                            },
                            icon = {
                                Icon(
                                    imageVector = if (selected) destination.selectedIcon
                                        else destination.unselectedIcon,
                                    contentDescription = destination.label,
                                )
                            },
                            label = { Text(destination.label) },
                        )
                    }
                }
            }
        },
    ) { innerPadding ->
        NavHost(
            navController = navController,
            startDestination = Route.Home,
            modifier = Modifier.padding(innerPadding),
        ) {
            composable<Route.Home> {
                HomeScreen(
                    onArticleClick = { articleId ->
                        navController.navigate(Route.ArticleDetail(articleId))
                    },
                )
            }

            composable<Route.Profile> {
                ProfileScreen(
                    onUserClick = { userId ->
                        navController.navigate(Route.UserProfile(userId))
                    },
                )
            }

            composable<Route.Settings> {
                SettingsScreen()
            }

            composable<Route.ArticleDetail> { backStackEntry ->
                val route = backStackEntry.toRoute<Route.ArticleDetail>()
                ArticleDetailScreen(articleId = route.articleId)
            }

            composable<Route.UserProfile> { backStackEntry ->
                val route = backStackEntry.toRoute<Route.UserProfile>()
                UserProfileScreen(userId = route.userId, initialTab = route.tab)
            }
        }
    }
}
```

**Deep Links**:

```kotlin
import androidx.navigation.navDeepLink

// Inside the NavHost builder:
composable<Route.ArticleDetail>(
    deepLinks = listOf(
        navDeepLink<Route.ArticleDetail>(
            basePath = "https://myapp.example.com/articles",
        ),
    ),
) { backStackEntry ->
    val route = backStackEntry.toRoute<Route.ArticleDetail>()
    ArticleDetailScreen(articleId = route.articleId)
}
```

**AndroidManifest.xml Deep Link Configuration**:

```xml
<activity android:name=".MainActivity"
    android:exported="true">
    <intent-filter android:autoVerify="true">
        <action android:name="android.intent.action.VIEW" />
        <category android:name="android.intent.category.DEFAULT" />
        <category android:name="android.intent.category.BROWSABLE" />
        <data android:scheme="https"
              android:host="myapp.example.com"
              android:pathPrefix="/articles" />
    </intent-filter>
</activity>
```

**Key Navigation Principles**:

- Define routes as `@Serializable` data classes or objects to get compile-time safety for navigation arguments
- Use `popUpTo` with `saveState = true` and `restoreState = true` on bottom navigation items to preserve each tab's back stack
- Hide the bottom navigation bar on detail screens by checking whether the current destination is a top-level route
- Use `launchSingleTop = true` to prevent duplicate destinations on repeated taps
- Configure deep links both in the `NavHost` and in `AndroidManifest.xml` with `android:autoVerify="true"` for App Links

### Step 5: Architecture Patterns

Modern Android architecture follows a unidirectional data flow pattern with clear separation between UI, domain, and data layers. ViewModel exposes UI state, the domain layer contains business logic, and the data layer manages data sources.

**UiState and ViewModel**:

```kotlin
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

/**
 * Sealed interface for UI state. Each subtype represents a distinct
 * state the screen can be in. Prefer a single sealed hierarchy over
 * multiple boolean flags to make impossible states unrepresentable.
 */
sealed interface ArticleListUiState {
    data object Loading : ArticleListUiState

    data class Success(
        val articles: List<ArticleUiModel>,
        val isRefreshing: Boolean = false,
    ) : ArticleListUiState

    data class Error(
        val message: String,
        val canRetry: Boolean = true,
    ) : ArticleListUiState
}

/**
 * One-shot events that the UI should handle exactly once (navigation,
 * snackbar, etc.). Use a Channel or SharedFlow, not StateFlow.
 */
sealed interface ArticleListEvent {
    data class ShowSnackbar(val message: String) : ArticleListEvent
    data class NavigateToDetail(val articleId: String) : ArticleListEvent
}

/**
 * User actions that the UI sends to the ViewModel.
 */
sealed interface ArticleListAction {
    data object LoadArticles : ArticleListAction
    data object Refresh : ArticleListAction
    data class ToggleBookmark(val articleId: String) : ArticleListAction
    data class ArticleClicked(val articleId: String) : ArticleListAction
}

@HiltViewModel
class ArticleListViewModel @Inject constructor(
    private val getArticlesUseCase: GetArticlesUseCase,
    private val toggleBookmarkUseCase: ToggleBookmarkUseCase,
) : ViewModel() {

    private val _uiState = MutableStateFlow<ArticleListUiState>(ArticleListUiState.Loading)
    val uiState: StateFlow<ArticleListUiState> = _uiState.asStateFlow()

    private val _events = MutableSharedFlow<ArticleListEvent>(extraBufferCapacity = 1)
    val events: SharedFlow<ArticleListEvent> = _events.asSharedFlow()

    init {
        onAction(ArticleListAction.LoadArticles)
    }

    fun onAction(action: ArticleListAction) {
        when (action) {
            is ArticleListAction.LoadArticles -> loadArticles()
            is ArticleListAction.Refresh -> refresh()
            is ArticleListAction.ToggleBookmark -> toggleBookmark(action.articleId)
            is ArticleListAction.ArticleClicked -> {
                _events.tryEmit(ArticleListEvent.NavigateToDetail(action.articleId))
            }
        }
    }

    private fun loadArticles() {
        viewModelScope.launch {
            _uiState.value = ArticleListUiState.Loading
            getArticlesUseCase()
                .catch { e ->
                    _uiState.value = ArticleListUiState.Error(
                        message = e.message ?: "Failed to load articles",
                    )
                }
                .collect { articles ->
                    _uiState.value = ArticleListUiState.Success(
                        articles = articles.map { it.toUiModel() },
                    )
                }
        }
    }

    private fun refresh() {
        val currentState = _uiState.value
        if (currentState is ArticleListUiState.Success) {
            _uiState.value = currentState.copy(isRefreshing = true)
        }
        loadArticles()
    }

    private fun toggleBookmark(articleId: String) {
        viewModelScope.launch {
            toggleBookmarkUseCase(articleId)
                .onFailure { e ->
                    _events.tryEmit(
                        ArticleListEvent.ShowSnackbar("Failed to update bookmark"),
                    )
                }
        }
    }
}
```

**Use Cases (Domain Layer)**:

```kotlin
import kotlinx.coroutines.flow.Flow
import javax.inject.Inject

/**
 * Use cases encapsulate a single piece of business logic.
 * They depend on repository interfaces (defined in domain),
 * not on concrete implementations (defined in data).
 */
class GetArticlesUseCase @Inject constructor(
    private val articleRepository: ArticleRepository,
) {
    /**
     * Returns a Flow of articles sorted by publication date.
     * The repository handles the offline-first caching strategy.
     */
    operator fun invoke(): Flow<List<Article>> {
        return articleRepository.getArticles()
    }
}

class ToggleBookmarkUseCase @Inject constructor(
    private val articleRepository: ArticleRepository,
) {
    suspend operator fun invoke(articleId: String): Result<Unit> {
        return runCatching {
            val article = articleRepository.getArticleById(articleId)
                ?: throw IllegalArgumentException("Article $articleId not found")
            articleRepository.updateBookmark(articleId, !article.isBookmarked)
        }
    }
}

/**
 * Repository interface defined in the domain layer.
 * The data layer provides the concrete implementation.
 */
interface ArticleRepository {
    fun getArticles(): Flow<List<Article>>
    suspend fun getArticleById(id: String): Article?
    suspend fun updateBookmark(id: String, isBookmarked: Boolean)
    suspend fun refreshArticles()
}
```

**Hilt Dependency Injection**:

```kotlin
import android.app.Application
import dagger.Binds
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.HiltAndroidApp
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@HiltAndroidApp
class MyApplication : Application()

@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryModule {
    @Binds
    @Singleton
    abstract fun bindArticleRepository(
        impl: ArticleRepositoryImpl,
    ): ArticleRepository
}

@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {
    @Provides
    @Singleton
    fun provideDatabase(app: Application): AppDatabase {
        return Room.databaseBuilder(
            app,
            AppDatabase::class.java,
            "myapp.db",
        )
            .addMigrations(MIGRATION_1_2, MIGRATION_2_3)
            .build()
    }

    @Provides
    fun provideArticleDao(db: AppDatabase): ArticleDao = db.articleDao()
}

@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {
    @Provides
    @Singleton
    fun provideOkHttpClient(): OkHttpClient {
        return OkHttpClient.Builder()
            .addInterceptor(HttpLoggingInterceptor().apply {
                level = if (BuildConfig.DEBUG) HttpLoggingInterceptor.Level.BODY
                    else HttpLoggingInterceptor.Level.NONE
            })
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .build()
    }

    @Provides
    @Singleton
    fun provideRetrofit(client: OkHttpClient): Retrofit {
        return Retrofit.Builder()
            .baseUrl("https://api.example.com/")
            .client(client)
            .addConverterFactory(
                Json.asConverterFactory("application/json".toMediaType()),
            )
            .build()
    }

    @Provides
    @Singleton
    fun provideArticleApi(retrofit: Retrofit): ArticleApi {
        return retrofit.create(ArticleApi::class.java)
    }
}
```

**Connecting ViewModel to Compose UI**:

```kotlin
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle

@Composable
fun ArticleListRoute(
    onNavigateToDetail: (String) -> Unit,
    viewModel: ArticleListViewModel = hiltViewModel(),
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    // Collect one-shot events
    LaunchedEffect(Unit) {
        viewModel.events.collect { event ->
            when (event) {
                is ArticleListEvent.NavigateToDetail -> {
                    onNavigateToDetail(event.articleId)
                }
                is ArticleListEvent.ShowSnackbar -> {
                    // Show snackbar via SnackbarHostState
                }
            }
        }
    }

    ArticleListScreen(
        uiState = uiState,
        onAction = viewModel::onAction,
    )
}
```

**Key Architecture Principles**:

- Use a sealed interface for UiState to make impossible states unrepresentable (a screen cannot be both loading and showing an error)
- One-shot events (navigation, snackbar) should use `SharedFlow` or `Channel`, not `StateFlow`, to ensure they are consumed exactly once
- Define repository interfaces in the domain layer and implementations in the data layer for testability and inversion of control
- Use `collectAsStateWithLifecycle()` (not `collectAsState()`) to automatically stop collection when the lifecycle is below the minimum active state
- ViewModels should never reference Android framework classes (Context, Activity) directly; use Hilt to inject dependencies instead

### Step 6: Data Layer

The data layer manages data from local (Room, DataStore) and remote (Retrofit, Ktor) sources. An offline-first approach serves cached data immediately while fetching updates in the background.

**Room Database**:

```kotlin
import androidx.room.*
import kotlinx.coroutines.flow.Flow

@Entity(tableName = "articles")
data class ArticleEntity(
    @PrimaryKey
    val id: String,
    val title: String,
    val summary: String,
    @ColumnInfo(name = "image_url")
    val imageUrl: String?,
    @ColumnInfo(name = "published_at")
    val publishedAt: Long,
    @ColumnInfo(name = "is_bookmarked")
    val isBookmarked: Boolean = false,
    @ColumnInfo(name = "last_fetched_at")
    val lastFetchedAt: Long = System.currentTimeMillis(),
)

@Dao
interface ArticleDao {
    @Query("SELECT * FROM articles ORDER BY published_at DESC")
    fun observeAll(): Flow<List<ArticleEntity>>

    @Query("SELECT * FROM articles WHERE id = :id")
    suspend fun getById(id: String): ArticleEntity?

    @Upsert
    suspend fun upsertAll(articles: List<ArticleEntity>)

    @Query("UPDATE articles SET is_bookmarked = :isBookmarked WHERE id = :id")
    suspend fun updateBookmark(id: String, isBookmarked: Boolean)

    @Query("DELETE FROM articles WHERE last_fetched_at < :cutoff")
    suspend fun deleteStale(cutoff: Long)

    @Query("SELECT COUNT(*) FROM articles")
    suspend fun count(): Int
}

@Database(
    entities = [ArticleEntity::class],
    version = 1,
    exportSchema = true,
)
@TypeConverters(Converters::class)
abstract class AppDatabase : RoomDatabase() {
    abstract fun articleDao(): ArticleDao
}

class Converters {
    @TypeConverter
    fun fromTimestamp(value: Long?): java.util.Date? = value?.let { java.util.Date(it) }

    @TypeConverter
    fun dateToTimestamp(date: java.util.Date?): Long? = date?.time
}
```

**Room Database Migrations**:

```kotlin
val MIGRATION_1_2 = object : Migration(1, 2) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL(
            "ALTER TABLE articles ADD COLUMN author_name TEXT DEFAULT NULL",
        )
    }
}

val MIGRATION_2_3 = object : Migration(2, 3) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL(
            """CREATE TABLE IF NOT EXISTS article_tags (
                article_id TEXT NOT NULL,
                tag TEXT NOT NULL,
                PRIMARY KEY(article_id, tag),
                FOREIGN KEY(article_id) REFERENCES articles(id) ON DELETE CASCADE
            )""",
        )
        db.execSQL(
            "CREATE INDEX index_article_tags_tag ON article_tags(tag)",
        )
    }
}
```

**DataStore for Preferences**:

```kotlin
import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.*
import androidx.datastore.preferences.preferencesDataStore
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.flow.map
import java.io.IOException
import javax.inject.Inject
import javax.inject.Singleton

private val Context.dataStore: DataStore<Preferences> by preferencesDataStore(
    name = "user_preferences",
)

data class UserPreferences(
    val darkMode: DarkMode = DarkMode.SYSTEM,
    val dynamicColor: Boolean = true,
    val notificationsEnabled: Boolean = true,
    val articlesPerPage: Int = 20,
)

enum class DarkMode { LIGHT, DARK, SYSTEM }

@Singleton
class UserPreferencesRepository @Inject constructor(
    @ApplicationContext private val context: Context,
) {
    private object Keys {
        val DARK_MODE = stringPreferencesKey("dark_mode")
        val DYNAMIC_COLOR = booleanPreferencesKey("dynamic_color")
        val NOTIFICATIONS = booleanPreferencesKey("notifications_enabled")
        val ARTICLES_PER_PAGE = intPreferencesKey("articles_per_page")
    }

    val preferences: Flow<UserPreferences> = context.dataStore.data
        .catch { exception ->
            if (exception is IOException) {
                emit(emptyPreferences())
            } else {
                throw exception
            }
        }
        .map { prefs ->
            UserPreferences(
                darkMode = prefs[Keys.DARK_MODE]?.let {
                    DarkMode.valueOf(it)
                } ?: DarkMode.SYSTEM,
                dynamicColor = prefs[Keys.DYNAMIC_COLOR] ?: true,
                notificationsEnabled = prefs[Keys.NOTIFICATIONS] ?: true,
                articlesPerPage = prefs[Keys.ARTICLES_PER_PAGE] ?: 20,
            )
        }

    suspend fun setDarkMode(mode: DarkMode) {
        context.dataStore.edit { it[Keys.DARK_MODE] = mode.name }
    }

    suspend fun setDynamicColor(enabled: Boolean) {
        context.dataStore.edit { it[Keys.DYNAMIC_COLOR] = enabled }
    }

    suspend fun setNotificationsEnabled(enabled: Boolean) {
        context.dataStore.edit { it[Keys.NOTIFICATIONS] = enabled }
    }
}
```

**Retrofit Networking**:

```kotlin
import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import retrofit2.http.*

@Serializable
data class ArticleDto(
    val id: String,
    val title: String,
    val summary: String,
    @SerialName("image_url")
    val imageUrl: String?,
    @SerialName("published_at")
    val publishedAt: String,
    @SerialName("author_name")
    val authorName: String?,
)

@Serializable
data class ArticleListResponse(
    val articles: List<ArticleDto>,
    @SerialName("total_count")
    val totalCount: Int,
    @SerialName("next_cursor")
    val nextCursor: String?,
)

interface ArticleApi {
    @GET("v1/articles")
    suspend fun getArticles(
        @Query("cursor") cursor: String? = null,
        @Query("limit") limit: Int = 20,
    ): ArticleListResponse

    @GET("v1/articles/{id}")
    suspend fun getArticle(@Path("id") id: String): ArticleDto

    @POST("v1/articles/{id}/bookmark")
    suspend fun bookmark(@Path("id") id: String)

    @DELETE("v1/articles/{id}/bookmark")
    suspend fun removeBookmark(@Path("id") id: String)
}
```

**Offline-First Repository Implementation**:

```kotlin
import kotlinx.coroutines.flow.*
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class ArticleRepositoryImpl @Inject constructor(
    private val articleApi: ArticleApi,
    private val articleDao: ArticleDao,
) : ArticleRepository {

    /**
     * Offline-first: emit cached data immediately, then fetch fresh data
     * from the network and update the cache. The Flow automatically
     * re-emits when the Room database is updated.
     */
    override fun getArticles(): Flow<List<Article>> {
        return articleDao.observeAll()
            .map { entities -> entities.map { it.toDomain() } }
            .onStart {
                // Trigger a background refresh; errors are logged, not propagated
                try {
                    refreshArticles()
                } catch (e: Exception) {
                    // Log but do not interrupt the cached data flow
                    timber.log.Timber.w(e, "Failed to refresh articles from network")
                }
            }
    }

    override suspend fun getArticleById(id: String): Article? {
        return articleDao.getById(id)?.toDomain()
    }

    override suspend fun updateBookmark(id: String, isBookmarked: Boolean) {
        // Optimistic update: update local first, then sync to server
        articleDao.updateBookmark(id, isBookmarked)
        try {
            if (isBookmarked) articleApi.bookmark(id)
            else articleApi.removeBookmark(id)
        } catch (e: Exception) {
            // Rollback local change on network failure
            articleDao.updateBookmark(id, !isBookmarked)
            throw e
        }
    }

    override suspend fun refreshArticles() {
        val response = articleApi.getArticles()
        val entities = response.articles.map { dto ->
            ArticleEntity(
                id = dto.id,
                title = dto.title,
                summary = dto.summary,
                imageUrl = dto.imageUrl,
                publishedAt = java.time.Instant.parse(dto.publishedAt).toEpochMilli(),
                lastFetchedAt = System.currentTimeMillis(),
            )
        }
        articleDao.upsertAll(entities)
        // Clean up articles not refreshed in the last 7 days
        val cutoff = System.currentTimeMillis() - 7 * 24 * 60 * 60 * 1000L
        articleDao.deleteStale(cutoff)
    }
}
```

**Paging 3 Integration**:

```kotlin
import androidx.paging.*
import kotlinx.coroutines.flow.Flow

@OptIn(ExperimentalPagingApi::class)
class ArticlePagingRepository @Inject constructor(
    private val articleApi: ArticleApi,
    private val articleDao: ArticleDao,
    private val database: AppDatabase,
) {
    fun getPagedArticles(): Flow<PagingData<Article>> {
        return Pager(
            config = PagingConfig(
                pageSize = 20,
                prefetchDistance = 5,
                enablePlaceholders = false,
            ),
            remoteMediator = ArticleRemoteMediator(articleApi, articleDao, database),
            pagingSourceFactory = { articleDao.pagingSource() },
        ).flow.map { pagingData ->
            pagingData.map { entity -> entity.toDomain() }
        }
    }
}

@OptIn(ExperimentalPagingApi::class)
class ArticleRemoteMediator(
    private val api: ArticleApi,
    private val dao: ArticleDao,
    private val database: AppDatabase,
) : RemoteMediator<Int, ArticleEntity>() {

    override suspend fun load(
        loadType: LoadType,
        state: PagingState<Int, ArticleEntity>,
    ): MediatorResult {
        val cursor = when (loadType) {
            LoadType.REFRESH -> null
            LoadType.PREPEND -> return MediatorResult.Success(endOfPaginationReached = true)
            LoadType.APPEND -> {
                // Retrieve the next cursor from the last loaded page
                state.lastItemOrNull()?.id ?: return MediatorResult.Success(
                    endOfPaginationReached = true,
                )
            }
        }

        return try {
            val response = api.getArticles(
                cursor = cursor,
                limit = state.config.pageSize,
            )
            val entities = response.articles.map { it.toEntity() }

            database.withTransaction {
                if (loadType == LoadType.REFRESH) {
                    dao.deleteStale(0) // Clear all on refresh
                }
                dao.upsertAll(entities)
            }

            MediatorResult.Success(
                endOfPaginationReached = response.nextCursor == null,
            )
        } catch (e: Exception) {
            MediatorResult.Error(e)
        }
    }
}
```

**Key Data Layer Principles**:

- Use Room's `Flow`-returning queries to observe database changes reactively. Updates from network refreshes automatically trigger UI updates through the Flow chain
- Prefer `@Upsert` over `@Insert(onConflict = REPLACE)` for batch updates, as Upsert is more efficient and explicit
- Use DataStore for key-value preferences (replacing SharedPreferences). Use Proto DataStore for complex structured data
- Implement optimistic updates for user actions (bookmarks, likes) by updating the local database first, then syncing to the server with rollback on failure
- Use Paging 3 with `RemoteMediator` for large datasets that combine local caching with network pagination
- Always define database migrations for schema changes; never use `fallbackToDestructiveMigration()` in production

### Step 7: Lifecycle and Side Effects

Android lifecycle management is critical for avoiding memory leaks, ensuring correct coroutine scoping, and performing background work reliably.

**LaunchedEffect and Lifecycle-Aware Collection**:

```kotlin
import androidx.compose.runtime.*
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.compose.LocalLifecycleOwner
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.repeatOnLifecycle
import kotlinx.coroutines.flow.Flow

/**
 * LaunchedEffect runs a suspend block when the composable enters
 * the composition. It cancels and relaunches when its key changes.
 */
@Composable
fun ArticleDetailScreen(
    articleId: String,
    viewModel: ArticleDetailViewModel = hiltViewModel(),
) {
    // Re-fetch when the articleId changes
    LaunchedEffect(articleId) {
        viewModel.loadArticle(articleId)
    }

    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    // Collect one-shot events with lifecycle awareness
    val lifecycleOwner = LocalLifecycleOwner.current
    LaunchedEffect(lifecycleOwner) {
        lifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
            viewModel.events.collect { event ->
                when (event) {
                    is ArticleDetailEvent.ShareArticle -> {
                        // Trigger share intent
                    }
                    is ArticleDetailEvent.OpenInBrowser -> {
                        // Open URL
                    }
                }
            }
        }
    }

    ArticleDetailContent(uiState = uiState)
}
```

**DisposableEffect for Cleanup**:

```kotlin
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.ui.platform.LocalContext

/**
 * DisposableEffect runs setup code when entering composition and
 * cleanup code via onDispose when leaving composition.
 * Use for registering/unregistering listeners, sensors, or callbacks.
 */
@Composable
fun LocationTracker(
    onLocationUpdate: (latitude: Double, longitude: Double) -> Unit,
) {
    val context = LocalContext.current

    DisposableEffect(context) {
        val locationManager = context.getSystemService(
            Context.LOCATION_SERVICE,
        ) as LocationManager

        val listener = object : LocationListener {
            override fun onLocationChanged(location: Location) {
                onLocationUpdate(location.latitude, location.longitude)
            }
        }

        try {
            locationManager.requestLocationUpdates(
                LocationManager.FUSED_PROVIDER,
                5000L,    // minimum time interval (ms)
                10f,      // minimum distance (meters)
                listener,
            )
        } catch (e: SecurityException) {
            // Permission not granted; handle gracefully
        }

        onDispose {
            locationManager.removeUpdates(listener)
        }
    }
}

/**
 * Lifecycle-aware analytics tracking.
 */
@Composable
fun ScreenTracker(screenName: String) {
    val lifecycleOwner = LocalLifecycleOwner.current

    DisposableEffect(lifecycleOwner, screenName) {
        val observer = LifecycleEventObserver { _, event ->
            when (event) {
                Lifecycle.Event.ON_RESUME -> {
                    Analytics.trackScreenView(screenName)
                }
                Lifecycle.Event.ON_PAUSE -> {
                    Analytics.trackScreenExit(screenName)
                }
                else -> {}
            }
        }
        lifecycleOwner.lifecycle.addObserver(observer)

        onDispose {
            lifecycleOwner.lifecycle.removeObserver(observer)
        }
    }
}
```

**WorkManager for Background Tasks**:

```kotlin
import android.content.Context
import androidx.hilt.work.HiltWorker
import androidx.work.*
import dagger.assisted.Assisted
import dagger.assisted.AssistedInject
import java.util.concurrent.TimeUnit

@HiltWorker
class ArticleSyncWorker @AssistedInject constructor(
    @Assisted appContext: Context,
    @Assisted workerParams: WorkerParameters,
    private val articleRepository: ArticleRepository,
) : CoroutineWorker(appContext, workerParams) {

    override suspend fun doWork(): Result {
        return try {
            articleRepository.refreshArticles()
            Result.success()
        } catch (e: Exception) {
            if (runAttemptCount < 3) {
                Result.retry()
            } else {
                Result.failure(
                    workDataOf("error" to e.message),
                )
            }
        }
    }

    companion object {
        const val WORK_NAME = "article_sync"

        fun buildPeriodicRequest(): PeriodicWorkRequest {
            val constraints = Constraints.Builder()
                .setRequiredNetworkType(NetworkType.CONNECTED)
                .setRequiresBatteryNotLow(true)
                .build()

            return PeriodicWorkRequestBuilder<ArticleSyncWorker>(
                repeatInterval = 6,
                repeatIntervalTimeUnit = TimeUnit.HOURS,
                flexInterval = 30,
                flexTimeUnit = TimeUnit.MINUTES,
            )
                .setConstraints(constraints)
                .setBackoffCriteria(
                    BackoffPolicy.EXPONENTIAL,
                    WorkRequest.MIN_BACKOFF_MILLIS,
                    TimeUnit.MILLISECONDS,
                )
                .addTag("sync")
                .build()
        }

        fun buildOneTimeRequest(): OneTimeWorkRequest {
            return OneTimeWorkRequestBuilder<ArticleSyncWorker>()
                .setConstraints(
                    Constraints.Builder()
                        .setRequiredNetworkType(NetworkType.CONNECTED)
                        .build(),
                )
                .setExpedited(OutOfQuotaPolicy.RUN_AS_NON_EXPEDITED_WORK_REQUEST)
                .build()
        }
    }
}

/**
 * Schedule the sync worker from the Application class or a ViewModel.
 */
fun schedulePeriodicSync(context: Context) {
    WorkManager.getInstance(context).enqueueUniquePeriodicWork(
        ArticleSyncWorker.WORK_NAME,
        ExistingPeriodicWorkPolicy.KEEP,
        ArticleSyncWorker.buildPeriodicRequest(),
    )
}
```

**Foreground Service for Long-Running Operations**:

```kotlin
import android.app.*
import android.content.Intent
import android.content.pm.ServiceInfo
import android.os.Build
import android.os.IBinder
import androidx.core.app.NotificationCompat
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.coroutines.*
import javax.inject.Inject

@AndroidEntryPoint
class FileUploadService : Service() {

    @Inject
    lateinit var uploadRepository: UploadRepository

    private val serviceScope = CoroutineScope(SupervisorJob() + Dispatchers.IO)

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val fileUri = intent?.getStringExtra("file_uri")
            ?: return START_NOT_STICKY

        val notification = createNotification("Uploading file...")
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            startForeground(
                NOTIFICATION_ID,
                notification,
                ServiceInfo.FOREGROUND_SERVICE_TYPE_DATA_SYNC,
            )
        } else {
            startForeground(NOTIFICATION_ID, notification)
        }

        serviceScope.launch {
            try {
                uploadRepository.uploadFile(fileUri) { progress ->
                    updateNotification("Uploading: ${progress}%")
                }
                updateNotification("Upload complete")
            } catch (e: Exception) {
                updateNotification("Upload failed: ${e.message}")
            } finally {
                delay(2000) // Brief pause to show final status
                stopSelf()
            }
        }

        return START_NOT_STICKY
    }

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onDestroy() {
        serviceScope.cancel()
        super.onDestroy()
    }

    private fun createNotification(text: String): Notification {
        createNotificationChannel()
        return NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("File Upload")
            .setContentText(text)
            .setSmallIcon(R.drawable.ic_upload)
            .setOngoing(true)
            .setProgress(100, 0, true)
            .build()
    }

    private fun updateNotification(text: String) {
        val notification = createNotification(text)
        val manager = getSystemService(NotificationManager::class.java)
        manager.notify(NOTIFICATION_ID, notification)
    }

    private fun createNotificationChannel() {
        val channel = NotificationChannel(
            CHANNEL_ID,
            "File Uploads",
            NotificationManager.IMPORTANCE_LOW,
        )
        val manager = getSystemService(NotificationManager::class.java)
        manager.createNotificationChannel(channel)
    }

    companion object {
        private const val CHANNEL_ID = "file_upload_channel"
        private const val NOTIFICATION_ID = 1001
    }
}
```

**Key Lifecycle and Side Effect Principles**:

- Use `LaunchedEffect(key)` for suspend operations that should restart when the key changes. Use `LaunchedEffect(Unit)` for one-time setup that runs once per composition
- Use `DisposableEffect` for operations that require explicit cleanup (listeners, sensors, observers)
- Always collect Flows with `collectAsStateWithLifecycle()` in Compose to stop collection when the app is in the background, saving battery and avoiding stale updates
- Use `repeatOnLifecycle(Lifecycle.State.STARTED)` when collecting events in `LaunchedEffect` to ensure proper lifecycle-aware collection
- Prefer WorkManager over foreground services for deferrable background work. WorkManager handles constraints, retries, and backoff automatically
- Declare foreground service types in `AndroidManifest.xml` (required on Android 14+) and request the `FOREGROUND_SERVICE_*` permissions

### Step 8: Testing

Comprehensive Android testing spans unit tests for ViewModels and use cases, Compose UI tests for screen behavior, and integration tests for the data layer.

**ViewModel Unit Tests with JUnit 5 and Turbine**:

```kotlin
import app.cash.turbine.test
import com.google.common.truth.Truth.assertThat
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.flowOf
import kotlinx.coroutines.test.UnconfinedTestDispatcher
import kotlinx.coroutines.test.runTest
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.DisplayName
import org.junit.jupiter.api.Nested
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.extension.ExtendWith

@OptIn(ExperimentalCoroutinesApi::class)
@ExtendWith(MainDispatcherExtension::class)
class ArticleListViewModelTest {

    private lateinit var getArticlesUseCase: FakeGetArticlesUseCase
    private lateinit var toggleBookmarkUseCase: FakeToggleBookmarkUseCase
    private lateinit var viewModel: ArticleListViewModel

    @BeforeEach
    fun setup() {
        getArticlesUseCase = FakeGetArticlesUseCase()
        toggleBookmarkUseCase = FakeToggleBookmarkUseCase()
        viewModel = ArticleListViewModel(getArticlesUseCase, toggleBookmarkUseCase)
    }

    @Nested
    @DisplayName("Loading articles")
    inner class LoadArticles {

        @Test
        fun `emits Loading then Success when articles are available`() = runTest {
            val articles = listOf(
                testArticle(id = "1", title = "First Article"),
                testArticle(id = "2", title = "Second Article"),
            )
            getArticlesUseCase.setArticles(articles)

            viewModel.uiState.test {
                // Init triggers LoadArticles, first emission is Loading
                assertThat(awaitItem()).isInstanceOf(ArticleListUiState.Loading::class.java)

                val success = awaitItem() as ArticleListUiState.Success
                assertThat(success.articles).hasSize(2)
                assertThat(success.articles[0].title).isEqualTo("First Article")
            }
        }

        @Test
        fun `emits Error when loading fails`() = runTest {
            getArticlesUseCase.setShouldFail(true)

            viewModel.uiState.test {
                assertThat(awaitItem()).isInstanceOf(ArticleListUiState.Loading::class.java)

                val error = awaitItem() as ArticleListUiState.Error
                assertThat(error.message).contains("Failed")
                assertThat(error.canRetry).isTrue()
            }
        }
    }

    @Nested
    @DisplayName("Bookmarking")
    inner class Bookmarking {

        @Test
        fun `emits snackbar event when bookmark toggle fails`() = runTest {
            toggleBookmarkUseCase.setShouldFail(true)

            viewModel.events.test {
                viewModel.onAction(ArticleListAction.ToggleBookmark("1"))

                val event = awaitItem() as ArticleListEvent.ShowSnackbar
                assertThat(event.message).contains("bookmark")
            }
        }
    }

    @Nested
    @DisplayName("Navigation")
    inner class Navigation {

        @Test
        fun `emits navigate event when article is clicked`() = runTest {
            viewModel.events.test {
                viewModel.onAction(ArticleListAction.ArticleClicked("article-42"))

                val event = awaitItem() as ArticleListEvent.NavigateToDetail
                assertThat(event.articleId).isEqualTo("article-42")
            }
        }
    }
}

/**
 * JUnit 5 extension to replace Dispatchers.Main with a test dispatcher.
 */
@OptIn(ExperimentalCoroutinesApi::class)
class MainDispatcherExtension : org.junit.jupiter.api.extension.BeforeEachCallback,
    org.junit.jupiter.api.extension.AfterEachCallback {

    private val testDispatcher = UnconfinedTestDispatcher()

    override fun beforeEach(context: org.junit.jupiter.api.extension.ExtensionContext?) {
        Dispatchers.setMain(testDispatcher)
    }

    override fun afterEach(context: org.junit.jupiter.api.extension.ExtensionContext?) {
        Dispatchers.resetMain()
    }
}
```

**Fake Implementations for Testing**:

```kotlin
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.flow

class FakeGetArticlesUseCase : GetArticlesUseCase(
    articleRepository = FakeArticleRepository(),
) {
    private var articles: List<Article> = emptyList()
    private var shouldFail = false

    fun setArticles(articles: List<Article>) {
        this.articles = articles
    }

    fun setShouldFail(fail: Boolean) {
        shouldFail = fail
    }

    override operator fun invoke(): Flow<List<Article>> = flow {
        if (shouldFail) {
            throw RuntimeException("Failed to load articles")
        }
        emit(articles)
    }
}

class FakeToggleBookmarkUseCase : ToggleBookmarkUseCase(
    articleRepository = FakeArticleRepository(),
) {
    private var shouldFail = false

    fun setShouldFail(fail: Boolean) {
        shouldFail = fail
    }

    override suspend operator fun invoke(articleId: String): Result<Unit> {
        return if (shouldFail) {
            Result.failure(RuntimeException("Bookmark failed"))
        } else {
            Result.success(Unit)
        }
    }
}

fun testArticle(
    id: String = "test-id",
    title: String = "Test Article",
    summary: String = "Test summary",
    isBookmarked: Boolean = false,
) = Article(
    id = id,
    title = title,
    summary = summary,
    imageUrl = null,
    publishedAt = java.time.Instant.now(),
    isBookmarked = isBookmarked,
)
```

**Compose UI Tests**:

```kotlin
import androidx.compose.ui.test.*
import androidx.compose.ui.test.junit4.createComposeRule
import org.junit.Rule
import org.junit.Test

class SearchContentTest {

    @get:Rule
    val composeTestRule = createComposeRule()

    @Test
    fun searchButton_isDisabled_whenQueryIsBlank() {
        composeTestRule.setContent {
            MyAppTheme {
                SearchContent(
                    query = "",
                    isSearching = false,
                    onQueryChange = {},
                    onSearch = {},
                )
            }
        }

        composeTestRule
            .onNodeWithText("Search")
            .assertIsNotEnabled()
    }

    @Test
    fun searchButton_isEnabled_whenQueryIsNotBlank() {
        composeTestRule.setContent {
            MyAppTheme {
                SearchContent(
                    query = "Kotlin",
                    isSearching = false,
                    onQueryChange = {},
                    onSearch = {},
                )
            }
        }

        composeTestRule
            .onNodeWithText("Search")
            .assertIsEnabled()
    }

    @Test
    fun searchButton_showsProgressIndicator_whenSearching() {
        composeTestRule.setContent {
            MyAppTheme {
                SearchContent(
                    query = "Kotlin",
                    isSearching = true,
                    onQueryChange = {},
                    onSearch = {},
                )
            }
        }

        composeTestRule
            .onNodeWithText("Searching...")
            .assertExists()

        composeTestRule
            .onNodeWithText("Searching...")
            .assertIsNotEnabled()
    }

    @Test
    fun textField_callsOnQueryChange_whenUserTypes() {
        var capturedQuery = ""
        composeTestRule.setContent {
            MyAppTheme {
                SearchContent(
                    query = "",
                    isSearching = false,
                    onQueryChange = { capturedQuery = it },
                    onSearch = {},
                )
            }
        }

        composeTestRule
            .onNodeWithText("Search", useUnmergedTree = true)
            // Find the text field by its label
            .onSiblings()
            .filterToOne(hasSetTextAction())
            .performTextInput("Android")

        assertThat(capturedQuery).isEqualTo("Android")
    }
}

class ArticleCardTest {

    @get:Rule
    val composeTestRule = createComposeRule()

    @Test
    fun articleCard_displaysTitle_andSummary() {
        val article = ArticleUiModel(
            id = "1",
            title = "Compose Testing",
            summary = "Learn to test Compose UIs",
            imageUrl = null,
            publishedAt = "2024-12-01",
            isBookmarked = false,
        )

        composeTestRule.setContent {
            MyAppTheme {
                ArticleCard(article = article)
            }
        }

        composeTestRule
            .onNodeWithText("Compose Testing")
            .assertIsDisplayed()

        composeTestRule
            .onNodeWithText("Learn to test Compose UIs")
            .assertIsDisplayed()
    }

    @Test
    fun articleCard_hasCorrectContentDescription() {
        val article = ArticleUiModel(
            id = "1",
            title = "Accessibility Test",
            summary = "Testing a11y",
            imageUrl = null,
            publishedAt = "2024-12-01",
            isBookmarked = false,
        )

        composeTestRule.setContent {
            MyAppTheme {
                ArticleCard(article = article)
            }
        }

        composeTestRule
            .onNodeWithContentDescription("Article: Accessibility Test")
            .assertExists()
    }
}
```

**Room Database Testing with Robolectric**:

```kotlin
import androidx.room.Room
import androidx.test.core.app.ApplicationProvider
import com.google.common.truth.Truth.assertThat
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.test.runTest
import org.junit.jupiter.api.AfterEach
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.extension.ExtendWith
import org.robolectric.RobolectricTestRunner

@ExtendWith(RobolectricTestRunner::class)
class ArticleDaoTest {

    private lateinit var database: AppDatabase
    private lateinit var dao: ArticleDao

    @BeforeEach
    fun setup() {
        database = Room.inMemoryDatabaseBuilder(
            ApplicationProvider.getApplicationContext(),
            AppDatabase::class.java,
        )
            .allowMainThreadQueries()
            .build()
        dao = database.articleDao()
    }

    @AfterEach
    fun teardown() {
        database.close()
    }

    @Test
    fun upsertAll_insertsNewArticles() = runTest {
        val articles = listOf(
            ArticleEntity(
                id = "1",
                title = "First",
                summary = "Summary 1",
                imageUrl = null,
                publishedAt = 1000L,
            ),
            ArticleEntity(
                id = "2",
                title = "Second",
                summary = "Summary 2",
                imageUrl = null,
                publishedAt = 2000L,
            ),
        )

        dao.upsertAll(articles)
        val result = dao.observeAll().first()

        assertThat(result).hasSize(2)
        // Ordered by published_at DESC
        assertThat(result[0].title).isEqualTo("Second")
        assertThat(result[1].title).isEqualTo("First")
    }

    @Test
    fun updateBookmark_togglesBookmarkFlag() = runTest {
        dao.upsertAll(listOf(
            ArticleEntity(
                id = "1",
                title = "Test",
                summary = "Summary",
                imageUrl = null,
                publishedAt = 1000L,
                isBookmarked = false,
            ),
        ))

        dao.updateBookmark("1", true)
        val article = dao.getById("1")

        assertThat(article).isNotNull()
        assertThat(article!!.isBookmarked).isTrue()
    }

    @Test
    fun deleteStale_removesOldArticles() = runTest {
        val now = System.currentTimeMillis()
        dao.upsertAll(listOf(
            ArticleEntity(
                id = "fresh",
                title = "Fresh",
                summary = "s",
                imageUrl = null,
                publishedAt = now,
                lastFetchedAt = now,
            ),
            ArticleEntity(
                id = "stale",
                title = "Stale",
                summary = "s",
                imageUrl = null,
                publishedAt = now - 86400000L * 10,
                lastFetchedAt = now - 86400000L * 10,
            ),
        ))

        dao.deleteStale(now - 86400000L * 7)
        val result = dao.observeAll().first()

        assertThat(result).hasSize(1)
        assertThat(result[0].id).isEqualTo("fresh")
    }
}
```

**Hilt Testing**:

```kotlin
import dagger.hilt.android.testing.HiltAndroidRule
import dagger.hilt.android.testing.HiltAndroidTest
import dagger.hilt.android.testing.HiltTestApplication
import org.junit.Before
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config
import javax.inject.Inject

/**
 * Custom test runner that uses HiltTestApplication.
 */
class HiltTestRunner : AndroidJUnitRunner() {
    override fun newApplication(
        cl: ClassLoader?,
        className: String?,
        context: android.content.Context?,
    ): Application {
        return super.newApplication(cl, HiltTestApplication::class.java.name, context)
    }
}

@HiltAndroidTest
@RunWith(RobolectricTestRunner::class)
@Config(application = HiltTestApplication::class)
class ArticleRepositoryIntegrationTest {

    @get:Rule
    val hiltRule = HiltAndroidRule(this)

    @Inject
    lateinit var articleRepository: ArticleRepository

    @Before
    fun setup() {
        hiltRule.inject()
    }

    @Test
    fun repository_returnsArticles_afterRefresh() = runTest {
        articleRepository.refreshArticles()
        val articles = articleRepository.getArticles().first()
        assertThat(articles).isNotEmpty()
    }
}
```

**Key Testing Principles**:

- Use JUnit 5 with `@Nested` classes to organize tests by behavior. Use `@DisplayName` for human-readable test descriptions
- Use Turbine (`test {}`) for testing Kotlin Flows. It provides `awaitItem()`, `awaitError()`, and `awaitComplete()` for asserting emissions
- Create a `MainDispatcherExtension` (JUnit 5) or `MainDispatcherRule` (JUnit 4) to replace `Dispatchers.Main` with a test dispatcher in ViewModel tests
- Prefer fake implementations over mocks for repositories and use cases. Fakes provide more realistic behavior and are easier to maintain
- Use `createComposeRule()` for Compose UI tests. Query elements by text, content description, or test tag rather than by implementation details
- Test Room DAOs with in-memory databases and `allowMainThreadQueries()` for synchronous assertions
- Use Robolectric to run Android-dependent tests on the JVM without an emulator, significantly speeding up the test suite

## Best Practices

- **Compose-first UI**: Build all new screens with Jetpack Compose. Use `ComposeView` to incrementally adopt Compose in existing View-based screens, but avoid mixing Compose and Views within the same screen
- **Single source of truth**: Every piece of data should have exactly one owner. The Room database is the source of truth for cached data; the ViewModel's StateFlow is the source of truth for UI state
- **Unidirectional data flow**: State flows down from ViewModel to UI; events flow up from UI to ViewModel as sealed interface actions. This makes state changes predictable and debuggable
- **Offline-first architecture**: Serve cached data from Room immediately and refresh from the network in the background. Users should always see data, even without connectivity
- **Type safety**: Use Kotlin serialization with `@Serializable` route classes for navigation, sealed interfaces for UI state, and strict Kotlin compiler flags to catch errors at compile time
- **Minimize Android framework coupling**: ViewModels, use cases, and repositories should not depend on Android classes (Context, Activity). Use Hilt to inject platform dependencies behind interfaces
- **Test at every layer**: Unit test ViewModels with Turbine, test Compose screens with ComposeTestRule, test DAOs with in-memory Room databases, and run integration tests with Hilt testing support
