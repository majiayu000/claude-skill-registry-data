---
name: dart-generate-test-mocks
description: Define and generate mock objects for external dependencies using `package:mockito` and `build_runner`. Use when unit testing classes that depend on complex external services like APIs or databases.
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Fri, 24 Apr 2026 15:13:58 GMT
---

## Contents
- [Structuring Code for Testability](#structuring-code-for-testability)
- [Managing Dependencies](#managing-dependencies)
- [Generating Mocks](#generating-mocks)
- [Implementing Unit Tests](#implementing-unit-tests)
- [Workflow: Creating and Running Mocked Tests](#workflow-creating-and-running-mocked-tests)
- [Examples](#examples)

## Structuring Code for Testability
Design Dart classes to support dependency injection.

- Inject external services (e.g., `http.Client`) through class constructors.
- Represent URLs strictly as `Uri` objects using `Uri.parse(string)`.
- Utilize Dart's object-oriented features (classes, mixins) to define clear interfaces.

## Managing Dependencies
- Add runtime dependencies: `dart pub add http`.
- Add testing dependencies: `dart pub add dev:test dev:mockito dev:build_runner`.
- Import HTTP libraries with a prefix: `import 'package:http/http.dart' as http;`.

## Generating Mocks
- Always use the `@GenerateNiceMocks` annotation (preferable to `@GenerateMocks`).
- Place the annotation in the test file, passing a list of `MockSpec<Type>()` objects.
- Import the generated file using the `.mocks.dart` extension.
- Execute `build_runner`: `dart run build_runner build`.

## Implementing Unit Tests
- **Stubbing:** Use `when(mock.method()).thenReturn(value)` for synchronous methods.
- **CRITICAL:** Always use `thenAnswer((_) async => value)` for methods returning a `Future` or `Stream`.
- **Verification:** Use `verify(mock.method()).called(1)` to check invocation counts.

## Workflow: Creating and Running Mocked Tests

### Task Progress
- [ ] 1. Identify the external dependency to mock.
- [ ] 2. Inject the dependency into the target class constructor.
- [ ] 3. Create test file and add `@GenerateNiceMocks([MockSpec<Dependency>()])`.
- [ ] 4. Add the import for the generated `.mocks.dart` file.
- [ ] 5. Run `dart run build_runner build`.
- [ ] 6. Write test cases using `group()` and `test()`.
- [ ] 7. Stub required behaviors using `when()`.
- [ ] 8. Execute the target method.
- [ ] 9. Verify interactions using `verify()` and assert with `expect()`.
- [ ] 10. Run `dart test`.

### Example: System Under Test (`lib/api_service.dart`)
```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  final http.Client client;
  ApiService(this.client);

  Future<String> fetchData(String urlString) async {
    final uri = Uri.parse(urlString);
    final response = await client.get(uri);
    if (response.statusCode == 200) {
      return jsonDecode(response.body)['data'];
    } else {
      throw Exception('Failed to load data');
    }
  }
}
```

### Example: Test (`test/api_service_test.dart`)
```dart
import 'package:test/test.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'package:http/http.dart' as http;
import 'package:my_app/api_service.dart';

@GenerateNiceMocks([MockSpec<http.Client>()])
import 'api_service_test.mocks.dart';

void main() {
  group('ApiService', () {
    late ApiService apiService;
    late MockClient mockHttpClient;

    setUp(() {
      mockHttpClient = MockClient();
      apiService = ApiService(mockHttpClient);
    });

    test('returns data on success', () async {
      when(mockHttpClient.get(any)).thenAnswer(
        (_) async => http.Response('{"data": "Success"}', 200),
      );
      final result = await apiService.fetchData('https://api.example.com/data');
      expect(result, 'Success');
      verify(mockHttpClient.get(Uri.parse('https://api.example.com/data'))).called(1);
    });

    test('throws on error', () {
      when(mockHttpClient.get(any)).thenAnswer(
        (_) async => http.Response('Not Found', 404),
      );
      expect(
        apiService.fetchData('https://api.example.com/data'),
        throwsException,
      );
    });
  });
}
```
