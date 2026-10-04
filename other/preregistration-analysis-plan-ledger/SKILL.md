---
name: preregistration-analysis-plan-ledger
description: Use when a study needs a preregistration or a frozen analysis plan, when confirmatory and exploratory analyses must be separated, or when every deviation from the registered plan must be logged before the result is reported.
---

# Preregistration and Analysis Plan Ledger

## When to use

Use this skill when a quantitative or mixed-methods study requires its hypotheses, primary outcomes, exclusion criteria, and analysis plan to be written and frozen before any data are examined. It applies when a study will be submitted to a preregistration registry (OSF, AsPredicted, ClinicalTrials.gov, or a journal's registered-report track), when confirmatory and exploratory analyses must be labelled separately in the methods section, or when any deviation from the registered plan must be documented before the result is reported. It is not for writing a preregistration retrospectively after the data have already been examined, for changing the primary outcome variable to match a more favourable result, for hiding deviations in the methods section, or for presenting exploratory findings as if they were confirmatory.

## Inputs

- The research question, distinguishing the confirmatory hypothesis from any exploratory questions.
- The primary and secondary outcome variables.
- The inclusion and exclusion criteria, and the data-cleaning rules.
- The planned statistical test or model family, with the software and version.
- The target registry or registered-report track and its required fields.
- The timestamp or submission deadline.
- For agent-assisted analysis: the stage at which AI may be consulted and the boundary beyond which human judgment must take over.

## Workflow

1. Separate the research question into the confirmatory hypothesis — the pre-specified claim the study is powered to test — and any exploratory questions, which will be labelled as such throughout.
2. Freeze the primary outcome variable before any result file is opened; secondary outcomes follow.
3. Write the exclusion criteria and the data-cleaning decision rules explicitly, without reference to what the cleaned data look like.
4. State the planned test or model family, the software version, and the correction strategy for multiple comparisons if applicable.
5. Record the boundary for AI assistance: which analysis-preparation steps AI may support, and where the statistical judgment is the researcher's alone; route technical consultation to statistical-consultation-protocol.
6. Submit or timestamp the plan to the chosen registry before data collection or data unblinding begins.
7. During analysis, log every deviation from the plan in the deviation ledger with the date, the original plan entry, the change made, and the reason; treat the absence of a logged deviation as a claim that the plan was followed exactly.
8. In the final methods section, report the preregistration location, the deviation log, and the confirmatory-versus-exploratory labelling transparently.

## Output

Return:

- A preregistration draft in the field structure required by the target registry.
- A frozen analysis plan document naming the primary and secondary outcomes, the exclusion and data-cleaning rules, and the planned tests.
- A confirmatory-versus-exploratory label table mapping each analysis to its designation.
- A deviation ledger template with columns for date, plan entry, change, and reason — ready to receive entries during analysis.
- A methods-section passage that discloses the preregistration location and the deviation status accurately.
- What to record at session end: the registry submission URL or timestamp, the open decisions still awaiting the researcher's sign-off, and the handoff of the included dataset to open-science-release-packager and, where a systematic review is feeding the study, to prisma-scoping-review-pipeline.

## Verification

- The primary outcome variable was fixed before any result file was opened, not after.
- The exclusion and data-cleaning criteria were written without reference to the cleaned data.
- Every deviation from the plan has a dated entry in the deviation ledger.
- Exploratory analyses are labelled as such; none are reported as if they were pre-specified.
- Before closing: the preregistration document carries the registry timestamp or submission confirmation; statistical consultation for any non-standard test has been routed to statistical-consultation-protocol; and the deviation ledger has been reviewed by the researcher, not only by the AI.

## Safety

Preregistration constrains nothing except the label: an unregistered finding is still a finding, but it must be called exploratory. The danger is not deviation — deviation is normal and reportable — but undisclosed deviation, which converts an exploratory result into a false confirmatory claim. AI may draft the plan and the deviation log, but the researcher must examine and approve every entry before the ledger is closed, because a misclassified analysis can pass peer review and enter the literature as confirmed evidence. When the analysis requires methods beyond the skill's scope — power calculations, Bayesian priors, complex longitudinal models — route to statistical-consultation-protocol before the plan is finalised. When the study's data will be released alongside the paper, route to open-science-release-packager. When the study is a systematic review rather than a primary study, route to prisma-scoping-review-pipeline for the screening layer.

## Example prompt

"Bu araştırma için veri görülmeden önce ön kayıt ve analiz planı defteri oluştur. Hipotezi, birincil ve ikincil sonuç değişkenlerini, dışlama ölçütlerini, planlanan testi ve sapma günlüğü şablonunu ver."

Expected smoke output:

- A preregistration draft in OSF field format, with the confirmatory hypothesis and primary outcome clearly separated from the exploratory questions.
- A frozen analysis plan naming the exclusion criteria, data-cleaning rules, planned test, and software version.
- A deviation ledger template with date, plan entry, change, and reason columns, empty and ready for use during analysis.
- A methods-section disclosure paragraph stating the registry location and the obligation to update the deviation log before any result is reported.

## Türkçe kullanım notu

Bu beceri, araştırmacının analiz özgürlüğünü kısıtlamak için değil, veriye baktıktan sonra analiz niyetini unutmasını engellemek için tasarlanmıştır. Ön kayıt, doğrulayıcı hipotezi ve birincil sonuç değişkenini herhangi bir sonuç dosyası açılmadan önce sabitler. Dışlama ölçütleri ve veri temizleme kararları temizlenmiş veriye bakılmadan yazılır. Analiz sırasında plandan her ayrılış tarih, özgün plan maddesi, yapılan değişiklik ve gerekçesiyle sapma günlüğüne geçirilir. Belgelenmemiş sapma bir ihlale dönüşür. Açıkça kayıt altına alınan sapma ise yöntemsel dürüstlüğün doğal parçasıdır. Keşfedici analizler keşfedici olarak etiketlenir ve yöntem bölümünde bu etiketle yer alır. Yapay zekâ taslağı ve günlüğü hazırlayabilir, ancak araştırmacı her girdiyi gözden geçirir ve kapatmadan önce onaylar. Teknik istatistik danışmanlığı gereken durumlarda statistical-consultation-protocol devreye girer. Verinin makaleyle birlikte yayınlanacak olması halinde open-science-release-packager'a devir yapılır. Çalışma sistematik derleme üzerine inşa ediliyorsa arama katmanı prisma-scoping-review-pipeline'da kurulur.
