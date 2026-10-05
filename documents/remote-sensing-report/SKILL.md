---
name: remote-sensing-report
description: "Write or polish Chinese remote sensing experiment reports from a report template, experiment guide, and original screenshot evidence. Use this skill whenever the user asks to 整理、规整、润色或生成遥感实验报告、ENVI 实验报告、按模板生成 Word/PDF，尤其是用户提供模板、实验指南、老师数据和逐步截图时。Preserve the template, use only original images, write reproducible methods, use three-line tables, and emphasize thinking questions."
---

# Remote Sensing Experiment Report Skill

Use this skill to turn a Chinese remote sensing experiment guide plus a student's rough draft into a polished Word report. The report should look like a formal lab report, not a screenshot dump.

## Core Contract

Follow the user's newest constraints first. In the common workflow from this skill:

- Use the report template as the formatting authority.
- Use the experiment guide as the technical authority for objectives, steps, formulas, and thinking questions.
- Use the student's draft as the evidence/source for screenshots, intermediate outputs, and observed values.
- Preserve all user-supplied facts, formulas, thresholds, and image order unless the guide or draft clearly contradicts them.
- Do not invent experimental results. If a result is not shown in the draft or guide, describe the method and limitation instead.

When the user says images must come from the draft, treat that as strict:

- Use only images embedded in the draft document.
- Do not use Python, Pillow, OpenCV, or any bitmap tool to crop, enhance, resize, stitch, combine, annotate, recolor, compress manually, or make contact sheets.
- It is acceptable to set display width in Word so the original image fits the page; this is document layout, not image processing.
- For a comparison, place two separate original image objects side by side or one above the other in Word. Do not create a composite image file.
- Add captions only after understanding each image from the surrounding draft text and guide context.
- Verify final DOCX media hashes against the draft media when possible.

## Required Inputs

Expect some or all of these files:

- Report template: `.doc` or `.docx`, often named `实验报告模板.doc`.
- Experiment guide: usually `.pdf`, often named like `实验十一：彩色图像分割-1.pdf`.
- Draft: `.docx`, often named `草稿.docx`, containing rough notes and screenshots.
- Optional data folder: original images used in the experiment.

If a legacy `.doc` template is provided, convert it to `.docx` with Microsoft Word or LibreOffice before editing. Do not overwrite the original template.

## Report Structure

Match the template headings unless the user gives another structure. For the observed template, use:

1. `1．实验目的和内容`
2. `2．图像处理方法和流程`
3. `3．实验结果`
4. `4．结果分析与思考题`
5. `参考文献：`

If the template has slightly different heading names, keep the template's naming and numbering style.

## Formatting Rules

Use the template's format as the source of truth. For the observed template:

- Title centered.
- Level-1 headings: black bold Chinese heading style, left aligned.
- Body text: Songti/宋体, 小四 or template body style, 1.25x line spacing, first-line indent.
- Figures: caption below image, centered, bold, format `图N. Caption`.
- Tables: caption above table, centered, bold, format `表N. Caption`.
- Tables must be three-line tables: top rule, header bottom rule, bottom rule; no full grid unless the template explicitly requires it.
- Avoid wording like `点击...` in formal report prose. Say `打开`、`选择`、`设置`、`执行`、`生成` instead.
- Use Chinese punctuation and technical terms consistently.

## Image Handling Workflow

1. Extract embedded draft images from `word/media/`.
2. Parse the draft document order so each image is associated with its preceding and following text.
3. Interpret each image using both draft context and guide steps.
4. Insert original image files directly into the report.
5. Add accurate captions. Do not reuse uncertain auto-captions.
6. Put most process screenshots in `2．图像处理方法和流程`.
7. Put only selected final outputs in `3．实验结果`.
8. After saving, verify:
   - final report has the expected number of inline images;
   - all report media hashes match draft media hashes;
   - no generated composite/contact-sheet images are present.
   - side-by-side or top/bottom comparisons still reference two separate original media files.

Good captions identify the image's role, not just its filename.

Examples:

- `图1. DSCF0153.jpg 原始图像`
- `图2. DSCF0153.jpg 红色通道原始直方图`
- `图9. 天空掩膜 Band Math 表达式设置窗口`
- `图10. 天空二值掩膜结果，白色区域为被识别出的天空`
- `图25. 阈值 0.98 分割得到的娃娃前景掩膜 m2，白色为娃娃区域`

