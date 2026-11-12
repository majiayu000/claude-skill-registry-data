---
name: nplus1-hunter
---

> متى تُستعمل: "N+1 and slow queries: select_related, prefetch_related, query count. Trigger: N+1, slow page, query count. بطء صفحة، استعلامات كثيرة، ليش بطيئة"

# صيّاد N+1 في SchoolOS

الغرض: ألّا يتبع عددُ استعلامات أيّ صفحةٍ أو نقطةٍ عددَ الصفوف — يُثبَت باختبارٍ يقارن صفّاً بثلاثة، ويُصلَح في مصدر الاستعلام لا في القالب.
السببُ الحيّ: تدقيقُ المعماريّة وجد سبعةً، أحدُها ثلاثةُ استعلاماتٍ لكلّ ابنٍ في صفحة وليّ الأمر، وقوائمُ الإدارة بلغت 373 استعلاماً (المصدر: `tests/test_n_plus_one_queries.py`، `tests/test_admin_changelist_queries.py`).

## متى تُستعمل ومتى لا
- نعم: حلقةٌ في بايثون أو `{% for %}` في قالبٍ تعبر علاقة، وserializer فيه حقلٌ من علاقة، وتصديرٌ يمرّ على الصفوف.
- لا: استعلامٌ واحدٌ بطيء (فهرس ← schoolos-migration-guard)، أو حسابٌ ثقيلٌ بلا قاعدة.

## الإجراء
1. **اصطد المرشّحات** (على المضيف أو في الحاوية، لا يحتاج Django):
   `python .claude/skills/nplus1-hunter/scripts/nplus1_scan.py --path <ملفٌّ أو تطبيق>`
   مرشّحاتٌ لا أحكام؛ حدودُه في `references/02-measure-and-test.md`.
2. **اقرأ مصدرَ القائمة:** الـview أو الـselector الذي يبني الـqueryset، والقالبَ أو الـserializer الذي يقرؤه — والدوالَّ والخصائصَ التي يستدعيها لكلّ صفّ (`references/00-project-patterns.md`).
3. **قِس قبل أن تُصلح:** اكتب في `tests/` اختباراً على نمط `assert_flat` — إحماء، ثمّ عدٌّ بصفٍّ واحد، ثمّ بثلاثة، والعددان متساويان. يجب أن **يسقط** قبل الإصلاح.
4. **أصلِح في المصدر** بالأداة المناسبة (`references/01-fix-patterns.md`)، ثمّ أعِد الاختبار حتّى يخضرّ.
5. **شغّل الاختبار في حاوية جلستك** بأمر الاختبار في `CLAUDE.md`، واذكر في وصف الطلب العددين قبل وبعد.

## القواعد وأسبابها
- **الإصلاحُ في الـview/selector لا في القالب.** القالبُ يقرأ ما يُعطى؛ `{% with %}` لا يوفّر استعلاماً. والقوالبُ 340 ملفّاً تُصيَّر على الخادم (HTMX يعيد جزءاً منها)، فالعبورُ فيها مخفيٌّ عن قارئ الـview.
- **الاختبارُ يقارن ولا يثبّت رقماً.** العددُ المطلق يتغيّر بالقالب والوسائط (الجلسة، الصلاحيّات، السياق) فيتقادم ويُعدَّل بلا تفكير؛ المقارنةُ بين صفٍّ وثلاثة لا تتقادم (المصدر: توثيقُ `tests/test_admin_changelist_queries.py`). و`django_assert_num_queries` مسموحٌ لدالّةٍ ضيّقة لا لصفحة.
- **`select_related` للأمام، `prefetch_related` للعكسيّ وM2M، `annotate` للعدّ والجمع.** والـprefetch يضيع إن تلاه `.filter()`/`.count()`/`.order_by()` على المدير نفسِه — ذلك استعلامٌ جديدٌ لكلّ صفّ؛ استعمل `Prefetch(..., queryset=..., to_attr=...)` واقرأ القائمة.
- **دوالُّ المستخدم تستعلم:** `user.get_role()` و`user.role` و`user.school`/`get_school()` تجلب العضويّات مرّةً لكلّ كائن مستخدم، و`has_role()` استعلامٌ في كلّ نداء (المصدر: `core/models/user.py`). في قائمة مستخدمين: امشِ على `Membership` بـ`select_related("user", "role")`.
- **لا تُصلح ما لم تقِسه، ولا تُفرط:** `select_related` لعلاقةٍ لا تُقرأ JOIN بلا فائدة.

## فخاخٌ حقيقيّة
- خطأ: `StudentEnrollment.objects.filter(school=school)`. الصواب: `filter(class_group__school=school)` — لا حقلَ `school` على التسجيل (`core/models/academic.py`)، والسابقةُ الصحيحة `api/views.py::StudentListView` بـ`.select_related("student", "class_group")`.
- خطأ: `{{ e.class_group.name }}`. الصواب: لا حقلَ `name` على الشعبة: `short_label` أو `label_with_track` خصائصُ محسوبةٌ من حقولها — واجلب الشعبةَ بـ`select_related` في المصدر.
- خطأ: `for c in classes: c.enrollments.filter(is_active=True).count()`. الصواب: `annotate(n=Count("enrollments", filter=Q(enrollments__is_active=True)))`.
- خطأ: `.prefetch_related("enrollments")` ثمّ `c.enrollments.filter(...)` في الحلقة. الصواب: `Prefetch("enrollments", queryset=StudentEnrollment.objects.filter(is_active=True).select_related("student"), to_attr="active_enrollments")`.
- خطأ: في قائمة موظّفين: `{{ u.get_role }}` لكلّ صفّ. الصواب: مصدرٌ على `Membership.objects.filter(...).select_related("user", "role")` و`{{ m.role.name }}`.
- خطأ: `client.force_authenticate(user)` في اختبار عدّ الاستعلامات لنقطة `/api/`. الصواب: `Client().force_login(user)` — الوسيطُ يردّ 401 قبل DRF لمن لا جلسةَ له (`core/middleware.py`).
- خطأ: الاعتمادُ على لوحة debug_toolbar. الصواب: `CaptureQueriesContext` — الحزمةُ ليست في المتطلّبات ولا في صورة الحاوية، فإعدادُها في `development.py` لا يعمل.
- خطأ: «المسار الوحيد `D:\shschool_mvp`». الصواب: اعمل في شجرتك (`CLAUDE.md`، القاعدة رقم 1)؛ والفاحصُ القديم كان لا يجد شيئاً داخل شجرة عمل — أُصلح.

## المراجع
| الملف | متى تقرأه |
|---|---|
| `references/00-project-patterns.md` | لتعرف العلاقاتِ الحقيقيّة وأسماءَها، والدوالَّ التي تستعلم خفيةً، وأين تعيش الـselectors |
| `references/01-fix-patterns.md` | حين تختار الأداة: select/prefetch/Prefetch/annotate/values، ومزالقُ كلٍّ منها |
| `references/02-measure-and-test.md` | لكتابة اختبار الثبات، والقياس اليدويّ، وحدود الفاحص وإيجابيّاته الكاذبة |
| `references/99-test-cases.md` | عند تعديل الوصف أو الجسم أو السكربت |
