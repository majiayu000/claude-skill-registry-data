---
name: flutter-gemma-skill
description: |
  Use this skill when building reusable AI capabilities on top of flutter_gemma. For developers who want to create packageable Skills with function calling, structured JSON output, system instructions, and result parsing. Covers: designing function schemas, implementing Skill classes, building execution engines, and publishing AI skill packages.
triggers:
  - create a Skill
  - wrap function calling
  - AI skill
  - structured output
  - build AI capability
  - function calling schema
  - Gemma skill development
  - reusable AI
---

# Flutter Gemma Skill Development

Guide for wrapping `flutter_gemma` function calling capabilities into reusable, production-ready AI Skills.

## What is a Skill?

A **Skill** is a self-contained AI capability package containing:
- **System Instruction** - How the model should behave
- **Function Schema** - JSON Schema for structured output
- **Result Parser** - Converts model output to typed results
- **Prompt Builder** - Constructs user input into model prompts

### Skill vs Direct API Calls

```dart
// ❌ Direct calls - repetitive boilerplate
final session = await model.createSession(tools: [myTool]);
await session.addQueryChunk(Message.text(text: 'translate to French', isUser: true));
// ... parse JSON manually ...

// ✅ Using Skill - clean, reusable
final translationSkill = TranslationSkill();
final result = await translationSkill.execute(model, text: 'Hello');
```

---

## Skill Architecture

Follow **feature-based project structure** for clean separation of concerns:

```
my_ai_skills/
├── lib/
│   ├── skill.dart                    # Skill base class & interfaces
│   ├── skill_result.dart             # Result types (immutable)
│   ├── skill_engine.dart            # Execution engine
│   └── features/
│       ├── translation/
│       │   ├── translation_skill.dart
│       │   ├── translation_schema.dart
│       │   └── translation_result.dart
│       └── summarization/
│           ├── summarization_skill.dart
│           ├── summarization_schema.dart
│           └── summarization_result.dart
```

---

## Defining a Skill

### Step 1: Define Result Types

```dart
// skill_result.dart

abstract class SkillResult {
  bool get success;
  String? get errorMessage;
}

class TranslationResult extends SkillResult {
  final String translatedText;
  final String sourceLanguage;
  final String targetLanguage;

  TranslationResult.success({
    required this.translatedText,
    required this.sourceLanguage,
    required this.targetLanguage,
  }) : success = true, errorMessage = null;

  TranslationResult.error(String message)
      : success = false,
        errorMessage = message,
        translatedText = '',
        sourceLanguage = '',
        targetLanguage = '';
}

class SummaryResult extends SkillResult {
  final String summary;
  final int wordCount;
  final List<String>? keyPoints;

  SummaryResult.success({
    required this.summary,
    required this.wordCount,
    this.keyPoints,
  }) : success = true, errorMessage = null;

  SummaryResult.error(String message)
      : success = false,
        errorMessage = message,
        summary = '',
        wordCount = 0,
        keyPoints = null;
}
```

### Step 2: Define Function Schema

```dart
// schemas/translation_schema.dart

const translationFunctionSchema = {
  'name': 'translate_text',
  'description': 'Translate text between languages accurately',
  'parameters': {
    'type': 'object',
    'properties': {
      'translated_text': {
        'type': 'string',
        'description': 'The translated text',
      },
      'source_language': {
        'type': 'string',
        'description': 'Source language name or code',
      },
      'target_language': {
        'type': 'string',
        'description': 'Target language name or code',
      },
    },
    'required': ['translated_text', 'source_language', 'target_language'],
  },
};
```

### Step 3: Implement Skill Class

