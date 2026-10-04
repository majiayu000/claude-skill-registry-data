---
name: ios-simulator-automation
description: Xcode 27 の iOS シミュレータをコマンドと MCP で操作・検証するときの道具の選び方と落とし穴。Device Hub を開かずに済む経路と、開くしかない操作の区別。タップ・スワイプ・撮影・回転・要素ツリーの取得、状態の作り込み、xcodebuildmcp / axe / simctl / devicectl / Device Hub / Xcode MCP の使い分けを扱う。シミュレータで画面を確認したい、タップが効かない、要素の座標が取れない、回転させたい、スクリーンショットを撮りたい、UI 自動操作が不安定、Device Hub を開かずに済ませたい、といったときに使う。
---

# iOS シミュレータの自動操作

シミュレータを操作する道具は複数あり、**同じことができる道具でも、動くものと動かないものが混ざっている**。
何を使うかだけでなく、**なぜそれを選んだのか**を区別して持っておく。壊れているから避けているのか、
それが本来の道なのかが分からないと、下の層が直ったときに見直せない。

## 対象バージョン

**Xcode 27.0 および 27.1 beta / iOS 27.0 / 27.1 のシミュレータ / macOS 26**。実測は 2026-09-20。

**Xcode 26 以前には当てはまらない。** 下の背景のとおり、土台ごと入れ替わっている。

複数の Xcode を入れている場合、`xcrun` も MCP も **`xcode-select` が指すほう**を使う。
別バージョンのランタイム（折りたたみ端末など）を触るときは、そのコマンドにだけ
`DEVELOPER_DIR=...` を付ける。

## 背景 — なぜ Xcode 27 で変わったのか

**Xcode 27 で `Simulator.app` が廃止され、`Device Hub` に置き換わった。**
ファイルの位置も `<Xcode>.app/Contents/Developer/Applications/Simulator.app` から
`<Xcode>.app/Contents/Applications/DeviceHub.app` へ移った（bundle id は `com.apple.dt.Devices`）。
27.0 / 27.1 beta とも旧パスに `Simulator.app` は存在しない。

置き換えの中身は**統合**である。Simulator は端末ごとに別ウインドウを開く作りだったが、
Device Hub は左に端末の一覧、右にその詳細という1ウインドウにまとめ、
**シミュレータと実機を同じ画面で扱う。** 回転・撮影・ダークモード・文字サイズ・リサイズ・
実機へのアプリ起動が、すべて同じ場所から行える。

このスキルの内容は、ほぼすべてこの移行から導かれる。

- **`devicectl` がシミュレータも扱うようになった。** `devicectl` はもともと実機用の CLI だったが、
  統合に合わせて拡張された。**`simctl` に無い回転が `devicectl` にあるのはこのため。**
  新しく何かをしたいときは、`simctl` だけでなく `devicectl` も見る
- **既存のツールが軒並み壊れた。** `Simulator.app` のパスや前提に依存していたものが動かなくなり、
  CI やテスト基盤が対応途中にある。このスキルに出てくる「成功と返すのに効かない」たぐいの失敗も、
  **この移行期にあたっているためと考えられる**（Apple の説明があるわけではなく、こちらの推測）。
  だからこそ、回避策には「いつ見直すか」を必ず書く

