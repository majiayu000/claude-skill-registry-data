---
name: pentab-engine
description: Complete blueprint, reference architecture, and implementation guide for building an ultra-low latency Android-to-PC Pen Tablet & Windows Precision Trackpad system using Jetpack Compose, Win32 SendInput, and RFC 6455 WebSockets over ADB/Wi-Fi.
---

# Pentab Engine — 再現・再実装マスターガイド (Complete Blueprint & Implementation Skill)

本スキルは、**Android タブレットを Windows PC の「超低遅延ペンタブレット」および「Windows 高精度トラックパッド」として機能させるシステム（クライアント & サーバー）** をゼロから完全に再構築・再実装するための包括的開発ガイドです。

---

## 1. システム要件 & アーキテクチャ

### 1.1 技術スタック
- **Android クライアント**:
  - 言語/フレームワーク: Kotlin 2.2.10 / Jetpack Compose BOM 2026.02.01 / Material 3
  - 最小/ターゲット SDK: minSdk `24` / targetSdk `37`
  - 通信/シリアライズ: OkHttp `4.12.0` / Gson `2.11.0`
  - 入力捕捉: Native `View` (`onTouchEvent`, `onGenericMotionEvent`) + Compose Overlay
- **Windows PC サーバー**:
  - 言語/フレームワーク: C# / .NET 8 / WPF (`net8.0-windows`)
  - OS 入力注入: Win32 API (`user32.dll` -> `SetCursorPos`, `mouse_event`, `SendInput`)
  - 通信: `System.Net.Sockets.TcpListener` による RFC 6455 準拠の自作 WebSocket サーバー（外部 NuGet 不要）
  - システム連携: `System.Windows.Forms.NotifyIcon` (トレイ常駐), レジストリ `HKCU\...\Run` (自動起動)

---

## 2. 通信プロトコル仕様 (WebSocket JSON on Port 8765)

### 2.1 データモデル (`PenData`)

```kotlin
// Android (Kotlin / Gson)
data class PenData(
    @SerializedName("mode") val mode: String = "TRACKPAD",     // "ABSOLUTE" or "TRACKPAD"
    @SerializedName("x") val x: Float = 0f,                    // Normalized 0.0 - 1.0
    @SerializedName("y") val y: Float = 0f,                    // Normalized 0.0 - 1.0
    @SerializedName("dx") val dx: Float = 0f,                  // Relative Delta X in px
    @SerializedName("dy") val dy: Float = 0f,                  // Relative Delta Y in px
    @SerializedName("pressure") val pressure: Float = 1.0f,    // 0.0 - 1.0
    @SerializedName("tiltX") val tiltX: Float = 0f,            // Tilt X
    @SerializedName("tiltY") val tiltY: Float = 0f,            // Tilt Y
    @SerializedName("toolType") val toolType: Int = 1,         // 1=Finger, 2=Stylus, 3=Eraser
    @SerializedName("action") val action: String,              // "MOVE", "DOWN", "UP", "CLICK", "SCROLL", etc.
    @SerializedName("clickType") val clickType: String = "",   // "LEFT", "RIGHT", "MIDDLE", "DOUBLE_LEFT"
    @SerializedName("buttonState") val buttonState: Int = 0,   // MotionEvent buttonState
    @SerializedName("scrollDelta") val scrollDelta: Int = 0,   // Wheel delta
    @SerializedName("timestamp") val timestamp: Long = System.currentTimeMillis()
)
```

```csharp
// Windows PC (C# / System.Text.Json)
public class PenData
{
    [JsonPropertyName("mode")] public string Mode { get; set; } = "ABSOLUTE";
    [JsonPropertyName("x")] public float X { get; set; }
    [JsonPropertyName("y")] public float Y { get; set; }
    [JsonPropertyName("dx")] public float Dx { get; set; }
    [JsonPropertyName("dy")] public float Dy { get; set; }
    [JsonPropertyName("pressure")] public float Pressure { get; set; }
    [JsonPropertyName("tiltX")] public float TiltX { get; set; }
    [JsonPropertyName("tiltY")] public float TiltY { get; set; }
    [JsonPropertyName("toolType")] public int ToolType { get; set; }
    [JsonPropertyName("action")] public string Action { get; set; } = string.Empty;
    [JsonPropertyName("clickType")] public string ClickType { get; set; } = string.Empty;
    [JsonPropertyName("buttonState")] public int ButtonState { get; set; }
    [JsonPropertyName("scrollDelta")] public int ScrollDelta { get; set; }
    [JsonPropertyName("timestamp")] public long Timestamp { get; set; }
}
```

---

## 3. Android クライアント実装レシピ (ステップバイステップ)

### Step 1: `AndroidManifest.xml` 設定
- `android.permission.INTERNET`, `android.permission.ACCESS_NETWORK_STATE` を付与。
- `MainActivity` に `android:screenOrientation="sensorLandscape"`, `android:configChanges="orientation|screenSize|screenLayout|keyboardHidden"` を指定。

### Step 2: `WebSocketManager.kt` の実装
- `OkHttpClient.Builder()` で `pingInterval(3, TimeUnit.SECONDS)`, `retryOnConnectionFailure(true)` を構成。
- `StateFlow<ConnectionState>` で接続状態を公開。
- `connectUrl(url)` で接続し、`onClosed` / `onFailure` 時に 2 秒待機後 `attemptReconnect()` を実行。
- デッドソケット滞留防止のため、再接続時に `client.connectionPool.evictAll()` を実行。

