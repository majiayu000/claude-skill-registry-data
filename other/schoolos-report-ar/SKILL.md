---
name: schoolos-report-ar
---

> متى تُستعمل: "Arabic RTL PDF and Excel exports: render_pdf, ExcelService, print frame. Trigger: PDF, Excel, export, WeasyPrint, A3. تقرير، كشف، شهادة، تصدير، طباعة"

# التقارير الرسميّة PDF وExcel — SchoolOS

الغرض: أن يخرج كلُّ ملفٍّ رسميٍّ من **مسارٍ واحد**: بنّاءٌ في سجلّ التصدير، وقالبٌ على الإطار المطبوع المركزيّ، وخطٌّ مقروءٌ بحدود المالك، وسطرُ تدقيق — لا نسخةً محلّيّةً لكلّ قالب.
كلُّ ما هنا متحقَّقٌ على `main` في 2026-09-28؛ والتفاصيلُ في المراجع.

## متى تُستعمل ومتى لا
- نعم: PDF أو Excel يُنزَّل أو يُطبع، قالبٌ ورقيّ، ترويسةٌ أو تذييل، مقاسُ ورق، حجمُ خطٍّ مطبوع، تحويلُ تصديرٍ متزامنٍ إلى خلفيّ.
- لا: صفحةُ ويبٍ تُعرض على الشاشة (ولا «زرَّ طباعة صفحة» — ممنوعٌ بحارس)، ولا قرارُ الخصوصيّة نفسُه.

## الإجراء
1. **ابنِ البنّاءَ لا الـview**: دالّةٌ نقيّةٌ `build(school, user, params) -> ExportResult` تُسجَّل في `AppConfig.ready()` بـ`core.exports.registry.register(kind, build=…, capability=…)`، والـview تنادي `respond_export(request, kind)`. الافتراضُ `mode="job"` (خلفيّ)، و`direct` يرفضه السجلُّ بلا p95 مقيسٍ ≤ 1000ms. ← `references/00-export-pipeline.md`
2. **القالبُ على الإطار المركزيّ**: انسخ `assets/report_template.html` (ترويسةٌ وتذييلٌ بوسوم `print_frame`، وعلامةُ `data-pdf-own-page`)، وعبّئ المحتوى وحدَه. ← `references/10-print-frame.md`
3. **الخطُّ بحدود المالك (D2)**: قوائمُ وجداولُ متعدّدةُ الصفحات 10pt، متنُ النماذج 11–12pt وأدنى 10، العنوانُ 16 (أدنى 14)، التذييلُ 10 (أدنى 9). ما لا يسع يأخذ A3 أو صفحاتٍ أكثر — لا خطّاً أصغر.
4. **Excel بأدوات المنصّة**: `ExcelService` أو `core.export_utils` (`add_excel_title_rows`، `excel_table_styles`)، ويخرج بـ`excel_to_response`/`ExcelService.to_response` لتلحقه رؤيةُ الوزارة في ذيل الطباعة. ← `references/20-excel.md`
5. **الخصوصيّة والتدقيق**: `log_export` (أو `rows`/`full_national_id` في `ExportResult`)، والرقمُ الشخصيّ مستورٌ في كلّ كشفٍ جماعيّ. ← `references/30-content-and-privacy.md` ومهارة `pdppl-pii-audit`.
6. **تحقّق**: صيّر PDF حقيقيّاً (WeasyPrint في حاوية الجلسة) وقس الصفحاتِ وأصغرَ خطّ، وشغّل `tests/test_print_frame_guard.py` و`tests/test_export_guards.py` و`tests/test_national_id_never_bulk.py`. تشغيلُ الخادم والاختبارات في شجرة عملك بأوامر `CLAUDE.md`؛ وخطواتُ الفلو في `schoolos-flow`.