```dart
// skills/translation_skill.dart

import 'dart:convert';
import 'package:flutter_gemma/flutter_gemma.dart';
import '../skill.dart';
import '../skill_result.dart';
import '../schemas/translation_schema.dart';

class TranslationSkill extends Skill {
  @override
  String get id => 'translation';

  @override
  String get name => 'Translator';

  @override
  String get description => 'Translate text between 140+ languages';

  @override
  String get systemInstruction => '''
You are an expert translator. Translate text accurately while preserving:
- Meaning and nuance
- Cultural context
- Technical terminology
- Tone and style
''';

  @override
  Map<String, dynamic>? get functionSchema => translationFunctionSchema;

  @override
  String buildPrompt(SkillInput input) {
    final targetLang = input.extra?['target_language'] ?? 'English';
    final sourceLang = input.extra?['source_language'];
    final prefix = sourceLang != null
        ? 'Translate from $sourceLang to $targetLang:'
        : 'Translate to $targetLang:';
    return '$prefix\n\n${input.text}\n\nUse the translate_text function.';
  }

  @override
  SkillResult parseResult(FunctionCall functionCall) {
    try {
      final args = jsonDecode(functionCall.argumentsText) as Map<String, dynamic>;
      return TranslationResult.success(
        translatedText: args['translated_text'] as String,
        sourceLanguage: args['source_language'] as String,
        targetLanguage: args['target_language'] as String,
      );
    } catch (e) {
      return TranslationResult.error('Parse error: $e');
    }
  }
}
```

### Step 4: Create SkillEngine

```dart
// skill_engine.dart

import 'dart:convert';
import 'package:flutter_gemma/flutter_gemma.dart';
import 'skill.dart';
import 'skill_result.dart';

class SkillEngine {
  InferenceModel? _model;

  bool get isModelLoaded => _model != null;

  /// Execute a skill
  Future<SkillResult> execute({
    required Skill skill,
    required String input,
    Map<String, dynamic>? extra,
  }) async {
    if (_model == null) {
      throw StateError('Model not loaded');
    }

    final tools = skill.functionSchema != null
        ? [Tool.fromJsonSchema(skill.functionSchema!)]
        : null;

    final session = await _model!.createSession(
      systemInstruction: SystemInstruction.text(skill.systemInstruction),
      tools: tools,
    );

    try {
      await session.addQueryChunk(Message.text(
        text: skill.buildPrompt(SkillInput(text: input, extra: extra)),
        isUser: true,
      ));

      final stream = session.getResponseStream();
      FunctionCall? functionCall;

      await for (final event in stream) {
        if (event is FunctionCallResponse) {
          functionCall = event.functionCall;
          break;
        } else if (event is ErrorResponse) {
          throw Exception(event.message);
        }
      }

      if (functionCall != null) {
        return skill.parseResult(functionCall);
      }

      throw Exception('No function call returned');
    } finally {
      await session.close();
    }
  }

  /// Execute with streaming (for real-time token display)
  Stream<String> executeStream({
    required Skill skill,
    required String input,
  }) async* {
    final session = await _model!.createSession(
      systemInstruction: SystemInstruction.text(skill.systemInstruction),
    );

    await session.addQueryChunk(Message.text(text: input, isUser: true));

    final stream = session.getResponseStream();
    await for (final event in stream) {
      if (event is TextResponse) {
        yield event.text;
      }
    }
  }
}
```

### Step 5: Skill Base Class

```dart
// skill.dart

import 'package:flutter/foundation.dart';
import 'package:flutter_gemma/flutter_gemma.dart';

abstract class Skill {
  String get id;
  String get name;
  String get description;
  String get systemInstruction;
  Map<String, dynamic>? get functionSchema => null;
  SkillResult parseResult(FunctionCall functionCall);
  String buildPrompt(SkillInput input);
}

class SkillInput {
  final String text;
  final List<Uint8List>? images;
  final Map<String, dynamic>? extra;

  const SkillInput({
    required this.text,
    this.images,
    this.extra,
  });
}
```

---

## Usage Example

This follows Flutter best practices with Riverpod and feature-based structure.

### Project Structure

```
lib/
├── main.dart
├── app.dart
├── features/
│   └── translation/
│       ├── data/
│       │   └── translation_repository.dart
│       ├── domain/
│       │   └── translation_service.dart
│       └── presentation/
│           ├── screens/
│           │   └── translation_screen.dart
│           └── providers/
│               └── translation_providers.dart
```

