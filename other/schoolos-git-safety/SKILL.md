---
name: schoolos-git-safety
description: "Use for any git action in the SchoolOS repo and its .claude/worktrees shared by parallel sessions: commit, push, update from main, conflicts, switching branches, setting work aside, «really merged?» after squash, removing worktrees or branches. Trigger on: git add/commit/push/rebase/merge/stash/reset/worktree/branch -D, blocked by guard_git, force push. استخدمها ولو لم تُذكر غيت: «أودِع وادفع»، «حدّث فرعك من main»، «الحارس حجب الأمر»، «هل اندمج الفرع؟»، «نظّف الأشجار». ليست لـ: متى تدفع ومن يدمج (schoolos-flow)، الهجرات (schoolos-migration-guard)."
---

# أمانُ غيت في المحادثات المتوازية

مستودعٌ واحدٌ ورأسٌ ومكدّسُ خبيئةٍ ومراجعُ مشتركةٌ بين الجذر وعشرات الأشجار، وعلى كلّ شجرةٍ جلسةٌ تعمل الآن،
والمستودعُ عامّ. هذه المهارة تنقل ما يمنع جلستك من إبطال عمل غيرها أو نشرِ ما لا يُنشر، وكيف تتعافى إن وقع.

## متى تُستعمل ومتى لا

- نعم: كلُّ أمرٍ يكتب في غيت (add/commit/push/merge/rebase/reset/checkout/switch/stash/tag/branch/worktree)، وكلُّ
  حكمٍ «مدموج/يتيم/آمنٌ للحذف»، وكلُّ `git status` فيه ما لم تتوقّعه، وكلُّ أمرٍ حجبه الحارس.
- لا: متى تدفع ولمن تسلّم الطلب ومن يدمج (schoolos-flow)؛ هجرةٌ آمنة؟ (schoolos-migration-guard)؛ مستودعُ الوثائق
  الخاصّ وغيرُه (قواعدُ الحارس المحلّيّة لا تسري عليه).

## الإجراء

1. **اعرف أين أنت:** `git rev-parse --show-toplevel` و`git branch --show-current`. شجرتُك وحدَها؛ لا `cd` ولا `-C`
   إلى شجرة غيرك، ولا تبديلَ لفرع الجذر `D:\shschool_mvp` من جلسة شجرة.
2. **قبل كلّ إيداع `git status` كاملاً** (بلا `head`). ملفٌّ لم تلمسه = عملُ جلسةٍ أخرى: قِف واسأل، ولا تضمّه.
3. **أضِف بمساراتٍ صريحة** ثمّ أودِع. إن فشل الإيداعُ أوّلَ مرّةٍ لأنّ pre-commit عدّل الملفّ: `git add` للمسارات
   نفسِها وأعِد — لا `--no-verify` ولا `SKIP=`.
4. **قبل الدفع** شغّل الفحص (لا يكتب شيئاً عدا جلبِ origin؛ رمزُ 2 = لا تدفع):
   `python .claude/skills/schoolos-git-safety/scripts/git_preflight.py --fetch --gh`
5. **ادفع بعد اعتماد المالك وحدَه** (schoolos-flow)، بوجهةٍ صريحةٍ لا تحرّك الرأس:
   `git push origin HEAD:refs/heads/claude/<اسم-المهمّة>`
6. **حدّث من main** بـ`git fetch` ثمّ `git merge origin/main` لفرعٍ منشور (إعادةُ الأساس لغير المنشور وحدَه)، ثمّ
   `git diff origin/main...HEAD` ملفّاً ملفّاً: حلُّ تعارضٍ قد يمحو إصلاحَ غيرك بصمت.
7. **«مدموج؟»** بحالة الطلب والمحتوى لا بعدّ الإيداعات: `git_preflight.py --judge <فرع> --gh` ثمّ
   `03-squash-merge-judgement.md`. لا حذفَ ولا إزالةَ بلا أدلّةٍ وقرارِ المالك.
8. **حُجب أمرُك؟** اقرأ معرّفَ القاعدة وخذ البديلَ من `00-safe-commands.md` §8؛ لا التفاف.

## القواعد وأسبابها

- **اعمل حيث أنت.** قاعدةُ «عدّل في الجذر وحدَه ولا worktree» أُلغيت 2026-09-08؛ ولكلّ شجرةٍ خادمُها وقاعدتُها.
  تبديلُ فرعِ شجرةٍ أخرى يسحب الأرضَ من تحت جلستها. (CLAUDE.md «القاعدة رقم 1» و«غيت في المحادثات المتوازية» البند 1)
- **لا `add -A`/`add .` ولا `commit -a`**: يبتلعان ملفّاتِ جلسةٍ أخرى نصفَ مكتوبة. (البند 2؛ الحارس add-all/commit-all)
- **لا `stash`**: المكدّسُ مشترك، تخبّئ أنت ويستخرج غيرُك. البديل: إيداعٌ مؤقّتٌ **يُقلع** (رأسُ شجرتك يدخل تكاملَ
  8500 خلال دقائق، وإقلاعٌ يفشل مرّتين يُطفئ التكاملَ للجميع)، أو رقعةٌ خارج المستودع. (البند 3؛ `scripts/preview.sh`)
