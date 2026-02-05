---
name: test-async-guardian
description: "Flutter/Dart 測試異步資源管理守護者。用於：(1) 診斷測試卡住問題，(2) 審查測試代碼中的異步資源清理，(3) 提供 tearDown 最佳實踐，(4) 掃描潛在的資源洩漏風險。觸發場景：測試卡住、撰寫新測試、Code Review 測試代碼、執行 flutter test 前自動掃描。"
---

# Test Async Guardian

測試異步資源管理守護者 - 防止測試因未清理的異步資源而卡住。

## 問題背景

Dart/Flutter 測試框架會等待所有未完成的 Future 才結束測試。如果測試啟動了長延遲的異步操作但沒有正確清理，測試會無限期卡住。

## 導致測試阻塞的異步資源類型

| 資源類型 | 問題描述 | 清理方法 |
|---------|---------|---------|
| **未完成的 Future** | 長延遲異步操作沒有等待完成或取消 | `service.clearAllQueries()` 或 `service.dispose()` |
| **Timer.periodic** | 週期性定時器未取消 | `timer.cancel()` |
| **StreamController** | 廣播流未關閉 | `controller.close()` |
| **Completer** | Completer 未完成 | `completer.complete()` |

## 正確的 tearDown 模式

### 模式 A：服務清理

```dart
late BookQueryService bookQueryService;

setUp(() {
  bookQueryService = BookQueryService(apiService: mockApiService);
});

tearDown(() {
  bookQueryService.clearAllQueries();  // 清理未完成的查詢
});
```

### 模式 B：Mock 狀態重置

```dart
late MockSearchBookViewModelForBatch mockSearchViewModel;

tearDown(() {
  mockSearchViewModel.setSlowSearch(false);  // 重置慢速模式
  mockBookRepository.setSlowQuery(false);
  mockBatchEnrichBooksUseCase.setFastExecution(true);
  container.dispose();
});
```

### 模式 C：StreamController 清理

```dart
final StreamController<EnrichmentProgress> _progressController =
    StreamController<EnrichmentProgress>.broadcast();

void dispose() {
  _progressController.close();
}
```

### 模式 D：Timer 清理

```dart
Timer? _memoryMonitorTimer;

void startMonitoring() {
  _memoryMonitorTimer = Timer.periodic(interval, (_) {
    captureSnapshot();
  });
}

void dispose() {
  _memoryMonitorTimer?.cancel();
  _memoryMonitorTimer = null;
}
```

## 危險模式檢測

### 危險模式 1：長延遲沒有清理

```dart
// ❌ 危險：10 秒延遲，測試只等 10ms
when(mockApiService.queryByIsbn('xxx'))
    .thenAnswer((_) async {
  await Future.delayed(const Duration(seconds: 10));
  return data;
});
await Future.delayed(const Duration(milliseconds: 10));
// 測試結束，但 Future 還在運行！
```

**修復**：添加 tearDown 清理或縮短延遲時間。

### 危險模式 2：週期性定時器沒有取消

```dart
// ❌ 危險：Timer.periodic 未在 tearDown 中取消
Timer.periodic(Duration(seconds: 1), (timer) {
  captureSnapshot();
});
```

**修復**：保存 Timer 引用並在 dispose/tearDown 中取消。

### 危險模式 3：StreamController 未關閉

```dart
// ❌ 危險：broadcast StreamController 未關閉
final controller = StreamController<Event>.broadcast();
// 測試結束但 controller 仍在監聽
```

**修復**：在 dispose 方法中調用 `controller.close()`。

## 掃描腳本使用

### 命令行模式

```bash
# 掃描單個測試檔案（嚴格模式）
uv run .claude/skills/test-async-guardian/scripts/async_resource_scanner.py \
  test/unit/domains/scanner/book_query_service_test.dart

# 掃描整個測試目錄
uv run .claude/skills/test-async-guardian/scripts/async_resource_scanner.py \
  test/unit/ --recursive

# 警告模式（不阻止執行）
uv run .claude/skills/test-async-guardian/scripts/async_resource_scanner.py \
  test/unit/ --warn-only
```

### Hook 模式

腳本已整合為 PreToolUse Hook，在執行 `flutter test` 或 `dart test` 前自動觸發掃描。

## 診斷流程

當測試卡住時：

1. **識別卡住的測試**
   ```bash
   # 使用 timeout 限制測試時間
   timeout 30 flutter test test/unit/path/to/test.dart
   ```

2. **掃描異步資源問題**
   ```bash
   uv run .claude/skills/test-async-guardian/scripts/async_resource_scanner.py \
     test/unit/path/to/test.dart
   ```

3. **檢查報告中的問題**
   - 長延遲（>= 5 秒）
   - 缺少 tearDown
   - Timer.periodic 未取消
   - StreamController 未關閉

4. **應用修復建議**

## Resources

### scripts/

- `async_resource_scanner.py` - 異步資源掃描腳本，支援嚴格模式和 Hook 模式

### references/

- `async-cleanup-patterns.md` - 清理模式參考和真實案例

### hooks/

- `pre-test-scan.py` - PreToolUse Hook 入口腳本
