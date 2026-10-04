---
name: release
description: BeeCount 全家桶发版流水线:App(BeeCount)与自建云(BeeCount-Cloud)打 tag 触发 CI 全自动构建,加上 changelog 双格式、官网文档同步、宣传视频与社媒文案的完整收尾。当用户说"发布新版本"、"发版"、"App 发 X.Y.Z"、"cloud 发个版本"、"打个 tag 发布"、"release 一下"、"准备上架"时必须使用本技能——哪怕只发一端、哪怕只是"先把 changelog 写了",也按本流水线对应步骤走。不适用于:日常 PR 合并(不发版)、honeycomb/video-studio 等其它仓的发布、商店审核被拒的申诉处理。
---

# beecount-release — 双仓发版流水线

**核心信念**:发版动作(打 tag)不可逆且公开,但流程的其余部分都可重复。所以**确认在前、tag 在后**,tag 之后的一切交给 CI 和收尾清单。

## 红线(先读)

1. **版本号与发布范围必须用户拍板**。用 AskUserQuestion 一次问清:这次发 App、Cloud,还是两个都发?各用什么版本号?可以用 `git tag --sort=-v:refname | head -1` 推算建议值(默认 minor +1)作为推荐选项,但**用户没确认前绝不打 tag**。
2. **打 tag 前的最后一步,把即将执行的 tag 命令(仓库+版本号)展示给用户过目**。两个仓的 tag 序列差很远(App 3.x vs Cloud 1.x),打串了就是公开事故——历史上真的发生过在 BeeCount 仓里打 Cloud 版本号的事。
3. 商店文案红线:Google Play `<lang>` 段**不得出现任何 iOS 内容**(纯 iOS 条目整条剔除,不是改写);商店文案**不写自部署/服务端运维**条目(那些只进 Cloud 的 GitHub Release 和官网)。

## 流程

```
0 预检 → 1 确认门(范围+版本号) → 2 Cloud 打 tag → 3 App 打 tag
→ 4 changelog 双格式 → 5 官网文档同步(纯 bug 修复可跳) → 6 视频+文案(可选) → 7 收尾核验
```

只发一端时跳过另一端的步骤;**双端都发时 Cloud 永远在 App 之前**(版本偏斜规则:老 App 忽略新字段没事,新 App 对老服务端可能表现为"设置不生效",所以让用户的生产环境先有新镜像可升)。

### 0. 预检(两仓各自)

```bash
git -C ~/code/mine/BeeCount status --short && git -C ~/code/mine/BeeCount log origin/main..main --oneline
git -C ~/code/mine/BeeCount-Cloud status --short && git -C ~/code/mine/BeeCount-Cloud log origin/main..main --oneline
```

- 工作区必须干净、main 与 origin 同步;有未合 PR 先问用户是否要进这个版本。
- 顺手列出上个 tag 以来的提交(`git log <last-tag>..main --oneline`),这既是确认门里"这版包含什么"的依据,也是 changelog 的素材。

### 1. 确认门

AskUserQuestion 问两件事(可一次问完):**范围**(仅 App / 仅 Cloud / 都发)与**版本号**(给出建议值供选,允许用户改)。得到明确答案后,把将要执行的命令原样列给用户看一眼再动手。

### 2. Cloud 发版(若在范围内)

```bash
cd ~/code/mine/BeeCount-Cloud && git tag <X.Y.Z> && git push origin <X.Y.Z>
```

- tag **必须三段式 `*.*.*`**(两段式不触发 release workflow)。
- CI 自动:测试 → 构建前端 → 推 Docker 镜像 `sunxiao0721/beecount-cloud:<X.Y.Z>` + `:latest` → 生成 GitHub Release。
- 数据库迁移随镜像启动自动执行,无需手工步骤;但若本版含迁移,收尾时要在升级提示里写明。

### 3. App 发版(若在范围内)

```bash
cd ~/code/mine/BeeCount && git tag <X.Y.Z> && git push origin <X.Y.Z>
```

- **不要改 pubspec.yaml 的 version**(本地永远是 0.0.1):CI 从 tag 名注入版本号,本地改了也会被覆盖,纯属白改。
- 任意 tag 名都会触发 Release workflow,所以 tag 名打错=错误版本直接开始构建,这就是红线 2 存在的原因。
- CI 产出:多 ABI APK(arm64 主包/armv7/x86_64/universal)+ iOS 构建 + GitHub Release。

### 4. changelog 双格式(App 发版时)

写 `BeeCount/.docs/changelogs/<X.Y.Z>.txt`,**单文件两段**,没有 CI 消费方——用户在 App Store Connect / Google Play Console 后台手动粘贴,所以格式必须可直接复制。模板(取自 3.4.0 真实例):

