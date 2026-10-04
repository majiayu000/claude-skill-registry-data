---
name: laohan-fengmianzhuzige
version: "6.1.0"
description: 完全对标柱子哥TzFilm封面体系（81张真实封面逐张检视实证2026-09-20）——三层合成管线：AI/真实背景板（无字无人）+真人环境照片层+Remotion材质级文字层。画幅1080x1440(3:4原生)。Use when 工作流⑥选用zhuzige套（默认），或用户说"柱子哥封面""做封面"。与 laohan-fengmianqiuzhi（秋芝套）互为可切换双轨。
---

# 柱子哥式封面：三层合成 v6.1（定版）

**v6.1定版（Jeffrey验收2026-09-20）**：`samples/shoucuogongju-v62-final.jpg`（SHA-256前缀`aeb933ed`）为风格基线样张——OPPO形象照（藏青衬衫+眼镜+胡茬）+全栈v6.2（3:4材质字+左中证据卡EvidenceCard+右上MiniStamp小章+人物提亮档）。定版参数基线=samples/brief-example.json：人物提亮档（env_brightness 0.66/saturation 0.78/tint 0.26/face_boost 1.7/弱scrim 160）+text_top 748+kicker 236+证据卡三行（内容取自当期口播稿深水区清单）。同日实测教训：暗场单侧光素材（微信头像照）若脸的一半在暗部+裁切不当会"脸看不全"——**素材验收第一优先级=脸完整明亮可见**，其次才是光比融入；定版因此回到亮场形象照+提亮档路线。出厂检查纪律：三段放大逐字转录+关键边界像素级检测（章×脸间隙、脸区零遮挡、无全黑行），不得只靠整体打分。

**路线定义**（81张真实封面逐张检视实证 + 2026-09-20复刻实测）：柱子哥封面**不是整幅AI生成**，是三层合成——①AI生成/UI截图的**无字背景物件板**；②他本人**真实照片**（每期服装姿势不同，脸100%一致靠真人）；③设计工具排版的**五层文字系统**；合成后**整图统一调色**（冷调暗调ONE GRADE——先合成后调色，人物与环境才是一张照片）。2026-01他本人试过"AI生成整幅含人物"（#03/#04）后放弃，2026-03起全部转为三层合成。本skill用同一结构复刻。

**历史教训链**：v2.0误判"纯抽帧"（抓错图层）→ v3.0误改"AI单pass生成整幅海报"（身份不像/英文错字ERLY/版式失控三硬伤实测）→ v4.0三层合成确立 → v4.x小窗/抠像"贴纸感"翻车 → v5.1定案`env_photo`唯一正解 → **v6.0实测钉死三个非参数级瓶颈并逐项修掉**：(a)画幅错位——参考系81张全部3:4(covers_real 323x430)而产物曾是9:16，画幅改为1080x1440原生；(b)文字材质——PIL平面填充=PPT感，改为**Remotion静帧渲染材质字**（与正片HUD同源组件，templates-v2已验收）；(c)素材光线——亮场平光照片压暗后=灰暗监控感（v6加入机器可判的亮场预检），**暗场摆拍是env_photo路线的硬前提**。

## 输入与前置

1. 当前 `01-口播稿.md`：取hook句+主记忆点→转标题组；
2. 真人帧：**封面专门摆拍优先**（暗场+单侧实用灯+讲解手势，见下方"素材光线准入"）；无摆拍时用 `07-剪辑/raw.mp4` hook时段抽帧（无烧录字幕，用raw-transcript.json定位时刻）；备选本期reference身份照；
3. `episode-config.schema_version` 为4，绑定不满足时停止。

## 素材光线准入（v6硬门槛，机器可判）

env_photo源裁区在build时自动测光：`mean>115 且 p95-p5<110` = **亮场平光**→打WARN提示预期灰暗监控感；`brief.strict_light=true`时直接拒绝。这不是调参能救的：柱子哥照片的前提是**暗场+实用灯**（融入六法实证"他的房间是暗场"），亮房间压暗只是变灰不是变暗场。正确解法=按"补拍清单"（references/）重拍，不是继续调brightness。

## 标题组（五层文字系统，逐条落字后再动工）

1. **英文眉题**：顶部小字大写宽字距，概括主题（如 "EARLY WIN IS BAIT"），可配中文副题一行（Eyebrow组件双语）；
2. **白色引导行**：语境句6-10字（如"AI手搓的早期成功"）；
3. **特大强调kicker**：一个词3-6字超大粗黑（如"是个诱饵"），字符高≈画布高16-18%——**语义色四选一**：金#F5C518默认/金钱结论，红#E04545负面质疑否定，蓝#3B82F6科技品牌，绿#22C55E开源赚钱正面（紫在81张实证中几乎不用）；
4. **高亮条/贴纸**：黄底黑字条或红/绿tag一句副信息（如"该撞的墙我都撞了"）；右上角可加贴纸章（StampRed，密度填充四角）；
5. **底部英文脚注**：品牌行 "LAOHAN AI · CASE FILES NO.XX" 式小字宽字距。
6. **品牌chip卡**（左上，眉题下方）：圆角描边小卡"老韩AI | LAOHAN.AI · CASE 01"。
7. **标题栈左对齐**（align=left，left_x≈64）：对齐原版下部大字块的左对齐排法，行距收紧。

