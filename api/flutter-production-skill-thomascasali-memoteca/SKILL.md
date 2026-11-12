---
name: flutter-production
description: Build production-grade Flutter apps with Firebase or custom API backends. Use when creating apps requiring Firebase Auth (Google Sign-In), Firestore real-time database, push notifications (FCM), RTMP streaming, WebSocket real-time (Pusher), JWT authentication, background services, or Play Store/TestFlight deployment. Covers both Riverpod and Provider state management, feature-based architecture, ProGuard configuration, iOS/Android release builds, and common troubleshooting patterns.
---

# Flutter Production Development

Production-grade Flutter architecture for mobile apps with real-time features, authentication, and cloud backends.

## When to Use This Skill

This skill covers two main app profiles:

| Profile | Use Case | Key Technologies |
|---------|----------|------------------|
| **Firebase Apps** | Collaborative apps, social features, real-time sync | Firebase Auth, Firestore, FCM, Riverpod |
| **Streaming Apps** | Live video, custom backends, media | RTMP, Pusher, JWT/Laravel, Provider |

**Trigger keywords**: Firebase, Firestore, Riverpod, Google Sign-In, FCM, push notifications, RTMP streaming, Pusher, WebSocket, JWT, release build, Play Store, TestFlight

## Project Structure

### Firebase Apps (Riverpod + Feature-based)

```
lib/
├── main.dart
├── app.dart
├── core/
│   ├── config/
│   │   └── firebase_options.dart
│   ├── constants/
│   │   ├── app_colors.dart
│   │   └── app_strings.dart
│   ├── router/
│   │   └── app_router.dart       # GoRouter
│   └── utils/
│       ├── extensions.dart
│       └── validators.dart
├── features/
│   ├── auth/
│   │   ├── data/
│   │   │   ├── models/
│   │   │   │   └── user_model.dart
│   │   │   └── repositories/
│   │   │       └── auth_repository.dart
│   │   └── presentation/
│   │       ├── providers/
│   │       │   └── auth_provider.dart
│   │       ├── screens/
│   │       │   ├── login_screen.dart
│   │       │   └── splash_screen.dart
│   │       └── widgets/
│   │           └── google_sign_in_button.dart
│   ├── lists/
│   │   ├── data/
│   │   └── presentation/
│   └── tasks/
│       ├── data/
│       └── presentation/
├── shared/
│   ├── widgets/
│   │   ├── loading_indicator.dart
│   │   └── error_widget.dart
│   └── providers/
│       └── firebase_providers.dart
└── firebase_options.dart
```

### Streaming/API Apps (Provider + Service-based)

```
lib/
├── config/
│   ├── api_config.dart           # Base URLs, endpoints
│   └── app_config.dart           # Constants, feature flags
├── models/
│   └── user.dart                 # Data classes with fromJson
├── services/
│   ├── auth_service.dart         # JWT auth, token refresh
│   ├── api_service.dart          # Dio with interceptors
│   ├── streaming_service.dart    # RTMP controller
│   └── realtime_service.dart     # Pusher/WebSocket
├── providers/
│   └── auth_provider.dart        # ChangeNotifier state
├── screens/
│   ├── auth/
│   ├── home/
│   └── streaming/
├── widgets/
└── utils/
```

## Core Dependencies

### Firebase Apps (pubspec.yaml)

```yaml
dependencies:
  flutter:
    sdk: flutter

  # Firebase
  firebase_core: ^3.8.1
  firebase_auth: ^5.3.4
  cloud_firestore: ^5.6.0
  firebase_messaging: ^15.1.5
  firebase_storage: ^12.3.7

  # Google Sign In
  google_sign_in: ^6.2.2

  # State Management
  flutter_riverpod: ^2.6.1
  riverpod_annotation: ^2.6.1

  # Navigation
  go_router: ^14.6.2

  # UI
  cached_network_image: ^3.4.1
  flutter_svg: ^2.0.16
  intl: ^0.20.1

  # Utilities
  url_launcher: ^6.3.1
  flutter_local_notifications: ^18.0.1
  shared_preferences: ^2.3.4
  uuid: ^4.5.1

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^5.0.0
  riverpod_generator: ^2.6.2
  build_runner: ^2.4.13
  mocktail: ^1.0.4
```

