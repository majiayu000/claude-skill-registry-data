---
name: schoolos-quality-guards
---

> متى تُستعمل: "Use for SchoolOS quality guards and post-deploy measurement: which CI guard, ratchet or budget failed, whether it blocks the merge, reproducing it with pinned versions (ruff 0.4.4, mypy 1.10.0), live budget margins, the nine lanes' KPI recipes, and the deviation card to 0204. Trigger on: «ملخص بوابة الجودة» red, axe-a11y, test_px_tokens, test_file_size, mypy_ratchet, baseline.json, detect-secrets, deploy-window, Nightly, Lighthouse, MAX_SHIPPED_BYTES, KPI, PK/RK/LK. استخدمها عند فشل حارسٍ أو سقّاطة (ولو بعد إصلاحين)، و«هل يحجب الدمج؟»، و«نقص — اخفض السقف»، وقبل إضافة CSS أو ملفٍّ طويل، وقياس المؤشّرات بعد النشر أو أسبوعيّاً (0702)، وبطاقة الانحراف — ولو قيل «CI أحمر وما فهمت ليش» أو «كم باقي في ميزانيّة CSS؟» أو «يمرّ عندي ويسقط في CI». ليست لـ: الدفع والدمج (schoolos-flow)، غيت (schoolos-git-safety)، الهجرات (schoolos-migration-guard)، رموز الألوان (web-design-mastery)، عطل الإنتاج (schoolos-watch)، هجرة الخارطة (schoolos-roadmap-sync)، N+1 (nplus1-hunter)، PII (pdppl-pii-audit)."

# حرّاسُ الجودة وقياسُ المؤشّرات — SchoolOS

الغرض: أن تعرف أيَّ حارسٍ فشل وماذا يحمي وهل يحجب الدمج، وتُعيد إنتاجه محلّيّاً بالإصدارات التي تحكم بها البوّابة، وتقيس مؤشّرات المسارات بقيمةٍ وتاريخٍ وأداة — لا تخميناً ولا نقلاً من ذاكرة.
الخريطةُ الكاملة للحرّاس في `docs/governance/regression_guards.md`؛ هذه المهارةُ تلخّصها وتضيف ما ليس فيها (الإصدارات، الانجراف، وصفات المسارات، البطاقة).

## متى تُستعمل ومتى لا
- جلسةُ «0702 · مراقبات الجودة»: بعد كلّ نشرٍ (قياسُ ما مسّه)، وأسبوعيّاً (قراءةُ المسارات التسعة)، وعند كلّ انحراف.
- أيُّ جلسة تنفيذ (04) يسقط فيها حارس، أو تنوي إضافةَ CSS أو ملفٍّ طويل أو تسجيلَ خطّ أساس.
- لا: متى تدفع ومن يدمج (schoolos-flow)؛ إنذارُ عطلٍ حيّ في الإنتاج (0203)؛ كتابةُ هجرة الخارطة (0701 وحدَها).

## الإجراء
أ. حارسٌ فشل (أيّ جلسة):
1. اقرأ اسمَ الوظيفة الفاشلة ثمّ `references/00-guards-map.md`: ما الذي يحميه، وهل هو داخل `gate-summary` أو `Security Summary` (وحدهما يحجبان).
2. حدِّد نوعَه: سقّاطةٌ أم سقفٌ أم ثابت (`references/01-budgets-and-ratchets.md`). «نقص ولم يُسجَّل» ليس خطأً في شيفرتك: سجِّل النقصَ في الطلب نفسِه.
3. أعِد إنتاجَه محلّيّاً بالإصدار المثبَّت (`references/02-running-locally.md`) قبل أيّ إصلاح؛ وبعد إصلاحَين فاشلَين لا ثالثَ قبل إعادة إنتاج البوّابة كاملةً.
4. أصلِح السبب، لا الحارس. رفعُ سقفٍ أو تخفيفُ شرطٍ قرارُ المالك وحدَه.

ب. بعد النشر (0702):
1. بعد `git fetch`: `python .claude/skills/schoolos-quality-guards/scripts/guard_margins.py --repo . --ref origin/main` (أو المسارُ حيث ثُبّتت المهارة) — هوامشُ السقوف وخطوطُ الأساس والإصداراتُ من الملفّات الحيّة مع sha وتاريخ، بلا خادمٍ ولا checkout.
2. قِس المؤشّرات التي مسّها النشرُ بوصفاتها (`references/03-track-measurement-recipes.md`).
3. الانحرافُ بطاقةٌ إلى «0204 · البوابة الموحّدة»، والقراءةُ إلى «0701 · تحديث الخارطة» (`references/04-deviation-card.md`).

ج. أسبوعيّاً: قراءةُ المسارات التسعة؛ مسارٌ بلا قراءةٍ أحدث من أسبوعين يُذكر في التقرير.

