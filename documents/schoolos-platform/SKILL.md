---
name: schoolos-platform
---

> متى تُستعمل: "SchoolOS codebase map: apps, models, services, roles, grading, scoping. Trigger: where is X, request.school, models/services/views. أين أجد، الأدوار، التقييم"

# SchoolOS — خريطةُ الشيفرة

خريطةٌ تقول أين يوجد الشيء في المنصّة، وما قواعدُ مجاله، وما الفخُّ الذي وقع فيه من سبقك. كلُّ اسمٍ هنا تحقّقتُ من وجوده على `main@81bc4937` (2026-09-28)؛ والشيفرةُ أصحُّ من هذه الخريطة إن اختلفتا.

## متى تُستعمل ومتى لا
- **نعم:** قبل كتابة model أو service أو view أو تقريرٍ أو تصدير؛ عند سؤال «أين/من يملك/كيف أستعلم»؛ عند لمس الدرجات أو الأدوار أو الغياب أو السلوك.
- **لا:** خطواتُ الفلو والمنافذ والدفع (schoolos-flow، schoolos-git-safety)؛ نصُّ اللائحة الوزاريّة نفسُه (schoolos-source-of-truth)؛ الواجهةُ والأنماط (web-design-mastery).

## الإجراء
1. حدّد المجال ثمّ اقرأ مرجعَه من الجدول أدناه — لا تقرأها كلَّها.
2. تحقّق من الاسم قبل استعماله: `git grep -n "class <Name>" origin/main -- '*.py'` — الخريطةُ لقطةٌ والمنصّةُ تتغيّر يوميّاً.
3. الأرقامُ القانونيّة (أوزان، عتبات، حدود) تُقرأ من ثابتها في الشيفرة (`core/domain/grades.py`، `operations/absence_policy.py`، `behavior/conduct_2026.py`) لا من ذاكرتك ولا من هذه الخريطة.
4. ضع الكود في طبقته (المرجع 04)، ثمّ شغّل الحرّاس المتأثّرة قبل الدفع (schoolos-quality-guards).

## القواعد وأسبابها
- **لا Student ولا Teacher model** — الكلُّ `CustomUser`، والدورُ عضويّةٌ `Membership` بمدرسةٍ ودور. السبب: شخصٌ واحدٌ قد يكون معلّماً ووليَّ أمرٍ في المدرسة نفسها. المصدر: `core/models/user.py`، `core/models/access.py`.
- **المدرسةُ من `request.school`** لا من `request.user.get_school()` في العروض؛ السبب: تُحسب مرّةً لكلّ طلبٍ في `SchoolContextMiddleware`، وسقّاطةُ الطبقات تعدّ `get_school()` في ملفّات العروض. المصدر: `core/middleware.py`، `docs/governance/regression_guards.md`.
- **مجموعاتُ الأدوار في `core/permissions.py` وحدَه**؛ السبب: مجموعةٌ في ملفّ واجهةٍ تغيّر الصلاحيّةَ دون أن يراها المراجع. المصدر: `tests/test_permission_groups_are_central.py`.
- **حكمُ النجاح والرسوب واحد** (`core.domain.grades.judge_student`)، والعدُّ بـ`core.verdict_read.passing_statuses()` لا `status="pass"`؛ السبب: عشرُ حالاتٍ لا اثنتان، ولا حكمَ موازٍ. المصدر: `core/verdict_read.py`.
- **لا تاريخَ حرفيّاً في المنطق** — العامُ من `core/academic_calendar.py`؛ السبب: نافذةٌ مكتوبةٌ أخلت حسابَ الغياب صامتاً عند بدء عامٍ جديد. المصدر: `tests/test_no_literal_dates_in_logic.py`.
- **كلُّ تصديرٍ PDF/Excel عبر سجلّ `core/exports`** (مهمّةٌ خلفيّةٌ افتراضاً)؛ السبب: 22 من 35 تصديراً فوق 300ms تزاحم daphne. المصدر: ADR-0007، `tests/test_export_guards.py`.

## فخاخ
- خطأ: `Student.objects.filter(...)` · الصواب: `StudentEnrollment.objects.filter(class_group=cg, is_active=True)` لطلبة شعبة، و`CustomUser.objects.in_school(school)` لمنتسبي مدرسة.
- خطأ: `StudentEnrollment.objects.filter(student=s, is_active=True).first()` · الصواب: `StudentEnrollment.objects.current_of(s, school)` — مئاتُ الطلبة لهم قيدان نشطان، و`first()` بلا ترتيبٍ عشوائيّ. المصدر: `core/models/academic.py`.
- خطأ: `filter(memberships__role__name="teacher")` لمن يدرّس · الصواب: `CustomUser.objects.teachers(school)` — المنسّقُ يحمل نصاباً (`TEACHING_ROLES = {"teacher","coordinator"}`). المصدر: `core/models/access.py`، `core/querysets.py`.
- خطأ: `user.role == "parent"` لمعرفة أهو وليُّ أمر · الصواب: `user.has_parent_membership` — `role` هو الدورُ الحاكم والكادرُ يتقدّم. المصدر: `core/models/user.py`.
- خطأ: ترتيبُ الشُّعب بـ`grade` نصّاً («G10» قبل «G7») · الصواب: `core.models.academic.grade_number(grade)`.
- خطأ: حدُّ نجاحٍ 60 أو أوزانٌ من `AssessmentPackage.weight` في الحساب · الصواب: `PASS_MARK = 50` و`exact_package_weight()` من القرار 14/2018. المصدر: `core/domain/grades.py`.
- خطأ: «معظمُ النماذج ترث `SchoolScopedModel`» · الصواب: أربعةٌ فقط ترثه؛ الباقي يعلن `school` بنفسه، وكلُّ جدولٍ جديدٍ يجب أن يُصنَّف في `core/tenancy.py` وإلّا سقط `tests/test_tenant_surface_coverage.py`.
- خطأ: `apply_async(queue="celery")` · الصواب: بلا اسمِ طابورٍ حرفيّ — طابورُ الجلسة باسم قاعدتها (`SESSION_NAMESPACE`). المصدر: `tests/test_export_core.py`، `shschool/settings/development.py`.

## المراجع

| الملف | متى تقرأه |
|---|---|
| `references/00-apps-map.md` | أين يوجد تطبيقٌ أو نموذجٌ أو خدمةٌ أو مسارُ URL؛ الإصداراتُ؛ جداول `core_*` الموروثة |
| `references/01-users-roles-tenancy.md` | مستخدمون، أدوار (36)، عضويّات، صلاحيّات، قدرات، نطاقُ الجناح، RLS، الدخول |
| `references/02-assessment.md` | الباقاتُ والأوزانُ والصفّ 12 وجبرُ الكسور وحدُّ النجاح والحالاتُ ومحرّكُ الحكم |
| `references/03-attendance-behavior-notifications.md` | الحصصُ والحضورُ وعتباتُ الغياب والأعذار؛ دليلُ السلوك 2026؛ مركزُ الإشعارات وقنواتُه |
| `references/04-architecture-rules.md` | أين أضع الكود، حدودُ العروض، `core` لا يستورد نازلاً، التصدير، التشفير، المحو، الحرّاس |
| `references/99-test-cases.md` | اختبارُ تفعيل المهارة وجودةِ مخرجها |
