---
description: Revisione del codice scritto contro le regole presenti in .claude/rules/ del progetto. È un'integrazione del code review integrato, non un suo sostituto. Non modifica file. Si lancia solo su richiesta.
argument-hint: [percorso-o-branch]
disable-model-invocation: true
---

# Revisione del codice secondo le regole del progetto

Rispondi in italiano. Non modificare nessun file.

1. Leggi le regole del progetto in `.claude/rules/*.md` e il `CLAUDE.md` della radice (per le scelte specifiche del progetto). Se `.claude/rules/` manca, dillo e fermati.
2. Scegli il codice da rivedere, in sola lettura:
   - se è passato un argomento, usa quel percorso o quel branch (`git diff <base>...<branch>`);
   - altrimenti usa le modifiche non committate (`git diff` e `git diff --cached`); se non ci sono, usa l'ultimo commit (`git show --stat HEAD` e il suo diff).
3. Controlla il codice contro le regole applicabili ai file toccati. Per ogni problema riporta: file e riga, regola violata (file e sezione), gravità (bloccante, importante, suggerimento), e una riga su come correggerlo.
4. Segnala anche ciò che non si può verificare leggendo il codice (per esempio il comportamento a runtime): non segnarlo come problema.
5. Chiudi con il conteggio per gravità e con il giudizio: pronto, oppure da correggere prima del commit.
6. Non modificare file e non creare commit: le correzioni le decide l'utente.
