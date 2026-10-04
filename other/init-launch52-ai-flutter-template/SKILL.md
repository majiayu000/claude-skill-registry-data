---
name: init
description: Initialize a new Flutter project. Gathers requirements, runs flutter create, adds dependencies, configures environment, and sets up main.dart. Run this first when creating a new app.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion, WebFetch
---

# Init - Project Initialization

Initialize a new Flutter project with proper architecture and dependencies.

## When to Use This Skill

- Starting a new Flutter project from scratch
- Setting up project structure before adding features
- **Run this FIRST** before any other skills

## Workflow

### Phase 1: Gather Requirements

Ask the user these questions using AskUserQuestion tool:

#### Required Information

1. **App Name** (display name, e.g., "My App")
2. **Project Name** (snake_case, e.g., "my_app")
3. **Bundle ID** (e.g., "com.company.myapp")
4. **Organization** (e.g., "com.company")
5. **Description** (short app description)

#### Backend Options

6. **Use Supabase?** (yes/no, default: yes)
7. **API Base URL** (optional, for custom REST API)

#### Authentication Methods

8. **Which auth methods?** (multi-select)
   - Social Login (Google + Apple)
   - Phone OTP
   - Email/Password

#### Design

9. **Primary Color** (hex, default: #2D9D78)
10. **Theme Mode** (light/dark/both, default: both)

### Phase 2: Create Project

```bash
# Verify Flutter is ready
flutter doctor

# Create project in current directory
flutter create --org {organization} --project-name {project_name} .
```

### Phase 3: Add Dependencies

Update `pubspec.yaml` with dependencies from [templates/pubspec_additions.yaml](templates/pubspec_additions.yaml).

Conditional dependencies:
- `supabase_flutter` - Only if Supabase = yes
- `dio` - Only if API Base URL provided
- `google_sign_in`, `sign_in_with_apple`, `crypto` - Only if Social Login selected

```bash
flutter pub get
```

### Phase 4: Configure Environment

1. Create `.env.example` from [templates/env_example.txt](templates/env_example.txt)
2. Create `.env` (copy of .env.example)
3. Add to `.gitignore` from [templates/gitignore_additions.txt](templates/gitignore_additions.txt)

### Phase 5: Setup Analysis Options

Replace `analysis_options.yaml` with [templates/analysis_options.yaml](templates/analysis_options.yaml).

### Phase 6: Modify main.dart

Update the generated `lib/main.dart`:

1. Add imports
2. Add `WidgetsFlutterBinding.ensureInitialized()`
3. Add `await dotenv.load()`
4. Add Supabase initialization (if selected)
5. Wrap app in `ProviderScope`

See [templates/main_dart.dart](templates/main_dart.dart) for the template.

### Phase 7: Create build.yaml

Create `build.yaml` for slang localization from [templates/build.yaml](templates/build.yaml).

### Phase 8: Verify Setup

```bash
flutter pub get
flutter analyze
```

## Output

After running `/init`, the project will have:

```
project/
├── lib/
│   └── main.dart           # Modified with ProviderScope, Supabase
├── pubspec.yaml            # With all dependencies
├── analysis_options.yaml   # Configured linting rules
├── build.yaml              # Slang configuration
├── .env.example            # Environment template
├── .env                    # Local environment (gitignored)
└── .gitignore              # Updated with .env, etc.
```

## Next Steps

After `/init`, run these skills in order:

### Core Setup (Required)

1. `/core` - Generate theme, router, providers, services, error handling

### Authentication (Based on your selections)

2. `/auth` - Generate auth feature scaffold
3. `/social-login` - *(If you selected Social Login)*
4. `/phone-auth` - *(If you selected Phone OTP)*

### Features

5. `/feature-init dashboard` - Initialize dashboard feature
6. `/feature-init settings` - Initialize settings feature

### Polish

7. `/i18n` - Localize all strings
8. `/testing` - Write tests
9. `/design` - Review UI/UX
10. `/a11y` - Accessibility audit

### Release (When ready)

11. `/release` - App store preparation
12. `/ci-cd` - Automated builds *(optional)*

## Stored Configuration

The skill stores gathered information for other skills to use:

```dart
// Values available to other skills:
appName: String          // "My App"
projectName: String      // "my_app"
bundleId: String         // "com.company.myapp"
organization: String     // "com.company"
description: String      // "App description"
useSupabase: bool        // true/false
apiBaseUrl: String?      // "https://api.example.com" or null
authMethods: List        // ["social", "phone", "email"]
primaryColor: String     // "#2D9D78"
themeMode: String        // "both" | "light" | "dark"
```

## Troubleshooting

### Gradle Build Fails

```bash
cd android && ./gradlew clean && ./gradlew --stop && cd ..
flutter clean && flutter pub get
```

### CocoaPods Issues

```bash
cd ios && rm -rf Pods Podfile.lock && pod install --repo-update && cd ..
```

### Flutter Doctor Issues

```bash
flutter doctor --android-licenses
flutter upgrade
```

## Guides

| Guide | Use For |
|-------|---------|
| [templates/](templates/) | pubspec additions, main.dart, env, build.yaml templates |

## Related Skills

- `/core` - Run immediately after init to create core infrastructure
- `/auth` - Add authentication after core setup
- `/feature-init` - Initialize feature scaffolds after auth

## Checklist

After running `/init`:

- [ ] `flutter create` completed successfully
- [ ] Dependencies added to pubspec.yaml
- [ ] `flutter pub get` succeeded
- [ ] `.env.example` and `.env` created
- [ ] `.gitignore` updated
- [ ] `analysis_options.yaml` configured
- [ ] `build.yaml` created
- [ ] `main.dart` modified with ProviderScope
- [ ] `flutter analyze` passes
