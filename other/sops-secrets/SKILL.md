---
name: sops-secrets
description: sops / age による secret の暗号化・復号・追加・再暗号化の運用手順。secret を暗号化する・inject する・`secrets/` 配下を触る・`.sops.yaml` や `devices/secrets.nix` を変更する・新デバイスの鍵を登録するとき、および sops 関連エラー（cannot parse dotenv / unexpected end of JSON input 等）の対処時に必ず使用する。
allowed-tools: Bash(python3 ~/.claude/skills/sops-secrets/scripts/inject.py *)
---

# sops-secrets

フリートの secret 運用。`secrets/` 配下はすべて sops（age 鍵）で暗号化してコミットし、`inject` コマンドで暗号化・配置を一括処理する。`devices/secrets.nix` がディレクトリを自動スキャンして全 secret を登録する。

**Agent が実行するときの注意**: Claude Code の Bash ツールは zsh の関数を読み込まないシェルで動くため、Agent は常に実体である `python3 ~/.claude/skills/sops-secrets/scripts/inject.py <file> <category>` を直接呼ぶこと（下記コマンド例もすべてこの形にしてある）。

## 安全規則

- 平文の secret をリポ内・ディスクバックの領域に置かない。生ファイルは RAM ディスク上でのみ作成する
- `secrets/` の読み取り・編集・作成は原則 Agent に許可しない。**例外**: JSON 形式（`secrets/**/*.json.age`）のみ Read/Edit/Write を許可する運用にする。これらは常に sops による暗号文（ciphertext）であり、平文が直接見えるわけではない。Edit/Write の直前に `.claude/hooks/backup-secret-json.sh`（PreToolUse, matcher `Edit|Write`）が自動でタイムスタンプ付きバックアップ（`*.json.age.bak.<timestamp>`）を残すため、誤編集時はそこから復元できる
  - 上記以外の format（`binary` / `dotenv`、ファイル名が `.json.age` で終わらないもの）は引き続き deny のまま。既存カテゴリを Agent に直接触らせたい場合は、新カテゴリを JSON format（`inject` 時に拡張子 `.json` の生ファイルを渡す）で作る
  - 復号値そのもの（`sops --decrypt` の出力）を確認する必要があるときは、値を表示せずコマンドに直接食わせるか user に依頼する（この規則は format に関わらず変わらない）
- Issue / PR / コミット等の説明文に実値を書かない。`~/dotfiles/secrets-agents/` の辞書を読み `<PLACEHOLDER>` を使う（グローバル CLAUDE.md の機密マスク規則）

## secret を追加する（通常運用）

```bash
# 1. RAMディスク上で生ファイルを作成・編集
#    Linux:
hx /dev/shm/filename.env
#    macOS（/dev/shm が無いので RAM ディスクを作る。詳細は references/macos.md）:
RAMDISK=$(hdiutil attach -nomount ram://65536 | tr -d ' ')
newfs_hfs -v ramdisk "$RAMDISK" && mkdir -p /Volumes/ramdisk
mount -t hfs "$RAMDISK" /Volumes/ramdisk
hx /Volumes/ramdisk/filename.env

# 2. 暗号化してdotfilesに配置（.age 拡張子が自動で付く。format は拡張子で決まる: .env → dotenv、.json → json、その他 → binary）
# Agent は実体を直接呼ぶ（上記「Agentが実行するときの注意」）
python3 ~/.claude/skills/sops-secrets/scripts/inject.py <生ファイルパス> <カテゴリ名>
# → secrets/<カテゴリ名>/filename.env.age が生成される

# 3. 生成確認（.age が存在すること。macOS は RAM ディスクを解放:
#    umount /Volumes/ramdisk && hdiutil detach "$RAMDISK"）
ls ~/dotfiles/secrets/<カテゴリ名>/

# 4. コミット
cd ~/dotfiles && git add -A && git commit -m "..."
# 5. 各デバイスで pull → rebuild すると新しい secret が復号される
#    （nixos-rebuild / darwin-rebuild / home-manager switch は user が実施。Agentは実行しない）
```

