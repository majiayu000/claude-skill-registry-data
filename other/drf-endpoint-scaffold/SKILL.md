---
name: drf-endpoint-scaffold
---

> متى تُستعمل: "DRF endpoints under /api/v1/: serializer, view, selector, RBAC, tests. Trigger: DRF, endpoint, REST API, APIView. نقطة API جديدة، serializer، api/urls.py"

# بناءُ نقطة REST في SchoolOS

الغرض: كلُّ نقطةٍ جديدة تولد بصلاحيّة دورٍ صريحة، ومقيّدةً بمدرسة المستخدم، بعددِ استعلاماتٍ ثابت، ومع اختبارٍ يثبت الثلاثة — وتعبر حرّاسَ CI من أوّل دفع.
السببُ الحيّ: مراجعةُ 2026-09-13 وجدت نقاطاً تكتفي بـ«مسجَّل الدخول» فبلغ الطالبُ سجلَّ حضور المدرسة ودرجاتِ زملائه (المصدر: `tests/test_every_route_is_guarded.py`، `tests/test_borrowings_api_scope.py`).

## متى تُستعمل ومتى لا
- نعم: نقطةٌ جديدة في `/api/v1/` (المسجّلة في `shschool/urls.py` باسم `api_v1`)، أو إنشاءٌ يُضاف لنقطةٍ قائمة.
- لا: `/api/students/search/` وأخواتُها في `operations/api_urls.py` (نقاطٌ داخليّةٌ للشاشات)، ولا شاشاتُ HTML.

## الإجراء
1. **اقرأ الأعراف** في `references/00-api-conventions.md` (الصلاحيّات، الترقيم، الوسائط، سقوفُ الملفّات).
2. **ولّد الهيكل** من جذر شجرتك (بايثون المضيف يكفي؛ لا يحتاج Django):
   ```bash
   python .claude/skills/drf-endpoint-scaffold/scripts/scaffold_endpoint.py --app transport --model BusRoute \
       --name bus-routes --fields id,area_name --school-path bus__school --order-by area_name,id \
       --permission IsStaffMember --readonly
   ```
   للإنشاء: `--write-fields a,b --unique-key b` بدل `--readonly`. يتحقّق من وجود التطبيق والنموذج والصلاحيّة، ويرفض `__all__` و`school` في حقول الإنشاء، وينذر بغياب قيدٍ فريدٍ أو ترتيبٍ أو حقل `school`.
3. **وزّع الكتل** من `<app>/_scaffold_<name>.py`: الـselector إلى ملفّ selectors المجال، والخدمةُ إلى خدمات التطبيق، والـserializer والـview إلى وحدةٍ جديدة `api/views_<name>.py` (السابقة `api/views_erasure.py`)، والمسارُ إلى `api/urls.py`. ثمّ **احذف ملفَّ التجهيز** — يتجاهله git (`_*.py`) فلن يذكّرك به `git status`.
4. **اكتب ما عليه `NotImplementedError`** في `tests/test_<name>_api.py` (`make_row`، و`payload` للإنشاء) — الاختبارُ يسقط حتّى تكتبه، عمداً.
5. **أضِف `select_related`/`prefetch_related`** لكلّ علاقةٍ يقرؤها الـserializer حتّى يخضرّ اختبارُ الثبات (مهارة nplus1-hunter).
6. **شغّل في حاوية جلستك:** اختبارَك، ثمّ `tests/test_every_route_is_guarded.py` و`tests/test_api_contract.py` و`tests/test_file_size.py` (بأمر الاختبار في `CLAUDE.md`)، ثمّ ruff بإصدار CI. التفصيل في `references/02-testing.md`.

