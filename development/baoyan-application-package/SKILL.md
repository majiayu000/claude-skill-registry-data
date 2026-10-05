---
name: baoyan-application-package
description: Create, rebuild, standardize, and visually QA Chinese 保研/推免/夏令营/预推免 application material packages from multiple PDF files. Use when Codex needs to inventory a folder of application PDFs, choose and reorder materials, obtain a school logo, generate a school-specific cover and contents page, normalize pages to A4, add PDF bookmarks and page-number labels, satisfy upload limits, or run the bundled configurable package builder.
---

# 保研资料包制作

把零散 PDF 整理成一份结构清楚、版式统一、可直接检查和上传的学校专项资料包。普通用户不需要自己编写 JSON；优先由 Codex 盘点文件并生成配置。

## 先判断任务类型

### A. 从文件夹新建资料包

读取申请学校要求和材料文件夹，自动完成盘点、排序、配置、生成和检查。

### B. 改造已有合并 PDF

保留原材料内容，增加封面、目录、书签和资料包页码；必要时重排页面和统一尺寸。

### C. 制作限页或限大小版本

先依据学校规则筛选和压缩材料，再生成目录。不得生成完整版后假定系统能够接受。

### D. 手动运行脚本

用户已经准备配置文件时，使用内置脚本生成。

## 最少输入

尽量从工作区和学校通知中自动提取：

- 目标学校和申请学院或方向。
- 官方校徽、校标或官网页面。
- 申请人姓名、本科院校和专业。
- PDF 材料文件夹或已有合并 PDF。
- 学校要求的材料、顺序、页数和文件大小限制。

学校要求不明确时可以先制作样版，但必须标出尚未核对的限制。

## 第一步：盘点材料

列出所有候选 PDF，并归入以下分类：

1. 个人材料：中英文简历、个人陈述。
2. 学业与身份：成绩单、排名、GPA、英语、在读证明、身份证、学生证。
3. 科研与知识产权：论文或项目摘要、模型图、专利、软著、结题证明。
4. 竞赛与实践：竞赛证书、调研或实践证明。
5. 荣誉奖励：奖学金、三好学生等。

不要把文件夹中所有 PDF 无差别合并。优先服从学校清单和上传限制。

## 第二步：确认视觉信息

- 优先从学校官网获取校徽或中英校标。
- 使用学校主色。
- 记录校标来源，避免使用来路不明或低清图片。
- 多个学院共用一份资料包时，封面并列写申请方向，不擅自选择一个。

## 第三步：确定顺序和目录

- 封面为第 1 页，目录为第 2 页。
- 正文默认按“个人—学业身份—科研—竞赛实践—荣誉”排序。
- 学校指定顺序时服从学校。
- 目录中的页码必须根据最终物理页码自动计算。
- 不创建空分类。

## 第四步：生成

普通用户模式：

1. 复制 [assets/package-config.example.json](assets/package-config.example.json) 到工作目录。
2. 根据盘点结果由 Codex 填写学校、申请人和材料路径。
3. 运行相对本 Skill 的 `scripts/build_package.py`。

命令行模式：

```powershell
python "scripts\build_package.py" --config "C:\path\package-config.json"
```

配置字段见 [references/config-schema.md](references/config-schema.md)，版式标准见 [references/format-spec.md](references/format-spec.md)。

## 固定成品标准

- A4 纵向封面，包含官方校标、学校名称、资料包标题和申请人信息。
- 第二页为目录，不写底部说明。
- 正文全部放入 A4 画布，等比例居中，不裁切、不拉伸。
- 横向证明材料保持方向，缩放后居中。
- 添加封面、目录和各一级分类书签。
- 每页底部居中显示 `01 / 34` 格式页码，包括封面和目录。
- 新页码不加横线，不覆盖原文。
- 原 PDF 内容、签章和证件信息不得重排或重绘。

## 第五步：视觉检查

必须渲染并查看：

- 封面。
- 目录。
- 第一正文页。
- 最后一页。

还要抽检：

- 横向页面。
- 成绩单和扫描证书。
- 身份证、学生证等页面；只做必要检查，不在最终答复中公开展示。

检查校标清晰度、中文乱码、目录溢出、裁切、拉伸、页码遮挡和书签目标。

## 第六步：自动验证

不得交付验证失败的文件。确认：

- 总页数正确。
- 每页均为 A4。
- 每页都有对应的 `当前页 / 总页数`。
- 目录范围和书签目标正确。
- 输出 PDF 可以正常打开。

## 输出与清理

- 有工作区时写入工作区的 `output/pdf/`。
- 无工作区时写入用户文档目录下的 `Codex` 文件夹。
- 文件名使用 `学校名称+资料包类型_姓名_版本.pdf`。
- 删除失败下载、临时渲染和过时草稿。
- 保留最终 PDF、必要预览、当前配置和可复用脚本。

## 默认交付

- 最终资料包 PDF。
- 封面和目录预览。
- 材料顺序或目录摘要。
- 页数、书签和自动验证结果。
- 尚未核对的学校限制；没有风险时不额外制造问题。
