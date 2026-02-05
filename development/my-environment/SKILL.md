---
name: my-environment
description: ユーザーの開発環境情報を提供。環境セットアップ、パス問題、依存関係の質問時に使用。
user-invocable: false
---

# 開発環境情報スキル

## システム構成
- OS: Windows 11 Pro
- ターミナル: PowerShell 7, Git Bash
- エディタ: VS Code

## Python環境
- pyenv-win でバージョン管理
- 主要パッケージ: pandas, openpyxl, xlwings, requests
- 仮想環境: venv推奨

## Office環境
- Microsoft 365 (Excel, Word, PowerPoint)
- VBAマクロ有効
- Oracle DBとの連携あり

## Google環境
- Google Workspace利用
- GAS (Google Apps Script) 開発
- clasp (GASローカル開発ツール) 利用可能

## パス・設定の注意点
- Windows特有のパス区切り（\\）に注意
- 日本語パスが含まれる場合あり
- エンコーディングはUTF-8を基本とする

## Examples

- `Pythonのバージョンを確認したい` → `pyenv versions` の実行方法を案内
- `Excelマクロが動かない` → VBA有効化設定の確認手順を提供
- `GASをローカルで開発したい` → clasp のセットアップ手順を案内
- `パスにスペースが含まれてエラー` → Windows特有のパス問題と対処法を説明

## Guidelines

- Windows環境では `\\` または `/` のパス区切りに注意
- 日本語を含むパスはエンコーディング問題の可能性を考慮
- pyenv-winでPythonバージョン切り替え時は `pyenv rehash` を忘れずに
- Office連携時はマクロセキュリティ設定を確認
- GAS開発はclaspでローカル開発を推奨（バージョン管理可能）
