---
name: laohan-donghua
version: "11.4.0-candidate"
description: METHOD_LAB/历史 episode 的双 renderer 动画编排器。默认 CODEX_DIRECT 生产不使用本 skill；只有用户明确要求旧 AST、Remotion/HyperFrames 对照或恢复历史 episode 时使用。
---

# 真人口播动画生产

> 2026-07-16 起，本 skill 仅保留 METHOD_LAB/历史兼容。新 episode 默认由 `codex-direct-production` 直接编写 Remotion、渲染完整 candidate、完整观看并最多修三轮；不经过 proposal/extension/seal 或双 renderer。

本 skill 执行已经做出的导演决策，不重新决定哪些话要动画。动画不是固定 B-roll 覆盖率，也不是一个 HTML 模板。

## 必要输入

读取当前 episode：

1. 07-剪辑/clean.mp4 与 subtitles.srt；
2. 09-导演/edl.json、animation-brief.json、animation-ast.json、source-manifest.json、renderer-brief.md、styleframes 与 animatic-manifest.json；NATIVE 还包括 renderer-route.json 与 caption-style.json；
3. 10-素材/素材清单.json（仅当 EDL 有 BROLL_STOCK）；
4. episode-config.json。

缺输入时报告文件名并停止。只有 素材清单.json 标为 visually_verified 的资产可以使用。

🛑 STOP：EDL、animation brief/AST、source manifest、renderer brief、animatic 或 required 素材缺失时，不创建 renderer 项目。先运行 `node animation-method/scripts/compile-animation-ast.mjs episodes/<slug>/09-导演 --check`；漂移时回⑨，不在⑪手修 AST。

## 工作流

### 1. 建立 renderer 任务

先在 workflow 根运行 `node scripts/prepare-renderer-handoff.mjs episodes/<slug> <remotion|hyperframes>`。两个 renderer 只能消费各自 `11-动画/renderer-handoffs/<renderer>/input-manifest.json`，先验证全部 SHA-256；禁止从 `视频动画` 的旧 pilot 或历史 project 猜输入。

渲染前运行 `node scripts/verify-renderer-handoff.mjs episodes/<slug>/11-动画/renderer-handoffs/<renderer>/input-manifest.json`。任何 hash 变化都回⑨或⑩重新生成 handoff，不能沿用旧 candidate。

读取 handoff 后，先为每个 renderer 写 `11-动画/renderer-proposals/<renderer>.json`：必须绑定当前 brief SHA，完整映射 AST state，能力只能来自 AST allow-list，proof 只能绑定⑩的 asset ID/SHA。再生成并验证 `11-动画/renderer-extensions/<renderer>.json`，同时绑定 AST/proposal SHA 和全部 state/transition/fact boundary；缺 extension 不得开始实现。

NATIVE 的确定性顺序固定为：

1. `node scripts/prepare-renderer-extension.mjs episodes/<slug> <renderer>`，再以 `--check` 验证；
2. `node scripts/create-renderer-workspace.mjs episodes/<slug> <renderer>` 创建未 seal scaffold；
3. 只在本期 workspace 实现批准 extension，移除 `NATIVE_IMPLEMENTATION_REQUIRED`；
4. `node scripts/seal-renderer-workspace.mjs episodes/<slug> <renderer>`，再运行 `node scripts/verify-renderer-workspace.mjs episodes/<slug> <renderer>`；
5. `node scripts/render-episode-<renderer>.mjs episodes/<slug>` 只生成 `candidates/base/<renderer>.mp4`；
6. `node scripts/apply-review-captions.mjs episodes/<slug> <renderer>` 使用同一 SRT/caption style 生成 `candidates/<renderer>.mp4` 和 caption evidence。

create workspace 之前缺 proposal/extension 必须失败且不得留下半成品 workspace；seal 必须拒绝 placeholder、renderer 内嵌字幕、非确定性时间/随机逻辑、未注册 timeline、合同/hash 漂移和 symlink。handoff 变化后旧 workspace、base 与 candidate 均不得继续使用。`renderer_track: PARITY` 才允许走旧 render_plan 兼容实现，且其结果不得冒充审美上限。

每个 candidate 先由独立审阅写入 `11-动画/qa-reviews/<renderer>.json`（绑定 candidate SHA、审阅者、时间、字幕安全区和有声审片结论及说明），再运行 `node scripts/create-qa-evidence.mjs episodes/<slug> <renderer> --review-file 11-动画/qa-reviews/<renderer>.json`，最后运行 `node scripts/create-render-manifest.mjs episodes/<slug>`。它生成真实 contact sheet、每个 selected beat 的入场/中段/退场帧、完整解码和结构化 `qa-evidence.json`。不能靠命令行或 Markdown 写 PASS 放行。

