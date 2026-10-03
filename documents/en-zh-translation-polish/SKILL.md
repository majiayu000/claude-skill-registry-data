---
name: en-zh-translation-polish
description: Translate English passages into natural Chinese or polish Chinese translations against the source; supports bilingual output.
license: MIT
allowed-tools: Read Write Edit Bash
metadata:
  version: 1.1.0
  tags: [translation, chinese, english-to-chinese, 英译汉, 润色, 中英对照, localization]
---

# 英译汉翻译润色 (English→Chinese Translate & Polish)

把英文译成**地道中文**并产出**英中对照**译文。核心信条（叶子南）：英译汉最致命的错误是把英语的“形合”结构迁移进汉语造成翻译腔；好译文 = **以读者为中心、按文本类型调节归化尺度、发挥汉语意合优势、兼顾音韵节奏**。

## 按请求选择交付与检查范围

聊天中的短段落翻译直接在回复中交付，用户要求文件时才落盘；全文或项目翻译沿用下述默认文件契约。用户明确选择纯译文、双语或已有目标文件时按其要求，不重复确认。先保留数字、术语、引文与限定条件，再按文体选择必要的润色检查；短文本不必逐项展示诊断过程或通读所有参考表。研究论文、文学和正式文件的专项边界继续适用。

## 独立使用与文档输入

本技能可独立安装使用，无需额外安装其他翻译技能。输入为 PDF 或其他文档时，先使用当前宿主可用的读取工具获取原文；保留用户要求的正文、图表说明、公式、引文和参考文献。无法可靠提取的内容应说明缺口，不将翻译任务转交给用户未安装的技能。

## 交付物

默认产出**一个**英中对照 Markdown 文件；用户要“全中文版”时再脚本派生。

1. **`<名称> 翻译(中英对照).md`** — 唯一真源。每段**英文原文作为 blockquote (`> `)**，紧跟其下是中文译文。
2. （按需）**`<名称> 翻译(全中文).md`** — 脱离对照文件**用脚本机械派生**（删掉 `> ` 行），不要重打中文。
   ```bash
   python3 - "<名称> 翻译(中英对照).md" "<名称> 翻译(全中文).md" <<'PY'
   import sys, re
   src, dst = sys.argv[1], sys.argv[2]
   lines = open(src, encoding='utf-8').read().split('\n')
   kept = [ln for ln in lines if not ln.lstrip().startswith('>')]
   open(dst,'w',encoding='utf-8').write(re.sub(r'\n{3,}','\n\n','\n'.join(kept)).strip()+'\n')
   PY
   ```
   > 顺序要求：**先跑阶段 6 的标点归一，再派生全中文版**——派生脚本原样继承标点，不会再纠正。

若输入只是聊天里的一小段（几句话），直接在回复里给对照即可，不必落盘；成篇文章或用户指明保存才写文件。命名沿用源文件名，无工具前缀（除非用户要）。目标文件已存在则更新而非新建。

## 工作流（严格按序；每段译文都要走完润色，不是初译就交）

### 阶段 0 — 文本分析：定归化档位 ★必做第一步
先回答：**这是硬文本还是软文本？属纽马克哪一类？自由度大致几分(1–10)？** 详见 `reference/text-analysis-and-qa.md` 小节 A。

- **偏硬（自由度 1–3）**：政治/法律/经贸/科技/合同/说明书。→ 贴原文逻辑，选词精准，**准确 > 流畅**，少介入，术语用固定译法。某些“西化”是为精确付的合理代价。
- **偏中 (4–6)**：教科书/新闻/一般论述。→ 平衡，默认交际翻译。
- **偏软 (7–9)**：文学/散文/评论/讲演/广告/宣传/营销。→ 大胆发挥意合与汉语之美，可调结构、可换形象，**流畅/效果优先**。
- 别忘**文本外因素**：翻译目的、读者是谁。档位一句话写进给用户的说明里。

### 阶段 1 — 理解 → 脱离语言外壳
读懂原文后，**抛开英文词句**，在脑中形成意义/图像，再用中文重构（不要在词面上挪移）。遇到结构纠缠的短语用“解包袱法”理清隐含语义关系（见 `reference/techniques.md`）。

