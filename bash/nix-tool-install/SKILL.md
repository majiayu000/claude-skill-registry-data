---
name: nix-tool-install
description: 新しい CLI ツール・パッケージをインストールしたくなったときの手順。brew install / npm -g / pip install --user 等を打つ前に必ず使用する。全デバイスが Nix 管理（nix-darwin / NixOS + home-manager）であり、Nix 外のパッケージマネージャでのインストールは禁止。
---

# nix-tool-install

フリートの全デバイスは Nix 管理下にある。ツールの導入は必ず Nix 経由で行い、**Homebrew・npm -g・pip install --user・cargo install 等でシステムにインストールしない**（`nix search` の前に brew へ手を伸ばすのが典型的な誤り）。

この禁止は `.claude/hooks/block-non-nix-install.sh` が PreToolUse で機械的に遮断しており、拒否メッセージから本スキルへ誘導される。

## 手順

### 1. 用途の寿命を判断する

| 用途 | 導入先 |
|---|---|
| 今この場で1回きり（以後使う見込みなし） | `nix run nixpkgs#<pkg> -- <args>` または `nix shell nixpkgs#<pkg>`（設定変更なし） |
| **繰り返し使う開発ツール（既定はこれ）** | `devices/<device>/home.nix` の `home.packages` |
| GUI 全デバイスで常用 | `devices/common/home.nix` の `home.packages` |
| リポ固有のランタイム依存（clone した他人にも必要なもの） | そのリポの `shell.nix`（または flake devShell） |

対象デバイスは `hostname -s` で確認する。

迷ったら home.nix。`nix run` / `nix shell` は使い捨てであり、同じツールを何度も一時起動するのは非効率（毎回 eval が走る）。shell.nix は「自分の道具置き場」ではなく、リポの再現性（他人が clone して動かすのに必要なもの）のためだけに使う。

### 2. パッケージ名を確認する

```bash
nix search nixpkgs <tool> 2>/dev/null | head
```

nixpkgs に無い場合はその旨を user に報告して指示を仰ぐ（flake input 追加・overlay はここで勝手にやらない）。
derivation を書いて載せると決まったら、言語別の書き方と配線は [reference/nix-packaging.md](reference/nix-packaging.md) を使う。

### 3. 反映する

- **一時利用**: `nix run` / `nix shell` はそのまま使える。反映作業なし
- **shell.nix**: 編集後、`nix-shell` に入り直せば反映される
- **home.nix**: 編集まで行い、rebuild は user に依頼する
  - macOS: `sudo darwin-rebuild switch --flake ~/dotfiles#<host>`
  - NixOS: `sudo nixos-rebuild switch --flake ~/dotfiles#<host>`
  - rebuild は sudo を要するため Agent は実行しない。編集内容と上記コマンドを提示して終わる

## 一時的な依存が要るとき

検証のためだけに Python パッケージ等が要る場合は、使い捨て環境で取り込む。

```bash
nix-shell -p "python3.withPackages (ps: [ ps.pyyaml ps.fastapi ])" --run '...'
```

## 注意

- dotfiles の変更はコミット対象。編集したら user に rebuild 依頼と合わせて伝える
- `~/.claude/` 配下（settings.json / CLAUDE.md / skills / hooks）も `home-manager/modules/claude.nix` が本リポの `.claude/` からコピーしている。この領域の恒久変更は本リポ側を編集する（`.claude/hooks/block-live-claude-config-edit.sh` が直接編集を遮断する）
