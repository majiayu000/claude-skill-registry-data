---
name: mobile-development-skill
description: Master iOS, Android, React Native, and Flutter development. Build native and cross-platform mobile apps with modern frameworks, handle platform-specific features, optimize performance, and deploy to app stores.
---

# Mobile Development Skill

Build powerful mobile applications across iOS, Android, and cross-platform platforms.

## Quick Start

### Choose Your Platform

```
Native Only              Cross-Platform
├─ iOS (Swift)          ├─ React Native
├─ Android (Kotlin)     └─ Flutter
```

### Decision Matrix

|  | iOS | Android | React Native | Flutter |
|---|---|---|---|---|
| **Learning Curve** | Medium | Medium | Easy (know JS) | Medium |
| **Performance** | Excellent | Excellent | Very Good | Excellent |
| **Code Sharing** | None | None | 70% | 80%+ |
| **Market Share** | 25% | 72% | Common | Growing |
| **Team Skills** | Xcode, Swift | Android Studio, Kotlin | JS/React | Dart |

---

## iOS Development

### **Swift Fundamentals**

```swift
// Variables and types
var name: String = "Alice"
let age: Int = 30  // immutable

// Optionals (handle nil safely)
var email: String? = nil
if let email = email {
    print("Email: \(email)")
}

// Functions
func greet(_ name: String) -> String {
    return "Hello, \(name)!"
}

// Classes vs Structs
class Person {
    var name: String
    init(name: String) {
        self.name = name
    }
}

struct Address {
    var street: String
    var city: String
}

// Extensions (add methods to existing types)
extension String {
    func capitalized() -> String {
        return self.prefix(1).uppercased() + self.dropFirst()
    }
}
```

### **SwiftUI (Modern Approach)**

```swift
import SwiftUI

struct ContentView: View {
    @State private var count = 0
    @State private var name: String = ""

    var body: some View {
        VStack(spacing: 20) {
            Text("Hello, World!")
                .font(.title)
                .foregroundColor(.blue)

            TextField("Enter name", text: $name)
                .textFieldStyle(.roundedBorder)
                .padding()

            Button(action: { count += 1 }) {
                Text("Count: \(count)")
                    .font(.headline)
                    .foregroundColor(.white)
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Color.blue)
                    .cornerRadius(10)
            }

            List {
                ForEach(0..<5, id: \.self) { index in
                    Text("Item \(index)")
                }
            }
        }
        .padding()
    }
}

// Preview
#Preview {
    ContentView()
}
```

### **iOS Lifecycle & Navigation**

```swift
// App Delegate (lifecycle)
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

// Navigation
NavigationStack {
    VStack {
        NavigationLink(value: 42) {
            Text("Go to Details")
        }
    }
    .navigationDestination(for: Int.self) { id in
        DetailView(id: id)
    }
}
```

### **Networking & Async/Await**

```swift
struct User: Codable {
    let id: Int
    let name: String
    let email: String
}

// MVVM Pattern
@MainActor
class UserViewModel: ObservableObject {
    @Published var users: [User] = []
    @Published var isLoading = false
    @Published var error: String?

    func fetchUsers() async {
        isLoading = true
        defer { isLoading = false }

        do {
            let url = URL(string: "https://api.example.com/users")!
            let (data, _) = try await URLSession.shared.data(from: url)
            users = try JSONDecoder().decode([User].self, from: data)
        } catch {
            self.error = error.localizedDescription
        }
    }
}

// Use in View
struct UserListView: View {
    @StateObject private var viewModel = UserViewModel()

    var body: some View {
        List(viewModel.users) { user in
            VStack(alignment: .leading) {
                Text(user.name).font(.headline)
                Text(user.email).font(.caption)
            }
        }
        .task {
            await viewModel.fetchUsers()
        }
    }
}
```

---

## Android Development

### **Kotlin Fundamentals**

```kotlin
// Variables
var name: String = "Alice"
val age: Int = 30  // immutable

// Nullable types
var email: String? = null
email?.let { println(it) }  // Safe call

// Functions
fun greet(name: String): String = "Hello, $name!"

// Data classes
data class User(val id: Int, val name: String, val email: String)

// Extension functions
fun <T> List<T>.printAll() {
    forEach { println(it) }
}

// Higher-order functions
val numbers = listOf(1, 2, 3, 4, 5)
numbers
    .filter { it > 2 }
    .map { it * 2 }
    .forEach { println(it) }
```

### **Jetpack Compose (Modern UI)**

```kotlin
import androidx.compose.material3.*
import androidx.compose.runtime.*

@Composable
fun UserProfile(userId: String) {
    var user by remember { mutableStateOf<User?>(null) }
    var isLoading by remember { mutableStateOf(true) }

    LaunchedEffect(userId) {
        user = fetchUser(userId)
        isLoading = false
    }

    Scaffold(
        topBar = { TopAppBar(title = { Text("Profile") }) }
    ) { padding ->
        Box(modifier = Modifier.padding(padding)) {
            when {
                isLoading -> CircularProgressIndicator()
                user != null -> {
                    Column {
                        Text(user!!.name, style = MaterialTheme.typography.headlineMedium)
                        Text(user!!.email)
                    }
                }
            }
        }
    }
}

@Preview
@Composable
fun PreviewUserProfile() {
    UserProfile("123")
}
```

### **Android Lifecycle & Architecture**

```kotlin
// MVVM with LiveData
class UserViewModel : ViewModel() {
    private val _users = MutableLiveData<List<User>>()
    val users: LiveData<List<User>> = _users

    fun loadUsers() {
        viewModelScope.launch {
            try {
                val data = apiService.getUsers()
                _users.value = data
            } catch (e: Exception) {
                // Handle error
            }
        }
    }
}

// Activity
class MainActivity : AppCompatActivity() {
    private val viewModel: UserViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        viewModel.users.observe(this) { users ->
            adapter.submitList(users)
        }

        viewModel.loadUsers()
    }
}
```

