---
name: flutter-quality
description: Flutter/Dartプロジェクトの品質チェック。dart analyze/dart format/flutter testを実行。「Flutterの品質チェック」「Flutter テスト」「Flutterのテスト実行」「Flutter lint」「Dart解析」「Flutterフォーマット」で起動。Do NOT use for 純粋なDartパッケージ（Flutterなし）。
allowed-tools: Bash, Read, Grep, Glob
---

## Tools
analyze: `dart analyze` | format: `dart format` | test: `flutter test` | coverage: `flutter test --coverage`

## Standards

| 項目 | 目標 |
|------|------|
| Analyze | issues 0 |
| Format | エラー0 |
| カバレッジ | 90%+ |

## Reference
- [reference.md](reference.md)
