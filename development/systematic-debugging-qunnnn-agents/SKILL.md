---
tags: [debugging, methodology, mobile, flutter, root-cause]
applies-to: [antigravity, cursor, copilot, gemini]
level: project
---

# Systematic Debugging

## Context

Use when encountering any bug, test failure, crash, or unexpected behavior in mobile applications — before proposing fixes. This applies to Flutter, native Android/iOS, and backend services that support mobile clients.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## Instructions

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

1. **Read Error Messages Carefully**
   - Don't skip past errors, warnings, or stack traces
   - They often contain the exact solution
   - Read the full stack trace — not just the first line
   - Note line numbers, file paths, error codes
   - For Flutter: read the `══╡ EXCEPTION CAUGHT BY WIDGETS LIBRARY ╞══` blocks completely

2. **Reproduce Consistently**
   - Can you trigger it reliably?
   - What are the exact steps?
   - Does it happen on both iOS and Android?
   - Does it happen on specific device sizes, OS versions, or states?
   - If not reproducible → gather more data, don't guess

3. **Check Recent Changes**
   - What changed that could cause this?
   - `git diff`, recent commits
   - New packages, pubspec changes, native config changes
   - Xcode/Gradle version updates, CocoaPods changes
   - Environmental differences (dev vs staging vs production)

4. **Gather Evidence in Multi-Layer Systems**

   Mobile apps have multiple layers. **BEFORE proposing fixes, trace through each layer:**

   ```
   For EACH layer boundary:
     - UI Layer: What does the widget tree show? What state is the Cubit/BLoC in?
     - State Layer: What event triggered? What state was emitted?
     - Repository Layer: What was passed to the repository? What came back?
     - Network Layer: What request was sent? What response came back?
     - Backend Layer: What did the API log?

   Run once to gather evidence showing WHERE it breaks
   THEN analyze evidence to identify the failing layer
   THEN investigate that specific layer
   ```

   **Flutter example:**
   ```dart
   // Layer 1: Widget — check what state is being rendered
   BlocBuilder<AuthCubit, AuthState>(
     builder: (context, state) {
       debugPrint('=== AuthCubit state: $state ===');
       debugPrint('=== status: ${state.status} ===');
       // ...
     },
   )

   // Layer 2: Cubit — check what events flow in/out
   Future<void> login(String email, String password) async {
     debugPrint('=== login called: email=$email ===');
     emit(state.copyWith(status: ApiStatus.loading));
     try {
       final result = await _authRepository.login(email, password);
       debugPrint('=== login result: $result ===');
     } catch (e, stack) {
       debugPrint('=== login error: $e ===');
       debugPrint('=== stack: $stack ===');
     }
   }

   // Layer 3: Repository — check API call
   Future<User> login(String email, String password) async {
     debugPrint('=== API request: POST /auth/login ===');
     final response = await _dio.post('/auth/login', data: {...});
     debugPrint('=== API response: ${response.statusCode} ${response.data} ===');
     return User.fromJson(response.data);
   }
   ```

5. **Trace Data Flow**

   **WHEN error is deep in widget tree or call stack:**

   - Where does the bad value originate?
   - What called this with the bad value?
   - Keep tracing up until you find the source
   - Fix at source, not at symptom

   **Common mobile data flow traces:**
   ```
   Widget shows wrong data
     ← BlocBuilder receives wrong state
       ← Cubit emitted wrong state
         ← Repository returned wrong data
           ← API response had unexpected format
             ← Backend schema changed (ROOT CAUSE)
   ```

### Phase 2: Pattern Analysis

**Find the pattern before fixing:**

1. **Find Working Examples**
   - Locate similar working code in the same codebase
   - Another feature with the same pattern that works?
   - Same API call that works elsewhere?

2. **Compare Against References**
   - If implementing a pattern (BLoC, Retrofit, navigation), read the reference completely
   - Don't skim — read every line
   - Check the package documentation for breaking changes

3. **Identify Differences**
   - What's different between working and broken?
   - List every difference, however small
   - Don't assume "that can't matter"

4. **Understand Dependencies**
   - Package version conflicts? (`pubspec.lock` changes)
   - Native dependency issues? (CocoaPods, Gradle)
   - Platform-specific behavior? (iOS vs Android vs Web)

### Phase 3: Hypothesis and Testing

**Scientific method:**

1. **Form Single Hypothesis**
   - State clearly: "I think X is the root cause because Y"
   - Write it down
   - Be specific, not vague

2. **Test Minimally**
   - Make the SMALLEST possible change to test hypothesis
   - One variable at a time
   - Don't fix multiple things at once

3. **Verify Before Continuing**
   - Did it work? Yes → Phase 4
   - Didn't work? Form NEW hypothesis
   - DON'T add more fixes on top

4. **When You Don't Know**
   - Say "I don't understand X"
   - Don't pretend to know
   - Ask for help or research more

### Phase 4: Implementation

**Fix the root cause, not the symptom:**

