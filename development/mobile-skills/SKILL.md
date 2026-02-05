---
name: mobile-skills
description: Master iOS development with Swift, Android development with Kotlin, React Native, Flutter, and cross-platform mobile technologies.
sasmp_version: "1.3.0"
skill_type: atomic
version: "2.0.0"

parameters:
  platform:
    type: string
    enum: [ios, android, cross-platform]
    default: cross-platform
  framework:
    type: string
    enum: [swift, kotlin, react-native, flutter]
    default: react-native

validation_rules:
  - pattern: "^[A-Z][a-zA-Z0-9]*$"
    target: component_names
    message: Components must be PascalCase
  - pattern: ".*\\.bundle$"
    target: ios_bundle_id
    message: Bundle ID must end with domain

retry_config:
  max_attempts: 3
  backoff: exponential
  initial_delay_ms: 500

logging:
  on_entry: "[Mobile] Starting: {task}"
  on_success: "[Mobile] Completed: {task}"
  on_error: "[Mobile] Failed: {task} - {error}"

dependencies:
  agents:
    - mobile-developer
---

# Mobile Development Skills

## iOS Development (Swift)

```swift
import SwiftUI

struct ContentView: View {
  @State private var count = 0
  @State private var isLoading = false
  @State private var error: Error?

  var body: some View {
    VStack {
      if isLoading {
        ProgressView()
      } else if let error = error {
        ErrorView(error: error, retry: loadData)
      } else {
        Text("Count: \(count)")
          .font(.headline)
        Button(action: { count += 1 }) {
          Text("Increment")
        }
      }
    }
    .task { await loadData() }
  }

  func loadData() async {
    isLoading = true
    defer { isLoading = false }
    do {
      // Fetch data
    } catch {
      self.error = error
    }
  }
}

// MVVM Pattern with Error Handling
@MainActor
class ViewModel: ObservableObject {
  @Published var items: [Item] = []
  @Published var error: Error?
  @Published var isLoading = false

  func fetchItems() async {
    isLoading = true
    defer { isLoading = false }

    do {
      items = try await APIService.getItems()
    } catch {
      self.error = error
    }
  }
}
```

## Android Development (Kotlin)

```kotlin
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.lifecycle.viewmodel.compose.viewModel

@Composable
fun CounterApp(viewModel: CounterViewModel = viewModel()) {
  val uiState by viewModel.uiState.collectAsState()

  Scaffold(
    topBar = { TopAppBar(title = { Text("Counter") }) }
  ) { padding ->
    Box(modifier = Modifier.padding(padding)) {
      when (val state = uiState) {
        is UiState.Loading -> CircularProgressIndicator()
        is UiState.Error -> ErrorMessage(state.message)
        is UiState.Success -> {
          Button(onClick = { viewModel.increment() }) {
            Text("Count: ${state.count}")
          }
        }
      }
    }
  }
}

// ViewModel with sealed class state
class CounterViewModel : ViewModel() {
  private val _uiState = MutableStateFlow<UiState>(UiState.Loading)
  val uiState: StateFlow<UiState> = _uiState.asStateFlow()

  sealed class UiState {
    object Loading : UiState()
    data class Success(val count: Int) : UiState()
    data class Error(val message: String) : UiState()
  }
}
```

## React Native with Error Boundaries

```javascript
import React, { useState, useEffect, useCallback } from 'react';
import { View, Text, Button, ActivityIndicator } from 'react-native';

export default function App() {
  const [count, setCount] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('https://api.example.com/data');
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      setCount(data.count);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  if (loading) return <ActivityIndicator />;
  if (error) return <ErrorView message={error} onRetry={fetchData} />;

  return (
    <View style={{ padding: 20 }}>
      <Text style={{ fontSize: 20 }}>Count: {count}</Text>
      <Button title="Increment" onPress={() => setCount(c => c + 1)} />
    </View>
  );
}
```

## Flutter with State Management

```dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

void main() => runApp(
  ChangeNotifierProvider(
    create: (_) => CounterProvider(),
    child: MyApp(),
  ),
);

class CounterProvider extends ChangeNotifier {
  int _count = 0;
  bool _loading = false;
  String? _error;

  int get count => _count;
  bool get loading => _loading;
  String? get error => _error;

  Future<void> increment() async {
    _loading = true;
    _error = null;
    notifyListeners();

    try {
      await Future.delayed(Duration(milliseconds: 100));
      _count++;
    } catch (e) {
      _error = e.toString();
    } finally {
      _loading = false;
      notifyListeners();
    }
  }
}

class CounterPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Consumer<CounterProvider>(
      builder: (context, provider, child) {
        if (provider.loading) return CircularProgressIndicator();
        if (provider.error != null) return ErrorWidget(provider.error!);

        return ElevatedButton(
          onPressed: () => provider.increment(),
          child: Text('Count: ${provider.count}'),
        );
      },
    );
  }
}
```

## State Management Comparison

| Framework | Solutions | Best For |
|-----------|-----------|----------|
| React Native | Redux, Zustand, Jotai | Complex global state |
| Flutter | Provider, Riverpod, Bloc | Reactive updates |
| iOS | SwiftUI @State, Combine | Declarative UI |
| Android | ViewModel, StateFlow | Lifecycle-aware |

## Mobile Best Practices

- **Performance**: Optimize bundle size, lazy loading
- **Battery**: Minimize background operations
- **Offline**: Support offline-first sync
- **Accessibility**: VoiceOver/TalkBack support
- **Security**: Keychain/Keystore for secrets
- **Testing**: Unit, widget, and integration tests

## Unit Test Template

```javascript
// React Native Test
import { render, fireEvent, waitFor } from '@testing-library/react-native';

describe('Counter', () => {
  test('increments on press', async () => {
    const { getByText } = render(<Counter />);

    fireEvent.press(getByText('Increment'));

    await waitFor(() => {
      expect(getByText('Count: 1')).toBeTruthy();
    });
  });
});
```

```swift
// Swift Test
import XCTest
@testable import MyApp

class CounterTests: XCTestCase {
  func testIncrement() async {
    let viewModel = ViewModel()
    await viewModel.increment()
    XCTAssertEqual(viewModel.count, 1)
  }
}
```

## Troubleshooting Guide

| Symptom | Platform | Solution |
|---------|----------|----------|
| EXC_BAD_ACCESS | iOS | Check retain cycles |
| ANR | Android | Move to background thread |
| Red Screen | React Native | Check JS error |
| RenderFlex overflow | Flutter | Use Expanded/Flexible |

## Key Concepts Checklist

- [ ] SwiftUI/Compose UI basics
- [ ] State management patterns
- [ ] Navigation stacks
- [ ] Network requests with retry
- [ ] Local storage (preferences, databases)
- [ ] Async operations
- [ ] Error handling
- [ ] Loading states
- [ ] Testing strategies
- [ ] Performance optimization
- [ ] App store requirements
- [ ] Code signing
- [ ] Debugging tools

---

**Source**: https://roadmap.sh
**Version**: 2.0.0
**Last Updated**: 2025-01-01
