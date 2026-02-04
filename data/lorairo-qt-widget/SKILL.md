---
name: lorairo-qt-widget
description: PySide6 widget implementation for LoRAIro GUI with Signal/Slot pattern, Direct Widget Communication, and Qt Designer integration best practices
allowed-tools: mcp__serena__find_symbol, mcp__serena__get_symbols_overview, mcp__serena__read_memory, Read, Edit, Write, Bash
---

# LoRAIro Qt Widget Skill

このSkillは、LoRAIroプロジェクトにおけるPySide6ウィジェット実装のベストプラクティスを提供します。

## 使用タイミング

- 新しいGUIウィジェットの実装
- 既存ウィジェットのリファクタリング
- Signal/Slot接続の実装
- Qt Designerファイル統合

## LoRAIroの Widget実装パターン

### 基本構造

```python
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal, Slot
from typing import Optional
from loguru import logger

class ExampleWidget(QWidget):
    """サンプルウィジェット

    Signals:
        data_changed: データ変更時に発火（新しいデータを送信）
        action_requested: ユーザーアクション時に発火
    """

    # 型安全なシグナル定義
    data_changed = Signal(str)  # str型のデータを送信
    action_requested = Signal()  # パラメータなし

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._setup_ui()
        self._connect_signals()
        self._data: Optional[str] = None

    def _setup_ui(self) -> None:
        """UI初期化"""
        # Qt Designerファイル使用時:
        # from .ExampleWidget_ui import Ui_ExampleWidget
        # self._ui = Ui_ExampleWidget()
        # self._ui.setupUi(self)

        # 手動レイアウト時:
        layout = QVBoxLayout()
        self.setLayout(layout)

    def _connect_signals(self) -> None:
        """内部Signal/Slot接続"""
        # self._ui.button.clicked.connect(self._on_button_clicked)
        pass

    @Slot(str)
    def set_data(self, data: str) -> None:
        """データ設定（外部から呼び出し可能）"""
        if self._data != data:
            self._data = data
            self._update_display()
            self.data_changed.emit(data)

    def _update_display(self) -> None:
        """表示更新（内部処理）"""
        # UI更新ロジック
        pass

    @Slot()
    def _on_button_clicked(self) -> None:
        """ボタンクリックハンドラ（プライベート）"""
        logger.debug("Button clicked")
        self.action_requested.emit()
```

## 重要な実装パターン

### 1. Direct Widget Communication

```python
# LoRAIroの推奨パターン: Widget間直接接続

class ThumbnailWidget(QWidget):
    """サムネイル表示ウィジェット"""
    image_metadata_selected = Signal(dict)  # メタデータを直接送信

    def _on_thumbnail_clicked(self, index: int) -> None:
        """サムネイルクリック時"""
        metadata = self._image_metadata[index]
        self.image_metadata_selected.emit(metadata)  # 直接送信

class ImageDetailsWidget(QWidget):
    """画像詳細表示ウィジェット"""

    def connect_to_thumbnail_widget(self, thumbnail_widget: ThumbnailWidget) -> None:
        """サムネイルウィジェットに直接接続"""
        thumbnail_widget.image_metadata_selected.connect(
            self._on_metadata_received
        )

    @Slot(dict)
    def _on_metadata_received(self, metadata: dict) -> None:
        """メタデータ受信時"""
        self._display_metadata(metadata)

# MainWindowでの接続
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._setup_widgets()
        self._connect_widgets()

    def _connect_widgets(self) -> None:
        """Widget間接続（一箇所に集約）"""
        self.image_details.connect_to_thumbnail_widget(self.thumbnail)
```

### 2. 型安全なSignal定義

```python
# ✅ Good: 型指定付きSignal
class DataWidget(QWidget):
    # 単一パラメータ
    data_changed = Signal(str)
    score_updated = Signal(float)
    count_changed = Signal(int)

    # 複数パラメータ
    item_selected = Signal(str, int)  # (name, index)

    # 複雑なデータは dict
    metadata_loaded = Signal(dict)

# ❌ Bad: 型なしSignal
class BadWidget(QWidget):
    data_changed = Signal()  # 何が送信されるか不明
    value_updated = Signal(object)  # 型が不明確
```

### 3. Qt Designerファイル統合

```python
# UI生成コマンド
# uv run python scripts/generate_ui.py

from .ExampleWidget_ui import Ui_ExampleWidget

class ExampleWidget(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        # Qt Designer UIのロード
        self._ui = Ui_ExampleWidget()
        self._ui.setupUi(self)

        # UI要素への接続
        self._ui.okButton.clicked.connect(self._on_ok_clicked)
        self._ui.inputField.textChanged.connect(self._on_text_changed)

    @Slot()
    def _on_ok_clicked(self) -> None:
        text = self._ui.inputField.text()
        logger.debug(f"OK clicked with text: {text}")
```

