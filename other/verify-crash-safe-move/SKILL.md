---
name: verify-crash-safe-move
description: Kura のファイルを動かす手順（src-tauri/src/fileops.rs の transfer / settle / recover と、library.rs の connect / apply_op）が、どこでプロセスが落ちても画像を失わず、DB と実ファイルを食い違わせないことを、TLA+ のモデル検査（TLC）で確かめる。fileops.rs、library.rs の connect と apply_op、pending_ops の扱い、画像やカテゴリを動かす操作（移動、名前変更、ゴミ箱、取り込みのコピー）の手順を変えたとき、またはこの検査が DRIFT を出したときに使う。
---

# 移動の手順の検証（CrashSafeMove）

## 何を確かめているか

**約束：** ファイルを動かす操作の途中でアプリが落ちても、画像は失われず、起動時の後始末のあとは DB と実ファイルが一致する（NFR-06。`CLAUDE.md` の「予定を `pending_ops` に記録 → 上書きしない rename → DB 更新」）。

**破れたときの害：** 利用者の参考画像が消える、または一覧が存在しないファイルを指し、実ファイルが一覧から見えなくなる。

テストは決まった止め方（`fileops.rs` の `予定の記録の後で止まったら…` など）だけを試す。このモデルは、1つの操作について、あらゆる段階での停止（後始末の途中で再び落ちる場合も含む）、rename やコピーの失敗、DB の更新の失敗の、すべての順番を試す。

| 性質（`CrashSafeMove.tla`） | 平易な言い方 |
| --- | --- |
| `NoLoss` | 移動では、画像のファイルはいつも src、一時ファイル、dst のどれか1か所にだけ、欠けずにある。コピーでは元を変えない |
| `NoPartialAtDst` | 移動先の名前に、書きかけのファイルが置かれることはない |
| `SettledConsistent` | `pending_ops` に行がないときは、一時ファイルが残っておらず、DB が指す場所に画像がある |
| `NeverUndecided` | ほかに誰もファイルを触らなければ、後始末は必ず「完了」か「取り消し」を決められる |
| `EventuallySettled` | 落ちることと失敗が止めば、操作は `pending_ops` の行を残さずに終わる |

## 実行

リポジトリのルートで：
```bash
.claude/skills/verify-crash-safe-move/check.sh
```
約5秒。出力の読み方：
- `ok     covered code matches coverage.tsv`：モデルが写しているコードは、最後に確かめたときから変わっていない
- `PASS   MC.cfg`：今のコードのモデルで、5つの性質がすべて成り立つ
- `ok     <mutant>.cfg fails <性質> as expected`：わざと壊した版で、その性質が落ちる（検査が落ちうることの確認）
- 終了コードは、すべて通れば 0

TLC の出力は `.claude/tmp/tla/out/<cfg 名>.txt` に残る。部分だけ流すときは `check.sh model`（今のモデルだけ）、`check.sh drift`（ずれの確認だけ）。

### 準備（初回だけ）

Java（`java -version` が 11 以上）と TLC 1.7.4 が要る。TLC は次の場所に置く（git の対象外）。`check.sh` が sha256 を確かめる。
```bash
mkdir -p .claude/tmp/tla && curl -fsSL -o .claude/tmp/tla/tla2tools-1.7.4.jar https://github.com/tlaplus/tlaplus/releases/download/v1.7.4/tla2tools.jar
```
別の場所の jar を使うときは `TLA2TOOLS=<パス>` を付けて流す。

## 変更がここに関わるか

関わるのは次のどれか：
- `coverage.tsv` に並んだ関数（`fileops.rs` の `rename_excl`、`present`、`transfer`、`record`、`tmp_path`、`finish`、`drop_op`、`settle`、`recover`、`library.rs` の `connect`、`apply_op`）を変えた
- `transfer` を呼ぶ操作を足した、または `Request.copy` の使い方を変えた（`import.rs`、`category.rs`、`trash.rs`）
- `pending_ops` を、`fileops.rs` の外で書くようにした

