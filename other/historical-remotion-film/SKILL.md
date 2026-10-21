---
name: historical-remotion-film
description: Produce or iterate Remotion films about historical art, museum collections, ancient paintings, and cultural motifs, covering source fidelity, evidence wording, cinematic motion, and original foley. Only for this kind of Remotion film; not for generic web animation, general editing, or historical research.
version: 1.0.2
---

# 历史艺术 Remotion 影片

从观众看到和听到的结果设计镜头；把史料、艺术解释与制作方法分开。沿用已有项目、素材与时间线，先找出最破坏观感的具体问题再迭代。

## 按任务读资料

- 选古画、藏品或改知识文案：读 [史料与观众文案](references/evidence-and-copy.md)。
- 改龙形、器物、美术、粒子或转场：读 [镜头与画面](references/art-and-motion.md)。
- 加画卷、墨滴、金石等声音：读 [原创拟音](references/foley.md)。
- 交付作品与工程、保存素材：读 [双目录归档](references/archive.md)。

## 核心判断

1. 历史图像的真实轮廓优先。裁切、抠像、光扫不能把原作纹理改成新造的“史料”。
2. 画面文字只承担片名、知识、问题、必要来源。展开方向、算法、版本名、构图意图放工程说明，不塞进观众画面。
3. 厚重感来自构图、尺度、缓慢蓄势和细节层次；颗粒、发光和粒子要服务主体，不能以数量替代设计。
4. 古画动画、程序拟音都是当代解释；不要称为历史现场或古物原声。
5. 交付时区分已检查的范围与审美判断。抽帧检查不等于逐帧视觉验收，技术通过也不等于导演层面的完成。

Remotion API 与预览/渲染参数以本机官方 `remotion-best-practices` 和当前依赖版本为准；不为了套用此技能重建项目或升级依赖。只有本次工作需要的参考资料才读取。

## Example

Bad caption, because evidence and interpretation are fused:

> 此画创作于开元盛世，体现了盛唐气象。

Good caption, because the viewer can tell which part is fact:

> 画作：传唐·佚名（馆藏编号 X，断代有争议）。
> 画面：青绿设色，山石以勾勒填色为主。
> 我们的处理：镜头沿山势推进，配金石拟音，不作断代表述。

Same frame, but nothing in it can be challenged as a false claim.