### main.dart

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_gemma/flutter_gemma.dart';
import 'app.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await FlutterGemma.initialize();
  runApp(const ProviderScope(child: TranslationApp()));
}
```

### translation_providers.dart

```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_gemma/flutter_gemma.dart';
import '../data/translation_repository.dart';

// Model provider
final inferenceModelProvider = FutureProvider<InferenceModel>((ref) async {
  return await FlutterGemma.getActiveModel(
    maxTokens: 2048,
    preferredBackend: PreferredBackend.gpu,
  );
});

// Translation notifier
@riverpod
class TranslationNotifier extends _$TranslationNotifier {
  @override
  AsyncValue<TranslationResult?> build() => const AsyncValue.data(null);

  Future<void> translate(String text, String targetLang) async {
    state = const AsyncValue.loading();

    state = await AsyncValue.guard(() async {
      final model = await ref.read(inferenceModelProvider.future);
      final session = await model.createSession();

      try {
        final skill = TranslationSkill();
        final tool = skill.functionSchema != null
            ? [Tool.fromJsonSchema(skill.functionSchema!)]
            : null;

        final chat = await model.createSession(tools: tool);

        await chat.addQueryChunk(Message.text(
          text: skill.buildPrompt(SkillInput(
            text: text,
            extra: {'target_language': targetLang},
          )),
          isUser: true,
        ));

        final stream = chat.generateChatResponseAsync();
        FunctionCall? functionCall;

        await for (final event in stream) {
          if (event is FunctionCallResponse) {
            functionCall = event.functionCall;
          }
        }

        if (functionCall != null) {
          return skill.parseResult(functionCall);
        }

        throw Exception('No function call returned');
      } finally {
        await session.close();
      }
    });
  }
}
```

### translation_screen.dart

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/translation_providers.dart';

class TranslationScreen extends ConsumerStatefulWidget {
  const TranslationScreen({super.key});

  @override
  ConsumerState<TranslationScreen> createState() => _TranslationScreenState();
}

class _TranslationScreenState extends ConsumerState<TranslationScreen> {
  final _controller = TextEditingController();
  String _targetLang = 'French';

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final translationState = ref.watch(translationNotifierProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('AI Translation'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            TextField(
              controller: _controller,
              maxLines: 5,
              decoration: const InputDecoration(
                hintText: 'Enter text to translate...',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),
            DropdownButtonFormField<String>(
              value: _targetLang,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'Target Language',
              ),
              items: const [
                DropdownMenuItem(value: 'French', child: Text('French')),
                DropdownMenuItem(value: 'Spanish', child: Text('Spanish')),
                DropdownMenuItem(value: 'German', child: Text('German')),
                DropdownMenuItem(value: 'Chinese', child: Text('Chinese')),
              ],
              onChanged: (value) {
                if (value != null) setState(() => _targetLang = value);
              },
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: translationState.isLoading
                  ? null
                  : () => ref
                      .read(translationNotifierProvider.notifier)
                      .translate(_controller.text, _targetLang),
              child: translationState.isLoading
                  ? const SizedBox(
                      height: 20,
                      width: 20,
                      child: CircularProgressIndicator(strokeWidth: 2),
                    )
                  : const Text('Translate'),
            ),
            const SizedBox(height: 16),
            Expanded(
              child: translationState.when(
                data: (result) {
                  if (result == null) return const SizedBox.shrink();
                  if (!result.success) {
                    return Text(
                      'Error: ${result.errorMessage}',
                      style: const TextStyle(color: Colors.red),
                    );
                  }
                  return SingleChildScrollView(
                    child: Text(
                      result.translatedText,
                      style: const TextStyle(fontSize: 16),
                    ),
                  );
                },
                loading: () => const Center(child: CircularProgressIndicator()),
                error: (err, _) => Text('Error: $err'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
```

---

## Common Skill Templates

### Summarization Schema