Avoid captions that misidentify intermediate outputs as final results.

## Content Standards

The report should be detailed enough that a peer can reproduce the experiment.

### Section 1: Purpose And Content

Write a concise but rich overview:

- experiment theme;
- data used;
- software environment;
- target methods, such as histogram thresholding, Band Math, masks, inverse masks, channel comparison, ratio operation;
- what each experiment demonstrates.

Include a data/task table when useful.

### Section 2: Image Processing Methods And Workflow

This is the most important section. It must be much more than a list of operations.

For each experiment, explain:

- why this method fits the image;
- what the target and background look like in RGB or grayscale channels;
- how thresholds or expressions are chosen;
- what each Band Math variable means;
- what each logical operator does;
- how the mask is interpreted;
- why inverse masks or channel synthesis are used;
- how to judge whether the result is reasonable;
- what errors may occur if the threshold is too high or too low.

Use the draft screenshots as visual evidence. Put parameter windows, histograms, masks, pixel-value samples, and intermediate outputs here.

### Section 3: Experimental Results

Do not repeat every process screenshot. Select representative final outputs:

- final sky-removal comparison;
- orchid extraction mask;
- doll final red-background or extracted foreground result;
- character final enhanced image.

Add a compact three-line evaluation table if helpful.

### Section 4: Analysis And Thinking Questions

Make the thinking questions prominent. For each question:

- restate the question;
- answer directly first;
- then explain mechanism and evidence from the experiment;
- mention limitations or conditions when relevant.

For this color segmentation experiment, expected reasoning includes:

- Removing bright sky reduces high-value background interference and improves ground feature visibility.
- Non-orchid extraction is `1-mask`, or `original image * (1-mask)` if preserving original colors.
- Ratio operation reduces illumination influence by comparing channel proportions; `0.98` comes from foreground/background samples in the ratio image.
- Thresholds like `200` and `100` come from channel grayscale observation and character/background sampling; they balance character integrity against noise suppression.

## Technical Pattern For DOCX Work

Prefer the `docx`/document workflow:

1. Convert `.doc` template to `.docx` if needed.
2. Load the template `.docx`.
3. Clear body content but preserve template styles, page margins, and usable heading/body styles.
4. Build the report programmatically with `python-docx` or targeted OOXML editing.
5. Use original draft media files directly.
6. Save as a new `.docx`; never overwrite the user's draft or template.
7. Export or render a preview when possible.

If using a script, keep it in the workspace and make its behavior auditable:

- no image processing functions for draft images;
- only insert existing media paths;
- no generated panel/contact-sheet image insertion;
- hash verification for report media vs draft media.

## Verification Checklist

Before final delivery, check:

- The final DOCX opens and can export/render.
- The report uses the template's page/style conventions.
- `2．图像处理方法和流程` is detailed and explanatory, not just step labels.
- All embedded images are original draft images if required.
- Figure captions match actual image meaning and context.
- Tables are three-line tables.
- Results section contains selected final outputs rather than all screenshots.
- Thinking questions are easy to find and answered deeply.
- There is no `点击`-style informal operation wording unless quoting the guide.
- References are cited in the body if a references section is included.

## Common Pitfalls

- Do not create composite figures unless the user explicitly allows image processing.
- Do not use contact sheets in the final report.
- Do not treat a Band Math setup screenshot as a segmentation result.
- Do not label an inverse mask as the positive target mask.
- Do not put every final output only in `实验结果`; process images belong mainly in `方法和流程`.
- Do not underwrite Section 2. The workflow section is graded for reproducibility and explanation.
- Do not silently change thresholds or formulas from the guide/draft.

## Useful Validation Snippets

Media hash validation concept:

```python
import hashlib, zipfile

def media_hashes(docx_path):
    with zipfile.ZipFile(docx_path) as z:
        return {
            hashlib.sha256(z.read(n)).hexdigest(): n
            for n in z.namelist()
            if n.startswith("word/media/") and not n.endswith("/")
        }

draft_hashes = media_hashes("草稿.docx")
report_hashes = media_hashes("final_report.docx")
unmatched = [h for h in report_hashes if h not in draft_hashes]
assert not unmatched
```

Use this idea when the user requires original draft images only.
