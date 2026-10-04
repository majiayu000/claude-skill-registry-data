---
name: md2view
description: |
  Re-encode a Markdown document into a traceable human-reading view: a single-file HTML with the original on the left and a model-designed visual re-organization on the right (architecture diagrams, flow chains, comparison matrices, argument maps, annotated cards), where every element carries data-sources anchors back to the source, visible text keeps lexical anchors and numbers are copied verbatim. Use when the user wants a retrospective, report, spec, README or long technical document turned into something easier to absorb and share, or says /md2view, md2view, 信息重组, 双栏阅读, 文档可视化, 把文档做成图. Do not use for plain faithful Markdown rendering.

---

# md2view

把 Markdown 重新编码成可独立阅读、可回原文核证的视觉阅读器。产物是单文件 `reader.html`:左栏权威原文,右栏信息重组,点击任意元素双向定位。

## 第一性原理

这个产品的价值链分工是:

| 环节 | 谁做 | 为什么 |
| --- | --- | --- |
| 理解文章、判断什么值得表达 | 模型 | 只有模型能读 |
| 设计表达形式(图/表/卡/散文)与视觉节奏 | 模型 | 设计判断不可形式化;模板渲染只会产出"两框一箭头"的机械图 |
| 写右栏 HTML | 模型 | 自由创作才能好看;但必须带着锚点写 |
| 左栏原文渲染、双栏联动、壳 | 确定性脚本 | 忠实与一致不由模型负责 |
| 溯源验证(覆盖/锚点/数字) | 确定性脚本 | 可核证性是机器问题 |
| 表达质量 | **模型亲眼截图自审** | 看不见自己作品的设计师不可能及格 |

历史的失败模式(v3)是把第 2、3 环交给确定性模板、把第 6 环删掉——门禁全过,表达全废。v4 的纪律只有一句话:**形式自由,锚点强制,自审闭环**。

## 执行流程

下文 `$SK` 是本 skill 的实际安装目录。为任务建立独立工作目录。

### 1. 解析来源(确定性)

```bash
python3 $SK/scripts/parse_blocks.py input.md blocks.json
```

`blocks.json` 是来源账本:每块有稳定 id(`b000`…);表格数据行与 checkbox 项有原子 id(`b030:r001`、`b038:i001`)。heading 与 `---` 分隔线不要求投影,其余每个 block 都必须被右栏引用。

### 2. 通读全文,先判断再动手(模型)

读完原文后先回答(写在工作笔记里,不用落盘成 JSON):

- 谁读?读完 5 秒后应形成什么判断?
- 全文真正的命题有几条?哪些是主关系,哪些是证据?
- **每块内容配什么载体**:图(关系是真的)、表(选项×维度)、卡(并列要点)、步骤条(阶段推进)、标注条(风险/约束/决策)、还是纯散文(不值得视觉化的内容允许是散文——但散文也要带锚点)?
- 视图序列怎么排(全局 → 机制 → 证据/取舍 → 决策 → 行动 → 验证)?一个视图只回答一个问题;若只是原文章节换皮,合并或删除。

**构图合同(信息图形态,不是文档形态):**

- 右栏是 6–10 个独立视觉场景(默认折叠的附录不计入),每个在 1440 下约一屏,最多 1.5 屏。
- 每个场景有一个主视觉焦点:一张图、一条链,或一张"本身就是主角"的决策表。图/链占场景高度 ≥50% 是常态。
- **明细默认进抽屉**:大行数表格、字段清单、验收细目、长规则列表,放进 `<details class="mv-drawer">`;附录级内容放 `<details class="mv-appendix">`。抽屉内容照常带锚点,点击溯源时壳会自动展开。
- `<details>`/`<summary>` 是结构容器,**不带** `data-sources`;抽屉标题是导航标签,不是来源断言。
- 不为过审把内容全塞进抽屉:验证器会列出"只在抽屉里被引用"的 block,核心命题必须留在主视觉。

不得从"这里能放几张卡片"倒推语义;不得按 block 顺序做"逐段取证"。

### 3. 自由创作 right-pane.html(模型)

