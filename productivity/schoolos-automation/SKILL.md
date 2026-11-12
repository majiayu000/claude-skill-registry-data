---
name: schoolos-automation
---

> متى تُستعمل: "Use for turning any recurring, scheduled or event-driven SchoolOS job into code that runs by itself, never a Claude Code scheduled task (D-50م): choosing Celery beat, GitHub Actions (cron or PR event) or Windows Task Scheduler, and designing it (idempotent, timeout, bounded retry, lock, exit code, silent-failure alert, tests, env secrets, no PII). Trigger on: cron, beat_schedule, periodic, nightly, weekly report, Task Scheduler, PowerShell job, watch_once, REP-10, MAE-06/09/11, worker-heartbeat, silent failure, 0801. استخدمها عند نقل مهمّةٍ دوريّةٍ من Claude إلى شيفرة، أو إضافة مهمّةٍ مجدولةٍ واختيار مكانها، أو أتمتةٍ «تنجح» ولا تعمل — ولو قيل «خلّ التقرير يطلع لحاله كلّ أحد» أو «ذكّر الجلسة كلّ يوم الساعة 7». ليست لـ: هجرة بياناتٍ لمرّة (schoolos-migration-guard)، حرّاس بوّابة الطلب (regression_guards.md)، الدمج والنشر (schoolos-flow، schoolos-deploy)، git (schoolos-git-safety)، تصديرٍ بطيءٍ عند الطلب (core/exports)، تذكيرٍ شخصيّ، تتبّع خطأ Celery (schoolos-debugger)."

# أتمتةُ الجدولة في الكود — SchoolOS

الغرض: كلُّ عملٍ دوريٍّ في المنصّة يصير شيفرةً تعمل وحدَها، ولا يبقى في Claude Code مهمّةٌ مجدولةٌ واحدة؛ والجلساتُ للحكم والتقدير فقط.
المصدر: `decisions.md` (D-50م، D-42م) و`projects/schoolos/tabs.json` (ميثاق «0801 · أتمتة الجدولة في الكود») في حزمة المايسترو.

## متى تُستعمل ومتى لا
- تُستعمل: طلبُ «شغّلها كلَّ …»، نقلُ مهمّةٍ من Claude Code (REP-10، المراقب `watch_once.py`)، مدخلٌ جديدٌ في `beat_schedule`، مسارُ عملٍ فيه `schedule:`، سكربتٌ لجدولة ويندوز، أو التحقيقُ في أتمتةٍ «تنجح» ولا تعمل.
- لا تُستعمل: إصلاحُ بياناتٍ لمرّةٍ واحدة، أو بوّاباتُ طلب الدمج، أو خطواتُ الدمج والنشر (أحِل إلى `schoolos-flow`)، أو أوامرُ git (أحِل إلى `schoolos-git-safety`).

## الإجراء
1. اجرد أوّلاً: هل الأتمتةُ موجودةٌ في beat أو Actions أو جدولة ويندوز؟ الجدولُ الحيّ في `references/00-inventory.md`؛ لا تبنِ ما يعمل (الحزمةُ الليليّةُ وتقريرُ الفروع الأسبوعيّ موجودان أصلاً).
2. اختر المكانَ بشجرة القرار (`references/01-decision-tree.md`) — بسؤال «ماذا تحتاج أن تلمس؟» لا «أين أسهل؟».
3. صمّم بقائمة الفحص (`references/02-automation-checklist.md`) كاملةً؛ صفٌّ حاسمٌ واحدٌ ناقصٌ يوقف الاعتماد.
4. حدّد المخرجَ بالعقد (`references/03-output-contract.md`): أين يقرأ 0203 الفشلَ، وأين يقرأ 0702 الاتّجاه، وكيف يُكتشف **الغياب** لا الفشلُ وحده.
5. ابدأ من القالب المناسب (`references/04-templates.md`) وشغّل المدقّق على ملفّك:
   `python scripts/audit_automation.py <مسار> [--json]` (رمزُ الخروج 1 عند FAIL).
6. اختبر محلّيّاً في شجرتك (أوامرُ الاختبار في CLAUDE.md)، ثمّ امضِ في الفلو كاملاً: معاينةٌ على 8500 واعتمادٌ ثمّ دفعٌ ثمّ الدمجُ والنشرُ لجلسة النشر — التفاصيلُ في `schoolos-flow`.
7. بعد النشر فقط: أوقِف ما يقابلها في Claude Code (إيقافٌ `enabled=false` لا حذف)، وسجّل ذلك لـ«0102» والمايسترو، وبطاقةٌ لأيّ فجوةٍ تبقى.

