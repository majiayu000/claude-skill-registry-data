---
name: resume-parser
description: 智能简历解析系统，支持PDF/Word/图片格式简历的结构化信息提取、岗位匹配度分析、优化建议生成。完全本地运行，无需外部API。使用场景：(1)
  解析上传的简历文件提取核心信息，(2) 输入岗位JD计算简历匹配度，(3) 生成简历优化建议，(4) 导出结构化简历数据。
---

# 智能简历解析系统 Skill

## 核心功能
1. **多格式支持**：PDF (.pdf)、Word (.docx/.doc)、图片 (.jpg/.png/.webp) 格式简历解析
2. **信息提取**：自动识别并提取以下核心信息：
   - 个人基本信息（姓名、电话、邮箱、年龄、性别、所在地）
   - 教育经历（学校、专业、学历、起止时间、GPA、相关课程）
   - 工作经历（公司名称、职位、起止时间、工作内容、业绩成果）
   - 项目经历（项目名称、角色、起止时间、项目描述、技术栈、成果）
   - 技能栈（编程语言、框架、工具、软技能、语言能力）
   - 证书、获奖经历、自我评价
3. **匹配度分析**：输入岗位JD后自动计算简历匹配度，从技能匹配、经验匹配、学历匹配等多维度打分
4. **优化建议**：针对简历不足生成具体优化建议，包括内容补充、表述优化、结构调整
5. **数据导出**：支持JSON/Markdown格式导出结构化简历数据

## 工作流程
1. 当用户上传简历文件或提供简历路径时，先调用对应解析脚本提取文本内容
2. 将提取的文本传入大模型进行结构化信息提取，输出标准JSON格式
3. 如果用户提供了岗位JD，按照以下严格规则进行匹配度分析：
   - **第一步：先区分JD中的「核心要求」和「加分要求」**：核心要求占比80%权重，加分要求占20%
   - **第二步：严格匹配核心要求**：核心要求只要有一项不满足，整体评分上限不超过60分；2项及以上不满足，上限不超过40分
   - **第三步：加权计算总分**：严格按照各维度权重计算，禁止主观加分
   - **第四步：客观说明匹配情况**：必须明确说明「完全匹配/基本匹配/不匹配」，禁止模糊表述
4. 最终返回结构化结果 + 严格的分析报告 + 可落地优化建议

## 匹配度评分严格规则
1. **90-100分：完全匹配**：所有核心要求100%满足，加分要求满足80%以上，有超出要求的亮点
2. **70-89分：基本匹配**：核心要求全部满足，加分要求满足50%以上，无明显核心短板
3. **60-69分：勉强匹配**：核心要求基本满足，有1项非关键核心要求不满足，加分要求满足30%以上，可以进入面试
4. **<60分：不匹配**：核心要求有2项及以上不满足，或有1项关键核心要求不满足，不符合岗位基本要求

## 核心要求判定规则
- 岗位JD中明确标注「必须」「要求」「需具备」的技能/经验
- 岗位名称对应的核心能力（如AI算法岗必须懂深度学习，后端岗必须懂编程语言）
- 明确的工作年限、学历要求

## 脚本使用
### 1. PDF文本提取
```bash
python scripts/extract_pdf.py <input-pdf-path>
```
返回纯文本内容

### 2. Word文本提取
```bash
python scripts/extract_docx.py <input-docx-path>
```
返回纯文本内容

### 3. 图片OCR提取
```bash
python scripts/extract_image.py <input-image-path>
```
返回OCR识别的文本内容

### 4. 结构化解析
```bash
python scripts/parse_resume.py <extracted-text-file>
```
返回结构化JSON数据

### 5. 匹配度分析
```bash
python scripts/match_jd.py <resume-json-path> <jd-text-path>
```
返回匹配度分析结果

## 输出格式规范
### 结构化简历JSON格式
```json
{
  "basic_info": {
    "name": "",
    "phone": "",
    "email": "",
    "age": null,
    "gender": "",
    "location": "",
    "work_years": null
  },
  "education": [
    {
      "school": "",
      "major": "",
      "degree": "",
      "start_date": "",
      "end_date": "",
      "gpa": "",
      "courses": []
    }
  ],
  "work_experience": [
    {
      "company": "",
      "position": "",
      "start_date": "",
      "end_date": "",
      "description": "",
      "achievements": [],
      "technologies": []
    }
  ],
  "projects": [
    {
      "name": "",
      "role": "",
      "start_date": "",
      "end_date": "",
      "description": "",
      "technologies": [],
      "achievements": []
    }
  ],
  "skills": {
    "technical": [],
    "soft": [],
    "languages": []
  },
  "certificates": [],
  "awards": [],
  "self_assessment": ""
}
```

### 匹配度分析格式
```json
{
  "overall_score": 0-100,
  "dimensions": [
    {
      "name": "核心技能匹配",
      "score": 0-100,
      "weight": 0.4,
      "matched": ["匹配的核心技能列表"],
      "missing": ["缺失的核心技能列表"],
      "analysis": "详细分析说明"
    },
    {
      "name": "岗位职责匹配",
      "score": 0-100,
      "weight": 0.3,
      "matched": ["匹配的职责经验"],
      "gap": "职责差距描述",
      "analysis": "详细分析说明"
    },
    {
      "name": "经验/资历匹配",
      "score": 0-100,
      "weight": 0.15,
      "matched": ["匹配的经验点"],
      "gap": "经验差距描述",
      "analysis": "详细分析说明"
    },
    {
      "name": "学历/背景匹配",
      "score": 0-100,
      "weight": 0.15,
      "matched": "匹配结果描述",
      "gap": "背景差距描述（如果有）",
      "analysis": "详细分析说明"
    }
  ],
  "overall_analysis": "整体匹配情况总结，明确说明是否匹配",
  "strengths": ["简历优势列表"],
  "weaknesses": ["简历不足列表，必须明确核心差距"],
  "suggestions": ["具体的优化建议列表"]
}
```

## 依赖安装
首次使用前安装依赖：
```bash
pip install PyPDF2 python-docx pytesseract pillow python-multipart
```
*注意：OCR功能需要安装Tesseract引擎*
