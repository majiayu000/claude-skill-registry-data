---
name: flutter-gemma-scaffold
description: |
  Use this skill when you need to add Gemma 4 on-device AI to a Flutter project. Handles: integrating flutter_gemma package, configuring iOS/Android/Web/Desktop platforms, model installation and loading, basic inference, function calling, multimodal input, and streaming responses. For developers building offline-capable AI features with local LLM inference.
triggers:
  - integrate Gemma
  - on-device LLM
  - offline AI
  - flutter_gemma
  - local AI model
  - mobile AI
  - edge AI
  - run Gemma locally
  - Flutter AI
  - local LLM
---

# Flutter Gemma Scaffold

Scaffold guide for integrating Gemma 4 on-device AI into Flutter projects.

## Capabilities

1. **Create new** Flutter project with Gemma integration from scratch
2. **Add Gemma** to existing Flutter project
3. **Configure platforms** (iOS, Android, Web, Desktop)

---

## Workflow

### Step 1: Confirm Requirements

Ask the user:
1. New project or existing project?
2. Target platform(s)? (iOS/Android/Web/All)
3. Need function calling support?
4. Have HuggingFace token? (for model downloads)

### Step 2: Add Dependencies

In `pubspec.yaml`:

```yaml
dependencies:
  flutter: sdk: flutter
  flutter_gemma: ^0.13.2
  flutter_riverpod: ^2.5.0
  riverpod_annotation: ^2.3.0
  go_router: ^14.0.0

dev_dependencies:
  build_runner: ^2.4.0
  riverpod_generator: ^2.4.0
  flutter_lints: ^4.0.0

flutter:
  uses-material-design: true
```

### Step 2b: Initialize Riverpod

Wrap your app with `ProviderScope` in `main.dart`:

```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';

void main() {
  runApp(
    const ProviderScope(
      child: MyApp(),
    ),
  );
}
```

### Step 3: Platform Configuration

#### iOS (`ios/Podfile`)

```ruby
platform :ios, '16.0'
use_frameworks! :linkage => :static
```

iOS 16.0+ required. Static linking required.

#### Android (`android/app/build.gradle.kts`)

```kotlin
android {
    defaultConfig {
        minSdk = 24  // Android 7.0+
    }
}
```

Optional GPU acceleration (requires OpenCL):
```xml
<uses-native-library android:name="libOpenCL.so" android:required="false"/>
<uses-native-library android:name="libOpenCL-car.so" android:required="false"/>
<uses-native-library android:name="libOpenCL-pixel.so" android:required="false"/>
```

#### Web (`web/index.html`)

In `<head>`:
```html
<script type="module">
  import { FilesetResolver, LlmInference } from 'https://cdn.jsdelivr.net/npm/@mediapipe/tasks-genai@0.10.27';
  window.FilesetResolver = FilesetResolver;
  window.LlmInference = LlmInference;
</script>
```

### Step 4: Model Installation

#### Recommended Models

| Model | Size | Memory | Best For |
|-------|------|--------|----------|
| Gemma 4 E2B Q4_K_M | ~3.5GB | <1.5GB | General purpose, balance of quality and performance |
| Gemma 4 E4B Q4_K_M | ~6.5GB | <2.5GB | Stronger reasoning |
| FunctionGemma 270M | ~284MB | <300MB | Function calling only, lightweight |

#### Installation Code

```dart
import 'package:flutter_gemma/flutter_gemma.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize (call once at app startup)
  await FlutterGemma.initialize(
    huggingFaceToken: 'hf_xxxx',  // Optional, required for gated models
  );

  runApp(MyApp());
}
```

#### Download Model

```dart
// From HuggingFace
await FlutterGemma.installModel(
  modelType: ModelType.gemma4E2BIt,
)
.fromNetwork(
  'https://huggingface.co/bartowski/gemma-4-2b-it-GGUF/resolve/main/gemma-4-2b-it-Q4_K_M.gguf',
  token: 'hf_xxxx',  // If model requires auth
)
.withProgress((progress) {
  print('Download: ${progress.percentage.toStringAsFixed(1)}%');
})
.install();
```

### Step 5: Model Loading & Inference

```dart
// Get active model
final model = await FlutterGemma.getActiveModel(
  maxTokens: 2048,
  preferredBackend: PreferredBackend.gpu,
);

// Create session
final session = await model.createSession();

// Send message
await session.addQueryChunk(Message.text(
  text: 'Hello, explain quantum computing',
  isUser: true,
));

// Get response
final response = await session.getResponse();
print(response.text);

// Close
await session.close();
```

### Step 6: Streaming Response

```dart
final session = await model.createSession();
await session.addQueryChunk(Message.text(text: prompt, isUser: true));

final stream = session.getResponseStream();
await for (final event in stream) {
  if (event is TextResponse) {
    print('token: ${event.text}');
  }
}
```