### 阶段 2 — 按档位初译
以**意合优先**起译：能不用连接词就不用，长句拆成流水短句，被动转主动，定语别堆在名词前。

### 阶段 3 — 润色诊断（核心）逐段过三张表
1. **翻译腔病症** — 对照 `reference/translationese-symptoms.md` 逐条排查并修：形合迁移/连接词冗余、长前置定语、“的的不休”、被动滥用、抽象名词作主语、习语硬译、语义关系隐含不清。
2. **技巧库** — 用 `reference/techniques.md` 的手段修：词性转换、增/减词、分句/合句、语序移位、定语从句转状语/独立句、正反译、被动转化。
3. **隐喻决策** — 基本/图像图式隐喻（旅程、大小、冷热…）可直译；文化专属隐喻糅合或舍弃；直译≠应直译，看档位（`reference/text-analysis-and-qa.md` 小节 B）。

### 阶段 4 — 音韵节奏打磨
读出声。利用双音节/四字结构、“偶字易适奇字难平”、对偶排比；并列词组尽量配偶字（“飞机小，便宜”→“体积不大，造价便宜”）。**但软文本才放开；硬文本点到为止。**

### 阶段 5 — 准确性质检
对照 `reference/text-analysis-and-qa.md` 小节 C 逐项核：擅自改结构/移焦点、漏译情态虚词、擅自添词、搭配、指代、逻辑关系、专名术语数字、语域对齐。
> 红线：放松准确性 ≠ 理解错误。理解错误没有原谅的余地。

### 阶段 6 — 中文标点规范化 ★（机械执行，落盘后必跑）
中文译文里的标点必须是中文全角，不能残留英文半角（译者最易忽略，逐字凭眼力一定会漏）。规则：
- `, : ; ? !` → `，：；？！`；句末用 `。`；并列用顿号 `、`；破折号 `——`；省略号 `……`。
- 圆括号 `( )` → 全角 `（ ）`：**仅当紧邻中文字符时才转**（包裹中文内容、含人名/术语原文注，如 "道德受体地位(moral patienthood)"）；纯英文括注（如电影演职 `(Harold D. Schuster, 1937)`）保持半角。
- 双引号统一为中文全角 `" "`（内层 `' '`）；直角引号 `「」`、`『』` 一并归一为 `" "` / `' '`。

**以下一律保持半角，绝不转：** ① 英文原文 blockquote（`> ` 行）整段不动；② Markdown 链接 `[文字](url)` 的括号与 URL；③ 中文行内嵌入的整句/词组英文，其内部标点——如被引用的英文原句 `…one nation under God, indivisible, …`；④ 数字/缩写/版本号里的点：`4.3`、`Word 2010`、`A.I.`、`L. M.`；⑤ 代码/公式块。

判定原理：**逗号类与圆括号都只在紧邻中文字符（前或后）时才转**；有方向的引号（“”「」‘’『』）按方向直接映射，只有歧义的直双引号 `"` 才靠交替判定开闭。落盘后跑下面脚本机械归一并自检（`残留` 必须为 0）：

