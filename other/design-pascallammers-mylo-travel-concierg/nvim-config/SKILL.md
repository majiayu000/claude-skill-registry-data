---
name: nvim-config
description: Neovim設定の相談と編集を行うスキル。プラグインの追加、キーバインドの設定、LSPの設定、UIのカスタマイズなど、init.luaの編集全般をサポートします。
allowed-tools: Read, Edit, Write, Bash, Glob, Grep
---

# Neovim設定エディタ

## 概要

このスキルは、Neovimの設定ファイル（`~/.config/nvim/init.lua`）の編集と管理をサポートします。

## 対象ファイル

- **メイン設定**: `/Users/toshiro/.config/nvim/init.lua`
- **プラグイン管理**: lazy.nvim
- **カラースキーム**: tokyonight.nvim

## サポートする操作

### 1. プラグインの追加と設定
- lazy.nvimを使用したプラグインのインストール
- プラグインの設定とオプション調整
- 依存関係の管理

### 2. キーバインドの設定
- ノーマル、ビジュアル、インサートモードのマッピング
- リーダーキーを使ったカスタムコマンド
- プラグイン専用のキーバインド

### 3. LSPサーバーの管理
- Mason経由でのLSPサーバーのインストール
- 言語サーバーの設定（Python、Terraform、Rustなど）
- LSP関連のキーバインド設定

### 4. UI・表示設定
- 行番号、相対行番号の設定
- ステータスライン（lualine）の設定
- ファイルツリー（nvim-tree）の設定
- カラースキームの変更

### 5. その他の設定
- オプション設定（`vim.opt`）
- グローバル変数（`vim.g`）
- autocommands
- カスタム関数

## 使用パターン

### プラグインの追加（lazy.nvim）
```lua
{
  "author/plugin-name",
  dependencies = { "required/plugin" },
  config = function()
    require("plugin-name").setup({
      -- 設定オプション
    })
  end,
}
```

### キーマップの設定
```lua
-- ノーマルモード
vim.keymap.set('n', '<leader>key', '<cmd>Command<cr>', { noremap = true, silent = true })

-- 関数を実行
vim.keymap.set('n', '<C-g>', function()
  local word = vim.fn.expand('<cword>')
  vim.cmd('Ggrep ' .. word .. ' * | cw')
end, { noremap = true, silent = true })
```

### LSPサーバーの追加
```lua
require('mason-lspconfig').setup({
  ensure_installed = {
    'pyright',     -- Python
    'terraformls', -- Terraform
    'rust_analyzer', -- Rust
  },
})
```

### オプション設定
```lua
vim.opt.relativenumber = true
vim.opt.number = true
vim.opt.tabstop = 2
vim.opt.shiftwidth = 2
vim.opt.expandtab = true
vim.g.mapleader = " "
```

## ワークフロー

1. **現在の設定を確認**: Readツールでinit.luaを読み込む
2. **変更箇所を特定**: ユーザーの要望に基づいて適切なセクションを見つける
3. **編集を実行**: Editツールで既存の設定を更新、またはWriteツールで新規作成
4. **検証**: Luaの構文エラーがないか確認
5. **適用方法を案内**: `:source ~/.config/nvim/init.lua`またはNeovim再起動を提案

## 注意事項

- 既存の設定を必ず読んでから編集すること
- プラグインマネージャー（lazy.nvim）の構文に従うこと
- リーダーキーはスペースキーに設定されている
- 変更後は必ずNeovimで動作確認すること
- 重要な変更の前にバックアップを推奨

## よくある質問

**Q: 新しいプラグインを追加したい**
A: lazy.nvimのプラグインリスト（`require("lazy").setup({...})`）に追加します

**Q: キーバインドを追加したい**
A: `vim.keymap.set()`を使って設定します。init.luaの末尾に追加するか、適切なセクションに配置します

**Q: LSPが動かない**
A: `:LspInfo`で状態確認、`:Mason`でサーバーのインストール状況を確認します

**Q: 設定を反映させるには？**
A: Neovim内で`:source ~/.config/nvim/init.lua`を実行するか、Neovimを再起動します

## 参考情報

- プラグインマネージャー: [lazy.nvim](https://github.com/folke/lazy.nvim)
- LSPマネージャー: [mason.nvim](https://github.com/williamboman/mason.nvim)
- カラースキーム: [tokyonight.nvim](https://github.com/folke/tokyonight.nvim)