---

## Common Configurations

### Multimodal (Image Input)

```dart
final model = await FlutterGemma.getActiveModel(
  supportImage: true,
  maxNumImages: 1,
);

final session = await model.createSession();

// Add image
final imageBytes = await rootBundle.load('assets/image.png');
await session.addQueryChunk(Message.multimodal(
  text: 'Describe this image',
  images: [imageBytes.buffer.asUint8List()],
  isUser: true,
));
```

### Function Calling

```dart
final tool = Tool.fromJsonSchema({
  'name': 'get_weather',
  'description': 'Get weather for a location',
  'parameters': {
    'type': 'object',
    'properties': {
      'location': {'type': 'string'},
    },
    'required': ['location'],
  },
});

final session = await model.createSession(tools: [tool]);
await session.addQueryChunk(Message.text(
  text: 'What\'s the weather in Tokyo?',
  isUser: true,
));

final stream = session.getResponseStream();
await for (final event in stream) {
  if (event is FunctionCallResponse) {
    print('Function: ${event.functionCall.functionName}');
    print('Args: ${event.functionCall.argumentsText}');
  }
}
```

### Thinking Mode (Gemma 4)

```dart
final session = await model.createSession(
  enableThinking: true,
);
```

---

## Platform Differences

| Capability | iOS | Android | Web | Desktop |
|------------|-----|---------|-----|---------|
| GPU acceleration | Metal | Vulkan/OpenCL | WebGPU | GPU |
| Multimodal | ✅ | ✅ | ✅ | ✅ |
| Audio | ✅ | ✅ | ❌ | ✅ |
| Thinking | ✅ | ✅ | ❌ | ✅ |
| Embeddings | ✅ | ✅ | ✅ | ✅ |
| Function Calling | ✅ | ✅ | ✅ | ✅ |

### Web Limitations
- Must use WebGPU backend
- Thinking mode not supported
- Audio not supported

### Desktop Limitations
- Requires JRE (auto-downloaded Azul Zulu)
- Communicates with LiteRT-LM via gRPC
- Model format: `.litertlm` only

---

## Model Download Sources

### Official MediaPipe Format (Recommended for Mobile)
```
https://huggingface.co/google/gemma-4-2b-it/
```

### GGUF Format (llama.cpp ecosystem)
```
https://huggingface.co/bartowski/gemma-4-2b-it-GGUF
https://huggingface.co/unsloth/gemma-4-2b-it-GGUF
```

### LiteRT-LM Format (Desktop)
```
https://huggingface.co/litert-community/gemma-4-e2b-it-litertlm
```

---

## Troubleshooting

### iOS Build Fails
- Verify `platform :ios, '16.0'`
- Verify `use_frameworks! :linkage => :static`
- Check entitlements configuration

### Android Build Fails
- Verify `minSdk = 24`
- For NPU, verify device support

### Web Not Working
- Verify MediaPipe script loads correctly in `index.html`
- Verify using `PreferredBackend.gpu`
- Safari doesn't support WebGPU (need Chrome/Edge)

### Slow Model Download
- Use HuggingFace token for faster downloads
- Consider GGUF Q4_K_M quantization (smaller, faster)

---

## Complete Example

This example follows **Flutter best practices**:
- Riverpod for state management
- Feature-based project structure
- `AsyncNotifierProvider` for async state
- `AsyncValue.guard()` for error handling
- `ConsumerWidget` for efficient rebuilds

### Project Structure

```
lib/
├── main.dart
├── app.dart
├── core/
│   └── theme/
│       └── app_theme.dart
├── features/
│   └── gemma_chat/
│       ├── data/
│       │   └── gemma_repository.dart
│       ├── domain/
│       │   └── gemma_service.dart
│       └── presentation/
│           ├── screens/
│           │   └── gemma_chat_screen.dart
│           ├── widgets/
│           │   └── chat_bubble.dart
│           └── providers/
│               └── gemma_providers.dart
└── routes/
    └── app_router.dart
```

### main.dart

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_gemma/flutter_gemma.dart';
import 'app.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize Gemma (call once at startup)
  await FlutterGemma.initialize();

  runApp(
    const ProviderScope(
      child: GemmaApp(),
    ),
  );
}
```

### app.dart

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'features/gemma_chat/presentation/screens/gemma_chat_screen.dart';

class GemmaApp extends ConsumerWidget {
  GemmaApp({super.key});

  final _router = GoRouter(
    initialLocation: '/',
    routes: [
      GoRoute(
        path: '/',
        name: 'chat',
        builder: (context, state) => const GemmaChatScreen(),
      ),
    ],
  );

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return MaterialApp.router(
      title: 'Gemma Chat',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      routerConfig: _router,
    );
  }
}
```