```bash
python3 - "<名称> 翻译(中英对照).md" <<'PY'
import re, sys
src = sys.argv[1]
lines = open(src, encoding='utf-8').read().split('\n')
CJK_EXTRA = set('“”‘’·—…《》〈〉「」『』【】、。，！？；：（）')
def is_cjk(c):
    if not c: return False
    o = ord(c)
    return (0x3400<=o<=0x9fff) or (0x3000<=o<=0x303f) or (0xff00<=o<=0xffef) or (c in CJK_EXTRA)
SMAP = {',':'，', ';':'；', ':':'：', '?':'？', '!':'！', '(':'（', ')':'）'}
OPEN2 = '“「'; CLOSE2 = '”」'; OPEN1 = '‘『'; CLOSE1 = '’』'
LINK = re.compile(r'\[[^\]]*\]\([^)]*\)')
def fix(line):
    store=[]
    line = LINK.sub(lambda m: store.append(m.group(0)) or '\x00%d\x00'%(len(store)-1), line)
    out=[]; sop=True                     # 有方向引号直接映射; 仅歧义直双引号 " 靠交替定开闭
    for c in line:
        if c == '"': out.append('“' if sop else '”'); sop = not sop
        elif c in OPEN2: out.append('“')
        elif c in CLOSE2: out.append('”')
        elif c in OPEN1: out.append('‘')
        elif c in CLOSE1: out.append('’')
        else: out.append(c)
    ch=out; n=len(ch)
    for i,c in enumerate(ch):            # 逗号类 + 圆括号: 紧邻中文才转全角
        if c in SMAP and (is_cjk(ch[i-1] if i else '') or is_cjk(ch[i+1] if i+1<n else '')):
            ch[i]=SMAP[c]
    line=''.join(ch)
    return re.sub('\x00(\\d+)\x00', lambda m: store[int(m.group(1))], line)
def skip(ln):
    s=ln.strip(); return s=='' or ln.lstrip().startswith('>') or s=='---'
res=[ln if skip(ln) else fix(ln) for ln in lines]
open(src,'w',encoding='utf-8').write('\n'.join(res))
def residual(ln):
    t = LINK.sub('', ln)                # 排除 markdown 链接内的括号/标点, 免误报
    return sum(1 for m in re.finditer(r'[,;:?!()]', t)
               if is_cjk(t[m.start()-1] if m.start() else '') or is_cjk(t[m.start()+1] if m.start()+1<len(t) else ''))
bad=sum(residual(ln) for ln in res if not skip(ln))
print('残留:', bad)
PY
```
聊天里直接给的小段对照（未落盘）同样要手动套用上述规则。

### 阶段 7 — 输出英中对照
按下方格式逐段配对；成篇则写文件；给用户附一句“档位判定 + 主要润色取舍”。

## 英中对照输出格式

**按段落配对**：英文原段作为 blockquote，紧接中文译文。

```markdown
> It is a truth universally acknowledged that a single man in possession of a
> good fortune must be in want of a wife.

凡是有钱的单身汉，总想娶位太太，这是一条举世公认的真理。
```

规则：
- 中文译文用中文全角标点；半角标点只留给英文原文、链接、行内英文词句、数字缩写、代码（详见阶段 6，落盘后用脚本自检）。
- 只清理提取噪声（接回断行连字符、删页眉页脚页码），**不要**从中文反推英文。
- 标题作中文 `##`/`###`，不加 blockquote；可选地把英文标题作为上一行 blockquote。
- 不该被脚本删掉、需保留进全中文版的东西（图片、表格、标题块）**不要** blockquote。
- 公式/代码用共享代码块，不按语言重复。

## 润色边界 ★（防止方法论被用过头）

叶子南本人警告的两个反模式，务必守住：
- **不要过度归化**：别为了“地道”抹掉原文该保留的风格、术语精度、文化标记。西化是一个**连续体**，可接受度随文本价值变化——硬文本/永久价值文本能容纳更多异化（见 `reference/translationese-symptoms.md` 第七节）。
- **不要堆砌四字成语**：音韵节奏是手段不是目的，为文字而文字会显得卖弄、失真。
- 拿不准“该改到多狠”时，回到阶段 0 的档位：**自由度越低，越克制**。

## 示例

输入（英文）：

```
The confidence that the West would remain a dominant force in the 21st century is giving way to a sense of foreboding.
```

输出（英中对照；阶段 0 判定：偏硬／政论，自由度≈3，准确优先、克制音韵）：

> The confidence that the West would remain a dominant force in the 21st century is giving way to a sense of foreboding.

西方曾笃信自己将在 21 世纪稳居主导地位，如今这份自信，正让位于一种隐隐的不祥之感。

## 致谢与许可

本 skill 的代码、提示词与组织方式以 **MIT 许可**发布，可自由使用、修改、再分发。

方法论与判例蒸馏、转述自叶子南《高级英汉翻译理论与实践》（第4版，清华大学出版社，2020），在此谨致谢忱。`reference/` 三张表中的少量引文系评注与教学目的的简短摘引，著作权归原作者与出版社所有；本 skill 仅为方法工具，不能替代原著，建议系统学习者购买正版。