## secret をローテーション・他システムと同期する（GitHub webhook secret 等）

**Agentは`sops --decrypt`で既存secretを読み出そうとしてはいけない**。`secrets/`の復号はJSON/binary/dotenv問わずAgentには許可されておらず（`inject`による新規書き込みだけが許可されている）、分類器に必ずブロックされる。値が必要になった時点で詰むので、**最初から復号が絶対に要らない順序**で進めること。

**この順序は「念のため」ではなく必須**: `inject.py`は暗号化に成功すると`src.unlink()`で元の平文ファイルを自分で削除する（`scripts/inject.py`）。つまり`inject`を先に実行した時点で、その回に使った平文はAgentの手元から完全に消え、後から取り戻す唯一の手段（`sops --decrypt`）はAgentには許可されていない。だから同期先への配布は必ずinjectより前に終わらせる。

1. RAMディスク上で新しい値を生成する（既存値を読みに行かない。値ごと作り直す）
2. **平文がまだ自分の手元にある間に**、同期先すべてに反映する（例: `gh api -X PATCH .../hooks/{id} -f config[secret]=@<RAMディスク上のファイル>` でGitHub webhook secretを更新）。`-f config[secret]=<値>`のように値をコマンド文字列に直接埋め込まず、`@<ファイルパス>`でファイル参照にすること（値がBashコマンドの引数として露出すると、それ自体が別途分類器にブロックされ得る）
3. 全ての同期先への反映が完了してから、最後に `python3 ~/.claude/skills/sops-secrets/scripts/inject.py <RAMディスク上のファイル> <カテゴリ名>` で暗号化してdotfilesに配置する（成功時に元ファイルは自動で消える。手動削除は不要）
4. `inject`が何らかの理由で失敗した場合は、RAMディスク上のファイルはまだ残っているので再実行できる。失敗を`sops --decrypt`で復旧しようとしない

途中で失敗して`sops --decrypt`に頼りたくなった場合は、そこで止めて user に値の受け渡しを依頼する（回避しようとしない）。

## カテゴリと format

| カテゴリ | format |
|---|---|
| `legacyBinaryCategories`（`devices/secrets.nix`）に列挙したカテゴリ | binary 固定（拡張子による自動判定を使わない） |
| それ以外の全カテゴリ | 拡張子で自動判定: `.env`→dotenv, `.json`→json, その他→binary |

- 新カテゴリは `devices/secrets.nix` の変更不要。`inject` で入れるだけで自動登録される
- JSON/YAML を「ファイル全体」で配置したい場合は json 自動判定（キー抽出）を避ける。カテゴリを `legacyBinaryCategories` に追加し、`sops -e --input-type binary --output-type binary -i <ファイル>` で暗号化する

## 復号確認

```bash
# dotenv 形式
sops --decrypt --input-type dotenv --output-type dotenv secrets/<カテゴリ>/<ファイル名>.env.age

# binary 形式（legacyBinaryCategories 所属カテゴリ）
sops --decrypt --output-type binary secrets/<カテゴリ>/<ファイル名>.age
```

## 新デバイス追加・トラブルシューティング

順序を誤ると SOPS デッドロック（鍵未登録 → 復号失敗 → Home Manager 破損 → TTY 送り）になる。**鍵登録 → 既存 secret 再暗号化 → ビルド**の順を厳守する。再暗号化は format ごとに2回に分ける（dotenv は `.age` 拡張子から JSON と誤判定されるため `--input-type dotenv` が要る。1本の `find` で済ませると dotenv 分だけ黙って失敗し、その1ファイルが原因で `sops-install-secrets` が全体を中断する）。

手順の詳細とエラー別対処は作業マシンの OS で選ぶ:

- Linux（linux-desktop 等から）: [references/linux.md](references/linux.md)
- macOS（macbook から）: [references/macos.md](references/macos.md)

Home Manager から secret を参照するときは `/run/secrets/...` を文字列で直書きせず、`config.lib.file.mkOutOfStoreSymlink` + `osConfig.sops.secrets."<KEY>".path` を使う。