### 4. 非同期処理との統合

```python
from PySide6.QtCore import QThreadPool
from src.lorairo.gui.workers.base import LoRAIroWorkerBase

class AsyncWidget(QWidget):
    """非同期処理を扱うウィジェット"""

    def __init__(self):
        super().__init__()
        self._worker_manager = None  # WorkerManagerへの参照

    def set_worker_manager(self, worker_manager) -> None:
        """WorkerManager設定"""
        self._worker_manager = worker_manager

    def start_async_operation(self) -> None:
        """非同期操作開始"""
        worker = MyAsyncWorker(data=self._data)
        worker.signals.progress.connect(self._on_progress)
        worker.signals.finished.connect(self._on_finished)
        worker.signals.error.connect(self._on_error)

        self._worker_manager.submit(worker)

    @Slot(int, int)
    def _on_progress(self, current: int, total: int) -> None:
        """進捗更新"""
        progress = int(current / total * 100)
        self._ui.progressBar.setValue(progress)

    @Slot(object)
    def _on_finished(self, result) -> None:
        """完了処理"""
        logger.info(f"Operation finished: {result}")
        self._display_result(result)

    @Slot(str)
    def _on_error(self, error_msg: str) -> None:
        """エラー処理"""
        logger.error(f"Operation error: {error_msg}")
        QMessageBox.warning(self, "Error", error_msg)
```

## LoRAIro固有のガイドライン

### ファイル配置
- **Widgets**: `src/lorairo/gui/widgets/`
- **Designer files**: `src/lorairo/gui/designer/*.ui`
- **Generated UI**: `src/lorairo/gui/designer/*_ui.py` (自動生成)
- **Window**: `src/lorairo/gui/window/main_window.py`

### 命名規則
- Class: `{Name}Widget`（例: `ThumbnailWidget`, `ImageDetailsWidget`）
- Signals: `{action}_{tense}` (例: `data_changed`, `item_selected`)
- Public methods: `set_*`, `get_*`, `update_*`
- Private methods: `_on_*` (イベントハンドラ), `_update_*` (内部処理)
- Slots: `@Slot()` デコレータ必須

### Direct Widget Communication原則
1. **中間レイヤー回避**: DatasetStateManager経由を避け、直接接続
2. **MainWindowで集約**: `_connect_widgets()` メソッドに全接続を集約
3. **connect_to_* メソッド**: 各Widgetに `connect_to_{other_widget}()` メソッド提供
4. **型安全**: Signal/Slotは型指定必須

## ベストプラクティス

### DO ✅
- **@Slot デコレータ**: 全Slotに `@Slot(型)` 必須
- **型ヒント**: 全メソッドに型ヒント
- **private/public分離**: `_` プレフィックスで明確化
- **connect_to_* パターン**: Widget間接続メソッド提供
- **ログ記録**: 重要なイベントはloguru でログ

### DON'T ❌
- **直接UI操作**: 外部から `widget._ui.button` は禁止
- **グローバル状態**: Widget内で共有状態を持たない
- **ビジネスロジック混入**: Widgetは表示とイベント処理のみ
- **長時間処理**: UI スレッドで重い処理を避ける（Worker使用）
- **暗黙的接続**: 自動接続に期待せず、明示的に `connect()`

## テスト戦略

```python
import pytest
from PySide6.QtWidgets import QApplication
from src.lorairo.gui.widgets.example_widget import ExampleWidget

@pytest.fixture
def app(qtbot):
    """Qt application fixture"""
    return QApplication.instance() or QApplication([])

@pytest.fixture
def widget(qtbot):
    """Widget fixture"""
    w = ExampleWidget()
    qtbot.addWidget(w)
    return w

def test_signal_emission(qtbot, widget):
    """Signal発火テスト"""
    with qtbot.waitSignal(widget.data_changed, timeout=1000) as blocker:
        widget.set_data("test data")

    assert blocker.args[0] == "test data"

def test_button_click(qtbot, widget):
    """ボタンクリックテスト"""
    with qtbot.waitSignal(widget.action_requested):
        qtbot.mouseClick(widget._ui.button, Qt.LeftButton)
```

## 参考リソース
- 既存Widget: `src/lorairo/gui/widgets/`
- MainWindow: `src/lorairo/gui/window/main_window.py`
- Worker Base: `src/lorairo/gui/workers/base.py`
- テスト例: `tests/gui/widgets/`
