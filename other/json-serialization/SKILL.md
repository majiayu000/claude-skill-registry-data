---
name: json-serialization
description: Standardizes JSON serialization and deserialization in Flutter and Dart using dart:convert, manual factory constructors, or code-generation with freezed.
version: 1.0.0
---

# JSON Serialization in Flutter

Best practices for mapping API JSON payloads to Dart models safely.

## 1. Immutable Model Pattern (No Code-Gen)

Ideal for simple to medium entities without heavy dependencies:

```dart
class UserModel {
  final String id;
  final String email;
  final String? displayName;
  final DateTime createdAt;

  const UserModel({
    required this.id,
    required this.email,
    this.displayName,
    required this.createdAt,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'] as String,
      email: json['email'] as String,
      displayName: json['display_name'] as String?,
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'email': email,
      if (displayName != null) 'display_name': displayName,
      'created_at': createdAt.toIso8601String(),
    };
  }

  UserModel copyWith({
    String? id,
    String? email,
    String? displayName,
    DateTime? createdAt,
  }) {
    return UserModel(
      id: id ?? this.id,
      email: email ?? this.email,
      displayName: displayName ?? this.displayName,
      createdAt: createdAt ?? this.createdAt,
    );
  }
}
```

## 2. Safe Parsing Helper
Always guard against nulls or unexpected types from network responses:
```dart
int parseCount(dynamic value) {
  if (value is int) return value;
  if (value is String) return int.tryParse(value) ?? 0;
  return 0;
}
```

## 3. List Parsing Pattern
```dart
List<UserModel> parseUsers(List<dynamic> list) {
  return list
      .whereType<Map<String, dynamic>>()
      .map(UserModel.fromJson)
      .toList();
}
```