## القواعد وأسبابها
- **صلاحيّةُ دورٍ من `api/permissions.py`، لا `IsAuthenticated` وحدها.** الحارسُ `tests/test_every_route_is_guarded.py` يسقط أيَّ مسارٍ صلاحيّتُه «مسجَّل الدخول» أو «الجميع» ما لم يُسمَّ في `GUARDED_INSIDE`/`OPEN_BY_DESIGN` بسببه. و`permission_classes = [IsTeacherOrAdmin]` تستبدل الافتراضيَّ (`IsAuthenticated` في `REST_FRAMEWORK`) وهي تفحص المصادقةَ بنفسها.
- **المدرسةُ من المستخدم لا من الطلب.** `_school(request)` = `request.user.get_school()` (`api/views.py`)، والاستعلامُ يبدأ منها بالمسار الصحيح للنموذج (`school`، أو `class_group__school`، أو `bus__school`). ولا `school` في حقول الكتابة: من يرسلها يكتب في مدرسةٍ أخرى.
- **حقولٌ صريحة، لا `__all__`.** الإضافةُ اللاحقة لحقلٍ شخصيٍّ في النموذج تخرج في الـAPI بلا مراجعة؛ القائمةُ الصريحة تجعل كلَّ عرضٍ قراراً (مهارة pdppl-pii-audit).
- **الإنشاءُ idempotent بقيدٍ في القاعدة.** `get_or_create` بلا `UniqueConstraint` على المفتاح يسبق فيه طلبان متزامنان فيتكرّر الصفّ (وثائق Django: `get_or_create`). مثالُ الإصدار السابق (`Subject` على `code`) بلا قيدٍ كهذا، و`code` فيه `blank=True` — فالمفتاحُ الفارغ يدمج موادَّ مختلفة (`operations/models/schedule.py`).
- **ترتيبٌ حتميٌّ لكلّ قائمةٍ مرقّمة.** نموذجٌ بلا `Meta.ordering` (مثل `BusRoute`) يكرّر صفوفاً ويُسقط أخرى بين الصفحات؛ مرّر `--order-by`.
- **لا تكبر `api/views.py`:** 915 سطراً وسقفُ الملفّ الجديد 1000 (`tests/file_size_ratchet.py`، 2026-09-28) — النقطةُ الجديدة في وحدتها.
- **ما يزيد عن 300ms مهمّةٌ خلفيّة؛** والتصديرُ بالآليّة المركزيّة (ADR-0007، `core/exports/`) لا في طلب API.

## فخاخٌ حقيقيّة
- خطأ: `client.force_authenticate(user)` أو `APIClient` في الاختبار. الصواب: `Client().force_login(user)` — `SchoolPermissionMiddleware` يفحص جلسةَ Django ويردّ `/api/` بـ401 قبل DRF (`core/middleware.py`)؛ مُثبَت: الاختبارُ القديم أخذ 401 حيث توقّع 200 و403.
- خطأ: ملفُّ الاختبار في `<app>/tests/`. الصواب: `tests/test_<name>_api.py` — fixtures الأدوار في `tests/conftest.py` لا تُرى خارجه (الاختبارُ القديم: «fixture 'teacher_user' not found»).
- خطأ: `django_assert_num_queries(4)` برقمٍ «يُضبط بعد أوّل تشغيل». الصواب: صفٌّ واحد مقابل ثلاثة بعد إحماء (نمط `tests/test_n_plus_one_queries.py`).
- خطأ: `assert r.status_code in (201, 400)` «مؤقّتاً». الصواب: `NotImplementedError` حتّى تُكتب الحمولة — القيمةُ المؤقّتة يجب أن تُفشل (ذاكرة `feedback_placeholders_must_fail.md`).
- خطأ: `fields = "__all__"` في serializer الكتابة. الصواب: قائمةٌ بلا `school`، واختبارُ `test_school_cannot_be_injected`.
- خطأ: `.order_by("-created_at")` لكلّ نموذج. الصواب: كثيرٌ من النماذج بلا `created_at` (`Subject`، `BusRoute`) — `Meta.ordering` أو `--order-by`.
- خطأ: «النماذجُ ترث `SchoolScopedModel`». الصواب: أربعةُ نماذج فقط ترثه؛ أغلبُها حقلُ `school` صريح أو مدرسةٌ عبر علاقة.
- خطأ: «المسار الوحيد `D:\shschool_mvp`». الصواب: اعمل في شجرتك (`CLAUDE.md`، القاعدة رقم 1).

## المراجع
| الملف | متى تقرأه |
|---|---|
| `references/00-api-conventions.md` | قبل التصميم: المصادقة والصلاحيّات والترقيم والوسائط والحرّاس التي تمرّ عليها كلُّ نقطة |
| `references/01-layers.md` | حين توزّع الكتل: ما يذهب إلى selector وخدمةٍ وserializer وview، ومثالٌ كاملٌ مصحَّح |
| `references/02-testing.md` | حين تكتب الاختبار أو تفهم سقوطه، وما يشغّله CI على النقطة |
| `references/99-test-cases.md` | عند تعديل الوصف أو الجسم أو السكربت |