## القواعدُ وأسبابها
- لا مهمّةَ مجدولةً في Claude Code، ولا `schedule`/`loop`/`CronCreate`/`Monitor` بديلاً — لأنّ المالك أمر بنقل الجدولة إلى شيفرةٍ تعمل بلا جلسة (D-50م)، ولأنّ مهمّةَ REP-10 عادت تعمل خلافاً لقرار إيقافها (D-42م). المصدر: `decisions.md`.
- جدولةُ GitHub بأفضل جهدٍ لا بضمان: قيس 2026-09-25 نحو 7% و4.4% من الوتيرة المتوقَّعة لمراقبَي 15 و10 دقائق. فلا يُبنى عليها إنذارُ غيابٍ ولا وتيرةٌ دون الساعة. المصدر: `tests/test_monitoring_claims_are_honest.py`، `.github/workflows/monitor.yml`.
- beat نسخةٌ واحدةٌ فقط، والوقتُ فيه بتوقيت قطر (`timezone="Asia/Qatar"`)، وcron في Actions بـUTC (الدوحة − 3). المصدر: `scripts/railway-beat.sh`، `shschool/celery.py`.
- المهمّةُ تُعاد تلقائيّاً (`task_acks_late` و`task_reject_on_worker_lost`، حتى 3 محاولات)، فعدمُ التكرار (idempotent) شرطٌ لا تحسين. المصدر: `shschool/celery.py`.
- الفشلُ الصامتُ أخطرُ من الخطأ: نسخُ ذاكرة المشروع تعطّل أربعةَ أشهرٍ ونصفاً ومهمّةُ ويندوز «ناجحة» لأنّ السكربت كتم أخطاءه. فالمراقَبُ عمرُ آخر نجاحٍ لا نتيجةُ المهمّة. المصدر: `project_claude_backup_stale_lock_2026_09_28`.
- المستودعُ عامّ: أسماءُ المتغيّرات فقط، ولا عنوانَ إنتاجٍ حرفيٍّ ولا سرَّ ولا رقمَ شخصيّ في شيفرةٍ أو سجلّ. المصدر: `feedback_no_real_ids_in_code`، `core/backup_status.py`.

## فخاخ
- خطأ: «أجدولها مهمّةَ Claude كلَّ 30 دقيقة مؤقّتاً» ← الصواب: لا مؤقّت: جدولةُ ويندوز لسكربتٍ محلّيّ أو beat؛ وحتى تُبنى يشغّلها صاحبُها يدويّاً.
- خطأ: نقلُ `prune_local_branches.py` حرفيّاً إلى beat ← الصواب: المنصّةُ على Railway لا ترى فروعَ الجهاز؛ البعيدُ عبر واجهة GitHub في مجمِّعٍ لمركز قيادة الجودة، والمحلّيُّ يبقى سكربتَ ويندوز. المصدر: `project_rk_metrics_native_collector_backlog`.
- خطأ: مراقبُ «كلَّ 10 دقائق» في Actions يُعدّ ضماناً ← الصواب: نبضةٌ تُختم في Redis ويُحكم بعمرها (`core/worker_heartbeat.py`)، والفحصُ الخارجيّ ثانويّ.
- خطأ: `@shared_task` بلا `name=` ← الصواب: اسمٌ صريحٌ ثابت؛ نقلُ الملفّ بين التطبيقات يغيّر الاسمَ الافتراضيّ فيُرسل beat اسماً بلا عامل. المصدر: `tests/test_beat_tasks_registered.py`.
- خطأ: عدّلتُ المهمّةَ ولم يتغيّر السلوك ← الصواب: العاملُ لا يعيد تحميلَ الكود: `restart worker` بأمر خادم الجلسة في CLAUDE.md. المصدر: `feedback_worker_no_hot_reload`.
- خطأ: `ErrorActionPreference='SilentlyContinue'` أو `except: pass` في سكربت ويندوز ← الصواب: `Stop` وexit غيرُ صفريّ وملفُّ فشلٍ ظاهر (`~/.claude/scripts/auto_backup.ps1` v2 مثالاً).
- خطأ: `TZ=Asia/Qatar date` في Git Bash ← الصواب: يطبع UTC صامتاً؛ احسب UTC+3 أو اكتب الوقتَ بإزاحته (`isoformat()`). المصدر: `feedback_doha_time_on_windows`.
- خطأ: «أعاين الجدولةَ على 8500» ← الصواب: المعاينةُ بلا beat؛ اعرض الأثرَ المرئيّ (لوحة، صفحة، ناتجُ أمرٍ بـ`--dry-run`) والجدولةُ يثبتها الاختبار. المصدر: CLAUDE.md (المعاينة المركزيّة).
- خطأ: تعديلُ `.github/workflows/*` كأيّ ملفّ ← الصواب: مصنِّفُ الأذونات يحجبه («Modify Shared Resources»)؛ اطلب إذنَ المالك الصريح ولا تلتفّ. المصدر: `feedback_ask_before_push`.
- خطأ: «أيقظ الجلسةَ 0201 كلَّ صباح بالكود» ← الصواب: الشيفرةُ لا تراسل جلسة؛ هذا بندُ دراسةٍ للمالك (`references/05-session-wakeup-study.md`).

## المراجع
| الملف | متى تقرؤه |
|---|---|
| `references/00-inventory.md` | قبل أيّ بناء: ما يعمل الآن وأين، وما يُنقل، والفجواتُ المعروفة |
| `references/01-decision-tree.md` | لاختيار المكان: beat أو Actions أو ويندوز أو «لا يُؤتمت» |
| `references/02-automation-checklist.md` | عند التصميم والمراجعة: البنودُ العشرة وكيف تتحقّق في كلّ منصّة |
| `references/03-output-contract.md` | عند تحديد المخرج والسجلّ وإنذار الغياب لـ0203 و0702 |
| `references/04-templates.md` | عند الكتابة: هياكلُ أمرٍ ومهمّةٍ ومسارِ عملٍ وسكربتِ ويندوز |
| `references/05-session-wakeup-study.md` | حين يُطلب «تذكيرُ الجلسات الثابتة بمواعيدها» |
| `references/99-test-cases.md` | لاختبار تفعيل المهارة وجودة الجواب |
| `scripts/audit_automation.py` | على كلّ ملفّ أتمتةٍ قبل «جاهزٌ للمعاينة» (اختباراتُه `scripts/test_audit_automation.py`) |
