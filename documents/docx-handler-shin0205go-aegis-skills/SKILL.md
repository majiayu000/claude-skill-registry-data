---
name: docx-handler
displayName: DOCX Handler
description: Word文書の読み取り、編集、作成を行うスキル
allowed-tools:
  - filesystem__read_file
  - filesystem__read_text_file
  - filesystem__write_file
  - filesystem__edit_file
  - filesystem__list_directory
  - filesystem__create_directory
allowedRoles:
  - editor
  - admin
---

# DOCX Handler Skill

このスキルはWord文書（.docx）の操作を行います。

## 機能

- Word文書の読み取りと内容抽出
- 新規Word文書の作成
- 既存文書の編集・更新
- 文書のフォーマット変換

## 使用方法

1. 文書を読み取る場合は、ファイルパスを指定してください
2. 新規作成の場合は、内容とファイル名を指定してください
3. 編集の場合は、対象ファイルと変更内容を指定してください

## 注意事項

- 大きなファイル（10MB以上）の処理には時間がかかる場合があります
- マクロを含む文書（.docm）は非対応です
- 文書のパスワード保護は解除できません