### Streaming Apps (pubspec.yaml)

```yaml
dependencies:
  flutter:
    sdk: flutter

  # State
  provider: ^6.1.2

  # Network
  dio: ^5.7.0
  web_socket_channel: ^3.0.1
  pusher_channels_flutter: ^2.2.1

  # Auth & Storage
  flutter_secure_storage: ^9.2.2
  hive_flutter: ^1.1.0

  # Streaming
  camera: ^0.11.0+2
  apivideo_live_stream: ^1.2.0
  wakelock_plus: ^1.2.10
  permission_handler: ^11.3.1

  # Background
  flutter_foreground_task: ^8.14.0

  # Firebase (notifications only)
  firebase_core: ^3.8.1
  firebase_messaging: ^15.1.5
  flutter_local_notifications: ^18.0.1
```

## Essential Patterns

### 1. App Entry Point with Firebase

```dart
// main.dart
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'firebase_options.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );

  runApp(const ProviderScope(child: MyApp()));
}
```

### 2. GoRouter with Auth Redirect

```dart
// core/router/app_router.dart
final routerProvider = Provider<GoRouter>((ref) {
  final authState = ref.watch(authStateProvider);

  return GoRouter(
    initialLocation: '/',
    redirect: (context, state) {
      final isLoggedIn = authState.valueOrNull != null;
      final isAuthRoute = state.matchedLocation == '/login';

      if (!isLoggedIn && !isAuthRoute) return '/login';
      if (isLoggedIn && isAuthRoute) return '/';
      return null;
    },
    routes: [
      GoRoute(path: '/', builder: (_, __) => const HomeScreen()),
      GoRoute(path: '/login', builder: (_, __) => const LoginScreen()),
      GoRoute(
        path: '/list/:id',
        builder: (_, state) => ListDetailScreen(
          listId: state.pathParameters['id']!,
        ),
      ),
    ],
  );
});
```

### 3. Riverpod Auth Provider

```dart
// features/auth/presentation/providers/auth_provider.dart
@riverpod
Stream<User?> authState(Ref ref) {
  return FirebaseAuth.instance.authStateChanges();
}

@riverpod
class AuthNotifier extends _$AuthNotifier {
  @override
  FutureOr<UserModel?> build() async {
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) return null;

    final doc = await FirebaseFirestore.instance
        .collection('users')
        .doc(user.uid)
        .get();

    return doc.exists ? UserModel.fromFirestore(doc) : null;
  }

  Future<void> signInWithGoogle() async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(() async {
      final googleUser = await GoogleSignIn().signIn();
      if (googleUser == null) throw Exception('Sign in cancelled');

      final googleAuth = await googleUser.authentication;
      final credential = GoogleAuthProvider.credential(
        accessToken: googleAuth.accessToken,
        idToken: googleAuth.idToken,
      );

      final userCred = await FirebaseAuth.instance
          .signInWithCredential(credential);

      return _createOrGetUser(userCred.user!);
    });
  }

  Future<UserModel> _createOrGetUser(User user) async {
    final docRef = FirebaseFirestore.instance
        .collection('users')
        .doc(user.uid);

    final doc = await docRef.get();
    if (doc.exists) {
      await docRef.update({'lastLoginAt': FieldValue.serverTimestamp()});
      return UserModel.fromFirestore(doc);
    }

    final newUser = UserModel(
      uid: user.uid,
      email: user.email!,
      displayName: user.displayName ?? '',
      photoURL: user.photoURL,
      isApproved: false,
      isAdmin: false,
      createdAt: DateTime.now(),
    );

    await docRef.set(newUser.toFirestore());
    return newUser;
  }

  Future<void> signOut() async {
    await GoogleSignIn().signOut();
    await FirebaseAuth.instance.signOut();
    state = const AsyncData(null);
  }
}
```

