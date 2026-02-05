---
name: Resolving-Conflict
description: 協助解決 Git Rebase 或 Merge 過程中的衝突，提供系統化的衝突解決流程。
---

# 解決 Git 衝突

協助使用者系統化地解決 Git Rebase 或 Merge 過程中的衝突。

## 核心功能

- 偵測當前的衝突狀態（rebase 或 merge）
- 列出所有衝突的檔案
- 逐個檢視並解決衝突
- 完成 rebase 或 merge 流程

## 執行步驟

### 1. 偵測衝突狀態

檢查當前是否處於衝突狀態：
```bash
git status
```

確認是 rebase 還是 merge 衝突：
- Rebase: 會顯示 `rebase in progress`
- Merge: 會顯示 `You have unmerged paths`

### 2. 列出衝突檔案

使用以下指令列出所有衝突的檔案：
```bash
git diff --name-only --diff-filter=U
```

或從 git status 中擷取：
```bash
git status --short | grep "^UU\|^AA\|^DD\|^AU\|^UA\|^UD\|^DU"
```

### 3. 解決衝突

對於每個衝突的檔案：

1. **讀取檔案內容**
   - 使用 Read tool 檢視衝突標記
   - 識別衝突區塊（`<<<<<<<`, `=======`, `>>>>>>>`）

2. **展示衝突資訊**
   - **IMPORTANT**: 在詢問使用者前，必須先清楚展示衝突的詳細內容
   - 明確標示雙方的修改內容
   - 說明衝突發生的位置和原因
   - 範例格式：
     ```
     檔案：src/example.ts
     衝突位置：第 10 行

     衝突內容比對：
     <<<<<<< HEAD (當前分支)
     const value = "version A"
     =======
     const value = "version B"
     >>>>>>> 合併進來的分支
     ```

3. **使用 AskUserQuestion 提供解決選項**
   - 列出所有可能的解決方案
   - 對於簡單衝突，提供：
     - 保留當前分支版本（ours）
     - 採用合併進來的版本（theirs）
   - 對於需要手動整合的情況，明確列出所有組合：
     - 方案 A + 方案 B
     - 方案 B + 方案 A
     - 其他自訂組合
   - 讓使用者基於完整資訊做出選擇

4. **執行解決**
   - 使用 Edit tool 根據使用者選擇移除衝突標記
   - 保留或整合正確的程式碼

5. **標記為已解決**
   ```bash
   git add <檔案路徑>
   ```

### 4. 完成流程

所有衝突解決後：

**Rebase:**
```bash
git rebase --continue
```

如果遇到「You must edit all merge conflicts」錯誤，可能是索引狀態不一致，使用以下方式重置：
```bash
git reset && git add <已解決的檔案> && git rebase --continue
```

**Merge:**
```bash
git commit
```

如果需要放棄：
- Rebase: `git rebase --abort`
- Merge: `git merge --abort`

## 使用場景

### 適用情境

- 執行 `git rebase` 時遇到衝突
- 執行 `git merge` 時遇到衝突
- 需要系統化地處理多個衝突檔案
- 不確定如何正確解決衝突

### 處理策略

**簡單衝突：**
- 完全採用一方的修改（ours 或 theirs）
- 直接使用對應策略：
  ```bash
  git checkout --ours <檔案>   # 保留當前分支的版本
  git checkout --theirs <檔案> # 採用合併進來的版本
  ```

**複雜衝突：**
- 需要手動合併雙方的修改
- 仔細檢視衝突區塊的上下文
- 整合兩邊的邏輯變更

## 工作流程範例

```
[執行 rebase 時遇到衝突]

User: 我在 rebase 時遇到衝突了，幫我解決。

Agent: 偵測到 rebase 衝突，有 2 個檔案需要解決：
  1. src/auth/login.ts
  2. README.md

開始解決第一個衝突...

檔案：src/auth/login.ts
衝突位置：第 15 行

衝突內容比對：
<<<<<<< HEAD (當前分支)
if (user.verified) {
  return authenticateUser(user)
}
=======
if (user.isVerified && user.active) {
  return authenticate(user)
}
>>>>>>> feature/new-auth

Agent: [使用 AskUserQuestion]
  要如何解決這個衝突？
  選項：
  1. 保留當前版本（user.verified）
  2. 採用新版本（user.isVerified && user.active）
  3. 整合：保留 isVerified 和 active 檢查，使用 authenticateUser
  4. 其他自訂方案

User: [選擇選項 3]

Agent: 已解決 login.ts 並標記為已解決。

繼續處理 README.md...
[展示衝突並詢問]

User: [選擇保留雙方的文件更新]

Agent: 所有衝突已解決，執行 git rebase --continue
  Rebase 成功完成！

User: [確認結果並繼續開發]
```

## 注意事項

### 安全檢查

- **資訊透明化**：在詢問使用者前，務必先展示完整的衝突內容和上下文
- **明確選項**：提供所有可能的解決方案，包括手動整合的不同組合方式
- 解決衝突前先確認了解雙方的修改意圖
- 不確定時使用 AskUserQuestion 詢問使用者應該保留哪個版本
- 解決後建議執行測試確保功能正常

### 常見錯誤

**避免：**
- 未展示衝突詳細內容就直接詢問使用者如何解決
- 手動整合選項不夠明確（例如只提供「整合雙方」而不列出具體組合方式）
- 直接刪除所有衝突標記而不檢視內容
- 未理解程式碼脈絡就決定保留哪個版本
- 解決衝突後未執行測試

**推薦：**
- 先展示完整的衝突資訊，再使用 AskUserQuestion 提供明確選項
- 列出所有可能的解決方案，包括不同的整合順序
- 仔細閱讀衝突區塊的上下文
- 理解兩個版本的差異原因
- 可能的話整合雙方的優點
- 解決後執行相關測試

### 特殊情況

**二進位檔案衝突：**
```bash
# 只能選擇其中一個版本
git checkout --ours <二進位檔案>
# 或
git checkout --theirs <二進位檔案>
```

**檔案刪除衝突：**
- 一方修改，一方刪除
- 需要判斷是否應該保留或刪除該檔案

## 整合其他工具

解決衝突後建議：
- 使用 `reviewers:requesting-code-review` 檢視解決方案
- 執行專案的測試套件