1. **Create Failing Test Case**
   - Simplest possible reproduction
   - Widget test, unit test, or integration test
   - MUST have before fixing

   ```dart
   // Example: reproduce a bug where empty email passes validation
   test('rejects empty email', () {
     final cubit = LoginCubit(mockAuthRepo);
     cubit.login('', 'password123');
     expect(cubit.state.status, ApiStatus.failure);
     expect(cubit.state.errorMessage, 'Email is required');
   });
   ```

2. **Implement Single Fix**
   - Address the root cause identified
   - ONE change at a time
   - No "while I'm here" improvements
   - No bundled refactoring

3. **Verify Fix**
   - Test passes now?
   - No other tests broken?
   - Run on both iOS and Android if platform-relevant
   - Issue actually resolved?

4. **If Fix Doesn't Work**
   - STOP
   - Count: How many fixes have you tried?
   - If < 3: Return to Phase 1, re-analyze with new information
   - **If ≥ 3: STOP and question the architecture**
   - DON'T attempt Fix #4 without discussing fundamentals

5. **If 3+ Fixes Failed: Question Architecture**

   **Pattern indicating architectural problem:**
   - Each fix reveals new shared state/coupling in different place
   - Fixes require "massive refactoring" to implement
   - Each fix creates new symptoms elsewhere

   **STOP and question fundamentals:**
   - Is this widget/cubit/repository pattern fundamentally sound?
   - Should this be restructured before continuing?
   - Discuss with your human partner before attempting more fixes

## Mobile-Specific Debugging Techniques

### Platform-Specific Issues

| Symptom | Check |
|---------|-------|
| Works on Android, fails on iOS | Check `Info.plist` permissions, iOS-specific native code, CocoaPods |
| Works on iOS, fails on Android | Check `AndroidManifest.xml` permissions, ProGuard rules, Gradle config |
| Works in debug, fails in release | Check tree-shaking, `--dart-define`, ProGuard/R8, code signing |
| Works locally, fails in CI | Check environment variables, signing certs, build agent config |
| Crash on app start | Check native initialization order, missing Firebase config, deep link setup |

### Flutter-Specific Patterns

```dart
// 🔍 Debug widget rebuild causes
class MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    debugPrint('=== MyWidget.build called ===');
    return ...;
  }
}

// 🔍 Debug BLoC state transitions
class MyCubit extends Cubit<MyState> {
  @override
  void onChange(Change<MyState> change) {
    super.onChange(change);
    debugPrint('=== ${change.currentState} → ${change.nextState} ===');
  }
}

// 🔍 Debug network calls (Dio interceptor)
dio.interceptors.add(LogInterceptor(
  requestBody: true,
  responseBody: true,
  error: true,
));

// 🔍 Debug navigation
GoRouter(
  debugLogDiagnostics: true, // Logs all route changes
  ...
);
```

### Build & Native Issues

```bash
# Flutter doctor — always check first
flutter doctor -v

# Clean everything when builds fail
flutter clean && rm -rf ios/Pods ios/Podfile.lock && flutter pub get && cd ios && pod install

# Check for package conflicts
flutter pub deps -- --style=compact

# Android build issues
cd android && ./gradlew --stacktrace assembleDebug

# iOS build issues — check Xcode logs
open ios/Runner.xcworkspace  # Build from Xcode for better error messages
```

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Let me add a `try-catch` around it"
- "It's probably a package version issue, let me upgrade"
- "Let me just add `?.` or `!` to fix the null check"
- "I'll wrap it in a `setState` / `Future.delayed`"
- "It works on my device, probably a device-specific issue"
- Proposing solutions before tracing data flow
- **"One more fix attempt" (when already tried 2+)**

**ALL of these mean: STOP. Return to Phase 1.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, production crash" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try a `flutter clean` first" | That's a workaround. If it works, you still don't know the root cause. |
| "Add a null check and move on" | You masked the symptom. The null came from somewhere — find it. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new bugs. |
| "I see the problem, let me fix it" | Seeing symptoms ≠ understanding root cause. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. Question the pattern. |

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|-----------------|
| **1. Root Cause** | Read errors, reproduce, check changes, trace layers | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare differences | Identify what's different |
| **3. Hypothesis** | Form theory, test minimally, one variable | Confirmed or new hypothesis |
| **4. Implementation** | Create test, fix, verify on all platforms | Bug resolved, tests pass |

## Anti-patterns

- ❌ Adding `try-catch` around everything without understanding the error
- ❌ Sprinkling `?.` and `!` to silence null safety warnings
- ❌ Using `Future.delayed` to "fix" race conditions in UI
- ❌ Upgrading packages hoping the bug goes away
- ❌ Running `flutter clean` as a fix instead of understanding the build error
- ❌ Proposing 3+ possible fixes simultaneously ("try A, or B, or C")
- ❌ Ignoring platform-specific differences ("it works on Android, ship it")
- ❌ Fixing the test instead of the code when a test fails