### Step 3: `PentabSurfaceView` (高精度タッチ & ジェスチャー) の実装
- **1本指相対移動**:
  ```kotlin
  val rawDx = (curX - prevX).coerceIn(-80f, 80f)
  val rawDy = (curY - prevY).coerceIn(-80f, 80f)
  val dist = hypot(rawDx.toDouble(), rawDy.toDouble()).toFloat()
  val speedFactor = when {
      dist < 2.5f -> 1.0f
      dist < 8.0f -> 1.35f
      dist < 25.0f -> 1.85f
      else -> 2.4f
  }
  webSocketManager.sendPenData(PenData(mode = "TRACKPAD", dx = rawDx * speedFactor, dy = rawDy * speedFactor, action = "MOVE"))
  ```
- **2本指スクロール**:
  ```kotlin
  val avgY = (event.getY(p0) + event.getY(p1)) / 2f
  val scrollDeltaY = avgY - lastTwoFingerY
  if (abs(scrollDeltaY) > 1.2f) {
      val wheelDelta = (scrollDeltaY * 7.5f).toInt()
      webSocketManager.sendPenData(PenData(mode = "TRACKPAD", action = "SCROLL", scrollDelta = wheelDelta))
  }
  ```
- **タップ判定 (ACTION_UP)**:
  - 1本指かつ時間 `< 270ms` かつ 移動距離 `< 28px`: `clickType = "LEFT"`
  - 2本指かつ時間 `< 350ms` かつ 移動距離 `< 45px`: `clickType = "RIGHT"`
  - 3本指かつ時間 `< 350ms` かつ 移動距離 `< 50px`: `clickType = "MIDDLE"`
- **ダブルタップ & ドラッグ (1.5 Tap)**:
  - 直前のタップ Up から `< 320ms` かつ 距離 `< 50px` で Down した場合、`isDoubleTapDragging = true` とし `DOWN_LEFT` を送信。
- **操作パネル領域の除外 (`isInsideTrackpad`)**:
  - フローティングパネルの RectF 領域に触れた場合はトラックパッド移動をスキップ。

### Step 4: UI 統合 & Immersive Mode
- Compose の `PenInputScreen` 上にフローティング操作パネル（ドラッグ位置移動、Left Click 長押しドラッグ、Right Click、Middle Click、Drag Lock、縦横切替）を配置。
- `WindowCompat.getInsetsController(window, window.decorView).hide(WindowInsetsCompat.Type.systemBars())` で全画面化。

---

## 4. PC WPF サーバー実装レシピ (ステップバイステップ)

### Step 1: `InputInjector.cs` (Win32 P/Invoke)
```csharp
[DllImport("user32.dll", SetLastError = true)]
private static extern bool SetCursorPos(int X, int Y);

[DllImport("user32.dll", SetLastError = true)]
private static extern void mouse_event(uint dwFlags, int dx, int dy, uint dwData, UIntPtr dwExtraInfo);

private const uint MOUSEEVENTF_MOVE = 0x0001;
private const uint MOUSEEVENTF_LEFTDOWN = 0x0002;
private const uint MOUSEEVENTF_LEFTUP = 0x0004;
private const uint MOUSEEVENTF_RIGHTDOWN = 0x0008;
private const uint MOUSEEVENTF_RIGHTUP = 0x0010;
private const uint MOUSEEVENTF_MIDDLEDOWN = 0x0020;
private const uint MOUSEEVENTF_MIDDLEUP = 0x0040;
private const uint MOUSEEVENTF_WHEEL = 0x0800;
```
- 相対移動: `mouse_event(MOUSEEVENTF_MOVE, dx, dy, 0, UIntPtr.Zero)`
- 絶対移動: `SetCursorPos(pixelX, pixelY)`
- クリック: Down -> `Thread.Sleep(20)` -> Up

### Step 2: `ScreenMapper.cs` (マルチモニター座標変換)
- `Screen.AllScreens` を取得。
- 正規化座標 (`normX`, `normY`) を対象モニターの `(targetLeft + normX * width, targetTop + normY * height)` にマッピング。

### Step 3: `WebSocketServer.cs` (RFC 6455 高速 TcpListener)
- `TcpListener(IPAddress.Any, 8765)` を起動。
- `Sec-WebSocket-Key` + `"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"` の SHA1 ハッシュを Base64 化して `HTTP 101` を返答。
- マスク付きフレームをアンマスク処理し、JSON を `PenData` にデシリアライズして `InputInjector.Inject()` を実行。
- Ping (`0x9`) を受信したら Pong (`0xA`) を即座に返信。

### Step 4: システムトレイ & 自動起動 (`MainWindow.xaml.cs` / `AppSettings.cs`)
- `System.Windows.Forms.NotifyIcon` を初期化し、最小化時や「×」ボタン押下時にトレイへ格納。
- `Registry.CurrentUser.OpenSubKey(@"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", true)` に `--minimized` 引数付きで登録。

---

## 5. 接続 & テスト実行コマンド

```powershell
# 1. USB ADB Reverse 設定 (最も低遅延)
adb reverse tcp:8765 tcp:8765

# 2. Android デバッグビルド & インストール
./gradlew.bat assembleDebug
adb install -r app/build/outputs/apk/debug/app-debug.apk

# 3. PC サーバービルド & 起動
dotnet build -c Debug
dotnet run
```
