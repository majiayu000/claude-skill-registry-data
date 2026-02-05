---
name: zhongyi-rules
description: Mandatory rules for the zhongyi TCM system. ALWAYS follow these rules when writing any code, templates, or content. Includes bilingual display requirements, Chinese-first format, and other project standards.
---

# Zhongyi Project Mandatory Rules

**IMPORTANT**: These rules are MANDATORY and must be followed for ALL code, templates, and content in this project.

---

## Rule 1: Bilingual Display (双语显示)

**ALL user-facing text MUST be bilingual with Chinese FIRST, English second.**

### Format: `中文 | English`

### Examples

#### In Templates (HTML):
```html
<!-- Correct -->
<h2>处方管理 | Prescriptions</h2>
<th>患者 | Patient</th>
<button>保存 | Save</button>
<a href="#">新建 | New</a>

<!-- Incorrect - English first -->
<h2>Prescriptions | 处方管理</h2>

<!-- Incorrect - Missing translation -->
<h2>Prescriptions</h2>
```

#### In Django Models:
```python
# Correct
name = models.CharField(_('名称 | Name'), max_length=200)
status = models.CharField(_('状态 | Status'), max_length=20)

# For TextChoices
class Status(models.TextChoices):
    DRAFT = 'draft', _('草稿 | Draft')
    CONFIRMED = 'confirmed', _('已确认 | Confirmed')
    COMPLETED = 'completed', _('已完成 | Completed')
```

#### In Messages:
```python
# Correct
messages.success(request, _('处方已创建！| Prescription created successfully!'))
messages.error(request, _('您没有权限。| You do not have permission.'))
```

#### In Page Titles:
```html
{% block title %}处方详情 | Prescription Detail{% endblock %}
```

#### In Buttons and Links:
```html
<button type="submit" class="btn btn-success">
    <i class="bi bi-check-lg"></i> 保存 | Save
</button>
<a href="{% url 'prescriptions:list' %}" class="btn btn-outline-secondary">
    <i class="bi bi-arrow-left"></i> 返回 | Back
</a>
```

#### In Table Headers:
```html
<thead class="table-light">
    <tr>
        <th>处方编号 | Number</th>
        <th>患者 | Patient</th>
        <th>日期 | Date</th>
        <th>状态 | Status</th>
        <th>操作 | Actions</th>
    </tr>
</thead>
```

#### In Form Labels:
```html
<label class="form-label">诊断 | Diagnosis</label>
<label class="form-label">治则治法 | Treatment Principle</label>
<label class="form-label">剂数 | Number of Doses</label>
```

#### In Card Headers:
```html
<div class="card-header">
    <h5 class="mb-0">处方信息 | Prescription Info</h5>
</div>
```

#### In Alert Messages:
```html
<div class="alert alert-info">
    <i class="bi bi-info-circle me-2"></i>
    暂无处方记录。| No prescriptions yet.
</div>
```

---

## Rule 2: TCM-Specific Terminology

Always use proper TCM terminology with bilingual format:

### Four Examinations (四诊):
- 望诊 | Inspection
- 闻诊 | Auscultation & Olfaction
- 问诊 | Inquiry
- 切诊 | Palpation

### Tongue Diagnosis (舌诊):
- 舌体 | Tongue Body
- 舌苔 | Tongue Coating
- 舌色 | Tongue Color

### Pulse Diagnosis (脉诊):
- 寸 | Cun
- 关 | Guan
- 尺 | Chi

### Prescription Terms:
- 处方 | Prescription
- 剂数 | Number of Doses
- 煎煮方法 | Decoction Method
- 药材 | Herbs
- 剂量 | Dosage

### Formula Roles:
- 君药 | Monarch
- 臣药 | Minister
- 佐药 | Assistant
- 使药 | Envoy

---

## Rule 3: Permission Messages

Permission-related messages must be clear and bilingual:

```python
# Edit permission denied
messages.error(request, _('您没有权限编辑此处方。| You do not have permission to edit this prescription.'))

# Delete permission denied
messages.error(request, _('您没有权限删除此诊断记录。| You do not have permission to delete this diagnosis.'))

# Success messages
messages.success(request, _('处方已创建！| Prescription created successfully!'))
messages.success(request, _('诊断记录已更新！| Diagnosis updated successfully!'))
messages.success(request, _('患者信息已保存！| Patient saved successfully!'))
```

---

## Rule 4: Empty State Messages