右栏是一个 HTML 片段:`<header class="mv-page-head">` 开场 + 若干 `<section class="mv-view">`。用 `references/design-system.md` 的组件词汇(`mv-*` 类)与 design token 组合;图的画法见 `references/diagram-cookbook.md`。允许为单张图写 scoped `<style>`(选择器必须以 `#视图id` 开头),禁止脚本、外部资源、隐藏文字的 CSS。

硬性纪律只有三条:

1. **每个承载内容的元素都带 `data-sources="b005 b006"`**(可选 `data-unit="b030:r002"` 精确认领表格行)。纯装饰容器不带。
2. **可见文本与每个被引 block 共享至少一个实义词锚**(≥3 字中文窗口,或两个 2 字窗口,或一个拉丁词)。可以概括,不能完全换词后只挂 id。
3. **数字逐字抄录**:元素里的每个阿拉伯数字必须出现在被引 block 原文里(`35`、`0.82.x`、`≥80%`),不心算、不换算、不新造。
4. **数字关系必须成立**:并排成算式或比例的数字,算术上必须真成立(35+13 ≠ 53 就不许写成"35+13");发现源文口径本身矛盾时,按源文原样表述并可注"待校准",不得把矛盾升级成 Hero 结论。验证器只保证"数字抄对",关系成立靠生产者自查。

第 2 条防换词,**防不住添加**。每个形容词、每个关系断言、每个"横切/唯一/首选"都要过一遍"源文说了吗"。这是生产者纪律,验证器兜不住。

### 4. 溯源验证(确定性)

```bash
python3 $SK/scripts/verify_anchors.py blocks.json right-pane.html
```

FAIL 时逐条修:补引用、补词锚、把数字改回原文写法。**不得**为过门把有来源的内容删掉或把数字改成无来源的约数;源文只有概数时就写概数。

### 5. 构建(确定性,验证不过不产出)

```bash
python3 $SK/scripts/build_reader.py blocks.json right-pane.html reader.html
```

### 6. 截图自审,至少两轮(模型,强制)

用浏览器(shot.js 或 chrome-devtools/playwright)在 1440 与 768 各截图,**亲眼看完每一屏**,写几句自评,修改,再来一轮。每轮先跑构图尺(在打开的页面上执行 `scripts/measure.js` 内容):总屏数、每个视图的屏数 / 主视觉占比 / 抽屉外表格数。审什么:

- 形态:每个场景约一屏、一个焦点;主视觉占比低的场景是不是把表格又铺回了主视觉?
- 5 秒测试:遮住说明文字,只看节点标题、位置、容器、连线,能否复述主结构?
- 连线不穿字、不穿容器、不压标签;同向双边加双向标签合并为一根;长链不散。
- 密度:没有大空白孤卡,没有句子密度冒充结构密度;信息按主次分区。
- 表格行完整;高亮(主路径/主对象)有且只有一处重点。
- 768 不横向溢出;双栏/原文/重组三模式可用;点右栏元素左栏滚动高亮;点左栏抽屉内源块,右栏抽屉自动展开并定位。
- 交互必须用**真实点击**验证(playwright `locator.click()` / chrome-devtools 真点):`el.click()` / `dispatchEvent` 不是可信激活事件,`<details>` 开合这类原生行为测不出来;浏览器有缓存,改完壳要禁缓存强刷再测。

未亲眼看过截图就交付 = 未完成。

## 返回前自检

- 右栏脱离原文能否回答:是什么、为什么、约束/取舍、如何行动或判断?
- 每个 `data-sources` 里的 block 是否真被该元素的可见文本锚住,还是"挂个 id 装溯源"?
- 每张图是否值得画?遮住图注后图本身是否还能读出主关系?不值得画的内容是否老实地写成了散文/表格?
- 有没有为了过验证删掉已取证内容、编造源文没有的关系(层级说成横切、并列说成因果)?
- 是否至少两轮截图自审,且第二轮真的改了东西?

## 对抗回归

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s $SK/scripts -p 'test_*.py'
```

反模式目录:`references/anti-patterns.md`(含 v3 时代的真实失败截图描述)。
