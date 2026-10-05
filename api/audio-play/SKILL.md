---
name: audio-play
description: "KDE Plasma / PipeWire(PulseAudio互換) 環境で通知音・効果音・テストトーン・VOICEVOX発話（VOICEBOX表記含む）を確実に再生する。現在は repos/acaption の IPC を使った字幕付き再生/通知を主経路とし、paplay/notify-send をフォールバックとして扱う。"
---

# audio-play Skill

KDE Plasma デスクトップ上で音を再生するためのスキルです。現在は `repos/acaption` の IPC (`127.0.0.1:47832`) を使った字幕付き再生/通知を主経路とし、`paplay` / `pw-play` / `canberra-gtk-play` / `notify-send` はフォールバック/切り分け用途として扱います。

この環境では「通知は出るが音が聞こえない」問題が起きやすいため、**音の出力先（sink）を明示して検証する**のが基本です。

## 前提

- デスクトップ: KDE Plasma（X11, 通常 `DISPLAY=:1`）
- 音声基盤: PipeWire（PulseAudio 互換）
- よく使うコマンド:
  - `pactl`, `wpctl`
  - `tmux`（overlay 起動確認）
  - `paplay`（最優先）
  - `notify-send`
  - `canberra-gtk-play`（通知風効果音）
  - `pw-play`（代替）
  - `curl`（VOICEVOX API）

## 重要ルール

- まず **音の経路確認**を行う（`pactl info`, `pactl list short sinks`）
- まず `acaption` IPC を使う（字幕と音声の同期を確保）
- 重要な再生は `paplay --device=<sink>` で **sink を明示**する（フォールバック/切り分け）
- `notify-send` 単体で「通知音が鳴る」と期待しない
  - 通知表示はできても、音は別コマンドが必要なことがある
- `canberra-gtk-play` は `DISPLAY` が必要（`DISPLAY=:1`）
- `paplay` 系は `DISPLAY` 不要だが、`XDG_RUNTIME_DIR` が必要なことがある
- 「聞こえない」ときは、短い効果音より **長めのテストトーン**で切り分ける

## 典型ユースケース

- `notify-send の代わりにちゃんと聞こえる通知音を鳴らして`
- `いま音が出るか確認して`
- `VOICEVOX で「作業が終わりました」と喋らせて`
- `VacuumTube と同じ出力先（テレビ）に音を出して`

## 基本ワークフロー（推奨）

1. 出力先（sink）確認
2. Tauri 字幕オーバーレイ IPC の起動確認
3. 明確なテスト音で再生確認（`paplay` + 明示 sink）
4. 必要に応じて `notify-send` と組み合わせる
5. VOICEVOX 利用時は API 生存確認 → WAV 生成 → overlay IPC（失敗時 `paplay`）

## acaption 字幕オーバーレイ（主経路）

字幕付きの通知/発話は `repos/acaption` を使う。`voice_command_loop` 連携時の overlay 管理は `yuiclaw voice-command operator` から行う。

```bash
yuiclaw voice-command operator status
yuiclaw voice-command operator start-overlay
yuiclaw voice-command operator logs-overlay
```

期待:

- `overlay: RUNNING (acaption-overlay)`
- `overlay endpoint ready: 127.0.0.1:47832`

### IPC でテキスト通知（字幕のみ）

```bash
python3 - <<'PY'
import json, socket
payload = {"type": "notify", "text": "通知テストです", "duration_ms": 1800}
with socket.create_connection(("127.0.0.1", 47832), timeout=5) as s:
    s.sendall((json.dumps(payload, ensure_ascii=False) + "\n").encode("utf-8"))
    s.shutdown(socket.SHUT_WR)
    print(s.recv(4096).decode("utf-8").strip())
PY
```

## 出力先（sink）確認

```bash
pactl info | sed -n '1,40p'
pactl list short sinks
wpctl status
```

見るべき項目:

- `Default Sink`
- sink 名（例: `alsa_output.pci-0000_04_00.1.hdmi-stereo`）
- `Mute: no`
- 音量

補足:

- `State: SUSPENDED` はアイドル時には普通
- `VacuumTube` の音がテレビから出ているなら、同じ HDMI sink を使うとよい

## 通知表示 + 音（フォールバック）

`notify-send` は通知表示、音は別コマンドで鳴らす。字幕オーバーレイが使えない場合のフォールバック。

```bash
export DISPLAY=:1
notify-send "完了" "処理が終わりました"
paplay --device=alsa_output.pci-0000_04_00.1.hdmi-stereo \
  /usr/share/sounds/freedesktop/stereo/message.oga
```

### `canberra-gtk-play` を使う場合

```bash
export DISPLAY=:1
notify-send "通知" "効果音テスト"
canberra-gtk-play -i dialog-information
```

注意:

- `AT-SPI` 警告が出ることがあるが、再生自体は成功する場合がある
- 成功しても音が小さい/短いと気づきにくい

## `notify-send` 単体で音が鳴らないときの理由（この環境）

KDE/Plasma の通知デーモン capability に `sound-name` / `sound-file` が無い場合、`notify-send -h ...` で音ヒントを渡しても効かない。

確認:

```bash
qdbus org.freedesktop.Notifications /org/freedesktop/Notifications \
  org.freedesktop.Notifications.GetCapabilities
```

