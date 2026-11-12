---
name: web-design-mastery
---

> متى تُستعمل: "SchoolOS web UI: CSS layers, tokens, dark mode, RTL, HTMX, a11y. Trigger: CSS, template, component, layout, mobile. واجهة، قالب، الوضع الليلي، الجوال"

# معاييرُ الواجهة في SchoolOS

الغرض: أن تُبنى كلُّ صفحةٍ ومكوّنٍ بمصادر الحقيقة المركزيّة — رموزٌ لا قيم، ومكوّناتُ `ui.py` لا بنيةٌ باليد، ونمطُ تخطيطٍ مسمّى لا شبكةٌ محلّيّة — فتبقى الحرّاسُ خضراءَ والهويّةُ واحدة.
المرجعُ الأعلى `CLAUDE.md` (الأقسامُ عن الأنماط والبطاقات والتنبيهات والانتقال والقائمة والتخطيط)؛ هذه المهارةُ تفصّله ولا تخالفه. تحقّقٌ على `main` في 2026-09-28.

## متى تُستعمل ومتى لا
- نعم: قالبٌ تحت `templates/`، ملفٌّ تحت `static/css/custom/` أو `static/js/`، وسمٌ في `core/templatetags/ui.py`، لونٌ أو خطٌّ أو تباعد، صفحةٌ جديدة.
- لا: قالبُ PDF (له إطارٌ مطبوعٌ مستقلّ)، ولا قرارُ دمجٍ أو نشر (`schoolos-flow`).

## الإجراء
0. **ابدأ من مرجع الهويّة المولَّد** `.claude/rules/identity-reference.md` (يُحمَّل تلقائياً حين تلمس `static/` أو `templates/`؛ وإلا اقرأه): رموزُ الألوان نهاراً وليلاً، وقاموسُ الأيقونات بمعانيها، وأنماطُ الصفحات السبعة — فلا تفتح `/styleguide/` (مطوّريّةٌ) ولا تخمّن لوناً أو أيقونة. مولَّدٌ من المصادر ويحرسه `tests/test_identity_reference_fresh.py`.
1. **اختر نمطَ الصفحة قبل أن تكتبها**: `{% block main_class %}{% page_layout "list" %}{% endblock %}` — أحدُ `dashboard|hub|list|detail|form|sheet|report` (أو `custom` بسطرٍ في جدول الاستثناءات). صفحةٌ جديدةٌ بلا نمطٍ تُسقط `tests/test_page_layouts.py`. ← `references/20-layouts-components.md`
2. **ابنِ من المكوّنات القائمة**: `page_header`، `section_card`، `kpi`/`kpi_strip`، `callout` (خمسة أنواع)، `empty_state`، `field`، `filter_bar`، `action_tile`، `entity_card`، و`{% icon "…" %}`. صنفٌ جديدٌ آخرُ الحلول.
3. **الأنماطُ في ملفّ طبقتها**: مكوّنٌ ← `20-components`، شاشةٌ ← `30..33-modules` (آخرُها 33)، ليليٌّ ← `40-themes`، مساعدٌ ← `50-utilities`؛ ولا قاعدةَ خارج `@layer`. ← `references/10-css-architecture.md`
4. **القيمُ رموز**: لونٌ بدوره (`--text-*`، `--status-*-fg`، `--on-fill`…)، تباعدٌ `var(--sp-*)`، تقوّسٌ `var(--radius-*)`، خطٌّ بـ`rem`. ← `references/00-tokens-theming.md`
5. **قِس على أربعة أجهزةٍ نهاراً وليلاً**: 1366×768 و1920×1080 ولوحيّ (~768×1024) و375×812 — وما لم يُقَس يُقال «لم يُقَس». طريقةُ القياس على صفحةٍ محميّةٍ في `schoolos-preview-8500` ← `03-measuring-protected-pages.md`؛ ثمّ التحقّقُ البصريُّ بالدور (تداخل، معطَّلٌ بلا سبب، اقتطاع، مصفوفةُ الحالات) **قبل** إعلان «جاهز». ← `references/50-responsive-mobile.md` و`references/55-visual-verification.md`
   وإن طُلب أن تطابق صفحةٌ صفحةً قائمة فاتّبع إجراءَ «طبقَ الأصل» في `references/20-layouts-components.md` قبل البناء.
