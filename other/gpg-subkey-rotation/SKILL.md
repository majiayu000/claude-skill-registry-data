---
name: gpg-subkey-rotation
description: GPG の機体ローカル [S]/[E] サブ鍵をローテーションするときの、抜け漏れなく完了させる手順(ADR-0003)。GPG 鍵ローテーション・署名鍵ローテーション・gpg-subkey rotate・signing key expiring・鍵の有効期限が近い・commit 署名が unknown_key・Commits must have verified signatures、といった文脈で使う。rotate GPG signing subkey, GitHub GPG key out of sync, verified signatures failing、といった英語の文脈でも使う。
---

`gpg-subkey`(`~/.local/bin/gpg-subkey`)は機体ローカルの `[S]`(署名)/`[E]`
(暗号化)サブ鍵をローテーションする CLI だが、`rotate` を実行しただけでは
何も完了しない。ローテーションは 8 ステップの一連の手続きで、途中の
どれか 1 つでも飛ばすと「鍵は新しくなったが宣言・登録先はどれも古いまま」
という壊れた中間状態で止まる。

**実例(このスキルが生まれた失敗)**: ある機体で `[S]` サブ鍵の `rotate` を
実行した後、export・nix 編集・GitHub/keyserver 同期・PR・`hms` 適用のどれも
行わずにセッションが終わった。数日後、別の作業で作った commit の GitHub
チェックが `Commits must have verified signatures` で失敗して初めて発覚した
— `gpg-subkey sync` の drift レポートを見るまで、何が未完了なのか誰も把握
していなかった。

## 1. 全体像(この 8 つが揃うまで「ローテーションした」と言わない)

1. **rotate**(ハードウェア操作、必ずユーザー): `gpg-subkey rotate --key
   <primary-fpr> [--usage sign|encrypt] --revoke-old`
   カードの `[C]` 権限で新サブ鍵に署名するため YubiKey の挿入・タッチ・PIN
   入力が要る。LLM エージェントは代行できない(資格情報/ハードウェア操作の
   ブロッキング理由)。`--revoke-old` を付けても **カード紐付けの旧サブ鍵は
   revoke されない**(on-disk 材料だけが revoke 対象 — CLI ヘルプに明記。
   これは意図的な設計であり次ステップの対象ではない)。
2. **revoke 単独実行**(旧鍵が残っている場合のみ、ハードウェア操作):
   `--revoke-old` を付け忘れた・rotate が途中失敗した等で on-disk の旧
   `[S]`/`[E]` サブ鍵が revoke されずに残っていたら、`gpg-subkey status` で
   その keyid を確認し `gpg-subkey revoke --key <primary-fpr> --subkey
   <keyid>` を実行する。新しい鍵を作らずにこの 1 本だけを revoke する
   standalone コマンド(rotate の `--revoke-old` とは別の入口)。これも
   カードの `[C]` 権限が要るためユーザー実行必須。card-backed/stub な
   subkey は(ステップ 1 と同じ理由で)拒否される。
3. **export**: `gpg-subkey export --repo <dotfiles-checkout> --identity
   <personal|company>`
   `keys/<identity>.pub` をローカル鍵束から再エクスポートし、次に nix へ
   書く新サブ鍵 ID を出力する。変更が無ければ「変更はありません」と出る
   (べき等)。ステップ 2 で revoke しただけでも鍵材料が変わるため、
   ここは rotate 後だけでなく revoke 後にも必ず再実行する。
4. **nix 編集**: `home/hosts/<host>.nix` の `programs.git.signing.key` を
   新サブ鍵の**フルフィンガープリント**(short ID ではない)で更新する。
   併せてコメントの生成日・失効日・旧サブ鍵 ID も書き換える(この
   ファイルは宣言的な正本 — 実際に signing key として何が使われているかを
   知る唯一の場所)。
5. **sync**: `gpg-subkey sync --repo <dotfiles-checkout> --identity
   <personal|company>`(report)→ drift があれば `--fix --yes`(非対話実行
   では `--yes` 必須、無いとエラーで止まる)。GitHub の GPG 鍵登録・
   keys.openpgp.org を現行サブ鍵に収束させる。GitHub は登録の in-place
   更新をサポートしないため、`--fix` は古いエントリを削除して現行の
   export を登録し直す。ステップ 2 で revoke した場合、その revoke で
   鍵材料が変わった分の drift がここで再度出る(export し直しただけでは
   GitHub/keyserver 側は古いまま) — `sync` が exit 0(drift ゼロ)を
   報告するまでステップ 3〜5 を繰り返す。
