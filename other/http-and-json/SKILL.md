---
name: flutter-handling-http-and-json
description: Executes HTTP requests and handles JSON serialization in a Flutter app using Dio and Retrofit. Use when integrating with REST APIs or parsing structured data.
tags: [flutter, dio, retrofit, http, json, api, serialization, networking, interceptors]
applies-to: [antigravity, cursor, copilot]
level: project
---

# Flutter HTTP & JSON (Dio + Retrofit)

## Contents
- [Core Guidelines](#core-guidelines)
- [Technology Stack](#technology-stack)
- [Workflow: Setting Up Dio](#workflow-setting-up-dio)
- [Workflow: Defining API with Retrofit](#workflow-defining-api-with-retrofit)
- [Workflow: Implementing Interceptors](#workflow-implementing-interceptors)
- [Workflow: Data Models & Domain Entities](#workflow-data-models--domain-entities)
- [Workflow: Error Handling](#workflow-error-handling)
- [Workflow: Functional Error Handling (Either + fpdart)](#workflow-functional-error-handling-either--fpdart)
- [Examples](#examples)
- [Anti-patterns](#anti-patterns)
- [Resources](#resources)

## Core Guidelines
- **Use Dio** as the HTTP client — never use `dart:io` `HttpClient` or `package:http` directly. Dio provides interceptors, cancellation, timeouts, and FormData out of the box.
- **Use Retrofit** for type-safe API definitions — annotate abstract classes with `@RestApi` to auto-generate Dio client implementations.
- **Enforce HTTPS:** iOS and Android disable cleartext (HTTP) connections by default. Always use HTTPS endpoints.
- **Singleton Dio:** Create a single `Dio` instance per app (or per base URL) to share interceptors, base options, and headers consistently.
- **Always use `handler.next()`** in interceptors — never swallow requests/responses/errors without forwarding them through the chain.
- **Structured Error Handling:** Catch `DioException` and map to domain-specific exceptions. Never expose raw error messages to users.

## Technology Stack

| Package | Purpose | Type |
|---|---|---|
| `dio` | HTTP client with interceptors, timeouts, cancellation | Runtime |
| `retrofit` | Type-safe API annotations (`@RestApi`, `@GET`, `@POST`, etc.) | Runtime |
| `retrofit_generator` | Code generation for Retrofit | Dev |
| `json_annotation` | JSON serialization annotations | Runtime |
| `json_serializable` | JSON serialization code generation | Dev |
| `freezed_annotation` | Annotations for Freezed (used in Entities) | Runtime |
| `freezed` | Code generation for immutable classes (used in Entities) | Dev |
| `build_runner` | Runs code generators | Dev |

## Workflow: Setting Up Dio

- [ ] Add `dio` to `pubspec.yaml`.
- [ ] Create a singleton Dio instance with `BaseOptions` (base URL, timeouts, default headers).
- [ ] Configure platform permissions (Internet permission in `AndroidManifest.xml` and macOS `.entitlements`).
- [ ] Register interceptors: auth, logging, error handling.
- [ ] Provide the Dio instance via DI (dependency injection).

### Dio Instance Setup

```dart
Dio createDio({required String baseUrl, required String accessToken}) {
  final dio = Dio(
    BaseOptions(
      baseUrl: baseUrl,
      connectTimeout: const Duration(seconds: 30),
      receiveTimeout: const Duration(seconds: 30),
      sendTimeout: const Duration(seconds: 30),
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    ),
  );

  dio.interceptors.addAll([
    AuthInterceptor(accessToken),
    LogInterceptor(requestBody: true, responseBody: true),
  ]);

  return dio;
}
```

## Workflow: Defining API with Retrofit

- [ ] Add dependencies: `retrofit`, `json_annotation` (runtime) and `retrofit_generator`, `json_serializable`, `build_runner` (dev).
- [ ] Create an abstract class annotated with `@RestApi(baseUrl: '...')`.
- [ ] Add a factory constructor: `factory ApiClient(Dio dio, {String? baseUrl}) = _ApiClient;`.
- [ ] Define methods using HTTP annotations: `@GET`, `@POST`, `@PUT`, `@PATCH`, `@DELETE`.
- [ ] Add the `part 'filename.g.dart';` directive.
- [ ] Run: `dart run build_runner build --delete-conflicting-outputs`.

### Retrofit Annotations Reference

| Annotation | Purpose |
|---|---|
| `@RestApi(baseUrl: '...')` | Marks an abstract class as a Retrofit API client |
| `@GET('/path')` | HTTP GET request |
| `@POST('/path')` | HTTP POST request |
| `@PUT('/path')` | HTTP PUT request |
| `@PATCH('/path')` | HTTP PATCH request |
| `@DELETE('/path')` | HTTP DELETE request |
| `@Path('name')` | URL path parameter |
| `@Query('name')` | URL query parameter |
| `@Queries()` | Map of query parameters |
| `@Body()` | Request body |
| `@Header('name')` | Request header parameter |
| `@Headers({...})` | Static request headers |
| `@Part()` | Multipart form field |
| `@MultiPart()` | Marks method as multipart |
| `@FormUrlEncoded()` | URL-encoded form data |

## Workflow: Implementing Interceptors

Interceptors run in FIFO order. Always call `handler.next()` to forward to the next interceptor.

- [ ] **Auth Interceptor:** Attach `Authorization` header to every request. Handle 401 by refreshing token and retrying.
- [ ] **Logging Interceptor:** Log requests/responses in debug mode only.
- [ ] **Error Interceptor:** Transform `DioException` into domain exceptions.

### Interceptor Structure

```dart
class AuthInterceptor extends Interceptor {
  final String _token;
  AuthInterceptor(this._token);

  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    options.headers['Authorization'] = 'Bearer $_token';
    handler.next(options); // ← MUST call handler.next()
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    if (err.response?.statusCode == 401) {
      // Handle token refresh logic here
    }
    handler.next(err); // ← MUST call handler.next()
  }
}
```

### QueuedInterceptor

Use `QueuedInterceptor` instead of `Interceptor` when interceptor logic is async (e.g., token refresh). This ensures requests are queued and processed one at a time, preventing race conditions during token refresh.

```dart
class TokenRefreshInterceptor extends QueuedInterceptor {
  @override
  void onError(DioException err, ErrorInterceptorHandler handler) async {
    if (err.response?.statusCode == 401) {
      // Refresh token — all other requests will queue behind this
      final newToken = await refreshToken();
      err.requestOptions.headers['Authorization'] = 'Bearer $newToken';
      // Retry the failed request
      final response = await dio.fetch(err.requestOptions);
      handler.resolve(response);
      return;
    }
    handler.next(err);
  }
}
```

## Workflow: Data Models & Domain Entities

Distinguish between **Data Models** (Data layer) and **Domain Entities** (Domain layer) for a clean architecture.

### Data Models (Data Layer)
Use `json_serializable` without `freezed` for models that interact with the API. This keeps the data layer lightweight and prevents overkill for simple DTOs (Data Transfer Objects).

- [ ] Add dependencies: `json_annotation` (runtime) and `json_serializable` (dev).
- [ ] Annotate the class with `@JsonSerializable()`.
- [ ] Use `explicitToJson: true` for nested models.
- [ ] Define `fromJson` and `toJson` delegating to generated functions.
- [ ] Add a mapper method (e.g., `toEntity()`) to convert the model to a domain entity.

### Domain Entities (Domain Layer)
Use `freezed` for domain entities to benefit from immutability, union types, and built-in `copyWith`.

- [ ] Add dependencies: `freezed_annotation` (runtime) and `freezed` (dev).
- [ ] Annotate the class with `@freezed`.
- [ ] **NEVER** add `fromJson` or `toJson` to domain entities. They should be completely decoupled from the data layer's serialization logic. Data conversion should only happen via mappers in the data layer (e.g., `UserModel.toEntity()`).

> **Important:** Retrofit requires a `factory Model.fromJson(Map<String, dynamic> json)` on every response model for automatic type conversion.

## Workflow: Error Handling

- [ ] Wrap all API calls in try-catch blocks catching `DioException`.
- [ ] Map `DioExceptionType` to user-friendly error messages.
- [ ] Use `ErrorInterceptor` for global error transformation.

### DioExceptionType Reference

| Type | Meaning |
|---|---|
| `connectionTimeout` | Server unreachable within timeout |
| `sendTimeout` | Request sending exceeded timeout |
| `receiveTimeout` | Response receiving exceeded timeout |
| `badResponse` | Server returned a non-success status code |
| `cancel` | Request was manually cancelled |
| `connectionError` | Network connection error |
| `badCertificate` | SSL certificate issue |
| `unknown` | Unexpected error |

## Workflow: Functional Error Handling (Either + fpdart)

For more robust and explicit error handling, use the functional programming approach with `fpdart`. This replaces the `try-catch` pattern with a type-safe `Either<Failure, T>` return type.

- [ ] Add `fpdart` to `pubspec.yaml`.
- [ ] Define a sealed `Failure` class hierarchy.
- [ ] Centralize error mapping from `DioException` to `Failure`.
- [ ] Use `TaskEither` or a generic request wrapper to convert API calls.

### Failure Hierarchy

```dart
sealed class Failure {
  final String message;
  const Failure(this.message);
}

class ServerFailure extends Failure {
  final int? statusCode;
  const ServerFailure(super.message, {this.statusCode});
}

class ConnectionFailure extends Failure {
  const ConnectionFailure() : super('No Internet Connection');
}
```

### Repository Implementation with Either

```dart
class UserRepository {
  final UserApi _api;
  final DioClient _dioClient; // Contains centralized mapping

  UserRepository(this._api, this._dioClient);

  Future<Either<Failure, UserEntity>> getUser(String id) async {
    return _dioClient.request(() async {
      final model = await _api.getUser(id);
      return model.toEntity();
    });
  }
}
```

### UI Consumption

```dart
final result = await repository.getUser(id);

result.match(
  (failure) => showError(failure.message),
  (user) => displayUser(user),
);
```

## Examples

### Full API Client with Retrofit

```dart
import 'package:dio/dio.dart';
import 'package:json_annotation/json_annotation.dart';
import 'package:retrofit/retrofit.dart';

part 'user_api.g.dart';

@RestApi(baseUrl: 'https://api.example.com/v1')
abstract class UserApi {
  factory UserApi(Dio dio, {String? baseUrl}) = _UserApi;

  @GET('/users')
  Future<List<UserModel>> getUsers();

  @GET('/users/{id}')
  Future<UserModel> getUser(@Path('id') String id);

  @POST('/users')
  Future<UserModel> createUser(@Body() CreateUserRequest request);

  @PUT('/users/{id}')
  Future<UserModel> updateUser(
    @Path('id') String id,
    @Body() UpdateUserRequest request,
  );

  @DELETE('/users/{id}')
  Future<void> deleteUser(@Path('id') String id);

  @GET('/users')
  Future<List<UserModel>> searchUsers(
    @Query('q') String query,
    @Query('page') int page,
    @Query('limit') int limit,
  );
}
```

### Domain Entity (Freezed)

```dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'user_entity.freezed.dart';

@freezed
class UserEntity with _$UserEntity {
  const factory UserEntity({
    required int id,
    required String name,
    required String email,
    required DateTime createdAt,
  }) = _UserEntity;
}
```

### Data Model (JsonSerializable)

```dart
import 'package:json_annotation/json_annotation.dart';
import 'package:your_app/domain/entities/user_entity.dart';

part 'user_model.g.dart';

@JsonSerializable()
class UserModel {
  final int id;
  final String name;
  @JsonKey(name: 'email_address')
  final String email;
  @JsonKey(name: 'created_at')
  final DateTime createdAt;

  const UserModel({
    required this.id,
    required this.name,
    required this.email,
    required this.createdAt,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) => _$UserModelFromJson(json);
  Map<String, dynamic> toJson() => _$UserModelToJson(this);

  // Mapper to Domain Entity
  UserEntity toEntity() => UserEntity(
    id: id,
    name: name,
    email: email,
    createdAt: createdAt,
  );
}
```

### Error Handling at Repository Level

```dart
class UserRepository {
  final UserApi _api;
  UserRepository(this._api);

  Future<List<UserEntity>> getUsers() async {
    try {
      final models = await _api.getUsers();
      return models.map((m) => m.toEntity()).toList();
    } on DioException catch (e) {
      switch (e.type) {
        case DioExceptionType.connectionTimeout:
        case DioExceptionType.receiveTimeout:
          throw NetworkTimeoutException();
        case DioExceptionType.badResponse:
          final statusCode = e.response?.statusCode;
          if (statusCode == 404) throw NotFoundException();
          if (statusCode == 401) throw UnauthorizedException();
          throw ServerException(statusCode: statusCode);
        case DioExceptionType.connectionError:
          throw NoInternetException();
        default:
          throw UnknownApiException(e.message);
      }
    }
  }
}
```

### File Upload with Retrofit

```dart
@POST('/upload')
@MultiPart()
Future<UploadResponse> uploadFile(
  @Part(name: 'file') File file,
  @Part(name: 'description') String description,
);
```

### Getting Raw HttpResponse

```dart
// Wrap return type in HttpResponse to access status code and headers
@GET('/users/{id}')
Future<HttpResponse<UserModel>> getUserWithResponse(@Path('id') String id);

// Usage
final httpResponse = await api.getUserWithResponse('123');
print(httpResponse.response.statusCode); // 200
print(httpResponse.data.name);           // User name
```

## Anti-patterns

- ❌ Using `package:http` or raw `HttpClient` instead of Dio
- ❌ Creating a new `Dio()` instance per request (use singleton)
- ❌ Forgetting `handler.next()` in interceptors (swallows the request/response)
- ❌ Writing manual HTTP calls when Retrofit can generate them
- ❌ Missing `fromJson` factory on response models (Retrofit can't deserialize)
- ❌ Catching `Exception` instead of `DioException` for network errors
- ❌ Exposing `DioException` to the UI layer (map to domain exceptions)
- ❌ Using `freezed` for Data Models (keep them simple with `json_serializable`)
- ❌ Mixing API response structure directly into Domain Entities
- ❌ Adding `fromJson`/`toJson` to Domain Entities (entities must remain data-agnostic)

## Resources

- https://pub.dev/packages/dio
- https://pub.dev/packages/retrofit
- https://pub.dev/packages/json_serializable
- https://pub.dev/packages/json_annotation
- https://docs.flutter.dev/data-and-backend/networking
- https://docs.flutter.dev/data-and-backend/serialization/json
- https://docs.flutter.dev/cookbook/networking/fetch-data
- https://docs.flutter.dev/release/breaking-changes/network-policy-ios-android