6. **شغّل الحرّاس** قبل الدفع (من شجرة عملك بأوامر `CLAUDE.md`): `tests/test_css_*.py`، `test_px_tokens`، `test_rtl_logical_properties`، `test_dark_parity`، `test_contrast_ratios`، `test_design_ratchet`، `test_a11y_ratchet`، `test_page_layouts`. وقراءةُ الفاشل منها في مهارة `schoolos-quality-guards`.

## تحديثاتُ الهويّة منذ 2026-09-28 (إلزاميّة)
- **لا صفحةَ خارج المنصّة ولا في لسانٍ جديد** (قرار المالك 2026-10-13): لا `target="_blank"` ولا `window.open(` ولا `href="http(s)://"` في القوالب وJS؛ الحارس `tests/test_no_external_pages.py` (الجديدُ ممنوع والقديمُ في خطّ أساسٍ يتناقص).
- **رأسُ الجدول ثابتٌ عند التمرير الرأسيّ** (قرار المالك 2026-10-13): كلُّ جدولٍ بـ`{% for %}` داخل `table-wrap` يحمل `table-wrap-scroll`؛ الحارس `tests/test_sticky_table_header.py`. ويمرّر الجدولُ الطويلُ داخلَه لا الصفحة (خاناتُ `95-checklist.md` الثلاث، W-20261009-019).
- **الانتقالُ**: لا `transition: all`؛ استعمل `--q-transition-ui` وخصائصَ صريحة، والاتّجاهُ بخصائص منطقيّة (`41dff8110`).
- **شعارُ المدرسة «ش»** (D-404م): الوسمُ `{% school_logo "nav" %}` من `core/school_logo.py` مصدرٌ واحدٌ للشاشة وPDF وExcel (الأصل `static/icons/v3/icon-192.png`). شعارُ الوزارة أُزيل ولا يعود؛ وسطرُ الانتماء للوزارة مخفيٌّ افتراضًا خلف `MINISTRY_AFFILIATION_VISIBLE` (`core/ministry.py`، الوسم `ministry_name`). تغييرُ الأيقونات يرفع `CACHE_NAME` في عامل الخدمة.
- **الطباعةُ**: ورقةٌ واحدة بـ`SINGLE_SHEET_BOOST`، وخطّ Tajawal، وإطارٌ مطبوعٌ مركزيّ (W-057)؛ ولا تحديدَ `.nav-inner` بعرض 1280px.
- **لا صنفَ `text-xs`** في القوالب (استعمل رموزَ الخطّ)، ونماذجُ الدخول هُجّرت.
- **ألوانُ الأجنحة** من `core/dept_colors.py:WING_KEY_OF_ORDER` (ترويسة الجناح وشريطه)، وأمّا **لونُ الصفّ الدراسيّ** (7 … 12) فمنفصلٌ: ستّةُ رموز `--grade-7..12` مطفأةٌ مع مرآتها في `core/brand.py` (W-20261013-016)، يُصبّ على تظليل صفّ الفصل 7/1 … 12/4 وشارته ولا يُخلط بلون جناح؛ وتدرّجُ الشعب داخل الصفّ بقرار المالك المنتظر.
- **أعمدةُ الجداول مرنةٌ تتكيّف مع محتواها** شاشةً وPDF وإكسل (قرار المالك 2026-10-13: «مرنة مرنة»): لا عرضَ ثابتاً يقتطع النصّ ولا `ellipsis` يخفي بيانة؛ لا عرضَ ثابتاً لعمود التسلسل والأسماءُ لا تنكسر؛ الحارس `tests/test_flexible_table_columns.py`، والتفصيلُ في `.claude/rules/tables.md`.
- **توسيطُ نصوص الجداول وترويستها** (قرار المالك 2026-10-13، للقائم والمستقبليّ وبأثرٍ رجعيّ، شاشةً وPDF وإكسل): الخلايا والترويسةُ `text-align: center` **عدا عمود الأسماء** فيبقى `start`؛ مركزيّاً لا نمطاً محلّيّاً. التفصيلُ في `.claude/rules/tables.md`.
- **حرّاسُ الهويّة** `test_dead_classes` و`test_design_ratchet` و`test_tailwind_freeze` تعمل في `prepush`، ومرجعُ الهويّة المولَّد يُحمَّل مع الواجهة.
- **قاعدةٌ دائمة: كلُّ تعديلٍ أو إضافةٍ على الهويّة يحدّث هذه المهارةَ و`CHANGES.md` في الطلب نفسه**، وإلا عُدّ ناقصًا.