6. **`[E]` をローテーションした場合のみ**: そのサブ鍵が暗号化している
   ファイルを再暗号化する(CLI ヘルプ曰く「例: esa MCP の
   `token.gpg`」)。対象が無ければスキップしてよいが、確認はする。
7. **commit → PR**: `keys/<identity>.pub`(変更があれば)+ host module を
   1 コミットにまとめて PR にする。ADR-0027 により、同一セッション内に
   dotfiles の他の open PR があれば、その head branch を base にして積む
   (base の PR が既にマージ・ブランチ削除済みなら `git fetch origin main`
   → `git rebase origin/main` → base を `main` に変更するのが定石)。
8. **適用**: PR マージ後 `hms .`(または `hms`)でこのホストに適用する。
   適用を忘れると、宣言(nix)と実体(実際に使われる signing key)が
   再び乖離する — ステップ 4 だけ終えてステップ 8 を飛ばした状態は、
   何もしていない状態より発見しにくい(diff が既にマージされて「完了した
   ように見える」ため)。

## 2. 完了条件

次の 4 つが揃うまで完成と呼ばない:

- `gpg-subkey sync --repo <dotfiles-checkout> --identity <identity>` が
  drift ゼロを報告する(出力なし・exit 0)
- `gpg-subkey status` で対象 identity・対象 usage の revoke されていない
  サブ鍵が現行の 1 本だけになっている(ローテーションで旧鍵が残ったまま
  なのに気づかず終わった、が本スキルの起票理由そのもの)
- `home/hosts/<host>.nix` の `programs.git.signing.key` が、`gpg-subkey
  status` が示す現行 `[S]` サブ鍵のフルフィンガープリントと一致する
- 直近のコミットが対象リポジトリで `verified: true` になっている
  (`gh api repos/<owner>/<repo>/commits/<sha> --jq '.commit.verification'`)

## 3. 「ローテーション進行中」の見分け方

`gpg-subkey status` で同一 identity に **revoke されていない `[S]`(または
`[E]`)サブ鍵が 2 つ以上**並んでいたら、rotate 済み・後続ステップ未完了の
サインである。その状態を見つけたらステップ 2(revoke 単独実行)から再開
する — 新しい鍵をもう一度作る必要はない。同様に `gpg-subkey sync`(引数
なしで drift レポートのみ)が何か出力したら、そこがどのステップで止まって
いるかの手がかりになる — 出力の文言(「GitHub の登録が反映していない」
「nix の signing.key が異なる」等)がそのまま次にやるべきステップを指す。

## 4. 既知の落とし穴

- `sync --fix` は非対話実行(スクリプト・hook 経由)では `--yes` が無いと
  `非対話実行では --yes が必要です` で失敗する。
- `rotate --revoke-old` はカード紐付けサブ鍵を revoke しない。on-disk 材料
  だけが対象 — 「rotate に revoke-old を付けたのに旧鍵がまだ生きている」は
  バグではなく仕様(card-backed の残置は ADR-0003 Amendment 4 の意図)。
  一方、on-disk の旧鍵が revoke されずに残ったままなのは仕様ではなくバグ
  なので、ステップ 2 の `revoke` で収束させる。
- `gpg-subkey revoke` も同じく on-disk 限定。card-backed/stub な subkey を
  指定すると「revoke 対象外」と明示的に拒否される(黙って何もしない、では
  ない)。
- revoke(rotate 経由・standalone 経由どちらも)の直後は `sync` が
  もう一度 drift を報告する。鍵材料が変わった分、GitHub/keyserver 側の
  コピーが古くなるため — ステップ 3〜5 を revoke のたびに繰り返す。
- `keys/<identity>.pub` の再 export は必ずしも差分を生まない(既に最新の
  ことがある)。「変更なし」を「失敗」と誤読しない。
- stacked-pr 運用中、base にした PR が既にマージ済みでブランチが削除されて
  いると `gh pr create --base <branch>` が失敗する(1節ステップ 7 参照)。