- CROSS_RENDER_VALIDATION_PAIR：Remotion 和 HyperFrames 各建独立 candidate 项目，使用同一 source hash、EDL、字幕和事实文字。
- PRIMARY_RENDERER：primary_renderer 必须是 remotion 或 hyperframes，且已有接受记录；否则停止并要求回到 CROSS_RENDER_VALIDATION_PAIR。专项 beat 只有在 EDL 明确指定后才交给另一 renderer。
- 两个 candidate 共享 AST 语义合同和已验证素材，但不共享组件实现、HTML、CSS、GSAP、React 布局常量、转场或旧项目 scene。

### 2. 实现 base video

- 每个 ILLUSTRATIVE beat 只实现 AST/approved proposal 指定的理解问题、state graph 和 must-preserve。
- HERO/NONE beat 保持真人，不新增主动画。
- PROOF beat 只能使用 source-manifest 记录的来源。
- BROLL_STOCK beat 只能使用 visually_verified 素材。
- Remotion 使用 frame-driven composition；HyperFrames 使用 deterministic paused timeline。
- BROLL/PROOF 只使用 handoff 锁定的本期真实资产；ILLUSTRATIVE 只显示 AST approved copy，禁止显示 `acceptance_question`。

### 3. 统一字幕与合成

- workspace 只读取 caption safe-band 数值做避让，不把 SRT 文本放入 NATIVE runtime；renderer base 不得各自烧字幕。两边 base 完成后必须由 `apply-review-captions.mjs` 用同一 SRT/caption style 生成 review candidate，并绑定 base/SRT/style/candidate/audio essence SHA。
- Remotion 使用 frame-driven native implementation；HyperFrames 使用可 seek 的 paused timeline。两者不得套同一固定卡片布局，也不得从 renderer 反向改 AST。
- 不把口播稿精简版、场景标题或旧项目字幕混入字幕轨。

### 4. QA 与交付

在 11-动画/ 写 candidates、contact sheets、render-manifest.json、qa-report.md。CROSS_RENDER_VALIDATION_PAIR 只写两个 candidate；viewer_verdict 为 ACCEPTED 且 selected_candidate 明确后，才把选中 candidate 写为 07-剪辑/final.mp4。PRIMARY_RENDERER 也遵守同一 final 条件。

QA 必须记录：画布、fps、时长、音视频 stream、完整解码、source hash、EDL 版本、字幕安全区、每个 selected beat 的 hero frame 与边界帧、有声审片结论。

## 执行模式

- REVIEW_GATED：静态构图和最终 MP4 等 Jeffrey 结论。
- AUTONOMOUS_RUN：在锁定 EDL 内自主渲染并最多三轮自检；发布始终等 Jeffrey。

技术 PASS 不等于 viewer PASS，不得因渲染成功把 candidate 写成 accepted 方法。

🔴 CHECKPOINT：只有 viewer_verdict=ACCEPTED 且 selected_candidate 是 technical_qa=PASS 的候选，才创建 final.mp4。

Jeffrey 明确选片后运行 `node scripts/accept-render-candidate.mjs episodes/<slug> candidates/<renderer>.mp4 --viewer-accepted`；脚本绑定 manifest、candidate、QA evidence，并创建同字节 final 与 review-record。

双 renderer 比较成立后运行 `node scripts/record-renderer-validation.mjs episodes/<slug> <renderer> --viewer-accepted "<选择理由>"`。它绑定两份 candidate/QA/review 并生成结构化 comparison；只有该记录通过后，下期才允许切 PRIMARY_RENDERER。

## 失败处理

| 情况 | 动作 |
|---|---|
| renderer 无法读 source | 生成兼容 production source，记录新 hash，并让两边使用同一字节文件 |
| 画面遮挡字幕 | 修 overlay 或字幕安全区后重渲染，不能删字幕掩盖 |
| 视觉像旧模板或两个 renderer 太像 | 回读 renderer-brief；保留同一语义，分别重做视觉语言 |
| EDL 缺 source 或事实来源 | 返回⑨，不由本 skill 猜补 |
| QA 不通过 | 最多三轮针对性修复；仍失败则保留 candidate 并报告失败证据 |

## 禁止事项

- 不按固定 coverage、每 N 秒场景、固定 face-wrapper、固定卡片或固定文字生成；
- 不把 clean.mp4 复制命名为 final.mp4；
- 不为展示素材而插无关 B-roll；
- 不使用旧 v10 的 index.html、示例、视觉常量或人工 gate 规则；
- 不自动发布。
