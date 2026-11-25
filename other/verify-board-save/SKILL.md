---
name: verify-board-save
description: Kura のボードの自動保存（src/board/saveQueue.ts の push / retry / clear / flush と run のループ）が、編集を失わず、未保存の変更を「保存済み」と示さず、閉じる・切り替えるときに最後の変更を保存し終えることを、TLA+ のモデル検査（TLC）で確かめる。saveQueue.ts を変えたとき、BoardApp.tsx の保存のキューの使い方（commit、flush の呼び方、clear）を変えたとき、またはこの検査が DRIFT を出したときに使う。
---

# ボードの自動保存の検証（BoardSaveQueue）

## 何を確かめているか

**約束：** ボードの編集は失われない。未保存の変更を「保存済み」と示さない（FR-704）。閉じる・切り替えるときは、最後の変更を保存し終えてから進む。

**破れたときの害：** 利用者が「保存済み」を見てボードを閉じたのに、最後の配置が保存されていない。または、保存できないのに理由を示さずに切り替えを断る。

単体テスト（`saveQueue.test.ts`）は、決まった順番だけを試す。このモデルは、JavaScript が切り替わりうるすべての所（`await` の前後、`run()` の終わりと `.finally()` の間）で、編集、再試行、ボードの削除、閉じる操作、保存の成功と失敗の、すべての順番を試す。

| 性質（`BoardSaveQueue.tla`） | 平易な言い方 |
| --- | --- |
| `OneInFlight` | 同時に送る保存は1つまで。2つ送ると、後の保存は同じ revision で断られる |
| `NoLostEdit` | 最後の変更は、保存済みか、待っているか、送っている途中のどれか（ボードを削除したときを除く） |
| `SavedMeansSaved` | 「保存済み」と示すのは、最後の変更を保存し終えたときだけ |
| `FlushMeansSaved` | `flush()` が成功で返ったときは、最後の変更を保存し終えている |
| `EventuallySaved` | 編集と失敗が止めば、最後の変更が保存され、「保存済み」と示す |

## 見つけて直した不具合（2026-11-19）

最初の検査で、3つの性質が破れた。原因は同じで、`run()` が終わってから `.finally()` が `running` を null にするまでに、別の処理が1つ入れたため。

- `SavedMeansSaved`：保存が成功した直後に編集すると、`kick()` は `running` が残っているので送らない。画面は「保存済み」のまま
- `FlushMeansSaved`：閉じる操作が待ち終えた直後に編集すると、新しい `run()` が `pending` を持っていく。`flush()` は `pending` が空と見て、保存し終える前に返る
- `EventuallySaved`：1つ目の後、再試行のボタンが出ず、次の編集まで送られない。間に `flush()` が入ると `null` で reject する

3つとも実際のコードで再現した。直し方は次の2つ。
- `run()` が終わると決めたのと同じ塊で `running` を null にする
- `flush()` は、`running` も `pending` もなくなるまで待つ

`saveQueue.test.ts` の「保存が終わった直後」と「flush を待つ間に来た変更」のテストが、元のコードで落ちて、直したコードで通る。壊した版の `lateRunningReset` は、元のコードの `.finally()` を写したもの。

## 実行

リポジトリのルートで：
```bash
.claude/skills/verify-board-save/check.sh
```
数秒で終わる。TLC の jar の準備は `verify-crash-safe-move` の SKILL.md の「準備」と同じ。出力の読み方：
- `ok     covered code matches coverage.tsv`：`saveQueue.ts` は、最後に確かめたときから変わっていない
- `PASS   MC.cfg`：今のコードのモデルで、5つの性質がすべて成り立つ
- `ok     <mutant>.cfg fails <性質> as expected`：わざと壊した版で、その性質が落ちる（検査が落ちうることの確認）

TLC の出力は `.claude/tmp/tla/out/board-save/<cfg 名>.txt` に残る。部分だけ流すときは `check.sh model`、`check.sh drift`。

## DRIFT や FAIL が出たとき

`DRIFT` は、`saveQueue.ts` の空白を詰めた中身が `coverage.tsv` の指紋と違うことを示す。

**同期したコミット：`1ffa469`**（`cc8cf25` から、`saveQueue.ts` は変わっていない。BoardApp に、キューを通らずにボードを書き換える道が2つ増えた。一覧からのドロップ（`dropImages`。FR-713）は `queue.flush()` を待ってから `drop_on_board` を呼び、まとめの置き換え（`board-replaced`。FR-610）は Rust が `windows::settle` で保存を待ってから配置を置き換える。どちらも間の編集を `revealing` か `held` で止める。キューの使い方は `flush()` の呼び出しが1つ増えただけなので、モデルは変えず、TLC と6つの故障モデルで確かめた。その前の同期は `cc8cf25`）