### 4. Firestore Repository Pattern

```dart
// features/lists/data/repositories/lists_repository.dart
@riverpod
ListsRepository listsRepository(Ref ref) => ListsRepository();

class ListsRepository {
  final _firestore = FirebaseFirestore.instance;

  CollectionReference<Map<String, dynamic>> get _collection =>
      _firestore.collection('lists');

  // Real-time stream
  Stream<List<TodoList>> watchUserLists(String userId) {
    return _collection
        .where('members', arrayContains: userId)
        .orderBy('updatedAt', descending: true)
        .snapshots()
        .map((snapshot) => snapshot.docs
            .map((doc) => TodoList.fromFirestore(doc))
            .toList());
  }

  // Single fetch
  Future<TodoList?> getList(String listId) async {
    final doc = await _collection.doc(listId).get();
    return doc.exists ? TodoList.fromFirestore(doc) : null;
  }

  // Create with auto-ID
  Future<String> createList(TodoList list) async {
    final docRef = await _collection.add(list.toFirestore());
    return docRef.id;
  }

  // Update
  Future<void> updateList(String listId, Map<String, dynamic> data) async {
    await _collection.doc(listId).update({
      ...data,
      'updatedAt': FieldValue.serverTimestamp(),
    });
  }

  // Delete with subcollections
  Future<void> deleteList(String listId) async {
    final batch = _firestore.batch();

    // Delete tasks subcollection
    final tasks = await _collection.doc(listId).collection('tasks').get();
    for (final doc in tasks.docs) {
      batch.delete(doc.reference);
    }

    // Delete list
    batch.delete(_collection.doc(listId));
    await batch.commit();
  }

  // Add member
  Future<void> addMember(String listId, String userId, String role) async {
    await _collection.doc(listId).update({
      'members': FieldValue.arrayUnion([userId]),
      'permissions.$userId': role,
      'updatedAt': FieldValue.serverTimestamp(),
    });
  }
}
```

### 5. Model with Firestore Serialization

```dart
// features/lists/data/models/todo_list_model.dart
import 'package:cloud_firestore/cloud_firestore.dart';

class TodoList {
  final String id;
  final String title;
  final String? description;
  final String ownerId;
  final List<String> members;
  final Map<String, String> permissions;
  final DateTime createdAt;
  final DateTime updatedAt;

  const TodoList({
    required this.id,
    required this.title,
    this.description,
    required this.ownerId,
    required this.members,
    required this.permissions,
    required this.createdAt,
    required this.updatedAt,
  });

  factory TodoList.fromFirestore(DocumentSnapshot<Map<String, dynamic>> doc) {
    final data = doc.data()!;
    return TodoList(
      id: doc.id,
      title: data['title'] ?? '',
      description: data['description'],
      ownerId: data['ownerId'] ?? '',
      members: List<String>.from(data['members'] ?? []),
      permissions: Map<String, String>.from(data['permissions'] ?? {}),
      createdAt: (data['createdAt'] as Timestamp?)?.toDate() ?? DateTime.now(),
      updatedAt: (data['updatedAt'] as Timestamp?)?.toDate() ?? DateTime.now(),
    );
  }

  Map<String, dynamic> toFirestore() => {
    'title': title,
    'description': description,
    'ownerId': ownerId,
    'members': members,
    'permissions': permissions,
    'createdAt': Timestamp.fromDate(createdAt),
    'updatedAt': FieldValue.serverTimestamp(),
  };

  TodoList copyWith({
    String? title,
    String? description,
    List<String>? members,
    Map<String, String>? permissions,
  }) {
    return TodoList(
      id: id,
      title: title ?? this.title,
      description: description ?? this.description,
      ownerId: ownerId,
      members: members ?? this.members,
      permissions: permissions ?? this.permissions,
      createdAt: createdAt,
      updatedAt: DateTime.now(),
    );
  }
}
```