`check.sh` の `DRIFT` は、上の関数の本体（空白を詰めたもの）が `coverage.tsv` の指紋と違うことを示す。整形だけの変更でも出る。

**同期したコミット：`1ffa469`**（`28c0622` から、移動の手順に関わるファイル（`fileops.rs`、`library.rs`、`import.rs`、`category.rs`、`trash.rs`、`skipped.rs`、`merge.rs`）は変わっていない。増えたコード（`origin.rs`、`similar.rs`、`calc.rs` など。FR-606、FR-608、FR-610、FR-611）は `transfer` も `pending_ops` も使わない。モデルは変えず、TLC と6つの故障モデルで確かめた。その前の同期は `28c0622`：`002d834` から、`library.rs` の `apply_op` に、DB に行のないファイルを動かす2つの種類（`skipped.rs` の `SET_ASIDE` と `TRASH_DUPLICATE`。FR-108、FR-109）を足した。どちらも DB を変えない `apply_none` で、`transfer` の移動（`copy: false`、`OnConflict::Number`）をそのまま使う。段階の順番もトランザクションの区切りも変わらないので、モデルは変更せず、TLC と6つの故障モデルで確かめた。前の同期は `002d834`）

## DRIFT や FAIL が出たとき

1. `git diff <上の同期したコミット> -- src-tauri/src/fileops.rs src-tauri/src/library.rs` で、変わった関数を読む。
2. 変わったのが、下の「モデルとコードの対応」の行のどれかを見る。
   - 対応する行がない（ログの文言、エラーメッセージ、整形）なら、モデルは変えない。`check.sh` を流して `PASS` を確かめ、`check.sh rehash` で指紋を書き直し、上の同期したコミットを今の `HEAD` にする。
   - 手順が変わった（段階の順番、1つのトランザクションに入れるもの、settle の判定）なら、`CrashSafeMove.tla` の該当するアクションを、コードと同じに直してから `check.sh` を流す。
3. `PASS` でなければ、まず TLC の出力（`.claude/tmp/tla/out/MC.txt`）を **`/pstack:statechart`** で読み、反例を「どの段階で落ち、何が残ったか」の手順に直す。
4. 本物の不具合か、モデルの誤りかを分ける：
   - 反例の各段階が、下の対応表でコードの1文に当たり、その順番がコードで実際に起こりうるなら、**本物の不具合**。性質やモデルを緩めて通さない。反例をコードの言葉で利用者に報告する。製品のコードは、頼まれたときだけ直す。
   - 反例に、コードではありえない段階がある（コードでは1つのトランザクションなのに、モデルでは2つに分かれている、など）なら、**モデルの誤り**。モデルをコードに合わせて直す。
5. モデルを直したら、`mutants/` の壊した版がまだそれぞれ落ちることも `check.sh` で確かめる。新しい段階を足したら、それを壊した版を `mutants/` に1つ足す（ファイルの1行目に `Expect <性質>` を書く）。
6. 確かめ終えたら `check.sh rehash` と、同期したコミットの更新。コードを読んでモデルとの対応を確かめる前に、同期したコミットを進めない。

通ったときに状態の移り方を見たいときも `/pstack:statechart` を使う。

## モデルとコードの対応

