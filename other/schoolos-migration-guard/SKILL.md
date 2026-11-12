---
name: schoolos-migration-guard
---

> متى تُستعمل: "Django migration safety: expand/contract, NOT NULL, indexes, RunPython. Trigger: migration, makemigrations, schema change. هجرة، تعديل models.py"

# حارس هجرات SchoolOS

الغرض: أن تمرّ كلُّ هجرةٍ على قاعدةٍ حيّةٍ بلا توقّفٍ ولا فقدٍ ولا كسرٍ للنسخة المنشورة، وأن تعبر بوّابةَ CI من أوّل مرّة.
السببُ الحيّ: 2026-09-11 حذفت هجرةٌ عموداً (`spread_days_scope`) فسقطت ثماني صفحاتٍ في كلّ شجرةٍ أخرى ساعات (المصدر: `CLAUDE.md`، قسم «الهجرات: توسيعٌ ثمّ تقليص»).

## متى تُستعمل ومتى لا
- نعم: أيُّ ملفٍّ جديدٍ أو معدَّلٍ تحت `*/migrations/`، وأيُّ تعديلٍ في نموذج، ومراجعةُ طلبٍ فيه هجرة.
- لا: هجراتُ `roadmap/migrations/` — لجلسة «خارطة التجويد» وحدها، وغيرُها يُبلغها برمز البند ورقم الطلب (المصدر: `CLAUDE.md`، قسم الخارطة الحيّة). ولا قرارُ «هل يُشفَّر الحقل» (pdppl-pii-audit).

## الإجراء
1. **حدِّد الخطوة قبل الكتابة:** توسيعٌ (أضِف وانقل القراءة) أم تقليصٌ (احذف ما لم يعد يُقرأ) — لا الاثنان في إصدارٍ واحد. التفصيل: `references/00-policy-and-ci.md`.
2. **ولّد الهجرة في شجرتك** ثمّ قارن رقمَها بآخر هجرةٍ للتطبيق على `origin/main` (`git fetch` ثمّ `git ls-tree --name-only origin/main <app>/migrations/`) — هجرتان من جلستين على الأصل نفسِه تُسقطان migrate. انظر `references/03-parallel-sessions.md`.
3. **شغّل الحارس داخل حاوية جلستك** (بادئةُ `$DC` معرَّفةٌ في `references/03-parallel-sessions.md`):
   `$DC python .claude/skills/schoolos-migration-guard/scripts/check_migration.py --file <app>/migrations/<file>.py --sql`
   يحلّل الملفَّ، ويولّد SQL بـ`sqlmigrate` ويصنّفه، ثمّ يمرّره على محلّل `django-migration-linter` نفسِه الذي تستدعيه البوّابة — فسطرُ «[مدقّق CI] خطأ» يعني أنّ CI سيسقط. رمزُ الخروج 1 عند أيّ 🔴.
4. **عالج كلَّ 🔴 بالبديل المذكور** في `references/01-operations-catalog.md`، وراجع كلَّ 🟠 بحجم الجدول.
5. **طبّقها على قاعدة جلستك واختبر:** `$DC python manage.py migrate` ثمّ `$DC python manage.py makemigrations --check --dry-run` (بوّابةٌ في CI أيضاً) ثمّ الاختبارات بأمر `CLAUDE.md`.
6. **في وصف الطلب:** أيُّ خطوةٍ هذه (توسيع/تقليص)، وما يعكسها، وأنّ الحارس خرج 0. ثمّ الدفعُ والتحويل وفق schoolos-flow.