## القواعد وأسبابُها
- الحاجبُ فحصان فقط في حماية `main`: «ملخص بوابة الجودة» و«Security Summary» (strict). وظيفةٌ خارج `needs` في الملخّص لا تحجب شيئاً ولو احمرّت — فحارسٌ جديدٌ يُوضع في وظيفةٍ مدرجة. المصدر: `gh api …/branches/main/protection/required_status_checks` (قيس 2026-09-28)، `regression_guards.md` §3.
- الأرقامُ من الملفّ الحيّ لا من الوثيقة: `regression_guards.md` لقطةٌ بتاريخ 2026-09-25 وقد تقادمت أرقامُها (سقفُ المصغَّر فيها 260KB والحيُّ 269KB). المصدر: رأس الوثيقة نفسُها.
- السقّاطةُ تسقط بالنقص كما بالزيادة، كي لا يصير التحسّنُ هامشاً يُنفق بصمت. المصدر: `regression_guards.md` §1.
- الإصدارُ الذي يحكم هو المكتوبُ في سير العمل، لا `requirements-dev.txt`: ruff 0.4.4 وmypy من `requirements-mypy.txt`، وbandit وpip-audit وdjango-migration-linter في الملفّين بإصداراتٍ مختلفة. المصدر: `.github/workflows/*.yml`، والسكربت يطبع الانجراف.
- «مرّ محلّيّاً» قد يعني «تُخطّي»: حرّاسُ المتصفّح تبدأ بـ`importorskip` فتتخطّى بلا Playwright. المصدر: `tests/test_web_vitals_budget.py`، `tests/test_mobile_audit.py`.
- لا ادّعاءَ بلا قياس: كلُّ قيمةٍ بتاريخها وأداتها ومرجعها، وما لا اشتقاقَ له يُوسم «اقتراحُ صاحبه لا قياساً». المصدر: `feedback_reproduce_ci_before_refix`، `project_lane_quality_8204`، ميثاق 0702.
- لا تشغّل أمرَ إنتاج؛ القياسُ الذي يحتاج الإنتاج أمرُ قراءةٍ يُجهَّز للمالك. المصدر: `project_ops_track_owner_2026_09_25`، `feedback_auto_classifier_production_actions`.

## فخاخ
- خطأ: `python -m ruff format --check .` على المضيف الصواب: الثنائيّ 0.4.4 نفسُه: `~/ruff044_work/bin/ruff.exe` (المضيف 0.15.9 يخالفه في التنسيق). المصدر: `feedback_ruff_pinned_version`.
- خطأ: `python -m tests.mypy_ratchet --update` على الأهداف كلِّها الصواب: عدّل سطرَ الملفّ والمجموعَ يدويّاً ثمّ `git diff` — التشغيلُ الكامل غيرُ حتميّ ومحا مدخلاتٍ لا علاقةَ لها. المصدر: `feedback_reproduce_ci_before_refix`.
- خطأ: «الخامُّ فيه 12KB فأضيف CSS» الصواب: السقفُ الأضيق اليوم هو المصغَّر: 58 بايتاً (2026-09-28، 81bc4937). قِس الاثنين.
- خطأ: رفعُ `MAX_SHIPPED_BYTES` أو `OFF_SCALE_*` ليمرّ الطلب الصواب: قلِّص مقابلها، أو اعرض القرارَ على المالك (VD8). المصدر: `tests/test_css_budget.py`.
- خطأ: «Nightly أحمر إذن الطلب مكسور» الصواب: Nightly وquality.yml وLighthouse ولقطاتُ الهويّة لا تحجب الدمج؛ وحمرةٌ قد تُخفي حمرةً خلفها — افحص ما بعد الإصلاح الأوّل فوراً. المصدر: `regression_guards.md` §5.
- خطأ: بطاقةٌ فيها رقمُ تشغيل CI (11 خانة) الصواب: اسمُ السير وتاريخُه: حارسُ السجلّ يرفض كلَّ رقمٍ من 9 خانات فأكثر. المصدر: `delivery_manager_work/tools/ledger.py`.

## المراجع
| الملف | متى تقرأه |
|---|---|
| `references/00-guards-map.md` | فشلت وظيفةٌ في CI، أو تسأل: من يحجب الدمج وأين يعيش الحارس |
| `references/01-budgets-and-ratchets.md` | تحتاج رقمَ سقفٍ أو هامشاً، أو تسجيلَ نقصٍ، أو تشكّ في رقمٍ منقول |
| `references/02-running-locally.md` | تعيد إنتاج حارسٍ محلّيّاً، أو فشل إصلاحان |
| `references/03-track-measurement-recipes.md` | تقيس مؤشّراً لمسارٍ من التسعة بعد النشر أو أسبوعيّاً |
| `references/04-deviation-card.md` | تكتب بطاقة انحراف لـ0204 أو قراءةً لـ0701 |
| `references/99-test-cases.md` | تختبر تفعيلَ المهارة وجودةَ جوابها |
| `scripts/guard_margins.py` | هوامشُ السقوف والسقّاطات والإصدارات من مرجعٍ في git بلا خادم |
