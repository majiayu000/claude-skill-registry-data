---
name: vacuumtube
description: "VacuumTube（/opt/VacuumTube/vacuumtube）を Chromium や playwright ではなく直接 remote debugging（CDP, 既定: http://127.0.0.1:9992）で操作して、YouTube TV のホームや視聴画面から BGM・音楽・ニュース動画を選択/再生する。ユーザーが「BGM再生して」「音楽再生して」「ライブニュース再生して」「国連総会の最新ニュース動画見たい」など依頼したときに使う。"
---

# vacuumtube Skill

VacuumTube を直接操作するためのスキルです。`Chromium` / `playwright-cli` を使うのではなく、VacuumTube の Electron/Chromium に対して **CDP (Chrome DevTools Protocol)** で接続して DOM を読み、動画タイルを選択します。

## 前提

- VacuumTube 本体: `/opt/VacuumTube/vacuumtube`
- Remote debugging: `127.0.0.1:9992`
- 推奨起動: `~/vacuumtube.sh`
  - `~/.config/VacuumTube/flags.txt` に `--remote-debugging-port=9992` を設定して起動する

確認（CDP）:

```bash
curl -fsS http://127.0.0.1:9992/json/version
curl -fsS http://127.0.0.1:9992/json/list | jq '.[] | {type,title,url}'
```

確認（プロセス/ウィンドウ存在）:

```bash
pgrep -af '^/opt/VacuumTube/vacuumtube( |$)'
DISPLAY=:1 wmctrl -l | rg -i 'VacuumTube'
```

## 重要ルール

- `playwright-cli` や通常の Chromium 操作に逃げない。対象は **VacuumTube**。
- スクリーンショット前提で判断しない。CDP で DOM を見る。
- `Esc` を連打しない。
  - 画面状態によっては終了/想定外遷移の原因になる。
  - 戻る/ホーム遷移はまず `location.hash` を使う。
- VacuumTube 設定オーバーレイ（`#vt-settings-overlay-root`）が重なっている場合がある。
  - DOM で存在判定し、必要なら `display:none` / `visibility:hidden` で一時的に退避してからタイル選択する。

## 典型ユースケース

- `BGM再生して`
- `音楽再生して`
- `ライブニュース再生して`
- `国連総会の最新ニュース動画見たい`

## 基本ワークフロー（推奨）

1. `:9992` の CDP エンドポイントを確認
2. `json/list` から `youtube.com/tv` の `page` target を取得
3. CDP (`Runtime`, `Page`, 必要なら `Input`) を有効化
4. 現在ルートを確認
   - `location.hash` が `#/watch?...` なら、必要に応じて `location.hash = '#/'` でホームへ戻す
5. DOM を横断（shadow DOM 含む）して `ytlr-tile-renderer` を列挙
6. 可視タイルだけを抽出し、要求に応じてスコアリング
7. 選択
   - まず DOM の `tile.click()` / `focus()`
   - 反応しない場合はタイル中心座標へ `Input.dispatchMouseEvent`
8. `location.hash` が `#/watch?v=...` に変わったら成功
9. 必要なら再生状態を確認（ただし選択直後の `paused=true` は瞬間値のことがある）

## 起動・停止（実務向け）

### 既存プロセスの停止

```bash
pkill -TERM -f '^/opt/VacuumTube/vacuumtube( |$)' || true
```

### `tmux` でバックグラウンド起動（推奨）

VacuumTube を長時間運用する場合は、`tmux` でデタッチ起動しておくと安定します。

```bash
tmux new-session -d -s vacuumtube-bg \
  "bash -lc 'export VACUUMTUBE_DISPLAY=:1; export XAUTHORITY=\"$HOME/.Xauthority\"; exec ~/vacuumtube.sh'"
```

確認:

```bash
tmux ls | rg '^vacuumtube-bg:'
pgrep -af '^/opt/VacuumTube/vacuumtube( |$)'
curl -fsS http://127.0.0.1:9992/json/version
```

### 起動直後の初期化（起動操作の完了条件）

VacuumTube の「起動操作」は、**プロセス起動だけでなく**次の 2 点まで含める。

1. 起動直後のアカウント選択画面で `YuisekinTV` を選ぶ
2. VacuumTube ウィンドウをデスクトップ右上に配置する

#### 1) アカウント `YuisekinTV` を選択

- 起動直後は YouTube TV のアカウント選択画面になることがある
- 画面文言の目安: `アカウントを追加`, `ゲストとして視聴`
- `YuisekinTV` の表示は DOM 上で `Yui ekinTV` のように空白分割されることがある（厳密文字列一致に依存しない）

実務上の安定手順:

- まず CDP でアカウント選択画面か判定
- 起動直後の既定フォーカスが `YuisekinTV` なら、`Enter` 1 回で選択
- 成功判定は、アカウント選択文言が消え、ホーム画面文言（例: `あなたへのおすすめ`）が出ること

補足:

- DOM から `YuisekinTV` 要素を直接引けない場合がある（テキスト分割/特殊レンダリング）
- その場合は `Enter` による既定フォーカス選択を優先する

#### 2) 右上に移動（desktop-windows-layout スキル併用）

起動後は `desktop-windows-layout` スキルの手順で右上タイルに配置する。