この環境の実測では、`sound-name` / `sound-file` は未対応。

## 明確なテスト音（聞こえるか切り分け）

短い通知音で判断しづらいときは、1kHz テストトーンを生成して再生する。

```bash
python3 - <<'PY'
import math, wave, struct
path = '/tmp/codex-tone-1khz.wav'
rate = 48000
dur = 1.8
freq = 1000.0
amp = 0.35
n = int(rate * dur)
with wave.open(path, 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(rate)
    for i in range(n):
        v = int(32767 * amp * math.sin(2 * math.pi * freq * i / rate))
        w.writeframesraw(struct.pack('<hh', v, v))
PY

paplay --device=alsa_output.pci-0000_04_00.1.hdmi-stereo \
  --volume=65536 /tmp/codex-tone-1khz.wav
```

## VOICEVOX 発話（WAV生成→再生）

### 1) API の生存確認

```bash
curl -fsS http://127.0.0.1:50021/version
```

起動していない場合:

- VOICEVOX AppImage / アプリを起動
- API ポート `50021` が開くまで待つ

### 2) 利用可能な話者を確認（任意）

```bash
curl -fsS http://127.0.0.1:50021/speakers | jq '.[].name'
```

### 3) 音声クエリ生成 → 合成 → overlay IPC 再生（推奨）

以下は `speaker=89`（Voidoll）の例。まずは overlay IPC へ `speak` を送る。

```bash
TEXT='作業が終わりました'
SPEAKER=89
OUT=/tmp/voicevox-notify.wav
TEXT_ENC=$(python3 -c 'import sys, urllib.parse; print(urllib.parse.quote(sys.argv[1]))' "$TEXT")

curl -fsS -X POST \
  "http://127.0.0.1:50021/audio_query?text=${TEXT_ENC}&speaker=${SPEAKER}" \
  -H 'accept: application/json' > /tmp/voicevox-query.json

curl -fsS -X POST \
  "http://127.0.0.1:50021/synthesis?speaker=${SPEAKER}" \
  -H 'Content-Type: application/json' \
  --data-binary @/tmp/voicevox-query.json \
  > "$OUT"

python3 - <<'PY' "$TEXT" "$OUT"
import json, socket, sys
text, wav = sys.argv[1], sys.argv[2]
payload = {"type":"speak","text": text, "wav_path": wav, "wait": True}
with socket.create_connection(("127.0.0.1", 47832), timeout=5) as s:
    s.sendall((json.dumps(payload, ensure_ascii=False) + "\n").encode("utf-8"))
    s.shutdown(socket.SHUT_WR)
    print(s.recv(4096).decode("utf-8").strip())
PY
```

実務メモ:

- URL エンコードが必要（日本語テキスト）
- `Tauri` overlay が落ちている場合は `paplay --device=<sink> "$OUT"` で切り分ける
- `VOICEVOX` 側の合成成功と、再生成功は別問題（出力先違いで無音に見える）

## 出力先を切り替えて試す（必要時のみ）

一時的にデフォルト sink を切り替えて検証できる。

```bash
wpctl status
wpctl set-default <SINK_ID>
paplay /usr/share/sounds/freedesktop/stereo/bell.oga
```

注意:

- デフォルト変更は他アプリ（VacuumTube 等）にも影響する
- まずは `paplay --device=...` での明示再生を優先する

## よくある失敗と対処

- `notify-send` は表示されるが音が鳴らない
  - `notify-send` 単体を諦める。`paplay` / `canberra-gtk-play` を併用
- overlay 字幕は出るが音が出ない
- `yuiclaw voice-command operator logs-overlay` を確認
  - `paplay --device=<sink>` で WAV を直接再生して切り分け
- `canberra-gtk-play` が `Cannot open display`
  - `DISPLAY=:1` を付ける
- `paplay` は成功するが聞こえない
  - sink が違う。`pactl info` の `Default Sink` と実際の出力先を照合
  - `paplay --device=<sink>` で明示
- 通知音が「鳴った気がしない」
  - サンプル音が短い/小さい。1kHz テストトーンで切り分ける
- `speaker-test -D pulse` が失敗
  - ALSA の `pulse` PCM プラグイン未導入のことがある。`paplay` を使う
- `tmux` / SSH 経由で `notify-send` / `canberra-gtk-play` が不安定
  - `DISPLAY=:1` を明示
  - 必要なら `XDG_RUNTIME_DIR=/run/user/$(id -u)` を明示

## 成功条件（報告時）

- 再生した音の種類（通知音 / 効果音 / テストトーン / VOICEVOX）
- 使用したコマンドと sink
- コマンドの成功可否
- 必要なら「ユーザーに聞こえたか」の確認

## ローカル参照（この環境で有用）

- freedesktop 効果音: `/usr/share/sounds/freedesktop/stereo/`
- caption overlay: `repos/acaption`
- 音声待ち受け operator 管理: `yuiclaw voice-command operator ...`
- 典型 sink（実測例）:
  - `alsa_output.pci-0000_04_00.1.hdmi-stereo`（HDMI / テレビ）
  - `alsa_output.pci-0000_0c_00.4.iec958-stereo`（S/PDIF）