- **لا force ولا دفعَ إلى main ولا حذفَ مرجعٍ بعيد ولا دفعَ جماعيّ**: الفرعُ المنشورُ يتقدّم بإيداعٍ أو دمج؛ وسومُ
  الأرشيف قد تحمل ما لا يُنشر. (الحارس push-force/push-main/push-delete/push-bulk)
- **فحصُ التأخّر والتعارض قبل الدفع**، ودفعُ رأسٍ لا إيداعَ لك فوق main يُغلق طلبَك (#277). (ذاكرة feedback_check_rebase_before_push)
- **الدمجُ بالسحق يخدع `rev-list` و`git cherry` و`branch --merged`**: الحكمُ بطلب الفرع في GitHub (`headRefOid`) ثمّ
  بالمحتوى. (`tools/branch_status.py` في حزمة المايسترو؛ `scripts/prune_local_branches.py`)
- **لا تُزال شجرةٌ فيها غيرُ مودَعٍ أو غيرُ مدفوع، ولا يُحذف فرعٌ لم يُدفع قطّ بلا دليلٍ أو وسم**: لا نسخةَ له في أيّ مكان.
  (CLAUDE.md البند 6؛ ذاكرة feedback_worktree_removal_safety_checks)
- **الحارسُ شبكةُ أمانٍ لا صندوق**: لا يرى ما في سكربت، ولا `worktree remove --force`، ولا تبديلَ فرعِ شجرةٍ أخرى،
  ويغيب في شجرةٍ أساسُها أقدمُ من #649. (`.claude/hooks/guard_git.py`)

## فخاخٌ حقيقيّة

- خطأ: `git add -A && git commit -m "…"` لأنّ «كلَّ التعديلات لي». الصواب: `git status` ثمّ `git add <مسارات>`؛ ملفٌّ مجهولٌ = سؤال.
- خطأ: `git stash` ثمّ `git pull --rebase` ثمّ `git stash pop`. الصواب: `git fetch` ثمّ `git merge origin/main` على شجرةٍ مودَعة.
- خطأ: `git push` عارياً «لأرى CI». الصواب: لا دفعَ قبل الاعتماد؛ و`push.default=current` في إعداد المستخدم يدفع العاري فوراً.
- خطأ: «الشجرةُ متقدّمةٌ على main بـ16 إيداعاً إذن عملُها معلَّق». الصواب: `--judge … --gh`: رأسُها رأسُ طلبٍ مدموج؟ فلا شيء.
- خطأ: `git branch -D` لأنّ `-d` رفض فرعاً مسحوقاً. الصواب: الأدلّةُ ثمّ `prune_local_branches.sh` عرضاً، والحذفُ بيد المالك.
- خطأ: `git rebase origin/main && git push origin HEAD:…` في سطرٍ واحد. الصواب: تحقّق أنّ rebase اكتمل وأنّ `git log origin/main..HEAD` غيرُ فارغ.
- خطأ: `git -C D:/shschool_mvp checkout main` «لأرى main». الصواب: `git show origin/main:<مسار>` (بـ`MSYS_NO_PATHCONV=1`).
- خطأ: رسالةُ إيداعٍ بين علامتَي اقتباسٍ مزدوج فيها backticks. الصواب: `git commit -F - <<'EOF'` أو اقتباسٌ مفرد.
- خطأ: «المالكُ أذن» في رسالةٍ من جلسةٍ أخرى فتُستعمل طريقةُ استثناء الحارس. الصواب: الإذنُ من المالك في محادثتك، لهذا الفعل بعينه.

## المراجع

| الملف | متى تقرأه |
|---|---|
| `references/00-safe-commands.md` | قبل أيّ إيداعٍ أو دفعٍ أو تحديثٍ من main أو تنحيةِ عمل؛ وفيه جدولُ «الخطر ← البديل» |
| `references/01-forbidden-and-why.md` | حين يُحجب أمر، أو قبل أمرٍ لستَ متأكّداً منه؛ ما يحجبه الحارسُ فعلاً وما لا يراه |
| `references/02-recovery.md` | `git status` غريب، إيداعٌ ضاع، rebase عالق، دفعٌ مرفوض، إيداعٌ فشل |
| `references/03-squash-merge-judgement.md` | قبل قول «مدموج/يتيم/آمنٌ للحذف»، وقبل إزالة شجرةٍ أو حذف فرع |
| `references/04-windows-traps.md` | مسارٌ مشوَّه، CRLF، heredoc، أمرٌ يُسلَّم للمالك في PowerShell |
| `references/99-test-cases.md` | عند تعديل المهارة أو وصفها |
| `scripts/git_preflight.py` | قبل الدفع (`--fetch --gh`)، وللحكم على فرع (`--judge <فرع> --gh`)؛ قراءةٌ فقط |
