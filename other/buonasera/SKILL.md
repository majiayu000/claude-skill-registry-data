---
description: Salva lo stato dei lavori della giornata in PIANO.md e i nuovi problemi in CHECKLIST.md, così il giorno dopo /kit:buongiorno sa da dove ripartire. Non salva la conversazione. Si lancia solo su richiesta, a fine giornata.
disable-model-invocation: true
---

# Buonasera: salvataggio dello stato

Rispondi in italiano. Non committare nulla.

1. Leggi `PIANO.md` e `CHECKLIST.md` nella radice del repository. Se non c'è lavoro in corso (nessun `PIANO.md` e nessuna modifica non committata), non creare file: dillo e termina.
2. Priorità, per questo progetto: leggi in `~/.claude/kit-progetti.json` la voce del progetto (chiave: il percorso assoluto della radice del repository, con `/` al posto di `\`). Se la voce `priorita` manca, chiedi una sola domanda: vuoi gestire le priorità in questo progetto (sì/no)? Salva la risposta nella voce del progetto; crea il file se non esiste e aggiorna solo quella voce, senza toccare le altre.
3. Raccogli lo stato, in sola lettura: `git status --short`, `git log --oneline` dei commit di oggi, e l'esito dei test se li hai eseguiti oggi (altrimenti scrivi «non eseguiti»).
4. Aggiorna `PIANO.md`:
   - spunta solo i passi verificati (build e test dove si applicano);
   - aggiungi o sostituisci la sezione `## Ripartenza` con: data, passo in corso, ultimo passo completato, prossimo passo, decisioni aperte, file toccati oggi, test rotti;
   - se le priorità sono gestite, indicale accanto ai passi aperti.
5. Aggiorna `CHECKLIST.md` aggiungendo i problemi nuovi come voci `[ ]`. Non cancellare quelli esistenti.
6. In fondo alla risposta stampa il prompt da copiare nella sessione successiva, esattamente così: «Riprendi il lavoro: usa /kit:buongiorno».