| モデル（`CrashSafeMove.tla`） | コード |
| --- | --- |
| `mode = "move"` / `"caseOnly"` / `"copy"` | `transfer` の分岐：`rename_excl(&src_abs, &dst_abs)` / `case_only` / `req.copy` |
| `Locs` の `tmp` | `tmp_path(op)`（移動先のフォルダの `.kura-tmp-<id>`） |
| `Record` | `transfer` の `record(...)`。`INSERT INTO pending_ops` は単独でコミットされる |
| `RenameSrcDst`、`RenameSrcTmp`、`RenameTmpDst` | `rename_excl`（`renamex_np` の `RENAME_EXCL`。1回の rename を1段階とみなす） |
| `CopyBegin` → `CopyEnd` | `fs::copy(&src_abs, &tmp)`。途中で落ちると書きかけが残る |
| `OpFails` | rename かコピーが `Err` を返す → `transfer` が `settle` を呼ぶ |
| `Finish`、`FinishCommit` | `finish`：`apply` と `drop_op` を1つのトランザクションでコミット。失敗すると `settle` |
| `ApplyDb` | `apply_move` などは行を `op.dst` に向ける。`import` は `transfer` のクロージャでは行を作り、`library::apply_op` では何もしない（FR-104 が後で登録する） |
| `Settle` | `settle`：一時ファイルがあれば戻す（コピーなら消す）、なければ `(at_src, at_dst)` で完了・取り消し・保留を決める。`present` は書きかけも「ある」と数える |
| `SettleDrop` | `settle` の一時ファイルの処理の後の `drop_op`（別の文） |
| `Recover` | `library::connect` → `fileops::recover` |
| `Reopen` | 決められなかった操作が残ったまま、利用者がライブラリを開き直す |
| `Crash` | プロセスの停止。ファイル、`pending_ops`、`images` だけが残る |

## 範囲と前提

検証済み：1つの操作について、3つの分岐（移動、大文字・小文字だけの名前変更、コピー）のすべての順番。範囲は、落ちる回数3回まで、DB の更新の失敗2回まで、rename かコピーの失敗1回まで（約370状態）。

前提（モデルに入れていないこと）：
- 落ちるのはプロセスだけ。電源断は入れていない。rename はディレクトリを fsync しないので、電源断で rename が消え、SQLite のコミット（`synchronous = FULL`）だけが残る場合は検証していない。
- 操作中に Finder など外から同じファイルを触る場合は入れていない。exFAT の「確かめてから rename」の隙（`rename_excl` の `shortcut:`）もこの外。
- 同時に1つの操作だけ。決められずに残った操作の上に、同じ画像の別の操作が重なる場合は入れていない。
- `rename_excl(tmp → src)` など、後始末の中の rename の失敗は入れていない。
- `apply_*` の中身（どの列をどう変えるか）は、「行が dst を指す」に縮めている。カテゴリのフォルダの移動（`MOVE_CATEGORY`）では、フォルダの中の画像の行の書き換えを見ていない。

## ファイル

| ファイル | 内容 |
| --- | --- |
| `CrashSafeMove.tla` | モデル。`Mutation` 定数で壊した版を選ぶ |
| `MC.cfg` | 今のコード（`Mutation = "none"`）。5つの性質をすべて検査する |
| `mutants/*.cfg` | 壊した版。1行目の `Expect <性質>` が、落ちるべき性質 |
| `coverage.tsv` | モデルが写す関数と、同期したコミットでの指紋 |
| `check.sh` | 実行 |
| `fingerprint.py` | 関数の本体の指紋。コメントと文字列の中の波括弧を数えない。`check.sh` が自己テストを流す |
| `statechart/chart.mmd` | 今のモデルの状態遷移図（Mermaid）。`/pstack:statechart` で描いた |
| `statechart/view.ts`、`statechart/chart.cfg` | 図の言葉と、図を描く範囲（落ちる回数1回、失敗1回ずつ。約100状態） |

### 図を描き直す

モデルを直したら、図も描き直す。作業用のフォルダで、完了で止まる手順 `Done` を足したモデルの写しを作ってから、`/pstack:statechart` のスクリプトに渡す（`check.sh` の検査には `Done` を入れない）。
```bash
W=.claude/tmp/statechart && D=.claude/skills/verify-crash-safe-move && mkdir -p $W
sed 's/^Next == Progress \\\/ Crash$/Done == pc = "done" \/\\ UNCHANGED vars\nNext == Progress \\\/ Crash \\\/ Done/' $D/CrashSafeMove.tla > $W/CrashSafeMove.tla
<statechart スキルのフォルダ>/scripts/statechart $W/CrashSafeMove.tla --config $D/statechart/chart.cfg --view $D/statechart/view.ts --out $W/out && cp $W/out/chart.mmd $D/statechart/chart.mmd
```
