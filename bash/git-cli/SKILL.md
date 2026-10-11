---
name: git-cli
description: >
  Git 命令地图：日常（status/add/commit/log/diff）、分支与合并、远程（push/fetch/pull/clone）、
  撤销（amend/reset/restore）、进阶（blame/bisect/stash/rebase -i/revert/worktree）、gitignore 与
  git config。Use when the user asks to commit, branch, merge, resolve conflicts, push, undo, or
  recover something in Git. 触发于「帮我 git 提交/合并/解冲突/推送/撤销/找回」。
---

# Git 命令行

主线：命令只是对数据模型（见 `git-data-model`）的操作；本条是命令地图，细节查 `git help <command>` 与 Pro Git。提交信息契约见 `writing-for-readers`；往上游发 PR 的规范见 `contributing-upstream`。

## 日常

- `git init` 建仓库（数据在 .git）；`git status` 看现状；`git add <file>` 加进暂存区；`git commit` 造新提交——写好的提交信息（见 `writing-for-readers`）。`-m` 命令行直接给信息，`-a` 提交所有已跟踪文件的改动。
- `git log` 扁平历史（不带 `--all` 只显示当前分支可达的历史）；`git log --all --graph --decorate` 把全部历史画成 DAG；`git log -p` 带每个提交的内联 diff。
- `git diff <file>` 相对暂存区的改动；`git diff <revision> <file>` 两个快照间的差异（`HEAD~` 表示 HEAD 的父提交）。
- `git checkout <revision>` / `git switch` 更新 HEAD 并把工作目录改成该快照的内容（检出分支时连当前分支一起动）。

## 分支与合并

- `git branch` 看/建分支；`git switch <name>` 切换；`git checkout -b <name>` 建并切换（= branch + switch）。
- `git merge <revision>` 合入当前分支；`git mergetool` 用图形/终端工具解冲突。合并启发式：改不同文件、或同文件相距较远的块 → 自动合并；改到同一处 → 冲突，文件里出现 `<<<<<<<` / `=======` / `>>>>>>>` 标记——编辑保留想要的内容、删标记，再 `git add` + `git commit`（或 `git merge --continue`）。
- `git rebase` 把一组补丁搬到新基底。

## 远程

- `git remote` / `git remote add <name> <url>`。
- `git push <remote> <本地>:<远程>`：发送到该提交为止的完整历史并更新远程引用；`git branch --set-upstream-to=<remote>/<remote branch>` 建立跟踪关系（之后裸 `git push` 即可）。
- `git fetch` 拉对象并更新 `origin/main` 等远程跟踪引用，不动你的本地分支；`git pull` = fetch + 更新本地分支（能快进就快进，否则合并）；`git clone` 下载整个仓库。

## 撤销

- `git commit --amend` 改最近提交的内容/信息；`git reset <file>` 取消暂存；`git restore` 丢弃改动。
- 敏感信息误提交：已推送 → 立即去服务方作废该密钥（历史里留着也不致命），别指望删历史；未推送 → 用 rebase 改写历史。
- detached HEAD 下误提交：记下打印出的哈希，`git branch <name> <hash>` 找回。
- 出了岔子查 [Oh Shit, Git!?!](https://ohshitgit.com/) 救火清单。

## 进阶

- `git blame` 谁最后改了哪行；`git bisect` 二分定位引入问题的提交（好提交信息+干净提交让 bisect 威力最大，见 `writing-for-readers`）。
- `git stash` 临时收起工作区改动；`git revert` 造新提交反做旧提交（安全回滚已推送的历史）。
- `git rebase -i` 交互式改写历史；`git add -p` 交互式挑拣暂存。
- `git worktree` 同时检出多个分支。
- `.gitignore` 声明故意不跟踪的文件；全局用 `git config --global core.excludesfile ~/.gitignore_global`（设定的是路径，文件要自己建）。
- `git config` 管一切配置，如别名：`git config --global alias.graph 'log --all --graph --decorate --oneline'`。

## 杂项

- GUI 客户端很多，讲师们不用，用命令行。
- Shell 提示符里显示 git 状态很实用（zsh/bash，Oh My Zsh 等框架常带）；Vim 集成用 fugitive.vim。
- GitHub ≠ Git：PR 是 GitHub 特有的协作方式；还有 GitLab、BitBucket 等托管。
- 常见分支惯例：main 放最新稳定代码，feature/bugfix 分支开发后合并回 main；网站类再加 staging 分支（先并 staging 测试，再并 main）。更复杂 workflow 见 Pro Git 后续章节。

## 资源

- [Pro Git](https://git-scm.com/book/en/v2) 1–5 章（懂模型后必读）；[Learn Git Branching](https://learngitbranching.js.org/)（浏览器游戏）；[Oh Shit, Git!?!](https://ohshitgit.com/)（救火）。

## 练习

学习材料在 `exercises.md`。

> 改编自 MIT The Missing Semester 课程 Lecture 5: Version Control and Git（讲义 + 口播稿，CC BY-NC-SA 4.0）：https://creativecommons.org/licenses/by-nc-sa/4.0/ · 课程站点：https://missing.csail.mit.edu/ · 讲座视频：https://www.youtube.com/watch?v=9K8lB61dl3Y
