---
description: ~ 配下の設定ファイルを dotfiles の管理下へ取り込む、または管理から外す。置き場の判定・秘匿値の切り出し・リンクの張り替えまで行う。ユーザーが「これも管理対象にして」「バックアップに含めて」「管理から外して」「/adopt-dotfile」等を指示したときに使う。
argument-hint: <~ からの相対パス> [public|private]
disable-model-invocation: true
allowed-tools: Bash(ls:*) Bash(find:*) Bash(du:*) Bash(readlink:*) Bash(grep:*) Bash(git check-ignore:*) Bash(git status:*) Bash(./scripts/adopt_dotfile.sh:*) Bash(mv:*) Bash(rm:*) Bash(ln:*)
---

置き場の定義と判断表は `docs/placement.md`。取り込みの実体は `scripts/adopt_dotfile.sh` が持つので、**手で `mv` + `ln` しない**。

## 進め方

1. **対象を確認する**: `ls -ld` で実体かリンクかを見る。既にリンクなら管理済みなので、その旨を伝えて終わる

2. **管理する価値があるかを判定する**

   | 判断 | 例 |
   | --- | --- |
   | **管理する** — 手で作り直すのが面倒で、再生成されない | 自作スクリプト、MCP 設定、エディタ設定、認証情報 |
   | **管理しない** — 再生成される / 巨大 / 揮発性 | パッケージキャッシュ、`node_modules` 相当、ログ、履歴 DB、ソケット |

   サイズも見る。数百 MB のディレクトリは、中の設定ファイルだけを個別に取り込む

3. **置き場を決める**: `docs/placement.md` の判断表に従う。**迷ったら private に倒す**

4. **秘匿値を切り出す**: 取り込む前に中身を走査し、実値があれば 1Password の Environment 「dotfiles」へ移して（アプリで足す）参照に置き換え、使うコマンドを `with-secrets` 経由にする。手順は `/audit-secrets`

5. **親ディレクトリが混在型なら `PARTIAL_DIRS` に足す**: `~/.claude` のように管理対象と管理外が同居するディレクトリは、丸ごとリンクすると管理外を巻き込む。`scripts/lib.sh` の `PARTIAL_DIRS` に親を追加してから取り込む

6. **取り込む**

   ```sh
   ./scripts/adopt_dotfile.sh private .codex/config.toml
   ```

7. **名前の衝突を確認する**: `home/` と `private/` に同名の要素があると、private が public を上書きする。`ls -A home private` で見る

8. **検証する**: `scripts/lib.sh` を変更したなら `/verify-restore`、公開側へ入れたなら `/audit-secrets` を走らせる

### 管理から外すとき

リンクを消し、リポジトリ側の実体を `~` へ戻す。`private/` から外した場合は、次回のバックアップから消えることを伝える。

## 出力の目安

判定の根拠（管理する理由・置き場を選んだ理由）を 1 行ずつ添え、取り込み後のリンクを**リンク元 → リンク先**で示す。秘匿値を切り出した場合は変数名だけを挙げる（値は出さない）。

## やってはいけないこと

- 中身を走査せずに公開側へ取り込むこと
- 巨大ディレクトリを丸ごと取り込むこと。zip が膨らみ、バックアップとリストアの所要時間に直結する
- `PARTIAL_DIRS` の確認を飛ばして混在型ディレクトリを丸ごとリンクすること
- 取り込んだ設定ファイルに「これは private です」等の**置き場の説明を書き足す**こと（`managed-file-purity.md`）