1. `git diff <同期したコミット> -- src/board/saveQueue.ts src/board/BoardApp.tsx` で、変わった所を読む。
2. 下の「モデルとコードの対応」のどの行が変わったかを見る。対応する行がなければ、モデルは変えない。手順が変わったら（`await` の位置、`running` を null にする所、`pending` の扱い、`flush()` の判定）、`BoardSaveQueue.tla` のアクションをコードと同じに直す。
3. `FAIL` なら、TLC の出力を `/pstack:statechart` で読み、反例を手順に直す。反例の各段階がコードの1つの塊（`await` と `await` の間）に当たるなら本物の不具合。性質を緩めて通さない。コードではありえない段階があれば、モデルの誤り。
4. 本物の不具合なら、反例をテストか小さなスクリプトで実際のコードに流して確かめる。マイクロタスクの順番が要る反例は、`Promise.resolve().then()` を何段か重ねた後に操作を入れて試す。
5. モデルを直したら `check.sh` で壊した版がまだ落ちることを確かめ、`check.sh rehash` の結果をコミットする。図も描き直す。

## モデルとコードの対応

| モデル | コード |
| --- | --- |
| `Push` | `push()`：`pending` を置き換えて `kick()`。BoardApp の `commit()` から呼ぶ |
| `Kick` | `kick()`：`running` があれば何もしない。`pending` がなければ `saved` を示す。あれば `running = run()`。`run()` は最初の `await` まで同じ塊で進み、`pending` を取って `send()` を呼ぶ |
| `SendOk` | `await send(snapshot)` が成功し、`while (pending)` が次を取るか、`running = null` にして `saved` を示す |
| `SendFail` | `send()` が throw し、`pending ??= { snapshot }`、`running = null` にして `failed` を示す |
| `End` | `run()` の終わり。`running` を同じ塊で null にし、待っていた `flush()` が続けられるようになる |
| `Finally` | 壊した版の `lateRunningReset` だけ。元のコードの `.finally(() => (running = null))` |
| `Retry` | `retry()`。画面の再試行のボタンは `failed` のときだけ出る |
| `Clear` | `clear()`。ボードを削除したとき |
| `FlushStart`、`FlushResume` | `flush()`：`while (running \|\| pending)` の間、`running` か `kick()` を待つ。待ち終えて `pending && !running` なら throw |

## 範囲と前提

- 検証の範囲：編集3回、保存の失敗2回まで（約1,000状態）。図は編集2回、失敗1回（約200状態）。
- `send()` の中（`invoke('save_board')` と revision の更新）は1つの塊とみなす。サーバーは受け取った版を保存する。
- 同じ回の中のマイクロタスクの順番は区別せず、`await` の間ならどこでも別の操作が入りうるとしている。
- BoardApp の `held` と `revealing`（閉じる間や、ドロップ・置き換えの間の編集の受け付けを止める）は入れていない。`drop_on_board` と `board-replaced` は、キューを通らずにボードを書き換える。これらとキューの保存が重ならないことは、`held` と `revealing` に頼っていて、このモデルでは確かめていない。表示の保存（`displayQueue`）も同じ `saveQueue` を使うが、モデルは配置の保存の使い方だけを見ている。

## ファイル

| ファイル | 内容 |
| --- | --- |
| `BoardSaveQueue.tla` | モデル。`Mutation` 定数で壊した版を選ぶ |
| `MC.cfg` | 今のコード（`Mutation = "none"`）。5つの性質をすべて検査する |
| `mutants/*.cfg` | 壊した版。1行目の `Expect <性質>` が、落ちるべき性質 |
| `coverage.tsv` | モデルが写すファイルと、同期したコミットでの指紋 |
| `check.sh` | 実行 |
| `statechart/chart.mmd` | 状態遷移図（Mermaid） |
| `statechart/view.ts`、`statechart/chart.cfg` | 図の言葉と、図を描く範囲 |

### 図を描き直す

```bash
<statechart スキルのフォルダ>/scripts/statechart .claude/skills/verify-board-save/BoardSaveQueue.tla --config .claude/skills/verify-board-save/statechart/chart.cfg --view .claude/skills/verify-board-save/statechart/view.ts --out .claude/tmp/statechart/board && cp .claude/tmp/statechart/board/chart.mmd .claude/skills/verify-board-save/statechart/
```