## 三层执行管线（scripts/build_cover.py 一条命令，1080x1440）

- **层1 背景板**：**优先真实素材**（UI截图/产品实拍/主题实拍，bg_image）；Seedream仅作兜底（bg_prompt，1152x1536，**无文字无人脸**，出图复核有字即废）；背景prompt**禁止要求"大面积留白/empty negative space"**——原版是满构图四角有元素（无空白墙），不是留白海报；
- **层2 真人融入层**（三模式；**v5.1定案：`env_photo`是唯一正解**——Jeffrey拍板"抠像人像太假"，柱子哥抠的是"人+周围真实环境"整块，不是人形抠像）：
  - `env_photo`（**默认**）：从raw帧/摆拍裁"人+真实环境"矩形区（**永不抠像**）→压暗(brightness≈0.44-0.55)+降饱和+冷色罩→**脸部径向提亮（env_face_boost≈1.6-2.0，脸必须是人物区最亮焦点）**→**径向alpha罩（只人物区不透明，四周长距溶入黑暗，椭圆必须收在块内收完衰减）**→四边scrims辅助；
  - `integrated`（人形抠像，历史保留，已被Jeffrey否决为主路线）；`block_tr`（小窗照片块，已否决）。
  - **融入六法**（后期统一风格实证）：①真人层压暗后脸必须仍是全画布最亮主体；②躯干必须溶进黑暗/裁出画底，不许亮块悬浮；③勾边光色=背景光源色、光向一致；④文字压人物下身形成深度三明治；⑤粒子/烟雾补空隙且人物前后各一层；⑥亮背景素材禁用带环境宽裁切。
  - **比例红线（Jeffrey 2026-09-20）**：脸占画布高≈15-20%，人像整体近全高（env_height≈0.70）；脸占比超30%=比例严重不符。
  - **接缝教训链**：edge-feather 170px盖不住亮photo→4边scrim仍露调差→暗框自身成新矩形→**唯解=径向alpha罩长距溶黑（椭圆收在块内）+海报侧渐变压黑带+全局黑位压缩（black_point≈14-22）**。任何"硬边+局部修补"都会被看见。
- **层3 文字层（v6默认Remotion）**：`animation-method/runtime/cover/index.tsx`（LaohanCover 1080x1440，frame=120静帧）——已验收组件（Eyebrow/StampRed）+SEMANTIC语义色+**材质级kicker**（底层实色厚描边挤出投影/前层线性渐变填充+辉光，思源黑体Heavy）+黄条贴纸+chip卡+居中脚注；brief的`remotion`节传参（kicker_tone/kicker_size/stamp/text_top等）。**PIL平面文字仅作runtime缺失时的兜底**（--text-engine pil）；
- **层4 全局统一调色（final_grade）**：三层合成完→整图brightness/contrast/color+冷tint+暗角一次grade；
- 产出单张1080x1440(3:4)母版；不做三候选；不满意改标题组或视觉概念重出。

## 红线（violation=立即停）

1. 背景板prompt**禁止出现文字/字母/人脸**要求，出图后复核有字即废；
2. **禁止用AI生成人物**，人物必须是Jeffrey真实照片/真实帧；
3. **禁止生图渲染任何标题文字**（中英文都不行，错字率不可接受）；文字层只走Remotion/PIL代码渲染；
4. rembg/字体/runtime缺失先修复本体，不得降级绕路（PIL兜底仅在runtime物理缺失时）；
5. **env_photo源亮场平光素材**（预检FLAT_BRIGHT）不得硬上——先补拍或换raw暗帧；strict_light=true时机器直接拒绝。

## 与开场首帧的关系

⑥海报封面（本skill）与⑪成片开场hook是两件事都要做，共用钩子创意不共享图。封面文字层与正片HUD共用templates-v2组件库（同源设计语言）。

## 依赖声明

Remotion runtime（`animation-method/runtime`，全机唯一本地执行层，cover/子目录）+ 火山方舟API（ARK_API_KEY，仅Seedream兜底）+ `~/.venvs/cover`（rembg+onnxruntime+pillow）+ assets/fonts/SourceHanSansCN-Heavy.otf（SIL OFL可商用，cover/public/有一份供@font-face）+ ffmpeg（raw抽帧）。
