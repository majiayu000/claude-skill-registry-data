---
name: source-passport-ledger
description: Use when sources must stay traceable across sessions and years, when each reference needs a passport recording where it was found, how it was verified, and where it is cited, or when a draft needs a cited-but-unverified sweep before submission.
---

# Source Passport Ledger

## When to use

Use this skill when a project has outgrown a flat reference list and every source needs a documented life: discovery, verification, archiving, citation. The regional-access-workflow skill creates passport entries at discovery, and this skill maintains them as a ledger across the project's lifetime. Before submission it answers one question precisely: is anything cited that was never verified. It is not for screening sources by scope or inclusion criteria, that is prisma-scoping-review-pipeline, and it does not anonymize sensitive content embedded in sources, that is sensitive-data-anonymization-gate.

## Inputs

- The vault location where the ledger lives.
- Existing passport entries or the reference list to backfill from.
- The citation manager state, when one is in use.
- The drafts currently citing sources.

## Workflow

1. Keep one passport per source and one ledger that indexes them. The passport is plain text in the vault, tool agnostic and diffable.
2. Record in each passport: a stable identifier with DOI preferred, where and when the source was found, metadata status, the verification lane and date from apa-doi-verifier, the full text location, the reading note link, and every place the source is cited.
3. Update the passport at the lifecycle event itself, at discovery, at verification, at archiving, at citation. Reconstructing a ledger from memory at the end produces fiction.
4. Enforce the quarantine rule: a source whose passport lacks a verification entry is not citable in a release draft.
5. Sweep periodically and before every submission, listing cited-but-unverified and verified-but-uncited sources.
6. When a source's record changes, a retraction, a correction, a moved URL, append to the passport rather than overwriting its history.

## Output

Return:

- The passport template and the ledger index format.
- Backfilled passports for existing references, with gaps marked honestly.
- The quarantine list, sources cited without verification.
- The sweep report, cited-but-unverified and verified-but-uncited.
- What to record at session end: the updated ledger file path, the quarantine list as of this session, and a one-line note on any passport entries still awaiting verification.

## Verification

- Every citation in the current draft resolves to a passport with a verification entry.
- The quarantine list is empty before a submission, or the submission is flagged as blocked.
- Passport entries carry dates, and lifecycle events were recorded when they happened where the history shows it.
- Retractions and corrections appear as appended history, with the original record intact.
- Before closing: the quarantine list is empty or every remaining item is explicitly flagged as blocked, so the next session starts from a known state.

## Safety

Passports record metadata and locations, and they store full text only where the license permits storage. Unknown provenance stays recorded as unknown, since a guessed discovery story is a small fabrication. The ledger never substitutes for the citation manager's bibliography, it audits it.

## Example prompt

"Üç yıldır süren tez projemde kaynak listem dağıldı, pasaport defterini kur ve gönderim öncesi doğrulanmamış atıf taraması yap."

Expected smoke output:

- A passport template and ledger index proposal for the vault.
- A backfill plan for the existing reference list with honest gaps.
- A first sweep report with the quarantine list.

## Türkçe kullanım notu

Bu beceri, her kaynağa bir pasaport tutar, nerede bulundu, nasıl doğrulandı, nereye arşivlendi, hangi taslakta kullanıldı. Defter olay anında güncellenir, sonradan hafızadan kurmak kurgu üretir. Karantina kuralı serttir, doğrulama kaydı olmayan kaynak yayın taslağında atıf alamaz. Gönderim öncesi tarama iki listeyi çıkarır, doğrulanmadan atıf alanlar ve doğrulanıp hiç kullanılmayanlar.