When no data is available, show helpful bilingual messages:

```html
{% if not items %}
<div class="alert alert-info">
    <i class="bi bi-info-circle me-2"></i>
    暂无记录。| No records yet.
    <a href="{% url 'app:create' %}" class="alert-link">新建 | Create one</a>
</div>
{% endif %}
```

---

## Rule 5: Confirmation Dialogs

Delete and important action confirmations must be bilingual:

```html
<div class="alert alert-warning">
    <i class="bi bi-exclamation-circle me-2"></i>
    <strong>警告 | Warning:</strong> 此操作无法撤销！| This action cannot be undone!
</div>

<p class="lead">
    您确定要删除以下记录吗？<br>
    Are you sure you want to delete this record?
</p>
```

---

## Rule 6: Navigation and Menu Items

All navigation must be bilingual:

```html
<nav>
    <a href="{% url 'home' %}">首页 | Home</a>
    <a href="{% url 'patients:list' %}">患者管理 | Patients</a>
    <a href="{% url 'diagnosis:list' %}">诊断系统 | Diagnosis</a>
    <a href="{% url 'prescriptions:list' %}">处方管理 | Prescriptions</a>
</nav>
```

---

## Rule 7: Status Badges

Status displays should be bilingual in the model choices:

```python
class Status(models.TextChoices):
    DRAFT = 'draft', _('草稿 | Draft')
    CONFIRMED = 'confirmed', _('已确认 | Confirmed')
    DISPENSED = 'dispensed', _('已配药 | Dispensed')
    COMPLETED = 'completed', _('已完成 | Completed')
    CANCELLED = 'cancelled', _('已取消 | Cancelled')
```

---

## Rule 8: Form Placeholders

Placeholders can be Chinese-only or bilingual:

```html
<input type="text" placeholder="请输入姓名">
<input type="text" placeholder="搜索 | Search...">
<textarea placeholder="请输入备注 | Enter notes..."></textarea>
```

---

## Rule 9: Pagination

Pagination controls must be bilingual:

```html
<nav aria-label="Page navigation">
    <ul class="pagination">
        <li class="page-item">
            <a class="page-link" href="?page={{ page_obj.previous_page_number }}">上一页 | Prev</a>
        </li>
        <li class="page-item">
            <a class="page-link" href="?page={{ page_obj.next_page_number }}">下一页 | Next</a>
        </li>
    </ul>
</nav>
```

---

## Rule 10: Date and Time Display

Use consistent date format and bilingual labels:

```html
<p><strong>日期 | Date:</strong> {{ obj.created_at|date:"Y-m-d H:i" }}</p>
<p><strong>更新时间 | Updated:</strong> {{ obj.updated_at|date:"Y-m-d" }}</p>
```

---

## Quick Reference Checklist

Before submitting any code, verify:

- [ ] All page titles are bilingual (Chinese | English)
- [ ] All headings and section titles are bilingual
- [ ] All button labels are bilingual
- [ ] All table headers are bilingual
- [ ] All form labels are bilingual
- [ ] All success/error messages are bilingual
- [ ] All model field verbose_names are bilingual
- [ ] All model choices are bilingual
- [ ] All empty state messages are bilingual
- [ ] All navigation items are bilingual
- [ ] Chinese text comes FIRST, then English

---

## Common Bilingual Phrases

| Chinese | English | Combined Format |
|---------|---------|-----------------|
| 新建 | New/Create | 新建 \| New |
| 编辑 | Edit | 编辑 \| Edit |
| 删除 | Delete | 删除 \| Delete |
| 保存 | Save | 保存 \| Save |
| 取消 | Cancel | 取消 \| Cancel |
| 返回 | Back | 返回 \| Back |
| 搜索 | Search | 搜索 \| Search |
| 查看 | View | 查看 \| View |
| 打印 | Print | 打印 \| Print |
| 确认 | Confirm | 确认 \| Confirm |
| 提交 | Submit | 提交 \| Submit |
| 患者 | Patient | 患者 \| Patient |
| 医师 | Practitioner | 医师 \| Practitioner |
| 诊断 | Diagnosis | 诊断 \| Diagnosis |
| 处方 | Prescription | 处方 \| Prescription |
| 药材 | Herbs | 药材 \| Herbs |
| 状态 | Status | 状态 \| Status |
| 日期 | Date | 日期 \| Date |
| 备注 | Notes | 备注 \| Notes |
| 操作 | Actions | 操作 \| Actions |