参考: [Michael Tsai — Xcode 27's Device Hub](https://mjtsai.com/blog/2026/06/25/xcode-27s-device-hub/) /
[Bitrise — WWDC 2026: Device Hub and what it means for CI/CD](https://bitrise.io/blog/post/wwdc-2026-device-hub-and-what-it-means-for-ci-cd)

## Device Hub 経由かどうか

これが最初の分かれ目になる。**Device Hub は画面を占有してユーザーの作業を止めるので、
直接叩ける経路で済むならそちらを使う。**

ただし前提が1つある。**ここに書いた検証はすべて Device Hub が起動している状態で行った。**
Device Hub を終了するとシミュレータも一緒に落ちるため、閉じた状態での可否は確かめていない。
実務上 Device Hub は常に起動しているので、区別が意味を持つのは「GUI を前面に出して人が操作するか」の
一点だと考えてよい。

## 道具の選び方

「経路」は、Device Hub を前面に出して人が操作する必要があるかどうか。

| やりたいこと | 使うもの | 経路 | なぜ | 種別 | 見直す条件 |
|---|---|---|---|---|---|
| タップ（縦向き） | Claude のシミュレータパネル `mcp__Claude_Code_iOS_Simulator__control` の `tap` | 直接 | 確実に効く。手数が少ない | 正道 | — |
| タップ（横向き・確実さ優先） | `axe touch -x -y --down --up` | 直接 | パネルのタップが横向きで届かない。`axe tap` は効かない | **回避策** | axe が上がったら `tap` と横向きのパネルを再試験 |
| 要素の座標・ラベル | `axe describe-ui` | 直接 | 座標を取る唯一の手段。画像から目測するより正確 | 正道 | — |
| 撮影 | `xcrun simctl io <UDID> screenshot` | 直接 | パネルの `screenshot` が `captureFailed` を返す | **回避策** | パネル側が直ったら |
| 回転 | `xcrun devicectl device orientation set` | 直接 | `simctl` に回転が無い。Xcode 27 の正規の手段 | 正道 | — |
| 回転＋タップ＋階層をまとめて | Xcode MCP の `DeviceInteractionSynthesize` | 直接 | 1回でスクリーンショットと hitPoint 付き階層が返る | 正道 | — |
| 外観・文字サイズ・コントラスト | `xcrun simctl ui` | 直接 | 正規の手段 | 正道 | — |
| 画面の状態づくり | アプリの UserDefaults を直接書く | 直接 | UI 自動操作は取りこぼす。シートが開かない・別の項目に当たる | **回避策** | 入力系が安定したら |
| キー入力 | 人に押してもらう | **Device Hub** | どの経路も届かない（下記） | **回避策** | axe 更新時、iOS / Xcode 更新時 |
| 折りたたみ端末の開閉 | 人に開いてもらう | **Device Hub** | コマンドに対応が無い | **回避策** | `devicectl` にサブコマンドが増えたら |
| 折りたたみ端末の内側へのタップ | 人に押してもらう | **Device Hub** | どの経路も届かない | **回避策** | axe 更新時 |
| 可変ウインドウの幅 | 人に操作してもらう | **Device Hub** | `devicectl device appResize` が非対応で弾かれる | **回避策** | Resizable のデバイスタイプが入ったら再試験 |

## 使ってはいけないもの

### xcodebuildmcp の `tap` / `swipe` / `key_press`

**「成功」と返しても効かない。** 返り値を信用しない。中身は同梱の `axe` を呼んでいるだけで、
その axe が動いていないため。`snapshot_ui` / `describe-ui` が失敗するのも同じ根。

### 同梱の `bundled/axe`

`/usr/local/lib/node_modules/xcodebuildmcp/bundled/axe` は `describe-ui` が失敗する。
**Homebrew 版を使う。**

```bash
brew trust --formula cameroncooke/axe/axe && brew install axe
# → /opt/homebrew/bin/axe
```

版はどちらも 1.8.0 で同じ。brew 版だけ動くのは、`FBSimulatorControl` などのフレームワークを同梱し、
インストール時にローカルで codesign されるため。**版を上げれば直るという話ではない。**

`XCODEBUILDMCP_AXE_PATH` に brew 版を指すと xcodebuildmcp 側も差し替えられるが、
`axe tap` 自体が効かないので `tap` ツールは直らない。

### `axe tap`

効かない。`✓ Tap at (x, y) completed successfully` と返すが画面は変わらない。
**`axe touch -x <x> -y <y> --down --up` を使う。** こちらは縦向き・横向きとも届く。

## キー入力は届かない

`keyboardShortcut` や `onKeyPress` の動作確認は、**この環境では自動化できない。**

| 試したもの | 結果 |
|---|---|
| `axe key <keycode>` | 届かない |
| `axe type "<text>"` | 届かない |
| xcodebuildmcp `key_press` | 届かない（修飾キーも送れない） |
| Xcode MCP `sender keyboard kbd <text>` | 届かない |

入力欄にフォーカスを置いて1文字送っても入らないので、**アプリ側の実装の問題ではない。**
シミュレータの「Simulate Hardware Keyboard」が入っていても変わらない。

検証はユーザーに Device Hub 上で押してもらうか、実機にキーボードを繋いで行う。
**未確認のままコミットするなら、その旨をコミットメッセージに書く。**

## 座標の落とし穴

- **`describe-ui` は画面上の全アプリの階層を返す。** 裏のアプリの座標を拾って誤タップしやすい。
  目的のアプリに絞ってから読む
- **横向きではパネルのタップが届かない。** `axe touch` を使う
- **折りたたみ端末の内側ディスプレイには、どの経路のタップも届かない。** Device Hub 越しのクリックだけ。
  `describe-ui` は内側の座標空間で正しい値を返すのに、注入したタッチは届かない
- **再起動すると向きは縦に戻る。** ユーザーが回したあとに勝手に `shutdown` / `boot` をしない

## Device Hub を開くしかない操作

コマンドに対応が無いのは次の4つだけ。ほかは全部、直接叩ける経路がある。

- **キーボードの接続**（`Device > Keyboard`）**とキー入力**
- **折りたたみ端末の開閉**
- **可変ウインドウ**（`Enter Resize Mode`）。`devicectl device appResize` は
  `Resizable App Management` 非対応で弾かれ、名前に `Resizable` を含むディスプレイが要る。
  そのデバイスタイプが入っていない環境では使えない
- **折りたたみ端末の内側へのクリック**

いずれも人にやってもらうことになる。**画面まで自分で進めてから、押す操作だけを頼む。**
何度も往復させない。

**Device Hub を終了するとシミュレータも一緒に落ちる。** 作業中は終了させない。

## 確認の作法

- **返り値ではなく、撮って確かめる。** 成功と返して効いていない道具が複数ある
- **読み出した値を報告に書く。** 「確認しました」だけでは、その確認をした証拠にならない
- 座標は目測せず `describe-ui` の `frame` から取る。撮った画像から読むのは最後の手段
- 数値が説明できないときは、**一時的な計測コードを入れて実測する。** 推測で定数を置かない。
  `onGeometryChange` で `proxy.size` と `proxy.safeAreaInsets` をオーバーレイに出し、
  確認後に必ず外す

## よく使う組み立て

```bash
UDID=<simulator-udid>
AXE=/opt/homebrew/bin/axe

# 要素の座標を取る
$AXE describe-ui --udid $UDID

# 押す
$AXE touch -x 344 -y 255 --down --up --udid $UDID

# 撮る
xcrun simctl io $UDID screenshot out.png

# 回す
xcrun devicectl device orientation set --device $UDID landscapeLeft
xcrun devicectl device orientation get --device $UDID

# 状態を作る（UI を触らない）
xcrun simctl status_bar $UDID override --time 9:41 --cellularBars 4 --batteryState charging
xcrun simctl ui $UDID appearance dark
```

複数ディスプレイを持つ端末は `--display` で選ぶ。`xcrun simctl io <UDID> enumerate` で一覧が出る。