## القواعد وأسبابها
- **لا لونَ حرفيّاً في CSS ولا في القالب** — الرموزُ تنقلب ليلاً والحرفُ لا ينقلب (`test_css_colours_are_tokens`، وسقّاطةُ الهويّة `hex_colour` = 0). في القالب `{% brand_color "MAROON" %}`، ومرآتُه `core/brand.py`.
- **نصٌّ فوق حشوٍ ثابتٍ `var(--on-fill)` لا `#fff`**؛ ونصٌّ على سطحٍ `--text-*` أو `--status-*-fg`. السبب: الأبيضُ يساوي السطحَ نهاراً مصادفةً ويُطفئ الترويسةَ ليلاً.
- **الذهبيُّ تمييزٌ لا نصّ** (`--gold-mark` للأيقونة على العنّابيّ) — تباينُه على الفاتح 2.2 (`test_identity_roles`).
- **الليلُ برموزٍ تنقلب** في `html.dark { --… }` داخل `40-themes.css`، والوضعُ اختيارُ المستخدم وحدَه (زرّ + `localStorage`) لا تفضيلُ النظام. وخلفيّةٌ فاتحةٌ ليلاً ممنوعة — الأبيضُ للنصوص والحدود فقط.
- **الاتّجاهُ منطقيّ**: `inset-inline-*`، `margin-inline-*`، `text-align: start` — لا `left:`/`right:` (`test_rtl_logical_properties`).
- **لا `?v=N` ولا `collectstatic` في التطوير**: الإنتاجُ يبصم الاسمَ بمحتواه والتطويرُ يخدم بـ`max-age=0` — حدِّث الصفحة وحسب (`CLAUDE.md`).
- **لا `onclick` ولا `<script>` بلا `nonce`**: CSP بـ`nonce` تُسقط المعالجاتِ المضمَّنة؛ السلوكُ بـ`data-action`/`data-call` (`static/js/actions.js`). وسكربتُ الصفحة داخل IIFE لأنّ `page-nav.js` يعيد تشغيله.
- **لا `@container`** (ADR-0005 D3، مؤكَّدٌ بالقياس في ADR-0006)، **ولا Tailwind جديد** (`test_tailwind_freeze`)، **ولا زرَّ طباعة صفحة** (`test_no_web_page_print_button`)، **ولا شريطٌ فرعيٌّ لقسم** (قرارُ 2026-09-20).
- **الميزانيّاتُ من ملفّاتها الحيّة**: CSS مصغَّرٌ ≤ 269KB (`tests/test_css_budget.py`)، وخامٌ ≤ 470KB وJS ≤ 400KB و≤ 10 أوراقٍ حاجبة وLCP ≤ 2500 وINP ≤ 300 وCLS ≤ 0.1 (`tests/web_vitals.py:BUDGET`). التعليقُ العربيّ في CSS يُحسب في الخامّ (بايتان للحرف).