### gemma_providers.dart

```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_gemma/flutter_gemma.dart';
import '../data/gemma_repository.dart';
import '../domain/gemma_service.dart';

// Inference model provider
final inferenceModelProvider = FutureProvider<InferenceModel>((ref) async {
  return await FlutterGemma.getActiveModel(
    maxTokens: 2048,
    preferredBackend: PreferredBackend.gpu,
  );
});

// Chat session provider
final chatSessionProvider = FutureProvider.autoDispose<InferenceSession>((ref) async {
  final model = await ref.watch(inferenceModelProvider.future);
  return await model.createSession();
});

// Chat state notifier
@riverpod
class ChatNotifier extends _$ChatNotifier {
  @override
  AsyncValue<List<ChatMessage>> build() => const AsyncValue.data([]);

  Future<void> sendMessage(String text) async {
    state = const AsyncValue.loading();

    state = await AsyncValue.guard(() async {
      final session = await ref.read(chatSessionProvider.future);
      final messages = [...state.value ?? []];

      // Add user message
      messages.add(ChatMessage(text: text, isUser: true));
      state = AsyncValue.data(messages);

      // Send to model
      await session.addQueryChunk(Message.text(text: text, isUser: true));

      // Collect response
      final buffer = StringBuffer();
      final stream = session.getResponseStream();

      await for (final event in stream) {
        if (event is TextResponse) {
          buffer.write(event.text);
        }
      }

      // Add assistant message
      messages.add(ChatMessage(text: buffer.toString(), isUser: false));
      return messages;
    });
  }
}

// Chat message model
class ChatMessage {
  final String text;
  final bool isUser;
  const ChatMessage({required this.text, required this.isUser});
}
```

### gemma_chat_screen.dart

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/gemma_providers.dart';

class GemmaChatScreen extends ConsumerWidget {
  const GemmaChatScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final chatState = ref.watch(chatNotifierProvider);
    final modelAsync = ref.watch(inferenceModelProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Gemma Chat'),
        actions: [
          modelAsync.when(
            data: (_) => const Icon(Icons.check_circle, color: Colors.green),
            loading: () => const SizedBox(
              width: 20,
              height: 20,
              child: CircularProgressIndicator(strokeWidth: 2),
            ),
            error: (_, __) => const Icon(Icons.error, color: Colors.red),
          ),
          const SizedBox(width: 16),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: chatState.when(
              data: (messages) => messages.isEmpty
                  ? const Center(
                      child: Text('Ask Gemma anything!'),
                    )
                  : ListView.builder(
                      padding: const EdgeInsets.all(16),
                      itemCount: messages.length,
                      itemBuilder: (context, index) {
                        final msg = messages[index];
                        return Align(
                          alignment: msg.isUser
                              ? Alignment.centerRight
                              : Alignment.centerLeft,
                          child: Container(
                            margin: const EdgeInsets.only(bottom: 8),
                            padding: const EdgeInsets.all(12),
                            decoration: BoxDecoration(
                              color: msg.isUser
                                  ? Colors.deepPurple
                                  : Colors.grey[300],
                              borderRadius: BorderRadius.circular(16),
                            ),
                            child: Text(
                              msg.text,
                              style: TextStyle(
                                color: msg.isUser ? Colors.white : Colors.black,
                              ),
                            ),
                          ),
                        );
                      },
                    ),
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (err, _) => Center(child: Text('Error: $err')),
            ),
          ),
          const _ChatInput(),
        ],
      ),
    );
  }
}

class _ChatInput extends ConsumerStatefulWidget {
  const _ChatInput();

  @override
  ConsumerState<_ChatInput> createState() => _ChatInputState();
}

class _ChatInputState extends ConsumerState<_ChatInput> {
  final _controller = TextEditingController();

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Theme.of(context).scaffoldBackgroundColor,
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.1),
            blurRadius: 4,
            offset: const Offset(0, -2),
          ),
        ],
      ),
      child: SafeArea(
        child: Row(
          children: [
            Expanded(
              child: TextField(
                controller: _controller,
                decoration: const InputDecoration(
                  hintText: 'Ask Gemma...',
                  border: OutlineInputBorder(),
                  contentPadding: EdgeInsets.symmetric(
                    horizontal: 16,
                    vertical: 12,
                  ),
                ),
                maxLines: null,
                textInputAction: TextInputAction.send,
                onSubmitted: (_) => _send(),
              ),
            ),
            const SizedBox(width: 8),
            IconButton.filled(
              onPressed: _send,
              icon: const Icon(Icons.send),
            ),
          ],
        ),
      ),
    );
  }

  void _send() {
    final text = _controller.text.trim();
    if (text.isEmpty) return;

    _controller.clear();
    ref.read(chatNotifierProvider.notifier).sendMessage(text);
  }
}
```
