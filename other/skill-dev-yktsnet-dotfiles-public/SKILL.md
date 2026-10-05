---
name: skill-dev
description: 新しい Claude Code skill を作る・追加する・整備したくなったときの配置ルール。「スキルを作って」「これをスキルにして」「skillを追加したい」等、SKILL.md を新規に書こうとする前に必ず使用する。どこに置くか（dotfiles管理のグローバル vs リポ固有）を先に決める。
---

# skill-dev

SKILL.md を書き始める前に、それが skill であるべきか、どこに置くかを決める。

## 1. skill にするか

知識の置き場は、読み込みの契機で決める。

| 契機 | 置き場 |
|---|---|
| 毎回効く短い規則 | CLAUDE.md に1行 |
| 「〜するとき」と条件を言える手順・規範 | skill（description が起動条件の宣言になる） |
| 判断の基準・ガイド | それを使う skill が持つ。1本の skill しか読まないなら `SKILL.md` 本体、複数の skill が読むか長いなら `reference/`。独立した MD に切り出さない |
| 規則から指す共有辞書 | 独立ディレクトリに置き、CLAUDE.md / skill から絶対パスで参照（例: `secrets-agents/`） |
| コードの非自明な前提・制約・罠 | そのコードの直上のコメント |
| 人間の下書き・未整理の思考 | ハーネスの外。AI に自動で読ませない |

skill に寄せきれないもの（どの手順にも属さない仕組みの説明など）だけを MD として残し、それを使うファイルの隣に置く。

移住のトリガーは「またこのドキュメントを手で渡したな」と気づいた瞬間。一括移行はしない。skill の更新も自動抽出しない。作業中にズレへ気づいたら提案に留め、レビューされない規範を量産しない。

## 2. 置き場所

- **複数リポで使う・リポに依存しない知識/手順**（`new-issue` `pr-workflow` `jp-writing` 等と同種）
  → `~/dotfiles/.claude/skills/<name>/SKILL.md`。
  home-manager の activation script（`home-manager/modules/claude.nix`）が rebuild のたびに
  `~/.claude/skills/` へ丸ごとコピーし、全リポ共通のグローバル skill になる。
  **`~/.claude/skills/` に直接書いても正本ではなく、次回 rebuild で消える**
  （`block-new-skill-md.sh` が直接作成を拒否する）。
  反映には rebuild が要るので、その場のセッションではまだ一覧に出ない場合がある。

- **そのリポ固有の手順・そのリポでしか意味を持たない知識**
  → 該当リポの `.claude/skills/<name>/SKILL.md`。dotfiles には置かない。

- 迷ったら「他のリポでこの手順が使われる場面があるか」で決める。使われるなら global。

## 3. 作成前の重複確認

global（`~/dotfiles/.claude/skills/`）と、作業中のリポの `.claude/skills/` の両方を検索し、
類似 skill が無いか確かめる。

## 4. frontmatter・内容の規約

`block-new-skill-md.sh` が Write 時に検査する。詳細はフック本体を参照。

```markdown
---
name: sops-secrets
description: sops / age による secret の暗号化・復号・再暗号化の運用手順。secret を暗号化するとき、`.sops.yaml` を変更するとき、新デバイスの鍵を登録するときに使用する。
---
```

- `name` / `description` は必須。description に「〜するとき使用する」と起動条件を列挙し、暗黙知を宣言に変える
- 既定は `disable-model-invocation: true`（明示呼び出し専用）。外すのは、条件を言語化できて、その条件が起きたときに読み落とすと事故る skill だけ。外すときは user に確認する
- 自動発火させる skill のうち、**効く場面がファイルで言えるものは `paths` で絞る**

```yaml
paths:
  - "articles/**"
  - "**/wrangler.jsonc"
```

絞る理由: skill の description 一覧はモデルのコンテキスト長の1%程度に収められ、溢れると**呼ぶ頻度の低いものから落ちる**。落ちる順は重要度ではなく頻度なので、放置すると稀にしか使わない重要な skill が先に痩せる。`disable-model-invocation: true` は description を一覧から消し、`paths` は一致するファイルを扱うときだけ自動発火させる。どちらも `/name` での手動呼び出しは残るので、絞りすぎの代償は「自動で出てこない」だけで済む。迷ったら絞る側へ倒す。ベンダー製の技術リファレンスは既定へ倒し、該当スタックのリポを実際に持っているものだけ `paths` で残す。

## 5. 読み込み量の多い skill は探索を分ける

全走査を伴う skill（棚卸し・公開前点検・台帳の突き合わせ）は、読んだ本文がそのまま親のコンテキストに残り、裁可の往復に使える残量を削る。読む対象が数ファイルを超えるなら、読み込みを読み取り専用の subagent へ出す。

- 渡すのは対象ファイルの一覧と観点。返させるのは所見だけ（1件につき「ファイル:該当箇所 → 何が問題か → 根拠になる原文の引用」）。要約や感想は返させない
- 親は**引用箇所だけを読み直して裏を取る**。読んでいない原文を根拠に user へ裁可を求めない
- 編集・裁可は親に残す。subagent は読むだけ

skill 全体を subagent 側で走らせる `context: fork` は、会話履歴を持たず背景で走るため、1件ずつ裁可を取る型の skill には使えない。分けるのは読み込みだけにする。
