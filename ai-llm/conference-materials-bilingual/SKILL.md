---
name: conference-materials-bilingual
description: Use when building slides, a poster, or a lightning talk from a manuscript, when a presentation must exist in Turkish and English, or when conference visuals need a traceability check so every number on a slide matches the analysis behind it.
---

# Conference Materials Bilingual

## When to use

Use this skill when a study is heading to a conference and the manuscript must become slides, a poster, or a short talk, in one language or two. It assumes the scientific content already exists; the work here is selection, compression, visual integrity, and bilingual preparation. It is not for preparing public-facing communication beyond the academic venue; for that use public-scholarship-ethics-adapter, which handles broader audience framing and ethics considerations that differ from conference presentation norms.

## Inputs

- The source manuscript or the analysis outputs.
- The venue format and the hard time or size limit.
- The presentation language, and whether a second language version is needed.
- The verified reference list for the study.

## Workflow

1. Extract the one claim the audience must remember, and build the deck or poster around it. Material that does not serve that claim competes with it.
2. Budget content to the limit before designing anything, roughly one idea per slide minute for talks, and a single visual path for a poster.
3. Draw every figure from the real analysis outputs, and keep the trace: each chart names the analysis artifact it came from. A visual without underlying data does not go on a slide.
4. Prepare the second language by re-authoring from the same outline, as parallel slides or as speaker notes. Caption-by-caption translation produces the same calques as sentence-by-sentence translation in manuscripts.
5. Cite only from the verified reference list, and keep the citation slide short rather than complete.
6. Add the AI use disclosure where the venue requires one, in the venue's format.
7. Rehearse against the clock. When it does not fit, cut content and keep the speaking pace.

## Output

Return:

- The one-claim statement and the content budget.
- The slide or poster outline with the figure trace per visual.
- Both language versions when requested, built from the same outline.
- The citation slide from verified sources.
- A rehearsal cut list, what leaves first if time runs short.
- What to record at session end: the final outline file, the figure trace table, both language versions if produced, and the rehearsal timing result.

## Verification

- Every number and every chart on a slide traces to a named analysis artifact.
- No visual exists without underlying data.
- Both language versions assert identical claims, checked claim by claim.
- The deck fits the time limit in an actual rehearsal, with the timing recorded.
- The disclosure requirement of the venue was checked, and the statement is present where required.
- Before closing: every figure trace is written down, the rehearsal time is recorded, and if the work will be shared with a broader audience the handoff to public-scholarship-ethics-adapter is noted.

## Safety

A visual that flatters the data has no place on a slide, and participant material stays within what the paper's anonymization already allows. Conference compression pressures exaggeration, so claims on slides stay within what the manuscript defends.

## Example prompt

"Kongre için on dakikalık sunum hazırlıyorum, makaleden slaytları çıkar, Türkçe sunacağım ama İngilizce paralel set de gereksin."

Expected smoke output:

- A one-claim statement with a ten-minute content budget.
- An outline with figure traces to the analysis outputs.
- A bilingual preparation plan from the same outline, with a rehearsal cut list.

## Türkçe kullanım notu

Bu beceri, el yazmasını kongre malzemesine çevirirken bilimsel dürüstlüğü korur. Sunum tek bir hatırlanacak iddia etrafında kurulur, her grafik hangi analiz çıktısından geldiğini söyler, verisi olmayan görsel slayta giremez. İkinci dil sürümü başlık başlık çevrilerek değil aynı taslaktan yeniden yazılarak hazırlanır. Prova süreye karşı yapılır, sığmıyorsa konuşma hızı değil içerik kısılır.