### 6. FCM Push Notifications (Both Profiles)

```dart
// services/notification_service.dart
class NotificationService {
  final _messaging = FirebaseMessaging.instance;
  final _localNotifications = FlutterLocalNotificationsPlugin();

  Future<void> initialize({
    required Function(RemoteMessage) onMessage,
    required Function(RemoteMessage) onMessageOpenedApp,
  }) async {
    // Request permissions
    final settings = await _messaging.requestPermission(
      alert: true,
      badge: true,
      sound: true,
      provisional: false,
    );

    if (settings.authorizationStatus != AuthorizationStatus.authorized) {
      debugPrint('FCM: Permission denied');
      return;
    }

    // Initialize local notifications for foreground
    await _localNotifications.initialize(
      const InitializationSettings(
        android: AndroidInitializationSettings('@mipmap/ic_launcher'),
        iOS: DarwinInitializationSettings(),
      ),
      onDidReceiveNotificationResponse: (response) {
        // Handle notification tap
        debugPrint('Notification tapped: ${response.payload}');
      },
    );

    // Create notification channel (Android)
    await _createAndroidChannel();

    // Foreground messages
    FirebaseMessaging.onMessage.listen((message) {
      _showLocalNotification(message);
      onMessage(message);
    });

    // Background -> app opened
    FirebaseMessaging.onMessageOpenedApp.listen(onMessageOpenedApp);

    // App opened from terminated state
    final initial = await _messaging.getInitialMessage();
    if (initial != null) {
      onMessageOpenedApp(initial);
    }
  }

  Future<void> _createAndroidChannel() async {
    const channel = AndroidNotificationChannel(
      'high_importance',
      'High Importance Notifications',
      importance: Importance.high,
    );

    await _localNotifications
        .resolvePlatformSpecificImplementation<
            AndroidFlutterLocalNotificationsPlugin>()
        ?.createNotificationChannel(channel);
  }

  Future<void> _showLocalNotification(RemoteMessage message) async {
    final notification = message.notification;
    if (notification == null) return;

    await _localNotifications.show(
      notification.hashCode,
      notification.title,
      notification.body,
      const NotificationDetails(
        android: AndroidNotificationDetails(
          'high_importance',
          'High Importance Notifications',
          importance: Importance.high,
          priority: Priority.high,
        ),
        iOS: DarwinNotificationDetails(),
      ),
      payload: message.data.toString(),
    );
  }

  Future<String?> getToken() => _messaging.getToken();

  void onTokenRefresh(Function(String) callback) {
    _messaging.onTokenRefresh.listen(callback);
  }

  Future<void> saveTokenToFirestore(String userId) async {
    final token = await getToken();
    if (token == null) return;

    await FirebaseFirestore.instance
        .collection('users')
        .doc(userId)
        .update({'fcmToken': token});
  }
}
```

## Android Configuration

### AndroidManifest.xml

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <!-- Internet -->
    <uses-permission android:name="android.permission.INTERNET"/>
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>

    <!-- Notifications -->
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS"/>
    <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED"/>
    <uses-permission android:name="android.permission.VIBRATE"/>

    <!-- Camera/Audio (streaming apps only) -->
    <uses-permission android:name="android.permission.CAMERA"/>
    <uses-permission android:name="android.permission.RECORD_AUDIO"/>

    <!-- Background Services -->
    <uses-permission android:name="android.permission.WAKE_LOCK"/>
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE"/>
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE_CAMERA"
        android:minSdkVersion="34"/>
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE_MICROPHONE"
        android:minSdkVersion="34"/>

    <!-- Features -->
    <uses-feature android:name="android.hardware.camera" android:required="false"/>
    <uses-feature android:name="android.hardware.camera.autofocus" android:required="false"/>

    <application
        android:label="@string/app_name"
        android:icon="@mipmap/ic_launcher">

        <!-- FCM default channel -->
        <meta-data
            android:name="com.google.firebase.messaging.default_notification_channel_id"
            android:value="high_importance" />

        <!-- Deep links -->
        <intent-filter android:autoVerify="true">
            <action android:name="android.intent.action.VIEW"/>
            <category android:name="android.intent.category.DEFAULT"/>
            <category android:name="android.intent.category.BROWSABLE"/>
            <data android:scheme="https"
                  android:host="yourdomain.com"
                  android:pathPrefix="/invite"/>
        </intent-filter>

        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:launchMode="singleTop">
            <!-- ... -->
        </activity>
    </application>