## القواعد وأسبابها
- **الهدّامُ خطوةٌ ثانيةٌ في إصدارٍ لاحق.** حذفُ عمودٍ أو جدولٍ أو إعادةُ تسميتهما أو NOT NULL بلا افتراض يُسقط الشيفرةَ التي ما زالت تعمل: الهجراتُ تجري في مرحلة `preDeploy` والنسخةُ القديمة وعاملُ Celery يخدمان (المصدر: `scripts/railway-predeploy.sh`، `.railway/railway.ts`)، وكلُّ شجرةٍ أخرى على شيفرتها. البوّابةُ تسقطه ولو كان صحيحاً منطقيّاً، والاستثناءُ قرارٌ في مراجعة الطلب (المصدر: `CLAUDE.md`).
- **عمودٌ NOT NULL جديد = `default=` و`db_default=` معاً.** بـ`default=` وحده يضيف Django العمودَ بافتراضٍ ثمّ يُسقطه (`DROP DEFAULT`) فتسقط كتابةُ النسخة القديمة، والبوّابةُ تُسقطه (NOT_NULL) — مُثبَتٌ بـ`sqlmigrate` و`lintmigrations` في مختبرٍ على PostgreSQL 18. السابقة: `operations/migrations/0053_excuse_review.py`.
- **الفهرسُ على جدولٍ قائمٍ كبير = `AddIndexConcurrently` و`atomic = False`**؛ والقيدُ الفريدُ وتغييرُ نوع العمود على جدولٍ قائم تُسقطهما البوّابة (ADD_UNIQUE، ALTER_COLUMN). السابقة: `operations/migrations/0055_attendance_exit_partial_index.py`.
- **RunPython يرى نموذجاً تاريخيّاً:** بلا `save()` ولا خصائص ولا مديراتٍ مخصّصة (`.live()`…) — مُثبَتٌ في المختبر. فما يملؤه `save()` (ثلاثيّةُ `national_id`/`phone`: خامٌ و`_encrypted` و`_hmac`) يُحسب صراحةً بـ`encrypt_field`/`hmac_field`. السابقة: `core/migrations/0020_populate_national_id_hmac_encrypted.py`. التفصيل: `references/02-data-migrations.md`.
- **كلُّ RunPython/RunSQL له عكس** (دالّةٌ أو `noop` صريحٌ بسببه). البوّابةُ تحذّر فقط؛ المهارةُ أشدّ لأنّ فشلَ النشر بلا عكسٍ إصلاحٌ يدويٌّ على الإنتاج.
- **لا تعدّل هجرةً طُبّقت على أيّ قاعدة** (جلستك أو المعاينة): Django لا يعيد تطبيقَ ما سُجّل، فتبقى القاعدةُ على المسوّدة صامتةً (المصدر: ذاكرة `feedback_local_roadmap_db_drift.md`). أنشئ هجرةً جديدة، أو ارجع بها (`migrate <app> <السابقة>`) ثمّ عدّل.
- **ما يزيد عن 300ms لا يُحشر في هجرة:** تعبئةُ جدولٍ كبير أمرُ إدارةٍ أو مهمّةٌ خلفيّة بعد النشر (المصدر: «القرارات الهندسيّة» في `~/.claude/CLAUDE.md`).

## فخاخٌ حقيقيّة
- خطأ: `AddField(..., field=models.TextField(default=""))` لعمودٍ إلزاميّ. الصواب: `models.TextField(default="", db_default="")`.
- خطأ: `RemoveField` في الطلب نفسِه الذي أوقف قراءةَ الحقل. الصواب: طلبٌ يوقف القراءةَ والكتابة ويُنشر، ثمّ طلبٌ لاحقٌ بالحذف (السابقة: حذفُ `StaffEvaluation` بعد #417، `shschool/settings/testing.py`).
- خطأ: `RunPython(forward)` وحده. الصواب: `RunPython(forward, backward)` أو `RunPython(forward, migrations.RunPython.noop)` مع تعليقٍ يشرح لماذا لا عكس.
- خطأ: في RunPython: `User.objects.filter(...).update(phone=new)`. الصواب: دفعاتٌ تحسب `phone_encrypted` و`phone_hmac` بالدالّتين ثمّ `bulk_update` بالأعمدة الثلاثة.
- خطأ: `AddIndex` على `studentattendance`. الصواب: `AddIndexConcurrently` في هجرةٍ وحدَها بـ`atomic = False`.
- خطأ: `default=uuid.uuid4` مع `unique=True` في `AddField`. الصواب: `null=True` أوّلاً، ثمّ تعبئةٌ لكلّ صفّ، ثمّ القيد — الدالّةُ تُحسب مرّةً واحدةً لكلّ الصفوف القائمة (مُثبَتٌ بـ`sqlmigrate`).
- خطأ: تعديلُ `0056_x.py` بعد تطبيقها على قاعدة جلستك «لأنّها لم تُدفع بعد». الصواب: ارجع بها أوّلاً، أو هجرةٌ جديدة.
- خطأ: «المسارُ الوحيد `D:\shschool_mvp` ولا تعدّل في worktrees» — أُلغيت 2026-09-08. الصواب: اعمل في شجرتك على قاعدتها (`CLAUDE.md`، القاعدة رقم 1).

## المراجع
| الملف | متى تقرأه |
|---|---|
| `references/00-policy-and-ci.md` | قبل أيّ هجرةٍ هدّامة، أو حين تسقط وظيفةُ المدقّق في CI وتريد معرفةَ ما تفحصه بالضبط |
| `references/01-operations-catalog.md` | لكلّ عمليّةٍ في ملفّك: خطرُها، وSQL الذي تولّده، وحكمُ البوّابة، والبديل |
| `references/02-data-migrations.md` | حين تكتب RunPython/RunSQL، ولا سيّما على حقولٍ مشفّرة أو `AuditLog` أو جدولٍ كبير |
| `references/03-parallel-sessions.md` | لتشغيل الأوامر في حاوية جلستك، أو عند تعارض ترقيم، أو قاعدةٍ متأخّرةٍ عن main |
| `references/99-test-cases.md` | عند تعديل الوصف أو الجسم — حالاتُ التفعيل واختباراتُ المخرج |