```bash
export DISPLAY=:1
WIN_ID=$(wmctrl -l | awk '/VacuumTube$/ {print $1; exit}')
xdotool windowactivate --sync "$WIN_ID"
timeout 2s qdbus org.kde.kglobalaccel /component/kwin \
  org.kde.kglobalaccel.Component.invokeShortcut \
  'Window Quick Tile Top Right' default || true
wmctrl -lG | awk -v id="$WIN_ID" '$1==id {print}'
```

期待値（この環境の実測）:

- `X=2048, Y=28, WIDTH=2048, HEIGHT=1052`

これで「VacuumTube 起動操作完了」として扱う。

### `tmux` 起動でハマりやすい点

- `tmux` サーバーが SSH/X11 forwarding の `DISPLAY=localhost:10.0` を保持していることがある
  - そのまま `~/vacuumtube.sh` を起動すると、VacuumTube が `localhost:10.0` を使おうとして失敗する
  - 実測エラー例: `Missing X server or $DISPLAY`
- 対策:
  - `VACUUMTUBE_DISPLAY=:1` を明示する（上記コマンド）
  - 必要に応じて `XAUTHORITY="$HOME/.Xauthority"` も明示する

失敗時のログ確認用（セッションが即終了する場合）:

```bash
tmux new-session -d -s vacuumtube-bg-debug \
  "bash -lc 'export VACUUMTUBE_DISPLAY=:1; export XAUTHORITY=\"$HOME/.Xauthority\"; ~/vacuumtube.sh; ec=$?; echo EXIT:$ec; sleep 20'"
tmux capture-pane -pt vacuumtube-bg-debug:0 -S -80
```

## 画面状態の判定（CDP / Runtime.evaluate）

最低限見る値:

- `location.href`, `location.hash`
- `document.title`
- `document.activeElement?.tagName`
- `document.body?.innerText`（先頭だけ）
- `#vt-settings-overlay-root` の可視状態
- `ytlr-tile-renderer`（可視タイル数とタイトル文字列）

動画要素の確認（任意）:

```js
const v =
  window.yt?.player?.utils?.videoElement_ || document.querySelector("video");
```

取得項目:

- `v.paused`
- `v.currentTime`
- `v.muted`
- `v.volume`

注意:

- **選択直後**は `paused=true`, `currentTime=0`, `muted=true` が見えることがある
- ユーザー体感で再生されていれば、route 遷移確認を優先して成功扱いにしてよい

## 選択ロジック（ヒューリスティック）

### 1) BGM / 音楽

優先キーワード（加点）:

- `ambient`, `ambience`, `relax`, `study`, `focus`, `music`, `bgm`, `lofi`, `jazz`, `piano`, `sleep`, `atmosphere`, `chill`
- `deep focus`, `flow state`, `serene`, `ethereal`, `winter`, `hyperflow`

除外（減点）:

- `news`, `速報`, `総理`, `国会`, `ウクライナ` などニュース系

### 2) ライブニュース / 最新ニュース

優先キーワード（加点）:

- `live`, `news`, `breaking`, `ライブ`, `速報`, `会見`, `ANN`, `TBS`, `NHK`, `BBC`, `Reuters`
- 要求語に合わせる: `国連`, `国連総会`, `停戦`, `ウクライナ` など

鮮度の目安（加点）:

- `minutes ago`, `hours ago`, `分前`, `時間前`, `live`

除外（減点）:

- 長尺 BGM / ambience / focus music など

## 国連総会など、具体トピック要求の扱い

優先順:

1. **ホーム可視タイル**に該当トピックがあるか CDP DOM で確認して再生
2. 可視タイルになければ、ホーム内の非可視タイル（DOM上に存在）をスコアリングして選択
3. それでも無ければ、外部検索/YouTube検索で動画IDを特定して `location.hash = '#/watch?v=<VIDEO_ID>'` を使う

補足:

- 「最新」を求められた場合は、タイトルだけでなく `○分前/○時間前` 等の表示を優先する
- 取得結果が曖昧なら、候補を 2-3 件提示して確認を取る

## クリック手順（実務上のコツ）

- DOM `click()` が効かないことがある
- その場合、**タイル中心座標**に対して CDP の mouse event を送ると通りやすい
- 先に `wmctrl -a VacuumTube` で前面化しておくと安定しやすい

例（前面化）:

```bash
DISPLAY=:1 wmctrl -a VacuumTube
```

## よくある失敗と対処

- `curl http://127.0.0.1:9992/json/version` が失敗:
  - VacuumTube が remote debugging なしで起動している
  - `~/vacuumtube.sh` で起動し直す
  - `tmux` 起動時は `VACUUMTUBE_DISPLAY=:1` 指定を確認
- `json/list` に `youtube.com/tv` がない:
  - 起動直後の読み込み途中。数秒待って再試行
- クリックしても遷移しない:
  - DOM `click()` → 座標クリックの順で試す
- 画面がおかしい / タイルが少ない:
  - VacuumTube の設定オーバーレイが重なっていないか確認
- `Esc` で戻れない/変な画面になる:
  - `Esc` 多用をやめて `location.hash = '#/'` を優先

## 実行時に見るべき最低限の成功条件

- `location.hash` が `#/watch?v=...` になった
- `document.body.innerText` 先頭が視聴画面らしい表示（再生時間/概要/チャンネル登録など）に変化した
- （任意）`video.currentTime` が増加、またはユーザー体感で再生確認済み

## ローカル参照

- VacuumTube ソース: `repos/_youtube/VacuumTube`
- 手動起動スクリプト: `~/vacuumtube.sh`
- 本体バイナリ: `/opt/VacuumTube/vacuumtube`