## القواعد وأسبابها
- **لا `render_pdf`/`render_pdf_bytes`/`Workbook` جديدٌ داخل view** — `HEAVY_IN_VIEWS` في `tests/test_export_guards.py` سقّاطةٌ تنقص ولا تزيد. السبب: WeasyPrint وحدَه 400–550ms، وأبطأُ تصديرٍ كان 19.9ث يزاحم daphne الذي يخدم WebSocket (ADR-0007).
- **الإطارُ في مكوّنٍ واحد**: لا `running(` ولا `@bottom-` ولا أصنافُ `*-footer` في قالب — `tests/print_frame_ratchet.py` (ملفٌّ جديدٌ رقمُه صفر). السبب: خمسُ نسخٍ متباينةٍ أخرجت تذييلاً بسطرين وخطّاً 6–8pt.
- **`data-pdf-own-page` إلزاميٌّ مع وسوم الإطار**: بدونه يحقن `core/pdf_utils.py` إطارَه القديم (يغلب الترويسةَ المركزيّةَ أو يضيف «SchoolOS v6» والتاريخ في الزاويتين). مقيسٌ بتصيير WeasyPrint في 2026-09-28.
- **الرؤيةُ سطرٌ واحدٌ في كلّ تذييل** (PDF وExcel)، ونصُّها من `components/ministry_vision.html` لا حرفيّاً. السبب: أمرُ المالك 2026-09-27 (المواصفة v2.4، D1).
- **لا `@font-face` ولا `{% static %}` للخطّ في قالب PDF**: `_inject_fonts` يحقن Tajawal/Amiri/Noto Naskh بمساراتٍ مطلقة؛ والرابطُ النسبيّ يسقط صامتاً إلى DejaVu. وفي العامل لا manifest: مساراتُ الثابت بمسارٍ نسبيٍّ (`for_pdf=True`).
- **لا قصَّ للنصّ الحرّ في المطبوع** (لا `line-clamp` ولا `truncatechars`) — رفضه المالك؛ والطويلُ يأخذ صفحةً أخرى.
- **الألوانُ `{% brand_color "…" %}`** لا سداسيّاً — حارسُ الهويّة يعدّ السداسيَّ في القوالب.

## فخاخٌ حقيقيّة
- خطأ: نسخُ ترويسة `reports/base_qatar_report.html` أو `@page { @top-center … }` إلى قالبٍ جديد. الصواب: `{% print_frame_css %}` + `{% print_frame_header %}` + `{% print_frame_footer %}` قبل المحتوى.
- خطأ: «وزارة التعليم والتعليم العالي» و`assets/brand/qatar-emblem-2022.svg`. الصواب: «وزارة التربية والتعليم والتعليم العالي — دولة قطر» (`core/templatetags/print_frame.py::MINISTRY`) نصّاً بلا صورةِ شعار — شعارُ الوزارة أُزيل من المنصّة كلِّها (D-386م)، والإطارُ يكتب السطرَ عنك.
- خطأ: خطوط Noto Sans Arabic أو Cairo أو IBM Plex. الصواب: غيرُ موجودةٍ في `static/fonts/`؛ المتاح Tajawal وAmiri وNoto Naskh Arabic (وTraditional Arabic من `StoredFile` إن ثُبّت).
- خطأ: «≥ 9pt للبيانات يكفي». الصواب: D2: 10pt للقوائم والجداول؛ الاستثناءُ الوحيد الجدولُ العامّ 7.9pt بقرارٍ خاصّ.
- خطأ: `ws.oddFooter.center.text = "صفحة &P من &N"` بعد البناء. الصواب: `apply_print_footer` (عبر `excel_to_response`) يكتب الصفحةَ والرؤيةَ سطراً واحداً — والكتابةُ فوقه تُسقط الرؤية.
- خطأ: `ws.freeze_panes = "A2"` مع ترويسة المنصّة. الصواب: ثلاثةُ صفوف عنوانٍ ثمّ رأسُ الأعمدة في الصفّ 4، فالتجميدُ `"A5"` وتكرارُ الطباعة `"1:4"`.
- خطأ: «التاريخ الهجريّ بـ`hijri-converter`» و«تصنيفُ السرّيّة في التذييل». الصواب: لا مكتبةَ هجريّةً في `requirements.txt` ولا تصنيفَ سرّيّةٍ في الإطار؛ كلاهما يحتاج قرارَ المالك قبل أن يُكتب.
- خطأ: جدولٌ فارغٌ يُمرَّر إلى المولّد. الصواب: حارسٌ قبل التوليد (رسالةٌ أو حالةٌ فارغة) — مسارُ xhtml2pdf الاحتياطيّ ينهار على الجدول الفارغ (`reports/views.py`).

## المراجع
| الملف | متى تقرأه |
|---|---|
| `references/00-export-pipeline.md` | قبل كتابة أيّ تصدير: السجلّ، البنّاء، الـview، العامل، الحرّاس |
| `references/10-print-frame.md` | حين تكتب قالب PDF أو تشتكي من ترويسةٍ أو تذييلٍ أو خطٍّ أو مقاس |
| `references/20-excel.md` | حين تبني ملفّ Excel أو تعدّل واحداً |
| `references/30-content-and-privacy.md` | لبنية المحتوى، والتوقيعات، والرقم الشخصيّ، واسم الملفّ، والحالات الحدّيّة |
| `references/99-test-cases.md` | لاختبار تفعيل المهارة وجودة جوابها |
| `assets/report_template.html` | نقطةُ بدايةٍ لقالب تقريرٍ جدوليٍّ جديد (مُختبَرٌ بتصييرٍ حقيقيّ) |