```
<X.Y.Z>

简体中文
- <条目,口语化一句话,带价值点>

繁體中文
- <同条目繁体>

English
- <同条目英文>


# ========== Google Play(直接复制粘贴) ==========

<en-US>
- <英文条目,已剔除纯 iOS 项>
</en-US>
<zh-CN>
- <简体条目,已剔除纯 iOS 项>
</zh-CN>
<zh-HK>
- <繁体条目,已剔除纯 iOS 项>
</zh-HK>
```

- 上段给 Apple(可以提 iOS 27 这类平台特性);下段 Google Play 执行红线 3。
- 条目从步骤 0 的提交列表提炼,只写用户可感知的变化。**`.docs/` 已被 gitignore,changelog 是本地文件、不进 git(历史版本也都未跟踪),写好供用户在商店后台手动粘贴即可——不要 commit,也别 `-f` 强加。**

### 5. 官网文档同步(BeeCount-Website)

- **纯 bug 修复版本可整步跳过**:本版只是修 bug、没有用户可感知的新功能 / 行为变化时,官网不需要同步(发了 changelog 即可)。下面几条只在**有新功能或行为调整**时做。
- `docs/changelog.md` 顶部加「X.Y.Z 亮点」小节(emoji + 一句话/条,链接到功能文档)。**亮点只写新功能/行为变化,修复类、翻译修正类条目一律不进**(修复细节看 GitHub Releases;商店 changelog 不受此限,照常包含修复条目)。
- **英文镜像 changelog 必须同步**:`i18n/en/docusaurus-plugin-content-docs/current/changelog.md` 加同版本「X.Y.Z highlights」小节,与中文条目一一对应——只更中文版等于英文站漏发。
- 大功能写专页:`docs/<分类>/<feature>.md` + `i18n/en/.../<feature>.md` 英文镜像 + `sidebars.ts` 挂载;相关旧页面(预算/统计/账本等)加行为标注。
- 若 App 新功能依赖 Cloud 新版本:在 `docs/cloud-sync/beecount-cloud.md` 的版本升级 `:::tip` 里写清**先服务端后 App**的升级顺序与迁移说明。
- commit + push(此仓允许直推 main);部署由仓库 CI 处理。

### 6. 宣传视频与社媒文案(可选)

素材(用户录屏)到位才做,没素材就明确告诉用户"这步等录屏"。在 video-studio 仓走既有技能链:**analyze-footage → author-narration → produce-video**(9:16,陕西话变体看用户偏好)。发布文案落 `projects/beecount/copy/v<X.Y.Z>-<feature>.md`,**必须包含 BeeCount-Cloud 的版本文案**;原始素材绝不入库(materials/ 已 gitignore)。

### 7. 收尾核验

```bash
gh run list --repo TNT-Likely/BeeCount --limit 3
gh run list --repo TNT-Likely/BeeCount-Cloud --limit 3
```

- 确认两边 Actions 绿、GitHub Release 已生成(失败要读日志、修复后重打 tag 或 rerun)。
- 给用户一份**人工待办清单**(机器做不了的):App Store Connect / Play Console 粘贴 changelog 并提审;生产环境 `docker compose pull && up -d` 升级 Cloud(在 App 商店通过审核**之前**完成);若本版关联 issue,发版后回复并关闭。

## 反模式(都是真踩过的)

- 没等用户确认版本号/范围就打 tag —— 不可逆,红线 1。
- 在错误的仓里打另一端的版本号 —— 红线 2 的由来。
- 本地改 pubspec version 再 tag —— CI 覆盖,白改还污染 diff。
- Cloud tag 打两段式(如 `1.4`)—— workflow 不触发,看起来"发了"实际什么都没发生。
- Google Play 段保留 iOS 条目、或商店文案写"配合 Cloud 升级" —— 商店审核/用户困惑,红线 3。
- 双端发布却先发 App —— 用户升了 App 连不上旧服务端功能,版本偏斜事故。
- 纯 bug 修复版还去同步官网 / 写功能页 —— 没新功能就只发 changelog,别给官网硬凑"亮点"。
- 混合版本把修复/翻译修正条目写进官网亮点 —— 亮点是营销性摘要,只挑功能写(3.5.5 真踩过,用户点名删)。
- 官网只更中文 changelog、漏掉 `i18n/en/.../changelog.md` 英文镜像 —— 英文站等于没发这版(3.5.5 真踩过)。
- 把 changelog 当成要 commit 的文件(它在 gitignore 的 `.docs/` 下)—— 本地写好供粘贴即可。

## 下一步

发版完成后若有新 issue 反馈,用 `github-issue-triage:analyze-issue` 评估;下个版本的功能规划走常规开发流程。