```dart
const summarizationFunctionSchema = {
  'name': 'summarize_text',
  'description': 'Generate a concise summary with key points',
  'parameters': {
    'type': 'object',
    'properties': {
      'summary': {
        'type': 'string',
        'description': 'The generated summary',
      },
      'word_count': {
        'type': 'integer',
        'description': 'Word count of the summary',
      },
      'key_points': {
        'type': 'array',
        'description': 'Key points extracted',
        'items': {'type': 'string'},
      },
    },
    'required': ['summary', 'word_count'],
  },
};
```

### Classification Schema

```dart
const classificationFunctionSchema = {
  'name': 'classify_text',
  'description': 'Classify text into categories',
  'parameters': {
    'type': 'object',
    'properties': {
      'category': {
        'type': 'string',
        'description': 'The assigned category',
      },
      'confidence': {
        'type': 'number',
        'description': 'Confidence score (0-1)',
      },
      'reasoning': {
        'type': 'string',
        'description': 'Explanation for classification',
      },
    },
    'required': ['category', 'confidence'],
  },
};
```

### Question Answering Schema

```dart
const qaFunctionSchema = {
  'name': 'answer_question',
  'description': 'Answer a question based on provided context',
  'parameters': {
    'type': 'object',
    'properties': {
      'answer': {
        'type': 'string',
        'description': 'The answer to the question',
      },
      'confidence': {
        'type': 'number',
        'description': 'Confidence score (0-1)',
      },
      'supporting_text': {
        'type': 'string',
        'description': 'Text from context supporting the answer',
      },
    },
    'required': ['answer', 'confidence'],
  },
};
```

---

## Best Practices

### 1. System Instruction Should Be Specific

```dart
// ❌ Too vague
'Be helpful'

// ✅ Specific and actionable
'''You are an expert at text summarization.
- Create accurate, concise summaries
- Capture main ideas and key information
- Maintain original meaning and context
- Extract 3-5 key points when appropriate
- Use clear, accessible language'''
```

### 2. Function Schema Needs Complete Descriptions

```dart
// ❌ Missing descriptions
'parameters': {'type': 'object', 'properties': {'text': {'type': 'string'}}}

// ✅ Every field has description
'parameters': {
  'type': 'object',
  'properties': {
    'text': {
      'type': 'string',
      'description': 'The translated text',
    },
  },
  'required': ['text'],
}
```

### 3. Robust Error Handling

```dart
@override
SkillResult parseResult(FunctionCall functionCall) {
  try {
    final args = jsonDecode(functionCall.argumentsText) as Map<String, dynamic>;
    // Parse...
  } on FormatException catch (e) {
    return MyResult.error('Invalid JSON: $e');
  } on TypeError catch (e) {
    return MyResult.error('Missing required field: $e');
  } catch (e) {
    return MyResult.error('Unexpected error: $e');
  }
}
```

### 4. Consider Multimodal Input

```dart
class SkillInput {
  final String text;
  final List<Uint8List>? images;  // Image support
  final Map<String, dynamic>? extra;

  const SkillInput({
    required this.text,
    this.images,
    this.extra,
  });
}
```

---

## Publishing a Skill Package

### pubspec.yaml

```yaml
name: my_ai_skills
description: Reusable AI skills powered by flutter_gemma
version: 0.1.0
repository: https://github.com/your-org/my_ai_skills
license: MIT

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter_gemma: ^0.13.2
  flutter:
    sdk: flutter

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^5.0.0
```

### Export File

```dart
library my_ai_skills;

export 'skill.dart';
export 'skill_result.dart';
export 'skill_engine.dart';
export 'skills/translation_skill.dart';
export 'skills/summarization_skill.dart';
export 'skills/classification_skill.dart';
```

---

## Extension Ideas

1. **Skill Chaining** - Compose multiple skills into workflows
2. **Skill Marketplace** - Load third-party skill packages
3. **LoRA Fine-tuning** - Use flutter_gemma's LoRA support
4. **Streaming Output** - Token-by-token real-time display
5. **Skill Builder** - Low-code custom skill creation
