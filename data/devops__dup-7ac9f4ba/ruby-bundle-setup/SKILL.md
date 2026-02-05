---
name: ruby-bundle-setup
description: Ruby environment setup and update workflow using rbenv and Bundler. Use when user asks to update Ruby environment, update rbenv, install Ruby version, run bundle install, update Gemfile.lock, or set up Jekyll/Ruby project dependencies. (user)
---

# Ruby Bundle Setup

rbenv and Bundler を使用した Ruby 環境のセットアップと更新ワークフロー。

## Initial Setup (初回インストール)

### rbenv のインストール

```bash
# Homebrew でインストール
brew install rbenv ruby-build
```

### zshrc の設定

`~/.zshrc` に以下を追加:
```bash
# rbenv
export PATH="$HOME/.rbenv/bin:$PATH"
eval "$(rbenv init - zsh)"
```

設定を反映:
```bash
source ~/.zshrc
```

### インストール確認

```bash
rbenv -v
which rbenv
```

---

## Update Workflow (更新)

### Step 1: rbenv の更新

```bash
# rbenv 本体の更新 (Homebrew)
brew upgrade rbenv ruby-build
```

### Step 2: Ruby バージョンの確認とインストール

```bash
# 利用可能な Ruby バージョン一覧
rbenv install -l

# 特定バージョンのインストール
rbenv install <version>

# グローバル設定
rbenv global <version>

# プロジェクトローカル設定
rbenv local <version>

# rehash (新しいバージョンを認識させる)
rbenv rehash
```

### Step 3: Bundler のセットアップ

```bash
# Bundler のインストール/更新
gem install bundler

# バージョン確認
bundle -v
```

### Step 4: bundle install と Gemfile.lock の更新

```bash
# 依存関係のインストール
bundle install

# Gemfile.lock の更新 (全てのgemを最新に)
bundle update

# 特定のgemのみ更新
bundle update <gem-name>
```

## Quick Reference

初回インストール:
```bash
brew install rbenv ruby-build
# ~/.zshrc に追加: eval "$(rbenv init - zsh)"
source ~/.zshrc
```

rbenv/ruby-build の更新:
```bash
brew upgrade rbenv ruby-build
```

日常の更新:
```bash
bundle update && bundle install
```