</manifest>
```

### ProGuard Rules (proguard-rules.pro)

```proguard
# Flutter
-keep class io.flutter.** { *; }
-keep class io.flutter.plugins.** { *; }

# Firebase
-keep class com.google.firebase.** { *; }
-dontwarn com.google.firebase.**
-keep class com.google.android.gms.** { *; }
-dontwarn com.google.android.gms.**

# Google Sign In
-keep class com.google.android.gms.auth.** { *; }

# Firestore
-keep class com.google.firestore.** { *; }
-keep class io.grpc.** { *; }

# Streaming (if used)
-keep class com.apivideo.** { *; }
-keep class com.pusher.** { *; }
-dontwarn com.pusher.**

# HTTP/OkHttp
-dontwarn okhttp3.**
-dontwarn okio.**
-keep class okhttp3.** { *; }
-keep class okio.** { *; }

# Gson (Firestore serialization)
-keep class * extends com.google.gson.TypeAdapter
-keep class * implements com.google.gson.TypeAdapterFactory
-keep class * implements com.google.gson.JsonSerializer
-keep class * implements com.google.gson.JsonDeserializer

# Keep model classes
-keep class **.models.** { *; }
-keep class **.data.** { *; }

# Remove debug logs in release
-assumenosideeffects class android.util.Log {
    public static *** d(...);
    public static *** v(...);
}
```

### build.gradle.kts Release Config

```kotlin
android {
    // ...

    signingConfigs {
        create("release") {
            keyAlias = System.getenv("KEY_ALIAS") ?: properties["keyAlias"] as String?
            keyPassword = System.getenv("KEY_PASSWORD") ?: properties["keyPassword"] as String?
            storeFile = file(System.getenv("STORE_FILE") ?: properties["storeFile"] as String? ?: "")
            storePassword = System.getenv("STORE_PASSWORD") ?: properties["storePassword"] as String?
        }
    }

    buildTypes {
        release {
            signingConfig = signingConfigs.getByName("release")
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
}
```

## iOS Configuration

See `references/ios-setup.md` for complete iOS configuration including:
- Info.plist permissions
- APNs setup for FCM
- Google Sign-In URL schemes
- Deep linking with Associated Domains

## Best Practices

**DO:**
- Use `const` constructors everywhere possible
- Separate data layer (repositories) from presentation (providers)
- Handle all async states: loading, error, data
- Dispose streams and controllers properly
- Test on real devices (especially notifications and streaming)
- Use Firestore batch writes for related operations
- Implement proper error boundaries

**DON'T:**
- Call `notifyListeners()` after dispose (Provider)
- Make network calls in `build()` methods
- Store sensitive data in SharedPreferences (use flutter_secure_storage)
- Forget ProGuard rules for release builds
- Skip iOS configuration for FCM (APNs required)
- Ignore lifecycle management for streaming apps

## Reference Files

For detailed patterns, see:
- `references/firebase-patterns.md` - Auth, Firestore queries, Security Rules
- `references/api-streaming.md` - Dio, JWT, RTMP, Pusher patterns
- `references/ios-setup.md` - Complete iOS configuration
- `references/troubleshooting.md` - Common issues and fixes
