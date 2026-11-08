---
description: Riprende il lavoro del giorno precedente. Rilegge PIANO.md e CHECKLIST.md, riassume dove si è arrivati, cosa fare e le priorità, e propone il primo passo da cui ripartire. Si lancia solo su richiesta, all'inizio della giornata di lavoro.
disable-model-invocation: true
---

# Buongiorno: ripartenza

Non modificare nessun file. Rispondi in italiano.

1. Leggi `PIANO.md` e `CHECKLIST.md` nella radice del repository in cui sei. Se `PIANO.md` manca, dillo e chiedi una sola domanda: c'è un altro file di ripartenza, oppure si parte da zero?
2. Controlla lo stato di git in sola lettura: branch corrente (`git branch --show-current`) e modifiche non committate (`git status --short`). Se ci sono modifiche non committate, segnalale.
3. Controlla in `~/.claude/kit-progetti.json` (sulla macchina dell'utente) la voce di questo progetto, chiave `priorita`. Se è `true`, ordina i passi aperti per priorità come indicata in `PIANO.md`. Se è assente o `false`, usa l'ordine dei passi.
4. Riassumi in 3-4 righe: ultimo passo completato, passo in corso, prossimo passo, decisioni ancora aperte.
5. Proponi il primo passo da cui ripartire, con una riga di motivazione.
6. Fermati e attendi l'ok dell'utente. Non iniziare il passo senza il suo ok. Se hai dubbi su una scelta, fai una sola domanda.
