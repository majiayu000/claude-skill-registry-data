---
name: claude-drives-gemini
description: Use when the user wants to generate images, video, or music with Gemini (生图/生视频/生乐/配图/PPT插图/用Gemini出图/做视频/做音乐/Nano Banana/Veo/Lyria) on a machine with a dedicated Chrome profile logged into Google AI Pro. Claude orchestrates; Gemini generates the pixels/frames/audio.
---

# claude-drives-gemini v1.0 — 用 Gemini Pro 网页(CDP)出图 / 视频 / 音乐

Claude 只当**导演**:经 CDP 操控已登录的专用 Chrome(9223),用 Nano Banana(图 2816×1536)/ Veo(视频,界面标 "Omni")/ Lyria(乐)出活。**产物全尺寸无损落盘,媒体字节绝不进上下文。**

## ⭐ 一条命令(默认打法)

```bash
cd ~/.claude/skills/claude-drives-gemini/scripts
node gemini-gen.mjs <image|video|music> "<提示词>" <out> [--use-tool]
```

全内置:preflight(查/拉专用 Chrome+取 ws)→ **确保模式 Pro+扩展思考** → 直发提交 → 阶段感知等待 → 原生下载 → 关 tab。回执一行 JSON:`{ok,type,file,dims,mb,mode,resubmits,seconds}`;失败含 `stage`(chrome/submit/wait/genfail/download/wait-infra/run)与可补捞的 `tid`。

- **阶段感知重试,绝不盲目重提交**:「无法生成」明确拒绝→同 tab 安全重发 1 次(未产出不烧额度);视频直发连拒→自动降级 `--use-tool`;超时→只延长等待;下载失败→只重下载并保留 tab。
- **耗时预期(Pro 扩展思考)**:图 1–3 分钟、乐 1–2 分钟、视频 2–5 分钟。比 Flash 慢数倍且思考期**无任何页面迹象**——是质量的代价,不是卡死,别中途放弃。
- 多个产物一律**串行**跑,复用 ws:`WS=$(node gemini-wsurl.mjs)` 后每次传 `--ws "$WS"`。

## 提示词契约(直发,必守)

- 必须带明确生成动词:「**直接生成/制作一段…图片/视频/音乐**」+「**不要解释**」。描述性措辞会被误路由(实测"适合阅读的钢琴曲"被当点歌弹 YouTube Music)。
- 视频需要 **9:16 竖屏 / 风格模板**(面板内建 18 款)→ 加 `--use-tool` 走工具面板。

## 铁律(违背 = 失败)

1. **媒体只落盘、只回元数据**;绝不 base64 进上下文(6MB 图 ≈ 50 万 token)。质检只看 384px 缩略图,或派子 agent 看了回文字结论。
2. **高清 = 原生下载钮**(真 2816×1536),不是截图(页面 `<img>` 只是 1408 半分辨率预览)。
3. **额度先评估再出活**:Veo App 仅 **3 条/天**;触顶降级并**告知用户**,不闷头重试 → `references/quota-tiers.md`。
4. **水印诚实**:可见水印用官方开关关(Gemini 网页 设置→媒体水印→关闭,一次即可,覆盖图/视频/乐);**SynthID 隐形水印仍在且去不掉**,如实告知用户。
5. **串行不并行、节流出活**(防封号)→ `references/runtime-env.md`。

## 渐进式披露(按需读,别全读)

| 什么时候 | 读哪个 |
|---|---|
| `stage=chrome` / 登录墙 / 代理·端口·下载目录 / 模式与耗时 / 防封号·无人值守 | `references/runtime-env.md` |
| 选择器失效、Gemini 改版 → 重探 + 自愈 + 回写(技能自我进化) | `references/gemini-ui.md` |
| 额度触顶 → 各模态降级路线 | `references/quota-tiers.md` |
| 水印:官方开关位置 / SynthID / 无开关账号的兜底 | `references/dewatermark.md` |
| 分步命令链、单步调试、全部脚本用法 | `scripts/README.md` |
| 换机/首装:setup 向导 · 零额度冒烟 | `setup/init.mjs` · `scripts/smoke.mjs` |

## 失败速查(看 JSON.stage)

- `chrome`:跑 `launchers/start-chrome.cmd|sh`(没有就先 `node setup/init.mjs` 生成);页面 ERR 多半是本地代理没开(runtime-env)。
- `genfail`:两次明确拒绝——换提示词表述再试。
- `wait`/`download` 且带 `tid`:产物可能已在页面,`node gemini-download.mjs "$WS" <tid> <type> <out>` 补捞(下载目录按 ws 端口自动判断;实测有效),完了关 tab。
- `wait-infra`/`run`:基础设施/未分类错误,看 `error` 文本。
- 登录墙:跑 `launchers/login-chrome.cmd|sh` 人工续期(**勿在调试端口窗口登录**),详见 runtime-env。