### **Networking with Retrofit**

```kotlin
interface ApiService {
    @GET("users")
    suspend fun getUsers(): List<User>

    @POST("users")
    suspend fun createUser(@Body user: User): User

    @GET("users/{id}")
    suspend fun getUser(@Path("id") id: Int): User
}

// Dependency Injection (Hilt)
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {
    @Provides
    fun provideApiService(): ApiService {
        return Retrofit.Builder()
            .baseUrl("https://api.example.com/")
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ApiService::class.java)
    }
}
```

---

## React Native

### **Setup & Basics**

```javascript
import React, { useState, useEffect } from 'react';
import { View, Text, ScrollView, TouchableOpacity } from 'react-native';

export default function App() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await fetch('https://api.example.com/users');
      const data = await response.json();
      setUsers(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView>
      {loading ? (
        <Text>Loading...</Text>
      ) : (
        users.map(user => (
          <TouchableOpacity key={user.id}>
            <Text>{user.name}</Text>
          </TouchableOpacity>
        ))
      )}
    </ScrollView>
  );
}
```

### **Navigation (React Navigation)**

```javascript
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';

const Tab = createBottomTabNavigator();

function HomeStack() {
  return (
    <Stack.Navigator>
      <Stack.Screen name="Home" component={HomeScreen} />
      <Stack.Screen name="Details" component={DetailsScreen} />
    </Stack.Navigator>
  );
}

export default function App() {
  return (
    <NavigationContainer>
      <Tab.Navigator>
        <Tab.Screen name="Home" component={HomeStack} />
        <Tab.Screen name="Settings" component={SettingsScreen} />
      </Tab.Navigator>
    </NavigationContainer>
  );
}
```

### **Native Modules**

```javascript
// JavaScript side
import { NativeModules } from 'react-native';

const { CameraModule } = NativeModules;

CameraModule.takePhoto().then(uri => {
  console.log('Photo saved to:', uri);
});
```

---

## Flutter

### **Dart Fundamentals**

```dart
// Variables
String name = "Alice";
int age = 30;
final email = "alice@example.com";  // Type inference
const PI = 3.14159;  // Compile-time constant

// Functions
String greet(String name) => "Hello, $name!";

// Classes
class User {
  final String name;
  final String email;

  User({required this.name, required this.email});

  factory User.fromJson(Map json) {
    return User(name: json['name'], email: json['email']);
  }
}

// Collections
List<int> numbers = [1, 2, 3, 4, 5];
Map<String, int> scores = {'Alice': 100, 'Bob': 95};
Set<String> tags = {'flutter', 'dart', 'mobile'};

// Async/await
Future<User> fetchUser(int id) async {
  final response = await http.get(Uri.parse('/users/$id'));
  return User.fromJson(jsonDecode(response.body));
}
```

### **Flutter UI with Widgets**

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: const HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  int count = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Home')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text('Count:'),
            Text('$count', style: const TextStyle(fontSize: 32)),
            ElevatedButton(
              onPressed: () {
                setState(() => count++);
              },
              child: const Text('Increment'),
            ),
          ],
        ),
      ),
    );
  }
}
```

### **State Management with Provider**

```dart
class UserProvider extends ChangeNotifier {
  List<User> _users = [];
  bool _loading = false;

  List<User> get users => _users;
  bool get loading => _loading;

  Future<void> fetchUsers() async {
    _loading = true;
    notifyListeners();

    try {
      _users = await apiService.getUsers();
    } finally {
      _loading = false;
      notifyListeners();
    }
  }
}

// In widget
class UserListScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (_) => UserProvider(),
      child: Consumer<UserProvider>(
        builder: (context, provider, _) {
          provider.fetchUsers();  // Load data

          if (provider.loading) return CircularProgressIndicator();

          return ListView.builder(
            itemCount: provider.users.length,
            itemBuilder: (_, index) {
              final user = provider.users[index];
              return ListTile(title: Text(user.name));
            },
          );
        },
      ),
    );
  }
}
```

---

## Mobile Best Practices

### **Performance**
- Minimize bundle size
- Optimize images (WebP, multiple resolutions)
- Use lazy loading for lists
- Profile with DevTools
- Memory management (dispose resources)

### **Security**
- Store sensitive data securely (Keychain/Keystore)
- Use HTTPS only
- Validate all inputs
- Implement certificate pinning
- Don't log sensitive data

### **User Experience**
- Handle offline scenarios
- Smooth animations (60 FPS)
- Responsive to screen sizes
- Clear error messages
- Accessibility support

### **Deployment**

**iOS App Store:**
```
1. Create Apple ID
2. Generate certificates
3. Build archive in Xcode
4. Submit to TestFlight (beta)
5. Submit to App Store
```

**Google Play:**
```
1. Create Google Play account
2. Generate key store
3. Build release APK/AAB
4. Submit with screenshots
5. Gradual rollout option
```

---

## Learning Checklist

- [ ] Understand mobile OS basics
- [ ] Know which platform to start with
- [ ] Can build basic UI
- [ ] Understand component/widget lifecycle
- [ ] Can fetch data from APIs
- [ ] Know state management
- [ ] Built 1-2 complete apps
- [ ] Can deploy to store/emulator
- [ ] Understand platform differences
- [ ] Ready for mobile developer role!

---

**Source**: https://roadmap.sh/ios, https://roadmap.sh/android, https://roadmap.sh/react-native, https://roadmap.sh/flutter