## فخاخٌ حقيقيّة
- خطأ: `{% if request.htmx %}…{% else %}{% extends "base.html" %}{% endif %}` — `extends` يجب أن يكون أوّلَ وسمٍ فلا يُشرَط. الصواب: الـview تختار: `core.htmx_utils.htmx_or_full(request, partial, full, ctx)`.
- خطأ: `.data-table` و`.card-header` و`.card-qatar` في صفحةٍ جديدة. الصواب: الأوّلان غيرُ معرَّفين، والثالثُ «بنيةٌ باليد» تعدّها سقّاطةُ الهويّة؛ استعمل `section_card` و`table-wrap`.
- خطأ: «النصُّ الخافت `#6b7280` بتباين 4.63». الصواب: `--text-muted` صار `#58606d` (6.35 على السطح)؛ اكتب الرمزَ لا القيمة.
- خطأ: «Amiri للجداول على الويب». الصواب: الويب Tajawal (و`Tajawal Tashkeel` للمشكول)؛ Amiri للـPDF وحدَه.
- خطأ: `templates/base.html`. الصواب: القالبُ الأساس `templates/base/base.html`.
- خطأ: «mobile-first بـ`min-width` فقط». الصواب: المنصّةُ تكتب `@media (max-width: 640px)` للجوال و`min-width: 641px`/`1025px` للأوسع — اتبع الملفَّ الذي تعمل فيه، وضع قاعدةَ `@media` **بعد** القاعدة الأساسيّة (الأخيرةُ تغلب).
- خطأ: `margin: 12px` أو `font-size: 14px`. الصواب: `var(--sp-3)` و`var(--text-sm)`/`0.875rem` — القيمةُ الحرفيّةُ التي تطابق درجةً ممنوعة (`test_px_tokens`).
- خطأ: بطاقةٌ تمتدّ بطول النافذة وفيها فراغ. الصواب: `fill-grid is-fit` للمحتوى المحدود؛ وقائمةٌ ضيّقةٌ طويلةٌ تُقسَّم أعمدةً بـ`chunk_for_grid` في الـview + `.auto-grid`.
- خطأ: ميزانيّة «Dashboard < 800KB» و«INP < 200ms». الصواب: تلك من كتاب؛ أرقامُ المشروع أعلاه من ملفّاتها.

## المراجع
| الملف | متى تقرأه |
|---|---|
| `references/00-tokens-theming.md` | قبل اختيار أيّ لونٍ أو خطٍّ أو تباعدٍ أو ظلّ، أو عند عملٍ ليليّ |
| `references/10-css-architecture.md` | قبل كتابة CSS: الملفّاتُ والطبقاتُ والحرّاسُ والميزانيّات |
| `references/20-layouts-components.md` | عند بناء صفحةٍ أو بطاقةٍ أو تنبيهٍ أو أيقونةٍ أو قائمة |
| `references/30-htmx-js.md` | عند HTMX أو JS أو تنقّلٍ أو تصديرٍ من الواجهة |
| `references/40-accessibility.md` | عند نموذجٍ أو حوارٍ أو جدولٍ أو تباينٍ أو تركيز |
| `references/50-responsive-mobile.md` | عند الجوال واللوحيّ و«بلا تمرير» والمنطقة الآمنة |
| `references/55-visual-verification.md` | قبل إعلان «جاهزٌ للمعاينة» على عملٍ يلمس الواجهة: الأجهزة والتداخل والحالات والأدوار |
| `references/60-typography.md` | عند الخطّ والأحجام والمسافات السطريّة والنصّ المختلط |
| `references/70-performance.md` | عند صورٍ أو خطوطٍ أو سكربتاتٍ أو عامل خدمة أو ميزانيّة |
| `references/80-print-and-export.md` | حين يتعلّق الطلبُ بالطباعة أو التصدير من الواجهة |
| `references/90-book-principles.md` | لمبادئ الكتب العشرة بعد مواءمتها مع المشروع |
| `references/95-checklist.md` | قائمةُ مراجعةٍ قبل الدفع |
| `references/99-test-cases.md` | لاختبار تفعيل المهارة وجودة جوابها |
